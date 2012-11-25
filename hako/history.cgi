#!/usr/local/bin/perl --

#---------------------------------------------------------------------
#	�Ƕ�ν�����ȺǶ��ŷ���������ɽ��
#
#	������ : 2001/11/25 V0.10
#	������ : �饹�ƥ���
#
#	��������
#	2001/12/31 V0.20 �������������̥ե����뤫�������褦�ˤ�����
#	2002/04/20 V0.30 ��ɽ�Υ��������ɽ������������ѹ������ɽ�����դ�����
#	2002/08/15 V0.40 ���ץե�����ɽ����ǽ�ɲá�
#	2002/09/18 V0.41 �����դ�����פ��ɲá�
#	2002/10/29 V0.50 �������륷�����դ��ŷ���ե�����ɽ�������
#	2003/05/05 V0.60 ���ۤ�Ȣ�����ͤ˽�����
#	2003/09/15 V0.70 ŷ����������ɽ�����礴�Ȥ�������������ߡ�neo_otacky���󤢤꤬�Ȥ���
#	2003/10/26 V0.80 ������̿���ɽ�����رĤ�����ɽ���������������̥ե������ʬΥ
#---------------------------------------------------------------------
#---------------------------------------------------------------------
#	�������
#---------------------------------------------------------------------
require './hako-init.cgi';
require './hako-io.cgi';
require './init-game.cgi';

#----------------------------
#	HTML�˴ؤ�������
#----------------------------
# �֥饦���Υ����ȥ�С���̾��
$title = '�Ƕ�ν������ŷ��';

# ���̤ο����طʤ�����(HTML)
$body = '<body>';

# ���̤Ρ����ץ����(URL)
$bye = $HthisFile;

# �Ƕ��ŷ���ο�°��
$headNameCellcolor	= 'class=headNameCellcolor';# �Ƕ��ŷ���Υإå���ʬ�Υ��뿧
$pointCellcolor		= 'class=pointCellcolor';	# �Ƕ��ŷ����ŷ����ʬ�Υ��뿧
$nameCellcolor		= 'class=nameCellcolor';	# �Ƕ��ŷ������̾��ɽ����ʬ�Υ��뿧

$tomorrowColor		= 'class=TomorrowColor';	# �Ƕ��ŷ���������ʹߤ�ʸ����
$todayColor			= 'class=TodayColor';		# �Ƕ��ŷ���κ�����ʸ����
$yesterdayColor		= 'class=YesterdayColor';	# �Ƕ��ŷ���κ���������ʸ����

#�ᥤ��롼����-------------------------------------------------------

&cookieInput();
&cgiInput;
if (-e $HpasswordFile) {
	# �ѥ���ɥե����뤬����
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword  = <PIN>); # �ޥ����ѥ���ɤ��ɤ߹���
	chomp($HspecialPassword = <PIN>); # �ü�ѥ���ɤ��ɤ߹���
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
		# ŷ��
		&logTenki();
	} elsif($HMode == 200) {
		# ����
		&logStatistical();
	} elsif($HMode == 300) {
		# ������̿��
		&tempCommandLate();
	} elsif($HMode == 400) {
		# �ر�����
		&tempAlly();
#	} elsif($HMode =~ /([0-9]*)/) {
	} else {
		# �Ƕ�ν����
		&logDekigoto();
		if($HMode == 99){
			if($HcurrentID == 0) {
				&logFilePrintAll();
			} else {
				&tempIslandHeader($HcurrentID, $HcurrentName);
				# �ѥ����
				if(&checkPassword($island, $HinputPassword) && ($HcurrentID eq $defaultID)) {
					&logPrintLocal(1);
				} else {
					# password�㤦
					&logPrintLocal(0);
				}
			}
		} else {
			if($HcurrentID == 0) {
				&logFilePrint($HMode, $HcurrentID, 0);
			} else {
				&tempIslandHeader($HcurrentID, $HcurrentName);
				# �ѥ����
				if(&checkPassword($island, $HinputPassword) && ($HcurrentID eq $defaultID)) {
					&logFilePrint($HMode, $HcurrentID, 1);
				} else {
					# password�ְ㤤
					&logFilePrint($HMode, $HcurrentID, 0);
				}
			}
		}
		print("<hr>\n");
#	} else {
#		# ŷ��
#		&logTenki();
	}
	print("</DIV>\n");
}
&tempFooter;
#��λ
exit(0);

