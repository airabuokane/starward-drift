import sys
from arr9 import *
def dup(a,sec,txt,vel,tr=0):return [(a,txt,vel,tr)]

def t12():
    A='C#m A E B C#m A F#m G#';B='A B G#m C#m A B E G#'
    MA='G#5:1.5! E5:.5 C#5:1 | E5:2 A5:1 | B5:1.5 G#5:.5 E5:1 | D#5:3 | G#5:1.5 B5:.5 C#6:1! | C#6:2 A5:1 | A5:1 F#5:1 C#5:1 | C6:3'
    return T('12_ice',[('A',A,0,80),('B',B,1,80),('A2',A,1,80)],{'cel':(8,0,.5,0),'vln':(P_STR,-1,.45,.15),'harp':(46,-8,.4,-.35)},
      {'A':[('cel',MA,84,-12)],'B':[('vln','E5:1 A5:1 C#6:1! | D#6:2 B5:1 | B5:1.5 G#5:.5 D#5:1 | E5:3 | C#6:1 E6:1 A6:1! | F#6:1.5 D#6:.5 B5:1 | G#5:1 B5:1 E6:1 | D#6:2 C6:1',86,-12),('cel','E5:1 A5:1 C#6:1 | D#6:2 B5:1 | B5:1.5 G#5:.5 D#5:1 | E5:3 | C#6:1 E6:1 A6:1 | F#6:1.5 D#6:.5 B5:1 | G#5:1 B5:1 E6:1 | D#6:2 C6:1',60,-12)],
       'A2':[('cel',MA,86,-12),('vln','E4:3 | C#4:3 | B3:3 | B3:3 | E4:3 | C#4:3 | C#4:3 | C4:3',54,0)]},
      {'A':['cel'],'B':['vln'],'A2':['cel']},style='waltz',bpb=3,target=-18,arp=True,extra=lambda a:[comp(a,b,'harp','arpup',58,lo=55,div=.5) for b in a.bars()])

def t13():
    def ex(a):
        a.stem('taiko',116,-6,.3,0)
        for b in a.bars():
            if b.sec!='C':drums(a,b,'tribal',80+b.lv*8,crash=False)
    return T('13_ruins',[('A','Fm Gb Fm Gb Fm Gb Eb Fm',1,100),('B','Db Eb Fm Fm Bbm Gb Eb F',2,100),('C','Fm Fm Bbm Fm',0,(92,100,1))],
      {'sitar':(104,0,.35,0),'vox':(P_VOX,-1,.5,0),'shk':(77,0,.45,0)},
      {'A':[('sitar','F4:.5 Gb4:.5 Ab4:1 C5:1.5! Bb4:.5 | Ab4:1 Gb4:1 F4:2 | C5:.5 Db5:.5 C5:1 Bb4:.5 Ab4:.5 Gb4:1 | F4:3 r:1 | F5:1! Eb5:.5 Db5:.5 C5:1 Bb4:1 | Bb4:.5 Db5:.5 Gb5:1.5! F5:.5 Eb5:1 | Eb5:1 Db5:1 C5:1 Bb4:1 | C5:3 r:1',90,0)],
       'B':[('sitar','Ab5:2! F5:1 Db5:1 | Bb5:2 G5:1 Eb5:1 | C6:3! Bb5:.5 Ab5:.5 | Ab5:1 Gb5:1 F5:2 | Db6:1.5! C6:.5 Bb5:1 F5:1 | Bb5:1 Db6:1 Gb6:2! | G5:1 Bb5:1 Eb6:2 | A5:3! r:1',98,0),('vox','Ab5:2 F5:1 Db5:1 | Bb5:2 G5:1 Eb5:1 | C6:3 Bb5:.5 Ab5:.5 | Ab5:1 Gb5:1 F5:2 | Db6:1.5 C6:.5 Bb5:1 F5:1 | Bb5:1 Db6:1 Gb6:2 | G5:1 Bb5:1 Eb6:2 | A5:3 r:1',90,-12)],
       'C':[('shk','C5:3 Bb4:.5 Ab4:.5 | G4:4 | F4:2 Db5:2 | C5:4',82,0)]},
      {'A':['sitar'],'B':['sitar','vox'],'C':['shk']},style='tribal',target=-16,arp=True,extra=ex)

