import sys,numpy as np
from synth import *
Q={'m':[0,3,7],'M':[0,4,7],'m7':[0,3,7,10],'M7':[0,4,7,11],'7':[0,4,7,10],'sus2':[0,2,7],'dim':[0,3,6],'m9':[0,3,7,10,14],'5':[0,7,12]}
def ch(root,q,oct_=0):return [root+i+12*oct_ for i in Q[q]]
def prog(m,P,bars_per=1):
    for i,(r,q) in enumerate(P):
        yield i*bars_per*m.beats,r,q
def pads(m,P,start,end,name='pad',vel=.5,cut=1600,kind='saw',a=.6,r=.8,oct_=1,det=(-9,0,9)):
    n=len(P)
    for b in range(start,end):
        r0,q=P[b%n];bt=b*m.beats
        for k in ch(r0+12,q,0)[:4]:
            m.note(name,bt,m.beats*1.0,k+12*(oct_-1),vel,kind=kind,cut=cut,a=a,d=.4,sus=.8,r=r,det=det)
def bassline(m,P,start,end,pat,vel=.8,cut=500,kind='saw',sub=.5,name='bass'):
    n=len(P)
    for b in range(start,end):
        r0,q=P[b%n];bt=b*m.beats
        for (off,dur,iv,v) in pat:
            m.note(name,bt+off,dur,r0+iv,vel*v,kind=kind,cut=cut,a=.004,d=.1,sus=.7,r=.06,sub=sub)
def arps(m,P,start,end,pattern,step=.5,name='arp',vel=.35,cut=3200,kind='sq',duty=.35,oct_=2,dur=.4,r=.1):
    n=len(P)
    for b in range(start,end):
        r0,q=P[b%n];bt=b*m.beats;c=ch(r0+12*oct_,q)+[r0+12*oct_+12]
        for i,idx in enumerate(pattern):
            if idx is None:continue
            m.note(name,bt+i*step,dur*step*2,c[idx%len(c)],vel*(1 if i%4==0 else .8),kind=kind,cut=cut,a=.003,d=.08,sus=.3,r=r,duty=duty)
def drums(m,start,end,kicks,snares,hats,openhats=(),claps=(),vk=.9,vs=.7,vh=.35,sw=0.0,hs=.5):
    for b in range(start,end):
        bt=b*m.beats
        for k in kicks:m.kick(bt+k,vk)
        for s_ in snares:m.snare(bt+s_,vs)
        for c_ in claps:m.clap(bt+c_,vs)
        for i in range(int(m.beats/hs)):
            off=i*hs;
            if sw and i%2==1:off+=hs*sw
            m.hat(bt+off,vh*(1 if i%2==0 else .6))
        for o in openhats:m.hat(bt+o,vh*1.3,True)
def lead(m,notes,name='lead',vel=.5,cut=3000,kind='sq',duty=.5,vib=.004,a=.01,d=.1,sus=.7,r=.15,det=(0,)):
    for bt,dur,mid in notes:
        if mid is None:continue
        m.note(name,bt,dur,mid,vel,kind=kind,cut=cut,a=a,d=d,sus=sus,r=r,vib=vib,duty=duty,det=det)
OUTD='/tmp/p7/music/out/'
import os;os.makedirs(OUTD,exist_ok=True)
def done(name,m,levels,rev,loop=True,fade=False):
    x=m.render(levels,rev=rev,loop=loop)
    save(OUTD+name,x,fade_end=fade);print(name,round(len(x)/OUT,1),'s')


# ---- cyberpunk rock helpers ----
def pc(m,name,bt,dur,root,vel=.5,cut=2600,oct_=0,third=None,a=.004,r=.08,sus=.8):
    ns=[root,root+7,root+12] if third is None else [root,root+third,root+7,root+12]
    for k in ns:
        m.note(name,bt,dur,k+12*oct_,vel,kind='saw',cut=cut,a=a,d=.1,sus=sus,r=r,det=(-7,7))
def pm(m,name,bt,root,vel=.5,oct_=1,dur=.2):
    m.note(name,bt,dur,root+12*oct_,vel,kind='saw',cut=1500,a=.002,d=.05,sus=.25,r=.03,det=(-6,6))
    m.note(name,bt,dur,root+7+12*oct_,vel*.8,kind='saw',cut=1500,a=.002,d=.05,sus=.25,r=.03,det=(-6,6))
def rows(m,P,start,end,fn):
    n=len(P)
    for b in range(start,end):fn(b,b*m.beats,*P[b%n])
def pmbar(m,P,start,end,pat,name='gtr',vel=.5,oct_=1):
    def f(b,bt,r,q):
        for (off,acc) in pat:pm(m,name,bt+off,r,vel*acc,oct_)
    rows(m,P,start,end,f)
def chords(m,P,start,end,name='pad',vel=.3,cut=1500,a=.5,r=.7,kind='saw'):
    pads(m,P,start,end,name=name,vel=vel,cut=cut,a=a,r=r,kind=kind)
def epch(m,P,start,end,name='ep',vel=.3,rolled=.06,beats=None):
    def f(b,bt,r,q):
        for i,k in enumerate(ch(r+24,q)):ep(m,name,bt+i*rolled,(beats or m.beats)*.95,k,vel)
    rows(m,P,start,end,f)
def plkarp(m,P,start,end,pat,name='pl',vel=.5,step=.5,oct_=2):
    def f(b,bt,r,q):
        c=ch(r+12*oct_,q)+[r+12*oct_+12]
        for i,ix in enumerate(pat):
            if ix is None:continue
            pluck(m,name,bt+i*step,step*1.8,c[ix%len(c)],vel*(1 if i%4==0 else .75),g=.995)
    rows(m,P,start,end,f)
