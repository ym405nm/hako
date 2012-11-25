#!/usr/local/bin/perl --

#---------------------------------------------------------------------
#
#	怪獣撃退ポイント＋獲得賞金　ランキング表示
#
#	作成日 : 2001/02/27
#	作成者 : Watson <watson@catnip.freemail.ne.jp>
#
#	タブ幅 : 4
#
#	究想の箱庭5.17用に独自拡張してあります。
#---------------------------------------------------------------------

#---------------------------------------------------------------------
#	初期設定
#---------------------------------------------------------------------
require './hako-init.cgi';
require './init-game.cgi';

# gzipを使用して圧縮伝送する？ 0 : 未使用  1 : 使用
$ gzip = 0;

# gzipのインストール先
$pathGzip = '/usr/bin';

# 画面の「戻る」リンク先(URL)
$bye = $HthisFile;

# ランキングデータの取得開始ターン
$start_turn = 1;

# 他の島の怪獣を倒した場合のポイント加算率
$ExternalRate  = 0.5; # 半分

# ミサイルで船を倒した場合のポイント加算率
$ExternalSRate  = 0.5; # 半分

#----------------------------
#	HTMLに関する設定
#----------------------------
# ブラウザのタイトルバーの名称
$title = '箱庭諸島 ランキング';

# 画面の色や背景の設定(HTML)
$body = '<body>';

# 冒頭のメッセージ(HTML書式)	 怪獣撃退ランキング用
$headKill = <<'EOF';
<h2 class=head2>怪獣撃退ランキング</h2>
EOF

# 冒頭のメッセージ(HTML書式)	 賞金ランキング用
$headMoney = <<'EOF';
<h2 class=head2>賞金ランキング</h2>
EOF

# 冒頭のメッセージ(HTML書式)	 部門賞ランキング用
$headBumon = <<'EOF';
<h2 class=head2>部門賞ランキング</h2>
EOF

# 冒頭のメッセージ(HTML書式)	 船撃沈ランキング用
$headShip = <<'EOF';
<h2 class=head2>船撃沈ランキング</h2>
EOF

$headPointCellcolor	= 'class=headPointCellcolor';    # 表の一番上のポイント部分のセル色
$headNameCellcolor	= 'class=headNameCellcolor';     # その下の怪獣が表示されている部分のセル色
$pointCellcolor		= 'class=pointCellcolor';        # ポイント部分のセル色
$nameCellcolor		= 'class=nameCellcolor';         # 島名の表示部分のセル色
$TotalPointColor	= 'class=TotalPointColor';       # トータルポイントの文字色
$PointColor			= 'class=PointColor';            # 個別のポイントの文字色
$ExternalPointColor	= 'class=ExternalPointColor';    # 他の島の怪獣を倒した場合の文字色

#ここまで-------------------------------------------------------------

splice(@HmonsterName,32,0,'究想いのら');
splice(@HmonsterImage,32,0,'kinora.gif');

# 怪獣撃退時ポイント
                   # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36
@HmonsterPoint   = ( 5, 3, 3, 4, 4, 4, 5, 7, 6, 6, 9, 5,12,16,18, 6, 4,10,15,10,14,13, 5,12, 5, 5,10, 2, 4, 4,14,40,30,15,17,16,20);

splice(@HshipImage,15,1,'ship163.gif');

# 船撃沈時ポイント
#               賊 獣 イ 探 　 　 霊 宝 漁 漁 漁 竜 流 夫 客 風
@HshipPoint  = ( 6, 3, 6, 3,10,10,11, 5, 2, 3, 4,10, 4, 5, 4, 4);

# 船の数
$HshipNumber = 16;

&htmlHeader;

