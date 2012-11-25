#----------------------------------------------------------------------
# �ʣ��֣�������ץ��� -ver1.11-
# ���Ѿ�������ˡ���ϡ����۸��Ǥ���ǧ��������
# ��°��js-readme.txt�⤪�ɤ߲�������
# ���äݡ���http://appoh.execweb.cx/hakoniwa/
#----------------------------------------------------------------------
# ���ۤ�Ȣ��  (ver5.52c)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �ʣ���᥹����ץȳ�ȯ����
#----------------------------------------------------------------------
# �����糫ȯ�ײ�

sub tempOwnerJava {
	$mapSize = ($HislandSize > $HoceanSize) ? $HislandSize : $HoceanSize;
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# ���ޥ�ɥ��å�
	$set_com = "";
	$com_max = "";
	for($i = 0; $i < $HcommandMax; $i++) {
		# �����Ǥμ��Ф�
		my($command) = $island->{'command'}->[$i];
		my($s_kind, $s_target, $s_x, $s_y, $s_arg, $s_tx, $s_ty) = 
		(
		$command->{'kind'},
		$command->{'target'},
		$command->{'x'},
		$command->{'y'},
		$command->{'arg'},
		$command->{'tx'},
		$command->{'ty'}
		);
		# ���ޥ����Ͽ
		if($i == $HcommandMax-1){
			$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\,$s_tx\,$s_ty\]\n";
			$com_max .= "0"
		}else{
			$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\,$s_tx\,$s_ty\]\,\n";
			$com_max .= "0,"
		}
	}

	# ���硼�ȥ��åȥ���������
	$keyName[$HcomPrepare2]	= "(Z)";
	$keyName[$HcomPlant]	= "(S)";
	$keyName[$HcomReclaim]	= "(U)";
	$keyName[$HcomDestroy]	= "(K)";
	$keyName[$HcomFarm]		= "(N)";
	$keyName[$HcomPresent]	= "(P)";
	$keyName[$HcomBase]		= "(B)";
	$keyName[$HcomDbase]	= "(D)";

	#���ޥ�ɥꥹ�ȥ��å�
	my($l_kind,$l_cost,$str);
	$set_listcom = "";
	$click_com = "";
	$click_com2 = "";
	$All_listCom = 0;
	$com_count = @HcommandDivido;
	for($m = 0; $m < $com_count; $m++) {
		($aa,$dd,$ff) = split(/,/,$HcommandDivido[$m]);
		$set_listcom .= "\[ ";
		for($i = 0; $i < $HcommandTotal; $i++) {
			$l_kind = $HcomList[$i];
			$l_cost = $HcomCost[$l_kind];
			if($l_cost == 0) { $l_cost = '̵��'	}
			elsif($l_cost < 0) { $l_cost = - $l_cost; $l_cost .= $HunitFood; }
			else { $l_cost .= $HunitMoney; }
			if($l_kind > $dd-1 && $l_kind < $ff+1) {
				$set_listcom .= "\[$l_kind\,\'$HcomName[$l_kind]\',\'$l_cost\'\]\,\n";
				if($l_kind == $HcomHaribote || $l_kind == $HcomPolice || $l_kind == $HcomMyhome || $l_kind == $HcomDon || $l_kind == $HcomUg){
					# ����
				}else{
					$str = "<a href='javascript:void(0);' onClick='cominput(myForm,6,$l_kind,0)' class='M' TITLE='$l_cost'>$HcomName[$l_kind]$keyName[$l_kind]</a>";
					if($m == 0 || $l_kind == $HcomFlower){
						if($l_kind == $HcomPrepare2){
							$click_com .= "$str (<a href='javascript:void(0);' onClick='cominput(myForm,8,$l_kind,0)' class='M' TITLE='$l_cost'>ALL</a>)<br>\n";
						}else{
							$click_com .= "$str<br>\n";
						}
					}elsif($m == 1){
						$click_com2 .= "$str<br>\n";
					}
				}
				$click_com2 .= "<hr>" if($l_kind == $HcomSFarm);
				$All_listCom++;
			}
			next if($l_kind < $ff+1);
		}
		$bai = length($set_listcom);
		$set_listcom = substr($set_listcom, 0,$bai-2);
		$set_listcom .= " \],\n";
	}
	$bai = length($set_listcom);
	$set_listcom = substr($set_listcom, 0,$bai-2);
	$default_Kind = (($HdefaultKind eq '') || ($HdefaultKind eq '��������������������')) ? 1 : $HdefaultKind;

	# �ꥹ�Ȥ��ɲ�
	$l_cost = $HcomCost[$HcomShip];
	$l_cost .= $HunitMoney;
	$click_com .= "<a href='javascript:void(0);' onClick='cominput(myForm,6,$HcomShip,0)' class='M' TITLE='$l_cost'>$HcomName[$HcomShip]</a>$keyName[$HcomShip]<br>\n";
	$l_cost = $HcomCost[$HcomEmigration];
	$l_cost = - $l_cost; $l_cost .= $HunitFood;
	$click_com .= "<a href='javascript:void(0);' onClick='cominput(myForm,6,$HcomEmigration,0)' class='M' TITLE='$l_cost'>$HcomName[$HcomEmigration]</a>$keyName[$HcomEmigration]<br>\n";

	# �ץ쥼���
	$click_com3 .= "�ץ쥼��ȷ���(̵��)<br>\n";
	$click_com3 .= "�ץ쥼��Ⱦ���(̵��)<br><br>\n";
	my($present) = $island->{'present'};
	my($Park, $Stadium, $Dome, $Casino, $Amusement, $School, $Airport, $Bigcity, $Zoo, $Expo, $MonMonu, $Saigai, $yobi2, $yobi3) = 
	(
		$present->[0],
		$present->[1],
		$present->[2],
		$present->[3],
		$present->[4],
		$present->[5],
		$present->[6],
		$present->[7],
		$present->[8],
		$present->[9],
		$present->[10],
		$present->[11],
		$present->[12],
		$present->[13]
	 );
	if(($Park + $Stadium + $Dome + $Casino + $Amusement + $School + $Airport + $Bigcity + $Zoo + $Expo + $MonMonu + $Saigai) == 0) {
		$click_com3 .= "�ץ쥼��ȤϤ���ޤ���<br><br>\n";
	} else {
		my $tmp = "<a href='javascript:void(0);' class='M' onClick='cominput(myForm,6,";
		if($Park > 0) {
			$click_com3 .= "${tmp}16,0)'>�������</a><br>\n";
			$click_com3 .= "${tmp}98,0)'>�������($Park)</a><br>\n";
		}
		if($Stadium > 0) {
			$click_com3 .= "${tmp}16,1)'>�������������</a><br>\n";
			$click_com3 .= "${tmp}98,1)'>�������������($Stadium)</a><br>\n";
		}
		if($Dome > 0) {
			$click_com3 .= "${tmp}16,2)'>�ɡ������</a><br>\n";
			$click_com3 .= "${tmp}98,2)'>�ɡ������($Dome)</a><br>\n";
		}
		if($Casino > 0) {
			$click_com3 .= "${tmp}16,3)'>�����η���</a><br>\n";
			$click_com3 .= "${tmp}98,3)'>�����ξ���($Casino)</a><br>\n";
		}
		if($Amusement > 0) {
			$click_com3 .= "${tmp}16,4)'>ͷ���Ϸ���</a><br>\n";
			$click_com3 .= "${tmp}98,4)'>ͷ���Ͼ���($Amusement)</a><br>\n";
		}
		if($School > 0) {
			$click_com3 .= "${tmp}16,5)'>�ع�����</a><br>\n";
			$click_com3 .= "${tmp}98,5)'>�ع�����($School)</a><br>\n";
		}
		if($Airport > 0) {
			$click_com3 .= "${tmp}16,6)'>��������</a><br>\n";
			$click_com3 .= "${tmp}98,6)'>��������($Airport)</a><br>\n";
		}
		if($Bigcity > 0) {
			$click_com3 .= "${tmp}16,7)'>���ԻԷ���</a><br>\n";
			$click_com3 .= "${tmp}98,7)'>���ԻԾ���($Bigcity)</a><br>\n";
		}
		if($Zoo > 0) {
			$click_com3 .= "${tmp}16,8)'>ưʪ�����</a><br>\n";
			$click_com3 .= "${tmp}98,8)'>ưʪ�����($Zoo)</a><br>\n";
		}
		if($Expo > 0) {
			$click_com3 .= "${tmp}16,9)'>���������</a><br>\n";
			$click_com3 .= "${tmp}98,9)'>���������($Expo)</a><br>\n";
		}
		if($MonMonu > 0) {
			$click_com3 .= "${tmp}16,10)'>���õ�ǰ�����</a><br>\n";
			$click_com3 .= "${tmp}98,10)'>���õ�ǰ�����($MonMonu)</a><br>\n";
		}
		if($Saigai > 0) {
			$click_com3 .= "${tmp}16,11)'>�ҳ��������</a><br>\n";
			$click_com3 .= "${tmp}98,11)'>�ҳ��������($Saigai)</a><br>\n";
		}
	}
	
	#��ꥹ�ȥ��å�
	my($set_island, $l_name, $l_id, $l_ally);
	$set_island = "";
	for($i = 0; $i < $HislandNumber; $i++) {
		$l_name = $Hislands[$i]->{'name'};
		$l_name =~ s/'/\\'/g;
		$l_id = $Hislands[$i]->{'id'};
		if($Hallyflg){
			$l_ally = $Hislands[$i]->{'ally'};
			$l_ally = $Hallymark[$l_ally] . " ";
		}else{
			$l_ally = "";
		}
		if($i == $HislandNumber-1){
			$set_island .= "'$l_id'\:\'$l_ally$l_name\'\n";
		}else{
			$set_island .= "'$l_id'\:\'$l_ally$l_name\'\,\n";
		}
	}
	tempOwnerHeader();
	out(<<END);
