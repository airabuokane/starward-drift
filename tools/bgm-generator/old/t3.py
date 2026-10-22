import sys,numpy as np,os
import t2
from t2 import *
import pretty_midi
SF=os.path.join(os.path.dirname(pretty_midi.__file__),'TimGM6mb.sf2')
COMMON={'gtr':30,'gtr2':30,'lead':29,'lead2':29,'bass':34,'str':48,'brass':61,'choir':52,'ep':4,'pl':27,'pl2':27}
GMCFG={
 'title':dict(COMMON),
 'town':dict(COMMON,bass=33,gtr=27,lead=27),
 'ship':dict(COMMON,bass=33,lead=27),
 'battle':dict(COMMON),'boss':dict(COMMON),'dungeon':dict(COMMON),
 'lastdungeon':dict(COMMON),'lastboss':dict(COMMON,harp=46,horn=60,trp=56,timp=47,hit=55,gl=9),
 'blackmarket':dict(COMMON,bass=36,gtr=28),
 'ending':dict(banjo=105,gtr=25,bass=33,harm=22,flute=73,whis=78,str=48,choir=52),
 'voyage':dict(COMMON,bass=33),
}
# role loudness (stem normalised to -24 dB RMS, then times this)
GMG={'gtr':1.1,'gtr2':.8,'lead':1.0,'lead2':.7,'bass':.9,'str':.8,'brass':.9,'choir':.9,'ep':.7,'pl':.8,'pl2':.6,'banjo':.8,'harm':.8,'flute':.8,'whis':.6,'drums':1.0,'harp':.8,'horn':.9,'trp':.9,'timp':1.0,'hit':.8,'gl':.5}
CUR=[None]
def mv(v):return int(np.clip(55+v*130,35,127))
class GMMix(Mix):
    def __init__(s,*a,**k):
        super().__init__(*a,**k);s.gm=GMCFG.get(CUR[0],{});s.ev={}
    def _ev(s,name,beat,dur,midi,vel):
        s.ev.setdefault(name,[]).append((beat,dur,int(midi),mv(vel)))
    def note(s,name,beat,dur,m,vel=1.0,**k):
        if name in s.gm:return s._ev(name,beat,dur,m,vel)
        return super().note(name,beat,dur,m,vel,**k)
    def _d(s,beat,midi,v):s.ev.setdefault('drums',[]).append((beat,0.1,midi,int(np.clip(40+v*85,30,127))))
    def kick(s,beat,v=1.0,**k):s._d(beat,36,v)
    def snare(s,beat,v=1.0,**k):s._d(beat,38,v)
    def clap(s,beat,v=1.0):s._d(beat,39,v)
    def hat(s,beat,v=1.0,open_=False):
        if open_ and v>=.5:s._d(beat,49,min(1,v*.8))
        else:s._d(beat,46 if open_ else 42,v)
    def tom(s,beat,m=50,v=1.0):s._d(beat,41 if m<=46 else 45 if m<=50 else 47 if m<=54 else 50,v)
    def render(s,levels,**k):
        lv=dict(levels);spb=s.spb
        for name,evs in s.ev.items():
            pm=pretty_midi.PrettyMIDI();prog=0 if name=='drums' else s.gm[name]
            ins=pretty_midi.Instrument(program=prog,is_drum=(name=='drums'))
            for b,d,p,v in evs:
                st=b*spb;ins.notes.append(pretty_midi.Note(velocity=v,pitch=p,start=st,end=st+max(.06,d*spb)))
            pm.instruments.append(ins)
            x=ins.fluidsynth(fs=SR,sf2_path=SF)
            act=np.abs(x)>0.02*np.max(np.abs(x)+1e-9);rm=np.sqrt(np.mean(x[act]**2))+1e-9
            x=x/rm*10**(-24/20)
            s.put(name,0,x,1.0)
            c=lv.get(name,{});c=dict(c) if isinstance(c,dict) else {}
            c.pop('dist',None);c.pop('cab',None);c['g']=c.get('G',GMG.get(name,.8))
            if name=='drums':c.pop('rev',None)
            lv[name]=c
        return super().render(lv,**k)
def gpluck(m,name,beat,dur,midi,vel=1.0,**k):
    if name in getattr(m,'gm',{}):return m._ev(name,beat,dur,midi,vel*.9)
    return _pl(m,name,beat,dur,midi,vel,**k)
def gvoice(m,name,beat,dur,midi,vel=.5,kind='choir',**k):
    if name in getattr(m,'gm',{}):return m._ev(name,beat,dur,midi,vel*1.4)
    return _vo(m,name,beat,dur,midi,vel,kind,**k)
def gep(m,name,beat,dur,midi,vel=.5):
    if name in getattr(m,'gm',{}):return m._ev(name,beat,dur,midi,vel*1.2)
    return _ep(m,name,beat,dur,midi,vel)
_pl,_vo,_ep=t2.pluck,t2.voice,t2.ep
t2.pluck,t2.voice,t2.ep,t2.Mix=gpluck,gvoice,gep,GMMix
t2.OUTD='/tmp/p7/music/out_gm/';os.makedirs(t2.OUTD,exist_ok=True)
def wrap(n):
    f=getattr(t2,n)
    def w():CUR[0]=n;f()
    return w
if __name__=='__main__':
    for n in (sys.argv[1:] or ['title','town','ship','battle','dungeon','boss','lastdungeon','blackmarket','ending','voyage','lastboss']):wrap(n)()
