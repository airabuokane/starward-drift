"""ラスボス「六枚翼の代行者」v5 — 作曲ルール準拠 (主役: Aメロ=弦 / サビ=金管+コーラスの2本柱)"""
import numpy as np,os,re,json
from song import Song,S,nm
from gf_mel import MA,SB
np.random.seed(5)
Q={'M':[0,4,7],'m':[0,3,7],'7':[0,4,7,10]}
def fold(p,lo,hi):
    while p>hi:p-=12
    while p<lo:p+=12
    return p
def voic(r,q,lo):return [fold(r+x,lo,lo+11) for x in Q[q]]
def C(spec):
    o=[]
    for c in spec.split():
        if '/' in c:o.append(tuple(C(x)[0] for x in c.split('/')));continue
        m=re.match(r'([A-G][#b]?)(.*)',c);o.append((nm(m.group(1)+'3'),m.group(2) or 'M'))
    return o

SEC=[('intro',4),('A',8),('A2',8),('bu',4),('S',16),('bd',8),('bd2',8),('bu2',4),('S2',8),('S3',8)]
B0={};b=0
for k,n in SEC:B0[k]=b;b+=n
NB=b
tempo={0:116,2:(116,140),3:(140,168),B0['A']:168,B0['bu']:(168,170),B0['bu']+1:(170,172),B0['bu']+2:(172,174),B0['bu']+3:(174,176),
       B0['S']:176,B0['bd']:144,B0['bu2']:(156,162),B0['bu2']+1:(162,168),B0['bu2']+2:(168,174),B0['bu2']+3:(174,180),B0['S2']:180}
for i_ in range(8):tempo[B0['bd2']+i_]=(144+1.5*i_,144+1.5*(i_+1))
s=Song(NB,tempo)
s.stem('thm',40,db=0,rev=.24,pan=-.05)      # Aメロの主役: 弦セクション
s.stem('tp',40,db=0,rev=.3,pan=.05)       # サビの主役1: トランペット
s.stem('chm',52,db=-5,rev=.35)             # サビの主役2: コーラス(主旋律)
s.stem('solo',40,db=0,rev=.3)              # ブレイクの主役: ソロ・ヴァイオリン
s.stem('hn',60,db=-9,rev=.28,pan=-.3)
s.stem('tb',57,db=-12,rev=.2,pan=.3)
s.stem('chp',52,db=-17,rev=.4)             # コーラスのパッド
s.stem('str',48,db=-16,rev=.3,pan=.25)
s.stem('run',48,db=-13,rev=.25,pan=-.25)
s.stem('pic',72,db=-15,rev=.3,pan=.2)
s.stem('glk',9,db=-20,rev=.35,pan=.4)
s.stem('pno',0,db=-8,rev=.25,pan=-.2)
s.stem('gtr',30,db=-15,rev=.08,pan=.5)
s.stem('bass',34,db=-8,rev=.03)
s.stem('cb',43,db=-12,rev=.2)
s.stem('timp',47,db=-9,rev=.3)
s.stem('taiko',116,db=-11,rev=.25)
s.stem('hit',55,db=-10,rev=.3)
s.stem('drums',0,db=-4,rev=.06,drum=True)

s.stem('tuba',58,db=-10,rev=.25)
s.stem('organ',19,db=-15,rev=.35)
s.stem('bells',14,db=-13,rev=.4,pan=-.15)
s.stem('harp',46,db=-12,rev=.35,pan=.35)
s.stem('vhi',48,db=-11,rev=.3,pan=.15)
s.stem('ooh',53,db=-13,rev=.4,pan=-.1)
SUPPORT_DB=3
for k_ in s.cfg:
    if k_ not in ('thm','tp','chm','solo'):s.cfg[k_]['db']+=SUPPORT_DB
