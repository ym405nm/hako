#
#
# ��ԡ�����������
# ���ա�������2001/03/17
# �С������1.5
# ���򡡡�����2001/01/17 ���Ǻ���
# ������������2001/01/17 �Х������Ⱦ��ͤؤ��б�
# ������������2001/01/19 ��̤��ȥåפ���ˤ����ۤ��Ԥ��ʤ��Х�����
# ������������2001/03/17 ��Ʊ�Τμ����ư�������뵡ǽ���ɲ�
#
# ������������2003/06/22 ���ۤ�Ȣ���Ѥ˥������ޥ���
# ������������2003/09/20 ��������ǧ��ǽ���ɲ�
# ������������2004/02/13 ���ǳ���礬�������������
# ������������2004/07/10 ���ۤ�ʼ����­�Ǽ��Ԥˤʤ����������
# ������������2005/01/24 �������֤��ĥ����ӡ���ȯ���̤��黲�Ȥ����������������
# ������������2005/02/06 ���󥿡��ե���������ɡ����۽����ΣϣΡ��ϣƣ������ɲ�(ShibaAni)
# ������������2006/04/15 ���ۤ�Ԥ�ʤ�����ξ�硢���ۥǡ�������ʤ��褦�˽���

# ��Ȣ�������˻񸻼������ߤ��ޤ���
#
#

# ����Ω�μ������ư�˴������ޤǤΥ������
$HexchangeDelTurns = 12;

# �������
@HexchangeName = ('���', '����', '����', '����', 'ʼ��');

# ������ܤ� $island->{} ��̾���ʡֲ����༣�פʤɻ񸻰ʳ��μ���Ǥ� '' �ǻ����
@HexchangeVars = ('money', 'food', 'ore', 'oil', 'weapon');

# ������ܤο�����Ψ
@HexchangeRate = (10, 10, 10, 10, 10);

# ������ܤ�ñ��
@HexchangeUnit = ($HunitMoney, $HunitFood, $HunitOre, $HunitOil, $HunitWeapon);

# ��Ʊ�Τμ����ư�������뤫��
# ����ư�������ʤ���
# ��������Ʊ�Τμ������Ω��˥ץ쥤�䡼����ȯ�ײ�Ȥ��ƹԤ��ޤ���
# �������񸻤���­�����äƤ�Ȣ��񸻼���Ѱ���ϴ��Τ��ޤ���
# ���������ͤȤμ������Ω�����ǹԤ��ޤ���
# ����ư���������
# ��������Ʊ�Τμ������Ω�����ǹԤ��ޤ���
# ���������ͤȤμ������Ω�����ǹԤ��ޤ���
$HexchangeAutoMode = 1; # 0:��ư��1:��ư

#�񸻤���­�������Ȣ��񸻼���Ѱ���ˤ�ä����ۤ�Ԥ���
$HpenaltyExchangeSwitch = 1; # 0:�Ԥ�ʤ���1:�Ԥ�

# ���ͤ�̾��
@HexchangeMerchantName = ('�����ȹ�', '�����ȹ�', '�����ȹ�', '����ȹ�');

# �ƾ��ͤνи���Ψ�ʳƾ��ͤ��� 0%��100%��
# �����ͤ��и����뤳�ȤϷ�ޤä����֤ǡ��ɤξ��ͤ��и����뤫Ƚ�ꤹ���Ψ�Ǥ�
# ����Ψ100%�ξ��ͤ����ʤ��ȡ�ï��и����ʤ��פ��Ȥ�����ޤ�
@HexchangeMerchantPercent = (80, 60, 50, 40);

# Ȣ��񸻼���Ѱ�������ۼ���
$HexchangePenaltyAttack = 3; # 0:�ߥ����롢1:��¤���á�2:��ǰ�ꡢ3:������

# ����ǡ����Υե�����
$HexchangeFile = "$HlogdirName/exchange.dat";

# ����ǡ���
$HexchangeID = 1;
@HexchangeData = ();

