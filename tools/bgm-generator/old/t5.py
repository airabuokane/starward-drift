import sys,os,numpy as np
import t2,t3
from t3 import GMMix
from t4 import Q,vo,fold,E,Dr
t2.OUTD='/tmp/p7/music/out_extra/';os.makedirs(t2.OUTD,exist_ok=True)
SC={'major':[0,2,4,5,7,9,11],'minor':[0,2,3,5,7,8,10],'dorian':[0,2,3,5,7,9,10],'phryg':[0,1,3,5,7,8,10],'lydian':[0,2,4,6,7,9,11],'mixo':[0,2,4,5,7,9,10],'pmin':[0,3,5,7,10],'pmaj':[0,2,4,7,9],'hmin':[0,2,3,5,7,8,11],'dim':[0,2,3,5,6,8,9,11]}
Q.update({'6':[0,4,7,9],'m6':[0,3,7,9],'9':[0,4,7,10,14],'dim7':[0,3,6,9]})
RT={4:{'sparse':[[(0,2),(2,1),(3,1)],[(0,1.5),(1.5,.5),(2,2)],[(0,3),(3,1)],[(0,1),(1,1),(2,2)]],
 'mid':[[(0,1),(1,.5),(1.5,.5),(2,1),(3,1)],[(0,.5),(.5,.5),(1,1),(2,1.5),(3.5,.5)],[(0,1.5),(1.5,.5),(2,1),(3,1)],[(0,1),(1,1),(2,.5),(2.5,.5),(3,1)]],
 'busy':[[(i*.5,.5) for i in range(8)],[(0,.5),(.5,.5),(1,.5),(1.5,.5),(2,1),(3,.5),(3.5,.5)],[(0,.25),(.25,.25),(.5,.5),(1,.5),(1.5,.5),(2,1),(3,1)]]},
 3:{'sparse':[[(0,2),(2,1)],[(0,3)],[(0,1),(1,2)]],'mid':[[(0,1),(1,.5),(1.5,.5),(2,1)],[(0,1.5),(1.5,.5),(2,1)],[(0,1),(1,1),(2,1)]],'busy':[[(i*.5,.5) for i in range(6)]]},
 5:{'sparse':[[(0,3),(3,2)],[(0,2),(2,3)]],'mid':[[(0,2),(2,1),(3,1),(4,1)],[(0,1),(1,1),(2,1),(3,2)]],'busy':[[(i,1) for i in range(5)]]},
 6:{'sparse':[[(0,3),(3,3)],[(0,2),(2,1),(3,3)]],'mid':[[(0,2),(2,1),(3,2),(5,1)],[(0,1),(1,1),(2,1),(3,3)]],'busy':[[(i,1) for i in range(6)]]}}
def gen_mel(m,cfg,L):
    B=cfg['beats'];rnd=np.random.default_rng(L.get('seed',1));ton=cfg['ton'];sc=SC[cfg['scale']]
    lo,hi=L['lo'],L['hi'];pit=[p for p in range(lo,hi+1) if (p-ton)%12 in sc]
    tm=RT[B][L.get('style','mid')];motif=[tm[rnd.integers(len(tm))] for _ in range(4)]
    mid=(lo+hi)//2;amp=(hi-lo)/4;prev=min(pit,key=lambda p:abs(p-mid));sh=[0,3,-2,2]
    for bar in range(L['from'],L.get('to',cfg['bars'])):
        k=bar%4;ph=bar//4;off,kind=cfg['ch'][bar%len(cfg['ch'])];root=ton+off
        ct={(root+i)%12 for i in Q[kind]};tgt=mid+amp*np.sin(np.pi*(k+.5)/4)+sh[ph%4]
        for (o,du) in motif[k]:
            if o==0 or (o==B/2) or (bar%4==3 and o==motif[k][-1][0]):
                c=[p for p in pit if p%12 in ct];c.sort(key=lambda p:abs(p-tgt));p=c[int(rnd.integers(min(2,len(c))))]
            else:
                i0=pit.index(prev);w=np.array([1,2,2,1,2,2,1.0]);d=np.array([-2,-1,-1,0,1,1,2])
                w=w*(1+(np.sign(tgt-prev)*d>0)*1.5);w/=w.sum();i1=int(np.clip(i0+rnd.choice(d,p=w),0,len(pit)-1));p=pit[i1]
            prev=p;E(m,L['n'],bar*B+o,du*.95,p,L.get('vel',.55))
            if L.get('dbl'):E(m,L['n'],bar*B+o,du*.95,p+L['dbl'],L.get('vel',.55)*.7)
