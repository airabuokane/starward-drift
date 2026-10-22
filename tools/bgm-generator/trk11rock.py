import sys
from arr9 import *

def t04():
    riff='G3:.5! G3:.25 G3:.25 Bb3:.5 G3:.5 C4:.5 G3:.5 D4:.5 C4:.5 | G3:.5! G3:.25 G3:.25 Bb3:.5 G3:.5 F4:.5 D4:.5 Eb4:.5 D4:.5'
    CH='G5:1.5! F5:.5 Eb5:1 Bb4:1 | A5:1.5! G5:.5 F5:1 C5:1 | F5:1 A5:1 D6:1.5! C6:.5 | Bb5:3 G5:1 | G5:1 Bb5:1 Eb6:1.5! D6:.5 | C6:1 A5:1 F5:2 | F#5:1 A5:1 C6:1 Eb6:1 | D6:2! A5:2'
    def ex(a):
        for b in a.bars(only=['bd']):
            if b.last:a.mel('dist','bd','r:4 | r:4 | r:4 | '+riff.split('|')[0],96,0)
    return T('04_battle',[('intro','Gm Gm',3,172),('A','Gm Eb F D Gm Eb Cm D',2,172),('pre','Eb F Gm D',2,(172,178)),('ch','Eb F Dm Gm Eb F D D',3,178),('bd','Cm D Gm Gm',1,(150,172,2))],
      {'lead':(29,0,.3,0),'dist':(30,-1,.18,.15),'cs':(17,0,.35,-.1)},
      {'intro':[('dist',riff,100,0),('lead',riff,92,12)],
       'A':[('lead','D5:1! G5:.5 F5:.5 D5:1 Bb4:1 | C5:.5 D5:.5 Eb5:1 G5:1.5! F5:.5 | F5:1 C5:.5 A4:.5 C5:1 F5:1 | F#5:2! D5:1 A4:1 | D5:1! G5:.5 F5:.5 D5:1 Bb5:1 | Bb5:.5 A5:.5 G5:1 Eb5:1 G5:1 | C6:1! Bb5:.5 G5:.5 Eb5:1 C5:1 | D5:.5 Eb5:.5 F#5:1 A5:2!',92,0)],
       'pre':[('lead','G5:1 Bb5:1 Eb6:1 D6:1 | C6:1 A5:1 F6:1 Eb6:1 | D6:.5 Bb5:.5 G5:.5 Bb5:.5 D6:.5 G6:.5 F6:.5 D6:.5 | F#6:1! r:3',94,-12)],
       'ch':[('lead',CH,108,0),('dist',CH,100,-12)],
       'bd':[('cs','Eb4:2 G4:2 | F#4:2 A4:2 | Bb4:4 | r:4',100,0)]},
      {'intro':['dist','lead'],'A':['lead'],'pre':['lead'],'ch':['lead','dist'],'bd':['cs']},style='rock',target=-14,extra=ex)

def t06():
    CH='F#5:1.5! E5:.5 D5:1 A4:1 | G#5:1.5! F#5:.5 E5:1 B4:1 | E5:1 G#5:1 C#6:1.5! B5:.5 | A5:3 F#5:1 | A5:1 F#5:1 D6:1.5! C#6:.5 | B5:1 G#5:1 E5:2 | F5:1 G#5:1 C#6:1 F6:1 | C#6:2! G#5:2'
    def ex(a):
        for b in a.bars(only=['intro']):
            for t in ((0,2) if b.i==0 else (0,2,3)):kime(a,b,[('cs',48),('pad',55)],112,beat=t,crash=t==0)
    return T('06_boss',[('intro','F#m D_E',3,156),('A','F#m D E C#m F#m D Bm C#',2,156),('pre','D E F#m C#',2,(156,160)),('ch','D E C#m F#m D E C# C#',3,160),('bd','Bm D E C#',1,(130,156,2))],
      {'cs':(29,0,.3,0),'lead':(29,-3,.3,.35),'dist':(30,-10,.2,.45),'vox':(17,0,.4,0)},
      {'A':[('cs','C#4:.5 F#4:.5 A4:1 C#5:1.5! B4:.5 | A4:1 F#4:.5 D4:.5 F#4:1 A4:1 | G#4:1 B4:1 E5:1 D5:1 | E5:3! C#5:1 | F#5:1! E5:.5 C#5:.5 A4:1 C#5:1 | D5:1 F#5:1 A5:1.5! G#5:.5 | F#5:1 D5:1 B4:1 D5:1 | F5:2 G#5:1 C#6:1!',92,0)],
       'pre':[('cs','F#5:1 A5:1 D6:1 C#6:1 | B5:1 G#5:1 E6:1 D6:1 | C#6:.5 A5:.5 F#5:.5 A5:.5 C#6:.5 F#6:.5 E6:.5 C#6:.5 | F6:1! r:3',92,-12)],
       'ch':[('cs',CH,104,0),('lead',CH,100,12)],
       'bd':[('vox','D4:2 F#4:2 | A4:2 F#4:2 | G#4:2 B4:2 | F4:2 G#4:2',96,12)]},
      {'intro':[],'A':['cs'],'pre':['cs'],'ch':['cs','lead'],'bd':['vox']},style='rock',target=-14,extra=ex)

