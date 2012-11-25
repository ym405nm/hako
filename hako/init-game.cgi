#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# ゲーム設定モジュール
# 使用条件、使用方法等は、qhako-readme.txtファイルを参照
#----------------------------------------------------------------------
# 究想の箱庭  (ver5.53)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 各種設定値
# (これ以降の部分の各設定値を、適切な値に変更してください)
#----------------------------------------------------------------------
#----------------------------------------
# ゲームの進行やファイルなど
#----------------------------------------
# トップページに表示するログのターン数
$HtopLogTurn = 12;

# ログファイル保持ターン数
$HlogMax = 12; 

# バックアップを何ターンおきに取るか
$HbackupTurn = 1;

# バックアップを何回分残すか
$HbackupTimes = 4;

# 発見ログ保持行数
$HhistoryMax = 10;

# 天気ログ保持行数(行数の指定しか出来ません)
$HWeatherMax = 400;

# 放棄コマンド自動入力ターン数
$HgiveupTurn = 28;

# write open の retry 回数
$HretryCount = 5;

#----------------------------------------
# 不正行為防止関係
#----------------------------------------

# ホスト名取得モード(ホスト名は現在使用していません)
#  --> 0 : $ENV{'REMOTE_HOST'} で取得できる場合
#  --> 1 : gethostbyaddr で取得できる場合
$get_remotehost = 1;

# COOKIEによるIDチェックをするか？(0:しない、1:する)
# 「する」にすると、同一ＰＣで複数の島を管理する時、COOKIEを削除しなければ別の島の開発画面に入れなくなります。
# 簡易重複対策なわけですが、島ごとにブラウザを変えることですぐにやぶられちゃいます(/_<。)
$checkID = 0;

# COOKIEによる「画像のローカル設定」もチェックする？(0:しない、1:する)
$checkImg = 0;

# COOKIEチェック（上の２つの設定）を免除する島のID
# 例：@freepass = (2, 7, 12);
@freepass = ();

# アクセスログをとるか？(0:とらない、1:開発画面に入る時と資源取引時、2:トップページ)
$HtopAxes = 1;
# 1にした場合、以下を設定
# ログファイル名
$HaxesLogfile = './axes.cgi';
# 最大記録件数
$HaxesMax = 500;

# 他人から資金を見えなくするか
# 0 見えない
# 1 見える
# 2 100の位で四捨五入
$HhideMoneyMode = 2;

# パスワードの暗号化(0だと暗号化しない、1だと暗号化する)
$cryptOn = 1;

#----------------------------------------
# 観光者通信(ローカル掲示版)
#----------------------------------------

# 使用するかどうか(0:使用しない、1:使用する)
$HuseLbbs = 1;

# IP表示
# 1のときはローカル掲示版、島作成時等にIPを表示する。マスター、島主、観光者も差別無く表示
$Hlipdisp = 0;

# ローカル掲示版のパスワード認証
# 他の島のオーナーが書き込むときにパスワード確認の有無(0:無、1:有)
$HlbbsAuth = 1;

# ローカル掲示版をパスワード認証する場合の設定
# 匿名発言(観光客選択)を許可するか(0:禁止、1:許可)
$HlbbsAnon = 0;

# ローカル掲示版をパスワード認証する場合の設定
# 発言に発言者の名前を表示するか(0:表示しない、1:表示する)
$HlbbsSpeaker = 1;

# 整地ログを１本化するか？(0:しない 1:座標あり 2:座標なし)
$HlogOmit2 = 1;

#----------------------------------------
# 資金、食料などの設定値と単位
#----------------------------------------
# 最大資金
$MaxMoney = 99999;

# 最大食料備蓄
$MaxFood = 99999;

# 最大資源(原油、鉱石、兵器)備蓄
$MaxSigen = 9999;

# お金の単位
$HunitMoney = '億円';

# 食料の単位
$HunitFood = '00トン';

# 鉱石の単位
$HunitOre = 'トン';

# 原油の単位
$HunitOil = '万バレル';

# 兵器の単位
$HunitWeapon = '万トン';

# 人口の単位
$HunitPop = '00人';

# 広さの単位
$HunitArea = '00万坪';

# 木の数の単位
$HunitTree = '00本';

# 木の単位当たりの売値
$HtreeValue = 5;

# 名前変更のコスト
$HcostChangeName = 0;

# 人口1単位あたりの食料消費料
$HeatenFood = 0.2;

# 宇宙工場、宇宙農場は、宇宙人口の何倍の規模分が稼働するか？
$HspaceEfficiency = 5; # ５倍

# 宇宙工場、宇宙農場の稼働している千人規模あたりの地上収入(億)
$HspaceIncome = 5;

#----------------------------------------
# 外見関係
#----------------------------------------

# <BODY>タグのオプション
$htmlBody = 'BGCOLOR="#EEFFFF"';
# 背景画像を指定する場合。画像は箱庭の画像フォルダに設置してください。ローカル指定している場合は画像配付してください。
#$htmlBody = 'BGCOLOR="#EEFFFF" BACKGROUND="kabe.gif"';

$htmlBgColor = 'BGCOLOR="#EEFFFF"';

# ゲームのタイトル文字 自由に変更して構いません。
$Htitle = '究想の箱庭';
$Htitle2 = $versionInfo;

# タグ
# タイトル文字
$HtagTitle_ = '<span class="title">';
$HtagTitle2_= '<span class="title2">';
$H_tagTitle = '</span>';

# 大きい文字
$HtagBig_ = '<span class="big">';
$H_tagBig = '</span>';

# 島の名前など
$HtagName_ = '<span class="islName">';
$H_tagName = '</span>';

# 薄くなった島の名前
$HtagName2_ = '<span class="islName2">';
$H_tagName2 = '</span>';

# 順位の番号など
$HtagNumber_ = '<span class="number">';
$H_tagNumber = '</span>';

# 順位表における見だし
$HtagTH_ = '<span class="head">';
$H_tagTH = '</span>';

# 開発計画の名前
$HtagComName_ = '<span class="command">';
$H_tagComName = '</span>';

# 災害
$HtagDisaster_ = '<span class="disaster">';
$H_tagDisaster = '</span>';

# ローカル掲示板、観光者の書いた文字
$HtagLbbsSS_ = '<span class="lbbsSS">';
$H_tagLbbsSS = '</span>';

# ローカル掲示板、島主の書いた文字
$HtagLbbsOW_ = '<span class="lbbsOW">';
$H_tagLbbsOW = '</span>';

# 通常の文字色
$HnormalColor_ = '<span class="normal">';
$H_normalColor = '</span>';

