import numpy as np
from scipy.signal import butter,lfilter,fftconvolve,resample_poly
SR=64000;OUT=32000
rng=np.random.default_rng(7)
def mf(m):return 440.0*2**((m-69)/12)
_bc={}
def lp(x,fc,order=2):
    fc=min(fc,SR/2*0.9);k=(round(fc),order)
    if k not in _bc:_bc[k]=butter(order,fc/(SR/2),'low')
    b,a=_bc[k];return lfilter(b,a,x)
def hp(x,fc):
    b,a=butter(2,fc/(SR/2),'high');return lfilter(b,a,x)
def adsr(n,a,d,s,r,gl):
    # gl: gate length in samples
    e=np.zeros(n);A=max(1,int(a*SR));D=max(1,int(d*SR));R=max(1,int(r*SR))
    g=min(gl,n)
    i=np.arange(g);e[:g]=np.where(i<A,i/A,np.where(i<A+D,1-(1-s)*(i-A)/D,s))
    if g<n:
        lvl=e[g-1] if g>0 else 0;j=np.arange(n-g);e[g:]=lvl*np.maximum(0,1-j/R)
    return e
def osc(kind,f,n,vib=0,vibr=5.5,duty=.5,det=0.0):
    t=np.arange(n)/SR
    fr=f*(1+vib*np.sin(2*np.pi*vibr*t))*2**(det/1200)
    ph=np.cumsum(fr)/SR
    if kind=='saw':return 2*(ph%1)-1
    if kind=='sq':return np.where(ph%1<duty,1.0,-1.0)
    if kind=='tri':return 2*np.abs(2*(ph%1)-1)-1
    return np.sin(2*np.pi*ph)
