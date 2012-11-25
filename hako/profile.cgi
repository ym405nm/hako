#!/usr/local/bin/perl --

#--------------------------------------------------------------------
# Ȣ����� Profiles
#
#	��������2001/03/13
#	�����ԡ�Watson <watson@catnip.freemail.ne.jp>
#
#	��������4
#
#	���ۤ�Ȣ���Ѥ��ȼ���ĥ���Ƥ���ޤ���
#--------------------------------------------------------------------

use Time::Local;

#---------------------------------------------------------------------
#	�������
#---------------------------------------------------------------------
# hako-init.cgi��require
require './hako-init.cgi';

$Hinit{'thisFile'} = 'profile.cgi';

# gzip�λ���  1 : ����  0 : ̤����
$Hinit{'gzip'} = 0;
# gzip�Υѥ�
$Hinit{'gzipPath'} = '/bin';

# HTML�˴ؤ�������
$Hhtml{'body'} = '<body>';
$Hhtml{'title'} = 'Ȣ����� �ץ�ե�����';

$Hhtml{'lineColor'}     = 'class=lineColor';
$Hhtml{'tdHeaderColor'} = 'class=tdHeaderColor';
$Hhtml{'cellColor'}     = 'class=cellColor';

# �����
$Hhtml{'bye'} = "$HbaseDir/hako-main.cgi";

#�ᥤ��--------------------------------------------------------------
#--------------------------------------------------------------------
&main;
exit(0);

