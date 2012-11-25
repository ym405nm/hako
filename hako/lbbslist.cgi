#!/usr/local/bin/perl --

#---------------------------------------------------------------------
#
#	究想の箱庭　ローカル掲示板を一覧表示
#
#	作成日 : 2001/10/06 V0.10
#	作成者 : ラスティア
#
#	管理者が島民の発言を逃さないよう一覧で確認するためのものです。
#	lbbslist.cgi?pass=マスタパス　でアクセスすると極秘通信も見れます。
#	lbbslist.cgi?id=島のＩＤ　でアクセスすると入力欄が現れます。
#
#	修正履歴
#	2001/10/20 V0.20 最近の発言を色を変えて表示できるようにした。
#	2001/12/31 V0.30 共通設定部をconfig.cgiから取り込むようにした。
#	2002/01/13 V0.31 version4対応
#	2002/02/03 V0.40 CSSを別ファイルから読み込むようにした。
#	2002/04/17 V0.41 負荷表示をつけた。スクリプトを全体的に見直し。
#	2002/07/27 V0.50 極秘通信に対応。見た目の改善等。
#	2002/10/28 V0.60 スタイルシート辺りを改良
#	2003/08/20 V0.70 究想の箱庭５仕様に修正。
#	2003/09/15 V0.80 管理者モードのときに投稿欄も付加。
#	2003/09/20 V0.81 各島の個別設定を表示。
#	2004/02/18 V0.90 id=島のＩＤで開くと投稿欄を表示。
#	2005/02/12 V0.91 ShibaAniさんの改造の取り込み(主にデザイン部分の修正)
#	2005/11/05 V0.92 パスワードサニタイズ漏れの対応
#---------------------------------------------------------------------
#	当スクリプトは以下を元に作成しました
#
#	怪獣撃退ポイント＋獲得賞金　ランキング表示
#	作成者 : Watson
#---------------------------------------------------------------------

#---------------------------------------------------------------------
#	初期設定
#---------------------------------------------------------------------
require './hako-init.cgi';
require './hako-io.cgi';

# 画面の「戻る」リンク先(URL) $HbaseDirはhako-init.cgiで指定。
$bye = "$HbaseDir/hako-main.cgi";

# 色を変えて表示するターン
$kyoutyouturn = 30;

# 各島の個別設定を表示(0:しない/1:する)
$viewOrder = 1;

#----------------------------
#	HTMLに関する設定
#----------------------------
# ブラウザのタイトルバーの名称
$title = '観光者通信一覧';

# 冒頭のメッセージ(HTML書式)
$headKill = <<'EOF';
<h2 class=head2>箱庭諸島 観光者通信一覧表</h2>
EOF

$HbgTitleCell   = 'class=TitleCell';
$HbgSubTCell    = 'class=SubTCell';
$HbgLbbsCell    = 'class=LbbsCell';
$HbgCommentCell = 'class=TitleCell';

# コメント文字
$HtagCo_ = '<span class="head">';
$H_tagCo = '</span>';

# ローカル掲示板、観光者の書いた文字
$HtagLbbsSS_ = '<span class="lbbsSS">';
$H_tagLbbsSS = '</span>';

# ローカル掲示板、島主の書いた文字
$HtagLbbsOW_ = '<span class="lbbsOW">';
$H_tagLbbsOW = '</span>';

# 順位の番号など
$HtagNumber_ = '<span class="number">';
$H_tagNumber = '</span>';

#ここまで-------------------------------------------------------------

&cgiInput;
&htmlHeader;

if(!(&readIslandsFile)){
	&htmlError;
} else {
	out($headKill);
	out("<CENTER><TABLE BORDER>");
	for($i = 0; $i < $HislandNumber; $i++) {
		&tempLbbsContents($i,0);
	}
	&tempLbbsContents(0,3);
	&tempLbbsContents(0,4);
	out("</TABLE></CENTER>");

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
	my($i, $id);
	for($i = 0; $i < $HislandNumber; $i++) {
		$Hislands[$i] = &readIsland();
		$HidToNumber{$Hislands[$i]->{'id'}} = $i;
	}
	# ファイルを閉じる
	close(IN);
	readsubmap(0);#宇宙マップ読込
	readsubmap(1);#海域マップ読込
	return 1;
}