<SCRIPT Language="JavaScript">
<!--
// �ʣ��֣�������ץȳ�ȯ�������۸�
// ���äݡ���Ȣ������ http://appoh.execweb.cx/hakoniwa/ ��
// Programmed by Jynichi Sakai(���äݡ�)
// �� ������ʤ��ǲ�������
var xmlhttp;
var str;
g = [$com_max];
k1 = [$com_max];
k2 = [$com_max];
tmpcom1 = [ [0,0,0,0,0,0,0] ];
tmpcom2 = [ [0,0,0,0,0,0,0] ];
command = [$set_com];
comlist = [$set_listcom];
islname = {$set_island};
function init(){
	for(i = 0; i < command.length ;i++) {
		for(s = 0; s < $com_count ;s++) {
			var comlist2 = comlist[s];
			for(j = 0; j < comlist2.length ; j++) {
				if(command[i][0] == comlist2[j][0]) {
					g[i] = comlist2[j][1];
				}
			}
		}
	}
	outp();
	str = plchg();
	str = "<TABLE border=0><TR><TD class='commandjs1'><B>�ݡݡݡ� �����Ѥ� �ݡݡݡ�</B><br><br>"+str+"<br><B>�ݡݡݡ� �����Ѥ� �ݡݡݡ�</B></TD></TR></TABLE>";
	disp(str, "#ccffcc");
	xmlhttp = new_http();
	if(document.layers) {
		document.captureEvents(Event.MOUSEMOVE | Event.MOUSEUP);
	}
	document.onmouseup   = Mup;
	document.onmousemove = Mmove;
	document.onkeydown = Kdown;
	document.ch_numForm.AMOUNT.options.length = 69;
	for(i=0;i<document.ch_numForm.AMOUNT.options.length;i++){
		document.ch_numForm.AMOUNT.options[i].value = i;
		document.ch_numForm.AMOUNT.options[i].text  = i;
		if(i>=50){
			document.ch_numForm.AMOUNT.options[i].value = (i-49) * 50;
			document.ch_numForm.AMOUNT.options[i].text  = (i-49) * 50;
		}
	}
	document.myForm.CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}.disabled = true;
	ns(0);
}

function cominput(theForm, x, k, pp, z) {
	a = theForm.NUMBER.options[theForm.NUMBER.selectedIndex].value;
	b = theForm.COMMAND.options[theForm.COMMAND.selectedIndex].value;
	c = theForm.POINTX.options[theForm.POINTX.selectedIndex].value;
	d = theForm.POINTY.options[theForm.POINTY.selectedIndex].value;
	e = theForm.AMOUNT.options[theForm.AMOUNT.selectedIndex].value;
	f = theForm.TARGETID.options[theForm.TARGETID.selectedIndex].value;
	cc = theForm.POINTTX.options[theForm.POINTTX.selectedIndex].value;
	dd = theForm.POINTTY.options[theForm.POINTTY.selectedIndex].value;
	var newNs = a;
	if(x == 8){x = 6;e = 22}
	if(x == 1 || x == 2 || x == 6){
		if(x == 6){
			b = k;
			if(pp != 0) {e = pp;}
		}
		if(x != 2) {
			for(i = $HcommandMax - 1; i > a; i--) {
				command[i] = command[i-1];
				g[i] = g[i-1];
			}
		}
		for(s = 0; s < $com_count ;s++) {
			var comlist2 = comlist[s];
			for(i = 0; i < comlist2.length; i++){
				if(comlist2[i][0] == b){
					g[a] = comlist2[i][1];
					break;
				}
			}
		}
		command[a] = [b,c,d,e,f,cc,dd];
		newNs++;
		menuclose();
	}else if(x == 3){
		var num = (k) ? k-1 : a;
		for(i = Math.floor(num); i < ($HcommandMax - 1); i++) {
			command[i] = command[i + 1];
			g[i] = g[i+1];
		}
		command[$HcommandMax-1] = [97,0,0,0,0,0,0];
		g[$HcommandMax-1] = '��ⷫ��';
	}else if(x == 4){
		i = Math.floor(a)
		if (i == 0){ return true; }
		i = Math.floor(a)
		tmpcom1[i] = command[i];tmpcom2[i] = command[i - 1];
		command[i] = tmpcom2[i];command[i-1] = tmpcom1[i];
		k1[i] = g[i];k2[i] = g[i - 1];
		g[i] = k2[i];g[i-1] = k1[i];
		newNs = i-1;
	}else if(x == 5){
		i = Math.floor(a)
		if (i == $HcommandMax-1){ return true; }
		tmpcom1[i] = command[i];tmpcom2[i] = command[i + 1];
		command[i] = tmpcom2[i];command[i+1] = tmpcom1[i];
		k1[i] = g[i];k2[i] = g[i + 1];
		g[i] = k2[i];g[i+1] = k1[i];
		newNs = i+1;
	}else if(x == 7){
		// ��ư
		var ctmp = command[k];
		var gtmp = g[k];
		if(z > k) {
			// �夫�鲼��
			for(i = k; i < z-1; i++) {
				command[i] = command[i+1];
				g[i] = g[i+1];
			}
		} else {
			// ��������
			for(i = k; i > z; i--) {
				command[i] = command[i-1];
				g[i] = g[i-1];
			}
		}
		command[i] = ctmp;
		g[i] = gtmp;
	}else if(x == 9){
		command[a][3] = k;
	}

	str = plchg();
	str = "<TABLE border=0><TR><TD class='commandjs2'><B>�ݡݡݡݡ�̤�����ݡݡݡݡ�</B><br><br>"+str+"<br><B>�ݡݡݡݡ�̤�����ݡݡݡݡ�</B></TD></TR></TABLE>";
	disp(str, "white");
	outp();
	theForm.CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}.disabled = false;
	ns(newNs);
	return true;
}

