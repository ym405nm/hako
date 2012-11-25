#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 新規作成モジュール
# 使用条件、使用方法等は、qhako-readme.txtファイルを参照
#----------------------------------------------------------------------
# 究想の箱庭(ver5.53d)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 島の新規作成モード
#----------------------------------------------------------------------
sub newIslandMain {
	my($mode) = @_;

	# 島がいっぱいでないかチェック(BattleField作成はチェックしない)
	if(($HislandNumber >= $HmaxIsland + $HbattleNumber) && (!$mode)) {
		unlock();
		tempHeader();
		tempNewIslandFull();
		return;
	}

	# 名前があるかチェック
	if($HcurrentName eq '') {
		unlock();
		tempHeader();
		tempNewIslandNoName();
		return;
	}

	# 名前が正当かチェック
	if(($HcurrentName =~ /[\\,\?\(\)\<\>\$]|^無人$/) || ($HcurrentName =~ /[\\,\?\(\)\<\>\$]|^匿名$/)) {
		# 使えない名前
		unlock();
		tempHeader();
		tempNewIslandBadName();
		return;
	}

	# 名前の重複チェック
	if(nameToNumber($HcurrentName) != -1) {
		# すでに発見ずみ
		unlock();
		tempHeader();
		tempNewIslandAlready();
		return;
	}
	
	# passwordの存在判定
	if($HinputPassword eq '') {
		# password無し
		unlock();
		tempHeader();
		tempNewIslandNoPassword();
		return;
	}

	# 確認用パスワード
	if($HinputPassword2 ne $HinputPassword) {
		# password間違い
		unlock();
		tempHeader();
		tempWrongPassword();
		return;
	}

	# 新しい島の番号を決める
	$HcurrentNumber = $HislandNumber;
	$HislandNumber++;
	$Hislands[$HcurrentNumber] = makeNewIsland($mode);
	my($island) = $Hislands[$HcurrentNumber];

	# 島のＩＤの再利用
	my($i,@logid);
	# ログのIDをサーチ
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
		# BattleFieldのとき
		$si = 91;
		$ei = 100;
	}else{
		$si = 1;
		$ei = 91;
	}

	for($i = $si;$i < $ei;$i++) {
		if(($HidToNumber{$i} eq '') && (!$logid[$i])) {
			unlink("$HprofileDir/profile${i}.dat"); # プロファイルデータ削除
			$nextid = $i;
			last;
		}
	}
	# ID数チェック
	if($nextid >= $ei) {
		# 仕様により新規参入不可
		unlock();
		tempHeader();
		if($mode){
			tempNewIslandIdB();
		}else{
			tempNewIslandId();
		}
		return;
	}
	
	# 管理人預かりモードだったら強制解除
	preDeleteMainP(0);

	# 各種の値を設定
	if($mode){
		# BattleFieldのとき
		$island->{'absent'} = 0;
		$island->{'comment'} = '(Battle Field)';
		$island->{'evil'} = 200;
	}else{
		#初期登録時の「資産繰り」回数
		$island->{'absent'} = $HgiveupTurn - 3;
		$island->{'comment'} = '(未登録)';
		if($Htournament){
			# 簡易トーナメント
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

	# 無人島を探して位置を確定する。
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

	# 人口その他算出
	estimateM($HcurrentNumber);

	# データ書き出し
	if(!writeIslandsFile($island->{'id'}, 0)) {
		unlock();
		tempHeader();
		tempFailWrite();
		return;
	}

	logDiscover($HcurrentName); # ログ

	if(!$mode){
		# BattleField以外
		$HcurrentID = $nextid;
		$HmainMode = 'owner';
		# COOKIE出力
		cookieOutput();
	}
	# 開放
	unlock();

	# 発見画面
	tempHeader();
	tempNewIslandHead($island->{'id'}); # 発見しました!!
	tempNavi();
	islandInfo(); # 島の情報
	islandMap(2); # 島の地図、特殊モード
}

# 新しい島を作成する
sub makeNewIsland {
	# 地形を作る
	my($land, $landValue, $land2, $landValue2) = makeNewLand($_[0]);
	
	# 初期コマンドを生成
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

	# 初期掲示板を作成
	my(@lbbs);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$lbbs[$i] = "0<<0>>";
	}

	my($StartMoney) = $HinitialMoney + $HislandTurn * 3;
	$StartMoney *= 2 if($HwarFlg);
	$HspacePrize = ($HspacePrize) ? 512 : 0;

	my($order) = ($HwarFlg) ? 0 : 128;

	# 島にして返す
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

# 新しい島の地形を作成する
sub makeNewLand {
	my($mode) = @_;

	# 基本形を作成
	my(@land, @landValue, @land2, @landValue2, $x, $y, $i, $r);

	# 海に初期化
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
		# 全て海のとき
		return (\@land, \@landValue, \@land2, \@landValue2);
	}elsif($mode == 3){
		# 平地
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
			# ランダム座標
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
		# 都市
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
			# ランダム座標
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
		# 荒地を配置 49
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
		# 荒地を配置 25
		for($y = $center - 2; $y < $center + 3; $y++) {
			for($x = $center - 2; $x < $center + 3; $x++) {
				$land[$x][$y] = $HlandWaste;
			}
		}
		$area = 25;
	}

	# 範囲内に陸地を増殖
	for($i = 0; $i < $rct; $i++) {
		# ランダム座標
		$x = random($range) + $center - $range2;
		$y = random($range) + $center - $range2;
		if(countAroundM(\@land, $x, $y, $HlandSea, 7) != 7){
			# 周りに陸地がある場合、浅瀬にする
			# 浅瀬は荒地にする
			# 荒地は平地にする
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

	# 森を作る
	my($count) = 0;
	while($count < 4) {
		# ランダム座標
		$x = random(4) + $center - 1;
		$y = random(4) + $center - 1;
		if(!(($land[$x][$y] == $HlandSea) && ($HinitialArea == $area)) &&
			($land[$x][$y] != $HlandForest)) {
			$land[$x][$y] = $HlandForest;
			$landValue[$x][$y] = 10;
			$count++;
		}
	}

	# 町を作る
	$count = 0;
	while($count < 2) {
		# ランダム座標
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

	# 山を作る
	$count = 0;
	while($count < 1) {
		# ランダム座標
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

	# 基地を作る
	$count = 0;
	if($HinitialBase > 3){
		$range = 6;
	}else{
		$range = 4;
	}
	while($count < $HinitialBase) {
		# ランダム座標
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

	# 農場を作る
	$count = 0;
	while($count < 1) {
		# ランダム座標
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
# 情報変更モード
#----------------------------------------------------------------------
# メイン
sub changeMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($flag) = 0;

	# パスワードチェック
	if(checkSpecialPassword($HoldPassword)) {
		# 特殊パスワード
		if($HcurrentName =~ /^無人$/) {
			# 島削除モード
			deleteIsland();
			return;
		} else {
			$island->{'money'} = $MaxMoney;
			$island->{'food'} = $MaxFood;
		}
	} elsif(!checkPassword($island->{'password'},$HoldPassword)) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	# 確認用パスワード
	if($HinputPassword2 ne $HinputPassword) {
		# password間違い
		unlock();
		tempWrongPassword();
		return;
	}

	if($HcurrentName ne '') {
		# 名前変更の場合
		# 名前が正当かチェック
		if(($HcurrentName =~ /[\\,\?\(\)\<\>\$]|^無人$/) || ($HcurrentName =~ /[\\,\?\(\)\<\>\$]|^匿名$/)) {
			# 使えない名前
			unlock();
			tempNewIslandBadName();
			return;
		}

		# 名前の重複チェック
		if(nameToNumber($HcurrentName) != -1) {
			# すでに発見ずみ
			unlock();
			tempNewIslandAlready();
			return;
		}

		if($island->{'money'} < $HcostChangeName) {
			# 金が足りない
			unlock();
			tempChangeNoMoney();
			return;
		}

		# 代金
		unless(checkSpecialPassword($HoldPassword)) {
			$island->{'money'} -= $HcostChangeName;
		}

		# 名前を変更
		logChangeName($island->{'name'}, $HcurrentName);
		$island->{'name'} = $HcurrentName;
		$flag = 1;
	}

	if($HcurrentOwnerName ne '') {
		# オーナー変更の場合
		$island->{'ownername'} = htmlEscape($HcurrentOwnerName);
		$flag = 1;
	}

	# password変更の場合
	if($HinputPassword ne '') {
		# パスワードを変更
		$island->{'password'} = encode($HinputPassword);
		$flag = 1;
	}

	if(($flag == 0) && !checkSpecialPassword($HoldPassword)) {
		# 何も変更されていない
		unlock();
		tempChangeNothing();
		return;
	}

	# データ書き出し
	if(!writeIslandsFile($HcurrentID, 1)) {
		unlock();
		tempFailWrite();
		return;
	}
	unlock();

	# 変更成功
	tempChange();
}

# 島の強制削除
sub deleteIsland {
	my($island) = $Hislands[$HidToNumber{$HcurrentID}];

	# 島テーブルの操作
	$island->{'pop'} = -100;

	# 人口順にソート
	my($flag, $i, $tmp);
	my @idx = (0..$#Hislands);
	@idx = sort { $Hislands[$b]->{'pop'} <=> $Hislands[$a]->{'pop'} || $a <=> $b } @idx;
	@Hislands = @Hislands[@idx];

	logDeleteIsland($tmpid, $island->{'name'});

	# メインデータの操作
	$HislandNumber--;
	OceanMente($island->{'id'});
	writeIslandsFile($HcurrentID);
	
	# データ書き出し
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

# 人口その他の値を算出 簡易版
sub estimateM {
	my($number) = $_[0];
	my($pop, $popsea, $area, $farm, $MissileK) = (0, 0, 0, 0, 0);
	# 地形を取得
	my($island) = $Hislands[$number];
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};

	# 数える
	my($x, $y, $kind, $value);
	for($y = 0; $y < $HislandSize; $y++) {
		for($x = 0; $x < $HislandSize; $x++) {
			$kind = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			
			$area++ if($HseaChk[$kind] == 0); # 海系でないとき
			if($kind == $HlandTown) {
				# 町
				$value = 200 if($value > 200);
				$pop += $value;
			} elsif($kind == $HlandFarm) {
				# 農場
				$farm += $value;
			} elsif(($kind == $HlandBase) || ($kind == $HlandSbase)) {
				# ミサイル発射数
				$MissileK += expToLevel($kind, $value);
			}
		}
	}
	# 代入
	$island->{'pop'}   = $pop;
	$island->{'farm'}  = $farm;
	$island->{'area'}  = $area;
	$island->{'MissileK'}   = $MissileK;
}


# 範囲内の地形を数える 簡易版
sub countAroundM {
	my($land, $x, $y, $kind, $range) = @_;
	my($i, $sx, $sy);
	my $count = 0;
	for($i = 0; $i < $range; $i++) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];

		# 行による位置調整
		$sx-- if (!($sy % 2) && ($y % 2));

		if(($sx < 0) || ($sx >= $HislandSize) || ($sy < 0) || ($sy >= $HislandSize)) {
			# 範囲外の場合 海なら加算
			$count++ if($kind == $HlandSea);
		} else {
			# 範囲内の場合
			$count++ if($land->[$sx][$sy] == $kind);
		}
	}
	return $count;
}

#----------------------------------------------------------------------
# 歴代人口記録 neo_otacky氏が作成
#----------------------------------------------------------------------
# メイン
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
	# 開放
	unlock();

	out(<<END);
<CENTER>$HtempBack</CENTER><BR>
<center>
<H1>歴代最多人口記録</H1>
<table border=0 width=50%><tr>
<TH $HbgTitleCell align=center nowrap=nowrap>${HtagTH_}順位${H_tagTH}</TH>
<TH $HbgTitleCell align=center nowrap=nowrap>${HtagTH_}${AfterName}名${H_tagTH}</TH>
<TH $HbgTitleCell align=center nowrap=nowrap>${HtagTH_}人口${H_tagTH}</TH>
<TH $HbgTitleCell align=center nowrap=nowrap>${HtagTH_}ターン${H_tagTH}</TH>
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
</tr><tr><TH colspan=4>データがありません！</TH>
END
	}
	out(<<END);
</tr></table></center>
<div align=right>Scripted By neo_otacky</div>
END
}

#----------------------------------------------------------------------
# 管理人モード neo_otacky氏が作成したのを究想用に改変
#----------------------------------------------------------------------

# BattleField作成モード
sub bfieldMain {
	if (!$HbfieldMode) {
		unlock();
		tempHeader();
		# パスワードチェック
		if(checkPassword($HspecialPassword, $HdefaultPassword)) {
			# 特殊パスワード
			tempBfieldPage();
		} else {
			# password間違い
			tempWrongPassword();
		}
	} else {
		# BattleField作成
		newIslandMain($HbfieldMode);
	}
}

# BattleField作成モードのトップページ
sub tempBfieldPage {
	out(<<END);
$HtempBack<hr>
<H1>Battle Fieldを作成</H1>
<FORM action="$HthisFile" method="POST">
どんなBattleFieldにしますか？<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>$AfterName<BR>
オーナー名(省略可)<br>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
パスワードは？<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
念のためパスワードをもう一回<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>
作成するBattle Fieldの地形のパターンを選択してください。<BR>
<SELECT NAME="LBFIELD">
<OPTION VALUE="1" SELECTED>中心が島
<OPTION VALUE="2">全て海
<OPTION VALUE="3">平地だらけの島
<OPTION VALUE="4">都市だらけの島
</SELECT><BR><BR>
<INPUT TYPE="hidden" VALUE="${\htmlEscape($HdefaultPassword)}" NAME="Bfield">
<INPUT TYPE="submit" VALUE="Battle Field作成" NAME="BfieldButton">
</FORM>
END
}

# BattleField作成完了
sub tempBfieldOK {
	out(<<END);
${HtagBig_}$_[0]${AfterName}のBattle Field設定を変更しました。<br>$_[1]${H_tagBig}$HtempBack
END
}

# BattleField作成失敗
sub tempBfieldNG {
	out(<<END);
${HtagBig_}Battle Fieldの設定エラー($_[0])。${H_tagBig}$HtempBack
END
}

# 管理人によるプレゼントモード
sub presentMain {
	if (!$HpresentMode) {
		# 開放
		unlock();

		# テンプレート出力
		tempPresentPage();
	} else {
		# パスワードチェック
		if(checkPassword($HspecialPassword, $HoldPassword)) {
			# 特殊パスワード

			if(!$HpresentMoney && !$HpresentFood) {
				# 金も食料もない
				tempPresentEmpty();
				unlock();
				return;
			}

			# idから島を取得
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

			# データ書き出し
			if(!writeIslandsFile($HcurrentID, 1)) {
				unlock();
				tempFailWrite();
				return;
			}
			unlock();
			# 変更成功
			tempPresentOK($name);
		} else {
			# password間違い
			unlock();
			tempWrongPassword();
			return;
		}
	}
}

# プレゼントモードのトップページ
sub tempPresentPage {
	out(<<END);
$HtempBack<hr>
<H1>参加${AfterName}にプレゼントを贈る</H1>
<UL>
<LI>「発見の記録」にログが残るイベントとして援助を行うことができます。
<LI>表示されたフォームに必要な値やメッセージを入力して、パスワードに「特殊パスワード」を入れ、「プレゼントを贈る」ボタンを押せばプレゼントできます。
<LI>ログにはHTMLタグも使えますが、間違ったログの削除ができませんので、慎重に入力してください。あらかじめブラウザで表示テストを行っておいたほうがいいでしょう。「発見の記録」に変なログが残ると、ちょっと恥ずかしいです。
<LI>資金や食料の保有量が制限値を超えることやマイナスにはならないように切り捨てています。バグ対策ですのでご了承ください。
</UL><BR>
<FORM action="$HthisFile" method="POST">
<B>プレゼントを受け取る${AfterName}は？</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR><BR>
<B>プレゼントの内容は？(マイナス値も可能)</B><BR>
<INPUT TYPE="text" NAME="PRESENTMONEY" VALUE="0" SIZE=16 MAXLENGTH=16>$HunitMoney<BR>
<INPUT TYPE="text" NAME="PRESENTFOOD"  VALUE="0" SIZE=16 MAXLENGTH=16>$HunitFood<BR>
<BR>
<B>ログメッセージは？(省略可能。先頭に${AfterName}名が挿入されます)</B><BR>
○○${AfterName}<INPUT TYPE="text" NAME="PRESENTLOG"  VALUE="" SIZE=128 MAXLENGTH=256><BR>
<BR>
<B>パスワードは？</B><BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="プレゼントを贈る" NAME="PresentButton"><BR>
</FORM>
END
}

# プレゼント完了
sub tempPresentOK {
	out(<<END);
${HtagBig_}$_[0]${AfterName}にプレゼントを贈りました${H_tagBig}$HtempBack
END
}

# プレゼント内容がおかしい
sub tempPresentEmpty {
	out(<<END);
${HtagBig_}プレゼントの内容がおかしいようです${H_tagBig}$HtempBack
END
}

# 管理人による制裁モード
sub punishMain {
	if(checkPassword($HspecialPassword, $HdefaultPassword)) {
		# 特殊パスワード
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

		# テンプレート出力
		tempPunishPage();

	} else {
		# パスワードが一致しなければトップページへ
		unlock();

		# テンプレート出力
		tempTopPage();
	}
}

# 制裁モードのトップページ
sub tempPunishPage {
	my(@punishName) =(
		 'なし',
		 '地震（座標指定）',
		 '津波',
		 '怪獣（人口条件クリア時のみ）',
		 '地盤沈下（面積条件クリア時のみ）',
		 '台風',
		 '巨大隕石（座標指定）',
		 '隕石',
		 '噴火（座標指定）',
		 '船を強制退避',
		 '究想いのら降臨（座標指定）',
		 '火災（座標指定）');
	out(<<END);
$HtempBack<hr>
<H1>参加${AfterName}に制裁を加える</H1>
制裁は指定した自然災害を必ず発生させます。例えば「Ａ${AfterName}に地盤沈下」という指示を出すと次のターンで地盤沈下します。
<br>この改造は、「荒らしというほどではないが箱庭の雰囲気を悪化させるような行為をするプレイヤー」や、
<br>「管理人の決めたローカルルールに違反していて改善の見込みがないプレイヤー」などに自然災害を発生させる物らしいです。
<br>「実にいい位置に巨大隕石」とか「運悪く地盤沈下」などが起きれば、あまり揉めずに問題${AfterName}は弱体化します。
<br>「ルールに違反した」と思う前に、「そのルールは誰もが読める場所に書いてあるか？」を確認しましょう。
<br>制裁を加えるのはたやすいことですが、本当に管理人としての立場で行っているか考えましょう。
<br>制裁を加えなければならないほど被害が大きいか考えましょう。他の${AfterName}に迷惑を掛けているといってもただのゲームなのですから。
<br><FONT COLOR="red">制裁の存在は極秘にしましょう。</FONT>制裁が明らかになると他のプレイヤーとの信頼関係も崩れます。
<br><br>究想の箱庭改造者は、この機能を推奨していません。
<br>問題がある参加者とは掲示板などで話し合いで解決すべきです。場合によっては強制的にやめて頂くのも
<br>仕方がないとは考えていますが、こういう内容で問題がある参加者を弱体化させるはどうかと思っています。
<br>全ての参加者はたとえ不正なことを行っていたとしてもゲームでは公平であるべきだと思っています。
<br>
<br>船を強制退避は、選択した${AfterName}にいる無所属以外の船を全て帰還させる処理です。
<br>究想いのら降臨は、選択した${AfterName}に究想のいのらを出現させます。
<br>火災は、燃える地形を選択した場合のみ実行されます。
</DL>

<FORM name="lcForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="${\htmlEscape($HdefaultPassword)}" NAME="Punish">
<B>制裁を加える${AfterName}は？</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<INPUT TYPE="button" VALUE="マップを開く" onclick="printIsland();">
<BR><BR>
<B>座標は？（座標指定できる制裁でのみ有効）</B><BR>
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
<B>制裁の内容は？</B><BR>
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
<INPUT TYPE="submit" VALUE="制裁を加える" NAME="PunishButton"><BR>
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
		out("<HR><TABLE BORDER><TR><TH $HbgTitleCell>${AfterName}名</TH><TH $HbgTitleCell>制裁内容</TH><TH $HbgTitleCell>座標</TH></TR>");
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

# 管理人による地形変更モード
sub lchangeMain {
	# 特殊パスワード
	if(checkPassword($HspecialPassword, $HdefaultPassword)) {
		
		# idから島を取得
		$HcurrentNumber = $HidToNumber{$HcurrentID};
		my($island) = $Hislands[$HcurrentNumber];
		if ($HlchangeMode) {

			# 地形の値の整合性をチェック
			if(!landCheck($HlchangeKIND, $HlchangeVALUE)) {
				tempBadValue();
				unlock();
				return;
			}

			$island->{'land'}->[$HcommandX][$HcommandY] = $HlchangeKIND;
			$island->{'landValue'}->[$HcommandX][$HcommandY] = $HlchangeVALUE;
			$island->{'land2'}->[$HcommandX][$HcommandY] = $HlandSea;
			$island->{'landValue2'}->[$HcommandX][$HcommandY] = 0;

			# データ書き出し
			if(!writeIslandsFile($HcurrentID, 2)) {
				unlock();
				tempFailWrite();
				return;
			}
			unlock();
			# 変更成功
			tempLchangeOK($island->{'name'});
		}
		unlock();
		# テンプレート出力
		tempLchangePage();
	} else {
		# パスワードが一致しなければトップページへ
		unlock();
		require('hako-top.cgi');
		# テンプレート出力
		tempTopPage();
	}
}

# 地形変更モードのトップページ
sub tempLchangePage {
	out(<<END);
$HtempBack<hr>
<H1>参加${AfterName}の地形データを変更する</H1>
基本的に、<b>正常に動作しなくなる恐れ</b>がありますので<B>${AfterName}のデータを書き換えないで下さい。</B><BR>
<b>必ず書き換える前に箱庭データのバックアップを行ってください。</b><BR>
バグなどで地形がおかしくなった場合にのみ応急処置として地形を変更してください。<BR>
知識が無い場合は海の０か１(浅瀬)、平地の０、荒地の０のどれかのみを使用してください。<BR>
間違って変更をした場合になんらかの問題が発生しても一切の責任はとれません。<BR>
「地形」に対して「地形の値」が適切であるかどうかをチェック(手抜き)をしていますので、注意してください。<BR>
<TABLE><TR><TD>
END
	if($HcurrentID != 0){
		islandMap(1);
	}else{
		out("地図表示するためには、<br>一度${AfterName}を選びマップを開いてください。");
	}
	$HtargetList = getIslandList($HcurrentID);
	out(<<END);
</TD><TD valign=top>
<FORM name="lcForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="${\htmlEscape($HdefaultPassword)}" NAME="Lchange">
<B>地形を変更する${AfterName}</B>(ID=$HcurrentID)<BR>
<SELECT NAME="ISLANDID">
$HtargetList
</SELECT><BR>
<INPUT TYPE="submit" VALUE="マップを開く" NAME="LchangeButtonM"><BR>
<BR><BR>
<B>座標は？</B><BR>
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
	out("</SELECT><B>)</B><BR><BR><B>地形は？</B><BR><SELECT NAME=\"LCHANGEKIND\">");
	@lcland = ("海","荒地","平地","町系","森","農場","工場","ミサイル基地","防衛施設","山","怪獣","海底基地","海底油田","記念碑","海底記念碑",
				"ハリボテ","汚染","スラム街","商業ビル","精製場","銀行","スタジアム","遊園地","カジノ","公園","学校","ドーム","空港",
				"消防署","転移装置","動物園","大都市","博覧会","巨大都市","巨大ビル","巨大工場","巨大農場","商業都市","超巨大都市","デストラップ","風車","マイホーム",
				"転移先装置","港","防波堤","警察署","病院","トランプ","花","土管","富士山","海賊船","海獣掃討艇","イージス艦","海底探査船","幽霊船",
				"宝船","小型漁船","中型漁船","大型漁船","翼竜","流氷","夫婦岩","豪華客船","海風船");
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
<B>地形の値は？</B><BR>
<INPUT TYPE="text" SIZE=6 NAME="LCHANGEVALUE" VALUE="$HlchangeVALUE"><BR>
(通常0-200)<BR>
(ミ基地0-250)<BR>
(怪獣1-3199)<BR>
(船系0-59999)<BR>
<BR>
<INPUT TYPE="submit" VALUE="変更する" NAME="LchangeButton"><BR>
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

# 地形変更完了
sub tempLchangeOK {
	out(<<END);
${HtagBig_}$_[0]${AfterName}の地形を変更しました${H_tagBig}<HR>
END
}

# 地形の値がおかしい
sub tempBadValue {
	out(<<END);
${HtagBig_}地形の値がおかしいようです${H_tagBig}$HtempBack
END
}

# 地形の値をチェック(手抜き、特に後半)
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

# 管理人によるあずかりモード
sub preDeleteMain {
	if(checkPassword($HspecialPassword, $HdefaultPassword)) {
		# 特殊パスワード
		preDeleteMainP(1) if($HpreDeleteMode);
		unlock();
		# テンプレート出力
		tempPdeleteMain();
	} else {
		# パスワードが一致しなければトップページへ
		require('hako-top.cgi');
		unlock();
		# テンプレート出力
		tempTopPage();
	}
}

# 管理人によるあずかりモード処理
sub preDeleteMainP {
	my($mode) = @_;
#	HdebugOut("preDeleteMainP　$mode");
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
		# Battle Fieldで追加モードのときは無効
		tempPreDelete2($Hislands[$HidToNumber{$HcurrentID}]->{'name'}) if($mode);
	}else{
		@HpreDeleteID = @newID;
		push(@HpreDeleteID, $HcurrentID) if(!$flag);
		# データ書き出し
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
# あずかりモードのトップページ
sub tempPdeleteMain {
	out(<<END);
<CENTER>$HtempBack</CENTER>
<H1>参加${AfterName}を管理人あずかりにする</H1>

<DL>
<DT>・あずかりになった${AfterName}は、ターン処理(収入処理・コマンド処理・成長・災害等)されなくなります。</DT>
<DT>・賞関係は処理されますし、他の${AfterName}からの攻撃はすべて受けつけてしまいます。</DT>
<DT>・Battle Fieldは、あずかり設定にすることができません。</DT>
<!--
<DT>・あずかり中の${AfterName}が「放棄」もしくは「強制削除」された場合、処理の都合上
あずかりのＩＤデータが次のあずかり処理を行うまでそのまま残りますが、利用者(管理人)は考慮する必要はありません。</DT>
-->
</DT>

</DL>

<FORM name="pdForm" action="$HthisFile" method="POST">
<INPUT TYPE="hidden" VALUE="${\htmlEscape($HdefaultPassword)}" NAME="Pdelete">
<B>管理人あずかりにする${AfterName}は？</B><BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
<INPUT TYPE="submit" VALUE="設定・解除" NAME="PdeleteButton"><BR>
</FORM>
<TABLE BORDER><TR><TH>あずかり中の${AfterName}</TH></TR>
END

	if($HpreDeleteID[0] eq '') {
		out("<TR><TH>管理人あずかりの${AfterName}はありません！</TH></TR>");
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

# 管理人あずかり設定
sub tempPreDelete {
	out(<<END);
${HtagBig_}$_[0]${AfterName}を管理人あずかりにしました${H_tagBig}
<HR>
END
}

# 管理人あずかり設定無効
sub tempPreDelete2 {
	out(<<END);
${HtagBig_}$_[0]${AfterName}は管理人あずかりにできません${H_tagBig}
<HR>
END
}

# 管理人あずかり解除
sub tempPreDeleteEnd {
	my($name) = @_;
	out(<<END);
${HtagBig_}$_[0]${AfterName}の管理人あずかりを解除しました${H_tagBig}
<HR>
END
}

# 管理人による各種島データ変更モード
sub ichangeMain {
	if(checkPassword($HspecialPassword, $HdefaultPassword)) {
		# 特殊パスワード
		ichangeMainP() if($HichangeMode);
		unlock();
		# テンプレート出力
		tempIchangePage();
	} else {
		# パスワードが一致しなければトップページへ
		require('hako-top.cgi');
		unlock();
		# テンプレート出力
		tempTopPage();
	}
}
# 管理人による各種島データ変更モード処理
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
	# データ書き出し
	if(!writeIslandsFile($HcurrentID, 1)) {
		unlock();
		tempFailWrite();
		return;
	}
}
# 管理人による各種島データ変更モード処理
sub tempIchangePage {
	my($mode) = @_;
	out(<<END);
<span class='attention'>※　必ずバックアップをしてから行ってください。データを直接修正するので危険です！</span>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>${HtagTH_}順位${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}資金${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}食料${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}兵器${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}国連等${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}宇宙賞${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}所属${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}変更${H_tagTH}</TH>
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
<TD><INPUT TYPE="submit" VALUE="変更" NAME="IchangeButton"></TD>
</FORM>
</TR>
END
	}
	out(<<END);
</TABLE>
1${AfterName}ごとの修正しか出来ません。<br>
国連等は、ミサイル基地がない${AfterName}の値を0にすると、国連保護化になります。<br>
また、10000以上にすると黄金期になります。<br>
宇宙賞は、与えることしか出来ません。<br>
END
}

# ブラウザ情報を取得
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

# 初期設定確認
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
		# flexTime処理の場合は表示する必要なし
	}else{
		my $sec = ($HunitTime % 60);
		$sec = ($sec ? "$sec秒" : '');
		my $min = ($HunitTime % 3600);
		$min = ($min ? "$min分" : '');
		my $hour = int($HunitTime / 3600);
		$hour = ($hour ? "$hour時間" : '');
		$turntime = "<BR>1ターンが何秒か　<B>${HunitTime}秒 ( $hour$min$sec )</B><BR>";
	}
	my @switchStr = ('OFF', 'ON');
	my @switchStrT = ('OFF', 'ON', "ON(怪獣付き)");
	my @enaStr  = ('できない', 'できる');
	my @doStr  = ('しない', 'する');
	
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
<A HREF="http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html">箱庭諸島スクリプト配布元</A>
</DIV>
<HR>
END

	$src .= <<"END";
<CENTER>$HtempBack</CENTER>
<DIV ID='setupValue'>
<H1>究想の箱庭　設定一覧</H1>
END

	$src .= <<"END" if($admin);
--- 管理人用　設定確認データ --- <BR><BR>

※　設定を変更した場合は、必ず以下のリンクを開き参加者用の再生成を行ってください。<BR>
<A HREF="$HbaseDir/hako-main.cgi?SetupV=0" target="_blank">参加者用の再生成</a><BR>
<BR>
デバッグモード　<B>$switchStr[$Hdebug]</B><BR>
設置ディレクトリ　<B>$HbaseDir</B><BR>
画像ディレクトリ　<B>$imageDir</B><BR>
<BR>
ログファイル保持ターン数　<B>$HlogMaxターン</B><BR>
「最近の出来事」に表示するログのターン数　<B>$HtopLogTurnターン</B><BR>
バックアップを何ターンおきに取るか　<B>$HbackupTurnターン</B><BR>
バックアップを何回分残すか　<B>$HbackupTimes回分</B><BR>
発見ログ保持行数　<B>$HhistoryMax行</B><BR>
天気ログ保持行数　<B>$HWeatherMax行</B><BR>
<BR>
IP表示　<B>$switchStr[$Hlipdisp]</B><BR>
<BR>
ローカル掲示版のパスワード認証　<B>$switchStr[$HlbbsAuth]</B><BR>
　観光客のローカル掲示版匿名発言機能　<B>$switchStr[$HlbbsAnon]</B><BR>
　発言に発言者の名前表示　<B>$switchStr[$HlbbsSpeaker]</B><BR>
<BR>
直開発モードのときのパスワード　<B>$Hurlownermode</B><BR>
　→　（　hako-main.cgi?島PASSWORD=****&${Hurlownermode}=島ＩＤ<BR>

<BR>
--- 参加者用　設定確認データ --- <BR><BR>
END
	my $tournament = "";
	if($Htournament){
#		$tournament  = "　予選後通過島数　<B>$HfightMem$AfterName</B><BR>";
#		$tournament .= "　予選期間ターン数　<B>$HyosenTurn$AfterName</B><BR>";
#		$tournament .= "　開発期間ターン数　<B>$HdevelopeTurn$AfterName</B><BR>";
#		$HfightTurn .= "　戦闘期間ターン数　<B>$HdevelopeTurn$AfterName</B><BR>";
		
		# 簡易トーナメント　ターン更新時間早見表
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
<br><INPUT TYPE="button" VALUE="クリップボードにコピー" onClick="textcopy(searchID('ALIST').value)"><br>
<textarea NAME="ALIST" cols="100" rows="5">
END
		my $fturn = 0;
		my $islandNumber = $HislandNumber;
		$HfightTurn = $HfinalTurn if($islandNumber <= 2);
		while($HislandTurn >= $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn){
			$fturn += $HdevelopeTurn + $HfightTurn;
		}
		$tournament .= "ターン\t$AfterName数\t進行状態\t更新時間\n";
		my $islandFightMode = $HislandFightMode;
		my $turnCount = $HislandTurnCount;
		while($islandNumber > 1){
			if($HislandTurn < $HyosenTurn){
				# 予選
				$islandFightMode = 1;
				$HislandLastTime += 3600 * $HtmTime1[($turnCount % ($#HtmTime1 + 1))];
				$timeString = timeToString($HislandLastTime);
				$tournament .= "$HislandTurn\t$islandNumber\t予選\t$timeString\n";
			}elsif($HislandTurn < $HyosenTurn + $HdevelopeTurn + $fturn){
				# 開発
				$islandNumber = $HfightMem if(($islandFightMode == 1) && ($islandNumber > $HfightMem));
				$islandFightMode = 2;
				$HislandLastTime += 3600 * $HtmTime2[($turnCount % ($#HtmTime2 + 1))];
				$timeString = timeToString($HislandLastTime);
				$HfightTurn = $HfinalTurn if($islandNumber <= 2);
				$tournament .= "$HislandTurn\t$islandNumber\t開発\t$timeString\n";
			}elsif($HislandTurn < $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn){
				# 戦闘
				$turnCount = 0 if($islandFightMode != 3);
				$HislandLastTime += $HinterTime if($islandFightMode != 3 && $islandNumber > 2);
				$islandFightMode = 3;
				$HislandLastTime += 3600 * $HtmTime3[($turnCount % ($#HtmTime3 + 1))];
				$timeString = timeToString($HislandLastTime);
				$tournament .= "$HislandTurn\t$islandNumber\t戦闘♪\t$timeString\n";
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
				$tournament .= "$HislandTurn\t$islandNumber\t開発\t$timeString\n" if($islandNumber > 1);
			}
			$turnCount++;
			$HislandTurn++;
		}
		$tournament .= "</textarea><br>";
	}
	$src .= <<"END";
簡易トーナメントモード　<B>$switchStrT[$Htournament]</B><BR>
$tournament
戦争モード　<B>$switchStr[$HwarFlg]</B><BR>
　負けになる自島占有数　<B>${Hpossess}未満</B>(0の場合は、負けになりません)<BR>
簡易サバイバルモード　<B>$switchStr[$HsurvFlg]</B><BR>
簡易陣営分けモード　<B>$switchStr[$Hallyflg]</B><BR>
　各陣営内の極秘通信を認証観光モードで参照できるか？　<B>$enaStr[$Hallybbs]</B><BR>

<BR>
管理者名　<B>$adminName</B><BR>
管理者のメールアドレス　<B><a href=\"mailto:$email\">$email</a></B><BR>
掲示板アドレス　<B><a href=\"$bbs\">$bbs</a></B><BR>
ホームページのアドレス　<B><a href=\"$toppage\">$toppage</a></B><BR>
ヘルプのアドレス　<B><a href=\"$helpDir\">$helpDir</a></B><BR>
<BR>
${AfterName}の最大数　<B>$HmaxIsland</B><BR>
${AfterName}の大きさ　<B>${HislandSize}x${HislandSize}</B><BR>
コマンド入力限界数　<B>$HcommandMax</B><BR>
END
	my $bigcity = "";
	if($HbigcityFood){
		$bigcity = "通常の町と同じ消費量";
	}else{
		$bigcity = "３倍の消費量";
	}
	my $aidpop = "";
	if($Haidpop <= 0){
		$aidpop = "制限なし";
	}else{
		$aidpop = "$Haidpop$HunitPop";
	}
	$src .= <<"END";
$turntime
<BR>
放棄コマンド自動入力ターン数　<B>$HgiveupTurnターン</B><BR>
<BR>
<TABLE>
<TR $HbgInfoCell><TH rowspan=2>${HtagTH_}初期資金 / 最大資金${H_tagTH}${H_tagTH}</TH><TH rowspan=2>${HtagTH_}初期食料 / 最大食料${H_tagTH}</TH><TH colspan=5>${HtagTH_}最小単位${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}お金${H_tagTH}</TH><TH>${HtagTH_}食料${H_tagTH}</TH><TH>${HtagTH_}人口${H_tagTH}</TH><TH>${HtagTH_}広さ${H_tagTH}</TH><TH>${HtagTH_}木の数${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='center'>$HinitialMoney$HunitMoney / $MaxMoney$HunitMoney</TD><TD align='center'>$HinitialFood$HunitFood / $MaxFood$HunitFood</TD><TD align='right'>1$HunitMoney</TD><TD align='right'>1$HunitFood</TD><TD align='right'>1$HunitPop</TD><TD align='right'>1$HunitArea</TD><TD align='right'>1$HunitTree</TD></TR>
</TABLE></B><BR>
名前変更のコスト　<B>$HcostChangeName$HunitMoney</B><BR>
人口1$HunitPopあたりの食料消費料　<B>${HeatenFood}x1$HunitFood</B><BR>
大都市の食糧消費量　<B>${bigcity}</B><BR>
援助系を不可とする人口　<B>${aidpop}</B><BR>
島発見から他島への攻撃系命令を制限を加えるターン数　<B>${Hatkturn}ターン</B><BR>
<BR>
宇宙工場、宇宙農場は、宇宙人口の何倍の規模分が稼働するか？ 　<B>${HspaceEfficiency}倍</B><BR>
宇宙工場、宇宙農場の稼働している千人規模あたりの地上収入 　<B>${HspaceIncome}億</B><BR>
<BR>
防衛施設は、怪獣に踏まれた時自爆するか？　<B>$doStr[$HdBaseAuto]</B><BR>
基地の経験値の最大値　<B>$HmaxExpPoint</B><BR>
<BR>
占有率による勝敗機能で勝利した島が貰える量。(Max値を超えると、切り捨てられます)<BR>
資金<B>$HwinMoney$HunitMoney</B><BR>
食料<B>$HwinFood$HunitFood</B><BR>
兵器<B>$HwinWeapon$HunitWeapon</B><BR>
<BR>
ターン差命令で、命令実行から実際に発動するターン数(0の場合は、ターン差無し)<BR>
コロニー落し：<B>$HcomcolonyTurn</B>ターン<BR>
S怪獣派遣：<B>$HcomSSendMonsterTurn</B>ターン<BR>
怪獣派遣：<B>$HcomSendMonsterTurn</B>ターン<BR>
<BR>
END
	$HdisEarthquake *= 0.1; # 地震
	$HdisTsunami    *= 0.1; # 津波
	$HdisTyphoon    *= 0.1; # 台風
	$HdisMeteo      *= 0.1; # 隕石
	$HdisHugeMeteo  *= 0.1; # 巨大隕石
	$HdisEruption   *= 0.1; # 噴火
	$HdisFire       *= 0.1; # 火災
	$HdisMaizo      *= 0.1; # 埋蔵金
	$HdisAkasio     *= 0.1; # 赤潮
	$HdisTinka      *= 0.01;# 温泉による地盤沈下
	$HdisVGHarvest  *= 0.1; # 大豊作
	$HdisGHarvest   *= 0.1; # 豊作
	$HdisBHarvest   *= 0.1; # 凶作
	$HdisAEruption  *= 0.1; # 再噴火
	$HdisPirate     *= 0.1; # 海賊船
	$HdisTreasureS  *= 0.1; # 宝船
	
	$HdisFalldown   *= 0.1; # 地盤沈下
	$HdisMonster    *= 0.01;# 怪獣
	
	$HdisPollution  *= 0.01;# 公害
	$HmaxdisPollution *=0.1;# 公害MAX
	$HdisCrime      *= 0.01;# 犯罪
	$HdisSHugeMeteo *= 0.0001;# 宇宙巨大隕石
	
	$src .= <<"END";

島全体の災害など
<TABLE>
<TR $HbgInfoCell><TH rowspan=2>${HtagTH_}地震${H_tagTH}</TH><TH rowspan=2>${HtagTH_}津波${H_tagTH}</TH><TH rowspan=2>${HtagTH_}台風${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}隕石${H_tagTH}</TH><TH rowspan=2>${HtagTH_}巨大隕石${H_tagTH}</TH><TH rowspan=2>${HtagTH_}噴火${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}赤潮${H_tagTH}</TH><TH rowspan=2>${HtagTH_}大豊作${H_tagTH}</TH><TH rowspan=2>${HtagTH_}豊作${H_tagTH}</TH><TH rowspan=2>${HtagTH_}凶作${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}海賊船${H_tagTH}</TH><TH rowspan=2>${HtagTH_}宝船${H_tagTH}</TH><TH colspan=2>${HtagTH_}地盤沈下${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell><TH>${HtagTH_}安全限界の広さ${H_tagTH}</TH><TH>${HtagTH_}超えた場合の確率${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TD align='right'>${HdisEarthquake}%</TD><TD align='right'>${HdisTsunami}%</TD><TD align='right'>${HdisTyphoon}%</TD><TD align='right'>${HdisMeteo}%</TD><TD align='right'>${HdisHugeMeteo}%</TD><TD align='right'>${HdisEruption}%</TD><TD align='right'>${HdisAkasio}%</TD>
<TD align='right'>${HdisVGHarvest}%</TD><TD align='right'>${HdisGHarvest}%</TD><TD align='right'>${HdisBHarvest}%</TD><TD align='right'>${HdisPirate}%</TD><TD align='right'>${HdisTreasureS}%</TD>
<TD align='right'>$HdisFallBorder$HunitArea(${HdisFallBorder}Hex)</TD><TD align='right'>${HdisFalldown}%</TD></TR>
</TABLE><BR>
単位面積あたりで発生する災害など
<TABLE><TR $HbgInfoCell>
<TH>${HtagTH_}火災${H_tagTH}</TH><TH>${HtagTH_}埋蔵金${H_tagTH}</TH><TH>${HtagTH_}温泉による<br>局地地盤沈下${H_tagTH}</TH><TH>${HtagTH_}再噴火${H_tagTH}</TH>
</TR>
<TR $HbgInfoCell><TD align='right'>${HdisFire}%</TD><TD align='right'>${HdisMaizo}%</TD><TD align='right'>${HdisTinka}%</TD><TD align='right'>${HdisAEruption}%</TD>
</TR>
</TABLE><BR>
その他の災害<BR>
公害　<B>${HdisPollution}%</B>　(人口１万人当たりの発生率)<BR>
公害最大確率　<B>$HmaxdisPollution%</B><BR>
犯罪　<B>${HdisCrime}%</B>(人口１万人当たりの発生率　人口以外の要素もあります)<BR>
宇宙工場１つあたりに巨大隕石が発生する確率　<B>${HdisSHugeMeteo}%</B>×開発面積<BR>
<BR>
単位面積あたりの怪獣出現率　<B>${HdisMonster}%</B><BR>
<BR>
単位面積あたりの埋め立ていのら、海風船の出現値　<B>$HdisMonsterU</B><BR>
（少ないほど確率が高い、サバイバルモード、怪獣出現率=0の場合は値に関係なく出現しない）<BR>
<BR>
宇宙での怪獣の出現値　<B>${HdisSpaceMonster1}／開発面積</B>(怪獣有り)　<B>${HdisSpaceMonster2}／開発面積</B>(怪獣無り)<BR>
(町系の数だけ判定、少ないほど確率が高い、怪獣出現率=0の場合は値に関係なく出現しない)<BR>
<BR>
海域での怪獣の出現値　<B>$HdisSeaMonster</B><BR>
(毎ターンこの確率で海の数だけ判定少ないほど確率が高い、怪獣出現率=0の場合は値に関係なく出現しない)<BR>
<BR>
怪獣出現人口基準1(怪獣レベル1)　<B>$HdisMonsBorder1$HunitPop</B><BR>
END
foreach $i (0..$#HmonsterL1) {
	$src .= "$HmonsterName[$HmonsterL1[$i]] ";
}
$src .= "<BR><BR>怪獣出現人口基準2(怪獣レベル2)　<B>$HdisMonsBorder2$HunitPop</B><BR>";
foreach $i (0..$#HmonsterL2) {
	$src .= "$HmonsterName[$HmonsterL2[$i]] ";
}
$src .= "<BR><BR>怪獣出現人口基準3(怪獣レベル3)　<B>$HdisMonsBorder3$HunitPop</B><BR>";
foreach $i (0..$#HmonsterL3) {
	$src .= "$HmonsterName[$HmonsterL3[$i]] ";
}
$src .= "<BR><BR>怪獣出現人口基準4(怪獣レベル4)　<B>$HdisMonsBorder4$HunitPop</B><BR>";
foreach $i (0..$#HmonsterL4) {
	$src .= "$HmonsterName[$HmonsterL4[$i]] ";
}
$src .= "<BR><BR>怪獣出現人口基準5(怪獣レベル5)　<B>$HdisMonsBorder5$HunitPop</B><BR>";
foreach $i (0..$#HmonsterL5) {
	$src .= "$HmonsterName[$HmonsterL5[$i]] ";
}
	$src .= <<"END";

<TABLE>
<TR $HbgInfoCell>
<TH colspan=2 rowspan=2>${HtagTH_}怪獣の名称${H_tagTH}</TH>
<TH colspan=2>${HtagTH_}体力${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}経験値${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}残骸の値段${H_tagTH}</TH>
<TH rowspan=2>${HtagTH_}基本的な能力${H_tagTH}</TH></TR>
<TR $HbgInfoCell><TH>${HtagTH_}min${H_tagTH}</TH><TH>${HtagTH_}max${H_tagTH}</TH></TR>
END

@Monspe = ("特になし","足が速い(最大2歩あるく)","足がとても速い(最大何歩あるくか不明)","奇数ターンは硬化",
			"偶数ターンは硬化","常に硬化だが２５％であたる","命令処理より先に移動(0-1歩)",
			"命令処理より先に移動(最大何歩あるくか不明)","周囲１へクスに霧を出す","回復する（毎ターンMAX）");

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
	return "${mon}月 ${date}日 ${hour}時 ${min}分";
}
#----------------------------------------------------------------------
# ログテンプレート
#----------------------------------------------------------------------
# 記録ログ
sub logHistory {
	open(HOUT, ">>${HlogdirName}/hakojima.his");
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# 発見
sub logDiscover {
	my($name) = @_;
	logHistory("${HtagName_}${name}${AfterName}${H_tagName}が発見される。$addr");
}

# 名前の変更
sub logChangeName {
	my($name1, $name2) = @_;
	logHistory("${HtagName_}${name1}${AfterName}${H_tagName}、名称を${HtagName_}${name2}${AfterName}${H_tagName}に変更する。$addr");
}

# 強制削除ログ
sub logDeleteIsland {
	my($id, $name) = @_;
#	logHistory("${HtagName_}${name}島${H_tagName}、<B>管理人権限により</B><B><FONT COLOR=\"ff0000\">退場</FONT></B>となる。");
	logHistory("${HtagName_}${name}${AfterName}${H_tagName}に、突然<B>天罰が降り</B>あっというまに<B><FONT COLOR=\"ff0000\">海に沈没し</FONT></B>跡形もなくなりました。");
}

# 島の強制削除(スペシャルモード)
sub tempDeleteIsland {
	my($name) = @_;
	out(<<END);
${HtagBig_}${name}${AfterName}を強制削除しました。${H_tagBig}$HtempBack
END
}

# 島がいっぱいな場合
sub tempNewIslandFull {
	out(<<END);
${HtagBig_}申し訳ありません、${AfterName}が一杯で登録できません！！${H_tagBig}$HtempBack
END
}

# 新規で名前がない場合
sub tempNewIslandNoName {
	out(<<END);
${HtagBig_}${AfterName}につける名前が必要です。${H_tagBig}$HtempBack
END
}

# 新規で名前が不正な場合
sub tempNewIslandBadName {
	out(<<END);
${HtagBig_}',?()<>\"\'\$'とか入ってたり、「無人${AfterName}」とかいった変な名前はやめましょうよ〜<BR>
また、究想独自仕様により「匿名${AfterName}」は使用不可になっています。${H_tagBig}$HtempBack
END
}

# すでにその名前の島がある場合
sub tempNewIslandAlready {
	out(<<END);
${HtagBig_}その${AfterName}ならすでに発見されています。${H_tagBig}$HtempBack
END
}

# ID数が多すぎる場合
sub tempNewIslandId {
	out(<<END);
${HtagBig_}「究想の箱庭」の仕様によりこれ以上の新規参入はできません。${H_tagBig}$HtempBack
END
}
# ID数が多すぎる場合
sub tempNewIslandIdB {
	out(<<END);
${HtagBig_}「究想の箱庭」の仕様によりこれ以上のBattle Fieldは作成できません。${H_tagBig}$HtempBack
END
}
# 島がない場合
sub tempNotNewIsland {
	out(<<END);
${HtagBig_}海域に空きが無い為、これ以上の作成はできません。${H_tagBig}$HtempBack
END
}
# パスワードがない場合
sub tempNewIslandNoPassword {
	out(<<END);
${HtagBig_}パスワードが必要です。${H_tagBig}$HtempBack
END
}

# 島を発見しました!!
sub tempNewIslandHead {
	out(<<END);
<CENTER>
${HtagBig_}${AfterName}を発見しました！！${H_tagBig}<BR>
${HtagBig_}${HtagName_}「${HcurrentName}${AfterName}」${H_tagName}と命名します。${H_tagBig}<BR>
${HtagBig_}引き続き<a href="${HbaseDir}/profile.cgi?profile=$_[0]&mode=edit">プロフィール登録</a>をお願いします。(任意)${H_tagBig}　$HtempBack<BR>
</CENTER>
END
}

# 名前変更失敗
sub tempChangeNothing {
	out(<<END);
${HtagBig_}名前、パスワードともに空欄です${H_tagBig}$HtempBack
END
}

# 名前変更資金足りず
sub tempChangeNoMoney {
	out(<<END);
${HtagBig_}資金不足のため変更できません${H_tagBig}$HtempBack
END
}

# 名前変更成功
sub tempChange {
	out(<<END);
${HtagBig_}変更完了しました${H_tagBig}$HtempBack
END
}
# プレゼント
sub logPresent {
	my($id, $name, $log) = @_;
	logHistory("${HtagName_}${name}${AfterName}${H_tagName}$log") if ($log ne '');
}

1;