def t14():
    def ex(a):
        a.lvvol('acc',{'A':0,'B':0,'C':8})
        for b in a.bars(only=['A','B']):comp(a,b,'acc','stab_off',70 if b.sec=='A' else 78,lo=55)
    return T('14_pirate',[('A','Em D Em B Em D C_D Em',2,160),('B','C D G Em C D B B',3,164),('C','Em C D B',1,(136,160,1))],
      {'fid':(110,0,.3,0),'vox':(P_VOX,-2,.4,0),'acc':(21,-8,.3,-.35)},
      {'A':[('fid','B4:.5 B4:.5 E5:.5 G5:.5 B5:1! G5:1 | A5:1 F#5:.5 E5:.5 D5:1 A4:1 | G4:.5 A4:.5 B4:1 E5:1 G5:1 | F#5:2! D#5:1 B4:1 | B4:.5 B4:.5 E5:.5 G5:.5 B5:1! A5:1 | A5:.5 G5:.5 F#5:.5 E5:.5 D5:1 A4:1 | G4:.5 C5:.5 E5:1 F#5:.5 A5:.5 D6:1 | E5:2! r:2',94,0)],
       'B':[('fid','E6:1.5! C6:.5 G5:1 C6:1 | F#6:1.5! D6:.5 A5:1 D6:1 | B5:2 D6:1 G6:1! | E6:3 B5:1 | G5:.5 A5:.5 B5:1 E6:1 G6:1! | F#6:1.5 D6:.5 A5:1 F#5:1 | D#6:1 F#6:1 B6:1.5! A6:.5 | F#6:2 D#6:2',104,0),('vox','E6:1.5 C6:.5 G5:1 C6:1 | F#6:1.5 D6:.5 A5:1 D6:1 | B5:2 D6:1 G6:1 | E6:3 B5:1 | G5:.5 A5:.5 B5:1 E6:1 G6:1 | F#6:1.5 D6:.5 A5:1 F#5:1 | D#6:1 F#6:1 B6:1.5 A6:.5 | F#6:2 D#6:2',94,-24)],
       'C':[('acc','E4:1 G4:1 B4:2 | E4:1 G4:1 C5:2 | F#4:1 A4:1 D5:2 | D#5:2 B4:2',92,0)]},
      {'A':['fid'],'B':['fid','vox'],'C':['acc']},style='darksynth',target=-14,arp=False,extra=ex)

def t15():
    return T('15_vector',[('A','Ebm B Gb Db Ebm B Ab Bb',0,76),('B','B Db Bbm Ebm B Db Gb Gb',1,80),('C','B Db Ebm Bbm B Db Gb Gb',2,84)],
      {'pno':(0,0,.4,0),'str':(P_STR,0,.45,.15),'vox':(P_VOX,-1,.5,0)},
      {'A':[('pno','Bb4:1 Eb5:1 Gb5:2! | F#5:1 D#5:1 B4:2 | Db5:1 Gb5:1 Bb5:2! | Ab5:3 r:1 | Bb5:1 Gb5:1 Eb5:2 | D#5:1 F#5:1 B5:2! | C6:1 Ab5:1 Eb5:1 C5:1 | D5:4',80,0)],
       'B':[('str','D#5:2 F#5:2 | F5:2 Ab5:2 | Db6:3! Bb5:1 | Gb5:4 | F#5:2 B5:2 | Ab5:3! F5:1 | Db6:2 Bb5:2 | Gb5:4',86,0)],
       'C':[('str','B5:2 D#6:2 | F6:2 Ab6:2! | Gb6:3 Eb6:1 | F6:4 | D#6:2 F#6:2 | Ab6:3! F6:1 | Bb6:2 Db7:2! | Gb6:4',96,-12),('vox','B5:2 D#6:2 | F6:2 Ab6:2 | Gb6:3 Eb6:1 | F6:4 | D#6:2 F#6:2 | Ab6:3 F6:1 | Bb6:2 Db7:2 | Gb6:4',90,-24)]},
      {'A':['pno'],'B':['str'],'C':['str','vox']},style='ambient',target=-17,extra=lambda a:([comp(a,b,'pno','arp8',52,lo=50) for b in a.bars(only=['B','C'])],a.lvvol('pno',{'A':0,'B':-6,'C':-6})))

