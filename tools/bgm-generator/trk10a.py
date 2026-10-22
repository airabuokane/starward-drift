import sys
from arr9 import *

def t01():
    return T('01_title',[('intro','Am F C G',0,84),('A','Am F C G Am F Dm E',1,92),('pre','F G Em Am',2,(92,96)),('B','F G C Am F G E E',3,96),('bd','Dm Am Dm E',1,(88,92,1))],
      {'cs':(P_BRASS,0,.45,0),'lead':(P_LEAD,0,.4,.05),'ep':(P_EP,-1,.4,.2),'st':(ST,-11,.5,0)},
      {'intro':[('ep','A4:2 E4:2 | C5:2 A4:2 | G4:2 E4:2 | B4:2 D5:2',60,0)],
       'A':[('cs','E4:1 A4:1 C5:1.5! B4:.5 | A4:2 F4:1 A4:1 | G4:1 C5:1 E5:1.5! D5:.5 | D5:3 r:1 | E5:1 A5:1 G5:1.5! E5:.5 | F5:2 C5:1 A4:1 | D5:1 F5:1 A5:1 G5:1 | G#5:3 r:1',86,0)],
       'pre':[('lead','A4:1 C5:1 F5:1 E5:1 | D5:1 B4:1 G5:1 F5:1 | E5:.5 D5:.5 B4:.5 G4:.5 B4:.5 E5:.5 G5:.5 B5:.5 | A5:1! r:3',88,0)],
       'B':[('lead','A5:1.5! G5:.5 F5:1 C5:1 | B5:1.5! A5:.5 G5:1 D5:1 | G5:1 E5:1 C5:1 E5:1 | A5:3! E5:1 | F5:1 A5:1 C6:1.5! B5:.5 | B5:1 G5:1 D5:2 | E5:1 G#5:1 B5:1 D6:1 | E6:3! r:1',100,0),
            ('cs','A5:1.5 G5:.5 F5:1 C5:1 | B5:1.5 A5:.5 G5:1 D5:1 | G5:1 E5:1 C5:1 E5:1 | A5:3 E5:1 | F5:1 A5:1 C6:1.5 B5:.5 | B5:1 G5:1 D5:2 | E5:1 G#5:1 B5:1 D6:1 | E6:3 r:1',90,-12)],
       'bd':[('ep','F5:2 D5:2 | E5:2 C5:2 | A5:2 F5:2 | G#5:2 B5:2',80,0)]},
      {'intro':['ep'],'A':['cs'],'pre':['lead'],'B':['lead','cs'],'bd':['ep']},style='darksynth',extra=lambda a:[comp(a,b,'st','pad',56,lo=55) for b in a.bars()])

def t02():
    A='F#m9 DM7 Bm7 C#7 F#m9 DM7 Bm7_E7 AM7_C#7';B='DM7 E C#m7 F#m9 DM7 E Bm7 C#7'
    return T('02_town',[('A',A,1,84),('B',B,2,84),('A2',A,1,84),('B2',B,2,84)],
      {'sax':(66,0,.45,0),'ep':(P_EP,-7,.4,-.3)},
      {'A':[('sax','C#5:1 E5:.5 F#5:1.5! E5:1 | C#5:1.5 A4:.5 F#4:2 | D5:1 C#5:.5 B4:.5 F#5:1.5! E5:.5 | F5:3 r:1 | A5:1! G#5:.5 F#5:.5 C#5:1 E5:1 | F#5:2 C#5:2 | D5:1 B4:1 G#4:1 B4:1 | C#5:2 G#4:2',82,-12)],
       'B':[('sax','F#5:1 A5:1 C#6:1.5! A5:.5 | B5:1.5 G#5:.5 E5:2 | E5:1 G#5:1 B5:1 C#6:1 | A5:3 r:1 | C#6:1.5! B5:.5 A5:1 F#5:1 | G#5:1 B5:1 E6:2! | D6:1 C#6:1 B5:1 A5:1 | G#5:2 F5:2',90,-12)],
       'A2':[('sax','C#5:1 E5:.5 F#5:1.5! E5:1 | C#5:1.5 A4:.5 F#4:2 | D5:1 C#5:.5 B4:.5 F#5:1.5! E5:.5 | F5:3 r:1 | A5:1! G#5:.5 F#5:.5 C#5:1 E5:1 | F#5:2 C#5:2 | D5:1 B4:1 G#4:1 B4:1 | C#5:2 G#4:2',84,-12)],
       'B2':[('sax','F#5:1 A5:1 C#6:1.5! A5:.5 | B5:1.5 G#5:.5 E5:2 | E5:1 G#5:1 B5:1 C#6:1 | A5:3 r:1 | C#6:1.5! B5:.5 A5:1 F#5:1 | G#5:1 B5:1 E6:2! | D6:1 C#6:1 B5:1 A5:1 | G#5:2 F5:2',92,-12)]},
      ['sax'],style='darkchill',target=-17,extra=lambda a:([comp(a,b,'ep','block',56,lo=52) for b in a.bars()],a.lvvol('bass',{1:-4,2:-2})))

