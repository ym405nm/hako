#!/usr/local/bin/perl --

#--------------------------------------------------------------------
# 箱庭諸島 Profiles
#
#	作成日：2001/03/13
#	作成者：Watson <watson@catnip.freemail.ne.jp>
#
#	タブ幅：4
#
#	究想の箱庭用に独自拡張してあります。
#--------------------------------------------------------------------

use Time::Local;

#---------------------------------------------------------------------
#	初期設定
#---------------------------------------------------------------------
# hako-init.cgiをrequire
require './hako-init.cgi';

$Hinit{'thisFile'} = 'profile.cgi';

# gzipの使用  1 : 使用  0 : 未使用
$Hinit{'gzip'} = 0;
# gzipのパス
$Hinit{'gzipPath'} = '/bin';

# HTMLに関する設定
$Hhtml{'body'} = '<body>';
$Hhtml{'title'} = '箱庭諸島 プロフィール';

$Hhtml{'lineColor'}     = 'class=lineColor';
$Hhtml{'tdHeaderColor'} = 'class=tdHeaderColor';
$Hhtml{'cellColor'}     = 'class=cellColor';

# 戻り先
$Hhtml{'bye'} = "$HbaseDir/hako-main.cgi";

#メイン--------------------------------------------------------------
#--------------------------------------------------------------------
&main;
exit(0);