def drum(m,pr,bar,bt,B,v):
    D=lambda t,p,x:Dr(m,bt+t,p,x*v)
    if pr=='none':D(0,53,.18)
    elif pr=='waltz':D(0,36,.5);D(1,42,.25);D(2,42,.22);D(0,51,.2)
    elif pr=='six8':
        for t in (0,3):D(t,36,.7)
        for t in (1,2,4,5):D(t,37,.3)
        for t in range(6):D(t,54,.4 if t%3==0 else .22)
    elif pr=='five':
        D(0,36,.6);D(3,36,.5);D(2,37,.3)
        for t in range(5):D(t,42,.22)
    elif pr=='lofi':
        D(0,36,.7);D(1.75,36,.45);D(1,38,.5);D(3,38,.5)
        for i in range(8):D(i*.5,42,.28 if i%2==0 else .17)
    elif pr=='swing':
        for t in (0,1,1.667,2,3,3.667):D(t,51,.42 if t in(1,3) else .34)
        D(1,44,.3);D(3,44,.3);D(0,36,.38)
    elif pr=='rock':
        for t in (0,2,2.5):D(t,36,.9)
        D(1,38,.95);D(3,38,.95)
        for i in range(8):D(i*.5,46 if i%2 else 42,.4 if i%2==0 else .28)
        if bar%4==0:D(0,49,.8)
    elif pr=='dance':
        for t in range(4):D(t,36,.85)
        D(1,39,.7);D(3,39,.7)
        for i in range(4):D(i+.5,46 if i%2==0 else 42,.38)
    elif pr=='half':
        D(0,36,.9);D(2.75,36,.7);D(2,38,1.0)
        for i in range(8):D(i*.5,42,.27)
        if bar%4==3:D(3.5,45,.7)
    elif pr=='soft':
        D(0,36,.45);D(2,36,.3);D(3,37,.3)
        for t in range(4):D(t,42,.18)
    elif pr=='tribal':
        for t,x in ((0,1),(.75,.5),(1.5,.7),(2,.9),(3.25,.6),(3.5,.6)):D(t,41,x*.8)
        for t in (.5,2.5):D(t,63,.45)
        for i in range(8):D(i*.5,70,.28 if i%2 else .38)
    elif pr=='latin':
        for t in ((0,1.5,3) if bar%2==0 else (1,2)):D(t,75,.35)
        for t in (1.5,2.5,3.5):D(t,64 if t==2.5 else 62,.4)
        D(0,36,.45);D(2,36,.35)
        for i in range(8):D(i*.5,70,.25)
    elif pr=='march':
        for t in (0,.5,1,1.5,2,2.5,3,3.25,3.5,3.75):D(t,38,.55 if t%1==0 else .38)
        D(0,36,.8);D(2,36,.7)
        if bar%4==0:D(0,49,.7)
    elif pr=='brush':
        D(1,44,.3);D(3,44,.3);D(1,37,.2);D(3,37,.2);D(0,36,.3)
    elif pr=='dub':
        D(0,36,.9);D(2.5,36,.7);D(2,38,.85);D(1.5,42,.2);D(3.5,42,.2)