def t04():
    riff='G3:.5! G3:.25 G3:.25 Bb3:.5 G3:.5 C4:.5 G3:.5 D4:.5 C4:.5 | G3:.5! G3:.25 G3:.25 Bb3:.5 G3:.5 F4:.5 D4:.5 Eb4:.5 D4:.5'
    CH='G5:1.5! F5:.5 Eb5:1 Bb4:1 | A5:1.5! G5:.5 F5:1 C5:1 | F5:1 A5:1 D6:1.5! C6:.5 | Bb5:3 G5:1 | G5:1 Bb5:1 Eb6:1.5! D6:.5 | C6:1 A5:1 F5:2 | F#5:1 A5:1 C6:1 Eb6:1 | D6:2! A5:2'
    def ex(a):
        for b in a.bars(only=['bd']):
            if b.last:a.mel('dist','bd','r:4 | r:4 | r:4 | '+riff.split('|')[0],96,0)
    return T('04_battle',[('intro','Gm Gm',3,172),('A','Gm Eb F D Gm Eb Cm D',2,172),('pre','Eb F Gm D',2,(172,178)),('ch','Eb F Dm Gm Eb F D D',3,178),('bd','Cm D Gm Gm',1,(150,172,2))],
      {'lead':(P_LEAD,0,.35,0),'dist':(P_DIST,-1,.25,.15),'cs':(P_BRASS,0,.4,-.1)},
      {'intro':[('dist',riff,100,0),('lead',riff,92,12)],
       'A':[('lead','D5:1! G5:.5 F5:.5 D5:1 Bb4:1 | C5:.5 D5:.5 Eb5:1 G5:1.5! F5:.5 | F5:1 C5:.5 A4:.5 C5:1 F5:1 | F#5:2! D5:1 A4:1 | D5:1! G5:.5 F5:.5 D5:1 Bb5:1 | Bb5:.5 A5:.5 G5:1 Eb5:1 G5:1 | C6:1! Bb5:.5 G5:.5 Eb5:1 C5:1 | D5:.5 Eb5:.5 F#5:1 A5:2!',92,0)],
       'pre':[('lead','G5:1 Bb5:1 Eb6:1 D6:1 | C6:1 A5:1 F6:1 Eb6:1 | D6:.5 Bb5:.5 G5:.5 Bb5:.5 D6:.5 G6:.5 F6:.5 D6:.5 | F#6:1! r:3',94,-12)],
       'ch':[('lead',CH,108,0),('dist',CH,100,-12)],
       'bd':[('cs','Eb4:2 G4:2 | F#4:2 A4:2 | Bb4:4 | r:4',100,0)]},
      {'intro':['dist','lead'],'A':['lead'],'pre':['lead'],'ch':['lead','dist'],'bd':['cs']},style='darksynth',target=-14,extra=ex)