function plchg(){
	strn1 = "";
	for(i = 0; i < $HcommandMax; i++)	{
		c = command[i];
		kind = '$HtagComName_' + g[i] + '$H_tagComName';
		x = c[1];
		y = c[2];
		tgt = c[4];
		xx = c[5];
		yy = c[6];
		point = '${HtagName_}(' + x + ',' + y + ')${H_tagName}';
		point2 = '${HtagName_}(' + xx + ',' + yy + ')${H_tagName}';
		if(tgt == ''){
			tgt = '$HtagName_' + '̵��' + '${AfterName}${H_tagName}';
		}else{
			tgt = '$HtagName_' + islname[tgt] + '${AfterName}${H_tagName}';
		}
		if(c[0] == $HcomDoNothing || c[0] == $HcomGiveup || c[0] == $HcomSMissileMGM){ // ��ⷫ�ꡢ�������
			strn2 = kind;
		}else if(c[0] == $HcomMissileNM || // �ߥ������Ϣ
			c[0] == $HcomMissilePP ||
			c[0] == $HcomBioMissile ||
			c[0] == $HcomMissileSPP ||
			c[0] == $HcomMissileST ||
			c[0] == $HcomMissileRM ||
			c[0] == $HcomMissileSRM ||
			c[0] == $HcomMissileGM ||
			c[0] == $HcomMissilePLD ||
			c[0] == $HcomMissileNCM ||
			c[0] == $HcomMissileDM ||
			c[0] == $HcomSMissileGM ||
			c[0] == $HcomSMissilePP ||
			c[0] == $HcomSMissile ||
			c[0] == $HcomOMissileNM ||
			c[0] == $HcomOMissilePP ||
			c[0] == $HcomOMissileSPP ||
			c[0] == $HcomMissileRNG ||
			c[0] == $HcomMissileLD) {
			if(c[0] == $HcomSMissileGM || c[0] == $HcomSMissilePP || c[0] == $HcomSMissile) {
				tgt = '$HtagName_' + "$SpaceName" + '${H_tagName}';
			}else if(c[0] == $HcomOMissileNM || c[0] == $HcomOMissilePP || c[0] == $HcomOMissileSPP) {
				tgt = '$HtagName_' + "$OceanName" + '${H_tagName}';
			}
			if(c[0] == $HcomMissileGM) { c[3] = 1; }
			if(c[3] == 0){
				arg = '($HtagName_̵����${H_tagName})';
			} else {
				arg = '($HtagName_' + c[3] + 'ȯ${H_tagName})';
			}
			strn2 = tgt + point + "��" + kind + arg;
		}else if(c[0] == $HcomMissileMGM) {
			strn2 = tgt + "��" + kind;
		}else if(c[0] == $Hcomcolony) {
			if(c[3] == 1 || c[3] == 2){
				strn2 = "�����ѡ�������ɥ����ƥ�ȯư����" + '(' + c[3] + ')';
			}else{
				strn2 = tgt + "��" + kind;
			}
		}else if(c[0] == $HcomTeisatu || c[0] == $HcomSpy) { // ��������廡
			strn2 = tgt + point + "��" + kind;
		}else if(c[0] == $HcomSendMonster){ // �����ɸ�
			if(c[3] == 1){
				strn2 = tgt + '$HtagName_�إᥫ�����ɸ�${H_tagName}';
			} else if(c[3] == 2){
				strn2 = tgt + '$HtagName_�إ���ƥͥ����Τ��ɸ�${H_tagName}';
			} else if(c[3] == 3){
				strn2 = tgt + '$HtagName_�س���ᥫ���Τ��ɸ�${H_tagName}';
			} else {
				strn2 = tgt + '$HtagName_�إᥫ���Τ��ɸ�${H_tagName}';
			}
		}else if(c[0] == $HcomSSendMonster) {
			strn2 = tgt + '��' + kind + '${HtagName_}��' + c[3] + '��${H_tagName}';
		}else if(c[0] == $HcomSell){ // �������
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * 100;
			arg = '$HtagName_' + arg + '$HunitFood${H_tagName}';
			strn2 = kind + arg;
		}else if(c[0] == $HcomOreSell || c[0] == $HcomOilSell || c[0] == $HcomWeponSell){ // ���
			if(c[3] == 0){ c[3] = 1; }
			arg = '$HtagName_��' + c[3] + '��${H_tagName}';
			strn2 = tgt + "��" + kind + arg;
		}else if(c[0] == $HcomOreBuy || c[0] == $HcomOilBuy || c[0] == $HcomWeponBuy){ // ����
			if(c[3] == 0){ c[3] = 1; }
			arg = '$HtagName_��' + c[3] + '��${H_tagName}';
			strn2 = kind + arg;
		}else if(c[0] == $HcomWarp){ // ž������
			if(c[3] == 0) {
				strn2 = point + "��" + kind + "��" + tgt + "�Ԥ���";
			} else {
				if(c[3] == 1) {
					direction = "����";
				} else if(c[3] == 2) {
					direction = "��";
				} else if(c[3] == 3) {
					direction = "����";
				} else if(c[3] == 4) {
					direction = "����";
				} else if(c[3] == 5) {
					direction = "��";
				} else {
					c[3] = 6;
					direction= "����";
				}
				kind = '$HtagComName_' + "ž�������ַ���" + '$H_tagComName';
				strn2 = point + "��" + kind + '��${HtagName_}' + direction + '${H_tagName}��';
			}
		}else if(c[0] == $HcomPropaganda){ // Ͷ�׳�ư
			if(c[3] == 0){
				strn2 = kind;
			} else {
				strn2 = kind + '($HtagName_' + c[3] + '��${H_tagName})';
			}
		}else if(c[0] == $HcomMoney){ // �����

			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * $HcomCost[$HcomMoney];
			arg = '($HtagName_' + arg + '$HunitMoney${H_tagName})';
			strn2 = tgt + "��" + kind + arg;
		}else if(c[0] == $HcomFood){ // �������

			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * 100;
			arg = '($HtagName_' + arg + '$HunitFood${H_tagName})';
			strn2 = tgt + "��" + kind + arg;
		}else if(c[0] == $HcomEmigration){ // ��̱
			strn2 = point + "�οͤ�" + tgt + "��" + kind;
		}else if(c[0] == $HcomDestroy){ // ����

			if(c[3] == 0){
				strn2 = point + "��" + kind;
			} else {
				arg = c[3] * $HcomCost[$HcomDestroy];
				arg = '(ͽ\��$HtagName_' + arg + '$HunitMoney${H_tagName})';
				strn2 = point + "��" + kind + arg;
			}
		}else if(c[0] == $HcomSearch || c[0] == $HcomBank){ // �ϼ�Ĵ��,������

			arg = c[3] * $HcomCost[$HcomSearch];
			if(arg == 0) {
				arg = $HcomCost[$HcomSearch]
			}
			arg = '(ͽ\��$HtagName_' + arg + '$HunitMoney${H_tagName})';
			strn2 = point + "��" + kind + arg;
		}else if(c[0] == $HcomDummy){ // ���ߡ�
			if(c[3] == 1) {
				strn2 = point + '$HtagName_�ǥ��ߡ��η���${H_tagName}';
			} else if(c[3] == 2) {
				strn2 = point + '$HtagName_�ǥ��ߡ����Ω��${H_tagName}';
			} else {
				strn2 = point + '$HtagName_�ǥ��ߡ�����${H_tagName}';
			}
		}else if(c[0] == $HcomManipulate || c[0] == $HcomSTManipulate || c[0] == $HcomShipM){
			// ������ST�����������
			if(c[3] <= 1) {
				c[3] = 1;
				direction = "����";
			} else if(c[3] == 2) {
				direction = "��";
			} else if(c[3] == 3) {
				direction = "����";
			} else if(c[3] == 4) {
				direction = "����";
			} else if(c[3] == 5) {
				direction = "��";
			} else {
				c[3] = 6;
				direction= "����";
			}
			if(c[0] == $HcomMonsEnsei){
				strn2 = kind + '��${HtagName_}' + direction + '${H_tagName}��';
			}else{
				strn2 = tgt + "��" + kind + '��${HtagName_}' + direction + '${H_tagName}��';
			}
		}else if(c[0] == $HcomMonument){ // ��ǰ��
			if(c[3] == 0) {
				strn2 = point + "��" + kind + '($HtagName_��Υꥹ${H_tagName})' + tgt;
			} else if(c[3] == 1) {
				strn2 = point + "��" + kind + '($HtagName_ʿ�µ�ǰ${H_tagName})' + tgt;
			} else if(c[3] == 2) {
				strn2 = point + "��" + kind + '($HtagName_�襤����${H_tagName})' + tgt;
			} else if(c[3] == 3) {
				strn2 = point + "��" + kind + '($HtagName_������ǰ��${H_tagName})' + tgt;
			} else {
				strn2 = point + "��" + kind;
			}
		}else if(c[0] == $HcomSMonument){ // ���쵭ǰ��
			if(c[3] == 0) {
				strn2 = point + "��" + kind + '($HtagName_���쵭ǰ��${H_tagName})' + tgt;
			} else if(c[3] == 1) {
				strn2 = point + "��" + kind + '($HtagName_���쵭ǰ��(��)${H_tagName})' + tgt;
			} else {
				strn2 = point + "��" + kind;
			}
		}else if(c[0] == $HcomDbase){
			if(c[3] == 1) {
				strn2 = point + "��" + kind + '(${HtagName_}ST${H_tagName})';
			} else if(c[3] == 2) {
				strn2 = point + "��" + kind + '(${HtagName_}̸${H_tagName})';
			} else {
				strn2 = point + "��" + kind;
			}
		}else if(c[0] == $HcomFarm || // ʣ���󤢤�ײ�
			c[0] == $HcomFactory ||
			c[0] == $HcomSFarm ||
			c[0] == $HcomTower ||
			c[0] == $HcomPort ||
			c[0] == $HcomBase ||
			c[0] == $HcomMountain) {
			if(c[3] != 0){
				arg = '($HtagName_' + c[3] + '��${H_tagName})';
				strn2 = point + "��" + kind + arg;
			}else{
				strn2 = point + "��" + kind;
			}
		}else if(c[0] == $HcomPresent || c[0] == $HcomPresentAid){ // �ץ쥼��ȡ��ץ쥼��Ⱦ���
			if(c[3] <= 0) {
				c[3] = 0;
				pres = "����";
			} else if(c[3] == 1) {
				pres = "����������";
			} else if(c[3] == 2) {
				pres = "�ɡ���";
			} else if(c[3] == 3) {
				pres = "������";
			} else if(c[3] == 4) {
				pres = "ͷ����";
			} else if(c[3] == 5) {
				pres = "�ع�";
			} else if(c[3] == 6) {
				pres = "����";
			} else if(c[3] == 7) {
				pres = "���Ի�";
			} else if(c[3] == 8) {
				pres = "ưʪ��";
			} else if(c[3] == 9) {
				pres= "������";
			} else if(c[3] == 10) {
				pres= "���õ�ǰ��";
			} else {
				c[3] = 11;
				pres= "�ҳ�����";
			}
			if(c[0] == $HcomPresent) {
				strn2 = point + "��" + kind + '��${HtagName_}' + pres + '${H_tagName}��';
			} else {
				strn2 = tgt + "��" + kind + '��${HtagName_}' + pres + '${H_tagName}��';
			}
		// ���åХȥ�

		} else if(c[0] == $HcomMonsEgg ||
			c[0] == $HcomMonsEsa ||
			c[0] == $HcomMonsTettai ||
			c[0] == $HcomMonsExer ||
			c[0] == $HcomMonsSell) {
			strn2 = kind;
		} else if(c[0] == $HcomMonsEnsei ||
			c[0] == $HcomMonsEsaAid ||
			c[0] == $HcomMonsAid) {
			strn2 = tgt + "��" + kind;
		// �ϲ���
		} else if(c[0] == $HcomUg){
			if(c[3] == 0) {
				strn2 = point + "���ϲ�" + point2 + "��"+ kind + '($HtagName_�ϲ��ԻԷ���${H_tagName})';
			} else if(c[3] == 1) {
				strn2 = point + "���ϲ�" + point2 + "��"+ kind + '($HtagName_�ϲ��������${H_tagName})';
			} else if(c[3] == 2) {
				strn2 = point + "���ϲ�" + point2 + "��"+ kind + '($HtagName_�ϲ��������${H_tagName})';
			} else if(c[3] == 3) {
				strn2 = point + "���ϲ�" + point2 + "��"+ kind + '($HtagName_�ϲ��ߥ�������Ϸ���${H_tagName})';
			} else if(c[3] == 4) {
				strn2 = point + "���ϲ�" + point2 + "��"+ kind + '($HtagName_�ϲ����������������${H_tagName})';
			} else {
				strn2 = point + "���ϲ�" + point2 + "��"+ kind;
			}
		} else if(c[0] == $HcomShip) {
			// �������ѹ�
			if(c[3] <= 0) {
				c[3] = 0;
				pres = "�ü�";
			} else if(c[3] == 1) {
				pres = "��ư";
			} else if(c[3] == 2) {
				pres = "�ɸ�";
			} else if(c[3] == 3) {
				pres = "ű��";
			} else if(c[3] >= 4) {
				pres = '����';
				c[3] = 4;
			}
			strn2 = tgt + point + "��" + kind + '��${HtagName_}' + pres + '${H_tagName}��';
		} else if(c[0] == $HcomShipbuild) {
			// ¤��
			strn2 = point + "��" + kind + '��${HtagName_}' + c[3] + '${H_tagName}��';
		} else if(c[0] == $HcomSBuild) {
			// ������߷�
			strn2 = "�����ĥͽ��̿��(���⤪���ޤ���)";
		} else if(c[0] == $HcomSUnit || c[0] == $HcomSpaceFarm || c[0] == $HcomSFactory || c[0] == $HcomSpaceBase) {
			tgt = '$HtagName_' + "$SpaceName" + '${H_tagName}';
			if(c[3] != 0){
				arg = '($HtagName_' + c[3] + '��${H_tagName})';
				strn2 = tgt + point + "��" + kind + arg;
			}else{
				strn2 = tgt + point + "��" + kind;
			}
		} else if(c[0] == $HcomSPioneer || c[0] == $HcomSOccupy || c[0] == $HcomSDestroy || c[0] == $HcomSDbase) {
			tgt = '$HtagName_' + "$SpaceName" + '${H_tagName}';
			strn2 = tgt + point + "��" + kind;
		} else if(c[0] == $HcomSEisei){
			if(c[3] <= 0) {
				c[3] = 0;
				pres = "$HsEisei[0]";
			} else if(c[3] == 1) {
				pres = "$HsEisei[1]";
			} else if(c[3] == 2) {
				pres = "$HsEisei[2]";
			} else if(c[3] == 3) {
				pres = "$HsEisei[3]";
			} else if(c[3] >= 4) {
				pres = "$HsEisei[4]";
				c[3] = 4;
			}
			tgt = '$HtagName_' + "$SpaceName" + '${H_tagName}';
			strn2 = tgt + point + "��" + kind + '��${HtagName_}' + pres + '${H_tagName}��';
		} else if(c[0] == $HcomSFood) {
			// ���迩���Ǿ夲
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * 100;
			arg = '($HtagName_' + arg + '$HunitFood${H_tagName})';
			strn2 = kind + arg;
		} else if(c[0] == $HcomPrepare2 && c[3] == 22) {
			strn2 = '$HtagComName_' + "���������Ϥʤ餷" + '${H_tagComName}';
		}else{
			strn2 = point + "��" + kind;
		}
		tmpnum = '';
		if(i < 9){ tmpnum = '0'; }
		strn1 += 
			'<div id="com_'+i+'" '+
			'onmouseover="mc_over('+i+');return false;" '+
			'><A STYLE="text-decoration:none;color:000000" HREF="JavaScript:void(0);" onClick="ns(' + i + ')" '+
			'onmousedown="return comListMove('+i+');" '+
			'ondblclick="chNum('+c[3]+');return false;" '+
			'><NOBR>' + tmpnum + (i + 1) + ':' + strn2 + '</NOBR></A></div>\\n';
	}
	return strn1;
}

