import sys
from arr9 import *

def drip(a,stem,v=60,n=3):
    for b in a.bars():
        for k in range(n+b.lv):
            t=np.random.choice(np.arange(0,b.B,.25));a.n(stem,b.bt+t,.3,fold(b.r,79,91)+np.random.choice([0,3,7,12]),v-np.random.randint(0,14))

def t27():
    MA='D5:.5 G5:.5 Bb5:.5 A5:.5 G5:1! D5:1 | Eb5:.5 D5:.5 Bb4:1 G4:2 | C5:.5 Eb5:.5 G5:.5 Bb5:.5 A5:1! G5:1 | F#5:3 r:1 | D5:.5 G5:.5 Bb5:.5 D6:.5 C6:1! Bb5:1 | Bb5:1 G5:1 Eb5:2 | Eb5:.5 G5:.5 C6:1 Bb5:.5 A5:.5 G5:1 | A5:2 F#5:2'
    return T('27_dg1_cistern',[('A','Gm Eb Cm D Gm Eb Cm D',1,92),('B','Eb F Dm Gm Eb Cm D D',2,92),('A2','Gm Eb Cm D Gm Eb Cm D',1,92)],
      {'kal':(108,0,.45,0),'vc':(42,-1,.4,-.1)},
      {'A':[('kal',MA,86,0)],'B':[('kal','G5:1 Bb5:1 Eb6:2! | F5:1 A5:1 C6:2 | D6:1.5! C6:.5 A5:1 F5:1 | G5:3 r:1 | Bb5:1 Eb6:1 G6:1.5! F6:.5 | Eb6:1 C6:1 G5:2 | F#5:1 A5:1 D6:1 C6:1 | A5:4',94,0),('vc','G5:1 Bb5:1 Eb6:2 | F5:1 A5:1 C6:2 | D6:1.5 C6:.5 A5:1 F5:1 | G5:3 r:1 | Bb5:1 Eb6:1 G6:1.5 F6:.5 | Eb6:1 C6:1 G5:2 | F#5:1 A5:1 D6:1 C6:1 | A5:4',84,-24)],'A2':[('kal',MA,88,0)]},
      {'A':['kal'],'B':['kal','vc'],'A2':['kal']},style='ambient',target=-17,extra=lambda a:drip(a,'bell',62,2))

def t28():
    return T('28_dg2_tunnel',[('A','Bm G Em F# Bm G A F#',1,116),('B','G A F#m Bm G A F# F#',2,120),('A2','Bm G Em F# Bm G A F#',2,116)],
      {'vc':(42,0,.35,0)},
      {'A':[('vc','B2:1! D3:.5 F#3:.5 B3:1 A3:1 | G3:1 D3:1 B2:2 | E3:.5 G3:.5 B3:1 E4:1.5! D4:.5 | C#4:3 A#2:1 | B2:1! D3:.5 F#3:.5 B3:1 D4:1 | D4:1 B3:1 G3:2 | A3:1 C#4:1 E4:1 A4:1! | F#4:2 C#4:2',88,12)],
       'B':[('vc','B3:1.5 D4:.5 G4:2! | A4:1.5 G4:.5 E4:2 | F#4:1 A4:1 C#5:1! A4:1 | B4:3 r:1 | G4:1 B4:1 D5:2! | C#5:1.5 B4:.5 A4:2 | A#4:1 C#5:1 F#5:2! | F#5:4',96,0)],
       'A2':[('vc','B2:1! D3:.5 F#3:.5 B3:1 A3:1 | G3:1 D3:1 B2:2 | E3:.5 G3:.5 B3:1 E4:1.5! D4:.5 | C#4:3 A#2:1 | B2:1! D3:.5 F#3:.5 B3:1 D4:1 | D4:1 B3:1 G3:2 | A3:1 C#4:1 E4:1 A4:1! | F#4:2 C#4:2',94,12)]},
      ['vc'],style='industrial',target=-15)