def bassp(m,L,cfg,bar,bt,root,kind,nroot):
    B=cfg['beats'];n=L['n'];v=L.get('vel',.65);r=fold(root,L.get('lo',28),L.get('hi',43));pt=L['pat']
    if pt=='drone':E(m,n,bt,B*.98,r,v)
    elif pt=='root4':
        for t in range(int(B)):E(m,n,bt+t,.9,r,v)
    elif pt=='root8':
        for i in range(int(B*2)):E(m,n,bt+i*.5,.45,r,v if i%2==0 else v*.75)
    elif pt=='oct8':
        for i in range(int(B*2)):E(m,n,bt+i*.5,.45,r+(12 if i%2 else 0),v if i%2==0 else v*.7)
    elif pt=='half':
        E(m,n,bt,B/2-.1,r,v);E(m,n,bt+B/2,B/2-.1,r+7 if bar%2 else r,v*.85)
    elif pt=='walk':
        nb=fold(nroot,L.get('lo',28),L.get('hi',43))
        for i,p in enumerate([r,r+7,r+(3 if 'm' in kind and kind!='M7' else 4),nb-1]):E(m,n,bt+i,.9,p,v)
    elif pt=='pulse16':
        for i in range(int(B*4)):E(m,n,bt+i*.25,.22,r+(12 if i%8==7 else 0),v if i%4==0 else v*.65)
    elif pt=='syncop':
        for t,du in ((0,1.2),(1.5,.5),(2.5,.5),(3.25,.6)):
            if t<B:E(m,n,bt+t,du,r,v)
    elif pt=='oompah':
        E(m,n,bt,2,r,v);E(m,n,bt+3,2,r+7,v*.9)
    elif pt=='waltz':
        E(m,n,bt,1.8,r,v);E(m,n,bt+2,.9,r+7,v*.7)
def chordv(root,kind,lo,n=4):return vo(root,kind,lo)[:n]
def build(cfg):
    B=cfg['beats'];bars=cfg['bars'];m=GMMix(bars,cfg['bpm'],beats=B,tail=cfg.get('tail',2.0));m.gm={};lv={}
    ton=cfg['ton']
    for L in cfg['layers']:
        if L['t']!='drums':
            m.gm[L['n']]=L['prog'];lv[L['n']]={'G':L.get('G',.8),'rev':L.get('rev',(2.0,.35))}
            if L.get('delay'):lv[L['n']]['delay']=L['delay']
    for bar in range(bars):
        bt=bar*B;off,kind=cfg['ch'][bar%len(cfg['ch'])];root=ton+off;noff,_=cfg['ch'][(bar+1)%len(cfg['ch'])];nroot=ton+noff
        for L in cfg['layers']:
            if not (L.get('from',0)<=bar<L.get('to',bars)):continue
            t=L['t']
            if t=='pad':
                for p in chordv(root+12*L.get('oct',0),kind,L.get('lo',55),L.get('k',4)):E(m,L['n'],bt,B*.98,p,L.get('vel',.34))
            elif t=='arp':
                c=vo(root+12*L.get('oct',0),kind,L.get('lo',60));c=c+[c[0]+12];st=L.get('step',.5)
                for i in range(int(B/st)):E(m,L['n'],bt+i*st,st*L.get('len',1.8),c[L['pat'][i%len(L['pat'])]%len(c)],L.get('vel',.34)*(1 if i%4==0 else .78))
            elif t=='bass':bassp(m,L,cfg,bar,bt,root,kind,nroot)
            elif t=='comp':
                for o,du in L['rh']:
                    if o<B:
                        for p in chordv(root,kind,L.get('lo',55),L.get('k',4)):E(m,L['n'],bt+o,du,p,L.get('vel',.4))
            elif t=='drums':drum(m,L['pr'],bar,bt,B,L.get('v',1.0))
            elif t=='hit' and bar%L.get('every',4)==0:E(m,L['n'],bt,.5,fold(root+12*L.get('oct',1),40,84),L.get('vel',.5))
    for L in cfg['layers']:
        if L['t']=='mel':gen_mel(m,cfg,L)
    if any(L['t']=='hit' for L in cfg['layers']):
        for L in cfg['layers']:
            if L['t']=='hit':m.gm[L['n']]=L['prog'];lv[L['n']]={'G':L.get('G',.6),'rev':(2.0,.4)}
    t2.done(cfg['name'],m,lv,cfg.get('rev',(2.0,.35)),loop=cfg.get('loop',True),fade=not cfg.get('loop',True))
def P(n,t,prog,**k):d=dict(n=n,t=t,prog=prog);d.update(k);return d
def Dm(pr,**k):d=dict(n='drums',t='drums',pr=pr);d.update(k);return d
def mk(name,bpm,beats,secs,ton,scale,ch,layers,**kw):
    bars=max(8,int(round(secs*bpm/60/beats/4))*4)
    c=dict(name=name,bpm=bpm,beats=beats,bars=bars,ton=ton,scale=scale,ch=ch,layers=layers);c.update(kw);return c