function disp(str,bgclr){
	if(str==null)  str = "";

	if(document.getElementById || document.all){
		LayWrite('LINKMSG1', str);
	} else if(document.layers) {
		lay = document.layers["PARENT_LINKMSG"].document.layers["LINKMSG1"];
		lay.document.open();
		lay.document.write("<font style='font-size:11pt'>"+str+"</font>");
		lay.document.close(); 
	}
}

function outp(){
	comary = "";
	for(k = 0; k < command.length; k++){
	comary = comary + command[k][0]
	+" "+command[k][1]
	+" "+command[k][2]
	+" "+command[k][3]
	+" "+command[k][4]
	+" "+command[k][5]
	+" "+command[k][6]
	+" ";
	}
	document.myForm.COMARY.value = comary;
}

function ps(x, y) {
	if(document.myForm.xy1.checked){
		document.myForm.POINTX.options[x].selected = true;
		document.myForm.POINTY.options[y].selected = true;
		document.allForm.POINTX.value = x;
		document.allForm.POINTY.value = y;
	}
	if(document.myForm.xy2.checked){
		document.myForm.POINTTX.options[x].selected = true;
		document.myForm.POINTTY.options[y].selected = true;
		document.allForm.POINTTX.value = x;
		document.allForm.POINTTY.value = y;
	}
	if(!(document.myForm.MENUOPEN.checked)) {
		if(document.myForm.MENUOPEN2.checked) {
			moveLAYER("menu2",mx+10,my-50);
		} else {
			moveLAYER("menu",mx+10,my-50);
		}
	}
	return true;
}

function SelectPOINT(){
	if(document.myForm.xy1.checked){
		document.allForm.POINTX.value = document.myForm.POINTX.options[document.myForm.POINTX.selectedIndex].value;
		document.allForm.POINTY.value = document.myForm.POINTY.options[document.myForm.POINTY.selectedIndex].value;
	}
	if(document.myForm.xy2.checked){
		document.allForm.POINTTX.value = document.myForm.POINTTX.options[document.myForm.POINTTX.selectedIndex].value;
		document.allForm.POINTTY.value = document.myForm.POINTTY.options[document.myForm.POINTTY.selectedIndex].value;
	}
	document.allForm.submit();
}

function ns(x) {
	if (x == $HcommandMax){ return true; }
	document.myForm.NUMBER.options[x].selected = true;
	document.allForm.NUMBER.value = x;
	selCommand(x);
	return true;
}
function openCUSTOM(){
	document.customform.submit();
}
function openCAMP(){
	document.campform.submit();
}
function openBBS(){
	document.bbsform.submit();
}
function openCHAT(){
	document.chatform.submit();
}
function set_com(x, y, land) {
	com_str = land + "\\n";
	for(i = 0; i < $HcommandMax; i++){
		c = command[i];
		x2 = c[1];
		y2 = c[2];
		if(x == x2 && y == y2 && c[0] < 50){
			com_str += "[" + (i + 1) +"]" ;
			kind = g[i];
			if(c[0] == $HcomDestroy){
				if(c[3] == 0){
					com_str += kind;
				} else {
					arg = c[3] * 200;
					arg = "��ͽ\��" + arg + "$HunitMoney��";
					com_str += kind + arg;
				}
			}else if(c[0] == $HcomFarm ||
				c[0] == $HcomFactory ||
				c[0] == $HcomMountain) {
				if(c[3] != 0){
					arg = "��" + c[3] + "���";
					com_str += kind + arg;
				}else{
					com_str += kind;
				}
			}else{
				com_str += kind;
			}
			com_str += " ";
		}
	}
	document.myForm.COMSTATUS.value= com_str;
}

function not_com() {
//	document.myForm.COMSTATUS.value="";
}