def t16():
    A='Cm7 Ab7 Dm7b5_G7 Cm7 Fm7 Bb7 EbM7 Dm7b5_G7';B='Fm7 Bb7 EbM7 AbM7 Dm7b5 G7 Cm7 Dm7b5_G7'
    MA='G5:.667! Eb5:.333 C5:1 r:.667 D5:.333 Eb5:1 | Gb5:1.5! Eb5:.5 C5:1 Ab4:1 | F5:1 Ab5:1 B5:1 D6:1! | C6:3 r:1 | Ab5:.667 C6:.333 Eb6:1! C6:1 Ab5:1 | D6:1.5 Bb5:.5 Ab5:1 F5:1 | G5:1 Bb5:1 D6:2! | C6:1 Ab5:1 G5:1 F5:1'
    MB='C6:.667! Eb6:.333 F6:1.5! Eb6:.5 C6:1 | D6:1 Ab5:1 Bb5:2 | G6:1.5! F6:.5 Eb6:1 Bb5:1 | C6:3 r:1 | Ab6:1! F6:.667 D6:.333 Ab5:1 F5:1 | B5:1 D6:1 F6:1 Ab6:1! | G6:2 Eb6:2 | D6:1 F6:1 B5:1 G5:1'
    return T('16_casino',[('A',A,2,164),('B',B,3,164),('A2',A,2,164)],{'sax':(65,0,.35,0),'cs':(P_BRASS,-1,.4,.2),'ep':(P_EP,-9,.35,-.3)},
      {'A':[('sax',MA,94,-12)],'B':[('sax',MB,104,-12),('cs',MB,96,-12)],'A2':[('sax',MA,98,-12),('cs',MA,80,-24)]},
      {'A':['sax'],'B':['sax','cs'],'A2':['sax']},style='swing',target=-15,arp=False,extra=lambda a:[comp(a,b,'ep','swingcomp',60,lo=53) for b in a.bars()])

def t17():
    return T('17_corp',[('A','Bbm Gb Db Ab Bbm Gb Ebm F',1,118),('B','Gb Ab Fm Bbm Gb Ab Db F',2,118),('A2','Bbm Gb Db Ab Bbm Gb Ebm F',2,118)],
      {'lead':(P_HOLLOW,0,.4,0),'cs':(P_BRASS,-2,.4,.15)},
      {'A':[('lead','F5:.5 Bb4:.5 Db5:1 F5:1.5! Eb5:.5 | Db5:1 Bb4:1 Gb4:2 | Ab4:.5 Db5:.5 F5:1 Ab5:1.5! Gb5:.5 | Eb5:3 r:1 | Db6:1! C6:.5 Bb5:.5 F5:1 Db5:1 | Eb5:1 Gb5:1 Bb5:2 | Gb5:1 Eb5:1 Bb4:1 Gb5:1 | A5:2! F5:2',84,0)],
       'B':[('lead','Bb5:1.5! Gb5:.5 Db6:2 | C6:1.5! Ab5:.5 Eb6:2 | F6:1 Eb6:1 C6:1 Ab5:1 | Bb5:3 r:1 | Db6:1 Eb6:1 F6:1.5! Gb6:.5 | Eb6:1 C6:1 Ab5:2 | F6:2! Db6:1 Ab5:1 | C6:2 A5:2',94,-12),('cs','Bb5:1.5 Gb5:.5 Db6:2 | C6:1.5 Ab5:.5 Eb6:2 | F6:1 Eb6:1 C6:1 Ab5:1 | Bb5:3 r:1 | Db6:1 Eb6:1 F6:1.5 Gb6:.5 | Eb6:1 C6:1 Ab5:2 | F6:2 Db6:1 Ab5:1 | C6:2 A5:2',86,-24)],
       'A2':[('lead','F5:.5 Bb4:.5 Db5:1 F5:1.5! Eb5:.5 | Db5:1 Bb4:1 Gb4:2 | Ab4:.5 Db5:.5 F5:1 Ab5:1.5! Gb5:.5 | Eb5:3 r:1 | Db6:1! C6:.5 Bb5:.5 F5:1 Db5:1 | Eb5:1 Gb5:1 Bb5:2 | Gb5:1 Eb5:1 Bb4:1 Gb5:1 | A5:2! F5:2',90,0)]},
      {'A':['lead'],'B':['lead','cs'],'A2':['lead']},style='darkchill',target=-16)