# ����ǡ������ɤ߹���
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
			$exchange{'id'}        = shift; # ����� ID
			$exchange{'iid'}       = shift; # ��� ID
			$exchange{'turn'}      = shift; # ��Ͽ������
			$exchange{'sell'}      = shift; # �󶡻�̾
			$exchange{'sell_cost'} = shift; # �󶡻���
			$exchange{'buy'}       = shift; # ��˾��̾
			$exchange{'buy_cost'}  = shift; # ��˾����
			$exchange{'bid'}       = shift; # ������� ID
			$exchange{'bid_cost'}  = shift; # ��������
			$exchange{'rtime'}     = shift; # ��������
			push(@HexchangeData, \%exchange);
		}

		close(Fexchange);

		($/) = @bac;
		return 1;
	}
	return undef;
}

# ����ǡ�����񤭹���
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


# �������
sub infoExchange {
	local($_);

	out(<<END);
<table border>
  <tr>
    <th $HbgTitleCell nowrap>${HtagTH_}����ֹ�${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}�󶡻�${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}����${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}��˾��${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}����${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}��Ͽ������${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}�罸��̾${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}�������${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}������̾${H_tagTH}</th>
  </tr>
END

	my($exchange, $id, $iid, $turn, $tn, $island, $name, $sell, $sell_cost, $buy, $buy_cost, $bid, $bid_cost);
	foreach $exchange (@HexchangeData) {
	next if (!defined $exchange);
	$id = $exchange->{'id'};

	$iid = $exchange->{'iid'};
	next if ($iid == -99999); # ����ϥڥʥ�ƥ��ǡ����ʤΤ�̵��
	if ($iid >= 0) {
		# ������
		$tn = $HidToNumber{$iid};
		$island = $Hislands[$tn];
		$name = $island->{'name'} . '��';
	} else {
		# ����
		$name = $HexchangeMerchantName[-$iid - 1];
	}

	$turn = $exchange->{'turn'};

	$sell      = $exchange->{'sell'};
	$sell_cost = $exchange->{'sell_cost'} * $HexchangeRate[$sell];
	$buy       = $exchange->{'buy'};
	$buy_cost  = $exchange->{'buy_cost'} * $HexchangeRate[$buy];

	$bid       = $exchange->{'bid'};
	if ($bid >= 0) {
		# ������
		$tn = $HidToNumber{$bid};
		$island = $Hislands[$tn];
		$bid = $island->{'name'} . '��';
	} elsif ($bid != -99999) {
		# ����
		$bid = $HexchangeMerchantName[-$bid - 1];
	} else {
		# ����ʤ�
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
    <td $HbgInfoCell nowrap align="right">$turn������</td>
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

# ���������(���۳�ĥ)
sub infoExchange2 {
	my($cmdtime) = @_;
	
	my $htmltmp = <<"END";
<hr><DIV ID='islandInfo'>�������줿�������<table border>
  <tr>
    <th $HbgTitleCell nowrap>${HtagTH_}����ֹ�${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}�󶡻�${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}����${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}��˾��${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}����${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}�������${H_tagTH}</th>
    <th $HbgTitleCell nowrap>${HtagTH_}������̾${H_tagTH}</th>
  </tr>
END
	my($exchange, $id, $iid, $turn, $tn, $island, $sell, $sell_cost, $buy, $buy_cost, $bid, $bid_cost);
	foreach $exchange (@HexchangeData) {
	next if (!defined $exchange);
	$id = $exchange->{'id'};
	$iid = $exchange->{'iid'};
	next if ($iid == -99999 || $cmdtime > $exchange->{'rtime'}); # ̵��
	
	$turn = $exchange->{'turn'};
	$sell      = $exchange->{'sell'};
	$sell_cost = $exchange->{'sell_cost'} * $HexchangeRate[$sell];
	$buy       = $exchange->{'buy'};
	$buy_cost  = $exchange->{'buy_cost'} * $HexchangeRate[$buy];
	$bid       = $exchange->{'bid'};
	if ($bid >= 0) {
		# ������
		$tn = $HidToNumber{$bid};
		$island = $Hislands[$tn];
		$bid = $island->{'name'} . '��';
	} elsif ($bid != -99999) {
		# ����
		$bid = $HexchangeMerchantName[-$bid - 1];
	} else {
		# ����ʤ�
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

# ����ե�����
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
		next if ($exchange->{'iid'} == -99999); # ����ϥڥʥ�ƥ��ǡ����ʤΤ�̵��
		$i = $exchange->{'id'};
		$j = $exchange->{'buy'};
		$idEx .= "<form action=\"$HthisFile\" method=\"POST\">
						  <tr>
							  <td><input type=\"submit\" value=\"��$i�פ˱���\" name=\"ExchangeBidButton\"><input type=\"hidden\" name=\"EXC_ID\" value=\"$i\"></th>
						    <td><select name=\"EXC_SELL1\">$number0</select><select name=\"EXC_SELL0\">$number00</select>���ߡ�$HexchangeRate[$j]$HexchangeUnit[$j]</td>
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
    <th nowrap>������</th>
    <th nowrap>����</th>
		<th nowrap>��̾</th>
    <th nowrap>�ѥ����</th>
  </tr>
	$idEx
</table>
<br>
<form action="$HthisFile" method="POST">
<table border>
  <tr>
    <th nowrap>�罸���</th>
    <th nowrap>�󶡻�</th>
    <th nowrap>��˾��</th>
    <th nowrap>��̾</th>
    <th nowrap>�ѥ����</th>
  </tr>
  <tr>
		<td><input type="submit" value="������罸" name="ExchangeButton"></td>
    <td><select name="EXC_SELL">$resource</select>���ߡ�<select name="EXC_SELL1">$number0</select><select name="EXC_SELL0">$number00</select></td>
    <td><select name="EXC_BUY">$resource</select>���ߡ�<select name="EXC_BUY1">$number0</select><select name="EXC_BUY0">$number00</select></td>
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
    <th nowrap>������</th>
    <th nowrap>����ֹ�</th>
    <th nowrap>��̾</th>
    <th nowrap>�ѥ����</th>
  </tr>
  <tr>
		<td><input type="submit" value="�������" name="ExchangeDelButton"></td>
    <td><select name="EXC_ID">$ids</select></td>
    <td><select name="ISLANDID">$HislandList</select></td>
    <td><input type="password" name="PASSWORD" value="${\htmlEscape($HdefaultPassword)}" size="32" maxlength="32"></td>
  </tr>
</table>
<input type="hidden" name="dummy">
</form>
END
}

# ����ڡ���
sub htmlExchange {
	local($_);

	readExchange();

	# ����
	unlock();

	out(<<END);
$HtempBack
<h1>���ۤ�Ȣ��񸻼����</h1>
<b>�����Ǥϳ��礬��ͭ���Ƥ���񸻤��̤λ񸻤˸򴹤�������ԤäƤ��ޤ���</b><br>
������ϥ��������������Ǥ�������ɤ����򼨤�����Ȥμ���������󹹿�����Ω���ޤ���<br>
���������Ω���ʤ��ޤ� $HexchangeDelTurns �����󤬷в᤹�����Ͽ�����ä���ޤ���<br>
END
	if ($HexchangeAutoMode) {
		out("����Ʊ�Τμ������Ω�����ǹԤ��ޤ���<br>");
	}else{
		out("��<font color=\"red\">�������Ω��������Ǥ����äƼ����¹Ԥ��Ƥ�����������ư�Ǥϼ¹Ԥ���ޤ���</font><br>");
	}
	out("����ʳ����罸���Ƥ������ϥ����󹹿����˼�ư��Ѥ���ޤ���<br>");
	out("��<font color=\"red\">��­����������ۤ��Ԥ��ޤ���</font><br>") if($HpenaltyExchangeSwitch);
	infoExchange();
	out("<br>");
	formExchange();
}

# �ڥʥ�ƥ�����
sub penaltyExchange {
	local($_);

	readExchange();
	return unless($HpenaltyExchangeSwitch);

	# �ڥʥ�ƥ��ǡ��������뤫Ĵ�٤�
	my($exchange, $iid, $tn, $island);
	foreach $exchange (@HexchangeData) {
		next if (!defined $exchange);
		$iid = $exchange->{'iid'};
		next if ($iid != -99999); # �ڥʥ�ƥ��ǡ����ʳ���̵��

		$tn = $HidToNumber{$exchange->{'bid'}};
		if (defined $tn) {
			# �礬¸�ߤ���
			$island = $Hislands[$tn];

			# ���ۼ¹�
			my($penalty) = $exchange->{'bid_cost'};
			$HexchangePenaltyAttack = random(3) if ($HexchangePenaltyAttack == 3);
			if ($HexchangePenaltyAttack == 0) {
				# �ߥ�����
				$penalty = 16 if ($penalty > 16); # �����16���16�� x 5ȯ = 80ȯ��

				my($comIsland) = makeComIsland("Ȣ��񸻼���Ѱ����");
				my($target) = $exchange->{'bid'};
				my($n) = $penalty;
				my($i);
				for ($i = 0; $i < $n; $i++) {
					doMissileFireRandom($comIsland, $target, $HcomMissileNM, 5); # �̾�ߥ������ȯñ�̤�ȯ��
					doCommand($comIsland);
				}
			} elsif ($HexchangePenaltyAttack == 1) {
				# ��¤����
				$penalty = 16 if ($penalty > 16); # �����16ɤ

				$island->{'monstersend'} += $penalty;
			} else {
				# ��ǰ��
				$penalty = 8 if ($penalty > 8); # �����8��

				$island->{'bigmissile'} += $penalty;
			}
		}

		$exchange = undef;
	}
}

# ����Υ������������
sub turnExchangeBegin {
	local($_);

}

# ����Υ��������
sub turnExchange {
	local($_);

	my($exchange);
	foreach $exchange (@HexchangeData) {
	next if (!defined $exchange);
	my($tn, $island, $iid, $name, $dead, $bisland, $bid, $bname, $bdead);

	$iid = $exchange->{'iid'};
	if ($iid == -99999){ # �ڥʥ�ƥ��ǡ����Ǥ���
		$iid = $exchange->{'bid'};
		$island = $Hislands[$HidToNumber{$iid}];
		if ($island->{'dead'}) {
			# �ڥʥ�ƥ��оݤ��礬��������Ƥ���
			$exchange = undef;
		}
		next;
	}

	if ($iid >= 0) {
		# �罸��
		$tn = $HidToNumber{$iid};
		$island = $Hislands[$tn];
		$name = $island->{'name'};
		$dead = $island->{'dead'};
	}

	$bid = $exchange->{'bid'};
	if ($bid >= 0) {
		# ������
		$tn = $HidToNumber{$bid};
		$bisland = $Hislands[$tn];
		$bname = $bisland->{'name'};
		$bdead = $bisland->{'dead'};
	}

	# �罸�礬��������Ƥ��ʤ�����
	if ($dead) {
		# ��������Ƥ���
		$bid = undef if ($bid < 0);
		logExcDead1($bid, $name, $exchange->{'id'});
		$exchange = undef;
		next;
	}

	# �����礬��������Ƥ��ʤ�����
	if ($bdead && ($iid < 0)) {
		# ���ͤ��罸�˱��礷���礬�������줿
		logExcDead1(undef, $bname, $exchange->{'id'});
		$exchange = undef;
		next;
	}
	if ($bdead) {
		# ��������Ƥ���
		logExcDead2($iid, $bname, $exchange->{'id'});
		$exchange->{'bid'} = -99999;
		$exchange->{'bid_cost'} = 0;
		goto L_LIMIT;
	}

	# �������Ω����
	if ($bid < 0) {
L_LIMIT:
		if ($HislandTurn - $exchange->{'turn'} >= $HexchangeDelTurns) {
			# ���꥿��������вᤷ��
			$iid = undef if ($iid < 0);
			logExcLimit($iid, $exchange->{'id'});
			$exchange = undef;
		} elsif ($iid < 0) {
			# ���ͤ��罸�����������Ω���ʤ��ȣ�������Ǻ��
			if ($HislandTurn - $exchange->{'turn'} >= 1) {
				$exchange = undef;
			}
		}
		next;
	}

	# �������Ω����
	my($sell, $sell_cost, $buy, $buy_cost, $bid_cost);
	$sell      = $exchange->{'sell'};
	$sell_cost = $exchange->{'sell_cost'} * $HexchangeRate[$sell];
	$buy       = $exchange->{'buy'};
	$buy_cost  = $exchange->{'buy_cost'} * $HexchangeRate[$buy];
	$bid_cost  = $exchange->{'bid_cost'} * $HexchangeRate[$buy];

	my($sell_value, $buy_value);
	my($penalty, $bpenalty);
	if ($iid >= 0) {
		# �罸��λ��̤��ǧ����
		$_ = $HexchangeVars[$sell];
		if (defined $_) {
			# ¸�ߤ���񸻤ʤ�
			$sell_value = $island->{$_};
			if ($sell_value < $sell_cost) {
				# ���̤�­��ʤ�
				$sell_value = 1 if($sell_value < 1);
				$penalty += int($sell_cost / $sell_value); # �ڥʥ�ƥ�ȯ��
			}
		}
	}

	if ($bid >= 0) {
		# ������λ��̤��ǧ����
		$_ = $HexchangeVars[$buy];
		if (defined $_) {
			# ¸�ߤ���񸻤ʤ�
			$buy_value = $bisland->{$_};
			if ($buy_value < $bid_cost) {
				# ���̤�­��ʤ�
				$buy_value = 1 if($buy_value < 1);
				$bpenalty += int($bid_cost / $buy_value); # �ڥʥ�ƥ�ȯ��
			}
		}
	}

	# ������̾������������
	if ($iid >= 0) {
		# ��Ʊ�Τμ��
		$name .= '��';
		$bname .= '��';
	} else {
		# ���ͤȤμ��
		$name = $HexchangeMerchantName[-$iid - 1];
		$bname .= '��';
	}

	if (!$penalty && !$bpenalty) {
		# �����Ω
		if ($iid >= 0) {
			# ��Ʊ�Τμ��
			if ($HexchangeAutoMode) {
				# ��ư����ʤ�

				# �󶡻�
				$_ = $HexchangeVars[$sell];
				if (defined $_) {
					# ¸�ߤ���񸻤ʤ�
					$island->{$_}  -= $sell_cost;
					$bisland->{$_} += $sell_cost;
				}

				# ��˾��
				$_ = $HexchangeVars[$buy];
				if (defined $_) {
					# ¸�ߤ���񸻤ʤ�
					$island->{$_}  += $bid_cost;
					$bisland->{$_} -= $bid_cost;
				}
			}
		} else {
			# ���ͤȤμ��

			# �󶡻�
			$_ = $HexchangeVars[$sell];
			$bisland->{$_} += $sell_cost;

			# ��˾��
			$_ = $HexchangeVars[$buy];
			$bisland->{$_} -= $bid_cost;
		}

		$sell = $HexchangeName[$sell] . $sell_cost . $HexchangeUnit[$sell];
		$buy  = $HexchangeName[$buy] . $bid_cost . $HexchangeUnit[$buy];
		logExcSuccess($bid, $name, ($iid >= 0 ? $iid : undef), $bname, $exchange->{'id'}, $sell, $buy, (($iid < 0) ? 1 : $HexchangeAutoMode));
	} else {
		# �������Ω

		$sell = $HexchangeName[$sell] . $sell_cost . $HexchangeUnit[$sell];
		$buy  = $HexchangeName[$buy] . $bid_cost . $HexchangeUnit[$buy];
		logExcSuccess($bid, $name, ($iid >= 0 ? $iid : undef), $bname, $exchange->{'id'}, $sell, $buy, (($iid < 0) ? 1 : $HexchangeAutoMode));

		if ($penalty) {
			# �罸��˥ڥʥ�ƥ�ȯ��
			if ($HexchangeAutoMode) {
				# ��ư����ʤ�
				if($HpenaltyExchangeSwitch){
					# ����
					my(%exchange);
					$exchange{'id'}        = $HexchangeID++;
					$exchange{'iid'}       = -99999;   # �ڥʥ�ƥ��Υե饰
					$exchange{'turn'}      = $HcurrentID;
					$exchange{'bid'}       = $iid;     # �ڥʥ�ƥ���ݤ���
					$exchange{'bid_cost'}  = $penalty; # �ڥʥ�ƥ��β��
					push(@HexchangeData, \%exchange);
				}
				logExcPenalty($iid, $bid, $name, $exchange->{'id'}, $sell, $penalty);
			}
		}

		if ($bpenalty) {
			# ������˥ڥʥ�ƥ�ȯ��
			if ($iid >= 0) {
				# ��Ʊ�Τμ��
				if ($HexchangeAutoMode) {
					# ��ư����ʤ�
					if($HpenaltyExchangeSwitch){
						# ����
						my(%exchange);
						$exchange{'id'}        = $HexchangeID++;
						$exchange{'iid'}       = -99999;    # �ڥʥ�ƥ��Υե饰
						$exchange{'turn'}      = $HcurrentID;
						$exchange{'bid'}       = $bid;      # �ڥʥ�ƥ���ݤ���
						$exchange{'bid_cost'}  = $bpenalty; # �ڥʥ�ƥ��β��
						push(@HexchangeData, \%exchange);
					}
					logExcPenalty($bid, $iid, $bname, $exchange->{'id'}, $buy, $bpenalty);
				}
			} else {
				# ���ͤȤμ��
				if($HpenaltyExchangeSwitch){
					# ����
					my(%exchange);
					$exchange{'id'}        = $HexchangeID++;
					$exchange{'iid'}       = -99999;    # �ڥʥ�ƥ��Υե饰
					$exchange{'turn'}      = $HcurrentID;
					$exchange{'bid'}       = $bid;      # �ڥʥ�ƥ���ݤ���
					$exchange{'bid_cost'}  = $bpenalty; # �ڥʥ�ƥ��β��
					push(@HexchangeData, \%exchange);
				}
				logExcPenalty($bid, undef, $bname, $exchange->{'id'}, $buy, $bpenalty);
			}
		}
	}

	$exchange = undef;
	}
}

# ����Υ�������������
sub turnExchangeEnd {
	local($_);

	writeExchange();
}

# �����Ͽ�����
sub mainExchange {
	local($_);

	if ($HexchangeMode eq 'show') {
		# ����ڡ�����
		htmlExchange();
		return;
	}

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

	readExchange();

	if ($HexchangeMode eq 'add') {
		# ����ɲ�
		if (($HexchangeSell == $HexchangeBuy) ||
			($HexchangeSellCost == 0) ||
			($HexchangeBuyCost == 0)) {
			# ���Ƥ��ְ�äƤ���
			tempExcAddMiss();
		} else {
			# ���Ƥ�������
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
		# �������
		my($exchange);
		foreach $exchange (@HexchangeData) {
			next if (!defined $exchange);
			if ($exchange->{'id'} == $HexchangeBidID) {
				if ($exchange->{'iid'} == $HcurrentID) {
					# ����ΰ��ꤷ�����
					tempExcBidMiss();
				} else {
					# ¾��ΰ��ꤷ�����
					if ($exchange->{'buy_cost'} > $HexchangeSellCost) {
						# �罸����ã���Ƥ��ʤ�
						tempExcBidLimit();
					} elsif ($exchange->{'bid_cost'} >= $HexchangeSellCost) {
						# ¾��˶����餱��
						tempExcBidLow();
					} elsif ($HexchangeCon) {
						# ����ξ�郎��äȤ��ɤ�(��ǧ)
						tempExcBidSuccess();
					} else {
						# ����ξ�郎��äȤ��ɤ�
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
		# ������
		my($exchange);
		foreach $exchange (@HexchangeData) {
			next if (!defined $exchange);
			if ($exchange->{'id'} == $HexchangeDelID) {
				if ($exchange->{'iid'} == $HcurrentID) {
					# ����ΰ��ꤷ�����
					$exchange = undef;
					tempExcDelSuccess();
				} else {
					# ¾��ΰ��ꤷ�����
					tempExcDelMiss();
				}
				last;
			}
		}
	}

	writeExchange();

	# ����ڡ�����
	htmlExchange();
}

# ���ͤ�����罸
sub merchantInviteExchange {
	local($_);

	my($i);
	for ($i = $[; $i <= $#HexchangeMerchantName; $i++) {
	next if (rand(100) >= $HexchangeMerchantPercent[$i]);

	my($sell, $sell_cost, $buy, $buy_cost);
	if ($i == 0) {
		# �����ȹ�
		$sell = 1; # ��������
		$sell_cost = random(8) + 3; # 30���ȥ��100���ȥ�
		$buy  = 0; # �����˾
		$buy_cost  = int($sell_cost * (20 - random(9)) / 10); # 12����/10000�ȥ��20����/10000�ȥ�

		$sell_cost *= 10; # �����μ��ñ�̤�Ĵ��

	} elsif ($i == 1) {
		# �����ȹ�
		$sell = 2; # ���Ф���
		$sell_cost = random(91) + 10; # 100�ȥ��1000�ȥ�
		$buy  = 0; # �����˾
		$buy_cost  = int($sell_cost * (19 - random(9)) / 10); # 11����/10�ȥ��19����/10�ȥ�

	} elsif ($i == 2) {
		# �����ȹ�
		$sell = 3; # ��������
		$sell_cost = random(91) + 10; # 100�Х���1000�Х��
		$buy  = 0; # �����˾
		$buy_cost  = int($sell_cost * (48 - random(23)) / 10); # 26����/10�Х���48����/10�Х��

	} elsif ($i == 3) {
		# ����ȹ�
		$sell = 4; # ʼ�����
		$sell_cost = random(36) + 5; # 50�ȥ��400�ȥ�
		$buy  = 0; # �����˾
		$buy_cost  = $sell_cost * (22 - random(12)); # 110����/10�ȥ��220����/10�ȥ�
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

# ����ԥ塼�����Ȥ���ǡ������������
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

	# �ߥ�������Ϥ�ʬ�˺��
	my($land, $landValue) = ($island->{'land'}, $island->{'landValue'});
	my($x, $y, $n);
L_LAND_BASE:
	for ($y = 0; $y < $HislandSize; $y++) {
		for ($x = 0; $x < $HislandSize; $x++) {
			next if ($land->[$x][$y] != $HlandSea); # ���ʳ��Ϥ��Τޤ�

			# �и��ͺ���Υߥ�������Ϥˤ���
			$land->[$x][$y] = $HlandBase;
			$landValue->[$x][$y] = $HmaxExpPoint;
			last L_LAND_BASE if (++$n >= 20); # 20�ս�ޤǺ��
		}
	}

	return $island;
}

# ������ʺ�ɸ�˥ߥ����빶�⤹�륳�ޥ�ɤ���Ͽ����
sub doMissileFireRandom {
	my($island, $target, $kind, $n) = @_;
	my($x) = int(rand($HislandSize - 2) + 1);
	my($y) = int(rand($HislandSize - 2) + 1);
	
	slideBack($island->{'command'}, 0, $kind, $target, $x, $y, $n);
}


# ����ɲ�����
sub tempExcAddSuccess {
	out(<<END);
${HtagBig_}����μ������Ͽ���ޤ�����${H_tagBig}
END
}

# ����ɲü���
sub tempExcAddMiss {
	out(<<END);
${HtagBig_}����μ����̵�������ƤǤ���${H_tagBig}
END
}
# ��������ǧ
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
${HtagBig_}�������α������ꤷ�ޤ�����${H_tagBig}
<form action="$HthisFile" method="POST">
<table border>
  <tr>
    <th nowrap rowspan="2"><input type="submit" value="��������" name="ExchangeBid2Button"></th>
    <th nowrap>����ֹ�</th>
    <th nowrap>����</th>
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

# ����������
sub tempExcBidSuccess2 {
	out(<<END);
${HtagBig_}����μ���˱��礷�ޤ�����${H_tagBig}
END
}

# �������Ѳ�
sub tempExcBidLimit {
	out(<<END);
${HtagBig_}������̤��罸����ã���Ƥ��ޤ���${H_tagBig}
END
}

# ������綥���餱
sub tempExcBidLow {
	out(<<END);
${HtagBig_}¾�礬�����ɤ����Ǳ��礷�Ƥ��ޤ���${H_tagBig}
END
}

# ������缺��
sub tempExcBidMiss {
	out(<<END);
${HtagBig_}����ϼ���ΰ��ꤷ������Ǥ���${H_tagBig}
END
}

# ����������
sub tempExcDelSuccess {
	out(<<END);
${HtagBig_}����μ���������ޤ�����${H_tagBig}
END
}

# ����������
sub tempExcDelMiss {
	out(<<END);
${HtagBig_}�����¾��ΰ��ꤷ������Ǥ���${H_tagBig}
END
}

# �罸������
sub logExcDead1 {
	my($id, $name, $no) = @_;
	logOut("����ֹ� ${no} ��${HtagName_}${name}��${H_tagName}��<B>̵����</B>�ˤʤä������̵���Ȥʤ�ޤ�����",$id);
}

# ����������
sub logExcDead2 {
	my($id, $name, $no) = @_;
	logOut("����ֹ� ${no} ��${HtagName_}${name}��${H_tagName}��<B>̵����</B>�ˤʤä�������罸��³�Ȥʤ�ޤ�����",$id);
}

# ���꥿������в�
sub logExcLimit {
	my($id, $no) = @_;
	logOut("����ֹ� ${no} �ϱ��礬�ʤ��ä������̵���Ȥʤ�ޤ�����",$id);
}

# �����Ω
sub logExcSuccess {
	my($id, $name, $bid, $bname, $no, $sell, $buy, $auto) = @_;
	$auto = ($auto ? '�ʼ�ư�����' : '�ʼ�ư�����');
	logOut("����ֹ� ${no} ��${HtagName_}${name}${H_tagName}��<B>${sell}</B>��${HtagName_}${bname}${H_tagName}��<B>${buy}</B>��򴹤��뤳�Ȥ���Ω���ޤ�����<B>${auto}</B>",$id, $bid);
}

# �ڥʥ�ƥ�ȯ��
sub logExcPenalty {
	my($id, $bid, $bname, $no, $buy, $penalty) = @_;
	if($HpenaltyExchangeSwitch){
		logOut("����ֹ� ${no} ��${HtagName_}${bname}${H_tagName}��<B>${buy}</B>�����ߤ��ʤ����Ȥ�Ƚ������Ȣ��񸻼���Ѱ���Ǥ�<B>����ȯư($penalty)</B>����ꤷ�ޤ�����",$id, $bid);
	}else{
		logOut("����ֹ� ${no} ��${HtagName_}${bname}${H_tagName}��<B>${buy}</B>�����ߤ��ʤ����Ȥ�Ƚ����������ϹԤ��ޤ���Ǥ�����",$id, $bid);
	}
}


1;
