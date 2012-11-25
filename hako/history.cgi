#!/usr/local/bin/perl --

#---------------------------------------------------------------------
#	最近の出来事と最近の天気の履歴を表示
#
#	作成日 : 2001/11/25 V0.10
#	作成者 : ラスティア
#
#	修正内容
#	2001/12/31 V0.20 共通設定部を別ファイルから取り込むようにした。
#	2002/04/20 V0.30 代表のターン数を表示する形式に変更。負荷表示を付けた。
#	2002/08/15 V0.40 統計ファイル表示機能追加。
#	2002/09/18 V0.41 １島辺りの統計を追加。
#	2002/10/29 V0.50 スタイルシート辺りと天気ファイル表示を改良
#	2003/05/05 V0.60 究想の箱庭５仕様に修正。
#	2003/09/15 V0.70 天気画像一覧表示、島ごとの履歴等を取り込み。neo_otackyさんありがとう♪
#	2003/10/26 V0.80 ターン差命令を表示、陣営の履歴表示、一部処理を別ファイルに分離
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#	初期設定
#---------------------------------------------------------------------
require './hako-init.cgi';
require './hako-io.cgi';
require './init-game.cgi';

#----------------------------
#	HTMLに関する設定
#----------------------------
# ブラウザのタイトルバーの名称
$title = '最近の出来事と天気';

# 画面の色や背景の設定(HTML)
$body = '<body>';

# 画面の「戻る」リンク先(URL)
$bye = $HthisFile;

# 最近の天気の色属性
$headNameCellcolor	= 'class=headNameCellcolor';# 最近の天気のヘッダ部分のセル色
$pointCellcolor		= 'class=pointCellcolor';	# 最近の天気の天気部分のセル色
$nameCellcolor		= 'class=nameCellcolor';	# 最近の天気の島名の表示部分のセル色

$tomorrowColor		= 'class=TomorrowColor';	# 最近の天気の明日以降の文字色
$todayColor			= 'class=TodayColor';		# 最近の天気の今日の文字色
$yesterdayColor		= 'class=YesterdayColor';	# 最近の天気の昨日以前の文字色

#メインルーチン-------------------------------------------------------

&cookieInput();
&cgiInput;
if (-e $HpasswordFile) {
	# パスワードファイルがある
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword  = <PIN>); # マスタパスワードを読み込む
	chomp($HspecialPassword = <PIN>); # 特殊パスワードを読み込む
	close(PIN);
}
if(!(&readIslandsFile())){
	&tempHeader();
	&htmlError();
} else {
	$HislandList = getIslandList($HcurrentID);
	&tempHeader();
	print("<DIV ID='RecentlyLog'>\n");
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($name) = $island->{'name'};
	$HcurrentName = "$name$AfterName";
	if($HMode == 100) {
		# 天気
		&logTenki();
	} elsif($HMode == 200) {
		# 統計
		&logStatistical();
	} elsif($HMode == 300) {
		# ターン差命令
		&tempCommandLate();
	} elsif($HMode == 400) {
		# 陣営履歴
		&tempAlly();
#	} elsif($HMode =~ /([0-9]*)/) {
	} else {
		# 最近の出来事
		&logDekigoto();
		if($HMode == 99){
			if($HcurrentID == 0) {
				&logFilePrintAll();
			} else {
				&tempIslandHeader($HcurrentID, $HcurrentName);
				# パスワード
				if(&checkPassword($island, $HinputPassword) && ($HcurrentID eq $defaultID)) {
					&logPrintLocal(1);
				} else {
					# password違う
					&logPrintLocal(0);
				}
			}
		} else {
			if($HcurrentID == 0) {
				&logFilePrint($HMode, $HcurrentID, 0);
			} else {
				&tempIslandHeader($HcurrentID, $HcurrentName);
				# パスワード
				if(&checkPassword($island, $HinputPassword) && ($HcurrentID eq $defaultID)) {
					&logFilePrint($HMode, $HcurrentID, 1);
				} else {
					# password間違い
					&logFilePrint($HMode, $HcurrentID, 0);
				}
			}
		}
		print("<hr>\n");
#	} else {
#		# 天気
#		&logTenki();
	}
	print("</DIV>\n");
}
&tempFooter;
#終了
exit(0);

