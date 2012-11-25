#!/usr/local/bin/perl --
# ���ϥ����С��˹�碌���ѹ����Ʋ�������

#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ���ƥʥ󥹥ġ���(ver1.01)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# ���ۤ�Ȣ��  (ver5.42b)
#----------------------------------------------------------------------

# ������������������������������������������������������������
# �Ƽ�������
# ������������������������������������������������������������
# hako-init.cgi��require
require './hako-init.cgi';

# use Time::Local���Ȥ��ʤ��Ķ��Ǥϡ�'use Time::Local'�ιԤ�ä��Ʋ�������
# ���������������֤��ѹ���'�û�����ѹ�'�����Ǥ��ʤ��ʤ�ޤ���
use Time::Local;

# ����ǡ����Υե�����(exchange.cgi�ǻ��ꤷ�����Ƥ�Ʊ���ˤ���)
$HexchangeFile = "exchange.dat";

# ������������������������������������������������������������
# ������ܤϰʾ�
# ������������������������������������������������������������

# �Ƽ��ѿ�
my($mainMode,$inputPass,$deleteID,$currentID,$ctYear,$ctMon,$ctDate,$ctHour,$ctMin,$ctSec, $mpass1, $mpass2, $spass1, $spass2, $dpass1, $dpass2);

print <<END;
Content-type: text/html

<HTML><HEAD><TITLE>Ȣ����ƥʥ󥹥ġ���</TITLE></HEAD><BODY>
END

cgiInput();

if (-e $HpasswordFile) {
	# �ѥ���ɥե����뤬����
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword = <PIN>); # �ޥ����ѥ���ɤ��ɤ߹���
	close(PIN);
}

if($mainMode eq 'delete') {
	deleteMode() if(passCheck());
} elsif($mainMode eq 'current') {
	currentMode() if(passCheck());
} elsif($mainMode eq 'time') {
	timeMode() if(passCheck());
} elsif($mainMode eq 'stime') {
	stimeMode() if(passCheck());
} elsif($mainMode eq 'new') {
	newMode() if(passCheck());
### ----- add -----
} elsif($mainMode eq 'change') {
	if(passCheck()) {
		if(changeMode()) {
			print <<END;
<FONT SIZE=7>���ǡ����ܹԤ��������ޤ�����</FONT>
END
		} else {
	print <<END;
<FONT SIZE=7>���ǡ����ܹԤ˼��Ԥ��ޤ�����</FONT>
END
		}
	}
} elsif($mainMode eq 'setup') {
	setupMode();
} elsif($mainMode eq 'mente') {
	menteMode() if(passCheck());
} elsif($mainMode eq 'unmente') {
	unmenteMode() if(passCheck());
}
if(($mainMode eq 'admin') && (passCheck())) {
	adminMode();
} else {
	mainMode();
}

print <<END;
</FORM></BODY></HTML>
END

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

sub currentMode {
	myrmtree "${HdirName}";
	mkdir("${HdirName}", $HdirMode);
### ----- add -----
	unless (-e "$HlogdirName") { mkdir($HlogdirName, $HdirMode); }

	opendir(DIN, "${HdirName}.bak$currentID/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		fileCopy("${HdirName}.bak$currentID/$fileName", "${HdirName}/$fileName");
	}
	closedir(DIN);
}

sub deleteMode {
	if($deleteID eq '') {
		myrmtree "${HdirName}";
### ----- add -----
		myrmtree("${HlogdirName}") if(-e "${HlogdirName}");
		myrmtree("${HtempdirName}") if(-e "${HtempdirName}");
		myrmtree("${HprofileDir}") if(-e "${HprofileDir}");
		myrmtree("deldata") if(-e "deldata");
	} else {
		myrmtree "${HdirName}.bak$deleteID";
	}
	unlink "hakojimalockflock";
}