def rockdr(m,start,end,k,sn,hs=.5,vk=.9,vs=.75,vh=.32,crash=None,fill=None):
    drums(m,start,end,k,sn,[],vk=vk,vs=vs,vh=vh,hs=hs)
    if crash:
        for b in range(start,end):
            if (b-start)%crash==0:m.hat(b*m.beats,vh*2.2,True)
    if fill:
        for b in range(start,end):
            if (b-start)%fill==fill-1:
                bt=b*m.beats
                for i,mm in enumerate([57,55,52,48]):m.tom(bt+3+i*.25,mm,.8)
def mel(m,notes,off=0,tr=0):
    return [(b+off,d,p+tr) for b,d,p in notes]

def title():
    m=Mix(24,84);P=[(40,'m'),(36,'M'),(43,'M'),(38,'M')]
    chords(m,P,0,24,vel=.3,cut=1300,a=.9,r=1.2)
    epch(m,P,0,8,vel=.28,rolled=.12)
    plkarp(m,P,0,8,[0,2,1,3,2,1,3,2],vel=.35,step=.5,oct_=2)
    bassline(m,P,8,24,[(0,1.8,0,.9),(2,.9,0,.7),(3,.9,7,.6)],cut=420,sub=.5)
    for b in range(8,24):
        bt=b*4;r_=P[b%4][0]
        pc(m,'gtr',bt,3.8,r_,.4,oct_=1,a=.01,r=.3)
    rockdr(m,8,24,[0,2.5],[1,3],vk=.8,vs=.6,vh=.25,crash=8)
    th=[(0,2,76),(2,1,79),(3,1,78),(4,3,76),(7,1,72),(8,2,74),(10,1,79),(11,1,83),(12,4,81),(16,2,79),(18,1,76),(19,1,79),(20,3,84),(23,1,83),(24,2,79),(26,1,74),(27,1,79),(28,4,78)]
    lead(m,mel(m,th,16*0+0)[:0]+[(b+4*8,d,p) for b,d,p in th],name='lead',vel=.38,cut=3200,kind='saw',vib=.006,a=.02,sus=.8,r=.25)
    lead(m,[(b+4*16,d,p) for b,d,p in th],name='lead',vel=.38,cut=3200,kind='saw',vib=.006,a=.02,sus=.8,r=.25)
    for b,d,p in th:m.note('bell',b+0.01,d*.5,p+12,.2,kind='sin',cut=5000,a=.003,d=.4,sus=0,r=.8)
    done('01_title',m,{'pad':{'g':.45,'rev':(2.5,.6)},'ep':{'g':.5,'rev':(1.8,.4)},'pl':{'g':.5,'delay':(.75,.4,.5),'rev':(1.5,.4)},'bass':.5,'gtr':{'g':.35,'dist':5,'rev':(1.2,.3)},'kick':.7,'snare':.45,'hat':.22,'lead':{'g':.45,'dist':4,'cab':4500,'delay':(.75,.35,.5),'rev':(1.8,.4)},'bell':{'g':.3,'rev':(2.0,.5)}},(2.2,.4))

def town():
    m=Mix(32,78);P=[(33,'m9'),(29,'M7'),(36,'M7'),(31,'M')]
    chords(m,P,0,32,vel=.3,cut=1200,a=.8,r=1.0)
    epch(m,P,0,32,vel=.3,rolled=.1)
    plkarp(m,P,0,32,[0,2,1,3,2,1,3,1],vel=.38,step=.5,oct_=2)
    bassline(m,P,8,32,[(0,1.4,0,.9),(1.5,.4,12,.5),(2,1,0,.8),(3.25,.5,7,.6)],cut=380,sub=.6)
    rockdr(m,8,32,[0,2.5],[3],hs=1,vk=.6,vs=.35,vh=.16)
    A=[(0,2,76),(2,1,74),(3,1,72),(4,3,69),(8,1,72),(9,1,74),(10,2,77),(12,3,76),(16,2,76),(18,1,79),(19,1,77),(20,3,76),(24,1,74),(25,1,72),(26,2,74),(28,4,71)]
    B=[(0,1.5,81),(1.5,.5,79),(2,2,76),(4,2,77),(6,2,76),(8,2,72),(10,1,76),(11,1,79),(12,4,76),(16,2,74),(18,1,76),(19,1,77),(20,4,79),(24,2,76),(26,1,74),(27,1,71),(28,4,69)]
    lead(m,mel(m,A,64),name='lead',vel=.33,cut=2600,kind='tri',vib=.005,a=.03,sus=.8,r=.3)
    lead(m,mel(m,B,96),name='lead',vel=.33,cut=2600,kind='tri',vib=.005,a=.03,sus=.8,r=.3)
    for b in range(16,24):pc(m,'gtr',b*4,3.9,P[b%4][0]+12 if False else P[b%4][0],.3,oct_=1,cut=1800,a=.05,r=.4)
    done('02_town',m,{'pad':{'g':.45,'rev':(2.5,.55)},'ep':{'g':.55,'rev':(1.8,.4)},'pl':{'g':.45,'delay':(.75,.4,.5),'rev':(1.5,.4)},'bass':.5,'kick':.6,'snare':.35,'hat':.18,'lead':{'g':.5,'delay':(.75,.4,.5),'rev':(2.0,.5)},'gtr':{'g':.28,'dist':2.2,'cab':2800,'rev':(1.5,.4)}},(2.2,.4))

