#!/usr/local/bin/perl --

#---------------------------------------------------------------------
#
#	���÷���ݥ���ȡܳ����޶⡡��󥭥�ɽ��
#
#	������ : 2001/02/27
#	������ : Watson <watson@catnip.freemail.ne.jp>
#
#	������ : 4
#
#	���ۤ�Ȣ��5.17�Ѥ��ȼ���ĥ���Ƥ���ޤ���
#---------------------------------------------------------------------

#---------------------------------------------------------------------
#	�������
#---------------------------------------------------------------------
require './hako-init.cgi';
require './init-game.cgi';

# gzip����Ѥ��ư����������롩 0 : ̤����  1 : ����
$ gzip = 0;

# gzip�Υ��󥹥ȡ�����
$pathGzip = '/usr/bin';

# ���̤Ρ����ץ����(URL)
$bye = $HthisFile;

# ��󥭥󥰥ǡ����μ������ϥ�����
$start_turn = 1;

# ¾����β��ä��ݤ������Υݥ���Ȳû�Ψ
$ExternalRate  = 0.5; # Ⱦʬ

# �ߥ�����������ݤ������Υݥ���Ȳû�Ψ
$ExternalSRate  = 0.5; # Ⱦʬ

#----------------------------
#	HTML�˴ؤ�������
#----------------------------
# �֥饦���Υ����ȥ�С���̾��
$title = 'Ȣ����� ��󥭥�';

# ���̤ο����طʤ�����(HTML)
$body = '<body>';

# ��Ƭ�Υ�å�����(HTML��)	 ���÷����󥭥���
$headKill = <<'EOF';
<h2 class=head2>���÷����󥭥�</h2>
EOF

# ��Ƭ�Υ�å�����(HTML��)	 �޶��󥭥���
$headMoney = <<'EOF';
<h2 class=head2>�޶��󥭥�</h2>
EOF

# ��Ƭ�Υ�å�����(HTML��)	 ����ޥ�󥭥���
$headBumon = <<'EOF';
<h2 class=head2>����ޥ�󥭥�</h2>
EOF

# ��Ƭ�Υ�å�����(HTML��)	 ��������󥭥���
$headShip = <<'EOF';
<h2 class=head2>��������󥭥�</h2>
EOF

$headPointCellcolor	= 'class=headPointCellcolor';    # ɽ�ΰ��־�Υݥ������ʬ�Υ��뿧
$headNameCellcolor	= 'class=headNameCellcolor';     # ���β��β��ä�ɽ������Ƥ�����ʬ�Υ��뿧
$pointCellcolor		= 'class=pointCellcolor';        # �ݥ������ʬ�Υ��뿧
$nameCellcolor		= 'class=nameCellcolor';         # ��̾��ɽ����ʬ�Υ��뿧
$TotalPointColor	= 'class=TotalPointColor';       # �ȡ�����ݥ���Ȥ�ʸ����
$PointColor			= 'class=PointColor';            # ���̤Υݥ���Ȥ�ʸ����
$ExternalPointColor	= 'class=ExternalPointColor';    # ¾����β��ä��ݤ�������ʸ����

#�����ޤ�-------------------------------------------------------------

splice(@HmonsterName,32,0,'���ۤ��Τ�');
splice(@HmonsterImage,32,0,'kinora.gif');

# ���÷�����ݥ����
                   # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36
@HmonsterPoint   = ( 5, 3, 3, 4, 4, 4, 5, 7, 6, 6, 9, 5,12,16,18, 6, 4,10,15,10,14,13, 5,12, 5, 5,10, 2, 4, 4,14,40,30,15,17,16,20);

splice(@HshipImage,15,1,'ship163.gif');

# ���������ݥ����
#               ± �� �� õ �� �� �� �� �� �� �� ε ή �� �� ��
@HshipPoint  = ( 6, 3, 6, 3,10,10,11, 5, 2, 3, 4,10, 4, 5, 4, 4);

# ���ο�
$HshipNumber = 16;

&htmlHeader;