function jump(theForm, j_mode) {
	var sIndex = theForm.TARGETID.selectedIndex;
	var url = theForm.TARGETID.options[sIndex].value;
	if (url != "" ) window.open("$HthisFile?IslandMap=" +url+"&JAVAMODE="+j_mode, "", "menubar=yes,toolbar=no,location=no,directories=no,status=yes,scrollbars=yes,resizable=yes,width=570,height=600");
}
function jumps(j_mode,str) {
	window.open("$HthisFile?IslandMap=" + str + "&JAVAMODE="+j_mode, "", "menubar=yes,toolbar=no,location=no,directories=no,status=yes,scrollbars=yes,resizable=yes,width=570,height=600");
}
function jumpu(theForm, j_mode) {
	var sIndex = theForm.TARGETID.selectedIndex;
	var url = parseInt(theForm.TARGETID.options[sIndex].value) + 1000;
	if (url != "" ) window.open("$HthisFile?IslandMap=" +url+"&JAVAMODE="+j_mode, "", "menubar=yes,toolbar=no,location=no,directories=no,status=yes,scrollbars=yes,resizable=yes,width=570,height=600");
}
function SelectList(theForm){
	var u, selected_ok;
	if(!theForm){s = ''}
	else { s = theForm.menu.options[theForm.menu.selectedIndex].value; }
	if(s == ''){
		u = 0; selected_ok = 0;
		document.myForm.COMMAND.options.length = $All_listCom;
		for (i=0; i<comlist.length; i++) {
			var command = comlist[i];
			for (a=0; a<command.length; a++) {
				comName = command[a][1] + "(" + command[a][2] + ")";
				document.myForm.COMMAND.options[u].value = command[a][0];
				document.myForm.COMMAND.options[u].text = comName;
				if(command[a][0] == $default_Kind){
					document.myForm.COMMAND.options[u].selected = true;
					selected_ok = 1;
				}
				u++;
			}
		}
		if(selected_ok == 0)
		document.myForm.COMMAND.selectedIndex = 0;
	} else {
		var command = comlist[s];
		document.myForm.COMMAND.options.length = command.length;
		for (i=0; i<command.length; i++) {
			comName = command[i][1] + "(" + command[i][2] + ")";
			document.myForm.COMMAND.options[i].value = command[i][0];
			document.myForm.COMMAND.options[i].text = comName;
			if(command[i][0] == $default_Kind){
				document.myForm.COMMAND.options[i].selected = true;
				selected_ok = 1;
			}
		}
		if(selected_ok == 0)
		document.myForm.COMMAND.selectedIndex = 0;
	}
}

function moveLAYER(layName,x,y){
	if(document.getElementById){		//NN6,IE5
		el = document.getElementById(layName);
		el.style.left = x;
		el.style.top  = y;
	} else if(document.layers){				//NN4
		msgLay.moveTo(x,y);
	} else if(document.all){				//IE4
		msgLay = document.all(layName).style;
		msgLay.pixelLeft = x;
		msgLay.pixelTop = y;
	}
}

function menuclose(){
	moveLAYER("menu",-500,-500);
	moveLAYER("menu2",-500,-500);
}

function Mmove(e){
	if(document.all){
		mx = event.x + document.body.scrollLeft;
		my = event.y + document.body.scrollTop;
	}else if(document.layers){
		mx = e.pageX;
		my = e.pageY;
	}else if(document.getElementById){
		mx = e.pageX;
		my = e.pageY;
	}
	return moveLay.move();
}

function Kdown(e){
	var c, el;
	if(document.all){
		if (event.altKey || event.ctrlKey || event.shiftKey) return;
		c = event.keyCode;
		el = new String(event.srcElement.tagName);
		el = el.toUpperCase();
		if (el == "INPUT") return;
//	}else if(document.layers){// NN4 KEYDOWN���٥�Ȥ�Win98�Ϥ�ʸ����������Τǥ����Ȳ�
//		if (e.modifiers != 0) return;
//		c = e.which;
//		if ((c >= 97) && (c <= 122)) c -= 32; // �Ѿ�ʸ�������ʸ���ˤ���

//		el = new String(e.target);
//		el = el.toUpperCase();
//		if (el.indexOf("<INPUT") >= 0) return;
	}else if(document.getElementById){
		if (e.altKey || e.ctrlKey || e.shiftKey) return;
		c = e.which;
		el = new String(e.target.tagName);
		el = el.toUpperCase();
		if (el == "INPUT") return;
	}
	c = String.fromCharCode(c);
//	window.status = c; //��ǧ��

	// �����줿�����˱����Ʒײ��ֹ�����ꤹ��

	switch (c) {
	case 'Z': c =  2; break; // �Ϥʤ餷
	case 'S': c = 11; break; // ����
	case 'U': c =  3; break; // ���Ω��
	case 'K': c =  5; break; // ����

	case 'N': c = 12; break; // ��������

	case 'P': c = 16; break; // �ץ쥼��ȷ���
	case 'B': c = 21; break; // �ߥ�������Ϸ���
	case 'D': c = 22; break; // �ɱһ��߷���
	case 'M': c = 51; break; // PP�ߥ�����ȯ��
	case 'Y': c = 61; break; // ����ͶƳ��ȯ��
	case 'A': c = 96; break; // Ͷ�׳�ư
	case '-': c = 97; break; //INS ��ⷫ��

	case '.': cominput(myForm,3); return; //DEL ���

	case'\b': //BS ��������

		var no = document.myForm.NUMBER.selectedIndex;
		if(no > 0) document.myForm.NUMBER.selectedIndex = no - 1;
		cominput(myForm,3);
		return;
	case '0':case'`': document.myForm.AMOUNT.selectedIndex = 0; return;
	case '1':case'a': document.myForm.AMOUNT.selectedIndex = 1; return;
	case '2':case'b': document.myForm.AMOUNT.selectedIndex = 2; return;
	case '3':case'c': document.myForm.AMOUNT.selectedIndex = 3; return;
	case '4':case'd': document.myForm.AMOUNT.selectedIndex = 4; return;
	case '5':case'e': document.myForm.AMOUNT.selectedIndex = 5; return;
	case '6':case'f': document.myForm.AMOUNT.selectedIndex = 6; return;
	case '7':case'g': document.myForm.AMOUNT.selectedIndex = 7; return;
	case '8':case'h': document.myForm.AMOUNT.selectedIndex = 8; return;
	case '9':case'i': document.myForm.AMOUNT.selectedIndex = 9; return;
	default:
	// IE �Ǥϥ���ɤΤ���� F5 �ޤǽ����Τǡ������˽����򤤤�ƤϤ����ʤ�
	return;
	}
	StatusMsg(c);
	cominput(document.myForm, 6, c, 0);
}

function StatusMsg(x) {
msg = new Array(64);
END
	my($i ,$k);
	for($i = 0; $i < $HcommandTotal; $i++) {
		$k = $HcomList[$i];
		my($Msg) = $HcomMsg[$k];
		out("msg[$k] = \"$Msg\";\n");
	}
	out(<<END);
	window.status = msg[x];
}

function myisland(theForm,myid) {
	for(i = 0; i < theForm.TARGETID.length ;i++) {
		if(theForm.TARGETID.options[i].value == myid) {
			theForm.TARGETID.selectedIndex = i;
			return;
		}
	}
}
function LayWrite(layName, str) {
	if(document.getElementById){
		document.getElementById(layName).innerHTML = str;
	} else if(document.all){
		document.all(layName).innerHTML = str;
	} else if(document.layers){
		lay = document.layers[layName];
		lay.document.open();
		lay.document.write(str);
		lay.document.close(); 
	}
}

var oldNum=0;
function selCommand(num) {
	document.getElementById('com_'+oldNum).style.backgroundColor = '';
	document.getElementById('com_'+num).style.backgroundColor = '#FFFFAA';
	oldNum = num;
}

// ���ޥ�� �ɥ�å����ɥ�å����ɲå�����ץ�
var moveLay = new MoveFalse();

var newLnum = -2;
var Mcommand = false;

function Mup() {
	moveLay.up();
	moveLay = new MoveFalse();
}

function setBorder(num, color) {
	if(document.getElementById) {
		if(color.length == 4) document.getElementById('com_'+num).style.borderTop = ' 1px solid '+color;
		else document.getElementById('com_'+num).style.border = '0px';
	}
}

function mc_out() {
	if(Mcommand && newLnum >= 0) {
		setBorder(newLnum, '');
		newLnum = -1;
	}
}

function mc_over(num) {
	if(Mcommand) {
		if(newLnum >= 0) setBorder(newLnum, '');
		newLnum = num;
		setBorder(newLnum, '#116');    // blue
	}
}

function comListMove(num) { moveLay = new MoveComList(num); return (document.layers) ? true : false; }

function MoveFalse() {
	this.move = function() { }
	this.up   = function() { }
}

function MoveComList(num) {
	var setLnum  = num;
	Mcommand = true;

	LayWrite('mc_div', '<NOBR><strong>'+(num+1)+': '+g[num]+'</strong></NOBR>');

	this.move = function() {
		moveLAYER('mc_div',mx+10,my-30);
		return false;
	}

	this.up   = function() {
		if(newLnum >= 0) {
			var com = command[setLnum];
			cominput(document.myForm,7,setLnum,0,newLnum);
		}
		else if(newLnum == -1) cominput(document.myForm,3,setLnum+1);

		mc_out();
		newLnum = -2;
		Mcommand = false;
		moveLAYER("mc_div",-50,-50);
	}
}