# 順位表、セルの属性
$HbgTitleCell	= 'class=TitleCell';	# 順位表見出し
$HbgSubTCell	= 'class=SubTCell';		# 順位表サブ見出し
$HbgNumberCell	= 'class=NumberCell';	# 順位表順位
$HbgNameCell	= 'class=NameCell';		# 順位表島の名前
$HbgInfoCell	= 'class=InfoCell';		# 順位表島の情報
$HbgCommentCell	= 'class=CommentCell';	# 順位表コメント欄
$HbgInputCell	= 'class=InputCell';	# 開発計画フォーム
$HbgMapCell		= 'class=MapCell';		# 開発計画地図
$HbgCommandCell	= 'class=CommandCell';	# 開発計画入力済み計画
$HbgLbbsCell	= 'class=LbbsCell';		# 観光者通信表示欄

#----------------------------------------
# 基地の経験値
#----------------------------------------

# 経験値の最大値
$HmaxExpPoint = 250;

# レベルの最大値
$maxBaseLevel = 6;  # ミサイル基地
$maxSBaseLevel = 4; # 海底基地

# 経験値がいくつでレベルアップか
@baseLevelUp = (20, 60, 120, 200, 250); # ミサイル基地
@sBaseLevelUp = (50, 200, 250);         # 海底基地

if($HwarFlg){
	$maxBaseLevel  = 9;
	$maxSBaseLevel = 6;
	@baseLevelUp  = (10, 30, 50, 70, 100, 150, 200, 250);
	@sBaseLevelUp = (20, 60, 120, 200, 250);
}

# 防衛施設の自爆 海底防衛施設も含まれる
# 怪獣に踏まれた時自爆するなら1、しないなら0
$HdBaseAuto = 1;

#----------------------------------------
# 災害
#----------------------------------------
# 災害半減期を導入するか？　する2(TOPに半減中と表示) する1 しない0
# 百の位が偶数の時、災害率が約半減します。
$Hdishangen = 0;

# 通常災害発生率(確率は0.1%単位)
$HdisEarthquake = 5;  # 地震
$HdisTsunami    = 15; # 津波
$HdisTyphoon    = 20; # 台風
$HdisMeteo      = 15; # 隕石
$HdisHugeMeteo  = 4;  # 巨大隕石
$HdisEruption   = 10; # 噴火
$HdisFire       = 10; # 火災
$HdisMaizo      = 10; # 埋蔵金
$HdisAkasio     = 30; # 赤潮
$HdisVGHarvest  = 10; # 大豊作
$HdisGHarvest   = 50; # 豊作
$HdisBHarvest   = 40; # 凶作
$HdisAEruption  = 4;  # 再噴火

$HdisPirate     = 20; # 海賊船
$HdisTreasureS  = 1;  # 宝船

$HdisTinka      = 9; # 温泉による地盤沈下(0.01%単位)

# 海底系(深い海の建造物全て)限界値(%)、これ以上増えるとシーいのらが出ます。
$HdisKLimit = 50;

# 人口１万人当たりの発生率
$HdisPollution    = 1;  # 公害(0.01%単位)
$HmaxdisPollution = 24; # 公害最大(0.1%単位)
$HdisCrime        = 10; # 犯罪(0.01%単位)(人口以外の要素もあります)

# 地盤沈下
$HdisFallBorder = 90; # 安全限界の広さ(Hex数)
$HdisFalldown   = 30; # その広さを超えた場合の確率

# 宇宙工場１つあたりに巨大隕石が発生する確率(0.0001%単位)
$HdisSHugeMeteo = 25; # ×開発面積

# 天候
@WeatherName = ('快晴','晴れ','曇り','濃霧','雨','大雨');
@WeatherIcon = ('weather/kaisei.gif','weather/hare.gif','weather/kumori.gif','weather/noumu.gif','weather/ame.gif','weather/ooame.gif');

#コメントのラベル画像 (4未使用。追加にはhako-main.cgiの改造が必要)by ShibaAni
@HlabelName = ('怪獣出現時にミサイル援護を拒否する<>怪獣出現時にミサイル援護を許可する','怪獣バトルでの遠征受入を拒否','資金援助できます','資金を援助して欲しい','予備1');
@HlabelImage = ('label00_2.gif<>label00_1.gif','label01.gif','label02.gif','label03.gif','label04.gif');

# 怪獣
$HdisMonsBorder1 = 1000; # 人口基準1(怪獣レベル1)
$HdisMonsBorder2 = 2500; # 人口基準2(怪獣レベル2)
$HdisMonsBorder3 = 4000; # 人口基準3(怪獣レベル3)
$HdisMonsBorder4 = 6000; # 人口基準4(怪獣レベル4)
$HdisMonsBorder5 = 8000; # 人口基準5(怪獣レベル5)
$HdisMonster     = 2.6;  # 単位面積あたりの出現率(0.01%単位)

# 単位面積あたりの埋め立ていのら、海風船の出現値（少ないほど確率が高い、サバイバルモード、$HdisMonster=0の場合は値に関係なく出現しない）
$HdisMonsterU    = 20000;

# 宇宙での怪獣の出現値（少ないほど確率が高い、$HdisMonster=0の場合は値に関係なく出現しない)
# 開発面積 ÷ $HdisSpaceMonster × 100 = 出現率(%)　(毎ターンこの確率で町系の数だけ判定)
$HdisSpaceMonster1 = 30000; # 怪獣有り
$HdisSpaceMonster2 = 10000; # 怪獣無り

# 海域での怪獣の出現値（少ないほど確率が高い、$HdisMonster=0の場合は値に関係なく出現しない)
# 1 ÷ $HdisSeaMonster × 100 = 出現率(%)　(毎ターンこの確率で海の数だけ判定)
$HdisSeaMonster = 8000;

# 種類
$HmonsterNumber  = 36; 

# 各基準において出てくる怪獣数と種類
$HmonsterL1Num = 2;
$HmonsterL2Num = 5;
$HmonsterL3Num = 7;
$HmonsterL4Num = 11;
$HmonsterL5Num = 12;
@HmonsterL1 = (1,2);
@HmonsterL2 = (1,2,3,4,5);
@HmonsterL3 = (1,2,3,4,5,6,7);
@HmonsterL4 = (1,3,4,5,6,7,8, 9,10,24,26);
@HmonsterL5 = (3,4,5,6,7,8,9,10,19,24,26,27);
# 宇宙怪獣
@HmonsterS = (32,33,34,35);

# 最低体力、体力の幅、特殊能力、荒らした後の地形、経験値、死体の値段
                   # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35