sub newMode {
	mkdir($HdirName, $HdirMode);
### ----- add -----
	mkdir($HlogdirName, $HdirMode);
	mkdir($HprofileDir, $HdirMode);
	unlink($HexchangeFile);

	# ���ߤλ��֤����
	$ENV{'TZ'} = "JST-9";
	my($now) = time;
	$now = $now - ($now % ($HunitTime));

	open(OUT, ">$HdirName/hakojima.dat"); # �ե�����򳫤�
	if($Htournament){
		print OUT "2\n";     # �������2
	}else{
		print OUT "1\n";     # �������1
	}
	print OUT "$now\n";      # ���ϻ���
	print OUT "0\n";         # ��ο�
	print OUT "1\n";         # ���˳�����Ƥ�ID

	# �ե�������Ĥ���
	close(OUT);
	if($Htournament){
		# �ʰץȡ��ʥ���
		open(OUT, ">$HdirName/tournament.dat"); # �ե�����򳫤�
		print OUT "1\n";          # ���ߤ���Ʈ�⡼��
		print OUT "$HyosenTurn\n";# �ڤ��ؤ�������
		print OUT "0\n";          # �������ܤ�
		print OUT "0\n";          # �����󹹿���
		# �ե�������Ĥ���
		close(OUT);
	}

	# ������������
	my($maxOcean) = $HoceanSize * $HoceanSize;
	my(@field, $i, $x, $y, $tm);

	# ��
	for ($i = 0; $i < $maxOcean; $i++) {
		push(@field, $HlandSea);
	}

	# ̵����
	$tm = 0;
	for ($i = 0; $i < $HmaxIsland; $i++) {
		do {
		$x = int(rand(1) * $HoceanSize - 2) + 1;
		$y = int(rand(1) * $HoceanSize - 2) + 1;
		if (++$tm > $maxOcean) {
			# ���襵�������Ф����礬¿������
			print <<END;
<H1>���顼ȯ��</H1>
<B>������֤˼��Ԥ��ޤ�����</B><BR><BR>
���襵�������Ф����礬¿�����ޤ���<BR>
���ٻ�ߤƤ�������������ԤäƤ⼺�Ԥ�����ϡ�<BR>
����򹭤��뤫����򸺤餷�Ƥ���������<BR>
END
			exit(0);
		}
		} until (countAroundSea(\@field, $x, $y) >= 6);

		$field[$y * $HoceanSize + $x] = 71; # ɬ��$HlandOcean��Ʊ���ˤ��뤳��
	}

	# �ޥåץǡ�������
	open(IOUT, ">$HdirName/submap.1"); # ����ޥåץե�����򳫤�
	for ($i = 0; $i < $maxOcean; $i++) {
		$HcurrentField = $field[$i];
		$HcurrentX = $i % $HoceanSize;
		$HcurrentY = int($i / $HoceanSize);
		printf IOUT ("%02x%04x%02x%04x%02x", $HcurrentField, 0, 0, 0, 0);
		print IOUT "\n" if($HcurrentX == $HoceanSize-1);
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
	# ������Ǽ���
	for($i = 0; $i < $HlbbsMax; $i++) {
		print IOUT "0<<0>>\n";
	}
	close(IOUT);
	print <<END;
<H1><A href="hako-main.cgi?Ocean=0" target="_blank">������ǧ����</A></H1>
�Фä����֤ˤʤäƤ�����ϡ��ǡ����������Ƥ�����ľ���Ƥ���������<BR>
<HR>
END
if($Htournament){
	print "<H1>�ʰץȡ��ʥ��ȵ�ǽ�ϡ��ǽ餫�饿���󣲤ˤʤäƤ��ޤ���</H1>";
	print "�����󹹿����Թ�塢�����󣲤���Ϥ�Ƥ���������<HR>";
}
}

sub setupMode {
	if(!($mpass1 && $mpass2) || ($mpass1 ne $mpass2)) {
		print "${HtagBig_}�ޥ����ѥ���ɤ����Ϥ���Ƥ��ʤ����ְ�äƤ��ޤ�${H_tagBig}";
		return;
	}
	if(!($spass1 && $spass2) || ($spass1 ne $spass2)) {
		print "${HtagBig_}�ü�ѥ���ɤ����Ϥ���Ƥ��ʤ����ְ�äƤ��ޤ�${H_tagBig}";
		return;
	}
#	if(!($dpass1 && $dpass2) || ($dpass1 ne $dpass2)) {
#		print "${HtagBig_}ľ��ȯ�⡼�ɥѥ���ɤ����Ϥ���Ƥ��ʤ����ְ�äƤ��ޤ�${H_tagBig}";
#		return;
#	}
	if(-e $HpasswordFile) {
		# �������ƥ����ۡ���Υ����å�
		print "${HtagBig_}���Ǥ˥ѥ���ɤ����ꤵ��Ƥ��ޤ�${H_tagBig}";
		return;
	}

	$mpass1 = crypt($mpass1, 'ma');
	$spass1 = crypt($spass1, 'sp');
#	$dpass1 = crypt($dpass1, 'dp');

	open(OUT, ">$HpasswordFile") || die $!;
	print OUT <<END;
$mpass1
$spass1
END
#$dpass1
	close(OUT);
	print "${HtagBig_}�ѥ���ɤ����ꤷ�ޤ���${H_tagBig}";
}


sub timeMode {
	$ctMon--;
	$ctYear -= 1900;
	$ctSec = timelocal($ctSec, $ctMin, $ctHour, $ctDate, $ctMon, $ctYear);
	stimeMode();
}

sub stimeMode {
	my($t) = $ctSec;
	open(IN, "${HdirName}/hakojima.dat");
	my(@lines);
	@lines = <IN>;
	close(IN);

	$lines[1] = "$t\n";

	open(OUT, ">${HdirName}/hakojima.dat");
	print OUT @lines;
	close(OUT);
}

### ----- add -----
sub changeMode {
	mkdir($HlogdirName, $HdirMode);

	opendir(DIN, "./${HdirName}");
	my($dn);
	while($dn = readdir(DIN)) {
		if($dn =~ /^hakojima.log(.*)/) {
		    return 0 if(!rename("${HdirName}/hakojima.log$1", "${HlogdirName}/hakojima.log$1"));
		}
	}
	closedir(DIN);

	if (-e "${HdirName}/hakojima.his") {
		return 0 if(!rename("${HdirName}/hakojima.his", "${HlogdirName}/hakojima.his"));
	}

	if (-e "${HdirName}/weather.his") {
		return 0 if(!rename("${HdirName}/weather.his", "${HlogdirName}/weather.his"));
	}

    return 1;
}

sub mainMode {
	print <<END;
<FORM action="$HmenteFile" method="POST">
<h1>���ۤ�Ȣ�������ƥʥ󥹥ġ���</h1>
END
	unless (-e $HpasswordFile) {
		# �ѥ���ɥե����뤬�ʤ�
		print <<END;
<h2>�ƥѥ���ɤ���Ƥ���������</h2>
<p>�����ϥߥ����ɤ�����ˡ����줾�죲�󤺤����Ϥ��Ƥ���������<br>
������������������줿�ե�����(passwd.cgi)��FTP���եȤʤɤ�ľ�ܾä��ƺ������Ϥ��Ƥ���������</p>
<b>�ޥ����ѥ���ɡ�</b><br>
(1) <INPUT type="password" name="MPASS1" value="$mpass1">&nbsp;&nbsp;(2) <INPUT type="password" name="MPASS2" value="$mpass2"><br><br>
<b>�ü�ѥ���ɡ�</b><br>
(1) <INPUT type="password" name="SPASS1" value="$spass1">&nbsp;&nbsp;(2) <INPUT type="password" name="SPASS2" value="$spass2"><br><br>
<INPUT type="submit" value="�ѥ���ɤ����ꤹ��" name="SETUP">
<p>���ޥ������ѥ���ɤȤϡ�¾����Υѥ�����ѹ����������٤ƤΤ��٤Ƥ���Υѥ���ɤ����ѤǤ��ޤ���<br>
���ü�ѥ���ɤȤϤ��Υѥ���ɤǡ�̾���ѹ��פ�Ԥ��ȡ�������λ�⡢�����������ͤˤʤ�ޤ���(�ºݤ�̾�����Ѥ���ɬ�פϤ���ޤ���)<br>
END

#<b>ľ��ȯ�⡼�ɥѥ���ɡ�</b><br>
#(1) <INPUT type="password" name="DPASS1" value="$dpass1">&nbsp;&nbsp;(2) <INPUT type="password" name="DPASS2" value="$dpass2"><br><br>
#<p>��ľ��ȯ�⡼�ɥѥ���ɤȤ�ľ��URL���ꤹ��Ȥ����ʤ�JS��ȯ�⡼�ɤ�����⡼�ɤ˻��Ѥ���ѥ���ɤǤ���<br>
#�ܤ�����"�����Ԥ�.txt"�򻲾Ȥ��Ƥ���������</p>

		return;
	}
	print <<END;
<B>�ޥ����ѥ���ɡ�</B><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$inputPass">
<INPUT type="submit" value="�����ͼ�������" name="ADMIN">
END
	opendir(DIN, "./");

### ----- add -----
	# ���ǡ����ܹ�
	if((-e "${HdirName}/hakojima.his")||(-e "${HdirName}/hakojima.log0")){
		print <<END;
<HR><INPUT TYPE="submit" VALUE="���ǡ�����ܹ�" NAME="CHANGE">
END
	}

	# ����ǡ���
	if(-d "${HdirName}") {
		dataPrint("");
	} else {
		print <<END;
<HR><INPUT TYPE="submit" VALUE="�������ǡ�������" NAME="NEW">
END
	}

	# �Хå����åץǡ���
	my($dn);
	while($dn = readdir(DIN)){
		dataPrint($1) if($dn =~ /^${HdirName}.bak(.*)/);
	}
	closedir(DIN);
}

# �����ͼ� neo_otacky�᤬����
sub adminMode {
	my $tmp = "";
	$tmp = "<A HREF=\"${HthisFile}?settei=${inputPass}\" target=\"_blank\"><H2>${AfterName}���������</H2></A>" if($HadminMode);
	print <<END;
<H1>���ۤ�Ȣ�� �����ͼ�</H1>
<H3><FONT COLOR="red">���ʲ��κ�Ȥϡ������󹹿�����˹Ԥ��Τ����˴��ʤ���Ԥ�ʤ����ȡ���</FONT></H3>
<FORM action="$HmenteFile" method="POST">
<INPUT type=hidden name=PASSWORD value="${inputPass}">
<INPUT type=hidden name=ADMIN value=1>
END
	if(-e "./mente_lock") {
		print qq#<INPUT TYPE="submit" VALUE="���ƥʥ󥹥⡼�ɲ��" NAME="UNMENTE">\n#;
	} else {
		print qq#<INPUT TYPE="submit" VALUE="���ƥʥ󥹥⡼��" NAME="MENTE">\n#;
	}
	print <<END;
</FORM>
$tmp
<A HREF="${HbaseDir}/hako-main.cgi?Present=" target="_blank"><H2>����${AfterName}�˥ץ쥼��Ȥ�£��</H2></A>
<A HREF="${HbaseDir}/hako-main.cgi?Pdelete=${inputPass}" target="_blank"><H2>����${AfterName}������ͤ�������ˤ���</H2></A>
<A HREF="${HbaseDir}/hako-main.cgi?Punish=${inputPass}" target="_blank"><H2>����${AfterName}�����ۤ�ä���</H2></A>
<A HREF="${HbaseDir}/hako-main.cgi?Lchange=${inputPass}" target="_blank"><H2>����${AfterName}���Ϸ��ǡ������ѹ�����</H2></A>
<UL>
<LI>�Ӥ餷���ﳲ�䡢�����С��ȥ�֥롢������ץȤΥХ��ʤɤǡ��Ϸ��ǡ��������ܰդʾ��֤ˤʤäƤ��ޤä�${AfterName}��ߺѤ��ޤ���
<LI>�͸������쵬�Ϥʤɤο��ͥǡ����ؤ�ȿ�Ǥϥ����󹹿��������Ԥ��Ƥ���ˤʤ�Τǡ���դ��Ƥ���������
</UL>
<A HREF="${HbaseDir}/hako-main.cgi?Ichange=${inputPass}" target="_blank"><H2>�Ƽ���ǡ��������ѹ�����</H2></A>
<UL>
<LI>��ˡ��ǥХå��ѤǤ�����°���ѹ�������Ū�ʳ��ǻ��Ѥ��ʤ��ǲ�������
</UL>
<A HREF="${HbaseDir}/hako-main.cgi?settei=${inputPass}" target="_blank"><H2>����${AfterName}�����������</H2></A>
<UL>
<LI>����̾�ȥѥ���ɤ��ѹ��פ����ϥե�����ǡ�������${AfterName}��̾�����̵�͡�${AfterName}�ˤ��Ƥ���������
<LI>���κݡ��ѥ������ˤϡ��ü�ѥ���ɡפ����Ϥ��Ƥ���������(�������ѥ��ȥѥ���ǧ��϶�)
</UL><BR>
<A HREF="${HbaseDir}/hako-main.cgi?Bfield=${inputPass}" target="_blank"><H2>Battle Field���������</H2></A>
<UL>
<LI>�ޤ���������Ǥ���������ͤ��ѹ�������ǽ���Ϥ���ޤ���
<LI>�͸����ˤʤäƤ���������ʤ�${AfterName}��������ޤ�������Сֱ齬${AfterName}�פǤ������и��ͤ���̱�Ԥ��ˤϤʤ�ޤ���
<LI>${AfterName}����Ͽ���ˤϴط��ʤ������Ǥ��ޤ��������磹${AfterName}�ޤǤ��������Ǥ��ޤ���(����)
<LI>�����ϤǤ��������ά�����Ƥޤ�������������ۤ���٤�������Τ���դ��Ƥ���������
<LI><B>Battle Field�λ���</B>
<UL>
<LI>��ñ�̤Υ��٥�Ȥ����ƽ�������ޤ���(���ۤʤɤ�ȯ�����ޤ���)
<LI>�Ρ��ޥ롢PP�ߥ����롢��̱�������ɸ��ʳ��ϼ����դ��ޤ���
<LI>�Ӥ��ϤϤ��ʤ���Ψ��ʿ�Ϥˤʤꡢʿ�ϤϿ����ԻԤ��ܤ��Ƥ��ʤ��Ƥ�¼��ȯ�����ޤ���
<LI>�����и�������äϡ����󥰤��Τ�ޤǤǰ�ư���Ϥ��ޤ���(�Ų��Ϥ���)
<LI>���ä��ݤ��������󾩶�ϡ��ݤ�����λ��ˤʤ�ޤ���
</UL>
</UL><BR>
<FORM action="${HbaseDir}/analyzer.cgi" method=POST>
<INPUT type=hidden name=password value="${inputPass}">
<INPUT type=hidden name=mode value="analyze">
<INPUT type=hidden name=category value="a">
<INPUT type=submit value='�����������򸫤�'>
</FORM>
<UL>
<LI>�ᥤ�󥹥���ץ�(hako-main.cgi)������ǡ֥�����������Ȥ�פ褦�ˤ��Ƥ��ʤ���С����뤳�Ȥ��Ǥ��ޤ���
<LI>����Ĥ�ư��ˤ��������ϥХ��ˤʤ�ޤ���Τǡ�Ȣ�����Τ�ư��ˤ�ƶ������뤳�Ȥ�и礷�Ʋ�������
</UL><BR>
<A HREF="${HbaseDir}/hako-main.cgi?SetupV=${inputPass}" target="_blank"><H2>�������ɽ��</H2></A>
END
}

# ɽ���⡼��
sub dataPrint {
	my($suf) = @_;
	print "<HR>";
	if($suf eq "") {
		open(IN, "${HdirName}/hakojima.dat");
		print "<H1>����ǡ���</H1>";
	} else {
		open(IN, "${HdirName}.bak$suf/hakojima.dat");
		print "<H1>�Хå����å�$suf</H1>";
	}
	my $lastTurn = int(<IN>);
	my $lastTime = int(<IN>);
	my $islandNumber = int(<IN>);
	my $timeString = timeToString($lastTime);
	print <<END;
<B>������$lastTurn</B><BR>
<B>�ǽ���������</B>:$timeString<BR>
<B>�ǽ���������(�ÿ�ɽ��)</B>:1970ǯ1��1������$lastTime ��<BR>
<INPUT TYPE="submit" VALUE="���Υǡ�������" NAME="DELETE$suf">
END
	if($suf eq "") {
		my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
		localtime($lastTime);
		$mon++;
		$year += 1900;
		print <<END;
<H2>�ǽ��������֤��ѹ�</H2>
<INPUT TYPE="text" SIZE=4 NAME="YEAR" VALUE="$year">ǯ
<INPUT TYPE="text" SIZE=2 NAME="MON" VALUE="$mon">��
<INPUT TYPE="text" SIZE=2 NAME="DATE" VALUE="$date">��
<INPUT TYPE="text" SIZE=2 NAME="HOUR" VALUE="$hour">��
<INPUT TYPE="text" SIZE=2 NAME="MIN" VALUE="$min">ʬ
<INPUT TYPE="text" SIZE=2 NAME="NSEC" VALUE="$sec">��
<INPUT TYPE="submit" VALUE="�ѹ�" NAME="NTIME"><BR>
1970ǯ1��1������<INPUT TYPE="text" SIZE=32 NAME="SSEC" VALUE="$lastTime">��
<INPUT TYPE="submit" VALUE="�û�����ѹ�" NAME="STIME">
<br><br><a href="$HthisFile">[��������̤�]</a><br>
END
		if($Htournament){
			if(($mainMode eq 'tournamenttime') && (passCheck())) {
				# �ʰץȡ��ʥ��ȡ������󹹿������ḫɽ
				print <<END;
<SCRIPT LANGUAGE="JavaScript">
<!--
function textcopy(mapdata){
	window.clipboardData.setData("text",mapdata);
}
function searchID(url){
	if(document.getElementById){
		return document.getElementById(url);
	} else if(document.all){
		return document.all(url);
	} else if(document.layers){
		return document.layers[url];
	}
}
//-->
</SCRIPT>
<br><INPUT TYPE="button" VALUE="����åץܡ��ɤ˥��ԡ�" onClick="textcopy(searchID('ALIST').value)">
��������Ȥ���Ž���դ��ƻȤäƤ���������<br>
<textarea NAME="ALIST" cols="100" rows="5">
END
				open(HIN, "${HdirName}/tournament.dat");
				my $islandFightMode = int(<HIN>);
				<HIN>;
				<HIN>;
				my $turnCount = int(<HIN>);
				close(HIN);
				my $fturn = 0;
				$HfightTurn = $HfinalTurn if($islandNumber <= 2);
				while($lastTurn >= $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn){
					$fturn += $HdevelopeTurn + $HfightTurn;
				}
				print "������\t$AfterName��\t�ʹԾ���\t��������\n";
				while($islandNumber > 1){
					if($lastTurn < $HyosenTurn){
						# ͽ��
						$islandFightMode = 1;
						$lastTime += 3600 * $HtmTime1[($turnCount % ($#HtmTime1 + 1))];
						$timeString = timeToString($lastTime);
						print "$lastTurn\t$islandNumber\tͽ��\t$timeString\n";
					}elsif($lastTurn < $HyosenTurn + $HdevelopeTurn + $fturn){
						# ��ȯ
						$islandNumber = $HfightMem if(($islandFightMode == 1) && ($islandNumber > $HfightMem));
						$islandFightMode = 2;
						$lastTime += 3600 * $HtmTime2[($turnCount % ($#HtmTime2 + 1))];
						$timeString = timeToString($lastTime);
						$HfightTurn = $HfinalTurn if($islandNumber <= 2);
						print "$lastTurn\t$islandNumber\t��ȯ\t$timeString\n";
					}elsif($lastTurn < $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn){
						# ��Ʈ
						$turnCount = 0 if($islandFightMode != 3);
						$lastTime += $HinterTime if($islandFightMode != 3 && $islandNumber > 2);
						$islandFightMode = 3;
						$lastTime += 3600 * $HtmTime3[($turnCount % ($#HtmTime3 + 1))];
						$timeString = timeToString($lastTime);
						print "$lastTurn\t$islandNumber\t��Ʈ��\t$timeString\n";
					}else{
						$turnCount = 0;
						$lastTime += $HinterTime2 if($islandFightMode != 2);
						$islandFightMode = 2;
						$lastTime += 3600 * $HtmTime2[($turnCount % ($#HtmTime2 + 1))];
						$timeString = timeToString($lastTime);
						$fturn += $HdevelopeTurn + $HfightTurn;
						$islandNumber = int($islandNumber / 2 + 0.5);
						$islandNumber++ if(($islandNumber > 2) && (($islandNumber % 2) != 0) && ($HconsolationMatch));
						$HfightTurn = $HfinalTurn if($islandNumber <= 2);
						print "$lastTurn\t$islandNumber\t��ȯ\t$timeString\n" if($islandNumber > 1);
					}
					$turnCount++;
					$lastTurn++;
				}
				print "</textarea>";
			}else{
				print "<br><INPUT TYPE=\"submit\" VALUE=\"�ȡ��ʥ��ȹ��������ḫɽ\" NAME=\"TOURNAMENTTIME\">";
			}
		}
	} else {
		print <<END;
<INPUT TYPE="submit" VALUE="���Υǡ��������" NAME="CURRENT$suf">
END
	}
}

sub timeToString {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	localtime($_[0]);
	$mon++;
	$year += 1900;
	return "${year}ǯ ${mon}�� ${date}�� ${hour}�� ${min}ʬ ${sec}��";
}

# CGI���ɤߤ���
sub cgiInput {
	my($line);

	# ���Ϥ�������
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	# GET�Τ�Ĥ�������
	$getLine = $ENV{'QUERY_STRING'};

	if($line =~ /DELETE([0-9]*)/) {
		$mainMode = 'delete';
		$deleteID = $1;
	} elsif($line =~ /CURRENT([0-9]*)/) {
		$mainMode = 'current';
		$currentID = $1;
	} elsif($line =~ /NEW/) {
		$mainMode = 'new';
	} elsif($line =~ /UNMENTE/) {
		$mainMode = 'unmente';
		if($line =~ /ADMIN=([0-9])\&/) {
			$dellcheck = $1;
		}
	} elsif($line =~ /MENTE/) {
		$mainMode = 'mente';
		if($line =~ /ADMIN=([0-9])\&/) {
			$dellcheck = $1;
		}
	} elsif($line =~ /ADMIN/) {
		$mainMode = 'admin';
	} elsif($getLine =~ /ADMIN=([^\&]*)/) {
		$mainMode = 'admin';
		$inputPass = $1;
	} elsif($line =~ /SETUP/) {
		$mainMode = 'setup';
		$mpass1 = $1 if($line =~ /MPASS1=([^\&]*)\&/);
		$mpass2 = $1 if($line =~ /MPASS2=([^\&]*)\&/);
		$spass1 = $1 if($line =~ /SPASS1=([^\&]*)\&/);
		$spass2 = $1 if($line =~ /SPASS2=([^\&]*)\&/);
		$dpass1 = $1 if($line =~ /DPASS1=([^\&]*)\&/);
		$dpass2 = $1 if($line =~ /DPASS2=([^\&]*)\&/);
	} elsif($line =~ /NTIME/) {
		$mainMode = 'time';
		$ctYear = $1 if($line =~ /YEAR=([0-9]*)/);
		$ctMon = $1 if($line =~ /MON=([0-9]*)/);
		$ctDate = $1 if($line =~ /DATE=([0-9]*)/);
		$ctHour = $1 if($line =~ /HOUR=([0-9]*)/);
		$ctMin = $1 if($line =~ /MIN=([0-9]*)/);
		$ctSec = $1 if($line =~ /NSEC=([0-9]*)/);
	} elsif($line =~ /STIME/) {
		$mainMode = 'stime';
		$ctSec = $1 if($line =~ /SSEC=([0-9]*)/);
	} elsif($line =~ /TOURNAMENTTIME/) {
		$mainMode = 'tournamenttime';
### ----- add -----
	} elsif($line =~ /CHANGE/) {
		$mainMode = 'change';
	}

	$inputPass = $1 if($line =~ /PASSWORD=([^\&]*)\&/);
}

# �ե�����Υ��ԡ�
sub fileCopy {
	my($src, $dist) = @_;
	open(IN, $src);
	open(OUT, ">$dist");
	while(<IN>) {
		print OUT;
	}
	close(IN);
	close(OUT);
}

# �ѥ������å�
sub passCheck {
	if(crypt($inputPass, 'ma') eq $HmasterPassword) {
		return 1;
	} else {
		print "${HtagBig_}�ѥ���ɤ��㤤�ޤ�${H_tagBig}";
		return 0;
	}
}
# ���ƥʥ󥹥⡼��
sub menteMode {
    mkdir("./mente_lock", $HdirMode);
}

# ���ƥ⡼�ɲ��
sub unmenteMode {
	rmdir("./mente_lock");
}

# �ϰ���γ��������
sub countAroundSea {
	my($field, $x, $y) = @_;

	my @ax = (0,1,1,1,0,-1,0); # ���ϣ��إå����κ�ɸ
	my @ay = (0,-1,0,1,1,0,-1);

	my($i, $count, $sx, $sy, $idx);

	$sx = $x + $ax[0];
	$sy = $y + $ay[0];
	$sx-- if(!($sy % 2) && ($y % 2));
	$idx = $sy * $HoceanSize + $sx;
	return 0 unless ($field->[$idx] == $HlandSea); # ��������Ǥʤ���Фʤ�ʤ�

	$count = 0;
	for($i = 1; $i < 7; $i++) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];

		$sx-- if(!($sy % 2) && ($y % 2));

		if(($sx < 0) || ($sx >= $HoceanSize) || ($sy < 0) || ($sy >= $HoceanSize)) {
			# �ϰϳ�
		} else {
			# �ϰ���
			$idx = $sy * $HoceanSize + $sx;
			$count++ if ($field->[$idx] == $HlandSea);
		}
	}

	return $count;
}


1;