def t05():
    return T('05_dungeon',[('A','Em C Am B Em C D B',1,104),('B','C D Bm Em C Am B B',2,104),('C','Em F Em B',1,(96,104,1)),('A2','Em C Am B Em C D B',2,104)],
      {'lead':(P_HOLLOW,0,.45,0),'vc':(42,-1,.35,-.1)},
      {'A':[('lead','B4:1 E5:1 G5:1.5! F#5:.5 | E5:1 C5:1 G4:2 | A4:.5 B4:.5 C5:1 E5:1.5! D5:.5 | D#5:3 B4:1 | E5:1 F#5:1 G5:1.5! A5:.5 | G5:1 E5:1 C5:2 | D5:1 F#5:1 A5:1 F#5:1 | B4:3 r:1',84,0)],
       'B':[('lead','G5:1.5! E5:.5 C5:1 E5:1 | F#5:1.5 D5:.5 A4:1 D5:1 | B5:1! A5:.5 F#5:.5 D5:1 B4:1 | E5:2 G5:2 | C6:1.5! B5:.5 G5:1 E5:1 | A5:1 C6:1 E6:1.5! D6:.5 | D#6:2 B5:1 F#5:1 | B5:4',92,0)],
       'C':[('vc','E3:3 G3:1 | A3:2 C4:1 A3:1 | G3:2 B3:2 | D#4:2 F#4:2',88,0)],
       'A2':[('lead','B4:1 E5:1 G5:1.5! F#5:.5 | E5:1 C5:1 G4:2 | A4:.5 B4:.5 C5:1 E5:1.5! D5:.5 | D#5:3 B4:1 | E5:1 F#5:1 G5:1.5! A5:.5 | G5:1 E5:1 C5:2 | D5:1 F#5:1 A5:1 F#5:1 | B4:3 r:1',90,12),('vc','E3:4 | C3:4 | A2:4 | B2:4 | E3:4 | C3:4 | D3:4 | B2:4',64,0)]},
      {'A':['lead'],'B':['lead'],'C':['vc'],'A2':['lead']},style='ambient',target=-16)

def t06():
    CH='F#5:1.5! E5:.5 D5:1 A4:1 | G#5:1.5! F#5:.5 E5:1 B4:1 | E5:1 G#5:1 C#6:1.5! B5:.5 | A5:3 F#5:1 | A5:1 F#5:1 D6:1.5! C#6:.5 | B5:1 G#5:1 E5:2 | F5:1 G#5:1 C#6:1 F6:1 | C#6:2! G#5:2'
    def ex(a):
        for b in a.bars(only=['intro']):
            for t in ((0,2) if b.i==0 else (0,2,3)):kime(a,b,[('cs',48),('pad',55)],112,beat=t,crash=t==0)
    return T('06_boss',[('intro','F#m D_E',3,156),('A','F#m D E C#m F#m D Bm C#',2,156),('pre','D E F#m C#',2,(156,160)),('ch','D E C#m F#m D E C# C#',3,160),('bd','Bm D E C#',1,(130,156,2))],
      {'cs':(P_BRASS,0,.4,0),'lead':(P_LEAD,-1,.35,.1),'dist':(P_DIST,-10,.2,.45),'vox':(P_VOX,0,.45,0)},
      {'A':[('cs','C#4:.5 F#4:.5 A4:1 C#5:1.5! B4:.5 | A4:1 F#4:.5 D4:.5 F#4:1 A4:1 | G#4:1 B4:1 E5:1 D5:1 | E5:3! C#5:1 | F#5:1! E5:.5 C#5:.5 A4:1 C#5:1 | D5:1 F#5:1 A5:1.5! G#5:.5 | F#5:1 D5:1 B4:1 D5:1 | F5:2 G#5:1 C#6:1!',92,0)],
       'pre':[('cs','F#5:1 A5:1 D6:1 C#6:1 | B5:1 G#5:1 E6:1 D6:1 | C#6:.5 A5:.5 F#5:.5 A5:.5 C#6:.5 F#6:.5 E6:.5 C#6:.5 | F6:1! r:3',92,-12)],
       'ch':[('cs',CH,104,0),('lead',CH,100,12)],
       'bd':[('vox','D4:2 F#4:2 | A4:2 F#4:2 | G#4:2 B4:2 | F4:2 G#4:2',96,12)]},
      {'intro':[],'A':['cs'],'pre':['cs'],'ch':['cs','lead'],'bd':['vox']},style='darksynth',target=-14,extra=lambda a:(ex(a),[comp(a,b,'dist','power8',80) for b in a.bars(only=['A','ch'])]))

