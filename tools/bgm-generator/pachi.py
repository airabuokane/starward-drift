import sys,os,re,numpy as np
import t2,t3
from t3 import GMMix
from t4 import vo,fold,E,Dr,Q
t2.OUTD='/tmp/p7/music/out_pachi/';os.makedirs(t2.OUTD,exist_ok=True)
NN={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def nm(s):
    b=NN[s[0]];i=1
    if s[i]=='#':b+=1;i+=1
    elif s[i]=='b':b-=1;i+=1
    return 12*(int(s[i:])+1)+b
def S(txt,off=0):
    """'E5:.5 A5:1 r:1' -> [(beat,dur,midi)] """
    t=0;out=[]
    for tok in txt.split():
        p,d=tok.split(':');d=float(d)
        if p!='r':out.append((off+t,d,nm(p)))
        t+=d
    return out,t
def mel(m,name,L,v,tr=0,leg=.95):
    for b,d,p in L:E(m,name,b,d*leg,p+tr,v)
def chords_of(spec):
    out=[]
    for c in spec.split():
        mm=re.match(r'([A-G])([#b]?)(.*)',c);root=NN[mm.group(1)]+{'#':1,'b':-1,'':0}[mm.group(2)];q=mm.group(3) or 'M'
        out.append((36+root,q))
    return out

# ===================================================== 1) 通常時  A minor 144bpm
def normal():
    BPM=144
    INTRO=chords_of('Am F G E')
    A=chords_of('Am F G Em Am F G E')
    B=chords_of('F G Em Am Dm G C E')
    P=[('i',)+c for c in INTRO]+[('A',)+c for c in A]+[('B',)+c for c in B]+[('A2',)+c for c in A]+[('B2',)+c for c in B]
    NB=len(P);m=GMMix(NB,BPM)
    m.gm={'sq':80,'saw':81,'bass':38,'pad':50,'stab':62,'arp':98,'hit':55,'bell':14}
    for b,(sec,r,k) in enumerate(P):
        bt=b*4;big=sec in('B','B2');rb=fold(r,33,44)
        # eurobeat octave bass
        for i in range(8):E(m,'bass',bt+i*.5,.42,rb+(12 if i%2 else 0),.72 if i%2==0 else .6)
        # drums
        for i in range(4):Dr(m,bt+i,36,.95)
        Dr(m,bt+1,38,.85);Dr(m,bt+3,38,.85)
        if big:Dr(m,bt+1,39,.5);Dr(m,bt+3,39,.5)
        for i in range(4):Dr(m,bt+i+.5,46,.42);Dr(m,bt+i,42,.3)
        if sec!='i':
            for i in range(16):Dr(m,bt+i*.25,42,.18) if i%4 in(1,3) else None
        if b%8==0:Dr(m,bt,49,.85)
        if b%4==3:
            for i,t in enumerate((3,3.25,3.5,3.75)):Dr(m,bt+t,[45,45,47,50][i] if not big else 38,.55+i*.08)
        # pad
        for n in vo(r+12,k,57):E(m,'pad',bt,3.9,n,.33 if not big else .4)
        # offbeat synth-brass stabs
        for t in (.5,1.5,2.5,3.5) if sec=='i' or big else (1.5,3.5):
            for n in vo(r+12,k,62):E(m,'stab',bt+t,.3,n,.42)
        # 16th arp
        c=vo(r+24,k,64);c=c+[c[0]+12]
        for i in range(16):E(m,'arp',bt+i*.25,.2,c[[0,1,2,3,2,1,0,1][i%8]%len(c)],.32 if i%4==0 else .24)
        if sec=='i' and b==0:E(m,'hit',bt,.6,r+36,.7)
    o=4*4
    MA,_=S('E5:.5 A5:.5 B5:.5 C6:1 B5:.5 A5:1  G5:.5 A5:.5 G5:.5 F5:.5 E5:1 C5:1  D5:.5 E5:.5 G5:.5 A5:.5 B5:1.5 G5:.5  E5:3 r:1 '
           'E5:.5 A5:.5 B5:.5 C6:1 D6:.5 E6:1  D6:.5 C6:.5 A5:.5 C6:.5 D6:1 C6:1  B5:.5 A5:.5 G5:.5 B5:.5 D6:1 B5:1  G#5:1.5 A5:.5 B5:2',o)
    MB,_=S('C6:1 A5:.5 C6:.5 F6:1.5 E6:.5  D6:1 B5:.5 D6:.5 G6:1.5 F6:.5  E6:1.5 D6:.5 B5:1 G5:1  A5:1.5 B5:.5 C6:1 E6:1 '
           'F6:1 E6:.5 D6:.5 A5:1 D6:1  D6:.5 E6:.5 F6:.5 E6:.5 D6:1 B5:1  C6:.5 D6:.5 E6:1 G6:1.5 E6:.5  E6:2 D6:1 B5:1',o+32)
    mel(m,'sq',MA,.62,-12);mel(m,'saw',MA,.42,-12)
    mel(m,'sq',MB,.66,-12);mel(m,'saw',MB,.5,-12);mel(m,'bell',MB,.3,0,.6)
    A2=[(b+64,d,p) for b,d,p in MA];B2=[(b+64,d,p) for b,d,p in MB]
    mel(m,'saw',A2,.55,-12);mel(m,'sq',A2,.45,0);mel(m,'bell',A2,.25,0,.6)
    mel(m,'saw',B2,.6,-12);mel(m,'sq',B2,.55,0);mel(m,'stab',B2,.35,-12)
    lv={'sq':{'G':.85,'rev':(1.2,.22)},'saw':{'G':.7,'rev':(1.2,.22)},'bass':{'G':.95},'pad':{'G':.55,'rev':(1.6,.3)},'stab':{'G':.6,'rev':(1.2,.2)},
        'arp':{'G':.45,'rev':(1.4,.3)},'hit':{'G':.6,'rev':(1.6,.3)},'bell':{'G':.45,'rev':(1.8,.35)},'drums':{'G':.95}}
    t2.done('p_normal',m,lv,(1.2,.2))

# ===================================================== 2) 大当たり  C major 156bpm triumphant
def bonus():
    BPM=156
    I=chords_of('C G')
    A=chords_of('C G Am F C G F G')
    B=chords_of('F G Em Am F G C C')
    P=[('i',)+c for c in I]+[('A',)+c for c in A]+[('B',)+c for c in B]+[('A2',)+c for c in A]+[('B2',)+c for c in B]
    NB=len(P);m=GMMix(NB,BPM)
    m.gm={'tp':56,'br':61,'sbr':62,'saw':81,'bass':39,'str':48,'hit':55,'glk':9,'timp':47}
    for b,(sec,r,k) in enumerate(P):
        bt=b*4;big=sec in('B','B2','A2');rb=fold(r,33,44)
        for i in range(8):E(m,'bass',bt+i*.5,.42,rb+(12 if i%2 else 0),.75 if i%2==0 else .6)
        for i in range(4):Dr(m,bt+i,36,.95)
        Dr(m,bt+1,38,.9);Dr(m,bt+3,38,.9);Dr(m,bt+1,39,.5);Dr(m,bt+3,39,.5)
        for i in range(8):Dr(m,bt+i*.5,46 if i%2 else 42,.4 if i%2 else .3)
        if b%4==0:Dr(m,bt,49,.9)
        if b%8==7:
            for i in range(8):Dr(m,bt+2+i*.25,38,.5+i*.06)
        for n in vo(r+12,k,55):E(m,'str',bt,3.9,n,.45)
        for t in (0,.75,1.5,2.5,3.25):
            for n in vo(r+12,k,60):E(m,'sbr',bt+t,.32,n,.5 if big else .4)
        if sec=='i':
            for n in vo(r+24,k,60):E(m,'tp',bt,1.5,n,.75);E(m,'br',bt+2,1.8,n,.7)
            E(m,'hit',bt,.6,r+36,.8);E(m,'timp',bt,.4,fold(r,40,52),.8);E(m,'timp',bt+2,.4,fold(r,40,52),.8)
    o=2*4
    MA,_=S('G5:1 C6:.5 D6:.5 E6:1.5 G6:.5  G6:1 F6:.5 E6:.5 D6:2  C6:.5 D6:.5 E6:1 A6:1 G6:1  F6:1.5 E6:.5 C6:1 A5:1 '
           'G5:1 C6:.5 D6:.5 E6:1.5 G6:.5  B6:1 A6:.5 G6:.5 D6:2  C6:1 D6:.5 E6:.5 F6:1 A6:1  G6:3 r:1',o)
    MB,_=S('A6:1.5 G6:.5 F6:1 C6:1  B5:.5 C6:.5 D6:1 G6:2  G6:1 F6:.5 E6:.5 B5:1 E6:1  E6:1.5 D6:.5 C6:1 A5:1 '
           'A5:.5 C6:.5 F6:1 A6:1.5 G6:.5  G6:.5 A6:.5 B6:1 D7:1.5 B6:.5  C7:4  r:2 G6:.5 A6:.5 B6:1',o+32)
    for L,o2 in ((MA,0),(MB,0),(MA,64),(MB,64)):
        L2=[(b+o2,d,p) for b,d,p in L]
        mel(m,'tp',L2,.72,-12);mel(m,'saw',L2,.4,-12)
        if o2:mel(m,'br',L2,.5,-24);mel(m,'glk',L2,.28,0,.5)
    lv={'tp':{'G':.95,'rev':(1.3,.25)},'br':{'G':.7,'rev':(1.3,.25)},'sbr':{'G':.6,'rev':(1.0,.2)},'saw':{'G':.6,'rev':(1.2,.2)},'bass':{'G':.95},
        'str':{'G':.6,'rev':(1.6,.3)},'hit':{'G':.6,'rev':(1.6,.3)},'glk':{'G':.45,'rev':(1.8,.35)},'timp':{'G':.7,'rev':(1.8,.3)},'drums':{'G':.95}}
    t2.done('p_bonus',m,lv,(1.2,.2))

# ===================================================== 3) 確変・時短  E minor 172bpm rush
def rush():
    BPM=172
    A=chords_of('Em C D Bm Em C D B7')
    B=chords_of('C D Bm Em C D B7 B7')
    P=[('i',)+c for c in chords_of('Em C D B7')]+[('A',)+c for c in A]+[('B',)+c for c in B]+[('A2',)+c for c in A]+[('B2',)+c for c in B]
    NB=len(P);m=GMMix(NB,BPM)
    m.gm={'saw':81,'sq':80,'bass':38,'pad':90,'stab':62,'arp':84,'hit':55,'gtr':30}
    RIFF=[0,0,12,0,10,0,7,0, 0,0,12,0,14,12,10,7]
    for b,(sec,r,k) in enumerate(P):
        bt=b*4;big=sec in('B','B2');rb=fold(r,28,39)
        for i in range(16):
            if i%4!=1:E(m,'bass',bt+i*.25,.2,rb+(12 if i%2 else 0),.7 if i%4==0 else .5)
        # breakbeat-ish
        for t in (0,1.5,2.5):Dr(m,bt+t,36,.95)
        for t in (1,3):Dr(m,bt+t,38,.95)
        Dr(m,bt+3.75,38,.45)
        for i in range(16):Dr(m,bt+i*.25,42,.32 if i%2==0 else .2)
        Dr(m,bt+2.5,46,.35)
        if b%4==0:Dr(m,bt,49,.9)
        if b%8==7:
            for i in range(8):Dr(m,bt+2+i*.25,[50,50,47,47,45,45,41,41][i],.55+i*.05)
        for n in vo(r+12,k,57):E(m,'pad',bt,3.9,n,.38)
        # synth riff
        for i,o in enumerate(RIFF):E(m,'arp',bt+i*.25,.2,fold(r,52,63)+o,.4 if i%4==0 else .3)
        if big:
            for n in vo(r+12,k,60)[:3]:E(m,'gtr',bt,.4,n,.55);E(m,'gtr',bt+1.5,.4,n,.5);E(m,'gtr',bt+3,.8,n,.55)
        if sec=='i' and b==0:E(m,'hit',bt,.6,r+36,.8)
    o=4*4
    MA,_=S('B5:.75 E6:.75 F#6:.5 G6:1 F#6:.5 E6:.5  E6:.5 G6:.5 A6:.5 G6:.5 E6:1 C6:1  D6:.75 F#6:.75 A6:.5 B6:1 A6:.5 F#6:.5  F#6:2 D6:1 B5:1 '
           'B5:.75 E6:.75 F#6:.5 G6:1 B6:.5 A6:.5  G6:.5 E6:.5 C6:.5 E6:.5 G6:1 A6:1  F#6:.5 A6:.5 D7:1 C7:.5 B6:.5 A6:1  B6:2.5 r:1.5',o)
    MB,_=S('E6:1 G6:1 C7:1.5 B6:.5  A6:1 F#6:1 D6:1.5 F#6:.5  F#6:1 D6:.5 F#6:.5 B6:1.5 A6:.5  G6:1.5 F#6:.5 E6:2 '
           'E6:1 G6:1 C7:1.5 D7:.5  D7:1 C7:.5 B6:.5 A6:1 F#6:1  D#6:1 F#6:1 B6:1 A6:1  B6:2 D#7:1 F#7:1',o+32)
    for L,o2 in ((MA,0),(MB,0),(MA,64),(MB,64)):
        L2=[(b+o2,d,p) for b,d,p in L]
        mel(m,'saw',L2,.62,-12);mel(m,'sq',L2,.42,-12 if not o2 else 0)
        if o2:mel(m,'stab',L2,.38,-12)
    lv={'saw':{'G':.85,'rev':(1.1,.2)},'sq':{'G':.65,'rev':(1.1,.2)},'bass':{'G':.95},'pad':{'G':.5,'rev':(1.6,.3)},'stab':{'G':.55,'rev':(1.0,.2)},
        'arp':{'G':.55,'rev':(1.2,.25)},'hit':{'G':.6,'rev':(1.6,.3)},'gtr':{'G':.6},'drums':{'G':.95}}
    t2.done('p_rush',m,lv,(1.1,.2))

# ===================================================== 4) ホール  D dorian 104bpm lounge-funk
def hall():
    BPM=104
    C=chords_of('Dm9 G7 CM7 Am7 Dm9 G7 BbM7 A7')
    P=[c for _ in range(3) for c in C]
    NB=len(P);m=GMMix(NB,BPM)
    m.gm={'ep':4,'bass':36,'vib':11,'pad':89,'fl':73,'gtr':27}
    for b,(r,k) in enumerate(P):
        bt=b*4;rb=fold(r,38,49)
        for i,n in enumerate(vo(r+12,k,55)[:4]):E(m,'ep',bt+i*.02,.8,n,.42);E(m,'ep',bt+1.75+i*.02,.5,n,.34);E(m,'ep',bt+2.5+i*.02,1.2,n,.36)
        for t,d,o,v in ((0,.4,0,.7),(.75,.2,12,.5),(1.5,.3,0,.6),(2,.2,7,.5),(2.5,.4,10,.55),(3.25,.2,12,.5),(3.5,.4,7,.55)):E(m,'bass',bt+t,d,rb+o,v)
        Dr(m,bt,36,.75);Dr(m,bt+2.5,36,.6);Dr(m,bt+1,38,.6);Dr(m,bt+3,38,.6)
        for i in range(8):Dr(m,bt+i*.5,42,.3 if i%2==0 else .22)
        Dr(m,bt+3.5,46,.3)
        if b>=8:
            for n in vo(r+12,k,60)[:3]:E(m,'pad',bt,3.9,n,.3)
        if b>=16:
            for t in (.5,2.5):E(m,'gtr',bt+t,.25,fold(r,52,63)+7,.4);E(m,'gtr',bt+t+.25,.2,fold(r,52,63)+12,.35)
    MA,_=S('A5:1 C6:.5 D6:1 F6:.5 E6:1  D6:.5 B5:.5 G5:1 r:2  E6:1 G6:.5 E6:1 D6:.5 B5:1  C6:2 A5:2 '
           'A5:1 C6:.5 D6:1 F6:.5 A6:1  G6:.5 F6:.5 D6:1 r:2  F6:1 D6:.5 Bb5:1 A5:.5 F5:1  E5:1 G5:1 C#6:2',32)
    mel(m,'vib',MA,.6);M2=[(b+32,d,p) for b,d,p in MA];mel(m,'fl',M2,.5,0);mel(m,'vib',M2,.4,-12)
    lv={'ep':{'G':.75,'rev':(1.6,.3)},'bass':{'G':.9},'vib':{'G':.8,'rev':(2.0,.4)},'pad':{'G':.5,'rev':(2.0,.4)},'fl':{'G':.65,'rev':(2.0,.4)},'gtr':{'G':.45,'rev':(1.2,.2)},'drums':{'G':.75}}
    t2.done('p_hall',m,lv,(1.6,.3))


# ===================================================== 2b) 大当たり v2  ファンファーレ・マーチ 168bpm
def bonus2():
    BPM=168
    I=[('i',48,'M',0),('i',46,'M',0),('i',41,'M',0),('i',43,'M',0)]
    A=chords_of('C F G C C Am D7 G7')
    B=chords_of('F G Em Am F G C C')
    P=I+[('A',r,k,0) for r,k in A]+[('B',r,k,0) for r,k in B]+[('A2',r,k,2) for r,k in A]+[('B2',r,k,2) for r,k in B]+[('t',46,'M',0),('t',43,'7',0)]
    NB=len(P);m=GMMix(NB,BPM)
    m.gm={'tp':56,'tb':57,'hn':60,'br':61,'tuba':58,'str':48,'glk':9,'ch':52,'timp':47,'hit':55,'pic':72}
    for b,(sec,r,k,tr) in enumerate(P):
        bt=b*4;r=r+tr;big=sec in('B','B2');rb=fold(r,31,42)
        if sec=='i':
            # ファンファーレ: 3連+ロングトーン、ティンパニ
            for n in vo(r+12,k,55)+vo(r+24,k,67):
                for j in range(3):E(m,'br',bt+j/3,.28,n,.75)
                E(m,'br',bt+1,2.9,n,.8);E(m,'hn',bt+1,2.9,n-12,.6);E(m,'str',bt+1,2.9,n,.55)
            E(m,'hit',bt+1,.8,r+36,.85);E(m,'tuba',bt+1,2.8,rb,.8)
            if b==3:
                for j in range(16):Dr(m,bt+j*.25,38,.4+j*.035);E(m,'timp',bt+j*.25,.24,fold(r,40,52),.45+j*.03)
            else:
                Dr(m,bt+1,49,1.0);Dr(m,bt+1,36,1.0);E(m,'timp',bt+1,.5,fold(r,40,52),.9)
            continue
        if sec=='t':
            for n in vo(r+12,k,55)+vo(r+24,k,67):E(m,'br',bt,3.8,n,.75);E(m,'str',bt,3.8,n,.5)
            E(m,'tuba',bt,3.8,rb,.8);Dr(m,bt,49,.9)
            for j in range(8):Dr(m,bt+j*.5,38,.45+j*.06)
            continue
        # マーチのウンパ
        five=rb+7 if rb+7<=45 else rb-5
        for t,p in ((0,rb),(1,None),(2,five),(3,None)):
            if p:E(m,'tuba',bt+t,.8,p,.85)
            else:
                for n in vo(r+12,k,60)[:3]:E(m,'tb',bt+t,.3,n,.55);E(m,'str',bt+t,.25,n+12,.4)
        Dr(m,bt,36,.9);Dr(m,bt+2,36,.85)
        for t in (1,3):Dr(m,bt+t,38,.95)
        for t in (.75,2.75,3.5,3.75):Dr(m,bt+t,38,.4)
        for j in range(8):Dr(m,bt+j*.5,42 if j%2==0 else 46,.3 if j%2==0 else .35)
        if b%2==0:Dr(m,bt,49,.9)
        if b%8==7:
            for j in range(8):Dr(m,bt+2+j*.25,[50,50,47,47,45,45,41,41][j],.6+j*.05)
        # グロッケンのキラキラ
        c=vo(r+36,k,79);c=c+[c[0]+12]
        for j in range(16):E(m,'glk',bt+j*.25,.2,c[[0,1,2,3,2,1,2,3][j%8]%len(c)],.35 if j%4==0 else .25)
        if big:
            for n in vo(r+24,k,64):E(m,'ch',bt,3.9,n,.5)
            sc=[0,2,4,5,7,9,11,12] if k!='m' else [0,2,3,5,7,8,10,12]
            for j in range(8):E(m,'str',bt+j*.5,.45,fold(r,60,71)+12+sc[j],.42)
            E(m,'timp',bt,.5,fold(r,40,52),.75);E(m,'timp',bt+2,.5,fold(r,40,52),.6)
        if b%8==0:E(m,'hit',bt,.6,r+36,.75)
    MA,_=S('G4:.75 C5:.25 E5:1 G5:1.5 E5:.5  A5:1.5 G5:.5 F5:1 A5:1  G5:.75 F5:.25 E5:1 D5:1 G5:1  E5:1 C5:1 G4:2 '
           'G4:.75 C5:.25 E5:1 G5:1.5 C6:.5  C6:1 B5:.5 A5:.5 E5:1 A5:1  F#5:.75 A5:.25 D6:1 C6:1 A5:1  G5:2 B5:1 D6:1',16)
    MB,_=S('C6:1.5 A5:.5 F5:1 C6:1  D6:1.5 B5:.5 G5:1 D6:1  E6:1 D6:.5 C6:.5 B5:1 G5:1  C6:1 E6:1 A6:2 '
           'A6:1.5 G6:.5 F6:1 C6:1  B5:.5 C6:.5 D6:.5 E6:.5 F6:1 D6:1  E6:.75 D6:.25 C6:1 G6:1.5 E6:.5  C6:3 r:1',48)
    for L,o2,tr in ((MA,0,0),(MB,0,0),(MA,64,2),(MB,64,2)):
        L2=[(b+o2,d,p) for b,d,p in L];big=L is MB
        mel(m,'tp',L2,.8,tr);mel(m,'hn',L2,.5,tr-12)
        if big or o2:mel(m,'tb',L2,.5,tr-12);mel(m,'pic',L2,.35,tr+12)
    lv={'tp':{'G':1.0,'rev':(1.4,.25)},'tb':{'G':.65,'rev':(1.3,.25)},'hn':{'G':.65,'rev':(1.6,.3)},'br':{'G':.85,'rev':(1.6,.3)},'tuba':{'G':.85,'rev':(1.0,.15)},
        'str':{'G':.6,'rev':(1.6,.3)},'glk':{'G':.55,'rev':(1.8,.35)},'ch':{'G':.6,'rev':(2.0,.4)},'timp':{'G':.75,'rev':(1.8,.3)},'hit':{'G':.6,'rev':(1.6,.3)},'pic':{'G':.45,'rev':(1.6,.3)},'drums':{'G':.9}}
    t2.done('p_bonus2',m,lv,(1.4,.25))


# ===================================================== 2c) 大当たり v3  無限転調(4小節ごとに半音上げ / シェパード音で終わりなく上がり続ける)
def bonus3():
    BPM=172;NBLK=12;m=GMMix(NBLK*4,BPM)
    m.gm={'tp':56,'br':61,'sbr':62,'str':48,'ch':52,'glk':9,'bass':38,'tuba':58,'hit':55,'pic':72}
    import math
    def shep(name,b,d,p,v,ctr,sig=9,octs=(-36,-24,-12,0,12,24)):
        for o in octs:
            q=p+o;w=math.exp(-((q-ctr)/sig)**2/2)
            if w>.12 and 24<=q<=100:E(m,name,b,d,q,v*(.35+.65*w))
    MEL=[S('E5:.5 G5:.5 C6:1 D6:.5 E6:1 C6:.5  D6:1 B5:.5 G5:.5 D6:1.5 E6:.5  C6:.5 E6:.5 A6:1 G6:.5 E6:.5 C6:1  Ab5:.5 C6:.5 Eb6:.5 Gb6:.5 Ab6:1 C7:1')[0],
         S('G5:1 E6:1 D6:.5 C6:.5 G5:1  B5:.5 D6:.5 G6:1 F6:.5 D6:.5 B5:1  A5:.5 C6:.5 E6:.5 A6:1.5 G6:1  Ab5:.5 C6:.5 Eb6:.5 Gb6:.5 Ab6:1 C7:1')[0]]
    CH=[(0,'M'),(7,'M'),(9,'m'),(8,'7')]
    for blk in range(NBLK):
        K=blk;b0=blk*16
        for bar,(off,q) in enumerate(CH):
            bt=b0+bar*4;r=48+K+off
            # ベース(シェパード)
            for i in range(8):shep('bass',bt+i*.5,.42,r-12+(12 if i%2 else 0),.75 if i%2==0 else .6,40,7)
            # コード: シンセブラスの刻み + 弦 + コーラス
            for t in (0,.75,1.5,2.5,3.25):
                for n in [r+x for x in Q[q]]:shep('sbr',bt+t,.3,n,.5,62,7)
            for n in [r+x for x in Q[q]]:shep('str',bt,3.9,n,.42,66,8);shep('ch',bt,3.9,n,.4,70,8)
            # グロッケン
            c=[r+x for x in Q[q]]+[r+12]
            for j in range(16):shep('glk',bt+j*.25,.2,c[[0,1,2,3,2,1,2,3][j%8]%len(c)]+24,.3 if j%4==0 else .22,86,8)
            # ドラム
            for i in range(4):Dr(m,bt+i,36,.95)
            Dr(m,bt+1,38,.9);Dr(m,bt+3,38,.9);Dr(m,bt+1,39,.45);Dr(m,bt+3,39,.45)
            for i in range(8):Dr(m,bt+i*.5,46 if i%2 else 42,.38 if i%2 else .28)
            if bar==0:Dr(m,bt,49,1.0);Dr(m,bt,57,.8);shep('hit',bt,.6,r+24,.7,72,8)
            if bar==3:
                for j in range(8):Dr(m,bt+2+j*.25,38,.45+j*.07)
        for b_,d,p in MEL[blk%2]:
            shep('tp',b0+b_,d*.95,p+K,.8,80,8);shep('br',b0+b_,d*.95,p+K-12,.5,68,8);shep('pic',b0+b_,d*.6,p+K+12,.3,90,6)
    lv={'tp':{'G':1.0,'rev':(1.3,.25)},'br':{'G':.7,'rev':(1.3,.25)},'sbr':{'G':.6,'rev':(1.0,.2)},'str':{'G':.55,'rev':(1.6,.3)},'ch':{'G':.55,'rev':(2.0,.4)},
        'glk':{'G':.5,'rev':(1.8,.35)},'bass':{'G':.95},'hit':{'G':.6,'rev':(1.6,.3)},'pic':{'G':.4,'rev':(1.6,.3)},'drums':{'G':.95}}
    t2.done('p_bonus3',m,lv,(1.3,.22))

if __name__=='__main__':
    for n in (sys.argv[1:] or ['normal','bonus','rush','hall']):globals()[n]()