@HmonsterBHP     = ( 2, 1, 1, 3, 2, 1, 4, 5, 2, 3, 6, 2, 2, 1, 2, 2, 2, 2, 5, 8, 5, 3, 2, 2, 2, 1, 3, 6, 2, 2, 5, 1, 2, 4, 2, 6);
@HmonsterDHP     = ( 3, 2, 2, 2, 2, 0, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 3, 4, 2, 2, 0, 3, 2, 2, 2, 3);
@HmonsterSpecial = ( 2, 0, 3, 0, 1, 2, 4, 0, 2, 0, 1, 5, 5, 6, 7, 2, 0, 0, 8, 0, 7, 7, 8, 0, 0, 5, 2, 0, 0, 0, 9, 5, 0, 1, 2, 0);
@HmonsterDestroy = ( 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,15, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0);
@HmonsterExp     = (10, 5,7,12,15,10,20,30,100,35,50,10,20,15,40,15,15,20,80,70,60,40,12,20,90,10,30,10,10,10,60,10,15,20,25,40);
                   # 0    1    2    3    4    5    6    7    8    9
@HmonsterValue   = (  0, 400, 500,1000, 800, 300,1500,2000,1000,2000,
                   3000, 100,3000,1000,2000,1000,1200,1500,6000,4000,
                   3500,2000, 200,4000, 300, 100,2000, 500,1000,1000,
                   5000,9999,2000,3000,3500,5000);

# 特殊能力の内容は、
# 0 特になし
# 1 足が速い(最大2歩あるく)
# 2 足がとても速い(最大何歩あるくか不明)
# 3 奇数ターンは硬化
# 4 偶数ターンは硬化
# 5 常に硬化だが２５％であたる
# 6 命令処理より先に移動(0-1歩)
# 7 命令処理より先に移動(最大何歩あるくか不明)
# 8 周囲１へクスに霧を出す
# 9 回復する（毎ターンMAX）

# 名前(途中で変更するとランキングがおかしくなります)
@HmonsterName = 
    (
     'メカいのら',     # 0(人造)
     'いのら',         # 1
     'サンジラ',       # 2
     'レッドいのら',   # 3
     'ダークいのら',   # 4
     'いのらゴースト', # 5
     'クジラ',         # 6
     'キングいのら',   # 7
     'メタルいのら',   # 8
     'シーいのら',     # 9
     'デビルいのら',   # 10
     'メカジラ',       # 11(人造)
 'エンシェントいのら', # 12(地質調査)
     'イダテン',       # 13(汚染)
     'ラピットいのら', # 14(汚染)
     'ジバクレイ',     # 15(ゴーストが変化)
     '埋め立ていのら', # 16(海にランダム)
     'タイムボカン',   # 17(ミサイル数)
     '反撃いのら',     # 18(ミサイル数)
     'アシュラ',       # 19(ミサイル数)
     'スペースいのら', # 20(ミサイル数)
     'シーゴースト',   # 21(ミサイル数)
    'グラテネスいのら',# 22(人造)
     'カネゴン',       # 23
     'リッチいのら',   # 24
     '海底メカいのら', # 25
     '迷彩いのら',     # 26
     '分裂いのら',     # 27
     'てるてるいのら', # 28
     '逆さてるてる',   # 29
     '回復いのら',     # 30
    'ゴールドゴースト',# 31
     '宇宙怪獣(緑)',   # 32
     '宇宙怪獣(黄)',   # 33
     '宇宙怪獣(赤)',   # 34
     '宇宙怪獣(青)'    # 35
);

# 怪獣バトル用
@HmonsterSP      = ( 7, 4, 1, 7, 7, 3, 2, 7, 6, 0,10, 6, 6, 5, 5, 5, 0, 8, 7, 0, 9, 5, 0, 8, 0, 6, 5, 5, 0, 0,11, 8, 0, 7, 7, 9); # 特殊
                   # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35
@HmonsterSTR     = (10, 7, 7,10, 7, 2, 8,12, 4, 7,13, 3,11, 5, 7, 3, 8,12,15, 9, 9, 9, 7, 5,10,10, 7, 7, 7, 9,11,11, 7, 9,11,11); # 攻撃
@HmonsterDEF     = ( 2, 3, 5, 2, 2, 0, 5, 3, 7, 3, 1, 5, 5, 0, 0, 0, 3, 5, 0, 3, 3, 1, 3, 2, 3, 5, 1, 1, 3, 3, 3, 5, 3, 3, 3, 3); # 防御
@HmonsterAGI     = ( 6, 5, 2, 3, 9,14, 4, 5,11, 5, 5, 1, 2,15,17,19, 6,11, 5, 9,15,20, 5,10,10, 7,15,20, 5, 6, 9,15, 5, 6, 6,14); # 回避
@HmonsterSKL     = ( 2, 7, 6, 5, 9, 9, 7, 4, 7, 7,10, 1, 5,10,13,13, 8,12,12, 9,10,16, 7,10,10, 7,12,10, 7, 7, 9,12, 7, 7, 8,12); # 命中
       #  計(参考)  20 22 20 20 27 25 24 24 29 22 29 10 23 30 37 35 25 40 32 30 37 46 22 27 33 29 35 38 22 25 32 43 22 25 28 40

# 怪獣バトル進化用
@HmonsterGRP     = ( 0, 0, 1, 3, 2, 2, 1, 3, 1, 4, 3, 1, 1, 2, 2, 2, 4, 5, 3, 4, 4, 2, 5, 5, 5, 5, 4, 5, 3, 3, 4, 1, 6, 6, 6, 6); # グループ
@HmonsterCLS     = ( 0, 0, 1, 3, 1, 2, 2, 4, 4, 1, 5, 3, 5, 3, 4, 2, 2, 6, 6, 3, 6, 5, 1, 5, 2, 3, 4, 4, 1, 2, 5, 6, 1, 2, 3, 4); # 階級
@HmonsterSEI     = ( 0, 1, 4, 2, 4, 5, 4, 2, 4, 4, 4, 2, 1, 5, 5, 5, 4, 3, 3, 0, 5, 3, 4, 5, 4, 4, 5, 5, 2, 2, 4, 1, 2, 4, 3, 5); # 成長

# 成長
# 0 普通
# 1 成長率が高い
# 2 成長率が低い
# 3 攻撃の伸びがいい
# 4 守備が上がる
# 5 回避、命中の伸びがいい

