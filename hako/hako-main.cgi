#!/usr/local/bin/perl --
# ↑はサーバーに合わせて変更して下さい。
# perl5用です。
#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# メインスクリプト(ver1.02)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 究想の箱庭「みんなで歩む箱庭進化論」
$versionInfo = "version5.54e";
#----------------------------------------------------------------------
BEGIN {
########################################
# エラー表示
$SIG{__WARN__} =
sub {
	my($msg) = @_;

	print STDOUT <<END;
Content-type: text/html

<p><big><tt>WARNNING: $msg</tt></big></p>
END
};

$SIG{__DIE__} =
sub {
	my($msg) = @_;

	print STDOUT <<END;
Content-type: text/html

<p><big><tt>ERROR: $msg</tt></big></p>
END
exit(-1);
};

$SIG{KILL} =
sub {
	my($msg) = @_;

	print STDOUT <<END;
Content-type: text/html

<p><big><tt>KILL: $msg</tt></big></p>
END
exit(-1);
};
########################################
}
#----------------------------------------------------------------------
# 環境設定部分は"hako-init.cgi"および"init-game.cgi"にあります。
#----------------------------------------------------------------------
require './hako-init.cgi';
require './hako-io.cgi';
require './init-game.cgi';

# 異常終了基準時間
# (ロック後何秒で、強制解除するか)
my($unlockTime) = 120;

#----------------------------------------------------------------------
# 変数
#----------------------------------------------------------------------

# COOKIE
#my($defaultID);   # 島の名前
$defaultID;     # 島の名前
$defaultTarget; # ターゲットの名前


# 島の座標数
$HpointNumber = $HislandSize * $HislandSize;

# 海域の座標数
$HpointOcean = $HoceanSize * $HoceanSize;

#----------------------------------------------------------------------
# メイン
#----------------------------------------------------------------------

get_host(0);

# 「戻る」リンク
$HtempBack = "<A HREF=\"$HthisFile\">${HtagBig_}トップへ戻る${H_tagBig}</A>";
$Body = "<BODY $htmlBody>";

# ロックをかける
if(!hakolock()) {
	# ロック失敗
	# ヘッダ出力
	tempHeader();

	# ロック失敗メッセージ
	tempLockFail();

	# フッタ出力
	tempFooter();

	# 終了
	exit(0);
}

# 乱数の初期化
srand(time^$$);

# COOKIE読みこみ
cookieInput();

# CGI読みこみ
cgiInput();

if (-e $HpasswordFile) {
	# パスワードファイルがある
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword  = <PIN>); # マスタパスワードを読み込む
	chomp($HspecialPassword = <PIN>); # 特殊パスワードを読み込む
	close(PIN);
} else {
	unlock();
	tempHeader();
	tempNoPasswordFile();
	tempFooter();
	exit(0);
}
# 直リンク禁止
if($Hlinkcheck){
unless(($HmainMode eq 'print') || ($HmainMode eq 'owner') || ($HmainMode eq 'landmap')){
L_LINK_CHECK:
{
	my($referer) = $ENV{HTTP_REFERER};
	local($_);
	for (@HokURL, $HthisFile) {
	    last L_LINK_CHECK if ($referer =~ /^$_/); # 許可ページか？
	}
	# エラー
	print "Location: $HjumpURL\n\n\n";
	exit;
}
}
}
# メンテモード
if((-e "./mente_lock") && !checkMasterPassword($HdefaultPassword)) {
	cookieOutput();
	unlock();
	mente_mode(1);
}
# 島データの読みこみ
if(readIslandsFile($HcurrentID) == 0) {
	unlock();
	tempHeader();
	tempNoDataFile();
	tempFooter();
	exit(0);
}

# テンプレートを初期化
tempInitialize();

# COOKIEによるIDチェック
if($HmainMode eq 'owner') {
	# アクセス・ログ
	axeslog() if($HtopAxes == 1);
	
	unless($ENV{'HTTP_COOKIE'}) {
		cookieOutput(); # COOKIEが削除されたかどうか書き込みチェック
		next if($ENV{'HTTP_COOKIE'}); # 書き込みOK
		# クッキーを有効にしていない
		unlock();
		tempHeader();
		tempWrong("クッキーを有効にしてください。");
		tempFooter();
		exit(0);
	}
	if($checkID || $checkImg) {
		# idから島を取得
		my($pcheck) = checkPassword($Hislands[$HidToNumber{$HcurrentID}]->{'password'},$HinputPassword);
		my $free = 0;
		foreach (@freepass){
			$free += 1 if(($_ == $defaultID) || ($_ == $HcurrentID));
		}
		my($icheck) = !($checkID && ($HcurrentID != $defaultID) && $defaultID);
		my($lcheck) = !($checkImg && ($HimgLine eq '' || $HimgLine eq $HimageDir));
		# パスワード
		if(($pcheck != 2) && ($free != 2) && (!$icheck || !$lcheck)) {
			# １つの島を初心者用に解放する時などは ($free != 2) の部分を !$free に変更して下さい。
			unlock();
			tempHeader();
			if(!$icheck) {
				tempWrong("自分の島以外には入れません！"); # ID違い
			} else {
				tempWrong("「画像のローカル設定」をして下さい。"); # ローカル設定していない
			}
			tempFooter();
			exit(0);
		}
	}
}

# COOKIE出力
cookieOutput();

if($HmainMode eq 'owner' && $HjavaMode eq 'java' ||
	$HmainMode eq 'monsedit' && $HjavaMode eq 'java' || # 怪獣編集
	$HmainMode eq 'commandJava' || # コマンド入力モード
	$HmainMode eq 'command2' || # コマンド入力モード（ver1.1より追加・自動系用）
	$HmainMode eq 'comment' && $HjavaMode eq 'java' || #コメント入力モード
	$HmainMode eq 'lbbs' && $HjavaMode eq 'java') { #コメント入力モード
	
	require('hako-js.cgi');
	require('hako-map.cgi');
	
	# ヘッダ出力
	tempHeader(1);
	if($HmainMode eq 'commandJava') {
		# 開発モード
		commandJavaMain();
	} elsif($HmainMode eq 'monsedit') {
		# 怪獣設定
		monsMain();
	} elsif($HmainMode eq 'command2') {
		# 開発モード２（自動系コマンド用（ver1.1より追加・自動系用））
		commandMain();
	} elsif($HmainMode eq 'comment') {
		# コメント入力モード
#		if($Hrsswrite){require('hako-rss.cgi');rssMain();}
		commentMain();
	} elsif($HmainMode eq 'lbbs') {
		# ローカル掲示板モード
#		if($Hrsswrite){require('hako-rss.cgi');rssMain();}
		localBbsMain();
	}else{
	    ownerMain();
	}
	# フッタ出力
	tempFooter();
	# 終了
	exit(0);
}elsif($HmainMode eq 'landmap'){
	require('hako-js.cgi');
	require('hako-map.cgi');
	if($HcurrentID == 999){
		# 宇宙
		$Body = "<BODY BGCOLOR=\"BLACK\" TEXT=\"WHITE\" LINK=\"#AAAAFF\" ALINK=\"GREEN\" VLINK=\"#AAAAFF\" BACKGROUND=\"star.gif\" BGPROPERTIES=FIXED>";
		$HskinName = 'space.css';
		tempHeader();
		printIslandJava(3);
	}elsif($HcurrentID == 888){
		# 海域
		$Body = "<BODY BGCOLOR=\"BULE\" TEXT=\"WHITE\" LINK=\"#AAAAFF\" ALINK=\"GREEN\" VLINK=\"#AAAAFF\" BACKGROUND=\"land0.gif\" BGPROPERTIES=FIXED>";
		$HskinName = 'ocean.css';
		tempHeader();
		printIslandJava(4);
	}elsif($Hugmode){
		# 地下
		tempHeader();
		printIslandJava(10);
	}else{
		tempHeader();
		printIslandJava(0);
	}
	# フッタ出力
	tempFooter();
	# 終了
	exit(0);
}elsif($HmainMode eq 'space'){
	$Body = "<BODY BGCOLOR=\"BLACK\" TEXT=\"WHITE\" LINK=\"#AAAAFF\" ALINK=\"GREEN\" VLINK=\"#AAAAFF\" BACKGROUND=\"star.gif\" BGPROPERTIES=FIXED>";
	$HskinName = 'space.css';
	tempHeader();
	require('hako-map.cgi');
	spaceMap();
	tempFooter();
	exit(0);
}elsif($HmainMode eq 'ocean'){
	$Body = "<BODY BGCOLOR=\"BULE\" TEXT=\"WHITE\" LINK=\"#AAAAFF\" ALINK=\"GREEN\" VLINK=\"#AAAAFF\" BACKGROUND=\"land0.gif\" BGPROPERTIES=FIXED>";
	$HskinName = 'ocean.css';
	tempHeader();
	require('hako-map.cgi');
	oceanMap();
	tempFooter();
	exit(0);
}elsif(($HmainMode eq 'new') || ($HmainMode eq 'bfield')) {
#	HdebugOut("モード:$HmainMode");
}else{
	# ヘッダ出力
	tempHeader();
}

