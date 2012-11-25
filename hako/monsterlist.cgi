#!/usr/local/bin/perl --

#---------------------------------------------------------------------
#
#	���ۤ�Ȣ�����åХȥ��ѡ�����ɽ��
#
#	������ : 2001/09/16 V0.10
#	������ : �饹�ƥ���
#
#	����������
#	2001/12/23 V0.11 V3.60�Ǥβ����ɲä��б�������
#	2001/12/31 V0.20 ������������config.cgi���������褦�ˤ�����
#	2002/01/13 V0.21 version4�б���
#	2002/02/03 V0.30 CSS���̥ե����뤫���ɤ߹���褦�ˤ�����
#	2002/03/31 V0.31 ��ٷڸ�����Ʈ���ɽ����
#	2002/11/02 V0.40 �������륷�����դ����ɡ������ɲ�
#	2003/09/24 V0.50 ���ۤ�Ȣ���б���
#---------------------------------------------------------------------
#	��������ץȤϰʲ��򸵤˺������ޤ���
#
#	���÷���ݥ���ȡܳ����޶⡡��󥭥�ɽ��
#	������ : Watson
#---------------------------------------------------------------------

#---------------------------------------------------------------------
#	�������
#---------------------------------------------------------------------
# hako-init.cgi��require
require './hako-init.cgi';

# ���̤Ρ����ץ����(URL) $HbaseDir��config.cgi�ǻ��ꡣ
$bye = "$HbaseDir/hako-main.cgi";

# ���ä�ǽ�Ϥ򸵲���ǽ�Ϥ�ޤ��ɽ������Ȥ��ϣ� ��ǽ�ϤΤߤϣ�
$Monshyouzi = 0;

#----------------------------
#	HTML�˴ؤ�������
#----------------------------
# �֥饦���Υ����ȥ�С���̾��
$title = 'Ȣ����� ���åꥹ��';

# ���̤ο����طʤ�����(HTML)
$body = '<body>';

# ��Ƭ�Υ�å�����(HTML��)	 ���÷����󥭥���
$headKill = <<'EOF';
<h2 class=head2>���åХȥ롡���ð���ɽ</h2>
EOF

$HbgTitleCell = 'class=TitleCell';
$HbgInfoCell = 'class=InfoCell';

#�����ޤ�-------------------------------------------------------------

# ����̾
@HmonsterName = 
    (
     '�ᥫ���Τ�',     # 0(��¤)
     '���Τ�',         # 1
     '���󥸥�',       # 2
     '��åɤ��Τ�',   # 3
     '���������Τ�',   # 4
     '���Τ饴������', # 5
     '������',         # 6
     '���󥰤��Τ�',   # 7
     '�᥿�뤤�Τ�',   # 8
     '�������Τ�',     # 9
     '�ǥӥ뤤�Τ�',   # 10
     '�ᥫ����',       # 11(��¤)
 '���󥷥���Ȥ��Τ�', # 12(�ϼ�Ĵ��)
     '�����ƥ�',       # 13(����)
     '��ԥåȤ��Τ�', # 14(����)
     '���Х��쥤',     # 15(�������Ȥ��Ѳ�)
     '���Ω�Ƥ��Τ�', # 16(���˥�����)
     '������ܥ���',   # 17(�ߥ������)
     'ȿ�⤤�Τ�',     # 18(�ߥ������)
     '�������',       # 19(�ߥ������)
     '���ڡ������Τ�', # 20(�ߥ������)
     '������������',   # 21(�ߥ������)
    '����ƥͥ����Τ�',# 22(��¤)
     '���ͥ���',       # 23
     '��å����Τ�',   # 24
     '����ᥫ���Τ�', # 25
     '�º̤��Τ�',     # 26
     'ʬ�����Τ�',     # 27
     '�Ƥ�Ƥ뤤�Τ�', # 28
     '�դ��Ƥ�Ƥ�',   # 29
     '�������Τ�',     # 30
    '������ɥ�������',# 31
     '�������(��)',   # 32
     '�������(��)',   # 33
     '�������(��)',   # 34
     '�������(��)'    # 35
);

# �����ե�����
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
     'land1.gif',     # ����
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

# ���åХȥ���
@HmonsterSP      = ( 7, 4, 1, 7, 7, 3, 2, 7, 6, 0,10, 6, 6, 5, 5, 5, 0, 8, 7, 0, 9, 5, 0, 8, 0, 6, 5, 5, 0, 0,11, 8, 0, 7, 7, 9); # �ü�
                   # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35