def t42():
    riff='C3:.5! C3:.25 C3:.25 Eb3:.5 C3:.5 F3:.5 C3:.5 G3:.5 F3:.5 | C3:.5! C3:.25 C3:.25 Eb3:.5 C3:.5 Bb3:.5 G3:.5 Ab3:.5 G3:.5'
    CH='C6:1.5! Bb5:.5 Ab5:1 Eb5:1 | D6:1.5! C6:.5 Bb5:1 F5:1 | Bb5:1 D6:1 G6:1.5! F6:.5 | Eb6:3 C6:1 | C6:1 Eb6:1 Ab6:1.5! G6:.5 | F6:1 D6:1 Bb5:2 | B5:1 D6:1 F6:1 Ab6:1! | G6:2 D6:2'
    return T('42_battle_org',[('intro','Cm Cm',3,184),('A','Cm Ab Bb G Cm Ab Fm G',2,184),('pre','Ab Bb Cm G',2,(184,190)),('ch','Ab Bb Gm Cm Ab Bb G G',3,190),('bd','Fm G Cm Cm',1,(160,184,2))],
      {'dist':(29,0,.25,0),'cs':(17,-1,.35,.15)},
      {'intro':[('dist',riff,100,12)],
       'A':[('dist','G4:1! C5:.5 Bb4:.5 G4:1 Eb4:1 | Eb4:.5 F4:.5 Ab4:1 C5:1.5! Bb4:.5 | Bb4:1 F4:.5 D4:.5 F4:1 Bb4:1 | D5:2! B4:1 G4:1 | G4:1! C5:.5 Bb4:.5 G4:1 Eb5:1 | Eb5:.5 D5:.5 C5:1 Ab4:1 C5:1 | F5:1! Eb5:.5 C5:.5 Ab4:1 F4:1 | G4:.5 Ab4:.5 B4:1 D5:2!',92,0)],
       'pre':[('dist','C5:1 Eb5:1 Ab5:1 G5:1 | F5:1 D5:1 Bb5:1 Ab5:1 | G5:.5 Eb5:.5 C5:.5 Eb5:.5 G5:.5 C6:.5 Bb5:.5 G5:.5 | B5:1! r:3',92,0)],
       'ch':[('dist',CH,108,0),('cs',CH,100,-12)],
       'bd':[('cs','Ab4:2 C5:2 | B4:2 D5:2 | C5:4 | r:4',96,0),('dist','r:4 | r:4 | r:4 | '+riff.split('|')[0],92,12)]},
      {'intro':['dist'],'A':['dist'],'pre':['dist'],'ch':['dist','cs'],'bd':['cs','dist']},style='rock',target=-14)

def t43():
    def ex(a):
        a.stem('glitch',None,-11,.2,.4);a.song.cfg['glitch']['syn']=dict(P_BELL)
        for b in a.bars():
            for t in np.random.choice(np.arange(0,4,.25),3 if b.lv<3 else 6,replace=False):a.n('glitch',b.bt+t,.08,fold(b.r,80,91)+np.random.choice([0,1,6,11]),76)
    return T('43_boss_raid',[('intro','Ebm E',3,176),('A','Ebm B Db Bbm Ebm E Ebm Bb',2,176),('ch','B Db Bbm Ebm B Db Bb Bb',3,180),('bd','Abm Bb7 Ebm Ebm',1,(146,176,2))],
      {'lead':(29,0,.3,0),'vox':(17,-1,.4,.15)},
      {'intro':[('lead','Eb4:.25 Eb4:.25 Bb4:.5 Eb5:1! r:2 | E4:.25 E4:.25 B4:.5 E5:1! r:1 Bb4:1',100,0)],
       'A':[('lead','Bb4:.5 Eb5:.5 Gb5:1! F5:.5 Eb5:.5 Bb4:1 | B4:1 D#5:.5 F#5:.5 B5:1.5! A#5:.5 | Ab5:1 F5:.5 Db5:.5 Ab4:1 Db5:1 | F5:2! Db5:1 Bb4:1 | Bb4:.5 Eb5:.5 Gb5:1 Bb5:1.5! Ab5:.5 | Ab5:1 E5:1 B4:2 | Eb5:.5 Gb5:.5 Bb5:1 Ab5:.5 Gb5:.5 Eb5:1 | F5:2! D5:1 Bb4:1',94,0)],
       'ch':[('lead','D#6:1.5! C#6:.5 B5:1 F#5:1 | F6:1.5! Eb6:.5 Db6:1 Ab5:1 | Db6:1 F6:1 Bb6:1.5! Ab6:.5 | Gb6:3 Eb6:1 | D#6:1 F#6:1 B6:1.5! A#6:.5 | Ab6:1 F6:1 Db6:2 | D6:1 F6:1 Bb6:2! | Bb6:2 F6:2',106,-12),('vox','D#6:1.5 C#6:.5 B5:1 F#5:1 | F6:1.5 Eb6:.5 Db6:1 Ab5:1 | Db6:1 F6:1 Bb6:1.5 Ab6:.5 | Gb6:3 Eb6:1 | D#6:1 F#6:1 B6:1.5 A#6:.5 | Ab6:1 F6:1 Db6:2 | D6:1 F6:1 Bb6:2 | Bb6:2 F6:2',98,-24)],
       'bd':[('vox','B4:2 Eb5:2 | D5:2 F5:2 | Gb5:4 | r:4',98,0)]},
      {'intro':['lead'],'A':['lead'],'ch':['lead','vox'],'bd':['vox']},style='rock',target=-14,extra=ex)


ALL=['t04','t06','t42','t43']
if __name__=='__main__':
    for f in (sys.argv[1:] or ALL):print('==',f);globals()[f]()