if($HmainMode eq 'turn') {
	# ターン進行
	require('hako-turn.cgi');
	require('hako-top.cgi');
	require('exchange.cgi');
	turnMain();
} elsif($HmainMode eq 'new') {
	# 島の新規作成
	require('hako-make.cgi');
	require('hako-map.cgi');
	newIslandMain(0);
} elsif($HmainMode eq 'rekidai') {
	# 歴代人口記録 neo_otacky氏が作成
	require('hako-make.cgi');
	rekidaiPopMain();
} elsif($HmainMode eq 'print') {
	# 観光モード
	require('hako-map.cgi');
	printIslandMain();
} elsif($HmainMode eq 'owner') {
	# 開発モード
	require('hako-map.cgi');
	ownerMain();
} elsif($HmainMode eq 'command') {
	# コマンド入力モード
	require('hako-map.cgi');
	commandMain();
} elsif($HmainMode eq 'comment') {
	# コメント入力モード
#	if($Hrsswrite){require('hako-rss.cgi');rssMain();}
	require('hako-map.cgi');
	commentMain();
} elsif($HmainMode eq 'clbbs') {
	# コメント・観光者通信・近況
	$HmainMode = 'owner';
	require('hako-map.cgi');
	clbbsMain();
} elsif($HmainMode eq 'custom') {
	# カスタマイズ
	$HmainMode = 'owner';
	require('hako-map.cgi');
	customMain();
} elsif($HmainMode eq 'custom2') {
	# カスタマイズ2
	$HmainMode = 'owner';
	require('hako-map.cgi');
	customMain(1);
} elsif($HmainMode eq 'lbbs') {
	# ローカル掲示板モード
#	if($Hrsswrite){require('hako-rss.cgi');rssMain();}
	require('hako-map.cgi');
	localBbsMain();
} elsif($HmainMode eq 'monsedit') {
	# 怪獣設定
	require('hako-map.cgi');
	monsMain();
} elsif($HmainMode eq 'change') {
	# 情報変更モード
	require('hako-make.cgi');
	changeMain();
} elsif($HmainMode eq 'FightIsland') {
	# 簡易トーナメント 敗者の島表示
	require('hako-js.cgi');
	require('hako-map.cgi');
	fight_map();
} elsif($HmainMode eq 'FightView') {
	# 簡易トーナメント LOGモード
	require('hako-js.cgi');
	require('hako-map.cgi');
	FightViewMain();
} elsif($HmainMode eq 'camp') {
	# 陣営モード
	require('hako-map.cgi');
	require('hako-camp.cgi');
	campMain();
} elsif($HmainMode eq 'exchange') {
	# 資源取引モード
	if(($HexchangeMode ne 'show') && ($HtopAxes == 1)){
		# アクセス・ログ
		axeslog();
	}
	require('exchange.cgi');
	mainExchange();
} elsif($HmainMode eq 'kani') {
	# 簡易トップページ表示モード
	require('hako-top.cgi');
	topPageMain(1);
} elsif($HmainMode eq 'alist') {
	# 簡易トップページ表示モード
	require('hako-top.cgi');
	topPageAlist();
} elsif($HmainMode eq 'settei') { # ローカル画像指定
	# 設定トップページ表示モード
	require('hako-top.cgi');
	topPageMain(2);

} elsif($HmainMode eq 'list') {
	# 詳細リスト
	require('hako-top.cgi');
	topPageMain(3);
} elsif($HmainMode eq 'bfield') {
	# BattleField作成モード
	require('hako-make.cgi');
	require('hako-map.cgi');
	bfieldMain();
} elsif($HmainMode eq 'present') {
	# 管理人によるプレゼントモード
	require('hako-make.cgi');
	presentMain();
} elsif($HmainMode eq 'punish') {
	# 管理人による制裁モード
	require('hako-make.cgi');
	punishMain();
} elsif($HmainMode eq 'lchange') {
	# 管理人による地形変更モード
	require('hako-map.cgi');
	require('hako-make.cgi');
	lchangeMain();
} elsif($HmainMode eq 'predelete') {
	# 管理人によるあずかりモード
	require('hako-make.cgi');
	preDeleteMain();
} elsif($HmainMode eq 'ichange') {
	# 管理人による各種島データ変更モード
	require('hako-make.cgi');
	ichangeMain();
} elsif($HmainMode eq 'setupv') {
	# 初期設定確認モード
	require('hako-make.cgi');
	setupValue();
} else {
	# その他の場合はトップページモード
	require('hako-top.cgi');
	topPageMain(0);
}

# フッタ出力
tempFooter();

# 終了
exit(0);

# コマンドを前にずらす
sub slideFront {
	my($command, $number) = @_;

	# それぞれずらす
	splice(@$command, $number, 1);

#	HdebugOut("最後に資金繰り:" . $#$command);
	# 最後に資金繰り
	$command->[$#$command + 1] = {
	'kind' => $HcomDoNothing,
	'target' => 0,
	'x' => 0,
	'y' => 0,
	'arg' => 0,
	'tx' => 0,
	'ty' => 0,
	'flg' => 0 # 一時的な領域
	};
}

# コマンドを後にずらす
sub slideBack {
	my($command, $number, $kind, $target, $x, $y, $arg, $tx, $ty, $flg) = @_;
	$tx = 0 if($tx eq '');
	$ty = 0 if($ty eq '');
	# それぞれずらす
	return if $number == $#$command;
#	pop(@$command);
	splice(@$command, $number, 0, $command->[$number]);
	if($kind > 0){
		$command->[$number] = {
		'kind' => $kind,
		'target' => $target,
		'x' => $x,
		'y' => $y,
		'arg' => $arg,
		'tx' => $tx,
		'ty' => $ty,
		'flg' => $flg # 一時的な領域
		};
	}
}

#----------------------------------------------------------------------
# 島データ入出力
#----------------------------------------------------------------------

