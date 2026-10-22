import numpy as np
from song import Song,S,nm
np.random.seed(11)
Q={'M':[0,4,7],'m':[0,3,7],'7':[0,4,7,10],'sus4':[0,5,7],'m7':[0,3,7,10]}
def C(spec):
    out=[]
    for c in spec.split():
        import re;m=re.match(r'([A-G][#b]?)(.*)',c);out.append((nm(m.group(1)+'3'),m.group(2) or 'M'))
    return out
def fold(p,lo,hi):
    while p>hi:p-=12
    while p<lo:p+=12
    return p
def voic(r,q,lo):return [fold(r+x,lo,lo+11) for x in Q[q]]
SCALE_D=[2,4,6,7,9,11,1]
def third_below(p,tr):
    pc=(p-tr)%12;sc=SCALE_D
    if pc not in sc:return p-3
    i=sc.index(pc);t=sc[(i-2)%7];d=(pc-t)%12;return p-d

# ---- 構成 ----
SEC=[('intro',4),('A',8),('pre',4),('ch',8),('ch2',8),('bd',8)]
B0={};b=0
for k,n in SEC:B0[k]=b;b+=n
NB=b
tempo={0:176,B0['A']:186,B0['ch2']:190,B0['bd']:150,B0['bd']+6:(150,168),B0['bd']+7:(168,186)}
s=Song(NB,tempo)
# 主役: トランペット / 脇役は全部これより下
s.stem('tp',56,db=0,rev=.2)
s.stem('tpm',59,db=-3,rev=.3)
s.stem('hn',60,db=-12,rev=.25,pan=-.25)
s.stem('br',61,db=-9,rev=.22,pan=.15)
s.stem('bass',34,db=-7,rev=.03)
s.stem('pno',0,db=-14,rev=.15,pan=-.35)
s.stem('gtr',29,db=-15,rev=.08,pan=.45)
s.stem('str',48,db=-17,rev=.3,pan=.25)
s.stem('run',48,db=-14,rev=.25,pan=-.2)
s.stem('glk',9,db=-19,rev=.3,pan=.4)
s.stem('ch',52,db=-18,rev=.35,pan=0)
s.stem('timp',47,db=-11,rev=.25)
s.stem('hit',55,db=-11,rev=.25)
s.stem('drums',0,db=-4,rev=.06,drum=True)

CH={'intro':C('D Bb D A7'),'A':C('D Bm G A D Bm Em A7'),'pre':C('G A Bm A'),
    'ch':C('D A Bm F#m G D Em A7'),'bd':C('Em A D Bm G A A7 A7')}
CH['ch2']=[(r+2,q) for r,q in CH['ch']]
def chord_at(sec,i):return CH[sec][i]

# ---- メロディ ----
MEL={
'intro':'D5:.333! D5:.333 D5:.334 A5:2.5! r:.5  F5:.333! F5:.333 F5:.334 Bb5:1.5! C6:1 r:.5  D6:2.5! C#6:.5 D6:.5 E6:.5  E6:2! r:2',
'A':'F#4:.5 A4:.5 D5:.5! r:.5 D5:.5 E5:.5 F#5:1!  E5:.5 D5:.5 B4:1 r:.5 F#4:.5 B4:1  D5:.5 E5:.5 G5:.5! r:.5 F#5:.5 E5:.5 D5:1  C#5:1.5 A4:.5 E5:2! '
    'F#4:.5 A4:.5 D5:.5! r:.5 D5:.5 E5:.5 F#5:1!  B5:1! A5:.5 F#5:.5 D5:1 B4:1  G5:.5 F#5:.5 E5:.5 D5:.5 E5:1 G5:1  A5:2! r:2',
'pre':'B4:1 D5:1 G5:1 B5:1  C#5:1 E5:1 A5:1 C#6:1  D6:.5 C#6:.5 B5:.5 A5:.5 B5:1 D6:1  E6:1! r:3',
'ch':'A5:1! D6:1.5! C#6:.5 D6:1  E6:1.5! D6:.5 C#6:1 A5:1  F#6:1! E6:.5 D6:.5 B5:1 D6:1  C#6:2! A5:1 C#6:1 '
     'B5:.5 C#6:.5 D6:1 G6:1.5! F#6:.5  F#6:1! E6:.5 D6:.5 A5:2  G5:.5 A5:.5 B5:.5 D6:.5 E6:1! G6:1!  A6:3! r:1',
'bd':'B4:2 G4:1 E4:1  C#5:2 A4:2  D5:1.5 E5:.5 F#5:2  F#5:1 E5:1 D5:1 B4:1  B4:1 D5:1 G5:2  A5:3 G5:1  F#5:.5 G5:.5 A5:.5 B5:.5 C#6:.5 D6:.5 E6:.5 G6:.5  A6:1! r:3',
}
for sec in ('intro','A','pre','ch','ch2','bd'):
    src=MEL['ch' if sec=='ch2' else sec];tr=2 if sec=='ch2' else 0
    L,tl=S(src,B0[sec]*4,tr);assert abs(tl-dict(SEC)[sec]*4)<.01,(sec,tl)
    if sec=='intro':s.mel('tp',L,96)
    elif sec=='A':s.mel('tp',L,84,leg=.8)          # 軽く・短め
    elif sec=='pre':
        for i,(b_,d,p,a) in enumerate(L):s.n('tp',b_,d*.9,p,80+i*3+(16 if a else 0))   # だんだん強く
    elif sec in('ch','ch2'):
        s.mel('tp',L,108 if sec=='ch' else 116,acc=10)
        for b_,d,p,a in L:
            s.n('hn',b_,d*.9,third_below(p,tr)-12 if sec=='ch2' else p-12,78)
            if d>=1:s.n('glk',b_,min(d,1.5),p+12,70)
    elif sec=='bd':s.mel('tpm',L,70,acc=10)