if(!(&readIslandsFile)){
	out("<h2 class=head2>���顼��ȯ�����ޤ���</h2>\n");
} else {
	if(!(&calcKillPoint)){
		out("<H3>�ޤ����÷����󥭥󥰥ǡ���������ޤ���</H3>\n");
	}else{
		&htmlKillMonster;
		out("<p align=right><span $ExternalPointColor>(��)</span>���¾����β��ä��ݤ�������ɽ���Ƥ��ޤ����ݥ���Ȥϼ�ʬ����β��ä��ݤ�����Τ�Ⱦʬ���û�����ޤ���<BR>ST�ߥ�������ݤ������äϲû�����ޤ���</p>");
	}
	if(!(&calcMoney)){
		out("<H3>�ޤ��޶��󥭥󥰥ǡ���������ޤ���</H3>\n");
	}else{
		&htmlMoney;
		out("<p align=right>��¢�����ˤ϶��̮�μ�����ޤޤ�ޤ����������ˤϡ�����(����������Τ�)��������μ�����ޤޤ�ޤ���</p>");
	}
	if(!(&calcBumon)){
		out("<H3>�ޤ�����ޥ�󥭥󥰥ǡ���������ޤ���</H3>\n");
	}else{
		&htmlBumon;
		out("<BR><BR>");
	}
	if(!(&calcShip)){
		out("<H3>�ޤ���������󥭥󥰥ǡ���������ޤ���</H3>\n");
	}else{
		&htmlShip;
		out("<p align=right><span $ExternalPointColor>(��)</span>��ϥߥ�����Ƿ�������������ɽ���Ƥ��ޤ����ݥ���Ȥ����Ϥ����Ϥ������������Τ�Ⱦʬ���û�����ޤ���<BR>ST�ߥ�����Ƿ������������Ϥϲû�����ޤ���</p>");
		out("<BR><BR>");
	}
}
&htmlFooter;
#��λ
exit(0);

