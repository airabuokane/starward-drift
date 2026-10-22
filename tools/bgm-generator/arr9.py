"""v10: 1から作り直し用の汎用アレンジャ(旧版の暗いアナログ・サイバーパンク)"""
import numpy as np
import kit
from kit import *
kit.DARK=False   # darken() は使わず、ここで音色を直接決める
P_SOFT=dict(kind='tri',det=(-4,4),cut=2600,vib=.004,a=.02,d=.3,sus=.7,r=.3)
P_HOLLOW=dict(kind='sq',duty=.5,det=(-5,5),cut=1800,vib=.004,a=.03,d=.3,sus=.7,r=.35)
P_SUB=dict(kind='sin',cut=400,a=.3,d=.3,sus=.9,r=.8)
P_SWEEP=dict(kind='saw',det=(-15,0,15),cut=700,cenv=3,cdec=1.2,a=.8,d=.5,sus=.8,r=1.4)
def syn(p,**k):d=dict(p);d.update(k);return d
GM=lambda prog:prog
ST,SCI,CRY,ATM=97,103,98,99
def T(name,secs,stems,mel,mains,style='darkchill',bpb=4,loop='A',target=-15,tail=0,seed=0,extra=None,pad=True,arp=None,drumkit=True,bell=True,keep=None):
    if isinstance(mains,list):mains={x[0]:mains for x in secs}
    a=Arr(name,bpb=bpb,seed=seed or sum(map(ord,name)))
    for s_ in secs:a.sec(*s_)
    # 共通の土台
    rock=style=='rock'
    if rock:pad=True;bell=False;drumkit=False;arp=False
    if pad:a.stem('pad',17 if rock else None,-15 if rock else -13,.45,-.2)
    a.stem('bass',34 if rock else None,-6 if rock else -5,.06)
    if rock:a.stem('gL',30,-3,.12,-.55);a.stem('gR',30,-3,.12,.55)
    a.stem('arp',None,-13,.35,.35)
    a.stem('bell',None,-15,.5,.4)
    a.stem('drums',0,-5,.2,drum=True)
    for k,v in stems.items():
        prog,db,rev,pan=(v+(0,.3,0))[:4] if isinstance(v,tuple) else (v,0,.3,0)
        a.stem(k,prog if isinstance(prog,int) else None,db,rev,pan)
    a.build();a.nocy=True
    c=a.song.cfg
    if pad and not rock:c['pad']['syn']=dict(P_PAD)
    if pad and not rock:c['pad']['pump']={'darksynth':.4,'darkchill':.25}.get(style,0)
    if not rock:c['bass']['syn']=dict(P_BASS)
    c['arp']['syn']=dict(P_PLK);c['arp']['delay']=(.33,.4,.45)
    c['bell']['syn']=dict(P_BELL);c['bell']['delay']=(.4,.45,.5)
    if drumkit:c['drums']['syn']='drums';c['drums']['rev']=.22
    if rock:c['drums']['prog']=16;c['drums']['rev']=.14
    for k,v in stems.items():
        prog=v[0] if isinstance(v,tuple) else v
        if isinstance(prog,dict):c[k]['syn']=dict(prog)
    # メロディ
    allL=[]
    for sec,lst in mel.items():
        for st,txt,vel,tr in lst:
            L=a.mel(st,sec,txt,vel,tr,leg=.9 if style!='darksynth' else .88);allL+=[(st,x) for x in L]
    if bell:
        for st,(b_,d,p,acc) in allL:
            if d>=2 and st in set(x for v in mains.values() for x in v):a.n('bell',b_,1.2,p+12,64)
    arrange(a,style,arp)
    if extra:extra(a)
    meta=a.render(name,loop=loop,target=target,tail=tail,dbg=True,mains=mains)
    return a