// ��������̵���ǤΥ��ޥ���������ɲå�����ץ�

function new_http() {
	if(document.getElementById) {
		try{
		   return new ActiveXObject("Msxml2.XMLHTTP");
		} catch (e){
			try {
				return new ActiveXObject("Microsoft.XMLHTTP");
			} catch (E){
				if(typeof XMLHttpRequest != 'undefined') return new XMLHttpRequest;
			}
		}
	}
}

function send_command(form) {
	if (!xmlhttp) return true;

	form.CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}.disabled = true;

	var progress  = document.getElementById('progress');
	progress.innerHTML = '<blink>Sending...</blink>';

	if (xmlhttp.readyState == 1 || xmlhttp.readyState == 2 || xmlhttp.readyState == 3) return; 

	xmlhttp.open("POST", "$HthisFile", true);
	if(!window.opera) xmlhttp.setRequestHeader("referer", "$HthisFile");

	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			var result = xmlhttp.responseText;
			if(result.indexOf('OK') == 0 || result.indexOf('OK') == 2048) {
				str = plchg($HcommandMax);
				str = "<TABLE border=0><TR><TD class='commandjs1'><B>�ݡݡݡ� �����Ѥ� �ݡݡݡ�</B><br><br>"+str+"<br><B>�ݡݡݡ� �����Ѥ� �ݡݡݡ�</B></TD></TR></TABLE>";
				disp(str, 1);
				selCommand(document.myForm.NUMBER.selectedIndex);
			} else {
				alert("�����˼��Ԥ��ޤ�����");
				form.CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}.disabled = false;
			}
			progress.innerHTML = '';
		}
	}

	var post;
	post += 'async=true&';
	post += 'CommandJavaButton$island->{'id'}=true&';
	post += 'COMMAND='+form.COMMAND.value+'&';
	post += 'TARGETID='+form.TARGETID.value+'&';
	post += 'JAVAMODE=java&';
	post += 'COMARY='+form.COMARY.value+'&';
	post += 'PASSWORD='+form.PASSWORD.value+'&';

	xmlhttp.send(post);
	return false;
}
function showElement(layName) {
	var element = document.getElementById(layName).style;
	element.display = "block";
	element.visibility ='visible';
}

function hideElement(layName) {
	var element = document.getElementById(layName).style;
	element.display = "none";
}

function chNum(num) {
	document.ch_numForm.AMOUNT.options.length = 69;
	for(i=0;i<document.ch_numForm.AMOUNT.options.length;i++){
		if(document.ch_numForm.AMOUNT.options[i].value == num){
			document.ch_numForm.AMOUNT.selectedIndex = i;
			document.ch_numForm.AMOUNT.options[i].selected = true;
			moveLAYER('ch_num', mx-10, my-60);
			showElement('ch_num');
			break;
		}
	}
}

function chNumDo() {
	var num = document.ch_numForm.AMOUNT.options[document.ch_numForm.AMOUNT.selectedIndex].value;
	cominput(document.myForm,9,num);
	hideElement('ch_num');
}
//-->
</SCRIPT>
<span id="menu2" style="position:absolute; top:-500;left:-500;">
<table border=0 class="PopupCell"><tr><td nowrap>
$click_com3
<hr>
<a href="Javascript:void(0);" onClick="menuclose()" class='M'>��˥塼���Ĥ���</A>
</td></tr></table></span>
<!-- �����ѹ��ե����� -->
<div id="ch_num" style="position:absolute;visibility:hidden;display:none">
<form name="ch_numForm">
<TABLE BORDER=1 BGCOLOR="#e0ffff" CELLSPACING=1>
<TR><TD VALIGN=TOP NOWRAP>
<A HREF="JavaScript:void(0)" onClick="hideElement('ch_num');" STYlE="text-decoration:none"><B>��</B></A><BR>
<select name="AMOUNT" size=13 onchange="chNumDo()">
</select>
</TD>
</TR>
</TABLE>
</form>
</div>
<!-- ���ޥ�ɥե����� -->
<span ID="mc_div" style="background-color:white;position:absolute;top:-50;left:-50;height:22px;">&nbsp;</span>
<span ID="menu" style="position:absolute; top:-500;left:-500;">
<table border=0 class="PopupCell"><tr><td nowrap>
$click_com
<TD NOWRAP>
$click_com2
<TR>
<TD NOWRAP COLSPAN=2>
<a href="Javascript:void(0);" onClick="menuclose()" class='M'>��˥塼���Ĥ���</A>
</td></tr></table></span>

END

	islandInfo();

	out(<<END);
<CENTER>
<TABLE BORDER>
<TR valign=top>
<TD $HbgInputCell width=25%>
<CENTER>
<FORM name="myForm" action="$HthisFile" method=POST onsubmit="return send_command(this);">
<BR>
<P>
<B>�ײ��ֹ�</B><SELECT NAME=NUMBER onchange="selCommand(this.selectedIndex)">
END
	# �ײ��ֹ�
	my($j);
	for($i = 0; $i < $HcommandMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}

	if ($HmenuOpen eq 'on') {
		$open = "CHECKED";
	}else{
		$open = "";
	}

	out(<<END);
</SELECT><BR>
<HR>
<B>��ȯ�ײ�</B>
<INPUT TYPE="checkbox" NAME="MENUOPEN" $open>��ɽ\��
<INPUT TYPE="checkbox" NAME="MENUOPEN2" $open>�ץ쥼��\��<br>
<SELECT NAME=menu onchange="SelectList(myForm)">
<OPTION VALUE=>������

END
	for($i = 0; $i < $com_count; $i++) {
		($aa) = split(/,/,$HcommandDivido[$i]);
		out("<OPTION VALUE=$i>$aa\n");
	}
	out(<<END);
</SELECT><br>
<SELECT NAME=COMMAND onChange=StatusMsg(this.options[this.selectedIndex].value) onClick=StatusMsg(this.options[this.selectedIndex].value)>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
<option>��������������������</option>
</SELECT>
<HR>
<B>���ޥ������</B><BR><B>
<A HREF=JavaScript:void(0); onClick="cominput(myForm,1)">����</A>
��<A HREF=JavaScript:void(0); onClick="cominput(myForm,2)">���</A>
��<A HREF=JavaScript:void(0); onClick="cominput(myForm,3)">���</A>
</B><HR>
<B>��ɸ��(</B><SELECT NAME=POINTX>
END
	for($i = 0; $i < $mapSize; $i++) {
		if($i == $HdefaultX) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}
	out("</SELECT>, <SELECT NAME=POINTY>");
	for($i = 0; $i < $mapSize; $i++) {
		if($i == $HdefaultY) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}
	out("</SELECT><B>)</B><INPUT TYPE=\"checkbox\" NAME=\"xy1\" CHECKED><br><B>��ɸ��(</B><SELECT NAME=POINTTX>");
	for($i = 0; $i < $mapSize; $i++) {
		if($i == $HdefaultTX) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}
	out("</SELECT>, <SELECT NAME=POINTTY>");
	for($i = 0; $i < $mapSize; $i++) {
		if($i == $HdefaultTY) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}
	out("</SELECT><B>)</B><INPUT TYPE=\"checkbox\" NAME=\"xy2\"><HR><B>����</B><SELECT NAME=AMOUNT>");
	# ����
	for($i = 0; $i < 50; $i++) {
		out("<OPTION VALUE=$i>$i\n");
	}
	for($i = 50; $i < 999; $i += 50) {
		out("<OPTION VALUE=$i>$i\n");
	}
#	my($myislandID) = $island->{'id'};
	my($myislandID) = $defaultTarget;
	out(<<END);
</SELECT>
<HR>
<B>��ɸ��${AfterName}</B>
[<B><A HREF=JavaScript:void(0); onClick="jump(myForm, '$HjavaMode')"> ɽ\�� </A></B>
��<B><A HREF=JavaScript:void(0); onClick="myisland(myForm,'$myislandID')"> ����\�� </A></B>]
<br>[<B><A HREF=JavaScript:void(0); onClick="jumps('$HjavaMode','999')"> ��\�� </A></B>
��<B><A HREF=JavaScript:void(0); onClick="jumps('$HjavaMode','888')"> ��\�� </A></B>
��<B><A HREF=JavaScript:void(0); onClick="jumpu(myForm, '$HjavaMode')"> ��\�� </A></B>]
<BR>

<SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT>
<HR>
<B>���ޥ�ɰ�ư</B>��
<BIG>
<A HREF=JavaScript:void(0); onClick="cominput(myForm,4)" STYlE="text-decoration:none"> �� </A>����
<A HREF=JavaScript:void(0); onClick="cominput(myForm,5)" STYlE="text-decoration:none"> �� </A>
</BIG>
<HR>
<INPUT TYPE="hidden" NAME="COMARY" value="comary">
<INPUT TYPE="hidden" NAME="JAVAMODE" value="$HjavaMode">
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}>
<span id="progress"></span>
<br><font size=2>�Ǹ��<font color=red>�ײ������ܥ���</font>��<br>�����Τ�˺��ʤ��褦�ˡ�</font>
<HR>
<B>�ѥ����</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}">
<HR>
</CENTER>
�������ϴʰ�����(NN4�Բ�)<BR>
����=���̡�BS=��������<BR>
DEL=�����Z=�Ϥʤ餷<BR>
S=���ӡ�U=���Ω��<BR>
K=���N=��������<BR>
B=�ߴ�D=�ɱһ���<BR>
M=�УС�Y=����ͶƳ��<BR>
A=Ͷ�ס�P=�ץ쥼���<BR>