def t29():
    return T('29_dg3_frozen',[('A','Am FM7 Dm E Am FM7 Dm_E Am',0,74),('B','FM7 G Em Am Dm G E E',1,74),('A2','Am FM7 Dm E Am FM7 Dm_E Am',1,74)],
      {'mbox':(10,0,.5,0),'str':(P_STR,-1,.45,.15)},
      {'A':[('mbox','E6:1 C6:1 A5:1 E6:1! | F6:2 C6:2 | D6:1.5 C6:.5 A5:1 F5:1 | G#5:4 | E6:1 A6:1! E6:1 C6:1 | A5:2 C6:2 | D6:1 F6:1 E6:1 B5:1 | A5:4',82,-12)],
       'B':[('mbox','A5:1 C6:1 F6:2! | G6:1.5 F6:.5 D6:2 | E6:1 G6:1 B6:2! | A6:4 | F6:1 D6:1 A5:2 | B5:1 D6:1 G6:2 | G#6:2! E6:2 | E6:4',88,-12),('str','A5:1 C6:1 F6:2 | G6:1.5 F6:.5 D6:2 | E6:1 G6:1 B6:2 | A6:4 | F6:1 D6:1 A5:2 | B5:1 D6:1 G6:2 | G#6:2 E6:2 | E6:4',80,-24)],
       'A2':[('mbox','E6:1 C6:1 A5:1 E6:1! | F6:2 C6:2 | D6:1.5 C6:.5 A5:1 F5:1 | G#5:4 | E6:1 A6:1! E6:1 C6:1 | A5:2 C6:2 | D6:1 F6:1 E6:1 B5:1 | A5:4',84,-12)]},
      {'A':['mbox'],'B':['mbox','str'],'A2':['mbox']},style='ambient',target=-18)

def t30():
    return T('30_dg4_bunker',[('A','Ebm B Db Bb Ebm B Ab Bb',1,124),('B','B Db Ebm Ebm B Db Bb Bb',2,124),('A2','Ebm B Db Bb Ebm B Ab Bb',2,124)],
      {'tbn':(57,0,.35,0),'cs':(P_BRASS,-1,.4,-.15)},
      {'A':[('tbn','Eb3:.75! Eb3:.25 Gb3:1 Bb3:1.5! Ab3:.5 | F#3:1 D#3:1 B2:2 | Db3:.75 Db3:.25 F3:1 Ab3:1 Db4:1! | D4:3 r:1 | Eb3:.75! Eb3:.25 Gb3:1 Bb3:1 Eb4:1! | D#4:1.5 C#4:.5 B3:2 | C4:1 Eb4:1 Ab4:1 Eb4:1 | F4:2 D4:2',92,0)],
       'B':[('tbn','F#4:1.5! D#4:.5 B3:1 D#4:1 | F4:1.5 Db4:.5 Ab3:1 Db4:1 | Gb4:2! Bb4:2 | Eb4:3 r:1 | B4:1.5! A#4:.5 F#4:1 D#4:1 | Ab4:1 F4:1 Db4:2 | D4:1 F4:1 Bb4:2! | Bb4:4',100,0),('cs','F#4:1.5 D#4:.5 B3:1 D#4:1 | F4:1.5 Db4:.5 Ab3:1 Db4:1 | Gb4:2 Bb4:2 | Eb4:3 r:1 | B4:1.5 A#4:.5 F#4:1 D#4:1 | Ab4:1 F4:1 Db4:2 | D4:1 F4:1 Bb4:2 | Bb4:4',92,12)],
       'A2':[('tbn','Eb3:.75! Eb3:.25 Gb3:1 Bb3:1.5! Ab3:.5 | F#3:1 D#3:1 B2:2 | Db3:.75 Db3:.25 F3:1 Ab3:1 Db4:1! | D4:3 r:1 | Eb3:.75! Eb3:.25 Gb3:1 Bb3:1 Eb4:1! | D#4:1.5 C#4:.5 B3:2 | C4:1 Eb4:1 Ab4:1 Eb4:1 | F4:2 D4:2',98,0)]},
      {'A':['tbn'],'B':['tbn','cs'],'A2':['tbn']},style='march',target=-15)