#--------------------------------------------------------------------
#	関数名 : main
#	機  能 : メイン関数
#	引  数 : なし
#	戻り値 : なし
#--------------------------------------------------------------------
sub main {
  &cookieInput;
  &cgiInput;
  &htmlHeader;

  # 島データ取得
  if(!(&readIslandsFile)) {
	&tempNoDataFile;
	&htmlFooter;
	return;
  }

  # IDが設定されていなければプロフィールリストを表示
  if($HidToNumber{$Hinput{'ID'}} eq ''){
	&getProfileLastModify;
	&lastModifySort;
	&htmlProfileList;
	&htmlFooter;
	return;
  }
  # プロフィール書込み (必ず取得する前に)
  if($HmainMode eq 'changeProfile'){
	if(&checkPassword($Hislands[$HidToNumber{$HdefaultID}]->{'password'}, $HinputPassword)){
	  &writeProfileFile;
	} else {
	  &tempWrongPassword;
	  &htmlFooter;
	  return;
	}
  }

  #プロフィール取得
  &readProfileFile;

  if($HmainMode eq 'edit'){
	&htmlEdit; # プロフィール編集
  } else {
	&htmlProfile; # プロフィール表示
  }
  &htmlFooter;

}
#サブルーチン--------------------------------------------------------
#--------------------------------------------------------------------
#	関数名 : checkPassword
#	機  能 : パスワードチェック
#	引  数 : 暗号化されたパスワード、生のパスワード
#	戻り値 : 0 - 照合失敗
#	         1 - 照合成功
#--------------------------------------------------------------------
sub checkPassword {
  my($p1, $p2) = @_;
  if($p1 eq crypt($p2, 'h2')){
	return 1;
  }
  return 0;
}
#--------------------------------------------------------------------
#	関数名 : checkUrl
#	機  能 : 文字列が http:// から始まっているかチェック
#	引  数 : 文字列
#	戻り値 : http:// から始まっていればそのまま文字列を返す
#	         そうでなければ空の文字列
#--------------------------------------------------------------------
sub checkUrl {
  my($url) = @_;
  my($temp) = substr($url,0,7);
  if($temp ne 'http://') {
	return '';
  }else{
	return $url;
  }
}
#--------------------------------------------------------------------
#	関数名 : lastModifySort
#	機  能 : 更新時刻に応じてリストをソート
#	引  数 : なし
#	戻り値 : なし
#--------------------------------------------------------------------
sub lastModifySort {

  # 更新時刻でソート
  my(@idx) = (0..$HislandNumber);
  @idx = sort { $Hislands[$b]->{'lastModify'} <=> $Hislands[$a]->{'lastModify'} || $a <=> $b } @idx;
  @Hislands = @Hislands[@idx];
}
#--------------------------------------------------------------------
#	関数名 : cutColumn
#	機  能 : 文字数を切り詰める
#	引  数 : 文字列、切り詰める数
#	戻り値 : 切り詰めた文字列
#--------------------------------------------------------------------
sub cutColumn {
  my($s, $c) = @_;
  if(length($s) <= $c) {
	return $s;
  } else {
	# 合計80ケタになるまで切り取り
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
#--------------------------------------------------------------------
#	関数名 : cgiInput
#	機  能 : POST or GETで入力されたデータ取得
#	引  数 : なし
#	戻り値 : なし
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

  if($line =~ /changeProfileButton=/) {
	$HmainMode = 'changeProfile';
  }elsif($getLine =~ /mode=edit/){
	$HmainMode = 'edit';
  }

  if($line =~ /PASSWORD=([^\&]*)\&/) {
	$HinputPassword = $1;
  }
  if($line =~ /ADDRESS=([^\&]*)\&/){
	$Hprofile{'address'} = &htmlEscape($1);
  }
  if($line =~ /AGE=([0-9]*)\&/){
	$Hprofile{'age'} = &htmlEscape($1);
  }
  if($line =~ /SEX=([1-3])\&/){
	$Hprofile{'sex'} = $1;
  }
  if($line =~ /JOB=([^\&]*)\&/){
	$Hprofile{'job'} = &htmlEscape($1);
  }
  if($line =~ /EMAIL=([^\&]*)\&/){
	$Hprofile{'email'} = &htmlEscape($1);
  }
  if($line =~ /ICQ=([^\&]*)\&/){
	$Hprofile{'icq'} = &htmlEscape($1);
  }
  if($line =~ /HPTITLE=([^\&]*)\&/){
	$Hprofile{'webTitle'} = &htmlEscape($1);
  }
  if($line =~ /URL=([^\&]*)\&/){
	$Hprofile{'webAddress'} = &checkUrl(&htmlEscape($1));
  }
  if($line =~ /PHOTO=([^\&]*)\&/){
	$Hprofile{'photo'} = &checkUrl(&htmlEscape($1));
  }
  if($line =~ /COMMENT=([^\&]*)\&/){
	$Hprofile{'comment'} = &cutColumn(&htmlEscape($1), 250);
  }
  if($line =~ /BESTWEB1=([^\&]*)\&/){
	$Hprofile{'BestWebsite1'} = &checkUrl(&htmlEscape($1));
  }
  if($line =~ /BESTWEB2=([^\&]*)\&/){
	$Hprofile{'BestWebsite2'} = &checkUrl(&htmlEscape($1));
  }
  if($line =~ /BESTWEB3=([^\&]*)\&/){
	$Hprofile{'BestWebsite3'} = &checkUrl(&htmlEscape($1));
  }
  if($line =~ /HOMEIMAGE=([^\&]*)\&/){
	$Hprofile{'MyHomeImage'} = &checkUrl(&htmlEscape($1));
  }
  if($line =~ /BGIMAGE=([^\&]*)\&/){
	$Hprofile{'BackgroundImage'} = &checkUrl(&htmlEscape($1));
  }
  if($line =~ /BGIMAGEUSE=([1-2])\&/){
	$Hprofile{'BackgroundUse'} = $1;
  }
  if($getLine =~ /profile=([0-9]+)/){
	$Hinput{'ID'} = $1;
  }
}

#--------------------------------------------------------------------
#	関数名 : getProfileLastModify
#	機  能 : プロフィールデータを書込む
#	引  数 : なし
#	戻り値 : なし
#--------------------------------------------------------------------
sub getProfileLastModify {
  my($i, $id);
  for($i = 0; $i < $HislandNumber; $i++) {
	$id = $Hislands[$i]->{'id'};
	if(-e "${HprofileDir}/profile${id}.dat"){
	  open(PIN, "${HprofileDir}/profile${id}.dat");
	  $Hislands[$i]->{'lastModify'} = int(<PIN>);
	  close(PIN);
	} else {
	  $Hislands[$i]->{'lastModify'} = 0;
	}
  }
}
#--------------------------------------------------------------------
#	関数名 : writeProfileFile
#	機  能 : プロフィールデータを書込む
#	引  数 : ID
#	戻り値 : 0 - ファイルオープンに失敗
#	         1 - 成功
#--------------------------------------------------------------------
sub writeProfileFile {
  my($num) = @_;
  mkdir($HprofileDir, $HdirMode) unless(-e "${HprofileDir}");
  open(POUT, "> ${HprofileDir}/profile${Hinput{'ID'}}.dat");
  $ENV{'TZ'} = "JST-9";
  my($writeTime) = time;
  print POUT "$writeTime\n";
  print POUT "$Hprofile{'photo'}\n";
  print POUT "$Hprofile{'address'}\n";
  print POUT "$Hprofile{'age'}\n";
  print POUT "$Hprofile{'sex'}\n";
  print POUT "$Hprofile{'job'}\n";
  print POUT "$Hprofile{'email'}\n";
  print POUT "$Hprofile{'icq'}\n";
  print POUT "$Hprofile{'webTitle'}\n";
  print POUT "$Hprofile{'webAddress'}\n";
  print POUT "$Hprofile{'comment'}\n";
  print POUT "$Hprofile{'BestWebsite1'}\n";
  print POUT "$Hprofile{'BestWebsite2'}\n";
  print POUT "$Hprofile{'BestWebsite3'}\n";
  print POUT "$Hprofile{'MyHomeImage'}\n";
  print POUT "$Hprofile{'BackgroundImage'}\n";
  print POUT "$Hprofile{'BackgroundUse'}\n";
  
  close(POUT);
}
#--------------------------------------------------------------------
#	関数名 : readProfileFile
#	機  能 : プロフィールデータを取得
#	引  数 : なし
#	戻り値 : 0 - ファイルオープンに失敗
#	         1 - 成功
#--------------------------------------------------------------------
sub readProfileFile {
  if(!open(PIN, "${HprofileDir}/profile${Hinput{'ID'}}.dat")){
	return 0;
  }

  my($lastModify, $photo, $address, $age, $sex, $job, $email, $icq, $webtitle, $webaddr, $comment);
  my($bestweb1, $bestweb2, $bestweb3, $HomeImage, $BGImage, $BGImageUse);
  $lastModify = int(<PIN>);
  $photo    = <PIN>;
  $address  = <PIN>;
  $age      = <PIN>;
  $sex      = int(<PIN>);
  $job      = <PIN>;
  $email    = <PIN>;
  $icq      = <PIN>;
  $webtitle = <PIN>;
  $webaddr  = <PIN>;
  $comment  = <PIN>;
  $bestweb1 = <PIN>;
  $bestweb2 = <PIN>;
  $bestweb3 = <PIN>;
  $HomeImage = <PIN>;
  $BGImage = <PIN>;
  $BGImageUse = int(<PIN>);

  chomp($address);
  chomp($age);
  chomp($photo);
  chomp($job);
  chomp($email);
  chomp($icq);
  chomp($webtitle);
  chomp($webaddr);
  chomp($comment);
  chomp($bestweb1);
  chomp($bestweb2);
  chomp($bestweb3);
  chomp($HomeImage);
  chomp($BGImage);

  $Hprofile{'lastModify'} = $lastModify;
  $Hprofile{'photo'} = $photo;
  $Hprofile{'address'} = $address;
  $Hprofile{'age'} = $age;
  $Hprofile{'sex'} = $sex;
  $Hprofile{'job'} = $job;
  $Hprofile{'email'} = $email;
  $Hprofile{'icq'} = $icq;
  $Hprofile{'webTitle'} = $webtitle;
  $Hprofile{'webAddress'} = $webaddr;
  $Hprofile{'comment'} = $comment;
  $Hprofile{'BestWebsite1'} = $bestweb1;
  $Hprofile{'BestWebsite2'} = $bestweb2;
  $Hprofile{'BestWebsite3'} = $bestweb3;
  $Hprofile{'MyHomeImage'} = $HomeImage;
  $Hprofile{'BackgroundImage'} = $BGImage;
  $Hprofile{'BackgroundUse'} = $BGImageUse;

  close(PIN);
  return 1;
}
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
	return 0;
  }
  
  # 各パラメータの読みこみ
  <IN>;	# ターン数

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

  my($id,$name,$ownername);

  $name = <IN>;
  $name =~ /(.*),(.*)/;	# 島の名前
  $name = $1;
  $id = int(<IN>);# ID番号

  $ownername = <IN>;
  chomp($ownername); # オーナ名

  # ファイルポインタを進める
  <IN>;	# 受賞
  <IN>;	# 連続資金繰り数
  <IN>;	# コメント
  my($password);
  $password = <IN>; # 暗号化パスワード
  chomp($password);
  # ファイルポインタを進める
  for($i = 7; $i < 35; $i++) {
	<IN>;
  }

  return {
	'id' => $id,
	'name' => $name,
	'ownername' => $ownername,
	'password' => $password,
  };
}
#---------------------------------------------------------------------
#	関数名 : cookieInput
#	機　能 : 箱庭諸島で生成されたクッキーを取得
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub cookieInput {
  my($cookie);

  $cookie = jcode::euc($ENV{'HTTP_COOKIE'});

  if($cookie =~ /OWNISLANDID=\(([^\)]*)\)/) {
    $HdefaultID = $1;
  }
  if($cookie =~ /OWNISLANDPASSWORD=\(([^\)]*)\)/) {
	$HdefaultPassword = $1;
  }
  if($cookie =~ /${HthisFile}SKIN=\(([^\)]*)\)/) {
	$HskinName = $1;
  }
}
#--------------------------------------------------------------------
#	関数名 : htmlEscape
#	機  能 : タグカット でもなぜか改行コードを<br>に変換
#	引  数 : なし
#	戻り値 : なし
#--------------------------------------------------------------------
sub htmlEscape {
  my($s) = @_;
  $s =~ s/&/&amp;/g;
  $s =~ s/</&lt;/g;
  $s =~ s/>/&gt;/g;
  $s =~ s/\"/&quot;/g; #"
  $s =~ s/\r\n/<br>/g; # win
  $s =~ s/\n/<br>/g;   # unix
  $s =~ s/\r/<br>/g;   # mac
  $s =~ s/'/&#39;/g;
  $s =~ s/ /&#32;/g;
  return $s;
}