</TD>
<TD $HbgMapCell><center>
<TEXTAREA NAME="COMSTATUS" cols="48" rows="2"></TEXTAREA>
</center>
END
	islandMapJava(1);    # ����Ͽޡ���ͭ�ԥ⡼��
	out(<<END);
</FORM>
</TD>
<TD $HbgCommandCell id="plan" onmouseout="mc_out();return false;">
<FORM name="allForm" action="$HthisFile" method=POST>
<INPUT TYPE="hidden" NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}">
<INPUT TYPE="hidden" NAME=NUMBER VALUE="allno">
<INPUT TYPE="hidden" NAME=POINTY VALUE="allpointy">
<INPUT TYPE="hidden" NAME=POINTX VALUE="allpointx">
<INPUT TYPE="hidden" NAME=POINTTY VALUE="allpointty">
<INPUT TYPE="hidden" NAME=POINTTX VALUE="allpointtx">
<br><INPUT TYPE="hidden" NAME=JAVAMODE value="$HjavaMode">
<DIV ID='AutoCommand'><B>��ư��</B><br>
<SELECT NAME=COMMAND>
END
	#���ޥ��
	my($kind, $cost, $s);
	my($m) = @HcommandDivido;
	my($aa,$dd,$ff) = split(/,/,$HcommandDivido[$m-1]);
	for($i = 0; $i < $HcommandTotal; $i++) {
		$kind = $HcomList[$i];
		$cost = $HcomCost[$kind];
		if(($kind > $ff) && ($kind < 190)) {
			next if($HcomAutoSellTree == $kind);# �����Բ�
			if($cost == 0) {
				$cost = '̵��'
			}
			if($kind == $HdefaultKind) {
				$s = 'SELECTED';
			} else {
				$s = '';
			}
			out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
		}
	}
	out(<<END);
</SELECT><br>
<INPUT TYPE="hidden" NAME="CommandButton$Hislands[$HcurrentNumber]->{'id'}">
<INPUT TYPE="button" onClick="SelectPOINT()" VALUE="��ư�Ϸײ�����"></DIV><HR>
<ilayer name="PARENT_LINKMSG" width="100%" height="100%">
   <layer name="LINKMSG1" width="200"></layer>
   <span id="LINKMSG1"></span>
</ilayer>
<BR>
</FORM>
</TD></TR></TABLE></CENTER>
END
}

#----------------------------------------------------------------------
# ���ޥ�ɥ⡼��
#----------------------------------------------------------------------
sub commandJavaMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# �ѥ����
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}
	# �⡼�ɤ�ʬ��

	my($command) = $island->{'command'};
	my($ckind) = $HcomDoNothing;
	for($i = 0; $i < $HcommandMax; $i++) {
		# ���ޥ����Ͽ
		$HcommandComary =~ s/([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) ([0-9]*) //;
		$ckind = $1;
		$ckind = $HcomDoNothing if($ckind == 0);
		$command->[$i] = {
			'kind' => $ckind,
			'x' => $2,
			'y' => $3,
			'arg' => $4,
			'target' => $5,
			'tx' => $6,
			'ty' => $7
		};
	}

	$island->{'cmdTurn'} = $HislandTurn;		# ������
	$island->{'cmdIp'}   = $ENV{'REMOTE_ADDR'};	# IP
	$island->{'cmdId'}   = $defaultID;			# ���å���ID
	$island->{'cmdtime'} = time;	# ���ϻ���

	# �ǡ����ν񤭽Ф�
	if(!writeIslandsFile($HcurrentID, 2)) {
		unlock();
		tempFailWrite();
		return;
	}
	if($Hasync) {
		unlock();
		out("OK");
	} else {
		tempCommandAdd();
		# owner mode��
		ownerMain();
	}
}

#----------------------------------------------------------------------
# �Ͽޤ�ɽ��
#----------------------------------------------------------------------
sub islandMapJava {
	my($mode) = @_;
	my($island);
	if($mode == 3){
		$island = $Hspace;
	}elsif($mode == 4){
		$island = $Hocean;
		$HislandSize = $HoceanSize;
	}else{
		$island = $Hislands[$HcurrentNumber];
	}

	# �Ϸ����Ϸ��ͤ����
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($nation) = $island->{'nation'};
	my($dis) = $island->{'landValue2'};
	my($l, $lv);
	my($pId) = 0;
	$pId = $island->{'id'} if($mode == 1);
	out(<<END);
<div id='islandMap'><table border>
END
	# ���ޥ�ɼ���
	my($command) = $island->{'command'};
	my($com, @comStr, $i);
	if($HmainMode eq 'owner') {
		for($i = 0; $i < $HcommandMax; $i++) {
			my($j) = $i + 1;
			$com = $command->[$i];
			if($com->{'kind'} < 50) {
				$comStr[$com->{'x'}][$com->{'y'}] .= " [${j}]$HcomName[$com->{'kind'}]";
			}
		}
	}

	# ��ɸ(��)�����
	my $widthsize = $HislandSize * 32 + 16;
	my $cspan = $HislandSize + 1;
	if($mode == 3){
		out("<tr><td colspan=$cspan class=s><img src=$HspaceSizeImage width=$widthsize height=16>");
	}elsif($mode == 4){
		out("<tr><td colspan=$cspan class=b><img src=$HoceanSizeImage width=$widthsize height=16>");
	}else{
		out("<tr><td colspan=$cspan class=b><img src=$HislandSizeImage width=$widthsize height=16>");
	}
	# ̸��ȯ����������á��ϥ�ܥ�õ����̸�ξ�����¸�������
	SearchKiriMons($land, $landValue);
	# ���Ϸ�����Ӳ��Ԥ����
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		out("<table border=0 cellspacing=0 cellpadding=0><tr>");

		# �������ܤʤ��ֹ�����
		if(($y % 2) == 0){
			if($mode == 3){
				out("<td class=s><img src=\"sspace${y}.gif\" width=16 height=32></td>");
			}elsif($mode == 4){
				out("<td class=b><img src=\"space${y}.gif\" width=16 height=32></td>");
			}else{
				out("<td class=b><img src=\"space${y}.gif\" width=16 height=32></td>");
			}
		}

		# ���Ϸ������
		for($x = 0; $x < $HislandSize; $x++) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			if(($Kiri->[$x][$y] == 1) || (($Kiri->[$x][$y] == 2) && ($mode != 1))) {
				landString2($l, $lv, $x, $y, $mode, $comStr[$x][$y], $nation->[$x][$y],1);
			} else {
				landString($l, $lv, $x, $y, $mode, $comStr[$x][$y], $nation->[$x][$y], $dis->[$x][$y], $pId,1);
			}
		}
		# ������ܤʤ��ֹ�����
		if(($y % 2) == 1){
			if($mode == 3){
			#	out("<td class=s><img src=\"cosmo1.gif\" width=16 height=32></td>");
				out("<td class=s><img src=\"sspace${y}.gif\" width=16 height=32></td>");
			}elsif($mode == 4){
				out("<td class=b><img src=\"space${y}.gif\" width=16 height=32></td>");
			}else{
				out("<td class=b><img src=\"space${y}.gif\" width=16 height=32></td>");
			}
		}
		# ���Ԥ����
		out("</tr></table>");
	}
	out("</table></div>\n");
}

