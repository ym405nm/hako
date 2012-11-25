#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ���������⥸�塼��
# ���Ѿ�������ˡ���ϡ�qhako-readme.txt�ե�����򻲾�
#----------------------------------------------------------------------
# ���ۤ�Ȣ��(ver5.53d)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# ��ο��������⡼��
#----------------------------------------------------------------------
sub newIslandMain {
	my($mode) = @_;

	# �礬���äѤ��Ǥʤ��������å�(BattleField�����ϥ����å����ʤ�)
	if(($HislandNumber >= $HmaxIsland + $HbattleNumber) && (!$mode)) {
		unlock();
		tempHeader();
		tempNewIslandFull();
		return;
	}

	# ̾�������뤫�����å�
	if($HcurrentName eq '') {
		unlock();
		tempHeader();
		tempNewIslandNoName();
		return;
	}

	# ̾���������������å�
	if(($HcurrentName =~ /[\\,\?\(\)\<\>\$]|^̵��$/) || ($HcurrentName =~ /[\\,\?\(\)\<\>\$]|^ƿ̾$/)) {
		# �Ȥ��ʤ�̾��
		unlock();
		tempHeader();
		tempNewIslandBadName();
		return;
	}

	# ̾���ν�ʣ�����å�
	if(nameToNumber($HcurrentName) != -1) {
		# ���Ǥ�ȯ������
		unlock();
		tempHeader();
		tempNewIslandAlready();
		return;
	}
	
	# password��¸��Ƚ��
	if($HinputPassword eq '') {
		# password̵��
		unlock();
		tempHeader();
		tempNewIslandNoPassword();
		return;
	}

	# ��ǧ�ѥѥ����
	if($HinputPassword2 ne $HinputPassword) {
		# password�ְ㤤
		unlock();
		tempHeader();
		tempWrongPassword();
		return;
	}

	# ����������ֹ�����
	$HcurrentNumber = $HislandNumber;
	$HislandNumber++;
	$Hislands[$HcurrentNumber] = makeNewIsland($mode);
	my($island) = $Hislands[$HcurrentNumber];

	# ��ΣɣĤκ�����
	my($i,@logid);
	# ����ID�򥵡���
	for($i = 0; $i < $HlogMax; $i++) {
		open(SIN, "${HlogdirName}/hakojima.log${i}");
		my($line, $lid);
		while($line = <SIN>) {
			$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
			$logid[$3] = 1;
		}
		close(SIN);
	}
	my $nextid = 999;
	
	my($si, $ei);
	if($mode){
		# BattleField�ΤȤ�
		$si = 91;
		$ei = 100;
	}else{
		$si = 1;
		$ei = 91;
	}

	for($i = $si;$i < $ei;$i++) {
		if(($HidToNumber{$i} eq '') && (!$logid[$i])) {
			unlink("$HprofileDir/profile${i}.dat"); # �ץ�ե�����ǡ������
			$nextid = $i;
			last;
		}
	}
	# ID�������å�
	if($nextid >= $ei) {
		# ���ͤˤ�꿷�������Բ�
		unlock();
		tempHeader();
		if($mode){
			tempNewIslandIdB();
		}else{
			tempNewIslandId();
		}
		return;
	}
	
	# �������¤���⡼�ɤ��ä��鶯�����
	preDeleteMainP(0);

	# �Ƽ���ͤ�����
	if($mode){
		# BattleField�ΤȤ�
		$island->{'absent'} = 0;
		$island->{'comment'} = '(Battle Field)';
		$island->{'evil'} = 200;
	}else{
		#�����Ͽ���Ρֻ񻺷���ײ��
		$island->{'absent'} = $HgiveupTurn - 3;
		$island->{'comment'} = '(̤��Ͽ)';
		if($Htournament){
			# �ʰץȡ��ʥ���
			$island->{'evil'} = 200;
		}else{
			$island->{'evil'} = 1;
		}
	}
	$island->{'name'} = $HcurrentName;
	$island->{'id'} = $nextid;
	$HislandNextID ++;
	$island->{'password'} = encode($HinputPassword);
	$island->{'weather'} = 14;
	$island->{'turnsu'} = 0;
	$island->{'zyuni'} = 0;
	$island->{'MissileK'} = 0;
	$island->{'MissileA'} = 0;
	$island->{'allex'}  = 0;
	$island->{'status'} = 0;
	$island->{'kaisi'} = $HislandTurn;
	$island->{'ownername'} = htmlEscape($HcurrentOwnerName);
	$island->{'ore'} = 30;
	$island->{'weapon'} = 10;
	$island->{'oil'} = 30;
	
	if($Htournament == 2){
							# $id,$name,$tId,$sId,$mId,$hp,$mhp,$str,$def,$agi,$skl,$winh,$win,$lose
		my(@tmonster) = ($nextid,$HcurrentName,0,1,$HtournamentmonsId,24,24,8,0,0,4,0,0,0);
		$island->{'monster'} = \@tmonster;
	}

	# ̵�����õ���ư��֤���ꤹ�롣
	makeRandomOceanPointArray();
	my($i, $x, $y);
#	for($y = 0; $y < $HoceanSize; $y++) {
#		for($x = 0; $x < $HoceanSize; $x++) {
#			push(@Uninhabited, $y * $HoceanSize + $x) if ($Hocean->{'land'}->[$x][$y] == $HlandOcean);
#		}
#	}
#	my $xy = $Uninhabited[random($#Uninhabited + 1)];
#	$x = $xy % $HoceanSize;
#	$y = int($xy / $HoceanSize);
#	if($Hocean->{'land'}->[$x][$y] != $HlandOcean){
		
	for($i = 0; $i < $HpointOcean; $i++){
		$x = $HrpxO[$i];
		$y = $HrpyO[$i];
		last if($Hocean->{'land'}->[$x][$y] == $HlandOcean);
	}
	if($i >= $HpointOcean){
		for($i = 0; $i < $HpointOcean; $i++){
			$x = $HrpxO[$i];
			$y = $HrpyO[$i];
#			last if($Hocean->{'land'}->[$x][$y] == $HlandSea);
			last if(seaAround($Hocean->{'land'}, $x, $y, 7) == 7);
		}
		if($i >= $HpointOcean){
			unlock();
			tempHeader();
			tempNotNewIsland();
			return;
		}
	}
	$Hocean->{'land'}->[$x][$y] = $HlandOPlayer;
	$Hocean->{'nation'}->[$x][$y] = $nextid;
	$island->{'x'} = $x;
	$island->{'y'} = $y;

	# �͸�����¾����
	estimateM($HcurrentNumber);

	# �ǡ����񤭽Ф�
	if(!writeIslandsFile($island->{'id'}, 0)) {
		unlock();
		tempHeader();
		tempFailWrite();
		return;
	}

	logDiscover($HcurrentName); # ��

	if(!$mode){
		# BattleField�ʳ�
		$HcurrentID = $nextid;
		$HmainMode = 'owner';
		# COOKIE����
		cookieOutput();
	}
	# ����
	unlock();

	# ȯ������
	tempHeader();
	tempNewIslandHead($island->{'id'}); # ȯ�����ޤ���!!
	tempNavi();
	islandInfo(); # ��ξ���
	islandMap(2); # ����Ͽޡ��ü�⡼��
}

# ����������������
sub makeNewIsland {
	# �Ϸ�����
	my($land, $landValue, $land2, $landValue2) = makeNewLand($_[0]);
	
	# ������ޥ�ɤ�����
	my(@command, $i);
	for($i = 0; $i < $HcommandMax; $i++) {
		$command[$i] = {
		'kind' => $HcomDoNothing,
		'target' => 0,
		'x' => 0,
		'y' => 0,
		'arg' => 0,
		'tx' => 0,
		'ty' => 0
		};
	}

	# ����Ǽ��Ĥ����
	my(@lbbs);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$lbbs[$i] = "0<<0>>";
	}

	my($StartMoney) = $HinitialMoney + $HislandTurn * 3;
	$StartMoney *= 2 if($HwarFlg);
	$HspacePrize = ($HspacePrize) ? 512 : 0;

	my($order) = ($HwarFlg) ? 0 : 128;

	# ��ˤ����֤�
	return {
	'land' => $land,
	'landValue' => $landValue,
	'land2' => $land2,
	'landValue2' => $landValue2,
	'command' => \@command,
	'lbbs' => \@lbbs,
	'money' => $StartMoney,
	'food' => $HinitialFood,
	'order' => $order,
	'prize' => "$HspacePrize,0,"
	};
}