#���֥롼����---------------------------------------------------------
#---------------------------------------------------------------------
#       �ؿ�̾ : htmlError
#       ����ǽ : HTML�Υ��顼��å������ν���
#       ������ : �ʤ�
#       ����� : �ʤ�
#---------------------------------------------------------------------
sub htmlError{
	print("<h2>���顼��ȯ�����ޤ���</h2>\n");
}
#---------------------------------------------------------------------
#       �ؿ�̾ : readIslandsFile
#       ����ǽ : ����Υǡ������ɤ߹���
#       ������ : �ʤ�
#       ����� : 0 - �ե����륪���ץ�˼���
#               1 - ����
#---------------------------------------------------------------------
sub readIslandsFile {
	# �ǡ����ե�����򳫤�
	if(!open(IN, "${HdirName}/hakojima.dat")) {
		rename("${HdirName}/hakojima.tmp", "${HdirName}/hakojima.dat");
		return 0 if(!open(IN, "${HdirName}/hakojima.dat"));
	}
	# �ƥѥ�᡼�����ɤߤ���
	$HislandTurn  = int(<IN>);    # �������
	<IN>; # �ǽ���������(���Ѥ��ʤ��ͤʤΤ��ɤ����Ф�)
	$HislandNumber        = int(<IN>);    # ������
	<IN>; # ���˳�����Ƥ�ID(���Ѥ��ʤ��ͤʤΤ��ɤ����Ф�)
	# ����ɤߤ���
	my($i, $id);
	for($i = 0; $i < $HislandNumber; $i++) {
		$Hislands[$i] = readIsland($i);
		$HidToNumber{$Hislands[$i]->{'id'}} = $i;
	}
	# �ե�������Ĥ���
	close(IN);
	readCommandLate();
	return 1;
}
#---------------------------------------------------------------------
#       �ؿ�̾ : readIsland
#       ����ǽ : ����˳�����Ƥ��Ƥ���ID�����
#       ������ : 0 .. $HislandNumber
#       ����� : ���ID
#---------------------------------------------------------------------
sub readIsland {
	my($num) = @_;
	my($id, $name, $wline, $weather, $pastweather);
	$name = <IN>;
	$name =~ /(.*),(.*)/; # ���̾��
	$name = $1;
	$id = int(<IN>);# ID�ֹ�
	# �ե�����ݥ��󥿤�ʤ������ʤΤ�name,ID�ʳ����ͤ��Ǽ���ʤ�
	for($i = 2; $i < 12; $i++) {
		<IN>;
	}
	$wline = <IN>;  # ŷ��
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
#	POST or GET�����Ϥ��줿�ǡ�������
#--------------------------------------------------------------------
sub cgiInput {
	my($line, $getLine);

	# ���Ϥ������ä����ܸ쥳���ɤ�EUC��
	$line = <>;
	$line =~ tr/+/ /;
#	$line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$line =~ s/%([a-fA-F0-9]{2})/pack(H2, $1)/eg;
#	$line = jcode::euc($line);
	jcode::convert(\$line, 'euc');
	$line =~ s/[\x00-\x1f\,]//g;

	# GET�Τ�Ĥ�������
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
#cookie����
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
#	HTML�Υإå��ȥեå���ʬ�����
#---------------------------------------------------------------------
# �إå�
sub tempHeader {
#	print qq{Content-type: text/html; charset=Shift_JIS\n\n};
	print qq{Content-type: text/html; charset=EUC-JP\n\n};
	print qq{<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n\n};
	$HskinName = ($HskinName ne '') ? "$imageDir/$HskinName" : "$imageDir/$HcssFile";
	print(<<END);
<html lang="ja">
<!--������-->
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
<A HREF="$bye">[���]</A>��
<B>[�Ƕ�ν����]</B>��<A HREF="history.cgi?saikin=99">[ALL]</A>
END
	my($i, $turn);
	for($i = 0;$i < $HtopLogTurn;$i++) {
		$turn = $HislandTurn - $i;
		return unless($turn > 0);
		print("<A HREF='history.cgi?saikin=${i}'>");
		if($i == 0) {
			print("[������${turn}(����)]");
		} else {
			print("[${turn}]");
		}
		print("</A>\n");
	}
	my $tmp = "";
	if($Hallyflg){
		$tmp = "<A HREF=\"history.cgi?ally=0\">[�رĤ�����]</A>";
	}
	print(<<END);
<SELECT NAME="ID">$HislandList</SELECT>
<INPUT type=hidden name=PASSWORD value=$HinputPassword>
<INPUT type="submit" value="�򸫤�">
</FORM><HR>
<A HREF="history.cgi?tenki=0">[�Ƕ��ŷ��]</A>
<A HREF="history.cgi?commandlate=0">[������̿��]</A>
$tmp
<A HREF="history.cgi?statistical=0">[���� ALL]</A>
<A HREF="history.cgi?statistical=30">[���ף��礢����]</A>
<HR></DIV>
END
}
# �եå�
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
#	ŷ���ե�����ɽ��
#---------------------------------------------------------------------
sub logTenki {
	my($i, $j, $name, $turn);
	print(<<END);
<H1>�Ƕ��ŷ��</H1>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=0 WIDTH=100% BGCOLOR="#000000"><TR><TD>
<TABLE BORDER=0 CELLPADDING=1 CELLSPACING=1 WIDTH=100%>
<TR><TD $headNameCellcolor rowspan=2 NOWRAP>���̾��</TD>
<TD $headNameCellcolor colspan=3 NOWRAP><span $tomorrowColor>ͽ��</span></TD>
END
for($i = 0; $i < 11; $i++) {
	$turn = $HislandTurn - $i;
	next if($turn < 1);
	print("<TD $headNameCellcolor rowspan=2 NOWRAP>");
	if($i == 0) {
		print("<nobr><span $todayColor>������${turn}<br>(����)</nobr>");
	} else {
		print("${turn}");
	}
	print("</TD>");
}
print("</TR><TR>");
$turn = $HislandTurn + 3;
print("<TD $headNameCellcolor NOWRAP>$turn<br><small>(������)</small></TD>");
$turn--;
print("<TD $headNameCellcolor NOWRAP>$turn<br><small>(����)</small></TD>");
$turn--;
print("<TD $headNameCellcolor NOWRAP>$turn<br><small>(����)</small></TD></TR>");
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
#	ŷ���ξ���
#---------------------------------------------------------------------
sub weatherinfo {
	my($lv) = @_;

	$lv = 1114 if($lv > 5559); # �����ʿ����λ�

	# ��������ŷ��
	my($kind3) = int($lv / 1000);
	$kind3 = 1 if($kind3 >= 6); # �����ʿ����λ�

	my($lv2) = $lv - ($kind3 * 1000);

	# ������ŷ��
	my($kind2) = int($lv2 / 100);
	$kind2 = 1 if($kind2 >= 6); # �����ʿ����λ�

	my($lv3) = $lv2 - ($kind2 * 100);

	# ŷ��
	my($kind) = int($lv3 / 10);
	$kind = 1 if($kind >= 6); # �����ʿ����λ�

	my($name) = $WeatherName[$kind];# ̾��
	my($hp) = $lv3 - ($kind * 10);# ���פξ���
	return ($kind, $name, $hp, $kind2, $kind3);
}
#---------------------------------------------------------------------
#	���ץե�����ɽ��
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
		print("�ޤ��ǡ���������ޤ���\n");
		return;
	}
	my $gimage = "$imageDir/graph.gif";
	my $oneisland = ($Graph >= 30) ? "(���礢����)" : "";
	print(<<END);
<H1>���ۤ�Ȣ������${oneisland}</H1>
<TABLE border=1><TR><TH $HbgTitleCell>������</TH><TH $HbgTitleCell>��͸�</TH><TH $HbgTitleCell>����</TH><TH $HbgTitleCell>������</TH><TH $HbgTitleCell>���¶�</TH><TH $HbgTitleCell>��ߥ�����ȯ�Ϳ�</TH><TH $HbgTitleCell>������</TH><TH $HbgTitleCell>����</TH><TH $HbgTitleCell>����</TH><TH $HbgTitleCell>���ܿ�</TH><TH $HbgTitleCell>����</TH><TH $HbgTitleCell>��ο�</TH></TR>
END
	my(@tdata,$title,@ld);
	foreach $l (@line) {
		@ld = split(/,/, $l);
		if($Graph >= 30){
			# ���礢����
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
			$title = "�ο�ܤΥ����(���礢����)";
		}else{
			$title = "�ο�ܤΥ����";
		}
		if($Graph == 1){
			$title = "��͸�${title}";
			push(@tdata, int(@ld[1]/100));
		}elsif($Graph == 2){
			$title = "����${title}";
			push(@tdata, int(@ld[2]/1000));
		}elsif($Graph == 3){
			$title = "������${title}";
			push(@tdata, @ld[3]);
		}elsif($Graph == 4){
			$title = "���¶�${title}";
			push(@tdata, @ld[4]);
		}elsif($Graph == 5){
			$title = "��ߥ�����ȯ�Ϳ�${title}";
			push(@tdata, int(@ld[5]/10));
		}elsif($Graph == 6){
			$title = "������${title}";
			push(@tdata, int(@ld[6]/10));
		}elsif($Graph == 7){
			$title = "����${title}";
			push(@tdata, int(@ld[7]/10));
		}elsif($Graph == 8){
			$title = "����${title}";
			push(@tdata, int(@ld[8]/10));
		}elsif($Graph == 9){
			$title = "���ܿ�${title}";
			push(@tdata, int(@ld[9]/10));
		}elsif($Graph == 10){
			$title = "����${title}";
			push(@tdata, int(@ld[10]/10));
		}elsif($Graph == 31){
			$title = "��͸�${title}";
			push(@tdata, int(@ld[1]/5));
		}elsif($Graph == 32){
			$title = "����${title}";
			push(@tdata, int(@ld[2]/50));
		}elsif($Graph == 33){
			$title = "������${title}";
			push(@tdata, int(@ld[3]*10));
		}elsif($Graph == 34){
			$title = "���¶�${title}";
			push(@tdata, int(@ld[4]*10));
		}elsif($Graph == 35){
			$title = "��ߥ�����ȯ�Ϳ�${title}";
			push(@tdata, int(@ld[5]));
		}elsif($Graph == 36){
			$title = "������${title}";
			push(@tdata, int(@ld[6]));
		}elsif($Graph == 37){
			$title = "����${title}";
			push(@tdata, int(@ld[7]));
		}elsif($Graph == 38){
			$title = "����${title}";
			push(@tdata, int(@ld[8]));
		}elsif($Graph == 39){
			$title = "���ܿ�${title}";
			push(@tdata, int(@ld[9]));
		}elsif($Graph == 40){
			$title = "����${title}";
			push(@tdata, int(@ld[10]));
		}

		my $allPop = (@ld[1] eq '') ? "��" : "@ld[1]ɴ��";
		my $allMoney = (@ld[2] eq '') ? "��" : "@ld[2]����";
		my $allArea = (@ld[3] eq '') ? "��" : "@ld[3]ɴ����";
		my $allBank = (@ld[4] eq '') ? "��" : "@ld[4]�鲯";
		my $allMissileA = (@ld[5] eq '') ? "��" : "@ld[5]ȯ";
		my $allFarm		= (@ld[6] eq '') ? "��" : "@ld[6]�鵬��";
		my $allTower	= (@ld[7] eq '') ? "��" : "@ld[7]�鵬��";
		my $allIndustry = (@ld[8] eq '') ? "��" : "@ld[8]�鵬��";
		my $allYousyoku= (@ld[9] eq '') ? "��" : "@ld[9]ɴɤ";
		my $allForest  = (@ld[10] eq '') ? "��" : "@ld[10]ɴ��";
		my $islandNumber = (@ld[11] eq '') ? "��" : "@ld[11]$AfterName";
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
�������ɽ��[����]
<A HREF="history.cgi?statistical=1#graph">[��͸�]</A>
<A HREF="history.cgi?statistical=2#graph">[����]</A>
<A HREF="history.cgi?statistical=3#graph">[������]</A>
<A HREF="history.cgi?statistical=4#graph">[���¶�]</A>
<A HREF="history.cgi?statistical=5#graph">[��ߥ�����ȯ�Ϳ�]</A>
<A HREF="history.cgi?statistical=6#graph">[������]</A>
<A HREF="history.cgi?statistical=7#graph">[����]</A>
<A HREF="history.cgi?statistical=8#graph">[����]</A>
<A HREF="history.cgi?statistical=9#graph">[���ܿ�]</A>
<A HREF="history.cgi?statistical=10#graph">[����]</A><HR>
�������ɽ��[����]
<A HREF="history.cgi?statistical=31#graph">[��͸�]</A>
<A HREF="history.cgi?statistical=32#graph">[����]</A>
<A HREF="history.cgi?statistical=33#graph">[������]</A>
<A HREF="history.cgi?statistical=34#graph">[���¶�]</A>
<A HREF="history.cgi?statistical=35#graph">[��ߥ�����ȯ�Ϳ�]</A>
<A HREF="history.cgi?statistical=36#graph">[������]</A>
<A HREF="history.cgi?statistical=37#graph">[����]</A>
<A HREF="history.cgi?statistical=38#graph">[����]</A>
<A HREF="history.cgi?statistical=39#graph">[���ܿ�]</A>
<A HREF="history.cgi?statistical=40#graph">[����]</A><HR>
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
#	��ζᶷ�Υ��
#---------------------------------------------------------------------
# �إå�
sub tempIslandHeader {
	my($id, $name) = @_;
	if(&checkPassword($Hislands[$HidToNumber{$id}], $HinputPassword) && ($HcurrentID eq $defaultID)) {
		print("<HR><span class=lbbsOW><B>[${name}�ζᶷ]</B></span>");
	} else {
		print("<HR><B>[${name}�ζᶷ]</B>��");
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
			print("[������${turn}(����)]");
		} else {
			print("[${turn}]");
		}
		print("</A>\n");
	}
	print("<br>\n");
}
#---------------------------------------------------------------------
#	������̿��
#---------------------------------------------------------------------
sub tempCommandLate {
	my($i, $turn, $turn2, $id, $kind, $target, $x, $y, $arg, $x2, $y2, $name, $tName);
	print("<H1>������̿����� ${HislandTurn}������</H1>");
	if($HcomLateCt <= 0){
		print("���ߡ�������̿��Ϥ���ޤ���");
		return;
	}
	print("<TABLE border=1><TR><TH $HbgTitleCell>���⥿����</TH><TH $HbgTitleCell>��Ͽ������</TH><TH $HbgTitleCell>�¹�${AfterName}</TH><TH $HbgTitleCell>̿��</TH><TH $HbgTitleCell>��ɸ${AfterName}</TH><TH $HbgTitleCell>��ɸX</TH><TH $HbgTitleCell>��ɸY</TH><TH $HbgTitleCell>����</TH><TH $HbgTitleCell>��ɸ2X</TH><TH $HbgTitleCell>��ɸ2Y</TH></TR>");
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
			$name = "��";
		}
		$tn = $HidToNumber{$target};
		if($tn ne ''){
			$tIsland = $Hislands[$tn];
			$tName = $tIsland->{'name'} . ${AfterName};
		}else{
			$tName = "��";
		}
		print("<TR><TD>$turn</TD><TD>$turn2</TD><TD>$name</TD><TD>$HcomName[$kind]</TD><TD>$tName</TD><TD>$x</TD><TD>$y</TD><TD>$arg</TD><TD>$x2</TD><TD>$y2</TD></TR>");
	}
	print("</TABLE>\n");
	print("����${AfterName}̾��ɽ������Ƥʤ�̿��ϡ��������Τ���˼¹Ԥ���ޤ���<BR><BR>\n");
}
#---------------------------------------------------------------------
#	�ر�����
#---------------------------------------------------------------------
sub tempAlly {
	my($logturn,$i);
	$allyturn = 'log' if($allyturn == 0);
	print("<H1>�رĤ�����</H1>");
	unless(($Hallyflg) && (open(LIN, "${HlogdirName}/ally.$allyturn"))){
		print("�رĤβ��ǡ�����������ޤ���");
		return;
	}
	print(<<END);
<TABLE BORDER><TR>
<TH $HbgTitleCell>${HtagTH_}������${H_tagTH}</TH>
<TH $HbgTitleCell colspan=100>${HtagTH_}�ꡡͭ��Ψ${H_tagTH}</TH>
</TR>
END
	my($turn, $line, @ally, $apop);
	my(%allyCount,%allyPop,%allyArea,%allyGnp,%allyPow,$amark);
	$turn = 0;
	while($line = <LIN>){
		# ������,�ر�ID,���,��͸�,������,��к���,������
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
			print("<TD $HbgNameCell colspan=$apop>$Hallygroup[$ally[1]]��($ally[7]%)</TD>");
		}else{
			print("<TD $HbgNameCell colspan=$apop>$Hallymark[$ally[1]]${HtagTH_}$Hallygroup[$ally[1]]${H_tagTH}�� ($ally[7]%)</TD>");
		}
	}
	close(LIN);
	print("</TR></TABLE>");
	print("������ͭΨ�ϡ��͸����黻�Ф���ޤ���<br><br>");
	print("���Υǡ�����<A HREF=\"history.cgi?ally=0\">[�ǿ�]</a> ");
	$logturn = $HislandTurn - $HturnPrizeVarious - ($HislandTurn % $HturnPrizeVarious);
	for($i = 0;$i < 5;$i++){
		return if($logturn <= 0);
		print("<A HREF=\"history.cgi?ally=$logturn\">[$logturn]</a> ");
		$logturn -= $HturnPrizeVarious;
	}
}
#---------------------------------------------------------------------
#	���ե����륿���ȥ�
#---------------------------------------------------------------------
sub logDekigoto {
	print(<<END);
<H1>�Ƕ�ν����</H1>
END
}
#---------------------------------------------------------------------
#	���ե���������ɽ��
#---------------------------------------------------------------------
sub logFilePrintAll {
	my($i);
	for($i = 0; $i < $HtopLogTurn; $i++) {
		&logFilePrint($i, 0, 0);
	}
}
#---------------------------------------------------------------------
# ���̥�ɽ��
#---------------------------------------------------------------------
sub logPrintLocal {
	my($mode) = @_;
	my($i);
	for($i = 0; $i < $HtopLogTurn; $i++) {
		&logFilePrint($i, $HcurrentID, $mode);
	}
}
#---------------------------------------------------------------------
#	�ե������ֹ����ǥ�ɽ��
#---------------------------------------------------------------------
sub logFilePrint {
	my($fileNumber, $id, $mode) = @_;
	open(LIN, "${HlogdirName}/hakojima.log$_[0]");
	my($line, $m, $turn, $id1, $id2, $message);
	my($set_turn) = 0;
	while($line = <LIN>) {
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
		($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

		# ��̩�ط�
		if($m == 1) {
			next if(($mode == 0) || ($id1 != $id)); # ��̩ɽ�������ʤ�
			$m = "${HtagNumber_}<B>(��̩)</B>${H_tagNumber}��";
		} else {
			$m = '';
		}

		# ɽ��Ū�Τ�
		if($id != 0) {
			next if(($id != $id1) && ($id != $id2));
		}
		
		if($set_turn == 0){
			print("<NOBR><B>=====[<span class=number><FONT SIZE=4> ������$turn </FONT></span>]================================================</B><NOBR><BR>\n");
			$set_turn++;
		}

		# ɽ��
		print("<NOBR>��${m}${message}</NOBR><BR>\n");
	}
	close(LIN);
}