M=lambda n,prog,fr,lo,hi,**k:P(n,'mel',prog,**dict(dict(**{'from':fr}),lo=lo,hi=hi,**k))
CF={}
# ---------- city kinds ----------
CF['16_casino']=mk('16_casino',132,4,80,48,'major',[(0,'6'),(9,'7'),(2,'m7'),(7,'7')],[
 P('pn','comp',0,rh=[(0,1.5),(2.667,1)],lo=57,vel=.4,G=.7),P('bs','bass',32,pat='walk',lo=34,hi=47,vel=.62),Dm('swing'),
 P('br','pad',61,**{'from':8,'oct':0,'lo':55,'vel':.3,'k':3,'G':.6}),M('tp',56,8,70,88,seed=11,style='mid',vel=.6,dbl=0),M('vb',11,16,72,90,seed=12,style='busy',vel=.4)])
CF['17_corp']=mk('17_corp',100,4,80,38,'dorian',[(0,'m9'),(8,'M7'),(5,'m9'),(7,'sus4')],[
 P('pd','pad',89,lo=55,vel=.34,G=.7),P('bs','bass',38,pat='root8',vel=.55,**{'from':4}),P('ar','arp',80,pat=[0,2,1,3,2,1,3,2],step=.5,lo=64,vel=.26,**{'from':4}),Dm('half',**{'from':8}),M('gl',98,8,72,92,seed=21,style='sparse',vel=.5),M('ep',4,16,64,84,seed=22,style='mid',vel=.4)])
CF['18_resort']=mk('18_resort',100,4,80,43,'major',[(0,'M7'),(9,'7'),(2,'m7'),(7,'7')],[
 P('ng','arp',24,pat=[0,1,2,3,2,1,2,1],step=.5,lo=57,vel=.4,len=1.6),P('bs','bass',32,pat='half',vel=.6,**{'from':2}),Dm('latin',**{'from':4}),M('mr',12,8,72,88,seed=31,style='mid',vel=.5),M('fl',73,16,76,92,seed=32,style='sparse',vel=.45)])
CF['19_terminal']=mk('19_terminal',112,4,80,40,'dorian',[(0,'m7'),(5,'7'),(10,'M7'),(3,'M7')],[
 P('cl','comp',7,rh=[(0,.4),(.75,.3),(1.5,.4),(2.5,.3),(3.25,.4)],lo=55,k=3,vel=.4),P('bs','bass',36,pat='syncop',vel=.65),Dm('rock'),P('pd','pad',89,lo=57,vel=.22,**{'from':8}),M('ld',81,8,70,90,seed=41,style='mid',vel=.5),M('ho',56,16,64,84,seed=42,style='sparse',vel=.4)])
CF['20_frontier']=mk('20_frontier',76,4,80,45,'minor',[(0,'m'),(10,'M'),(8,'M'),(7,'M')],[
 P('sg','arp',25,pat=[0,1,2,1,0,2,1,2],step=.5,lo=52,vel=.4,len=2.0),P('bs','bass',32,pat='half',vel=.55,**{'from':4}),Dm('brush',**{'from':8}),M('hm',22,4,69,86,seed=51,style='sparse',vel=.55),P('pd','pad',48,lo=52,vel=.2,**{'from':12})])
CF['21_mining']=mk('21_mining',90,4,75,40,'phryg',[(0,'5'),(8,'5'),(10,'5'),(0,'5')],[
 P('gt','arp',30,pat=[0,0,2,0,0,2,0,2],step=.5,lo=40,vel=.55,len=.8),P('bs','bass',38,pat='root8',vel=.65),Dm('tribal',**{'from':2}),P('hr','hit',55,every=8,G=.6),M('tb',57,8,43,64,seed=61,style='sparse',vel=.6)])
CF['22_lab']=mk('22_lab',118,4,75,36,'lydian',[(0,'M7'),(2,'M7'),(9,'m7'),(7,'sus4')],[
 P('vb','arp',11,pat=[0,2,1,3,2,3,1,2],step=.25,lo=64,vel=.3,len=1.2),P('pd','pad',103,lo=55,vel=.3,G=.7),P('bs','bass',38,pat='pulse16',vel=.5,**{'from':4}),Dm('dance',v=.7,**{'from':8}),M('gl',98,8,76,96,seed=71,style='sparse',vel=.5)])