# ����������Ϸ����������
sub makeNewLand {
	my($mode) = @_;

	# ���ܷ������
	my(@land, @landValue, @land2, @landValue2, $x, $y, $i, $r);

	# ���˽����
	for($y = 0; $y < $HislandSize; $y++) {
		for($x = 0; $x < $HislandSize; $x++) {
			$land[$x][$y] = $HlandSea;
			$landValue[$x][$y] = 0;
			$land2[$x][$y] = $HlandSea;
			$landValue2[$x][$y] = 0;
		}
	}
	my($center) = $HislandSize / 2 - 1;
	if($mode == 2){
		# ���Ƴ��ΤȤ�
		return (\@land, \@landValue, \@land2, \@landValue2);
	}elsif($mode == 3){
		# ʿ��
		for($y = 1; $y < $HislandSize-1; $y++) {
			$st = abs($y - $center) - 1;
			$st = 1 if($st < 1);
			$en = $HislandSize - abs($y - $center) + 1;
			$en = $HislandSize-1 if($en > $HislandSize-1);
			for($x = $st; $x < $en; $x++) {
				$land[$x][$y] = $HlandPlains;
				$landValue[$x][$y] = 0;
				$land2[$x][$y] = $HlandSea;
				$landValue2[$x][$y] = 0;
			}
		}
		my($count) = 0;
		while($count < 5) {
			# �������ɸ
			$x = random(6) + $center - 1;
			$y = random(6) + $center - 1;
			if(random(2)){
				$land[$x][$y] = $HlandForest;
				$landValue[$x][$y] = 5;
			}else{
				$land[$x][$y] = $HlandSea;
				$landValue[$x][$y] = 1;
			}
			$count++;
		}
		return (\@land, \@landValue, \@land2, \@landValue2);
	}elsif($mode == 4){
		# �Ի�
		for($y = 1; $y < $HislandSize-1; $y++) {
			$st = abs($y - $center) - 1;
			$st = 1 if($st < 1);
			$en = $HislandSize - abs($y - $center) + 1;
			$en = $HislandSize-1 if($en > $HislandSize-1);
			for($x = $st; $x < $en; $x++) {
				$land[$x][$y] = $HlandTown;
				$landValue[$x][$y] = 200;
				$land2[$x][$y] = $HlandSea;
				$landValue2[$x][$y] = 0;
			}
		}
		my($count) = 0;
		while($count < 5) {
			# �������ɸ
			$x = random(6) + $center - 1;
			$y = random(6) + $center - 1;
			if(random(2)){
				$land[$x][$y] = $HlandForest;
				$landValue[$x][$y] = 5;
			}else{
				$land[$x][$y] = $HlandSea;
				$landValue[$x][$y] = 1;
			}
			$count++;
		}
		return (\@land, \@landValue, \@land2, \@landValue2);
	}
	
	$r = random(100);
	if($r < 60) {
	} elsif($r < 70) {
		$center += 1;
	} elsif($r < 80) {
		$center += 2;
	} elsif($r < 90) {
		$center -= 1;
	} else {
		$center -= 2;
	}

	my($rct,$range,$range2,$area) = (999,8,3,25);
	if($HinitialArea < 35){
		$HinitialArea = 44;
		$rct = 100;
	}
	if($HinitialArea > 60){
		$HinitialArea = 80 if($HinitialArea > 80);
		$center = $HislandSize / 2 - 1;
		# ���Ϥ����� 49
		for($y = $center - 3; $y < $center + 4; $y++) {
			for($x = $center - 3; $x < $center + 4; $x++) {
				$land[$x][$y] = $HlandWaste;
			}
		}
		$range = 12;
		$range2 = 5;
		$area = 49;
		$HinitialBase = 10 if($HinitialBase > 10);
	}else{
		if($HinitialArea > 44){
			$center = $HislandSize / 2 - 1;
			$range = 10;
			$range2 = 4;
			$HinitialBase = 10 if($HinitialBase > 10);
		}else{
			$HinitialBase = 5 if($HinitialBase > 5);
		}
		# ���Ϥ����� 25
		for($y = $center - 2; $y < $center + 3; $y++) {
			for($x = $center - 2; $x < $center + 3; $x++) {
				$land[$x][$y] = $HlandWaste;
			}
		}
		$area = 25;
	}

	# �ϰ����Φ�Ϥ�����
	for($i = 0; $i < $rct; $i++) {
		# �������ɸ
		$x = random($range) + $center - $range2;
		$y = random($range) + $center - $range2;
		if(countAroundM(\@land, $x, $y, $HlandSea, 7) != 7){
			# �����Φ�Ϥ������硢�����ˤ���
			# �����Ϲ��Ϥˤ���
			# ���Ϥ�ʿ�Ϥˤ���
			if($land[$x][$y] == $HlandWaste){
				$land[$x][$y] = $HlandPlains;
				$landValue[$x][$y] = 0;
			}elsif($land[$x][$y] == $HlandSea){
				if($landValue[$x][$y] == 1) {
					$land[$x][$y] = $HlandWaste;
					$landValue[$x][$y] = 0;
					$area++;
					last if($HinitialArea <= $area);
				}else{
					$landValue[$x][$y] = 1;
				}
			}
		}
	}

	# ������
	my($count) = 0;
	while($count < 4) {
		# �������ɸ
		$x = random(4) + $center - 1;
		$y = random(4) + $center - 1;
		if(!(($land[$x][$y] == $HlandSea) && ($HinitialArea == $area)) &&
			($land[$x][$y] != $HlandForest)) {
			$land[$x][$y] = $HlandForest;
			$landValue[$x][$y] = 10;
			$count++;
		}
	}

	# Į����
	$count = 0;
	while($count < 2) {
		# �������ɸ
		$x = random(4) + $center - 1;
		$y = random(4) + $center - 1;
		if(!(($land[$x][$y] == $HlandSea) && ($HinitialArea == $area)) &&
			($land[$x][$y] != $HlandTown) &&
			($land[$x][$y] != $HlandForest)) {
			$land[$x][$y] = $HlandTown;
			$landValue[$x][$y] = 10;
			$count++;
		}
	}

	# ������
	$count = 0;
	while($count < 1) {
		# �������ɸ
		$x = random($range) + $center - 3;
		$y = random($range) + $center - 3;
		if(!(($land[$x][$y] == $HlandSea) && ($HinitialArea == $area)) &&
			($land[$x][$y] != $HlandTown) &&
			($land[$x][$y] != $HlandForest) &&
			($land[$x][$y] != $HlandMountain)) {
			$land[$x][$y] = $HlandMountain;
			$landValue[$x][$y] = 0;
			$count++;
		}
	}

	# ���Ϥ���
	$count = 0;
	if($HinitialBase > 3){
		$range = 6;
	}else{
		$range = 4;
	}
	while($count < $HinitialBase) {
		# �������ɸ
		$x = random($range) + $center - 1;
		$y = random($range) + $center - 1;
		if(!(($land[$x][$y] == $HlandSea) && ($HinitialArea == $area)) &&
			($land[$x][$y] != $HlandTown) &&
			($land[$x][$y] != $HlandForest) &&
			($land[$x][$y] != $HlandMountain) &&
			($land[$x][$y] != $HlandBase)) {
			$land[$x][$y] = $HlandBase;
			$landValue[$x][$y] = $HinitialBaseEx;
			$count++;
		}
	}

	# �������
	$count = 0;
	while($count < 1) {
		# �������ɸ
		$x = random(4) + $center - 1;
		$y = random(4) + $center - 1;
		if(!(($land[$x][$y] == $HlandSea) && ($HinitialArea == $area)) &&
			($land[$x][$y] != $HlandTown) &&
			($land[$x][$y] != $HlandForest) &&
			($land[$x][$y] != $HlandMountain) &&
			($land[$x][$y] != $HlandBase) &&
			($land[$x][$y] != $HlandFarm)) {
			$land[$x][$y] = $HlandFarm;
			$landValue[$x][$y] = 10;
			$count++;
		}
	}

	return (\@land, \@landValue, \@land2, \@landValue2);
}

#----------------------------------------------------------------------
# �����ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub changeMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($flag) = 0;

	# �ѥ���ɥ����å�
	if(checkSpecialPassword($HoldPassword)) {
		# �ü�ѥ����
		if($HcurrentName =~ /^̵��$/) {
			# �����⡼��
			deleteIsland();
			return;
		} else {
			$island->{'money'} = $MaxMoney;
			$island->{'food'} = $MaxFood;
		}
	} elsif(!checkPassword($island->{'password'},$HoldPassword)) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	# ��ǧ�ѥѥ����
	if($HinputPassword2 ne $HinputPassword) {
		# password�ְ㤤
		unlock();
		tempWrongPassword();
		return;
	}

	if($HcurrentName ne '') {
		# ̾���ѹ��ξ��
		# ̾���������������å�
		if(($HcurrentName =~ /[\\,\?\(\)\<\>\$]|^̵��$/) || ($HcurrentName =~ /[\\,\?\(\)\<\>\$]|^ƿ̾$/)) {
			# �Ȥ��ʤ�̾��
			unlock();
			tempNewIslandBadName();
			return;
		}

		# ̾���ν�ʣ�����å�
		if(nameToNumber($HcurrentName) != -1) {
			# ���Ǥ�ȯ������
			unlock();
			tempNewIslandAlready();
			return;
		}

		if($island->{'money'} < $HcostChangeName) {
			# �⤬­��ʤ�
			unlock();
			tempChangeNoMoney();
			return;
		}

		# ���
		unless(checkSpecialPassword($HoldPassword)) {
			$island->{'money'} -= $HcostChangeName;
		}

		# ̾�����ѹ�
		logChangeName($island->{'name'}, $HcurrentName);
		$island->{'name'} = $HcurrentName;
		$flag = 1;
	}

	if($HcurrentOwnerName ne '') {
		# �����ʡ��ѹ��ξ��
		$island->{'ownername'} = htmlEscape($HcurrentOwnerName);
		$flag = 1;
	}

	# password�ѹ��ξ��
	if($HinputPassword ne '') {
		# �ѥ���ɤ��ѹ�
		$island->{'password'} = encode($HinputPassword);
		$flag = 1;
	}

	if(($flag == 0) && !checkSpecialPassword($HoldPassword)) {
		# �����ѹ�����Ƥ��ʤ�
		unlock();
		tempChangeNothing();
		return;
	}

	# �ǡ����񤭽Ф�
	if(!writeIslandsFile($HcurrentID, 1)) {
		unlock();
		tempFailWrite();
		return;
	}
	unlock();

	# �ѹ�����
	tempChange();
}

# ��ζ������
sub deleteIsland {
	my($island) = $Hislands[$HidToNumber{$HcurrentID}];

	# ��ơ��֥�����
	$island->{'pop'} = -100;

	# �͸���˥�����
	my($flag, $i, $tmp);
	my @idx = (0..$#Hislands);
	@idx = sort { $Hislands[$b]->{'pop'} <=> $Hislands[$a]->{'pop'} || $a <=> $b } @idx;
	@Hislands = @Hislands[@idx];

	logDeleteIsland($tmpid, $island->{'name'});

	# �ᥤ��ǡ��������
	$HislandNumber--;
	OceanMente($island->{'id'});
	writeIslandsFile($HcurrentID);
	
	# �ǡ����񤭽Ф�
	if(!writeIslandsFile($HcurrentID, 1)) {
		unlock();
		tempFailWrite();
		return;
	}
	unlink("${HdirName}/island.${HcurrentID}");
#	unlink("island.$HcurrentID");
	unlock();
	tempDeleteIsland($island->{'name'});
}

# �͸�����¾���ͤ򻻽� �ʰ���
sub estimateM {
	my($number) = $_[0];
	my($pop, $popsea, $area, $farm, $MissileK) = (0, 0, 0, 0, 0);
	# �Ϸ������
	my($island) = $Hislands[$number];
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};

	# ������
	my($x, $y, $kind, $value);
	for($y = 0; $y < $HislandSize; $y++) {
		for($x = 0; $x < $HislandSize; $x++) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			
			$area++ if($HseaChk[$kind] == 0); # ���ϤǤʤ��Ȥ�
			if($kind == $HlandTown) {
				# Į
				$value = 200 if($value > 200);
				$pop += $value;
			} elsif($kind == $HlandFarm) {
				# ����
				$farm += $value;
			} elsif(($kind == $HlandBase) || ($kind == $HlandSbase)) {
				# �ߥ�����ȯ�Ϳ�
				$MissileK += expToLevel($kind, $value);
			}
		}
	}
	# ����
	$island->{'pop'}   = $pop;
	$island->{'farm'}  = $farm;
	$island->{'area'}  = $area;
	$island->{'MissileK'}   = $MissileK;
}


# �ϰ�����Ϸ�������� �ʰ���
sub countAroundM {
	my($land, $x, $y, $kind, $range) = @_;
	my($i, $sx, $sy);
	my $count = 0;
	for($i = 0; $i < $range; $i++) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];

		# �Ԥˤ�����Ĵ��
		$sx-- if (!($sy % 2) && ($y % 2));

		if(($sx < 0) || ($sx >= $HislandSize) || ($sy < 0) || ($sy >= $HislandSize)) {
			# �ϰϳ��ξ�� ���ʤ�û�
			$count++ if($kind == $HlandSea);
		} else {
			# �ϰ���ξ��
			$count++ if($land->[$sx][$sy] == $kind);
		}
	}
	return $count;
}