#----------------------------------------------------------------------
# �Ѹ��⡼��
#----------------------------------------------------------------------
sub printIslandJava {
	my($mode) = @_;
	# ����

	unlock();

	my($popcmd1,$popcmd2,$msg);
	if($mode == 3){
		# ����

#		spaceMap();
		$HcurrentID = 999;
		$HcurrentName = $SpaceName;
		$sAfterName = $AfterName;
		$AfterName = "";
		$island = $Hspace;
		$popcmd1 = 6;
		$popcmd2 = 6;
		$msg = "���Ϥ���̿�����������ȯ���̤�ͽ��̿��Ⱥ�ɸ��ȿ�Ǥ���ޤ���<br>������ȯ����ϡ�����̿�᤬��ߤˤʤ�ޤ�����";
	}elsif($mode == 4){
		# ����

		$HcurrentID = 888;
		$HcurrentName = $OceanName;
		$sAfterName = $AfterName;
		$AfterName = "";
		$island = $Hocean;
		$popcmd1 = 7;
		$popcmd2 = 7;
		$msg = "���Ϥ���̿�����������ȯ���̤�ͽ��̿��Ⱥ�ɸ��ȿ�Ǥ���ޤ�����";
	}else{
		$HcurrentNumber = $HidToNumber{$HcurrentID};
		$island = $Hislands[$HcurrentNumber];
		# �ʤ��������礬�ʤ����

		if($HcurrentNumber eq '') {
			tempProblem();
			return;
		}
		# ̾���μ���
		$HcurrentName = $island->{'name'};
		if($mode == 10){
			# �ϲ�
			$msg = "���Ϥ���̿�����������ȯ���̤�ͽ��̿��Ⱥ�ɸ��(�ڴ�)��<br>��ɸ��(�ϲ���ɸ)��ȿ�Ǥ���ޤ�����";
		}else{
			$popcmd1 = 2;
			$popcmd2 = 3;
			$msg = "���⤹�������򥯥�å����Ʋ�������<br>����å�������������ȯ���̤κ�ɸ�����ꤵ��ޤ�����";
		}
	}

	#���ޥ�ɥꥹ�ȥ��å�
	my($l_kind,$l_cost,$str);
	$click_com = "";
	$str = "<a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,6,";
	if($mode == 10){
		# �ϲ�
		$l_cost = $HcomCost[$HcomUg];
		if($l_cost == 0) { $l_cost = '̵��'	}
		else { $l_cost .= $HunitMoney; }
		$click_com .= "$HcomName[$HcomUg]($l_cost)<br>\n";
		$click_com .= $str . "$HcomUg,0)' class='M'>�ϲ��ԻԷ���</a><br>\n";
		$click_com .= $str . "$HcomUg,1)' class='M'>�ϲ��������</a><br>\n";
		$click_com .= $str . "$HcomUg,2)' class='M'>�ϲ��������</a><br>\n";
		$click_com .= $str . "$HcomUg,3)' class='M'>�ϲ��ߥ��������</a><br>\n";
		$click_com .= $str . "$HcomUg,4)' class='M'>�ϲ�������������</a>(2400��)<br>\n";
	}elsif($HjavaMode eq 'java'){
		$com_count = @HcommandDivido;
		for($m = 0; $m < $com_count; $m++) {
			($aa,$dd,$ff) = split(/,/,$HcommandDivido[$m]);
			for($i = 0; $i < $HcommandTotal; $i++) {
				$l_kind = $HcomList[$i];
				$l_cost = $HcomCost[$l_kind];
				if($l_cost == 0) { $l_cost = '̵��'	}
				else { $l_cost .= $HunitMoney; }
				if($l_kind > $dd-1 && $l_kind < $ff+1) {
					if(($m == $popcmd1) || ($m == $popcmd2)){
						$click_com .= "<hr>" if($l_kind == $HcomSMissileGM);
						if($l_kind == $HcomSBuild){
						}elsif($l_kind == $HcomSEisei){
							$click_com .= $str . "$l_kind,0)' class='M'>����$HsEisei[0]($l_cost)</a><br>\n";
							$click_com .= $str . "$l_kind,1)' class='M'>����$HsEisei[1]($l_cost)</a><br>\n";
							$click_com .= $str . "$l_kind,2)' class='M'>����$HsEisei[2]($l_cost)</a><br>\n";
							$click_com .= $str . "$l_kind,3)' class='M'>����$HsEisei[3]($l_cost)</a><br>\n";
							$click_com .= $str . "$l_kind,4)' class='M'>����$HsEisei[4]($l_cost)</a><br>\n";
						}else{
							$click_com .= $str . "$l_kind,0)' class='M'>$HcomName[$l_kind]($l_cost)</a><br>\n";
						}
					}else{
						last;
					}
				}
				if($l_kind < $ff+1) { next; }
			}
		}
	}

out(<<END);
<SCRIPT Language="JavaScript">
<!--
if(document.getElementById){
	document.onmousemove = Mmove;
} else if(document.layers){
	window.captureEvents(Event.MOUSEMOVE);
	window.onMouseMove = Mmove;
} else if(document.all){
	document.onmousemove = Mmove;
}
if((document.layers) || (document.all)){  // IE4��IE5��NN4
	window.document.onmouseup = menuclose;
}
END
	if($mode == 10){
		# �ϲ�
out(<<END);
function ps(x, y, xx, yy) {
	var java = '$HjavaMode';
	if(xx != "?" && yy != "?"){
		window.opener.document.myForm.POINTX.options[xx].selected = true;
		window.opener.document.myForm.POINTY.options[yy].selected = true;
	}
	window.opener.document.myForm.POINTTX.options[x].selected = true;
	window.opener.document.myForm.POINTTY.options[y].selected = true;
	if(java == 'java')moveLAYER("menu",mx,my);
	return true;
}
END
	}else{
out(<<END);
function ps(x, y) {
	var java = '$HjavaMode';
	
	if(window.opener.document.myForm.xy1.checked){
		window.opener.document.myForm.POINTX.options[x].selected = true;
		window.opener.document.myForm.POINTY.options[y].selected = true;
	}
	if(window.opener.document.myForm.xy2.checked){
		window.opener.document.myForm.POINTTX.options[x].selected = true;
		window.opener.document.myForm.POINTTY.options[y].selected = true;
	}
	if(java == 'java')moveLAYER("menu",mx,my);
	return true;
}
END
	}
out(<<END);
function moveLAYER(layName,x,y){
	if(document.getElementById){		//NN6,IE5
		if(document.all){				//IE5
			el = document.getElementById(layName);
			el.style.left= event.clientX + document.body.scrollLeft + 10;
			el.style.top= event.clientY + document.body.scrollTop - 30;
			el.style.display = "block";
			el.style.visibility ='visible';
		}else{
			el = document.getElementById(layName);
			el.style.left=x+10;
			el.style.top=y-30;
			el.style.display = "block";
			el.style.visibility ='visible';
		}
	} else if(document.layers){				//NN4
		msgLay = document.layers[layName];
		msgLay.moveTo(x+10,y-30);
		msgLay.visibility = "show";
	} else if(document.all){				//IE4
		msgLay = document.all(layName);
		msgLay.style.pixelLeft = x+10;
		msgLay.style.pixelTop = y-30;
		msgLay.style.display = "block";
		msgLay.style.visibility = "visible";
	}

}

function menuclose(){ 
	if (document.getElementById){
		document.getElementById("menu").style.display = "none";
	} else if (document.layers){
		document.menu.visibility = "hide";
	} else if (document.all){
		window["menu"].style.display = "none";
	}
}

function Mmove(e){
	if(document.all){
		mx = event.x;
		my = event.y;
	}else if(document.layers){
		mx = e.pageX;
		my = e.pageY;
	}else if(document.getElementById){
		mx = e.pageX;
		my = e.pageY;
	}
}
//-->
</SCRIPT>
<DIV ID='targetMap'>
<H1>$HcurrentName$AfterName</H1><p>$msg
<a href="Javascript:void(0);" onclick="window.close()">���̤��Ĥ���</A>
</DIV>
<span id="menu" style="position:absolute; visibility:hidden;">
<table border=0 class="PopupCell"><tr><td nowrap>
$click_com<HR>
<a href="Javascript:void(0);" onClick="menuclose()" class='M'>��˥塼���Ĥ���</A>
</td></tr></table></span>
END
	if($mode == 3){
		# ����

		my($food) = $Hspace->{'food'};
		$food = ($food <= 0) ? "0" : "${food}$HunitFood";
		my($solarwind);
		if($Hspace->{'solarwind'} <= $HislandTurn){
			$solarwind = "<b>ȯ����</b>";
		}else{
			$solarwind = $Hspace->{'solarwind'} . "�����󤫤�";
		}
	out(<<END);
<DIV ID='islandInfo'><TABLE BORDER><TR>
<TD>${HtagTH_}������${H_tagTH}</TD>
<TD>${HislandTurn}������</TD>
<TD>${HtagTH_}������ͽ��${H_tagTH}</TD>
<TD>${solarwind}</TD>
<TD>${HtagTH_}������͸�${H_tagTH}</TD>
<TD>$Hspace->{'pop'}$HunitPop</TD>
<TD>${HtagTH_}�Ŀ���${H_tagTH}</TD>
<TD>${food}</TD>
</TR></TABLE></DIV>
END
	}elsif($mode == 10){
		# �ϲ�
		if(checkPassword($island->{'password'},$HdefaultPassword) && $island->{'id'} eq $defaultID) {
			ugMap($island, 1);
		}else{
			ugMap($island, 0);
		}
		out("</BODY></HTML>");
		return;
	}
	if($island->{'password'} eq encode($HdefaultPassword) && $island->{'id'} eq $defaultID) {
		islandMapJava(1);  # ����Ͽ�
	}else{
		islandMapJava($mode);  # ����Ͽޡ��Ѹ��⡼��
	}
	# �ᶷ
	tempRecent(0);
	out("</BODY></HTML>");
}

1;