def t18():
    A='DM7 Em7_A7 DM7 Bm7 Em7 A7 F#m7_B7 Em7_A7';B='GM7 F#m7 Em7 A7 GM7 F#m7_B7 Em7 A7sus4_A7'
    MA='F#5:1.5! A5:.5 C#6:1 A5:1 | G5:1 E5:.5 C#5:.5 E5:2 | D5:.5 F#5:.5 A5:1 C#6:1.5! B5:.5 | B5:3 r:1 | G5:1.5 B5:.5 D6:1! B5:1 | C#6:1 A5:1 G5:2 | F#5:1 A5:1 D#5:1 F#5:1 | E5:2 C#5:2'
    return T('18_resort',[('A',A,1,128),('B',B,2,128),('A2',A,1,128)],{'fl':(73,0,.4,0),'ng':(24,-6,.25,-.3),'vib':(P_BELL,-12,.45,.35)},
      {'A':[('fl',MA,82,0)],'B':[('fl','B5:1 D6:1 F#6:1.5! D6:.5 | C#6:1 A5:1 F#5:2 | G5:.5 B5:.5 D6:1 E6:1.5! D6:.5 | C#6:3 r:1 | D6:1.5! B5:.5 G5:1 D6:1 | C#6:1 A5:1 D#6:1 F#6:1 | E6:2! D6:1 B5:1 | D6:2 C#6:2',90,0)],'A2':[('fl',MA,84,0)]},
      ['fl'],style='bossa',target=-17,arp=False,extra=lambda a:[comp(a,b,'ng','bossa_gtr',70,lo=55) for b in a.bars()])