#----------------------------------------------------------------------
# ����͸���Ͽ neo_otacky�᤬����
#----------------------------------------------------------------------
# �ᥤ��
sub rekidaiPopMain {
	my($line, $j, $id, $pop, $turn, $name, $n, @rekidai, $reki, $oldpop);
	my $flag = 0;
	if(!open(RIN, "<${HlogdirName}/rekidai.dat")) {
		rename("${HlogdirName}/rekidai.tmp", "${HlogdirName}/rekidai.dat");
		if(!open(RIN, "<${HlogdirName}/rekidai.dat")) {
			$flag = 1;
		}
	}
	if(!$flag) {
		$n = 0;
		while($line = <RIN>) {
			$line =~ /^([0-9]*),([0-9]*),([0-9]*),(.*)$/;
			($id, $pop, $turn, $name) = ($1, $2, $3, $4);
			$rekidai[$n]->{'id'} = $id;
			$rekidai[$n]->{'pop'} = $pop;
			$rekidai[$n]->{'turn'} = $turn;
			$rekidai[$n]->{'name'} = $name;
			$n++;
		}
		close(RIN);
	}
	# ����
	unlock();

	out(<<END);
<CENTER>$HtempBack</CENTER><BR>
<center>
<H1>�����¿�͸���Ͽ</H1>
<table border=0 width=50%><tr>
<TH $HbgTitleCell align=center nowrap=nowrap>${HtagTH_}���${H_tagTH}</TH>
<TH $HbgTitleCell align=center nowrap=nowrap>${HtagTH_}${AfterName}̾${H_tagTH}</TH>
<TH $HbgTitleCell align=center nowrap=nowrap>${HtagTH_}�͸�${H_tagTH}</TH>
<TH $HbgTitleCell align=center nowrap=nowrap>${HtagTH_}������${H_tagTH}</TH>
END
	if(!$flag) {
		$j = 0;
		$n = 1;
		$oldpop = 0;
		$pop = 0;
		while(($j < 10) || $flag) {
			$reki = $rekidai[$j];
			last unless(defined $reki->{'pop'});
			$oldpop = $pop;
			($id, $pop, $turn, $name) = ($reki->{'id'}, $reki->{'pop'}, $reki->{'turn'}, $reki->{'name'});
			if(defined $HidToNumber{$id}) {
				$name = "<A STYlE=\"text-decoration:none\" HREF=\"${HthisFile}?Sight=${id}\" alt=\"ID=${id}\" title=\"ID=${id}\">${HtagName_}$name${AfterName}${H_tagName}</A>";
			} else {
				$name = "${HtagName2_}$name${AfterName}${H_tagName2}";
			}
			$j++;
			$n = $j if($oldpop > $pop);
			$reki = $rekidai[$j];
			$flag =0 unless(defined $reki->{'pop'});
			if($reki->{'pop'} < $pop) {
				$flag =0;
			} else {
				$flag =1;
			}
			out(<<END);
</tr><tr>
<TD $HbgNumberCell align=right nowrap=nowrap>${HtagNumber_}$n${H_tagNumber}</TD>
<TD $HbgNameCell align=right nowrap=nowrap>$name</TD>
<TD $HbgInfoCell align=right nowrap=nowrap>$pop${HunitPop}</TD>
<TD $HbgInfoCell align=right nowrap=nowrap>$turn</TD>
END
		}
	} else {
		out(<<END);
</tr><tr><TH colspan=4>�ǡ���������ޤ���</TH>
END
	}
	out(<<END);
</tr></table></center>
<div align=right>Scripted By neo_otacky</div>
END
}

#----------------------------------------------------------------------
# �����ͥ⡼�� neo_otacky�᤬���������Τ�����Ѥ˲���
#----------------------------------------------------------------------

# BattleField�����⡼��
sub bfieldMain {
	if (!$HbfieldMode) {
		unlock();
		tempHeader();
		# �ѥ���ɥ����å�
		if(checkPassword($HspecialPassword, $HdefaultPassword)) {
			# �ü�ѥ����
			tempBfieldPage();
		} else {
			# password�ְ㤤
			tempWrongPassword();
		}
	} else {
		# BattleField����
		newIslandMain($HbfieldMode);
	}
}

# BattleField�����⡼�ɤΥȥåץڡ���
sub tempBfieldPage {
	out(<<END);
$HtempBack<hr>
<H1>Battle Field�����</H1>
<FORM action="$HthisFile" method="POST">
�ɤ��BattleField�ˤ��ޤ�����<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>$AfterName<BR>
�����ʡ�̾(��ά��)<br>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
�ѥ���ɤϡ�<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
ǰ�Τ���ѥ���ɤ�⤦���<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>
��������Battle Field���Ϸ��Υѥ���������򤷤Ƥ���������<BR>
<SELECT NAME="LBFIELD">
<OPTION VALUE="1" SELECTED>�濴����
<OPTION VALUE="2">���Ƴ�
<OPTION VALUE="3">ʿ�Ϥ��餱����
<OPTION VALUE="4">�ԻԤ��餱����
</SELECT><BR><BR>
<INPUT TYPE="hidden" VALUE="${\htmlEscape($HdefaultPassword)}" NAME="Bfield">
<INPUT TYPE="submit" VALUE="Battle Field����" NAME="BfieldButton">
</FORM>
END
}

# BattleField������λ
sub tempBfieldOK {
	out(<<END);
${HtagBig_}$_[0]${AfterName}��Battle Field������ѹ����ޤ�����<br>$_[1]${H_tagBig}$HtempBack
END
}

# BattleField��������
sub tempBfieldNG {
	out(<<END);
${HtagBig_}Battle Field�����ꥨ�顼($_[0])��${H_tagBig}$HtempBack
END
}

# �����ͤˤ��ץ쥼��ȥ⡼��
sub presentMain {
	if (!$HpresentMode) {
		# ����
		unlock();

		# �ƥ�ץ졼�Ƚ���
		tempPresentPage();
	} else {
		# �ѥ���ɥ����å�
		if(checkPassword($HspecialPassword, $HoldPassword)) {
			# �ü�ѥ����

			if(!$HpresentMoney && !$HpresentFood) {
				# ��⿩����ʤ�
				tempPresentEmpty();
				unlock();
				return;
			}

			# id����������
			$HcurrentNumber = $HidToNumber{$HcurrentID};
			my($island) = $Hislands[$HcurrentNumber];
			my($name)   = $island->{'name'};

			$island->{'money'} += $HpresentMoney;
			if($island->{'money'} < 0){
				$island->{'money'} = 0;
			}elsif($island->{'money'} > $MaxMoney){
				$island->{'money'} = $MaxMoney;
			}
			$island->{'food'} += $HpresentFood;
			if($island->{'food'} < 0){
				$island->{'food'} = 0;
			}elsif($island->{'food'} > $MaxFood){
				$island->{'food'} = $MaxFood;
			}
			logPresent($HcurrentID, $name, $HpresentLog);

			# �ǡ����񤭽Ф�
			if(!writeIslandsFile($HcurrentID, 1)) {
				unlock();
				tempFailWrite();
				return;
			}
			unlock();
			# �ѹ�����
			tempPresentOK($name);
		} else {
			# password�ְ㤤
			unlock();
			tempWrongPassword();
			return;
		}
	}
}

# �ץ쥼��ȥ⡼�ɤΥȥåץڡ���
sub tempPresentPage {
	out(<<END);
$HtempBack<hr>
<H1>����${AfterName}�˥ץ쥼��Ȥ�£��</H1>
<UL>
<LI>��ȯ���ε�Ͽ�פ˥����Ĥ륤�٥�ȤȤ��Ʊ����Ԥ����Ȥ��Ǥ��ޤ���
<LI>ɽ�����줿�ե������ɬ�פ��ͤ��å����������Ϥ��ơ��ѥ���ɤˡ��ü�ѥ���ɡפ����졢�֥ץ쥼��Ȥ�£��ץܥ���򲡤��Хץ쥼��ȤǤ��ޤ���
<LI>���ˤ�HTML������Ȥ��ޤ������ְ�ä����κ�����Ǥ��ޤ���Τǡ����Ť����Ϥ��Ƥ������������餫����֥饦����ɽ���ƥ��Ȥ�ԤäƤ������ۤ��������Ǥ��礦����ȯ���ε�Ͽ�פ��Ѥʥ����Ĥ�ȡ�����ä��Ѥ��������Ǥ���
<LI>���俩������ͭ�̤������ͤ�Ķ���뤳�Ȥ�ޥ��ʥ��ˤϤʤ�ʤ��褦���ڤ�ΤƤƤ��ޤ����Х��к��Ǥ��ΤǤ�λ������������
</UL><BR>
<FORM action="$HthisFile" method="POST">
<B>�ץ쥼��Ȥ�������${AfterName}�ϡ�</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR><BR>
<B>�ץ쥼��Ȥ����Ƥϡ�(�ޥ��ʥ��ͤ��ǽ)</B><BR>
<INPUT TYPE="text" NAME="PRESENTMONEY" VALUE="0" SIZE=16 MAXLENGTH=16>$HunitMoney<BR>
<INPUT TYPE="text" NAME="PRESENTFOOD"  VALUE="0" SIZE=16 MAXLENGTH=16>$HunitFood<BR>
<BR>
<B>����å������ϡ�(��ά��ǽ����Ƭ��${AfterName}̾����������ޤ�)</B><BR>
����${AfterName}<INPUT TYPE="text" NAME="PRESENTLOG"  VALUE="" SIZE=128 MAXLENGTH=256><BR>
<BR>
<B>�ѥ���ɤϡ�</B><BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="�ץ쥼��Ȥ�£��" NAME="PresentButton"><BR>
</FORM>
END
}

# �ץ쥼��ȴ�λ
sub tempPresentOK {
	out(<<END);
${HtagBig_}$_[0]${AfterName}�˥ץ쥼��Ȥ�£��ޤ���${H_tagBig}$HtempBack
END
}

# �ץ쥼������Ƥ���������
sub tempPresentEmpty {
	out(<<END);
${HtagBig_}�ץ쥼��Ȥ����Ƥ����������褦�Ǥ�${H_tagBig}$HtempBack
END
}

# �����ͤˤ�����ۥ⡼��
sub punishMain {
	if(checkPassword($HspecialPassword, $HdefaultPassword)) {
		# �ü�ѥ����
		if ($HpunishMode) {
			my(%punish);
			if (open(Fpunish, "<${HdirName}/punish.dat")) {
				local(@_);
				while (<Fpunish>) {
					chomp;
					@_ = split(',');
					my($obj);
					$obj->{turn} = shift;
					$obj->{id} = shift;
					$obj->{punish} = shift;
					$obj->{x} = shift;
					$obj->{y} = shift;
					$punish{$obj->{id}} = $obj;
				}
				close(Fpunish);
			}

			if (open(Fpunish, ">${HdirName}/punish.dat")) {
				{
					my($obj);
					$obj->{turn} = $HislandTurn;
					$obj->{id} = $HcurrentID;
					$obj->{punish} = $HpunishID;
					$obj->{x} = $HcommandX;
					$obj->{y} = $HcommandY;
					$punish{$obj->{id}} = $obj;
				}

				my($key, $obj);
				while (($key, $obj) = each %punish) {
					next if ($obj->{punish} == 0);
					print Fpunish
						$obj->{turn} . ','.
						$obj->{id} . ','.
						$obj->{punish} . ','.
						$obj->{x} . ','.
						$obj->{y} . "\n";
				}
				close(Fpunish);
			}
		}

		unlock();

		# �ƥ�ץ졼�Ƚ���
		tempPunishPage();

	} else {
		# �ѥ���ɤ����פ��ʤ���Хȥåץڡ�����
		unlock();

		# �ƥ�ץ졼�Ƚ���
		tempTopPage();
	}
}