CF['23_farm']=mk('23_farm',90,4,80,43,'major',[(0,'M'),(9,'m'),(5,'M'),(7,'M')],[
 P('ag','arp',25,pat=[0,2,1,2,0,2,1,2],step=.5,lo=55,vel=.4,len=2.0),P('bs','bass',32,pat='half',vel=.55,**{'from':4}),Dm('brush',**{'from':8}),M('fl',73,4,72,90,seed=81,style='sparse',vel=.55),M('cl',71,16,64,82,seed=82,style='mid',vel=.4)])
CF['24_shipyard']=mk('24_shipyard',108,4,75,38,'minor',[(0,'m'),(8,'M'),(10,'M'),(0,'m')],[
 P('br','comp',61,rh=[(0,.5),(1.5,.4),(2,.5)],lo=50,k=3,vel=.4,**{'from':4}),P('tb','bass',58,pat='root4',vel=.7),Dm('march'),P('st','arp',45,pat=[0,1,2,1],step=.5,lo=57,vel=.3,**{'from':8}),M('tp',56,8,70,86,seed=91,style='mid',vel=.6),M('hn',60,16,58,76,seed=92,style='sparse',vel=.45)])
CF['25_residential']=mk('25_residential',92,4,80,36,'major',[(0,'M'),(7,'M'),(9,'m'),(5,'M')],[
 P('ep','comp',4,rh=[(0,1.5),(2,1.5)],lo=55,vel=.4),P('ag','arp',24,pat=[0,2,1,2],step=1,lo=60,vel=.3,len=2.0,**{'from':4}),P('bs','bass',33,pat='half',vel=.55,**{'from':4}),Dm('lofi',**{'from':8}),M('gk',9,8,76,94,seed=101,style='mid',vel=.5)])
CF['26_oldresort']=mk('26_oldresort',72,3,80,38,'minor',[(0,'m'),(8,'M'),(5,'m'),(7,'7')],[
 P('pn','arp',0,pat=[0,1,2],step=1,lo=52,vel=.4,len=2.5),P('bs','bass',32,pat='waltz',vel=.55,**{'from':4}),Dm('waltz',v=.7,**{'from':8}),M('ac',21,4,64,82,seed=111,style='mid',vel=.5),M('tp',59,16,70,86,seed=112,style='sparse',vel=.4)])
# ---------- dungeons ----------
CF['27_dg1_cistern']=mk('27_dg1_cistern',70,4,75,38,'minor',[(0,'m'),(1,'M'),(0,'m'),(6,'dim')],[
 P('vx','pad',91,lo=50,vel=.3,G=.7),P('bs','bass',39,pat='drone',vel=.55),P('cl','arp',8,pat=[0,None] if False else [0,3,1,3],step=2,lo=76,vel=.3,len=1.5,delay=(1,.5,.5)),Dm('none',**{'from':4}),P('tm','hit',47,every=4,oct=0,**{'from':0}),M('mr',12,8,72,90,seed=121,style='sparse',vel=.38)])
CF['28_dg2_tunnel']=mk('28_dg2_tunnel',84,4,70,35,'phryg',[(0,'5'),(1,'5'),(0,'5'),(10,'5')],[
 P('gt','arp',30,pat=[0,0,2,0,0,0,2,0],step=.5,lo=35,vel=.6,len=.8),P('bs','bass',38,pat='syncop',vel=.65),Dm('tribal',v=.9),P('hr','hit',55,every=8,G=.5),P('st','pad',48,lo=47,vel=.25,k=3,**{'from':4})])
CF['29_dg3_frozen']=mk('29_dg3_frozen',66,4,75,33,'minor',[(0,'m'),(8,'M7'),(5,'m'),(7,'M')],[
 P('pn','arp',0,pat=[0,2,1,3,2,1],step=.667,lo=57,vel=.32,len=2.0),P('hl','pad',94,lo=60,vel=.3,G=.7),P('cr','pad',98,lo=72,vel=.25,k=2,**{'from':4}),M('ce',8,8,80,96,seed=131,style='sparse',vel=.5),P('vc','bass',42,pat='drone',vel=.5,**{'from':8})])