CH={'intro':C('Dm Bb Gm A'),'A':C('Dm Bb Gm A Dm Bb Gm A'),'bu':C('Bb Gm Bb C7'),
    'S':C('F C Dm Bb F C Bb C Dm Bb F C Bb C Bb/C F'),'bd':C('Em C Am B Em C Am B'),'bd2':C('Em C Am B Em C Am B'),'bu2':C('Em D F D7')}
CH['A2']=CH['A']
CH['S2']=[((r+2,q) if not isinstance(r,tuple) else r) for r,q in CH['S'][:8]]
CH['S3']=[(r+3,q) if not isinstance(r,tuple) else tuple((x+3,y) for x,y in (r,q)) for r,q in CH['S'][8:]]
def chord(sec,i,beat=0):
    c=CH[sec][i]
    if isinstance(c[0],tuple):return c[0] if beat<2 else c[1]
    return c

# ---- メロディ ----
def place(L,off,tr=0):return [(off+b,d,p+tr,False) for b,d,p in L]
mA=place(MA,B0['A']*4);mA2=place(MA,B0['A2']*4,12)          # 2回目は1オクターブ上
s.mel('thm',mA,84,leg=.6);s.mel('thm',mA2,98,leg=.7)

mS=place(SB,B0['S']*4)
mBD=place(MA,B0['bd']*4,2-12)                               # ブレイク: Eマイナー、低い音域で
for b_,d,p,a in mBD:s.n('solo',b_,d*.95,p,74)
# ブレイク2周目: 同じスタイルのまま1オクターブ上で、楽器を増やす
mBD2=place(MA,B0['bd2']*4,2)
for b_,d,p,a in mBD2:
    s.n('solo',b_,d*.95,p,84)
    if d>=1:s.n('pic',b_,d*.9,p+12,62)
    if d>=2:s.n('glk',b_,1.2,p+12,66)
# チェロの対旋律(2周目の後半)
for b_,d,p,a in S('E4:4 E4:2 G4:2 A4:4 B4:2 A4:2 G4:4 E4:2 C4:2 E4:2 F#4:2 D#4:4',B0['bd2']*4)[0]:s.n('vhi',b_,d*.95,p-12,78)
h1=[(t,d,p) for t,d,p in SB if t<32];h2=[(t-32,d,p) for t,d,p in SB if t>=32]
mS2=place(h1,B0['S2']*4,2);mS3=place(h2,B0['S3']*4,3)
mS3[-1]=(mS3[-1][0],mS3[-1][1],mS3[-1][2]+12,True)          # 最高音はサビの最後に
for L,v in ((mS,104),(mS2,112),(mS3,118)):
    for b_,d,p,a in L:
        s.n('tp',b_,d*.95,p,v+(8 if d>=2 else 0));s.n('chm',b_,d*.98,p,v-8);s.n('hn',b_,d*.95,p-12,v-14)
        if d>=1.5:s.n('glk',b_,1,p+12,72)
for b_,d,p,a in mS3:
    if d>=1:s.n('pic',b_,d*.9,p+12,82)

# ビルドの主旋律(主役不在にしない)
for L,v in ((S('D5:4 D5:2 F5:2 F5:2 Bb5:2 C6:1! r:3',B0['bu']*4)[0],90),(S('B4:4 A4:2 D5:2 C5:2 F5:2 F#5:3 A5:1!',B0['bu2']*4)[0],86)):
    for i,(b_,d,p,acc) in enumerate(L):s.n('tp',b_,d*.95,p,v+i*4+(14 if acc else 0));s.n('hn',b_,d*.95,p-12,v-14+i*3)
# ---- 伴奏 ----
def drums_rock(bt,i,lvl,big=False,crash=True):
    s.d(bt,36,lvl);s.d(bt+1.5,36,lvl-12);s.d(bt+2.5,36,lvl-6)
    for t in (1,3):s.d(bt+t,38,lvl)
    for j in range(8):s.d(bt+j*.5,51 if big else 42,lvl-30 if j%2 else lvl-20)
    if crash and i%2==0:s.d(bt,49,lvl+4)