if(!(&readIslandsFile)){
	out("<h2 class=head2>エラーが発生しました</h2>\n");
} else {
	if(!(&calcKillPoint)){
		out("<H3>まだ怪獣撃退ランキングデータがありません。</H3>\n");
	}else{
		&htmlKillMonster;
		out("<p align=right><span $ExternalPointColor>(　)</span>内は他の島の怪獣を倒した数を表しています。ポイントは自分の島の怪獣を倒したものの半分が加算されます。<BR>STミサイルで倒した怪獣は加算されません。</p>");
	}
	if(!(&calcMoney)){
		out("<H3>まだ賞金ランキングデータがありません。</H3>\n");
	}else{
		&htmlMoney;
		out("<p align=right>埋蔵金等には金鉱脈の収入も含まれます、温泉等には、油田(資金生産時のみ)、精製場の収入も含まれます。</p>");
	}
	if(!(&calcBumon)){
		out("<H3>まだ部門賞ランキングデータがありません。</H3>\n");
	}else{
		&htmlBumon;
		out("<BR><BR>");
	}
	if(!(&calcShip)){
		out("<H3>まだ船撃沈ランキングデータがありません。</H3>\n");
	}else{
		&htmlShip;
		out("<p align=right><span $ExternalPointColor>(　)</span>内はミサイルで撃沈させた数を表しています。ポイントは船系で船系を撃沈させたものの半分が加算されます。<BR>STミサイルで撃沈させた船系は加算されません。</p>");
		out("<BR><BR>");
	}
}
&htmlFooter;
#終了
exit(0);

#サブルーチン---------------------------------------------------------
#---------------------------------------------------------------------
#	関数名 : readIslandsFile
#	機　能 : 全島のデータを読み込む
#	引　数 : なし
#	戻り値 : 0 - ファイルオープンに失敗
#	         1 - 成功
#---------------------------------------------------------------------
sub readIslandsFile {
  # データファイルを開く
  if(!open(IN, "${HdirName}/hakojima.dat")) {
	rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
	return 0 if(!open(IN, "${HdirName}/hakojima.dat"));
  }

  # 各パラメータの読みこみ
  $HislandTurn	= int(<IN>);	# ターン数
  <IN>;	# 最終更新時間(使用しない値なので読み飛ばす)

  $HislandNumber	= int(<IN>);	# 島の総数
  <IN>;	# 次に割り当てるID(使用しない値なので読み飛ばす)

  # 島の読みこみ
  my($i);
  for($i = 0; $i < $HislandNumber; $i++) {
	$Hislands[$i] = readIsland();
	$HidToNumber{$Hislands[$i]->{'id'}} = $i;
  }

  # ファイルを閉じる
  close(IN);

  return 1;
}

#---------------------------------------------------------------------
#	関数名 : readIsland
#	機　能 : 各島に割り当てられているIDを取得
#	引　数 : 0 .. $HislandNumber
#	戻り値 : 島のID
#---------------------------------------------------------------------
sub readIsland {
  my($id,$name);
  $name = <IN>;
  $name =~ /(.*),(.*)/;	# 島の名前
  $name = $1;
  $id = int(<IN>);# ID番号

  # ファイルポインタを進めるだけなのでname,ID以外は値を格納しない
  <IN>;	# オーナ名
  <IN>;	# 受賞
  <IN>;	# 連続資金繰り数
  <IN>;	# コメント
  <IN>;	# 暗号化パスワード
  <IN>;	# 資金
  <IN>;	# 食料
  <IN>;	# 人口
  <IN>;	# 広さ
  <IN>;	# 農場
  <IN>;	# 天候
  <IN>;	# 工場
  <IN>;	# 港
  <IN>;	# 採掘場;
  <IN>;	# 商業地
  <IN>;	# 養殖場
  my $turnsu   = <IN>; # 繰越を除いたその島のターン数,順位点,開始ターン
  my @hturn = split(/,/, $turnsu);
  <IN>;	# 
  <IN>;	# ミサイル発射可能数
  <IN>;	# 発射ミサイル総数
  <IN>;	# プレゼント
  <IN>;	# 経験獲得数
  <IN>;	# 部門賞
  <IN>;	# 
  <IN>;
  <IN>;
  <IN>;
  <IN>;
  <IN>;
  <IN>;
  <IN>;
  <IN>;
  <IN>;
  return {
	'name' => $name,
	'id' => $id,
	'sturn' => int($hturn[2]),
  };
}