#---------------------------------------------------------------------
#	関数名 : readIsland
#	機　能 : 各島のデータを取得
#	引　数 : なし
#	戻り値 : 島のデータ
#---------------------------------------------------------------------
sub readIsland {
	my($id, $name, $comment, @comments,$order, $i, $line, @lbbs);
	$name = <IN>;
	$name =~ /(.*),(.*)/;	# 島の名前
	$name = $1;
	$id = int(<IN>); # ID番号
		<IN>;  # オーナ名
		<IN>;  # 受賞
		<IN>;  # 連続資金繰り数
	$comment = <IN>;       # コメント
	chomp($comment);
	my @comments = split(/<>/, $comment);
	# ファイルポインタを進めるだけなのでname,ID以外は値を格納しない
	for($i = 6; $i < 27; $i++) {
		<IN>;
	}
	$order = <IN>;# 命令
	for($i = 28; $i < 35; $i++) {
		<IN>;
	}
	if(!open(IIN, "${HdirName}/island.$id")) {
		rename("${HdirName}/islandtmp.$id", "${HdirName}/island.$id");
		exit(0) if(!open(IIN, "${HdirName}/island.$id"));
	}
	for($i = 0; $i < $HislandSize; $i++) {
		$line = <IIN>;
	}
	for($i = 0; $i < $HugMax; $i++) {
		$line = <IIN>;
	}
	<IIN>;
	<IIN>;
	<IIN>;
	<IIN>;
	<IIN>;
	for($i = 0; $i < $HcommandMax; $i++) {
		$line = <IIN>;
	}

	# ローカル掲示板
	for($i = 0; $i < $HlbbsMax; $i++) {
		$line = <IIN>;
		chomp($line);
		$lbbs[$i] = $line;
	}

	close(IIN);

	return {
	'name' => $name,
	'id' => $id,
	'comment' => $comments[0],
	'order' => $order,
	'lbbs' => \@lbbs
	};
}
#---------------------------------------------------------------------
#	関数名 : readsubmap
#	機　能 : サブマップのデータを取得
#	引　数 : 0 - 宇宙マップ
#			 1 - 海域マップ
#	戻り値 : 島のデータ
#---------------------------------------------------------------------
# サブマップひとつ読みこみ
sub readsubmap {
	my($num) = @_;
	# 宇宙、海域マップ読みこみ
	if(open(IIN, "${HdirName}/submap.$num")){
		my($i, $line, @lbbs);
		if($num == 0){
			#宇宙
			for($i = 0; $i < $HislandSize; $i++) {
				$line = <IIN>;
			}
		}else{
			#海域
			for($i = 0; $i < $HoceanSize; $i++) {
				$line = <IIN>;
			}
		}
		<IIN>;
		<IIN>;
		<IIN>;
		<IIN>;
		<IIN>;
		<IIN>;
		<IIN>;
		<IIN>;
		<IIN>;
		<IIN>;
		<IIN>;
		<IIN>;
		# ローカル掲示板
		for($i = 0; $i < $HlbbsMax; $i++) {
			$line = <IIN>;
			chomp($line);
			$lbbs[$i] = $line;
		}
		if($num == 0){
			#宇宙
			$Hspace = {'lbbs' => \@lbbs};
		}else{
			#海域
			$Hocean = {'lbbs' => \@lbbs};
		}
		close(IIN);
	}
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
#--------------------------------------------------------------------
#	POST or GETで入力されたデータ取得
#--------------------------------------------------------------------
sub cgiInput {
	my($line, $getLine);

	# 入力を受け取って日本語コードをEUCに
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$line = jcode::euc($line);
	$line =~ s/[\,\r]//g;

	# GETのやつも受け取る
	$getLine = $ENV{'QUERY_STRING'};

	if($getLine =~ /pass=([^\&]*)/) {
		# 最初の起動
		$HdefaultPassword = $1;
		$HdecodePassword = crypt($HdefaultPassword, 'ma')
	}
	if($getLine =~ /id=([^\&]*)/) {
		$HcurrentID = $1;
	}
	if (-e $HpasswordFile) {
		# パスワードファイルがある
		open(PIN, "<$HpasswordFile") || die $!;
		chomp($HmasterPassword = <PIN>); # マスタパスワードを読み込む
		close(PIN);
	}
}
#---------------------------------------------------------------------
#	関数名 : htmlHeader
#	機　能 : HTMLのヘッダ部分を出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlHeader {
	print qq{Content-type: text/html; charset=Shift_JIS\n\n};
	print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
	my($skinName) = "";
	my($cookie) = jcode::euc($ENV{'HTTP_COOKIE'});
	if($cookie =~ /${HthisFile}SKIN=\(([^\)]*)\)/) {
		$skinName = $1;
	}
	$skinName = ($skinName ne '') ? "$skinName" : "$HcssFile";
	out(<<END);
<HTML><HEAD><TITLE>$title</TITLE>
<BASE HREF="$imageDir/">
<link rel="stylesheet" type="text/css" href="$skinName">
</HEAD>
<DIV ID='BodySpecial'><DIV ID='LinkHead'></DIV><DIV ID='LinkTop'>
<BODY>
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
	my($orderTxt) = "";
	if($viewOrder){
		$orderTxt = "<br>□や■の意味は・・・島ごとの固有設定状態だったりします。詳細秘密です。";
	}
	out(<<END);