def ship():
    m=Mix(24,72);P=[(36,'M7'),(33,'m9'),(29,'M7'),(31,'M')]
    chords(m,P,0,24,vel=.35,cut=1000,a=1.4,r=1.8)
    plkarp(m,P,0,24,[0,None,2,None,1,None,3,None],vel=.4,step=1,oct_=2)
    bassline(m,P,4,24,[(0,3.8,0,.7)],cut=260,sub=.8)
    rockdr(m,8,24,[0],[],hs=1,vk=.45,vh=.12)
    for b in range(8,24):
        if b%2==1:
            for i,p in enumerate([76,79,83,81]):pluck(m,'pl2',b*4+i*1.0,1.8,p,.35,g=.996)
    ms=[(0,3,79),(4,3,76),(8,3,77),(12,4,74)]
    for off in (64,80):lead(m,mel(m,ms,off),name='lead',vel=.28,cut=2200,kind='tri',vib=.006,a=.15,sus=.8,r=.8)
    done('03_ship',m,{'pad':{'g':.5,'rev':(3.0,.65)},'pl':{'g':.5,'delay':(.75,.45,.55),'rev':(2.0,.5)},'pl2':{'g':.35,'delay':(.75,.45,.55),'rev':(2.0,.5)},'bass':.45,'kick':.5,'hat':.15,'lead':{'g':.5,'delay':(.75,.4,.5),'rev':(2.5,.55)}},(3.0,.5))

def battle():
    m=Mix(24,152);P=[(40,'5'),(36,'5'),(38,'5'),(35,'5')]
    pmbar(m,P,0,24,[(0,1),(.5,.6),(1,.6),(1.5,.6),(2,.9),(2.5,.6),(3,.6),(3.5,.6)],vel=.5)
    bassline(m,P,0,24,[(0,.5,0,.9),(.5,.5,0,.6),(1,.5,0,.7),(1.5,.5,0,.6),(2,.5,0,.9),(2.5,.5,0,.6),(3,.5,12,.7),(3.5,.5,0,.6)],cut=500,sub=.4)
    rockdr(m,0,24,[0,1.5,2,3.5],[1,3],vk=.9,vs=.8,vh=.3,crash=4,fill=4)
    arps(m,P,8,24,[0,1,2,3,2,1,2,3],step=.5,vel=.14,cut=3500,duty=.3,oct_=3,dur=.5)
    M1=[(0,1,76),(1,.5,79),(1.5,.5,78),(2,2,76),(4,1,79),(5,.5,76),(5.5,.5,72),(6,2,76),(8,1,74),(9,.5,78),(9.5,.5,74),(10,2,78),(12,1,71),(13,1,75),(14,2,78),(16,1,76),(17,.5,79),(17.5,.5,83),(18,2,81),(20,1,79),(21,.5,76),(21.5,.5,79),(22,2,84),(24,1,83),(25,1,81),(26,2,78),(28,4,75)]
    lead(m,mel(m,M1,32),name='lead',vel=.38,cut=3200,kind='saw',vib=.005,a=.01,sus=.8,r=.1)
    lead(m,mel(m,M1,64),name='lead',vel=.38,cut=3200,kind='saw',vib=.005,a=.01,sus=.8,r=.1)
    lead(m,mel(m,M1,64,-12),name='lead2',vel=.3,cut=2800,kind='saw',vib=.005,a=.01,sus=.8,r=.1)
    for b in range(0,24,2):pc(m,'gtr2',b*4,.4,P[b%4][0],.45,oct_=1)
    done('04_battle',m,{'gtr':{'g':.4,'dist':6,'cab':3500},'gtr2':{'g':.3,'dist':6},'bass':.5,'kick':.85,'snare':.55,'hat':.25,'arp':{'g':.3,'delay':(.75,.35,.4)},'lead':{'g':.45,'dist':4,'cab':4500,'rev':(1.0,.3)},'lead2':{'g':.35,'dist':4,'rev':(1.0,.3)}},(1.2,.25))

def dungeon():
    m=Mix(24,108);P=[(38,'5'),(34,'5'),(31,'5'),(33,'5')]
    chords(m,P,0,24,vel=.3,cut=800,a=1.2,r=1.5)
    bassline(m,P,0,24,[(0,1.5,0,.9),(2,1,0,.8),(3,.5,-2,.6)],cut=300,sub=.8)
    pmbar(m,P,4,24,[(0,1),(.75,.6),(1.5,.6),(2,.8),(3,.6),(3.5,.6)],vel=.4,oct_=1)
    rockdr(m,8,24,[0,2.75],[2],hs=1,vk=.75,vs=.7,vh=.2,fill=8)
    for b in range(0,24,4):m.noise_sweep('sw',b*4+8,8,.2)
    for b in range(12,24,2):
        for i,p in enumerate([74,72,70,69]):pluck(m,'pl',b*4+i*2,2.2,p+12 if False else p,.3)
    done('05_dungeon',m,{'pad':{'g':.5,'rev':(2.8,.6)},'bass':.5,'gtr':{'g':.33,'dist':5,'cab':3000,'rev':(1.5,.4)},'kick':.75,'snare':.5,'hat':.18,'sw':{'g':.3,'rev':(2.0,.5)},'pl':{'g':.4,'delay':(.75,.45,.5),'rev':(2.5,.6)}},(2.5,.45))