# 画像ファイル
@HmonsterImage =
    (
     'monster7.gif',
     'monster0.gif',
     'monster5.gif', # 2
     'monster1.gif',
     'monster2.gif',
     'monster8.gif',
     'monster6.gif', # 6
     'monster3.gif',
     'monster9.gif',
     'monster10.gif',
     'monster11.gif', # 10
     'monster12.gif',
     'monster13.gif',
     'monster14.gif',
     'monster15.gif', # 14
     'monster16.gif',
     'monster17.gif',
     'monster18.gif',
     'monster19.gif', # 18
     'monster20.gif',
     'monster21.gif',
     'monster22.gif',
     'monster23.gif', # 22
     'monster24.gif',
     'monster25.gif',
     'monster26.gif',
     'land1.gif',     # 荒地
     'monster27.gif',
     'monster28.gif',
     'monster29.gif',
     'monster30.gif', # 30
     'monster31.gif',
     'cmonster1.gif',
     'cmonster2.gif',
     'cmonster3.gif', # 34
     'cmonster4.gif'
     );

# 画像ファイルその2(硬化中)
@HmonsterImage2 =
  ('','','monster4.gif','','','','monster4.gif','','','','','','','','','','','','','','','','','','','','','','','','','','','','','');
 # 0  1         2       3  4  5        6        7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35

#----------------------------------------
# 油田
#----------------------------------------
# 油田の収入(量)
$HoilMoney = 400;

# 油田の枯渇確率
$HoilRatio = 40;

#----------------------------------------
# 記念碑
#----------------------------------------
# 何種類あるか
$HmonumentNumber = 19;

# 通常ミサイルを効果なしにする場合１
$HmonumentMissile = 1;

# ロケット開始位置
$HmonumentRocket = 11;

# 名前
@HmonumentName = 
    (
     'モノリス',   #0
     '平和記念碑',
     '戦いの碑',
     '廉価記念碑',
     '予備記念碑',
     '予備記念碑', #5
     '予備記念碑',
     '予備記念碑',
     '災害の碑',
     '純金の碑',
     '怪獣記念碑', #10
     'ロケット記念碑',
     'ロケット台(LV1)',
     'ロケット台(LV2)',
     'ロケット台(LV3)',
     'ロケット台(LV4)', #15
     'ロケット台(LV5)',
     'ロケット台(LV6)',
     'ロケット台(LV7)'
    );

# 画像ファイル
@HmonumentImage = 
    (
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monumentP.gif',
     'monumentG.gif',
     'monumentM.gif',
     'monument3.gif',
     'monument4.gif',
     'monument4.gif',
     'monument4.gif',
     'monument4.gif',
     'monument4.gif',
     'monument4.gif',
     'monument4.gif'
     );

#----------------------------------------
# 海底記念碑
#----------------------------------------
# 何種類あるか
$HsmonumentNumber = 2;

# 名前
@HsmonumentName = 
    (
     '海底記念碑',
     '海底記念碑'
    );

# 画像ファイル
@HsmonumentImage = 
    (
     'smonument0.gif',
     'smonument1.gif'
     );

#----------------------------------------
# 賞関係
#----------------------------------------
# ターン杯を何ターン毎に出すか
$HturnPrizeUnit = 100;

# 賞の名前
@Hprize = ('ターン杯','繁栄賞','超繁栄賞','究極繁栄賞','平和賞',
			'超平和賞','究極平和賞','災難賞','超災難賞','究極災難賞',
			'宇宙賞','究想いのら賞');

# 部門賞を何ターン毎に出すか
$HturnPrizeVarious = 20;

# 部門賞の加算順位点
$HturnPrizePoint = 50;

# 部門賞の数
$HturnPrizeNumber = 14;

# 賞の名前
@HprizeV = ('','農業王','工業王','商業王','水産王',
			'森林王','ミサイル王','ハリボテ王','怪獣王','石油王',
			'災害王','船舶王','記念碑王','宇宙王','園芸王');

#----------------------------------------------------------------------
# 好みによって設定する部分は以上
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# これ以降のスクリプトは、変更されることを想定していませんが、
# いじってもかまいません。
# コマンドの名前、値段などは解りやすいと思います。
#----------------------------------------------------------------------

#----------------------------------------
# 船系
#----------------------------------------
#              賊 獣 イ 探 　 　 霊 宝 漁 漁 漁 竜 流 夫 客 風
@HshipHP    = ( 3, 2, 4, 2, 3, 3, 1, 1, 1, 2, 3, 4, 1, 2, 2, 6); # HP
@HshipKAI   = ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0); # 回復
@HshipSP    = ( 1, 0, 1, 1, 0, 1, 2, 2, 0, 0, 0, 2, 0, 0, 0, 1); # 速力(怪獣と同じ)
@HshipMATK  = ( 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0); # 対怪攻撃力
@HshipSATK  = ( 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); # 対艦攻撃力
@HshipEX    = (10, 5,12, 4,40,35,20,30, 2, 4, 6,60,10,10, 5, 5); # 経験値
@HshipMoney = ( 0,50,50,100,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); # 維持費
@HshipFood  = ( 0, 0, 0,100,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); # 維持食料
@HshipMoneyE= ( 0,50,50,100,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); # 維持費遠征
@HshipFoodE = ( 0, 0, 0,100,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); # 維持食料遠征

@HshipSell =(2000, 800,1500, 600,4000,
			 2000,1000,9999, 300, 700,
			 1200,1000,2000,2000,1200,1000);

# 指令
@Hshiporder = ('特殊','移動','防御','撤退','攻撃');

# 名前
@HshipName = ('海賊船','海獣掃討艇','イージス艦','海底探査船', '予備',
			'予備','幽霊船','宝船','小型漁船','中型漁船',
			'大型漁船','翼竜','流氷','夫婦岩','豪華客船',
			'海風船');

# 画像ファイル
@HshipImage = ( 'ship01.gif','ship02.gif','ship03.gif','ship04.gif','ship05.gif',
				'ship06.gif','land0.gif','ship08.gif','ship09.gif','ship10.gif',
				'ship11.gif','ship12.gif','ship13.gif','ship14.gif','ship15.gif',
				'ship16');

# 海系地形かどうかチェックする(-1対策で最後は0にすること)
# 1以上海系、2船、3防波堤
#           0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9
@HseaChk = (1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0, # 19
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, # 39
			0,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0, # 59
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, # 79
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, # 99
			0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #119
			2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0);#139

#----------------------------------------
# 地下系
#----------------------------------------

@Hunderground = ('地下空間','地下出口','地下梯子','地下','地下都市',
				'地下農場','地下工場','地下ミサイル基地','地下合成石油工場');