for sec,nbars in SEC:
    for i in range(nbars):
        bt=(B0[sec]+i)*4;r,q=chord(sec,i);rb=fold(r,38,49);V=voic(r,q,55)
        if sec=='intro':
            # 不穏: 低弦のトレモロ+ティンパニ+低いコーラス、だんだん強く
            for j in range(16):
                for v in voic(r,q,43)[:2]:s.n('str',bt+j*.25,.25,v,50+i*14)
            s.n('cb',bt,3.9,fold(r,28,39),70+i*12)
            for v in voic(r,q,52):s.n('chp',bt,3.9,v,60+i*14)
            s.n('pno',bt,2,fold(r,26,37),80+i*8);s.n('pno',bt,2,fold(r,26,37)+12,70+i*8)
            for t in (0,2):s.n('timp',bt+t,.5,fold(r,40,52),70+i*12)
            s.n('taiko',bt,.5,48,70+i*12)
            if i==3:
                for j in range(16):s.d(bt+j*.25,38,40+j*5);s.n('timp',bt+j*.25,.24,fold(r,40,52),60+j*4)
            continue
        if sec in('A','A2'):
            big=sec=='A2'
            for j in range(8):s.n('bass',bt+j*.5,.42,rb,86 if j%2==0 else 72)
            s.n('cb',bt,3.8,fold(r,28,39),70)
            for t in (.5,1.5,2.5,3.5) if not big else (0,.5,1.5,2,2.5,3.5):
                for v in voic(r,q,52)[:2]+[fold(r,52,63)+12]:
                    if big:s.n('gtr',bt+t,.2,v,84)
            for v in V:s.n('str',bt,3.95,v,62 if not big else 72)
            if big:
                for t in (0,2.5):
                    for v in V:s.n('tb',bt+t,.4,v,80)
                drums_rock(bt,i,100)
            else:
                s.d(bt,36,90);s.d(bt+2.5,36,80)
                for t in (1,3):s.n('taiko',bt+t,.3,50,70)
                for j in range(8):s.d(bt+j*.5,42,52 if j%2==0 else 40)
                if i==0:s.d(bt,49,96)
            if i==7:
                for j in range(8):s.d(bt+2+j*.25,[50,50,48,48,45,45,43,43][j],80+j*5)
        elif sec=='bu':
            if i<3:
                for j in range(8):s.n('bass',bt+j*.5,.42,rb+(12 if j%2 else 0),90+i*6)
                for v in V:s.n('str',bt,3.95,v+12,70+i*14);s.n('chp',bt,3.95,v+12,70+i*14)
                for t in range(4):s.d(bt+t,36,96+i*5);s.n('taiko',bt+t,.3,50,80+i*10)
                n_=8 if i<2 else 16
                for j in range(n_):s.d(bt+j*4/n_,38,60+i*14+j*2)
                # 弦の上昇
                for j in range(8):s.n('run',bt+j*.5,.45,fold(r,55,66)+[0,2,4,5,7,9,11,12][j]+i*0,62+i*12+j*2)
            else:
                s.d(bt,49,126);s.d(bt,36,126);s.n('hit',bt,.6,r+24,118);s.n('timp',bt,.6,fold(r,40,52),118);s.n('bass',bt,.5,rb,118)
                for v in V+[x+12 for x in V]:s.n('tb',bt,.6,v,115);s.n('str',bt,.6,v+12,110)
                for j in range(8):s.d(bt+2+j*.25,[50,50,48,48,45,45,41,41][j],96+j*4)
        elif sec in('S','S2','S3'):
            lv={'S':0,'S2':6,'S3':10}[sec]
            for half in (0,2):
                r2,q2=chord(sec,i,half);rb2=fold(r2,38,49);V2=voic(r2,q2,55)
                for j in range(4):s.n('bass',bt+half+j*.5,.42,rb2+(12 if j%2 else 0),100+lv)
                s.n('cb',bt+half,1.9,fold(r2,28,39),80+lv)
                for j in range(4):
                    for v in voic(r2,'M' if q2=='7' else q2,52)[:2]+[fold(r2,52,63)+12]:s.n('gtr',bt+half+j*.5,.22,v,88 if j%2==0 else 74)
                for v in V2:s.n('str',bt+half,1.95,v+12,80+lv);s.n('chp',bt+half,1.95,v+12,74+lv)
            drums_rock(bt,i,108+lv,big=True,crash=True)
            if sec!='S' and i%2==1:
                for j in range(8):s.d(bt+2+j*.25,36,90+lv)
            if i%4==0:
                s.n('timp',bt,.5,fold(r,40,52),110);s.n('hit',bt,.6,r+24,100+lv)
                for v in V+[x+12 for x in V]:s.n('tb',bt,.45,v,104+lv)
            # 主旋律が伸ばす所で弦の駆け上がり
            L_={'S':mS,'S2':mS2,'S3':mS3}[sec]
            if any(abs(b_-(bt+2))<.01 and d>=2 for b_,d,p,a in L_) or any(abs(b_-bt)<.01 and d>=3 for b_,d,p,a in L_):
                sc=[0,2,4,5,7,9,11,12] if q!='m' else [0,2,3,5,7,8,10,12]
                for j in range(8):s.n('run',bt+2+j*.25,.24,fold(r,62,73)+sc[j],72+j*4+lv)
            if i==nbars-1 and sec!='S3':
                for j in range(8):s.d(bt+2+j*.25,[50,50,48,48,45,45,41,41][j],100+j*4)
            if sec=='S3' and i==nbars-1:
                for j in range(8):s.d(bt+2+j*.25,38,90+j*4)
        elif sec=='bd':
            s.n('cb',bt,3.9,fold(r,28,39),62)
            for j in range(8):s.n('pno',bt+j*.5,.7,(V+[V[0]+12,V[1]+12,V[2]+12,V[0]+24,V[2]+12])[j%8],60+(j==0)*12)
            for v in voic(r,q,60):s.n('chp',bt,3.95,v,60)
            s.d(bt,36,70)
            if i>=4:s.d(bt+2,38,64)
            for j in range(4):s.d(bt+j,42,40)
        elif sec=='bd2':
            s.n('cb',bt,3.9,fold(r,28,39),70);s.n('bass',bt,3.9,fold(r,28,39)+12,64)
            for j in range(8):s.n('pno',bt+j*.5,.7,(V+[V[0]+12,V[1]+12,V[2]+12,V[0]+24,V[2]+12])[j%8],62+(j==0)*12)
            for v in voic(r,q,60):s.n('chp',bt,3.95,v,68+i*2)
            for v in voic(r,q,52):s.n('str',bt,3.95,v,58+i*3)
            if i%2==0:
                ar=[x for o in (0,12,24) for x in voic(r,q,55+o)]
                for j,v in enumerate(ar[:9]):s.n('harp',bt+j*.25,.8,v,64+j*2)
            if i>=4:
                for v in voic(r,q,48):s.n('hn',bt,3.9,v,64+(i-4)*5)
                s.n('timp',bt,.5,fold(r,40,52),70+(i-4)*6)
            s.n('bells',bt,2.5,fold(r,72,83),70) if i%4==0 else None
            s.d(bt,36,74);s.d(bt+2,38,66)
            for j in range(8):s.d(bt+j*.5,42,40+(j%2==0)*8)
            if i==7:
                for j in range(8):s.d(bt+2+j*.25,38,60+j*5)
        elif sec=='bu2':
            for j in range(8):s.n('bass',bt+j*.5,.42,rb+(12 if j%2 else 0),88+i*8)
            for v in V:s.n('str',bt,3.95,v+12,70+i*14);s.n('chp',bt,3.95,v+12,66+i*14)
            for t in range(4):s.d(bt+t,36,90+i*8);s.n('taiko',bt+t,.3,50,80+i*12)
            n_=8 if i<2 else 16
            for j in range(n_):s.d(bt+j*4/n_,38,56+i*16+j*2)
            if i==3:
                s.d(bt+3,49,124);s.n('hit',bt+3,.6,r+24,115)
                for v in V+[x+12 for x in V]:s.n('tb',bt+3,.6,v,112)
            for j in range(8):s.n('run',bt+j*.5,.45,fold(r,55,66)+[0,2,4,5,7,9,10,12][j],60+i*14+j*2)