# 全島データ読みこみ
sub readIslandsFile {
	my($num) = @_;  # 0だと地形読みこまず
					# -1だと全地形を読む
					# 番号だとその島の地形だけは読みこむ

	# データファイルを開く
	return 0 if(!open(IN, "${HdirName}/hakojima.dat"));
	
	# 各パラメータの読みこみ
	$HislandTurn     = int(<IN>); # ターン数
	return 0 if($HislandTurn == 0);
	$HislandLastTime = int(<IN>); # 最終更新時間
	return 0 if($HislandLastTime == 0);
	$HislandNumber   = int(<IN>); # 島の総数
	# 次に割り当てるIDと管理人預かりの島ID
	my $tmp = <IN>;
	chomp($tmp);
	($HislandNextID, @HpreDeleteID) = split(/,/, $tmp);

	if($Htournament){
		# 簡易トーナメント
		$HflexTimeSet = 1;
		$Hallyflg = 0;
		$Hpossess = 0;
		# データファイルを開く
		return 0 if(!open(TIN, "${HdirName}/tournament.dat"));
		$HislandFightMode	= int(<TIN>);  # 現在の戦闘モード
		$HislandChangeTurn	= int(<TIN>);  # 切り替えターン
		$HislandFightCount	= int(<TIN>);  # 何回戦目か
		$HislandTurnCount	= int(<TIN>);  # ターン更新数
		<TIN>;
		<TIN>;
		<TIN>;
		<TIN>;
		if($HislandFightMode == 1){
			# 予選
			@HflexTime = @HtmTime1;
		}elsif($HislandFightMode == 2){
			# 開発
			@HflexTime = @HtmTime2;
		}elsif($HislandFightMode == 3){
			# 戦闘
			@HflexTime = @HtmTime3;
		}
		# flexTime処理
		$HunitTime = 3600 * $HflexTime[($HislandTurnCount % ($#HflexTime + 1))] if($HflexTimeSet);
	}else{
		# flexTime処理
		$HunitTime = 3600 * $HflexTime[($HislandTurn % ($#HflexTime + 1))] if($HflexTimeSet);
	}

	# ターン処理判定
	my($now) = time;
	if(((($Hdebug == 1) && ($HmainMode eq 'Hdebugturn')) ||
		(($now - $HislandLastTime) >= $HunitTime)) &&
		(($HlastTurn == 0)||($HislandTurn < $HlastTurn))) { # 終了ターン
		$HmainMode = 'turn';
		$num = -1; # 全島読みこむ
	}

	# 島の読みこみ
	my($i);
	for($i = 0; $i < $HislandNumber; $i++) {
		$Hislands[$i] = readIsland($num);
		$HidToNumber{$Hislands[$i]->{'id'}} = $i;
		foreach (@HpreDeleteID) {
			if($Hislands[$i]->{'id'} == $_) {
				$Hislands[$i]->{'predelete'} = 1;
			}
		}
		$Hislands[$i]->{'predelete'} = 1 if($Hislands[$i]->{'fight_id'} == -1); # 不戦勝時はあずかりと同じ動作
	}
	readsubmap(0);#宇宙マップ読込
	readsubmap(1);#海域マップ読込
	readCommandLate(); #ターン差命令データ読込
	# ファイルを閉じる
	close(IN);
	close(TIN) if($Htournament);
	return 1;
}
# サブマップひとつ読みこみ
sub readsubmap {
	my($num) = @_;
	# 宇宙、海域マップ読みこみ
	if(open(IN, "${HdirName}/submap.$num")){
		# 地形
		my(@land, @landValue, @land2, @landValue2, @nation, $line, @lbbs);
		my($x, $y, $i);
		if($num == 0){
			#宇宙
			$Hspacemap = 1;
			for($y = 0; $y < $HislandSize; $y++) {
				$line = <IN>;
				for($x = 0; $x < $HislandSize; $x++) {
					$line =~ s/^(..)(....)(..)(....)(..)//;
					$land[$x][$y] = hex($1);
					$landValue[$x][$y] = hex($2);
					$land2[$x][$y] = hex($3);
					$landValue2[$x][$y] = hex($4);
					$nation[$x][$y] = hex($5);
				}
			}
		}else{
			#海域
			for($y = 0; $y < $HoceanSize; $y++) {
				$line = <IN>;
				for($x = 0; $x < $HoceanSize; $x++) {
					$line =~ s/^(..)(....)(..)(....)(..)//;
					$land[$x][$y] = hex($1);
					$landValue[$x][$y] = hex($2);
					$land2[$x][$y] = hex($3);
					$landValue2[$x][$y] = hex($4);
					$nation[$x][$y] = hex($5);
				}
			}
		}
		my $spaces = <IN>;# 宇宙資産上位５位
		chomp($spaces);
		my $solarwind= int(<IN>); # 太陽風ターン
		my $area	= int(<IN>); # 開発面積
		my $pop		= int(<IN>); # 宇宙人口
		my $farm	= int(<IN>); # 宇宙農場
		my $factory	= int(<IN>); # 宇宙工場
		my $food	= <IN>; # 宇宙食料
		my @foods	= split(/,/, $food);
#		HdebugOut("$foods[0],$foods[1],$foods[2]");
		<IN>;# 拡張用
		<IN>;# 拡張用
		<IN>;# 拡張用
		<IN>;# 拡張用
		<IN>;# 拡張用
		# ローカル掲示板
		for($i = 0; $i < $HlbbsMax; $i++) {
			$line = <IN>;
			chomp($line);
			$lbbs[$i] = $line;
		}
		if($num == 0){
			#宇宙
			$Hspace = {
			 'land' => \@land,
			 'landValue' => \@landValue,
			 'land2' => \@land2,
			 'landValue2' => \@landValue2,
			 'nation' => \@nation,
			 'solarwind' => $solarwind,
			 'space' => $spaces,
			 'area' => $area,
			 'pop' => $pop,
			 'farm' => $farm,
			 'factory' => $factory,
			 'food' => int($foods[0]),
			 'foodP' => int($foods[1]),
			 'foodC' => int($foods[2]),
			 'lbbs' => \@lbbs
			};
		}else{
			#海域
			$Hocean = {
			 'land' => \@land,
			 'landValue' => \@landValue,
			 'land2' => \@land2,
			 'landValue2' => \@landValue2,
			 'nation' => \@nation,
			 'solarwind' => $solarwind,
			 'space' => $spaces,
			 'area' => $area,
			 'pop' => $pop,
			 'farm' => $farm,
			 'factory' => $factory,
			 'food' => int($foods[0]),
			 'foodP' => int($foods[1]),
			 'foodC' => int($foods[2]),
			 'lbbs' => \@lbbs
			};
		}
		close(IN);
	}
}

# 島ひとつ読みこみ
sub readIsland {
	my($num) = @_;
	my($name, $id, $ownername, $prize, $absent, $comment, $password, $money, $food,
		$pop, $area, $farm, $weather, $factory, $port, $mountain, $tower,
		$yousyoku, $turnsu, $ally, $MissileK, $MissileA, $present,
		$allex, $status , $evil, $order, $mons1, $monsurl, $score, $xy, $ore,$weapon,$oil,$oilfield,
		$monsfound,$cmdTurn,$cmdIp,$cmdId,$cmdtime);
	$name = <IN>; # 島の名前
	chomp($name);
	if($name =~ s/,(.*)$//g) {
		$score = int($1);
	} else {
		$score = 0;
	}
	$id = int(<IN>);       # ID番号
	$ownername= <IN>;      # オーナ名
	chomp($ownername);
	$prize = <IN>;         # 受賞
	chomp($prize);
	$absent = int(<IN>);   # 連続資金繰り数
	$comment = <IN>;       # コメント
	chomp($comment);
	my @comments = split(/<>/, $comment);
	$password = <IN>;      # 暗号化パスワード
	chomp($password);
	$money = int(<IN>);    # 資金
	$food = int(<IN>);     # 食料
	$pop = <IN>; # 人口
	my @pops = split(/,/, $pop);
	$area = int(<IN>);     # 広さ
	$farm = int(<IN>);     # 農場
	$weather = <IN>;  # 天候
	my($neww,@pastw);
	my($w) = 0;
	$weather =~ s/([0-9]*),//;
	$neww = int($1);
	for($w = 0; $w < 10; $w++) {
		$weather =~ s/([0-9]*),//;
		$pastw[$w] = int($1);
	}
	$weather =~ s/([0-9]*)$//;
	$pastw[$w] = int($1);
	$factory = int(<IN>);  # 工場
	$port     = int(<IN>); # 港
	$mountain = int(<IN>); # 採掘場
	$tower    = int(<IN>); # 商業地
	$yousyoku = int(<IN>); # 養殖場
	$turnsu   = <IN>; # 繰越を除いたその島のターン数,順位点,開始ターン
	my @hturn = split(/,/, $turnsu);
	my $winp  = <IN>; # 勝ち、負けポイント、勝った数
	my @win   = split(/,/, $winp);
	$MissileK = <IN>; # ミサイル発射可能数,発射ミサイル総数
	$ally     = int(<IN>); # 所属ID
	$present  = <IN>;      # プレゼント
	$allex    = int(<IN>); # 経験獲得数
	$status   = int(<IN>); # 部門賞
	$evil     = int(<IN>); # 
	$monsfound= int(<IN>); # 現在出現している怪獣の数
	$order    = int(<IN>); # 命令
	$xy       = <IN>; # 座標
	$ore      = int(<IN>); # 鉱石
	$weapon   = int(<IN>); # 兵器
	$oil      = int(<IN>); # 原油
	$oilfield = int(<IN>); # 油田生産量
	my @Missile = split(/,/, $MissileK);
	my @coordinate = split(/,/, $xy);
	
	$present =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)$/;
	my @prese = (int($1),int($2),int($3),int($4),int($5),int($6),int($7),int($8),int($9),int($10),int($11),int($12),int($13),int($14));
	
	# 怪獣バトル用
	$mons1    = <IN>; # 自分の怪獣
	$monsurl  = <IN>; # 怪獣URL
	chomp($monsurl);
	my @monster = split(/,/, $mons1);

	# HidToNameテーブルへ保存
	$HidToName{$id} = $name;

	# 地形
	my(@land, @landValue, @land2, @landValue2, @nation, $line, @command, @lbbs);
	my(@ugL, @ugV, @ugX, @ugY);# 地下
	if(($num == -1) || ($num == $id)) {
		exit(0) if(!open(IIN, "${HdirName}/island.$id"));
		my($x, $y, $i);
		for($y = 0; $y < $HislandSize; $y++) {
			$line = <IIN>;
			for($x = 0; $x < $HislandSize; $x++) {
				$line =~ s/^(..)(....)(..)(....)(..)//;
				$land[$x][$y] = hex($1);
				$landValue[$x][$y] = hex($2);
				$land2[$x][$y] = hex($3);
				$landValue2[$x][$y] = hex($4);
				$nation[$x][$y] = hex($5);
			}
		}
		# 地下
		for($i = 0; $i < $HugMax; $i++) {
			$line = <IIN>;
			for($x = 0; $x < 9; $x++) {
				$line =~ s/^(.)(..)//;
				$ugL[$i][$x] = hex($1);
				$ugV[$i][$x] = hex($2);
			}
			$line =~ /^,([0-9]*),([0-9]*)$/;
			$ugX[$i] = $1;
			$ugY[$i] = $2;
		}
		$cmdTurn	= int(<IIN>); # ターン
		$cmdIp		= <IIN>;# IP
		chomp($cmdIp);
		$cmdId		= int(<IIN>);# クッキーID
		$cmdtime	= int(<IIN>);# 入力時間
		<IIN>;# 拡張用
		# コマンド
		for($i = 0; $i < $HcommandMax; $i++) {
			$line = <IIN>;
			$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)$/;
			$command[$i] = {
			'kind' => int($1),
			'target' => int($2),
			'x' => int($3),
			'y' => int($4),
			'arg' => int($5),
			'tx' => int($6),
			'ty' => int($7)
			}
		}

		# ローカル掲示板
		for($i = 0; $i < $HlbbsMax; $i++) {
			$line = <IIN>;
			chomp($line);
			$lbbs[$i] = $line;
		}

		close(IIN);
	}

	my($fight_id);
	if($Htournament){
		# 簡易トーナメント
		$fight_id = int(<TIN>);	# 対戦相手ID
		<TIN>;
		<TIN>;
		<TIN>;
		<TIN>;
	}

	# 島型にして返す
	return {
	 'name' => $name,
	 'ownername' => $ownername, # オーナ名表示のため追加
	 'id' => $id,
	 'score' => $score,
	 'prize' => $prize,
	 'absent' => $absent,
	 'comment' => $comments[0],
	 'commentLabel0' => $comments[1],
	 'commentLabel1' => $comments[2],
	 'commentLabel2' => $comments[3],
	 'commentLabel3' => $comments[4],
	 'commentLabel4' => $comments[5],
	 'password' => $password,
	 'money' => $money,
	 'food' => $food,
	 'pop' => int($pops[0]),
	 'popspace' => int($pops[1]),
	 'spa' => int($pops[2]),
	 'area' => $area,
	 'farm' => $farm,
	 'weather' => $neww,
	 'pastweather' => \@pastw,
	 'factory' => $factory,
	 'port' => $port,
	 'mountain' => $mountain,
	 'tower' => $tower,
	 'yousyoku' => $yousyoku,
	 'turnsu' => int($hturn[0]),
	 'zyuni' => int($hturn[1]),
	 'winP' => int($win[0]),
	 'loseP' => int($win[1]),
	 'winS' => int($win[2]),
	 'possess' => int($win[3]),
	 'ally' => $ally,
	 'MissileK' => int($Missile[0]),
	 'MissileA' => int($Missile[1]),
	 'present' => \@prese,
	 'allex' => $allex,
	 'status' => $status,
	 'evil' => $evil,
	 'kaisi' => int($hturn[2]),
	 'order' => $order,
	 'x' => int($coordinate[0]),
	 'y' => int($coordinate[1]),
	 'ore' => $ore,
	 'weapon' => $weapon,
	 'oil' => $oil,
	 'oilfield' => $oilfield,
	 'land' => \@land,
	 'landValue' => \@landValue,
	 'land2' => \@land2,
	 'landValue2' => \@landValue2,
	 'nation' => \@nation,
	 'ugL' => \@ugL,
	 'ugV' => \@ugV,
	 'ugX' => \@ugX,
	 'ugY' => \@ugY,
	 'fight_id' => $fight_id,
	 'command' => \@command,
	 'lbbs' => \@lbbs,
	 'monsurl' => $monsurl,
	 'monster' => \@monster,
	 'monsfound' => $monsfound,
	 'cmdTurn' => $cmdTurn,
	 'cmdIp' => $cmdIp,
	 'cmdId' => $cmdId,
	 'cmdtime' => $cmdtime,
	};
}

# 全島データ書き込み
sub writeIslandsFile {
	my($num, $mode) = @_;

	unless(-e "${HtempdirName}") { mkdir(${HtempdirName}, $HdirMode); }
	if(-e "deldata") { myrmtree("deldata"); }

	if(($mode == 0)||($mode == 1)) {
		# ファイルを開く
		my($retry) = $HretryCount;
		while(!open(OUT, ">${HtempdirName}/hakojima.tmp")) {
			$retry--;
			if($retry <= 0) {
				$HerrorNum = '100';
				return 0;
			}
			# 0.2 秒 sleep
			select undef, undef, undef, 0.2;
		}

		# 各パラメータ書き込み
		print OUT "$HislandTurn\n";
		print OUT "$HislandLastTime\n";
		print OUT "$HislandNumber\n";
		print OUT "$HislandNextID," . join(',', @HpreDeleteID) . "\n";
		
		if($Htournament){
			# ファイルを開く
			my($retry) = $HretryCount;
			while(!open(TOUT, ">${HtempdirName}/tournament.tmp")) {
				$retry--;
				if($retry <= 0) {
					$HerrorNum = '100';
					return 0;
				}
				# 0.2 秒 sleep
				select undef, undef, undef, 0.2;
			}
			print TOUT "$HislandFightMode\n";
			print TOUT "$HislandChangeTurn\n";
			print TOUT "$HislandFightCount\n";
			print TOUT "$HislandTurnCount\n";
			print TOUT "\n";
			print TOUT "\n";
			print TOUT "\n";
			print TOUT "\n";
			
		}
	}
	# 島の書きこみ
	my($i);
	my($flag) = 1;
	for($i = 0; $i < $HislandNumber; $i++) {
		if(!writeIsland($Hislands[$i], $num, 0)) {
			$flag = 0;
			last;
		}
	}

	# 宇宙マップの書きこみ
	if($flag) {
		my($c) = $HislandSize / 2 - 1;
#		HdebugOut("宇宙マップの作成 $num モード $mode 初期化 $Hspacemap 地球 $c");
		$Hspace->{'land'}->[$c][$c] = $HlandEarth;
		if($Hspacemap != 1){
			# 宇宙マップ初期化
			$Hspace->{'solarwind'} = $HislandTurn + random(30) + 30;
			# 初期掲示板を作成
			my(@lbbs);
			for($i = 0; $i < $HlbbsMax; $i++) {
				$lbbs[$i] = "0<<0>>";
			}
			$Hspace->{'lbbs'} = \@lbbs;
		}
		$flag = 0 if(!writeIsland($Hspace, 0, 3));
	}

	# 海域マップの書きこみ
	if($flag) {
		$flag = 0 if(!writeIsland($Hocean, 0, 4));
	}

	# ターン差命令データ書き込み
	open(COUT, ">${HtempdirName}/command.tmp");
	for($i = $#HcomL; $i >= 0; $i--){
		next if($HcomL[$i]->{turn} <= $HislandTurn);
		printf COUT ("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n",
			$HcomL[$i]->{turn},
			$HcomL[$i]->{turn2},
			$HcomL[$i]->{id},
			$HcomL[$i]->{kind},
			$HcomL[$i]->{target},
			$HcomL[$i]->{x},
			$HcomL[$i]->{y},
			$HcomL[$i]->{arg},
			$HcomL[$i]->{x2},
			$HcomL[$i]->{y2}
		);
	}
	close(COUT);

	# ファイルを閉じる
	if(($mode == 0)||($mode == 1)){
		close(OUT);
		close(TOUT) if($Htournament);
	}

	if(!$flag) {
		if(-e "${HtempdirName}/hakojima.tmp") { unlink("${HtempdirName}/hakojima.tmp"); }
		$HerrorNum = '200';
		return 0;
	}
	
	
	if($Htournament){
		rename("${HdirName}/fight.log","${HtempdirName}/fight.tmp");
	}

	# 本来の名前にする
	if($num <= -1) {
		if(!(-s "${HtempdirName}/hakojima.tmp")) { $HerrorNum = '111'; return 0; }
		if(!rename("${HtempdirName}/hakojima.tmp", "${HtempdirName}/hakojima.dat")) { $HerrorNum = '121'; return 0; }
		for($i = 0; $i < $HislandNumber; $i++) {
			if(!(-s "${HtempdirName}/islandtmp.$Hislands[$i]->{'id'}")) { $HerrorNum = '211'; return 0; }
			if(!rename("${HtempdirName}/islandtmp.$Hislands[$i]->{'id'}", "${HtempdirName}/island.$Hislands[$i]->{'id'}")) {
				$HerrorNum = '221';
				return 0;
			}
		}
		if(!(-s "${HtempdirName}/submaptmp.0")) { $HerrorNum = '511'; return 0; }
		if(!rename("${HtempdirName}/submaptmp.0", "${HtempdirName}/submap.0")) { $HerrorNum = '521'; return 0; }
		if(!(-s "${HtempdirName}/submaptmp.1")) { $HerrorNum = '611'; return 0; }
		if(!rename("${HtempdirName}/submaptmp.1", "${HtempdirName}/submap.1")) { $HerrorNum = '621'; return 0; }
		if(-s "${HtempdirName}/command.tmp") {
			if(!rename("${HtempdirName}/command.tmp", "${HtempdirName}/command.dat")) { $HerrorNum = '721'; return 0; }
		}
		if($Htournament){
			if(-s "${HtempdirName}/tournament.tmp") {
				if(!rename("${HtempdirName}/tournament.tmp", "${HtempdirName}/tournament.dat")) { $HerrorNum = '821'; return 0; }
			}
			if(-s "${HtempdirName}/fight.tmp") {
				if(!rename("${HtempdirName}/fight.tmp", "${HtempdirName}/fight.log")) { $HerrorNum = '921'; return 0; }
			}
		}
#		if($Hrsswrite){
#			rename("${HdirName}/rss.dat", "${HtempdirName}/rss.dat");
#		}
		
		if(!rename("${HdirName}", "deldata")) { $HerrorNum = '321'; return 0; }
		if(!rename("${HtempdirName}", "${HdirName}")) {
			rename("deldata", "${HdirName}");
			$HerrorNum = '421';
			return 0;
		}
		myrmtree("deldata");
		return 1;
	}

	if(($mode == 0)||($mode == 1)) {
		if(!(-s "${HtempdirName}/hakojima.tmp")) { $HerrorNum = '112'; return 0; }
		if(!rename("${HtempdirName}/hakojima.tmp", "${HdirName}/hakojima.dat")) { $HerrorNum = '122'; return 0; }
	}

	if(($mode == 0)||($mode == 2)) {
		for($i = 0; $i < $HislandNumber; $i++) {
			if (-e "${HtempdirName}/islandtmp.$Hislands[$i]->{'id'}") {
				if(!(-s "${HtempdirName}/islandtmp.$Hislands[$i]->{'id'}")) { $HerrorNum = '212'; return 0; }
				if(!rename("${HtempdirName}/islandtmp.$Hislands[$i]->{'id'}", "${HdirName}/island.$Hislands[$i]->{'id'}")) {
					$HerrorNum = '222';
					return 0;
				}
			}
		}
	}
	
	if(($mode == 0)||($mode == 3)) {
		if(!(-s "${HtempdirName}/submaptmp.0")) { $HerrorNum = '512'; return 0; }
		if(!rename("${HtempdirName}/submaptmp.0", "${HdirName}/submap.0")) { $HerrorNum = '522'; return 0; }
	}
	if(($mode == 0)||($mode == 4)) {
		if(!(-s "${HtempdirName}/submaptmp.1")) { $HerrorNum = '612'; return 0; }
		if(!rename("${HtempdirName}/submaptmp.1", "${HdirName}/submap.1")) { $HerrorNum = '622'; return 0; }
	}
	if(($mode == 0)||($mode == 4)) {
		if(-s "${HtempdirName}/command.tmp") {
			if(!rename("${HtempdirName}/command.tmp", "${HdirName}/command.dat")) { $HerrorNum = '722'; return 0; }
		}
	}
	if($Htournament){
		if(-s "${HtempdirName}/tournament.tmp") {
			if(!rename("${HtempdirName}/tournament.tmp", "${HdirName}/tournament.dat")) { $HerrorNum = '822'; return 0; }
		}
		if(-s "${HtempdirName}/fight.tmp") {
			if(!rename("${HtempdirName}/fight.tmp", "${HdirName}/fight.log")) { $HerrorNum = '922'; return 0; }
		}
	}
#	if(($mode == 0) && ($Hrsswrite)){
#		if(!(-s "${HtempdirName}/rss.tmp")) { $HerrorNum = '612'; return 0; }
#		if(!rename("${HtempdirName}/rss.tmp", "${HdirName}/rss.dat")) { $HerrorNum = '622'; return 0; }
#	}
	
	return 1;

}

# 島ひとつ書き込み
sub writeIsland {
	my($island, $num, $mode) = @_;
	if($mode == 0){
	my($score);
	$score = int($island->{'score'});
	print OUT $island->{'name'} . ",$score\n";
	print OUT $island->{'id'} . "\n";
	print OUT $island->{'ownername'} . "\n";
	print OUT $island->{'prize'} . "\n";
	print OUT $island->{'absent'} . "\n";
	my($comments) = "$island->{'comment'}<>$island->{'commentLabel0'}<>$island->{'commentLabel1'}<>$island->{'commentLabel2'}<>$island->{'commentLabel3'}<>$island->{'commentLabel4'}";
	print OUT $comments . "\n";
	print OUT $island->{'password'} . "\n";
	print OUT $island->{'money'} . "\n";
	print OUT $island->{'food'} . "\n";
	print OUT $island->{'pop'} . "," . $island->{'popspace'} . "," . $island->{'spa'} . "\n";
	print OUT $island->{'area'} . "\n";
	print OUT $island->{'farm'} . "\n";
	my($pastweather) = $island->{'pastweather'};
	printf OUT ("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n",
		$island->{'weather'},
		$pastweather->[0],
		$pastweather->[1],
		$pastweather->[2],
		$pastweather->[3],
		$pastweather->[4],
		$pastweather->[5],
		$pastweather->[6],
		$pastweather->[7],
		$pastweather->[8],
		$pastweather->[9],
		$pastweather->[10]
	);
	print OUT $island->{'factory'} . "\n";
	print OUT $island->{'port'} . "\n";
	print OUT $island->{'mountain'} . "\n";
	print OUT $island->{'tower'} . "\n";
	print OUT $island->{'yousyoku'} . "\n";
	print OUT $island->{'turnsu'} . "," . $island->{'zyuni'} . "," . $island->{'kaisi'} . "\n";
	print OUT $island->{'winP'} . "," . $island->{'loseP'} . "," . $island->{'winS'} . "," . $island->{'possess'} . "\n";
	print OUT $island->{'MissileK'} . "," . $island->{'MissileA'} . "\n";
	print OUT $island->{'ally'} . "\n";
	my($present) = $island->{'present'};
	printf OUT ("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n", 
		$present->[0],
		$present->[1],
		$present->[2],
		$present->[3],
		$present->[4],
		$present->[5],
		$present->[6],
		$present->[7],
		$present->[8],
		$present->[9],
		$present->[10],
		$present->[11],
		$present->[12],
		$present->[13]
	);
	
	print OUT $island->{'allex'} . "\n";
	print OUT $island->{'status'} . "\n";
	print OUT $island->{'evil'} . "\n";
	print OUT $island->{'monsfound'} . "\n";
	print OUT $island->{'order'} . "\n";
	print OUT $island->{'x'} . "," . $island->{'y'} . "\n";
	
	print OUT $island->{'ore'} . "\n";
	print OUT $island->{'weapon'} . "\n";
	print OUT $island->{'oil'} . "\n";
	print OUT $island->{'oilfield'} . "\n";
	
	# 怪獣バトル用
	my($monster) = $island->{'monster'};
	printf OUT ("%d,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n", 
		$monster->[0],
		$monster->[1],
		$monster->[2],
		$monster->[3],
		$monster->[4],
		$monster->[5],
		$monster->[6],
		$monster->[7],
		$monster->[8],
		$monster->[9],
		$monster->[10],
		$monster->[11],
		$monster->[12],
		$monster->[13]
	);
	print OUT $island->{'monsurl'} . "\n";

	
	if($Htournament){
		# 簡易トーナメント
		print TOUT $island->{'fight_id'} . "\n";
		print TOUT "\n";
		print TOUT "\n";
		print TOUT "\n";
		print TOUT "\n";
	}
	}
	
	# 地形
	if(($num <= -1) || ($num == $island->{'id'})) {
		my($retry) = $HretryCount;
		if($mode == 3){
			# 宇宙マップ
			while(!open(IOUT, ">${HtempdirName}/submaptmp.0")) {
				$retry--;
				return 0 if($retry <= 0);
				# 0.2 秒 sleep
				select undef, undef, undef, 0.2;
			}
		}elsif($mode == 4){
			while(!open(IOUT, ">${HtempdirName}/submaptmp.1")) {
				$retry--;
				return 0 if($retry <= 0);
				# 0.2 秒 sleep
				select undef, undef, undef, 0.2;
			}
		}else{
			while(!open(IOUT, ">${HtempdirName}/islandtmp.$island->{'id'}")) {
				$retry--;
				return 0 if($retry <= 0);
				# 0.2 秒 sleep
				select undef, undef, undef, 0.2;
			}
		}

		my($land, $landValue, $land2, $landValue2, $nation);
		$land		= $island->{'land'};
		$landValue	= $island->{'landValue'};
		$land2		= $island->{'land2'};
		$landValue2	= $island->{'landValue2'};
		$nation		= $island->{'nation'};
		
		# 地下
		my($ugL,$ugV,$ugX,$ugY) = ($island->{'ugL'},$island->{'ugV'},$island->{'ugX'},$island->{'ugY'});
		
		my($x, $y);
		if($mode == 3){
			# 宇宙マップ
			for($y = 0; $y < $HislandSize; $y++) {
				for($x = 0; $x < $HislandSize; $x++) {
					printf IOUT ("%02x%04x%02x%04x%02x", $land->[$x][$y], $landValue->[$x][$y], $land2->[$x][$y], $landValue2->[$x][$y], $nation->[$x][$y]);
				}
				print IOUT "\n";
			}
			print IOUT $island->{'space'} . "\n";
			print IOUT $island->{'solarwind'} . "\n";
			print IOUT $island->{'area'} . "\n";
			print IOUT $island->{'pop'} . "\n";
			print IOUT $island->{'farm'} . "\n";
			print IOUT $island->{'factory'} . "\n";
			print IOUT $island->{'food'} . "," . $island->{'foodP'} . "," . $island->{'foodC'} . "\n";
			
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
		}elsif($mode == 4){
			# 海域マップ
			for($y = 0; $y < $HoceanSize; $y++) {
				for($x = 0; $x < $HoceanSize; $x++) {
					printf IOUT ("%02x%04x%02x%04x%02x", $land->[$x][$y], $landValue->[$x][$y], $land2->[$x][$y], $landValue2->[$x][$y], $nation->[$x][$y]);
				}
				print IOUT "\n";
			}
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
		}else{
			# 通常マップ
			for($y = 0; $y < $HislandSize; $y++) {
				for($x = 0; $x < $HislandSize; $x++) {
					printf IOUT ("%02x%04x%02x%04x%02x", $land->[$x][$y], $landValue->[$x][$y], $land2->[$x][$y], $landValue2->[$x][$y], $nation->[$x][$y]);
				}
				print IOUT "\n";
			}
			# 地下
			my($i);
			for($i = 0; $i < $HugMax; $i++) {
				# チェック
				if(($land->[$ugX->[$i]][$ugY->[$i]] != $HlandDokan) && ($land2->[$ugX->[$i]][$ugY->[$i]] != $HlandDokan)){
					# 出口がないのでクリアする
					$ugX->[$i] = "";
					$ugY->[$i] = "";
				}
				for($x = 0; $x < 9; $x++) {
					printf IOUT ("%01x%02x", $ugL->[$i][$x], $ugV->[$i][$x]);
				}
				print IOUT "," . $ugX->[$i] . "," . $ugY->[$i] . "\n";
			}
			# コマンド
			print IOUT $island->{'cmdTurn'} . "\n";
			print IOUT $island->{'cmdIp'} . "\n";
			print IOUT $island->{'cmdId'} . "\n";
			print IOUT $island->{'cmdtime'} . "\n";
			print IOUT "\n";
			my($command, $i);
			$command = $island->{'command'};
			for($i = 0; $i < $HcommandMax; $i++) {
				chomp($command->[$i]->{'ip'});
				printf IOUT ("%d,%d,%d,%d,%d,%d,%d\n", 
					 $command->[$i]->{'kind'},
					 $command->[$i]->{'target'},
					 $command->[$i]->{'x'},
					 $command->[$i]->{'y'},
					 $command->[$i]->{'arg'},
					 $command->[$i]->{'tx'},
					 $command->[$i]->{'ty'}
				);
			}
		}

		# ローカル掲示板
		my($lbbs) = $island->{'lbbs'};
		for($i = 0; $i < $HlbbsMax; $i++) {
			print IOUT $lbbs->[$i] . "\n";
		}

		close(IOUT);
	}
	return 1;
}

# ディレクトリ消し
sub myrmtree {
	my($dn) = @_;
	opendir(DIN, "$dn/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		unlink("$dn/$fileName");
	}
	closedir(DIN);
	rmdir($dn);
}

#----------------------------------------------------------------------
# 入出力
#----------------------------------------------------------------------

# CGIの読みこみ
sub cgiInput {
	my($line, $getLine);

	# 入力を受け取って日本語コードをEUCに
	$line = <>;
	$line =~ tr/+/ /;
#	$line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$line =~ s/%([a-fA-F0-9]{2})/pack(H2, $1)/eg;
#	$line = jcode::euc($line);
	jcode::convert(\$line, 'euc');
	$line =~ s/[\x00-\x1f\,]//g;

	# GETのやつも受け取る
	$getLine = $ENV{'QUERY_STRING'};

#	HdebugOut("POST=$line");
#	HdebugOut("GET =$getLine");

	# 対象の島
	if($line =~ /CommandButton([0-9]+)=/) {
		# コマンド送信ボタンの場合
		$HcurrentID = $1;
	}

	if($line =~ /ISLANDNAME=([^\&]*)\&/){
		# 名前指定の場合
		$HcurrentName = cutColumn($1, 32);
	}

	if($line =~ /OWNERNAME=([^\&]*)\&/){
		# オーナー名の場合
		$HcurrentOwnerName = cutColumn($1, 32);
	}

	if($line =~ /ISLANDID=([0-9]+)\&/){
		# その他の場合
		$HcurrentID = $1;
	}

	if($line =~ /LBBSTYPE=([^\&]*)\&/){
		# 掲示板の通信形式
		$HlbbsType = $1;
	}

	# パスワード
	if($line =~ /OLDPASS=([^\&]*)\&/) {
		$HoldPassword = $1;
		$HdefaultPassword = $1;
	}
	if($line =~ /PASSWORD=([^\&]*)\&/) {
		$HinputPassword = $1;
		$HdefaultPassword = $1;
	}
	if($line =~ /PASSWORD2=([^\&]*)\&/) {
		$HinputPassword2 = $1;
	}

	# メッセージ
	if($line =~ /MESSAGE=([^\&]*)\&/) {
		$Hmessage = cutColumn($1, 120);
	}

	# コメントラベル
	if($line =~ /COMMENT_LABEL0=([^\&]*)\&/) {
		$HcommentLabel0 = $1;
	}
	if($line =~ /COMMENT_LABEL1=([^\&]*)\&/) {
		$HcommentLabel1 = $1;
	}
	if($line =~ /COMMENT_LABEL2=([^\&]*)\&/) {
		$HcommentLabel2 = $1;
	}
	if($line =~ /COMMENT_LABEL3=([^\&]*)\&/) {
		$HcommentLabel3 = $1;
	}
	if($line =~ /COMMENT_LABEL4=([^\&]*)\&/) {
		$HcommentLabel4 = $1;
	}
	
	# 怪獣設定
	if($line =~ /MONSNAME=([^\&]*)\&/) {
		$Hmonsname = cutColumn($1, 32);
	}
	if($line =~ /MONSURL=([^\&]*)\&/) {
		$Hmonsurl = cutColumn($1, 80);
	}
	
	# Ｊａｖａスクリプトモード
	if($line =~ /JAVAMODE=(cgi|java)/) {
		$HjavaMode = $1;
	}
	if($getLine =~ /JAVAMODE=(cgi|java)/) {
		$HjavaMode = $1;
	}
	# 非同期通信フラグ
	if($line =~ /async=true\&/) {
		$Hasync = 1;
	}
	if($line =~ /CommandJavaButton([0-9]+)=/) {
		# コマンド送信ボタンの場合（Ｊａｖａスクリプト）
		$HcurrentID = $1;
		$defaultID = $1;
	}

	# ローカル掲示板
	if($line =~ /LBBSNAME=([^\&]*)\&/) {
		$HlbbsName = $1;
		$HdefaultName = $1;
	}
	if($line =~ /LBBSMESSAGE=([^\&]*)\&/) {
		$HlbbsMessage = cutColumn($1, 100);
	}

	# ローカル画像指定
	if($line =~ /IMGLINEMAC=([^&]*)\&/) {
		my($flag) = $1;
		if($flag eq ''){
			$flag = $imageDir;
		} else {
			$flag =~ s/ /%20/g;
			$flag = 'file:///' . $flag;
		}
		$HimgLine = $flag;
	} elsif($line =~ /IMGLINE=([^&]*)\&/) {
		my($flag) = substr($1, 0 , -10);
		$flag =~ tr/\\/\//;
		if($flag eq ''){
			$flag = $imageDir;
		} else {
			$flag =~ s/ /%20/g;
			$flag = 'file:///' . $flag;
		}
		$HimgLine = $flag;
	}

	# 船系で透過画像を使用するか
	if($line =~ /RMYSHIP=([^&]*)\&/) {
		$HmyshipFlg = 1;
		$Hmyship = $1;
	}

	# main modeの取得
	if($line =~ /TurnButton/) {
		if($Hdebug == 1) {
			$HmainMode = 'Hdebugturn';
		}
	} elsif($getLine =~ /kani/) {
		$HmainMode = 'kani';
	} elsif($getLine =~ /alist=([0-9]*)/) {
		$HmainMode = 'alist';
		$Halistmode = $1;
	} elsif($getLine =~ /$Hurlownermode=([0-9]*)/) {
		$HjavaMode = 'java';
		$defaultID = $1;
		$HcurrentID = $1;
		$HmainMode = 'owner';
		if($getLine =~ /PASSWORD=([^\&]*)\&/) {
			$HinputPassword = $1;
			$HdefaultPassword = $1;
		}
	} elsif($getLine =~ /settei=([^\&]*)/) { # ローカル画像指定
		$HmainMode = 'settei';
		$HdefaultPassword = $1;
	} elsif($line =~ /SIGHTMODE=on/) {
		# 認証観光モード
		if($line =~ /PISLANDID=([0-9]+)\&/){
			$HprintID = $1;# 自分のID
		}
		$HmainMode = 'print';
	} elsif($line =~ /OwnerButton/) {
		$HmainMode = 'owner';
	} elsif($getLine =~ /SUCCESSIVE=([0-9]*)/) { # neo_otacky氏が作成
		$HmainMode = 'rekidai';
	} elsif($getLine =~ /Sight=([0-9]*)/) {
		$HmainMode = 'print';
		$HcurrentID = $1;
	} elsif($getLine =~ /IslandMap=([0-9]*)/) {
		$HmainMode = 'landmap';
		if($1 >= 1000){
			# 地下
			$Hugmode = 1;
			$HcurrentID = $1 - 1000;
		}else{
			$HcurrentID = $1;
		}
	} elsif($line =~ /NewIslandButton/) {
		$HmainMode = 'new';
		$line =~ /TOURNAMENTMONS=([0-9]*)/;
		$HtournamentmonsId = $1;
	} elsif($line =~ /LbbsButton(..)([0-9]*)/) {
		$HmainMode = 'lbbs';
		if($1 eq 'SS') {
			# 観光者
			$HlbbsMode = 0;
		} elsif($1 eq 'OW') {
			# 島主
			$HlbbsMode = 1;
		} elsif($1 eq 'FO') {
			# 他の島主
			$HlbbsMode = 3;
			$HforeignerID = $HcurrentID;
		} elsif($1 eq 'FD') {
			# 他の島主削除
			$HlbbsMode = 4;
			$HforeignerID = $HcurrentID;
		} else {
			# 削除
			$HlbbsMode = 2;
		}
		$HcurrentID = $2;

		# 削除かもしれないので、番号を取得
		$line =~ /NUMBER=([^\&]*)\&/;
		$HcommandPlanNumber = $1;
		
		$line =~ /LBBSLIST=([^\&]*)\&/;
		$HlbbsMode2 = $1;
	} elsif($line =~ /ChangeInfoButton/) {
		$HmainMode = 'change';
	} elsif($line =~ /MessageButton([0-9]*)/) {
		$HmainMode = 'comment';
		$HcurrentID = $1;
	} elsif($line =~ /CLbbsRButton([0-9]*)/) {
		$HmainMode = 'clbbs';
		$HcurrentID = $1;
	} elsif($line =~ /customButton([0-9]*)/) {
		$HmainMode = 'custom';
		$HcurrentID = $1;
	} elsif($line =~ /customMButton([0-9]*)/) {
		$HmainMode = 'custom2';
		$HcurrentID = $1;
		$Hcustom[3] = 1  if($line =~ /custom3=on/);
		$Hcustom[4] = 1  if($line =~ /custom4=on/);
		$Hcustom[5] = 1  if($line =~ /custom5=on/);
		$Hcustom[6] = 1  if($line =~ /custom6=on/);
		$Hcustom[7] = 1  if($line =~ /custom7=on/);
		$Hcustom[8] = 1  if($line =~ /custom8=on/);
		$Hcustom[9] = 1  if($line =~ /custom9=on/);
		$Hcustom[10] = 1 if($line =~ /custom10=on/);
		$Hcustom[11] = 1 if($line =~ /custom11=on/);
	} elsif($line =~ /MonsButton([0-9]*)/) {
		$HmainMode = 'monsedit';
		$HcurrentID = $1;
	} elsif($line =~ /CommandJavaButton/) {
		$HmainMode = 'commandJava';
		$line =~ /COMARY=([^\&]*)\&/;
		$HcommandComary = $1;
		
		$line =~ /COMMAND=([^\&]*)\&/;
		$HcommandKind = $1;
		$HdefaultKind = $1;
		$line =~ /AMOUNT=([^\&]*)\&/;
		$HcommandArg = $1;
		$line =~ /TARGETID=([^\&]*)\&/;
		$HcommandTarget = $1;
		$defaultTarget = $1;
		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /POINTTX=([^\&]*)\&/;
		$HcommandTX = $1;
		$HdefaultTX = $1;
		$line =~ /POINTTY=([^\&]*)\&/;
		$HcommandTY = $1;
		$HdefaultTY = $1;
		
	} elsif($line =~ /CommandButton/) {
		if($HjavaMode eq 'java'){
			$HmainMode = 'command2';
		}else{
			$HmainMode = 'command';
		}
		# コマンドモードの場合、コマンドの取得
		$line =~ /NUMBER=([^\&]*)\&/;
		
		$HcommandPlanNumber = $1;
		$line =~ /COMMAND=([^\&]*)\&/;
		$HcommandKind = $1;
		$HdefaultKind = $1;
		$line =~ /AMOUNT=([^\&]*)\&/;
		$HcommandArg = $1;
		$line =~ /TARGETID=([^\&]*)\&/;
		$HcommandTarget = $1;
		$defaultTarget = $1;
		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /POINTTX=([^\&]*)\&/;
		$HcommandTX = $1;
		$HdefaultTX = $1;
		$line =~ /POINTTY=([^\&]*)\&/;
		$HcommandTY = $1;
		$HdefaultTY = $1;

		$line =~ /COMMANDMODE=(write|insert|delete)/;
		$HcommandMode = $1;
	} elsif ($line =~ /camp([0-9]*)/) {
		$HmainMode = 'camp';
		$HcurrentID = $1;
# 資源取引所
	} elsif($getLine =~ /Exchange=([0-9]*)/) {
		$HmainMode = 'exchange';
		$HexchangeMode = 'show';
	} elsif($line =~ /ExchangeButton/) {
		$HmainMode = 'exchange';
		$HexchangeMode = 'add';

		$line =~ /EXC_SELL=([^\&]*)\&/;
		$HexchangeSell = $1;
		$line =~ /EXC_SELL1=([^\&]*)\&/;
		$HexchangeSellCost = $1 * 100;
		$line =~ /EXC_SELL0=([^\&]*)\&/;
		$HexchangeSellCost += $1;
		$line =~ /EXC_BUY=([^\&]*)\&/;
		$HexchangeBuy = $1;
		$line =~ /EXC_BUY1=([^\&]*)\&/;
		$HexchangeBuyCost = $1 * 100;
		$line =~ /EXC_BUY0=([^\&]*)\&/;
		$HexchangeBuyCost += $1;
	} elsif($line =~ /ExchangeBidButton/) {
		$HmainMode = 'exchange';
		$HexchangeMode = 'bid';
		$line =~ /EXC_SELL1=([^\&]*)\&/;
		$HexchangeSellCost = $1 * 100;
		$line =~ /EXC_SELL0=([^\&]*)\&/;
		$HexchangeSellCost += $1;
		$line =~ /EXC_ID=([^\&]*)\&/;
		$HexchangeBidID = $1;
		$HexchangeCon = 1;
	} elsif($line =~ /ExchangeBid2Button/) {
		$HmainMode = 'exchange';
		$HexchangeMode = 'bid';
		$line =~ /EXC_SELL=([^\&]*)\&/;
		$HexchangeSellCost = $1;
		$line =~ /EXC_ID=([^\&]*)\&/;
		$HexchangeBidID = $1;
		$HexchangeCon = 0;
	} elsif($line =~ /ExchangeDelButton/) {
		$HmainMode = 'exchange';
		$HexchangeMode = 'del';

		$line =~ /EXC_ID=([^\&]*)\&/;
		$HexchangeDelID = $1;

# 詳細表示
	} elsif($getLine =~ /list=([0-9]*)/) {
		$HlistID = $1;
		$HmainMode = 'list';

# 宇宙マップ表示
	} elsif($getLine =~ /space=([0-9]*)/) {
		$HspaceID = $1;
		$HmainMode = 'space';

# 海域マップ表示
	} elsif($getLine =~ /Ocean=([0-9]*)/) {
		$HmainMode = 'ocean';

# BattleField作成モード
	} elsif($getLine =~ /Bfield=([^\&]*)/) {
		# 最初の起動
		$HmainMode = 'bfield';
		$HbfieldMode = 0;
		$HdefaultPassword = $1;
	} elsif($line =~ /Bfield=([^\&]*)\&/) {
		# BattleField作成ボタンが押された起動
		$HmainMode = 'bfield';
		if($line =~ /LBFIELD=([0-9]+)\&/){
			$HbfieldMode = $1;
		}else{
			$HbfieldMode = 0;
		}
		$HdefaultPassword = $1;
# 初期設定確認モード
	} elsif($getLine =~ /SetupV=([^\&]*)/) {
		$HmainMode = 'setupv';
		$HdefaultPassword = $1;

# 簡易トーナメント
} elsif($getLine =~ /LoseMap=([0-9]*)/) {
	$HmainMode = 'FightIsland';
	$HcurrentID = $1;
} elsif($getLine =~ /FightLog/) {
	$HmainMode = 'FightView';

# 管理人によるプレゼントモード
	} elsif($getLine =~ /Present/) {
		# 最初の起動
		$HmainMode = 'present';
		$HpresentMode = 0;
	} elsif($line =~ /Present/) {
		# プレゼントボタンが押された起動
		$HmainMode = 'present';
		$HpresentMode = 1;
		($HpresentMoney) = ($line =~ /PRESENTMONEY=([^\&]*)\&/);
		($HpresentFood ) = ($line =~ /PRESENTFOOD=([^\&]*)\&/);
		($HpresentLog)   = ($line =~ /PRESENTLOG=([^\&]*)\&/);

# 管理人による制裁モード
	} elsif($getLine =~ /Punish=([^\&]*)/) {
		# 最初の起動
		$HmainMode = 'punish';
		$HpunishMode = 0;
		$HdefaultPassword = $1;
	} elsif($line =~ /Punish=([^\&]*)\&/) {
		# 制裁ボタンが押された起動
		$HmainMode = 'punish';
		$HpunishMode = 1;
		$HdefaultPassword = $1;

		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /PUNISHID=([^\&]*)\&/;
		$HpunishID = $1;
# 管理人による地形変更モード
	} elsif($getLine =~ /Lchange=([^\&]*)/) {
		# 最初の起動
		$HmainMode = 'lchange';
		$HlchangeMode = 0;
		$HdefaultPassword = $1;
	} elsif($line =~ /LchangeButtonM=([^\&]*)\&/) {
		# マップ変更
		$HmainMode = 'lchange';
		$HlchangeMode = 0;
		$line =~ /Lchange=([^\&]*)\&/;
		$HdefaultPassword = $1;
	} elsif($line =~ /Lchange=([^\&]*)\&/) {
		# 変更ボタンが押された起動
		$HmainMode = 'lchange';
		$HlchangeMode = 1;
		$HdefaultPassword = $1;

		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /LCHANGEKIND=([^\&]*)\&/;
		$HlchangeKIND = $1;
		$line =~ /LCHANGEVALUE=([^\&]*)\&/;
		$HlchangeVALUE = $1;
# 管理人による各種島データ変更モード
	} elsif($getLine =~ /Ichange=([^\&]*)/) {
		# 最初の起動
		$HmainMode = 'ichange';
		$HichangeMode = 0;
		$HdefaultPassword = $1;
	} elsif($line =~ /Ichange=([^\&]*)\&/) {
		$HmainMode = 'ichange';
		$HichangeMode = 1;
		$HdefaultPassword = $1;
		$line =~ /ICID=([^\&]*)\&/;
		$HcurrentID = $1;
		$line =~ /ICMONEY=([^\&]*)\&/;
		$Hicmoney = $1;
		$line =~ /ICFOOD=([^\&]*)\&/;
		$Hicfood = $1;
		$line =~ /ICWEAPON=([^\&]*)\&/;
		$Hicweapon = $1;
		$line =~ /ICEVIL=([^\&]*)\&/;
		$Hicevil = $1;
		$Hicspace = 1 if($line =~ /ICSPACE=on/);
		$line =~ /ICALLY=([^\&]*)\&/;
		$Hically = $1;
# 管理人によるあずかりモード
	} elsif($getLine =~ /Pdelete=([^\&]*)/) {
		# 最初の起動
		$HmainMode = 'predelete';
		$HpreDeleteMode = 0;
		$HdefaultPassword = $1;
	} elsif($line =~ /Pdelete=([^\&]*)\&/) {
		# 変更ボタンが押された起動
		$HmainMode = 'predelete';
		$HpreDeleteMode = 1;
		$HdefaultPassword = $1;
	} else {
		$HmainMode = 'top';
	}

	if($line =~ /SKIN=([^\&]*)\&/) {
		my($flag) = $1;
		if(($flag eq 'del') || ($flag eq '')){
			$flag = $HcssFile;
		}
		$HskinName = $flag;
	}

# デバッグ
	if($getLine =~ /debug=([0-9]*)/) {
		$HdebugMode = $1;
	}
}


#cookie入力
sub cookieInput {
	my($cookie);

	$cookie = jcode::euc($ENV{'HTTP_COOKIE'});

	if($cookie =~ /${HthisFile}OWNISLANDID=\(([^\)]*)\)/) {
		$defaultID = $1;
	}
	if($cookie =~ /${HthisFile}OWNISLANDPASSWORD=\(([^\)]*)\)/) {
		$HdefaultPassword = $1;
	}
	if($cookie =~ /${HthisFile}TARGETISLANDID=\(([^\)]*)\)/) {
		$defaultTarget = $1;
	}
	if($cookie =~ /${HthisFile}LBBSNAME=\(([^\)]*)\)/) {
		$HdefaultName = $1;
	}
	if($cookie =~ /${HthisFile}POINTX=\(([^\)]*)\)/) {
		$HdefaultX = $1;
	}
	if($cookie =~ /${HthisFile}POINTY=\(([^\)]*)\)/) {
		$HdefaultY = $1;
	}
	if($cookie =~ /${HthisFile}POINTTX=\(([^\)]*)\)/) {
		$HdefaultTX = $1;
	}
	if($cookie =~ /${HthisFile}POINTTY=\(([^\)]*)\)/) {
		$HdefaultTY = $1;
	}
	if($cookie =~ /${HthisFile}KIND=\(([^\)]*)\)/) {
		$HdefaultKind = $1;
	}
	if($cookie =~ /${HthisFile}JAVAMODESET=\(([^\)]*)\)/) {
		$HjavaModeSet = $1;
	}
	# ローカル画像指定
	if($cookie =~ /${HthisFile}IMGLINE=\(([^\)]*)\)/) {
		$HimgLine = $1;
	}
	# 船系で透過画像を使用するか
	if($cookie =~ /${HthisFile}MYSHIP=\(([^\)]*)\)/) {
		$Hmyship = $1;
	}
	# スタイルシート
	if($cookie =~ /${HthisFile}SKIN=\(([^\)]*)\)/) {
		$HskinName = $1;
	}
}