#---------------------------------------------------------------------
#	関数名 : calcKillPoint
#	機　能 : 怪獣撃退ポイントを計算
#	引　数 : なし
#	戻り値 : 0 - ファイルオープンエラー
#	         1 - 成功
#---------------------------------------------------------------------
sub calcKillPoint {
  return 0 if(!open(LIN, "${HlogdirName}/ranking.log"));

  my($turn, $num, $id1, $id2, $monster, $line, $i);
  while($line = <LIN>){
	$line =~ /^([0-9]*),([0-9]*),([0-9]*),(.*)\n/;
	$turn	 = $1;
	$id1	 = $2;
	$id2	 = $3;
	$monster = $4;

	$num = $HidToNumber{$id1};
	next if($num eq '');
	my($island) = $Hislands[$num];
	next if($turn <= $island->{'sturn'});

	$i = 0;
	# 何番目に登録されている怪獣かサーチ
	while($HmonsterName[$i] ne $monster && $i <= $HmonsterNumber){
	  $i++;
	}
	if($id1 ne $id2){
	  #他島の怪獣を撃退
	  $HkillExtPoint[$num][$i]++;
	  $HtotalPoint[$num] += $HmonsterPoint[$i] * $ExternalRate;
	}else{
	  $HkillPoint[$num][$i]++;
	  $HtotalPoint[$num] += $HmonsterPoint[$i];
	}
  }
  close(LIN);

  # ソート
  my @idx = (0..$HislandNumber);
  @idx = sort { $HtotalPoint[$b] <=> $HtotalPoint[$a] || $a <=> $b } @idx;
  @HtotalPoint = @HtotalPoint[@idx];
  @HkillPoint = @HkillPoint[@idx];
  @HkillExtPoint = @HkillExtPoint[@idx];
  @Kisland = @Hislands[@idx];

  return 1;
}
#---------------------------------------------------------------------
#	関数名 : calcMoney
#	機　能 : 獲得賞金の計算
#	引　数 : なし
#	戻り値 : 0 - ファイルオープンエラー
#	         1 - 成功
#---------------------------------------------------------------------
sub calcMoney {
  return 0 if(!open(MIN, "${HlogdirName}/money.log"));
  my($turn, $num, $id, $kind, $money);
  while($line = <MIN>){
	$line =~ /^([0-9]*),([0-9]*),(.*),([0-9]*)\n/;
	$turn  = $1;
	$id    = $2;
	$kind  = $3;
	$money = $4;

	$num = $HidToNumber{$id};
	next if($num eq '');
	my($island) = $Hislands[$num];
	next if($turn <= $island->{'sturn'});
	$HeachMoney[$num]{$kind} += $money;
	$HtotalMoney[$num] += $money;
  }
  close(MIN);
  
  # ソート
  my @idx = (0..$HislandNumber);
  @idx = sort { $HtotalMoney[$b] <=> $HtotalMoney[$a] || $a <=> $b } @idx;
  @HtotalMoney = @HtotalMoney[@idx];
  @HeachMoney  = @HeachMoney[@idx];
  @Misland = @Hislands[@idx];

  return 1;
}
#---------------------------------------------------------------------
#	関数名 : calcBumon
#	機　能 : 部門賞の計算
#	引　数 : なし
#	戻り値 : 0 - ファイルオープンエラー
#	         1 - 成功
#---------------------------------------------------------------------
sub calcBumon {
  return 0 if(!open(MIN, "${HlogdirName}/bumon.log"));
  my($turn, $num, $id, $kind);
  while($line = <MIN>){
	$line =~ /^([0-9]*),([0-9]*),(.*),(.*)\n/;
	$turn  = $1;
	$id    = $2;
	$kind  = $3;

	$num = $HidToNumber{$id};
	next if($num eq '');
	my($island) = $Hislands[$num];
	next if($turn <= $island->{'sturn'});
	$HeachBumon[$num]{$kind}++;
	$HtotalBumon[$num]++;
  }
  close(MIN);
  
  # ソート
  my @idx = (0..$HislandNumber);
  @idx = sort { $HtotalBumon[$b] <=> $HtotalBumon[$a] || $a <=> $b } @idx;
  @HtotalBumon = @HtotalBumon[@idx];
  @HeachBumon  = @HeachBumon[@idx];
  @Bisland = @Hislands[@idx];

  return 1;
}
#---------------------------------------------------------------------
#	関数名 : calcShip
#	機　能 : 船撃沈ポイントを計算
#	引　数 : なし
#	戻り値 : 0 - ファイルオープンエラー
#	         1 - 成功
#---------------------------------------------------------------------
sub calcShip {
  return 0 if(!open(LIN, "${HlogdirName}/ship.log"));

  my($turn, $num, $id1, $id2, $ship, $line, $i);
  while($line = <LIN>){
	$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*)\n/;
	$turn = $1;
	$id1  = $2;
	$id2  = $3;
	$ship = $4;

	$num = $HidToNumber{$id1};
	next if($num eq '');
	my($island) = $Hislands[$num];
	next if($turn <= $island->{'sturn'});

	# 不正な値だったらとりあえず海賊船にしとく
	$ship = 0 if($ship >= $HshipNumber);
	if($id2 == 99){
	  #ミサイルで撃沈
	  $HSkillExtPoint[$num][$ship]++;
	  $HStotalPoint[$num] += $HshipPoint[$ship] * $ExternalSRate;
	}else{
	  $HSkillPoint[$num][$ship]++;
	  $HStotalPoint[$num] += $HshipPoint[$ship];
	}
  }
  close(LIN);

  # ソート
  my @idx = (0..$HislandNumber);
  @idx = sort { $HStotalPoint[$b] <=> $HStotalPoint[$a] || $a <=> $b } @idx;
  @HStotalPoint = @HStotalPoint[@idx];
  @HSkillPoint = @HSkillPoint[@idx];
  @HSkillExtPoint = @HSkillExtPoint[@idx];
  
  @Sisland = @Hislands[@idx];

  return 1;
}
#---------------------------------------------------------------------
#	関数名 : out
#	機　能 : 文字コードをshift jisで標準出力にアウトプット
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub out {
  print STDOUT jcode::sjis($_[0]);
}