# ���ۥ⡼�ɤΥȥåץڡ���
sub tempPunishPage {
	my(@punishName) =(
		 '�ʤ�',
		 '�Ͽ̡ʺ�ɸ�����',
		 '����',
		 '���áʿ͸���說�ꥢ���Τߡ�',
		 '�������������Ѿ�說�ꥢ���Τߡ�',
		 '����',
		 '������Сʺ�ɸ�����',
		 '���',
		 'ʮ�Сʺ�ɸ�����',
		 '����������',
		 '���ۤ��Τ���סʺ�ɸ�����',
		 '�кҡʺ�ɸ�����');
	out(<<END);
$HtempBack<hr>
<H1>����${AfterName}�����ۤ�ä���</H1>
���ۤϻ��ꤷ�������ҳ���ɬ��ȯ�������ޤ����㤨�С֣�${AfterName}�����������פȤ����ؼ���Ф��ȼ��Υ�����������������ޤ���
<br>���β�¤�ϡ��ֹӤ餷�Ȥ����ۤɤǤϤʤ���Ȣ���ʷ�ϵ��򰭲�������褦�ʹ԰٤򤹤�ץ쥤�䡼�פ䡢
<br>�ִ����ͤη�᤿������롼��˰�ȿ���Ƥ��Ʋ����θ����ߤ��ʤ��ץ쥤�䡼�פʤɤ˼����ҳ���ȯ��������ʪ�餷���Ǥ���
<br>�ּ¤ˤ������֤˵�����СפȤ��ֱ��������������פʤɤ�������С����ޤ���᤺������${AfterName}�ϼ��β����ޤ���
<br>�֥롼��˰�ȿ�����פȻפ����ˡ��֤��Υ롼���ï�⤬�ɤ����˽񤤤Ƥ��뤫���פ��ǧ���ޤ��礦��
<br>���ۤ�ä���ΤϤ��䤹�����ȤǤ����������˴����ͤȤ��Ƥ�Ω��ǹԤäƤ��뤫�ͤ��ޤ��礦��
<br>���ۤ�ä��ʤ���Фʤ�ʤ��ۤ��ﳲ���礭�����ͤ��ޤ��礦��¾��${AfterName}�����Ǥ�ݤ��Ƥ���Ȥ��äƤ⤿���Υ�����ʤΤǤ����顣
<br><FONT COLOR="red">���ۤ�¸�ߤ϶���ˤ��ޤ��礦��</FONT>���ۤ����餫�ˤʤ��¾�Υץ쥤�䡼�Ȥο���ط�������ޤ���
<br><br>���ۤ�Ȣ���¤�Ԥϡ����ε�ǽ��侩���Ƥ��ޤ���
<br>���꤬���뻲�üԤȤϷǼ��Ĥʤɤ��ä��礤�ǲ�褹�٤��Ǥ������ˤ�äƤ϶���Ū�ˤ���ĺ���Τ�
<br>�������ʤ��ȤϹͤ��Ƥ��ޤ����������������Ƥ����꤬���뻲�üԤ���β�������Ϥɤ����ȻפäƤ��ޤ���
<br>���Ƥλ��üԤϤ��Ȥ������ʤ��Ȥ�ԤäƤ����Ȥ��Ƥ⥲����Ǥϸ�ʿ�Ǥ���٤����ȻפäƤ��ޤ���
<br>
<br>����������ϡ����򤷤�${AfterName}�ˤ���̵��°�ʳ����������Ƶ��Ԥ���������Ǥ���
<br>���ۤ��Τ���פϡ����򤷤�${AfterName}�˵��ۤΤ��Τ��и������ޤ���
<br>�кҤϡ�ǳ�����Ϸ������򤷤����Τ߼¹Ԥ���ޤ���
</DL>

<FORM name="lcForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="${\htmlEscape($HdefaultPassword)}" NAME="Punish">
<B>���ۤ�ä���${AfterName}�ϡ�</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<INPUT TYPE="button" VALUE="�ޥåפ򳫤�" onclick="printIsland();">
<BR><BR>
<B>��ɸ�ϡ��ʺ�ɸ����Ǥ������ۤǤΤ�ͭ����</B><BR>
<B>(</B><SELECT NAME=POINTX>
END

	my($i);
	for($i = 0; $i < $HislandSize; $i++) {
		if($i == $HdefaultX) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}

	out(<<END);
</SELECT><B>, </B><SELECT NAME=POINTY>
END

	for($i = 0; $i < $HislandSize; $i++) {
		if($i == $HdefaultY) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}

	out(<<END);
</SELECT><B>)</B><BR>
<BR>
<B>���ۤ����Ƥϡ�</B><BR>
<SELECT NAME="PUNISHID">
<OPTION VALUE="0">$punishName[0]
<OPTION VALUE="1">$punishName[1]
<OPTION VALUE="2">$punishName[2]
<OPTION VALUE="3">$punishName[3]
<OPTION VALUE="4">$punishName[4]
<OPTION VALUE="5">$punishName[5]
<OPTION VALUE="6">$punishName[6]
<OPTION VALUE="7">$punishName[7]
<OPTION VALUE="8">$punishName[8]
<OPTION VALUE="9">$punishName[9]
<OPTION VALUE="10">$punishName[10]
<OPTION VALUE="11">$punishName[11]
</SELECT><BR>
<BR>
<INPUT TYPE="submit" VALUE="���ۤ�ä���" NAME="PunishButton"><BR>
</FORM>
<SCRIPT Language="JavaScript">
<!--
function printIsland() {
	var iid;
	with (document.forms[0].elements[1]) {
		iid = options[selectedIndex].value;
	}
	window.open("$HthisFile?Sight=" + iid, "punish", "toolbar=0,location=0,directories=0,menubar=0,status=1,scrollbars=1,resizable=1,width=450,height=630");
}
//-->
</SCRIPT>
END

	if (open(Fpunish, "<${HdirName}/punish.dat")) {
		out("<HR><TABLE BORDER><TR><TH $HbgTitleCell>${AfterName}̾</TH><TH $HbgTitleCell>��������</TH><TH $HbgTitleCell>��ɸ</TH></TR>");
		local(@_);
		my($island);
		while (<Fpunish>) {
			chomp;
			@_ = split(',');
			my($obj);
			$obj->{turn} = shift;
			$obj->{id} = shift;
			$obj->{punish} = shift;
			$obj->{x} = shift;
			$obj->{y} = shift;

			$HcurrentNumber = $HidToNumber{$obj->{id}};
			$island = $Hislands[$HcurrentNumber];

			out("<TR><TD $HbgInfoCell>$island->{'name'}${AfterName}</TD><TD $HbgInfoCell>$punishName[$obj->{punish}]</TD><TD $HbgInfoCell>($obj->{x}, $obj->{y})</TD></TR>");
		}
		out('</TABLE>');
		close(Fpunish);
	}
}

# �����ͤˤ���Ϸ��ѹ��⡼��
sub lchangeMain {
	# �ü�ѥ����
	if(checkPassword($HspecialPassword, $HdefaultPassword)) {
		
		# id����������
		$HcurrentNumber = $HidToNumber{$HcurrentID};
		my($island) = $Hislands[$HcurrentNumber];
		if ($HlchangeMode) {

			# �Ϸ����ͤ�������������å�
			if(!landCheck($HlchangeKIND, $HlchangeVALUE)) {
				tempBadValue();
				unlock();
				return;
			}

			$island->{'land'}->[$HcommandX][$HcommandY] = $HlchangeKIND;
			$island->{'landValue'}->[$HcommandX][$HcommandY] = $HlchangeVALUE;
			$island->{'land2'}->[$HcommandX][$HcommandY] = $HlandSea;
			$island->{'landValue2'}->[$HcommandX][$HcommandY] = 0;

			# �ǡ����񤭽Ф�
			if(!writeIslandsFile($HcurrentID, 2)) {
				unlock();
				tempFailWrite();
				return;
			}
			unlock();
			# �ѹ�����
			tempLchangeOK($island->{'name'});
		}
		unlock();
		# �ƥ�ץ졼�Ƚ���
		tempLchangePage();
	} else {
		# �ѥ���ɤ����פ��ʤ���Хȥåץڡ�����
		unlock();
		require('hako-top.cgi');
		# �ƥ�ץ졼�Ƚ���
		tempTopPage();
	}
}