#cookie出力
sub cookieOutput {
	my($cookie, $info);

	# 消える期限の設定
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	gmtime(time + 30 * 86400); # 現在 + 30日

	# 2ケタ化
	$year += 1900;
	$date = "0$date" if($date < 10);
	$hour = "0$hour" if($hour < 10);
	$min  = "0$min" if($min < 10);
	$sec  = "0$sec" if($sec < 10);

	# 曜日を文字に
	$day = ("Sunday", "Monday", "Tuesday", "Wednesday",
			"Thursday", "Friday", "Saturday")[$day];

	# 月を文字に
	$mon = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
			"Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[$mon];

	# パスと期限のセット
	$info = "; expires=$day, $date\-$mon\-$year $hour:$min:$sec GMT\n";
	$cookie = '';

	if(($HcurrentID) && ($HmainMode eq 'owner')){
		$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDID=($HcurrentID) $info";
	}
	if($HinputPassword) {
		$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDPASSWORD=($HinputPassword) $info";
	}
	if($HcommandTarget) {
		$cookie .= "Set-Cookie: ${HthisFile}TARGETISLANDID=($HcommandTarget) $info";
	}
	if($HlbbsName) {
		$cookie .= "Set-Cookie: ${HthisFile}LBBSNAME=($HlbbsName) $info";
	}
	if($HcommandX) {
		$cookie .= "Set-Cookie: ${HthisFile}POINTX=($HcommandX) $info";
	}
	if($HcommandY) {
		$cookie .= "Set-Cookie: ${HthisFile}POINTY=($HcommandY) $info";
	}
	if($HcommandTX) {
		$cookie .= "Set-Cookie: ${HthisFile}POINTTX=($HcommandTX) $info";
	}
	if($HcommandTY) {
		$cookie .= "Set-Cookie: ${HthisFile}POINTTY=($HcommandTY) $info";
	}
	if($HcommandKind) {
		# 自動系以外
		$cookie .= "Set-Cookie: ${HthisFile}KIND=($HcommandKind) $info";
	}
	if($HjavaMode) {
		$cookie .= "Set-Cookie: ${HthisFile}JAVAMODESET=($HjavaMode) $info";
	}
	# ローカル画像指定
	if($HimgLine) {
		$cookie .= "Set-Cookie: ${HthisFile}IMGLINE=($HimgLine) $info";
	}
	# 船系で透過画像を使用するか
	if($HmyshipFlg) {
		$cookie .= "Set-Cookie: ${HthisFile}MYSHIP=($Hmyship) $info";
	}
	# スタイルシート
	if($HskinName) {
		$cookie .= "Set-Cookie: ${HthisFile}SKIN=($HskinName) $info";
	}
	out($cookie);
}

