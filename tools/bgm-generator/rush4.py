import numpy as np,os,re
from song import Song,S,nm
np.random.seed(21)
Q={'M':[0,4,7],'m':[0,3,7],'7':[0,4,7,10],'5':[0,7,12]}
def C(spec):return [(nm(re.match(r'([A-G][#b]?)',c).group(1)+'3'),re.match(r'[A-G][#b]?(.*)',c).group(1) or 'M') for c in spec.split()]
def fold(p,lo,hi):
    while p>hi:p-=12
    while p<lo:p+=12
    return p
def voic(r,q,lo):return [fold(r+x,lo,lo+11) for x in Q[q]]

SEC=[('intro',4),('A',8),('pre',4),('ch',8),('ch2',8),('bd',6)]
B0={};b=0
for k,n in SEC:B0[k]=b;b+=n
NB=b
tempo={0:196,B0['pre']:(196,198),B0['pre']+1:(198,201),B0['pre']+2:(201,204),B0['pre']+3:(204,206),B0['ch']:206,B0['ch2']:210,
       B0['bd']:168,B0['bd']+4:(168,182),B0['bd']+5:(182,196)}
s=Song(NB,tempo)
# 主役: ディストーション・ギターのリード
s.stem('lead',30,db=0,rev=.2,pan=0)
s.stem('clean',27,db=-2,rev=.3,pan=0)
s.stem('rhy',29,db=-13,rev=.08,pan=-.5)
s.stem('rhy2',29,db=-14,rev=.08,pan=.5)
s.stem('bass',34,db=-7,rev=.03)
s.stem('arp',81,db=-19,rev=.25,pan=.3)
s.stem('str',48,db=-17,rev=.3,pan=.2)
s.stem('ch',52,db=-19,rev=.35)
s.stem('sbr',62,db=-10,rev=.2,pan=-.1)
s.stem('drums',0,db=-4,rev=.05,drum=True)

CH={'intro':C('Em Em Em Em'),'A':C('Em C D B7 Em C Am B7'),'pre':C('C D Bm B7'),
    'ch':C('C D G Em C D B7 C7'),'bd':C('Em C G D Am B7')}
CH['ch2']=[(r+1,q) for r,q in CH['ch'][:7]]+[(nm('B3'),'7')]

MEL={
'intro':'E3:.5! E3:.25 E3:.25 G3:.5 E3:.5 A3:.5 E3:.5 Bb3:.5 A3:.5  E3:.5! E3:.25 E3:.25 G3:.5 E3:.5 D4:.5 C4:.5 B3:1  '
        'E3:.5! E3:.25 E3:.25 G3:.5 E3:.5 A3:.5 E3:.5 Bb3:.5 A3:.5  E4:.5 D4:.5 B3:.5 G3:.5 E4:1! r:1',
'A':'B4:.75! B4:.75 G4:.5 E4:1 F#4:.5 G4:.5  A4:.75! G4:.75 E4:.5 C5:2  B4:.75! A4:.75 F#4:.5 D4:1 A4:1  F#4:2! D#4:1 F#4:1 '
    'B4:.75! B4:.75 G4:.5 E5:1! D5:.5 B4:.5  C5:.75 B4:.75 G4:.5 E4:1 G4:1  A4:.5 B4:.5 C5:.5 E5:.5 A5:1! G5:1  F#5:2! D#5:1 B4:1',
'pre':'E5:1 G5:1 C6:1 B5:1  A5:1 F#5:1 D6:1 C6:1  B5:.5 A5:.5 G5:.5 F#5:.5 E5:.5 F#5:.5 G5:.5 A5:.5  B5:1! r:3',
'ch':'G5:.5 C6:.5 E6:1.5! D6:.5 C6:1  D6:.5 F#6:.5 A6:1.5! G6:.5 F#6:1  G6:1.5! D6:.5 B5:1 D6:1  E6:3! r:.5 B5:.5 '
     'C6:.5 E6:.5 G6:1.5! F#6:.5 E6:1  F#6:.5 A6:.5 D7:1.5! C7:.5 A6:1  B6:1! A6:.5 G6:.5 F#6:1 D#6:1  E6:2! G6:1 Bb6:1',
'bd':'E5:2 B4:2  C5:2 G4:2  D5:1.5 B4:.5 G4:2  F#4:2 A4:2  E4:.5 A4:.5 C5:.5 E5:.5 A5:2  B3:.5! B3:.25 B3:.25 D#4:.5 F#4:.5 A4:.5 B4:.5 D#5:.5 F#5:.5',
}
for sec in ('intro','A','pre','ch','ch2','bd'):
    if sec=='ch2':
        src=MEL['ch'].rsplit('  ',1)[0];L,tl=S(src,B0[sec]*4,1)
        L2,t2_=S('F#6:2! A6:1 B6:1',B0[sec]*4+28);L+=L2;tl+=t2_
    else:L,tl=S(MEL[sec],B0[sec]*4)
    assert abs(tl-dict(SEC)[sec]*4)<.01,(sec,tl)
    if sec=='intro':s.mel('lead',L,100,leg=.85)
    elif sec=='A':s.mel('lead',L,88,leg=.85)
    elif sec=='pre':
        for i,(b_,d,p,a) in enumerate(L):s.n('lead',b_,d*.9,p,84+i*2+(16 if a else 0))
    elif sec in ('ch','ch2'):s.mel('lead',L,110 if sec=='ch' else 118,acc=9,leg=.95)
    elif sec=='bd':
        for b_,d,p,a in L:s.n('clean' if b_<(B0['bd']+5)*4 else 'lead',b_,d*.95,p,72 if b_<(B0['bd']+5)*4 else 96+(12 if a else 0))