def t07():
    return T('07_lastdungeon',[('intro','C#m C#m A G#',0,(80,112,2)),('A','C#m A F#m G# C#m D F#m G#',1,112),('B','A B C#m C#m F#m D G# G#',2,112),('C','C#m A F#m D C#m A D G#',3,116),('D','C#m D C#m G#',1,112)],
      {'str':(P_STR,0,.45,0),'vox':(P_VOX,0,.5,0),'cs':(P_BRASS,0,.4,.1),'sdr':(118,-8,.35,0)},
      {'A':[('str','C#4:2 E4:1 G#4:1! | A4:2 G#4:1 E4:1 | F#4:1 G#4:1 A4:1 C#5:1! | C5:3 G#4:1 | C#5:1.5 D#5:.5 E5:1 C#5:1 | F#5:2! E5:1 D5:1 | C#5:1 A4:1 F#4:1 A4:1 | G#4:3 r:1',88,0)],
       'B':[('vox','C#5:2 E5:2 | D#5:2 F#5:2 | G#5:3! F#5:.5 E5:.5 | E5:4 | F#5:2 A5:2 | A5:1 G#5:1 F#5:2 | G#5:2 C6:2! | G#5:4',94,0)],
       'C':[('cs','C#6:2! G#5:1 E5:1 | E5:1 A5:1 C#6:2 | F#6:2! E6:1 C#6:1 | D6:3 C#6:.5 B5:.5 | C#6:1 E6:1 G#6:2! | A6:2 G#6:1 E6:1 | F#6:2 D6:2 | D#6:2! C6:2',102,-12),('vox','C#6:2 G#5:1 E5:1 | E5:1 A5:1 C#6:2 | F#6:2 E6:1 C#6:1 | D6:3 C#6:.5 B5:.5 | C#6:1 E6:1 G#6:2 | A6:2 G#6:1 E6:1 | F#6:2 D6:2 | D#6:2 C6:2',90,-24)],
       'D':[('str','G#4:4 | F#4:4 | E4:4 | D#4:2 C4:2',76,0)]},
      {'intro':[],'A':['str'],'B':['vox'],'C':['cs','vox'],'D':['str']},style='industrial',target=-15,
      extra=lambda a:[a.n('sdr',b.bt,.5,fold(b.r,38,50),60+b.lv*12) for b in a.bars()])

def t08():
    A='Bbm7 Ebm7_Ab7 DbM7 GbM7 Cm7b5 F7 Bbm7 F7';B='Ebm7 Ab7 DbM7 Bbm7 Ebm7 F7 Bbm7_Gb7 F7'
    MA='F5:.667! Db5:.333 Bb4:1 r:.667 C5:.333 Db5:1 | Eb5:1.5! Gb5:.5 F5:1 C5:1 | Db5:.667 F5:.333 Ab5:1 C6:1.5! Bb5:.5 | Bb5:3 r:1 | Eb5:.667 Gb5:.333 Bb5:1! Gb5:1 Eb5:1 | A5:1.5 C6:.5 Eb6:1! C6:1 | Db6:1 Bb5:.667 F5:.333 Db5:2 | C5:.667 Eb5:.333 A5:1 F5:2'
    return T('08_blackmarket',[('A',A,1,96),('B',B,2,96),('C','Bbm7 Gb7 Cm7b5 F7',1,96),('A2',A,2,96)],
      {'mtp':(59,0,.4,0),'ep':(P_EP,0,.4,-.3),'vib':(P_BELL,-12,.45,.35)},
      {'A':[('mtp',MA,84,-12)],
       'B':[('mtp','Bb5:.667 Db6:.333 Eb6:1.5! Db6:.5 Bb5:1 | C6:1 Gb5:1 Ab5:2 | F6:1.5! Eb6:.5 Db6:1 Ab5:1 | Bb5:3 r:1 | Gb6:1! F6:.667 Eb6:.333 Bb5:1 Gb5:1 | A5:1 C6:1 Eb6:1 Gb6:1! | F6:2 E6:2 | Eb6:1 C6:1 A5:1 F5:1',92,-12)],
       'C':[('ep','Bb4:.667 Db5:.333 F5:1 Ab5:2 | Gb5:1 E5:1 Db5:2 | Eb5:.667 Gb5:.333 Bb5:1 Gb5:2 | A5:2 F5:2',90,0)],
       'A2':[('mtp',MA,92,-12)]},
      {'A':['mtp'],'B':['mtp'],'C':['ep'],'A2':['mtp']},style='swing',target=-17,arp=False,
      extra=lambda a:([comp(a,b,'ep','swingcomp',56,lo=52) for b in a.bars() if b.sec!='C'],a.lvvol('ep',{'A':-6,'B':-6,'C':0,'A2':-6})))