#���֥롼����---------------------------------------------------------
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
	rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
	return 0 if(!open(IN, "${HdirName}/hakojima.dat"));
  }

  # �ƥѥ�᡼�����ɤߤ���
  $HislandTurn	= int(<IN>);	# �������
  <IN>;	# �ǽ���������(���Ѥ��ʤ��ͤʤΤ��ɤ����Ф�)

  $HislandNumber	= int(<IN>);	# ������
  <IN>;	# ���˳�����Ƥ�ID(���Ѥ��ʤ��ͤʤΤ��ɤ����Ф�)

  # ����ɤߤ���
  my($i);
  for($i = 0; $i < $HislandNumber; $i++) {
	$Hislands[$i] = readIsland();
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
  my($id,$name);
  $name = <IN>;
  $name =~ /(.*),(.*)/;	# ���̾��
  $name = $1;
  $id = int(<IN>);# ID�ֹ�

  # �ե�����ݥ��󥿤�ʤ������ʤΤ�name,ID�ʳ����ͤ��Ǽ���ʤ�
  <IN>;	# ������̾
  <IN>;	# ����
  <IN>;	# Ϣ³��ⷫ���
  <IN>;	# ������
  <IN>;	# �Ź沽�ѥ����
  <IN>;	# ���
  <IN>;	# ����
  <IN>;	# �͸�
  <IN>;	# ����
  <IN>;	# ����
  <IN>;	# ŷ��
  <IN>;	# ����
  <IN>;	# ��
  <IN>;	# �η���;
  <IN>;	# ������
  <IN>;	# �ܿ���
  my $turnsu   = <IN>; # ���ۤ������������Υ������,�����,���ϥ�����
  my @hturn = split(/,/, $turnsu);
  <IN>;	# 
  <IN>;	# �ߥ�����ȯ�Ͳ�ǽ��
  <IN>;	# ȯ�ͥߥ��������
  <IN>;	# �ץ쥼���
  <IN>;	# �и�������
  <IN>;	# �����
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
#	�ؿ�̾ : calcKillPoint
#	����ǽ : ���÷���ݥ���Ȥ�׻�
#	������ : �ʤ�
#	����� : 0 - �ե����륪���ץ󥨥顼
#	         1 - ����
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
	# �����ܤ���Ͽ����Ƥ�����ä�������
	while($HmonsterName[$i] ne $monster && $i <= $HmonsterNumber){
	  $i++;
	}
	if($id1 ne $id2){
	  #¾��β��ä����
	  $HkillExtPoint[$num][$i]++;
	  $HtotalPoint[$num] += $HmonsterPoint[$i] * $ExternalRate;
	}else{
	  $HkillPoint[$num][$i]++;
	  $HtotalPoint[$num] += $HmonsterPoint[$i];
	}
  }
  close(LIN);

  # ������
  my @idx = (0..$HislandNumber);
  @idx = sort { $HtotalPoint[$b] <=> $HtotalPoint[$a] || $a <=> $b } @idx;
  @HtotalPoint = @HtotalPoint[@idx];
  @HkillPoint = @HkillPoint[@idx];
  @HkillExtPoint = @HkillExtPoint[@idx];
  @Kisland = @Hislands[@idx];

  return 1;
}
#---------------------------------------------------------------------
#	�ؿ�̾ : calcMoney
#	����ǽ : �����޶�η׻�
#	������ : �ʤ�
#	����� : 0 - �ե����륪���ץ󥨥顼
#	         1 - ����
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
  
  # ������
  my @idx = (0..$HislandNumber);
  @idx = sort { $HtotalMoney[$b] <=> $HtotalMoney[$a] || $a <=> $b } @idx;
  @HtotalMoney = @HtotalMoney[@idx];
  @HeachMoney  = @HeachMoney[@idx];
  @Misland = @Hislands[@idx];

  return 1;
}
#---------------------------------------------------------------------
#	�ؿ�̾ : calcBumon
#	����ǽ : ����ޤη׻�
#	������ : �ʤ�
#	����� : 0 - �ե����륪���ץ󥨥顼
#	         1 - ����
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
  
  # ������
  my @idx = (0..$HislandNumber);
  @idx = sort { $HtotalBumon[$b] <=> $HtotalBumon[$a] || $a <=> $b } @idx;
  @HtotalBumon = @HtotalBumon[@idx];
  @HeachBumon  = @HeachBumon[@idx];
  @Bisland = @Hislands[@idx];

  return 1;
}
#---------------------------------------------------------------------
#	�ؿ�̾ : calcShip
#	����ǽ : �������ݥ���Ȥ�׻�
#	������ : �ʤ�
#	����� : 0 - �ե����륪���ץ󥨥顼
#	         1 - ����
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

	# �������ͤ��ä���Ȥꤢ������±���ˤ��Ȥ�
	$ship = 0 if($ship >= $HshipNumber);
	if($id2 == 99){
	  #�ߥ�����Ƿ���
	  $HSkillExtPoint[$num][$ship]++;
	  $HStotalPoint[$num] += $HshipPoint[$ship] * $ExternalSRate;
	}else{
	  $HSkillPoint[$num][$ship]++;
	  $HStotalPoint[$num] += $HshipPoint[$ship];
	}
  }
  close(LIN);

  # ������
  my @idx = (0..$HislandNumber);
  @idx = sort { $HStotalPoint[$b] <=> $HStotalPoint[$a] || $a <=> $b } @idx;
  @HStotalPoint = @HStotalPoint[@idx];
  @HSkillPoint = @HSkillPoint[@idx];
  @HSkillExtPoint = @HSkillExtPoint[@idx];
  
  @Sisland = @Hislands[@idx];

  return 1;
}
#---------------------------------------------------------------------
#	�ؿ�̾ : out
#	����ǽ : ʸ�������ɤ�shift jis��ɸ����Ϥ˥����ȥץå�
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub out {
  print STDOUT jcode::sjis($_[0]);
}