def t31():
    return T('31_dg5_cathedral',[('A','Dm Bb Gm A Dm F C A',0,70),('B','Bb Gm Dm A Bb C Dm Dm',1,70),('A2','Dm Bb Gm A Dm F C A',1,70)],
      {'org':(19,0,.5,0),'vox':(P_VOX,-1,.55,0)},
      {'A':[('org','D5:2 A4:2 | Bb4:2 F5:2! | G5:2 D5:1 Bb4:1 | C#5:4 | F5:2 A5:2! | A5:2 C6:2 | G5:2 E5:2 | E5:4',84,0)],
       'B':[('org','D6:2! Bb5:2 | G5:2 Bb5:2 | A5:3 F5:1 | E5:4 | F5:2 D6:2! | E6:2 C6:2 | D6:3 A5:1 | D6:4',90,0),('vox','D6:2 Bb5:2 | G5:2 Bb5:2 | A5:3 F5:1 | E5:4 | F5:2 D6:2 | E6:2 C6:2 | D6:3 A5:1 | D6:4',86,-12)],
       'A2':[('org','D5:2 A4:2 | Bb4:2 F5:2! | G5:2 D5:1 Bb4:1 | C#5:4 | F5:2 A5:2! | A5:2 C6:2 | G5:2 E5:2 | E5:4',86,0),('vox','D4:4 | D4:4 | D4:4 | E4:4 | F4:4 | F4:4 | E4:4 | E4:4',64,0)]},
      {'A':['org'],'B':['org','vox'],'A2':['org']},style='ambient',target=-17)

def t32():
    def ex(a):
        a.stem('blk',115,-12,.15,.4)
        for b in a.bars():
            for t in range(8):a.n('blk',b.bt+t*.5,.1,76 if t%2==0 else 77,60)
    return T('32_dg6_vault',[('A','Gm Gm Eb D Gm Gm Cm D',1,130),('B','Eb F Dm Gm Eb F D D',2,130),('A2','Gm Gm Eb D Gm Gm Cm D',2,130)],
      {'pz':(45,3,.3,0)},
      {'A':[('pz','G4:.5 Bb4:.5 D5:.5 G5:.5 F5:.5 D5:.5 Bb4:1 | A4:.5 Bb4:.5 C5:.5 D5:.5 G4:2 | Eb4:.5 G4:.5 Bb4:.5 Eb5:.5 D5:1! Bb4:1 | A4:2 F#4:2 | G4:.5 Bb4:.5 D5:.5 G5:.5 A5:1! G5:1 | F5:.5 Eb5:.5 D5:.5 C5:.5 Bb4:1 G4:1 | C5:.5 Eb5:.5 G5:1 F5:.5 Eb5:.5 C5:1 | D5:2 F#5:2',90,0)],
       'B':[('pz','Bb5:1! G5:.5 Eb5:.5 Bb5:1 G5:1 | C6:1! A5:.5 F5:.5 C6:1 A5:1 | A5:1 F5:.5 D5:.5 F5:1 A5:1 | Bb5:3! r:1 | G5:1 Bb5:1 Eb6:1.5! D6:.5 | C6:1 A5:1 F5:2 | F#5:1 A5:1 D6:1.5! C6:.5 | A5:2 F#5:2',98,0)],
       'A2':[('pz','G4:.5 Bb4:.5 D5:.5 G5:.5 F5:.5 D5:.5 Bb4:1 | A4:.5 Bb4:.5 C5:.5 D5:.5 G4:2 | Eb4:.5 G4:.5 Bb4:.5 Eb5:.5 D5:1! Bb4:1 | A4:2 F#4:2 | G4:.5 Bb4:.5 D5:.5 G5:.5 A5:1! G5:1 | F5:.5 Eb5:.5 D5:.5 C5:.5 Bb4:1 G4:1 | C5:.5 Eb5:.5 G5:1 F5:.5 Eb5:.5 C5:1 | D5:2 F#5:2',96,12)]},
      ['pz'],style='darksynth',target=-16,extra=ex)

