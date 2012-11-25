#
#
# 作者　　　：親方
# 日付　　　：2001/03/17
# バージョン：1.5
# 履歴　　　：2001/01/17 初版作成
# 　　　　　：2001/01/17 バグ修正と商人への対応
# 　　　　　：2001/01/19 順位がトップの島には制裁が行われないバグを修正
# 　　　　　：2001/03/17 島同士の取引を自動処理する機能を追加
#
# 　　　　　：2003/06/22 究想の箱庭５用にカスタマイズ
# 　　　　　：2003/09/20 取引応募確認機能を追加
# 　　　　　：2004/02/13 ０で割る場合がある問題を修正。
# 　　　　　：2004/07/10 制裁が兵器不足で失敗になる問題を修正。
# 　　　　　：2005/01/24 更新時間を拡張および、開発画面から参照する取引状況２を作成
# 　　　　　：2005/02/06 インターフェイスを改良・制裁処理のＯＮ、ＯＦＦ設定追加(ShibaAni)
# 　　　　　：2006/04/15 制裁を行わない設定の場合、制裁データを作らないように修正

# 　箱庭世界に資源取引所を開設します。
#
#

# 不成立の取引が自動破棄されるまでのターン数
$HexchangeDelTurns = 12;

# 取引品目
@HexchangeName = ('資金', '食料', '鉱石', '原油', '兵器');

# 取引品目の $island->{} の名前（「怪獣退治」など資源以外の取引では '' で指定）
@HexchangeVars = ('money', 'food', 'ore', 'oil', 'weapon');

# 取引品目の数量倍率
@HexchangeRate = (10, 10, 10, 10, 10);

# 取引品目の単位
@HexchangeUnit = ($HunitMoney, $HunitFood, $HunitOre, $HunitOil, $HunitWeapon);

# 島同士の取引を自動処理するか？
# 　自動処理しないと
# 　　・島同士の取引は成立後にプレイヤーが開発計画として行います。
# 　　・資源の不足があっても箱庭資源取引委員会は関知しません。
# 　　・商人との取引は成立時点で行われます。
# 　自動処理すると
# 　　・島同士の取引は成立時点で行われます。
# 　　・商人との取引は成立時点で行われます。
$HexchangeAutoMode = 1; # 0:手動、1:自動

#資源の不足があると箱庭資源取引委員会によって制裁を行う。
$HpenaltyExchangeSwitch = 1; # 0:行わない、1:行う

# 商人の名前
@HexchangeMerchantName = ('農業組合', '鉱石組合', '原油組合', '武器組合');

# 各商人の出現確率（各商人ごと 0%〜100%）
# ・商人が出現することは決まった状態で、どの商人が出現するか判定する確率です
# ・確率100%の商人がいないと「誰も出現しない」ことがあります
@HexchangeMerchantPercent = (80, 60, 50, 40);

# 箱庭資源取引委員会の制裁手段
$HexchangePenaltyAttack = 3; # 0:ミサイル、1:人造怪獣、2:記念碑、3:ランダム

# 取引データのファイル
$HexchangeFile = "$HlogdirName/exchange.dat";

# 取引データ
$HexchangeID = 1;
@HexchangeData = ();

# 取引データを読み込む
sub readExchange {
	local($_);
	if (open(Fexchange, "<$HexchangeFile")) {
		my(@bac) = ($/);
		local($/) = ("\n");

		chomp($HexchangeID = <Fexchange>);
		@HexchangeData = ();
		while (<Fexchange>) {
			chomp;
			@_ = split(',');
			my(%exchange);
			$exchange{'id'}        = shift; # 取引の ID
			$exchange{'iid'}       = shift; # 島の ID
			$exchange{'turn'}      = shift; # 登録ターン
			$exchange{'sell'}      = shift; # 提供資源名
			$exchange{'sell_cost'} = shift; # 提供資源量
			$exchange{'buy'}       = shift; # 希望資源名
			$exchange{'buy_cost'}  = shift; # 希望資源量
			$exchange{'bid'}       = shift; # 入札島の ID
			$exchange{'bid_cost'}  = shift; # 入札資源量
			$exchange{'rtime'}     = shift; # 更新時間
			push(@HexchangeData, \%exchange);
		}

		close(Fexchange);

		($/) = @bac;
		return 1;
	}
	return undef;
}