#---------------------------------------------------------------------
#	関数名 : htmlHeader
#	機　能 : HTMLのヘッダ部分を出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlHeader {
	if($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/ && $gzip == 1){
		print qq{Content-type: text/html; charset=Shift_JIS\n};
		print qq{Content-encoding: gzip\n\n};
		open(STDOUT,"| $pathGzip/gzip -1 -c");
		print " " x 2048 if($ENV{HTTP_USER_AGENT}=~/MSIE/);
		print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
	}else{
		print qq{Content-type: text/html; charset=Shift_JIS\n\n};
		print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
	}
	my($skinName) = "";
	my($cookie) = jcode::euc($ENV{'HTTP_COOKIE'});
	if($cookie =~ /${HthisFile}SKIN=\(([^\)]*)\)/) {
		$skinName = $1;
	}
	$skinName = ($skinName ne '') ? "$skinName" : "$HcssFile";
	out(<<END);
<HTML><HEAD>
<TITLE>$title</TITLE>
<base href="$imageDir/">
<link rel="stylesheet" type="text/css" href="$skinName">
</HEAD>
<DIV ID='BodySpecial'><DIV ID='LinkHead'></DIV><DIV ID='LinkTop'>
$body
<A HREF="$bye">[戻る]</A></DIV>
END
}
#---------------------------------------------------------------------
#	関数名 : htmlFooter
#	機　能 : HTMLのフッタ部分を出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlFooter {
	my($uti, $sti, $cuti, $csti) = times();
	$uti += $cuti;
	$sti += $csti;
	my($cpu) = $uti + $sti;
	out(<<END);
<P>
どのランキングも一度に複数増える現象がたまに発生しますが、修正は困難な為ランダムでもらえるボーナスだと考えてください。<BR>
$HislandTurnターン時点($start_turnターンからデータを取得)<BR></P><BR>
<DIV align="right"><SMALL>CPU($cpu) : user($uti) system($sti)</SMALL></DIV>
<P><I><A HREF="http://club.www.infoseek.co.jp/club.asp?cid=j1100037">Scripted By Watson</A></I></P>
<P></DIV></DIV>
</BODY></HTML>
END
}
#---------------------------------------------------------------------
#	関数名 : htmlKillMonster
#	機　能 : HTMLの怪獣撃退部分を出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlKillMonster {
  my($i, $j);
  out(<<END);
