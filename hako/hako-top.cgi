#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �ȥåץ⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# ���ۤ�Ȣ��  (ver5.52c)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ȥåץڡ����⡼��
#----------------------------------------------------------------------
# �ᥤ��

sub topPageMain {
	axeslog() if($HtopAxes == 2); #��������������
	unlock();		# ����

	if(-e "./mente_lock"){
		mente_mode(0);
	}else{
		tempTopPage($_[0]);	# �ƥ�ץ졼�Ƚ���
	}
}

# �ȥåץڡ���
sub tempTopPage {
	my($mode) = @_;
	# flexTime����
	if($Htournament){
		# �ʰץȡ��ʥ���
		$HflexTimeSet = 1;
		if($HislandFightMode == 1){
			# ͽ��
			@HflexTime = @HtmTime1;
		}elsif($HislandFightMode == 2){
			# ��ȯ
			@HflexTime = @HtmTime2;
			$HmaxIsland = 0;
		}elsif($HislandFightMode == 3){
			# ��Ʈ
			@HflexTime = @HtmTime3;
			$HmaxIsland = 0;
		}elsif($HislandFightMode == 9){
			# ��λ
			$HlastTurn = $HislandTurn;
		}
		$HunitTime = 3600 * $HflexTime[($HislandTurnCount % ($#HflexTime + 1))] if($HflexTimeSet);
	}else{
		$HunitTime = 3600 * $HflexTime[($HislandTurn % ($#HflexTime + 1))] if($HflexTimeSet);
	}
	if($mode != 2){
	out(<<END);
${HtagTitle_}$Htitle${HtagTitle2_}$Htitle2${H_tagTitle}${H_tagTitle}
END
#${HthisFile}?Sight=${id}" class=\"M\" TARGET=_blank>
	# �ǥХå��⡼�ɤʤ�֥������ʤ��ץܥ���

	if($Hdebug == 1) {
		out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="�������ʤ��" NAME="TurnButton">
</FORM>
END
	}
	# ���󹹿�����ɽ��
	my($now) = time;
	# ���󹹿��ޤǤλ��֤�׻�����
	$aaa = $HislandLastTime + $HunitTime;
	my($sec, $min, $hour, $day, $sss);
	$sec = $aaa - $now;
	if($sec < 0) {
		$aaa += $HunitTime;
		if(-$sec < $HunitTime) {
			$sec += $HunitTime;
		} else {
			$sec = 0;
		}
	}
	$min  = int($sec  / 60); $sec  %= 60;
	$hour = int($min  / 60); $min  %= 60;
	$day  = int($hour / 24); $hour %= 24;
	if($day){
		$sss = "$day����${hour}����${min}ʬ${sec}��";
	}else{
		$sss = "${hour}����${min}ʬ${sec}��";
	}
	
	my($min2, $hour2, $date2, $mon2) = (localtime($aaa))[1,2,3,4];
	$mon2++;
	my($bbb) = "${mon2}��${date2}��${hour2}��${min2}ʬ";
	
	my $bb1 = "";
	if($HflexTimeSet) {
		my($i,$nnn,$ftime,$ct,$rt) = (0,0,0,0,0);
		$ct = $#HflexTime + 1;
		if($Htournament){
			$rt = ($HislandTurnCount % ($ct));
		}else{
			$rt = ($HislandTurn % ($ct));
		}
		$bb1 = "�������١�${ct}����(��";
		my $bb2;
		for($i = $rt;$i <= $#HflexTime;$i++){
			$ftime += $HflexTime[($i % ($#HflexTime + 1))];
			$nnn = $HislandLastTime + 3600 * $ftime;
			($min2, $hour2) = (localtime($nnn))[1,2];
			if($rt == $i){
				$bb2 .= "<b>${hour2}��${min2}ʬ</b>��";
			}else{
				$bb2 .= "${hour2}��${min2}ʬ��";
			}
		}
		for($i = 0;$i < $rt;$i++){
			$ftime += $HflexTime[($i % ($#HflexTime + 1))];
			$nnn = $HislandLastTime + 3600 * $ftime;
			($min2, $hour2) = (localtime($nnn))[1,2];
			$bb1 .= "${hour2}��${min2}ʬ��";
		}
		$bb1 .= "${bb2})";
	}
	
	if ($HjavaModeSet eq 'cgi') {
		$radio = "CHECKED";	$radio2 = "";
	}else{
		$radio = ""; $radio2 = "CHECKED";
	}

	# �������ɽ��
	my($HlastTurnS);
	if($HlastTurn == 0) {
		$HlastTurnS = "";
	} elsif($HislandTurn < $HlastTurn) {
		$HlastTurnS = "��${HlastTurn}";
	} else {
		$HlastTurnS = "���ʥ�����Ͻ�λ���ޤ�����";
		$bbb = "����̵��";
	}

	my($sinkiStr) = '';
	if($HislandNumber < $HmaxIsland + $HbattleNumber) {
		$sinkiStr = "[<A HREF=\"${HthisFile}?settei=0\" class=\"M\">���������������ѹ�</A>]<br>";
	} else {
		# �����

		$sinkiStr = "[<A HREF=\"${HthisFile}?settei=0\" class=\"M\">���������������ѹ�</A>�����ա�]<br>";
	}

	# �ե�����

	$monthname = $Hmonthname[($HislandTurn % 12) + 1];
	
	my $fightmode = "";
	if($Htournament){
		# �ʰץȡ��ʥ���
		my($tst1,$tst2);
		my $flog = "[<A href=\"$HthisFile?FightLog=0\" class=\"M\" TARGET=_blank>����ε�Ͽ</A>]";
		if($HislandFightMode == 1){
			# ͽ��
			if($HislandNumber > $HfightMem){
				$tst2 = $HislandNumber - $HfightMem;
				$tst2 = "$tst2$AfterName���פ�";
			}
			$tst1 = "��ͽ����λ�塢$tst2��ȯ���֤˰ܹԤ��ޤ���";
			$fightmode = "<font color=blue>ͽ��������</font>��[$HislandTurn��$HislandChangeTurn������]��($HislandNumber$AfterName��$HfightMem${AfterName})$tst1";
		}elsif($HislandFightMode == 2){
			# ��ȯ
			$tst1 = $HislandChangeTurn + 1;
			$fightmode = "<font color=blue>��ȯ������</font>��[$HislandTurn��$HislandChangeTurn������]��($tst1�����󤫤鹶�Ⳬ��)";
		}elsif($HislandFightMode == 3){
			# ��Ʈ
			$fightmode = "<font color=red>��Ʈ������</font>��[$HislandTurn��$HislandChangeTurn������]";
		}elsif($HislandFightMode == 9){
			# ��λ
			$fightmode = "�ȡ��ʥ��ȤϽ�λ���ޤ�����";
		}
		$fightmode = "<DIV ID='fightmode'><b>$fightmode $flog</b></DIV><br><br>";
	}
	out(<<END);
<DIV ID='Turn'>
<H1>������$HislandTurn$HlastTurnS��($monthname)</H1>
</DIV>
$fightmode
<DIV ID='nexttime'>
<font size=4>����ι������֡�$bbb </FONT><font size=3>(�Ĥ� $sss)</FONT>
<br>$bb1
</DIV>

<span class='attention'>


</span>

<HR><TABLE><TR><TD style="border-width:0px;">
<DIV ID='myIsland'>
<H1>��ʬ��${AfterName}��</H1>
<SCRIPT language="JavaScript">
<!--
function develope(){
	if(document.Island.DEVELOPEMODE[1].checked){
		document.Island.SIGHTMODE.value = "on";
	}
	document.Island.target = "";
}
function newdevelope(){
	if(document.Island.DEVELOPEMODE[1].checked){
		document.Island.SIGHTMODE.value = "on";
	}
//	newWindow = window.open("", "newWindow");
	document.Island.target = "newWindow";
	document.Island.submit();
}
//-->
</SCRIPT>
<FORM name="Island" action="$HthisFile" method="POST">
�����󤹤�${AfterName}��̾���ϡ�<BR>
<SELECT NAME="ISLANDID">
<OPTION VALUE="0">-${AfterName}�����򤷤Ʋ�����-
$HislandList
</SELECT><BR>
���ʤ���${AfterName}��̾���ϡ�<BR>
<SELECT NAME="PISLANDID">
$HislandList
</SELECT><BR>
�ѥ���ɤ�ɤ�������<BR>
<INPUT TYPE="hidden" NAME="OwnerButton">
<INPUT TYPE="password" NAME="PASSWORD" VALUE="${\htmlEscape($HdefaultPassword)}" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=cgi $radio>��⡼��
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=java $radio2>Java������ץȥ⡼��<BR>
<INPUT TYPE="radio" NAME=DEVELOPEMODE VALUE=DEVELOPE CHECKED>��ȯ�⡼��
<INPUT TYPE="radio" NAME=DEVELOPEMODE VALUE=SIGHT>�Ѹ��⡼��<BR>
<INPUT TYPE="hidden" NAME="SIGHTMODE" VALUE=off>
<INPUT TYPE="submit" VALUE="Ʊ������" onClick="develope()">��
<INPUT TYPE="button" VALUE="����������" onClick="newdevelope()">
</FORM></DIV></TD>
<TD WIDTH=40 style="border-width:0px;" >��</TD>
<TD VALIGN="top" style="border-width:0px;" >
<H1>�����ѹ���Ƽ�����ɽ��</H1>
$sinkiStr<br>
[<A HREF="${HbaseDir}/history.cgi?saikin=99" class=\"M\" TARGET=_blank>���ν�����Υ�</A>����
<A HREF="${HbaseDir}/history.cgi?tenki=0" class=\"M\" TARGET=_blank>����ŷ��</A>����
<A HREF="${HbaseDir}/history.cgi?statistical=0" class=\"M\" TARGET=_blank>����</A>]<br>
<br>
[<A href="${HbaseDir}/profile.cgi" class=\"M\" TARGET=_blank>�ץ�ե�����(${AfterName}��ξ���)</A> ��
<A href="$HthisFile?Exchange=0" class=\"M\" TARGET=_blank>�񸻼����</A>]<br>
<br>
[<A href="${HbaseDir}/ranking.cgi" class=\"M\" TARGET=_blank>�ݤ������ÿ��ʤɤΥ�󥭥�</A> ��
<A href="$HthisFile?SUCCESSIVE=0" class=\"M\" TARGET=_blank>�����¿�͸��Υ�󥭥�ɽ��</A>]<br>
<br>
END
	my $sftime = (-M "${HefileDir}/setup.html");
	my @Files = ('hako-main.cgi', 'hako-init.cgi', 'init-game.cgi', 'hako-make.cgi');
	my $sfFlag = 1;
	foreach (@Files) {
		if($sftime >= (-M "./$_")){
			$sfFlag = 0;
			last;
		}
	}
	if((-e "${HefileDir}/setup.html") && $sfFlag) {
		out("[<A href=\"${efileDir}/setup.html\" class=\"M\" TARGET=_blank>�������</A>] ");
	} else {
		out("[<A href=\"$HthisFile?SetupV=0\" class=\"M\" TARGET=_blank>�������</A>] ");
	}
	out("</TD></TR></TABLE>");
	}else{
		# ����⡼��
		out("$Htitle���������������ѹ�������<A HREF=\"${HthisFile}\" class=\"M\">�̾�ΰ������̤����</A>");
	}
	my $mStr1 = ($HhideMoneyMode != 0) ? "<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>" : '';
	if($mode == 1) {
		# �ʰ�ɽ���⡼��
		return;
	} elsif($mode == 2) {
		# ����⡼��
	} else {
		my $solarwind = ($Hspace->{'solarwind'} <= $HislandTurn) ? "(<b>������ȯ����</b>)" : "";
		my $hangen = "";
		my $hmode = "";
		if($Hdishangen == 2) {
			# �ҳ�Ⱦ������ɽ�����롣
			if((int($HislandTurn / 100) % 2) == 0){
				# ��ΨȾ��
				$hangen = "���ҳ�ΨȾ����";
			}
		}
		if($mode == 3){
			# �ܺ٥⡼��
			$hmode = "[<A href=\"$HthisFile\" class=\"M\">�ʰװ���</A>]";
		}else{
			$hmode = "[<A href=\"$HthisFile?list=0\" class=\"M\">�ٰܺ���</A>]";
		}
		my $warstr = "";
		if($HwarFlg){
			$warstr = "<TH $HbgTitleCell>${HtagTH_}�����и���${H_tagTH}</TH>";
		}
		# �ر�ɽ��ɽ��?
		&campInfoList;
		my $vsith = "";
		if($Htournament){
			$vsith = "<TH $HbgTitleCell>${HtagTH_}�������${H_tagTH}</TH>";
		}
		out(<<END);
<HR><DIV ID='islandView'>
<H1>��${AfterName}�ξ���${hangen}</H1>
<P>${AfterName}��̾���򥯥�å�����ȡ�<B>�Ѹ�</B>���뤳�Ȥ��Ǥ��ޤ���$hmode
[<A href="${HbaseDir}/monsterlist.cgi" class=\"M\">���åХȥ롡������ð���</A>]
</P>
[<A href=\"$HthisFile?Ocean=0" class=\"M\">������դγ���</A>]
[<A href=\"$HthisFile?space=0\" class=\"M\">�����</A>${solarwind}]
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>
<TH $HbgTitleCell COLSPAN=2>${HtagTH_}${AfterName}${H_tagTH}</TH>
$vsith
<TH $HbgTitleCell>${HtagTH_}��ɸ${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}ŷ��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�͸�${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
$mStr1
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
$warstr
<TH $HbgTitleCell>${HtagTH_}�ջ�ɽ��${H_tagTH}</TH>
END
		if($mode == 3){
			# �ܺ�
	out(<<END);
<TH $HbgTitleCell>${HtagTH_}���ȵ���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���ȵ���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���ȵ���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�η��쵬��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�ץ쥼���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����ͭ��${H_tagTH}</TH></TR>
END
		}else{
			out("</TR>\n");
		}
	}
	
	if(($mode == 0) || ($mode == 3)) {
		# �̾�ܺ٥⡼��

	my($island, $j, $food, $farm, $factory, $tower, $mountain, $ally, $amark, $name, $id, $prize, $vprize, $present, $ii, $monsfound);
	my $bcount = 0;
	for($ii = 0; $ii < $HislandNumber; $ii++) {

	$island = $Hislands[$ii];

	$id = $island->{'id'};
	
	if($id > 90) {
		$bcount++;
	}else{
		# �̾����ΤȤ�
	
#	my($wkind, $wname, $whp, $wkind2, $wkind3) = weatherinfo($island->{'weather'});
#	my($wname2) = $WeatherName[$wkind2];
#	my($wname3) = $WeatherName[$wkind3];
	
	$j = $ii + 1 - $bcount;
	$farm = $island->{'farm'};
	$factory = $island->{'factory'} + $island->{'port'};
	$tower = $island->{'tower'};
	$mountain = $island->{'mountain'};
	$farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
	$tower = ($tower == 0) ? "��ͭ����" : "${tower}0$HunitPop";
	$mountain = ($mountain == 0) ? "��ͭ����" : "${mountain}0$HunitPop";
	my($turnsu)   = $island->{'turnsu'};
	my($zyuni) = $island->{'zyuni'};

	$prize = $island->{'prize'};
	my($flags, $monsters, $turns);
	$prize =~ /([0-9]*),([0-9]*),(.*)/;
	$flags = $1;
	$monsters= $2;
	$turns = $3;
	$prize = '';

	if($Hallyflg){
		# �����Ϥ�����
		$ally = $island->{'ally'};
		$amark = "<b>$Hallymark[$ally]</b> ";
	}else{
		$amark = "";
	}
	# �ݸ��ˤ��ݸ��ɽ��
	my($hogo) = '��';
	if(($turnsu + $island->{'evil'} < $HdisUN) || ($island->{'evil'} == 0)){
		$hogo = '��';
	} elsif(($island->{'evil'} < $HdisUN) && (!$HwarFlg)) {
		$hogo = '��';
	}

	# ���ä��������ɽ��
	if($island->{'monsfound'} > 0){
		$monsfound = "<b>(����$island->{'monsfound'})</b>";
	}else{
		$monsfound = "";
	}

	# ŷ��
	my($wkind, $wname, $whp, $wkind2, $wkind3) = weatherinfo($island->{'weather'});
	my $tenki = "<img src =\"${imageDir}/$WeatherIcon[${wkind}]\">";

	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}${AfterName}${H_tagName}";
	} else {
		$name = "${HtagName2_}$island->{'name'}${AfterName}($island->{'absent'})${H_tagName2}";
	}
	$name = "<span class='attention'>�ڴ����ͤ��������</span><BR>" . $name if($island->{'predelete'});
	
	# �������դ�ɽ��
	my($kazu) = 0;
	my($mTurnList) = '';
	while($turns =~ s/([0-9]*),//) {
		$kazu++;
		$mTurnList .= "[$1${Hprize[0]}] ";
	}
	if($kazu >= 5) {
		$prize .= "<IMG SRC=\"prize00.gif\" ALT=\"$mTurnList\" WIDTH=16 HEIGHT=16> ";
	} elsif($kazu >= 3) {
		$prize .= "<IMG SRC=\"prize.gif\" ALT=\"$mTurnList\" WIDTH=16 HEIGHT=16> ";
	} elsif($kazu != 0) {
		$prize .= "<IMG SRC=\"prize0.gif\" ALT=\"$mTurnList\" WIDTH=16 HEIGHT=16> ";
	}

	# ̾���˾ޤ�ʸ�����ɲ�
	my($f) = 1;
	my($i);
	for($i = 1; $i < 11; $i++) {
		$prize .= "<IMG SRC=\"prize${i}.gif\" ALT=\"${Hprize[$i]}\" WIDTH=16 HEIGHT=16> " if($flags & $f);
		$f *= 2;
	}
	$prize .= "<IMG SRC=\"prize11.gif\" ALT=\"${Hprize[11]}\" WIDTH=16 HEIGHT=16> " if($flags & 2048);
	
	# �ݤ������åꥹ��
	$f = 1;
	my($max) = -1;
	my($mNameList) = '';
#	for($i = 0; $i < 32; $i++) {
#		if($monsters & $f) {
#			$mNameList .= "[$HmonsterName[$i]] ";
#			$max = $i;
#		}
#		$f *= 2;
#	}
	for($i = $HmonsterNumber-1; $i >= 0; $i--) {
		$f = 2 ** $i;
		if($monsters >= $f){
			$monsters -= $f;
			$mNameList .= "[$HmonsterName[$i]] ";
			$max = $i if($max == -1);
		}
	}
	$prize .= "<IMG SRC=\"${HmonsterImage[$max]}\" ALT=\"$mNameList\" WIDTH=16 HEIGHT=16> " if($max != -1);

	my($cspan,$comment,$popspace);
	if($mode == 3){
		# �ܺ٥⡼��
		$popspace = $island->{'popspace'};
		$popspace = ($popspace > 0) ? "(${popspace}${HunitPop})" : "";
		$comment = $island->{'comment'};
		$cspan = 16;
		# �ץ쥼��Ȥ�ɽ��
		$present = '';
		my $pre  = $island->{'present'};
		$present .= "<IMG SRC=\"land30.gif\" ALT=\"$pre->[0]\" WIDTH=16 HEIGHT=16> " if($pre->[0] > 0);
		$present .= "<IMG SRC=\"land27.gif\" ALT=\"$pre->[1]\" WIDTH=16 HEIGHT=16> " if($pre->[1] > 0);
		$present .= "<IMG SRC=\"land32.gif\" ALT=\"$pre->[2]\" WIDTH=16 HEIGHT=16> " if($pre->[2] > 0);
		$present .= "<IMG SRC=\"land29.gif\" ALT=\"$pre->[3]\" WIDTH=16 HEIGHT=16> " if($pre->[3] > 0);
		$present .= "<IMG SRC=\"land28.gif\" ALT=\"$pre->[4]\" WIDTH=16 HEIGHT=16> " if($pre->[4] > 0);
		$present .= "<IMG SRC=\"land31.gif\" ALT=\"$pre->[5]\" WIDTH=16 HEIGHT=16> " if($pre->[5] > 0);
		$present .= "<IMG SRC=\"land33.gif\" ALT=\"$pre->[6]\" WIDTH=16 HEIGHT=16> " if($pre->[6] > 0);
		$present .= "<IMG SRC=\"land39.gif\" ALT=\"$pre->[7]\" WIDTH=16 HEIGHT=16> " if($pre->[7] > 0);
		$present .= "<IMG SRC=\"land38.gif\" ALT=\"$pre->[8]\" WIDTH=16 HEIGHT=16> " if($pre->[8] > 0);
		$present .= "<IMG SRC=\"land40.gif\" ALT=\"$pre->[9]\" WIDTH=16 HEIGHT=16> " if($pre->[9] > 0);
		$present .= "<IMG SRC=\"monumentM.gif\" ALT=\"$pre->[10]\" WIDTH=16 HEIGHT=16> " if($pre->[10] > 0);
		$present .= "<IMG SRC=\"monumentP.gif\" ALT=\"$pre->[11]\" WIDTH=16 HEIGHT=16> " if($pre->[11] > 0);
		$present = '��' if($present eq '');

		# �ƾޤ�ɽ��
		$f = 1;
		$vprize = '';
		$flags = $island->{'status'};
		for($i = 1; $i < $HturnPrizeNumber + 1; $i++) {
			$vprize .= "<IMG SRC=\"Vprize${i}.gif\" ALT=\"${HprizeV[$i]}\" WIDTH=16 HEIGHT=16> " if($flags & $f);
			$f *= 2;
		}
		$vprize = '��' if($vprize eq '');
	}else{
		$comment = cutColumn($island->{'comment'}, 70);
		$cspan = 7;
	}
	
	#�����ȥ�٥�
	my($label0, $label1, $label2, $label3, $label4);
	my($label0_1n,$label0_2n) = split(/<>/,$HlabelName[0]);
	my($label0_1i,$label0_2i) = split(/<>/,$HlabelImage[0]);
	if($island->{'commentLabel0'}){
		$label0 = " <IMG SRC=\"$imageDir/$label0_1i\" ALT=\"$label0_1n\">" 
	}else{
		$label0 = " <IMG SRC=\"$imageDir/$label0_2i\" ALT=\"$label0_2n\">"
	}
	$label1 = " <IMG SRC=\"$imageDir/$HlabelImage[1]\" ALT=\"$HlabelName[1]\">" if($island->{'commentLabel1'});
	$label2 = " <IMG SRC=\"$imageDir/$HlabelImage[2]\" ALT=\"$HlabelName[2]\">" if($island->{'commentLabel2'});
	$label3 = " <IMG SRC=\"$imageDir/$HlabelImage[3]\" ALT=\"$HlabelName[3]\">" if($island->{'commentLabel3'});
	$label4 = " <IMG SRC=\"$imageDir/$HlabelImage[4]\" ALT=\"$HlabelName[4]\">" if($island->{'commentLabel4'});
	
	if($HwarFlg){
		# ����⡼��
		$warstr = "<TD $HbgInfoCell>" . $island->{'allex'} . "</TD>";
		$cspan++;
	}
	# �ʰץȡ��ʥ���
	my $vsitd = "";
	if($Htournament){
		my $tName = "";
		if($HislandFightMode == 9){
			$tName = "��- ��λ -";
		}elsif($island->{'fight_id'} == -1){
			$tName = "��- ���ﾡ -";
		}else{
			$tName = $HidToName{$island->{'fight_id'}};
			$tName = ($tName eq '') ? "��- ̤�� -" : "$tName$AfterName";
		}
		$vsitd = "<TD $HbgNameCell>$tName</TD>";
		$cspan++;
	}
	my($mStr1) = '';
	if($HhideMoneyMode == 1) {
		$mStr1 = "<TD $HbgInfoCell>$island->{'money'}$HunitMoney</TD>";
	} elsif($HhideMoneyMode == 2) {
		my($mTmp) = aboutMoney($island->{'money'});
		$mStr1 = "<TD $HbgInfoCell>$mTmp</TD>";
	}

	my($oStr) = ''; # ������̾ɽ���Τ����ɲ�
	if($island->{'ownername'} eq ''){
		$oStr = "<TD $HbgCommentCell COLSPAN=$cspan>$amark${HtagTH_}������ : ${H_tagTH}${comment}</TD>";
	} else {
		$oStr = "<TD $HbgCommentCell COLSPAN=$cspan>$amark<A HREF=\"$HbaseDir/profile.cgi?profile=${id}\" class=\"M\" TARGET=_blank>$island->{'ownername'}</A> : ${comment}</TD>";
	}
	out(<<END);
<TR>
<TD $HbgNumberCell ROWSPAN=2>${HtagNumber_}$j${H_tagNumber}($zyuni)</TD>
<TD $HbgNameCell ROWSPAN=2>
<A HREF="${HthisFile}?Sight=${id}" class=\"M\" TARGET=_blank>
$name$monsfound
</A><BR>
$prize
</TD>
<TD $HbgInfoCell>$hogo</TD>
$vsitd
<TD $HbgInfoCell>$island->{'x'},$island->{'y'}</TD>
<TD $HbgInfoCell>$tenki</TD>
<TD $HbgInfoCell>$island->{'pop'}$HunitPop$popspace</TD>
<TD $HbgInfoCell>$island->{'area'}$HunitArea</TD>
$mStr1
<TD $HbgInfoCell>$island->{'food'}$HunitFood</TD>
$warstr
<TD $HbgInfoCell>$label0$label1$label2$label3$label4</TD>
END
	if($mode == 3){
		out(<<END);
<TD $HbgInfoCell>$farm</TD>
<TD $HbgInfoCell>$factory</TD>
<TD $HbgInfoCell>$tower</TD>
<TD $HbgInfoCell>$mountain</TD>
<TD $HbgInfoCell>$vprize</TD>
<TD $HbgInfoCell>$present</TD>
<TD $HbgInfoCell>$island->{'winP'}</TD>
<TD $HbgInfoCell>$island->{'loseP'}</TD>
<TD $HbgInfoCell>$island->{'possess'}</TD></TR>
END
	}else{
		out("</TR>\n");
	}
	out(<<END);
<TR>
<TD $HbgInfoCell>$turnsu</TD>
$oStr
</TR>
END
	}
	}
	out(<<END);
</TABLE></DIV>
END
	my $bHeader = 1;
	for($ii = 0; $ii < $HislandNumber; $ii++) {
		$island = $Hislands[$ii];
		$id = $island->{'id'};
		if($id > 90) {
			# Battle Field
			if($island->{'ownername'} eq ''){
				$oStr = "<TD $HbgNameCell>$island->{'comment'}</TD>";
			} else {
				$oStr = "<TD $HbgNameCell><A HREF=\"$HbaseDir/profile.cgi?profile=${id}\" class=\"M\" TARGET=_blank>$island->{'ownername'}</A> : $island->{'comment'}</TD>";
			}
			if($bHeader){
				$bHeader = 0;
	out(<<END);
<DIV ID='islandViewBf'>
<H1>Battle Field�ξ���</H1>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}ID${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}��ɸ${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}������${H_tagTH}</TH>
</TR>
END
			}
	out(<<END);
<TR>
<TD $HbgNumberCell align=center><span class="star">��</span></TD>
<TD $HbgInfoCell>$island->{'id'}</TD>
<TD $HbgNameCell>
<A HREF="${HthisFile}?Sight=${id}" class=\"M\" TARGET=_blank>${HtagName_}$island->{'name'}${AfterName}${H_tagName}</A><BR></TD>
<TD $HbgInfoCell>$island->{'x'},$island->{'y'}</TD>
$oStr
</TR>
END
			}
		}
		if($bHeader){
			out("<HR>");
		}else{
			out("</TABLE></DIV><HR>");
		}
	} else {
		my $tournamentMons = "";
		if($Htournament == 2){
			$tournamentMons = "������(���åХȥ�)�ϡ�<BR><SELECT NAME=TOURNAMENTMONS>\n";
			for($i = 1; $i < $HmonsterNumber; $i++) {
				$tournamentMons .= "<OPTION VALUE=$i>$HmonsterName[$i]\n";
			}
			$tournamentMons .= "</SELECT><BR>\n";
		}
		out(<<END);
<HR>
<TABLE><TR><TD style="border-width:0px;" >
<DIV ID='changeInfo'>
<H1>$AfterName̾��ѥ���ɤ��ѹ�</H1>
<P>(���)̾�����ѹ��ˤ�$HcostChangeName${HunitMoney}������ޤ���</P>
<FORM action="$HthisFile" method="POST">
�ɤ�$AfterName�Ǥ�����<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
�ɤ��̾�����Ѥ��ޤ�����(�ѹ�������Τ�)<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>$AfterName<BR>
�ɤ�ʥ����ʡ�̾���Ѥ��ޤ�����(�ѹ�������Τ�)<BR>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
�ѥ���ɤϡ�(ɬ��)<BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
�������ѥ���ɤϡ�(�ѹ�������Τ�)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
ǰ�Τ���ѥ���ɤ�⤦���(�ѹ�������Τ�)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="�ѹ�����" NAME="ChangeInfoButton">
</FORM></DIV></TD>
<TD WIDTH=40 style="border-width:0px;" >��</TD>
<TD VALIGN="top" style="border-width:0px;" >
<DIV ID='newIsland'>
<H1>������$AfterName��õ��</H1>
END
		if($HislandNumber < $HmaxIsland + $HbattleNumber) {
			if((!$HadminMode) || (checkPassword($HspecialPassword, $HdefaultPassword))){
				out(<<END);
<FORM action="$HthisFile" method="POST">
�ɤ��̾����Ĥ���ͽ�ꡩ<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>$AfterName<BR>
�����ʡ�̾(��ά��)<br>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
$tournamentMons
�ѥ���ɤϡ�<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
ǰ�Τ���ѥ���ɤ�⤦���<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="õ���˹Ԥ�" NAME="NewIslandButton">
</FORM>
END
			}else{
				# �����⡼��
				out(<<END);
        ��Ȣ��Ǥ���Ŭ����${AfterName}̾�ʤɤλ��������å���ԤäƤ��ޤ���<BR>
        ���ô�˾�����ϡ������ͤޤǡ�${AfterName}̾�פȡ֥ѥ���ɡפ�<BR>
        �᡼�뤷�Ƥ���������<BR>
END
			}
		}else{
			out(<<END);
        $AfterName�ο���������Ǥ�������������Ͽ�Ǥ��ޤ���
END
		}
		
		my($cookie) = jcode::euc($ENV{'HTTP_COOKIE'});
		if($cookie =~ /MYSHIP=\(([^\)]*)\)/) {
			if($1) {
				$radio = ""; $radio2 = "CHECKED";
			}else{
				$radio = "CHECKED";	$radio2 = "";
			}
		}
		out(<<END);
</DIV>
</TD></TR></TABLE>
<HR>
<FORM action="$HthisFile" method="POST">
<H1>��������β����μ��Ϥ�Ʃ�ᤵ���ƶ��̤��䤹�����뤫�ɤ���������</H1>
<INPUT TYPE="radio" NAME=RMYSHIP VALUE=0 $radio>Ʃ�ᤵ����

<INPUT TYPE="radio" NAME=RMYSHIP VALUE=1 $radio2>Ʃ�ᤵ���ʤ�
<INPUT TYPE="submit" VALUE="�ѹ�����" NAME="MyShipImgMode">
</FORM>
END
	my($Hskinflag);
	if($HskinName eq '' || $HskinName eq "$HcssFile"){
		$Hskinflag = '<span class=attention>̤����</span>';
	} else {
		$Hskinflag = $HskinName;
	}
	my $select_list = "<OPTION value='del' selected>�ǥե����\n";
	foreach(0 .. $#HskinList) {
		$Hskinflag = $HskinName[$_] if($HskinList[$_] eq $HskinName);
		$select_list .= "<OPTION value='$HskinList[$_]'>$HskinName[$_]\n";
	}
	out(<<END);
<hr><div id='hakoSkin'>
<h1>�������륷���Ȥ�����</h1>
���ߤ�����<b>[</b> ${Hskinflag} <b>]</b>
<form action=$HthisFile method=POST>
<SELECT NAME="SKIN">$select_list</SELECT>
<INPUT TYPE="submit" VALUE="����" name=SKINSET>
</form>
</div>
END
		if($Hlocalimage) {
			my $setsumei = ($Hlocalimagehtml ne '') ? "<p>�ܤ�����<a href=\"${Hlocalimagehtml}\"target=\"_blank\">�����Υڡ���</a>������������ </p>" : "";
			my $dlimg = ($HlocalImg ne '') ? "������<B><a href=\"$HlocalImg\">����</a></B>�����������ɤ��Ʋ�������<br>" : "";
			my $Himfflag = ($HimgLine eq '') ? '<FONT COLOR=RED>̤����</FONT>' : $HimgLine;
			out(<<END);
<HR>
<TABLE><TR><TD style="border-width:0px;" >
<H1>�����Υ���������</H1>
$dlimg
���ȤΥܥ���򥯥�å����ѥ�����Υ�����ǥ�������Ȣ�������¸�ե������land0.gif������Ǥ���������<BR>
����Υե�����ޤǤΥ롼�Ȥ����Ʊѿ����ΤߤΥե����̾��侩���ޤ���<BR>
Ⱦ�ѥ��ʤϻ����Բ�ǽ�Ǥ���Ⱦ�ѥ��ڡ�����%20�˼�ư�ִ�����ޤ���<BR>
�ޤ�����������ꤹ��Ȼ��꤬�������ޤ���<BR><BR>
$setsumei
���ߤ�����<B>[</b> ${Himfflag} <B>]</B>
<form action=$HthisFile method=POST>
<INPUT TYPE=file NAME="IMGLINE" SIZE="80">
<INPUT TYPE="submit" VALUE="����" name=IMGSET>
</form>

<form action=$HthisFile method=POST>
ľ�ܻ����Mac�桼�����ѡ�<BR>
��(WIN) D:\\image\\hakogif<BR>
<INPUT TYPE=text NAME="IMGLINEMAC" SIZE="80">
<INPUT TYPE="submit" VALUE="����" name=IMGSET><BR>
Mac�򿨤ä����Ȥ��ʤ��ΤǤ褯�狼��ޤ���<BR>
</form>

</TD></TR></TABLE>
END

			return;
		} else {
			return;
		}
	}
	out(<<END);
<DIV ID='RecentlyLog'>
<H1>�Ƕ�ν����</H1>
[<A HREF="${HbaseDir}/history.cgi?saikin=99" class=\"M\" TARGET=_blank>���${HtopLogTurn}������ʬ�Υ���ɽ��</A>]<BR><BR>
</DIV>
END
	for($i=0; $i < $HrepeatTurn; $i++){
		logFilePrint($i, 0, 0);
	}
	out(<<END);
<DIV ID='RecentlyLog'>
<H1>ȯ���ε�Ͽ</H1>
END
	historyPrint();
	out("</DIV>");
}

# �ر�ɽ��ɽ��
sub campInfoList {
	if(($Hallyflg) && (open(LIN, "${HlogdirName}/ally.log"))){
	out(<<END);
<HR><DIV ID='campInfo'>
<H1>�ƿرĤξ���</H1>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���롼��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}��͸�${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}��ͭΨ${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}������${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}��к���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}������${H_tagTH}</TH>
</TR>
END
	my($i, $line, @ally, @apop, $up);
	$i = 1;
	while($line = <LIN>){
		# ������,�ر�ID,���,��͸�,������,��к���,������
		@ally = split(/,/, $line);
		if($ally[0] != $HislandTurn){
			$apop[$ally[1]] = $ally[3];
			next;
		}
		out("<TR><TD $HbgNumberCell align=center><a href=\"$HthisFile?alist=$ally[1]\" class=\"M\">${HtagNumber_}$i${H_tagNumber}</a></TD>");
		if($ally[1] == 0){
			out("<TD $HbgNameCell>$Hallygroup[$ally[1]]</TD>");
		}else{
			out("<TD $HbgNameCell>$Hallymark[$ally[1]]${HtagTH_}$Hallygroup[$ally[1]]${H_tagTH}</TD>");
		}
		out("<TD $HbgInfoCell>$ally[2]</TD>");
		if(($HislandTurn % $HturnPrizeVarious) == 0){
			$up = "";
		}else{
			if($apop[$ally[1]] > $ally[3] + 100){
				$up = "��";
			}elsif($apop[$ally[1]] < $ally[3] - 100){
				$up = "��";
			}else{
				$up = "��";
			}
		}
		out("<TD $HbgInfoCell>$ally[3]${HunitPop} <B>$up</B></TD>");
		out("<TD $HbgInfoCell>$ally[7]%</TD>");
		out("<TD $HbgInfoCell>$ally[4]${HunitArea}</TD>");
		out("<TD $HbgInfoCell>$ally[5]${HunitMoney}</TD>");
		out("<TD $HbgInfoCell>$ally[6]P</TD></TR>");
		$i++;
	}
	close(LIN);
	out("</TABLE>");
	out("[<A HREF=\"${HbaseDir}/history.cgi?ally=0\" class=\"M\" TARGET=_blank>���Υǡ���</a>]</DIV>");
	}
}
sub topPageAlist {
	out(<<END);
${HtagTitle_}$Htitle${HtagTitle2_}$Htitle2${H_tagTitle}${H_tagTitle}
<br><br>
����Ԥ걣����ǽ���ä��ꤹ�롦������(<A HREF="${HthisFile}" class="M">�̾�ΰ������̤����</A>)<br>
<h2>$Hallygroup[$Halistmode]��$Hallymark[$Halistmode]����°����</h2>
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
<INPUT TYPE="button" VALUE="����åץܡ��ɤ˥��ԡ�" onClick="textcopy(searchID('ALIST').value)">
��������Ȥ���Ž���դ��ƻȤäƤ���������<br>
<textarea NAME="ALIST" cols="100" rows="10">
END

	my($i,$island,$id,$name,$pop,$money,$food,$weapon);
	out("��̾\t�͸�\t���\t����\tʼ��\n");
	for($i = 0; $i < $HislandNumber; $i++){
		$island = $Hislands[$i];
		my($tAlly) = $island->{'ally'};
		if($Halistmode == $tAlly){
			$id = $island->{'id'};
			$name = $island->{'name'};
			$pop = $island->{'pop'} . $HunitPop;
			if($HhideMoneyMode == 1) {
				$money = $island->{'money'} . $HunitMoney;
			} elsif($HhideMoneyMode == 2) {
				$money = aboutMoney($island->{'money'});
			} else {
				$money = '��̩';
			}
			$food = $island->{'food'} . $HunitFood;
			$weapon = $island->{'weapon'} . $HunitWeapon;
			out("$name$AfterName\t$pop\t$money\t$food\t$weapon\n");
		}
	}
	out("</textarea>");
	# �ر�ɽ��ɽ��
	&campInfoList;
}

# ��Ͽ�ե�����ɽ��
sub historyPrint {
	open(HIN, "${HlogdirName}/hakojima.his");
	my(@line, $l);
	while($l = <HIN>) {
		chomp($l);
		push(@line, $l);
	}
	@line = reverse(@line);

	foreach $l (@line) {
		$l =~ /^([0-9]*),(.*)$/;
		out("${HtagNumber_}������${1}${H_tagNumber}��${2}<BR>\n");
	}
	close(HIN);
}

1;