@HugImage = ('ug.gif','ug_dokan.gif','ug_hasigo.gif','ug_road.gif','ug_tosi.gif',
			'ug_farm.gif','ug_fact.gif','ug_kiti.gif','ug_oil.gif');

$HugSpace  = 0;
$HugDokan  = 1;
$HugHasigo = 2;
$HugRoad   = 3;
$HugTosi   = 4;
$HugFarm   = 5;
$HugFact   = 6;
$HugKiti   = 7;
$HugOil    = 8;

#----------------------------------------
# 富士山
#----------------------------------------
@HfujiImage = ('fuji/fuji1.gif','fuji/fuji2.gif','fuji/fuji3.gif');

#----------------------------------------
# 宇宙衛星
#----------------------------------------
@HsEisei      = ('気象衛星','観測衛星','迎撃衛星','軍事衛星','防衛衛星');
@HsEiseiImage = ('cosmo20.gif','cosmo21.gif','cosmo22.gif','cosmo23.gif','cosmo24.gif');

#----------------------------------------
# 周囲4ヘックスの座標 0-60
#----------------------------------------

@ax = (0, 1, 1, 1, 0,-1, 0, 1, 2, 2, 2, 1, 0,-1,-1,-2,-1,-1, 0,
		2, 2, 3, 3, 3, 2, 2, 1, 0,-1,-2,-2,-3,-2,-2,-1, 0, 1,
		2,3,3,4,4,4,3,3,2,1,0,-1,-2,-2,-3,-3,-4,-3,-3,-2,-2,-1,0,1);
@ay = (0,-1, 0, 1, 1, 0,-1,-2,-1, 0, 1, 2, 2, 2, 1, 0,-1,-2,-2,
		-3,-2,-1, 0, 1, 2, 3, 3, 3, 3, 2, 1, 0,-1,-2,-3,-3,-3,
		-4,-3,-2,-1,0,1,2,3,4,4,4,4,4,3,2,1,0,-1,-2,-3,-4,-4,-4,-4);

#----------------------------------------------------------------------
# 各種定数
#----------------------------------------------------------------------
# 地形番号
$HlandSea      = 0;  # 海
$HlandWaste    = 1;  # 荒地
$HlandPlains   = 2;  # 平地
$HlandTown     = 3;  # 町系
$HlandForest   = 4;  # 森
$HlandFarm     = 5;  # 農場
$HlandFactory  = 6;  # 工場
$HlandBase     = 7;  # ミサイル基地
$HlandDefence  = 8;  # 防衛施設
$HlandMountain = 9;  # 山
$HlandMonster  = 10; # 怪獣
$HlandSbase    = 11; # 海底基地
$HlandOil      = 12; # 海底油田
$HlandMonument = 13; # 記念碑
$HlandHaribote = 14; # ハリボテ
$HlandOsen     = 15; # 汚染
$HlandSlum     = 16; # スラム街
$HlandTower    = 17; # 商業ビル
$HlandSeisei   = 18; # 精製場
$HlandBank     = 19; # 銀行
$HlandStadium  = 20; # スタジアム
$HlandAmusement = 21; # 遊園地
$HlandCasino    = 22; # カジノ
$HlandPark      = 23; # 公園
$HlandSchool    = 24; # 学校
$HlandDome      = 25; # ドーム
$HlandAirport   = 26; # 空港
$HlandFire      = 27; # 消防署
$HlandWarp      = 28; # 転移装置
$HlandZoo       = 29; # 動物園
$HlandBigcity   = 30; # 大都市
$HlandExpo      = 31; # 博覧会
$HlandMegacity  = 32; # 巨大都市
$HlandMegatower = 33; # 巨大ビル
$HlandMegaFact  = 34; # 巨大工場
$HlandDeathtrap = 35; # デストラップ
$HlandWindmill  = 36; # 風車
$HlandMyhome    = 37; # マイホーム
$HlandWarpR     = 38; # 転移先装置
$HlandPort      = 39; # 港
$HlandPolice    = 40; # 警察署
$HlandKInora    = 41; # 究想いのら
$HlandTrump     = 42; # トランプ
$HlandFlower    = 43; # 花
$HlandDokan     = 44; # 土管
$HlandFuji      = 45; # 富士山
$HlandTcity     = 46; # 商業都市
$HlandMegaFarm  = 47; # 巨大農場
$HlandHugecity  = 48; # 超巨大都市
$HlandBreakwater= 49; # 防波堤
$HlandSMonument = 50; # 海底記念碑
$HlandHospital  = 51; # 病院

# 海域用
$HlandOcean     = 71; # 無人島(変更する場合hako-mente.cgiも)
$HlandOPlayer   = 72; # プレイヤー島
$HlandOmonster  = 73; # モンスター(未使用)

# 海系
$HlandPirate    = 101; # 海賊船

$HlandMonsShip  = 102; # 海獣掃討艇
$HlandAegisShip = 103; # イージス艦
$HlandProbeShip = 104; # 海底探査船

$HlandGhostShip = 107; # 幽霊船
$HlandTreasureS = 108; # 宝船
$HlandFishSShip = 109; # 小型漁船
$HlandFishMShip = 110; # 中型漁船
$HlandFishLShip = 111; # 大型漁船
$HlandWingDragon= 112; # 翼竜
$HlandIceFloe   = 113; # 流氷
$HlandCoupleRock= 114; # 夫婦岩
$HlandTitanic   = 115; # 豪華客船
$HlandBalloonS  = 116; # 海風船

# 宇宙用
$HlandEarth = 201; # 地球
$HlandSunit = 202; # 宇宙ユニット
$HlandSCity = 203; # 宇宙都市

$HlandSFarm    = 205; # 宇宙農場
$HlandSFactory = 206; # 宇宙工場
$HlandSpaceBase= 207; # 宇宙ミサイル基地
$HlandSDefence = 208; # 宇宙防衛施設

$HlandSAEisei  = 210; # 宇宙衛星

# コマンド
# ミサイルと一緒に出来るのは0-19、90-
@HcommandDivido = 
	(
	'開発,0,17',
	'建設,18,49',
	'ミサイル,50,65',
	'攻撃,66,89',
	'運営,90,109',
	'怪獣,110,119',
	'宇宙,120,139',
	'海域,140,149'
	);
# 注意：スペースは入れないように
# ○→	'開発,0,10',  # 計画番号00〜10
# ×→	'開発, 0  ,10  ',  # 計画番号00〜10