CF['30_dg4_bunker']=mk('30_dg4_bunker',100,4,70,41,'minor',[(0,'m'),(8,'M'),(10,'M'),(7,'M')],[
 P('pz','arp',45,pat=[0,0,2,0,1,0,2,0],step=.5,lo=48,vel=.4,len=.6),P('tb','bass',57,pat='root4',vel=.65),Dm('march'),P('ti','hit',47,every=2,oct=0,G=.7),P('hr','hit',61,every=8,oct=1,G=.5)])
CF['31_dg5_cathedral']=mk('31_dg5_cathedral',60,4,75,40,'phryg',[(0,'m'),(1,'M'),(0,'m'),(10,'M')],[
 P('og','pad',19,lo=45,vel=.36,G=.8),P('ch','pad',52,lo=60,vel=.3,**{'from':4}),P('bl','hit',14,every=4,oct=2,vel=.45),P('ti','hit',47,every=4,oct=0,vel=.5,**{'from':8}),M('ch2',53,8,64,84,seed=151,style='sparse',vel=.42)])
CF['32_dg6_vault']=mk('32_dg6_vault',112,4,70,43,'minor',[(0,'m'),(3,'M7'),(8,'M'),(2,'m')],[
 P('pz','arp',45,pat=[0,2,1,2,0,2,1,3],step=.5,lo=55,vel=.35,len=.6),P('bs','bass',38,pat='pulse16',vel=.5),Dm('half',v=.8,**{'from':4}),P('pd','pad',89,lo=55,vel=.22),M('vb',11,8,72,92,seed=161,style='sparse',vel=.45)])
CF['33_dg7_greenhouse']=mk('33_dg7_greenhouse',72,3,75,40,'minor',[(0,'m'),(8,'M'),(5,'m'),(7,'7')],[
 P('mb','arp',10,pat=[0,1,2],step=1,lo=66,vel=.4,len=2.0),P('pd','pad',95,lo=52,vel=.28,G=.7),P('fl','pad',73,lo=72,vel=.0,k=1) if False else P('bs','bass',32,pat='waltz',vel=.5,**{'from':4}),M('fl',73,4,69,88,seed=171,style='sparse',vel=.5)])
CF['34_dg8_sunken']=mk('34_dg8_sunken',78,4,75,34,'minor',[(0,'m7'),(5,'M7'),(3,'M7'),(10,'m7')],[
 P('at','pad',99,lo=48,vel=.32,G=.7),P('bs','bass',39,pat='drone',vel=.55),P('vc','pad',42,lo=40,vel=.3,k=1,**{'from':4}),P('pg','hit',14,every=2,oct=2,vel=.35,G=.5),Dm('dub',v=.7,**{'from':8}),M('gl',98,8,76,94,seed=181,style='sparse',vel=.4)])
CF['35_dg9_relay']=mk('35_dg9_relay',98,4,75,42,'minor',[(0,'m'),(8,'M'),(3,'M'),(10,'M')],[
 P('bp','arp',80,pat=[0,None] and [0,2,0,3,0,2,0,1],step=.25,lo=66,vel=.22,len=.7,**{'from':4}),P('pd','pad',91,lo=55,vel=.3,G=.7),P('bs','bass',38,pat='pulse16',vel=.5,**{'from':4}),Dm('soft',**{'from':8}),M('gl',98,8,76,96,seed=191,style='sparse',vel=.45)])
# ---------- endings (non-loop) ----------
CF['36_end_win']=mk('36_end_win',100,4,75,48,'major',[(0,'M7'),(9,'m7'),(2,'m7'),(7,'7')],[
 P('pn','comp',0,rh=[(0,1.5),(2.667,1)],lo=57,vel=.42),P('bs','bass',32,pat='walk',lo=34,hi=47,vel=.6),Dm('swing',**{'from':4}),M('tp',59,4,70,88,seed=201,style='mid',vel=.55),M('vb',11,12,76,94,seed=202,style='sparse',vel=.4)],loop=False,tail=4.0)
