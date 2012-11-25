#!/usr/local/bin/perl --

#---------------------------------------------------------------------
#
#	究想の箱庭　怪獣バトル用　一覧表示
#
#	作成日 : 2001/09/16 V0.10
#	作成者 : ラスティア
#
#	修正日履歴
#	2001/12/23 V0.11 V3.60での怪獣追加に対応した。
#	2001/12/31 V0.20 共通設定部をconfig.cgiから取り込むようにした。
#	2002/01/13 V0.21 version4対応。
#	2002/02/03 V0.30 CSSを別ファイルから読み込むようにした。
#	2002/03/31 V0.31 負荷軽減と戦闘相手表示。
#	2002/11/02 V0.40 スタイルシート辺りを改良、怪獣追加
#	2003/09/24 V0.50 究想の箱庭５対応。
#---------------------------------------------------------------------
#	当スクリプトは以下を元に作成しました
#
#	怪獣撃退ポイント＋獲得賞金　ランキング表示
#	作成者 : Watson
#---------------------------------------------------------------------

#---------------------------------------------------------------------
#	初期設定
#---------------------------------------------------------------------
# hako-init.cgiをrequire
require './hako-init.cgi';

# 画面の「戻る」リンク先(URL) $HbaseDirはconfig.cgiで指定。
$bye = "$HbaseDir/hako-main.cgi";

# 怪獣の能力を元怪獣能力を含めて表示するときは１ 自能力のみは０
$Monshyouzi = 0;

#----------------------------
#	HTMLに関する設定
#----------------------------
# ブラウザのタイトルバーの名称
$title = '箱庭諸島 怪獣リスト';

# 画面の色や背景の設定(HTML)
$body = '<body>';

# 冒頭のメッセージ(HTML書式)	 怪獣撃退ランキング用
$headKill = <<'EOF';
<h2 class=head2>怪獣バトル　怪獣一覧表</h2>
EOF

$HbgTitleCell = 'class=TitleCell';
$HbgInfoCell = 'class=InfoCell';

#ここまで-------------------------------------------------------------

# 怪獣名
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

# 怪獣バトル用
@HmonsterSP      = ( 7, 4, 1, 7, 7, 3, 2, 7, 6, 0,10, 6, 6, 5, 5, 5, 0, 8, 7, 0, 9, 5, 0, 8, 0, 6, 5, 5, 0, 0,11, 8, 0, 7, 7, 9); # 特殊
                   # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35
@HmonsterSTR     = (10, 7, 7,10, 7, 2, 8,12, 4, 7,13, 3,11, 5, 7, 3, 8,12,15, 9, 9, 9, 7, 5,10,10, 7, 7, 7, 9,11,11, 7, 9,11,11); # 攻撃
@HmonsterDEF     = ( 2, 3, 5, 2, 2, 0, 5, 3, 7, 3, 1, 5, 5, 0, 0, 0, 3, 5, 0, 3, 3, 1, 3, 2, 3, 5, 1, 1, 3, 3, 3, 5, 3, 3, 3, 3); # 防御
@HmonsterAGI     = ( 6, 5, 2, 3, 9,14, 4, 5,11, 5, 5, 1, 2,15,17,19, 6,11, 5, 9,15,20, 5,10,10, 7,15,20, 5, 6, 9,15, 5, 6, 6,14); # 回避
@HmonsterSKL     = ( 2, 7, 6, 5, 9, 9, 7, 4, 7, 7,10, 1, 5,10,13,13, 8,12,12, 9,10,16, 7,10,10, 7,12,10, 7, 7, 9,12, 7, 7, 8,12); # 命中
       #  計(参考)  20 22 20 20 27 25 24 24 29 22 29 10 23 30 37 35 25 40 32 30 37 46 22 27 33 29 35 38 22 25 32 43 22 25 28 40

&htmlHeader;