# 計画番号の設定
# 整地系 9
$HcomPrepare  = 1; # 整地
$HcomPrepare2 = 2; # 地ならし
$HcomReclaim  = 3; # 埋め立て
$HcomReclaim2 = 4; # 高速埋め立て
$HcomDestroy  = 5; # 掘削
$HcomSellTree = 6; # 伐採
$HcomSearch   = 7; # 地質調査
$HcomPioneer  = 8; # 入植
$HcomDestroy2 = 9; # 高速掘削

# 作る系 29
$HcomPlant    = 11; # 植林
$HcomFarm     = 12; # 農場整備
$HcomFactory  = 13; # 工場建設
$HcomMountain = 14; # 採掘場整備
$HcomBank     = 15; # 銀行
$HcomPresent  = 16; # プレゼント建設

$HcomShipbuild	= 18; # 造船
$HcomSMonument	= 20; # 海底記念碑建造
$HcomBase		= 21; # ミサイル基地建設
$HcomDbase		= 22; # 防衛施設建設
$HcomSbase		= 23; # 海底基地建設
$HcomMonument	= 24; # 記念碑建造

$HcomHaribote	= 25; # ハリボテ設置
$HcomScity		= 26; # 海底都市建設
$HcomSFarm		= 27; # 海底農場整備
$HcomTower		= 28; # 商業ビル整備
$HcomFire		= 29; # 消防署
$HcomWarp		= 30; # 転移装置作成
$HcomWindmill	= 31; # 風車作成
$HcomMyhome		= 32; # マイホーム作成
$HcomDeathtrap	= 33; # デストラップ作成
$HcomPort		= 34; # 港建設
$HcomPolice		= 35; # 警察署建設
$HcomTrump		= 36; # トランプ設置
$HcomFlower		= 37; # 花を植える
$HcomBreakwater	= 38; # 防波堤を建設
$HcomHospital	= 39; # 病院建設

$HcomDokan		= 45; # 土管(地下)建設
$HcomUg			= 46; # 地下建設

# 攻撃系 24
$HcomMissileNM	= 50; # ミサイル発射
$HcomMissilePP	= 51; # PPミサイル発射
$HcomMissileSPP	= 52; # SPPミサイル発射
$HcomMissileDM	= 53; # 拡散弾発射
$HcomMissileST	= 54; # STミサイル発射
$HcomMissileLD	= 55; # 陸地破壊弾発射
$HcomMissilePLD	= 56; # 破壊PP弾発射
$HcomMissileRM	= 57; # 埋め立て弾発射
$HcomMissileSRM	= 58; # S埋め立て弾発射
$HcomBioMissile	= 59; # バイオミサイル
$HcomMissileNCM	= 60; # 核ミサイル発射
$HcomMissileMGM	= 61; # 怪獣誘導弾発射
$HcomMissileGM	= 62; # 誘導弾発射
$HcomMissileRNG	= 63; # リングミサイル発射


$Hcomcolony			= 69; # コロニー落し
$HcomSendMonster	= 70; # 怪獣派遣
$HcomManipulate		= 71; # 怪獣操作
$HcomSTManipulate	= 72; # ST怪獣操作
$HcomSpy			= 73; # 工作員
$HcomTeisatu		= 74; # 偵察
$HcomDummy			= 75; # ダミー命令
$HcomSSendMonster	= 76; # S怪獣派遣
$HcomShip			= 80; # 船指令変更
$HcomShipM			= 81; # 船全体操作

# 運営系 15
$HcomShipSell	= 92; # 船売却
$HcomSell		= 93; # 食料売却
$HcomMoney		= 94; # 資金援助
$HcomFood		= 95; # 食料援助
$HcomPropaganda	= 96; # 誘致活動
$HcomDoNothing	= 97; # 資金繰り
$HcomPresentAid	= 98; # プレゼント譲渡
$HcomEmigration	= 99; # 移民
$HcomGiveup		= 100; # 島の放棄
$HcomOreSell	= 101; # 鉱石売却(援助)
$HcomOilSell	= 102; # 原油売却(援助)
$HcomWeponSell	= 103; # 兵器売却(援助)
$HcomOreBuy		= 104; # 鉱石購入
$HcomOilBuy		= 105; # 原油購入
$HcomWeponBuy	= 106; # 兵器購入

# 怪獣バトル系 8 (全てターンはかかりません)
$HcomMonsEgg	= 110; # 怪獣エッグ購入
$HcomMonsEsa	= 111; # 怪獣に餌
$HcomMonsEnsei	= 112; # 怪獣遠征
$HcomMonsTettai	= 113; # 怪獣撤退
$HcomMonsEsaAid	= 114; # 怪獣餌譲渡
$HcomMonsAid	= 115; # 怪獣譲渡
$HcomMonsSell	= 116; # 怪獣売却
$HcomMonsExer	= 117; # 怪獣模擬訓練

# 宇宙開発系
$HcomSUnit		= 120; # 宇宙ユニット建設
$HcomSFood		= 121; # 宇宙食料打上げ
$HcomSPioneer	= 122; # 宇宙入植
$HcomSBuild		= 123; # 宇宙建設系
$HcomSpaceFarm	= 124; # 宇宙農場建設
$HcomSFactory	= 125; # 宇宙工場建設
$HcomSOccupy	= 126; # 宇宙占領
$HcomSMissileGM	= 127; # 宇宙誘導ミサイル発射
$HcomSpaceBase	= 128; # 宇宙ミ基地建設
$HcomSDestroy	= 129; # 宇宙ユニット破壊
$HcomSMissileMGM= 130; # 宇宙怪獣誘導
$HcomSMissilePP	= 131; # 宇宙PPミサイル発射
$HcomSMissile	= 132; # 宇宙ミサイル発射
$HcomSDbase		= 133; # 宇宙防衛施設建設
$HcomSEisei		= 134; # 宇宙衛星建設

$HcomOMissileNM		= 140; # 海域ミサイル
$HcomOMissilePP		= 141; # 海域PPミサイル
$HcomOMissileSPP	= 142; # 海域SPPミサイル

# 自動入力系、放棄 4
$HcomAutoPrepare	= 184; # フル整地
$HcomAutoPrepare2	= 185; # フル地ならし
$HcomAutoSellTree	= 186; # フル伐採
$HcomAutoDelete		= 188; # 全コマンド消去

# 特殊命令($HcommandTotalには含めないこと)
$HcomSpecialSPP	= 200;