#---------------------------------------------------------------------
#	�ؿ�̾ : htmlHeader
#	����ǽ : HTML�Υإå���ʬ�����
#	������ : �ʤ�
#	����� : �ʤ�
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
<A HREF="$bye">[���]</A></DIV>
END
}
#---------------------------------------------------------------------
#	�ؿ�̾ : htmlFooter
#	����ǽ : HTML�Υեå���ʬ�����
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub htmlFooter {
	my($uti, $sti, $cuti, $csti) = times();
	$uti += $cuti;
	$sti += $csti;
	my($cpu) = $uti + $sti;
	out(<<END);
<P>
�ɤΥ�󥭥󥰤���٤�ʣ�������븽�ݤ����ޤ�ȯ�����ޤ����������Ϻ���ʰ٥�����Ǥ�館��ܡ��ʥ����ȹͤ��Ƥ���������<BR>
$HislandTurn���������($start_turn�����󤫤�ǡ��������)<BR></P><BR>
<DIV align="right"><SMALL>CPU($cpu) : user($uti) system($sti)</SMALL></DIV>
<P><I><A HREF="http://club.www.infoseek.co.jp/club.asp?cid=j1100037">Scripted By Watson</A></I></P>
<P></DIV></DIV>
</BODY></HTML>
END
}
#---------------------------------------------------------------------
#	�ؿ�̾ : htmlKillMonster
#	����ǽ : HTML�β��÷�����ʬ�����
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub htmlKillMonster {
  my($i, $j);
  out(<<END);
$headKill
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=100% BGCOLOR="#000000"><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<TR>
<TD $headPointCellcolor NOWRAP>&nbsp;</TD>
<TD $headPointCellcolor NOWRAP>�ݥ����</TD>
END
  for($i = 1; $i <= $HmonsterNumber; $i++){
	out("<TD $headPointCellcolor NOWRAP>$HmonsterPoint[$i]</TD>\n");
  }
  out("<TD $headPointCellcolor NOWRAP>$HmonsterPoint[0]</TD></TR>\n");
  out("<TR><TD $headNameCellcolor NOWRAP>���̾��</TD>\n");
  out("<TD $headNameCellcolor NOWRAP><span $TotalPointColor>�ݥ����</span></TD>");
  for($i = 1; $i <= $HmonsterNumber; $i++){
	out("<TD $headNameCellcolor NOWRAP><IMG SRC=\"$HmonsterImage[$i]\" width=24 height=24 ALT=\"$HmonsterName[$i]\" TITLE=\"$HmonsterName[$i]\"></TD>\n");
  }
  
  out("<TD $headNameCellcolor NOWRAP><IMG SRC=\"$HmonsterImage[0]\" width=24 height=24 ALT=\"$HmonsterName[0]\" TITLE=\"$HmonsterName[0]\"></TD></TR>\n");
#�����ޤǤ�ɽ�Υإå���ʬ

  for($i = 0; $i < $HislandNumber; $i++){
	out("<TR><TD $nameCellcolor NOWRAP>$Kisland[$i]->{'name'}��</TD>\n");
	if($HtotalPoint[$i]){
	  # �ȡ�����ݥ���Ȥ��û�����Ƥ�����
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HtotalPoint[$i]</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	for($j = 1; $j <= $HmonsterNumber; $j++){
	  if($HkillExtPoint[$i][$j]){
		# ��ʬ����β��� �� ¾����β��ä����
		out("<TD $pointCellcolor NOWRAP>$HkillPoint[$i][$j]<span $ExternalPointColor>($HkillExtPoint[$i][$j])</span></TD>\n");
	  } elsif($HkillPoint[$i][$j]){
		# ��ʬ����β��ä��������
		out("<TD $pointCellcolor NOWRAP>$HkillPoint[$i][$j]</TD>\n");
	  } else {
		# �ʤ�
		out("<TD></TD>\n");
	  }
	}
	# �ᥫ���Τ���
	if($HkillExtPoint[$i][0]){
	  # ��ʬ����β��� �� ¾����β��ä����
	  out("<TD $pointCellcolor NOWRAP>$HkillPoint[$i][0]<span $ExternalPointColor>($HkillExtPoint[$i][0])</span></TD>\n");
	} elsif($HkillPoint[$i][0]){
	  # ��ʬ����β��ä��������
	  out("<TD $pointCellcolor NOWRAP>$HkillPoint[$i][0]</TD>\n");
	} 	else {
	  # �ʤ�
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
#	�ؿ�̾ : htmlMoney
#	����ǽ : HTML�γ����޶�����
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub htmlMoney {
  my($i);
  out(<<END);
$headMoney
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=100% BGCOLOR="#000000"><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<TR>
<TD $headNameCellcolor NOWRAP>���̾��</TD>
<TD $headNameCellcolor NOWRAP><span $TotalPointColor>������޶��</span></TD>
<TD $headNameCellcolor NOWRAP>���÷���</TD>
<TD $headNameCellcolor NOWRAP>��¢����</TD>
<TD $headNameCellcolor NOWRAP>������</TD>
<TD $headNameCellcolor NOWRAP>����</TD>
<TD $headNameCellcolor NOWRAP>������</TD>
<TD $headNameCellcolor NOWRAP>�ȥ���</TD>
</TR>
END
  for($i = 0; $i < $HislandNumber; $i++){
	out("<TR><TD $nameCellcolor NOWRAP>$Misland[$i]->{'name'}��</TD>\n");
	if($HtotalMoney[$i]){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HtotalMoney[$i]$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	if($HeachMoney[$i]{'���÷���'}){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HeachMoney[$i]{'���÷���'}$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	if($HeachMoney[$i]{'��¢��'}){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HeachMoney[$i]{'��¢��'}$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	if($HeachMoney[$i]{'����'}){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HeachMoney[$i]{'����'}$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	if($HeachMoney[$i]{'����'}){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HeachMoney[$i]{'����'}$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	if($HeachMoney[$i]{'������'}){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HeachMoney[$i]{'������'}$HunitMoney</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	if($HeachMoney[$i]{'�ȥ���'}){
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HeachMoney[$i]{'�ȥ���'}$HunitMoney</span></TD>\n");
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
#	�ؿ�̾ : htmlBumon
#	����ǽ : HTML������ޤ����
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub htmlBumon {
  my($i);
  out(<<END);
$headBumon
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=100% BGCOLOR="#000000"><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<TR>
<TD $headNameCellcolor NOWRAP>���̾��</TD>
<TD $headNameCellcolor NOWRAP><span $TotalPointColor>������޿�</span></TD>
END
  for($i = 1; $i <= $HturnPrizeNumber; $i++){
	out("<TD $headNameCellcolor NOWRAP><IMG SRC=\"Vprize${i}.gif\">${HprizeV[$i]}</TD>\n");
  }
  out("</TR>");
  for($i = 0; $i < $HislandNumber; $i++){
	out("<TR><TD $nameCellcolor NOWRAP>$Bisland[$i]->{'name'}��</TD>\n");
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
#	�ؿ�̾ : htmlShip
#	����ǽ : HTML����������ʬ�����
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub htmlShip {
  my($i);
  out(<<END);
$headShip
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=100% BGCOLOR="#000000"><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<TR>
<TD $headPointCellcolor NOWRAP>&nbsp;</TD>
<TD $headPointCellcolor NOWRAP>�ݥ����</TD>
END
  for($i = 0; $i < $HshipNumber; $i++){
	next if(($i > 3) && ($i < 6));
	out("<TD $headPointCellcolor NOWRAP>$HshipPoint[$i]</TD>\n");
  }
  out("<TR><TD $headNameCellcolor NOWRAP>���̾��</TD>\n");
  out("<TD $headNameCellcolor NOWRAP><span $TotalPointColor>�ݥ����</span></TD>");
  for($i = 0; $i < $HshipNumber; $i++){
	next if(($i > 3) && ($i < 6));
	out("<TD $headNameCellcolor NOWRAP><IMG SRC=\"$HshipImage[$i]\" ALT=\"$HshipName[$i]\" TITLE=\"$HshipName[$i]\"></TD>\n");
  }
#�����ޤǤ�ɽ�Υإå���ʬ
  for($i = 0; $i < $HislandNumber; $i++){
	out("<TR><TD $nameCellcolor NOWRAP>$Sisland[$i]->{'name'}��</TD>\n");
	if($HStotalPoint[$i]){
	  # �ȡ�����ݥ���Ȥ��û�����Ƥ�����
	  out("<TD $pointCellcolor NOWRAP><span $TotalPointColor>$HStotalPoint[$i]</span></TD>\n");
	} else {
	  out("<TD></TD>\n");
	}
	for($j = 0; $j < $HshipNumber; $j++){
	  next if(($j > 3) && ($j < 6));
	  if($HSkillExtPoint[$i][$j]){
		# ���Ƿ��� �� �ߥ�����Ƿ���
		out("<TD $pointCellcolor NOWRAP>$HSkillPoint[$i][$j]<span $ExternalPointColor>($HSkillExtPoint[$i][$j])</span></TD>\n");
	  } elsif($HSkillPoint[$i][$j]){
		# ���Ƿ����Τ�
		out("<TD $pointCellcolor NOWRAP>$HSkillPoint[$i][$j]</TD>\n");
	  } else {
		# �ʤ�
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

