"""テンポ変化・音量automation・ミックス階層付きの GM 曲レンダラ (GeneralUser GS)"""
import numpy as np,pretty_midi,subprocess,wave,re
from synthx import synrender,syndrums,_lp,_delay
from scipy.signal import fftconvolve
SF='/tmp/p7/music/sf/GeneralUser-GS.sf2'
FS=44100
NN={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def nm(s):
    m=re.match(r'([A-G])([#b]?)(-?\d)',s);return 12*(int(m.group(3))+1)+NN[m.group(1)]+{'#':1,'b':-1,'':0}[m.group(2)]
def S(txt,off=0,tr=0):
    """'E5:.5 r:1 A5:1' -> [(beat,dur,midi)]  ※ 'E5:.5!' でアクセント"""
    t=0;out=[]
    for tok in txt.split():
        p,d=tok.split(':');acc=d.endswith('!');d=float(d.rstrip('!'))
        if p!='r':out.append((off+t,d,nm(p)+tr,acc))
        t+=d
    return out,t
class Song:
    def __init__(s,bars,tempo,bpb=4):
        """tempo: dict bar->(bpm) または (bpm_start,bpm_end) でその小節間を直線変化"""
        s.bars=bars;s.ev={};s.cfg={};s.auto={};s.B=bpb;BP=bpb
        bpb=[];cur=120
        for b in range(bars):
            t=tempo.get(b)
            if t is not None:cur=t
            if isinstance(cur,tuple):a,z=cur;bpb.append([a+(z-a)*(i/BP) for i in range(BP)]);cur=z
            else:bpb.append([cur]*BP)
        s.bpm=[x for b in bpb for x in b]
        s.t=np.concatenate([[0],np.cumsum([60/x for x in s.bpm])])
    def sec(s,beat):
        i=int(np.clip(np.floor(beat),0,len(s.bpm)-1));return s.t[i]+(beat-i)*60/s.bpm[i]
    def stem(s,name,prog,db=0,rev=.15,pan=0,drum=False,cut=None,syn=None,lp=None,delay=None):
        s.cfg[name]=dict(prog=prog,db=db,rev=rev,pan=pan,drum=drum,cut=cut,syn=syn,lp=lp,delay=delay);s.ev.setdefault(name,[])
    def n(s,name,beat,dur,p,vel):
        j=np.random.uniform(-.004,.004);s.ev[name].append((max(0,s.sec(beat)+j),max(.05,s.sec(beat+dur)-s.sec(beat)),int(p),int(np.clip(vel+np.random.uniform(-4,4),1,127))))
    def d(s,beat,p,vel):s.n('drums',beat,.1,p,vel)
    def mel(s,name,L,vel,acc=14,leg=.92,tr=0):
        for b,dd,p,a in L:s.n(name,b,dd*leg,p+tr,vel+(acc if a else 0))
    def vol(s,name,pts):
        """pts: [(beat,dB),...] 直線補間"""
        out=[]
        for i,(b,g) in enumerate(pts):
            ramp=isinstance(g,str)
            g=float(g.lstrip('~')) if ramp else g
            if i and not ramp:out.append((b-.05,out[-1][1]))
            out.append((b,g))
        s.auto[name]=out
    def render(s,out,loop_beat=None,end_beat=None,peak_db=-1.0,target=-14.0,tail=0.0,mains=None,gap=3.0,secs=None):
        end_beat=end_beat or s.bars*s.B;L=int(s.sec(end_beat)*FS);T=L+int(5*FS)
        mixL=np.zeros(T);mixR=np.zeros(T);rv=np.zeros(T);X={}
        for name,evs in s.ev.items():
            if not evs:continue
            c=s.cfg[name]
            if c.get('syn')=='drums':x=syndrums(evs,T)
            elif c.get('syn'):x=synrender(evs,c['syn'],T)
            else:
                pm=pretty_midi.PrettyMIDI();ins=pretty_midi.Instrument(program=c['prog'],is_drum=c['drum'])
                for st,du,p,v in evs:ins.notes.append(pretty_midi.Note(velocity=v,pitch=p,start=st,end=st+du))
                pm.instruments.append(ins);x=pm.fluidsynth(fs=FS,sf2_path=SF)[:T]
                x=np.pad(x,(0,T-len(x)))
            if c.get('lp'):x=_lp(x,c['lp'])
            if c.get('delay'):x=_delay(x,*c['delay'])
            act=np.abs(x)>.02*np.max(np.abs(x)+1e-9);rm=np.sqrt(np.mean(x[act]**2))+1e-9
            x=x/rm*10**((-20+c['db'])/20)
            if c.get('pump'):
                # サイドチェイン風の揺れ(拍ごとに一瞬沈む)
                env=np.ones(T);dep=c['pump'];bt=s.t*FS;tau=.16*FS
                for k in range(len(bt)-1):
                    i0=int(bt[k]);i1=min(T,int(bt[k+1]))
                    if i0>=T:break
                    tt_=np.arange(i1-i0);env[i0:i1]=1-dep*np.exp(-tt_/tau)
                x=x*env
            if name in s.auto:
                pts=s.auto[name];tt=np.array([s.sec(b) for b,_ in pts])*FS;gg=np.array([g for _,g in pts])
                x*=10**(np.interp(np.arange(T),tt,gg)/20)
            X[name]=x
        s.boost=0.0
        if mains and secs:
            # 脇役を一律に動かし、主役との最小の差を gap dB にそろえる
            dB=lambda v:20*np.log10(np.sqrt(np.mean(v**2))+1e-12)
            gaps=[]
            allm=set(x for v in (mains.values() if isinstance(mains,dict) else [mains]) for x in v)
            for a0,b0,sn in secs:
                i,j=int(a0*FS),int(b0*FS);ms=mains.get(sn,[]) if isinstance(mains,dict) else mains
                ml=max([dB(X[m][i:j]) for m in ms if m in X]+[-200])
                if ml<-45:continue
                sl=max([dB(v[i:j]) for k,v in X.items() if k not in ms and k!='drums']+[-200])
                dl=dB(X['drums'][i:j]) if 'drums' in X else -200
                sl=max(sl,dl)
                if sl>-200:gaps.append(ml-sl)
            if gaps:
                s.boost=float(np.clip(np.median(gaps)-gap,-6,8))
                for k in X:
                    if k not in allm:X[k]=X[k]*10**(s.boost/20)
        for name,x in X.items():
            c=s.cfg[name]
            if getattr(s,'dbg',None) is not None:s.dbg[name]=x
            pl=np.cos((c['pan']+1)*np.pi/4);pr=np.sin((c['pan']+1)*np.pi/4)
            mixL+=x*pl*1.41;mixR+=x*pr*1.41;rv+=x*c['rev']
        rng=np.random.default_rng(3);n=int(1.8*FS);tt=np.arange(n)/FS
        for ch,(m,sd) in enumerate(((mixL,1),(mixR,2))):
            ir=np.random.default_rng(sd).standard_normal(n)*np.exp(-tt*3.6);ir[:int(.015*FS)]=0;ir/=np.sqrt(np.sum(ir**2))
            m+=fftconvolve(rv,ir)[:T]*.9
        st=np.stack([mixL,mixR],1)
        if loop_beat is not None:
            ls=int(s.sec(loop_beat)*FS);tail=st[L:];k=min(len(tail),L-ls);st2=st[:L].copy();st2[ls:ls+k]+=tail[:k];st=st2
        else:
            st=st[:L+int(tail*FS)]
            if tail:n_=int(min(tail,1.5)*FS);st[-n_:]*=np.linspace(1,0,n_)[:,None]
        m=st.mean(1);w=int(2*FS);rr=[np.sqrt(np.mean(m[i:i+w]**2)) for i in range(0,max(1,len(m)-w),w//2)]
        loud=np.percentile(rr,95)+1e-9;st=st*(10**(target/20)/loud)
        st=np.tanh(st*1.15)/np.tanh(1.15)
        pk=np.max(np.abs(st))+1e-9
        if pk>10**(peak_db/20):st=st/pk*10**(peak_db/20)
        pcm=(st*32767).astype('<i2')
        with wave.open(out+'.wav','wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(FS);w.writeframes(pcm.tobytes())
        subprocess.run(['ffmpeg','-y','-loglevel','error','-i',out+'.wav','-c:a','libmp3lame','-b:a','128k',out+'.mp3'])
        info=dict(len=L/FS,loop=(s.sec(loop_beat) if loop_beat is not None else 0),boost=s.boost)
        print(out,info);return info
