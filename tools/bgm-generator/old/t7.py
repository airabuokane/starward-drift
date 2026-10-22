import numpy as np
import t2
from t3 import GMMix
from t4 import vo,fold,E,Dr,mel,Q
t2.OUTD='/tmp/p7/music/out_gf/'
MA=[(0,.5,69),(.5,.5,74),(1,1,77),(2,.5,76),(2.5,.5,74),(3,1,73),(4,1.5,74),(5.5,.5,77),(6,1,82),(7,1,81),
    (8,.5,79),(8.5,.5,81),(9,1,82),(10,.5,81),(10.5,.5,79),(11,1,77),(12,2,76),(14,1,73),(15,1,69),
    (16,.5,69),(16.5,.5,74),(17,1,77),(18,1,81),(19,.5,79),(19.5,.5,77),(20,1,77),(21,1,74),(22,2,82),
    (24,.5,79),(24.5,.5,77),(25,.5,76),(25.5,.5,77),(26,1,79),(27,1,82),(28,2,81),(30,.5,76),(30.5,.5,79),(31,1,85)]
# CHORUS (F major, 16 bars) - long soaring notes
SB=[(0,1,72),(1,2,77),(3,1,79),(4,2.5,81),(6.5,.5,79),(7,.5,77),(7.5,.5,76),(8,1,77),(9,1,74),(10,2,81),(12,2,79),(14,1,77),(15,1,79),
    (16,1,81),(17,2,84),(19,1,82),(20,1.5,81),(21.5,.5,79),(22,2,76),(24,1,77),(25,1,79),(26,1,81),(27,1,82),(28,4,84),
    (32,2,86),(34,1,84),(35,1,81),(36,2,82),(38,1,81),(39,1,79),(40,1,81),(41,1,79),(42,1,77),(43,1,81),(44,3,79),(47,1,72),
    (48,2,86),(50,1,84),(51,1,82),(52,2,84),(54,1,81),(55,1,79),(56,1,77),(57,1,79),(58,1,81),(59,1,82),(60,4,77)]
SBC=[(53,'M'),(48,'M'),(50,'m'),(46,'M'),(53,'M'),(48,'M'),(46,'M'),(48,'M'),(50,'m'),(46,'M'),(53,'M'),(48,'M'),(46,'M'),(48,'M'),('BC',),(53,'M')]
DM=[(38,'m'),(34,'M'),(43,'m'),(45,'M')]
def riff(r,k):
    t=Q[k][1];return [r,r+t,r+7,r+t,r+8 if k=='m' else r+9,r+7,r+t,r+7]
def drive(r,k):  # chorus string drive
    t=Q[k][1];return [r,r+7,r+12,r+7,r+t+12,r+7,r+12,r+7]