#----------------------------------------------------------------------
# ユーティリティ
#----------------------------------------------------------------------
sub hakolock {
	if($lockMode == 1) {
		# directory式ロック
		return hakolock1();
	} elsif($lockMode == 2) {
		# flock式ロック
		return hakolock2();
	} elsif($lockMode == 3) {
		# symlink式ロック
		return hakolock3();
	} elsif($lockMode == 4) {
		# 通常ファイル式ロック
		return hakolock4();
	} else {
		# rename式ロック
		$lfh = hakolock5() or die return 0;
		return 1;
	}
}

sub hakolock1 {
	# ロックを試す
	if(mkdir('hakojimalock', $HdirMode)) {
		# 成功
		return 1;
	} else {
		# 失敗
		my($b) = (stat('hakojimalock'))[9];
		if(($b > 0) && ((time() -  $b)> $unlockTime)) {
			# 強制解除
			unlock();

			# ヘッダ出力
			tempHeader();

			# 強制解除メッセージ
			tempUnlock();

			# フッタ出力
			tempFooter();

			# 終了
			exit(0);
		}
		return 0;
	}
}

sub hakolock2 {
	open(LOCKID, '>>hakojimalockflock');
	if(flock(LOCKID, 2)) {
		# 成功
		return 1;
	} else {
		# 失敗
		return 0;
	}
}