def t33():
    return T('33_dg7_greenhouse',[('A','F G Dm Bb F G Bb C',0,88),('B','Bb C Am Dm Bb G Gm_C F',1,88),('A2','F G Dm Bb F G Bb C',1,88)],
      {'fl':(73,0,.45,0),'harp':(46,-6,.4,-.3)},
      {'A':[('fl','C5:1 F5:1 G5:1 B5:1! | A5:2 G5:2 | F5:1 D5:1 A4:2 | Bb4:3 r:1 | C5:1 F5:1 A5:1.5! G5:.5 | B5:2 G5:2 | D5:1 F5:1 Bb5:1 A5:1 | G5:3 r:1',80,0)],
       'B':[('fl','D5:1 F5:1 Bb5:2! | E5:1 G5:1 C6:2 | C6:1.5 A5:.5 E5:2 | F5:3 r:1 | Bb5:1! A5:1 F5:1 D5:1 | B5:2 G5:2 | G5:1 Bb5:1 E5:2 | F5:4',86,0)],
       'A2':[('fl','C5:1 F5:1 G5:1 B5:1! | A5:2 G5:2 | F5:1 D5:1 A4:2 | Bb4:3 r:1 | C5:1 F5:1 A5:1.5! G5:.5 | B5:2 G5:2 | D5:1 F5:1 Bb5:1 A5:1 | G5:3 r:1',84,0)]},
      ['fl'],style='ambient',target=-18,extra=lambda a:[comp(a,b,'harp','arpup',58,lo=55,div=.5) for b in a.bars()])

def t34():
    return T('34_dg8_sunken',[('A','Ebm B Abm Bb Ebm Gb Abm_Bb Ebm',0,66),('B','B Db Bbm Ebm B Abm Bb Bb',1,66),('A2','Ebm B Abm Bb Ebm Gb Abm_Bb Ebm',1,66)],
      {'eh':(69,0,.45,0),'vc':(42,-1,.45,0)},
      {'A':[('eh','Bb4:2 Eb5:1 Gb5:1! | F#5:2 D#5:1 B4:1 | Ab4:2 B4:1 Eb5:1 | D5:4 | Bb4:1 Eb5:1 Gb5:1 Bb5:1! | Ab5:2 Gb5:2 | Eb5:1 B4:1 D5:1 F5:1 | Eb5:4',80,0)],
       'B':[('eh','F#5:2 B5:2! | Ab5:2 F5:2 | Db5:1 F5:1 Bb5:2! | Gb5:4 | D#5:1 F#5:1 B5:2 | B5:1.5 Bb5:.5 Ab5:2 | F5:2 D5:2 | Bb4:4',86,0),('vc','F#5:2 B5:2 | Ab5:2 F5:2 | Db5:1 F5:1 Bb5:2 | Gb5:4 | D#5:1 F#5:1 B5:2 | B5:1.5 Bb5:.5 Ab5:2 | F5:2 D5:2 | Bb4:4',80,-12)],
       'A2':[('eh','Bb4:2 Eb5:1 Gb5:1! | F#5:2 D#5:1 B4:1 | Ab4:2 B4:1 Eb5:1 | D5:4 | Bb4:1 Eb5:1 Gb5:1 Bb5:1! | Ab5:2 Gb5:2 | Eb5:1 B4:1 D5:1 F5:1 | Eb5:4',82,0)]},
      {'A':['eh'],'B':['eh','vc'],'A2':['eh']},style='ambient',target=-18,extra=lambda a:drip(a,'bell',56,1))