def arrange(a,style,arp):
    for b in a.bars():
        lv=b.lv;v=b.v;sec=b.sec
        pre=sec.startswith('pre');bd=sec.startswith('bd');intro=sec.startswith('intro');out=sec.startswith('out')
        # パッド
        if 'pad' in a.song.cfg:comp(a,b,'pad','pad',50+lv*8,lo=52)
        if out and b.last:
            kime(a,b,[('pad',55)],110);a.n('bass',b.bt,b.B*1.5,fold(b.r,28,40),100);continue
        # ベース
        if style=='rock':
            bass(a,b,'bass',['root8','root8','oct8','oct8'][lv] if not bd else 'long',78+lv*6,lo=28,hi=40)
            if lv==0 or bd:comp(a,b,'gL','powerlong',70+lv*6,lo=40);comp(a,b,'gR','powerlong',66+lv*6,lo=40)
            else:comp(a,b,'gL','power8',76+lv*6,lo=40);comp(a,b,'gR','power8',72+lv*6,lo=40)
            if not(intro and lv==0):
                crash=b.i==0 and lv>=2
                drums(a,b,['half','rock','rock16','rock16'][lv] if not bd else 'half',88+lv*6,crash=crash or (lv==3 and b.i%2==0))
                if lv==3:
                    for t in (0,.25,2,2.25):a.d(b.bt+t,36,90)
            if pre and b.last:kime(a,b,[('pad',55)],118);tom_fill(a,b,100,1)
            elif pre:snare_roll(a,b,50+b.i*12,70+b.i*12,b.B,.5 if b.i<b.n-2 else .25)
            continue
        bk={'darksynth':['drone','pulse8','oct16','oct16'],'darkchill':['drone','drone','pulse8','pulse8'],'ambient':['drone']*4,
            'industrial':['pulse8','pulse8','gallop','oct16']}.get(style)
        if bk:sbass(a,b,'bass',bk[lv] if not bd else 'drone',70+lv*8)
        elif style=='swing':bass(a,b,'bass','walk',74+lv*6,lo=33,hi=45)
        elif style=='march':bass(a,b,'bass','tuba',80+lv*4,lo=33,hi=45)
        elif style=='bossa':bass(a,b,'bass','bossa',74,lo=33,hi=45)
        elif style=='waltz':bass(a,b,'bass','waltz',74,lo=33,hi=45)
        elif style in('western','folk','tribal'):bass(a,b,'bass','root4',72+lv*4,lo=33,hi=45)
        elif style=='funk':bass(a,b,'bass','funk',86,lo=28,hi=40)
        # アルペジオ(やまびこ付き)
        if (arp if arp is not None else style in('darkchill','darksynth','ambient','industrial')) and lv>=1 and not bd:
            comp(a,b,'arp','arp16' if style in('darksynth','industrial') else 'arp8',56+lv*6,lo=60)
        # ドラム
        crash=b.i==0 and lv>=2
        if intro and lv==0:continue
        if style=='darksynth':
            k=['halfdark','halfdark','break','dark4'][lv] if not bd else 'halfdark'
            ddrums(a,b,k,80+lv*8,crash=crash or (lv==3 and b.i%2==0),fill=b.last and not bd)
        elif style=='industrial':
            ddrums(a,b,['halfdark','break','gated','dark4'][lv],84+lv*6,crash=crash,fill=b.last)
            for t in (.5,1.5,2.5,3.5):a.d(b.bt+t,46,50+lv*6)
        elif style=='darkchill':
            ddrums(a,b,['slow','slow','gated','gated'][lv],66+lv*8,crash=crash and lv>=2)
        elif style=='ambient':
            if lv>=1:ddrums(a,b,'halfdark',60+lv*8,crash=False)
        elif style=='swing':drums(a,b,'swing',80+lv*6,crash=crash)
        elif style=='march':drums(a,b,'march',84+lv*6,crash=crash)
        elif style=='bossa':drums(a,b,'bossa',80,crash=False)
        elif style=='waltz':drums(a,b,'waltz',70+lv*4,crash=False)
        elif style=='western':drums(a,b,'train',80+lv*6,crash=crash)
        elif style=='folk':
            if lv>=1:drums(a,b,'brush',76+lv*4,crash=False)
        elif style=='tribal':
            if 'taiko' in a.stems:drums(a,b,'tribal',76+lv*8,crash=False)
            for j in range(8):a.d(b.bt+j*.5,69,44)
        elif style=='funk':drums(a,b,'funk',88+lv*4,crash=crash)
        # 盛り上げ(サビ前の最後はキメ)
        if pre and b.last:
            kime(a,b,[('pad',55)],118);tom_fill(a,b,100,1)
        elif pre:
            snare_roll(a,b,50+b.i*12,70+b.i*12,b.B,.5 if b.i<b.n-2 else .25)