# 計画の名前と値段
$HcomName[$HcomPrepare]  = '整地';
$HcomCost[$HcomPrepare]  = 5;
$HcomName[$HcomPrepare2] = '地ならし';
$HcomCost[$HcomPrepare2] = 100;
$HcomName[$HcomReclaim]  = '埋め立て';
$HcomCost[$HcomReclaim]  = 150;
$HcomName[$HcomReclaim2] = '高速埋め立て';
$HcomCost[$HcomReclaim2] = 800;
$HcomName[$HcomDestroy]  = '掘削';
$HcomCost[$HcomDestroy]  = 200;
$HcomName[$HcomDestroy2]  = '高速掘削';
$HcomCost[$HcomDestroy2]  = 800;
$HcomName[$HcomSearch]   = '地質調査';
$HcomCost[$HcomSearch]   = 1000;
$HcomName[$HcomSellTree] = '伐採';
$HcomCost[$HcomSellTree] = 0;
$HcomName[$HcomPlant]    = '植林';
$HcomCost[$HcomPlant]    = 50;
$HcomName[$HcomBank]     = '銀行投資';
$HcomCost[$HcomBank]     = 1000;
$HcomName[$HcomPioneer]  = '入植';
$HcomCost[$HcomPioneer]  = -500;
$HcomName[$HcomFarm]     = '農場整備';
$HcomCost[$HcomFarm]     = 20;
$HcomName[$HcomFactory]  = '工場建設';
$HcomCost[$HcomFactory]  = 100;
$HcomName[$HcomMountain] = '採掘場整備';
$HcomCost[$HcomMountain] = 300;
$HcomName[$HcomPresent]  = 'プレゼント建設';
$HcomCost[$HcomPresent]  = 0;
$HcomName[$HcomPresentAid] = 'プレゼント譲渡';
$HcomCost[$HcomPresentAid] = 0;
$HcomName[$HcomBase]     = 'ミサイル基地建設';
$HcomCost[$HcomBase]     = 300;
$HcomName[$HcomDbase]    = '防衛施設建設';
$HcomCost[$HcomDbase]    = 500;
$HcomName[$HcomSbase]    = '海底基地建設';
$HcomCost[$HcomSbase]    = 8000;
$HcomName[$HcomMonument] = '記念碑建造';
$HcomCost[$HcomMonument] = 9999;
$HcomName[$HcomSMonument] = '海底記念碑建造';
$HcomCost[$HcomSMonument] = 19999;
$HcomName[$HcomHaribote] = 'ハリボテ設置';
$HcomCost[$HcomHaribote] = 100;
$HcomName[$HcomScity]    = '海底都市建設';
$HcomCost[$HcomScity]    = 1000;
$HcomName[$HcomSFarm]    = '海底農場整備';
$HcomCost[$HcomSFarm]    = 600;
$HcomName[$HcomTower]    = '商業ビル整備';
$HcomCost[$HcomTower]    = 400;
$HcomName[$HcomFire]     = '消防署建設';
$HcomCost[$HcomFire]     = 600;
$HcomName[$HcomWindmill] = '風車建設';
$HcomCost[$HcomWindmill] = 3000;
$HcomName[$HcomMyhome]   = 'マイホーム建設';
$HcomCost[$HcomMyhome]   = 500;
$HcomName[$HcomPort]     = '港建設';
$HcomCost[$HcomPort]     = 800;
$HcomName[$HcomPolice]   = '警察署建設';
$HcomCost[$HcomPolice]   = 1000;
$HcomName[$HcomHospital] = '病院建設';
$HcomCost[$HcomHospital] = 1000;
$HcomName[$HcomTrump]    = 'トランプ設置';
$HcomCost[$HcomTrump]    = 1500;
$HcomName[$HcomFlower]   = 'お花を植える';
$HcomCost[$HcomFlower]   = 100;
$HcomName[$HcomBreakwater]= '防波堤建設';
$HcomCost[$HcomBreakwater]= 300;
$HcomName[$HcomDokan]	= '土管(地下)建設';
$HcomCost[$HcomDokan]	= 1000;
$HcomName[$HcomUg]		= '地下建設';
$HcomCost[$HcomUg]		= 800;
$HcomName[$HcomShipbuild]  = '造船';
$HcomCost[$HcomShipbuild]  = 500;
$HcomName[$HcomManipulate] = '怪獣操作';
$HcomCost[$HcomManipulate] = 700;
$HcomName[$HcomSTManipulate] = 'ST怪獣操作';
$HcomCost[$HcomSTManipulate] = 1500;
$HcomName[$HcomSpy]          = '工作員派遣';
$HcomCost[$HcomSpy]          = 3800;
$HcomName[$HcomTeisatu]      = '偵察';
$HcomCost[$HcomTeisatu]      = 300;
$HcomName[$HcomWarp]         = '転移装置建設';
$HcomCost[$HcomWarp]         = 1800;
$HcomName[$HcomDeathtrap]    = 'デストラップ建設';
$HcomCost[$HcomDeathtrap]    = 350;
$HcomName[$Hcomcolony]       = 'コロニー落し';
$HcomCost[$Hcomcolony]       = ($HwarFlg) ? 26000 : 34000;
$HcomName[$HcomBioMissile]   = 'バイオミサイル';
$HcomCost[$HcomBioMissile]   = 170;
$HcomName[$HcomMissileNM]    = 'ミサイル発射';
$HcomCost[$HcomMissileNM]    = 20;
$HcomName[$HcomMissilePP]    = 'PPミサイル発射';
$HcomCost[$HcomMissilePP]    = 40;
$HcomName[$HcomMissileSPP]   = 'SPPミサイル発射';
$HcomCost[$HcomMissileSPP]   = 50;
$HcomName[$HcomMissileRNG]   = 'リングミサイル発射';
$HcomCost[$HcomMissileRNG]   = 60;
$HcomName[$HcomMissileST]    = 'STミサイル発射';
$HcomCost[$HcomMissileST]    = 150;
$HcomName[$HcomMissileLD]    = '陸地破壊弾発射';
$HcomCost[$HcomMissileLD]    = 180;
$HcomName[$HcomSendMonster]  = '怪獣派遣';
$HcomCost[$HcomSendMonster]  = 3000;
$HcomName[$HcomSSendMonster] = 'S怪獣派遣';
$HcomCost[$HcomSSendMonster] = 6000;
$HcomName[$HcomMissileRM]    = '埋め立て弾発射';
$HcomCost[$HcomMissileRM]    = 100;
$HcomName[$HcomMissileSRM]   = 'S埋め立て弾発射';
$HcomCost[$HcomMissileSRM]   = ($HwarFlg) ? 800 : 3000;
$HcomName[$HcomMissileGM]    = '誘導弾発射';
$HcomCost[$HcomMissileGM]    = 1000;
$HcomName[$HcomMissileMGM]   = '怪獣誘導弾発射';
$HcomCost[$HcomMissileMGM]   = 1000;
$HcomName[$HcomMissileDM]    = '拡散弾発射';
$HcomCost[$HcomMissileDM]    = 30;
$HcomName[$HcomMissileNCM]   = '核ミサイル発射';
$HcomCost[$HcomMissileNCM]   = ($HwarFlg) ? 6000 : 9800;
$HcomName[$HcomMissilePLD]   = '破壊PP弾発射';
$HcomCost[$HcomMissilePLD]   = 200;
$HcomName[$HcomDummy]        = 'ダミー命令';
$HcomCost[$HcomDummy]        = 10;
$HcomName[$HcomShip]         = '船指令変更';
$HcomCost[$HcomShip]         = 100;
$HcomName[$HcomShipM]        = '船全体移動';
$HcomCost[$HcomShipM]        = 300;
$HcomName[$HcomDoNothing]    = '資金繰り';
$HcomCost[$HcomDoNothing]    = 0;
$HcomName[$HcomShipSell]     = '船売却';
$HcomCost[$HcomShipSell]     = 0;
$HcomName[$HcomSell]         = '食料売却';
$HcomCost[$HcomSell]         = -100;
$HcomName[$HcomOreSell]      = '鉱石売却・援助';
$HcomCost[$HcomOreSell]      = 0;
$HcomName[$HcomOilSell]      = '原油売却・援助';
$HcomCost[$HcomOilSell]      = 0;
$HcomName[$HcomWeponSell]    = '兵器売却・援助';
$HcomCost[$HcomWeponSell]    = 0;
$HcomName[$HcomOreBuy]       = '鉱石購入';
$HcomCost[$HcomOreBuy]       = 2;
$HcomName[$HcomOilBuy]       = '原油購入';
$HcomCost[$HcomOilBuy]       = 5;
$HcomName[$HcomWeponBuy]     = '兵器購入';
$HcomCost[$HcomWeponBuy]     = 24;
$HcomName[$HcomMoney]        = '資金援助';
$HcomCost[$HcomMoney]        = 100;
$HcomName[$HcomFood]         = '食料援助';
$HcomCost[$HcomFood]         = -100;
$HcomName[$HcomEmigration]   = '移民';
$HcomCost[$HcomEmigration]   = -100;
$HcomName[$HcomPropaganda]   = '誘致活動';
$HcomCost[$HcomPropaganda]   = 1000;
$HcomName[$HcomMonsEgg]      = '怪獣エッグ購入';
$HcomCost[$HcomMonsEgg]      = 3000;
$HcomName[$HcomMonsEsa]      = '怪獣に餌';
$HcomCost[$HcomMonsEsa]      = 500;
$HcomName[$HcomMonsEnsei]    = '怪獣遠征';
$HcomCost[$HcomMonsEnsei]    = 500;
$HcomName[$HcomMonsTettai]   = '怪獣撤退';
$HcomCost[$HcomMonsTettai]   = 0;
$HcomName[$HcomMonsEsaAid]   = '怪獣餌譲渡';
$HcomCost[$HcomMonsEsaAid]   = 0;
$HcomName[$HcomMonsAid]      = '怪獣譲渡';
$HcomCost[$HcomMonsAid]      = 0;
$HcomName[$HcomMonsSell]     = '怪獣売却';
$HcomCost[$HcomMonsSell]     = 0;
$HcomName[$HcomMonsExer]     = '怪獣模擬訓練';
$HcomCost[$HcomMonsExer]     = 500;

