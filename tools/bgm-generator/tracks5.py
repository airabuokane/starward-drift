import sys,json
import kit
from kit import *
kit.DARK=False

# 真エンディング「夜明けの航海日誌」: 仲間が1人ずつ楽器を持ち寄り、最後は全員で合奏する
PROG='Em C G D Em C Am_B Em'
SECS=[('p1',1),('p2',1),('p3',2),('p4',2),('p5',2),('p6',3)]   # 各8小節
def build(name,use,out=False):
    a=Arr(name,seed=209)
    for n_,lv in SECS:
        if n_ in use:a.sec(n_,PROG,lv,78)
    if out:a.sec('out','Am_B Em',3,(78,54,2))
    a.stem('ag',25,0,.25,-.2)        # 主人公: アコースティックギター
    a.stem('banjo',105,-3,.3,.35)     # 整備士: バンジョー
    a.stem('whis',78,0,.3,.05)       # 航海士: 口笛(主旋律)
    a.stem('harm',22,0,.28,-.3)      # 交渉人: ハーモニカ
    a.stem('bass',32,-6,.06)         # 用心棒: ウッドベース
    a.stem('drums',0,-1,.08,drum=True)  # 傭兵: ドラム(ブラシ)
    a.stem('pno',0,0,.25,.2)         # 医者: ピアノ
    a.stem('mio',10,0,.4,.4)         # ミオ: オルゴール(電子の音)
    a.stem('mpad',88,-14,.4)         # ミオの光(シンセ)
    a.stem('vc',42,-2,.35,-.1);a.stem('str',48,-12,.35,.15)
    a.build()
    a.song.cfg['drums']['prog']=40   # ブラシ・キット
    U=[x['name'] for x in a.secs]
    def lv(st,tab):
        t={k:v for k,v in tab.items() if k in U}
        if t:a.lvvol(st,t)
    lv('mio',{'p5':5,'p6':2,'out':2});lv('ag',{'p1':0,'p2':-1,'p3':-2,'p4':-2,'p5':-2,'p6':0,'out':0})
    lv('drums',{'p4':0,'p5':1,'p6':4,'out':4});lv('str',{'p6':4,'out':4});lv('banjo',{'p2':0,'p3':-1,'p4':-2,'p5':-2,'p6':1,'out':1})
    # 前半4小節 = タイトル曲Aメロの引用(旅の始まり)、後半 = ため息のように下がる新しい句
    TH='B4:1 E5:1 G5:1.5! F#5:.5 | E5:2 C5:1 E5:1 | D5:1 G5:1 B5:1.5! A5:.5 | A5:3 r:1 | B5:1.5! A5:.5 G5:1 E5:1 | E5:1 G5:1 C6:1.5! B5:.5 | A5:1 C6:.5 B5:.5 A5:1 F#5:1 | E5:3 r:1'
    CM='G4:4 | E4:2 G4:2 | B4:2 D5:2 | F#4:2 A4:2 | G4:4 | E4:2 G4:2 | C5:2 D#5:2 | B4:4'
    for b in a.bars():
        if b.sec=='out':continue
        # 1: ギターは最初から最後まで
        comp(a,b,'ag','pluck8',66 if b.sec=='p1' else 60,lo=50)
        if b.sec>='p2':comp(a,b,'banjo','arp16',62 if b.sec=='p2' else 54,lo=60)
        if b.sec>='p3':bass(a,b,'bass','root4',70)
        if b.sec>='p4':
            v=70 if b.sec=='p4' else 78
            a.d(b.bt,36,v);a.d(b.bt+2,36,v-8);a.d(b.bt+1,38,v-10);a.d(b.bt+3,38,v-6)
            for t in range(4):a.d(b.bt+t+.5,42,v-30)
        if b.sec>='p4':comp(a,b,'pno','arp8',60 if b.sec=='p4' else 52,lo=55)
        if b.sec>='p5':comp(a,b,'mpad','pad',54,lo=60)
        if b.sec=='p6':
            comp(a,b,'str','pad',70,lo=55)
            for t in (1.5,3.5):a.d(b.bt+t,36,70)
            if b.i%2==0:a.d(b.bt,49,74)
            if b.last:
                for j in range(8):a.d(b.bt+2+j*.25,38,50+j*5)
    if 'p2' in use:a.mel('whis','p2',TH,80)
    if 'p3' in use:a.mel('whis','p3',TH,80);a.mel('harm','p3',CM,82)
    if 'p4' in use:a.mel('whis','p4',TH,82);a.mel('harm','p4',CM,74);a.mel('pno','p4','r:4 | r:4 | r:4 | r:2 A5:1 D6:1 | r:4 | r:4 | r:4 | r:2 B5:1 E6:1',72)
    if 'p5' in use:
        a.mel('whis','p5',TH,84);a.mel('harm','p5',CM,74)
        a.mel('mio','p5','r:4 | r:2 G5:1 E6:1 | r:4 | A6:2 F#6:2 | r:4 | r:2 G6:1 E6:1 | r:4 | B6:2 G6:2',80)
    if 'p6' in use:
        L=a.mel('whis','p6',TH,92);a.mel('harm','p6',CM,80);a.dbl('vc',L,80,-12);a.dbl('mio',L,70,12,minlen=1.5)
        a.mel('pno','p6','r:4 | r:4 | r:4 | r:2 A5:1 D6:1 | r:4 | r:4 | r:4 | r:2 B5:1 E6:1',70)
    if out:
        for st,lo in (('ag',50),('pno',48),('str',55),('mpad',60)):
            pass
        b0=a.at('out')
        a.mel('whis','out','C6:1 B5:1 A5:1 F#5:1 | E5:4!',90);a.mel('harm','out','E5:2 D#5:2 | B4:4',80);a.mel('mio','out','r:4 | B6:4',74)
        ch=voic(nm('E3'),'m',55)+voic(nm('E3'),'m',67)+[nm('F#5')]
        for p_ in ch:a.n('str',b0+4,4,p_,78);a.n('pno',b0+4,4,p_,72)
        a.n('vc',b0+4,4,nm('E3'),78)
        a.n('bass',b0,1.9,fold(nm('A2'),36,47),74);a.n('bass',b0+2,1.9,fold(nm('B2'),36,47),74);a.n('bass',b0+4,4,fold(nm('E2'),36,47),78)
        for k in range(10):a.n('banjo',b0+4+k*.12,.8,voic(nm('E3'),'m',60)[k%3]+12*(k//3),62)
        comp_bar=[x for x in a.bars(only=['out'])]
        comp(a,comp_bar[0],'ag','pluck8',60,lo=50);a.d(b0+4,49,66);a.d(b0+4,36,70)
    return a
# その時その時の主役 = 新しく加わった楽器 + 主旋律
MAINS={'p1':['ag'],'p2':['banjo','whis'],'p3':['whis','harm'],'p4':['whis','pno'],'p5':['whis','mio'],'p6':['whis','harm','mio','vc'],'out':['whis','harm']}
def t09():
    full=build('09_ending',['p1','p2','p3','p4','p5','p6'],out=True);full.nocy=True;full.render('09_ending',loop=None,tail=4,target=-15,dbg=True,mains=MAINS)
    ab=build('09_ending_ab',['p1','p2','p3','p4','p5','p6']);ab.nocy=True;m=ab.render('09_ending_ab',loop='p6',target=-15,mains=MAINS)
    c=Arr('09_ending_c')  # お尻だけ
    c=build('09_ending_c',[],out=True);c.nocy=True;c.render('09_ending_c',loop=None,tail=4,target=-15,mains=MAINS)
    print('ending loop',m['loop'],'bar',60*4/78)

def tlb():
    import subprocess
    subprocess.run(['python3','lastboss5.py'],cwd='/tmp/p7/music');subprocess.run(['python3','lbend5.py'],cwd='/tmp/p7/music')
    import shutil,json as J
    for f in ('lastboss5','lastboss5_end'):
        for ext in ('mp3','wav'):shutil.copy(f'/tmp/p7/music/out_pachi/{f}.{ext}',OUT+('11_lastboss' if f=='lastboss5' else '11_lastboss_end')+'.'+ext)
    shutil.copy('/tmp/p7/music/out_pachi/lastboss5.json',OUT+'11_lastboss.json')

if __name__=='__main__':
    for f in (sys.argv[1:] or ['t09','tlb']):print('==',f);globals()[f]()