for sec,nbars in SEC:
    for i in range(nbars):
        bt=(B0[sec]+i)*4;r,q=CH[sec][i];rb=fold(r,40,51);V=voic(r,q,55);pw=[fold(r,40,51),fold(r,40,51)+7,fold(r,40,51)+12]
        if sec=='intro':
            # リフと同じリズムでキック・ベースがユニゾン
            for t in (0,.5,.75,1.5,2.5,3.5):s.n('bass',bt+t,.22,rb,96);s.d(bt+t,36,100)
            for t in (1,3):s.d(bt+t,38,100)
            for j in range(8):s.d(bt+j*.5,42,60)
            if i==0:s.d(bt,49,118)
            if i==3:
                s.d(bt+2,49,124);s.d(bt+2,36,124)
                for v in V+[x+12 for x in V]:s.n('sbr',bt+2,.5,v,110)
                for j in range(4):s.d(bt+3+j*.25,[50,48,45,41][j],96+j*7)
            continue
        if sec=='A':
            for j in range(8):s.n('bass',bt+j*.5,.4,rb,86 if j%2==0 else 74)
            for j in range(8):
                for v in pw:s.n('rhy',bt+j*.5,.18,v,70)
            for j in range(16):s.n('arp',bt+j*.25,.18,(V+[V[0]+12])[[0,1,2,3,2,1,0,1][j%8]]+12,62 if j%4==0 else 50)
            for t in (0,1.5,2,2.5):s.d(bt+t,36,96)
            for t in (1,3):s.d(bt+t,38,92)
            for j in range(8):s.d(bt+j*.5,42,64 if j%2==0 else 48)
            if i in(0,4):s.d(bt,49,100)
            if i==7:
                for j in range(8):s.d(bt+2+j*.25,[50,50,48,48,45,45,41,41][j],80+j*4)
        elif sec=='pre':
            if i<3:
                for j in range(8):s.n('bass',bt+j*.5,.42,rb+(12 if j%2 else 0),88+i*6)
                for t in range(4):
                    for v in pw:s.n('rhy',bt+t,.8,v,74+i*8);s.n('rhy2',bt+t,.8,v+(0 if v!=pw[2] else 0),70+i*8)
                for v in V:s.n('str',bt,3.95,v+12,66+i*14)
                for t in range(4):s.d(bt+t,36,92+i*5)
                n_=8 if i<2 else 16
                for j in range(n_):s.d(bt+j*4/n_,38,56+i*14+j*(2 if n_==8 else 2))
            else:
                s.d(bt,49,126);s.d(bt,36,126);s.n('bass',bt,.5,rb,118)
                for v in V+[x+12 for x in V]:s.n('sbr',bt,.6,v,118)
                for v in pw:s.n('rhy',bt,.8,v,110);s.n('rhy2',bt,.8,v,110)
                for j in range(8):s.d(bt+2+j*.25,[50,50,48,48,45,45,41,41][j],92+j*4)
        elif sec in ('ch','ch2'):
            big=sec=='ch2'
            for j in range(8):s.n('bass',bt+j*.5,.42,rb+(12 if j%2 else 0),106 if j%2==0 else 94)
            for t,d in ((0,1.4),(1.5,.9),(2.5,1.4)):
                for v in pw:s.n('rhy',bt+t,d,v,96);s.n('rhy2',bt+t,d,v,92)
            for v in V:s.n('str',bt,3.95,v+12,82)
            if big:
                for v in voic(r,q,64):s.n('ch',bt,3.95,v,84)
            for t in (0,1.5,2,2.5) if not big else (0,.5,1.5,2,2.5,3.5):s.d(bt+t,36,114)
            if big and i%2==1:
                for j in range(8):s.d(bt+2+j*.25,36,96)   # ツーバス連打
            for t in (1,3):s.d(bt+t,38,116)
            for j in range(8):s.d(bt+j*.5,51 if not big else 46,78 if j%2==0 else 64)
            if i%2==0:s.d(bt,49,120)
            if big and i%2==1:s.d(bt,57,104)
            if i==7:
                for j in range(8):s.d(bt+2+j*.25,[50,50,48,48,45,45,41,41][j],96+j*4)
        elif sec=='bd':
            if i<4:
                s.n('bass',bt,3.8,rb,76)
                for v in voic(r,q,60):s.n('ch',bt,3.95,v,64);s.n('str',bt,3.95,v+12,60)
                s.d(bt,36,84);s.d(bt+2,38,80)
                for j in range(4):s.d(bt+j,51,52)
            else:
                for j in range(8):s.n('bass',bt+j*.5,.42,rb,80+(i-4)*14+j*2)
                for j in range(8):
                    for v in pw:s.n('rhy',bt+j*.5,.18,v,70+(i-4)*16)
                for j in range(8):s.d(bt+j*.5,36,82+(i-4)*12)
                for j in range(16):s.d(bt+j*.25,38,46+(i-4)*34+j*2)
                if i==5:s.d(bt+3.5,49,110)

