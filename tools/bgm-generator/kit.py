"""作曲キット: セクション/コード/定番パターン/メロディ記法 (song.py の上に乗る)"""
import numpy as np,re,json,os
from song import Song,nm,FS
OUT='/tmp/p7/music/v6/'
os.makedirs(OUT,exist_ok=True)
Q={'M':[0,4,7],'m':[0,3,7],'7':[0,4,7,10],'M7':[0,4,7,11],'m7':[0,3,7,10],'m9':[0,3,7,10,14],'9':[0,4,7,10,14],'M9':[0,4,7,11,14],
   'add9':[0,4,7,14],'sus4':[0,5,7],'sus2':[0,2,7],'dim':[0,3,6],'aug':[0,4,8],'6':[0,4,7,9],'m6':[0,3,7,9],'5':[0,7],
   '7sus4':[0,5,7,10],'mM7':[0,3,7,11],'dim7':[0,3,6,9],'m7b5':[0,3,6,10],'7b9':[0,4,7,10,13],'m11':[0,3,7,10,17]}
PC={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
VEL=[60,76,92,108]
def chd(tok):
    m=re.match(r'([A-G])([#b]?)(.*)',tok);r=48+PC[m.group(1)]+{'#':1,'b':-1,'':0}[m.group(2)];q=m.group(3) or 'M'
    assert q in Q,tok;return r,q
def fold(p,lo,hi):
    while p>hi:p-=12
    while p<lo:p+=12
    return p
def voic(r,q,lo,top=None):
    v=sorted(fold(r+x,lo,lo+11) for x in Q[q])
    return v
class Bar:
    def __init__(s,**k):s.__dict__.update(k)
    def at(s,beat):
        """拍位置のコード"""
        c=s.ch[0]
        for x in s.ch:
            if x[0]<=beat+1e-6:c=x
        return c[2],c[3]
class Arr:
    def __init__(s,name,bpb=4,seed=1):
        s.name=name;s.B=bpb;s.secs=[];np.random.seed(seed);s.stems={}
    def sec(s,name,chords,lv,tempo=None):
        bars=[]
        for tok in chords.split():
            parts=tok.split('_');d=s.B/len(parts)
            bars.append([(k*d,d)+chd(p) for k,p in enumerate(parts)])
        s.secs.append(dict(name=name,ch=bars,lv=lv,tempo=tempo,n=len(bars)));return s
    def build(s):
        s.B0={};b=0;tempo={}
        for x in s.secs:
            s.B0[x['name']]=b;t=x['tempo']
            if isinstance(t,tuple) and len(t)==2:
                a,z=t
                for i in range(x['n']):tempo[b+i]=(a+(z-a)*i/x['n'],a+(z-a)*(i+1)/x['n'])
            elif isinstance(t,tuple) and len(t)==3:   # (bpm, ramp_to, ramp_bars) 最後の数小節だけ変化
                a,z,k=t
                for i in range(x['n']):
                    j=i-(x['n']-k)
                    tempo[b+i]=a if j<0 else (a+(z-a)*j/k,a+(z-a)*(j+1)/k)
            elif t is not None:tempo[b]=t
            b+=x['n']
        s.NB=b;s.song=Song(b,tempo,s.B)
        for k,v in s.stems.items():s.song.stem(k,**v)
        return s
    def stem(s,name,prog,db=0,rev=.15,pan=0,drum=False):
        s.stems[name]=dict(prog=prog,db=db,rev=rev,pan=pan,drum=drum)
        if hasattr(s,'song'):s.song.stem(name,prog,db=db,rev=rev,pan=pan,drum=drum)
    def bars(s,only=None):
        for x in s.secs:
            if only and x['name'] not in only:continue
            for i in range(x['n']):
                bt=(s.B0[x['name']]+i)*s.B
                yield Bar(sec=x['name'],i=i,n=x['n'],bt=bt,ch=x['ch'][i],lv=x['lv'],last=(i==x['n']-1),r=x['ch'][i][0][2],q=x['ch'][i][0][3],v=VEL[x['lv']],B=s.B)
    def at(s,sec,bar=0):return (s.B0[sec]+bar)*s.B
    def n(s,*a):s.song.n(*a)
    def d(s,beat,p,vel):s.song.n('drums',beat,.1,p,vel)
    def mel(s,stem,sec,txt,vel,tr=0,leg=.92,acc=14,bar=0,lvramp=0):
        """'E5:.5 A5:.5 | ...' 小節ごとに長さを検証して配置。戻り値: [(beat,dur,midi,acc)]"""
        off=s.at(sec,bar);out=[];t=0
        for bi,bt_ in enumerate(txt.split('|')):
            tt=0
            for tok in bt_.split():
                p,d=tok.split(':');a=d.endswith('!');d=float(d.rstrip('!'))
                if p!='r':out.append((off+t+tt,d,nm(p)+tr,a))
                tt+=d
            assert abs(tt-s.B)<.01 or not bt_.strip(),(s.name,sec,bi,tt)
            t+=tt
        for k,(b,d,p,a) in enumerate(out):
            s.n(stem,b,d*leg,p,vel+(acc if a else 0)+lvramp*k/max(1,len(out)))
        return out
    def dbl(s,stem,notes,vel,tr=0,leg=.92,minlen=0):
        for b,d,p,a in notes:
            if d>=minlen:s.n(stem,b,d*leg,p+tr,vel)
    def lvvol(s,stem,tab):
        """セクションの lv ごとの音量(dB)。tab: {0:-6,1:-3,2:0,3:2} または 名前→dB"""
        pts=[]
        for x in s.secs:
            g=tab.get(x['name'],tab.get(x['lv'],0));pts.append((s.at(x['name']),g))
        s.song.vol(stem,pts)
    def render(s,fname,loop=None,target=-14.0,tail=0.0,dbg=False,mains=None,gap=3.0):
        if dbg:s.song.dbg={}
        if DARK:darken(s,mains)
        elif fname in CY and not getattr(s,'nocy',False):cyberize(s,**CY[fname])
        lb=s.at(loop) if loop else None
        secs=[(s.song.sec(s.at(x['name'])),s.song.sec(s.at(x['name'])+x['n']*s.B),x['name']) for x in s.secs]
        info=s.song.render(OUT+fname,loop_beat=lb,target=target,tail=tail,mains=mains,gap=gap,secs=secs)
        print('  boost',round(info['boost'],1))
        bars=[s.song.sec(b*s.B) for b in range(s.NB+1)]
        meta=dict(len=info['len'],loop=[s.song.sec(lb),s.song.sec(s.NB*s.B)] if loop else None,bars=bars,secs=[(x['name'],s.song.sec(s.at(x['name']))) for x in s.secs])
        json.dump(meta,open(OUT+fname+'.json','w'))
        if dbg:s.report(fname)
        return meta
    def report(s,fname):
        import wave
        w=wave.open(OUT+fname+'.wav');x=np.frombuffer(w.readframes(w.getnframes()),'<i2').reshape(-1,2)/32768;m=x.mean(1)
        for sx in s.secs:
            a=int(s.song.sec(s.at(sx['name']))*FS);b=int(s.song.sec(s.at(sx['name'])+sx['n']*s.B)*FS)
            row=sorted(((20*np.log10(np.sqrt(np.mean(v[a:b]**2))+1e-9),k) for k,v in s.song.dbg.items()),reverse=True)
            mix=20*np.log10(np.sqrt(np.mean(m[a:b]**2))+1e-9)
            print(f"  {sx['name']:6s} mix{mix:6.1f} | "+' '.join(f'{k}:{v:.0f}' for v,k in row[:7] if v>-55))

# ================= 定番パターン =================
def drums(a,b,kind,v=None,crash=None,fill=False):
    v=v or b.v;bt=b.bt;d=a.d;B=b.B
    if kind=='rock':
        d(bt,36,v);d(bt+1.5,36,v-14);d(bt+2,36,v-4)
        for t in (1,3):d(bt+t,38,v)
        for j in range(8):d(bt+j*.5,42,v-28 if j%2 else v-18)
    elif kind=='rock16':
        for t in (0,.75,1.5,2,2.5):d(bt+t,36,v-(0 if t in(0,2) else 10))
        for t in (1,3):d(bt+t,38,v+4)
        for j in range(16):d(bt+j*.25,42,v-34 if j%2 else v-22)
    elif kind=='ride':
        d(bt,36,v);d(bt+2.5,36,v-8)
        for t in (1,3):d(bt+t,38,v)
        for j in range(8):d(bt+j*.5,51,v-24 if j%2 else v-14)
    elif kind=='four':
        for t in range(4):d(bt+t,36,v)
        for t in (1,3):d(bt+t,38,v-6);d(bt+t,39,v-30)
        for j in range(8):d(bt+j*.5,46 if j%2 else 42,v-26 if j%2 else v-34)
    elif kind=='half':
        d(bt,36,v);d(bt+2,38,v)
        for j in range(8):d(bt+j*.5,42,v-30)
    elif kind=='funk':
        for t in (0,.75,2.5):d(bt+t,36,v-(0 if t==0 else 10))
        for t in (1,3):d(bt+t,38,v)
        for t in (1.75,3.25):d(bt+t,38,v-40)
        for j in range(16):d(bt+j*.25,42,v-36 if j%2 else v-22)
    elif kind=='swing':
        sw=[0,.667]
        for t in range(B):
            d(bt+t,51,v-22)
            if t%2==1:d(bt+t+.667,51,v-34);d(bt+t,44,v-30)
        if b.i%2==0:d(bt,36,v-24)
        d(bt+3.667,38,v-40)
    elif kind=='brush':
        for t in range(B):d(bt+t,40 if t%2 else 37,v-40);d(bt+t+.5,42,v-44)
        d(bt,36,v-30)
    elif kind=='march':
        d(bt,36,v-6);d(bt+2,36,v-10)
        for t in (1,3):d(bt+t,38,v)
        for t in (.75,2.75,3.5,3.75):d(bt+t,38,v-32)
        for t in range(4):d(bt+t,49 if False else 42,v-34)
    elif kind=='train':
        d(bt,36,v-6);d(bt+2,36,v-10)
        for j in range(16):d(bt+j*.25,38,v-(26 if j%4 in(1,3) else 36 if j%4==2 else 18))
    elif kind=='bossa':
        for t in (0,1.5,2,3.5):d(bt+t,36,v-20)
        for t in (0,.75,1.5,2.5,3.25):d(bt+t,37,v-26)
        for j in range(8):d(bt+j*.5,70,v-36)
    elif kind=='tribal':
        for t,p_,g in ((0,116,0),(.75,116,-18),(1.5,116,-10),(2,116,-4),(3,117,-12),(3.5,117,-18)):a.n('taiko',bt+t,.3,{116:45,117:52}[p_],v+g) if 'taiko' in a.stems else d(bt+t,{116:41,117:45}[p_],v+g)
    elif kind=='waltz':
        d(bt,36,v-10)
        for t in (1,2):d(bt+t,42,v-36);d(bt+t,37,v-40)
    elif kind=='shuffle':
        d(bt,36,v);d(bt+2,36,v-8)
        for t in (1,3):d(bt+t,38,v)
        for t in range(4):d(bt+t,42,v-24);d(bt+t+.667,42,v-34)
    elif kind=='dbass':
        for j in range(8):d(bt+j*.5,36,v-6)
        for t in (1,3):d(bt+t,38,v+4)
        for t in range(4):d(bt+t,49 if t==0 else 42,v-10 if t==0 else v-24)
    elif kind=='pulse':
        for t in range(B):d(bt+t,36,v-14)
        d(bt+B-1+.5,36,v-24)
    elif kind=='none':pass
    if crash is None:crash=b.i==0
    if crash:d(bt,49,v+6);d(bt,36,v)
    if fill:tom_fill(a,b,v)
def tom_fill(a,b,v,beats=2,snare=False):
    st=b.bt+b.B-beats;n_=int(beats*4)
    seq=[50,50,48,48,45,45,43,43,41,41,41,41][-n_:] if not snare else [38]*n_
    for j in range(n_):a.d(st+j*.25,seq[j%len(seq)],v-10+j*int(20/n_))
def snare_roll(a,b,v0,v1,beats=None,div=.25):
    beats=beats or b.B;n_=int(beats/div)
    for j in range(n_):a.d(b.bt+b.B-beats+j*div,38,int(v0+(v1-v0)*j/max(1,n_-1)))
def bass(a,b,stem,kind,v=None,lo=36,hi=47):
    v=v or b.v;bt=b.bt;n=a.n
    for (off,dur,r,q) in b.ch:
        rb=fold(r,lo,hi);fifth=rb+7 if rb+7<=hi+5 else rb-5;t0=bt+off
        if kind=='root8':
            for j in range(int(dur*2)):n(stem,t0+j*.5,.42,rb,v-(0 if j%2==0 else 10))
        elif kind=='oct8':
            for j in range(int(dur*2)):n(stem,t0+j*.5,.42,rb+(12 if j%2 else 0),v-(0 if j%2==0 else 8))
        elif kind=='root4':
            for j in range(int(dur)):n(stem,t0+j,.85,rb if j%2==0 else fifth,v-(0 if j==0 else 8))
        elif kind=='long':n(stem,t0,dur*.97,rb,v)
        elif kind=='half':
            for j in range(int(dur/2)):n(stem,t0+j*2,1.9,rb if j==0 else fifth,v)
        elif kind=='walk':
            third=rb+(3 if 'm' in q and q not in('M7','M9') else 4);seq=[rb,third,fifth,fifth+(2 if fifth<rb+7 else -1)]
            for j in range(int(dur)):n(stem,t0+j,.9,seq[j%4],v-(0 if j==0 else 10))
        elif kind=='bossa':
            for t,p_ in ((0,rb),(1.5,fifth),(2,fifth),(3.5,rb)):
                if t<dur:n(stem,t0+t,.45 if t in(1.5,3.5) else 1.4,p_,v-(0 if t==0 else 8))
        elif kind=='funk':
            for t,o,dd in ((0,0,.3),(.75,12,.2),(1.5,0,.2),(2,7,.3),(2.75,10,.2),(3.25,12,.2),(3.5,0,.3)):
                if t<dur:n(stem,t0+t,dd,rb+o,v-(0 if t==0 else 12))
        elif kind=='syncop':
            for t,dd in ((0,.4),(.75,.2),(1.5,.4),(2.5,.4),(3,.2),(3.5,.4)):
                if t<dur:n(stem,t0+t,dd,rb,v-(0 if t in(0,2.5) else 12))
        elif kind=='gallop':
            for j in range(int(dur)):
                for t,dd in ((0,.4),(.5,.2),(.75,.2)):n(stem,t0+j+t,dd,rb,v-(0 if t==0 else 10))
        elif kind=='waltz':
            n(stem,t0,.9,rb,v);
            if dur>=3:n(stem,t0+1.5,.4,fifth,v-20) if False else None
        elif kind=='pedal16':
            for j in range(int(dur*4)):n(stem,t0+j*.25,.2,rb,v-(0 if j%4==0 else 14))
        elif kind=='tuba':
            for j in range(int(dur)):
                if j%2==0:n(stem,t0+j,.8,rb if j%4==0 else fifth,v)
def comp(a,b,stem,kind,v=None,lo=55,div=None):
    v=v or b.v;bt=b.bt;n=a.n
    for (off,dur,r,q) in b.ch:
        V=voic(r,q,lo);t0=bt+off
        if kind=='pad':
            for p_ in V:n(stem,t0,dur*.98,p_,v)
        elif kind=='block':
            for p_ in V:n(stem,t0,min(dur,2)*.9,p_,v)
        elif kind=='stab_off':
            for j in range(int(dur)):
                for p_ in V:n(stem,t0+j+.5,.22,p_,v-(0 if j%2 else 6))
        elif kind=='stab4':
            for j in range(int(dur)):
                for p_ in V:n(stem,t0+j,.3,p_,v-(0 if j%2==0 else 8))
        elif kind=='charleston':
            for t,dd in ((0,.6),(1.5,.4)):
                if t<dur:
                    for p_ in V:n(stem,t0+t,dd,p_,v)
        elif kind=='swingcomp':
            for t,dd in ((0,.5),(1.667,.3),(2.667,.5)):
                if t<dur:
                    for p_ in V:n(stem,t0+t,dd,p_,v-(0 if t==0 else 8))
        elif kind=='bossa_gtr':
            for t in (0,.75,1.5,2.5,3.25):
                if t<dur:
                    n(stem,t0+t,.3,fold(r,40,51),v-6)
                    for p_ in V[1:]:n(stem,t0+t+.02,.35,p_,v-12)
        elif kind=='strum':
            for t in (0,1,1.5,2.5,3,3.5):
                if t<dur:
                    for k,p_ in enumerate(V+[V[0]+12]):n(stem,t0+t+k*.012,.4,p_,v-(0 if t in(0,2.5) else 12))
        elif kind=='power8':
            P=[fold(r,40,51),fold(r,40,51)+7,fold(r,40,51)+12]
            for j in range(int(dur*2)):
                for p_ in P:n(stem,t0+j*.5,.2,p_,v-(0 if j%2==0 else 12))
        elif kind=='powerlong':
            P=[fold(r,40,51),fold(r,40,51)+7,fold(r,40,51)+12]
            for p_ in P:n(stem,t0,dur*.95,p_,v)
        elif kind=='waltz':
            for j in (1,2):
                if j<dur:
                    for p_ in V:n(stem,t0+j,.5,p_,v-8)
        elif kind=='tremolo':
            for j in range(int(dur*4)):
                for p_ in V[:2]:n(stem,t0+j*.25,.24,p_,v-(0 if j%4==0 else 10))
        elif kind=='arp8' or kind=='arp16':
            dv=.5 if kind=='arp8' else .25;seq=V+[V[0]+12,V[1]+12]
            pat=[0,1,2,3,4,3,2,1]
            for j in range(int(dur/dv)):n(stem,t0+j*dv,dv*1.6,seq[pat[j%8]%len(seq)],v-(0 if j%4==0 else 10))
        elif kind=='arpup':
            seq=V+[x+12 for x in V]+[V[0]+24];dv=div or .25
            for j in range(int(dur/dv)):n(stem,t0+j*dv,dv*2,seq[j%len(seq)],v-(0 if j%4==0 else 10))
        elif kind=='pluck8':
            seq=[V[0],V[2],V[1],V[2]]
            for j in range(int(dur*2)):n(stem,t0+j*.5,.45,seq[j%4]+(0 if j<4 else 0),v-(0 if j%2==0 else 10))
def run_up(a,stem,beat,r,q,v,beats=1,lo=62,minor=None):
    minor='m' in q and q not in('M7','M9') if minor is None else minor
    sc=[0,2,3,5,7,8,10,12] if minor else [0,2,4,5,7,9,11,12];n_=int(beats*4)
    for j in range(n_):a.n(stem,beat+j*.25*(beats*4/n_)*1,.24,fold(r,lo,lo+11)+sc[j%8]+12*(j//8),v-12+j*3)
def kime(a,b,stems,v=118,beat=0,crash=True):
    r,q=b.at(beat)
    for st,lo in stems:
        for p_ in voic(r,q,lo):a.n(st,b.bt+beat,.5,p_,v)
    if crash:a.d(b.bt+beat,49,v+4);a.d(b.bt+beat,36,v+4)

# ================= サイバーパンク・チル化 =================
def cyberize(a,kit=None,pad=-16,arp=None,pump=.3,remap=None,hats=None,pad_prog=90,arp_prog=81,lofi=False):
    """電子ドラム化・シンセパッド(ポンプ)・控えめなアルペジオ・楽器の置き換え"""
    if kit is not None and 'drums' in a.song.cfg:a.song.cfg['drums']['prog']=kit
    for k_,p_ in (remap or {}).items():
        if k_ in a.song.cfg:a.song.cfg[k_]['prog']=p_
    if pad is not None:
        a.stem('cpad',pad_prog,pad+5,.4,-.15);a.song.cfg['cpad']['pump']=pump
        for b in a.bars():
            for (off,dur,r,q) in b.ch:
                for p_ in voic(r,q,55)[:3]:a.n('cpad',b.bt+off,dur*.98,p_,50+b.lv*8)
    if arp is not None:
        a.stem('carp',arp_prog,arp+4,.35,.3)
        for b in a.bars():
            if b.lv==0 and arp>-14:continue
            for (off,dur,r,q) in b.ch:
                V=voic(r,q,64);seq=V+[V[0]+12]
                for j in range(int(dur*4)):a.n('carp',b.bt+off+j*.25,.12,seq[[0,2,1,3,2,0,3,1][j%8]%len(seq)],(44 if j%4 else 56)+b.lv*4)
    if hats is not None and 'drums' in a.song.cfg:
        for b in a.bars():
            for j in range(b.B*4):
                if j%2==1 or b.lv>=2:a.d(b.bt+j*.25,42,hats+(8 if j%4==2 else 0)-(10 if j%2 else 0))
    if lofi and 'drums' in a.song.cfg:
        a.song.cfg['drums']['prog']=25
# 曲ごとの設定(ラスボスは対象外 = 異質なまま)
SYN={'cho':54,'vln':50,'str':50,'br':63,'tb':63,'timp':118,'taiko':118,'org':90,'run':81,'bell':98,'hn':62,'lstr':95,'pad':90}
CY={
 '01_title':dict(kit=24,pad=-15,arp=-17,pump=.3,remap={'vln':50,'cho':54,'timp':118,'br':63}),
 '02_town':dict(kit=25,pad=-15,arp=-19,pump=.35),
 '03_ship':dict(kit=25,pad=-15,arp=-18,pump=.25),
 '04_battle':dict(kit=24,pad=-15,remap={'str':90,'sbr':63},pump=.35),
 '05_dungeon':dict(kit=24,pad=-16,arp=-19,pump=.25,remap={'lstr':95}),
 '06_boss':dict(kit=24,pad=-15,pump=.35,remap={'br':63,'cho':81,'vc':80,'tb':63,'org':90,'str':90,'run':81,'timp':118,'taiko':118}),
 '07_lastdungeon':dict(kit=24,pad=-15,arp=-18,pump=.25,remap={'cho':54,'br':63,'org':95,'timp':118,'taiko':118,'bell':98,'str':50}),
 '08_blackmarket':dict(pad=-17,pump=.2),
 '41_hotel':dict(kit=25,pad=-15,arp=-20,pump=.35),
 '42_battle_org':dict(kit=24,pad=-15,pump=.35,remap={'br':63,'str':90}),
 '43_boss_raid':dict(kit=24,pad=-15,pump=.35,remap={'org':90,'cho':54,'vln':80}),
 '10_voyage':dict(kit=24,pad=-15,arp=-14,pump=.25,remap={'timp':118}),
 '44_sleep':dict(pad=-16,pump=.15),
}
for k_ in ('12_ice','13_ruins','14_pirate','15_vector','16_casino','17_corp','18_resort','19_terminal','20_frontier','21_mining','22_lab','23_farm','24_shipyard','25_residential','26_oldresort'):
    CY[k_]=dict(pad=-17,pump=.25)
for k_ in ('17_corp','19_terminal','22_lab'):CY[k_]=dict(kit=24,pad=-16,pump=.35)
for k_ in ('27_dg1_cistern','28_dg2_tunnel','29_dg3_frozen','30_dg4_bunker','31_dg5_cathedral','32_dg6_vault','33_dg7_greenhouse','34_dg8_sunken','35_dg9_relay'):
    CY[k_]=dict(pad=-16,arp=-20,pump=.25)
CY['28_dg2_tunnel'].update(kit=24);CY['30_dg4_bunker'].update(kit=24,remap={'timp':118});CY['32_dg6_vault'].update(kit=24);CY['35_dg9_relay'].update(kit=24)
for k_ in ('36_end_win','37_end_escape','38_end_counter','39_end_sad'):CY[k_]=dict(pad=-17,pump=.2)
CY['40_end_cyber']=dict(kit=24,pad=-16,pump=.35)

# ================= 暗いサイバーパンク用の部品 =================
def rain(a,stem='rain',v=60):
    """雨音(FX Rain)を全編に薄く"""
    for b in a.bars():a.n(stem,b.bt,b.B*.99,72,v)
def sbass(a,b,stem,kind='oct16',v=None,lo=28,hi=39):
    v=v or b.v
    for (off,dur,r,q) in b.ch:
        rb=fold(r,lo,hi);t0=b.bt+off
        if kind=='oct16':
            for j in range(int(dur*4)):a.n(stem,t0+j*.25,.2,rb+(12 if j%4==2 else 0),v-(0 if j%4==0 else 14))
        elif kind=='gallop':
            for j in range(int(dur)):
                for t,dd in ((0,.22),(.5,.2),(.75,.2)):a.n(stem,t0+j+t,dd,rb,v-(0 if t==0 else 12))
        elif kind=='pulse8':
            for j in range(int(dur*2)):a.n(stem,t0+j*.5,.4,rb,v-(0 if j%2==0 else 10))
        elif kind=='drone':a.n(stem,t0,dur*.99,rb,v)
def ddrums(a,b,kind,v=None,crash=None,fill=False):
    """暗いサイバー向けドラム(キットは電子/パワー)"""
    v=v or b.v;bt=b.bt;d=a.d
    if kind=='gated':          # 80年代のゲートリバーブ風: 重いキックと大きいスネア
        d(bt,36,v);d(bt+2.5,36,v-12)
        for t in (1,3):d(bt+t,38,v+6);d(bt+t,39,v-20)
        for j in range(8):d(bt+j*.5,42,v-34 if j%2 else v-26)
    elif kind=='dark4':        # 四つ打ち+裏のハット+クラップ
        for t in range(4):d(bt+t,36,v)
        for t in (1,3):d(bt+t,39,v-4);d(bt+t,38,v-14)
        for t in range(4):d(bt+t+.5,46,v-26)
        for j in range(16):d(bt+j*.25,42,v-40) if j%2 else None
    elif kind=='slow':         # 遅い808: キック+遠いスネア
        d(bt,36,v);d(bt+1.75,36,v-20);d(bt+2,38,v-6)
        for j in range(8):d(bt+j*.5,42,v-36+(6 if j%2==0 else 0))
    elif kind=='halfdark':
        d(bt,36,v);d(bt+2,38,v+4)
        for j in range(4):d(bt+j,42,v-30)
    elif kind=='break':
        for t in (0,.75,2.25,2.5):d(bt+t,36,v-(0 if t in(0,2.5) else 10))
        for t in (1,3):d(bt+t,38,v+4)
        d(bt+3.75,38,v-24)
        for j in range(16):d(bt+j*.25,42,v-30 if j%2==0 else v-42)
    if crash is None:crash=b.i==0
    if crash:d(bt,49,v);d(bt,36,v)
    if fill:tom_fill(a,b,v)

# ================= 旧版を意識した暗いアナログ化(v9) =================
P_PAD=dict(kind='saw',det=(-12,0,12),cut=1100,a=.5,d=.4,sus=.85,r=1.0)
P_BASS=dict(kind='saw',cut=520,sub=.6,a=.005,d=.2,sus=.6,r=.08,cenv=2,cdec=.08)
P_PLK=dict(kind='sq',duty=.3,cut=2000,a=.002,d=.18,sus=0,r=.12,cenv=1.5,cdec=.05)
P_LEAD=dict(kind='saw',det=(-7,7),cut=3400,vib=.005,a=.02,d=.2,sus=.8,r=.25)
P_BRASS=dict(kind='saw',det=(-9,0,9),cut=1500,cenv=2.2,cdec=.25,a=.06,d=.3,sus=.75,r=.4)
P_DIST=dict(kind='saw',det=(-10,10),cut=2600,a=.005,d=.1,sus=.9,r=.08,dist=6,cab=3400)
P_EP=dict(kind='tri',cut=2600,a=.003,d=.6,sus=.25,r=.3)
P_BELL=dict(kind='sin',cut=8000,a=.002,d=.6,sus=0,r=.9)
P_STR=dict(kind='saw',det=(-10,0,10),cut=2200,a=.18,d=.3,sus=.8,r=.5)
P_VOX=dict(kind='tri',det=(-5,5),cut=2000,vib=.006,a=.15,d=.3,sus=.8,r=.5)
GROUP=[({'pad','st','str','lstr','swp','cpad','atm','glass','drone','opad','mpad','fid','pad2'},P_PAD,None),
       ({'bass','cb','fb','tuba','sbass'},P_BASS,None),
       ({'arp','carp','pizz','mar','harp','dul','clav'},P_PLK,(.33,.4,.45)),
       ({'gtr','rhy','ch2'},P_DIST,None),
       ({'ep','epc','pno'},P_EP,(.33,.3,.3)),
       ({'glk','cel','crys','bell','mbox','beep','glitch','vib'},P_BELL,(.4,.45,.5)),
       ({'br','tb','tbn','sbr','cs','hn'},P_BRASS,None),
       ({'cho','chp','ooh','voice','vox'},P_VOX,None),
       ({'run','vhi','vln','vc'},P_STR,None)]
DM={'01_title':{'cs':P_BRASS,'lead':P_LEAD,'vox':P_VOX},'04_battle':{'lead':P_LEAD,'lead2':P_DIST,'cs':P_BRASS},
    '06_boss':{'cs':P_BRASS,'lead':P_LEAD,'vox':P_VOX},'07_lastdungeon':{'vc':P_STR,'vox':P_VOX,'cs':P_BRASS},
    '42_battle_org':{'lead':P_DIST,'cs':P_BRASS},'43_boss_raid':{'lead':P_LEAD,'vox':P_VOX},'10_voyage':{'cs':P_BRASS,'lead':P_LEAD},
    '37_end_escape':{'lead':P_LEAD,'vox':P_VOX,'cs':P_BRASS},'38_end_counter':{'cs':P_BRASS,'lead':P_LEAD},'40_end_cyber':{'vox':P_VOX},'36_end_win':{'cs':P_BRASS}}
DARK=True
def darken(a,mains):
    allm=set(x for v in (mains.values() if isinstance(mains,dict) else [mains or []]) for x in v)
    cfg=a.song.cfg;over=DM.get(a.name,{})
    for k,c in cfg.items():
        if k=='drums':c['syn']='drums';c['rev']=max(c['rev'],.18);continue
        if k in over:c['syn']=dict(over[k]);c['rev']=max(c['rev'],.3);continue
        if k in allm:c['rev']=c['rev']+.08;continue
        for names,P,dl in GROUP:
            if k in names:
                c['syn']=dict(P);c['rev']=max(c['rev'],.3)
                if dl:c['delay']=dl
                break
        else:
            if not c.get('syn'):c['lp']=3200;c['rev']=c['rev']+.08