$HcomName[$HcomSUnit]		= '宇宙ユニット建設';
$HcomCost[$HcomSUnit]		= 400;
$HcomName[$HcomSFood]		= '宇宙食料打上げ';
$HcomCost[$HcomSFood]		= 1000;
$HcomName[$HcomSPioneer]	= '宇宙入植';
$HcomCost[$HcomSPioneer]	= 1000;
$HcomName[$HcomSBuild]		= '宇宙建設系';
$HcomCost[$HcomSBuild]		= 1000;
$HcomName[$HcomSMissileGM]	= '宇宙誘導ミサイル発射';
$HcomCost[$HcomSMissileGM]	= 200;
$HcomName[$HcomSMissilePP]	= '宇宙PPミサイル発射';
$HcomCost[$HcomSMissilePP]	= 200;
$HcomName[$HcomSMissile]	= '宇宙ミサイル発射';
$HcomCost[$HcomSMissile]	= 300;
$HcomName[$HcomSMissileMGM]	= '宇宙怪獣誘導弾発射';
$HcomCost[$HcomSMissileMGM]	= 1400;
$HcomName[$HcomSOccupy]		= '宇宙占領';
$HcomCost[$HcomSOccupy]		= 1000;
$HcomName[$HcomSpaceFarm]	= '宇宙農場建設';
$HcomCost[$HcomSpaceFarm]	= 500;
$HcomName[$HcomSFactory]	= '宇宙工場建設';
$HcomCost[$HcomSFactory]	= 1000;
$HcomName[$HcomSpaceBase]	= '宇宙ミ基地建設';
$HcomCost[$HcomSpaceBase]	= 1000;
$HcomName[$HcomSDbase]		= '宇宙防衛施設建設';
$HcomCost[$HcomSDbase]		= 1000;
$HcomName[$HcomSEisei]		= '宇宙衛星建設';
$HcomCost[$HcomSEisei]		= 2000;
$HcomName[$HcomSDestroy]	= '宇宙ユニット破壊';
$HcomCost[$HcomSDestroy]	= 200;

$HcomName[$HcomOMissileNM]	= '海域ミサイル';
$HcomCost[$HcomOMissileNM]	= 40;
$HcomName[$HcomOMissilePP]	= '海域PPミサイル';
$HcomCost[$HcomOMissilePP]	= 50;
$HcomName[$HcomOMissileSPP]	= '海域SPPミサイル';
$HcomCost[$HcomOMissileSPP]	= 60;

$HcomName[$HcomGiveup]		= '島の放棄';
$HcomCost[$HcomGiveup]		= 0;
$HcomName[$HcomAutoPrepare]	= '整地自動入力';
$HcomCost[$HcomAutoPrepare]	= 0;
$HcomName[$HcomAutoPrepare2]= '地ならし自動入力';
$HcomCost[$HcomAutoPrepare2]= 0;
$HcomName[$HcomAutoSellTree]= '伐採自動入力';
$HcomCost[$HcomAutoSellTree]= 0;
$HcomName[$HcomAutoDelete]	= '全計画を白紙撤回';
$HcomCost[$HcomAutoDelete]	= 0;

1;