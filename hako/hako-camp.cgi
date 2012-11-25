#----------------------------------------------------------------------
# Ȣ����� ver2.20
# �رĲ��̥⥸�塼��
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# �����ζ�˴�� ver1.0.0 by ������ http://www.bekkoame.ne.jp/~tokuoka/ozzy.html
# ���Ѿ���Ȣ�����˽ऺ�롥�ܤ�������°��readme.txt�ե�����򻲾�
#----------------------------------------------------------------------
# ���ۤ�Ȣ��  (ver5.16)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �رĲ���
#----------------------------------------------------------------------
# �ᥤ��
sub campMain {
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	$HcurrentCamp = $Hislands[$HcurrentNumber];
	# ����
	unlock ();

	# �ѥ����
	if(!checkPassword($HcurrentCamp->{'password'},$HinputPassword)) {
		# password�ְ㤤
		tempWrongPassword();
		return;
	}
	$HcurrentCampID = $HcurrentCamp->{'ally'};

	tempPrintCampHead (); # ��������
	campAllIslandsInfo(); # �رĤ�°�������ξ���
}

#----------------------------------------------------------------------
# �ƥ�ץ졼�Ȥ���¾
#----------------------------------------------------------------------

# �����ر� ��������
sub tempPrintCampHead {
	out(<<END);
<DIV align='center'>
${HtagBig_}�رİ���ɽ��${H_tagBig}<BR>
$HtempBack<BR><BR>
</DIV>
�����ۤȤ�ɤ������ϡ���ɸ��¾����Ǥ��äƤ⼫����Ф��Ƽ¹Ԥ���ޤ���<BR>
END
}

# �����ɽ��
sub campAllIslandsInfo {
	# �رĤ�°������Υ��ޥ�ɤΤ��ɤ߽Ф�
	my($i);
	for($i = 0; $i < $HislandNumber; $i++) {
		($Hislands[$i]->{'command'}, $Hislands[$i]->{'land'}, $Hislands[$i]->{'landValue'}) = readCommands($Hislands[$i]->{'id'});
	}

	# ����ξ���񤭽Ф�
	for($i = 0; $i < $HislandNumber; $i++) {
		next if(($Hislands[$i]->{'ally'} eq '') || ($Hislands[$i]->{'ally'} < 1));
		if ($HcurrentCampID == $Hislands[$i]->{'ally'}) {
			next if($Hislands[$i]->{'id'} > 90);
			campIslandInfo($Hislands[$i], $i+1);
		}
	}

}

# ��Υ��ޥ���ɤ߹���(�رĲ��̺�����)
sub readCommands {
	my($id) = @_;
	my(@command, @land, @landValue, $i);
	if(!open(IIN, "${HdirName}/island.$id")) {
		rename("${HdirName}/islandtmp.$id", "${HdirName}/island.$id");
		exit(0) if(!open(IIN, "${HdirName}/island.$id"));
	}
	my($line, $x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		$line = <IIN>;
		for($x = 0; $x < $HislandSize; $x++) {
			$line =~ s/^(..)(....)(..)(....)(..)//;
			$land[$x][$y] = hex($1);
			$landValue[$x][$y] = hex($2);
		}
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
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)$/;
		$command[$i] = {
		'kind' => int($1),
		'target' => int($2),
		'x' => int($3),
		'y' => int($4),
		'arg' => int($5),
		'tx' => int($6),
		'ty' => int($7)
		}
	}
	close(IIN);

	# ���ޥ�ɤΤ��֤�
	return \@command, \@land, \@landValue,
}

sub campIslandInfo {
	my($island, $rank) = @_;

	# ����ɽ��
	my($id) = $island->{'id'};
	my($name);
	my($MissileK) = $island->{'MissileK'};
	my($ore) = $island->{'ore'};
	my($oil) = $island->{'oil'};
	my($weapon) = $island->{'weapon'};
	my($money) = "$island->{'money'}$HunitMoney";
	my($food) = "$island->{'food'}$HunitFood";
	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}${AfterName}${H_tagName}";
	} else {
		$name = "${HtagName2_}$island->{'name'}${AfterName}($island->{'absent'})${H_tagName2}";
	}

#	my($totalDefence, $totalBase, $totalOil, $totalSBase, $totalHaribote, $totalLevel) = (0, 0, 0, 0, 0, 0);
#	my($land) = $island->{'land'};
#    my($landValue) = $island->{'landValue'};
#	my($x, $y, $i);
#	for($y = 0; $y < $HislandSize; $y++) {
#		for($x = 0; $x < $HislandSize; $x++) {
#			$l = $land->[$x][$y];
#			$lv = $landValue->[$x][$y];
#			if($l == $HlandDefence) {
#				$totalDefence++;
#			}elsif($l == $HlandHaribote) {
#				$totalHaribote++;
#			}elsif($l == $HlandOil) {
#				$totalOil++;
#			}
#		}
#	}
#���ϥ�ܥơ�$totalHaribote��<BR>
#���ɱһ��ߡ�$totalDefence��<BR>
#���������ġ�$totalOil��<BR>

	out(<<END);
<table><tr><th $HbgTitleCell>�ǡ���</th><th $HbgTitleCell>NO</th><th $HbgTitleCell>̿��</th><th $HbgTitleCell>��ɸ</th><th $HbgTitleCell>��ɸ��</th><th $HbgTitleCell>����</th><th $HbgTitleCell>��ɸ��</th>
<tr><td rowspan=30>
<A HREF=\"$HthisFile?Sight=${id}\" class=\"M\" TARGET=_blank>$name</A><br>
$island->{'ownername'}<br><br>
��⡧$island->{'money'}$HunitMoney<br>
������$island->{'food'}$HunitFood<br>
���С�$island->{'ore'}$HunitOre<br>
������$island->{'oil'}$HunitOil<br>
ʼ�$island->{'weapon'}$HunitWeapon<br>
�ߥ�����ȯ�Ϳ���$island->{'MissileK'}<br>
</td>
END
	for($i = 0; $i < 15; $i++) {
		campCommand($i, $island->{'command'}->[$i]);
	}
	out("</table>");
}

# ���ϺѤߥ��ޥ��ɽ��
sub campCommand {
	my($number, $command) = @_;
	my($kind, $target, $x, $y, $arg, $tx, $ty) =
	(
		$command->{'kind'},
		$command->{'target'},
		$command->{'x'},
		$command->{'y'},
		$command->{'arg'},
		$command->{'tx'},
		$command->{'ty'}
	);
	my($name) = "$HtagComName_${HcomName[$kind]}$H_tagComName";
	my($point) = "$HtagName_($x,$y)$H_tagName";
	my($point2) = "$HtagName_($tx,$ty)$H_tagName";
	my($id) = $target;
	$target = $HidToName{$target};
	if($target eq ''){
		$target = "-------";
	}else{
		$target = "<A HREF=\"$HthisFile?Sight=${id}\" class=\"M\" TARGET=_blank>$HtagName_${target}${AfterName}$H_tagName</a>";
	}
	my($value) = $arg * $HcomCost[$kind];
	$value = $HcomCost[$kind] if($value == 0);
	if($value < 0) {
		$value = -$value;
		$value = "$value$HunitFood";
	} else {
		$value = "$value$HunitMoney";
	}
	$value = "$HtagName_$value$H_tagName";
	my($j) = sprintf("%02d", $number + 1);
	out("<tr>") if($number > 0);
	out("<td>$HtagNumber_$j$H_tagNumber</td>");
	out("<td>${name}</td><td>${target}</td><td>${point}</td><td>${arg}</td><td>${point2}</td>");
	out("</tr>");
}

1;