if(!(&readIslandsFile)){
	&htmlError;
} else {
	out($headKill);
	out("<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100% bgcolor=\"steelblue\">");
	for($i = 0; $i < $HislandNumber; $i++) {
		&monsterlist($i);
	}
	out("</TABLE>");

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
	if(!open(IN, "${HdirName}/hakojima.dat")) {
	  return 0;
	}
  }
  
  # 各パラメータの読みこみ
  $HislandTurn	= int(<IN>);	# ターン数
  
  <IN>;	# 最終更新時間(使用しない値なので読み飛ばす)
  
  $HislandNumber	= int(<IN>);	# 島の総数
  <IN>;	# 次に割り当てるID(使用しない値なので読み飛ばす)
  
  # 島の読みこみ
  my($i, $id);
  for($i = 0; $i < $HislandNumber; $i++) {
	$Hislands[$i] = readIsland($i);
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
	my($num) = @_;

	my($id,$name);

	$name = <IN>;
	$name =~ /(.*),(.*)/;	# 島の名前
	$name = $1;
	$id = int(<IN>);# ID番号

	# ファイルポインタを進めるだけなのでname,ID以外は値を格納しない
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;	# 10
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;	# 20
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;	# 28
	<IN>;
	<IN>;
	<IN>;
	<IN>;
	<IN>;	# 33
	
	# 怪獣バトル用
	$mons1    = <IN>; # 自分の怪獣
	$monsurl  = <IN>; # 怪獣URL
	chomp($monsurl);
	my @monster = split(/,/, $mons1);

  return {
	'name' => $name,
	'id' => $id,
	'monsurl' => $monsurl,
	'monster' => \@monster
  };
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
	print qq{Content-type: text/html; charset=Shift_JIS\n\n};
	print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
	my($skinName) = "";
	my($cookie) = jcode::euc($ENV{'HTTP_COOKIE'});
	if($cookie =~ /${HthisFile}SKIN=\(([^\)]*)\)/) {
		$skinName = $1;
	}
	$skinName = ($skinName ne '') ? "$skinName" : "$HcssFile";
	out(<<END);
<html>
<head>
<title>
$title
</title>
<base href="$imageDir/">
<link rel="stylesheet" type="text/css" href="$skinName">
</head>
<DIV ID='BodySpecial'><DIV ID='LinkHead'></DIV><DIV ID='LinkTop'>
$body
<a href="$bye">[戻る]</a></DIV>
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
<p>
島の名前をクリックすると、観光することができます。 <br>
表示されている怪獣の能力値は怪獣個人の能力です。実際の戦闘には元怪獣の能力が足されます。 <br>
戦闘はランダムな数値がかなり入りますので能力どおりに勝敗が決まるわけではありません。 <br>
</p>
<DIV align="right"><SMALL>CPU($cpu) : user($uti) system($sti)</SMALL></DIV>
</body></html>
END
}
#---------------------------------------------------------------------
#	関数名 : htmlError
#	機　能 : HTMLのエラーメッセージの出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlError{
	out("<h2 class=head2>エラーが発生しました</h2>\n");
}
#---------------------------------------------------------------------
#	関数名 : monsterlist
#	機　能 : 怪獣バトル　怪獣一覧表作成
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub monsterlist {
	my($island) = $Hislands[$_[0]];

	my($id,$name,$monster) = ($island->{'id'},$island->{'name'},$island->{'monster'});
	my($MBsId,$MBmId) = ($monster->[3],$monster->[4]);

	my($tn) = $HidToNumber{$monster->[2]};
	my($tMonster,$tIsland,$tName,$tMBsId, $tMBmId);

	if($tn eq '') {
	} else {
		# 対戦相手がいるとき
		$tIsland = $Hislands[$tn];
		$tName = $tIsland->{'name'};
		$tMonster = $tIsland->{'monster'};
		($tMBsId, $tMBmId) = ($tMonster->[3],$tMonster->[4]);
	}
	my($MBidName);
	if($monster->[0] == 0) {
		return;
	} else {
		my($monsIsland) = $Hislands[$HidToNumber{$monster->[0]}];
		$MBidName = $monsIsland->{'name'};
		
		if($monster->[2] == 0) {
			$MBidName = "自島";
		} else {
			$MBidName = "$MBidName$AfterNameで<br>$tMonster->[1]と<b>戦闘中</b>";;
		}
	}

	# 怪獣画像処理
	my $image = $HmonsterImage[$MBmId];
	my $special = $HmonsterSpecial[$MBmId];
	# 硬化中?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
		(($special == 4) && (($HislandTurn % 2) == 0))) {
		$image = $HmonsterImage2[$MBmId];
	}
	$image = $island->{'monsurl'} if(substr($island->{'monsurl'},0,7) eq 'http://');
	
	my $image2 = $HmonsterImage[$tMBmId];
	$special = $HmonsterSpecial[$tMBmId];
	# 硬化中?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
		(($special == 4) && (($HislandTurn % 2) == 0))) {
		$image2 = $HmonsterImage2[$tMBmId];
	}
	$image2 = $tIsland->{'monsurl'} if(substr($tIsland->{'monsurl'},0,7) eq 'http://');
	
	my($seityou) = $monster->[7] + $monster->[8] + $monster->[9] + $monster->[10];
	my($tseityou) = $tMonster->[7] + $tMonster->[8] + $tMonster->[9] + $tMonster->[10];

	my $mSTR = $HmonsterSTR[$MBmId] + $monster->[7];
	my $mDEF = $HmonsterDEF[$MBmId] + $monster->[8];
	my $mAGI = $HmonsterAGI[$MBmId] + $monster->[9];
	my $mSKL = $HmonsterSKL[$MBmId] + $monster->[10];

	$MBmId = ($MBmId == 0) ? "　" : $HmonsterName[$MBmId];
	$MBsId = ($MBsId == 0) ? "無" : $HmonsterName[$MBsId];
	$tMBmId = ($tMBmId == 0) ? "　" : $HmonsterName[$tMBmId];
	$tMBsId = ($tMBsId == 0) ? "無" : $HmonsterName[$tMBsId];
	
	if($seityou < 12) {
		$seityou = "幼年";
	} elsif($seityou < 25) {
		$seityou = "壮年";
	} else {
		$seityou = "老年";
	}
	if($tseityou < 12) {
		$tseityou = "幼年";
	} elsif($tseityou < 25) {
		$tseityou = "壮年";
	} else {
		$tseityou = "老年";
	}

	out(<<END);