def t19():
    def ex(a):
        a.lvvol('bass',{'A':0,'B':0,'C':6})
        a.stem('clav',None,-9,.15,-.35);a.song.cfg['clav']['syn']=dict(P_PLK)
        for b in a.bars(only=['A','B']):
            for (off,dur,r,q) in b.ch:
                for t in (.25,.75,1.75,2.25,3.25):
                    if t<dur:
                        for p_ in voic(r,q,58)[:3]:a.n('clav',b.bt+off+t,.15,p_,70)
    return T('19_terminal',[('A','Cm7 F7 Cm7 F7 AbM7 G7 Cm7 F7',1,108),('B','AbM7 Bb Gm7 Cm7 AbM7 Bb G7 G7',2,108),('C','Cm7 F7 Cm7 F7',1,108)],
      {'lead':(P_SOFT,0,.35,0),'cs':(P_BRASS,-1,.35,.2)},
      {'A':[('lead','G4:.5 Bb4:.5 C5:.5 r:.5 Eb5:.5 C5:.5 Bb4:1 | A4:.5 C5:.5 Eb5:1! D5:.5 C5:.5 A4:1 | G4:.5 Bb4:.5 C5:.5 Eb5:.5 G5:1! F5:1 | F5:.5 Eb5:.5 C5:1 A4:2 | C5:.5 Eb5:.5 G5:1 Ab5:1.5! G5:.5 | F5:1 D5:.5 B4:.5 G4:2 | C5:.5 D5:.5 Eb5:.5 G5:.5 C6:1! Bb5:1 | A5:2 F5:2',88,12)],
       'B':[('lead','Eb5:1 C5:.5 Eb5:.5 G5:1.5! Ab5:.5 | F5:1 D5:.5 F5:.5 Bb5:2! | D5:1 Bb4:.5 D5:.5 F5:1 G5:1 | Eb5:3 r:1 | C6:1.5! Bb5:.5 Ab5:1 G5:1 | F5:1 Bb5:1 D6:2! | B5:1 G5:1 D5:1 F5:1 | G5:2 r:2',96,12),('cs','Eb5:1 C5:.5 Eb5:.5 G5:1.5 Ab5:.5 | F5:1 D5:.5 F5:.5 Bb5:2 | D5:1 Bb4:.5 D5:.5 F5:1 G5:1 | Eb5:3 r:1 | C6:1.5 Bb5:.5 Ab5:1 G5:1 | F5:1 Bb5:1 D6:2 | B5:1 G5:1 D5:1 F5:1 | G5:2 r:2',88,0)]},
      {'A':['lead'],'B':['lead','cs'],'C':['bass']},style='funk',target=-15,arp=False,extra=ex)

def t20():
    def ex(a):
        a.stem('ag',25,-6,.2,-.35);a.stem('banjo',105,-10,.2,.4)
        for b in a.bars():comp(a,b,'ag','strum',70,lo=52);comp(a,b,'banjo','pluck8',62,lo=60)
    return T('20_frontier',[('A','Am G F E Am G F_E Am',1,116),('B','F G C Am F G E E',2,120),('A2','Am G F E Am G F_E Am',2,116)],
      {'harm':(22,0,.35,0),'whis':(78,-2,.4,.1)},
      {'A':[('harm','E4:1.5! A4:.5 C5:1 A4:1 | B4:1.5 D5:.5 G4:2 | A4:1 C5:1 F5:1.5! E5:.5 | E5:3 r:1 | A4:1.5 C5:.5 E5:1 A5:1! | G5:1 D5:1 B4:2 | A4:1 C5:1 G#4:1 B4:1 | A4:3 r:1',86,0)],
       'B':[('whis','C5:1 F5:1 A5:2! | B5:1.5 A5:.5 G5:2 | E5:1 G5:1 C6:2! | A5:3 E5:1 | F5:1.5 G5:.5 A5:1 C6:1! | B5:1 G5:1 D5:2 | E5:1 G#5:1 B5:1 D6:1 | E6:4!',90,0),('harm','C5:1 F5:1 A5:2 | B5:1.5 A5:.5 G5:2 | E5:1 G5:1 C6:2 | A5:3 E5:1 | F5:1.5 G5:.5 A5:1 C6:1 | B5:1 G5:1 D5:2 | E5:1 G#5:1 B5:1 D6:1 | E6:4',84,-12)],
       'A2':[('harm','E4:1.5! A4:.5 C5:1 A4:1 | B4:1.5 D5:.5 G4:2 | A4:1 C5:1 F5:1.5! E5:.5 | E5:3 r:1 | A4:1.5 C5:.5 E5:1 A5:1! | G5:1 D5:1 B4:2 | A4:1 C5:1 G#4:1 B4:1 | A4:3 r:1',92,0)]},
      {'A':['harm'],'B':['whis','harm'],'A2':['harm']},style='western',target=-15,arp=False,extra=ex)

