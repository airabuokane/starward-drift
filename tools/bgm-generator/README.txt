BGM 生成コード(v10)
- song.py    : テンポ変化・セクションごとの音量・楽器ごとの音量差・主役との差の自動調整つきレンダラ
- synthx.py  : 旧版の音(アナログ風の減算シンセと合成ドラム)を秒単位で鳴らす部分
- kit.py     : セクション・コード・定番パターン・音色プリセット
- arr9.py    : 暗いアナログ・サイバーパンク用の汎用アレンジャ
- trk10a/b/c.py : 各曲(基本曲 / 星の街 / ダンジョンとエンディング)
- tracks5.py : 真エンディング(仲間が楽器を持ち寄る曲)  ※ t09 を実行
- lastboss12.py / lbend7.py / gf_mel.py : ラスボス(現行版)と撃破時の締め(TR=-1でG版、TR=-3でF版)
- lastboss6.py : ラスボスの1つ前の版
- lastboss5.py / lbend5.py : ラスボスの旧版
- pachi.py   : パチンコの曲(hall()=45 受付、normal()=46 通常)
- bonus4.py / rush4.py : パチンコの大当たり(47)・確変(48)
- trk11town.py : 街(02)。ラスボスのサビの出だしを引用した版
- trk11rock.py : 戦闘系4曲の90年代ロック版(arr9.py の style='rock')
- old/       : 旧版の生成コード
必要: numpy scipy pretty_midi pyfluidsynth、ffmpeg、libfluidsynth、GeneralUser-GS.sf2(song.py の SF にパスを書く)