<P>${AfterName}の名前をクリックすると、観光することができます。$orderTxt</P>
<DIV align="right">
<SMALL>CPU($cpu) : user($uti) system($sti)</SMALL>
</DIV></DIV></BODY></HTML>
END
}
#---------------------------------------------------------------------
#	関数名 : htmlError
#	機　能 : HTMLのエラーメッセージの出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlError{
	out("${h2}エラーが発生しました</H2>\n");
}
#---------------------------------------------------------------------
#	関数名 : tempLbbsContents
#	機　能 : ローカル掲示板内容
#	引　数 : 島のID、モード(3宇宙、4海域)
#	戻り値 : なし
#---------------------------------------------------------------------
sub tempLbbsContents {
	my($number,$mode) = @_;
	$HislandList = getIslandList($HcurrentID);
	my($island,$id,$name,$link,$lbbs,$comment,$line,@ccbx);
	if($mode == 3){
		# 宇宙マップ
		$island = $Hspace;
		$name = "宇宙マップ";
		$link = "space=0";
		$comment = "";
		$id = "999";
	}elsif($mode == 4){
		# 海域マップ
		$island = $Hocean;
		$name = "海域マップ";
		$link = "Ocean=0";
		$comment = "";
		$id = "888";
	}else{
		$island = $Hislands[$number];
		$name = $island->{'name'} . $AfterName;
		$link = "Sight=" . $island->{'id'};
		$comment = $island->{'comment'};
		my($i);
		for($i = 0; $i < 12; $i++) {
			if($island->{'order'} & 2 ** $i){
				$ccbx[$i] = "■";
			}else{
				$ccbx[$i] = "□";
			}
		}
		$id = $island->{'id'};
	}
	$lbbs = $island->{'lbbs'};
	$comment = "　" if($comment eq '');
	my($owner) = 0;
	if($HdecodePassword eq $HmasterPassword) {
		# 極秘も表示
		$owner = 1;
	}
	if($viewOrder){
		$order = "${ccbx[4]}${ccbx[5]}${ccbx[7]}${ccbx[11]}${ccbx[3]}${ccbx[8]}${ccbx[6]}${ccbx[9]}${ccbx[10]}";
	}
	out(<<END);
<TR><TD $HbgTitleCell><a name=$id><b>島名</b></a></TD>
<TD $HbgTitleCell>
<A HREF="$HthisFile?${link}" TARGET=_blank>
<b>$name</b></A>$order
</TD></TR>
<TR><TD $HbgTitleCell><b>コメント</b></TD>
<TD $HbgTitleCell>${HtagCo_}$comment${H_tagCo}
</TD></TR>
END
	out(<<END) if($owner || $HcurrentID);
<TR>
<TD $HbgTitleCell><b>投稿</b></TD>
<TD $HbgTitleCell>
<FORM action="$HthisFile" method="POST">
名前:<INPUT TYPE="text" SIZE=12 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName">
<SELECT NAME="ISLANDID">$HislandList</SELECT>
内容:<INPUT TYPE="text" SIZE=40 NAME="LBBSMESSAGE">
<INPUT TYPE="hidden" NAME="LBBSLIST" VALUE="lbbslist">
パス:<INPUT TYPE="password" SIZE=4 MAXLENGTH=16 NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}">
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="PUBLIC" CHECKED>公開
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="SECRET"><span class='lbbsST'>極秘</span>
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonFO$id">
</TD>
</TR>
</FORM>
END
	my($i);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$line = $lbbs->[$i];
		if($line =~ /([0-9]*)\<(.*)\<([0-9]*)\>(.*)\>(.*)$/) {
			my($j) = $i + 1;
			out("<TR><TD $HbgSubTCell align=center>$HtagNumber_$j$H_tagNumber</TD>");
			my($speaker,$CellColor);
			my($bbs1,$bbs2,$bbs3,$bbs4,$bbs5) = ($1,$2,$3,$4,$5);
			$bbs4 =~ /([0-9]*)/;
			if($1 >= $HislandTurn - $kyoutyouturn) {
				$CellColor = $HbgCommentCell;
			} else {
				$CellColor = $HbgLbbsCell;
			}
			if($bbs3 == 0){
				my($sName, $sID) = split(/,/, $bbs2);
				$sNo = $HidToNumber{$sID};
				if($sName ne ''){
					if(defined $sNo){
						$speaker = "<span class='lbbsST'><B><SMALL>(<A HREF=\"${HbaseDir}/hako-main.cgi?Sight=$sID\" class=\"M\">$sName</A>)</SMALL></B></span>";
					} else {
						$speaker = "<span class='lbbsST'><B><SMALL>($sName)</SMALL></B></span>";
					}
				}
				# 観光者
				if ($bbs1 == 0) {
					# 公開
					out("<TD $CellColor>$HtagLbbsSS_$bbs4 > $bbs5$H_tagLbbsSS $speaker</TD></TR>");
				} else {
					# 極秘
					if ($owner) {
						# オーナー
						out("<TD $CellColor>$HtagLbbsSS_$bbs4 >(秘) $bbs5$H_tagLbbsSS $speaker</TD></TR>");
					} else {
						# 観光客
						out("<TD $CellColor><CENTER><span class='lbbsST'>- 極秘 -</span></CENTER></TD></TR>");
					}
				}
			} else {
				# 島主
				$speaker = "<span class='lbbsST'><B><SMALL>$bbs2</SMALL></B></span>" if($bbs2 ne '');
				out("<TD $CellColor>$HtagLbbsOW_$bbs4 > $bbs5$H_tagLbbsOW $speaker</TD></TR>");
			}
		}
	}
	out(<<END);
</TD></TR>
END
	out("<TR></TR><TR></TR>");
}

