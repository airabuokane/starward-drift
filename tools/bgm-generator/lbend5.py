import numpy as np
from song import Song,nm
np.random.seed(9)
s=Song(4,{0:180})
for k,p,db,rv,pan in (('tp',56,0,.3,0),('chm',52,-1,.4,0),('hn',60,-9,.3,-.3),('tb',57,-11,.25,.3),('str',48,-13,.35,.2),('cb',43,-12,.3,0),('timp',47,-8,.35,0),('hit',55,-9,.35,0),('glk',9,-19,.4,.4)):s.stem(k,p,db=db,rev=rv,pan=pan)
s.stem('drums',0,db=-3,rev=.1,drum=True)
SUPPORT_DB=3
for k_ in s.cfg:
    if k_ not in ('tp','chm'):s.cfg[k_]['db']+=SUPPORT_DB
Ab=nm('Ab3');V=[Ab+12,Ab+16,Ab+19]
# 1小節目: 3連の決めの打撃 → 2小節目: 最後の長い和音
for t,v in ((0,118),(1.5,110),(3,122)):
    s.d(t,49 if t!=1.5 else 57,v);s.d(t,36,v);s.n('hit',t,.6,Ab+24,v)
    for x in V+[y+12 for y in V]:s.n('tb',t,.45,x,v-6);s.n('str',t,.4,x+12,v-10)
    s.n('timp',t,.5,nm('Ab2'),v);s.n('cb',t,.5,nm('Ab1'),v)
s.n('tp',0,.45,nm('Eb5'),110);s.n('tp',1.5,.45,nm('Eb5'),106);s.n('tp',3,.45,nm('G5'),112)
s.n('tp',4,7.5,nm('Ab5'),124);s.n('chm',4,8,nm('Ab5'),110);s.n('hn',4,7.5,nm('Ab4'),100)
for x in V+[y+12 for y in V]:s.n('chm',4,8,x+12,96);s.n('str',4,8,x+12,104);s.n('tb',4,7,x,96)
s.n('cb',4,8,nm('Ab1'),110);s.d(4,49,127);s.d(4,57,120);s.d(4,36,127);s.n('hit',4,.8,Ab+24,124);s.n('glk',4,2,nm('Ab6'),90)
for j in range(24):s.n('timp',4+j*.25,.24,nm('Ab2'),110-j*3)
s.vol('tp',[(0,0),(8,0),(16,'~-30')]);s.vol('chm',[(0,0),(8,0),(16,'~-30')]);s.vol('str',[(0,0),(8,0),(16,'~-30')])
s.vol('hn',[(0,0),(8,0),(16,'~-30')]);s.vol('tb',[(0,0),(8,0),(16,'~-30')]);s.vol('cb',[(0,0),(8,0),(16,'~-30')])
s.render('/tmp/p7/music/out_pachi/lastboss5_end',peak_db=-1.0)