# ---- 雄大さの追加レイヤー ----
for sec in ('A2','S','S2','S3','bu','bu2','intro'):
    nb=dict(SEC)[sec]
    for i in range(nb):
        bt=(B0[sec]+i)*4
        for half in (0,2):
            r2,q2=chord(sec,i,half)
            if sec in('S','S2','S3','A2'):s.n('tuba',bt+half,1.9,fold(r2,29,40),86 if sec=='A2' else 98)
        r,q=chord(sec,i)
        if sec=='intro' and i>=2:
            for v in voic(r,q,48):s.n('hn',bt,3.9,v,70+i*10)
            s.n('tuba',bt,3.9,fold(r,29,40),80+i*8)
        if sec in('S','S2','S3'):
            lv={'S':0,'S2':6,'S3':10}[sec]
            for v in voic(r,q,48):s.n('ooh',bt,3.95,v,80+lv)
            if sec!='S':
                for v in voic(r,q,48)+[fold(r,36,47)]:s.n('organ',bt,3.95,v,78+lv)
            if i%2==0:s.n('bells',bt,2.5,fold(r,72,83),92+lv)
            for t in (0,2):s.n('taiko',bt+t,.4,50,86+lv)
            if i%4==0:
                ar=[x for o in (0,12,24) for x in voic(r,q,55+o)]
                for j,v in enumerate(ar[:9]):s.n('harp',bt+j*.2,.8,v,76+j*3)
        if sec in('bu','bu2') and i<3:
            for v in voic(r,q,48):s.n('ooh',bt,3.95,v,70+i*12)