#サブルーチン---------------------------------------------------------
#---------------------------------------------------------------------
#       関数名 : htmlError
#       機　能 : HTMLのエラーメッセージの出力
#       引　数 : なし
#       戻り値 : なし
#---------------------------------------------------------------------
sub htmlError{
	print("<h2>エラーが発生しました</h2>\n");
}
#---------------------------------------------------------------------
#       関数名 : readIslandsFile
#       機　能 : 全島のデータを読み込む
#       引　数 : なし
#       戻り値 : 0 - ファイルオープンに失敗
#               1 - 成功
#---------------------------------------------------------------------
sub readIslandsFile {
	# データファイルを開く
	if(!open(IN, "${HdirName}/hakojima.dat")) {
		rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
		return 0 if(!open(IN, "${HdirName}/hakojima.dat"));
	}
	# 各パラメータの読みこみ
	$HislandTurn  = int(<IN>);    # ターン数
	<IN>; # 最終更新時間(使用しない値なので読み飛ばす)
	$HislandNumber        = int(<IN>);    # 島の総数
	<IN>; # 次に割り当てるID(使用しない値なので読み飛ばす)
	# 島の読みこみ
	my($i, $id);
	for($i = 0; $i < $HislandNumber; $i++) {
		$Hislands[$i] = readIsland($i);
		$HidToNumber{$Hislands[$i]->{'id'}} = $i;
	}
	# ファイルを閉じる
	close(IN);
	readCommandLate();
	return 1;
}
#---------------------------------------------------------------------
#       関数名 : readIsland
#       機　能 : 各島に割り当てられているIDを取得
#       引　数 : 0 .. $HislandNumber
#       戻り値 : 島のID
#---------------------------------------------------------------------
sub readIsland {
	my($num) = @_;
	my($id, $name, $wline, $weather, $pastweather);
	$name = <IN>;
	$name =~ /(.*),(.*)/; # 島の名前
	$name = $1;
	$id = int(<IN>);# ID番号
	# ファイルポインタを進めるだけなのでname,ID以外は値を格納しない
	for($i = 2; $i < 12; $i++) {
		<IN>;
	}
	$wline = <IN>;  # 天候
	for($i = 13; $i < 35; $i++) {
		<IN>;
	}
	my(@pastw);
	my($w) = 0;
	$wline =~ s/([0-9]*),//;
	$weather = int($1);
	for($w = 0; $w < 10; $w++) {
		$wline =~ s/([0-9]*),//;
		$pastw[$w] = int($1);
	}
	$wline =~ s/([0-9]*)$//;
	$pastw[$w] = int($1);
	return {
		'name' => $name,
		'id' => $id,
		'weather' => $weather,
		'pastweather' => \@pastw,
	};
}
#--------------------------------------------------------------------
#	POST or GETで入力されたデータ取得
#--------------------------------------------------------------------
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

	if($getLine =~ /tenki=([0-9]*)/){
		$HMode = 100;
	} elsif($getLine =~ /statistical=([0-9]*)/){
		$HMode = 200;
		$Graph = $1;
	} elsif($getLine =~ /commandlate=([0-9]*)/){
		$HMode = 300;
	} elsif($getLine =~ /ally=([0-9]*)/){
		$HMode = 400;
		$allyturn = $1;
	} elsif($getLine =~ /saikin=([0-9]*)/){
		$HMode = $1;
	} else {
		$HMode = 0;
	}
	if($line =~ /ID=([0-9]*)/){
		$HcurrentID = $1;
	}
	if($line =~ /PASSWORD=([^\&]*)/) {
		$HinputPassword = $1;
	}
	if($getLine =~ /ID=([0-9]*)/){
		$HcurrentID = $1;
	}
	if($getLine =~ /PASSWORD=([^\&]*)/) {
		$HinputPassword = $1;
	}
	if($getLine =~ /Event=([0-9]*)/){
		$HMode = $1;
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
	if($cookie =~ /${HthisFile}SKIN=\(([^\)]*)\)/) {
		$HskinName = $1;
	}

}