sub hakolock3 {
	# ロックを試す
	if(symlink('hakojimalockdummy', 'hakojimalock')) {
		# 成功
		return 1;
	} else {
		# 失敗
		my($b) = (lstat('hakojimalock'))[9];
		if(($b > 0) && ((time() -  $b)> $unlockTime)) {
			# 強制解除
			unlock();

			# ヘッダ出力
			tempHeader();

			# 強制解除メッセージ
			tempUnlock();

			# フッタ出力
			tempFooter();

			# 終了
			exit(0);
		}
		return 0;
	}
}

sub hakolock4 {
	# ロックを試す
	if(unlink('lockfile')) {
		# 成功
		open(OUT, '>lockfile.lock');
		print OUT time;
		close(OUT);
		return 1;
	} else {
		# ロック時間チェック
		if(!open(IN, 'lockfile.lock')) {
			return 0;
		}
		my($t);
		$t = <IN>;
		close(IN);
		if(($t != 0) && (($t + $unlockTime) < time)) {
			# 120秒以上経過してたら、強制的にロックを外す
			unlock();

			# ヘッダ出力
			tempHeader();

			# 強制解除メッセージ
			tempUnlock();

			# フッタ出力
			tempFooter();

			# 終了
			exit(0);
		}
		return 0;
	}
}