def t21():
    def ex(a):
        a.stem('taiko',116,-5,.25,0);a.stem('anv',114,-12,.2,.35);a.stem('dist',None,-10,.12,-.4);a.song.cfg['dist']['syn']=dict(P_DIST)
        a.lvvol('taiko',{'A':0,'B':0,'C':-4})
        for b in a.bars():
            drums(a,b,'tribal',90,crash=False);comp(a,b,'dist','power8',78)
            for t in (.5,1.5,2.5,3.5):a.n('anv',b.bt+t,.2,fold(b.r,72,83),70 if b.sec!='C' else 90)
            if b.sec=='C':[a.n('taiko',b.bt+j*.25,.2,45 if j%2 else 52,70+j*2) for j in range(16)]
    return T('21_mining',[('A','Gm Gm Eb D Gm Gm Cm D',1,100),('B','Cm Gm Eb D Cm Gm Ab D',2,104),('C','Gm Gm Gm D',2,104)],
      {'bari':(67,0,.3,0),'lgt':(P_DIST,-2,.2,.1)},
      {'A':[('bari','G2:1! G2:.5 Bb2:.5 D3:1 C3:1 | Bb2:.5 A2:.5 G2:1 D2:2 | Eb2:1 G2:1 Bb2:1 Eb3:1! | D3:3 F#2:1 | G2:1! G2:.5 Bb2:.5 D3:1 F3:1 | G3:2! D3:2 | Eb3:1 D3:1 C3:1 G2:1 | A2:2 F#2:2',96,12)],
       'B':[('bari','C3:1 Eb3:1 G3:1.5! F3:.5 | D3:1 Bb2:1 G2:2 | Bb2:1 Eb3:1 G3:1 Bb3:1! | A3:3 F#3:1 | G3:1 C4:1 Eb4:1.5! D4:.5 | Bb3:1 G3:1 D3:2 | C3:1 Eb3:1 Ab3:1 C4:1 | D4:3! r:1',104,12),('lgt','C3:1 Eb3:1 G3:1.5 F3:.5 | D3:1 Bb2:1 G2:2 | Bb2:1 Eb3:1 G3:1 Bb3:1 | A3:3 F#3:1 | G3:1 C4:1 Eb4:1.5 D4:.5 | Bb3:1 G3:1 D3:2 | C3:1 Eb3:1 Ab3:1 C4:1 | D4:3 r:1',96,12)]},
      {'A':['bari'],'B':['bari','lgt'],'C':[]},style='industrial',target=-14,arp=False,extra=ex)

def t22():
    def ex(a):
        a.stem('mar',12,-7,.25,-.35)
        for b in a.bars():comp(a,b,'mar','arp16',60,lo=55)
    MA='F5:1 Db5:.5 Bb4:.5 F5:1 Ab5:1! | Gb5:1.5 F5:.5 Db5:2 | Eb5:.5 Gb5:.5 Bb5:1.5! Ab5:.5 Gb5:1 | F5:3 r:1 | Bb5:1! Ab5:.5 F5:.5 Db5:1 F5:1 | Gb5:1 Bb5:1 Db6:2! | C6:1 Ab5:1 Eb5:1 C5:1 | C5:2 Eb5:1 A5:1'
    return T('22_lab',[('A','Bbm Gb Ebm F Bbm Gb Ab F',1,126),('B','Gb Ab Fm Bbm Ebm Ab Db F',2,126),('A2','Bbm Gb Ebm F Bbm Gb Ab F',1,126)],
      {'vib':(11,0,.4,0)},
      {'A':[('vib',MA,84,0)],'B':[('vib','Bb5:1 Db6:1 Gb6:2! | Ab5:1 C6:1 Eb6:2 | C6:1.5 Ab5:.5 F5:1 Ab5:1 | Bb5:3 r:1 | Gb5:1 Bb5:1 Eb6:1.5! Db6:.5 | C6:1 Ab5:1 Eb5:2 | F5:1 Ab5:1 Db6:1 F6:1! | E6:2 C6:1 A5:1',94,0)],'A2':[('vib',MA,88,12)]},
      ['vib'],style='darkchill',target=-17,arp=False,extra=ex)