def t35():
    def ex(a):
        a.stem('echo',None,-9,.45,.5);a.song.cfg['echo']['syn']=dict(P_HOLLOW)
        for st,ev in list(a.song.ev.items()):
            pass
        for (b_,d,p,v) in []:pass
    MA='E5:.5 A5:.5 C6:1! B5:.5 A5:.5 E5:1 | E5:1 G5:1 C6:1.5! B5:.5 | D6:1 B5:1 G5:1 D5:1 | F#5:3 r:1 | E5:.5 A5:.5 C6:1 E6:1.5! D6:.5 | C6:1 G5:1 E5:2 | F5:1 A5:1 C6:1 A5:1 | G#5:3 r:1'
    a=T('35_dg9_relay',[('A','Am C G D Am C F E',1,118),('B','F G Em Am F G E E',2,118),('A2','Am C G D Am C F E',2,118)],
      {'lead':(P_HOLLOW,0,.4,0)},
      {'A':[('lead',MA,84,0)],'B':[('lead','A5:1.5! C6:.5 F6:2 | G6:1.5! F6:.5 D6:2 | E6:1 G6:1 B6:1.5! A6:.5 | A6:3 r:1 | F6:1 A6:1 C7:1.5! B6:.5 | B6:1 G6:1 D6:2 | E6:1 G#6:1 B6:2! | B6:4',92,-12)],'A2':[('lead',MA,90,0)]},
      ['lead'],style='darkchill',target=-16)
    return a

def t36():
    def ex(a):
        for b in a.bars(only=['intro']):kime(a,b,[('pad',55)],100,beat=0)
    return T('36_end_win',[('intro','AbM7 Eb7',1,104),('A','AbM7 Fm7 DbM7 Eb7 AbM7 Fm7 Bbm7_Eb7 AbM7',1,104),('B','DbM7 Eb Cm7 Fm7 DbM7 Eb Bbm7_Eb AbM7',2,108),('out','Db_Eb Ab',3,(108,80,2))],
      {'sax':(65,0,.4,0),'cs':(P_BRASS,-2,.4,.2),'ep':(P_EP,-8,.4,-.3)},
      {'intro':[('cs','C5:.333! Eb5:.333 Ab5:.334 C6:2.5! r:.5 | Bb5:1 G5:1 Eb5:1 Db5:1',96,-12)],
       'A':[('sax','C5:.5 Eb5:.5 Ab5:1! G5:.5 F5:.5 Eb5:1 | C5:1 Ab4:.5 F4:.5 Ab4:1 C5:1 | Db5:.5 F5:.5 Ab5:1 C6:1.5! Bb5:.5 | G5:3 r:1 | C5:.5 Eb5:.5 Ab5:1 Bb5:1.5! Ab5:.5 | F5:1 C5:1 Ab4:2 | F5:1 Db5:1 G5:1 Bb5:1 | Ab5:3! r:1',88,-12)],
       'B':[('sax','F5:1 Ab5:1 C6:2! | Bb5:1.5 G5:.5 Eb5:2 | G5:1 Bb5:1 Eb6:2! | C6:3 r:1 | Ab5:1 C6:1 F6:1.5! Eb6:.5 | Eb6:1 Bb5:1 G5:2 | Db6:1 Bb5:1 G5:1 Bb5:1 | Ab5:3! r:1',96,-12),('cs','F5:1 Ab5:1 C6:2 | Bb5:1.5 G5:.5 Eb5:2 | G5:1 Bb5:1 Eb6:2 | C6:3 r:1 | Ab5:1 C6:1 F6:1.5 Eb6:.5 | Eb6:1 Bb5:1 G5:2 | Db6:1 Bb5:1 G5:1 Bb5:1 | Ab5:3 r:1',86,-24)],
       'out':[('sax','F5:2 G5:2 | Ab5:4!',100,-12),('cs','Db5:2 Eb5:2 | Eb5:4!',92,-12)]},
      {'intro':['cs'],'A':['sax'],'B':['sax','cs'],'out':['sax','cs']},style='darkchill',loop=None,tail=3,target=-15,extra=lambda a:(ex(a),[comp(a,b,'ep','stab_off',60,lo=55) for b in a.bars(only=['A','B'])]))