for L in (mS2,mS3):
    for b_,d,p,a in L:s.n('vhi',b_,d*.95,p+12,84)
# ラスサビ専用の上乗せ: ホルンの対旋律(3度下)、毎小節の鐘とティンパニ、ハープ、コーラスの高い声部、シンバルロール
for b_,d,p,a in mS3:
    s.n('hn',b_,d*.95,p-4 if (p%12) in (4,9,11) else p-3,96)
    if d>=1.5:s.n('glk',b_,1.5,p+24,80)
for i in range(8):
    bt=(B0['S3']+i)*4;r,q=chord('S3',i)
    s.n('bells',bt,2.5,fold(r,72,83),104);s.n('timp',bt,.5,fold(r,40,52),112);s.n('timp',bt+2,.5,fold(r,40,52),100)
    for v in voic(r,q,60):s.n('ooh',bt,3.95,v+12,86)
    for v in voic(r,q,55):s.n('str',bt,3.95,v+12,80)
    if i%2==0:
        ar=[x for o in (0,12,24) for x in voic(r,q,55+o)]
        for j,v in enumerate(ar[:9]):s.n('harp',bt+2+j*.2,.8,v,84+j*2)
    if i%4==3:
        for j in range(16):s.d(bt+j*.25,51,60+j*3)