class Mix:
    def __init__(s,bars,bpm,beats=4,tail=2.0):
        s.bpm=bpm;s.spb=60.0/bpm;s.bars=bars;s.beats=beats
        s.len=int(bars*beats*s.spb*SR);s.tail=int(tail*SR)
        s.tr={}
    def buf(s,name):
        if name not in s.tr:s.tr[name]=np.zeros(s.len+s.tail+int(3*SR))
        return s.tr[name]
    def put(s,name,beat,x,g=1.0):
        b=s.buf(name);i=int(beat*s.spb*SR);j=min(len(b),i+len(x))
        if i<len(b):b[i:j]+=x[:j-i]*g
    def note(s,name,beat,dur,m,vel=1.0,kind='saw',cut=2000,a=.005,d=.15,sus=.6,r=.12,vib=0,duty=.5,det=(0,),sub=0.0,cenv=0.0):
        n=int((dur*s.spb+r*2+.05)*SR);gl=int(dur*s.spb*SR);f=mf(m)
        x=sum(osc(kind,f,n,vib=vib,duty=duty,det=dd) for dd in det)/len(det)
        if sub:x=x+sub*osc('sin',f/2,n)
        if cenv:
            xs=lp(x,cut*(1+cenv),2)*0.5+lp(x,cut,2)*0.5
        else: xs=lp(x,cut,2)
        s.put(name,beat,xs*adsr(n,a,d,sus,r,gl)*vel)
    # drums
    def kick(s,beat,v=1.0,f0=130,f1=42,dur=.28):
        n=int(dur*SR);t=np.arange(n)/SR;fr=f1+(f0-f1)*np.exp(-t*28);ph=np.cumsum(fr)/SR
        x=np.sin(2*np.pi*ph)*np.exp(-t*9)+0.3*np.sin(2*np.pi*ph*2)*np.exp(-t*20)
        s.put('kick',beat,x,v)
    def snare(s,beat,v=1.0,tone=190,dur=.22):
        n=int(dur*SR);t=np.arange(n)/SR
        nz=hp(rng.standard_normal(n),1400)*np.exp(-t*20)
        x=0.55*nz+0.45*np.sin(2*np.pi*tone*t)*np.exp(-t*28)
        s.put('snare',beat,x,v)
    def hat(s,beat,v=1.0,open_=False):
        d=.22 if open_ else .05;n=int(d*SR);t=np.arange(n)/SR
        x=hp(rng.standard_normal(n),6500)*np.exp(-t*(14 if open_ else 70))
        s.put('hat',beat,x,v)
    def clap(s,beat,v=1.0):
        n=int(.2*SR);t=np.arange(n)/SR
        x=hp(rng.standard_normal(n),900)*(np.exp(-t*18)+.6*np.exp(-((t-.012)*80)**2))
        s.put('snare',beat,x,v)
    def tom(s,beat,m=50,v=1.0):
        n=int(.3*SR);t=np.arange(n)/SR;fr=mf(m)*(1+.6*np.exp(-t*22));ph=np.cumsum(fr)/SR
        s.put('kick',beat,np.sin(2*np.pi*ph)*np.exp(-t*10),v)
    def noise_sweep(s,name,beat,dur,v=.3,up=True):
        n=int(dur*s.spb*SR);t=np.linspace(0,1,n);x=hp(rng.standard_normal(n),2500)*(t if up else 1-t)**2
        s.put(name,beat,x,v)
    def render(s,levels,rev=None,delay=None,loop=True,master=.9):
        total=np.zeros(s.len+s.tail+int(3*SR))
        for name,b in s.tr.items():
            x=b.copy();cfg=levels.get(name,{})
            g=cfg.get('g',.5) if isinstance(cfg,dict) else cfg
            if isinstance(cfg,dict):
                if cfg.get('dist'):
                    x=np.tanh(x*cfg['dist']);x=hp(lp(x,cfg.get('cab',3800),2),70)*0.6
                if cfg.get('hp'):x=hp(x,cfg['hp'])
                if cfg.get('lp'):x=lp(x,cfg['lp'])
                d=cfg.get('delay')
                if d:
                    dl=int(d[0]*s.spb*SR);fb=d[1];mx=d[2]
                    y=x.copy()
                    for k in range(1,6):
                        sh=dl*k
                        if sh<len(y):y[sh:]+=x[:len(y)-sh]*(fb**k)*mx
                    x=y
                rv=cfg.get('rev')
                if rv:
                    ir=make_ir(rv[0]);wet=fftconvolve(x,ir)[:len(x)];x=x*(1-rv[1]*.5)+wet*rv[1]
            total+=x*g
        if rev:
            ir=make_ir(rev[0]);wet=fftconvolve(total,ir)[:len(total)];total=total*(1-rev[1]*.4)+wet*rev[1]
        # fold tail
        L=s.len
        if loop:
            tl=total[L:L+s.tail+int(3*SR)]
            out=total[:L].copy();m=min(len(tl),L);out[:m]+=tl[:m]
        else:
            out=total[:L+s.tail]
        ref=np.percentile(np.abs(out),99.7)+1e-9;out=out/ref*0.9
        out=np.tanh(out*1.15)/np.tanh(1.15)
        tgt=10**(-14.5/20);rm=np.sqrt(np.mean(out**2))+1e-9;out=out*min(1.0,tgt/rm) if False else out*(tgt/rm)
        out=np.tanh(out*1.1)/np.tanh(1.1)
        pk=np.max(np.abs(out))+1e-9
        if pk>0.95:out=out/pk*0.95
        out=resample_poly(out,OUT,SR)
        return out.astype(np.float32)
_ir={}
def make_ir(sec):
    if sec in _ir:return _ir[sec]
    n=int(sec*SR);t=np.arange(n)/SR
    ir=rng.standard_normal(n)*np.exp(-t*(6.0/sec));ir=lp(ir,6000);ir[:int(.01*SR)]*=np.linspace(0,1,int(.01*SR))
    ir/=np.sqrt(np.sum(ir**2))*1.0;_ir[sec]=ir*3.5;return _ir[sec]
