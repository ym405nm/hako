#!/usr/local/bin/perl --

#---------------------------------------------------------------------
#
#	���ۤ�Ȣ��������Ǽ��Ĥ����ɽ��
#
#	������ : 2001/10/06 V0.10
#	������ : �饹�ƥ���
#
#	�����Ԥ���̱��ȯ����ƨ���ʤ��褦�����ǳ�ǧ���뤿��Τ�ΤǤ���
#	lbbslist.cgi?pass=�ޥ����ѥ����ǥ�����������ȶ����̿��⸫��ޤ���
#	lbbslist.cgi?id=��Σɣġ��ǥ�����������������󤬸���ޤ���
#
#	��������
#	2001/10/20 V0.20 �Ƕ��ȯ���򿧤��Ѥ���ɽ���Ǥ���褦�ˤ�����
#	2001/12/31 V0.30 ������������config.cgi���������褦�ˤ�����
#	2002/01/13 V0.31 version4�б�
#	2002/02/03 V0.40 CSS���̥ե����뤫���ɤ߹���褦�ˤ�����
#	2002/04/17 V0.41 ���ɽ����Ĥ�����������ץȤ�����Ū�˸�ľ����
#	2002/07/27 V0.50 �����̿����б��������ܤβ�������
#	2002/10/28 V0.60 �������륷�����դ�����
#	2003/08/20 V0.70 ���ۤ�Ȣ�����ͤ˽�����
#	2003/09/15 V0.80 �����ԥ⡼�ɤΤȤ����������ղá�
#	2003/09/20 V0.81 ����θ��������ɽ����
#	2004/02/18 V0.90 id=��ΣɣĤǳ�����������ɽ����
#	2005/02/12 V0.91 ShibaAni����β�¤�μ�����(��˥ǥ�������ʬ�ν���)
#	2005/11/05 V0.92 �ѥ���ɥ��˥�����ϳ����б�
#---------------------------------------------------------------------
#	��������ץȤϰʲ��򸵤˺������ޤ���
#
#	���÷���ݥ���ȡܳ����޶⡡��󥭥�ɽ��
#	������ : Watson
#---------------------------------------------------------------------

#---------------------------------------------------------------------
#	�������
#---------------------------------------------------------------------
require './hako-init.cgi';
require './hako-io.cgi';

# ���̤Ρ����ץ����(URL) $HbaseDir��hako-init.cgi�ǻ��ꡣ
$bye = "$HbaseDir/hako-main.cgi";

# �����Ѥ���ɽ�����륿����
$kyoutyouturn = 30;

# ����θ��������ɽ��(0:���ʤ�/1:����)
$viewOrder = 1;

#----------------------------
#	HTML�˴ؤ�������
#----------------------------
# �֥饦���Υ����ȥ�С���̾��
$title = '�Ѹ����̿�����';

# ��Ƭ�Υ�å�����(HTML��)
$headKill = <<'EOF';
<h2 class=head2>Ȣ����� �Ѹ����̿�����ɽ</h2>
EOF

$HbgTitleCell   = 'class=TitleCell';
$HbgSubTCell    = 'class=SubTCell';
$HbgLbbsCell    = 'class=LbbsCell';
$HbgCommentCell = 'class=TitleCell';

# ������ʸ��
$HtagCo_ = '<span class="head">';
$H_tagCo = '</span>';

# ������Ǽ��ġ��Ѹ��Ԥν񤤤�ʸ��
$HtagLbbsSS_ = '<span class="lbbsSS">';
$H_tagLbbsSS = '</span>';

# ������Ǽ��ġ����ν񤤤�ʸ��
$HtagLbbsOW_ = '<span class="lbbsOW">';
$H_tagLbbsOW = '</span>';

# ��̤��ֹ�ʤ�
$HtagNumber_ = '<span class="number">';
$H_tagNumber = '</span>';

#�����ޤ�-------------------------------------------------------------

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
	my($i, $id);
	for($i = 0; $i < $HislandNumber; $i++) {
		$Hislands[$i] = &readIsland();
		$HidToNumber{$Hislands[$i]->{'id'}} = $i;
	}
	# �ե�������Ĥ���
	close(IN);
	readsubmap(0);#����ޥå��ɹ�
	readsubmap(1);#����ޥå��ɹ�
	return 1;
}