#---------------------------------------------------------------------
#	HTMLのヘッダとフッタ部分を出力
#---------------------------------------------------------------------
# ヘッダ
sub tempHeader {
#	print qq{Content-type: text/html; charset=Shift_JIS\n\n};
	print qq{Content-type: text/html; charset=EUC-JP\n\n};
	print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
	$HskinName = ($HskinName ne '') ? "$imageDir/$HskinName" : "$imageDir/$HcssFile";
	print(<<END);
<html lang="ja">
<!--龠龠龠-->
<head>
<meta http-equiv="Content-Type" content="text/html; charset=EUC-JP">
<TITLE>
$title
</TITLE>
<link rel="stylesheet" type="text/css" href="$HskinName">
</HEAD>
$body
<DIV ID='BodySpecial'><DIV ID='LinkHead'></DIV><DIV ID='LinkTop'>
<FORM name="recentForm" action="${HbaseDir}/history.cgi" method="POST" style="margin  : 2px 0px;">
<A HREF="$bye">[戻る]</A>　
<B>[最近の出来事]</B>　<A HREF="history.cgi?saikin=99">[ALL]</A>
END
	my($i, $turn);
	for($i = 0;$i < $HtopLogTurn;$i++) {
		$turn = $HislandTurn - $i;
		return unless($turn > 0);
		print("<A HREF='history.cgi?saikin=${i}'>");
		if($i == 0) {
			print("[ターン${turn}(現在)]");
		} else {
			print("[${turn}]");
		}
		print("</A>\n");
	}
	my $tmp = "";
	if($Hallyflg){
		$tmp = "<A HREF=\"history.cgi?ally=0\">[陣営の履歴]</A>";
	}
	print(<<END);
<SELECT NAME="ID">$HislandList</SELECT>
<INPUT type=hidden name=PASSWORD value=$HinputPassword>
<INPUT type="submit" value="を見る">
</FORM><HR>
<A HREF="history.cgi?tenki=0">[最近の天気]</A>
<A HREF="history.cgi?commandlate=0">[ターン差命令]</A>
$tmp
<A HREF="history.cgi?statistical=0">[統計 ALL]</A>
<A HREF="history.cgi?statistical=30">[統計１島あたり]</A>
<HR></DIV>
END
}
# フッタ
sub tempFooter {
	my($uti, $sti, $cuti, $csti) = times();
	$uti += $cuti;
	$sti += $csti;
	my($cpu) = $uti + $sti;
	print(<<END);
<DIV align="right"><SMALL>CPU($cpu) : user($uti) system($sti)</SMALL></DIV>
<P></DIV></BODY></HTML>
END
}
#---------------------------------------------------------------------
#	天気ファイル表示
#---------------------------------------------------------------------
sub logTenki {
	my($i, $j, $name, $turn);
	print(<<END);
<H1>最近の天気</H1>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=100% BGCOLOR="#000000"><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<TR><TD $headNameCellcolor rowspan=2 NOWRAP>島の名前</TD>
<TD $headNameCellcolor colspan=3 NOWRAP><span $tomorrowColor>予報</span></TD>
END
for($i = 0; $i < 11; $i++) {
	$turn = $HislandTurn - $i;
	next if($turn < 1);
	print("<TD $headNameCellcolor rowspan=2 NOWRAP>");
	if($i == 0) {
		print("<nobr><span $todayColor>ターン${turn}<br>(現在)</nobr>");
	} else {
		print("${turn}");
	}
	print("</TD>");
}
print("</TR><TR>");
$turn = $HislandTurn + 3;
print("<TD $headNameCellcolor NOWRAP>$turn<br><small>(明後日)</small></TD>");
$turn--;
print("<TD $headNameCellcolor NOWRAP>$turn<br><small>(明日)</small></TD>");
$turn--;
print("<TD $headNameCellcolor NOWRAP>$turn<br><small>(今日)</small></TD></TR>");
for($i = 0; $i < $HislandNumber; $i++) {
	$no = $HidToNumber{$Hislands[$i]->{'id'}};
	$name = $Hislands[$i]->{'name'};
	my($wkind, $wname, $whp, $wkind2, $wkind3) = weatherinfo($Hislands[$i]->{'weather'});
	$pastweather = $Hislands[$i]->{'pastweather'};
	print(<<END);
<TR>
<TD $nameCellcolor NOWRAP><nobr>${name}${AfterName}</TD>
<TD $pointCellcolor NOWRAP><img src ="${imageDir}/$WeatherIcon[${wkind3}]"><br><span $tomorrowColor>$WeatherName[${wkind3}]</span></TD>
<TD $pointCellcolor NOWRAP><img src ="${imageDir}/$WeatherIcon[${wkind2}]"><br><span $tomorrowColor>$WeatherName[${wkind2}]</span></TD>
<TD $pointCellcolor NOWRAP><img src ="${imageDir}/$WeatherIcon[${wkind}]"><br><span $tomorrowColor>$WeatherName[${wkind}]</span></TD>
END
	for($j = 0; $j < 11; $j++) {
		$turn = $HislandTurn - $j;
		next if($turn < 1);
		print("<TD BGCOLOR=#ffffff NOWRAP><img src ='${imageDir}/$WeatherIcon[$pastweather->[$j]]'><br>");
		if($j){
			print("<span $yesterdayColor>");
		}else{
			print("<span $todayColor>");
		}
		print("$WeatherName[$pastweather->[$j]]</span></TD>");
	}
	print("</TR>\n");
}
print("</TABLE></TD></TR></TABLE><br>\n");
}
#---------------------------------------------------------------------
#	天候の情報
#---------------------------------------------------------------------
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
#---------------------------------------------------------------------
#	統計ファイル表示
#---------------------------------------------------------------------
sub logStatistical {
	my(@line, $l);
	if(open(HIN, "${HlogdirName}/statistical.log")){
		while($l = <HIN>) {
			chomp($l);
			push(@line, $l);
		}
		close(HIN);
	}else{
		print("まだデータがありません。\n");
		return;
	}
	my $gimage = "$imageDir/graph.gif";
	my $oneisland = ($Graph >= 30) ? "(１島あたり)" : "";
	print(<<END);
<H1>究想の箱庭統計${oneisland}</H1>
<TABLE border=1><TR><TH $HbgTitleCell>ターン</TH><TH $HbgTitleCell>総人口</TH><TH $HbgTitleCell>総資金</TH><TH $HbgTitleCell>総面積</TH><TH $HbgTitleCell>総預金</TH><TH $HbgTitleCell>総ミサイル発射数</TH><TH $HbgTitleCell>総農場</TH><TH $HbgTitleCell>総商業</TH><TH $HbgTitleCell>総工業</TH><TH $HbgTitleCell>総養殖</TH><TH $HbgTitleCell>総森林</TH><TH $HbgTitleCell>島の数</TH></TR>
END
	my(@tdata,$title,@ld);
	foreach $l (@line) {
		@ld = split(/,/, $l);
		if($Graph >= 30){
			# １島あたり
			if(int(@ld[11]) < 1){
				@ld[1] = '';
				@ld[2] = '';
				@ld[3] = '';
				@ld[4] = '';
				@ld[5] = '';
				@ld[6] = '';
				@ld[7] = '';
				@ld[8] = '';
				@ld[9] = '';
				@ld[10] = '';
			}else{
				@ld[1] = int(@ld[1] / @ld[11]);
				@ld[2] = int(@ld[2] / @ld[11]);
				@ld[3] = int(@ld[3] / @ld[11]);
				@ld[4] = int(@ld[4] / @ld[11]);
				@ld[5] = int(@ld[5] / @ld[11]);
				@ld[6] = int(@ld[6] / @ld[11]);
				@ld[7] = int(@ld[7] / @ld[11]);
				@ld[8] = int(@ld[8] / @ld[11]);
				@ld[9] = int(@ld[9] / @ld[11]);
				@ld[10] = int(@ld[10] / @ld[11]);
			}
			$title = "の推移のグラフ(１島あたり)";
		}else{
			$title = "の推移のグラフ";
		}
		if($Graph == 1){
			$title = "総人口${title}";
			push(@tdata, int(@ld[1]/100));
		}elsif($Graph == 2){
			$title = "総資金${title}";
			push(@tdata, int(@ld[2]/1000));
		}elsif($Graph == 3){
			$title = "総面積${title}";
			push(@tdata, @ld[3]);
		}elsif($Graph == 4){
			$title = "総預金${title}";
			push(@tdata, @ld[4]);
		}elsif($Graph == 5){
			$title = "総ミサイル発射数${title}";
			push(@tdata, int(@ld[5]/10));
		}elsif($Graph == 6){
			$title = "総農場${title}";
			push(@tdata, int(@ld[6]/10));
		}elsif($Graph == 7){
			$title = "総商業${title}";
			push(@tdata, int(@ld[7]/10));
		}elsif($Graph == 8){
			$title = "総工業${title}";
			push(@tdata, int(@ld[8]/10));
		}elsif($Graph == 9){
			$title = "総養殖${title}";
			push(@tdata, int(@ld[9]/10));
		}elsif($Graph == 10){
			$title = "総森林${title}";
			push(@tdata, int(@ld[10]/10));
		}elsif($Graph == 31){
			$title = "総人口${title}";
			push(@tdata, int(@ld[1]/5));
		}elsif($Graph == 32){
			$title = "総資金${title}";
			push(@tdata, int(@ld[2]/50));
		}elsif($Graph == 33){
			$title = "総面積${title}";
			push(@tdata, int(@ld[3]*10));
		}elsif($Graph == 34){
			$title = "総預金${title}";
			push(@tdata, int(@ld[4]*10));
		}elsif($Graph == 35){
			$title = "総ミサイル発射数${title}";
			push(@tdata, int(@ld[5]));
		}elsif($Graph == 36){
			$title = "総農場${title}";
			push(@tdata, int(@ld[6]));
		}elsif($Graph == 37){
			$title = "総商業${title}";
			push(@tdata, int(@ld[7]));
		}elsif($Graph == 38){
			$title = "総工業${title}";
			push(@tdata, int(@ld[8]));
		}elsif($Graph == 39){
			$title = "総養殖${title}";
			push(@tdata, int(@ld[9]));
		}elsif($Graph == 40){
			$title = "総森林${title}";
			push(@tdata, int(@ld[10]));
		}

		my $allPop = (@ld[1] eq '') ? "　" : "@ld[1]百人";
		my $allMoney = (@ld[2] eq '') ? "　" : "@ld[2]億円";
		my $allArea = (@ld[3] eq '') ? "　" : "@ld[3]百万坪";
		my $allBank = (@ld[4] eq '') ? "　" : "@ld[4]千億";
		my $allMissileA = (@ld[5] eq '') ? "　" : "@ld[5]発";
		my $allFarm		= (@ld[6] eq '') ? "　" : "@ld[6]千規模";
		my $allTower	= (@ld[7] eq '') ? "　" : "@ld[7]千規模";
		my $allIndustry = (@ld[8] eq '') ? "　" : "@ld[8]千規模";
		my $allYousyoku= (@ld[9] eq '') ? "　" : "@ld[9]百匹";
		my $allForest  = (@ld[10] eq '') ? "　" : "@ld[10]百本";
		my $islandNumber = (@ld[11] eq '') ? "　" : "@ld[11]$AfterName";
	print(<<END);
<TR>
<TD>${HtagNumber_}@ld[0]${H_tagNumber}</TD>
<TD align=right>$allPop</TD>
<TD align=right>$allMoney</TD>
<TD align=right>$allArea</TD>
<TD align=right>$allBank</TD>
<TD align=right>$allMissileA</TD>
<TD align=right>$allFarm</TD>
<TD align=right>$allTower</TD>
<TD align=right>$allIndustry</TD>
<TD align=right>$allYousyoku</TD>
<TD align=right>$allForest</TD>
<TD align=right>$islandNumber</TD></TR>
END
	}
	print(<<END);
</TABLE><a name="graph"></a><HR>
棒グラフ表示[全島]
<A HREF="history.cgi?statistical=1#graph">[総人口]</A>
<A HREF="history.cgi?statistical=2#graph">[総資金]</A>
<A HREF="history.cgi?statistical=3#graph">[総面積]</A>
<A HREF="history.cgi?statistical=4#graph">[総預金]</A>
<A HREF="history.cgi?statistical=5#graph">[総ミサイル発射数]</A>
<A HREF="history.cgi?statistical=6#graph">[総農場]</A>
<A HREF="history.cgi?statistical=7#graph">[総商業]</A>
<A HREF="history.cgi?statistical=8#graph">[総工業]</A>
<A HREF="history.cgi?statistical=9#graph">[総養殖]</A>
<A HREF="history.cgi?statistical=10#graph">[総森林]</A><HR>
棒グラフ表示[１島]
<A HREF="history.cgi?statistical=31#graph">[総人口]</A>
<A HREF="history.cgi?statistical=32#graph">[総資金]</A>
<A HREF="history.cgi?statistical=33#graph">[総面積]</A>
<A HREF="history.cgi?statistical=34#graph">[総預金]</A>
<A HREF="history.cgi?statistical=35#graph">[総ミサイル発射数]</A>
<A HREF="history.cgi?statistical=36#graph">[総農場]</A>
<A HREF="history.cgi?statistical=37#graph">[総商業]</A>
<A HREF="history.cgi?statistical=38#graph">[総工業]</A>
<A HREF="history.cgi?statistical=39#graph">[総養殖]</A>
<A HREF="history.cgi?statistical=40#graph">[総森林]</A><HR>
END
	if(($Graph != 0) && ($Graph != 30)) {
		print("<h2>$title</h2>\n");
		print("<TABLE><TR>\n");
		my($d,$w);
		foreach $d(@tdata){
			$w = int($d / 10);
			print("<td valign=bottom align=center><br><img src=\"${gimage}\" width=10 height=$w></td>\n");
		}
		print("</TABLE><BR><BR>\n");
	}
}
#---------------------------------------------------------------------
#	島の近況のリンク
#---------------------------------------------------------------------
# ヘッダ
sub tempIslandHeader {
	my($id, $name) = @_;
	if(&checkPassword($Hislands[$HidToNumber{$id}], $HinputPassword) && ($HcurrentID eq $defaultID)) {
		print("<HR><span class=lbbsOW><B>[${name}の近況]</B></span>");
	} else {
		print("<HR><B>[${name}の近況]</B>　");
	}
	if($HinputPassword eq '') {
		print("<A HREF='history.cgi?ID=${id}&Event=99'>[ALL]</A>");
	} else {
		print("<A HREF='history.cgi?ID=${id}&PASSWORD=${HinputPassword}&Event=99'>[ALL]</A> ");
	}
	my($i, $turn);
	for($i = 0;$i < $HtopLogTurn;$i++) {
		$turn = $HislandTurn - $i;
		return unless($turn > 0);
		if($HinputPassword eq '') {
			print("<A HREF='history.cgi?ID=${id}&Event=${i}'>");
		} else {
			print("<A HREF='history.cgi?ID=${id}&PASSWORD=${HinputPassword}&Event=${i}'>");
		}
		if($i == 0) {
			print("[ターン${turn}(現在)]");
		} else {
			print("[${turn}]");
		}
		print("</A>\n");
	}
	print("<br>\n");
}
#---------------------------------------------------------------------
#	ターン差命令
#---------------------------------------------------------------------
sub tempCommandLate {
	my($i, $turn, $turn2, $id, $kind, $target, $x, $y, $arg, $x2, $y2, $name, $tName);
	print("<H1>ターン差命令一覧 ${HislandTurn}ターン</H1>");
	if($HcomLateCt <= 0){
		print("現在、ターン差命令はありません。");
		return;
	}
	print("<TABLE border=1><TR><TH $HbgTitleCell>攻撃ターン</TH><TH $HbgTitleCell>登録ターン</TH><TH $HbgTitleCell>実行${AfterName}</TH><TH $HbgTitleCell>命令</TH><TH $HbgTitleCell>目標${AfterName}</TH><TH $HbgTitleCell>座標X</TH><TH $HbgTitleCell>座標Y</TH><TH $HbgTitleCell>数量</TH><TH $HbgTitleCell>座標2X</TH><TH $HbgTitleCell>座標2Y</TH></TR>");
	for($i = $#HcomL; $i >= 0; $i--){
		$turn	= $HcomL[$i]->{turn};
		$turn2	= $HcomL[$i]->{turn2};
		$id		= $HcomL[$i]->{id};
		$kind	= $HcomL[$i]->{kind};
		$target	= $HcomL[$i]->{target};
		$x		= $HcomL[$i]->{x};
		$y		= $HcomL[$i]->{y};
		$arg	= $HcomL[$i]->{arg};
		$x2		= $HcomL[$i]->{x2};
		$y2		= $HcomL[$i]->{y2};
		my($tn,$tIsland);
		$tn = $HidToNumber{$id};
		if($tn ne ''){
			$tIsland = $Hislands[$tn];
			$name = $tIsland->{'name'} . ${AfterName};
		}else{
			$name = "　";
		}
		$tn = $HidToNumber{$target};
		if($tn ne ''){
			$tIsland = $Hislands[$tn];
			$tName = $tIsland->{'name'} . ${AfterName};
		}else{
			$tName = "　";
		}
		print("<TR><TD>$turn</TD><TD>$turn2</TD><TD>$name</TD><TD>$HcomName[$kind]</TD><TD>$tName</TD><TD>$x</TD><TD>$y</TD><TD>$arg</TD><TD>$x2</TD><TD>$y2</TD></TR>");
	}
	print("</TABLE>\n");
	print("※　${AfterName}名が表示されてない命令は、放棄等のために実行されません。<BR><BR>\n");
}
#---------------------------------------------------------------------
#	陣営履歴
#---------------------------------------------------------------------
sub tempAlly {
	my($logturn,$i);
	$allyturn = 'log' if($allyturn == 0);
	print("<H1>陣営の履歴</H1>");
	unless(($Hallyflg) && (open(LIN, "${HlogdirName}/ally.$allyturn"))){
		print("陣営の過去データが、ありません。");
		return;
	}
	print(<<END);
<TABLE BORDER><TR>
<TH $HbgTitleCell>${HtagTH_}ターン${H_tagTH}</TH>
<TH $HbgTitleCell colspan=100>${HtagTH_}占　有　率${H_tagTH}</TH>
</TR>
END
	my($turn, $line, @ally, $apop);
	my(%allyCount,%allyPop,%allyArea,%allyGnp,%allyPow,$amark);
	$turn = 0;
	while($line = <LIN>){
		# ターン,陣営ID,島数,総人口,総領土,総経済力,総軍事力
		@ally = split(/,/, $line);
		chomp $ally[7];
		$apop = int($ally[7]);
		if($turn != $ally[0]){
			print("</TR>") if($turn != 0);
			$turn = $ally[0];
			print("<TR><TD $HbgNumberCell>${HtagNumber_}$turn${H_tagNumber}</TD>");
			$apop++;
		}
		if($ally[1] == 0){
			print("<TD $HbgNameCell colspan=$apop>$Hallygroup[$ally[1]]　($ally[7]%)</TD>");
		}else{
			print("<TD $HbgNameCell colspan=$apop>$Hallymark[$ally[1]]${HtagTH_}$Hallygroup[$ally[1]]${H_tagTH}　 ($ally[7]%)</TD>");
		}
	}
	close(LIN);
	print("</TR></TABLE>");
	print("※　占有率は、人口から算出されます。<br><br>");
	print("過去のデータ　<A HREF=\"history.cgi?ally=0\">[最新]</a> ");
	$logturn = $HislandTurn - $HturnPrizeVarious - ($HislandTurn % $HturnPrizeVarious);
	for($i = 0;$i < 5;$i++){
		return if($logturn <= 0);
		print("<A HREF=\"history.cgi?ally=$logturn\">[$logturn]</a> ");
		$logturn -= $HturnPrizeVarious;
	}
}
#---------------------------------------------------------------------
#	ログファイルタイトル
#---------------------------------------------------------------------
sub logDekigoto {
	print(<<END);
<H1>最近の出来事</H1>
END
}
#---------------------------------------------------------------------
#	ログファイル全て表示
#---------------------------------------------------------------------
sub logFilePrintAll {
	my($i);
	for($i = 0; $i < $HtopLogTurn; $i++) {
		&logFilePrint($i, 0, 0);
	}
}
#---------------------------------------------------------------------
# 個別ログ表示
#---------------------------------------------------------------------
sub logPrintLocal {
	my($mode) = @_;
	my($i);
	for($i = 0; $i < $HtopLogTurn; $i++) {
		&logFilePrint($i, $HcurrentID, $mode);
	}
}
#---------------------------------------------------------------------
#	ファイル番号指定でログ表示
#---------------------------------------------------------------------
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
			print("<NOBR><B>=====[<span class=number><FONT SIZE=4> ターン$turn </FONT></span>]================================================</B><NOBR><BR>\n");
			$set_turn++;
		}

		# 表示
		print("<NOBR>　${m}${message}</NOBR><BR>\n");
	}
	close(LIN);
}