def t10():
    def ex(a):
        for b in a.bars():
            if b.sec=='intro':
                for j in range(16):a.n('sdr',b.bt+j*.25,.24,fold(b.r,38,50),50+b.i*20+j*2)
                if b.last:snare_roll(a,b,40,100,4)
            elif b.last:kime(a,b,[('pad',55),('cs',52)],124);a.d(b.bt,57,118)
    return T('10_voyage',[('intro','Am Am',0,(90,116)),('go','Am F G Em_F G A',3,(116,166))],
      {'cs':(P_BRASS,0,.45,0),'lead':(P_LEAD,-2,.4,.1),'sdr':(118,-8,.35,0)},
      {'go':[('cs','E4:1 A4:1 C5:2! | C5:1 F5:1 A5:2! | G5:1 B5:1 D6:2! | E6:2 F6:2 | G6:4! | A6:4!',96,0),('lead','E4:1 A4:1 C5:2 | C5:1 F5:1 A5:2 | G5:1 B5:1 D6:2 | E6:2 F6:2 | G6:4 | A6:4',88,12)]},
      {'intro':[],'go':['cs','lead']},style='darksynth',loop=None,tail=3.5,target=-14,extra=ex)

def t42():
    riff='C3:.5! C3:.25 C3:.25 Eb3:.5 C3:.5 F3:.5 C3:.5 G3:.5 F3:.5 | C3:.5! C3:.25 C3:.25 Eb3:.5 C3:.5 Bb3:.5 G3:.5 Ab3:.5 G3:.5'
    CH='C6:1.5! Bb5:.5 Ab5:1 Eb5:1 | D6:1.5! C6:.5 Bb5:1 F5:1 | Bb5:1 D6:1 G6:1.5! F6:.5 | Eb6:3 C6:1 | C6:1 Eb6:1 Ab6:1.5! G6:.5 | F6:1 D6:1 Bb5:2 | B5:1 D6:1 F6:1 Ab6:1! | G6:2 D6:2'
    return T('42_battle_org',[('intro','Cm Cm',3,184),('A','Cm Ab Bb G Cm Ab Fm G',2,184),('pre','Ab Bb Cm G',2,(184,190)),('ch','Ab Bb Gm Cm Ab Bb G G',3,190),('bd','Fm G Cm Cm',1,(160,184,2))],
      {'dist':(P_DIST,0,.25,0),'cs':(P_BRASS,-1,.4,.15)},
      {'intro':[('dist',riff,100,12)],
       'A':[('dist','G4:1! C5:.5 Bb4:.5 G4:1 Eb4:1 | Eb4:.5 F4:.5 Ab4:1 C5:1.5! Bb4:.5 | Bb4:1 F4:.5 D4:.5 F4:1 Bb4:1 | D5:2! B4:1 G4:1 | G4:1! C5:.5 Bb4:.5 G4:1 Eb5:1 | Eb5:.5 D5:.5 C5:1 Ab4:1 C5:1 | F5:1! Eb5:.5 C5:.5 Ab4:1 F4:1 | G4:.5 Ab4:.5 B4:1 D5:2!',92,0)],
       'pre':[('dist','C5:1 Eb5:1 Ab5:1 G5:1 | F5:1 D5:1 Bb5:1 Ab5:1 | G5:.5 Eb5:.5 C5:.5 Eb5:.5 G5:.5 C6:.5 Bb5:.5 G5:.5 | B5:1! r:3',92,0)],
       'ch':[('dist',CH,108,0),('cs',CH,100,-12)],
       'bd':[('cs','Ab4:2 C5:2 | B4:2 D5:2 | C5:4 | r:4',96,0),('dist','r:4 | r:4 | r:4 | '+riff.split('|')[0],92,12)]},
      {'intro':['dist'],'A':['dist'],'pre':['dist'],'ch':['dist','cs'],'bd':['cs','dist']},style='industrial',target=-14)