<tr>
<td $HbgTitleCell align=center>島名</td>
<td $HbgTitleCell align=center>怪獣名</td>
<td $HbgTitleCell align=center>外観</td>
<td $HbgTitleCell align=center>元怪獣</td>
<td $HbgTitleCell align=center>勝数</td>
<td $HbgTitleCell align=center>負数</td>
<td $HbgTitleCell align=center>成長</td>
<td $HbgTitleCell align=center>HP</td>
<td $HbgTitleCell align=center>攻撃</td>
<td $HbgTitleCell align=center>守備</td>
<td $HbgTitleCell align=center>回避</td>
<td $HbgTitleCell align=center>命中</td>
<td $HbgTitleCell align=center>状況</td>
<td $HbgTitleCell align=center>餌</td>
</tr>
<tr>
<td $HbgInfoCell>
<A HREF="${HbaseDir}/hako-main.cgi?Sight=${id}" TARGET=_blank>
$name$AfterName
</A></td>
<td $HbgInfoCell>$monster->[1]</td>
<td $HbgInfoCell><IMG SRC=\"$image\" width=32 height=32 BORDER=0></td>
<td $HbgInfoCell>$MBmId</td>
<td $HbgInfoCell align=center>$monster->[12]</td>
<td $HbgInfoCell align=center>$monster->[13]</td>
<td $HbgInfoCell>$seityou</td>
<td $HbgInfoCell align=center>$monster->[5]/$monster->[6]</td>

END
	if($Monshyouzi) { # 怪獣の能力を元怪獣能力を含めて表示
	out(<<END);
<td $HbgInfoCell align=center>$mSTR($monster->[7])</td>
<td $HbgInfoCell align=center>$mDEF($monster->[8])</td>
<td $HbgInfoCell align=center>$mAGI($monster->[9])</td>
<td $HbgInfoCell align=center>$mSKL($monster->[10])</td>
END
	} else { # 怪獣の能力を自分の能力のみ表示
	out(<<END);
<td $HbgInfoCell align=center>$monster->[7]</td>
<td $HbgInfoCell align=center>$monster->[8]</td>
<td $HbgInfoCell align=center>$monster->[9]</td>
<td $HbgInfoCell align=center>$monster->[10]</td>
END
	}
	out(<<END);

<td $HbgInfoCell>$MBidName</td>
<td $HbgInfoCell>$MBsId</td>

</tr>

END
}