#--------------------------------------------------------------------
#	関数名 : timeToString
#	機  能 : 組込み関数timeで取得した時刻を文字列に変換
#	引  数 : timeで取得した数値データ
#	戻り値 : 文字列
#--------------------------------------------------------------------
sub timeToString {
  my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	localtime($_[0]);
  $mon++;
  $year += 1900;

  return "${year}年 ${mon}月 ${date}日 ${hour}時 ${min}分 ${sec}秒";
}
#--------------------------------------------------------------------
#	関数名 : HdebugOut
#	機  能 : デバッグ用関数
#	引  数 : なし
#	戻り値 : なし
#--------------------------------------------------------------------
sub HdebugOut {
  open(DOUT, ">>debug.log");
  print DOUT ($_[0]);
  close(DOUT);
}

#---------------------------------------------------------------------
# データ表示関係
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
#	関数名 : htmlHeader
#	機  能 : HTMLヘッダ部分出力
#	引  数 : なし
#	戻り値 : なし
#--------------------------------------------------------------------
sub htmlHeader {
  if($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/ && $Hinit{'gzip'} == 1){
	print qq{Content-type: text/html; charset=Shift-JIS\n};
	print qq{Content-encoding: gzip\n\n};
	open(STDOUT,"| $Hinit{'gzipPath'}/gzip -1 -c");
	print " " x 2048 if($ENV{HTTP_USER_AGENT}=~/MSIE/);
	print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
  }else{
	print qq{Content-type: text/html; charset=Shift-JIS\n\n};
	print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
}
  $HskinName = ($HskinName ne '') ? "$HskinName" : "$HcssFile";
  out(<<END);
<HTML>
<HEAD>
<TITLE>
$Hhtml{'title'}
</TITLE>
<base href="$imageDir/">
<link rel="stylesheet" type="text/css" href="$HskinName">
</HEAD>
$Hhtml{'body'}
<DIV ID='BodySpecial'><DIV ID='LinkHead'></DIV><DIV ID='LinkTop'>
<A HREF="$Hhtml{'bye'}">[戻る]</A>　<a href="${HbaseDir}/$Hinit{'thisFile'}">[プロフィール一覧]</a>　<a href="${HbaseDir}/$Hinit{'thisFile'}?profile=$HdefaultID&mode=edit">[プロフィール編集]</a>
<HR></DIV>
END
}
#---------------------------------------------------------------------
#	関数名 : htmlFooter
#	機　能 : HTMLのフッタ部分を出力
#	引　数 : なし
#	戻り値 : なし
#---------------------------------------------------------------------
sub htmlFooter {
  out(<<END);
<P>
<I><A HREF="http://club.www.infoseek.co.jp/club.asp?cid=j1100037">Scripted By Watson</A></I>
</P><P></DIV>
</BODY>
</HTML>
END
}
#--------------------------------------------------------------------
#	関数名 : htmlProfileList
#	機  能 : HTMLのプロフィールリスト部分を出力
#	引  数 : なし
#	戻り値 : なし
#--------------------------------------------------------------------
sub htmlProfileList {
  my($i);

  out(<<END);
  <TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=100% $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>島名</td><td $Hhtml{'tdHeaderColor'}>オーナ名</td><td $Hhtml{'tdHeaderColor'}>更新時刻</td></tr>
END
  my($timeString);
  for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'lastModify'} > 0){
	  $timeString = timeToString($Hislands[$i]->{'lastModify'});
	  out("<tr><td $Hhtml{'cellColor'}><a href=\"${HbaseDir}/$Hinit{'thisFile'}?profile=$Hislands[$i]->{'id'}\">$Hislands[$i]->{'name'}島</a></td><td $Hhtml{'cellColor'}>$Hislands[$i]->{'ownername'}</td><td $Hhtml{'cellColor'}>$timeString</td></tr>");
	}
  }