def t43():
    def ex(a):
        a.stem('glitch',None,-11,.2,.4);a.song.cfg['glitch']['syn']=dict(P_BELL)
        for b in a.bars():
            for t in np.random.choice(np.arange(0,4,.25),3 if b.lv<3 else 6,replace=False):a.n('glitch',b.bt+t,.08,fold(b.r,80,91)+np.random.choice([0,1,6,11]),76)
    return T('43_boss_raid',[('intro','Ebm E',3,176),('A','Ebm B Db Bbm Ebm E Ebm Bb',2,176),('ch','B Db Bbm Ebm B Db Bb Bb',3,180),('bd','Abm Bb7 Ebm Ebm',1,(146,176,2))],
      {'lead':(P_LEAD,0,.35,0),'vox':(P_VOX,-1,.45,.15)},
      {'intro':[('lead','Eb4:.25 Eb4:.25 Bb4:.5 Eb5:1! r:2 | E4:.25 E4:.25 B4:.5 E5:1! r:1 Bb4:1',100,0)],
       'A':[('lead','Bb4:.5 Eb5:.5 Gb5:1! F5:.5 Eb5:.5 Bb4:1 | B4:1 D#5:.5 F#5:.5 B5:1.5! A#5:.5 | Ab5:1 F5:.5 Db5:.5 Ab4:1 Db5:1 | F5:2! Db5:1 Bb4:1 | Bb4:.5 Eb5:.5 Gb5:1 Bb5:1.5! Ab5:.5 | Ab5:1 E5:1 B4:2 | Eb5:.5 Gb5:.5 Bb5:1 Ab5:.5 Gb5:.5 Eb5:1 | F5:2! D5:1 Bb4:1',94,0)],
       'ch':[('lead','D#6:1.5! C#6:.5 B5:1 F#5:1 | F6:1.5! Eb6:.5 Db6:1 Ab5:1 | Db6:1 F6:1 Bb6:1.5! Ab6:.5 | Gb6:3 Eb6:1 | D#6:1 F#6:1 B6:1.5! A#6:.5 | Ab6:1 F6:1 Db6:2 | D6:1 F6:1 Bb6:2! | Bb6:2 F6:2',106,-12),('vox','D#6:1.5 C#6:.5 B5:1 F#5:1 | F6:1.5 Eb6:.5 Db6:1 Ab5:1 | Db6:1 F6:1 Bb6:1.5 Ab6:.5 | Gb6:3 Eb6:1 | D#6:1 F#6:1 B6:1.5 A#6:.5 | Ab6:1 F6:1 Db6:2 | D6:1 F6:1 Bb6:2 | Bb6:2 F6:2',98,-24)],
       'bd':[('vox','B4:2 Eb5:2 | D5:2 F5:2 | Gb5:4 | r:4',98,0)]},
      {'intro':['lead'],'A':['lead'],'ch':['lead','vox'],'bd':['vox']},style='darksynth',target=-14,extra=ex)

def t44():
    return T('44_sleep',[('A','Ab Eb Fm Db Ab Eb Db_Eb Ab',0,(60,48,2))],
      {'mbox':(10,0,.5,0)},
      {'A':[('mbox','Eb5:1 C5:1 Ab4:1 | Bb4:2 G4:1 | Ab4:1 C5:1 F5:1 | F5:2 Db5:1 | C5:1 Eb5:1 Ab5:1 | G5:2 Bb5:1 | F5:1.5 G5:1.5 | Ab5:3',80,12)]},
      ['mbox'],style='ambient',bpb=3,loop=None,tail=4,target=-19)

ALL=['t01','t02','t04','t05','t06','t07','t08','t10','t42','t43','t44']
if __name__=='__main__':
    for f in (sys.argv[1:] or ALL):print('==',f);globals()[f]()