# rename式(Perlメモ http://www.din.or.jp/~ohzaki/perl.htm#File_Lock)
sub hakolock5 {
	my %lfh = (dir => "./", basename => "lockfile", timeout => $unlockTime, trytime => 3, @_);
	$lfh{path} = $lfh{dir}.$lfh{basename};

	for (my $i = 0; $i < $lfh{trytime}; $i++, sleep 1) {
		return \%lfh if (rename($lfh{path}, $lfh{current} = $lfh{path} . time));
	}

	opendir(LOCKDIR, $lfh{dir});
	my @filelist = readdir(LOCKDIR);
	closedir(LOCKDIR);

	foreach (@filelist) {
		if (/^$lfh{basename}(\d+)/) {
			return \%lfh if (time - $1 > $lfh{timeout} and
			rename($lfh{dir} . $_, $lfh{current} = $lfh{path} . time));
			last;
		}
	}
	undef;
}

# ロックを外す
sub unlock {
	if($lockMode == 1) {
		# directory式ロック
		rmdir('hakojimalock');
	} elsif($lockMode == 2) {
		# flock式ロック
		close(LOCKID);
	} elsif($lockMode == 3) {
		# symlink式ロック
		unlink('hakojimalock');
	} elsif($lockMode == 4) {
		# 通常ファイル式ロック
		my($i);
		$i = rename('lockfile.lock', 'lockfile');
	} else {
		# rename式ロック
		rename($lfh->{current}, $lfh->{path});
	}
}

# 小さい方を返す
sub min {
	return ($_[0] < $_[1]) ? $_[0] : $_[1];
}

# 1000億単位丸めルーチン
sub aboutMoney {
	my($m) = @_;
	if($m < 500) {
		return "推定500${HunitMoney}未満";
	} else {
		$m = int(($m + 500) / 1000);
		return "推定${m}000${HunitMoney}";
	}
}

# 切り揃え
sub cutColumn {
	my($s, $c) = @_;
	if(length($s) <= $c) {
		return $s;
	} else {
		# 合計$cケタになるまで切り取り
		my($ss) = '';
		my($count) = 0;
		while($count < $c) {
			$s =~ s/(^[\x80-\xFF][\x80-\xFF])|(^[\x00-\x7F])//;
			if($1) {
				$ss .= $1;
				$count ++;
			} else {
				$ss .= $2;
			}
			$count ++;
		}
		return $ss;
	}
}

# 島の名前から番号を得る(IDじゃなくて番号)
sub nameToNumber {
	# 全島から探す
	my($i);
	for($i = 0; $i < $HislandNumber; $i++) {
		return $i if($Hislands[$i]->{'name'} eq $_[0]);
	}
	return -1; # 見つからなかった場合
}

# 怪獣の情報
sub monsterSpec {
	my($kind) = int($_[0] / 100);
	# 種類,名前,体力
	return ($kind, $HmonsterName[$kind], $_[0] - ($kind * 100));
}

# 巨大怪獣の情報
sub bigMonsterSpec {
	my($limit) = int($_[0] / 10000);
	my($d) = $_[0] - ($limit * 10000);
	my($hp) = int($d / 100);
	$d = $d - ($hp * 100);
	my($ld) = int($d / 10);
	# 制限時間,HP,地形,位置
	return ($limit, $hp, $ld, $d - ($ld * 10));
}

# 船の情報
sub shipSpec {
	my($order) = int($_[0] / 10000);
	my($lv2) = $_[0] - ($order * 10000);
	my($hp) = int($lv2 / 1000);
	# 指令,耐久力,ID
	return ($order, $hp, $lv2 - ($hp * 1000));
}

# 天候の情報
sub weatherinfo {
	my($lv) = @_;

	$lv = 1114 if($lv > 5559); # 不正な数字の時

	# 明後日の天気
	my($kind3) = int($lv / 1000);
	$kind3 = 1 if($kind3 >= 6); # 不正な数字の時

	my($lv2) = $lv - ($kind3 * 1000);

	# 明日の天気
	my($kind2) = int($lv2 / 100);
	$kind2 = 1 if($kind2 >= 6); # 不正な数字の時

	my($lv3) = $lv2 - ($kind2 * 100);

	# 天気
	my($kind) = int($lv3 / 10);
	$kind = 1 if($kind >= 6); # 不正な数字の時

	my($name) = $WeatherName[$kind];# 名前
	my($hp) = $lv3 - ($kind * 10);# 地盤の状態
	return ($kind, $name, $hp, $kind2, $kind3);
}

# 経験地からレベルを算出
sub expToLevel {
	my($kind, $exp) = @_;
	my($i);
	if(($kind == $HlandBase) || ($kind == $HlandSpaceBase)) {
		# ミサイル基地
		for($i = $maxBaseLevel; $i > 1; $i--) {
			return $i if($exp >= $baseLevelUp[$i - 2]);
		}
	}elsif($kind == $HlandDokan){
		# 地下 土管
		return $exp % 100;
	}else{
		# 海底基地など
		for($i = $maxSBaseLevel; $i > 1; $i--) {
			return $i if($exp >= $sBaseLevelUp[$i - 2]);
		}
	}
	return 1;
}

# 周囲の海系地形の数を数える
sub seaAround {
	my($land, $x, $y, $range, $mode) = @_;
	my($i, $count, $sx, $sy);
	$count = 0;
	for($i = 0; $i < $range; $i++) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		
		# 行による位置調整
		$sx-- if(!($sy % 2) && ($y % 2));
		
		if(($sx < 0) || ($sx >= $HislandSize) || ($sy < 0) || ($sy >= $HislandSize)) {
			# 範囲外の場合
			$count++;
		} elsif(($HseaChk[$land->[$sx][$sy]] == 3) && ($mode)){
			# 防波堤は除く
			next;
		} elsif($HseaChk[$land->[$sx][$sy]]) {
			# 海系地形の場合
			$count++;
		}
	}
	return $count;
}

