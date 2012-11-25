#----------------------------------------------------------------------
# ＪＡＶＡスクリプト版 -ver1.11-
# 使用条件、使用方法等は、配布元でご確認下さい。
# 付属のjs-readme.txtもお読み下さい。
# あっぽー：http://appoh.execweb.cx/hakoniwa/
#----------------------------------------------------------------------
# 究想の箱庭  (ver5.52c)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Ｊａｖａスクリプト開発画面
#----------------------------------------------------------------------
# ○○島開発計画

sub tempOwnerJava {
	$mapSize = ($HislandSize > $HoceanSize) ? $HislandSize : $HoceanSize;
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];

	# コマンドセット
	$set_com = "";
	$com_max = "";
	for($i = 0; $i < $HcommandMax; $i++) {
		# 各要素の取り出し
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
		# コマンド登録
		if($i == $HcommandMax-1){
			$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\,$s_tx\,$s_ty\]\n";
			$com_max .= "0"
		}else{
			$set_com .= "\[$s_kind\,$s_x\,$s_y\,$s_arg\,$s_target\,$s_tx\,$s_ty\]\,\n";
			$com_max .= "0,"
		}
	}

	# ショートカットキーの説明
	$keyName[$HcomPrepare2]	= "(Z)";
	$keyName[$HcomPlant]	= "(S)";
	$keyName[$HcomReclaim]	= "(U)";
	$keyName[$HcomDestroy]	= "(K)";
	$keyName[$HcomFarm]		= "(N)";
	$keyName[$HcomPresent]	= "(P)";
	$keyName[$HcomBase]		= "(B)";
	$keyName[$HcomDbase]	= "(D)";

	#コマンドリストセット
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
			if($l_cost == 0) { $l_cost = '無料'	}
			elsif($l_cost < 0) { $l_cost = - $l_cost; $l_cost .= $HunitFood; }
			else { $l_cost .= $HunitMoney; }
			if($l_kind > $dd-1 && $l_kind < $ff+1) {
				$set_listcom .= "\[$l_kind\,\'$HcomName[$l_kind]\',\'$l_cost\'\]\,\n";
				if($l_kind == $HcomHaribote || $l_kind == $HcomPolice || $l_kind == $HcomMyhome || $l_kind == $HcomDon || $l_kind == $HcomUg){
					# 除外
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
	$default_Kind = (($HdefaultKind eq '') || ($HdefaultKind eq '　　　　　　　　　　')) ? 1 : $HdefaultKind;

	# リストに追加
	$l_cost = $HcomCost[$HcomShip];
	$l_cost .= $HunitMoney;
	$click_com .= "<a href='javascript:void(0);' onClick='cominput(myForm,6,$HcomShip,0)' class='M' TITLE='$l_cost'>$HcomName[$HcomShip]</a>$keyName[$HcomShip]<br>\n";
	$l_cost = $HcomCost[$HcomEmigration];
	$l_cost = - $l_cost; $l_cost .= $HunitFood;
	$click_com .= "<a href='javascript:void(0);' onClick='cominput(myForm,6,$HcomEmigration,0)' class='M' TITLE='$l_cost'>$HcomName[$HcomEmigration]</a>$keyName[$HcomEmigration]<br>\n";

	# プレゼント
	$click_com3 .= "プレゼント建設(無料)<br>\n";
	$click_com3 .= "プレゼント譲渡(無料)<br><br>\n";
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
		$click_com3 .= "プレゼントはありません。<br><br>\n";
	} else {
		my $tmp = "<a href='javascript:void(0);' class='M' onClick='cominput(myForm,6,";
		if($Park > 0) {
			$click_com3 .= "${tmp}16,0)'>公園建設</a><br>\n";
			$click_com3 .= "${tmp}98,0)'>公園譲渡($Park)</a><br>\n";
		}
		if($Stadium > 0) {
			$click_com3 .= "${tmp}16,1)'>スタジアム建設</a><br>\n";
			$click_com3 .= "${tmp}98,1)'>スタジアム譲渡($Stadium)</a><br>\n";
		}
		if($Dome > 0) {
			$click_com3 .= "${tmp}16,2)'>ドーム建設</a><br>\n";
			$click_com3 .= "${tmp}98,2)'>ドーム譲渡($Dome)</a><br>\n";
		}
		if($Casino > 0) {
			$click_com3 .= "${tmp}16,3)'>カジノ建設</a><br>\n";
			$click_com3 .= "${tmp}98,3)'>カジノ譲渡($Casino)</a><br>\n";
		}
		if($Amusement > 0) {
			$click_com3 .= "${tmp}16,4)'>遊園地建設</a><br>\n";
			$click_com3 .= "${tmp}98,4)'>遊園地譲渡($Amusement)</a><br>\n";
		}
		if($School > 0) {
			$click_com3 .= "${tmp}16,5)'>学校建設</a><br>\n";
			$click_com3 .= "${tmp}98,5)'>学校譲渡($School)</a><br>\n";
		}
		if($Airport > 0) {
			$click_com3 .= "${tmp}16,6)'>空港建設</a><br>\n";
			$click_com3 .= "${tmp}98,6)'>空港譲渡($Airport)</a><br>\n";
		}
		if($Bigcity > 0) {
			$click_com3 .= "${tmp}16,7)'>大都市建設</a><br>\n";
			$click_com3 .= "${tmp}98,7)'>大都市譲渡($Bigcity)</a><br>\n";
		}
		if($Zoo > 0) {
			$click_com3 .= "${tmp}16,8)'>動物園建設</a><br>\n";
			$click_com3 .= "${tmp}98,8)'>動物園譲渡($Zoo)</a><br>\n";
		}
		if($Expo > 0) {
			$click_com3 .= "${tmp}16,9)'>博覧会建設</a><br>\n";
			$click_com3 .= "${tmp}98,9)'>博覧会譲渡($Expo)</a><br>\n";
		}
		if($MonMonu > 0) {
			$click_com3 .= "${tmp}16,10)'>怪獣記念碑建設</a><br>\n";
			$click_com3 .= "${tmp}98,10)'>怪獣記念碑譲渡($MonMonu)</a><br>\n";
		}
		if($Saigai > 0) {
			$click_com3 .= "${tmp}16,11)'>災害の碑建設</a><br>\n";
			$click_com3 .= "${tmp}98,11)'>災害の碑譲渡($Saigai)</a><br>\n";
		}
	}
	
	#島リストセット
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
// ＪＡＶＡスクリプト開発画面配布元
// あっぽー庵箱庭諸島（ http://appoh.execweb.cx/hakoniwa/ ）
// Programmed by Jynichi Sakai(あっぽー)
// ↑ 削除しないで下さい。
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
	str = "<TABLE border=0><TR><TD class='commandjs1'><B>−−−− 送信済み −−−−</B><br><br>"+str+"<br><B>−−−− 送信済み −−−−</B></TD></TR></TABLE>";
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
		g[$HcommandMax-1] = '資金繰り';
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
		// 移動
		var ctmp = command[k];
		var gtmp = g[k];
		if(z > k) {
			// 上から下へ
			for(i = k; i < z-1; i++) {
				command[i] = command[i+1];
				g[i] = g[i+1];
			}
		} else {
			// 下から上へ
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
	str = "<TABLE border=0><TR><TD class='commandjs2'><B>−−−−−未送信−−−−−</B><br><br>"+str+"<br><B>−−−−−未送信−−−−−</B></TD></TR></TABLE>";
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
			tgt = '$HtagName_' + '無人' + '${AfterName}${H_tagName}';
		}else{
			tgt = '$HtagName_' + islname[tgt] + '${AfterName}${H_tagName}';
		}
		if(c[0] == $HcomDoNothing || c[0] == $HcomGiveup || c[0] == $HcomSMissileMGM){ // 資金繰り、島の放棄
			strn2 = kind;
		}else if(c[0] == $HcomMissileNM || // ミサイル関連
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
				arg = '($HtagName_無制限${H_tagName})';
			} else {
				arg = '($HtagName_' + c[3] + '発${H_tagName})';
			}
			strn2 = tgt + point + "へ" + kind + arg;
		}else if(c[0] == $HcomMissileMGM) {
			strn2 = tgt + "へ" + kind;
		}else if(c[0] == $Hcomcolony) {
			if(c[3] == 1 || c[3] == 2){
				strn2 = "スーパーシールドシステム発動！！" + '(' + c[3] + ')';
			}else{
				strn2 = tgt + "へ" + kind;
			}
		}else if(c[0] == $HcomTeisatu || c[0] == $HcomSpy) { // 工作員、偵察
			strn2 = tgt + point + "へ" + kind;
		}else if(c[0] == $HcomSendMonster){ // 怪獣派遣
			if(c[3] == 1){
				strn2 = tgt + '$HtagName_へメカジラ派遣${H_tagName}';
			} else if(c[3] == 2){
				strn2 = tgt + '$HtagName_へグラテネスいのら派遣${H_tagName}';
			} else if(c[3] == 3){
				strn2 = tgt + '$HtagName_へ海底メカいのら派遣${H_tagName}';
			} else {
				strn2 = tgt + '$HtagName_へメカいのら派遣${H_tagName}';
			}
		}else if(c[0] == $HcomSSendMonster) {
			strn2 = tgt + 'へ' + kind + '${HtagName_}（' + c[3] + '）${H_tagName}';
		}else if(c[0] == $HcomSell){ // 食料売却
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * 100;
			arg = '$HtagName_' + arg + '$HunitFood${H_tagName}';
			strn2 = kind + arg;
		}else if(c[0] == $HcomOreSell || c[0] == $HcomOilSell || c[0] == $HcomWeponSell){ // 売却
			if(c[3] == 0){ c[3] = 1; }
			arg = '$HtagName_（' + c[3] + '）${H_tagName}';
			strn2 = tgt + "へ" + kind + arg;
		}else if(c[0] == $HcomOreBuy || c[0] == $HcomOilBuy || c[0] == $HcomWeponBuy){ // 購入
			if(c[3] == 0){ c[3] = 1; }
			arg = '$HtagName_（' + c[3] + '）${H_tagName}';
			strn2 = kind + arg;
		}else if(c[0] == $HcomWarp){ // 転移装置
			if(c[3] == 0) {
				strn2 = point + "で" + kind + "（" + tgt + "行き）";
			} else {
				if(c[3] == 1) {
					direction = "右上";
				} else if(c[3] == 2) {
					direction = "右";
				} else if(c[3] == 3) {
					direction = "右下";
				} else if(c[3] == 4) {
					direction = "左下";
				} else if(c[3] == 5) {
					direction = "左";
				} else {
					c[3] = 6;
					direction= "左上";
				}
				kind = '$HtagComName_' + "転移先装置建設" + '$H_tagComName';
				strn2 = point + "で" + kind + '（${HtagName_}' + direction + '${H_tagName}）';
			}
		}else if(c[0] == $HcomPropaganda){ // 誘致活動
			if(c[3] == 0){
				strn2 = kind;
			} else {
				strn2 = kind + '($HtagName_' + c[3] + '回${H_tagName})';
			}
		}else if(c[0] == $HcomMoney){ // 資金援助

			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * $HcomCost[$HcomMoney];
			arg = '($HtagName_' + arg + '$HunitMoney${H_tagName})';
			strn2 = tgt + "へ" + kind + arg;
		}else if(c[0] == $HcomFood){ // 食料援助

			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * 100;
			arg = '($HtagName_' + arg + '$HunitFood${H_tagName})';
			strn2 = tgt + "へ" + kind + arg;
		}else if(c[0] == $HcomEmigration){ // 移民
			strn2 = point + "の人を" + tgt + "へ" + kind;
		}else if(c[0] == $HcomDestroy){ // 掘削

			if(c[3] == 0){
				strn2 = point + "で" + kind;
			} else {
				arg = c[3] * $HcomCost[$HcomDestroy];
				arg = '(予\算$HtagName_' + arg + '$HunitMoney${H_tagName})';
				strn2 = point + "で" + kind + arg;
			}
		}else if(c[0] == $HcomSearch || c[0] == $HcomBank){ // 地質調査,銀行投資

			arg = c[3] * $HcomCost[$HcomSearch];
			if(arg == 0) {
				arg = $HcomCost[$HcomSearch]
			}
			arg = '(予\算$HtagName_' + arg + '$HunitMoney${H_tagName})';
			strn2 = point + "で" + kind + arg;
		}else if(c[0] == $HcomDummy){ // ダミー
			if(c[3] == 1) {
				strn2 = point + '$HtagName_でダミー採掘場${H_tagName}';
			} else if(c[3] == 2) {
				strn2 = point + '$HtagName_でダミー埋め立て${H_tagName}';
			} else {
				strn2 = point + '$HtagName_でダミー農場${H_tagName}';
			}
		}else if(c[0] == $HcomManipulate || c[0] == $HcomSTManipulate || c[0] == $HcomShipM){
			// 怪獣操作、ST怪獣操作、船操作
			if(c[3] <= 1) {
				c[3] = 1;
				direction = "右上";
			} else if(c[3] == 2) {
				direction = "右";
			} else if(c[3] == 3) {
				direction = "右下";
			} else if(c[3] == 4) {
				direction = "左下";
			} else if(c[3] == 5) {
				direction = "左";
			} else {
				c[3] = 6;
				direction= "左上";
			}
			if(c[0] == $HcomMonsEnsei){
				strn2 = kind + '（${HtagName_}' + direction + '${H_tagName}）';
			}else{
				strn2 = tgt + "へ" + kind + '（${HtagName_}' + direction + '${H_tagName}）';
			}
		}else if(c[0] == $HcomMonument){ // 記念碑
			if(c[3] == 0) {
				strn2 = point + "で" + kind + '($HtagName_モノリス${H_tagName})' + tgt;
			} else if(c[3] == 1) {
				strn2 = point + "で" + kind + '($HtagName_平和記念${H_tagName})' + tgt;
			} else if(c[3] == 2) {
				strn2 = point + "で" + kind + '($HtagName_戦いの碑${H_tagName})' + tgt;
			} else if(c[3] == 3) {
				strn2 = point + "で" + kind + '($HtagName_廉価記念碑${H_tagName})' + tgt;
			} else {
				strn2 = point + "で" + kind;
			}
		}else if(c[0] == $HcomSMonument){ // 海底記念碑
			if(c[3] == 0) {
				strn2 = point + "で" + kind + '($HtagName_海底記念碑${H_tagName})' + tgt;
			} else if(c[3] == 1) {
				strn2 = point + "で" + kind + '($HtagName_海底記念碑(青)${H_tagName})' + tgt;
			} else {
				strn2 = point + "で" + kind;
			}
		}else if(c[0] == $HcomDbase){
			if(c[3] == 1) {
				strn2 = point + "で" + kind + '(${HtagName_}ST${H_tagName})';
			} else if(c[3] == 2) {
				strn2 = point + "で" + kind + '(${HtagName_}霧${H_tagName})';
			} else {
				strn2 = point + "で" + kind;
			}
		}else if(c[0] == $HcomFarm || // 複数回ある計画
			c[0] == $HcomFactory ||
			c[0] == $HcomSFarm ||
			c[0] == $HcomTower ||
			c[0] == $HcomPort ||
			c[0] == $HcomBase ||
			c[0] == $HcomMountain) {
			if(c[3] != 0){
				arg = '($HtagName_' + c[3] + '回${H_tagName})';
				strn2 = point + "で" + kind + arg;
			}else{
				strn2 = point + "で" + kind;
			}
		}else if(c[0] == $HcomPresent || c[0] == $HcomPresentAid){ // プレゼント、プレゼント譲渡
			if(c[3] <= 0) {
				c[3] = 0;
				pres = "公園";
			} else if(c[3] == 1) {
				pres = "スタジアム";
			} else if(c[3] == 2) {
				pres = "ドーム";
			} else if(c[3] == 3) {
				pres = "カジノ";
			} else if(c[3] == 4) {
				pres = "遊園地";
			} else if(c[3] == 5) {
				pres = "学校";
			} else if(c[3] == 6) {
				pres = "空港";
			} else if(c[3] == 7) {
				pres = "大都市";
			} else if(c[3] == 8) {
				pres = "動物園";
			} else if(c[3] == 9) {
				pres= "博覧会";
			} else if(c[3] == 10) {
				pres= "怪獣記念碑";
			} else {
				c[3] = 11;
				pres= "災害の碑";
			}
			if(c[0] == $HcomPresent) {
				strn2 = point + "で" + kind + '（${HtagName_}' + pres + '${H_tagName}）';
			} else {
				strn2 = tgt + "へ" + kind + '（${HtagName_}' + pres + '${H_tagName}）';
			}
		// 怪獣バトル

		} else if(c[0] == $HcomMonsEgg ||
			c[0] == $HcomMonsEsa ||
			c[0] == $HcomMonsTettai ||
			c[0] == $HcomMonsExer ||
			c[0] == $HcomMonsSell) {
			strn2 = kind;
		} else if(c[0] == $HcomMonsEnsei ||
			c[0] == $HcomMonsEsaAid ||
			c[0] == $HcomMonsAid) {
			strn2 = tgt + "へ" + kind;
		// 地下系
		} else if(c[0] == $HcomUg){
			if(c[3] == 0) {
				strn2 = point + "の地下" + point2 + "で"+ kind + '($HtagName_地下都市建設${H_tagName})';
			} else if(c[3] == 1) {
				strn2 = point + "の地下" + point2 + "で"+ kind + '($HtagName_地下農場建設${H_tagName})';
			} else if(c[3] == 2) {
				strn2 = point + "の地下" + point2 + "で"+ kind + '($HtagName_地下工場建設${H_tagName})';
			} else if(c[3] == 3) {
				strn2 = point + "の地下" + point2 + "で"+ kind + '($HtagName_地下ミサイル基地建設${H_tagName})';
			} else if(c[3] == 4) {
				strn2 = point + "の地下" + point2 + "で"+ kind + '($HtagName_地下合成石油工場建設${H_tagName})';
			} else {
				strn2 = point + "の地下" + point2 + "で"+ kind;
			}
		} else if(c[0] == $HcomShip) {
			// 船指令変更
			if(c[3] <= 0) {
				c[3] = 0;
				pres = "特殊";
			} else if(c[3] == 1) {
				pres = "移動";
			} else if(c[3] == 2) {
				pres = "防御";
			} else if(c[3] == 3) {
				pres = "撤退";
			} else if(c[3] >= 4) {
				pres = '攻撃';
				c[3] = 4;
			}
			strn2 = tgt + point + "に" + kind + '（${HtagName_}' + pres + '${H_tagName}）';
		} else if(c[0] == $HcomShipbuild) {
			// 造船
			strn2 = point + "で" + kind + '（${HtagName_}' + c[3] + '${H_tagName}）';
		} else if(c[0] == $HcomSBuild) {
			// 宇宙建設系
			strn2 = "今後拡張予定命令(何もおきません)";
		} else if(c[0] == $HcomSUnit || c[0] == $HcomSpaceFarm || c[0] == $HcomSFactory || c[0] == $HcomSpaceBase) {
			tgt = '$HtagName_' + "$SpaceName" + '${H_tagName}';
			if(c[3] != 0){
				arg = '($HtagName_' + c[3] + '回${H_tagName})';
				strn2 = tgt + point + "で" + kind + arg;
			}else{
				strn2 = tgt + point + "で" + kind;
			}
		} else if(c[0] == $HcomSPioneer || c[0] == $HcomSOccupy || c[0] == $HcomSDestroy || c[0] == $HcomSDbase) {
			tgt = '$HtagName_' + "$SpaceName" + '${H_tagName}';
			strn2 = tgt + point + "で" + kind;
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
			strn2 = tgt + point + "に" + kind + '（${HtagName_}' + pres + '${H_tagName}）';
		} else if(c[0] == $HcomSFood) {
			// 宇宙食料打上げ
			if(c[3] == 0){ c[3] = 1; }
			arg = c[3] * 100;
			arg = '($HtagName_' + arg + '$HunitFood${H_tagName})';
			strn2 = kind + arg;
		} else if(c[0] == $HcomPrepare2 && c[3] == 22) {
			strn2 = '$HtagComName_' + "荒地全て地ならし" + '${H_tagComName}';
		}else{
			strn2 = point + "で" + kind;
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
					arg = "（予\算" + arg + "$HunitMoney）";
					com_str += kind + arg;
				}
			}else if(c[0] == $HcomFarm ||
				c[0] == $HcomFactory ||
				c[0] == $HcomMountain) {
				if(c[3] != 0){
					arg = "（" + c[3] + "回）";
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
//	}else if(document.layers){// NN4 KEYDOWNイベントはWin98系で文字化けするのでコメント化
//		if (e.modifiers != 0) return;
//		c = e.which;
//		if ((c >= 97) && (c <= 122)) c -= 32; // 英小文字を英大文字にする

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
//	window.status = c; //確認用

	// 押されたキーに応じて計画番号を設定する

	switch (c) {
	case 'Z': c =  2; break; // 地ならし
	case 'S': c = 11; break; // 植林
	case 'U': c =  3; break; // 埋め立て
	case 'K': c =  5; break; // 掘削

	case 'N': c = 12; break; // 農場整備

	case 'P': c = 16; break; // プレゼント建設
	case 'B': c = 21; break; // ミサイル基地建設
	case 'D': c = 22; break; // 防衛施設建設
	case 'M': c = 51; break; // PPミサイル発射
	case 'Y': c = 61; break; // 怪獣誘導弾発射
	case 'A': c = 96; break; // 誘致活動
	case '-': c = 97; break; //INS 資金繰り

	case '.': cominput(myForm,3); return; //DEL 削除

	case'\b': //BS 一つ前削除

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
	// IE ではリロードのための F5 まで拾うので、ここに処理をいれてはいけない
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

// コマンド ドラッグ＆ドロップ用追加スクリプト
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

// 画面遷移無しでのコマンド送信用追加スクリプト

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
				str = "<TABLE border=0><TR><TD class='commandjs1'><B>−−−− 送信済み −−−−</B><br><br>"+str+"<br><B>−−−− 送信済み −−−−</B></TD></TR></TABLE>";
				disp(str, 1);
				selCommand(document.myForm.NUMBER.selectedIndex);
			} else {
				alert("送信に失敗しました。");
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
<a href="Javascript:void(0);" onClick="menuclose()" class='M'>メニューを閉じる</A>
</td></tr></table></span>
<!-- 数量変更フォーム -->
<div id="ch_num" style="position:absolute;visibility:hidden;display:none">
<form name="ch_numForm">
<TABLE BORDER=1 BGCOLOR="#e0ffff" CELLSPACING=1>
<TR><TD VALIGN=TOP NOWRAP>
<A HREF="JavaScript:void(0)" onClick="hideElement('ch_num');" STYlE="text-decoration:none"><B>×</B></A><BR>
<select name="AMOUNT" size=13 onchange="chNumDo()">
</select>
</TD>
</TR>
</TABLE>
</form>
</div>
<!-- コマンドフォーム -->
<span ID="mc_div" style="background-color:white;position:absolute;top:-50;left:-50;height:22px;">&nbsp;</span>
<span ID="menu" style="position:absolute; top:-500;left:-500;">
<table border=0 class="PopupCell"><tr><td nowrap>
$click_com
<TD NOWRAP>
$click_com2
<TR>
<TD NOWRAP COLSPAN=2>
<a href="Javascript:void(0);" onClick="menuclose()" class='M'>メニューを閉じる</A>
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
<B>計画番号</B><SELECT NAME=NUMBER onchange="selCommand(this.selectedIndex)">
END
	# 計画番号
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
<B>開発計画</B>
<INPUT TYPE="checkbox" NAME="MENUOPEN" $open>非表\示
<INPUT TYPE="checkbox" NAME="MENUOPEN2" $open>プレゼン\ト<br>
<SELECT NAME=menu onchange="SelectList(myForm)">
<OPTION VALUE=>全種類

END
	for($i = 0; $i < $com_count; $i++) {
		($aa) = split(/,/,$HcommandDivido[$i]);
		out("<OPTION VALUE=$i>$aa\n");
	}
	out(<<END);
</SELECT><br>
<SELECT NAME=COMMAND onChange=StatusMsg(this.options[this.selectedIndex].value) onClick=StatusMsg(this.options[this.selectedIndex].value)>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
<option>　　　　　　　　　　</option>
</SELECT>
<HR>
<B>コマンド入力</B><BR><B>
<A HREF=JavaScript:void(0); onClick="cominput(myForm,1)">挿入</A>
　<A HREF=JavaScript:void(0); onClick="cominput(myForm,2)">上書き</A>
　<A HREF=JavaScript:void(0); onClick="cominput(myForm,3)">削除</A>
</B><HR>
<B>座標１(</B><SELECT NAME=POINTX>
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
	out("</SELECT><B>)</B><INPUT TYPE=\"checkbox\" NAME=\"xy1\" CHECKED><br><B>座標２(</B><SELECT NAME=POINTTX>");
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
	out("</SELECT><B>)</B><INPUT TYPE=\"checkbox\" NAME=\"xy2\"><HR><B>数量</B><SELECT NAME=AMOUNT>");
	# 数量
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
<B>目標の${AfterName}</B>
[<B><A HREF=JavaScript:void(0); onClick="jump(myForm, '$HjavaMode')"> 表\示 </A></B>
／<B><A HREF=JavaScript:void(0); onClick="myisland(myForm,'$myislandID')"> 前選\択 </A></B>]
<br>[<B><A HREF=JavaScript:void(0); onClick="jumps('$HjavaMode','999')"> 宇\宙 </A></B>
／<B><A HREF=JavaScript:void(0); onClick="jumps('$HjavaMode','888')"> 海\域 </A></B>
／<B><A HREF=JavaScript:void(0); onClick="jumpu(myForm, '$HjavaMode')"> 地\下 </A></B>]
<BR>

<SELECT NAME=TARGETID>
$HtargetList<BR>
</SELECT>
<HR>
<B>コマンド移動</B>：
<BIG>
<A HREF=JavaScript:void(0); onClick="cominput(myForm,4)" STYlE="text-decoration:none"> ▲ </A>・・
<A HREF=JavaScript:void(0); onClick="cominput(myForm,5)" STYlE="text-decoration:none"> ▼ </A>
</BIG>
<HR>
<INPUT TYPE="hidden" NAME="COMARY" value="comary">
<INPUT TYPE="hidden" NAME="JAVAMODE" value="$HjavaMode">
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandJavaButton$Hislands[$HcurrentNumber]->{'id'}>
<span id="progress"></span>
<br><font size=2>最後に<font color=red>計画送信ボタン</font>を<br>押すのを忘れないように。</font>
<HR>
<B>パスワード</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}">
<HR>
</CENTER>
キー入力簡易説明(NN4不可)<BR>
数字=数量　BS=一つ前削除<BR>
DEL=削除　Z=地ならし<BR>
S=植林　U=埋め立て<BR>
K=掘削　N=農場整備<BR>
B=ミ基　D=防衛施設<BR>
M=ＰＰ　Y=怪獣誘導弾<BR>
A=誘致　P=プレゼント<BR>

</TD>
<TD $HbgMapCell><center>
<TEXTAREA NAME="COMSTATUS" cols="48" rows="2"></TEXTAREA>
</center>
END
	islandMapJava(1);    # 島の地図、所有者モード
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
<DIV ID='AutoCommand'><B>自動系</B><br>
<SELECT NAME=COMMAND>
END
	#コマンド
	my($kind, $cost, $s);
	my($m) = @HcommandDivido;
	my($aa,$dd,$ff) = split(/,/,$HcommandDivido[$m-1]);
	for($i = 0; $i < $HcommandTotal; $i++) {
		$kind = $HcomList[$i];
		$cost = $HcomCost[$kind];
		if(($kind > $ff) && ($kind < 190)) {
			next if($HcomAutoSellTree == $kind);# 使用不可
			if($cost == 0) {
				$cost = '無料'
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
<INPUT TYPE="button" onClick="SelectPOINT()" VALUE="自動系計画送信"></DIV><HR>
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
# コマンドモード
#----------------------------------------------------------------------
sub commandJavaMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# パスワード
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}
	# モードで分岐

	my($command) = $island->{'command'};
	my($ckind) = $HcomDoNothing;
	for($i = 0; $i < $HcommandMax; $i++) {
		# コマンド登録
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

	$island->{'cmdTurn'} = $HislandTurn;		# ターン
	$island->{'cmdIp'}   = $ENV{'REMOTE_ADDR'};	# IP
	$island->{'cmdId'}   = $defaultID;			# クッキーID
	$island->{'cmdtime'} = time;	# 入力時間

	# データの書き出し
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
		# owner modeへ
		ownerMain();
	}
}

#----------------------------------------------------------------------
# 地図の表示
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

	# 地形、地形値を取得
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
	# コマンド取得
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

	# 座標(上)を出力
	my $widthsize = $HislandSize * 32 + 16;
	my $cspan = $HislandSize + 1;
	if($mode == 3){
		out("<tr><td colspan=$cspan class=s><img src=$HspaceSizeImage width=$widthsize height=16>");
	}elsif($mode == 4){
		out("<tr><td colspan=$cspan class=b><img src=$HoceanSizeImage width=$widthsize height=16>");
	}else{
		out("<tr><td colspan=$cspan class=b><img src=$HislandSizeImage width=$widthsize height=16>");
	}
	# 霧を発生させる怪獣、ハリボテ探して霧の場所を保存する処理
	SearchKiriMons($land, $landValue);
	# 各地形および改行を出力
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		out("<table border=0 cellspacing=0 cellpadding=0><tr>");

		# 偶数行目なら番号を出力
		if(($y % 2) == 0){
			if($mode == 3){
				out("<td class=s><img src=\"sspace${y}.gif\" width=16 height=32></td>");
			}elsif($mode == 4){
				out("<td class=b><img src=\"space${y}.gif\" width=16 height=32></td>");
			}else{
				out("<td class=b><img src=\"space${y}.gif\" width=16 height=32></td>");
			}
		}

		# 各地形を出力
		for($x = 0; $x < $HislandSize; $x++) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			if(($Kiri->[$x][$y] == 1) || (($Kiri->[$x][$y] == 2) && ($mode != 1))) {
				landString2($l, $lv, $x, $y, $mode, $comStr[$x][$y], $nation->[$x][$y],1);
			} else {
				landString($l, $lv, $x, $y, $mode, $comStr[$x][$y], $nation->[$x][$y], $dis->[$x][$y], $pId,1);
			}
		}
		# 奇数行目なら番号を出力
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
		# 改行を出力
		out("</tr></table>");
	}
	out("</table></div>\n");
}

#----------------------------------------------------------------------
# 観光モード
#----------------------------------------------------------------------
sub printIslandJava {
	my($mode) = @_;
	# 開放

	unlock();

	my($popcmd1,$popcmd2,$msg);
	if($mode == 3){
		# 宇宙

#		spaceMap();
		$HcurrentID = 999;
		$HcurrentName = $SpaceName;
		$sAfterName = $AfterName;
		$AfterName = "";
		$island = $Hspace;
		$popcmd1 = 6;
		$popcmd2 = 6;
		$msg = "入力した命令と地点が開発画面の予定命令と座標に反映されます。<br>太陽風発生中は、全て命令が中止になります。　";
	}elsif($mode == 4){
		# 海域

		$HcurrentID = 888;
		$HcurrentName = $OceanName;
		$sAfterName = $AfterName;
		$AfterName = "";
		$island = $Hocean;
		$popcmd1 = 7;
		$popcmd2 = 7;
		$msg = "入力した命令と地点が開発画面の予定命令と座標に反映されます。　";
	}else{
		$HcurrentNumber = $HidToNumber{$HcurrentID};
		$island = $Hislands[$HcurrentNumber];
		# なぜかその島がない場合

		if($HcurrentNumber eq '') {
			tempProblem();
			return;
		}
		# 名前の取得
		$HcurrentName = $island->{'name'};
		if($mode == 10){
			# 地下
			$msg = "入力した命令と地点が開発画面の予定命令と座標１(土管)、<br>座標２(地下座標)に反映されます。　";
		}else{
			$popcmd1 = 2;
			$popcmd2 = 3;
			$msg = "攻撃する地点をクリックして下さい。<br>クリックした地点が開発画面の座標に設定されます。　";
		}
	}

	#コマンドリストセット
	my($l_kind,$l_cost,$str);
	$click_com = "";
	$str = "<a href='javascript:void(0);' onClick='window.opener.cominput(window.opener.document.myForm,6,";
	if($mode == 10){
		# 地下
		$l_cost = $HcomCost[$HcomUg];
		if($l_cost == 0) { $l_cost = '無料'	}
		else { $l_cost .= $HunitMoney; }
		$click_com .= "$HcomName[$HcomUg]($l_cost)<br>\n";
		$click_com .= $str . "$HcomUg,0)' class='M'>地下都市建設</a><br>\n";
		$click_com .= $str . "$HcomUg,1)' class='M'>地下農場建設</a><br>\n";
		$click_com .= $str . "$HcomUg,2)' class='M'>地下工場建設</a><br>\n";
		$click_com .= $str . "$HcomUg,3)' class='M'>地下ミサイル基地</a><br>\n";
		$click_com .= $str . "$HcomUg,4)' class='M'>地下合成石油工場</a>(2400億)<br>\n";
	}elsif($HjavaMode eq 'java'){
		$com_count = @HcommandDivido;
		for($m = 0; $m < $com_count; $m++) {
			($aa,$dd,$ff) = split(/,/,$HcommandDivido[$m]);
			for($i = 0; $i < $HcommandTotal; $i++) {
				$l_kind = $HcomList[$i];
				$l_cost = $HcomCost[$l_kind];
				if($l_cost == 0) { $l_cost = '無料'	}
				else { $l_cost .= $HunitMoney; }
				if($l_kind > $dd-1 && $l_kind < $ff+1) {
					if(($m == $popcmd1) || ($m == $popcmd2)){
						$click_com .= "<hr>" if($l_kind == $HcomSMissileGM);
						if($l_kind == $HcomSBuild){
						}elsif($l_kind == $HcomSEisei){
							$click_com .= $str . "$l_kind,0)' class='M'>宇宙$HsEisei[0]($l_cost)</a><br>\n";
							$click_com .= $str . "$l_kind,1)' class='M'>宇宙$HsEisei[1]($l_cost)</a><br>\n";
							$click_com .= $str . "$l_kind,2)' class='M'>宇宙$HsEisei[2]($l_cost)</a><br>\n";
							$click_com .= $str . "$l_kind,3)' class='M'>宇宙$HsEisei[3]($l_cost)</a><br>\n";
							$click_com .= $str . "$l_kind,4)' class='M'>宇宙$HsEisei[4]($l_cost)</a><br>\n";
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
if((document.layers) || (document.all)){  // IE4、IE5、NN4
	window.document.onmouseup = menuclose;
}
END
	if($mode == 10){
		# 地下
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
<a href="Javascript:void(0);" onclick="window.close()">画面を閉じる</A>
</DIV>
<span id="menu" style="position:absolute; visibility:hidden;">
<table border=0 class="PopupCell"><tr><td nowrap>
$click_com<HR>
<a href="Javascript:void(0);" onClick="menuclose()" class='M'>メニューを閉じる</A>
</td></tr></table></span>
END
	if($mode == 3){
		# 宇宙

		my($food) = $Hspace->{'food'};
		$food = ($food <= 0) ? "0" : "${food}$HunitFood";
		my($solarwind);
		if($Hspace->{'solarwind'} <= $HislandTurn){
			$solarwind = "<b>発生中</b>";
		}else{
			$solarwind = $Hspace->{'solarwind'} . "ターンから";
		}
	out(<<END);
<DIV ID='islandInfo'><TABLE BORDER><TR>
<TD>${HtagTH_}宇宙歴${H_tagTH}</TD>
<TD>${HislandTurn}ターン</TD>
<TD>${HtagTH_}太陽風予報${H_tagTH}</TD>
<TD>${solarwind}</TD>
<TD>${HtagTH_}宇宙総人口${H_tagTH}</TD>
<TD>$Hspace->{'pop'}$HunitPop</TD>
<TD>${HtagTH_}残食料${H_tagTH}</TD>
<TD>${food}</TD>
</TR></TABLE></DIV>
END
	}elsif($mode == 10){
		# 地下
		if(checkPassword($island->{'password'},$HdefaultPassword) && $island->{'id'} eq $defaultID) {
			ugMap($island, 1);
		}else{
			ugMap($island, 0);
		}
		out("</BODY></HTML>");
		return;
	}
	if($island->{'password'} eq encode($HdefaultPassword) && $island->{'id'} eq $defaultID) {
		islandMapJava(1);  # 島の地図
	}else{
		islandMapJava($mode);  # 島の地図、観光モード
	}
	# 近況
	tempRecent(0);
	out("</BODY></HTML>");
}

1;