#---------------------------------------------------------------------
#	�ؿ�̾ : readIsland
#	����ǽ : ����Υǡ��������
#	������ : �ʤ�
#	����� : ��Υǡ���
#---------------------------------------------------------------------
sub readIsland {
	my($id, $name, $comment, @comments,$order, $i, $line, @lbbs);
	$name = <IN>;
	$name =~ /(.*),(.*)/;	# ���̾��
	$name = $1;
	$id = int(<IN>); # ID�ֹ�
		<IN>;  # ������̾
		<IN>;  # ����
		<IN>;  # Ϣ³��ⷫ���
	$comment = <IN>;       # ������
	chomp($comment);
	my @comments = split(/<>/, $comment);
	# �ե�����ݥ��󥿤�ʤ������ʤΤ�name,ID�ʳ����ͤ��Ǽ���ʤ�
	for($i = 6; $i < 27; $i++) {
		<IN>;
	}
	$order = <IN>;# ̿��
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

	# ������Ǽ���
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
#	�ؿ�̾ : readsubmap
#	����ǽ : ���֥ޥåפΥǡ��������
#	������ : 0 - ����ޥå�
#			 1 - ����ޥå�
#	����� : ��Υǡ���
#---------------------------------------------------------------------
# ���֥ޥåפҤȤ��ɤߤ���
sub readsubmap {
	my($num) = @_;
	# ���衢����ޥå��ɤߤ���
	if(open(IIN, "${HdirName}/submap.$num")){
		my($i, $line, @lbbs);
		if($num == 0){
			#����
			for($i = 0; $i < $HislandSize; $i++) {
				$line = <IIN>;
			}
		}else{
			#����
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
		# ������Ǽ���
		for($i = 0; $i < $HlbbsMax; $i++) {
			$line = <IIN>;
			chomp($line);
			$lbbs[$i] = $line;
		}
		if($num == 0){
			#����
			$Hspace = {'lbbs' => \@lbbs};
		}else{
			#����
			$Hocean = {'lbbs' => \@lbbs};
		}
		close(IIN);
	}
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
#--------------------------------------------------------------------
#	POST or GET�����Ϥ��줿�ǡ�������
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

	if($getLine =~ /pass=([^\&]*)/) {
		# �ǽ�ε�ư
		$HdefaultPassword = $1;
		$HdecodePassword = crypt($HdefaultPassword, 'ma')
	}
	if($getLine =~ /id=([^\&]*)/) {
		$HcurrentID = $1;
	}
	if (-e $HpasswordFile) {
		# �ѥ���ɥե����뤬����
		open(PIN, "<$HpasswordFile") || die $!;
		chomp($HmasterPassword = <PIN>); # �ޥ����ѥ���ɤ��ɤ߹���
		close(PIN);
	}
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
<HTML><HEAD><TITLE>$title</TITLE>
<BASE HREF="$imageDir/">
<link rel="stylesheet" type="text/css" href="$skinName">
</HEAD>
<DIV ID='BodySpecial'><DIV ID='LinkHead'></DIV><DIV ID='LinkTop'>
<BODY>
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
	my($orderTxt) = "";
	if($viewOrder){
		$orderTxt = "<br>���䢣�ΰ�̣�ϡ������礴�Ȥθ�ͭ������֤��ä��ꤷ�ޤ����ܺ���̩�Ǥ���";
	}
	out(<<END);
<P>${AfterName}��̾���򥯥�å�����ȡ��Ѹ����뤳�Ȥ��Ǥ��ޤ���$orderTxt</P>
<DIV align="right">
<SMALL>CPU($cpu) : user($uti) system($sti)</SMALL>
</DIV></DIV></BODY></HTML>
END
}
#---------------------------------------------------------------------
#	�ؿ�̾ : htmlError
#	����ǽ : HTML�Υ��顼��å������ν���
#	������ : �ʤ�
#	����� : �ʤ�
#---------------------------------------------------------------------
sub htmlError{
	out("${h2}���顼��ȯ�����ޤ���</H2>\n");
}
#---------------------------------------------------------------------
#	�ؿ�̾ : tempLbbsContents
#	����ǽ : ������Ǽ�������
#	������ : ���ID���⡼��(3���衢4����)
#	����� : �ʤ�
#---------------------------------------------------------------------
sub tempLbbsContents {
	my($number,$mode) = @_;
	$HislandList = getIslandList($HcurrentID);
	my($island,$id,$name,$link,$lbbs,$comment,$line,@ccbx);
	if($mode == 3){
		# ����ޥå�
		$island = $Hspace;
		$name = "����ޥå�";
		$link = "space=0";
		$comment = "";
		$id = "999";
	}elsif($mode == 4){
		# ����ޥå�
		$island = $Hocean;
		$name = "����ޥå�";
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
				$ccbx[$i] = "��";
			}else{
				$ccbx[$i] = "��";
			}
		}
		$id = $island->{'id'};
	}
	$lbbs = $island->{'lbbs'};
	$comment = "��" if($comment eq '');
	my($owner) = 0;
	if($HdecodePassword eq $HmasterPassword) {
		# �����ɽ��
		$owner = 1;
	}
	if($viewOrder){
		$order = "${ccbx[4]}${ccbx[5]}${ccbx[7]}${ccbx[11]}${ccbx[3]}${ccbx[8]}${ccbx[6]}${ccbx[9]}${ccbx[10]}";
	}
	out(<<END);
<TR><TD $HbgTitleCell><a name=$id><b>��̾</b></a></TD>
<TD $HbgTitleCell>
<A HREF="$HthisFile?${link}" TARGET=_blank>
<b>$name</b></A>$order
</TD></TR>
<TR><TD $HbgTitleCell><b>������</b></TD>
<TD $HbgTitleCell>${HtagCo_}$comment${H_tagCo}
</TD></TR>
END
	out(<<END) if($owner || $HcurrentID);
<TR>
<TD $HbgTitleCell><b>���</b></TD>
<TD $HbgTitleCell>
<FORM action="$HthisFile" method="POST">
̾��:<INPUT TYPE="text" SIZE=12 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName">
<SELECT NAME="ISLANDID">$HislandList</SELECT>
����:<INPUT TYPE="text" SIZE=40 NAME="LBBSMESSAGE">
<INPUT TYPE="hidden" NAME="LBBSLIST" VALUE="lbbslist">
�ѥ�:<INPUT TYPE="password" SIZE=4 MAXLENGTH=16 NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}">
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="PUBLIC" CHECKED>����
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="SECRET"><span class='lbbsST'>����</span>
<INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonFO$id">
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
				# �Ѹ���
				if ($bbs1 == 0) {
					# ����
					out("<TD $CellColor>$HtagLbbsSS_$bbs4 > $bbs5$H_tagLbbsSS $speaker</TD></TR>");
				} else {
					# ����
					if ($owner) {
						# �����ʡ�
						out("<TD $CellColor>$HtagLbbsSS_$bbs4 >(��) $bbs5$H_tagLbbsSS $speaker</TD></TR>");
					} else {
						# �Ѹ���
						out("<TD $CellColor><CENTER><span class='lbbsST'>- ���� -</span></CENTER></TD></TR>");
					}
				}
			} else {
				# ���
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