# (0,0)から(size - 1, size - 1)までの数字が一回づつ出てくるように
# (@Hrpx, @Hrpy)を設定
sub makeRandomPointArray {
	# 初期値
	my($y,$i,$j);
	@Hrpx = (0..$HislandSize-1) x $HislandSize;
	for($y = 0; $y < $HislandSize; $y++) {
		push(@Hrpy, ($y) x $HislandSize);
	}

	# シャッフル
	for ($i = $HpointNumber; --$i; ) {
		$j = int(rand($i+1)); 
		next if($i == $j);
		@Hrpx[$i,$j] = @Hrpx[$j,$i];
		@Hrpy[$i,$j] = @Hrpy[$j,$i];
	}
}
sub makeRandomOceanPointArray {
	# 初期値
	my($y,$i,$j);
	@HrpxO = (0..$HoceanSize-1) x $HoceanSize;
	for($y = 0; $y < $HoceanSize; $y++) {
		push(@HrpyO, ($y) x $HoceanSize);
	}
	# シャッフル
	for ($i = $HpointOcean; --$i; ) {
		$j = int(rand($i+1)); 
		next if($i == $j);
		@HrpxO[$i,$j] = @HrpxO[$j,$i];
		@HrpyO[$i,$j] = @HrpyO[$j,$i];
	}
}

# 0から(n - 1)の乱数
sub random {
	return int(rand(1) * $_[0]);
}

# 海域の整備
sub OceanMente {
	my($id) = @_;
	my($x,$y,$i,$j);
	for($y = 0; $y < $HoceanSize; $y++) {
		for($x = 0; $x < $HoceanSize; $x++) {
			if($Hocean->{'nation'}->[$x][$y] == $id){
				if(($Hocean->{'land'}->[$x][$y] == $HlandOPlayer) ||
				   ($Hocean->{'land'}->[$x][$y] == $HlandOcean)){
					$Hocean->{'land'}->[$x][$y] = $HlandOcean;
				}else{
					$Hocean->{'land'}->[$x][$y] = $HlandSea;
				}
				$Hocean->{'landValue'}->[$x][$y] = 0;
				$Hocean->{'land2'}->[$x][$y] = 0;
				$Hocean->{'landValue2'}->[$x][$y] = 0;
				$Hocean->{'nation'}->[$x][$y] = 0;
			}
		}
	}
}

#----------------------------------------------------------------------
# ログ表示
#----------------------------------------------------------------------
# ファイル番号指定でログ表示
sub logFilePrint {
	my($fileNumber, $id, $mode) = @_;
	open(LIN, "${HlogdirName}/hakojima.log$_[0]");
	my($line, $m, $turn, $id1, $id2, $message);
	my($set_turn) = 0;
	while($line = <LIN>) {
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
		($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

		# 機密関係
		if($m == 1) {
			next if(($mode == 0) || ($id1 != $id)); # 機密表示権利なし
			$m = "${HtagNumber_}<B>(機密)</B>${H_tagNumber}：";
		} else {
			$m = '';
		}

		# 表示的確か
		if($id != 0) {
			next if(($id != $id1) && ($id != $id2));
		}
		
		if($set_turn == 0){
			out("<NOBR><B>=====[<span class=number><FONT SIZE=4> ターン$turn </FONT></span>]================================================</B><NOBR><BR>\n");
			$set_turn++;
		}

		# 表示
		out("<NOBR>${m}${message}</NOBR><BR>\n");
	}
	close(LIN);
}

#----------------------------------------------------------------------
# プロファイルから情報取得
#----------------------------------------------------------------------
#
# プロファイルを読んで指定された島IDの背景画像URLを返す
sub getBGImageUrl {
	my($bgimageid) = @_;

	# クッキーから自分のID取得
	my($bgcookie, $myId);
	$bgcookie = jcode::euc($ENV{'HTTP_COOKIE'});
	if($bgcookie =~ /OWNISLANDID=\(([^\)]*)\)/) {
		$myId = $1;
		&readProfileMAP($myId);
	}
	if($Hprofile{'BackgroundUse'} == 2) {
		# 背景画像を表示しない時
		return '';
	}
	if($myId == $bgimageid) {
		# 自分の島の場合
		return $Hprofile{'BackgroundImage'};
	}
	
	&readProfileMAP($bgimageid);
	return $Hprofile{'BackgroundImage'};
}

sub readProfileMAP {
	my($proid) = @_;
	if(!open(PIN, "$HprofileDir/profile${proid}.dat")){
		$Hprofile{'MyHomeImage'} = '';
		$Hprofile{'BackgroundImage'} = '';
		$Hprofile{'BackgroundUse'} = '';
		return 0;
	}

	<PIN>;#lastModify
	<PIN>;#photo
	<PIN>;#address
	<PIN>;#age
	<PIN>;#sex
	<PIN>;#job
	<PIN>;#email
	<PIN>;#icq
	<PIN>;#webtitle
	<PIN>;#webaddr
	<PIN>;#comment
	<PIN>;#bestweb1
	<PIN>;#bestweb2
	<PIN>;#bestweb3
	
	my($HomeImage, $BGImage, $BGImageUse);
	$HomeImage = <PIN>;
	$BGImage   = <PIN>;
	$BGImageUse = int(<PIN>);
	
	chomp($HomeImage);
	chomp($BGImage);
	
	$Hprofile{'MyHomeImage'} = $HomeImage;
	$Hprofile{'BackgroundImage'} = $BGImage;
	$Hprofile{'BackgroundUse'} = $BGImageUse;

	close(PIN);
	return 1;
}

#----------------------------------------------------------------------
# テンプレート
#----------------------------------------------------------------------
# ヘッダ
sub tempHeader {
	my($js) = @_;
	# ローカル画像指定
	$baseIMG = ($HimgLine ne '') ? $HimgLine : $imageDir;
	$baseSKIN = ($HskinName ne '') ? "$imageDir/$HskinName" : "$imageDir/$HcssFile";
	out("Content-type: text/html\n\n");
	return if($Hasync);
	out(<<END);
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<TITLE>$Htitle</TITLE>
<BASE HREF="$baseIMG/">
END
	if($js == 1){
		# jsモード
		$Body = "<BODY onload=\"SelectList('');init()\">";
		my($MyImage) = getBGImageUrl($HcurrentID);
		if(substr($MyImage,0,7) eq 'http://'){
			if($MyImage =~ /\.css$/){
				$baseSKIN = $MyImage;
			}else{
				$Body = "<BODY onload=\"SelectList('');init()\" $htmlBgColor BACKGROUND=${MyImage}>";
			}
		}
	}else{
		if(($HmainMode eq 'print') || ($HmainMode eq 'command') ||
			($HmainMode eq 'owner') || ($HmainMode eq 'comment') || ($HmainMode eq 'lbbs')) {
			# 島のマップを呼び出す時
			my($MyImage) = getBGImageUrl($HcurrentID);
			if(substr($MyImage,0,7) eq 'http://'){
				if($MyImage =~ /\.css$/){
					$Body = "<BODY>";
					$baseSKIN = $MyImage;
				}else{
					$Body = "<BODY $htmlBgColor BACKGROUND=${MyImage}>";
				}
			}
		}
	}
	out(<<END);
<link rel="stylesheet" type="text/css" href="$baseSKIN">
</HEAD>
$Body
<DIV ID='BodySpecial'><DIV ID='LinkHead'>
<A HREF="http://t.pos.to/hako/" target="_blank">箱庭諸島スクリプト配布元</A> /
<A HREF="http://appoh.execweb.cx/hakoniwa/" target="_blank">箱庭Javaスクリプト版 配布元</A> /
<A HREF="$HbaseDir/history.cgi?saikin=0" target="_blank"> 最近の出来事</A> /
<A HREF="$HbaseDir/ranking.cgi" target="_blank"> ランキング</A> /
<A HREF="$HbaseDir/profile.cgi" target="_blank"> プロファイル</A> /
<A HREF="$helpDir" target="_blank">ヘルプ</A> /
<A HREF="$bbs" target="_blank">掲示板</A> /
<A HREF="$toppage">トップページ</A> /
</DIV><HR>
END
}
# フッタ
sub tempFooter {
	out(<<END);
<HR>
<DIV ID='LinkFoot'>
究想の箱庭「みんなで歩む箱庭進化論」${versionInfo}<BR>
管理者：$adminName(<A HREF="mailto:$email">$email</A>)<BR>
改造元：究想の箱庭開発(<A HREF="http://www8.plala.or.jp/nayupon/">http://www8.plala.or.jp/nayupon/</A>)<BR>
箱庭諸島のページ(<A HREF="http://t.pos.to/hako/">http://t.pos.to/hako/</A>)<BR>
画像配布元：<A HREF="http://www.propel.ne.jp/~yysky/">K.Y studio</A>/
<A HREF="http://www5b.biglobe.ne.jp/~k-e-i/i.html">Hakoniwa R.A.</A>/
<A HREF="http://www.qoonet.com/hakoniwa.html">箱庭QooLand</A>/
<A HREF="http://color.2.pro.tok2.com/">P L U S +</A><BR>
</DIV>
END
##### 追加 親方20020307
	if($Hperformance) {
		my($uti, $sti, $cuti, $csti) = times();
		$uti += $cuti;
		$sti += $csti;
		my($cpu) = $uti + $sti;

		# ログファイル書き出し(テスト計測用　普段はコメントにしておいてください)
#		open(POUT,">>cpu-h.log");
#		print POUT "CPU($cpu) : user($uti) system($sti)\n";
#		close(POUT);

		out(<<END);
<DIV align="right">
<SMALL>CPU($cpu) : user($uti) system($sti)</SMALL>
</DIV>
END
	}
#####
	out(<<END);
</BODY>
</HTML>
END
}

# ロック失敗
sub tempLockFail {
	# タイトル
	out(<<END);
${HtagBig_}同時アクセスエラーです。<BR>
ブラウザの「戻る」ボタンを押し、<BR>
しばらく待ってから再度お試し下さい。${H_tagBig}$HtempBack
END
}

# 強制解除
sub tempUnlock {
	# タイトル
	out(<<END);
${HtagBig_}前回のアクセスが異常終了だったようです。<BR>
ロックを強制解除しました。${H_tagBig}$HtempBack

END
}

# パスワードファイルがない
sub tempNoPasswordFile {
	out(<<END);
${HtagBig_}パスワードファイルが開けません。${H_tagBig}$HtempBack
END
}

# hakojima.datがない
sub tempNoDataFile {
	out(<<END);
${HtagBig_}データファイルが開けません。${H_tagBig}$HtempBack
END
}

# 何か問題発生
sub tempProblem {
	out(<<END);
${HtagBig_}問題発生、とりあえず戻ってください。${H_tagBig}$HtempBack
END
}

# 書き込み失敗
sub tempFailWrite {
	out(<<END);
${HtagBig_}データファイルの書き込みに失敗しました。(エラー番号 ${HerrorNum})${H_tagBig}$HtempBack
END
}

# メンテナンス中
sub mente_mode {
	# ヘッダ出力
	tempHeader() if($_[0]);

	# メッセージ
	out("${HtagBig_}只今メンテナンス中です。<BR>暫くお待ち下さい。${H_tagBig}");

	# フッタ出力
	tempFooter();

	# 終了
	exit(0);
}