def t23():
    def ex(a):
        a.stem('ag',25,-6,.2,-.35);a.stem('acc',21,-12,.3,.3)
        for b in a.bars():comp(a,b,'ag','pluck8',66,lo=50);comp(a,b,'acc','stab_off',54,lo=55)
    MA='D5:1 B4:.5 D5:.5 G5:1.5! A5:.5 | B5:1 G5:1 E5:2 | E5:1 G5:.5 E5:.5 C5:1 E5:1 | D5:3 r:1 | D5:1 G5:1 B5:1.5! A5:.5 | G5:1 E5:1 B4:2 | C5:1 E5:1 D5:1 F#5:1 | G5:3 r:1'
    return T('23_farm',[('A','G Em C D G Em Am_D G',1,96),('B','C D Bm Em C D G G',2,96),('A2','G Em C D G Em Am_D G',1,96)],
      {'whis':(78,0,.4,0),'fid':(110,-2,.35,.15)},
      {'A':[('whis',MA,82,0)],'B':[('whis','E5:1 G5:1 C6:2! | D6:1.5 C6:.5 A5:2 | B5:1 D6:1 F#5:2 | G5:3 r:1 | C6:1! B5:1 A5:1 G5:1 | F#5:1 A5:1 D6:2! | B5:2 A5:1 G5:1 | G5:4',90,0),('fid','E5:1 G5:1 C6:2 | D6:1.5 C6:.5 A5:2 | B5:1 D6:1 F#5:2 | G5:3 r:1 | C6:1 B5:1 A5:1 G5:1 | F#5:1 A5:1 D6:2 | B5:2 A5:1 G5:1 | G5:4',82,-12)],'A2':[('whis',MA,84,0)]},
      {'A':['whis'],'B':['whis','fid'],'A2':['whis']},style='folk',target=-17,arp=False,extra=ex)

def t24():
    def ex(a):
        a.stem('anv',114,-10,.25,.4)
        for b in a.bars():
            for t in (1,3):a.n('anv',b.bt+t,.2,fold(b.r,76,87),64 if b.sec!='C' else 90)
            if b.sec=='intro':
                for t in (0,1.5,3):a.n('anv',b.bt+t,.3,fold(b.r,76,87),100)
    return T('24_shipyard',[('intro','Dm A',2,120),('A','Dm Bb F C Dm Bb Gm A',2,120),('B','Bb C Am Dm Bb C Gm_A Dm',3,124),('C','Dm Dm Bb A',1,120)],
      {'hn':(60,0,.35,0),'cs':(P_BRASS,-1,.4,.2)},
      {'A':[('hn','A3:.75! A3:.25 D4:1 F4:1.5! E4:.5 | D4:1 Bb3:1 F3:2 | A3:.75 A3:.25 C4:1 F4:1 A4:1! | G4:2 E4:2 | A3:.75! A3:.25 D4:1 F4:1 A4:1! | Bb4:1.5 A4:.5 F4:2 | D4:1 G4:1 Bb4:1 G4:1 | A4:3! r:1',92,0)],
       'B':[('hn','F4:1.5! D4:.5 Bb3:1 D4:1 | E4:1 G4:1 C5:2 | C5:1.5 A4:.5 E4:1 A4:1 | D5:3! A4:1 | Bb4:1 D5:1 F5:1.5! D5:.5 | E5:1 C5:1 G4:2 | Bb4:1 D5:1 C#5:1 E5:1 | D5:3! r:1',100,0),('cs','F4:1.5 D4:.5 Bb3:1 D4:1 | E4:1 G4:1 C5:2 | C5:1.5 A4:.5 E4:1 A4:1 | D5:3 A4:1 | Bb4:1 D5:1 F5:1.5 D5:.5 | E5:1 C5:1 G4:2 | Bb4:1 D5:1 C#5:1 E5:1 | D5:3 r:1',94,12)]},
      {'intro':[],'A':['hn'],'B':['hn','cs'],'C':[]},style='march',target=-15,arp=False,extra=ex)

