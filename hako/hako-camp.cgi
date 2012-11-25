#----------------------------------------------------------------------
# 箱庭諸島 ver2.20
# 陣営画面モジュール
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 「帝国の興亡」 ver1.0.0 by おじー http://www.bekkoame.ne.jp/~tokuoka/ozzy.html
# 使用条件は箱庭諸島に準ずる．詳しくは付属のreadme.txtファイルを参照
#----------------------------------------------------------------------
# 究想の箱庭  (ver5.16)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 陣営画面
#----------------------------------------------------------------------
# メイン
sub campMain {
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	$HcurrentCamp = $Hislands[$HcurrentNumber];
	# 開放
	unlock ();

	# パスワード
	if(!checkPassword($HcurrentCamp->{'password'},$HinputPassword)) {
		# password間違い
		tempWrongPassword();
		return;
	}
	$HcurrentCampID = $HcurrentCamp->{'ally'};

	tempPrintCampHead (); # 作戦本部
	campAllIslandsInfo(); # 陣営に属する諸島の情報
}

#----------------------------------------------------------------------
# テンプレートその他
#----------------------------------------------------------------------

# ○○陣営 作戦本部
sub tempPrintCampHead {
	out(<<END);
<DIV align='center'>
${HtagBig_}陣営一覧表示${H_tagBig}<BR>
$HtempBack<BR><BR>
</DIV>
※　ほとんどの内政は、目標が他の島であっても自島に対して実行されます。<BR>
END
}

# 情報の表示
sub campAllIslandsInfo {
	# 陣営に属する島のコマンドのみ読み出し
	my($i);
	for($i = 0; $i < $HislandNumber; $i++) {
		($Hislands[$i]->{'command'}, $Hislands[$i]->{'land'}, $Hislands[$i]->{'landValue'}) = readCommands($Hislands[$i]->{'id'});
	}

	# 各島の情報書き出し
	for($i = 0; $i < $HislandNumber; $i++) {
		next if(($Hislands[$i]->{'ally'} eq '') || ($Hislands[$i]->{'ally'} < 1));
		if ($HcurrentCampID == $Hislands[$i]->{'ally'}) {
			next if($Hislands[$i]->{'id'} > 90);
			campIslandInfo($Hislands[$i], $i+1);
		}
	}

}

# 島のコマンド読み込み(陣営画面作成用)
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

	# コマンドのみ返す
	return \@command, \@land, \@landValue,
}

sub campIslandInfo {
	my($island, $rank) = @_;

	# 情報表示
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
#◎ハリボテ：$totalHaribote基<BR>
#○防衛施設：$totalDefence基<BR>
#◎海底油田：$totalOil基<BR>

	out(<<END);
<table><tr><th $HbgTitleCell>データ</th><th $HbgTitleCell>NO</th><th $HbgTitleCell>命令</th><th $HbgTitleCell>目標</th><th $HbgTitleCell>座標１</th><th $HbgTitleCell>数量</th><th $HbgTitleCell>座標２</th>
<tr><td rowspan=30>
<A HREF=\"$HthisFile?Sight=${id}\" class=\"M\" TARGET=_blank>$name</A><br>
$island->{'ownername'}<br><br>
資金：$island->{'money'}$HunitMoney<br>
食料：$island->{'food'}$HunitFood<br>
鉱石：$island->{'ore'}$HunitOre<br>
原油：$island->{'oil'}$HunitOil<br>
兵器：$island->{'weapon'}$HunitWeapon<br>
ミサイル発射数：$island->{'MissileK'}<br>
</td>
END
	for($i = 0; $i < 15; $i++) {
		campCommand($i, $island->{'command'}->[$i]);
	}
	out("</table>");
}

# 入力済みコマンド表示
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