out(<<END);
</table>
</td></tr></table>
END
}
#--------------------------------------------------------------------
#	関数名 : htmlProfile
#	機  能 : HTMLのプロフィール部分を出力
#	引  数 : なし
#	戻り値 : なし
#--------------------------------------------------------------------
sub htmlProfile {
  my($num) = $HidToNumber{$Hinput{'ID'}};
  my($sex) = '無回答';
  if($Hprofile{'sex'} == 1) {
	$sex = '男性';
  } elsif($Hprofile{'sex'} == 2) {
	$sex = '女性';
  }
  my($comment) = '未設定';
  if($Hprofile{'comment'} ne '') {
	$comment = $Hprofile{'comment'};
  }
  my($email) = '未設定';
  if($Hprofile{'email'} ne '') {
	$email = "<a href=\"mailto:$Hprofile{'email'}\">$Hprofile{'email'}</a>";
  }
  my($icq) = '未設定';
  if($Hprofile{'icq'} ne '') {
	$icq = "UIN : $Hprofile{'icq'} - <img src=\"http://online.mirabilis.com/scripts/online.dll?icq=$Hprofile{'icq'}&img=1\">";
  }
  my($hp) = '未設定';
  if(($Hprofile{'webTitle'} ne '') && ($Hprofile{'webAddress'} =~ /http:\/\/.+/)) {
	$hp = "<a href=\"$Hprofile{'webAddress'}\">$Hprofile{'webTitle'}</a>";
  }
  my($MyImage) = '未設定';
  if($Hprofile{'MyHomeImage'} =~ /http:\/\/+/) {
	$MyImage = "<a href=\"$Hprofile{'MyHomeImage'}\">$Hprofile{'MyHomeImage'}</a>";
  }
  my($bgimage) = '未設定';
  if($Hprofile{'BackgroundImage'} =~ /http:\/\/+/) {
	$bgimage = "<a href=\"$Hprofile{'BackgroundImage'}\">$Hprofile{'BackgroundImage'}</a>";
  }
  my($bgimageuse) = '表示する';
  if($Hprofile{'BackgroundUse'} == 2) {
	$bgimageuse = '表示しない';
  }
  
  my($timeString);
  if($Hprofile{'lastModify'} != 0){
	$timeString = timeToString($Hprofile{'lastModify'});
  }
  out(<<END);
<p>
<div align="right">更新時刻 : $timeString</div>
<div class="bar1"><div class="bar2"><b>プロフィール</b></div></div>
</p>

<table>
<tr><td valign=top>
END
  if($Hprofile{'photo'} =~ /http:\/\/.+/){
	out(<<END);
<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=250 $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>写真</td></tr>
<tr><td $Hhtml{'cellColor'} align=center><a href="$Hprofile{'photo'}"><img src="$Hprofile{'photo'}" alt="me" border=0 width=230></a></td></tr>
</table>
</td></tr></table>
</p>
END
  }
  out(<<END);
<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=250 $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'} width=80>島の名前</td><td $Hhtml{'cellColor'}>$Hislands[$num]->{'name'}島</td></tr>
<tr><td $Hhtml{'tdHeaderColor'} width=80>オーナの名前</td><td $Hhtml{'cellColor'}>$Hislands[$num]->{'ownername'}</td></tr>
<tr><td $Hhtml{'tdHeaderColor'} width=80>住所</td><td $Hhtml{'cellColor'}>$Hprofile{'address'}</td></tr>
<tr><td $Hhtml{'tdHeaderColor'} width=80>年齢</td><td $Hhtml{'cellColor'}>$Hprofile{'age'}</td></tr>
<tr><td $Hhtml{'tdHeaderColor'} width=80>性別</td><td $Hhtml{'cellColor'}>$sex</td></tr>
<tr><td $Hhtml{'tdHeaderColor'} width=80>職業</td><td $Hhtml{'cellColor'}>$Hprofile{'job'}</td></tr>
</table>
</td></tr></table>
</p>

<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=250 $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>E-Mail</td></tr>
<tr><td $Hhtml{'cellColor'}>$email</td></tr>
</table>
</td></tr></table>
</p>

<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=250 $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>ICQ</td></tr>
<tr><td $Hhtml{'cellColor'}>$icq</td></tr>
</table>
</td></tr></table>
</p>

</td>
<td width=10></td>

<td valign=top>
<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=340 $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>興味・関心</td></tr>
<td $Hhtml{'cellColor'}>$comment</td></tr>
</table>
</td></tr></table>
</p>

<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=340 $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>My ホームページ</td></tr>
<tr><td $Hhtml{'cellColor'}>$hp</td></tr>
</table>
</td></tr></table>
</p>


<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=340 $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>おすすめサイト</td></tr>
<td $Hhtml{'cellColor'}>
<ul>
END
if($Hprofile{'BestWebsite1'} =~ /http:\/\/.+/){
  out("<li><a href=\"$Hprofile{'BestWebsite1'}\">$Hprofile{'BestWebsite1'}</a>");
}else{
  out("<li>");
}
if($Hprofile{'BestWebsite2'} =~ /http:\/\/.+/){
  out("<li><a href=\"$Hprofile{'BestWebsite2'}\">$Hprofile{'BestWebsite2'}</a>");
}else{
  out("<li>");
}
if($Hprofile{'BestWebsite3'} =~ /http:\/\/.+/){
  out("<li><a href=\"$Hprofile{'BestWebsite3'}\">$Hprofile{'BestWebsite3'}</a>");
}else{
  out("<li>");
}
  out(<<END);
</ul>
</td></tr>
</table>
</td></tr></table>
</p>

<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=340 $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>マイホーム画像 URL</td></tr>
<tr><td $Hhtml{'cellColor'}>$MyImage</td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>島独自背景画像 or スタイルシート URL</td></tr>
<tr><td $Hhtml{'cellColor'}>$bgimage</td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>島独自背景画像 or スタイルシート 表示</td></tr>
<tr><td $Hhtml{'cellColor'}>$bgimageuse</td></tr>
</table>
</td></tr></table>
</p>

</td></tr></table>


END
}