import wave,subprocess
def save(name,x,fade_end=False):
    if fade_end:
        n=int(.5*OUT);x=x.copy();x[-n:]*=np.linspace(1,0,n)
    pcm=(np.clip(x,-1,1)*32767).astype('<i2')
    with wave.open(f'{name}.wav','wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(OUT);w.writeframes(pcm.tobytes())
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'{name}.wav','-c:a','libmp3lame','-b:a','64k','-ac','1',f'{name}.mp3'])

from scipy.signal import butter as _b
def bp(x,lo,hi):
    b,a=_b(2,[lo/(SR/2),min(hi,SR/2*.9)/(SR/2)],'band');return lfilter(b,a,x)
def pluck(m,name,beat,dur,midi,vel=1.0,g=.996,bright=.6,rel=.15):
    f=mf(midi);N=max(2,int(SR/f));n=int((dur*m.spb+rel+.4)*SR)
    ex=rng.standard_normal(N);ex=lp(ex,bright*SR/2*.5+1500,1);x=np.zeros(n);x[:N]=ex
    a=np.zeros(N+2);a[0]=1;a[N]=-g*.5;a[N+1]=-g*.5
    y=lfilter([1.0],a,x)
    gl=int(dur*m.spb*SR);e=np.ones(n);R=int(rel*SR)
    if gl<n:
        j=np.arange(n-gl);e[gl:]=np.maximum(0,1-j/max(1,R))
    y=y*e;y/=np.max(np.abs(y))+1e-9
    m.put(name,beat,y,vel*.8)
def voice(m,name,beat,dur,midi,vel=.5,kind='choir',a=.25,r=.5,vib=.004,cut=3000,det=(-8,0,8)):
    n=int((dur*m.spb+r*2+.05)*SR);gl=int(dur*m.spb*SR);f=mf(midi)
    if kind=='choir':
        x=sum(osc('saw',f,n,vib=vib,det=d) for d in det)/len(det)
        x=bp(x,600,1000)*1.0+bp(x,1000,1600)*.7+bp(x,2200,3200)*.25
    elif kind=='flute':
        x=osc('sin',f,n,vib=vib)+.12*osc('sin',2*f,n)+.05*osc('sin',3*f,n)
        t=np.arange(n)/SR;x=x+bp(rng.standard_normal(n),2500,6000)*.06
        x=x*np.minimum(1,t/.15)
    elif kind=='whistle':
        x=osc('sin',f,n,vib=vib,vibr=5.0)+.04*osc('sin',2*f,n)
    elif kind=='harm':
        x=osc('sq',f,n,vib=vib,duty=.4)+.3*osc('saw',f,n,det=6)
        x=lp(x,2600,2)+bp(rng.standard_normal(n),1500,5000)*.05
    elif kind=='brass':
        x=sum(osc('saw',f,n,vib=vib,det=d) for d in det)/len(det);x=lp(x,cut,2)
    elif kind=='str':
        x=sum(osc('saw',f,n,vib=vib,vibr=5.5,det=d) for d in det)/len(det);x=lp(x,cut,2)
    else:
        x=osc('sin',f,n)
    m.put(name,beat,x*adsr(n,a,.2,.85,r,gl)*vel)
def ep(m,name,beat,dur,midi,vel=.5):
    n=int((dur*m.spb+.8)*SR);gl=int(dur*m.spb*SR);f=mf(midi);t=np.arange(n)/SR
    mod=np.sin(2*np.pi*f*t)*np.exp(-t*4)*.9
    x=np.sin(2*np.pi*f*t+mod*1.5)*np.exp(-t*1.6)+.25*np.sin(2*np.pi*f*2*t+mod)*np.exp(-t*3)
    e=adsr(n,.003,.3,1.0,.25,gl);m.put(name,beat,x*e*vel*.8)