def boss():
    m=Mix(24,164);P=[(33,'5'),(29,'5'),(31,'5'),(28,'5')]
    pmbar(m,P,0,24,[(i*.25,1 if i%4==0 else .55) for i in range(16)],vel=.45)
    bassline(m,P,0,24,[(i*.5,.45,0,1 if i%2==0 else .6) for i in range(8)],cut=550,sub=.4)
    rockdr(m,0,24,[0,.5,1.5,2,2.5,3.5],[1,3],vk=.9,vs=.85,vh=.28,crash=4,fill=4)
    arps(m,P,4,24,[0,1,2,3,0,1,2,3],step=.25,vel=.12,cut=4000,duty=.25,oct_=3,dur=.9)
    chords(m,P,8,24,vel=.3,cut=1800,a=.1,r=.3)
    M2=[(0,.5,81),(.5,.5,81),(1,1,84),(2,1,81),(3,1,80),(4,.5,77),(4.5,.5,77),(5,1,81),(6,1,77),(7,1,76),(8,.5,79),(8.5,.5,79),(9,1,83),(10,1,79),(11,1,78),(12,2,76),(14,2,80),(16,.5,81),(16.5,.5,84),(17,1,88),(18,1,84),(19,1,83),(20,1,81),(21,1,77),(22,2,81),(24,1,79),(25,1,83),(26,1,86),(27,1,83),(28,2,80),(30,2,76)]
    lead(m,mel(m,M2,32),name='lead',vel=.4,cut=3400,kind='saw',vib=.006,a=.01,sus=.8,r=.1)
    lead(m,mel(m,M2,64),name='lead',vel=.4,cut=3400,kind='saw',vib=.006,a=.01,sus=.8,r=.1)
    done('06_boss',m,{'gtr':{'g':.42,'dist':7,'cab':3500},'bass':.5,'kick':.9,'snare':.6,'hat':.26,'arp':{'g':.3,'delay':(.75,.3,.4)},'pad':{'g':.3,'dist':3},'lead':{'g':.45,'dist':4,'cab':4500,'rev':(1.0,.3)}},(1.1,.2))

def lastdungeon():
    m=Mix(48,140)
    P=[(38,'m'),(34,'M'),(41,'M'),(36,'M'),(38,'m'),(34,'M'),(31,'m'),(33,'M')]
    bass_roots=[38,34,29,36,38,34,31,33]
    def strs(a,b,vel,cut=2200):
        for bar in range(a,b):
            r0,q=P[bar%8];c=ch(r0+24,q)
            for i in range(16):
                m.note('str',bar*4+i*.25,.28,c[[0,1,2,1][i%4]],vel*(1 if i%4==0 else .7),kind='saw',cut=cut,a=.004,d=.05,sus=.6,r=.04,det=(-8,8))
    strs(0,48,.26)
    chords(m,P,0,48,vel=.28,cut=1500,a=.4,r=.8)
    for bar in range(0,48):
        r0,q=P[bar%8]
        for k in ch(r0+36,q)[:3]:voice(m,'choir',bar*4,4,k,.2,'choir',a=.4,r=.6)
    # ep intro arps
    epch(m,P,0,8,vel=.25,rolled=.15)
    # bass (from bar 8) 
    def bf(b,bt,*_):
        r0=bass_roots[b%8]
        for i in range(8):m.note('bass',bt+i*.5,.45,r0+(12 if i==7 else 0),.8*(1 if i%2==0 else .6),kind='saw',cut=520,a=.003,d=.08,sus=.7,r=.04,sub=.5)
    rows(m,P,8,48,bf)
    # guitar chug bars 8-16, 32-48
    for rg in ((8,16),(24,48)):
        pmbar(m,P,rg[0],rg[1],[(i*.5,1 if i%4==0 else .6) for i in range(8)],vel=.38,oct_=1)
    # drums
    rockdr(m,8,16,[0,2],[1,3],vk=.8,vs=.7,vh=.28,crash=4,fill=8)
    rockdr(m,16,24,[0,2.5],[2],hs=1,vk=.7,vs=.7,vh=.2,crash=8)
    rockdr(m,24,40,[0,.5,2,2.5],[1,3],vk=.9,vs=.85,vh=.3,crash=2,fill=4)
    rockdr(m,40,48,[0,2],[2],hs=1,vk=.6,vs=.6,vh=.15)
    for b in range(24,40):m.clap(b*4+1,.5);m.clap(b*4+3,.5)
    # theme
    T=[(0,1.5,74),(1.5,.5,77),(2,2,81),(4,1.5,82),(5.5,.5,81),(6,2,77),(8,1.5,77),(9.5,.5,81),(10,2,84),(12,1.5,84),(13.5,.5,79),(14,2,76),(16,1.5,77),(17.5,.5,81),(18,2,86),(20,1.5,84),(21.5,.5,82),(22,2,81),(24,1,79),(25,1,82),(26,2,86),(28,2,85),(30,2,81)]
    lead(m,mel(m,T,32),name='lead',vel=.38,cut=3300,kind='saw',vib=.007,a=.03,sus=.85,r=.2)           # bars 8-15 guitar
    for b,d,p in mel(m,T,64):voice(m,'brass',b,d*.97,p-12,.28,'brass',a=.05,r=.2,cut=2600,vib=.005)   # bars 16-23 brass (low) 
    for b,d,p in mel(m,T,96):
        voice(m,'brass',b,d*.97,p-12,.3,'brass',a=.05,r=.2,cut=2800,vib=.006)
        m.note('lead',b,d*.97,p,.38,kind='saw',cut=3600,a=.02,d=.1,sus=.85,r=.2,vib=.007,det=(-6,6))
    for b,d,p in mel(m,T,128):
        voice(m,'brass',b,d*.97,p-12,.3,'brass',a=.05,r=.2,cut=2800,vib=.006)
        m.note('lead',b,d*.97,p+12,.3,kind='saw',cut=4200,a=.02,d=.1,sus=.85,r=.2,vib=.007,det=(-6,6))
        m.note('lead',b,d*.97,p,.38,kind='saw',cut=3600,a=.02,d=.1,sus=.85,r=.2,vib=.007,det=(-6,6))
    # bridge (bars 16-23) ep melody a tenth below  + tom hits
    for b,d,p in mel(m,T,64,0):m.note('bell',b+.01,d*.6,p+12,.12,kind='sin',cut=5000,a=.003,d=.5,sus=0,r=1.0)
    for b in range(16,24,4):
        for i in range(4):m.tom(b*4+14+i*.5,50-i*2,.7)
    for b in range(40,48,4):m.noise_sweep('sw',b*4,16,.2)
    done('07_lastdungeon',m,{'str':{'g':.42,'rev':(2.0,.35)},'pad':{'g':.38,'rev':(2.5,.5)},'choir':{'g':.45,'rev':(3.0,.6)},'ep':{'g':.4,'rev':(2.0,.4)},'bass':.5,'gtr':{'g':.38,'dist':5,'cab':3500},'kick':.9,'snare':.6,'hat':.24,'lead':{'g':.45,'dist':3.5,'cab':4800,'delay':(.75,.25,.35),'rev':(1.8,.4)},'brass':{'g':.5,'rev':(2.0,.4)},'bell':{'g':.3,'rev':(2.5,.5)},'sw':{'g':.3}},(2.6,.45))