$headKill
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=100% BGCOLOR="#000000"><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<TR>
<TD $headPointCellcolor NOWRAP>&nbsp;</TD>
<TD $headPointCellcolor NOWRAP>ポイント</TD>
END
  for($i = 1; $i <= $HmonsterNumber; $i++){
	out("<TD $headPointCellcolor NOWRAP>$HmonsterPoint[$i]</TD>\n");
  }
  out("<TD $headPointCellcolor NOWRAP>$HmonsterPoint[0]</TD></TR>\n");
  out("<TR><TD $headNameCellcolor NOWRAP>島の名前</TD>\n");
  out("<TD $headNameCellcolor NOWRAP><span $TotalPointColor>ポイント</span></TD>");
  for($i = 1; $i <= $HmonsterNumber; $i++){
	out("<TD $headNameCellcolor NOWRAP><IMG SRC=\"$HmonsterImage[$i]\" width=24 height=24 ALT=\"$HmonsterName[$i]\" TITLE=\"$HmonsterName[$i]\"></TD>\n");
  }
  
  out("<TD $headNameCellcolor NOWRAP><IMG SRC=\"$HmonsterImage[0]\" width=24 height=24 ALT=\"$HmonsterName[0]\" TITLE=\"$HmonsterName[0]\"></TD></TR>\n");
#ここまでが表のヘッダ部分

  for($i = 0; $i < $HislandNumber; $i++){
	out("<TR><TD $nameCellcolor NOWRAP>$Kisland[$i]->{'name'}島</TD>\n");
	if($HtotalPoint[$i]){
	  # トータルポイントが加算されている場合
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HtotalPoint[$i]</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	for($j = 1; $j <= $HmonsterNumber; $j++){
	  if($HkillExtPoint[$i][$j]){
		# 自分の島の怪獣 ＋ 他の島の怪獣を撃破
		out("<TD $pointCellcolor NOWRAP>$HkillPoint[$i][$j]<span $ExternalPointColor>($HkillExtPoint[$i][$j])</span></TD>\n");
	  } elsif($HkillPoint[$i][$j]){
		# 自分の島の怪獣だけを撃破
		out("<TD $pointCellcolor NOWRAP>$HkillPoint[$i][$j]</TD>\n");
	  } else {
		# なし
		out("<TD></TD>\n");
	  }
	}
	# メカいのら用
	if($HkillExtPoint[$i][0]){
	  # 自分の島の怪獣 ＋ 他の島の怪獣を撃破
	  out("<TD $pointCellcolor NOWRAP>$HkillPoint[$i][0]<span $ExternalPointColor>($HkillExtPoint[$i][0])</span></TD>\n");
	} elsif($HkillPoint[$i][0]){
	  # 自分の島の怪獣だけを撃破
	  out("<TD $pointCellcolor NOWRAP>$HkillPoint[$i][0]</TD>\n");
	} 	else {
	  # なし
	  out("<TD></TD>\n");
	}
	out("</TR>\n");
  }
  out(<<END);
</TABLE>
</TD></TR></TABLE>
END
}
#---------------------------------------------------------------------
#	関数名 : htmlMoney
#	機　能 : HTMLの獲得賞金を出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlMoney {
  my($i);
  out(<<END);