# �Ϸ��ѹ��⡼�ɤΥȥåץڡ���
sub tempLchangePage {
	out(<<END);
$HtempBack<hr>
<H1>����${AfterName}���Ϸ��ǡ������ѹ�����</H1>
����Ū�ˡ�<b>�����ư��ʤ��ʤ붲��</b>������ޤ��Τ�<B>${AfterName}�Υǡ�����񤭴����ʤ��ǲ�������</B><BR>
<b>ɬ���񤭴���������Ȣ��ǡ����ΥХå����åפ�ԤäƤ���������</b><BR>
�Х��ʤɤ��Ϸ������������ʤä����ˤΤ߱��޽��֤Ȥ����Ϸ����ѹ����Ƥ���������<BR>
�μ���̵�����ϳ��Σ�����(����)��ʿ�ϤΣ������ϤΣ��Τɤ줫�Τߤ���Ѥ��Ƥ���������<BR>
�ְ�ä��ѹ��򤷤����ˤʤ�餫�����꤬ȯ�����Ƥ���ڤ���Ǥ�ϤȤ�ޤ���<BR>
���Ϸ��פ��Ф��ơ��Ϸ����͡פ�Ŭ�ڤǤ��뤫�ɤ���������å�(��ȴ��)�򤷤Ƥ��ޤ��Τǡ���դ��Ƥ���������<BR>
<TABLE><TR><TD>
END
	if($HcurrentID != 0){
		islandMap(1);
	}else{
		out("�Ͽ�ɽ�����뤿��ˤϡ�<br>����${AfterName}�����ӥޥåפ򳫤��Ƥ���������");
	}
	$HtargetList = getIslandList($HcurrentID);
	out(<<END);
</TD><TD valign=top>
<FORM name="lcForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="${\htmlEscape($HdefaultPassword)}" NAME="Lchange">
<B>�Ϸ����ѹ�����${AfterName}</B>(ID=$HcurrentID)<BR>
<SELECT NAME="ISLANDID">
$HtargetList
</SELECT><BR>
<INPUT TYPE="submit" VALUE="�ޥåפ򳫤�" NAME="LchangeButtonM"><BR>
<BR><BR>
<B>��ɸ�ϡ�</B><BR>
<B>(</B><SELECT NAME=POINTX>
END
	my($i);
	for($i = 0; $i < $HislandSize; $i++) {
		if($i == $HdefaultX) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}
	out(<<END);
</SELECT><B>, </B><SELECT NAME=POINTY>
END
	for($i = 0; $i < $HislandSize; $i++) {
		if($i == $HdefaultY) {
			out("<OPTION VALUE=$i SELECTED>$i\n");
		} else {
			out("<OPTION VALUE=$i>$i\n");
		}
	}
	out("</SELECT><B>)</B><BR><BR><B>�Ϸ��ϡ�</B><BR><SELECT NAME=\"LCHANGEKIND\">");
	@lcland = ("��","����","ʿ��","Į��","��","����","����","�ߥ��������","�ɱһ���","��","����","�������","��������","��ǰ��","���쵭ǰ��",
				"�ϥ�ܥ�","����","����೹","���ȥӥ�","������","���","����������","ͷ����","������","����","�ع�","�ɡ���","����",
				"���ɽ�","ž������","ưʪ��","���Ի�","������","�����Ի�","����ӥ�","���繩��","��������","�����Ի�","Ķ�����Ի�","�ǥ��ȥ�å�","����","�ޥ��ۡ���",
				"ž��������","��","������","�ٻ���","�±�","�ȥ���","��","�ڴ�","�ٻλ�","��±��","������Ƥ��","����������","����õ����","ͩ����",
				"����","��������","�淿����","�緿����","��ε","ήɹ","���ش�","��ڵ���","������");
	@lclandId = ($HlandSea,$HlandWaste,$HlandPlains,$HlandTown,$HlandForest,$HlandFarm,$HlandFactory,$HlandBase,$HlandDefence,$HlandMountain,
				$HlandMonster,$HlandSbase,$HlandOil,$HlandMonument,$HlandSMonument,$HlandHaribote,$HlandOsen,$HlandSlum,$HlandTower,$HlandSeisei,$HlandBank,
				$HlandStadium,$HlandAmusement,$HlandCasino,$HlandPark,$HlandSchool,$HlandDome,$HlandAirport,$HlandFire,$HlandWarp,$HlandZoo,
				$HlandBigcity,$HlandExpo,$HlandMegacity,$HlandMegatower,$HlandMegaFact,$HlandMegaFarm,$HlandTcity,$HlandHugecity,
				$HlandDeathtrap,$HlandWindmill,$HlandMyhome,$HlandWarpR,$HlandPort,$HlandBreakwater,$HlandPolice,$HlandHospital,$HlandTrump,$HlandFlower,$HlandDokan,$HlandFuji,
				$HlandPirate,$HlandMonsShip,$HlandAegisShip,$HlandProbeShip,$HlandGhostShip,$HlandTreasureS,$HlandFishSShip,
				$HlandFishMShip,$HlandFishLShip,$HlandWingDragon,$HlandIceFloe,$HlandCoupleRock,$HlandTitanic,$HlandBalloonS);
	for($i = 0; $i <= $#lcland; $i++) {
		if($lclandId[$i] == $HlchangeKIND) {
			out("<OPTION VALUE=$lclandId[$i] SELECTED>$lcland[$i]\n");
		} else {
			out("<OPTION VALUE=$lclandId[$i]>$lcland[$i]\n");
		}
	}
	$HlchangeVALUE = 0 if($HlchangeVALUE eq '');
	out(<<END);
</SELECT><BR><BR>
<B>�Ϸ����ͤϡ�</B><BR>
<INPUT TYPE="text" SIZE=6 NAME="LCHANGEVALUE" VALUE="$HlchangeVALUE"><BR>
(�̾�0-200)<BR>
(�ߴ���0-250)<BR>
(����1-3199)<BR>
(����0-59999)<BR>
<BR>
<INPUT TYPE="submit" VALUE="�ѹ�����" NAME="LchangeButton"><BR>
</FORM>
</TD></TR></TABLE>
<SCRIPT Language="JavaScript">
<!--
function ps(x, y) {
	document.lcForm.POINTX.options[x].selected = true;
	document.lcForm.POINTY.options[y].selected = true;
	return true;
}
//-->
</SCRIPT>
END
}

# �Ϸ��ѹ���λ
sub tempLchangeOK {
	out(<<END);
${HtagBig_}$_[0]${AfterName}���Ϸ����ѹ����ޤ���${H_tagBig}<HR>
END
}

# �Ϸ����ͤ���������
sub tempBadValue {
	out(<<END);
${HtagBig_}�Ϸ����ͤ����������褦�Ǥ�${H_tagBig}$HtempBack
END
}

# �Ϸ����ͤ�����å�(��ȴ�����ä˸�Ⱦ)
sub landCheck {
	my($land, $lv) = @_;
	return 0 if($lv < 0);
	if($land == $HlandSea) {
		return 0 if($lv > 200);
	} elsif($land == $HlandWaste) {
		return 0 if($lv > 200);
	} elsif($land == $HlandPlains) {
		return 0 if($lv != 0);
	} elsif($land == $HlandTown) {
		return 0 if(($lv < 1) || ($lv > 200));
	} elsif($land == $HlandForest) {
		return 0 if(($lv < 1) || ($lv > 200));
	} elsif($land == $HlandFarm) {
		return 0 if(($lv < 10) || ($lv > 50));
	} elsif($land == $HlandFactory) {
		return 0 if(($lv < 30) || ($lv > 100));
#		return if(($lv - 30) % 10 != 0);
	} elsif($land == $HlandBase) {
		return 0 if(($lv < 0) || ($lv > $HmaxExpPoint));
	} elsif($land == $HlandDefence) {
		return 0 if($lv > 200);
	} elsif($land == $HlandMountain) {
		return 0 if(($lv < 0) || ($lv > 200));
#		return if($lv % 5 != 0);
	} elsif($land == $HlandMonster) {
		return 0 if($lv > 3199);
	} elsif($land == $HlandSbase) {
		return 0 if(($lv < 0) || ($lv > $HmaxExpPoint));
	} elsif($land == $HlandOil) {
		return 0 if($lv > 200);
	} elsif($land == $HlandMonument) {
		return 0 if($lv > 200);
	} elsif($land == $HlandHaribote) {
		return 0 if($lv > 3199);
	} elsif($land == $HlandOsen) {
		return 0 if($lv > 9);
	} elsif($land == $HlandSlum) {
		return 0 if($lv > 200);
	} elsif($land == $HlandTower) {
		return 0 if(($lv < 0) || ($lv > 200));
#		return if($lv % 10 != 0);
	} elsif($land == $HlandSeisei) {
		return 0 if($lv > 30);
	} elsif($land == $HlandBank) {
		return 0 if($lv > 100);
	} elsif($land == $HlandSeisei) {
		return 0 if($lv > 30);
	} elsif($land == $HlandTrump) {
		return 0 if($lv > 14);
	} elsif($land >= $HlandPirate) {
		return 0 if($lv > 59999);
	} else {
		return 0 if($lv > 200);
	}
	return 1;
}

# �����ͤˤ�뤢������⡼��
sub preDeleteMain {
	if(checkPassword($HspecialPassword, $HdefaultPassword)) {
		# �ü�ѥ����
		preDeleteMainP(1) if($HpreDeleteMode);
		unlock();
		# �ƥ�ץ졼�Ƚ���
		tempPdeleteMain();
	} else {
		# �ѥ���ɤ����פ��ʤ���Хȥåץڡ�����
		require('hako-top.cgi');
		unlock();
		# �ƥ�ץ졼�Ƚ���
		tempTopPage();
	}
}

# �����ͤˤ�뤢������⡼�ɽ���
sub preDeleteMainP {
	my($mode) = @_;
#	HdebugOut("preDeleteMainP��$mode");
	my @newID = ();
	my $flag = 0;
	foreach (@HpreDeleteID) {
		if(!(defined $HidToNumber{$_})) {
		} elsif($_ == $HcurrentID) {
			$flag = 1;
		} else {
			push(@newID, $_);
		}
	}
	if(($HcurrentID > 90) && (!$flag)){
		# Battle Field���ɲå⡼�ɤΤȤ���̵��
		tempPreDelete2($Hislands[$HidToNumber{$HcurrentID}]->{'name'}) if($mode);
	}else{
		@HpreDeleteID = @newID;
		push(@HpreDeleteID, $HcurrentID) if(!$flag);
		# �ǡ����񤭽Ф�
		if($mode){
			writeIslandsFile($HcurrentID);
			if($flag) {
				tempPreDeleteEnd($Hislands[$HidToNumber{$HcurrentID}]->{'name'});
			} else {
				tempPreDelete($Hislands[$HidToNumber{$HcurrentID}]->{'name'});
			}
		}
	}
}
# ��������⡼�ɤΥȥåץڡ���
sub tempPdeleteMain {
	out(<<END);
<CENTER>$HtempBack</CENTER>
<H1>����${AfterName}������ͤ�������ˤ���</H1>

<DL>
<DT>����������ˤʤä�${AfterName}�ϡ����������(�������������ޥ�ɽ�������Ĺ���ҳ���)����ʤ��ʤ�ޤ���</DT>
<DT>���޴ط��Ͻ�������ޤ�����¾��${AfterName}����ι���Ϥ��٤Ƽ����Ĥ��Ƥ��ޤ��ޤ���</DT>
<DT>��Battle Field�ϡ�������������ˤ��뤳�Ȥ��Ǥ��ޤ���</DT>
<!--
<DT>�������������${AfterName}���������פ⤷���ϡֶ�������פ��줿��硢�������Թ��
��������Σɣĥǡ��������Τ������������Ԥ��ޤǤ��Τޤ޻Ĥ�ޤ��������Ѽ�(������)�Ϲ�θ����ɬ�פϤ���ޤ���</DT>
-->
</DT>

</DL>

<FORM name="pdForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="${\htmlEscape($HdefaultPassword)}" NAME="Pdelete">
<B>�����ͤ�������ˤ���${AfterName}�ϡ�</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
<INPUT TYPE="submit" VALUE="���ꡦ���" NAME="PdeleteButton"><BR>
</FORM>
<TABLE BORDER><TR><TH>�����������${AfterName}</TH></TR>
END

	if($HpreDeleteID[0] eq '') {
		out("<TR><TH>�����ͤ��������${AfterName}�Ϥ���ޤ���</TH></TR>");
	} else {
		my($name);
		foreach (@HpreDeleteID) {
			next if(!(defined $HidToNumber{$_}));
			$name = $Hislands[$HidToNumber{$_}]->{'name'};
			out("<TR><TD>$name${AfterName}</TD></TR>");
		}
	}
	out("</TABLE>");
}

# �����ͤ�����������
sub tempPreDelete {
	out(<<END);
${HtagBig_}$_[0]${AfterName}������ͤ�������ˤ��ޤ���${H_tagBig}
<HR>
END
}

# �����ͤ�����������̵��
sub tempPreDelete2 {
	out(<<END);
${HtagBig_}$_[0]${AfterName}�ϴ����ͤ�������ˤǤ��ޤ���${H_tagBig}
<HR>
END
}

# �����ͤ���������
sub tempPreDeleteEnd {
	my($name) = @_;
	out(<<END);
${HtagBig_}$_[0]${AfterName}�δ����ͤ�������������ޤ���${H_tagBig}
<HR>
END
}

# �����ͤˤ��Ƽ���ǡ����ѹ��⡼��
sub ichangeMain {
	if(checkPassword($HspecialPassword, $HdefaultPassword)) {
		# �ü�ѥ����
		ichangeMainP() if($HichangeMode);
		unlock();
		# �ƥ�ץ졼�Ƚ���
		tempIchangePage();
	} else {
		# �ѥ���ɤ����פ��ʤ���Хȥåץڡ�����
		require('hako-top.cgi');
		unlock();
		# �ƥ�ץ졼�Ƚ���
		tempTopPage();
	}
}
# �����ͤˤ��Ƽ���ǡ����ѹ��⡼�ɽ���
sub ichangeMainP {
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$island->{'money'} = int($Hicmoney);
	$island->{'food'} = int($Hicfood);
	$island->{'ally'} = int($Hically);
	$island->{'weapon'} = int($Hicweapon);
	$island->{'evil'} = int($Hicevil);
	if($Hicspace == 1){
		my($prize) = $island->{'prize'};
		$prize =~ /([0-9]*),([0-9]*),(.*)/;
		my($flags,$monsters,$turns) = ($1,$2,$3);
		$flags |= 512 if(!($flags & 512));
		$island->{'prize'} = "$flags,$monsters,$turns";
	}
	if($island->{'money'} > $MaxMoney){
		$island->{'money'} = $MaxMoney;
	}
	if($island->{'food'} > $MaxFood){
		$island->{'food'} = $MaxFood;
	}
	if($island->{'weapon'} > $MaxSigen){
		$island->{'weapon'} = $MaxSigen;
	}
	# �ǡ����񤭽Ф�
	if(!writeIslandsFile($HcurrentID, 1)) {
		unlock();
		tempFailWrite();
		return;
	}
}
# �����ͤˤ��Ƽ���ǡ����ѹ��⡼�ɽ���
sub tempIchangePage {
	my($mode) = @_;
	out(<<END);
<span class='attention'>����ɬ���Хå����åפ򤷤Ƥ���ԤäƤ����������ǡ�����ľ�ܽ�������ΤǴ��Ǥ���</span>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}���${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}ʼ��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}��Ϣ��${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�����${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}��°${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}�ѹ�${H_tagTH}</TH>
</TR>
END
	my($island,$id,$name,$money,$food,$weapon,$evil,$ally,$space,$i,$j,$select_list);
	for($i = 0; $i < $HislandNumber; $i++) {

		$island = $Hislands[$i];
		$id = $island->{'id'};
		next if($id > 90);
		$name = $island->{'name'};
		$money = $island->{'money'};
		$food = $island->{'food'};
		$weapon = $island->{'weapon'};
		$evil = $island->{'evil'};
		$ally = $island->{'ally'};
		
		$space = "";
		my($prize) = $island->{'prize'};
		$prize =~ /([0-9]*),([0-9]*),(.*)/;
		if($1 & 512){
			$space = "CHECKED"
		}
		$j = $i + 1;
		my($zyuni) = $island->{'zyuni'};
		$select_list = "";
		foreach(0 .. $#Hallygroup) {
			if($_ == $ally){
				$select_list .= "<OPTION value=${_} selected>$Hallygroup[$_]\n";
			}else{
				$select_list .= "<OPTION value=${_}>$Hallygroup[$_]\n";
			}
		}
		# <TD><INPUT TYPE="text" SIZE=2 NAME="ICALLY" VALUE="$ally"></TD>
	out(<<END);
<TR>
<FORM name="IchForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="${\htmlEscape($HdefaultPassword)}" NAME="Ichange">
<INPUT TYPE="hidden" VALUE="$id" NAME="ICID">
<TD $HbgNumberCell>${HtagNumber_}$j${H_tagNumber}($zyuni)</TD>
<TD $HbgNameCell>${HtagTH_}${name}${AfterName}${H_tagTH}(${id})</TD>
<TD><INPUT TYPE="text" SIZE=5 NAME="ICMONEY" VALUE="$money">$HunitMoney</TD>
<TD><INPUT TYPE="text" SIZE=5 NAME="ICFOOD" VALUE="$food">$HunitFood</TD>
<TD><INPUT TYPE="text" SIZE=4 NAME="ICWEAPON" VALUE="$weapon">$HunitWeapon</TD>
<TD><INPUT TYPE="text" SIZE=5 NAME="ICEVIL" VALUE="$evil"></TD>
<TD><INPUT TYPE="checkbox"    NAME="ICSPACE" $space></TD>
<TD><SELECT NAME="ICALLY">$select_list</SELECT><b>$Hallymark[$ally]</b></TD>
<TD><INPUT TYPE="submit" VALUE="�ѹ�" NAME="IchangeButton"></TD>
</FORM>
</TR>
END
	}
	out(<<END);
</TABLE>
1${AfterName}���Ȥν�����������ޤ���<br>
��Ϣ���ϡ��ߥ�������Ϥ��ʤ�${AfterName}���ͤ�0�ˤ���ȡ���Ϣ�ݸ�ˤʤ�ޤ���<br>
�ޤ���10000�ʾ�ˤ���Ȳ�����ˤʤ�ޤ���<br>
����ޤϡ�Ϳ���뤳�Ȥ�������ޤ���<br>
END
}