def at(sec,bar=0):return (B0[sec]+bar)*4
s.stem('thm2',40,db=-1,rev=.26,pan=-.35);s.stem('thm3',40,db=-2,rev=.28,pan=.3)
s.ev['thm2']=[(t+.013,d,p,max(1,v-5)) for t,d,p,v in s.ev['thm']];s.ev['thm3']=[(t+.022,d,p,max(1,v-8)) for t,d,p,v in s.ev['thm']]
for k_ in ('thm','thm2','thm3'):s.vol(k_,[(0,-3),(at('A'),-5),(at('A2'),-4)])
s.stem('tp2',40,db=-1,rev=.32,pan=-.3);s.stem('tp3',40,db=-2,rev=.34,pan=.35)
s.stem('vla',41,db=-5,rev=.32,pan=-.15);s.stem('vc',42,db=-4,rev=.3,pan=.1)
s.ev['tp2']=[(t+.013,d,p,max(1,v-5)) for t,d,p,v in s.ev['tp']];s.ev['tp3']=[(t+.022,d,p,max(1,v-8)) for t,d,p,v in s.ev['tp']]
s.ev['vla']=[(t+.008,d,p,max(1,v-6)) for t,d,p,v in s.ev['tp']];s.ev['vc']=[(t+.004,d,p-12,max(1,v-4)) for t,d,p,v in s.ev['tp']]
s.vol('drums',[(0,-6),(at('A'),-6),(at('A2'),-4),(at('bu'),-7),(at('bu',3),'~-2'),(at('S'),0),(at('bd'),-8),(at('bd2'),-7),(at('bu2'),-9),(at('bu2',4),'~-2'),(at('S2'),1),(at('S3'),2)])
s.vol('bass',[(0,0),(at('A'),-2),(at('A2'),0),(at('S'),0),(at('S2'),1),(at('S3'),3)])
for st_ in ('chp','ooh','organ','vhi','hn','tb','tuba','harp','bells','glk','pic','run','gtr','timp','taiko','cb','hit'):s.vol(st_,[(0,0),(at('S3'),3)])
for k_ in ('tp','tp2','tp3','vla','vc'):s.vol(k_,[(0,-3),(at('bu'),-4),(at('S'),-3),(at('bd'),-5),(at('bu2'),-4),(at('S2'),-3),(at('S3'),-3)])
s.vol('chm',[(0,0),(at('S'),7),(at('S2'),7),(at('S3'),7)])
s.vol('str',[(0,-6),(at('intro',4),'~0'),(at('A'),0),(at('S3'),3)])
s.vol('solo',[(0,-4)])
if os.environ.get('DBG'):s.dbg={}
info=s.render('/tmp/p7/music/out_pachi/lastboss6',loop_beat=at('S2'))
bars=[s.sec(b*4) for b in range(NB+1)]
json.dump({'loop':[s.sec(at('S2')),s.sec(NB*4)],'bars':bars},open('/tmp/p7/music/out_pachi/lastboss6.json','w'))
print('loop',s.sec(at('S2')),s.sec(NB*4))
if os.environ.get('DBG'):
    FS=44100
    for k,n in SEC:
        a=int(s.sec(B0[k]*4)*FS);b=int(s.sec((B0[k]+n)*4)*FS)
        row=sorted(((20*np.log10(np.sqrt(np.mean(x[a:b]**2))+1e-9),nm_) for nm_,x in s.dbg.items()),reverse=True)
        print(k,' '.join(f'{nm_}:{v:.0f}' for v,nm_ in row if v>-60))
    import wave
    w=wave.open('/tmp/p7/music/out_pachi/lastboss6.wav');x=np.frombuffer(w.readframes(w.getnframes()),'<i2').reshape(-1,2)/32768;m=x.mean(1)
    for k,n in SEC:
        a=int(s.sec(B0[k]*4)*FS);b=int(s.sec((B0[k]+n)*4)*FS);seg=m[a:b]
        print(f'{k:6s} {s.sec(B0[k]*4):5.1f}s mix {20*np.log10(np.sqrt(np.mean(seg**2))):6.1f}dB')