CF['37_end_escape']=mk('37_end_escape',112,4,90,50,'major',[(0,'M'),(7,'M'),(9,'m'),(5,'M')],[
 P('ag','arp',25,pat=[0,1,2,1,0,1,2,1],step=.5,lo=55,vel=.4,len=2.0),P('st','pad',48,lo=57,vel=.28,**{'from':8}),P('bs','bass',33,pat='root8',vel=.55,**{'from':12}),Dm('rock',v=.9,**{'from':16}),M('fl',73,4,74,92,seed=211,style='mid',vel=.55),M('ld',29,20,69,88,seed=212,style='mid',vel=.5),P('ch','pad',52,lo=62,vel=.26,**{'from':24})],loop=False,tail=4.0)
CF['38_end_counter']=mk('38_end_counter',88,4,80,33,'minor',[(0,'m'),(8,'M'),(3,'M'),(10,'M')],[
 P('st','pad',48,lo=52,vel=.3),P('tp','hit',47,every=2,oct=0,vel=.5),P('bs','bass',57,pat='half',vel=.6,**{'from':4}),Dm('march',v=.7,**{'from':8}),M('br',61,8,64,84,seed=221,style='sparse',vel=.55),M('ch',52,16,64,84,seed=222,style='sparse',vel=.45)],loop=False,tail=4.0)
CF['39_end_sad']=mk('39_end_sad',66,4,70,33,'minor',[(0,'m'),(5,'M7'),(8,'M'),(7,'M')],[
 P('pn','arp',0,pat=[0,2,1,3,2,1],step=.667,lo=52,vel=.34,len=2.0),P('st','pad',48,lo=52,vel=.26,**{'from':4}),P('vc','bass',42,pat='drone',vel=.5,**{'from':4}),M('vn',40,8,69,86,seed=231,style='sparse',vel=.55)],loop=False,tail=4.0)
CF['40_end_cyber']=mk('40_end_cyber',90,4,70,37,'dim',[(0,'m'),(6,'dim'),(1,'M'),(6,'dim')],[
 P('pd','pad',103,lo=52,vel=.3,G=.7),P('bs','bass',38,pat='pulse16',vel=.55),P('vb','arp',11,pat=[0,3,1,2,3,0,2,1],step=.25,lo=66,vel=.3,len=1.2),Dm('half',v=.8,**{'from':4}),P('gt','pad',30,lo=36,vel=.3,k=2,**{'from':8}),M('gl',98,6,76,96,seed=241,style='sparse',vel=.45)],loop=False,tail=4.0)
# ---------- misc ----------
CF['41_hotel']=mk('41_hotel',70,4,80,36,'minor',[(0,'m7'),(8,'M7'),(3,'M7'),(10,'7')],[
 P('pn','arp',4,pat=[0,2,1,3],step=1,lo=55,vel=.36,len=3.0),P('pd','pad',89,lo=52,vel=.24,G=.7),P('bs','bass',32,pat='half',vel=.5,**{'from':4}),Dm('lofi',v=.6,**{'from':8}),M('ep',4,8,67,86,seed=251,style='sparse',vel=.45)])
CF['42_battle_org']=mk('42_battle_org',150,4,50,42,'phryg',[(0,'5'),(1,'5'),(8,'5'),(6,'5')],[
 P('gt','arp',30,pat=[0,0,0,2,0,0,2,0],step=.5,lo=42,vel=.6,len=.8),P('bs','bass',38,pat='root8',vel=.65),Dm('rock'),P('st','arp',45,pat=[0,1,2,1],step=.25,lo=60,vel=.25,len=.6,**{'from':4}),M('ld',29,8,64,86,seed=261,style='mid',vel=.55)])
CF['43_boss_raid']=mk('43_boss_raid',128,4,55,36,'minor',[(0,'5'),(8,'5'),(5,'5'),(7,'5')],[
 P('gt','arp',30,pat=[0,0,2,0,0,2,0,2],step=.5,lo=36,vel=.6,len=.8),P('bs','bass',38,pat='root8',vel=.65),Dm('half'),P('tk','hit',116,every=2,oct=1,vel=.7,G=.9),P('hr','hit',55,every=8,vel=.5),P('br','comp',61,rh=[(0,.5),(1.5,.4)],lo=48,k=3,vel=.4,**{'from':4}),M('ch',52,8,60,80,seed=271,style='sparse',vel=.5)])
if __name__=='__main__':
    for n in (sys.argv[1:] or list(CF)):
        k=[x for x in CF if n in x][0];build(CF[k])