def t37():
    B='E6:2! G6:2 | F#6:1.5 E6:.5 D6:2 | D6:1 G6:1 B6:2! | B6:3 G6:1 | G6:1 E6:1 C7:2! | A6:1.5 G6:.5 F#6:2 | G6:2 B6:2! | G6:4'
    return T('37_end_escape',[('intro','Em Em C D',0,(100,132,2)),('A','Em C G D Em C Am B',1,132),('B','C D G Em C D G G',2,136),('C','Eb F Bb Gm Eb F Bb Bb',3,142),('out','Bb Bb',3,(142,100,2))],
      {'lead':(P_LEAD,0,.45,0),'vox':(P_VOX,-1,.5,-.1),'cs':(P_BRASS,-3,.45,.2)},
      {'A':[('lead','B4:1 E5:1 G5:1.5! F#5:.5 | E5:2 C5:2 | B4:1 D5:1 G5:1.5! A5:.5 | F#5:4 | B4:1 E5:1 B5:1.5! A5:.5 | G5:2 E5:2 | A5:1 C6:1 E6:1! C6:1 | D#6:4',88,0)],
       'B':[('lead',B,98,-12),('vox',B,92,-24)],
       'C':[('lead',B,106,-9),('vox',B,100,-21),('cs',B,90,-33)],
       'out':[('lead','Bb6:4! | Bb6:3 r:1',100,-12),('vox','Bb5:4 | Bb5:3 r:1',92,-12)]},
      {'intro':[],'A':['lead'],'B':['lead','vox'],'C':['lead','vox'],'out':['lead','vox']},style='darksynth',loop=None,tail=3.5,target=-15)

def t38():
    def ex(a):
        for b in a.bars(only=['intro']):kime(a,b,[('pad',55),('cs',48)],108)
    return T('38_end_counter',[('intro','Dm A',2,136),('A','Dm Bb C A Dm Bb Gm A',2,136),('B','Bb C Am Dm Bb C Gm_A D',3,140),('out','G_A D',3,(140,96,2))],
      {'cs':(P_BRASS,0,.4,0),'lead':(P_LEAD,-1,.35,.1)},
      {'intro':[('cs','A4:.333! A4:.333 A4:.334 D5:2.5! r:.5 | C#5:1 E5:1 A5:2!',100,0)],
       'A':[('cs','A4:.75! A4:.25 D5:1 F5:1.5! E5:.5 | D5:1 Bb4:1 F4:2 | G4:.75 G4:.25 C5:1 E5:1 G5:1! | E5:2 C#5:2 | A4:.75! A4:.25 D5:1 F5:1 A5:1! | Bb5:1.5 A5:.5 F5:2 | D5:1 G5:1 Bb5:1 G5:1 | A5:3! r:1',94,0)],
       'B':[('lead','F5:1.5! D5:.5 Bb4:1 D5:1 | E5:1 G5:1 C6:2 | C6:1.5 A5:.5 E5:1 A5:1 | D6:3! A5:1 | Bb5:1 D6:1 F6:1.5! D6:.5 | E6:1 C6:1 G5:2 | Bb5:1 D6:1 C#6:1 E6:1 | F#6:3! r:1',104,0),('cs','F5:1.5 D5:.5 Bb4:1 D5:1 | E5:1 G5:1 C6:2 | C6:1.5 A5:.5 E5:1 A5:1 | D6:3 A5:1 | Bb5:1 D6:1 F6:1.5 D6:.5 | E6:1 C6:1 G5:2 | Bb5:1 D6:1 C#6:1 E6:1 | F#6:3 r:1',96,-12)],
       'out':[('lead','B5:2 C#6:2 | D6:4!',108,0),('cs','B4:2 C#5:2 | D5:4!',100,0)]},
      {'intro':['cs'],'A':['cs'],'B':['lead','cs'],'out':['lead','cs']},style='darksynth',loop=None,tail=3.5,target=-15,extra=ex)