def gf():
    # sections: list of (kind, root, quality, transpose)
    P=[]
    for b in range(4):P.append(('in',)+DM[b]+(0,))
    for b in range(8):P.append(('A',)+DM[b%4]+(0,))
    for r,k in [(34,'M'),(43,'m'),(34,'M'),(48,'7')]:P.append(('bu',r,k,0))      # -> V of F
    for i in range(16):P.append(('S',)+((SBC[i][0],SBC[i][1]) if SBC[i][0]!='BC' else (46,'M'))+(0,i))
    for b in range(8):r,k=DM[b%4];P.append(('A2',r+2,k,2))                     # theme in E minor
    for r,k in [(38+2,'m'),(36+2,'M'),(41,'M'),(50,'7')]:P.append(('bu2',r,k,2))   # -> D7 = V of G
    for i in range(8):c=SBC[i];P.append(('S2',c[0]+2,c[1],2,i))                 # chorus in G
    for i in range(8,16):c=SBC[i] if SBC[i][0]!='BC' else (46,'M');P.append(('S3',c[0]+3,c[1],3,i))  # up to Ab
    P.append(('end',56,'M',3))
    BARS=len(P)+1;m=GMMix(BARS,152)
    m.gm={'piz':45,'glk':9,'wh':78,'str':48,'hs':49,'trem':44,'br':61,'tp':56,'hn':60,'ch':52,'timp':47,'tuba':58,'hit':55,'lo':42}
    def drums_full(bt,b,big=False):
        Dr(m,bt,36,.95);Dr(m,bt+1.5,36,.7);Dr(m,bt+2.5,36,.8);Dr(m,bt+1,38,1.0);Dr(m,bt+3,38,1.0)
        for i in range(8):Dr(m,bt+i*.5,51 if big else 42,.45 if i%2==0 else .3)
        if b%4==0 or (big and b%2==0):Dr(m,bt,49,.85)
    for b,p in enumerate(P):
        bt=b*4;sec,r,k=p[0],p[1],p[2];
        if sec=='end':
            for n in vo(r+12,k,50)+vo(r+24,k,62):E(m,'br',bt,3,n,.85);E(m,'str',bt,3,n,.7)
            for n in vo(r+36,k,67):E(m,'ch',bt,3.5,n,.7)
            Dr(m,bt,49,1.0);Dr(m,bt,36,1.0);E(m,'hit',bt,1,r+36,.85);E(m,'timp',bt,2,fold(r+12,40,52),.85);E(m,'tuba',bt,3,fold(r,33,44),.7)
            continue
        rf=riff(r+24,k if k in('m','M') else 'M')
        lo=fold(r,36,47)
        if sec=='in':
            for n in vo(r+12,k,50):E(m,'trem',bt,4,n,.3+.06*b)
            E(m,'lo',bt,4,lo,.45)
            if b==3:
                for i in range(16):E(m,'timp',bt+i*.25,.25,fold(r+12,40,52),.25+.04*i)
            else:E(m,'timp',bt,1,fold(r+12,40,52),.5)
            for i,n in enumerate(rf[:4]):E(m,'glk',bt+i*.5,.3,n+24,.35)
        elif sec=='A':
            for i,n in enumerate(rf):E(m,'piz',bt+i*.5,.3,n+12,.55 if i%2==0 else .42);E(m,'glk',bt+i*.5,.25,n+24,.3)
            E(m,'lo',bt,2,lo,.5);E(m,'lo',bt+2,2,lo,.45)
            for i in range(4):Dr(m,bt+i,36 if i%2==0 else 39,.55)
            for i in range(8):Dr(m,bt+i*.5,42,.25)
        elif sec in('bu','bu2'):
            j=b-[x[0] for x in P].index(sec)
            for i,n in enumerate(rf):E(m,'piz',bt+i*.5,.3,n+12,.5+.03*j);E(m,'str',bt+i*.5,.35,n+12,.3+.06*j)
            for n in vo(r+24,k,55):E(m,'br',bt,4,n,.3+.12*j)
            E(m,'lo',bt,4,lo,.5);E(m,'tuba',bt,4,fold(r,33,44),.4+.08*j)
            st=.5 if j<2 else .25
            for i in range(int(4/st)):Dr(m,bt+i*st,38,.35+.04*i+.06*j)
            if j==3:
                for i in range(16):E(m,'timp',bt+i*.25,.25,fold(r+12,40,52),.35+.04*i)
                for i in range(4):E(m,'tp',bt+i,1,fold(r+24+4*i,60,80),.5+.08*i)   # rising brass
                Dr(m,bt+3.5,49,.8)
        elif sec=='A2':
            for i,n in enumerate(rf):E(m,'str',bt+i*.5,.38,n+12,.6 if i%2==0 else .46);E(m,'str',bt+i*.5,.38,n,.48 if i%2==0 else .36)
            drums_full(bt,b)
            for n in vo(r+24,k,55):E(m,'hn',bt,4,n,.42)
            E(m,'tuba',bt,1.5,fold(r,33,44),.6);E(m,'tuba',bt+2,1.5,fold(r,33,44),.55)
            for t_ in (0,1.5,2.5):E(m,'timp',bt+t_,.4,fold(r+12,40,52),.6)
            if b%4==0:E(m,'hit',bt,.6,r+36,.55)
        elif sec in('S','S2','S3'):
            i=p[4]
            ch_=[(0,r,k)]
            if p[1]==46+p[3] and i==14:ch_=[(0,46+p[3],'M'),(2,48+p[3],'M')]
            for (o,rr,kk) in ch_:
                L=4-o if len(ch_)==1 else 2
                dv=drive(rr+12,kk)
                for q in range(int(L*2)):
                    n=dv[(q+int(o*2))%8];E(m,'str',bt+o+q*.5,.4,n+12,.58 if q%2==0 else .45);E(m,'piz',bt+o+q*.5,.3,n,.4)
                for n in vo(rr+24,kk,55):E(m,'br',bt+o,L,n,.5);E(m,'hn',bt+o,L,n,.45)
                for n in vo(rr+36,kk,67):E(m,'ch',bt+o,L,n,.42)
                E(m,'tuba',bt+o,L*.45,fold(rr,33,44),.65);E(m,'tuba',bt+o+L/2,L*.45,fold(rr,33,44),.6)
                E(m,'lo',bt+o,L,fold(rr,36,47),.55)
            drums_full(bt,b,big=True)
            for t_ in (0,2):E(m,'timp',bt+t_,.5,fold(r+12,40,52),.65)
            if i%4==0:E(m,'hit',bt,.6,r+36,.6)
            if sec=='S3' and i==8:   # modulation kick
                Dr(m,bt,49,1.0);E(m,'hit',bt,.8,r+36,.8)
    # melodies
    mel(m,'wh',MA,16,.6)
    off=[x[0] for x in P].index('S')*4
    mel(m,'tp',SB,off,.72);mel(m,'hs',SB,off,.6);mel(m,'ch',SB,off,.55);mel(m,'hn',SB,off,.5,-12)
    off=[x[0] for x in P].index('A2')*4
    mel(m,'tp',MA,off,.7,2);mel(m,'br',MA,off,.5,-10);mel(m,'glk',MA,off,.3,14)
    o2=[x[0] for x in P].index('S2')*4
    a=[n for n in SB if n[0]<32];bb=[(t-32,d,pp) for t,d,pp in SB if t>=32]
    for name,v,tr in (('tp',.78,2),('hs',.65,2),('ch',.62,2),('hn',.55,-10),('wh',.45,14)):mel(m,name,a,o2,v,tr)
    o3=[x[0] for x in P].index('S3')*4
    for name,v,tr in (('tp',.82,3),('hs',.7,3),('ch',.68,3),('hn',.6,-9),('wh',.5,15),('glk',.32,27)):mel(m,name,bb,o3,v,tr)
    lv={'piz':{'G':.7,'rev':(1.2,.25)},'glk':{'G':.5,'rev':(1.6,.35)},'wh':{'G':.7,'rev':(1.5,.3)},'str':{'G':.85,'rev':(1.2,.25)},'hs':{'G':.75,'rev':(1.8,.35)},'trem':{'G':.6,'rev':(2.0,.4)},
        'br':{'G':.8,'rev':(1.5,.3)},'tp':{'G':.9,'rev':(1.5,.3)},'hn':{'G':.65,'rev':(1.8,.35)},'ch':{'G':.7,'rev':(2.2,.4)},'timp':{'G':.85,'rev':(1.8,.3)},
        'tuba':{'G':.7},'hit':{'G':.6,'rev':(2.0,.35)},'lo':{'G':.65,'rev':(1.5,.3)},'drums':{'G':.9}}
    print('bars',BARS,[x[0] for x in P])
    t2.done('gf_final_battle_v2_loop',m,lv,(1.4,.28),loop=True,fade=False)
gf()