#--------------------------------------------------------------------
#	�ؿ�̾ : main
#	��  ǽ : �ᥤ��ؿ�
#	��  �� : �ʤ�
#	����� : �ʤ�
#--------------------------------------------------------------------
sub main {
  &cookieInput;
  &cgiInput;
  &htmlHeader;

  # ��ǡ�������
  if(!(&readIslandsFile)) {
	&tempNoDataFile;
	&htmlFooter;
	return;
  }

  # ID�����ꤵ��Ƥ��ʤ���Хץ�ե�����ꥹ�Ȥ�ɽ��
  if($HidToNumber{$Hinput{'ID'}} eq ''){
	&getProfileLastModify;
	&lastModifySort;
	&htmlProfileList;
	&htmlFooter;
	return;
  }
  # �ץ�ե��������� (ɬ��������������)
  if($HmainMode eq 'changeProfile'){
	if(&checkPassword($Hislands[$HidToNumber{$HdefaultID}]->{'password'}, $HinputPassword)){
	  &writeProfileFile;
	} else {
	  &tempWrongPassword;
	  &htmlFooter;
	  return;
	}
  }

  #�ץ�ե��������
  &readProfileFile;

  if($HmainMode eq 'edit'){
	&htmlEdit; # �ץ�ե������Խ�
  } else {
	&htmlProfile; # �ץ�ե�����ɽ��
  }
  &htmlFooter;

}
#���֥롼����--------------------------------------------------------
#--------------------------------------------------------------------
#	�ؿ�̾ : checkPassword
#	��  ǽ : �ѥ���ɥ����å�
#	��  �� : �Ź沽���줿�ѥ���ɡ����Υѥ����
#	����� : 0 - �ȹ缺��
#	         1 - �ȹ�����
#--------------------------------------------------------------------
sub checkPassword {
  my($p1, $p2) = @_;
  if($p1 eq crypt($p2, 'h2')){
	return 1;
  }
  return 0;
}
#--------------------------------------------------------------------
#	�ؿ�̾ : checkUrl
#	��  ǽ : ʸ���� http:// ����ϤޤäƤ��뤫�����å�
#	��  �� : ʸ����
#	����� : http:// ����ϤޤäƤ���Ф��Τޤ�ʸ������֤�
#	         �����Ǥʤ���ж���ʸ����
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
#	�ؿ�̾ : lastModifySort
#	��  ǽ : ��������˱����ƥꥹ�Ȥ򥽡���
#	��  �� : �ʤ�
#	����� : �ʤ�
#--------------------------------------------------------------------
sub lastModifySort {

  # ��������ǥ�����
  my(@idx) = (0..$HislandNumber);
  @idx = sort { $Hislands[$b]->{'lastModify'} <=> $Hislands[$a]->{'lastModify'} || $a <=> $b } @idx;
  @Hislands = @Hislands[@idx];
}
#--------------------------------------------------------------------
#	�ؿ�̾ : cutColumn
#	��  ǽ : ʸ�������ڤ�ͤ��
#	��  �� : ʸ�����ڤ�ͤ���
#	����� : �ڤ�ͤ᤿ʸ����
#--------------------------------------------------------------------
sub cutColumn {
  my($s, $c) = @_;
  if(length($s) <= $c) {
	return $s;
  } else {
	# ���80�����ˤʤ�ޤ��ڤ���
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
#	�ؿ�̾ : cgiInput
#	��  ǽ : POST or GET�����Ϥ��줿�ǡ�������
#	��  �� : �ʤ�
#	����� : �ʤ�
#--------------------------------------------------------------------
sub cgiInput {
  my($line, $getLine);

  # ���Ϥ������ä����ܸ쥳���ɤ�EUC��
  $line = <>;
  $line =~ tr/+/ /;
  $line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $line = jcode::euc($line);
  $line =~ s/[\,\r]//g;

  # GET�Τ�Ĥ�������
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
#	�ؿ�̾ : getProfileLastModify
#	��  ǽ : �ץ�ե�����ǡ���������
#	��  �� : �ʤ�
#	����� : �ʤ�
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
#	�ؿ�̾ : writeProfileFile
#	��  ǽ : �ץ�ե�����ǡ���������
#	��  �� : ID
#	����� : 0 - �ե����륪���ץ�˼���
#	         1 - ����
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
#	�ؿ�̾ : readProfileFile
#	��  ǽ : �ץ�ե�����ǡ��������
#	��  �� : �ʤ�
#	����� : 0 - �ե����륪���ץ�˼���
#	         1 - ����
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
#	�ؿ�̾ : readIslandsFile
#	����ǽ : ����Υǡ������ɤ߹���
#	������ : �ʤ�
#	����� : 0 - �ե����륪���ץ�˼���
#	         1 - ����
#---------------------------------------------------------------------
sub readIslandsFile {

  # �ǡ����ե�����򳫤�
  if(!open(IN, "${HdirName}/hakojima.dat")) {
	return 0;
  }
  
  # �ƥѥ�᡼�����ɤߤ���
  <IN>;	# �������

  <IN>;	# �ǽ���������(���Ѥ��ʤ��ͤʤΤ��ɤ����Ф�)

  $HislandNumber	= int(<IN>);	# ������
  <IN>;	# ���˳�����Ƥ�ID(���Ѥ��ʤ��ͤʤΤ��ɤ����Ф�)

  # ����ɤߤ���
  my($i, $id);
  for($i = 0; $i < $HislandNumber; $i++) {
	$Hislands[$i] = readIsland($i);
	$HidToNumber{$Hislands[$i]->{'id'}} = $i;
  }

  # �ե�������Ĥ���
  close(IN);

  return 1;
}
#---------------------------------------------------------------------
#	�ؿ�̾ : readIsland
#	����ǽ : ����˳�����Ƥ��Ƥ���ID�����
#	������ : 0 .. $HislandNumber
#	����� : ���ID
#---------------------------------------------------------------------
sub readIsland {
  my($num) = @_;

  my($id,$name,$ownername);

  $name = <IN>;
  $name =~ /(.*),(.*)/;	# ���̾��
  $name = $1;
  $id = int(<IN>);# ID�ֹ�

  $ownername = <IN>;
  chomp($ownername); # ������̾

  # �ե�����ݥ��󥿤�ʤ��
  <IN>;	# ����
  <IN>;	# Ϣ³��ⷫ���
  <IN>;	# ������
  my($password);
  $password = <IN>; # �Ź沽�ѥ����
  chomp($password);
  # �ե�����ݥ��󥿤�ʤ��
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
#	�ؿ�̾ : cookieInput
#	����ǽ : Ȣ�������������줿���å��������
#	������ : �ʤ�
#	����� : �ʤ�
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
#	�ؿ�̾ : htmlEscape
#	��  ǽ : �������å� �Ǥ�ʤ������ԥ����ɤ�<br>���Ѵ�
#	��  �� : �ʤ�
#	����� : �ʤ�
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
#	�ؿ�̾ : timeToString
#	��  ǽ : �ȹ��ߴؿ�time�Ǽ������������ʸ������Ѵ�
#	��  �� : time�Ǽ����������ͥǡ���
#	����� : ʸ����
#--------------------------------------------------------------------
sub timeToString {
  my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	localtime($_[0]);
  $mon++;
  $year += 1900;

  return "${year}ǯ ${mon}�� ${date}�� ${hour}�� ${min}ʬ ${sec}��";
}
#--------------------------------------------------------------------
#	�ؿ�̾ : HdebugOut
#	��  ǽ : �ǥХå��Ѵؿ�
#	��  �� : �ʤ�
#	����� : �ʤ�
#--------------------------------------------------------------------
sub HdebugOut {
  open(DOUT, ">>debug.log");
  print DOUT ($_[0]);
  close(DOUT);
}

#---------------------------------------------------------------------
# �ǡ���ɽ���ط�
#---------------------------------------------------------------------
#	�ؿ�̾ : out
#	����ǽ : ʸ�������ɤ�shift jis��ɸ����Ϥ˥����ȥץå�
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub out {
  print STDOUT jcode::sjis($_[0]);
}

#--------------------------------------------------------------------
#	�ؿ�̾ : htmlHeader
#	��  ǽ : HTML�إå���ʬ����
#	��  �� : �ʤ�
#	����� : �ʤ�
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
<A HREF="$Hhtml{'bye'}">[���]</A>��<a href="${HbaseDir}/$Hinit{'thisFile'}">[�ץ�ե��������]</a>��<a href="${HbaseDir}/$Hinit{'thisFile'}?profile=$HdefaultID&mode=edit">[�ץ�ե������Խ�]</a>
<HR></DIV>
END
}
#---------------------------------------------------------------------
#	�ؿ�̾ : htmlFooter
#	����ǽ : HTML�Υեå���ʬ�����
#	������ : �ʤ�
#	����� : �ʤ�
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
#	�ؿ�̾ : htmlProfileList
#	��  ǽ : HTML�Υץ�ե�����ꥹ����ʬ�����
#	��  �� : �ʤ�
#	����� : �ʤ�
#--------------------------------------------------------------------
sub htmlProfileList {
  my($i);

  out(<<END);
  <TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=100% $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>��̾</td><td $Hhtml{'tdHeaderColor'}>������̾</td><td $Hhtml{'tdHeaderColor'}>��������</td></tr>
END
  my($timeString);
  for($i = 0; $i < $HislandNumber; $i++) {
	if($Hislands[$i]->{'lastModify'} > 0){
	  $timeString = timeToString($Hislands[$i]->{'lastModify'});
	  out("<tr><td $Hhtml{'cellColor'}><a href=\"${HbaseDir}/$Hinit{'thisFile'}?profile=$Hislands[$i]->{'id'}\">$Hislands[$i]->{'name'}��</a></td><td $Hhtml{'cellColor'}>$Hislands[$i]->{'ownername'}</td><td $Hhtml{'cellColor'}>$timeString</td></tr>");
	}
  }
out(<<END);
</table>
</td></tr></table>
END
}
#--------------------------------------------------------------------
#	�ؿ�̾ : htmlProfile
#	��  ǽ : HTML�Υץ�ե�������ʬ�����
#	��  �� : �ʤ�
#	����� : �ʤ�
#--------------------------------------------------------------------
sub htmlProfile {
  my($num) = $HidToNumber{$Hinput{'ID'}};
  my($sex) = '̵����';
  if($Hprofile{'sex'} == 1) {
	$sex = '����';
  } elsif($Hprofile{'sex'} == 2) {
	$sex = '����';
  }
  my($comment) = '̤����';
  if($Hprofile{'comment'} ne '') {
	$comment = $Hprofile{'comment'};
  }
  my($email) = '̤����';
  if($Hprofile{'email'} ne '') {
	$email = "<a href=\"mailto:$Hprofile{'email'}\">$Hprofile{'email'}</a>";
  }
  my($icq) = '̤����';
  if($Hprofile{'icq'} ne '') {
	$icq = "UIN : $Hprofile{'icq'} - <img src=\"http://online.mirabilis.com/scripts/online.dll?icq=$Hprofile{'icq'}&img=1\">";
  }
  my($hp) = '̤����';
  if(($Hprofile{'webTitle'} ne '') && ($Hprofile{'webAddress'} =~ /http:\/\/.+/)) {
	$hp = "<a href=\"$Hprofile{'webAddress'}\">$Hprofile{'webTitle'}</a>";
  }
  my($MyImage) = '̤����';
  if($Hprofile{'MyHomeImage'} =~ /http:\/\/+/) {
	$MyImage = "<a href=\"$Hprofile{'MyHomeImage'}\">$Hprofile{'MyHomeImage'}</a>";
  }
  my($bgimage) = '̤����';
  if($Hprofile{'BackgroundImage'} =~ /http:\/\/+/) {
	$bgimage = "<a href=\"$Hprofile{'BackgroundImage'}\">$Hprofile{'BackgroundImage'}</a>";
  }
  my($bgimageuse) = 'ɽ������';
  if($Hprofile{'BackgroundUse'} == 2) {
	$bgimageuse = 'ɽ�����ʤ�';
  }
  
  my($timeString);
  if($Hprofile{'lastModify'} != 0){
	$timeString = timeToString($Hprofile{'lastModify'});
  }
  out(<<END);
<p>
<div align="right">�������� : $timeString</div>
<div class="bar1"><div class="bar2"><b>�ץ�ե�����</b></div></div>
</p>

<table>
<tr><td valign=top>
END
  if($Hprofile{'photo'} =~ /http:\/\/.+/){
	out(<<END);
<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=250 $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>�̿�</td></tr>
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
<tr><td $Hhtml{'tdHeaderColor'} width=80>���̾��</td><td $Hhtml{'cellColor'}>$Hislands[$num]->{'name'}��</td></tr>
<tr><td $Hhtml{'tdHeaderColor'} width=80>�����ʤ�̾��</td><td $Hhtml{'cellColor'}>$Hislands[$num]->{'ownername'}</td></tr>
<tr><td $Hhtml{'tdHeaderColor'} width=80>����</td><td $Hhtml{'cellColor'}>$Hprofile{'address'}</td></tr>
<tr><td $Hhtml{'tdHeaderColor'} width=80>ǯ��</td><td $Hhtml{'cellColor'}>$Hprofile{'age'}</td></tr>
<tr><td $Hhtml{'tdHeaderColor'} width=80>����</td><td $Hhtml{'cellColor'}>$sex</td></tr>
<tr><td $Hhtml{'tdHeaderColor'} width=80>����</td><td $Hhtml{'cellColor'}>$Hprofile{'job'}</td></tr>
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
<tr><td $Hhtml{'tdHeaderColor'}>��̣���ؿ�</td></tr>
<td $Hhtml{'cellColor'}>$comment</td></tr>
</table>
</td></tr></table>
</p>

<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=340 $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>My �ۡ���ڡ���</td></tr>
<tr><td $Hhtml{'cellColor'}>$hp</td></tr>
</table>
</td></tr></table>
</p>


<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=340 $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>�������᥵����</td></tr>
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
<tr><td $Hhtml{'tdHeaderColor'}>�ޥ��ۡ������ URL</td></tr>
<tr><td $Hhtml{'cellColor'}>$MyImage</td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>���ȼ��طʲ��� or �������륷���� URL</td></tr>
<tr><td $Hhtml{'cellColor'}>$bgimage</td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>���ȼ��طʲ��� or �������륷���� ɽ��</td></tr>
<tr><td $Hhtml{'cellColor'}>$bgimageuse</td></tr>
</table>
</td></tr></table>
</p>

</td></tr></table>


END
}


#--------------------------------------------------------------------
#	�ؿ�̾ : htmlEdit
#	��  ǽ : HTML �ץ�ե������Խ���ʬ�����
#	��  �� : �ʤ�
#	����� : �ʤ�
#--------------------------------------------------------------------
sub htmlEdit {

  my($num) = $HidToNumber{$Hinput{'ID'}};
  my($timeString);
  if($Hprofile{'lastModify'} != 0){
	$timeString = timeToString($Hprofile{'lastModify'});
  }
  out(<<END);
<p>
<div align="right">�������� : $timeString</div>
<div class="bar1"><div class="bar2">�ץ�ե������Խ�</div></div>
</p>
<form action="${HbaseDir}/$Hinit{'thisFile'}?profile=$HdefaultID" method="POST">
<div style="margin-left:2em">
�������ꤹ�뤫������Ǥ�դǤ������ƤϤ��٤Ƹ�������ޤ��Τ���դ��Ƥ���������
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0  $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>���̾��</td><td $Hhtml{'cellColor'}>$Hislands[$num]->{'name'}��</td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>�����ʤ�̾��</td><td $Hhtml{'cellColor'}>$Hislands[$num]->{'ownername'}</td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>����</td>
<td $Hhtml{'cellColor'}><input type="text" name="ADDRESS" size=40 maxlength=40 value="$Hprofile{'address'}"></td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>ǯ��</td>
<td $Hhtml{'cellColor'}><input type="text" name="AGE" size=3 maxlength=3 value="$Hprofile{'age'}"></td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>����</td>
<td $Hhtml{'cellColor'}>
END
if($Hprofile{'sex'} == 1) {
  out("<input type=\"radio\" name=\"SEX\" value=\"1\" checked>����");
} else {
  out("<input type=\"radio\" name=\"SEX\" value=\"1\">����");
}
if($Hprofile{'sex'} == 2) {
  out("<input type=\"radio\" name=\"SEX\" value=\"2\" checked>����");
} else {
  out("<input type=\"radio\" name=\"SEX\" value=\"2\">����");
}
if($Hprofile{'sex'} != 1 && $Hprofile{'sex'} != 2) {
  out("<input type=\"radio\" name=\"SEX\" value=\"3\" checked>̵����");
} else {
  out("<input type=\"radio\" name=\"SEX\" value=\"3\">̵����");
}

out(<<END);
</td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>����</td>
<td $Hhtml{'cellColor'}><input type="text" name="JOB" size=40 maxlength=40 value="$Hprofile{'job'}"></td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>E-mail</td>
<td $Hhtml{'cellColor'}><input type="text" name="EMAIL" size=40 maxlength=40 value="$Hprofile{'email'}"></td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>ICQ</td>
<td $Hhtml{'cellColor'}><input type="text" name="ICQ" size=10 maxlength=10 value="$Hprofile{'icq'}"></td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>�ۡ���ڡ��� �����ȥ�</td>
<td $Hhtml{'cellColor'}><input type="text" name="HPTITLE" size=40 maxlength=40 value="$Hprofile{'webTitle'}"></td></tr>
<tr><td $Hhtml{'tdHeaderColor'}>�ۡ���ڡ��� URL</td>
<td $Hhtml{'cellColor'}>
END
if($Hprofile{'webAddress'} ne ''){
  out("<input type=\"text\" name=\"URL\" size=80 maxlength=80 value=\"$Hprofile{'webAddress'}\"></td></tr>");
} else {
  out("<input type=\"text\" name=\"URL\" size=80 maxlength=80 value=\"http://\"></td></tr>");
}
out(<<END);
<tr><td $Hhtml{'tdHeaderColor'}>�̿�������URL</td>
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

<tr><td $Hhtml{'tdHeaderColor'}>�ޥ��ۡ������ URL</td>
<td $Hhtml{'cellColor'}>
END
if($Hprofile{'MyHomeImage'} ne ''){
  out("<input type=\"text\" name=\"HOMEIMAGE\" size=80 maxlength=80 value=\"$Hprofile{'MyHomeImage'}\"></td></tr>");
} else {
  out("<input type=\"text\" name=\"HOMEIMAGE\" size=80 maxlength=80 value=\"\"></td></tr>");
}
out(<<END);
<tr><td $Hhtml{'tdHeaderColor'}>���ȼ��طʲ��� or �������륷���� URL</td>
<td $Hhtml{'cellColor'}>
END
if($Hprofile{'BackgroundImage'} ne ''){
  out("<input type=\"text\" name=\"BGIMAGE\" size=80 maxlength=80 value=\"$Hprofile{'BackgroundImage'}\"></td></tr>");
} else {
  out("<input type=\"text\" name=\"BGIMAGE\" size=80 maxlength=80 value=\"\"></td></tr>");
}

out(<<END);
<tr><td $Hhtml{'tdHeaderColor'}>���ȼ��طʲ��� or �������륷���� ɽ��</td>
<td $Hhtml{'cellColor'}>
END
if($Hprofile{'BackgroundUse'} == 1) {
  out("<input type=\"radio\" name=\"BGIMAGEUSE\" value=\"1\" checked>�ϣ�");
} else {
  out("<input type=\"radio\" name=\"BGIMAGEUSE\" value=\"1\">�ϣ�");
}
if($Hprofile{'BackgroundUse'} == 2) {
  out("<input type=\"radio\" name=\"BGIMAGEUSE\" value=\"2\" checked>�ϣƣ�");
} else {
  out("<input type=\"radio\" name=\"BGIMAGEUSE\" value=\"2\">�ϣƣ�");
}

out(<<END);

</td></tr>

</table>
</td></tr></table>
<p>�����ȼ��طʲ��� or �������륷���� URL�ϡ�ɬ����http://�פ������ꤷ�Ƥ���������<br>
�����ե��������ꤹ������ȼ��طʲ��������ꤵ��ޤ���<br>
��ĥ�Ҥ���css�פΥե��������ꤹ������ȼ��������륷���Ȥ����ꤵ��ޤ���</p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0  $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>��̣���ؿ�</td></tr>
<tr><td $Hhtml{'cellColor'}><textarea cols=50 rows=5 name="COMMENT">$comment</textarea></td></tr>
</table>
</td></tr></table>
</p>

<p>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0  $Hhtml{'lineColor'}><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<tr><td $Hhtml{'tdHeaderColor'}>�������᥵����</td></tr>
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

�ѥ���� : <input type="password" name="PASSWORD" size=32 maxlength=32 value="${\htmlEscape($HdefaultPassword)}">
<INPUT TYPE="submit" VALUE="�ѹ�����" NAME="changeProfileButton">
</div>
</form>
END
}

#--------------------------------------------------------------------
#	�ؿ�̾ : tempNoDataFile
#	��  ǽ : Ȣ��Υǡ����䥪�����ѤΥǡ����ե����뤬�����ץ�Ǥ��ʤ�
#	         �Ȥ��ʤɤ�ɽ�����륨�顼��å�����
#	��  �� : �ʤ�
#	����� : �ʤ�
#--------------------------------------------------------------------
sub tempNoDataFile {
  out(<<END);
�ǡ����ե����뤬�����ޤ���
END
}
#--------------------------------------------------------------------
#	�ؿ�̾ : tempNoProfileDataFile
#	��  ǽ : �ץ�ե������ѤΥǡ����ե����뤬�����ʤ��Ȥ��Υ��顼��å�����
#	��  �� : �ʤ�
#	����� : �ʤ�
#--------------------------------------------------------------------
sub tempNoProfileDataFile {
  out(<<END);
�ץ�ե�����ǡ����ե����뤬�����ޤ���
END
}
#--------------------------------------------------------------------
#	�ؿ�̾ : tempWrongPassword
#	��  ǽ : �ѥ���ɥ����å��˼��Ԥ������Υ��顼��å�����
#	��  �� : �ʤ�
#	����� : �ʤ�
#--------------------------------------------------------------------
sub tempWrongPassword {
  out(<<END);
�ѥ���ɤ��㤤�ޤ���
END
}