#--------------------------------------------------------------------
#	関数名 : htmlEdit
#	機  能 : HTML プロフィール編集部分を出力
#	引  数 : なし
#	戻り値 : なし
#--------------------------------------------------------------------
sub htmlEdit {

  my($num) = $HidToNumber{$Hinput{'ID'}};
  my($timeString);
  if($Hprofile{'lastModify'} != 0){
	$timeString = timeToString($Hprofile{'lastModify'});
  }
  out(<<END);
<p>
<div align="right">更新時刻 : $timeString</div>
<div class="bar1"><div class="bar2">プロフィール編集</div></div>
</p>
<form action="${HbaseDir}/$Hinit{'thisFile'}?profile=$HdefaultID" method="POST">
<div style="margin-left:2em">
※　設定するかは全て任意です。内容はすべて公開されますので注意してください。
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0  $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>島の名前</td><td $Hhtml{'cellColor'}>$Hislands[$num]->{'name'}島</td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>オーナの名前</td><td $Hhtml{'cellColor'}>$Hislands[$num]->{'ownername'}</td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>住所</td>
<td $Hhtml{'cellColor'}><input type="text" name="ADDRESS" size=40 maxlength=40 value="$Hprofile{'address'}"></td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>年齢</td>
<td $Hhtml{'cellColor'}><input type="text" name="AGE" size=3 maxlength=3 value="$Hprofile{'age'}"></td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>性別</td>
<td $Hhtml{'cellColor'}>
END
if($Hprofile{'sex'} == 1) {
  out("<input type=\"radio\" name=\"SEX\" value=\"1\" checked>男性");
} else {
  out("<input type=\"radio\" name=\"SEX\" value=\"1\">男性");
}
if($Hprofile{'sex'} == 2) {
  out("<input type=\"radio\" name=\"SEX\" value=\"2\" checked>女性");
} else {
  out("<input type=\"radio\" name=\"SEX\" value=\"2\">女性");
}
if($Hprofile{'sex'} != 1 && $Hprofile{'sex'} != 2) {
  out("<input type=\"radio\" name=\"SEX\" value=\"3\" checked>無回答");
} else {
  out("<input type=\"radio\" name=\"SEX\" value=\"3\">無回答");
}

out(<<END);
</td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>職業</td>
<td $Hhtml{'cellColor'}><input type="text" name="JOB" size=40 maxlength=40 value="$Hprofile{'job'}"></td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>E-mail</td>
<td $Hhtml{'cellColor'}><input type="text" name="EMAIL" size=40 maxlength=40 value="$Hprofile{'email'}"></td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>ICQ</td>
<td $Hhtml{'cellColor'}><input type="text" name="ICQ" size=10 maxlength=10 value="$Hprofile{'icq'}"></td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>ホームページ タイトル</td>
<td $Hhtml{'cellColor'}><input type="text" name="HPTITLE" size=40 maxlength=40 value="$Hprofile{'webTitle'}"></td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>ホームページ URL</td>
<td $Hhtml{'cellColor'}>
END
if($Hprofile{'webAddress'} ne ''){
  out("<input type=\"text\" name=\"URL\" size=80 maxlength=80 value=\"$Hprofile{'webAddress'}\"></td></tr>");
} else {
  out("<input type=\"text\" name=\"URL\" size=80 maxlength=80 value=\"http://\"></td></tr>");
}
out(<<END);
<tr><td $Hhtml{'tdHeaderColor'}>写真があるURL</td>
<td $Hhtml{'cellColor'}>
END
if($Hprofile{'photo'} ne ''){
  out("<input type=\"text\" name=\"PHOTO\" size=80 maxlength=80 value=\"$Hprofile{'photo'}\"></td></tr>");
} else {
  out("<input type=\"text\" name=\"PHOTO\" size=80 maxlength=80 value=\"http://\"></td></tr>");
}
my($comment) = $Hprofile{'comment'};
$comment =~ s/<br>/\n/g;
out(<<END);

<tr><td $Hhtml{'tdHeaderColor'}>マイホーム画像 URL</td>
<td $Hhtml{'cellColor'}>
END
if($Hprofile{'MyHomeImage'} ne ''){
  out("<input type=\"text\" name=\"HOMEIMAGE\" size=80 maxlength=80 value=\"$Hprofile{'MyHomeImage'}\"></td></tr>");
} else {
  out("<input type=\"text\" name=\"HOMEIMAGE\" size=80 maxlength=80 value=\"\"></td></tr>");
}
out(<<END);
<tr><td $Hhtml{'tdHeaderColor'}>島独自背景画像 or スタイルシート URL</td>
<td $Hhtml{'cellColor'}>
END
if($Hprofile{'BackgroundImage'} ne ''){
  out("<input type=\"text\" name=\"BGIMAGE\" size=80 maxlength=80 value=\"$Hprofile{'BackgroundImage'}\"></td></tr>");
} else {
  out("<input type=\"text\" name=\"BGIMAGE\" size=80 maxlength=80 value=\"\"></td></tr>");
}

out(<<END);
<tr><td $Hhtml{'tdHeaderColor'}>島独自背景画像 or スタイルシート 表示</td>
<td $Hhtml{'cellColor'}>
END
if($Hprofile{'BackgroundUse'} == 1) {
  out("<input type=\"radio\" name=\"BGIMAGEUSE\" value=\"1\" checked>ＯＮ");
} else {
  out("<input type=\"radio\" name=\"BGIMAGEUSE\" value=\"1\">ＯＮ");
}
if($Hprofile{'BackgroundUse'} == 2) {
  out("<input type=\"radio\" name=\"BGIMAGEUSE\" value=\"2\" checked>ＯＦＦ");
} else {
  out("<input type=\"radio\" name=\"BGIMAGEUSE\" value=\"2\">ＯＦＦ");
}

out(<<END);

</td></tr>

</table>
</td></tr></table>
<p>※島独自背景画像 or スタイルシート URLは、必ず「http://」から設定してください。<br>
画像ファイルを指定すると島独自背景画像が設定されます。<br>
拡張子が「css」のファイルを指定すると島独自スタイルシートが設定されます。</p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0  $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>興味・関心</td></tr>
<tr><td $Hhtml{'cellColor'}><textarea cols=50 rows=5 name="COMMENT">$comment</textarea></td></tr>
</table>
</td></tr></table>
</p>

<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0  $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>おすすめサイト</td></tr>
<tr><td $Hhtml{'cellColor'}>
END
if($Hprofile{'BestWebsite1'} ne ''){
  out("1. <input type=\"text\" name=\"BESTWEB1\" size=80 maxlength=80 value=\"$Hprofile{'BestWebsite1'}\"><br>");
} else {
  out("1. <input type=\"text\" name=\"BESTWEB1\" size=80 maxlength=80 value=\"http://\"><br>");
}
if($Hprofile{'BestWebsite2'} ne ''){
  out("2. <input type=\"text\" name=\"BESTWEB2\" size=80 maxlength=80 value=\"$Hprofile{'BestWebsite2'}\"><br>");
} else {
  out("2. <input type=\"text\" name=\"BESTWEB2\" size=80 maxlength=80 value=\"http://\"><br>");
}
if($Hprofile{'BestWebsite3'} ne ''){
  out("3. <input type=\"text\" name=\"BESTWEB3\" size=80 maxlength=80 value=\"$Hprofile{'BestWebsite3'}\"><br>");
} else {
  out("3. <input type=\"text\" name=\"BESTWEB3\" size=80 maxlength=80 value=\"http://\"><br>");
}
  out(<<END);
</td></tr>
</table>
</td></tr></table>
</p>

パスワード : <input type="password" name="PASSWORD" size=32 maxlength=32 value="${\htmlEscape($HdefaultPassword)}">
<INPUT TYPE="submit" VALUE="変更する" NAME="changeProfileButton">
</div>
</form>
END
}

#--------------------------------------------------------------------
#	関数名 : tempNoDataFile
#	機  能 : 箱庭のデータやオーナ用のデータファイルがオープンできない
#	         ときなどに表示するエラーメッセージ
#	引  数 : なし
#	戻り値 : なし
#--------------------------------------------------------------------
sub tempNoDataFile {
  out(<<END);
データファイルが開けません。
END
}
#--------------------------------------------------------------------
#	関数名 : tempNoProfileDataFile
#	機  能 : プロフィール用のデータファイルが開けないときのエラーメッセージ
#	引  数 : なし
#	戻り値 : なし
#--------------------------------------------------------------------
sub tempNoProfileDataFile {
  out(<<END);
プロフィールデータファイルが開けません。
END
}
#--------------------------------------------------------------------
#	関数名 : tempWrongPassword
#	機  能 : パスワードチェックに失敗した場合のエラーメッセージ
#	引  数 : なし
#	戻り値 : なし
#--------------------------------------------------------------------
sub tempWrongPassword {
  out(<<END);
パスワードが違います。
END
}