# ---- 伴奏 ----
for sec,nbars in SEC:
    for i in range(nbars):
        bt=(B0[sec]+i)*4;r,q=chord_at(sec,i);rb=fold(r,38,49)
        V=voic(r,q,57)
        if sec=='intro':
            if i<3:
                for v in V+[x+12 for x in V]:
                    for j in range(3):s.n('br',bt+j/3,.25,v,90)
                    s.n('br',bt+1,2.3,v,100);s.n('str',bt+1,2.8,v,85)
                s.n('bass',bt+1,2.5,rb,100);s.n('timp',bt+1,.5,fold(r,40,52),110);s.n('hit',bt+1,.6,r+24,100)
                s.d(bt+1,49,120);s.d(bt+1,36,120)
                if i==1:
                    r2,q2=(nm('C3'),'M')
                    for v in voic(r2,q2,57):s.n('br',bt+2.5,1.2,v,95)
                    s.n('bass',bt+2.5,1.2,fold(r2,38,49),100);s.d(bt+2.5,49,110)
            else:
                for j in range(16):s.d(bt+j*.25,38,50+j*4);s.n('timp',bt+j*.25,.24,fold(r,40,52),60+j*3)
                for v in V:s.n('str',bt,3.9,v+12,70)
                s.n('bass',bt,3.8,rb,90)
            continue
        if sec=='A':
            for t,o,dd in ((0,0,.45),(1.5,12,.3),(2,7,.45),(3.5,12,.3)):s.n('bass',bt+t,dd,rb+o,82)
            for t in (.5,1.5,2.5,3.5):
                for v in V:s.n('pno',bt+t,.22,v+12,62)
            for t in (0,2.5):s.d(bt+t,36,92)
            s.d(bt+1.5,36,70)
            for t in (1,3):s.d(bt+t,38,84)
            for j in range(8):s.d(bt+j*.5,42,58 if j%2==0 else 44)
            if i==0:s.d(bt,49,95)
            if i==7:
                for j in range(4):s.d(bt+2+j*.5,[48,47,45,43][j],75+j*6)
        elif sec=='pre':
            if i<3:
                for j in range(8):s.n('bass',bt+j*.5,.42,rb+(12 if j%2 else 0),86+i*5)
                for t in range(4):
                    for v in V:s.n('pno',bt+t,.5,v+12,64+i*6)
                for v in V:s.n('str',bt,3.95,v+12,60+i*12)
                for t in range(4):s.d(bt+t,36,90+i*5)
            else:
                s.n('bass',bt,.5,rb,115)
                for v in V:s.n('pno',bt,.5,v+12,100);s.n('str',bt,.6,v+12,110)
            if i<2:
                for j in range(8):s.d(bt+j*.5,38,55+i*12+j*2)
            elif i==2:
                for j in range(16):s.d(bt+j*.25,38,62+j*3)
            else:
                # キメ: 1拍目だけ全員 → 無音 → 4拍目にタムのフィル
                s.d(bt,49,124);s.d(bt,36,124);s.n('hit',bt,.6,r+24,115);s.n('timp',bt,.6,fold(r,40,52),115)
                for v in V+[x+12 for x in V]:s.n('br',bt,.5,v,112)
                for j in range(4):s.d(bt+3+j*.25,[50,48,45,41][j],100+j*6)
        elif sec in ('ch','ch2'):
            big=sec=='ch2'
            for j in range(8):s.n('bass',bt+j*.5,.42,rb+(12 if j%2 else 0),104 if j%2==0 else 92)
            for j in range(8):
                for v in voic(r,'M' if q=='7' else q,52)[:2]+[voic(r,q,52)[0]+12]:s.n('gtr',bt+j*.5,.22,v,92 if j%2==0 else 78)
            for v in V:s.n('str',bt,3.95,v+12,80);s.n('pno',bt,1.5,v+12,70)
            if big:
                for v in voic(r,q,64):s.n('ch',bt,3.95,v,80)
            if i in(0,4):
                for v in V+[x+12 for x in V]:s.n('br',bt,.45,v,108)
                s.n('timp',bt,.5,fold(r,40,52),105)
            if i in(3,7):  # 主旋律が伸ばす所で弦の駆け上がり
                sc=[0,2,4,5,7,9,11,12] if q!='m' else [0,2,3,5,7,8,10,12]
                for j in range(8):s.n('run',bt+2+j*.25,.24,fold(r,62,73)+sc[j],70+j*4)
            for t in range(4):s.d(bt+t,36,112)
            for t in (1,3):s.d(bt+t,38,112);s.d(bt+t,39,70 if not big else 92)
            for j in range(8):s.d(bt+j*.5,46 if j%2 else 42,82 if j%2 else 56)
            if i%2==0 or big:s.d(bt,49,118 if i%2==0 else 96)
            if i==7:
                for j in range(8):s.d(bt+2+j*.25,[50,50,48,48,45,45,43,43][j],92+j*4)
        elif sec=='bd':
            s.n('bass',bt,3.8,rb,72)
            for j in range(8):s.n('pno',bt+j*.5,.6,(V+[V[0]+12,V[1]+12,V[2]+12,V[0]+24,V[2]+12])[j%8]+12,58+(j==0)*10)
            for v in voic(r,q,64):s.n('ch',bt,3.95,v,62)
            if i<6:
                s.d(bt,36,82);s.d(bt+2,38,78)
                for j in range(8):s.d(bt+j*.5,51,46)
            else:
                for j in range(8):s.d(bt+j*.5,36,80+i*4)
                for j in range(16):s.d(bt+j*.25,38,50+(i-6)*30+j*2)
                for v in V:s.n('str',bt,3.95,v+12,70+(i-6)*20)