@HmonsterSTR     = (10, 7, 7,10, 7, 2, 8,12, 4, 7,13, 3,11, 5, 7, 3, 8,12,15, 9, 9, 9, 7, 5,10,10, 7, 7, 7, 9,11,11, 7, 9,11,11); # ����
@HmonsterDEF     = ( 2, 3, 5, 2, 2, 0, 5, 3, 7, 3, 1, 5, 5, 0, 0, 0, 3, 5, 0, 3, 3, 1, 3, 2, 3, 5, 1, 1, 3, 3, 3, 5, 3, 3, 3, 3); # �ɸ�
@HmonsterAGI     = ( 6, 5, 2, 3, 9,14, 4, 5,11, 5, 5, 1, 2,15,17,19, 6,11, 5, 9,15,20, 5,10,10, 7,15,20, 5, 6, 9,15, 5, 6, 6,14); # ����
@HmonsterSKL     = ( 2, 7, 6, 5, 9, 9, 7, 4, 7, 7,10, 1, 5,10,13,13, 8,12,12, 9,10,16, 7,10,10, 7,12,10, 7, 7, 9,12, 7, 7, 8,12); # ̿��
       #  ��(����)  20 22 20 20 27 25 24 24 29 22 29 10 23 30 37 35 25 40 32 30 37 46 22 27 33 29 35 38 22 25 32 43 22 25 28 40

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
	if(!open(IN, "${HdirName}/hakojima.dat")) {
	  return 0;
	}
  }
  
  # �ƥѥ�᡼�����ɤߤ���
  $HislandTurn	= int(<IN>);	# �������
  
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

	my($id,$name);

	$name = <IN>;
	$name =~ /(.*),(.*)/;	# ���̾��
	$name = $1;
	$id = int(<IN>);# ID�ֹ�

	# �ե�����ݥ��󥿤�ʤ������ʤΤ�name,ID�ʳ����ͤ��Ǽ���ʤ�
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
	
	# ���åХȥ���
	$mons1    = <IN>; # ��ʬ�β���
	$monsurl  = <IN>; # ����URL
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
<a href="$bye">[���]</a></DIV>
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
<p>
���̾���򥯥�å�����ȡ��Ѹ����뤳�Ȥ��Ǥ��ޤ��� <br>
ɽ������Ƥ�����ä�ǽ���ͤϲ��øĿͤ�ǽ�ϤǤ����ºݤ���Ʈ�ˤϸ����ä�ǽ�Ϥ�­����ޤ��� <br>
��Ʈ�ϥ�����ʿ��ͤ����ʤ�����ޤ��Τ�ǽ�Ϥɤ���˾��Ԥ���ޤ�櫓�ǤϤ���ޤ��� <br>
</p>
<DIV align="right"><SMALL>CPU($cpu) : user($uti) system($sti)</SMALL></DIV>
</body></html>
END
}
#---------------------------------------------------------------------
#	�ؿ�̾ : htmlError
#	����ǽ : HTML�Υ��顼��å������ν���
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub htmlError{
	out("<h2 class=head2>���顼��ȯ�����ޤ���</h2>\n");
}
#---------------------------------------------------------------------
#	�ؿ�̾ : monsterlist
#	����ǽ : ���åХȥ롡���ð���ɽ����
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub monsterlist {
	my($island) = $Hislands[$_[0]];

	my($id,$name,$monster) = ($island->{'id'},$island->{'name'},$island->{'monster'});
	my($MBsId,$MBmId) = ($monster->[3],$monster->[4]);

	my($tn) = $HidToNumber{$monster->[2]};
	my($tMonster,$tIsland,$tName,$tMBsId, $tMBmId);

	if($tn eq '') {
	} else {
		# ������꤬����Ȥ�
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
			$MBidName = "����";
		} else {
			$MBidName = "$MBidName$AfterName��<br>$tMonster->[1]��<b>��Ʈ��</b>";;
		}
	}

	# ���ò�������
	my $image = $HmonsterImage[$MBmId];
	my $special = $HmonsterSpecial[$MBmId];
	# �Ų���?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
		(($special == 4) && (($HislandTurn % 2) == 0))) {
		$image = $HmonsterImage2[$MBmId];
	}
	$image = $island->{'monsurl'} if(substr($island->{'monsurl'},0,7) eq 'http://');
	
	my $image2 = $HmonsterImage[$tMBmId];
	$special = $HmonsterSpecial[$tMBmId];
	# �Ų���?
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

	$MBmId = ($MBmId == 0) ? "��" : $HmonsterName[$MBmId];
	$MBsId = ($MBsId == 0) ? "̵" : $HmonsterName[$MBsId];
	$tMBmId = ($tMBmId == 0) ? "��" : $HmonsterName[$tMBmId];
	$tMBsId = ($tMBsId == 0) ? "̵" : $HmonsterName[$tMBsId];
	
	if($seityou < 12) {
		$seityou = "��ǯ";
	} elsif($seityou < 25) {
		$seityou = "��ǯ";
	} else {
		$seityou = "Ϸǯ";
	}
	if($tseityou < 12) {
		$tseityou = "��ǯ";
	} elsif($tseityou < 25) {
		$tseityou = "��ǯ";
	} else {
		$tseityou = "Ϸǯ";
	}

	out(<<END);

<tr>
<td $HbgTitleCell align=center>��̾</td>
<td $HbgTitleCell align=center>����̾</td>
<td $HbgTitleCell align=center>����</td>
<td $HbgTitleCell align=center>������</td>
<td $HbgTitleCell align=center>����</td>
<td $HbgTitleCell align=center>���</td>
<td $HbgTitleCell align=center>��Ĺ</td>
<td $HbgTitleCell align=center>HP</td>
<td $HbgTitleCell align=center>����</td>
<td $HbgTitleCell align=center>����</td>
<td $HbgTitleCell align=center>����</td>
<td $HbgTitleCell align=center>̿��</td>
<td $HbgTitleCell align=center>����</td>
<td $HbgTitleCell align=center>��</td>
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
	if($Monshyouzi) { # ���ä�ǽ�Ϥ򸵲���ǽ�Ϥ�ޤ��ɽ��
	out(<<END);
<td $HbgInfoCell align=center>$mSTR($monster->[7])</td>
<td $HbgInfoCell align=center>$mDEF($monster->[8])</td>
<td $HbgInfoCell align=center>$mAGI($monster->[9])</td>
<td $HbgInfoCell align=center>$mSKL($monster->[10])</td>
END
	} else { # ���ä�ǽ�Ϥ�ʬ��ǽ�ϤΤ�ɽ��
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