def t25():
    def ex(a):
        a.stem('ag',25,-8,.2,-.35)
        for b in a.bars():comp(a,b,'ag','arp8',60,lo=52)
    MA='D5:1 F5:1 Bb5:1.5! A5:.5 | G5:2 D5:2 | Eb5:1 G5:1 Bb5:1 G5:1 | F5:3 r:1 | D5:1 F5:1 C6:1.5! Bb5:.5 | Bb5:1 G5:1 D5:2 | Eb5:1 G5:1 F5:1 Eb5:1 | C5:3 r:1'
    return T('25_residential',[('A','Bb Gm Eb F Bb Gm Eb F',1,90),('B','Eb F Dm Gm Eb F Bb_Gm Eb_F',2,90),('A2','Bb Gm Eb F Bb Gm Eb F',1,90)],
      {'pno':(0,0,.35,0),'str':(P_STR,-1,.45,.15)},
      {'A':[('pno',MA,80,0)],'B':[('pno','G5:1 Bb5:1 Eb6:2! | F5:1 A5:1 C6:2 | D6:1.5! C6:.5 A5:1 F5:1 | G5:3 r:1 | Eb6:1 D6:1 Bb5:1 G5:1 | A5:1 C6:1 F6:2! | D6:2 Bb5:2 | G5:2 A5:2',88,0),('str','G5:1 Bb5:1 Eb6:2 | F5:1 A5:1 C6:2 | D6:1.5 C6:.5 A5:1 F5:1 | G5:3 r:1 | Eb6:1 D6:1 Bb5:1 G5:1 | A5:1 C6:1 F6:2 | D6:2 Bb5:2 | G5:2 A5:2',82,-12)],'A2':[('pno',MA,84,0)]},
      {'A':['pno'],'B':['pno','str'],'A2':['pno']},style='darkchill',target=-17,extra=ex)

def t26():
    MA='E5:1.5! C5:.5 A4:1 | B4:1 D5:1 G#5:1 | A5:2! E5:1 | C5:3 | D5:1 F5:1 A5:1 | C6:2! A5:1 | B5:1.5 G#5:.5 E5:1 | A5:3'
    return T('26_oldresort',[('A','Am E Am Am Dm Am E Am',1,124),('B','C G C Am F C Dm E',2,124),('A2','Am E Am Am Dm Am E Am',1,(124,112,2))],
      {'acc':(21,0,.4,0),'vln':(40,-1,.45,.2),'ep':(P_EP,-8,.4,-.3)},
      {'A':[('acc',MA,84,0)],'B':[('acc','G5:1 C6:1 E6:1! | D6:2 B5:1 | C6:1.5 B5:.5 G5:1 | A5:3 | A5:1 C6:1 F6:1! | E6:2 C6:1 | D6:1.5 C6:.5 B5:1 | G#5:3',90,0),('vln','G5:1 C6:1 E6:1 | D6:2 B5:1 | C6:1.5 B5:.5 G5:1 | A5:3 | A5:1 C6:1 F6:1 | E6:2 C6:1 | D6:1.5 C6:.5 B5:1 | G#5:3',84,-12)],'A2':[('acc',MA,82,0)]},
      {'A':['acc'],'B':['acc','vln'],'A2':['acc']},style='waltz',bpb=3,target=-17,arp=False,extra=lambda a:[comp(a,b,'ep','waltz',56,lo=55) for b in a.bars()])

ALL=['t12','t13','t14','t15','t16','t17','t18','t19','t20','t21','t22','t23','t24','t25','t26']
if __name__=='__main__':
    for f in (sys.argv[1:] or ALL):print('==',f);globals()[f]()