# ---- 音量の流れ(セクション毎) ----
def at(sec,bar=0):return (B0[sec]+bar)*4
s.vol('tp',[(0,0),(at('A'),-3),(at('pre'),-3),(at('ch'),0),(at('ch2'),2),(at('bd'),-6)])
s.vol('gtr',[(0,0),(at('ch2'),2)])
s.vol('drums',[(0,-2),(at('A'),-5),(at('pre'),-5),(at('pre',3),-1),(at('ch'),0),(at('ch2'),2),(at('bd'),-7),(at('bd',6),-7),(at('bd',8),'~0')])
s.vol('bass',[(0,0),(at('A'),-2),(at('ch'),0),(at('ch2'),1.5),(at('bd'),-4)])
s.vol('pno',[(0,0),(at('A'),0),(at('ch'),-5),(at('bd'),4)])
s.vol('str',[(0,0),(at('pre'),-10),(at('pre',4),'~0'),(at('bd'),-4)])
s.vol('ch',[(0,0),(at('bd'),-2)])
s.vol('tpm',[(0,0)])
import os
if os.environ.get('DBG'):s.dbg={}
info=s.render('/tmp/p7/music/out_pachi/p_bonus4',loop_beat=at('A'))

if os.environ.get('DBG'):
    FS=44100
    for k,n in SEC:
        a=int(s.sec(B0[k]*4)*FS);b=int(s.sec((B0[k]+n)*4)*FS)
        row=sorted(((20*np.log10(np.sqrt(np.mean(x[a:b]**2))+1e-9),nm_) for nm_,x in s.dbg.items()),reverse=True)
        print(k,' '.join(f'{nm_}:{v:.0f}' for v,nm_ in row if v>-60))