def lastboss():
    NB=68;m=Mix(NB,184)
    CHR=[(36,'m'),(32,'M'),(39,'M'),(34,'M'),(36,'m'),(32,'M'),(29,'m'),(31,'M')]
    PRE=[(29,'m'),(31,'M'),(29,'m'),(31,'M'),(32,'M'),(34,'M'),(31,'M'),(31,'M')]
    INT=[(36,'m'),(36,'m'),(32,'M'),(31,'M')]
    SEC=[('intro',0,4),('verse',4,16),('pre',20,8),('chorus',28,16),('bridge',44,8),('final',52,16)]
    def sec(bar):
        for n,a,l in SEC:
            if a<=bar<a+l:return n,bar-a
    def cp(bar):
        n,k=sec(bar)
        r,q={'intro':INT,'pre':PRE}.get(n,CHR)[k%(4 if n=='intro' else 8)]
        return r+(2 if n=='final' else 0),q
    def tr(bar):return 2 if sec(bar)[0]=='final' else 0
    def dyn(bar):
        n,k=sec(bar)
        return {'intro':.8,'verse':.72+.01*k,'pre':.82+.025*k,'chorus':1.0,'bridge':.55+.02*k,'final':1.0}[n]
    def each(a,b,fn):
        for bar in range(a,b):fn(bar,bar*4,*cp(bar))
    def bars(*names):return [b for b in range(NB) if sec(b)[0] in names]
    def eachs(names,fn):
        for bar in bars(*names):fn(bar,bar*4,*cp(bar))
    RH=('verse','pre','chorus','final')
    # ---- rhythm: タタタン x4 ----
    def strs(bar,bt,r,q):
        c=ch(r+24,q);D=dyn(bar);n=sec(bar)[0];base=.18 if n in('verse','pre') else .3
        for i in range(16):
            acc=1.0 if i%4==3 else (.65 if i%4==0 else .5)
            m.note('str',bt+i*.25,.2,c[[0,1,2,1][i%4]],base*acc*D,kind='saw')
    eachs(RH,strs)
    def bf(bar,bt,r,q):
        D=dyn(bar)
        for b in range(4):
            for off,du,acc in ((0,.2,.7),(.25,.2,.6),(.5,.2,.6),(.75,.24,1.0)):
                m.note('bass',bt+b+off,du,r+(12 if off==.75 else 0),.8*acc*D,kind='saw')
    eachs(RH,bf)
    def gf(bar,bt,r,q):
        D=dyn(bar);n=sec(bar)[0]
        for b in range(4):
            for off,acc in ((0,.7),(.25,.55),(.5,.55),(.75,1.0)):pm(m,'gtr',bt+b+off,r,.4*acc*D,1,dur=.2)
        if n in('chorus','final') and bar%2==0:pc(m,'gtr',bt,.9,r,.5*D,oct_=1)
    eachs(RH,gf)
    # ---- pads / choir / horn / brass / harp / timp ----
    def pd(bar,bt,r,q):
        for k in ch(r+12,q)[:3]:m.note('pad',bt,4,k,.3*dyn(bar),kind='saw',cut=1400,a=.5,d=.4,sus=.8,r=.8,det=(-9,0,9))
    each(0,NB,pd)
    def chp(bar,bt,r,q):
        D=dyn(bar);n=sec(bar)[0];v=.1 if n=='verse' else .2
        for k in ch(r+24,q)[:3]:
            voice(m,'choir',bt,4,k,v*D,'choir',a=.5,r=.6)
            if n!='verse':voice(m,'choir',bt,4,k+12,v*.55*D,'choir',a=.6,r=.6)
    each(0,NB,chp)
    def horn(bar,bt,r,q):
        for k in ch(r+12,q)[:3]:m.note('horn',bt,3.9,k,.3*dyn(bar),kind='saw')
    eachs(('pre','chorus','final','bridge'),horn)
    def stab(bar,bt,r,q):
        D=dyn(bar)
        for off,v in ((0,1),(.75,.8),(2.75,.8)):
            for k in ch(r+12,q)[:3]:m.note('brass',bt+off,.4,k,.3*v*D,kind='saw')
    eachs(('chorus','final'),stab)
    def harp(bar,bt,r,q):
        c=ch(r+36,q)+[r+48];D=dyn(bar)
        for i in range(8):m.note('harp',bt+i*.5,.5,c[[0,1,2,3,2,1,2,1][i]],.3*(1 if i%2==0 else .6)*D,kind='sin')
    eachs(('chorus','final','bridge'),harp)
    for bar in range(NB):
        n,k=sec(bar);r0=cp(bar)[0]+12;D=dyn(bar)
        m.note('timp',bar*4,.5,r0,.55*D,kind='sin')
        if n=='intro' or (n=='pre' and k>=6) or (bar+1<NB and sec(bar+1)[0] in('chorus','final','verse') and sec(bar+1)[1]==0) :
            for i in range(8):m.note('timp',bar*4+2+i*.25,.25,r0,(.2+.04*i)*D,kind='sin')
    for a,_,_ in [x for x in SEC if x[0] in('chorus','final','verse')]:
        pass
    for n,a,l in SEC:
        if n in('verse','chorus','final'):m.note('hit',a*4,.5,cp(a)[0]+24,.7,kind='sin')
    m.noise_sweep('sw',16*4+0,16,.25);m.noise_sweep('sw',20*4,32,.25);m.noise_sweep('sw',44*4+16,16,.25)
    # ---- drums: ドパ ----
    for bar in range(NB):
        n,k=sec(bar);bt=bar*4;D=dyn(bar)
        if n in('verse','pre','chorus','final'):
            ks=[0,1,2,3] if n!='final' and n!='chorus' else [0,1,1.75,2,3,3.75]
            for k_ in ks:m.kick(bt+k_,(1.0 if k_%1==0 else .7)*D)
            for s_ in (.5,1.5,2.5,3.5):m.snare(bt+s_,.95*D)
            for i in range(16):m.hat(bt+i*.25,(.34 if i%4==0 else .2)*D)
            if k==0:m.hat(bt,.75*D,True)
            if n=='pre' and k>=6:
                for i in range(8):m.snare(bt+i*.5,(.2+.1*(k-6)+.02*i)*D)
            if bar%4==3 and n!='pre':
                for i,mm in enumerate([57,55,52,48,46,44,42,40]):m.tom(bt+2.5+i*.1875,mm,(.5+.06*i)*D)
        elif n=='intro':
            if k>=2:
                for i in range(8):m.snare(bt+2+i*.25,(.25+.05*i)*D)
        elif n=='bridge':
            m.kick(bt,.6*D)
            if k%2==1:
                for i,mm in enumerate([52,50,48,46]):m.tom(bt+2+i*.5,mm,.5*D)
    # intro rising strings run
    for i,p in enumerate([48,51,55,60,63,67,72,75]):m.note('str',i*.5,.5,p+12,.25+.03*i,kind='saw')
    # ---- melodies ----
    VM=[(0,.5,72),(.5,.5,75),(1,.5,79),(1.5,.5,75),(2,1,77),(3,1,75),(4,.5,72),(4.5,.5,75),(5,.5,80),(5.5,.5,75),(6,1,79),(7,1,77),(8,.5,75),(8.5,.5,79),(9,.5,82),(9.5,.5,79),(10,1,79),(11,1,75),(12,.5,74),(12.5,.5,77),(13,.5,82),(13.5,.5,77),(14,2,74),(16,.5,72),(16.5,.5,75),(17,.5,79),(17.5,.5,84),(18,1,82),(19,1,79),(20,.5,80),(20.5,.5,77),(21,.5,75),(21.5,.5,77),(22,2,80),(24,.5,77),(24.5,.5,80),(25,.5,84),(25.5,.5,80),(26,1,77),(27,1,80),(28,1,79),(29,1,83),(30,2,86)]
    PM=[(0,4,80),(4,4,83),(8,4,84),(12,4,86),(16,4,87),(20,4,89),(24,8,91)]
    CM=[(0,1.5,79),(1.5,.5,77),(2,1,75),(3,1,79),(4,1.5,80),(5.5,.5,84),(6,2,80),(8,1.5,82),(9.5,.5,79),(10,1,75),(11,1,79),(12,1.5,82),(13.5,.5,86),(14,2,82),(16,1.5,84),(17.5,.5,82),(18,1,79),(19,1,84),(20,1.5,87),(21.5,.5,84),(22,2,80),(24,1,80),(25,1,84),(26,1,87),(27,1,84),(28,2,86),(30,2,83)]
    def place(L,bar0,tr_,fn):
        for b,d,p in L:fn(bar0*4+b,d,p+tr_,bar0+int(b//4))
    def gl(b,d,p,bar):m.note('lead',b,d*.95,p,.5*dyn(bar),kind='saw')
    def tp(b,d,p,bar):m.note('trp',b,d*.95,p,.42*dyn(bar),kind='saw')
    def br(b,d,p,bar):m.note('brass',b,d*.95,p-12,.4*dyn(bar),kind='saw')
    def hn(b,d,p,bar):m.note('horn',b,d*.95,p-12,.35*dyn(bar),kind='saw')
    def glk(b,d,p,bar):m.note('gl',b,d*.5,p+12,.3*dyn(bar),kind='sin')
    def chr_(b,d,p,bar):
        voice(m,'choir',b,d*.95,p,.32*dyn(bar),'choir',a=.08,r=.3)
        voice(m,'choir',b,d*.95,p-12,.24*dyn(bar),'choir',a=.08,r=.3)
    place(VM,4,0,gl);place(VM,12,0,lambda b,d,p,r:(gl(b,d,p,r),tp(b,d,p,r)))
    place(PM,20,0,lambda b,d,p,r:(tp(b,d,p,r),chr_(b,d,p,r),gl(b,d,p,r)))
    full=lambda t:(lambda b,d,p,r:(gl(b,d,p,r),gl(b,d,p+12,r),tp(b,d,p,r),br(b,d,p,r),hn(b,d,p,r),chr_(b,d,p,r),glk(b,d,p,r)))
    place(CM,28,0,full(0));place(CM,36,0,lambda b,d,p,r:(full(0)(b,d,p,r),tp(b,d,p+12,r)))
    for b,d,p in CM[:16]:
        chr_(44*4+b,d,p,44+int(b//4));voice(m,'str',44*4+b,d,p,.3*dyn(44+int(b//4)),'str')
    place(CM,52,2,lambda b,d,p,r:(full(0)(b,d,p,r),tp(b,d,p+12,r)))
    place(CM,60,2,lambda b,d,p,r:(full(0)(b,d,p,r),tp(b,d,p+12,r),gl(b,d,p+24,r)))
    done('11_lastboss',m,{'str':{'g':.42,'rev':(1.6,.3)},'pad':{'g':.3,'rev':(2.0,.45)},'choir':{'g':.5,'rev':(2.6,.55)},'bass':.5,'gtr':{'g':.4,'rev':(1.0,.2)},'lead':{'g':.45,'delay':(.75,.25,.3),'rev':(1.6,.35)},'brass':{'g':.5,'rev':(1.8,.35)},'sw':{'g':.3},'harp':{'g':.5,'rev':(1.8,.4)},'horn':{'g':.5,'rev':(2.0,.4)},'trp':{'g':.5,'rev':(1.8,.35)},'timp':{'g':.5,'rev':(1.8,.3)},'hit':{'g':.5,'rev':(2.0,.3)},'gl':{'g':.4,'rev':(2.0,.4)}},(2.0,.35))

def blackmarket():
    m=Mix(24,100);P=[(36,'m7'),(41,'7'),(36,'m7'),(43,'7')]
    bassline(m,P,0,24,[(0,.4,0,.9),(.75,.25,12,.6),(1.5,.4,0,.8),(2,.4,3,.7),(2.75,.25,0,.6),(3.5,.4,-2,.7)],cut=700,sub=.4)
    def st(b,bt,r,q):
        for off in (1,2.5,3.75):
            for k in ch(r+24,q)[:4]:m.note('stab',bt+off,.22,k,.25,kind='sq',duty=.3,cut=2800,a=.002,d=.05,sus=.2,r=.04)
    rows(m,P,4,24,st)
    rockdr(m,0,24,[0,1.75,2.5],[1,3],hs=.25,vk=.8,vs=.7,vh=.2)
    pmbar(m,P,8,24,[(0,1),(.75,.6),(1.5,.7),(2.25,.6),(3,.8),(3.75,.5)],vel=.28,oct_=1)
    L=[(0,.5,72),(.5,.5,75),(1,1,77),(2.5,.5,78),(3,1,79),(4,.5,82),(4.5,.5,79),(5,1,77),(6,2,75),(8,.5,72),(8.5,.5,75),(9,1,77),(10.5,.5,79),(11,.5,82),(12,2,79),(14,2,75)]
    lead(m,mel(m,L,48),name='lead',vel=.33,cut=2800,kind='sq',duty=.4,vib=.006,a=.01,sus=.7,r=.1)
    lead(m,mel(m,L,64),name='lead',vel=.33,cut=2800,kind='sq',duty=.4,vib=.006,a=.01,sus=.7,r=.1)
    lead(m,mel(m,L,80),name='lead',vel=.33,cut=2800,kind='sq',duty=.4,vib=.006,a=.01,sus=.7,r=.1)
    done('08_blackmarket',m,{'bass':.55,'stab':{'g':.4,'delay':(.75,.3,.4)},'kick':.8,'snare':.5,'hat':.2,'gtr':{'g':.3,'dist':3,'cab':3000},'lead':{'g':.45,'dist':2,'cab':4000,'delay':(.75,.3,.4),'rev':(1.2,.3)}},(1.4,.3))

def ending():
    m=Mix(48,96,tail=4.0);P=[(38,'M'),(33,'M'),(35,'m'),(31,'M')]
    P2=[(31,'M'),(33,'M'),(38,'M'),(35,'m')]
    def prg(b):return (P if b<32 else P2)[b%4]
    T1=[(0,1,78),(1,1,76),(2,2,74),(4,1,76),(5,1,73),(6,2,69),(8,1,71),(9,1,74),(10,2,78),(12,1,79),(13,1,78),(14,2,74)]
    T2=[(0,2,81),(2,1,78),(3,1,81),(4,2,80),(6,2,76),(8,2,78),(10,1,74),(11,1,71),(12,1,79),(13,1,83),(14,2,81)]
    def apply(a,b,fn):
        for bar in range(a,b):fn(bar,bar*4,*prg(bar))
    def banjo(bar,bt,r,q):
        c=ch(r+24,q)
        for i,ix in enumerate([0,2,1,2,0,2,1,2]):pluck(m,'banjo',bt+i*.5,.6,c[ix],.5-.1*(i%2),g=.99,bright=.9)
    apply(0,48-4,banjo)
    def gstr(bar,bt,r,q):
        for beat,dn in ((0,1),(1,0),(1.5,1),(2.5,0),(3,1)):
            for i,k in enumerate(ch(r+12,q)+[r+24]):pluck(m,'gtr',bt+beat+i*.02,1.2,k,.32,g=.996,bright=.7)
    apply(8,44,gstr)
    def bs(bar,bt,r,q):
        m.note('bass',bt,1.8,r,.8,kind='tri',cut=500,a=.01,d=.2,sus=.7,r=.1,sub=.3);m.note('bass',bt+2,1.8,r+(7 if bar%2 else 0),.7,kind='tri',cut=500,a=.01,d=.2,sus=.7,r=.1,sub=.3)
    apply(16,44,bs)
    # drums
    for bar in range(16,44):
        bt=bar*4
        if bar<24:m.kick(bt,.5);m.kick(bt+2,.45)
        else:
            m.kick(bt,.7);m.kick(bt+1.5,.45);m.kick(bt+2,.65)
        if bar>=20:m.snare(bt+1,.35 if bar<32 else .5);m.snare(bt+3,.35 if bar<32 else .5)
        if bar>=20:
            for i in range(8):m.hat(bt+i*.5,.18)
        if bar>=20:
            for beat in (1,3):m.clap(bt+beat,.3)
    # melody: harmonica (4-8 then returns), flute, whistle, voices
    def mm(T,bar0,name,kind,vel,tr=0,**kw):
        for b,d,p in T:voice(m,name,bar0*4+b,d*.95,p+tr,vel,kind,**kw)
    for bar0 in (4,8,12): mm(T1,bar0,'harm','harm',.3,a=.04,r=.2,vib=.006)
    for bar0 in (16,20): mm(T1,bar0,'flute','flute',.3,tr=12,a=.08,r=.2,vib=.006)
    for bar0 in (12,16,20): mm(T2,bar0,'whis','whistle',.25,tr=0,a=.06,r=.2,vib=.006)
    for bar0 in (24,28): mm(T1,bar0,'harm','harm',.3,a=.04,r=.2,vib=.006); mm(T1,bar0,'flute','flute',.3,tr=12,a=.08,r=.2)
    for bar0 in (32,36): 
        mm(T2,bar0,'harm','harm',.32,a=.04,r=.2,vib=.006); mm(T2,bar0,'flute','flute',.3,tr=12,a=.08,r=.2); mm(T2,bar0,'whis','whistle',.25,tr=-12,a=.06,r=.2)
        mm(T2,bar0,'choir','choir',.18,tr=-12,a=.2,r=.4)
    # pad/strings swell from 24, choir chords from 28
    for bar in range(24,44):
        r0,q=prg(bar)
        for k in ch(r0+24,q)[:3]:
            voice(m,'str',bar*4,4,k,.2,'str',a=.8,r=.8,cut=2000)
            if bar>=28:voice(m,'choir',bar*4,4,k+12,.14,'choir',a=.6,r=.8)
    # outro 44-47: final chord, soft melody fragment
    for k in (50,57,62,66,69):pluck(m,'gtr',44*4,6,k,.45,g=.997,bright=.7)
    for k in (62,66,69,74):voice(m,'str',44*4,12,k,.25,'str',a=1.0,r=2.5,cut=1800)
    for b,d,p in [(0,2,78),(2,2,76),(4,4,74)]:voice(m,'flute',44*4+4+b,d*.95,p+12,.28,'flute',a=.1,r=1.5)
    m.kick(44*4,.6)
    done('09_ending',m,{'banjo':{'g':.5,'rev':(1.5,.35)},'gtr':{'g':.45,'rev':(1.8,.4)},'bass':.5,'kick':.6,'snare':.35,'hat':.2,'harm':{'g':.5,'rev':(1.8,.4)},'flute':{'g':.5,'rev':(2.0,.45)},'whis':{'g':.4,'rev':(2.0,.45)},'str':{'g':.4,'rev':(2.5,.5)},'choir':{'g':.45,'rev':(3.0,.6)}},(2.8,.4),loop=False,fade=True)

def voyage():
    m=Mix(6,104)
    P=[(38,'m'),(34,'M'),(41,'M'),(33,'M')]
    chords(m,P,0,4,vel=.35,cut=1600,a=.1,r=.8)
    plkarp(m,P,0,4,[0,1,2,3,2,1,3,2],vel=.45,step=.5,oct_=2)
    bassline(m,P,1,4,[(0,3.8,0,.8)],cut=300,sub=.6)
    for b,d,p in [(0,2,74),(2,1,77),(3,1,81),(4,3,82),(8,2,81),(10,2,77),(12,4,86)]:
        m.note('lead',b,d*.95,p,.4,kind='saw',cut=3400,a=.02,d=.1,sus=.8,r=.4,vib=.006,det=(-6,6))
    for k in (50,57,62,65,69,74):pc(m,'gtr',16,5,k-12 if False else k-12,.35,oct_=0,a=.01,r=1.2) if k==50 else None
    m.kick(0,.7);m.kick(16,.7)
    done('10_voyage',m,{'pad':{'g':.45,'rev':(2.2,.5)},'pl':{'g':.5,'delay':(.75,.4,.5),'rev':(1.5,.4)},'bass':.5,'lead':{'g':.5,'dist':3,'cab':4500,'delay':(.75,.3,.4),'rev':(2.0,.5)},'gtr':{'g':.4,'dist':4,'rev':(2.0,.4)},'kick':.6},(2.4,.45),loop=False,fade=True)

if __name__=='__main__':
    for n in (sys.argv[1:] or ['title','town','ship','battle','dungeon','boss','lastdungeon','blackmarket','ending','voyage']):globals()[n]()