def at(sec,bar=0):return (B0[sec]+bar)*4
s.vol('lead',[(0,-2),(at('A'),-3),(at('pre'),-2),(at('ch'),0),(at('ch2'),2),(at('bd'),-4)])
s.vol('drums',[(0,-2),(at('A'),-5),(at('pre'),-5),(at('pre',3),'~-1'),(at('ch'),0),(at('ch2'),2),(at('bd'),-8),(at('bd',4),-8),(at('bd',6),'~0')])
s.vol('bass',[(0,0),(at('A'),-2),(at('ch'),0),(at('ch2'),1.5),(at('bd'),-5)])
s.vol('rhy',[(0,0),(at('A'),-4),(at('pre'),-2),(at('ch'),0),(at('ch2'),1.5)])
s.vol('rhy2',[(0,0),(at('ch2'),1.5)])
s.vol('str',[(0,0),(at('pre'),-8),(at('pre',3),'~0'),(at('bd'),-3)])
if os.environ.get('DBG'):s.dbg={}
info=s.render('/tmp/p7/music/out_pachi/p_rush4',loop_beat=at('A'))
if os.environ.get('DBG'):
    FS=44100
    for k,n in SEC:
        a=int(s.sec(B0[k]*4)*FS);b=int(s.sec((B0[k]+n)*4)*FS)
        row=sorted(((20*np.log10(np.sqrt(np.mean(x[a:b]**2))+1e-9),nm_) for nm_,x in s.dbg.items()),reverse=True)
        print(k,' '.join(f'{nm_}:{v:.0f}' for v,nm_ in row if v>-60))
    import wave
    w=wave.open('/tmp/p7/music/out_pachi/p_rush4.wav');x=np.frombuffer(w.readframes(w.getnframes()),'<i2').reshape(-1,2)/32768;m=x.mean(1)
    for k,n in SEC:
        a=int(s.sec(B0[k]*4)*FS);b=int(s.sec((B0[k]+n)*4)*FS);seg=m[a:b]
        print(f'{k:6s} {s.sec(B0[k]*4):5.1f}s mix {20*np.log10(np.sqrt(np.mean(seg**2))):6.1f}dB')