$headMoney
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=100% BGCOLOR="#000000"><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<TR>
<TD $headNameCellcolor NOWRAP>島の名前</TD>
<TD $headNameCellcolor NOWRAP><span $TotalPointColor>総獲得賞金額</span></TD>
<TD $headNameCellcolor NOWRAP>怪獣撃退</TD>
<TD $headNameCellcolor NOWRAP>埋蔵金等</TD>
<TD $headNameCellcolor NOWRAP>温泉等</TD>
<TD $headNameCellcolor NOWRAP>宝船</TD>
<TD $headNameCellcolor NOWRAP>海風船</TD>
<TD $headNameCellcolor NOWRAP>トランプ</TD>
</TR>
END
  for($i = 0; $i < $HislandNumber; $i++){
	out("<TR><TD $nameCellcolor NOWRAP>$Misland[$i]->{'name'}島</TD>\n");
	if($HtotalMoney[$i]){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HtotalMoney[$i]$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	if($HeachMoney[$i]{'怪獣撃破'}){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HeachMoney[$i]{'怪獣撃破'}$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	if($HeachMoney[$i]{'埋蔵金'}){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HeachMoney[$i]{'埋蔵金'}$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	if($HeachMoney[$i]{'温泉'}){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HeachMoney[$i]{'温泉'}$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	if($HeachMoney[$i]{'宝船'}){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HeachMoney[$i]{'宝船'}$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	if($HeachMoney[$i]{'海風船'}){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HeachMoney[$i]{'海風船'}$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	if($HeachMoney[$i]{'トランプ'}){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HeachMoney[$i]{'トランプ'}$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	out("</TR>\n");
  }
  out(<<END);
</TABLE>
</TD></TR></TABLE>
END
}
#---------------------------------------------------------------------
#	関数名 : htmlBumon
#	機　能 : HTMLの部門賞を出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlBumon {
  my($i);
  out(<<END);
$headBumon
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=100% BGCOLOR="#000000"><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<TR>
<TD $headNameCellcolor NOWRAP>島の名前</TD>
<TD $headNameCellcolor NOWRAP><span $TotalPointColor>総部門賞数</span></TD>
END
  for($i = 1; $i <= $HturnPrizeNumber; $i++){
	out("<TD $headNameCellcolor NOWRAP><IMG SRC=\"Vprize${i}.gif\">${HprizeV[$i]}</TD>\n");
  }
  out("</TR>");
  for($i = 0; $i < $HislandNumber; $i++){
	out("<TR><TD $nameCellcolor NOWRAP>$Bisland[$i]->{'name'}島</TD>\n");
	if($HtotalBumon[$i]){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HtotalBumon[$i]</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	for($j = 1; $j <= $HturnPrizeNumber; $j++){
	  my($bumondata) = $HeachBumon[$i]{$HprizeV[$j]};
	  if($bumondata){
		out("<TD $pointCellcolor NOWRAP>$bumondata</TD>\n");
	  } else {
		out("<TD></TD>\n");
	  }
	}
	out("</TR>\n");
  }
  
  out(<<END);
</TABLE>
</TD></TR></TABLE>
END
}
#---------------------------------------------------------------------
#	関数名 : htmlShip
#	機　能 : HTMLの船撃沈部分を出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlShip {
  my($i);
  out(<<END);
$headShip
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=100% BGCOLOR="#000000"><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<TR>
<TD $headPointCellcolor NOWRAP>&nbsp;</TD>
<TD $headPointCellcolor NOWRAP>ポイント</TD>
END
  for($i = 0; $i < $HshipNumber; $i++){
	next if(($i > 3) && ($i < 6));
	out("<TD $headPointCellcolor NOWRAP>$HshipPoint[$i]</TD>\n");
  }
  out("<TR><TD $headNameCellcolor NOWRAP>島の名前</TD>\n");
  out("<TD $headNameCellcolor NOWRAP><span $TotalPointColor>ポイント</span></TD>");
  for($i = 0; $i < $HshipNumber; $i++){
	next if(($i > 3) && ($i < 6));
	out("<TD $headNameCellcolor NOWRAP><IMG SRC=\"$HshipImage[$i]\" ALT=\"$HshipName[$i]\" TITLE=\"$HshipName[$i]\"></TD>\n");
  }
#ここまでが表のヘッダ部分
  for($i = 0; $i < $HislandNumber; $i++){
	out("<TR><TD $nameCellcolor NOWRAP>$Sisland[$i]->{'name'}島</TD>\n");
	if($HStotalPoint[$i]){
	  # トータルポイントが加算されている場合
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HStotalPoint[$i]</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	for($j = 0; $j < $HshipNumber; $j++){
	  next if(($j > 3) && ($j < 6));
	  if($HSkillExtPoint[$i][$j]){
		# 船で撃沈 ＋ ミサイルで撃沈
		out("<TD $pointCellcolor NOWRAP>$HSkillPoint[$i][$j]<span $ExternalPointColor>($HSkillExtPoint[$i][$j])</span></TD>\n");
	  } elsif($HSkillPoint[$i][$j]){
		# 船で撃沈のみ
		out("<TD $pointCellcolor NOWRAP>$HSkillPoint[$i][$j]</TD>\n");
	  } else {
		# なし
		out("<TD></TD>\n");
	  }
	}
	out("</TR>\n");
  }
  out(<<END);
</TABLE>
</TD></TR></TABLE>
END
}