def t39():
    def ex(a):
        a.stem('rain',96,-14,.3,0)
        for b in a.bars():a.n('rain',b.bt,b.B*.99,72,72)
        a.lvvol('bass',{'A':0,'B':0,'out':-8})
    return T('39_end_sad',[('A','Fm Db Ab Eb Fm Db Bbm C',0,60),('B','Db Eb Cm Fm Db Eb C C',1,60),('out','Fm Fm',0,(60,48,2))],
      {'ep':(P_EP,0,.5,0),'str':(P_STR,-1,.5,.15)},
      {'A':[('ep','C5:1.5! Bb4:.5 Ab4:1 F4:1 | Db4:1 F4:1 Ab4:2 | C5:1.5 Bb4:.5 Ab4:1 Eb4:1 | G4:3 r:1 | C5:1 F5:1! Eb5:1 C5:1 | Db5:2 Ab4:2 | Bb4:1 Db5:1 F5:1 Db5:1 | C5:4',80,0)],
       'B':[('ep','Ab4:1 Db5:1 F5:2! | G5:1.5 F5:.5 Eb5:2 | Eb5:1 C5:1 G4:2 | Ab4:3 r:1 | F4:1 Ab4:1 Db5:2 | Bb4:1 Eb5:1 G5:2! | E5:2 G5:2 | C5:4',84,0),('str','Ab4:1 Db5:1 F5:2 | G5:1.5 F5:.5 Eb5:2 | Eb5:1 C5:1 G4:2 | Ab4:3 r:1 | F4:1 Ab4:1 Db5:2 | Bb4:1 Eb5:1 G5:2 | E5:2 G5:2 | C5:4',76,0)],
       'out':[('ep','F4:4 | r:4',70,0)]},
      {'A':['ep'],'B':['ep','str'],'out':['ep']},style='ambient',loop=None,tail=4,target=-19,extra=ex)

def t40():
    def ex(a):
        a.stem('glitch',None,-11,.2,.4);a.song.cfg['glitch']['syn']=dict(P_BELL)
        for b in a.bars():
            n_=6 if b.sec!='out' else 10-b.i*4
            for t in np.random.choice(np.arange(0,4,.25),max(1,n_),replace=False):a.n('glitch',b.bt+t,.08,fold(b.r,76,90)+np.random.choice([0,1,6,13]),66)
    return T('40_end_cyber',[('intro','Gm Gm',0,94),('A','Gm Eb Bb F Gm Eb Cm D',1,94),('B','Eb F Dm Gm Eb Cm D D',2,94),('out','Gm Gm',1,(94,72,2))],
      {'vox':(P_VOX,0,.5,0)},
      {'A':[('vox','D4:2 G4:1 Bb4:1! | A4:2 G4:1 Eb4:1 | F4:1 Bb4:1 D5:2! | C5:4 | D4:1 G4:1 Bb4:1 D5:1! | Eb5:2 Bb4:2 | C5:1 Eb5:1 G5:1 F#5:1 | A4:4',84,12)],
       'B':[('vox','G5:2 Bb5:2! | A5:2 C6:2 | F5:1 A5:1 D6:2! | Bb5:4 | G5:1 Bb5:1 Eb6:2! | Eb6:1.5 D6:.5 C6:2 | A5:2 F#5:2 | D5:4',92,0)]},
      {'intro':[],'A':['vox'],'B':['vox'],'out':[]},style='darksynth',loop=None,tail=3,target=-16,extra=ex)

ALL=['t27','t28','t29','t30','t31','t32','t33','t34','t35','t36','t37','t38','t39','t40']
if __name__=='__main__':
    for f in (sys.argv[1:] or ALL):print('==',f);globals()[f]()
