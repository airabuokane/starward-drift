"""ラスボス撃破の締め v7: ラスサビ最後の旋律をそのまま全員で弾き切り、キメ → 一撃で断ち切る"""
import numpy as np
from song import Song,nm as nm0
import os
TR=int(os.environ.get('TR','0'))
def nm(x):return nm0(x)+TR
np.random.seed(12)
s=Song(4,{0:180})
for k,p,db,rv,pan in (('vn',40,0,.32,0),('vn2',40,-1,.34,-.3),('vn3',40,-2,.36,.35),('vla',41,-5,.32,-.15),('vc',42,-4,.3,.1),('chm',52,-1,.42,0),('hn',60,-8,.3,-.3),('tb',57,-10,.25,.3),
                      ('str',48,-12,.35,.2),('ooh',53,-12,.4,-.1),('bass',34,-8,.05,0),('cb',43,-11,.3,0),('timp',47,-7,.35,0),('hit',55,-8,.4,0),('glk',9,-18,.4,.4),('bells',14,-14,.45,-.2),('tuba',58,-10,.25,0),('taiko',116,-10,.25,0)):s.stem(k,p,db=db,rev=rv,pan=pan)
s.stem('drums',0,db=-3,rev=.1,drum=True)
SUPPORT_DB=6
for k_ in s.cfg:
    if k_ not in ('vn','vn2','vn3','vla','vc','chm'):s.cfg[k_]['db']+=SUPPORT_DB
def mel(b,d,p,v):
    for k,o,dv,dl in (('vn',0,0,0),('vn2',0,-5,.04),('vn3',0,-8,.07),('vla',0,-6,.02),('vc',-12,-4,.01)):s.n(k,b+dl*.33,d,p+o,v+dv)
    s.n('chm',b,d,p,v-6);s.n('hn',b,d,p-12,v-12)
Q={'M':[0,4,7],'7':[0,4,7,10]}
def chord(b,d,root,q,v):
    for x in Q[q]:
        s.n('tb',b,d,root+12+x,v-6);s.n('str',b,d,root+24+x,v-10);s.n('ooh',b,d,root+24+x,v-8)
    s.n('cb',b,d,root,v-4);s.n('tuba',b,d,root,v-8)
def rock(bt,v):
    s.d(bt,36,v);s.d(bt+1.5,36,v-12);s.d(bt+2.5,36,v-6)
    for t in (1,3):s.d(bt+t,38,v)
    for j in range(8):s.d(bt+j*.5,51,v-20 if j%2 else v-12)
    for t in (0,2):s.n('taiko',bt+t,.4,50,v-10)
Ab=nm('Ab2');Db=nm('Db2');Eb=nm('Eb2')
# 1小節目(Db): ラスサビの旋律の続き Eb6-C6-Bb5
for b,d,p in ((0,2,nm('Eb6')),(2,1,nm('C6')),(3,1,nm('Bb5'))):mel(b,d*.95,p,112)
chord(0,4,Db,'M',104);rock(0,112);s.d(0,49,124);s.d(0,57,116)
for j in range(8):s.n('bass',j*.5,.42,Db+12+(12 if j%2 else 0),100)
# 2小節目(Db→Eb): Ab5-Bb5-C6-Db6 で駆け上がる、スネアの連打で煽る
for i,p in enumerate(('Ab5','Bb5','C6','Db6')):mel(4+i,.95,nm(p),110+i*4)
chord(4,2,Db,'M',104);chord(6,2,Eb,'7',110);rock(4,114)
for j in range(16):s.d(4+j*.25,38,70+j*3)
for j in range(8):s.n('bass',4+j*.5,.42,(Db if j<4 else Eb)+12+(12 if j%2 else 0),104)
for j in range(8):s.n('timp',6+j*.25,.24,Eb+12,90+j*4)
# 3小節目(Ab): 最高音 Ab6 を全員で鳴らす → 3拍目からキメ「ダ・ダ・ダン」
mel(8,1.9,nm('Ab6'),124);chord(8,2,Ab,'M',118);s.d(8,49,127);s.d(8,57,124);s.d(8,36,127);s.n('hit',8,.8,Ab+24,124);s.n('bells',8,2,nm('Ab5'),112);s.n('glk',8,1.5,nm('Ab6'),96)
s.n('timp',8,.5,Ab+12,124);s.n('bass',8,1.9,Ab+12,116)
for t,r,q,v in ((10,Eb,'7',118),(10.75,Eb,'7',118),(11.5,Eb,'7',122)):
    chord(t,.3,r,q,v);s.n('hit',t,.35,r+36,v);s.n('timp',t,.35,r+12,v);s.d(t,36,v);s.d(t,57 if t!=11.5 else 49,v-8)
    mel(t,.3,nm('G5') if t<11.5 else nm('Bb5'),v);s.n('bass',t,.3,r+12,v)
# 4小節目の頭: 全員で Ab を一撃、そこで断ち切る
t=12
for x in (Ab,Ab+12,Ab+24,Ab+36):s.n('tb',t,.32,x+12,124);s.n('str',t,.32,x+12,118)
mel(t,.35,nm('Ab6'),127);s.n('chm',t,.4,nm('Ab5'),120);s.n('cb',t,.45,nm('Ab1'),127);s.n('tuba',t,.45,nm('Ab1'),124);s.n('bass',t,.4,Ab,124)
s.n('hit',t,1.2,Ab+24,127);s.n('hit',t,1.2,Ab+12,124);s.n('timp',t,.6,Ab+12,127);s.n('timp',t,.6,Ab,127);s.n('taiko',t,.5,48,127)
s.d(t,36,127);s.d(t,49,127);s.d(t,57,124);s.d(t,52,120)
s.render('/tmp/p7/music/out_pachi/lastboss7_end'+('' if not TR else ('_g' if TR==-1 else '_f')),end_beat=13,peak_db=-1.0,tail=2.5,target=-12.0)