# �֥饦����������
sub getUserAgent {
	$agent2 = $agent = $ENV{'HTTP_USER_AGENT'};
	if ($agent =~ /AOL/) { $agent = 'AOL'; }
	elsif ($agent =~ /Opera/i) {
		if($agent =~ /7./){
			$agent = 'Opera7';
		}elsif($agent =~ /6./){
			$agent = 'Opera6';
		}else{
			$agent = 'Opera';
		}
	}elsif ($agent =~ /MSIE 3/i) { $agent = 'Internet Explorer 3'; }
	elsif ($agent =~ /MSIE 4/i) { $agent = 'Internet Explorer 4'; }
	elsif ($agent =~ /MSIE 5/i) { $agent = 'Internet Explorer 5'; }
	elsif ($agent =~ /MSIE 6/i) { $agent = 'Internet Explorer 6'; }
	elsif ($agent =~ /MSIE 7/i) { $agent = 'Internet Explorer 7'; }
	elsif ($agent =~ /Mozilla\/2/i) { $agent = 'Netscape 2'; }
	elsif ($agent =~ /Mozilla\/3/i) { $agent = 'Netscape 3'; }
	elsif ($agent =~ /Mozilla\/4/i) { $agent = 'Netscape 4'; }
	elsif ($agent =~ /Netscape ?6/i) { $agent = 'Netscape 6'; }
	elsif ($agent =~ /Netscape\/7/i) { $agent = 'Netscape 7'; }
	elsif ($agent =~ /Mozilla\/5/i) { $agent = 'Mozilla'; }
	elsif ($agent =~ /Lynx/i) { $agent = 'Lynx'; }

	if ($agent2 =~ /Wind?o?w?s? ?95/i) { $os = 'Win95'; }
	elsif ($agent2 =~ /Wind?o?w?s? ?9x/i) { $os = 'WinMe'; }
	elsif ($agent2 =~ /Wind?o?w?s? ?98/i) { $os = 'Win98'; }
	elsif ($agent2 =~ /Wind?o?w?s? ?NT ?5.2/i) { $os = 'Win2003'; }
	elsif ($agent2 =~ /Wind?o?w?s? ?NT ?5.1/i) { $os = 'WinXP'; }
	elsif ($agent2 =~ /Wind?o?w?s? ?NT ?5.0/i) { $os = 'Win2000'; }
	elsif ($agent2 =~ /Wind?o?w?s? ?NT/i) { $os = 'WinNT'; }
	elsif ($agent2 =~ /Wind?o?w?s? ?CE/i) { $os = 'WinCE'; }
	elsif ($agent2 =~ /Mac/i) { $os = 'Mac'; }
	elsif ($agent2 =~ /X/ || $agent2 =~ /Sun/i || $agent2 =~ /Linux/i || $agent2 =~ /HP-UX/i || $agent2 =~ /BSD/i) { $os = 'UNIX'; }
	return ($agent,$os);
}