# 取引データを書き込む
sub writeExchange {
	local($_);
	if (open(Fexchange, ">$HexchangeFile")) {
		my(@bac) = ($\, $,, $");
		local($\, $,, $") = ("\n", ',', ',');

		print Fexchange $HexchangeID;
		my($exchange);
		foreach $exchange (@HexchangeData) {
			next if (!defined $exchange);
			print Fexchange
			$exchange->{'id'},
			$exchange->{'iid'},
			$exchange->{'turn'},
			$exchange->{'sell'},
			$exchange->{'sell_cost'},
			$exchange->{'buy'},
			$exchange->{'buy_cost'},
			$exchange->{'bid'},
			$exchange->{'bid_cost'},
			$exchange->{'rtime'},
			;
		}

		close(Fexchange);

		($\, $,, $") = @bac;
		return 1;
	}
	return undef;
}


# 取引状況
sub infoExchange {
	local($_);

	out(<<END);
<table border>
  <tr>
    <th $HbgTitleCell nowrap>${HtagTH_}取引番号${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}提供資源${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}数量${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}希望資源${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}数量${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}登録ターン${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}募集島名${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}応募数量${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}応募島名${H_tagTH}</th>
  </tr>
END

	my($exchange, $id, $iid, $turn, $tn, $island, $name, $sell, $sell_cost, $buy, $buy_cost, $bid, $bid_cost);
	foreach $exchange (@HexchangeData) {
	next if (!defined $exchange);
	$id = $exchange->{'id'};

	$iid = $exchange->{'iid'};
	next if ($iid == -99999); # これはペナルティデータなので無視
	if ($iid >= 0) {
		# 参加島
		$tn = $HidToNumber{$iid};
		$island = $Hislands[$tn];
		$name = $island->{'name'} . '島';
	} else {
		# 商人
		$name = $HexchangeMerchantName[-$iid - 1];
	}

	$turn = $exchange->{'turn'};

	$sell      = $exchange->{'sell'};
	$sell_cost = $exchange->{'sell_cost'} * $HexchangeRate[$sell];
	$buy       = $exchange->{'buy'};
	$buy_cost  = $exchange->{'buy_cost'} * $HexchangeRate[$buy];

	$bid       = $exchange->{'bid'};
	if ($bid >= 0) {
		# 参加島
		$tn = $HidToNumber{$bid};
		$island = $Hislands[$tn];
		$bid = $island->{'name'} . '島';
	} elsif ($bid != -99999) {
		# 商人
		$bid = $HexchangeMerchantName[-$bid - 1];
	} else {
		# 応募なし
		$bid = '&nbsp;';
	}
	$bid_cost  = $exchange->{'bid_cost'} * $HexchangeRate[$buy];;

	out(<<END);
  <tr>
    <th $HbgNumberCell nowrap align="right">${HtagNumber_}$id${H_tagNumber}</th>
    <td $HbgInfoCell nowrap align="center">$HexchangeName[$sell]</td>
    <td $HbgInfoCell nowrap align="right">$sell_cost$HexchangeUnit[$sell]</td>
    <td $HbgInfoCell nowrap align="center">$HexchangeName[$buy]</td>
    <td $HbgInfoCell nowrap align="right">$buy_cost$HexchangeUnit[$buy]</td>
    <td $HbgInfoCell nowrap align="right">$turnターン</td>
    <td $HbgInfoCell nowrap>${HtagName_}$name${H_tagName}</td>
    <td $HbgInfoCell nowrap align="right">$bid_cost$HexchangeUnit[$buy]</td>
    <td $HbgInfoCell nowrap>${HtagName_}$bid${H_tagName}</td>
  </tr>
END
	}

	out(<<END);
</table>
END
}

# 取引状況２(究想拡張)
sub infoExchange2 {
	my($cmdtime) = @_;
	
	my $htmltmp = <<"END";
<hr><DIV ID='islandInfo'>更新された取引情報<table border>
  <tr>
    <th $HbgTitleCell nowrap>${HtagTH_}取引番号${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}提供資源${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}数量${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}希望資源${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}数量${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}応募数量${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}応募島名${H_tagTH}</th>
  </tr>
END
	my($exchange, $id, $iid, $turn, $tn, $island, $sell, $sell_cost, $buy, $buy_cost, $bid, $bid_cost);
	foreach $exchange (@HexchangeData) {
	next if (!defined $exchange);
	$id = $exchange->{'id'};
	$iid = $exchange->{'iid'};
	next if ($iid == -99999 || $cmdtime > $exchange->{'rtime'}); # 無視
	
	$turn = $exchange->{'turn'};
	$sell      = $exchange->{'sell'};
	$sell_cost = $exchange->{'sell_cost'} * $HexchangeRate[$sell];
	$buy       = $exchange->{'buy'};
	$buy_cost  = $exchange->{'buy_cost'} * $HexchangeRate[$buy];
	$bid       = $exchange->{'bid'};
	if ($bid >= 0) {
		# 参加島
		$tn = $HidToNumber{$bid};
		$island = $Hislands[$tn];
		$bid = $island->{'name'} . '島';
	} elsif ($bid != -99999) {
		# 商人
		$bid = $HexchangeMerchantName[-$bid - 1];
	} else {
		# 応募なし
		$bid = '&nbsp;';
	}
	$bid_cost  = $exchange->{'bid_cost'} * $HexchangeRate[$buy];;
	out(<<END);
$htmltmp
  <tr>
    <th $HbgNumberCell nowrap align="right">${HtagNumber_}$id${H_tagNumber}</th>
    <td $HbgInfoCell nowrap align="center">$HexchangeName[$sell]</td>
    <td $HbgInfoCell nowrap align="right">$sell_cost$HexchangeUnit[$sell]</td>
    <td $HbgInfoCell nowrap align="center">$HexchangeName[$buy]</td>
    <td $HbgInfoCell nowrap align="right">$buy_cost$HexchangeUnit[$buy]</td>
    <td $HbgInfoCell nowrap align="right">$bid_cost$HexchangeUnit[$buy]</td>
    <td $HbgInfoCell nowrap>${HtagName_}$bid${H_tagName}</td>
  </tr>
END
$htmltmp = "";
	}
	out("</table></DIV><hr>") if($htmltmp eq "");
}

# 取引フォーム
sub formExchange {
	local($_);
	my($resource, $number0, $number00, $idEx, $ids);

	my($i);
	for ($i = $[; $i <= $#HexchangeName; $i++) {
		$resource .= "<option value=\"$i\">$HexchangeName[$i] ($HexchangeRate[$i]$HexchangeUnit[$i])";
	}

	for ($i = 0; $i < 100; $i++) {
		$number0  .= "<option value=\"$i\">$i";
		$number00 .= "<option value=\"$i\">" . sprintf('%02d', $i);
	}

	my($exchange);
	foreach $exchange (@HexchangeData) {
		next if (!defined $exchange);
		next if ($exchange->{'iid'} == -99999); # これはペナルティデータなので無視
		$i = $exchange->{'id'};
		$j = $exchange->{'buy'};
		$idEx .= "<form action=\"$HthisFile\" method=\"POST\">
						  <tr>
							  <td><input type=\"submit\" value=\"「$i」に応募\" name=\"ExchangeBidButton\"><input type=\"hidden\" name=\"EXC_ID\" value=\"$i\"></th>
						    <td><select name=\"EXC_SELL1\">$number0</select><select name=\"EXC_SELL0\">$number00</select>　×　$HexchangeRate[$j]$HexchangeUnit[$j]</td>
								<td><select name=\"ISLANDID\">$HislandList</select></td>
						    <td><input type=\"password\" name=\"PASSWORD\" value=\"${\htmlEscape($HdefaultPassword)}\" size=\"32\" maxlength=\"32\"></td>
						  </tr>
							<input type=\"hidden\" name=\"dummy\">
						 </form>";
						 
		$ids .= "<option value=\"$i\">$i";
	}

	out(<<END);
<table border>
  <tr>
    <th nowrap>応募取引</th>
    <th nowrap>数量</th>
		<th nowrap>島名</th>
    <th nowrap>パスワード</th>
  </tr>
	$idEx
</table>
<br>
<form action="$HthisFile" method="POST">
<table border>
  <tr>
    <th nowrap>募集取引</th>
    <th nowrap>提供資源</th>
    <th nowrap>希望資源</th>
    <th nowrap>島名</th>
    <th nowrap>パスワード</th>
  </tr>
  <tr>
		<td><input type="submit" value="取引を募集" name="ExchangeButton"></td>
    <td><select name="EXC_SELL">$resource</select>　×　<select name="EXC_SELL1">$number0</select><select name="EXC_SELL0">$number00</select></td>
    <td><select name="EXC_BUY">$resource</select>　×　<select name="EXC_BUY1">$number0</select><select name="EXC_BUY0">$number00</select></td>
    <td><select name="ISLANDID">$HislandList</select></td>
    <td><input type="password" name="PASSWORD" value="${\htmlEscape($HdefaultPassword)}" size="32" maxlength="32"></td>
  </tr>
</table>
<input type="hidden" name="dummy">
</form>
<br>
<form action="$HthisFile" method="POST">
<table border>
  <tr>
    <th nowrap>削除取引</th>
    <th nowrap>取引番号</th>
    <th nowrap>島名</th>
    <th nowrap>パスワード</th>
  </tr>
  <tr>
		<td><input type="submit" value="取引を削除" name="ExchangeDelButton"></td>
    <td><select name="EXC_ID">$ids</select></td>
    <td><select name="ISLANDID">$HislandList</select></td>
    <td><input type="password" name="PASSWORD" value="${\htmlEscape($HdefaultPassword)}" size="32" maxlength="32"></td>
  </tr>
</table>
<input type="hidden" name="dummy">
</form>
END
}

# 取引ページ
sub htmlExchange {
	local($_);

	readExchange();

	# 開放
	unlock();

	out(<<END);
$HtempBack
<h1>究想の箱庭資源取引所</h1>
<b>ここでは各島が所有している資源を別の資源に交換する仲介を行っています。</b><br>
・取引はオークション形式です。より良い条件を示した島との取引がターン更新で成立します。<br>
・取引が成立しないまま $HexchangeDelTurns ターンが経過すると登録が抹消されます。<br>
END
	if ($HexchangeAutoMode) {
		out("・島同士の取引は成立時点で行われます。<br>");
	}else{
		out("・<font color=\"red\">取引が成立したら責任を持って取引を実行してください。自動では実行されません。</font><br>");
	}
	out("・島以外が募集している取引はターン更新時に自動決済されます。<br>");
	out("・<font color=\"red\">不足があると制裁が行われます。</font><br>") if($HpenaltyExchangeSwitch);
	infoExchange();
	out("<br>");
	formExchange();
}

# ペナルティ処理
sub penaltyExchange {
	local($_);

	readExchange();
	return unless($HpenaltyExchangeSwitch);

	# ペナルティデータがあるか調べる
	my($exchange, $iid, $tn, $island);
	foreach $exchange (@HexchangeData) {
		next if (!defined $exchange);
		$iid = $exchange->{'iid'};
		next if ($iid != -99999); # ペナルティデータ以外は無視

		$tn = $HidToNumber{$exchange->{'bid'}};
		if (defined $tn) {
			# 島が存在する
			$island = $Hislands[$tn];

			# 制裁実行
			my($penalty) = $exchange->{'bid_cost'};
			$HexchangePenaltyAttack = random(3) if ($HexchangePenaltyAttack == 3);
			if ($HexchangePenaltyAttack == 0) {
				# ミサイル
				$penalty = 16 if ($penalty > 16); # 最大で16回（16回 x 5発 = 80発）

				my($comIsland) = makeComIsland("箱庭資源取引委員会の");
				my($target) = $exchange->{'bid'};
				my($n) = $penalty;
				my($i);
				for ($i = 0; $i < $n; $i++) {
					doMissileFireRandom($comIsland, $target, $HcomMissileNM, 5); # 通常ミサイルを５発単位で発射
					doCommand($comIsland);
				}
			} elsif ($HexchangePenaltyAttack == 1) {
				# 人造怪獣
				$penalty = 16 if ($penalty > 16); # 最大で16匹

				$island->{'monstersend'} += $penalty;
			} else {
				# 記念碑
				$penalty = 8 if ($penalty > 8); # 最大で8個

				$island->{'bigmissile'} += $penalty;
			}
		}

		$exchange = undef;
	}
}

# 取引のターン処理準備
sub turnExchangeBegin {
	local($_);

}

# 取引のターン処理
sub turnExchange {
	local($_);

	my($exchange);
	foreach $exchange (@HexchangeData) {
	next if (!defined $exchange);
	my($tn, $island, $iid, $name, $dead, $bisland, $bid, $bname, $bdead);

	$iid = $exchange->{'iid'};
	if ($iid == -99999){ # ペナルティデータである
		$iid = $exchange->{'bid'};
		$island = $Hislands[$HidToNumber{$iid}];
		if ($island->{'dead'}) {
			# ペナルティ対象の島が放棄されている
			$exchange = undef;
		}
		next;
	}

	if ($iid >= 0) {
		# 募集島
		$tn = $HidToNumber{$iid};
		$island = $Hislands[$tn];
		$name = $island->{'name'};
		$dead = $island->{'dead'};
	}

	$bid = $exchange->{'bid'};
	if ($bid >= 0) {
		# 応募島
		$tn = $HidToNumber{$bid};
		$bisland = $Hislands[$tn];
		$bname = $bisland->{'name'};
		$bdead = $bisland->{'dead'};
	}

	# 募集島が放棄されていないか？
	if ($dead) {
		# 放棄されている
		$bid = undef if ($bid < 0);
		logExcDead1($bid, $name, $exchange->{'id'});
		$exchange = undef;
		next;
	}

	# 応募島が放棄されていないか？
	if ($bdead && ($iid < 0)) {
		# 商人の募集に応募した島が放棄された
		logExcDead1(undef, $bname, $exchange->{'id'});
		$exchange = undef;
		next;
	}
	if ($bdead) {
		# 放棄されている
		logExcDead2($iid, $bname, $exchange->{'id'});
		$exchange->{'bid'} = -99999;
		$exchange->{'bid_cost'} = 0;
		goto L_LIMIT;
	}

	# 取引不成立か？
	if ($bid < 0) {
L_LIMIT:
		if ($HislandTurn - $exchange->{'turn'} >= $HexchangeDelTurns) {
			# 規定ターン数が経過した
			$iid = undef if ($iid < 0);
			logExcLimit($iid, $exchange->{'id'});
			$exchange = undef;
		} elsif ($iid < 0) {
			# 商人の募集した取引は成立しないと１ターンで削除
			if ($HislandTurn - $exchange->{'turn'} >= 1) {
				$exchange = undef;
			}
		}
		next;
	}

	# 取引が成立した
	my($sell, $sell_cost, $buy, $buy_cost, $bid_cost);
	$sell      = $exchange->{'sell'};
	$sell_cost = $exchange->{'sell_cost'} * $HexchangeRate[$sell];
	$buy       = $exchange->{'buy'};
	$buy_cost  = $exchange->{'buy_cost'} * $HexchangeRate[$buy];
	$bid_cost  = $exchange->{'bid_cost'} * $HexchangeRate[$buy];

	my($sell_value, $buy_value);
	my($penalty, $bpenalty);
	if ($iid >= 0) {
		# 募集島の資源量を確認する
		$_ = $HexchangeVars[$sell];
		if (defined $_) {
			# 存在する資源なら
			$sell_value = $island->{$_};
			if ($sell_value < $sell_cost) {
				# 資源量が足りない
				$sell_value = 1 if($sell_value < 1);
				$penalty += int($sell_cost / $sell_value); # ペナルティ発生
			}
		}
	}

	if ($bid >= 0) {
		# 応募島の資源量を確認する
		$_ = $HexchangeVars[$buy];
		if (defined $_) {
			# 存在する資源なら
			$buy_value = $bisland->{$_};
			if ($buy_value < $bid_cost) {
				# 資源量が足りない
				$buy_value = 1 if($buy_value < 1);
				$bpenalty += int($bid_cost / $buy_value); # ペナルティ発生
			}
		}
	}

	# 取引島の名前を整形する
	if ($iid >= 0) {
		# 島同士の取引
		$name .= '島';
		$bname .= '島';
	} else {
		# 商人との取引
		$name = $HexchangeMerchantName[-$iid - 1];
		$bname .= '島';
	}

	if (!$penalty && !$bpenalty) {
		# 取引成立
		if ($iid >= 0) {
			# 島同士の取引
			if ($HexchangeAutoMode) {
				# 自動取引なら

				# 提供資源
				$_ = $HexchangeVars[$sell];
				if (defined $_) {
					# 存在する資源なら
					$island->{$_}  -= $sell_cost;
					$bisland->{$_} += $sell_cost;
				}

				# 希望資源
				$_ = $HexchangeVars[$buy];
				if (defined $_) {
					# 存在する資源なら
					$island->{$_}  += $bid_cost;
					$bisland->{$_} -= $bid_cost;
				}
			}
		} else {
			# 商人との取引

			# 提供資源
			$_ = $HexchangeVars[$sell];
			$bisland->{$_} += $sell_cost;

			# 希望資源
			$_ = $HexchangeVars[$buy];
			$bisland->{$_} -= $bid_cost;
		}

		$sell = $HexchangeName[$sell] . $sell_cost . $HexchangeUnit[$sell];
		$buy  = $HexchangeName[$buy] . $bid_cost . $HexchangeUnit[$buy];
		logExcSuccess($bid, $name, ($iid >= 0 ? $iid : undef), $bname, $exchange->{'id'}, $sell, $buy, (($iid < 0) ? 1 : $HexchangeAutoMode));
	} else {
		# 取引不成立

		$sell = $HexchangeName[$sell] . $sell_cost . $HexchangeUnit[$sell];
		$buy  = $HexchangeName[$buy] . $bid_cost . $HexchangeUnit[$buy];
		logExcSuccess($bid, $name, ($iid >= 0 ? $iid : undef), $bname, $exchange->{'id'}, $sell, $buy, (($iid < 0) ? 1 : $HexchangeAutoMode));

		if ($penalty) {
			# 募集島にペナルティ発生
			if ($HexchangeAutoMode) {
				# 自動取引なら
				if($HpenaltyExchangeSwitch){
					# 制裁
					my(%exchange);
					$exchange{'id'}        = $HexchangeID++;
					$exchange{'iid'}       = -99999;   # ペナルティのフラグ
					$exchange{'turn'}      = $HcurrentID;
					$exchange{'bid'}       = $iid;     # ペナルティを課す島
					$exchange{'bid_cost'}  = $penalty; # ペナルティの回数
					push(@HexchangeData, \%exchange);
				}
				logExcPenalty($iid, $bid, $name, $exchange->{'id'}, $sell, $penalty);
			}
		}

		if ($bpenalty) {
			# 応募島にペナルティ発生
			if ($iid >= 0) {
				# 島同士の取引
				if ($HexchangeAutoMode) {
					# 自動取引なら
					if($HpenaltyExchangeSwitch){
						# 制裁
						my(%exchange);
						$exchange{'id'}        = $HexchangeID++;
						$exchange{'iid'}       = -99999;    # ペナルティのフラグ
						$exchange{'turn'}      = $HcurrentID;
						$exchange{'bid'}       = $bid;      # ペナルティを課す島
						$exchange{'bid_cost'}  = $bpenalty; # ペナルティの回数
						push(@HexchangeData, \%exchange);
					}
					logExcPenalty($bid, $iid, $bname, $exchange->{'id'}, $buy, $bpenalty);
				}
			} else {
				# 商人との取引
				if($HpenaltyExchangeSwitch){
					# 制裁
					my(%exchange);
					$exchange{'id'}        = $HexchangeID++;
					$exchange{'iid'}       = -99999;    # ペナルティのフラグ
					$exchange{'turn'}      = $HcurrentID;
					$exchange{'bid'}       = $bid;      # ペナルティを課す島
					$exchange{'bid_cost'}  = $bpenalty; # ペナルティの回数
					push(@HexchangeData, \%exchange);
				}
				logExcPenalty($bid, undef, $bname, $exchange->{'id'}, $buy, $bpenalty);
			}
		}
	}

	$exchange = undef;
	}
}

# 取引のターン処理後始末
sub turnExchangeEnd {
	local($_);

	writeExchange();
}

# 取引登録・削除
sub mainExchange {
	local($_);

	if ($HexchangeMode eq 'show') {
		# 取引ページへ
		htmlExchange();
		return;
	}

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

	readExchange();

	if ($HexchangeMode eq 'add') {
		# 取引追加
		if (($HexchangeSell == $HexchangeBuy) ||
			($HexchangeSellCost == 0) ||
			($HexchangeBuyCost == 0)) {
			# 内容が間違っている
			tempExcAddMiss();
		} else {
			# 内容が正しい
			my(%exchange);
			$exchange{'id'}        = $HexchangeID++;
			$exchange{'iid'}       = $HcurrentID;
			$exchange{'turn'}      = $HislandTurn;
			$exchange{'sell'}      = $HexchangeSell;
			$exchange{'sell_cost'} = $HexchangeSellCost;
			$exchange{'buy'}       = $HexchangeBuy;
			$exchange{'buy_cost'}  = $HexchangeBuyCost;
			$exchange{'bid'}       = -99999;
			$exchange{'rtime'}     = time;
			push(@HexchangeData, \%exchange);
			tempExcAddSuccess();
		}
	} elsif ($HexchangeMode eq 'bid') {
		# 取引応募
		my($exchange);
		foreach $exchange (@HexchangeData) {
			next if (!defined $exchange);
			if ($exchange->{'id'} == $HexchangeBidID) {
				if ($exchange->{'iid'} == $HcurrentID) {
					# 自島の依頼した取引
					tempExcBidMiss();
				} else {
					# 他島の依頼した取引
					if ($exchange->{'buy_cost'} > $HexchangeSellCost) {
						# 募集条件に達していない
						tempExcBidLimit();
					} elsif ($exchange->{'bid_cost'} >= $HexchangeSellCost) {
						# 他島に競り負けた
						tempExcBidLow();
					} elsif ($HexchangeCon) {
						# 自島の条件がもっとも良い(確認)
						tempExcBidSuccess();
					} else {
						# 自島の条件がもっとも良い
						tempExcBidSuccess2();
						$exchange->{'bid'} = $HcurrentID;
						$exchange->{'bid_cost'} = $HexchangeSellCost;
						$exchange->{'rtime'}    = time;
					}
				}
				last;
			}
		}
	} elsif ($HexchangeMode eq 'del') {
		# 取引削除
		my($exchange);
		foreach $exchange (@HexchangeData) {
			next if (!defined $exchange);
			if ($exchange->{'id'} == $HexchangeDelID) {
				if ($exchange->{'iid'} == $HcurrentID) {
					# 自島の依頼した取引
					$exchange = undef;
					tempExcDelSuccess();
				} else {
					# 他島の依頼した取引
					tempExcDelMiss();
				}
				last;
			}
		}
	}

	writeExchange();

	# 取引ページへ
	htmlExchange();
}

# 商人が取引募集
sub merchantInviteExchange {
	local($_);

	my($i);
	for ($i = $[; $i <= $#HexchangeMerchantName; $i++) {
	next if (rand(100) >= $HexchangeMerchantPercent[$i]);

	my($sell, $sell_cost, $buy, $buy_cost);
	if ($i == 0) {
		# 農業組合
		$sell = 1; # 食料を提供
		$sell_cost = random(8) + 3; # 30万トン〜100万トン
		$buy  = 0; # 資金を希望
		$buy_cost  = int($sell_cost * (20 - random(9)) / 10); # 12億円/10000トン〜20億円/10000トン

		$sell_cost *= 10; # 食料の取引単位を調整

	} elsif ($i == 1) {
		# 鉱石組合
		$sell = 2; # 鉱石を提供
		$sell_cost = random(91) + 10; # 100トン〜1000トン
		$buy  = 0; # 資金を希望
		$buy_cost  = int($sell_cost * (19 - random(9)) / 10); # 11億円/10トン〜19億円/10トン

	} elsif ($i == 2) {
		# 原油組合
		$sell = 3; # 原油を提供
		$sell_cost = random(91) + 10; # 100バレル〜1000バレル
		$buy  = 0; # 資金を希望
		$buy_cost  = int($sell_cost * (48 - random(23)) / 10); # 26億円/10バレル〜48億円/10バレル

	} elsif ($i == 3) {
		# 武器組合
		$sell = 4; # 兵器を提供
		$sell_cost = random(36) + 5; # 50トン〜400トン
		$buy  = 0; # 資金を希望
		$buy_cost  = $sell_cost * (22 - random(12)); # 110億円/10トン〜220億円/10トン
	}

	my(%exchange);
	$exchange{'id'}        = $HexchangeID++;
	$exchange{'iid'}       = -$i - 1;
	$exchange{'turn'}      = $HislandTurn;
	$exchange{'sell'}      = $sell;
	$exchange{'sell_cost'} = $sell_cost;
	$exchange{'buy'}       = $buy;
	$exchange{'buy_cost'}  = $buy_cost;
	$exchange{'bid'}       = -99999;
	$exchange{'rtime'}     = time;
	push(@HexchangeData, \%exchange);
	}
}

# コンピュータが使う島データを作成する
sub makeComIsland {
	my($name) = @_;
	my($id) = 255;
	require './hako-make.cgi';
	my($island) = makeNewIsland();

	$island->{'name'} = $name;
	$island->{'id'} = $id;

	$island->{'money'} = 0x7fffffff;
	$island->{'food'} = 0x7fffffff;
	$island->{'weapon'} = 0x7fffffff;

	# ミサイル基地を十分に作る
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($x, $y, $n);
L_LAND_BASE:
	for ($y = 0; $y < $HislandSize; $y++) {
		for ($x = 0; $x < $HislandSize; $x++) {
			next if ($land->[$x][$y] != $HlandSea); # 海以外はそのまま

			# 経験値最大のミサイル基地にする
			$land->[$x][$y] = $HlandBase;
			$landValue->[$x][$y] = $HmaxExpPoint;
			last L_LAND_BASE if (++$n >= 20); # 20箇所まで作る
		}
	}

	return $island;
}

# ランダムな座標にミサイル攻撃するコマンドを登録する
sub doMissileFireRandom {
	my($island, $target, $kind, $n) = @_;
	my($x) = int(rand($HislandSize - 2) + 1);
	my($y) = int(rand($HislandSize - 2) + 1);
	
	slideBack($island->{'command'}, 0, $kind, $target, $x, $y, $n);
}


# 取引追加成功
sub tempExcAddSuccess {
	out(<<END);
${HtagBig_}指定の取引を登録しました。${H_tagBig}
END
}

# 取引追加失敗
sub tempExcAddMiss {
	out(<<END);
${HtagBig_}指定の取引は無効な内容です。${H_tagBig}
END
}
# 取引応募確認
sub tempExcBidSuccess {
	my($buy,$bid_cost);
	foreach $exchange (@HexchangeData) {
		next if (!defined $exchange);
		if($exchange->{'id'} == $HexchangeBidID){
			$HexchangeBuy = $exchange->{'buy'};
			$bid_cost = $HexchangeSellCost * $HexchangeRate[$HexchangeBuy];
			$bid_cost = $HexchangeName[$HexchangeBuy] . $bid_cost . $HexchangeUnit[$HexchangeBuy];
		}
	}
	out(<<END);
${HtagBig_}指定取引の応募を確定しますか？${H_tagBig}
<form action="$HthisFile" method="POST">
<table border>
  <tr>
    <th nowrap rowspan="2"><input type="submit" value="取引を確定" name="ExchangeBid2Button"></th>
    <th nowrap>取引番号</th>
    <th nowrap>数量</th>
  </tr>
  <tr>
    <td>$HexchangeBidID</td>
    <td>$bid_cost</td>
  </tr>
</table>
<input type="hidden" name="ISLANDID" value="$HcurrentID">
<input type="hidden" name="PASSWORD" value="${\htmlEscape($HdefaultPassword)}">
<input type="hidden" name="EXC_ID" value="$HexchangeBidID">
<input type="hidden" name="EXC_SELL" value="$HexchangeSellCost">
<input type="hidden" name="dummy">
</form>
END
}

# 取引応募確定
sub tempExcBidSuccess2 {
	out(<<END);
${HtagBig_}指定の取引に応募しました。${H_tagBig}
END
}

# 取引応募却下
sub tempExcBidLimit {
	out(<<END);
${HtagBig_}応募数量が募集条件に達していません。${H_tagBig}
END
}

# 取引応募競り負け
sub tempExcBidLow {
	out(<<END);
${HtagBig_}他島が更に良い条件で応募しています。${H_tagBig}
END
}

# 取引応募失敗
sub tempExcBidMiss {
	out(<<END);
${HtagBig_}これは自島の依頼した取引です。${H_tagBig}
END
}

# 取引削除成功
sub tempExcDelSuccess {
	out(<<END);
${HtagBig_}指定の取引を削除しました。${H_tagBig}
END
}

# 取引削除失敗
sub tempExcDelMiss {
	out(<<END);
${HtagBig_}これは他島の依頼した取引です。${H_tagBig}
END
}

# 募集島放棄
sub logExcDead1 {
	my($id, $name, $no) = @_;
	logOut("取引番号 ${no} は${HtagName_}${name}島${H_tagName}が<B>無人島</B>になったために無効となりました。",$id);
}

# 応募島放棄
sub logExcDead2 {
	my($id, $name, $no) = @_;
	logOut("取引番号 ${no} は${HtagName_}${name}島${H_tagName}が<B>無人島</B>になったために募集継続となりました。",$id);
}

# 規定ターン数経過
sub logExcLimit {
	my($id, $no) = @_;
	logOut("取引番号 ${no} は応募がなかったために無効となりました。",$id);
}

# 取引成立
sub logExcSuccess {
	my($id, $name, $bid, $bname, $no, $sell, $buy, $auto) = @_;
	$auto = ($auto ? '（自動取引）' : '（手動取引）');
	logOut("取引番号 ${no} は${HtagName_}${name}${H_tagName}が<B>${sell}</B>、${HtagName_}${bname}${H_tagName}が<B>${buy}</B>を交換することで成立しました。<B>${auto}</B>",$id, $bid);
}

# ペナルティ発生
sub logExcPenalty {
	my($id, $bid, $bname, $no, $buy, $penalty) = @_;
	if($HpenaltyExchangeSwitch){
		logOut("取引番号 ${no} は${HtagName_}${bname}${H_tagName}に<B>${buy}</B>の備蓄がないことが判明！！箱庭資源取引委員会では<B>制裁発動($penalty)</B>を決定しました。",$id, $bid);
	}else{
		logOut("取引番号 ${no} は${HtagName_}${bname}${H_tagName}に<B>${buy}</B>の備蓄がないことが判明！！取引は行われませんでした。",$id, $bid);
	}
}


1;
