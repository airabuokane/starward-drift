"""旧版の音(アナログ風の減算シンセと合成ドラム)を、テンポ変化つきの秒単位で鳴らす"""
import numpy as np
from scipy.signal import butter,lfilter,sosfilt
FS=44100
rng=np.random.default_rng(11)
def _lp(x,fc,order=2):
    sos=butter(order,min(fc,FS*.45)/(FS/2),'low',output='sos');return sosfilt(sos,x)
def _hp(x,fc,order=2):
    sos=butter(order,fc/(FS/2),'high',output='sos');return sosfilt(sos,x)
def _delay(x,t,fb=.35,mix=.35):
    d=int(t*FS);y=x.copy()
    for k in range(1,6):
        g=fb**k
        if g<.02:break
        y[d*k:]+=x[:len(x)-d*k]*g*mix/fb
    return y
def mf(m):return 440.0*2**((m-69)/12)
def osc(kind,f,n,vib=0,duty=.5,det=0.0):
    t=np.arange(n)/FS;fr=f*(1+vib*np.sin(2*np.pi*5.5*t))*2**(det/1200);ph=np.cumsum(fr)/FS
    if kind=='saw':return 2*(ph%1)-1
    if kind=='sq':return np.where(ph%1<duty,1.0,-1.0)
    if kind=='tri':return 2*np.abs(2*(ph%1)-1)-1
    return np.sin(2*np.pi*ph)
def adsr(n,a,d,s,r,gl):
    e=np.zeros(n);A=max(1,int(a*FS));D=max(1,int(d*FS));R=max(1,int(r*FS));g=min(gl,n);i=np.arange(g)
    e[:g]=np.where(i<A,i/A,np.where(i<A+D,1-(1-s)*(i-A)/D,s))
    if g<n:lvl=e[g-1] if g>0 else 0;j=np.arange(n-g);e[g:]=lvl*np.maximum(0,1-j/R)
    return e
def synrender(evs,P,T):
    out=np.zeros(T);kind=P.get('kind','saw');det=P.get('det',(0,));cut=P.get('cut',2000);cenv=P.get('cenv',0)
    a,d,s_,r=P.get('a',.01),P.get('d',.15),P.get('sus',.6),P.get('r',.15)
    for st,du,p,v in evs:
        n=int((du+r*2+.05)*FS);gl=int(du*FS);f=mf(p)
        x=sum(osc(kind,f,n,vib=P.get('vib',0),duty=P.get('duty',.5),det=dd) for dd in det)/len(det)
        if P.get('sub'):x=x+P['sub']*osc('sin',f/2,n)
        if P.get('noise'):x=x+P['noise']*rng.standard_normal(n)
        fc=cut*(.6+.8*v/127)
        if cenv:
            env=np.exp(-np.arange(n)/FS/max(.03,P.get('cdec',.15)))
            x=_lp(x,fc)*(1-env*.5)+_lp(x,fc*(1+cenv))*(env*.5)
        else:x=_lp(x,fc)
        if P.get('dist'):x=np.tanh(x*P['dist']);x=_hp(_lp(x,P.get('cab',3600)),80)*.7
        x=x*adsr(n,a,d,s_,r,gl)*(v/127)**1.3
        i=int(st*FS);j=min(T,i+n)
        if i<T:out[i:j]+=x[:j-i]
    return out
def syndrums(evs,T):
    out=np.zeros(T)
    for st,du,p,v in evs:
        g=(v/127)**1.4;i=int(st*FS)
        if p==36:   # キック
            n=int(.3*FS);t=np.arange(n)/FS;fr=40+95*np.exp(-t*30);ph=np.cumsum(fr)/FS
            x=(np.sin(2*np.pi*ph)*np.exp(-t*8)+.25*np.sin(4*np.pi*ph)*np.exp(-t*25))*1.3
        elif p in(38,40,37):  # スネア(太め・残響は後段)
            n=int(.28*FS);t=np.arange(n)/FS;nz=_hp(rng.standard_normal(n),1200)*np.exp(-t*16)
            x=.6*nz+.5*np.sin(2*np.pi*185*t)*np.exp(-t*25)
            if p==37:x*=.35
        elif p==39:
            n=int(.22*FS);t=np.arange(n)/FS;x=_hp(rng.standard_normal(n),900)*(np.exp(-t*18)+.6*np.exp(-((t-.012)*80)**2))*.8
        elif p in(42,44,70,69):
            n=int(.06*FS);t=np.arange(n)/FS;x=_hp(rng.standard_normal(n),7000)*np.exp(-t*70)*.55
        elif p==46:
            n=int(.25*FS);t=np.arange(n)/FS;x=_hp(rng.standard_normal(n),6500)*np.exp(-t*13)*.5
        elif p in(49,57,55):
            n=int(1.8*FS);t=np.arange(n)/FS;x=_hp(rng.standard_normal(n),4500)*np.exp(-t*2.2)*.5
        elif p==51 or p==53:
            n=int(.5*FS);t=np.arange(n)/FS;x=(_hp(rng.standard_normal(n),5000)*.3+.3*np.sin(2*np.pi*3100*t))*np.exp(-t*7)
        elif 41<=p<=50:
            n=int(.35*FS);t=np.arange(n)/FS;f0=mf(p+12);fr=f0*(1+.6*np.exp(-t*22));ph=np.cumsum(fr)/FS;x=np.sin(2*np.pi*ph)*np.exp(-t*9)
        else:
            n=int(.1*FS);t=np.arange(n)/FS;x=_hp(rng.standard_normal(n),3000)*np.exp(-t*40)*.3
        j=min(T,i+n)
        if i<T:out[i:j]+=x[:j-i]*g
    return out