# ��������ǧ
sub setupValue{
	my $mode = 1;
	my $admin;

	if(checkPassword($HspecialPassword, $HdefaultPassword)) {
		$admin = 1;
		$mode = 0;
	}elsif(-e "setup.html") {
		out("<meta HTTP-EQUIV=\"refresh\" CONTENT=\"0; URL=setup.html\">");
	}

	my($src);

	unlock();

	my $turntime = "";
	if($HflexTimeSet){
		# flexTime�����ξ���ɽ������ɬ�פʤ�
	}else{
		my $sec = ($HunitTime % 60);
		$sec = ($sec ? "$sec��" : '');
		my $min = ($HunitTime % 3600);
		$min = ($min ? "$minʬ" : '');
		my $hour = int($HunitTime / 3600);
		$hour = ($hour ? "$hour����" : '');
		$turntime = "<BR>1�����󤬲��ä���<B>${HunitTime}�� ( $hour$min$sec )</B><BR>";
	}
	my @switchStr = ('OFF', 'ON');
	my @switchStrT = ('OFF', 'ON', "ON(�����դ�)");
	my @enaStr  = ('�Ǥ��ʤ�', '�Ǥ���');
	my @doStr  = ('���ʤ�', '����');
	
	$src = <<"END" if($mode);
<HTML>
<HEAD>
<TITLE>
$Htitle
</TITLE>
<BASE HREF="$imageDir/">
<link rel="stylesheet" type="text/css" href="$HcssFile">
</HEAD>
$Body<DIV ID='BodySpecial'>
<DIV ID='LinkHead'>
<A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">Ȣ����祹����ץ����۸�</A>
</DIV>
<HR>
END

	$src .= <<"END";
<CENTER>$HtempBack</CENTER>
<DIV ID='setupValue'>
<H1>���ۤ�Ȣ���������</H1>
END

	$src .= <<"END" if($admin);
--- �������ѡ������ǧ�ǡ��� --- <BR><BR>

����������ѹ��������ϡ�ɬ���ʲ��Υ�󥯤򳫤����ü��Ѥκ�������ԤäƤ���������<BR>
<A HREF="$HbaseDir/hako-main.cgi?SetupV=0" target="_blank">���ü��Ѥκ�����</a><BR>
<BR>
�ǥХå��⡼�ɡ�<B>$switchStr[$Hdebug]</B><BR>
���֥ǥ��쥯�ȥꡡ<B>$HbaseDir</B><BR>
�����ǥ��쥯�ȥꡡ<B>$imageDir</B><BR>
<BR>
���ե������ݻ����������<B>$HlogMax������</B><BR>
�ֺǶ�ν�����פ�ɽ��������Υ��������<B>$HtopLogTurn������</B><BR>
�Хå����åפ򲿥����󤪤��˼�뤫��<B>$HbackupTurn������</B><BR>
�Хå����åפ򲿲�ʬ�Ĥ�����<B>$HbackupTimes��ʬ</B><BR>
ȯ�����ݻ��Կ���<B>$HhistoryMax��</B><BR>
ŷ�����ݻ��Կ���<B>$HWeatherMax��</B><BR>
<BR>
IPɽ����<B>$switchStr[$Hlipdisp]</B><BR>
<BR>
������Ǽ��ǤΥѥ����ǧ�ڡ�<B>$switchStr[$HlbbsAuth]</B><BR>
���Ѹ��ҤΥ�����Ǽ���ƿ̾ȯ����ǽ��<B>$switchStr[$HlbbsAnon]</B><BR>
��ȯ����ȯ���Ԥ�̾��ɽ����<B>$switchStr[$HlbbsSpeaker]</B><BR>
<BR>
ľ��ȯ�⡼�ɤΤȤ��Υѥ���ɡ�<B>$Hurlownermode</B><BR>
�������ʡ�hako-main.cgi?��PASSWORD=****&${Hurlownermode}=��ɣ�<BR>

<BR>
--- ���ü��ѡ������ǧ�ǡ��� --- <BR><BR>
END
	my $tournament = "";
	if($Htournament){
#		$tournament  = "��ͽ�����̲������<B>$HfightMem$AfterName</B><BR>";
#		$tournament .= "��ͽ�����֥��������<B>$HyosenTurn$AfterName</B><BR>";
#		$tournament .= "����ȯ���֥��������<B>$HdevelopeTurn$AfterName</B><BR>";
#		$HfightTurn .= "����Ʈ���֥��������<B>$HdevelopeTurn$AfterName</B><BR>";
		
		# �ʰץȡ��ʥ��ȡ������󹹿������ḫɽ
		$tournament = <<"END";
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
<br><INPUT TYPE="button" VALUE="����åץܡ��ɤ˥��ԡ�" onClick="textcopy(searchID('ALIST').value)"><br>
<textarea NAME="ALIST" cols="100" rows="5">
END
		my $fturn = 0;
		my $islandNumber = $HislandNumber;
		$HfightTurn = $HfinalTurn if($islandNumber <= 2);
		while($HislandTurn >= $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn){
			$fturn += $HdevelopeTurn + $HfightTurn;
		}
		$tournament .= "������\t$AfterName��\t�ʹԾ���\t��������\n";
		my $islandFightMode = $HislandFightMode;
		my $turnCount = $HislandTurnCount;
		while($islandNumber > 1){
			if($HislandTurn < $HyosenTurn){
				# ͽ��
				$islandFightMode = 1;
				$HislandLastTime += 3600 * $HtmTime1[($turnCount % ($#HtmTime1 + 1))];
				$timeString = timeToString($HislandLastTime);
				$tournament .= "$HislandTurn\t$islandNumber\tͽ��\t$timeString\n";
			}elsif($HislandTurn < $HyosenTurn + $HdevelopeTurn + $fturn){
				# ��ȯ
				$islandNumber = $HfightMem if(($islandFightMode == 1) && ($islandNumber > $HfightMem));
				$islandFightMode = 2;
				$HislandLastTime += 3600 * $HtmTime2[($turnCount % ($#HtmTime2 + 1))];
				$timeString = timeToString($HislandLastTime);
				$HfightTurn = $HfinalTurn if($islandNumber <= 2);
				$tournament .= "$HislandTurn\t$islandNumber\t��ȯ\t$timeString\n";
			}elsif($HislandTurn < $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn){
				# ��Ʈ
				$turnCount = 0 if($islandFightMode != 3);
				$HislandLastTime += $HinterTime if($islandFightMode != 3 && $islandNumber > 2);
				$islandFightMode = 3;
				$HislandLastTime += 3600 * $HtmTime3[($turnCount % ($#HtmTime3 + 1))];
				$timeString = timeToString($HislandLastTime);
				$tournament .= "$HislandTurn\t$islandNumber\t��Ʈ��\t$timeString\n";
			}else{
				$turnCount = 0;
				$HislandLastTime += $HinterTime2 if($islandFightMode != 2);
				$islandFightMode = 2;
				$HislandLastTime += 3600 * $HtmTime2[($turnCount % ($#HtmTime2 + 1))];
				$timeString = timeToString($HislandLastTime);
				$fturn += $HdevelopeTurn + $HfightTurn;
				$islandNumber = int($islandNumber / 2 + 0.5);
				$islandNumber++ if(($islandNumber > 2) && (($islandNumber % 2) != 0) && ($HconsolationMatch));
				$HfightTurn = $HfinalTurn if($islandNumber <= 2);
				$tournament .= "$HislandTurn\t$islandNumber\t��ȯ\t$timeString\n" if($islandNumber > 1);
			}
			$turnCount++;
			$HislandTurn++;
		}
		$tournament .= "</textarea><br>";
	}
	$src .= <<"END";
�ʰץȡ��ʥ��ȥ⡼�ɡ�<B>$switchStrT[$Htournament]</B><BR>
$tournament
����⡼�ɡ�<B>$switchStr[$HwarFlg]</B><BR>
���餱�ˤʤ뼫����ͭ����<B>${Hpossess}̤��</B>(0�ξ��ϡ��餱�ˤʤ�ޤ���)<BR>
�ʰץ��Х��Х�⡼�ɡ�<B>$switchStr[$HsurvFlg]</B><BR>
�ʰ׿ر�ʬ���⡼�ɡ�<B>$switchStr[$Hallyflg]</B><BR>
���ƿر���ζ����̿���ǧ�ڴѸ��⡼�ɤǻ��ȤǤ��뤫����<B>$enaStr[$Hallybbs]</B><BR>

<BR>
������̾��<B>$adminName</B><BR>
�����ԤΥ᡼�륢�ɥ쥹��<B><a href=\"mailto:$email\">$email</a></B><BR>
�Ǽ��ĥ��ɥ쥹��<B><a href=\"$bbs\">$bbs</a></B><BR>
�ۡ���ڡ����Υ��ɥ쥹��<B><a href=\"$toppage\">$toppage</a></B><BR>
�إ�פΥ��ɥ쥹��<B><a href=\"$helpDir\">$helpDir</a></B><BR>
<BR>
${AfterName}�κ������<B>$HmaxIsland</B><BR>
${AfterName}���礭����<B>${HislandSize}x${HislandSize}</B><BR>
���ޥ�����ϸ³�����<B>$HcommandMax</B><BR>
END
	my $bigcity = "";
	if($HbigcityFood){
		$bigcity = "�̾��Į��Ʊ��������";
	}else{
		$bigcity = "���ܤξ�����";
	}
	my $aidpop = "";
	if($Haidpop <= 0){
		$aidpop = "���¤ʤ�";
	}else{
		$aidpop = "$Haidpop$HunitPop";
	}
	$src .= <<"END";
$turntime
<BR>
�������ޥ�ɼ�ư���ϥ��������<B>$HgiveupTurn������</B><BR>
<BR>
<TABLE>
<TR $HbgInfoCell><TH rowspan=2>${HtagTH_}������ / ������${H_tagTH}${H_tagTH}</TH><TH rowspan=2>${HtagTH_}������� / ���翩��${H_tagTH}</TH><TH colspan=5>${HtagTH_}�Ǿ�ñ��${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}�͸�${H_tagTH}</TH><TH>${HtagTH_}����${H_tagTH}</TH><TH>${HtagTH_}�ڤο�${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='center'>$HinitialMoney$HunitMoney / $MaxMoney$HunitMoney</TD><TD align='center'>$HinitialFood$HunitFood / $MaxFood$HunitFood</TD><TD align='right'>1$HunitMoney</TD><TD align='right'>1$HunitFood</TD><TD align='right'>1$HunitPop</TD><TD align='right'>1$HunitArea</TD><TD align='right'>1$HunitTree</TD></TR>
</TABLE></B><BR>
̾���ѹ��Υ����ȡ�<B>$HcostChangeName$HunitMoney</B><BR>
�͸�1$HunitPop������ο�����������<B>${HeatenFood}x1$HunitFood</B><BR>
���ԻԤο��Ⱦ����̡�<B>${bigcity}</B><BR>
����Ϥ��ԲĤȤ���͸���<B>${aidpop}</B><BR>
��ȯ������¾��ؤι����̿������¤�ä��륿�������<B>${Hatkturn}������</B><BR>
<BR>
���蹩�졢��������ϡ�����͸��β��ܤε���ʬ����Ư���뤫�� ��<B>${HspaceEfficiency}��</B><BR>
���蹩�졢��������β�Ư���Ƥ�����͵��Ϥ�������Ͼ���� ��<B>${HspaceIncome}��</B><BR>
<BR>
�ɱһ��ߤϡ����ä�Ƨ�ޤ줿���������뤫����<B>$doStr[$HdBaseAuto]</B><BR>
���Ϥηи��ͤκ����͡�<B>$HmaxExpPoint</B><BR>
<BR>
��ͭΨ�ˤ�뾡�Ե�ǽ�Ǿ��������礬�㤨���̡�(Max�ͤ�Ķ����ȡ��ڤ�ΤƤ��ޤ�)<BR>
���<B>$HwinMoney$HunitMoney</B><BR>
����<B>$HwinFood$HunitFood</B><BR>
ʼ��<B>$HwinWeapon$HunitWeapon</B><BR>
<BR>
������̿��ǡ�̿��¹Ԥ���ºݤ�ȯư���륿�����(0�ξ��ϡ�������̵��)<BR>
����ˡ����<B>$HcomcolonyTurn</B>������<BR>
S�����ɸ���<B>$HcomSSendMonsterTurn</B>������<BR>
�����ɸ���<B>$HcomSendMonsterTurn</B>������<BR>
<BR>
END
	$HdisEarthquake *= 0.1; # �Ͽ�
	$HdisTsunami    *= 0.1; # ����
	$HdisTyphoon    *= 0.1; # ����
	$HdisMeteo      *= 0.1; # ���
	$HdisHugeMeteo  *= 0.1; # �������
	$HdisEruption   *= 0.1; # ʮ��
	$HdisFire       *= 0.1; # �к�
	$HdisMaizo      *= 0.1; # ��¢��
	$HdisAkasio     *= 0.1; # ��Ĭ
	$HdisTinka      *= 0.01;# �����ˤ����������
	$HdisVGHarvest  *= 0.1; # ��˭��
	$HdisGHarvest   *= 0.1; # ˭��
	$HdisBHarvest   *= 0.1; # ����
	$HdisAEruption  *= 0.1; # ��ʮ��
	$HdisPirate     *= 0.1; # ��±��
	$HdisTreasureS  *= 0.1; # ����
	
	$HdisFalldown   *= 0.1; # ��������
	$HdisMonster    *= 0.01;# ����
	
	$HdisPollution  *= 0.01;# ����
	$HmaxdisPollution *=0.1;# ����MAX
	$HdisCrime      *= 0.01;# �Ⱥ�
	$HdisSHugeMeteo *= 0.0001;# ����������
	
	$src .= <<"END";

�����Τκҳ��ʤ�
<TABLE>
<TR $HbgInfoCell><TH rowspan=2>${HtagTH_}�Ͽ�${H_tagTH}</TH><TH rowspan=2>${HtagTH_}����${H_tagTH}</TH><TH rowspan=2>${HtagTH_}����${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}���${H_tagTH}</TH><TH rowspan=2>${HtagTH_}�������${H_tagTH}</TH><TH rowspan=2>${HtagTH_}ʮ��${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}��Ĭ${H_tagTH}</TH><TH rowspan=2>${HtagTH_}��˭��${H_tagTH}</TH><TH rowspan=2>${HtagTH_}˭��${H_tagTH}</TH><TH rowspan=2>${HtagTH_}����${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}��±��${H_tagTH}</TH><TH rowspan=2>${HtagTH_}����${H_tagTH}</TH><TH colspan=2>${HtagTH_}��������${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell><TH>${HtagTH_}�����³��ι���${H_tagTH}</TH><TH>${HtagTH_}Ķ�������γ�Ψ${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='right'>${HdisEarthquake}%</TD><TD align='right'>${HdisTsunami}%</TD><TD align='right'>${HdisTyphoon}%</TD><TD align='right'>${HdisMeteo}%</TD><TD align='right'>${HdisHugeMeteo}%</TD><TD align='right'>${HdisEruption}%</TD><TD align='right'>${HdisAkasio}%</TD>
<TD align='right'>${HdisVGHarvest}%</TD><TD align='right'>${HdisGHarvest}%</TD><TD align='right'>${HdisBHarvest}%</TD><TD align='right'>${HdisPirate}%</TD><TD align='right'>${HdisTreasureS}%</TD>
<TD align='right'>$HdisFallBorder$HunitArea(${HdisFallBorder}Hex)</TD><TD align='right'>${HdisFalldown}%</TD></TR>
</TABLE><BR>
ñ�����Ѥ������ȯ������ҳ��ʤ�
<TABLE><TR $HbgInfoCell>
<TH>${HtagTH_}�к�${H_tagTH}</TH><TH>${HtagTH_}��¢��${H_tagTH}</TH><TH>${HtagTH_}�����ˤ��<br>������������${H_tagTH}</TH><TH>${HtagTH_}��ʮ��${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell><TD align='right'>${HdisFire}%</TD><TD align='right'>${HdisMaizo}%</TD><TD align='right'>${HdisTinka}%</TD><TD align='right'>${HdisAEruption}%</TD>
</TR>
</TABLE><BR>
����¾�κҳ�<BR>
������<B>${HdisPollution}%</B>��(�͸��������������ȯ��Ψ)<BR>
���������Ψ��<B>$HmaxdisPollution%</B><BR>
�Ⱥᡡ<B>${HdisCrime}%</B>(�͸��������������ȯ��Ψ���͸��ʳ������Ǥ⤢��ޤ�)<BR>
���蹩�죱�Ĥ�����˵�����Ф�ȯ�������Ψ��<B>${HdisSHugeMeteo}%</B>�߳�ȯ����<BR>
<BR>
ñ�����Ѥ�����β��ýи�Ψ��<B>${HdisMonster}%</B><BR>
<BR>
ñ�����Ѥ���������Ω�Ƥ��Τ顢�������νи��͡�<B>$HdisMonsterU</B><BR>
�ʾ��ʤ��ۤɳ�Ψ���⤤�����Х��Х�⡼�ɡ����ýи�Ψ=0�ξ����ͤ˴ط��ʤ��и����ʤ���<BR>
<BR>
����Ǥβ��äνи��͡�<B>${HdisSpaceMonster1}����ȯ����</B>(����ͭ��)��<B>${HdisSpaceMonster2}����ȯ����</B>(����̵��)<BR>
(Į�Ϥο�����Ƚ�ꡢ���ʤ��ۤɳ�Ψ���⤤�����ýи�Ψ=0�ξ����ͤ˴ط��ʤ��и����ʤ�)<BR>
<BR>
����Ǥβ��äνи��͡�<B>$HdisSeaMonster</B><BR>
(�西���󤳤γ�Ψ�ǳ��ο�����Ƚ�꾯�ʤ��ۤɳ�Ψ���⤤�����ýи�Ψ=0�ξ����ͤ˴ط��ʤ��и����ʤ�)<BR>
<BR>
���ýи��͸����1(���å�٥�1)��<B>$HdisMonsBorder1$HunitPop</B><BR>
END
foreach $i (0..$#HmonsterL1) {
	$src .= "$HmonsterName[$HmonsterL1[$i]] ";
}
$src .= "<BR><BR>���ýи��͸����2(���å�٥�2)��<B>$HdisMonsBorder2$HunitPop</B><BR>";
foreach $i (0..$#HmonsterL2) {
	$src .= "$HmonsterName[$HmonsterL2[$i]] ";
}
$src .= "<BR><BR>���ýи��͸����3(���å�٥�3)��<B>$HdisMonsBorder3$HunitPop</B><BR>";
foreach $i (0..$#HmonsterL3) {
	$src .= "$HmonsterName[$HmonsterL3[$i]] ";
}
$src .= "<BR><BR>���ýи��͸����4(���å�٥�4)��<B>$HdisMonsBorder4$HunitPop</B><BR>";
foreach $i (0..$#HmonsterL4) {
	$src .= "$HmonsterName[$HmonsterL4[$i]] ";
}
$src .= "<BR><BR>���ýи��͸����5(���å�٥�5)��<B>$HdisMonsBorder5$HunitPop</B><BR>";
foreach $i (0..$#HmonsterL5) {
	$src .= "$HmonsterName[$HmonsterL5[$i]] ";
}
	$src .= <<"END";

<TABLE>
<TR $HbgInfoCell>
<TH colspan=2 rowspan=2>${HtagTH_}���ä�̾��${H_tagTH}</TH>
<TH colspan=2>${HtagTH_}����${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}�и���${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}�ĳ�������${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}����Ū��ǽ��${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}min${H_tagTH}</TH><TH>${HtagTH_}max${H_tagTH}</TH></TR>
END

@Monspe = ("�äˤʤ�","­��®��(����2�⤢�뤯)","­���ȤƤ�®��(���粿�⤢�뤯������)","���������ϹŲ�",
			"����������ϹŲ�","��˹Ų�����������Ǥ�����","̿����������˰�ư(0-1��)",
			"̿����������˰�ư(���粿�⤢�뤯������)","���ϣ��إ�����̸��Ф�","����������西����MAX��");

	foreach $i (0..$#HmonsterName) {
		my $maxHP = $HmonsterBHP[$i] + $HmonsterDHP[$i] - 1;
		$maxHP++ if(!$HmonsterDHP[$i]);
		$src .= <<"END";
<TR $HbgInfoCell>
<TD align='right'><img src='$HmonsterImage[$i]'></TD>
<TH>$HmonsterName[$i]</TH>
<TD align='right'>$HmonsterBHP[$i]</TD><TD align='right'>$maxHP</TD>
<TD align='right'>$HmonsterExp[$i]</TD><TD align='right'>$HmonsterValue[$i]$HunitMoney</TD>
<TD align='right'>$Monspe[$HmonsterSpecial[$i]]</TD></TR>
END
	}
	$src .= <<"END";

</TABLE>

END

	if($mode) {
		open(OUT,">${HefileDir}/setup.html");
		print OUT jcode::sjis($src);
		close(OUT);
		chmod(0666, "${HefileDir}/setup.html");

		out("<meta HTTP-EQUIV=\"refresh\" CONTENT=\"0; URL=${efileDir}/setup.html\">");
	} else {
		out("$src");
	}
}
sub timeToString {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	localtime($_[0]);
	$mon++;
	$year += 1900;
	return "${mon}�� ${date}�� ${hour}�� ${min}ʬ";
}
#----------------------------------------------------------------------
# ���ƥ�ץ졼��
#----------------------------------------------------------------------
# ��Ͽ��
sub logHistory {
	open(HOUT, ">>${HlogdirName}/hakojima.his");
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# ȯ��
sub logDiscover {
	my($name) = @_;
	logHistory("${HtagName_}${name}${AfterName}${H_tagName}��ȯ������롣$addr");
}

# ̾�����ѹ�
sub logChangeName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}${AfterName}${H_tagName}��̾�Τ�${HtagName_}${name2}${AfterName}${H_tagName}���ѹ����롣$addr");
}

# ���������
sub logDeleteIsland {
	my($id, $name) = @_;
#	logHistory("${HtagName_}${name}��${H_tagName}��<B>�����͸��¤ˤ��</B><B><FONT COLOR=\"ff0000\">���</FONT></B>�Ȥʤ롣");
	logHistory("${HtagName_}${name}${AfterName}${H_tagName}�ˡ�����<B>ŷȳ���ߤ�</B>���äȤ����ޤ�<B><FONT COLOR=\"ff0000\">�������פ�</FONT></B>�׷���ʤ��ʤ�ޤ�����");
}

# ��ζ������(���ڥ����⡼��)
sub tempDeleteIsland {
	my($name) = @_;
	out(<<END);
${HtagBig_}${name}${AfterName}����������ޤ�����${H_tagBig}$HtempBack
END
}

# �礬���äѤ��ʾ��
sub tempNewIslandFull {
	out(<<END);
${HtagBig_}����������ޤ���${AfterName}�����դ���Ͽ�Ǥ��ޤ��󡪡�${H_tagBig}$HtempBack
END
}

# ������̾�����ʤ����
sub tempNewIslandNoName {
	out(<<END);
${HtagBig_}${AfterName}�ˤĤ���̾����ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# ������̾���������ʾ��
sub tempNewIslandBadName {
	out(<<END);
${HtagBig_}',?()<>\"\'\$'�Ȥ����äƤ��ꡢ��̵��${AfterName}�פȤ����ä��Ѥ�̾���Ϥ��ޤ��礦���<BR>
�ޤ��������ȼ����ͤˤ���ƿ̾${AfterName}�פϻ����ԲĤˤʤäƤ��ޤ���${H_tagBig}$HtempBack
END
}

# ���Ǥˤ���̾�����礬������
sub tempNewIslandAlready {
	out(<<END);
${HtagBig_}����${AfterName}�ʤ餹�Ǥ�ȯ������Ƥ��ޤ���${H_tagBig}$HtempBack
END
}

# ID����¿��������
sub tempNewIslandId {
	out(<<END);
${HtagBig_}�ֵ��ۤ�Ȣ��פλ��ͤˤ�ꤳ��ʾ�ο��������ϤǤ��ޤ���${H_tagBig}$HtempBack
END
}
# ID����¿��������
sub tempNewIslandIdB {
	out(<<END);
${HtagBig_}�ֵ��ۤ�Ȣ��פλ��ͤˤ�ꤳ��ʾ��Battle Field�Ϻ����Ǥ��ޤ���${H_tagBig}$HtempBack
END
}
# �礬�ʤ����
sub tempNotNewIsland {
	out(<<END);
${HtagBig_}����˶�����̵���١�����ʾ�κ����ϤǤ��ޤ���${H_tagBig}$HtempBack
END
}
# �ѥ���ɤ��ʤ����
sub tempNewIslandNoPassword {
	out(<<END);
${HtagBig_}�ѥ���ɤ�ɬ�פǤ���${H_tagBig}$HtempBack
END
}

# ���ȯ�����ޤ���!!
sub tempNewIslandHead {
	out(<<END);
<CENTER>
${HtagBig_}${AfterName}��ȯ�����ޤ�������${H_tagBig}<BR>
${HtagBig_}${HtagName_}��${HcurrentName}${AfterName}��${H_tagName}��̿̾���ޤ���${H_tagBig}<BR>
${HtagBig_}����³��<a href="${HbaseDir}/profile.cgi?profile=$_[0]&mode=edit">�ץ�ե�������Ͽ</a>�򤪴ꤤ���ޤ���(Ǥ��)${H_tagBig}��$HtempBack<BR>
</CENTER>
END
}

# ̾���ѹ�����
sub tempChangeNothing {
	out(<<END);
${HtagBig_}̾�����ѥ���ɤȤ�˶���Ǥ�${H_tagBig}$HtempBack
END
}

# ̾���ѹ����­�ꤺ
sub tempChangeNoMoney {
	out(<<END);
${HtagBig_}�����­�Τ����ѹ��Ǥ��ޤ���${H_tagBig}$HtempBack
END
}

# ̾���ѹ�����
sub tempChange {
	out(<<END);
${HtagBig_}�ѹ���λ���ޤ���${H_tagBig}$HtempBack
END
}
# �ץ쥼���
sub logPresent {
	my($id, $name, $log) = @_;
	logHistory("${HtagName_}${name}${AfterName}${H_tagName}$log") if ($log ne '');
}

1;
