#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ������ʹԥ⥸�塼��(ver1.02)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# ���ۤ�Ȣ��(ver5.54e)
#----------------------------------------------------------------------
# 2009/08/05 5.54e �����ԻԤ�ȯŸ���ʤ��Х��ȱ����˥å��˲��ǲ��ä��˲��Ǥ���Х�������
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# ������ʹԥ⡼��
#----------------------------------------------------------------------
# �ᥤ��
sub turnMain {
	my ( $i, $j );

	# �ǽ��������֤򹹿�
	if ( $HrepeatTurn > 0 ) {
		if ( $HislandTurn % $HrepeatTurn == ( $HrepeatTurn - 1 ) ) {
			$HislandLastTime += $HunitTime;
		}
	}
	else {
		$HislandLastTime += $HunitTime;
	}

	# ��ɸ�������
	makeRandomPointArray();
	makeRandomOceanPointArray();

	# �������ֹ�
	$HislandTurn++;

	# �������
	$Hmonth = ( $HislandTurn % 12 ) + 1;

	# ���ַ��
	my (@order) = randomArray($HislandNumber);

	# �񸻼���Υڥʥ�ƥ�����
	penaltyExchange();

	$HmonsterSpecial[19] = random(7) + 2;    # ��������°��(2��8)

	if ($Hdishangen) {

		# �ҳ�Ⱦ������Ƴ�����롣
		if ( ( int( $HislandTurn / 100 ) % 2 ) == 0 ) {

			# ��ΨȾ�������ƤǤϤʤ���
			$HdisEarthquake /= 2;
			$HdisTsunami    /= 2;
			$HdisTyphoon    /= 2;
			$HdisMeteo      /= 2;
			$HdisHugeMeteo  /= 2;
			$HdisEruption   /= 2;
			$HdisFire       /= 2;
			$HdisAkasio     /= 2;
			$HdisAEruption  /= 2;
			$HdisPirate     /= 2;
			$HdisPollution  /= 2;
			$HdisMonster    /= 2;
		}
	}

	# ����ˤ����ư
	if ( ( $Hmonth < 4 ) || ( 11 < $Hmonth ) ) {
		$HdisAkasio  = 0;
		$HdisTyphoon = 0;
	}

	# ������ؤ��������Ƥ��ɤ߹���
	readPunishData();

	# ����������ե�����
	for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
		estimateS( $order[$i] );
		$Hislands[ $order[$i] ]->{'oldmoney'} =
		  $Hislands[ $order[$i] ]->{'money'};
		$Hislands[ $order[$i] ]->{'oldfood'} =
		  $Hislands[ $order[$i] ]->{'food'};

		# �����󳫻����ο͸������
		$Hislands[ $order[$i] ]->{'oldPop'} = $Hislands[ $order[$i] ]->{'pop'};
		next if ( $Hislands[ $order[$i] ]->{'predelete'} );
		income( $order[$i], $Hislands[ $order[$i] ] );
	}
	spaceEstimate(0);    # �������

	doCommandLate();     # ������̿��

	# ���ޥ�ɽ���
	for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
		$island = $Hislands[ $order[$i] ];
		next if ( $island->{'predelete'} );

		# �����1�ˤʤ�ޤǷ����֤�
		$Hwflg = 10;     # ŷ���ˤ���ᤷ�κ����(������)
		while ( !doCommand($island) ) { }

		# ���ϥ�(�ޤȤ�ƥ�����)
		logMatome( $island, $HlogOmit2, 'seichi' ) if ($HlogOmit2);
	}

	# Battle Field�ѵ��ۤ��Τ�ե饰
	if ( $HislandTurn > 250 ) {
		$kinoraFlg = 1 if ( ( $HislandTurn % $HturnPrizeUnit ) == 0 );
	}

	$HearthAttack = 0;    # �ϵ并�⤬���줿��
	spaceHex();           # ������Ĺ����
	oceanHex();           # ������Ĺ����
	                      # ��Ĺ�����ñ�إå����ҳ�
	for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
		next if ( $Hislands[ $order[$i] ]->{'predelete'} );
		doEachHex( $Hislands[ $order[$i] ] );
	}

	# �����ν���
	my ($remainNumber) = $HislandNumber;
	my ($island);

	# ���åХȥ륿���������ѿ������
	$MonsBattleTurn   = 2;    # ����Ǥ⣳���ʾ�
	$MonsBattleTurnID = 0;

	(
		$allPop,  $allMoney, $allArea,     $allBank,     $allMissileA,
		$allFarm, $allTower, $allIndustry, $allYousyoku, $allForest
	  )
	  = ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 );

	for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
		$island = $Hislands[ $order[$i] ];
		next if ( $island->{'predelete'} );
		doIslandProcess( $order[$i], $island );

		# ����Ƚ��
		if ( $island->{'dead'} == 1 ) {
			$island->{'pop'} = -100;
			$remainNumber--;
			OceanMente( $island->{'id'} );
		}
		elsif ( ( $island->{'pop'} == 0 ) && ( $island->{'id'} <= 90 ) ) {
			$island->{'dead'} = 1;
			$island->{'pop'}  = -100;
			$remainNumber--;
			OceanMente( $island->{'id'} );

			# ���ǥ�å�����
			my ($tmpid) = $island->{'id'};
			logDead( $tmpid, $island->{'name'} );
		}
	}

	# �񸻼���Υ������������
	turnExchangeBegin();

	# ���ͤ�����򤹤롩
	if ( rand(100) < 100 ) {    # 10%
		merchantInviteExchange();
	}

	# �񸻼���Υ��������
	turnExchange();

	for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
		doIslandProcess2( $Hislands[ $order[$i] ] );
	}

	spaceEstimate(1);           # �������

	# �͸�����������
	for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
		$island = $Hislands[ $order[$i] ];
		$island->{'pop'} += $island->{'popspace'};
		if ( $island->{'pop'} < 1 ) {
			$island->{'rank'} = -100;
		}
		else {
			$island->{'rank'} = $island->{'allex'};
		}
	}

	# ����
	my $allBank2;
	if ( $allBank > 0 ) {
		$allBank2 = "�����¶� ${allBank}000${HunitMoney}";
	}
	else {
		$allBank2 = "";
	}
#	push( @HlogPool,
#"0,$HislandTurn,0,,Ȣ��������ס���͸� ${allPop}${HunitPop}�������� ${allArea}${HunitArea}������ $allMoney${HunitMoney}${allBank2}"
#	);

	if ( ( $HislandTurn % $HturnPrizeVarious ) == 0 ) {

		# �����

		# ����ޤΥ���������פΥ�����
		open( POUT, ">>${HlogdirName}/statistical.log" );
		print POUT
"$HislandTurn,$allPop,$allMoney,$allArea,$allBank,$allMissileA,$allFarm,$allTower,$allIndustry,$allYousyoku,$allForest,$HislandNumber\n";
		close(POUT);

		# ���Ȳ�
		my @idx = ( 0 .. $#Hislands );
		@idx = sort {
			$Hislands[$b]->{'farm'} <=> $Hislands[$a]->{'farm'} || $a <=> $b
		} @idx;
		my $tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'farm'} > 0 ) {
			$tIsland->{'status'} |= 1;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[1] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
		}

		# ���Ȳ�
		@idx = sort {
			$Hislands[$b]->{'industry'} <=> $Hislands[$a]->{'industry'}
			  || $a <=> $b
		} @idx;
		$tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'industry'} > 0 ) {
			$tIsland->{'status'} |= 2;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[2] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
		}

		# ���Ȳ�
		@idx = sort {
			$Hislands[$b]->{'tower'} <=> $Hislands[$a]->{'tower'} || $a <=> $b
		} @idx;
		$tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'tower'} > 0 ) {
			$tIsland->{'status'} |= 4;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[3] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
		}

		# �建��
		@idx = sort {
			$Hislands[$b]->{'yousyoku'} <=> $Hislands[$a]->{'yousyoku'}
			  || $a <=> $b
		} @idx;
		$tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'yousyoku'} > 0 ) {
			$tIsland->{'status'} |= 8;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[4] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
		}

		# ���Ӳ�
		@idx = sort {
			$Hislands[$b]->{'forestV'} <=> $Hislands[$a]->{'forestV'}
			  || $a <=> $b
		} @idx;
		$tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'forestV'} > 0 ) {
			$tIsland->{'status'} |= 16;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[5] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
		}

		# �ߥ����벦
		# ���Ӳ�
		@idx = sort {
			$Hislands[$b]->{'MissileK'} <=> $Hislands[$a]->{'MissileK'}
			  || $a <=> $b
		} @idx;
		$tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'MissileK'} > 0 ) {
			$tIsland->{'status'} |= 32;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[6] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
		}

		# �ϥ�ܥƲ�
		@idx = sort {
			$Hislands[$b]->{'haribote'} <=> $Hislands[$a]->{'haribote'}
			  || $a <=> $b
		} @idx;
		$tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'haribote'} > 0 ) {
			$tIsland->{'status'} |= 64;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[7] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
		}

		# ���ò�
		@idx = sort {
			$Hislands[$b]->{'mons'} <=> $Hislands[$a]->{'mons'} || $a <=> $b
		} @idx;
		$tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'mons'} > 0 ) {
			$tIsland->{'status'} |= 128;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[8] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
		}

		# ������
		@idx = sort {
			$Hislands[$b]->{'oilfield'} <=> $Hislands[$a]->{'oilfield'}
			  || $a <=> $b
		} @idx;
		$tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'oilfield'} > 0 ) {
			$tIsland->{'status'} |= 256;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[9] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
		}

		# �ҳ���
		@idx = sort {
			$Hislands[$b]->{'score2'} <=> $Hislands[$a]->{'score2'}
			  || $a <=> $b
		} @idx;
		$tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'score2'} > 0 ) {
			$tIsland->{'status'} |= 512;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[10] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
			if ( $tIsland->{'score2'} > 3000 ) {

				# �߷�30���ͤ�Ķ���븺
				logEvent( $tIsland->{'id'}, $tIsland->{'name'},
"���ҳ����������¿���ε����Ԥλ�����Ǻҳ����꤬£���ޤ�����"
				);
				$tIsland->{'present'}->[11]++;
			}
		}

		# ������
		@idx = sort {
			$Hislands[$b]->{'ship'} <=> $Hislands[$a]->{'ship'} || $a <=> $b
		} @idx;
		$tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'ship'} > 0 ) {
			$tIsland->{'status'} |= 1024;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[11] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
		}

		# ��ǰ�겦
		@idx = sort {
			$Hislands[$b]->{'monument'} <=> $Hislands[$a]->{'monument'}
			  || $a <=> $b
		} @idx;
		$tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'monument'} > 0 ) {
			$tIsland->{'status'} |= 2048;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[12] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
		}

		# ��ݲ�
		@idx = sort {
			$Hislands[$b]->{'flower'} <=> $Hislands[$a]->{'flower'}
			  || $a <=> $b
		} @idx;
		$tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'flower'} > 0 ) {
			$tIsland->{'status'} |= 8192;
			$tIsland->{'zyuni'} += $HturnPrizePoint;
			logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[14] );
			$tIsland->{'money'} += 2000 if ($HsurvFlg);
		}
	}

	# ���������оݥ�������ä��顢�����ս���
	if (   ( ( $HislandTurn % $HturnPrizeUnit ) == 0 )
		&& ( $MonsBattleTurnID != 0 ) )
	{
		my ($island) = $Hislands[ $HidToNumber{$MonsBattleTurnID} ];
		$island->{'present'}->[10]++;    # ���õ�ǰ��������䤹
		logPrize( $island->{'id'}, $island->{'name'}, "������" );
		logEvent( $island->{'id'}, $island->{'name'},
"�������դ���������õ�ǰ���ץ쥼��Ȥ���ޤ�����"
		);
	}

	# ��Ʈ���֤ؤΰܹ���
	my $tournamentflg = 0;
	if ($Htournament) {

		# �ʰץȡ��ʥ���
		$HislandTurnCount++;
		if ( $HislandFightMode == 1 ) {

			# ͽ��
			if ( $HislandTurn == $HislandChangeTurn ) {

				# ��ȯ������˰ܹ�
				$tournamentflg     = 1;
				$HislandFightMode  = 2;
				$HislandTurnCount  = 0;
				$HislandChangeTurn = $HislandTurn + $HdevelopeTurn;
			}
		}
		elsif ( $HislandFightMode == 2 ) {

			# ��ȯ
			if ( $HislandTurn == $HislandChangeTurn ) {

				# ��Ʈ������˰ܹ�
				$tournamentflg =
				  2;    # ��������������Ͽ͸������ȸ��
				$HislandFightMode = 3;
				$HislandFightCount++;
				$HislandTurnCount = 0;
				if ( $remainNumber > 2 ) {

					# �辡��ʳ��ϡ����֤������
					$HislandLastTime += $HinterTime;
					$HislandChangeTurn = $HislandTurn + $HfightTurn;
				}
				else {

					# �辡��
					$HislandChangeTurn = $HislandTurn + $HfinalTurn;
				}
			}
		}
		elsif ( $HislandFightMode == 3 ) {

			# ��Ʈ
			if ( $HislandTurn == $HislandChangeTurn ) {

				# ���Է��塡��ȯ������˰ܹ�
				$tournamentflg = 3;
				if ( $remainNumber <= 2 ) {

					# ��λ
					$HislandFightMode = 9;
				}
				else {
					$HislandTurnCount = 0;
					$HislandFightMode = 2;
				}
				$HislandChangeTurn = $HislandTurn + $HdevelopeTurn;
				my $HwinIsland     = 0;    # ����������ο�
				my $consolationPop = 0;    # �Լ������о���͸�
				my $consolationID  = 0;    # �Լ������о���ɣ�
				for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
					$island = $Hislands[$i];
					my $HcurrentNumber = $HidToNumber{ $island->{'fight_id'} };
					my $tIsland        = $Hislands[$HcurrentNumber];

					# ��Ʈ��ξ���
					my $reward = $island->{'waste'};
					if (
						(
							    $HcurrentNumber ne ''
							and $island->{'pop'} >= $tIsland->{'pop'}
						)
						or ( $island->{'fight_id'} == -1 )
					  )
					{

						# ����
						my $tPop = 0;
						$HwinIsland++;
						if ( $island->{'fight_id'} > 0 ) {
							logWin( $island->{'id'}, $island->{'name'},
								"����", $reward );
							$tPop = $tIsland->{'pop'};
							$tIsland->{'fight_id'} = 0;
							if ( $consolationPop <= $tPop ) {
								$consolationPop = $tPop;
								$consolationID  = $tIsland->{'id'};
							}
							$tIsland->{'lose'} = 1;
							logOut(
"${HtagName_}$tIsland->{'name'}${AfterName}${H_tagName}��<B>����</B>��",
								$tIsland->{'id'}
							);
						}
						else {

							# ���ﾡ
							logWin( $island->{'id'}, $island->{'name'},
								"���ﾡ" );
						}
						push( @fight_log_flag,
"$island->{'name'},$tIsland->{'name'},$reward,0,$island->{'pop'},0,$tPop,0,$island->{'fight_id'}"
						);
						$island->{'fight_id'} = 0;
					}
					elsif (( $HcurrentNumber eq '' )
						&& ( $island->{'fight_id'} > 0 ) )
					{
						$HwinIsland++;
						logWin( $island->{'id'}, $island->{'name'}, "����",
							$reward );
						push( @fight_log_flag,
"$island->{'name'},,$reward,0,$island->{'pop'},0,0,0,-2"
						);
						$island->{'fight_id'} = 0;
					}
					$island->{'reward'} = 0;
				}

				# ���ष����ν���
				$consolationName = "";
				if ( $HislandFightMode != 9 ) {

					# ��λ���ʳ�
					for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
						$island = $Hislands[$i];
						if ( $island->{'lose'} ) {
							if (   ( $consolationID == $island->{'id'} )
								&& ( ( $HwinIsland % 2 ) != 0 )
								&& ($HconsolationMatch) )
							{

		 # �Լ������о���Ǽ������ξ����Լ�����⡼��
								$consolationName =
"${HtagName_}$island->{'name'}${AfterName}${H_tagName}��<B>�Լ����衪</B>";
								logOut( $consolationName, $island->{'id'} );
							}
							else {
								logHistory(
"${HtagName_}$island->{'name'}${AfterName}${H_tagName}��<B>���������</B>��"
								);
								$island->{'pop'} = 0;
								$remainNumber--;
								OceanMente( $island->{'id'} );
							}
						}
					}
				}
			}
		}
	}

	#------------------------------------------------

	# �͸���˥�����
	# �͸���Ʊ���Ȥ���ľ���Υ�����ν��֤Τޤ�
	my @idx = ( 0 .. $#Hislands );
	@idx =
	  sort { $Hislands[$b]->{'pop'} <=> $Hislands[$a]->{'pop'} || $a <=> $b }
	  @idx;
	@Hislands = @Hislands[@idx];

	islandReki();

	# ���������оݥ�������ä��顢���ν���
	if ( ( $HislandTurn % $HturnPrizeUnit ) == 0 ) {
		my ($island) = $Hislands[0];
		logPrize( $island->{'id'}, $island->{'name'},
			"$HislandTurn${Hprize[0]}" );
		$island->{'prize'} .= "${HislandTurn},";
	}
	if ($Htournament) {

		# �ʰץȡ��ʥ���
		if ( $tournamentflg == 1 ) {

			# ͽ����������פ�����
			while ( $remainNumber > $HfightMem ) {
				$remainNumber--;
				unshift( @yosen_log,
"$Hislands[$remainNumber]->{'pop'},$Hislands[$remainNumber]->{'name'}"
				);
				logLoseOut(
					$Hislands[$remainNumber]->{'id'},
					$Hislands[$remainNumber]->{'name'}
				);
				OceanMente( $Hislands[$remainNumber]->{'id'} );
			}
		}
		elsif ( $tournamentflg == 2 ) {

			# �������������
			my ( $l, $r );
			$r = $remainNumber - 1;
			for ( $l = 0 ; $l <= $r ; $l++, $r-- ) {
				if ( $Hislands[$r]->{'id'} == $Hislands[$l]->{'id'} ) {

					# ���ﾡ
					$Hislands[$r]->{'fight_id'} = -1;
				}
				else {
					$Hislands[$l]->{'fight_id'} = $Hislands[$r]->{'id'};
					$Hislands[$r]->{'fight_id'} = $Hislands[$l]->{'id'};
				}
			}
		}
	}
	else {

		# ��᤿������ֳ֤Ǻǲ��̤���������
		if ($HsurvFlg) {
			if (   ( $HislandTurn > $Hsstartturn )
				&& ( ( ( $HislandTurn - $Hsstartturn ) % $Hsurvivalturn ) == 0 )
			  )
			{
				if ( $remainNumber > 1 ) {
					$remainNumber--;
					logDead2(
						$Hislands[$remainNumber]->{'id'},
						$Hislands[$remainNumber]->{'name'}
					);
					OceanMente( $Hislands[$remainNumber]->{'id'} );
				}
			}
		}
	}

	# ������å�
	$HislandNumber = $remainNumber;

	# �ر� �����Ϥ���������
	if ($Hallyflg) {
		my ( $ctpop, %allyCount, %allyPop, %allyArea, %allyGnp, %allyPow );
		$ctpop = 0;
		for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
			$island = $Hislands[$i];
			next if ( $island->{'id'} > 90 );
			$ally = $island->{'ally'};
			$allyCount{$ally}++;
			$allyPop{$ally}  += $island->{'pop'};
			$ctpop           += $island->{'pop'};
			$allyArea{$ally} += $island->{'area'};
			$allyGnp{$ally}  +=
			  $island->{'money'} +
			  int( ( $island->{'food'} / 10 ) + ( $island->{'ore'} * 1.2 ) +
				  ( $island->{'oil'} * 2.6 ) + ( $island->{'weapon'} * 7 ) );
			$allyPow{$ally} +=
			  $island->{'MissileK'} * 200 + $island->{'weapon'};
			$prize = $island->{'prize'};
			$prize =~ /([0-9]*),([0-9]*),(.*)/;
			$allyPow{$ally} += 3000 if ( $1 & 512 );
		}
		if ( ( $HislandTurn % $HturnPrizeVarious ) == 0 ) {
			my $aturn = $HislandTurn - $HturnPrizeVarious;
			rename( "${HlogdirName}/ally.log", "${HlogdirName}/ally.$aturn" );
		}
		foreach ( sort { $allyPop{$b} <=> $allyPop{$a} } keys %allyPop ) {
			if ( $allyPop{$_} > 0 ) {

				my $w = int( $allyPop{$_} * 10000 / $ctpop + 0.5 ) / 100;
				open( AOUT, ">>${HlogdirName}/ally.log" );

# ������,�ر�ID,���,��͸�,������,��к���,������,��ͭΨ
				print AOUT
"$HislandTurn,$_,$allyCount{$_},$allyPop{$_},$allyArea{$_},$allyGnp{$_},$allyPow{$_},$w\n";
				close(AOUT);
			}
		}
	}

	# �Хå����åץ�����Ǥ���С�������rename
	if ( ( $HislandTurn % $HbackupTurn ) == 0 ) {
		my ($tmp) = $HbackupTimes - 1;
		myrmtree("${HdirName}.bak$tmp");
		for ( $i = ( $HbackupTimes - 1 ) ; $i > 0 ; $i-- ) {
			$j = $i - 1;
			rename( "${HdirName}.bak$j", "${HdirName}.bak$i" );
		}
		rename( "${HdirName}", "${HdirName}.bak0" );
		mkdir( "${HdirName}", $HdirMode );
		rename( "${HdirName}.bak0/fight.log", "${HdirName}/fight.log" );
	}

	# �񸻼���Υ�������������
	turnExchangeEnd();

	if ($Htournament) {

		# �ʰץȡ��ʥ���
		if ( $tournamentflg == 3 ) {
			fihgt_log();
		}
		elsif ( $tournamentflg == 1 ) {
			log_yosen();
		}
	}

	# �ե�����˽񤭽Ф�
	if ( !writeIslandsFile( -1, 0 ) ) {
		if ( ( $HislandTurn % $HbackupTurn ) == 0 ) {
			rmdir("${HdirName}");
			rename( "${HdirName}.bak0", "${HdirName}" );
		}
		unlock();
		tempFailWrite();
		return;
	}

	# ���ե��������ˤ��餹
	for ( $i = ( $HlogMax - 1 ) ; $i >= 0 ; $i-- ) {
		$j = $i + 1;
		unlink("${HlogdirName}/hakojima.log$j");
		rename( "${HlogdirName}/hakojima.log$i",
			"${HlogdirName}/hakojima.log$j" );
	}

##### �ɲ� ����20020307
	if ($Hperformance) {
		my ( $uti, $sti, $cuti, $csti ) = times();
		$uti += $cuti;
		$sti += $csti;
		my ($cpu) = $uti + $sti;

# ���ե�����񤭽Ф�(�ƥ��ȷ�¬�ѡ����ʤϥ����Ȥˤ��Ƥ����Ƥ�������)
#		open(POUT,">>cpu-t.log");
#		print POUT "CPU($cpu) : user($uti) system($sti)\n";
#		close(POUT);

#		push( @HlogPool,
#"0,$HislandTurn,0,,<SMALL>��ٷ�¬ CPU($cpu) : user($uti) system($sti)</SMALL>"
#	);
	}
#####

	# ���񤭽Ф�
	logFlush();

	# ��Ͽ��Ĵ��
	logHistoryTrim( "hakojima.his", $HhistoryMax );
	logHistoryTrim( "weather.his",  $HWeatherMax );

	# �ȥåפ�
	topPageMain();
}

# ������ؤ��������Ƥ��ɤ߹���
sub readPunishData {
	if ( open( Fpunish, "<${HdirName}/punish.dat" ) ) {
		local (@_);
		my ($island);
		while (<Fpunish>) {
			chomp;
			@_ = split(',');
			my ($obj);
			$obj->{turn}               = shift;
			$obj->{id}                 = shift;
			$obj->{punish}             = shift;
			$obj->{x}                  = shift;
			$obj->{y}                  = shift;
			$HpunishInfo{ $obj->{id} } = $obj;
		}
		close(Fpunish);
	}

	# ���ۥǡ�����������
	unlink("${HdirName}/punish.dat");
}

# ����������ե�����
sub income {
	my ( $number, $island ) = @_;

	my ( $name, $id, $land, $landValue, $p, $r ) = (
		$island->{'name'}, $island->{'id'}, $island->{'land'},
		$island->{'landValue'},
		1, random(1000)
	);

	if ( $island->{'id'} > 90 ) {

		# Battle Field�ΤȤ�
	}
	else {
		my ( $pop, $farm, $factory, $oilfactory, $port, $tower, $mountain ) = (
			$island->{'pop'},
			( $island->{'farm'} * 10 ) + $island->{'yousyoku'},
			$island->{'factory'},
			int( $island->{'oilfactory'} / 3 ),
			$island->{'port'},
			$island->{'tower'},
			$island->{'mountain'}
		);
		$pop -=
		  $island->{
			'slum'};    # ����೹�οͤ�ϫƯ�ϼ����ˤʤ�ʤ���

		my ( $wkind, $wname, $whp, $wkind2, $wkind3 ) =
		  weatherinfo( $island->{'weather'} );
		if ( ( $r < $HdisVGHarvest ) && ( $whp > 1 ) && ( $whp < 8 ) ) {
			logEvent2( $id, $name, '��˭��', '�Ǥ�' );
			$p = 4;
		}
		elsif (( $r < $HdisGHarvest + $HdisVGHarvest )
			&& ( $whp > 1 )
			&& ( $whp < 8 ) )
		{
			logEvent2( $id, $name, '˭��', '�Ǥ�' );
			$p = 2;
		}
		elsif ( $r < $HdisBHarvest + $HdisGHarvest + $HdisVGHarvest ) {
			logEvent2( $id, $name, '����', '�Ǥ�' );
			$p = 0;
		}

		$island->{'turnsu'}++;    #���ͭ�Υ������

		#w		if($HwarFlg){
		#w			# �����
		#w			$island->{'evil'} = 10;
		#w		}elsif($island->{'MissileK'} == 0){ # �ߥ���������ͭ��

		if ( $island->{'MissileK'} == 0 ) {    # �ߥ���������ͭ��
			$island->{'evil'} -=
			  2;    # 0�λ��ϥ�������˴ط��ʤ��ݸ��ˤʤ�
			$island->{'evil'} = 0 if ( $island->{'evil'} < 0 );
		}
		elsif ( $island->{'evil'} < 10 ) {
			$island->{'evil'} = 10;
		}
		if ( $island->{'evil'} > 10000 ) {
			$island->{'evil'} -= 1000;
			$island->{'gold'} = 1;    # �����
		}
		elsif ( $island->{'evil'} > 300 ) {
			$island->{'evil'} = 300;
		}

# �ݸ��ǽ�����������ʾ������Ͽ̤γ�Ψ����������գФ���
		$island->{'prepare2'}++
		  if ( ( $island->{'evil'} == 0 ) && ( $island->{'zyuni'} >= 40 ) );

		# ����
		if ( $number < 5 ) {

			# ��̤˥ܡ��ʥ�
			$island->{'money'} += 100 - $number * 20 if ( $HislandTurn > 100 );
		}

		# ��̤�������û���
		$island->{'zyuni'} += 10 - $number if ( $number < 10 );

	  # ���������оݥ�������ä��顢������ꥻ�åȤ��롣
		$island->{'zyuni'} = 0 if ( ( $HislandTurn % $HturnPrizeUnit ) == 0 );

		# �͸�10��̤���λ��Ͼ��ȥӥ�ϰ�̣��̵��
		$tower = 0 if ( $pop < 1000 );

		if ( $factory < $port ) {

			# ��������������¿����
			$factory += $factory;
		}
		else {
			$factory += $port;    # �����ͤ򹩾���ͤˤ���
		}
		if ( $island->{'order'} & 32 ) {

			# �η���ϻ�����������
			$tower += $mountain;
			$mountain = 0;
		}
		if ( $island->{'order'} & 128 ) {

			# ����ϻ�����������
			$tower += $factory;
			$factory = 0;
		}
		if ( $pop > $farm ) {
			$island->{'food'} += $farm * $p;    # ����ե��Ư
			$pop -= $farm;
			if ( $pop > $mountain * 10 ) {

				# ����
				$island->{'ore'} += $mountain;
				$pop -= $mountain * 10;
				if (   ( $pop > $oilfactory * 30 )
					&& ( $island->{'ore'} > $oilfactory ) )
				{

					# ��������
					$island->{'ore'} -= $oilfactory;
					$island->{'oil'} += $oilfactory;
					$pop -= $oilfactory * 30;
				}
				if ( $pop > $factory * 10 ) {

					# ʼ��
					$factory = $island->{'ore'}
					  if ( $island->{'ore'} < $factory );
					$factory = $island->{'oil'}
					  if ( $island->{'oil'} < $factory );
					$island->{'ore'} -= $factory;
					$island->{'oil'} -= $factory;
					$island->{'weapon'} += $factory;

					# ���
					$island->{'money'} +=
					  min( int( ( $pop - $factory ) / 10 ), $tower );
				}
				else {
					$island->{'money'} += int( $pop / 10 );
				}
			}
			else {
				$island->{'ore'} += int( $pop / 10 );
			}
		}
		else {
			$island->{'food'} += $pop * $p;    # �������ɻŻ�
		}

		# ��������
		$island->{'food'} =
		  int( ( $island->{'food'} ) - ( $island->{'pop'} * $HeatenFood ) );
	}

	# �������ư
	if ( $island->{'smons'} > 0 ) {
		my ( $x, $y );
		for ( $p = 0 ; $p < $HpointNumber ; $p++ ) {
			$x = $Hrpx[$p];
			$y = $Hrpy[$p];
			if ( $land->[$x][$y] == $HlandMonster ) {
				my ( $mKind, $mName, $mHp ) =
				  monsterSpec( $landValue->[$x][$y] );
				my ($special) = $HmonsterSpecial[$mKind];
				if ( ( $special == 6 ) || ( $special == 7 ) ) {
					monmove( $island, $x, $y, 0 );
					last if ( $special == 6 );
				}
			}
		}
	}

	# ���Ϥ�������Ϥʤ餷����(�Ϥʤ餷�ο��ͻ��ꣲ��)
	my ( $comArray, $command, $cNo, $i, $sx, $sy );
	for ( $cNo = 0 ; $cNo < $HcommandMax ; $cNo++ ) {
		$comArray = $island->{'command'};
		$command  = $comArray->[$cNo];
		next if ( $command->{'kind'} == $HcomSpecialSPP );
		if (   ( $command->{'kind'} == $HcomPrepare2 )
			&& ( $command->{'arg'} == 22 ) )
		{
			slideFront( $island->{'command'}, $cNo );    # �ʹߤ�ͤ��
			for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
				$sx = $Hrpx[$i];
				$sy = $Hrpy[$i];
				slideBack( $island->{'command'}, $cNo, $HcomPrepare2, $id, $sx,
					$sy, 0 )
				  if ( ( $land->[$sx][$sy] == $HlandWaste )
					&& ( $landValue->[$sx][$sy] <= 1 ) );
			}
		}
		last;
	}

	#	for($cNo = 0; $cNo < $HcommandMax; $cNo++){
	#		$comArray = $island->{'command'};
	#		$command = $comArray->[$cNo];
	#		HdebugOut($id . "=" . $command->{'kind'});
	#	}
}    # income

# ���ޥ�ɥե�����
sub doCommand {
	my ($island) = @_;

	# ���ޥ�ɼ��Ф�(ŷ��������ߤ��줿̿��϶���)
	my ( $comArray, $command, $cNo );
	for ( $cNo = 0 ; $cNo < $HcommandMax ; $cNo++ ) {
		$comArray = $island->{'command'};
		$command  = $comArray->[$cNo];
		last if ( $command->{'flg'} <= 0 );
	}

	if ($Htournament) {

		# �ʰץȡ��ʥ���
		my $tName = $HidToName{ $island->{'fight_id'} };
		if ( $tName eq '' ) {

			# ̵��
			$command->{'target'} = $island->{'id'};
		}
		elsif ( $command->{'target'} != $island->{'id'} ) {
			$command->{'target'} = $island->{'fight_id'};
		}
	}

	# �����Ǥμ��Ф�
	my ( $name, $id, $land, $landValue ) = (
		$island->{'name'}, $island->{'id'},
		$island->{'land'}, $island->{'landValue'}
	);
	my ( $kind, $target, $x, $y, $arg, $x2, $y2 ) = (
		$command->{'kind'}, $command->{'target'}, $command->{'x'},
		$command->{'y'},    $command->{'arg'},    $command->{'tx'},
		$command->{'ty'}
	);

	if ( $Htournament == 2 ) {

		# �ʰץȡ��ʥ��Ȳ����դ�
		if ( $HislandFightMode == 3 ) {

			# ������
			my ($tn) = $HidToNumber{ $island->{'fight_id'} };
			if ( $tn ne '' ) {

		# $id,$name,$tId,$sId,$mId,$hp,$mhp,$str,$def,$agi,$skl,$winh,$win,$lose
				my ($tIsland) = $Hislands[$tn];
				if (   $tIsland->{'monster'}->[0] == $island->{'fight_id'}
					|| $tIsland->{'monster'}->[2] == 0 )
				{

					# ��꤬����Ȥ��ϡ�����˱������롣
					logMonsENSEI( $id, $name, $island->{'fight_id'},
						$tIsland->{'name'}, "���ñ���" );
					$island->{'monster'}->[0]  = $island->{'fight_id'};
					$island->{'monster'}->[2]  = $island->{'fight_id'};
					$tIsland->{'monster'}->[2] = $id;
				}
			}
		}
		else {

			# ű�ࡩ
		}
		if (   $kind == $HcomMonsEgg
			|| $kind == $HcomMonsEnsei
			|| $kind == $HcomMonsTettai
			|| $kind == $HcomMonsEsaAid
			|| $kind == $HcomMonsAid
			|| $kind == $HcomMonsSell )
		{

			# �嵭��̿��ϤǤ��ʤ�
			return 0;
		}
	}

	# ���˥ߥ�������ä���
	if (
		(
			   ( ( $kind >= 18 ) && ( $kind <= 24 ) )
			|| ( ( $kind >= 26 ) && ( $kind <= 27 ) )
			|| ( ( $kind >= 45 ) && ( $kind <= 109 ) )
			|| ( $kind >= 140 )
		)
		&& ( $island->{'Afmissile'} >= 1 )
	  )
	{
		return 1;
	}

	# ��̱�ϣ�������ˣ���ޤǡ�
	return 1
	  if ( ( $kind == $HcomEmigration ) && ( $island->{'AfEmigra'} == 1 ) );

	if (
		( $kind != $HcomSpecialSPP )
		&&    # ������Ƥ���ˤ��SPP�ǤϤʤ�
		( $island->{'order'} & 16 ) &&    # ��������ͶƳ������
		( $island->{'monsmgmflg'} == 1 )
	  )
	{                                     # ���ä�����(������)
		                                  # ��������ͶƳ��
		$island->{'monsmgmflg'} = 0;
		( $kind, $target, $x, $y, $arg, $x2, $y2 ) =
		  ( $HcomMissileMGM, $island->{'id'}, 0, 0, 1, 0, 0 );
	}
	else {
		return 1
		  if ( ( $command->{'kind'} == $HcomPrepare2 )
			&& ( $command->{'arg'} == 22 ) );
		slideFront( $comArray, $cNo );    # �ʹߤ�ͤ��
	}

	# �ü�̿��
	my $kind2;
	if ( $kind == $HcomSpecialSPP ) {

		# ������Ƥ���ˤ��SPP
		if (   ( $island->{'turnsu'} + $island->{'evil'} < $HdisUN )
			|| ( $island->{'evil'} == 0 )
			|| ( $island->{'monsship'} < 1 ) )
		{

			# ��Ϣ�ݸ������Ƥ����¸�ߤ��ʤ����ϥ��å�
			return 0;
		}
		$kind  = $HcomMissileSPP;
		$kind2 = $HcomSpecialSPP;
	}

	if (   ( $kind == $HcomOMissilePP )
		|| ( $kind == $HcomOMissileSPP )
		|| ( $kind == $HcomOMissileNM ) )
	{

		# �����
		$x  = $HoceanSize - 1 if ( $x >= $HoceanSize );
		$y  = $HoceanSize - 1 if ( $y >= $HoceanSize );
		$x2 = $HoceanSize - 1 if ( $x2 >= $HoceanSize );
		$y2 = $HoceanSize - 1 if ( $y2 >= $HoceanSize );
	}
	else {
		$x  = $HislandSize - 1 if ( $x >= $HislandSize );
		$y  = $HislandSize - 1 if ( $y >= $HislandSize );
		$x2 = $HislandSize - 1 if ( $x2 >= $HislandSize );
		$y2 = $HislandSize - 1 if ( $y2 >= $HislandSize );
	}

	# Ƴ����
	my ( $landKind, $lv, $cost, $comName, $point ) = (
		$land->[$x][$y],  $landValue->[$x][$y], $HcomCost[$kind],
		$HcomName[$kind], "($x, $y)"
	);
	my ($landName) = landName( $landKind, $lv );

	if (
		( $id != $target )
		&& (   ( ( $kind >= 50 ) && ( $kind <= 90 ) )
			|| ( $kind >= 140 )
			|| ( $kind == $HcomWarp ) )
		&& ( $HislandTurn - $island->{'kaisi'} <= $Hatkturn )
	  )
	{
		logMiss( $id, $name, $comName,
"$Hatkturn������δ֡�����ϥ��ޥ�ɤϼ���ʳ��ػߤ���Ƥ���"
		);
		return 0;
	}

	if (   ( $kind <= 19 )
		|| ( ( $kind >= 21 )  && ( $kind <= 23 ) )
		|| ( ( $kind >= 25 )  && ( $kind <= 46 ) )
		|| ( $kind == 75 )
		|| ( $kind == 100 )
		|| ( $kind == 113 )
		|| ( ( $kind >= 92 )  && ( $kind <= 97 ) )
		|| ( ( $kind >= 104 ) && ( $kind <= 111 ) )
		|| ( ( $kind >= 116 ) && ( $kind <= 142 ) ) )
	{

		# �������åȤ��ط��ʤ�̿��ΤȤ�
	}
	else {
		if ( $HdefenceHex[$target] == 1 ) {
			logOut(
"${HtagName_}$name$AfterName${H_tagName}��${HtagComName_}$comName${H_tagComName}�ϡ���ɸ�������ѡ�������ɥ����ƥࣲȯư��Τ��Ἲ�Ԥ��ޤ�����",
				$id, $target
			);
			return 1;
		}
		if ( $target > 90 ) {

			# Battle Field�ΤȤ�
			if (   ( $kind < 50 )
				|| ( $kind == $HcomMissileNM )
				|| ( $kind == $HcomMissilePP )
				|| ( $kind == $HcomSendMonster )
				|| ( $kind == $HcomEmigration ) )
			{

				# ���Ĥ��줿̿��
			}
			else {
				logMiss( $id, $name, $comName,
					"�������åȤ�Battle Field��" );
				return 0;
			}
		}
	}

	if ( $kind == $HcomDoNothing ) {

		# ��ⷫ��
		$island->{'turnsu'}--;

		#	logDoNothing($id, $name, $comName);
		$island->{'money'} += 10;
		$island->{'absent'}++;

		# ��ư����
		if ( $island->{'absent'} >= $HgiveupTurn ) {
			$comArray->[0] = {
				'kind'   => $HcomGiveup,
				'target' => 0,
				'x'      => 0,
				'y'      => 0,
				'arg'    => 0,
				'tx'     => 0,
				'ty'     => 0
			};
		}
		return 1;
	}

	$island->{'absent'} = 0;

	# �����ȥ����å�
	if ( $cost > 0 ) {

		# ��ξ��
		if ( $island->{'money'} < $cost ) {
			logMiss( $id, $name, $comName, "�����­��" );
			return 0;
		}
	}
	elsif ( $cost < 0 ) {

		# �����ξ��
		if ( $island->{'food'} < ( -$cost ) ) {
			logMiss( $id, $name, $comName, "���߿�����­��" );
			return 0;
		}
	}

	# ���ޥ�ɤ�ʬ��
	if ( ( $kind == $HcomPrepare ) || ( $kind == $HcomPrepare2 ) ) {

		# ���ϡ��Ϥʤ餷
		if (   ( $landKind == $HlandSea )
			|| ( ( $landKind == $HlandOil ) && ( $lv == 0 ) )
			|| ( $landKind == $HlandOsen )
			|| ( $landKind == $HlandMountain )
			|| ( $landKind == $HlandMonster )
			|| ( $landKind == $HlandKInora )
			|| ( $landKind == $HlandBreakwater )
			|| ( $HseaChk[$landKind] == 2 ) )
		{

	  # �������ġ��������á������ھ����Ϥ����ϤǤ��ʤ�
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
		if (   ( $landKind == $HlandOil )
			|| ( $landKind == $HlandSbase )
			|| ( $landKind == $HlandSMonument ) )
		{
			$land->[$x][$y] = $HlandSea;
		}
		else {
			$land->[$x][$y] = $HlandPlains;  # ��Ū�ξ���ʿ�Ϥˤ���
		}
		$landValue->[$x][$y] = 0;

		if ($HlogOmit2) {
			my $sno = $island->{'seichi'};
			$island->{'seichi'}++;
			if ( $HlogOmit2 == 1 ) {
				my $seichipnt;
				( $seichipnt->{x}, $seichipnt->{y}, $seichipnt->{z} ) =
				  ( $x, $y, '����' );
				$island->{'seichipnt'}->[$sno] = $seichipnt;
			}
		}
		else {
			logLandSuc( $id, $name, '����', $point );
		}

		# ��򺹤�����
		$island->{'money'} -= $cost;

		if ( $kind == $HcomPrepare2 ) {

			# �Ϥʤ餷
			$island->{'prepare2'}++;
			return 0;
		}
		else {

			# ���Ϥʤ顢��¢��β�ǽ������
			if ( random(1000) < $HdisMaizo ) {
				my ($v) = 100 + random(901);
				$island->{'money'} += $v;
				logMaizo( $id, $name, $comName, $v );
			}
			return 1;
		}
	}
	elsif ( ( $kind == $HcomReclaim ) || ( $kind == $HcomReclaim2 ) ) {

		# ���Ω�ơ���®���Ω��

		# �����Φ�����뤫�����å�
		my ($seaCount) = seaAround( $land, $x, $y, 7 );

		if (   ( $landKind == $HlandPlains )
			&& ( $seaCount == 0 )
			&& ( $kind == $HcomReclaim )
			&& ( countAround( $land, $x, $y, $HlandMountain, 7 ) > 1 )
			&& ( chkAround( $land, $x, $y, $HlandFuji, 7 ) == 0 ) )
		{

# ʿ�ϤǼ��ϣ��إ����˻������İʾ�ǡ����Ϥ˳��ϡ��ٻλ���̵���Ϸ������Ω��(��®�Ϥ���)�ǡ��ٻλ����Ǥ��롪��
			$land->[$x][$y]      = $HlandFuji;
			$landValue->[$x][$y] = 0;
			fujiAround( $land, $landValue, $x, $y, 0 );
			$island->{'money'} -= $cost;
			logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��${HtagComName_}�ٻλ�¤��${H_tagComName}���Ԥ��ޤ�������ǡ�Ȥ��Ƽ��Ϥ����פ�δ�����ٻλ��ˤʤ�ޤ�����",
				$id
			);
			return 1;
		}

		if ( $HseaChk[$landKind] == 0 || $HseaChk[$landKind] == 2 ) {

		 # ����������ϡ����ġ������餷�����Ω�ƤǤ��ʤ�
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}

		if ( $seaCount == 7 ) {

			# ���������������Ω����ǽ
			logNoLandAround( $id, $name, $comName, "Φ��", $point );
			return 0;
		}

		if (   ( $landKind == $HlandSea ) && ( $lv >= 1 )
			|| ( $landKind == $HlandBreakwater ) && ( $lv >= 1 ) )
		{

			# ������������ξ��
			# ��Ū�ξ�����Ϥˤ���
			$land->[$x][$y]      = $HlandWaste;
			$landValue->[$x][$y] = 0;
			$island->{'area'}++;

			if ( $seaCount <= 4 ) {

				# ����γ���3�إå�������ʤΤǡ������ˤ���
				my ( $i, $sx, $sy );
				for ( $i = 1 ; $i < 7 ; $i++ ) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];
					$sx--
					  if ( !( $sy % 2 ) && ( $y % 2 ) )
					  ;    # �Ԥˤ�����Ĵ��
					if (   ( $sx < 0 )
						|| ( $sx >= $HislandSize )
						|| ( $sy < 0 )
						|| ( $sy >= $HislandSize ) )
					{
					}
					else {

						# �ϰ���ξ��
						$landValue->[$sx][$sy] = 1
						  if ( $land->[$sx][$sy] == $HlandSea );
					}
				}
			}
		}
		else {

			# ���ʤ顢��Ū�ξ��������ˤ���
			$land->[$x][$y]      = $HlandSea;
			$landValue->[$x][$y] = 1;
		}
		if ($HlogOmit2) {
			my $sno = $island->{'seichi'};
			$island->{'seichi'}++;
			if ( $HlogOmit2 == 1 ) {
				my $seichipnt;
				( $seichipnt->{x}, $seichipnt->{y}, $seichipnt->{z} ) =
				  ( $x, $y, '���Ω��' );
				$island->{'seichipnt'}->[$sno] = $seichipnt;
			}
		}
		else {
			logLandSuc( $id, $name, $comName, $point );
		}

		# ��򺹤�����
		$island->{'money'} -= $cost;
		if ( $kind == $HcomReclaim2 ) {

			# ��®
			$island->{'prepare2'} += 4;

			# ��������񤻤�
			return 0;
		}
		else {
			return 1;
		}
	}
	elsif ( ( $kind == $HcomDestroy ) || ( $kind == $HcomDestroy2 ) ) {

		# ����
		if (   ( $landKind == $HlandSbase )
			|| ( $landKind == $HlandOil )
			|| ( $landKind == $HlandMonster )
			|| ( $landKind == $HlandKInora )
			|| ( $HseaChk[$landKind] == 2 ) )
		{

			# ������ϡ����ġ����á����ϤϷ���Ǥ��ʤ�
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}

		if ( $kind == $HcomDestroy ) {
			if (
				   ( ( $landKind == $HlandSea ) && ( $lv == 0 ) )
				|| ( ( $landKind == $HlandPlains ) && ( $arg != 0 ) )
				|| ( ( $landKind == $HlandTown )   && ( $arg != 0 ) )
				|| (   ( $landKind == $HlandWaste )
					&& ( $lv <= 1 )
					&& ( $arg != 0 ) )
			  )
			{

# ���ʤ顢����õ�� ʿ�ϡ�Į�����Ϥǲ����������ϲ����򷡤�
# ���۷���
				$arg = 1 if ( $arg == 0 );
				my ( $value, $str, $p );
				$value = min( $arg * ($cost), $island->{'money'} );
				$str   = "$value$HunitMoney";
				$p     = int( $value / $cost );
				$p     = 50 if ( $p > 50 );                          # �ǹ�50%
				$island->{'money'} -= $p * $cost;

				if ( $landKind == $HlandSea ) {

					# ���Ĥ��뤫Ƚ��
					if ( $p > random(100) ) {

						# ���ĸ��Ĥ���
						logChosa( $id, $name, $point, $comName, $str,
							"��<B>����</B>���������Ƥ���" );
						$land->[$x][$y]      = $HlandOil;
						$landValue->[$x][$y] = 0;
						$island->{'oilfield'}++;
					}
					else {

						# ̵�̷���˽����
						logChosa( $id, $name, $point, $comName, $str,
							"�ޤ����������Ĥϸ��Ĥ���ޤ����"
						);
					}
				}
				elsif ( $p +
					( countAround( $land, $x, $y, $HlandMountain, 7 ) * 10 ) >
					random(100) )
				{

					# �������Ĥ���
					logChosa( $id, $name, $point, $comName, $str,
						"��<B>����</B>���������Ƥ���" );
					$land->[$x][$y]      = $HlandWaste;
					$landValue->[$x][$y] = 20 + random( $p + 41 );
				}
				else {

					# ̵�̷���˽����
					logChosa( $id, $name, $point, $comName, $str,
"�ޤ������������ϸ��Ĥ��餺���Ϥˤʤ��"
					);
					$land->[$x][$y]      = $HlandWaste;
					$landValue->[$x][$y] = 1;
				}
				return 1;
			}
		}

   # ��Ū�ξ��򳤤ˤ��롣���ʤ���Ϥˡ������ʤ鳤�ˡ�
		if ( $landKind == $HlandMountain ) {
			$land->[$x][$y]      = $HlandWaste;
			$landValue->[$x][$y] = 0;
		}
		elsif (( $landKind == $HlandSea )
			|| ( $landKind == $HlandBreakwater )
			|| ( $landKind == $HlandSMonument ) )
		{
			$land->[$x][$y]      = $HlandSea;
			$landValue->[$x][$y] = 0;
		}
		else {
			$land->[$x][$y]      = $HlandSea;
			$landValue->[$x][$y] = 1;
			$island->{'area'}--;
		}
		if ($HlogOmit2) {
			my $sno = $island->{'seichi'};
			$island->{'seichi'}++;
			if ( $HlogOmit2 == 1 ) {
				my $seichipnt;
				( $seichipnt->{x}, $seichipnt->{y}, $seichipnt->{z} ) =
				  ( $x, $y, '����' );
				$island->{'seichipnt'}->[$sno] = $seichipnt;
			}
		}
		else {
			logLandSuc( $id, $name, $comName, $point );
		}

		# ��򺹤�����
		$island->{'money'} -= $cost;
		if ( $kind == $HcomDestroy2 ) {

			# ��®
			$island->{'prepare2'} += 4;
			return 0;
		}
		else {
			return 1;
		}
	}
	elsif ( $kind == $HcomSellTree ) {

		# Ȳ��
		if ( $landKind == $HlandForest ) {

			# ���λ���ʿ�Ϥˤ���
			$land->[$x][$y]      = $HlandPlains;
			$landValue->[$x][$y] = 0;
		}
		elsif ( ( $landKind == $HlandSea ) && ( $lv >= 10 ) ) {

			# �ܿ���λ��������ˤ���
			$land->[$x][$y]      = $HlandSea;
			$landValue->[$x][$y] = 1;
			$comName             = '�����';
		}
		else {

			# Ȳ�ΤǤ��ʤ���
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
		logLandSuc( $id, $name, $comName, $point );

		# ��Ѷ������
		$island->{'money'} += $HtreeValue * $lv;
		return 0;
	}
	elsif (( $kind == $HcomPlant )
		|| ( $kind == $HcomFarm )
		|| ( $kind == $HcomFactory )
		|| ( $kind == $HcomTower )
		|| ( $kind == $HcomFire )
		|| ( $kind == $HcomWindmill )
		|| ( $kind == $HcomMyhome )
		|| ( $kind == $HcomPort )
		|| ( $kind == $HcomPolice )
		|| ( $kind == $HcomHospital )
		|| ( $kind == $HcomFlower )
		|| ( $kind == $HcomTrump )
		|| ( $kind == $HcomBase )
		|| ( $kind == $HcomMonument )
		|| ( $kind == $HcomHaribote )
		|| ( $kind == $HcomBank )
		|| ( $kind == $HcomWarp )
		|| ( $kind == $HcomDeathtrap )
		|| ( $kind == $HcomDokan )
		|| ( $kind == $HcomDbase ) )
	{

		# �Ͼ���߷�
		if ( ( $landKind == $HlandForest ) && ( $kind != $HcomPlant ) ) {

			# �����������Ǽ�ưȲ��
			$island->{'money'} += $HtreeValue * $lv;
			logLandSuc( $id, $name, "��ưȲ��", $point );
			$land->[$x][$y]      = $HlandPlains;
			$landValue->[$x][$y] = 0;
			( $landKind, $lv ) = ( $land->[$x][$y], $landValue->[$x][$y] );
		}
		if (
			!(
				   ( $landKind == $HlandPlains )
				|| ( $landKind == $HlandTown )
				|| (   ( $landKind == $HlandSea )
					&& ( $lv == 0 )
					&& ( $kind == $HcomFire ) )
				|| (   ( $landKind == $HlandSea )
					&& ( $lv == 0 )
					&& ( $kind == $HcomDbase ) )
				|| (   ( $landKind == $HlandSea )
					&& ( $lv == 1 )
					&& ( $kind == $HcomPlant ) )
				|| (   ( $landKind == $HlandMonument )
					&& ( $kind == $HcomMonument ) )
				|| ( ( $landKind == $HlandBank ) && ( $kind == $HcomBank ) )
				|| ( ( $landKind == $HlandBase ) && ( $kind == $HcomBase ) )
				|| ( ( $landKind == $HlandBase ) && ( $kind == $HcomMonument ) )
				|| ( ( $landKind == $HlandMyhome ) && ( $kind == $HcomMyhome ) )
				|| (   ( $landKind == $HlandDeathtrap )
					&& ( $kind == $HcomDeathtrap ) )
				|| (   ( $landKind == $HlandSea )
					&& ( $lv == 0 )
					&& ( $kind == $HcomDeathtrap ) )
				|| ( ( $landKind == $HlandFarm ) && ( $kind == $HcomFarm ) )
				|| (   ( $landKind == $HlandFactory )
					&& ( $kind == $HcomFactory ) )
				|| ( ( $landKind == $HlandTower )   && ( $kind == $HcomTower ) )
				|| ( ( $landKind == $HlandPort )    && ( $kind == $HcomPort ) )
				|| ( ( $landKind == $HlandDokan )   && ( $kind == $HcomDokan ) )
				|| ( ( $landKind == $HlandDefence ) && ( $kind == $HcomDbase ) )
			)
		  )
		{

			# ��Ŭ�����Ϸ�
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}

		# �����ʬ��
		if ( $kind == $HcomPlant ) {

			# �������ܿ���ˤ���
			if ( ( $landKind == $HlandSea ) && ( $lv == 1 ) ) {
				$landValue->[$x][$y] = 10;    # ����1000ɤ����
				logLandSuc( $id, $name, '�ܿ�������', $point );
			}
			else {

				# ��Ū�ξ��򿹤ˤ��롣
				$land->[$x][$y]      = $HlandForest;
				$landValue->[$x][$y] = 1;              # �ڤϺ���ñ��
				logPBSuc( $id, $name, $comName, $point );
			}
		}
		elsif ( $kind == $HcomFarm ) {

			# ����
			if ( $landKind == $HlandFarm ) {

				# ���Ǥ�����ξ��
				$landValue->[$x][$y] += 5;             # ���� + 5000��
				$landValue->[$x][$y] = 50
				  if ( $landValue->[$x][$y] > 50 );    # ���� 50000��
			}
			else {

				# ��Ū�ξ��������
				$land->[$x][$y]      = $HlandFarm;
				$landValue->[$x][$y] = 10;             # ���� = 10000��
			}
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomFactory ) {

			# ����
			if ( $landKind == $HlandFactory ) {

				# ���Ǥ˹���ξ��
				$landValue->[$x][$y] += 10;            # ���� + 10000��
				$landValue->[$x][$y] = 100
				  if ( $landValue->[$x][$y] > 100 );    # ���� 100000��
			}
			else {

				# ��Ū�ξ��򹩾��
				$land->[$x][$y]      = $HlandFactory;
				$landValue->[$x][$y] = 30;
			}
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomTower ) {

			# ���ȥӥ�
			if ( $landKind == $HlandTower ) {
				$landValue->[$x][$y] += 10;
				$landValue->[$x][$y] = 200 if ( $landValue->[$x][$y] > 200 );
			}
			else {
				$land->[$x][$y]      = $HlandTower;
				$landValue->[$x][$y] = 30;
			}
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomPort ) {

			# ��
			if ( seaAround( $land, $x, $y, 7 ) == 0 ) {

				# ���Ϥ˳��Ϥ�̵���������Բ�
				logNoLandAround( $id, $name, $comName, "��", $point );
				return 0;
			}
			if ( $landKind == $HlandPort ) {
				$landValue->[$x][$y] += 20;
				$landValue->[$x][$y] = 200 if ( $landValue->[$x][$y] > 200 );
			}
			else {
				$land->[$x][$y]      = $HlandPort;
				$landValue->[$x][$y] = 40;
			}
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomBase ) {

			# ��Ū�ξ���ߥ�������Ϥˤ��롣
			if ( $landKind == $HlandBase ) {
				if ( $landValue->[$x][$y] < 15 ) {
					$landValue->[$x][$y] += 5;
				}
				elsif ( $landValue->[$x][$y] < 20 ) {
					$landValue->[$x][$y] = 20;
				}
				elsif ( $landValue->[$x][$y] < $HmaxExpPoint ) {
					$landValue->[$x][$y]++;
				}
				elsif ( $landValue->[$x][$y] > $HmaxExpPoint ) {
					$landValue->[$x][$y] = $HmaxExpPoint;
				}
			}
			else {
				$land->[$x][$y]      = $HlandBase;
				$landValue->[$x][$y] = 0;
			}
			logPBSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomHaribote ) {

			# ��Ū�ξ���ϥ�ܥƤˤ���
			$island->{'Afmissile'} = 1;
			$land->[$x][$y]        = $HlandHaribote;
			$landValue->[$x][$y]   = 0;
			logHariSuc( $id, $name, $comName, $HcomName[$HcomDbase], $point );
			return 0;
		}
		elsif ( $kind == $HcomDokan ) {

			# �ڴ�(�ϲ�)����
			my ( $ugL, $ugV, $ugX, $ugY ) = (
				$island->{'ugL'}, $island->{'ugV'},
				$island->{'ugX'}, $island->{'ugY'}
			);
			my ($i);
			$arg = $HugMax;
			for ( $i = 0 ; $i < $HugMax ; $i++ ) {
				if ( ( $ugX->[$i] == $x ) && ( $ugY->[$i] == $y ) ) {

					# �����ϲ�������
					return 0;
				}
				elsif (( $land->[ $ugX->[$i] ][ $ugY->[$i] ] != $HlandDokan )
					&& ( $land2->[ $ugX->[$i] ][ $ugY->[$i] ] != $HlandDokan ) )
				{
					$arg = $i;
				}
			}
			if ( $arg == $HugMax ) {
				return 0;
			}
			$land->[$x][$y]      = $HlandDokan;
			$landValue->[$x][$y] = 0;
			$ugX->[$arg]         = $x;
			$ugY->[$arg]         = $y;
			$ugL->[$arg][0]      = $HugSpace;
			$ugL->[$arg][1]      = $HugDokan;
			$ugL->[$arg][2]      = $HugSpace;
			$ugL->[$arg][3]      = $HugRoad;
			$ugL->[$arg][4]      = $HugHasigo;
			$ugL->[$arg][5]      = $HugRoad;
			$ugL->[$arg][6]      = $HugRoad;
			$ugL->[$arg][7]      = $HugHasigo;
			$ugL->[$arg][8]      = $HugRoad;

			for ( $i = 0 ; $i < 9 ; $i++ ) {
				$ugV->[$arg][$i] = 0;
			}
			logPBSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomBank ) {

			# ���
			$arg = 1 if ( $arg == 0 );
			my ($value) = min( $arg * $cost, $island->{'money'} );
			my ($p) = int( $value / $cost );
			$cost = $p * $cost;
			if ( $landKind == $HlandBank ) {
				$landValue->[$x][$y] += $p;
			}
			else {
				$land->[$x][$y]      = $HlandBank;
				$landValue->[$x][$y] = $p;
			}
			$landValue->[$x][$y] = 200 if ( $landValue->[$x][$y] > 200 );
			logLandSuc( $id, $name, $comName, '(?, ?)' );
		}
		elsif ( $kind == $HcomWarp ) {
			if ( $arg == 0 ) {

				# ��Ū�ξ���ž�����֤ˤ���
				my ($tn) = $HidToNumber{$target};
				return 0 if ( $tn eq '' );
				$land->[$x][$y]      = $HlandWarp;
				$landValue->[$x][$y] = $target;
			}
			else {
				$land->[$x][$y]      = $HlandWarpR;
				$landValue->[$x][$y] = $arg;
				$comName             = 'ž�������ַ���';
			}
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomDbase ) {

			# �ɱһ���
			$island->{'defence'} = 1;    # �ե饰ON
			if ( $landKind == $HlandDefence ) {

				# ���Ǥ��ɱһ��ߤξ��
				$landValue->[$x][$y] = 1;    # �������֥��å�
				logBombSet( $id, $name, $landName, $point );
			}
			elsif ( $landKind == $HlandSea ) {
				$land->[$x][$y]      = $HlandOil;
				$landValue->[$x][$y] = 5;
				logLandSuc( $id, $name, $comName, $point );
			}
			else {

				# ��Ū�ξ����ɱһ��ߤ�
				$land->[$x][$y] = $HlandDefence;
				if ( $arg == 1 ) {
					$landValue->[$x][$y] = 10;
					logPBSuc( $id, $name, $comName, $point );
				}
				elsif ( $arg == 2 ) {
					$landValue->[$x][$y] = 20;
					logPBSuc( $id, $name, $comName, $point );
				}
				else {
					$landValue->[$x][$y] = 0;
					logLandSuc( $id, $name, $comName, $point );
				}
			}
		}
		elsif ( $kind == $HcomFire ) {

			# ���ɽ𡢳�����ɽ�
			if ( $landKind == $HlandSea ) {
				$land->[$x][$y]      = $HlandOil;
				$landValue->[$x][$y] = 7;
				logLandSuc( $id, $name, "������ɽ����", $point );
			}
			else {
				$land->[$x][$y]      = $HlandFire;
				$landValue->[$x][$y] = 0;
				$cost                = int( $cost / 2 );
				logLandSuc( $id, $name, $comName, $point );
			}
		}
		elsif ( $kind == $HcomMonument ) {

			# ��ǰ��
			if (   ( $landKind == $HlandMonument )
				&& ( $lv <= $HmonumentRocket )
				&& ( $lv != 3 ) )
			{

		# ���Ǥ˵�ǰ��ξ�� ���å��桢������ǰ��Ͻ���
		# �������åȼ���
				my ($tn) = $HidToNumber{$target};
				return 0 if ( $tn eq '' );
				my ($tIsland) = $Hislands[$tn];
				if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
					|| ( $tIsland->{'evil'} == 0 ) )
				{

					# ��꤬�Ӿ��ΰ���ߡ�
					logUNMiss( $id, $target, $name, $tIsland->{'name'},
						$comName );
					return 0;
				}
				$island->{'evil'} += 60;

				# ���ξ��Ϲ��Ϥ�
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
				logMonFly( $id, $name, $landName, $point );
				if ( ( $x2 == 0 ) && ( $y2 == 0 ) ) {
					$x = random($HislandSize);
					$y = random($HislandSize);
				}
				else {
					my ($r) = random(61);
					$x = $x2 + $ax[$r];
					$y = $y2 + $ay[$r];
					$x-- if ( !( $y % 2 ) && ( $y2 % 2 ) );
				}
				my ( $tId, $tName, $tLand, $tLandValue ) = (
					$tIsland->{'id'},   $tIsland->{'name'},
					$tIsland->{'land'}, $tIsland->{'landValue'}
				);
				logMonDamage( $tId, $tName, "($x, $y)" );
				wideDamage( $tId, $tName, $tLand, $tLandValue, $x, $y, 0 );
			}
			elsif (( $landKind == $HlandMonument )
				&& ( $lv > $HmonumentRocket ) )
			{

				# ���å�ȯ��
				my ( $wkind, $wname, $whp, $wkind2, $wkind3 ) =
				  weatherinfo( $island->{'weather'} );
				if ( $wkind > 1 ) {
					logMiss( $id, $name, "���å��Ǥ��夲",
						"ŷ���Խ��" );
					if ( ( $island->{'order'} & 512 ) && ( $Hwflg > 0 ) )
					{    # �����ʤ���ǲ������
						slideBack(
							$comArray, $cNo, $kind, $target, $x,
							$y,        $arg, $x2,   $y2,     $Hwflg
						);    # �ե饰�դ���̿���᤹
						$Hwflg--;
					}
					return 0;
				}
				if ( $lv - $HmonumentRocket > random(10) ) {
					logRocketS( $id, $name );
					$landValue->[$x][$y] = $HmonumentRocket;
					my ($prize) = $island->{'prize'};
					$prize =~ /([0-9]*),([0-9]*),(.*)/;
					my ( $flags, $monsters, $turns ) = ( $1, $2, $3 );
					if ( !( $flags & 512 ) ) {
						$flags |= 512;
						$island->{'money'} += 64999;

# ����޼��ޤΥ��ϥ���������κǸ�����ǽ��ϡ���ͳ������ǽ��Ϥ���ȥ���������˼��Ԥ�����¿�ŤˤǤ뤫�顩
						$island->{'space'} = 1;
					}
					else {
						$island->{'money'} += 54999;
					}
					$island->{'prize'} = "$flags,$monsters,$turns";
				}
				else {
					$landValue->[$x][$y]++
					  if ( $landValue->[$x][$y] < $HmonumentRocket + 7 );
					logRocketF( $id, $name );
				}
			}
			elsif ( $landKind == $HlandBase ) {

				# �ߥ�������Ϥλ������å������
				$land->[$x][$y]      = $HlandMonument;
				$landValue->[$x][$y] = $HmonumentRocket + 1;
				logLandSuc( $id, $name, "���å������", $point );
			}
			else {

				# ��Ū�ξ���ǰ���
				$land->[$x][$y] = $HlandMonument;
				if ( $arg == 3 ) {

					# ������ǰ��
					$cost = 2500;
				}
				elsif ( $arg > 3 ) {
					$arg = 0;
				}
				$landValue->[$x][$y] = $arg;
				logLandSuc( $id, $name, $comName, $point );
			}
		}
		elsif ( $kind == $HcomFlower ) {

			# ���֤򿢤���
			$land->[$x][$y]      = $HlandFlower;
			$landValue->[$x][$y] = random(13) + 1;
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomTrump ) {

			# �ȥ�������
			$land->[$x][$y]      = $HlandTrump;
			$landValue->[$x][$y] = 0;
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomPolice ) {

			# �ٻ���
			$land->[$x][$y]      = $HlandPolice;
			$landValue->[$x][$y] = 0;
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomHospital ) {

			# �±�
			$land->[$x][$y]      = $HlandHospital;
			$landValue->[$x][$y] = 0;
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomWindmill ) {

			# ����
			$land->[$x][$y]      = $HlandWindmill;
			$landValue->[$x][$y] = 0;
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomDeathtrap ) {

			# �ǥ��ȥ�å�
			if ( $landKind == $HlandSea ) {
				$land->[$x][$y]      = $HlandOil;
				$landValue->[$x][$y] = 6;
				$comName             = "����ǥ��ȥ�å׷���";
			}
			elsif ( $landKind == $HlandDeathtrap ) {

				# ���Ǥ˥ǥ��ȥ�åפξ��
				$landValue->[$x][$y]++;
				$landValue->[$x][$y] = 3 if ( $landValue->[$x][$y] > 2 );
			}
			else {
				$land->[$x][$y]      = $HlandDeathtrap;
				$landValue->[$x][$y] = 1;
			}
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomMyhome ) {

			# �ޥ��ۡ���
			if ( $landKind == $HlandMyhome ) {
				$landValue->[$x][$y] += 3;
				$landValue->[$x][$y] = 12 if ( $landValue->[$x][$y] > 12 );
			}
			elsif ( $island->{'myhome'} == 1 ) {

				# ���Ǥˤ��� ������鷺�����
				return 0;
			}
			else {
				$land->[$x][$y] = $HlandMyhome;

				$landValue->[$x][$y] = 0;
			}
			logLandSuc( $id, $name, $comName, $point );
		}

		# ��򺹤�����
		$island->{'money'} -= $cost;

		# ����դ��ʤ顢���ޥ�ɤ��᤹
		if (   ( $kind == $HcomFarm )
			|| ( $kind == $HcomTower )
			|| ( $kind == $HcomBase )
			|| ( $kind == $HcomPort )
			|| ( $kind == $HcomFactory ) )
		{
			if ( $arg > 1 ) {
				$arg--;
				slideBack( $comArray, $cNo, $kind, $target, $x, $y, $arg );
			}
		}

		return 1;

		#w	if(($HwarFlg) && ($island->{'dcount'} < 3)){
		#w		# ����Ϥ�Ϣ³��ȯ����ǽ
		#w		$island->{'dcount'}++;
		#w		return 0;
		#w	}else{
		#w		return 1;
		#w	}

	}
	elsif ( $kind == $HcomMountain ) {

		# �η���
		if ( $landKind != $HlandMountain ) {

			# ���ʳ��ˤϺ��ʤ�
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
		$landValue->[$x][$y] += 10;    # ���� + 10000��
		if ( $landValue->[$x][$y] > 200 ) {    # ���� 200000��
			$landValue->[$x][$y] = 200;
			logMiss( $id, $name, $comName, "���˺��絬�Ϥ�" );
			return 0;
		}
		if ( random(250) < $HdisMaizo ) {      # ���̮ȯ���γ�Ψ����
			my ($v) = 200 + random(1001);
			$island->{'money'} += $v;
			logGold( $id, $name, $comName, $v );
		}
		logLandSuc( $id, $name, $comName, $point );

		# ��򺹤�����
		$island->{'money'} -= $cost;
		if ( $arg > 1 ) {
			$arg--;
			slideBack( $comArray, $cNo, $kind, $target, $x, $y, $arg );
		}
		return 1;
	}
	elsif ( ( $kind == $HcomSFarm ) || ( $kind == $HcomPropaganda ) ) {

		# ��������,Ͷ�׳�ư
		if ( $kind == $HcomPropaganda ) {    # Ͷ�׳�ư
			logPropaganda( $id, $name, $comName );
			$island->{'propaganda'} = 1;
		}
		else {                               # ��������
			if ( ( $landKind == $HlandOil ) && ( $lv >= 10 ) && ( $lv <= 30 ) )
			{

				# ���Ǥ˳�������ξ��
				$landValue->[$x][$y] += 5;
				$landValue->[$x][$y] = 30 if ( $landValue->[$x][$y] > 30 );
			}
			elsif ( ( $landKind != $HlandSea ) || ( $lv != 0 ) ) {

				# ���ʳ��ˤϺ��ʤ�
				logLandFail( $id, $name, $comName, $landName, $point, $landKind,
					$lv );
				return 0;
			}
			else {

				# ��Ū�ξ����������
				$land->[$x][$y]      = $HlandOil;
				$landValue->[$x][$y] = 10;
			}
			logLandSuc( $id, $name, $comName, $point );
		}

		# ��򺹤�����
		$island->{'money'} -= $cost;
		if ( $arg > 1 ) {
			$arg--;
			slideBack( $comArray, $cNo, $kind, $target, $x, $y, $arg );
		}
		return 1;
	}
	elsif ( ( $kind == $HcomSbase ) || ( $kind == $HcomScity ) ) {

		# ������ϡ������Ի�
		if ( ( $landKind != $HlandSea ) || ( $lv != 0 ) ) {

			# ���ʳ��ˤϺ��ʤ�
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
		if ( $kind == $HcomSbase ) {
			$land->[$x][$y]      = $HlandSbase;
			$landValue->[$x][$y] = 0;             # �и���0
			logLandSuc( $id, $name, $comName, '(?, ?)' );
		}
		else {
			my ( $wkind, $wname, $whp, $wkind2, $wkind3 ) =
			  weatherinfo( $island->{'weather'} );
			if ( $wkind > 2 ) {
				logMiss( $id, $name, $comName, "ŷ���Խ��" );
				if ( ( $island->{'order'} & 512 ) && ( $Hwflg > 0 ) )
				{    # �����ʤ���ǲ������
					slideBack(
						$comArray, $cNo, $kind, $target, $x,
						$y,        $arg, $x2,   $y2,     $Hwflg
					);    # �ե饰�դ���̿���᤹
					$Hwflg--;
				}
				return 0;
			}
			$land->[$x][$y]      = $HlandOil;
			$landValue->[$x][$y] = 35;
			logLandSuc( $id, $name, $comName, $point );
		}

		# ��򺹤�����
		$island->{'money'} -= $cost;
		return 1;
	}
	elsif ( $kind == $HcomSMonument ) {

		# ���쵭ǰ��
		if ( $landKind == $HlandSMonument ) {

			# ���Ǥ˳��쵭ǰ��ξ��
			# �������åȼ���
			my ($tn) = $HidToNumber{$target};
			return 0 if ( $tn eq '' );
			my ($tIsland) = $Hislands[$tn];
			if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
				|| ( $tIsland->{'evil'} == 0 ) )
			{

				# ��꤬�Ӿ��ΰ���ߡ�
				logUNMiss( $id, $target, $name, $tIsland->{'name'}, $comName );
				return 0;
			}
			$island->{'evil'} += 70;

			# ���ξ��ϳ���
			$land->[$x][$y]      = $HlandSea;
			$landValue->[$x][$y] = 0;
			logMonFly( $id, $name, $landName, $point );
			if ( ( $x2 == 0 ) && ( $y2 == 0 ) ) {
				$x = random($HislandSize);
				$y = random($HislandSize);
			}
			else {
				my ($r) = random(19);
				$x = $x2 + $ax[$r];
				$y = $y2 + $ay[$r];
				$x-- if ( !( $y % 2 ) && ( $y2 % 2 ) );
			}
			my ( $tId, $tName, $tLand, $tLandValue ) = (
				$tIsland->{'id'},   $tIsland->{'name'},
				$tIsland->{'land'}, $tIsland->{'landValue'}
			);
			logMonDamage( $tId, $tName, "($x, $y)" );
			wideDamage( $tId, $tName, $tLand, $tLandValue, $x, $y, 0 );
		}
		elsif ( ( $landKind != $HlandSea ) || ( $lv != 0 ) ) {

			# ���ʳ��ˤϺ��ʤ�
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
		else {

			# ��Ū�ξ���ǰ���
			$land->[$x][$y] = $HlandSMonument;
			$arg = 0 if ( $arg >= $HsmonumentNumber );
			$landValue->[$x][$y] = $arg;
			logLandSuc( $id, $name, $comName, $point );
		}
		$island->{'money'} -= $cost;
		return 1;
	}
	elsif ( $kind == $HcomBreakwater ) {

		# ������
		if ( ( $landKind != $HlandSea ) || ( $lv != 1 ) ) {

			# �����ʳ��ˤϺ��ʤ�
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
		$land->[$x][$y]      = $HlandBreakwater;
		$landValue->[$x][$y] = 1;
		logLandSuc( $id, $name, $comName, $point );
		$island->{'money'} -= $cost;
		return 1;
	}
	elsif ( $kind == $HcomShipbuild ) {

		# ¤��
		# ���ϣ��ޥ��˹������뤫�����å�
		return 0 if ( !chkAround( $land, $x, $y, $HlandPort, 19 ) );

		# ���������ɲò�ǽ�μ����������å�
		if ( ( $landKind == $HlandSea ) && ( $lv > 0 ) ) {

			# ¤��
			$land->[$x][$y]      = $HlandFishSShip;
			$landValue->[$x][$y] = 21000 + $id;       # ���������ɸ�
			$island->{'land2'}->[$x][$y]      = $HlandSea;
			$island->{'landValue2'}->[$x][$y] = 1;
			$comName                          = "����¤��";
		}
		elsif (( $landKind == $HlandFishSShip )
			|| ( $landKind == $HlandFishMShip ) )
		{

			# �������淿����
			my ( $order, $hp, $sId ) = shipSpec($lv);
			return 0
			  if ( $sId != $id )
			  ;    # �������åȤ������Ǥʤ��������
			if ( $landKind == $HlandFishMShip ) {
				if ( $arg == 1 ) {

					# ��ڵ���
					$land->[$x][$y] = $HlandTitanic;
					$comName = "��ڵ���¤��";
				}
				elsif ( $arg == 2 ) {

					# ����������
					$land->[$x][$y] = $HlandAegisShip;
					$comName = "����������¤��";
				}
				else {
					$land->[$x][$y] = $HlandFishLShip;
					$comName = "�����ɲ�¤��";
				}
			}
			else {

				# ����
				if ( $arg == 1 ) {

					# ����õ����
					$land->[$x][$y] = $HlandProbeShip;
					$comName = "����õ����¤��";
				}
				elsif ( $arg == 2 ) {

					# ������Ƥ��
					$land->[$x][$y] = $HlandMonsShip;
					$comName = "������Ƥ��¤��";
				}
				else {
					$land->[$x][$y] = $HlandFishMShip;
					$comName = "�����ɲ�¤��";
				}
			}
		}
		else {
			return 0;
		}
		logLandSuc( $id, $name, $comName, $point );
		$island->{'money'} -= $cost;
		return 1;
	}
	elsif ( ( $kind == $HcomPresent ) || ( $kind == $HcomPresentAid ) ) {

		# �ץ쥼���,�ץ쥼��Ⱦ���
		my ( $tn, $tIsland, $tName );
		if ( $kind == $HcomPresent ) {
			if (
				!(
					( $landKind == $HlandPlains ) || ( $landKind == $HlandTown )
				)
			  )
			{

				# ��Ŭ�����Ϸ�
				logLandFail( $id, $name, $comName, $landName, $point, $landKind,
					$lv );
				return 0;
			}
		}
		else {
			$tn = $HidToNumber{$target};
			return 0 if ( $tn eq '' );    # ������鷺�����
			$tIsland = $Hislands[$tn];
			$tName   = $tIsland->{'name'};
		}
		if ( $kind == $HcomPresent ) {
			$landValue->[$x][$y] = 0;
			if ( ( $arg <= 0 ) && ( $island->{'present'}->[0] > 0 ) ) {
				$island->{'present'}->[0]--;
				$land->[$x][$y] = $HlandPark;
			}
			elsif ( ( $arg == 1 ) && ( $island->{'present'}->[1] > 0 ) ) {
				$island->{'present'}->[1]--;
				$land->[$x][$y] = $HlandStadium;
			}
			elsif ( ( $arg == 2 ) && ( $island->{'present'}->[2] > 0 ) ) {
				$island->{'present'}->[2]--;
				$land->[$x][$y] = $HlandDome;
			}
			elsif ( ( $arg == 3 ) && ( $island->{'present'}->[3] > 0 ) ) {
				$island->{'present'}->[3]--;
				$land->[$x][$y] = $HlandCasino;
			}
			elsif ( ( $arg == 4 ) && ( $island->{'present'}->[4] > 0 ) ) {
				$island->{'present'}->[4]--;
				$land->[$x][$y] = $HlandAmusement;
			}
			elsif ( ( $arg == 5 ) && ( $island->{'present'}->[5] > 0 ) ) {
				$island->{'present'}->[5]--;
				$land->[$x][$y] = $HlandSchool;
			}
			elsif ( ( $arg == 6 ) && ( $island->{'present'}->[6] > 0 ) ) {
				$island->{'present'}->[6]--;
				$land->[$x][$y] = $HlandAirport;
			}
			elsif ( ( $arg == 7 ) && ( $island->{'present'}->[7] > 0 ) ) {
				$island->{'present'}->[7]--;
				$land->[$x][$y] = $HlandBigcity;
			}
			elsif ( ( $arg == 8 ) && ( $island->{'present'}->[8] > 0 ) ) {
				$island->{'present'}->[8]--;
				$land->[$x][$y] = $HlandZoo;
			}
			elsif ( ( $arg == 9 ) && ( $island->{'present'}->[9] > 0 ) ) {
				$island->{'present'}->[9]--;
				$land->[$x][$y] = $HlandExpo;
			}
			elsif ( ( $arg == 10 ) && ( $island->{'present'}->[10] > 0 ) ) {
				$island->{'present'}->[10]--;
				$land->[$x][$y]      = $HlandMonument;
				$landValue->[$x][$y] = 10;
			}
			elsif ( ( $arg >= 11 ) && ( $island->{'present'}->[11] > 0 ) ) {
				$island->{'present'}->[11]--;
				$land->[$x][$y]      = $HlandMonument;
				$landValue->[$x][$y] = 8;
			}
			else {

				# ���ꤨ�ʤ����ɤȤꤢ�������Ϥˤ��Ȥ�
				$land->[$x][$y] = $HlandWaste;
				logNoPresent( $id, $name, $comName, $point );
				return 0;
			}
			logLandSuc( $id, $name, $comName, $point );

			#	$island->{'money'} -= $cost;
		}
		else {
			if ( ( $arg <= 0 ) && ( $island->{'present'}->[0] > 0 ) ) {
				$island->{'present'}->[0]--;
				$tIsland->{'present'}->[0]++;
			}
			elsif ( ( $arg == 1 ) && ( $island->{'present'}->[1] > 0 ) ) {
				$island->{'present'}->[1]--;
				$tIsland->{'present'}->[1]++;
			}
			elsif ( ( $arg == 2 ) && ( $island->{'present'}->[2] > 0 ) ) {
				$island->{'present'}->[2]--;
				$tIsland->{'present'}->[2]++;
			}
			elsif ( ( $arg == 3 ) && ( $island->{'present'}->[3] > 0 ) ) {
				$island->{'present'}->[3]--;
				$tIsland->{'present'}->[3]++;
			}
			elsif ( ( $arg == 4 ) && ( $island->{'present'}->[4] > 0 ) ) {
				$island->{'present'}->[4]--;
				$tIsland->{'present'}->[4]++;
			}
			elsif ( ( $arg == 5 ) && ( $island->{'present'}->[5] > 0 ) ) {
				$island->{'present'}->[5]--;
				$tIsland->{'present'}->[5]++;
			}
			elsif ( ( $arg == 6 ) && ( $island->{'present'}->[6] > 0 ) ) {
				$island->{'present'}->[6]--;
				$tIsland->{'present'}->[6]++;
			}
			elsif ( ( $arg == 7 ) && ( $island->{'present'}->[7] > 0 ) ) {
				$island->{'present'}->[7]--;
				$tIsland->{'present'}->[7]++;
			}
			elsif ( ( $arg == 8 ) && ( $island->{'present'}->[8] > 0 ) ) {
				$island->{'present'}->[8]--;
				$tIsland->{'present'}->[8]++;
			}
			elsif ( ( $arg == 9 ) && ( $island->{'present'}->[9] > 0 ) ) {
				$island->{'present'}->[9]--;
				$tIsland->{'present'}->[9]++;
			}
			elsif ( ( $arg == 10 ) && ( $island->{'present'}->[10] > 0 ) ) {
				$island->{'present'}->[10]--;
				$tIsland->{'present'}->[10]++;
			}
			elsif ( ( $arg >= 11 ) && ( $island->{'present'}->[11] > 0 ) ) {
				$island->{'present'}->[11]--;
				$tIsland->{'present'}->[11]++;
			}
			else {
				logNoPresent( $id, $name, $comName, $point );
				return 0;
			}
			logPresent( $id, $target, $name, $tName );
			return 0;
		}
		return 1;
	}
	elsif ( ( $kind == $HcomSpy ) || ( $kind == $HcomTeisatu ) ) {

		# ������ɸ����廡
		my ($tn) = $HidToNumber{$target};
		return 0
		  if ( $tn eq '' )
		  ;    # �������åȤ����Ǥˤʤ����Ჿ����鷺�����
		my ($tIsland) = $Hislands[$tn];
		if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
			|| ( $tIsland->{'evil'} == 0 ) )
		{

			# ��꤬�Ӿ��ΰ���ߡ�
			logUNMiss( $id, $target, $name, $tIsland->{'name'}, $comName );
			return 0;
		}
		$island->{'evil'} += 30;
		my ($tName)       = $tIsland->{'name'};
		my ($tLand)       = $tIsland->{'land'};
		my ($tLandValue)  = $tIsland->{'landValue'};
		my ($tLand2)      = $tIsland->{'land2'};
		my ($tLandValue2) = $tIsland->{'landValue2'};

		my ( $tx, $ty, $i );

		if ( $kind == $HcomSpy ) {
			$island->{'money'} -= $cost;
			if ( random(5) == 0 ) {    # ����
				logSpyF( $id, $target, $name, $tName, $comName );
				return 1;
			}
			foreach ( 0 .. 36 ) {
				$tx = $x + $ax[$_];
				$ty = $y + $ay[$_];
				$tx-- if ( !( $ty % 2 ) && ( $y % 2 ) );
				next
				  if ( ( $tx < 0 )
					|| ( $tx >= $HislandSize )
					|| ( $ty < 0 )
					|| ( $ty >= $HislandSize ) );
				if ( $tLand->[$tx][$ty] == $HlandPolice ) {

			   #					HdebugOut("��ɸ���ϣ��إ����˷ٻ���ϼ���");
					logSpyF( $id, $target, $name, $tName, $comName );
					return 1;
				}
				elsif (( $tLand->[$tx][$ty] == $HlandAegisShip )
					&& ( $HseaChk[ $tLand->[$x][$y] ] ) )
				{
					my ( $order, $hp, $sId ) =
					  shipSpec( $tLandValue->[$tx][$ty] );
					if ( $sId == $target ) {

#						HdebugOut("��ɸ�����ϤǼ��ϣ��إ����˥��������Ϥϼ���");
						logSpyF( $id, $target, $name, $tName, $comName );
						return 1;
					}
				}
			}

			#			HdebugOut("��������������å�������");
			if ( $arg == 0 ) {

				# �Ͽ�ȯ��������
				if ( ( $HseaChk[ $tLand->[$x][$y] ] ) && ( random(2) == 0 ) ) {

					# ���ξ��ϣ�����Ǽ���
					logSpyF( $id, $target, $name, $tName, $comName );
					return 1;
				}
				$comName = "������ɸ����Ͽ�";
				addCommandLate( 3, $HislandTurn, $id, $kind, $target, $x, $y,
					$arg, $x2, $y2 );    # ������̿��
			}
			elsif ( $arg == 1 ) {

				# ���������
				$comName = "������ɸ������������($x,$y)";
				addCommandLate( 1, $HislandTurn, $id, $kind, $target, $x, $y,
					$arg, $x2, $y2 );    # ������̿��
			}
			else {

				# �����Ƥ�Ƥ��
				$comName = "������ɸ��������Ƥ�Ƥ��";
				$tIsland->{'food'} -= int( $tIsland->{'food'} * 0.2 );
				logLate(
"${HtagName_}${tName}${AfterName}${H_tagName}�ο��Ȥΰ��������Ԥ��ˤ��ǳ�䤵��ޤ�����",
					$target
				);
			}
			logSecret(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${AfterName}${H_tagName}��${HtagComName_}$comName${H_tagComName}��Ԥ������������ޤ�����",
				$id
			);
			return 1;
		}
		else {

			#	$arg = 1 if($arg < 1);
			#	$arg = 37 if($arg > 36); # ����37�ޥ�
			$arg = 37;
		}

		# ��������̤���Ĵ�٤�
		for ( $i = 0 ; $i < $arg ; $i++ ) {

			#	if(random(25) == 0){ # ����
			#		logSpyF($id, $target, $name, $tName, $comName);
			#		last;
			#	}
			$tx = $x + $ax[$i];
			$ty = $y + $ay[$i];
			$tx-- if ( !( $ty % 2 ) && ( $y % 2 ) );  # �Ԥˤ�����Ĵ��
			next
			  if ( ( $tx < 0 )
				|| ( $tx >= $HislandSize )
				|| ( $ty < 0 )
				|| ( $ty >= $HislandSize ) );

			# �Ϸ�������
			my ($tL)     = $tLand->[$tx][$ty];
			my ($tLv)    = $tLandValue->[$tx][$ty];
			my ($tLname) = landName( $tL, $tLv );
			my ($tPoint) = "($tx, $ty)";
			if ( ( $tL == $HlandBase ) || ( $tL == $HlandSbase ) )
			{    # �ߴ��ϡ�����ߴ��Ϥλ�
				logBeseFind( $id, $tName, $tPoint, $tLv, $tLname );
			}
			elsif ( ( $tL == $HlandForest ) || ( $tL == $HlandDefence ) ) {
				logLandTruth( $id, $tName, $tPoint, $tLname, '��ʪ' );
			}
			elsif ( ( $tL == $HlandHaribote ) && ( $tLv == 0 ) ) {
				logLandTruth( $id, $tName, $tPoint, '�ɱһ���', $tLname );
			}
			elsif ( ( $tL == $HlandHaribote ) && ( $tLv > 0 ) ) {
				logLandTruth( $id, $tName, $tPoint, '�ɱһ���',
					'�ϥ�ܥƤ��Τ�' );
			}
			elsif ( $tL == $HlandBank ) {
				logLandTruth( $id, $tName, $tPoint, '��', $tLname );
			}
			elsif ( $tL == $HlandGhostShip ) {
				logLandTruth( $id, $tName, $tPoint, '��', $tLname )
				  ;    # ͩ����
			}
			elsif ( $tL == $HlandPirate ) {
				logLandTruth( $id, $tName, $tPoint, '��±��', $tLname )
				  ;    # ��±��
			}
		}
		$island->{'money'} -= $cost;
		return 1;
	}
	elsif ( $kind == $HcomPioneer ) {

		# ����
		if ( $landKind != $HlandPlains ) {

			# ʿ�ϰʳ��ǤϤǤ��ʤ���
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
		$land->[$x][$y]      = $HlandTown;
		$landValue->[$x][$y] = 1;
		logLandSuc( $id, $name, $comName, $point );

		# ���Ȥ򺹤�����
		$island->{'food'} += $cost;
		return 1;
	}
	elsif ( $kind == $HcomDummy ) {

		# ���ߡ�̿��
		if ( $arg == 1 ) {
			$comName = '�η�������';
		}
		elsif ( $arg == 2 ) {
			$comName = '���Ω��';
		}
		else {
			$comName = '��������';
		}
		if ( ( $arg == 2 ) && ($HlogOmit2) ) {
			my $sno = $island->{'seichi'};
			$island->{'seichi'}++;
			if ( $HlogOmit2 == 1 ) {
				my $seichipnt;
				( $seichipnt->{x}, $seichipnt->{y}, $seichipnt->{z} ) =
				  ( $x, $y, '���Ω��' );
				$island->{'seichipnt'}->[$sno] = $seichipnt;
			}
		}
		else {
			logLandSuc( $id, $name, $comName, $point );
		}
		logDummy( $id, $name, $comName, $point );
		$island->{'money'} -= $cost;
		return 0;
	}
	elsif ( $kind == $HcomUg ) {

		# �ϲ�����
		my ( $ugL, $ugV, $ugX, $ugY ) = (
			$island->{'ugL'}, $island->{'ugV'},
			$island->{'ugX'}, $island->{'ugY'}
		);
		my ($i);
		for ( $i = 0 ; $i < $HugMax ; $i++ ) {
			last
			  if ( ( $land->[$x][$y] == $HlandDokan )
				&& ( ( $x == $ugX->[$i] ) && ( $y == $ugY->[$i] ) ) );
		}
		if ( $i >= $HugMax ) {
			return 0;
		}
		my $v = ( $x2 + $y2 * 3 );
		if (   ( $ugL->[$i][$v] == $HugSpace )
			|| ( $ugL->[$i][$v] == $HugDokan )
			|| ( $ugL->[$i][$v] == $HugHasigo ) )
		{
			return 0;
		}
		if ( ( $arg == 4 ) && ( $island->{'money'} < 2400 ) ) {

			# ��������
			return 0;
		}
		$landValue->[$x][$y]--
		  if ( ( $ugL->[$i][$v] == $HugKiti ) && ( $landValue->[$x][$y] > 0 ) );
		if ( $arg <= 0 ) {
			$ugL->[$i][$v] = $HugTosi;
			$ugV->[$i][$v] = 1;
			$comName       = "�ϲ��ԻԷ���";
		}
		elsif ( $arg == 1 ) {
			$ugL->[$i][$v] = $HugFarm;
			$ugV->[$i][$v] = 10;
			$comName       = "�ϲ��������";
		}
		elsif ( $arg == 2 ) {
			$ugL->[$i][$v] = $HugFact;
			$ugV->[$i][$v] = 30;
			$comName       = "�ϲ��������";
		}
		elsif ( $arg == 3 ) {
			$ugL->[$i][$v] = $HugKiti;
			$ugV->[$i][$v] = 0;
			$comName       = "�ϲ��ߥ��������";
			$landValue->[$x][$y]++;
		}
		else {
			$ugL->[$i][$v] = $HugOil;
			$ugV->[$i][$v] = 30;
			$cost *= 3;
			$comName = "�ϲ����������������";
		}
		$island->{'money'} -= $cost;
		logPBSuc( $id, $name, $comName, "($x, $y)��($x2, $y2)" );
		return 1;
	}
	elsif ( $kind == $Hcomcolony ) {

		# ����ˡ��
		if ( $arg == 1 ) {
			logEvent( $id, $name,
"����<B>�����ѡ�������ɥ����ƥ�</B>��ȯư����"
			);
			$island->{'SSSystem'} = 1;
			$island->{'Crime'}    = 1;
			$island->{'money'} -= $cost;
			return 1;
		}
		elsif ( $arg == 2 ) {
			$island->{'money'} -= $cost;
			addCommandLate( 1, $HislandTurn, $id, $kind, $target, $x, $y, $arg,
				$x2, $y2 );    # ������̿��
			return 1;
		}
		my ($tn) = $HidToNumber{$target};
		return 0
		  if ( $tn eq '' )
		  ;    # �������åȤ����Ǥˤʤ����Ჿ����鷺�����
		my ($prize) = $island->{'prize'};
		$prize =~ /([0-9]*),([0-9]*),(.*)/;
		my ( $flags, $monsters, $turns ) = ( $1, $2, $3 );
		if ( !( $flags & 512 ) ) {

			# ������­�ˤ�����
			logMiss( $id, $name, $comName, "������­��" );
			return 0;
		}
		my ($tIsland) = $Hislands[$tn];
		my ($tName)   = $tIsland->{'name'};
		if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
			|| ( $tIsland->{'evil'} == 0 ) )
		{

			# ��꤬�Ӿ��ΰ���ߡ�
			logUNMiss( $id, $target, $name, $tName, $comName );
			return 0;
		}

#	�˰��ʤΤǥ����ȡ��������������٤ϻȤ���������
#		if($arg == 49){
#			$HpunishInfo{$target}->{punish} = 10;
#			$HpunishInfo{$target}->{x} = $x;
#			$HpunishInfo{$target}->{y} = $y;
#			logEventT($id, $target, $name,"��<B>���ۤ��Τ�򾤴���</B>${HtagName_}${tName}${AfterName}${H_tagName}�˸����ƽз⤵���ޤ�����");
#			return 1;
#		}elsif($arg == 48){
#			my($i);
#			my($tAlly) = $tIsland->{'ally'};
#			logEvent($id, $name,"����<B>¿��Ƭ�˥ߥ�����</B>��$Hallygroup[$tAlly]�رĤ˸�����ȯ�ͤ������͡���");
#			for($i = 0; $i < $HislandNumber; $i++){
#				$tIsland = $Hislands[$i];
#				my($ttAlly) = $tIsland->{'ally'};
#				if($tAlly == $ttAlly){
#					$target = $tIsland->{'id'};
#					$tName = $tIsland->{'name'};
#					logOut("¿��Ƭ�˥ߥ�����ϡ�${HtagName_}${tName}${AfterName}($x,$y)${H_tagName}��̿�椷���Ϥˤ��ﳲ���Фޤ�����",$id, $target);
#					wideDamage($target, $tName, $tIsland->{'land'}, $tIsland->{'landValue'}, $x, $y, 1);
#				}
#			}
#			return 1;
#		}elsif($arg == 47){
#			my($i);
#			my($tAlly) = $tIsland->{'ally'};
#			logEvent($id, $name,"����<B>���ۤ��Τ�򾤴���</B>$Hallygroup[$tAlly]�رĤ˸����ƽз⤵���ޤ�����");
#			for($i = 0; $i < $HislandNumber; $i++){
#				$tIsland = $Hislands[$i];
#				my($ttAlly) = $tIsland->{'ally'};
#				if($tAlly == $ttAlly){
#					$target = $tIsland->{'id'};
#					$tName = $tIsland->{'name'};
#					$HpunishInfo{$target}->{punish} = 10;
#					$HpunishInfo{$target}->{x} = $x;
#					$HpunishInfo{$target}->{y} = $y;
#				}
#			}
#			return 1;
#		}
		if ( $island->{'weapon'} < 200 ) {
			logMiss( $id, $name, $comName,
				"����ˡ��߲���ɬ�פ�ʼ����­��" );
			return 0;
		}
		my ( $wkind, $wname, $whp, $wkind2, $wkind3 ) =
		  weatherinfo( $tIsland->{'weather'} );
		if ( $wkind > 1 && $island->{'eis3'} != 1 ) {
			logMiss( $id, $name, $comName, "ɸŪ��ŷ���Խ��" );
			if ( ( $island->{'order'} & 512 ) && ( $Hwflg > 0 ) )
			{    # �����ʤ���ǲ������
				slideBack(
					$comArray, $cNo, $kind, $target, $x,
					$y,        $arg, $x2,   $y2,     $Hwflg
				);    # �ե饰�դ���̿���᤹
				$Hwflg--;
			}
			return 0;
		}
		$arg = 0;
		$island->{'weapon'} -= 200;
		$island->{'evil'} += 200;
		logEventT( $id, $target, $name,
"��<B>���ڡ�������ˡ�</B>��${HtagName_}${tName}${AfterName}${H_tagName}�˸����ƹ߲������ޤ�����"
		);

		# ��򺹤�����
		$island->{'money'} -= $cost;

		addCommandLate( $HcomcolonyTurn, $HislandTurn, $id, $kind, $target, $x,
			$y, $arg, $x2, $y2 );    # ������̿��

		#CL		$tIsland->{'colony'}++;
		#CL		$tIsland->{'tunami'} = 2;
		return 1;
	}
	elsif (( $kind == $HcomMissileNM )
		|| ( $kind == $HcomMissilePP )
		|| ( $kind == $HcomMissileSPP )
		|| ( $kind == $HcomMissileST )
		|| ( $kind == $HcomMissileLD )
		|| ( $kind == $HcomMissileRM )
		|| ( $kind == $HcomMissileSRM )
		|| ( $kind == $HcomMissileGM )
		|| ( $kind == $HcomMissileMGM )
		|| ( $kind == $HcomBioMissile )
		|| ( $kind == $HcomMissilePLD )
		|| ( $kind == $HcomMissileNCM )
		|| ( $kind == $HcomMissileRNG )
		|| ( $kind == $HcomMissileDM ) )
	{

		# �ߥ������

		# �������åȼ���
		my ($tn) = $HidToNumber{$target};
		if ( $tn eq '' ) {

			# �������åȤ����Ǥˤʤ�
			logMsNoTarget( $id, $name, $comName );

			return 0;
		}

		# ��Ƥ���򻻽�
		if ( ( $kind == $HcomMissileGM ) || ( $kind == $HcomMissileMGM ) ) {
			$arg = 1;
		}
		elsif ( $arg == 0 ) {

			# 0�ξ��Ϸ�Ƥ����
			$arg = 10000;
		}

		# ��������
		my ($tIsland) = $Hislands[$tn];
		my ( $tName, $tLand, $tLandValue, $flag, $boat ) = (
			$tIsland->{'name'}, $tIsland->{'land'}, $tIsland->{'landValue'},
			0, 0
		);
		my ( $tx, $ty, $err );

		#		if($kind != $HcomMissileRM){ # ���Ω���ưʳ�
		$island->{'evil'} += 30 if ( $id != $target );
		if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
			|| ( $tIsland->{'evil'} == 0 ) )
		{

			# ��꤬�Ӿ��ΰ���ߡ�
			logUNMiss( $id, $target, $name, $tName, $comName );
			return 0;
		}

		#		}
		my $we            = 1;    # ʼ��
		                          # �˲��ߥ�����
		my ($DestMissile) = 0;
		if (   ( $kind == $HcomMissileLD )
			|| ( $kind == $HcomMissilePLD )
			|| ( $kind == $HcomMissileNCM ) )
		{
			$DestMissile = 1;
			$we          = 10;
		}

		# ��
		if (   ( $kind == $HcomMissileGM )
			|| ( $kind == $HcomMissileMGM ) )
		{
			$err = 1;
			$we  = 0;
		}
		elsif (( $kind == $HcomMissilePP )
			|| ( $kind == $HcomBioMissile )
			|| ( $kind == $HcomMissilePLD )
			|| ( $kind == $HcomMissileRM ) )
		{
			$err = 7;
		}
		elsif ( $kind == $HcomMissileSPP ) {
			$err = 8;
		}
		elsif ( $kind == $HcomMissileDM ) {
			$err = 37;
		}
		elsif ( $kind == $HcomMissileRNG ) {
			$err = 18;
		}
		elsif ( $kind == $HcomMissileNCM ) {
			$err = 61;
			$we  = 30;
		}
		else {
			$err = 19;
		}

		if ( $id != $target ) {
			if ( $island->{'weapon'} < $we ) {
				logMiss( $id, $name, $comName,
					"�ߥ�����ȯ�ͤ�ɬ�פ�ʼ����­��" );
				return 0;
			}
			$island->{'weapon'} -= $we;
		}

		my ( $renzoku, $rouryoku ) = ( 0, 0 );
		if ( ( $kind == $HcomMissilePP ) || ( $kind == $HcomMissileNM ) ) {
			$command = $comArray->[$cNo];    # ����̿���Ĵ�٤�
			     # Ϣ³�˷�Ƥ��оݤ�̿��ΤȤ�
			if (   ( $command->{'kind'} == $HcomMissilePP )
				|| ( $command->{'kind'} == $HcomMissileNM ) )
			{
				$renzoku = 1;
			}
		}

		if ( $kind == $HcomMissileNCM ) {    # �˥ߥ�����
			if (   ( $tIsland->{'MissileK'} < 30 )
				&& ( $id != $target )
				&& ( !$HwarFlg ) )
			{
				logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${AfterName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ����Ȥ��ޤ��������㤷��ȿ�˱�ư�Τ�����ߤ���ޤ�����",
					$id
				);
				return 0;
			}
			$rouryoku = 9;
		}

		# ����⡼�ɤǤϤ�����Ѥ���ʼ������
		my $mcost = 'money';
		if ( ($HwarFlg) && ( $id != $target ) && ( $cost < 500 ) ) {
			$mcost = 'weapon';
			$cost  = int( $cost / 10 );
		}

		# ����ޤȤ��
		my ( $msCt, $mslogCtM, $mslogCtW, $mslogCtD ) = ( 0, 0, 0, 0 );

# �⤬�Ԥ��뤫�������­��뤫������������Ĥޤǥ롼�ס�Ϣ³�λ���³���롣
		my ( $bx, $by, $count, $level ) = ( 0, 0, 0, 0 );
		while (( ( $arg > 0 ) && ( $island->{'money'} >= $cost ) )
			|| ( ( $renzoku == 1 ) && ( $island->{$mcost} >= $cost ) ) )
		{

			# ���Ϥ򸫤Ĥ���ޤǥ롼��
			if ( $kind2 == $HcomSpecialSPP ) {

				# ������Ƥ���ˤ��SPP
				if ( $island->{'monsship'} < 1 ) {
					return 0 if ( $flag == 0 );
					last;
				}
				elsif ( $island->{'monsship'} < 5 ) {
					$level = $island->{'monsship'};
					$island->{'monsship'} = 0;
				}
				else {
					$level = 5;
					$island->{'monsship'} -= 5;
				}
			}
			else {
				while ( $count < $HpointNumber ) {
					$bx = $Hrpx[$count];
					$by = $Hrpy[$count];
					last
					  if (
						(
							   ( $land->[$bx][$by] == $HlandDefence )
							&& ( $landValue->[$bx][$by] == 3 )
						)
						|| ( $land->[$bx][$by] == $HlandBase )
						|| ( $land->[$bx][$by] == $HlandSbase )
						|| ( $land->[$bx][$by] == $HlandDokan )
					  );
					$count++;
				}
				last
				  if ( $count >= $HpointNumber )
				  ;    # ���Ĥ���ʤ��ä��餽���ޤ�
				$level =
				  expToLevel( $land->[$bx][$by], $landValue->[$bx][$by] )
				  ;    # ���ϤΥ�٥�򻻽�
			}

			# �����Ĵ��Ϥ����ä��Τǡ�flag��Ω�Ƥ�
			$flag = 1;

			# ������ǥ롼��
			while ( ( $level > 0 ) && ( $island->{$mcost} > $cost ) ) {

				last if ( ( $arg <= 0 ) && ( $renzoku == 0 ) );

				# ��ä��Τ�����ʤΤǡ����ͤ���פ�����
				$level--;
				if ( $rouryoku > 0 ) { $rouryoku--; next; }    # ϫ�Ͼ���

				if ( ( $arg <= 0 ) && ( $renzoku == 1 ) ) {    # Ϣ³�λ�

					slideFront( $comArray, $cNo );    # �ʹߤ�ͤ��

					# �ߥ�����ȯ�Ϳ��ʤɤΥ�
					$island->{'MissileA'} += $msCt;
					logMissile(
						$id,       $target,
						$name,     $tName,
						$comName,  $point,
						$msCt,     $msCt - $mslogCtM - $mslogCtW - $mslogCtD,
						$mslogCtM, $mslogCtW,
						$mslogCtD
					);
					( $msCt, $mslogCtM, $mslogCtW, $mslogCtD ) = ( 0, 0, 0, 0 );

					# ������ɸ������
					$kind   = $command->{'kind'};
					$target = $command->{'target'};

					# �������åȼ���
					$tn = $HidToNumber{$target};
					if ( $tn eq '' ) {
						logMsNoTarget( $id, $name, $comName );
						return 1;
					}
					$tIsland = $Hislands[$tn];

					$tName      = $tIsland->{'name'};
					$tLand      = $tIsland->{'land'};
					$tLandValue = $tIsland->{'landValue'};

					$x = $command->{'x'};
					$y = $command->{'y'};

					$arg = $command->{'arg'};
					$arg = 10000 if ( $arg == 0 );

					if ($HsurvFlg) {

						# ���Х��Х�Ǥ�����̵��
					}
					else {
						$arg = 5 if ( ( $id != $target ) && ( $arg > 5 ) );
					}
					$err = ( $kind == $HcomMissilePP ) ? 7 : 19;

					$cost    = $HcomCost[$kind];
					$comName = $HcomName[$kind];
					$point   = "($x, $y)";

					# ����⡼�ɤǤϤ�����Ѥ���ʼ������
					$mcost = 'money';
					if ( ($HwarFlg) && ( $id != $target ) && ( $cost < 500 ) ) {
						$mcost = 'weapon';
						$cost  = int( $cost / 10 );
					}

					# ̿���ʤޤ���
					$command = $comArray->[$cNo];    # �ǽ�Τ���Ф�

					$island->{'evil'} += 30 if ( $id != $target );
					if ( ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
						|| ( $tIsland->{'evil'} == 0 ) )
					{

						# ��꤬�Ӿ��ΰ���ߡ�
						logUNMiss( $id, $target, $name, $tName, $comName );
						return 1;
					}

					# Ϣ³�˷�Ƥ��оݤ�̿��ΤȤ�
					if (   ( $command->{'kind'} == $HcomMissilePP )
						|| ( $command->{'kind'} == $HcomMissileNM ) )
					{
						$renzoku = 1;
					}
					else {
						$renzoku = 0;
					}
					if ($HsurvFlg) {

						# ���Х��Х�Ǥ�ϫ�ϣ�
					}
					else {
						$rouryoku = 2;
					}
					next;
				}

				$msCt++;    # ȯ�Ϳ���׻�

				$arg--;
				$island->{$mcost} -= $cost;

				if ( $kind == $HcomMissileNCM ) {    # �˥ߥ�����λ�
					$ncm      = 1;                   # �ߥ�������ä�
					$rouryoku = 9;                   # ϫ��
				}

				if ( $kind == $HcomMissileMGM ) {    # ����ͶƳ�Ƥλ�
					my ($Mcount);
					for ( $Mcount = 0 ; $Mcount < $HpointNumber ; $Mcount++ ) {
						$x = $Hrpx[$Mcount];
						$y = $Hrpy[$Mcount];
						if ( $tLand->[$x][$y] == $HlandMonster ) {
							my ($special) =
							  $HmonsterSpecial[ (
								  monsterSpec( $tLandValue->[$x][$y] ) )[0] ];
							if (
								(
									   ( $special == 3 )
									&& ( ( $HislandTurn % 2 ) == 1 )
								)
								|| (   ( $special == 4 )
									&& ( ( $HislandTurn % 2 ) == 0 ) )
							  )
							{

					  #								(($special == 4) && (($HislandTurn % 2) == 0)) ||
					  #								($special == 5)){
							}
							else {
								last;
							}
						}
					}
					if ( $Mcount >= $HpointNumber ) {
						logMiss( $id, $name, $comName,
							"Ŭ���ʲ��ä����ʤ��ä�" );
						$island->{$mcost} += $cost;
						return 0;
					}
				}

				# ����������
				my ($r) = random($err);
				$r = 0 if ( ( $kind == $HcomMissileSPP ) && ( $r == 7 ) );
				$r += 19 if ( $kind == $HcomMissileRNG );
				$tx = $x + $ax[$r];
				$ty = $y + $ay[$r];
				$tx-- if ( !( $ty % 2 ) && ( $y % 2 ) );

				my ( $wkind, $wname, $whp, $wkind2, $wkind3 ) =
				  weatherinfo( $island->{'weather'} );
				my ( $twkind, $twname, $twhp, $twkind2, $twkind3 ) =
				  weatherinfo( $tIsland->{'weather'} );

				if ( $kind != $HcomMissileMGM )
				{    # ����ͶƳ�Ƥϳ����ʤ�
					    # ŷ�������å�
					if (
						   ( $id != $target )
						&& ( $kind != $HcomMissileRM )
						&& # ��ʬ��������Ω�ƥߥ������ŷ���˺�������ʤ���
						( $island->{'eis3'} != 1 ) &&    # ����������̵��
						(
							   ( ( $wkind >= 2 ) && ( random(6) == 0 ) )
							|| ( ( $twkind >= 2 ) && ( random(6) == 0 ) )
						)
					  )
					{
						$mslogCtW++;
						next;
					}

					# ���������ϥ����å�
					if ( ( $id != $target ) && ( $tIsland->{'aegis'} > 0 ) ) {
						$tIsland->{'aegis'}--;
						if (   ( random(3) == 0 )
							&& ( $tIsland->{'money'} > 100 ) )
						{

							#					HdebugOut("���������Ϥ��ɤ���");
							$tIsland->{'money'} -= 100;
							$mslogCtD++;
							next;
						}
					}

					# �ɱұ��������å�
					if (   ( $id != $target )
						&& ( $tIsland->{'eis4'} )
						&& ( random(2) == 0 ) )
					{

						#				HdebugOut("�ɱұ������ɤ���");
						$tIsland->{'eis4'}++;
						$mslogCtD++;
						next;
					}

					# �������ϰ��⳰�����å�
					if (   ( $tx < 0 )
						|| ( $tx >= $HislandSize )
						|| ( $ty < 0 )
						|| ( $ty >= $HislandSize ) )
					{
						$mslogCtM++;
						next;
					}
				}

				# ���������Ϸ�������
				my ( $tL, $tLv ) =
				  ( $tLand->[$tx][$ty], $tLandValue->[$tx][$ty] );
				my ( $tLname, $tPoint ) =
				  ( landName( $tL, $tLv ), "($tx, $ty)" );

				if ( $tIsland->{'defence'} > 0 ) {

					# �ɱһ��ߤ������� �ɱһ���Ƚ��
					my ($defence) = 0;
					if ( $HdefenceHex[$target][$tx][$ty] == 1 ) {
						$defence = 1;
					}
					elsif (( $tL == $HlandDefence )
						|| ( ( $tL == $HlandOil ) && ( $tLv == 5 ) ) )
					{

					 # �ɱһ��ߤ�̿��
					 #				HdebugOut("�ɱһ��ߤ�̿��:($tx,$ty) = ${tLv}");
						if ( $tLv == 2 ) {
							$tLandValue->[$tx][$ty] = 0;
							$defence = 1;
							logDefenceD( $id, $target, $tName,
								landName( $HlandDefence, 0 ),
								"($tx, $ty)" );
						}
						elsif ( $tLv == 3 ) {
							$tLandValue->[$tx][$ty] = 2;
							$defence = 1;
							logDefenceD( $id, $target, $tName,
								landName( $HlandDefence, 2 ),
								"($tx, $ty)" );
						}
						elsif ( $tLv == 11 ) {
							$tLandValue->[$tx][$ty] = 10;
							$defence = 1;
							logDefenceD( $id, $target, $tName,
								landName( $HlandDefence, 10 ),
								"(?, ?)" );
						}
						elsif ( $tLv == 21 ) {
							$tLandValue->[$tx][$ty] = 20;
							$defence = 1;
							logDefenceD( $id, $target, $tName,
								landName( $HlandDefence, 20 ),
								"($tx, $ty)" );
						}
						else {

							# �ե饰�򥯥ꥢ
							my ( $i, $count, $sx, $sy );
							for ( $i = 0 ; $i < 19 ; $i++ ) {
								$sx = $tx + $ax[$i];
								$sy = $ty + $ay[$i];
								$sx--
								  if ( !( $sy % 2 ) && ( $ty % 2 ) )
								  ;    # �Ԥˤ�����Ĵ��
								if (   ( $sx < 0 )
									|| ( $sx >= $HislandSize )
									|| ( $sy < 0 )
									|| ( $sy >= $HislandSize ) )
								{

									# �ϰϳ��ξ�粿�⤷�ʤ�
								}
								else {

									# �ϰ���ξ��
									$HdefenceHex[$target][$sx][$sy] = 0
									  if (
										$HdefenceHex[$target][$sx][$sy] != -1 );
								}
							}
						}
					}
					elsif ( $HdefenceHex[$target][$tx][$ty] == -1 ) {
						$defence = 0;
					}
					elsif ( chkAround( $tLand, $tx, $ty, $HlandDefence, 19 ) ) {
						$HdefenceHex[$target][$tx][$ty] = 1;
						$defence = 1;
					}
					elsif (
						chkAroundEX(
							$tLand, $tLandValue, $tx, $ty, $HlandOil, 5, 19
						)
					  )
					{
						$HdefenceHex[$target][$tx][$ty] = 1;
						$defence = 1;
					}
					else {
						$HdefenceHex[$target][$tx][$ty] = -1;
						$defence = 0;
					}

					if ( ( $defence == 1 ) && ( $kind != $HcomMissileMGM ) ) {

						# ��������
						$mslogCtD++;
						if ( $kind == $HcomMissileST ) {    # ���ƥ륹
							logMsCaughtH( $target, $name, $comName )
							  if ( random(25) == 0 );
						}
						if ( random(25) == 0 ) {

							# S�ɱһ��ߤ˿ʲ����롣
							my ( $i, $sx, $sy );
							for ( $i = 1 ; $i < 19 ; $i++ ) {
								$sx = $tx + $ax[$i];
								$sy = $ty + $ay[$i];
								$sx--
								  if ( !( $sy % 2 ) && ( $ty % 2 ) )
								  ;    # �Ԥˤ�����Ĵ��
								if (   ( $sx < 0 )
									|| ( $sx >= $HislandSize )
									|| ( $sy < 0 )
									|| ( $sy >= $HislandSize ) )
								{

									# �ϰϳ��ξ�粿�⤷�ʤ�
								}
								elsif (( $tLand->[$sx][$sy] == $HlandDefence )
									&& ( $tLandValue->[$sx][$sy] == 0 ) )
								{
									logDefenceS( $id, $target, $tName,
										landName( $HlandDefence, 0 ),
										"($sx, $sy)" );
									$tLandValue->[$sx][$sy] = 2;
									last;
								}
								elsif (( $tLand->[$sx][$sy] == $HlandDefence )
									&& ( $tLandValue->[$sx][$sy] == 2 ) )
								{
									logDefenceS( $id, $target, $tName,
										landName( $HlandDefence, 2 ),
										"($sx, $sy)" );
									$tLandValue->[$sx][$sy] = 3;
									last;
								}
								elsif (( $tLand->[$sx][$sy] == $HlandDefence )
									&& ( $tLandValue->[$sx][$sy] == 10 ) )
								{
									logDefenceS( $id, $target, $tName,
										landName( $HlandDefence, 10 ),
										"(?, ?)" );
									$tLandValue->[$sx][$sy] = 11;
									last;
								}
								elsif (( $tLand->[$sx][$sy] == $HlandDefence )
									&& ( $tLandValue->[$sx][$sy] == 20 ) )
								{
									logDefenceS( $id, $target, $tName,
										landName( $HlandDefence, 20 ),
										"($sx, $sy)" );
									$tLandValue->[$sx][$sy] = 21;
									last;
								}
							}
						}
						next;
					}
				}

				# ž�����֤���������
				if ( $tL == $HlandWarp ) {
					logOut(
"--- ${HtagName_}$tPoint${H_tagName}��<B>${tLname}</B>�����ơ�<B>�����ζ��֤˵ۤ����ޤ�ޤ�������</B>",
						$id, $target
					);

					#		$tLand->[$tx][$ty] = $HlandWaste;
					#		$tLandValue->[$tx][$ty] = 0;
					my ($st) = warp( $id, $name, 0, 0, $comName, $tLv, 11 );
					next;
				}

				# ���Ω����
				if ( $kind == $HcomMissileRM ) {
					if (   ( $tIsland->{'area'} < $HdisFallBorder )
						&& ( ( $tL == $HlandSea ) && ( $tLv <= 1 ) ) )
					{
						if ( ( $tL == $HlandSea ) && ( $tLv == 0 ) ) {
							$tLand->[$tx][$ty]      = $HlandSea;
							$tLandValue->[$tx][$ty] = 1;
							logMsNormal( $id, $target, $tLname, $tPoint,
								"δ����" );
						}
						else {
							$tLand->[$tx][$ty]      = $HlandWaste;
							$tLandValue->[$tx][$ty] = 1;
							$tIsland->{'area'}++;
							logMsNormal( $id, $target, $tLname, $tPoint,
								"δ����" );
						}
					}
					else {
						$mslogCtD++;
					}
					next;
				}

				# ���������Ω����
				if ( $kind == $HcomMissileSRM ) {
					if ( ( $tL == $HlandSea ) && ( $tLv > 0 ) ) {

						# �����ط��λ�
						$tLand->[$tx][$ty]      = $HlandWaste;
						$tLandValue->[$tx][$ty] = 1;
						$tIsland->{'area'}++;
					}
					elsif ( $HseaChk[$tL] ) {

						# ���ط��λ�
						$tLand->[$tx][$ty]      = $HlandSea;
						$tLandValue->[$tx][$ty] = 1;
					}
					else {
						$tLand->[$tx][$ty]      = $HlandWaste;
						$tLandValue->[$tx][$ty] = 1;
					}
					logMsNormal( $id, $target, $tLname, $tPoint, "δ����" );
					next;
				}

				# �˥ߥ�����
				if ( $kind == $HcomMissileNCM ) {
					logOut(
"�ˤϡ�${HtagName_}${tName}${AfterName}$tPoint${H_tagName}��<B>$tLname</B>��̿�椷���Ϥˤ��ﳲ���Фޤ�����",
						$id, $target
					);
					wideDamage( $target, $tName, $tLand, $tLandValue, $tx, $ty,
						1 );
					$tIsland->{'trump'}->[15] =
					  1;    # �ȥ��ץ��٥�ȥ���󥻥�
					next;
				}

				# �ָ��̤ʤ���hex��ǽ��Ƚ��
				if (
					( ( $tL == $HlandSea ) && ( $tLv == 0 ) ) ||    # ������
					(
						(
							( ( $tL == $HlandSea ) && ( $tLv <= 1 ) )
							|| (   ( $tL == $HlandOsen )
								&& ( $kind != $HcomBioMissile ) )
							|| (   ( $HmonumentMissile == 1 )
								&& ( $tL == $HlandMonument ) )
							||    # �ʵ�ǰ��������)
							( $tL == $HlandSMonument )
							||    # ���쵭ǰ��ޤ��ϡ�����
							( $tL == $HlandSbase )
							||    # ������Ϥޤ��ϡ�����
							( $tL == $HlandMountain )
						)         # ���ǡ�����
						&& ( $DestMissile == 0 )
					)
				  )
				{                 # �˲��ߥ�����ʳ�
					$mslogCtM++;    # ̵����
					next;
				}

				# �Ƥμ����ʬ��
				if ( $DestMissile == 1 ) {

					# �˲��ߥ������

					if ( $tL == $HlandMountain ) {

						# ��(���Ϥˤʤ�)
						logMsLD( $id, $target, $tPoint,
							"��<B>$tLname</B>��̿�椷���ϤȲ���" );
						$tLand->[$tx][$ty]      = $HlandWaste;
						$tLandValue->[$tx][$ty] = 0;
						next;

					}
					elsif ( $tL == $HlandSbase ) {

						# �������
						logMsLD( $id, $target, $tPoint,
"��������ȯ��<B>$tLname</B>���׷���ʤ��ʤ�"
						);
					}
					elsif ( $tL == $HlandMonster ) {

						# ����
						logMsLD( $id, $target, $tPoint,
"�����Ƹ���ȯ��<B>����$tLname</B>���Ȥ���פ�"
						);
					}
					elsif ( $tL == $HlandSea || $tL == $HlandBreakwater ) {

						# ������������
						logMsLD( $id, $target, $tPoint,
							"��<B>$tLname</B>�����ơ����줬�������"
						);
					}
					elsif ( $tL == $HlandKInora ) {

						# ���ۤ��Τ�
						$mslogCtD++;    # ��������
						next;
					}
					else {

						# ����¾
						logMsLD( $id, $target, $tPoint,
							"��<B>$tLname</B>�����ơ�Φ�ϤϿ��פ�" );
					}

					# �и���
					if ( $tL == $HlandTown ) {
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandSbase ) )
						{

							# �ޤ����Ϥξ��Τ�
							$landValue->[$bx][$by] += int( $tLv / 20 );
							$island->{'allex'}     +=
							  int( $tLv / 20 );    # �и�����������
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
						}
					}

					# �����ˤʤ�
					$tLand->[$tx][$ty] = $HlandSea;
					$tIsland->{'area'}--;
					$tLandValue->[$tx][$ty] = 1;
					$tIsland->{'nation'}->[$tx][$ty] = $id
					  if ( $id != $target );

					# �Ǥⳤ���Ϸ��ʤ鳤
					$tLandValue->[$tx][$ty] = 0 if ( $HseaChk[$tL] );

					$tIsland->{'trump'}->[$tLv] = 0 if ( $tL == $HlandTrump );
				}
				else {

					# ����¾�ߥ�����
					if ( ( $tL == $HlandWaste ) && ( $tLv <= 1 ) ) {

						# ����
						if ( $kind == $HcomBioMissile ) {
							logBioMs( $id, $target, $tLname, $tPoint );
						}
						else {

							# �ﳲ�ʤ�
							$mslogCtM++;    # ̵���ߥ�����˥������
						}
					}
					elsif ( $tL == $HlandHugecity ) {

						# Ķ�����ԻԤϥߥ����뤬�����ʤ���
						$mslogCtM++;        # ̵���ߥ�����˥������
						next;
					}
					elsif ( $tL == $HlandMonster ) {

						# ����
						my ( $mKind, $mName, $mHp ) = monsterSpec($tLv);
						my ($special) = $HmonsterSpecial[$mKind];

						# ȿ�⤤�Τ�(ST�ʳ�)
						if (   ( $mKind == 18 )
							&& ( random(2) == 0 )
							&& ( $kind != $HcomMissileST ) )
						{
							if ( random(20) == 0 ) {
								logMonsCounter( $id, $target, $mName, $tPoint,
									"������Ф�ƤӴ󤻤ޤ�����" );
								$island->{'bigmissile'}++;
							}
							else {
								logMonsCounter( $id, $target, $mName, $tPoint,
									"��Ф�Ƥܤ��Ȥ��Ƥ��롣" );
								$island->{'Meteo'} += 10;
							}
							next;
						}

						# �Ų���?
						if (
							(
								   ( $special == 3 )
								&& ( ( $HislandTurn % 2 ) == 1 )
							)
							|| (   ( $special == 4 )
								&& ( ( $HislandTurn % 2 ) == 0 ) )
							|| ( ( $special == 5 ) && ( random(4) != 0 ) )
						  )
						{

							# �Ų���
							if ( $kind == $HcomMissileST ) {

								# ���ƥ륹
								logMsMonNoDamageS(
									$id,      $target, $name,  $tName,
									$comName, $mName,  $point, $tPoint
								);
							}
							else {

								# �̾���
								logMsMonNoDamage( $id, $target, $mName,
									$tPoint );
							}
							next;
						}
						else {

							# �Ų��椸��ʤ�
							if ( $mHp == 1 ) {

								# ���Τ饴�����Ȥ����Х��쥤��
								if ( ( $mKind == 5 ) && ( random(5) == 0 ) ) {
									logMonsRei( $id, $target, $mName, $tPoint );
									$tLandValue->[$tx][$ty] =
									  1500 + $HmonsterBHP[15] +
									  random( $HmonsterDHP[15] );
									next;
								}

								# ���ä��Ȥ᤿�Ȥ��ηи���
								if (   ( $land->[$bx][$by] == $HlandBase )
									|| ( $land->[$bx][$by] == $HlandSbase ) )
								{
									$landValue->[$bx][$by] +=
									  $HmonsterExp[$mKind];
									$island->{'allex'} +=
									  $HmonsterExp[$mKind]
									  ;    # �и�����������
									$landValue->[$bx][$by] = $HmaxExpPoint
									  if ( $landValue->[$bx][$by] >
										$HmaxExpPoint );
								}

								# ���ñ¼����ե饰��Ω�Ƥ�

								$island->{'esa'}  = $mKind;
								$tIsland->{'esa'} = $mKind;

								# ���äξ޴ط�
								monstersPrize( $mKind, $island );

						   # ������ɥ������Ȥ�������ˤʤ롣
								if ( $mKind == 31 ) {
									logMonsGold(
										$id,      $target, $name,  $tName,
										$comName, $mName,  $point, $tPoint
									);
									$tLand->[$tx][$ty]      = $HlandMonument;
									$tLandValue->[$tx][$ty] = 9;
								}
								elsif ( $kind == $HcomMissileST ) {

									# ���ƥ륹
									logMsMonKillS(
										$id,      $target, $name,  $tName,
										$comName, $mName,  $point, $tPoint
									);
								}
								else {

									# �̾�
									logMsMonKill(
										$id,    $target, $name,
										$tName, $mName,  $tPoint
									);
								}

								# ����
								my ($value) = $HmonsterValue[$mKind];
								if ( $value > 0 ) {
									if ( $target <= 90 ) {
										$tIsland->{'money'} += $value;
										logMsMonMoney( $target, $mName,
											$value );
									}
									else {
										$island->{'money'} += $value;
										logMsMonMoney( $id, $mName, $value );
									}
								}
								next if ( $mKind == 31 );
							}
							else {

								# ���������Ƥ�
								if ( $kind == $HcomMissileST ) {

									# ���ƥ륹
									logMsMonsterS(
										$id,      $target, $name,  $tName,
										$comName, $mName,  $point, $tPoint
									);
								}
								else {

									# �̾�
									logMsMonster( $id, $target, $mName,
										$tPoint );
								}

								# HP��1����
								$tLandValue->[$tx][$ty]--;
								if (
									( $kind == $HcomBioMissile )
									&& (   ( $mKind == 6 )
										|| ( $mKind == 7 )
										|| ( $mKind == 8 ) )
								  )
								{
									if ( random(4) == 0 )
									{    # �����ˤ���ü��Ѱ�
										if ( random(2) == 0 ) {
											$tLandValue->[$tx][$ty] =
											  1300 + $HmonsterBHP[13] +
											  random( $HmonsterDHP[13] );
										}
										else {
											$tLandValue->[$tx][$ty] =
											  1400 + $HmonsterBHP[14] +
											  random( $HmonsterDHP[14] );
										}
										my ( $afmKind, $afmName, $afmHp ) =
										  monsterSpec(
											$tLandValue->[$tx][$ty] );
										logMonsC(
											$target, $name, $point,
											$mName,  $afmName
										);
									}
								}
								next;
							}
						}
					}
					elsif (( $tL == $HlandTown )
						|| ( $tL == $HlandTower )
						|| ( $tL == $HlandFactory )
						|| ( $tL == $HlandPort )
						|| ( $tL == $HlandFarm )
						|| ( $tL == $HlandBase ) )
					{

			   # Į�����졢���졢���ȥӥ롢�����ߥ��������
						my ($result) = "�ﳲ�����";
						my ( $break, $Ept ) = ( 0, 2 );
						if ( $tL == $HlandFarm ) {    # ����
							$tLandValue->[$tx][$ty] -= 5;
							$tLandValue->[$tx][$ty] -= 5
							  if ( $kind == $HcomMissileGM );
							if ( $tLandValue->[$tx][$ty] < 10 ) {
								$result = "���Ǥ�";
								$break  = 1;
								$Ept    = 4;
							}
						}
						elsif ( $tL == $HlandBase ) {
							$tLandValue->[$tx][$ty] -= 50;
							$tLandValue->[$tx][$ty] -= 50
							  if ( $kind == $HcomMissileGM );
							if ( $tLandValue->[$tx][$ty] < 0 ) {
								$result = "���Ǥ�";
								$break  = 1;
								$Ept    = 4;
							}
						}
						elsif ( $tL == $HlandPort ) {
							$tLandValue->[$tx][$ty] -= 40;
							$tLandValue->[$tx][$ty] -= 40
							  if ( $kind == $HcomMissileGM );
							if ( $tLandValue->[$tx][$ty] < 40 ) {
								$result = "���Ǥ�";
								$break  = 1;
								$Ept    = 4;
							}
						}
						elsif ( $tL == $HlandTown ) {
							my $p = 100;
							$p = 80 if ( $tIsland->{'Hospital'} == 1 );
							$tLandValue->[$tx][$ty] -= $p;
							$tLandValue->[$tx][$ty] -= $p
							  if ( $kind == $HcomMissileGM );
							if ( $tLandValue->[$tx][$ty] < 1 ) {
								$result = "���Ǥ�";
								$break  = 1;
								$Ept    = 0;
							}
							else {
								$Ept = 5;
								$boat += $p;
							}
						}
						else {
							$tLandValue->[$tx][$ty] -= 10;
							$tLandValue->[$tx][$ty] -= 10
							  if ( $kind == $HcomMissileGM );
							if ( $tLandValue->[$tx][$ty] < 30 ) {
								$result = "���Ǥ�";
								$break  = 1;
								$Ept    = 4;
							}
						}
						if ( $kind == $HcomMissileST ) {    # ���ƥ륹
							logMsNormalS(
								$id,    $target,  $name,
								$tName, $comName, $tLname,
								$point, $tPoint,  $result
							);
						}
						elsif (( $kind == $HcomBioMissile )
							&& ( $break == 1 ) )
						{                                   # �Х���
							logBioMs( $id, $target, $tLname, $tPoint );
						}
						else {                              # �̾�
							logMsNormal( $id, $target, $tLname, $tPoint,
								$result );
						}

						# �и���
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandSbase ) )
						{
							$landValue->[$bx][$by] += $Ept;
							$island->{'allex'}     +=
							  $Ept;    # �и�����������
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
						}
						next if ( $break == 0 );
					}
					elsif (( $tL == $HlandMegacity )
						|| ( $tL == $HlandMegaFarm )
						|| ( $tL == $HlandMegaFact )
						|| ( $tL == $HlandMegatower ) )
					{

						# �����Ϸ��ΤȤ�
						my ( $tL2, $tLname2 );
						if ( $tL == $HlandMegaFact ) {
							$tL2                    = $HlandFactory;
							$tLand->[$tx][$ty]      = $tL2;
							$tLandValue->[$tx][$ty] = 90;
							$tLname2                = landName( $tL2, 90 );
						}
						elsif ( $tL == $HlandMegaFarm ) {
							$tL2                    = $HlandFarm;
							$tLand->[$tx][$ty]      = $tL2;
							$tLandValue->[$tx][$ty] = 50;
							$tLname2                = landName( $tL2, 50 );
						}
						else {
							if ( $tL == $HlandMegacity ) {
								$tL2 = $HlandTown;
								$boat += 300
								  ; # �̾�ߥ�����ʤΤ���̱�˥ץ饹
							}
							elsif ( $tL == $HlandMegatower ) {
								$tL2 = $HlandTower;
							}
							$tLand->[$tx][$ty]      = $tL2;
							$tLandValue->[$tx][$ty] = 190;
							$tLname2 = landName( $tL2, 190 );
						}
						my ($result) =
						  "�ﳲ�����${tLname2}����äƤ��ޤ�";

						if ( $kind == $HcomMissileST ) {    # ���ƥ륹
							logMsNormalS(
								$id,    $target,  $name,
								$tName, $comName, $tLname,
								$point, $tPoint,  $result
							);
						}
						else {                              # �̾�
							logMsNormal( $id, $target, $tLname, $tPoint,
								$result );
						}

						# �����Ϸ��ΤȤ��ηи���
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandSbase ) )
						{
							$landValue->[$bx][$by] += 10;
							$island->{'allex'} += 10; # �и�����������
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
						}
						next;
					}
					elsif ( ( $tL > 100 ) && ( $tL < 120 ) ) {

						# ���Ϥξ��
						my ( $order, $hp, $sId ) = shipSpec($tLv);
						if ( ( $hp <= 1 ) || ( $tL == $HlandBalloonS ) ) {

							# ������(�������ϰ��ǳ���)
							if ( $tL == $HlandPirate ) {
								if ( random(5) == 0 ) {

									# ��±�����������ͩ�����и�
									$tIsland->{'ghost'} = $target;
								}
								elsif (( $sId == 0 )
									&& ( $kind != $HcomMissileST ) )
								{

									# ��±�� ��°������
									logMsShip( $id, $target, $tLname, $tPoint,
										$tL, "��ǰ���ޤ�����" );
									$tLandValue->[$tx][$ty] = 21000 + $id;
									next;
								}
							}
							elsif ( $tL == $HlandTreasureS ) {

								# ����
								$island->{'money'}  += 5000;
								$tIsland->{'money'} += 5000;

							   #��󥭥��ѥ��ե�����񤭽Ф�
								open( MOUT, ">>${HlogdirName}/money.log" );
								print MOUT "$HislandTurn,$id,����,5000\n";
								print MOUT "$HislandTurn,$target,����,5000\n";
								close(MOUT);
							}
							elsif ( $tL == $HlandBalloonS ) {

								# ������
								if ( $kind == $HcomMissileST ) {
									logMsShipS(
										$id,      $target,
										$name,    $tName,
										$comName, $tLname,
										$point,   $tPoint,
										"���ޤ�����"
									);
								}
								else {
									my $tLand2      = $tIsland->{'land2'};
									my $tLandValue2 = $tIsland->{'landValue2'};

									my $p = random(100);
									if ( $p < 20 ) {    # ���
										my $r = random(10000);
										$tIsland->{'money'} += $r;
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}�γ���������첿�Τ�������äƤ���$r$HunitMoney���ߤäƤ��ޤ�����",
											$id, $target
										);

							   #��󥭥��ѥ��ե�����񤭽Ф�
										open( MOUT,
											">>${HlogdirName}/money.log" );
										print MOUT
										  "$HislandTurn,$id,������,$r\n";
										close(MOUT);
									}
									elsif ( $p < 30 ) {    # ����
										$tIsland->{'food'} += 10000;
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}�γ���������첿�Τ�������äƤ����������ߤäƤ��ޤ�����",
											$id, $target
										);
									}
									elsif ( $p < 45 ) {    # ����
										$tLand->[$tx][$ty]      = $HlandFlower;
										$tLandValue->[$tx][$ty] =
										  random(13) + 1;
										$tLand2->[$tx][$ty]      = $HlandSea;
										$tLandValue2->[$tx][$ty] = 0;
										my $mName =
										  landName( $HlandFlower,
											$tLandValue->[$tx][$ty] );
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}�γ���������줿��Ʊ�����椫�����̤�<B>$mName</B>���ߤäƤ��ޤ�������",
											$id, $target
										);
									}
									elsif ( $p < 60 ) {    # ���
										$tIsland->{'Meteo'} += 10;
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}�γ����������ޤ���",
											$id, $target
										);
									}
									elsif ( $p < 68 ) {    # �������
										$tIsland->{'bigmissile'}++;
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}�γ���������������и������۶��֤���<b>�������</b>������ޤ�����",
											$id, $target
										);
									}
									elsif ( $p < 88 ) {    # �Ͽ�
										$tIsland->{'prepare2'} += 10;
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}�γ����������ޤ���",
											$id, $target
										);
									}
									elsif ( $p < 98 ) {    # ������������
										$tLand->[$tx][$ty]      = $HlandMonster;
										$tLandValue->[$tx][$ty] = 2105;
										$tLand2->[$tx][$ty]     = $HlandSea;
										$tLandValue2->[$tx][$ty] = 0;
										my $mName = ( monsterSpec(2105) )[1];
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}�γ���������줿��Ʊ���˰۶��֤���ǡ�Ȥ��ƹ������椫��<B>����$mName</B>���и����ޤ�������",
											$id, $target
										);
									}
									else {    # ������ɥ�������
										$tLand->[$tx][$ty]      = $HlandMonster;
										$tLandValue->[$tx][$ty] =
										  3100 + $HmonsterBHP[31] +
										  random( $HmonsterDHP[31] );
										$tLand2->[$tx][$ty]      = $HlandSea;
										$tLandValue2->[$tx][$ty] = 0;
										my $mName = ( monsterSpec(3100) )[1];
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}�γ���������줿��Ʊ���˰۶��֤���ǡ�Ȥ��ƹ������椫��<B>����$mName</B>���и����ޤ�������",
											$id, $target
										);
									}

							   #��󥭥��ѥ��ե�����񤭽Ф�
									my $rL = $tL - $HlandPirate;
									open( ROUT, ">>${HlogdirName}/ship.log" );
									print ROUT "$HislandTurn,$id,99,$rL\n";
									close(ROUT);
								}
							}

							# �����᤿�Ȥ��ηи���
							if (   ( $land->[$bx][$by] == $HlandBase )
								|| ( $land->[$bx][$by] == $HlandSbase ) )
							{
								$landValue->[$bx][$by] +=
								  $HshipEX[ $tL - $HlandPirate ];
								$island->{'allex'} +=
								  $HshipEX[ $tL - $HlandPirate ]
								  ;    # �и�����������
								$landValue->[$bx][$by] = $HmaxExpPoint
								  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
							}

							if ( $tL == $HlandBalloonS ) {
								next
								  if ( $tLand->[$tx][$ty] != $HlandBalloonS );
							}
							elsif ( $kind == $HcomMissileST ) {

								# ���ƥ륹
								logMsShipS(
									$id,      $target,
									$name,    $tName,
									$comName, $tLname,
									$point,   $tPoint,
									"���פ��ޤ�����"
								);
							}
							else {

								# �̾�
								logMsShip( $id, $target, $tLname, $tPoint, $tL,
									"���פ��ޤ�����" );
							}

						}
						else {

							# �����᡼��
							if ( $kind == $HcomMissileST ) {

								# ���ƥ륹
								logMsShipS(
									$id,
									$target,
									$name,
									$tName,
									$comName,
									$tLname,
									$point,
									$tPoint,
									"���᡼��������ޤ�����"
								);
							}
							else {

								# �̾�
								logMsShipD( $id, $target, $tLname, $tPoint, $tL,
									"���᡼��������ޤ�����" );
							}

							# HP��1����
							$tLandValue->[$tx][$ty] -= 1000;
							next;
						}
					}
					elsif ( $tL == $HlandKInora ) {

						# ���ۤ��Τ�
						my ( $limit, $hp, $ld, $d ) = bigMonsterSpec($tLv);
						if ( $kind == $HcomMissileST ) {
							$mslogCtD++;    # ��������
							next;
						}
						$tLandValue->[$tx][$ty] += 100 if ( $hp < 100 );
						if ( $d == 0 ) {

							# �濴
							logOut(
"--- ${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�椷�ޤ����������̤�̵���Ф��꤫�������Ƥ���褦����",
								$id, $target
							);
						}
						else {

							# �и���
							if (   ( $land->[$bx][$by] == $HlandBase )
								|| ( $land->[$bx][$by] == $HlandSbase ) )
							{
								$landValue->[$bx][$by] += 2;
								$island->{'allex'}     += 2;
								$landValue->[$bx][$by] = $HmaxExpPoint
								  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
							}

							# �饹�ȥ��᡼����¸
							$lastDamage = $id;
							logOut(
"--- ${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�椷��<B>����$tLname</B>�ϥ��᡼��������ޤ�����",
								$id, $target
							);
						}
						next;
					}
					elsif ( ( $tL == $HlandTrump ) && ( $tLv == 0 ) ) {

						# �ȥ���
						my $tNumber = random(14) + 1;
						$tLandValue->[$tx][$ty] = $tNumber;
						my $tLname2 = landName( $tL, $tNumber );
						if ( $kind == $HcomMissileST ) {    # ���ƥ륹
							logMsNormalS( $id, $target, $name, $tName, $comName,
								$tLname, $point, $tPoint,
								"�᤯���<b>${tLname2}</b>�ˤʤ�" );
						}
						else {                              # �̾�
							logMsNormal( $id, $target, $tLname, $tPoint,
								"�᤯���<b>${tLname2}</b>�ˤʤ�" );
						}
						if ( $tIsland->{'trump'}->[15] != 1 ) {

							# �˥ߥ����뤬�⤿��Ƥ��ʤ���
							my ($i);
							for ( $i = 1 ; $i < 14 ; $i++ ) {
								next if ( $tIsland->{'trump'}->[$i] != 1 );
								if ( $i == $tNumber ) {

									# Ʊ���ֹ�
									my $str = "";
									my $r   = 0;
									if ( $i < 6 ) {
										$r   = 10000;
										$str =
"�޶��${r}${HunitMoney}���åȤ�";
									}
									elsif ( $i < 10 ) {
										$r   = 5000;
										$str =
"�޶��${r}${HunitMoney}���åȤ�";
										$island->{'event2'} = 1;
									}
									elsif ( $i < 13 ) {
										$r   = 4000;
										$str =
"�޶��${r}${HunitMoney}�ȥץ쥼��ȥ��åȤ򥲥åȤ�";
										$island->{'present'}->[4]++;
										$island->{'present'}->[5]++;
										$island->{'present'}->[8]++;
									}
									if ( $r == 0 ) {
										$island->{'present'}->[7]++; # ���Ի�
										$str =
"���Τ����ԻԤ�����ͽ��ˤʤ�";
									}
									else {
										$island->{'money'} += $r;
										open( MOUT,
											">>${HlogdirName}/money.log" );
										print MOUT
										  "$HislandTurn,$id,�ȥ���,$r\n";
										close(MOUT);
									}
									logOut(
"${HtagName_}$name${AfterName}${H_tagName}�ϡ������������ɤ�·��${str}�ޤ�����",
										$id, $target
									);
									$tLand->[$tx][$ty]      = $HlandWaste;
									$tLandValue->[$tx][$ty] = 1;
									last;
								}
							}
						}
						if ( $tLandValue->[$tx][$ty] == 14 ) {

							# ���⤷����˥���ƥͥ��и�
							logOut(
"���硼������<B>����</B>��${HtagName_}${name}${AfterName}${H_tagName}�����߽Ф����Ȥ��Ƥ��롣",
								$id, $target
							);
							$island->{'monstersend2'}++;
						}
						else {
							$tIsland->{'trump'}->[$tNumber] = 1;
						}
						next;
					}
					else {

						# �̾��Ϸ�
						if ( $kind == $HcomMissileST ) {    # ���ƥ륹
							logMsNormalS(
								$id,    $target,  $name,
								$tName, $comName, $tLname,
								$point, $tPoint,  "���Ǥ�"
							);
						}
						elsif ( $kind == $HcomBioMissile ) {    # �Х���
							logBioMs( $id, $target, $tLname, $tPoint );
						}
						else {                                  # �̾�
							logMsNormal( $id, $target, $tLname, $tPoint,
								"���Ǥ�" );
						}
						$tIsland->{'trump'}->[$tLv] = 0
						  if ( $tL == $HlandTrump );
					}

					# �и���
					if (   ( ( $tL == $HlandTown ) || ( $tL == $HlandSlum ) )
						|| ( ( $tL == $HlandOil ) && ( $tLv >= 35 ) ) )
					{
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandSbase ) )
						{
							$landValue->[$bx][$by] += int( $tLv / 20 );
							$island->{'allex'}     +=
							  int( $tLv / 20 );    # �и�����������
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );

		 # ����ʳ��ΤȤ����̾�ߥ�����ʤΤ���̱�˥ץ饹
							$boat += $tLv if ( $tL != $HlandOil );
						}
					}
					elsif (( $tL == $HlandOil )
						&& ( $tLv >= 10 )
						&& ( $tLv <= 30 ) )
					{
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandSbase ) )
						{
							$landValue->[$bx][$by] += int( $tLv / 5 );
							$island->{'allex'}     +=
							  int( $tLv / 5 );    # �и�����������
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
						}
					}

					if ( $kind != $HcomMissileST ) {

						# ST�ߥ�����ʳ�
						if ( $tL == $HlandBank ) {

							# ��Ԥ��˲������Ȥ�
							$island->{'money'} += $tLv * 500;
							logMsBank( $id, $name, $tLv * 500 );
						}

						# ST�ߥ�����ʳ�����ͭ
						$tIsland->{'nation'}->[$tx][$ty] = $id
						  if ( ( $tLand->[$tx][$ty] != $HlandWaste )
							&& ( $id != $target ) );
					}

					if (   ( $tL == $HlandOil )
						|| ( ( $tL > 100 ) && ( $tL < 120 ) ) )
					{

						# ���ġ����Ϥ��ä��鳤
						$tLand->[$tx][$ty]      = $HlandSea;
						$tLandValue->[$tx][$ty] = 0;
					}
					elsif (( ( $tL == $HlandSea ) && ( $tLv >= 10 ) )
						|| ( ( $tL == $HlandBreakwater ) && ( $tLv >= 1 ) ) )
					{

						# �ܿ��졢��������ä�������
						$tLand->[$tx][$ty]      = $HlandSea;
						$tLandValue->[$tx][$ty] = 1;
					}
					elsif ( $kind == $HcomBioMissile ) {

						# �Х����ߥ�����λ��ϱ���
						if ( ( $tL == $HlandOsen ) && ( $tLv < 10 ) ) {
							$tLandValue->[$tx][$ty]++;
						}
						elsif ( $tL != $HlandOsen ) {
							$tLand->[$tx][$ty]      = $HlandOsen;
							$tLandValue->[$tx][$ty] = 1;
						}
					}
					else {

						# ����¾�Ϲ��Ϥˤʤ�
						$tLand->[$tx][$ty]      = $HlandWaste;
						$tLandValue->[$tx][$ty] = 1;             # ������
					}
				}
			}

			# ����������䤷�Ȥ�
			$count++;
		}

		if ( $flag == 0 ) {

			# ���Ϥ���Ĥ�̵���ä����
			logMsMiss( $id, $name, $comName );
			return 0;
		}

		$island->{'MissileA'} += $msCt;   # ȯ�Ϳ���׻�
		                                  # �ߥ�����ȯ�Ϳ��ʤɤΥ�
		if ( $kind == $HcomMissileST ) {  # ���ƥ륹
			logMissileS(
				$id,       $target,
				$name,     $tName,
				$comName,  $point,
				$msCt,     $msCt - $mslogCtM - $mslogCtW - $mslogCtD,
				$mslogCtM, $mslogCtW,
				$mslogCtD
			);
		}
		else {
			logMissile(
				$id,       $target,
				$name,     $tName,
				$comName,  $point,
				$msCt,     $msCt - $mslogCtM - $mslogCtW - $mslogCtD,
				$mslogCtM, $mslogCtW,
				$mslogCtD
			);
		}

		# ��̱Ƚ��
		$boat = ($HwarFlg) ? $boat : int( $boat / 2 );

#	HdebugOut("��̱�ǥХå���=${id}=>${target} ̿��=${kind} ��=${boat}");
		if (   ( $boat > 0 )
			&& ( $id != $target )
			&& ( $kind != $HcomMissileST ) )
		{
			my ($achive) = refugees( $boat, $island );

			#		HdebugOut("��̱�ǥХå���=${achive}");
			if ( $achive > 0 ) {

				# �����Ǥ����夷����硢�����Ǥ�
				logMsBoatPeople( $id, $name, $achive );
				$island->{'achive'} =
				  ($HwarFlg) ? 0 : $achive;    # ��̱����¸
				   # ��̱�ο���������ʾ�ʤ顢ʿ�¾ޤβ�ǽ������
				if ( $achive >= 200 ) {
					my ($prize) = $island->{'prize'};
					$prize =~ /([0-9]*),([0-9]*),(.*)/;
					my ( $flags, $monsters, $turns ) = ( $1, $2, $3 );

					if ( ( !( $flags & 8 ) ) && $achive >= 200 ) {
						$flags |= 8;
						logPrize( $id, $name, $Hprize[4] );
					}
					elsif ( ( !( $flags & 16 ) ) && $achive > 500 ) {

						$flags |= 16;
						logPrize( $id, $name, $Hprize[5] );
					}
					elsif ( ( !( $flags & 32 ) ) && $achive > 800 ) {
						$flags |= 32;
						logPrize( $id, $name, $Hprize[6] );
					}
					$island->{'prize'} = "$flags,$monsters,$turns";
				}
			}
			else {
				logOut(
"${HtagName_}${name}${AfterName}${H_tagName}�ˤɤ�����Ȥ�ʤ���̱��ɺ�夷�ޤ�������${HtagName_}${name}${AfterName}${H_tagName}�ϼ����������䤷���褦�Ǥ���",
					$id
				);
			}
		}

		if ( $kind2 == $HcomSpecialSPP ) {

			# ������Ƥ���ˤ��SPP
			return 0;
		}
		elsif ( ( $kind == $HcomMissileST ) || ( $kind == $HcomMissileNCM ) ) {

			# ���ƥ륹���ˤξ��Ͻ�λ
			if ( ( $kind == $HcomMissileNCM ) && ( $ncm == 0 ) )
			{    # �ߥ����������­�ǳˤ���Ƥʤ��ä�
				logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${AfterName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ����Ȥ��ޤ��������ߥ�������Ϥ���­�ˤ����ߤ���ޤ�����",
					$id
				);
				return 0;
			}
			return 1;
		}
		else {
			$island->{'Afmissile'} = 2;
			return 0;
		}

	}
	elsif ( ( $kind == $HcomSendMonster ) || ( $kind == $HcomSSendMonster ) ) {

		# �����ɸ�
		# �������åȼ���
		my ($tn)      = $HidToNumber{$target};
		my ($tIsland) = $Hislands[$tn];
		my ($tName)   = $tIsland->{'name'};

		if ( $tn eq '' ) {

			# �������åȤ����Ǥˤʤ�
			logMsNoTarget( $id, $name, $comName );
			return 0;
		}
		if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
			|| ( $tIsland->{'evil'} == 0 ) )
		{

			# ��꤬�Ӿ��ΰ���ߡ�
			logUNMiss( $id, $target, $name, $tName, $comName );
			return 0;
		}
		my $we = 100;
		if ( $kind == $HcomSSendMonster ) {
			if ( ($HsurvFlg) && ( $HislandTurn > $Hsstartturn ) ) {

				# ���Х��Х�ξ�������̵��
			}
			elsif (( $arg > 30 )
				|| ( ( 12 <= $arg ) && ( $arg <= 17 ) )
				|| ( $arg == 23 )
				|| ( $arg == 24 ) )
			{
				logMiss( $id, $name, $comName,
					"���÷�¤���Ǥ��ʤ����ä�" );
				return 0;
			}
			$we = 200;
		}
		if ( ( $kind == $HcomSSendMonster ) || ( $arg == 2 ) ) {
			if ( $island->{'weapon'} < $we ) {
				logMiss( $id, $name, $comName,
					"���÷�¤��ɬ�פ�ʼ����­��" );
				return 0;
			}
			$island->{'weapon'} -= $we;
		}
		$island->{'evil'} += 40 if ( $id != $target );

		# ��å�����
		logMonsSend( $id, $target, $name, $tName );
		$island->{'money'} -= $cost;
		if ( $kind == $HcomSSendMonster ) {
			addCommandLate( $HcomSSendMonsterTurn, $HislandTurn, $id, $kind,
				$target, $x, $y, $arg, $x2, $y2 );    # ������̿��
		}
		else {
			addCommandLate( $HcomSendMonsterTurn, $HislandTurn, $id, $kind,
				$target, $x, $y, $arg, $x2, $y2 );    # ������̿��
		}

		#CL		if($arg == 1){
		#CL			$tIsland->{'monstersend1'}++;
		#CL		}elsif($arg == 2){
		#CL			$tIsland->{'monstersend2'}++;
		#CL		}elsif($arg == 3){
		#CL			$tIsland->{'monstersend3'}++;
		#CL		}else{
		#CL			$tIsland->{'monstersend'}++;
		#CL		}
		return 1;
	}
	elsif (( $kind == $HcomManipulate )
		|| ( $kind == $HcomSTManipulate )
		|| ( $kind == $HcomShipM ) )
	{

		# ������ST�����������
		my ($tn) = $HidToNumber{$target};
		return 0
		  if ( $tn eq '' )
		  ;    # �������åȤ����Ǥˤʤ����Ჿ����鷺�����
		my ($tIsland) = $Hislands[$tn];
		my ($tName)   = $tIsland->{'name'};
		if ( $arg < 1 ) {
			$arg = 1;
		}
		elsif ( $arg >= 7 ) {
			$arg = 6;
		}
		if ( $kind == $HcomShipM ) {
			if ( $id == $target ) {

				# ����ξ��
				$tIsland->{'shipMoveM'}   = $arg;
				$tIsland->{'shipMoveMt'}  = $target;
				$tIsland->{'shipMoveMid'} = $id;
			}
			else {
				$tIsland->{'shipMoveT'}   = $arg;
				$tIsland->{'shipMoveTt'}  = $target;
				$tIsland->{'shipMoveTid'} = $id;
			}
			logManipulateS( $id, $target, $name, $tName, $comName );
		}
		else {
			$tIsland->{'manipulate'} = $arg;
			if ( $kind == $HcomManipulate ) {
				logManipulate( $id, $target, $name, $tName, $comName );
			}
			else {
				logManipulateS( $id, $target, $name, $tName, $comName );
			}
		}
		$island->{'money'} -= $cost;
		return 1;
	}
	elsif ( $kind == $HcomShip ) {

		# �������ѹ�
		my ($tn) = $HidToNumber{$target};
		return 0
		  if ( $tn eq '' );    # �������åȤ����Ǥˤʤ��������

		my ($tIsland)    = $Hislands[$tn];
		my ($tName)      = $tIsland->{'name'};
		my ($tLand)      = $tIsland->{'land'};
		my ($tLandValue) = $tIsland->{'landValue'};
		my ($tL)         = $tLand->[$x][$y];
		my ($tLv)        = $tLandValue->[$x][$y];

		return 0
		  if ( $HseaChk[$tL] != 2 )
		  ;                    # �������åȤ����Ǥʤ��������
		my ( $order, $hp, $sId ) = shipSpec($tLv);
		return 0
		  if ( $sId != $id );    # �������åȤ������Ǥʤ��������
		if ( $arg < 0 ) {
			$arg = 0;
		}
		elsif ( $arg >= 4 ) {
			$arg = 4;
		}
		return 0
		  if ( $order == $arg );    # �������åȤ�Ʊ�����᤿�����
		logShipOrderC( $id, $tName, landName( $tL, $tLv ),
			"($x, $y)", $Hshiporder[$arg] );
		$tLandValue->[$x][$y] = $arg * 10000 + $hp * 1000 + $sId;
		$island->{'money'} -= $cost;
		return 0;
	}
	elsif ( $kind == $HcomShipSell ) {

		# �����
		return 0
		  if ( $HseaChk[$landKind] != 2 )
		  ;                         # �������åȤ����Ǥʤ��������
		my ( $order, $hp, $sId ) = shipSpec($lv);
		return 0
		  if ( $sId != $id );    # �������åȤ������Ǥʤ��������
		$island->{'money'} += $HshipSell[ $landKind - $HlandPirate ];
		$land->[$x][$y]       = $land2->[$x][$y];
		$landValue->[$x][$y]  = $landValue2->[$x][$y];
		$land2->[$x][$y]      = $HlandSea;
		$landValue2->[$x][$y] = 0;
		logEventP( $id, $name, "($x, $y)",
			"��������Ѥ���ޤ�����" );
		return 0;
	}
	elsif ( $kind == $HcomEmigration ) {

		# ��̱
		my ($tn) = $HidToNumber{$target};
		return 0 if ( $tn eq '' );
		my ($tIsland) = $Hislands[$tn];
		my ($tName)   = $tIsland->{'name'};
		if ( ( $landKind == $HlandTown ) || ( $landKind == $HlandSlum ) ) {
			my ($boat) = $landValue->[$x][$y];
			$boat = int( $boat / 2 );
			my ($achive) = refugees( $boat, $tIsland );
			logRefugees( $id, $target, $name, $tName, $achive )
			  if ( $achive > 0 );
			$land->[$x][$y]      = $HlandPlains;
			$landValue->[$x][$y] = 0;
			$island->{'money'} -= $cost;
			$island->{'AfEmigra'} = 1;
			return 0;
		}
		else {
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
	}
	elsif ( $kind == $HcomSell ) {

		# ͢���̷���
		$arg = 1 if ( $arg == 0 );
		my ($value) = min( $arg * ( -$cost ), $island->{'food'} );

		# ͢�Х�
		logSell( $id, $name, $comName, "$value$HunitFood" );
		$island->{'food'} -= $value;
		$island->{'money'} += int( $value / 10 );
		return 0;
	}
	elsif (( $kind == $HcomOreSell )
		|| ( $kind == $HcomOilSell )
		|| ( $kind == $HcomWeponSell ) )
	{

		# ����̷���
		$arg = 1 if ( $arg == 0 );
		my ($value);
		if ( $id != $target ) {

			# ����ξ��
			return 0 if ( $island->{'pop'} < $Haidpop );
			my ($tn) = $HidToNumber{$target};
			return 0 if ( $tn eq '' );
			my ($tIsland) = $Hislands[$tn];
			my ($tName)   = $tIsland->{'name'};

			# ����̷���
			if ( $kind == $HcomOreSell ) {
				$value = min( $arg, $island->{'ore'} );
				$island->{'ore'} -= $value;
				$tIsland->{'ore'} += $value;
				$value = "$value$HunitOre";
			}
			elsif ( $kind == $HcomOilSell ) {
				$value = min( $arg, $island->{'oil'} );
				$island->{'oil'} -= $value;
				$tIsland->{'oil'} += $value;
				$value = "$value$HunitOil";
			}
			elsif ( $kind == $HcomWeponSell ) {
				$value = min( $arg, $island->{'weapon'} );
				$island->{'weapon'} -= $value;
				$tIsland->{'weapon'} += $value;
				$value = "$value$HunitWeapon";
			}

			# �����
			logAid( $id, $target, $name, "$tName$AfterName", $comName, $value );
			return 0;
		}
		else {
			if ( $kind == $HcomOreSell ) {
				$value = min( $arg, $island->{'ore'} );
				$island->{'ore'} -= $value;
				$island->{'money'} += ( $value * 1 );
				$value = "$value$HunitOre";
			}
			elsif ( $kind == $HcomOilSell ) {
				$value = min( $arg, $island->{'oil'} );
				$island->{'oil'} -= $value;
				$island->{'money'} += ( $value * 2 );
				$value = "$value$HunitOil";
			}
			elsif ( $kind == $HcomWeponSell ) {
				$value = min( $arg, $island->{'weapon'} );
				$island->{'weapon'} -= $value;
				$island->{'money'} += ( $value * 6 );
				$value = "$value$HunitWeapon";
			}
		}

		# ��ѥ�
		logSell( $id, $name, $comName, $value );
		return 0;
	}
	elsif (( $kind == $HcomOreBuy )
		|| ( $kind == $HcomOilBuy )
		|| ( $kind == $HcomWeponBuy ) )
	{

		# �����̷���
		$arg = 1 if ( $arg == 0 );
		if ( $kind == $HcomOreBuy ) {
			if ( $island->{'money'} > $arg * 2 ) {
				$island->{'ore'} += $arg;
				$island->{'money'} -= ( $arg * 2 );
			}
			else {
				logMiss( $id, $name, $comName, "�����­��" );
				return 0;
			}
		}
		elsif ( $kind == $HcomOilBuy ) {
			if ( $island->{'money'} > $arg * 5 ) {
				$island->{'oil'} += $arg;
				$island->{'money'} -= ( $arg * 5 );
			}
			else {
				logMiss( $id, $name, $comName, "�����­��" );
				return 0;
			}
		}
		elsif ( $kind == $HcomWeponBuy ) {
			if ( $island->{'money'} > $arg * 24 ) {
				$island->{'weapon'} += $arg;
				$island->{'money'} -= ( $arg * 24 );
			}
			else {
				logMiss( $id, $name, $comName, "�����­��" );
				return 0;
			}
		}
		logSell( $id, $name, $comName, $arg );
		return 1;
	}
	elsif ( ( $kind == $HcomFood ) || ( $kind == $HcomMoney ) ) {

		# �����
		if ( $island->{'pop'} < $Haidpop ) {

#			HdebugOut("�͸���������������ʤ����ϡ����̿��ϤǤ��ޤ���")
			return 0;
		}

		# �������åȼ���
		my ($tn)      = $HidToNumber{$target};
		my ($tIsland) = $Hislands[$tn];
		my ($tName)   = $tIsland->{'name'};

		# ����̷���
		$arg = 1 if ( $arg == 0 );
		my ( $value, $str );
		if ( $cost < 0 ) {
			$value = min( $arg * ( -$cost ), $island->{'food'} );
			$str = "$value$HunitFood";
		}
		else {
			$value = min( $arg * ($cost), $island->{'money'} );
			$str = "$value$HunitMoney";
		}

		# �����
		logAid( $id, $target, $name, "$tName$AfterName", $comName, $str );

		if ( $cost < 0 ) {
			$island->{'food'} -= $value;
			$tIsland->{'food'} += $value;
		}
		else {
			$island->{'money'} -= $value;
			$tIsland->{'money'} += $value;
		}
		return 0;
	}
	elsif ( $kind == $HcomSearch ) {

		# �ϼ�Ĵ��
		if (   ( $landKind == $HlandPlains )
			|| ( $landKind == $HlandTown )
			|| ( ( $landKind == $HlandWaste ) && ( $lv <= 1 ) ) )
		{

			# ���۷���
			$arg = 1  if ( $arg == 0 );
			$arg = 10 if ( $arg > 10 );
			my ( $value, $str, $p, $q );
			$value = min( $arg * ($cost), $island->{'money'} );
			$str   = "$value$HunitMoney";
			$p     = int( $value / $cost );
			$p     = 10 if ( $p > 10 );
			$island->{'money'} -= $p * $cost;
			$q = random(1000);
			$island->{'prepare2'} += $p;

			if ( $q < 3 * $p ) {    # ���
				$land->[$x][$y]      = $HlandSeisei;
				$landValue->[$x][$y] = 30;
				logChosa( $id, $name, $point, $comName, $str,
					"�����̮��ȯ�������" );
			}
			elsif ( $q < 17 * $p ) {    # Ƽ��
				$land->[$x][$y]      = $HlandSeisei;
				$landValue->[$x][$y] = 10;
				logChosa( $id, $name, $point, $comName, $str,
					"��Ƽ��̮��ȯ�������" );
			}
			elsif ( $q < 50 * $p ) {    # ú��
				$land->[$x][$y]      = $HlandSeisei;
				$landValue->[$x][$y] = 5;
				logChosa( $id, $name, $point, $comName, $str,
					"��ú��̮��ȯ�������" );
			}
			elsif ( $q < 60 * $p ) {    # ����
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 20 + random(51);
				logChosa( $id, $name, $point, $comName, $str,
					"��������ȯ�������" );
			}
			elsif ( $q < 86 * $p ) {    # �ϲ���
				$land->[$x][$y]      = $HlandSea;
				$landValue->[$x][$y] = 1;
				logChosa( $id, $name, $point, $comName, $str,
					"�����̤��ϲ��夬ʮ�Ф��������ˤʤ��" );
			}
			elsif ( $q < 90 * $p ) {    # ����
				$land->[$x][$y]      = $HlandMonster;
				$landValue->[$x][$y] =
				  1200 + $HmonsterBHP[12] + random( $HmonsterDHP[12] );
				logChosa( $id, $name, $point, $comName, $str,
					"�����Ťβ��ä�ȯ�������" );
			}
			else {                      # ����
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
				logChosa( $id, $name, $point, $comName, $str,
					"�ޤ��������⸫�Ĥ��餺���Ϥˤʤ��" );
			}
			return 1;
		}
		else {
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
	}
	elsif ( $kind == $HcomGiveup ) {

		# ����
		$island->{'giveup'} = 1;
		$island->{'dead'}   = 1;
		return 1;
	}
	elsif (( $kind == $HcomSUnit )
		|| ( $kind == $HcomSMissileGM )
		|| ( $kind == $HcomSMissilePP )
		|| ( $kind == $HcomSMissile )
		|| ( $kind == $HcomSMissileMGM )
		|| ( $kind == $HcomSBuild )
		|| ( $kind == $HcomSpaceFarm )
		|| ( $kind == $HcomSFactory )
		|| ( $kind == $HcomSpaceBase )
		|| ( $kind == $HcomSDbase )
		|| ( $kind == $HcomSEisei )
		|| ( $kind == $HcomSPioneer )
		|| ( $kind == $HcomSOccupy )
		|| ( $kind == $HcomSDestroy )
		|| ( $kind == $HcomSFood ) )
	{

		# �����
		my ($prize) = $island->{'prize'};
		$prize =~ /([0-9]*),([0-9]*),(.*)/;
		if ( !( $1 & 512 ) ) {

			# ������­�ˤ�����
			logMiss( $id, $name, $comName, "������­��" );
			return 0;
		}
		elsif ( $Hsolarwind == 1 ) {
			logMiss( $id, $name, $comName,
				"���������㤷���᤭�Ӥ�Ƥ���" );
			return 0;
		}
		my ( $land, $landValue, $dis, $nation ) = (
			$Hspace->{'land'},       $Hspace->{'landValue'},
			$Hspace->{'landValue2'}, $Hspace->{'nation'}
		);
		my $l      = $land->[$x][$y];
		my $tLname = landName( $l, $landValue->[$x][$y] );

		if ( $kind == $HcomSFood ) {

			# ���迩���Ǿ夲�����̣�=�����ȥ�
			$arg = 1 if ( $arg <= 0 );
			$arg *= 100;
			my ($value) = min( $arg, $island->{'food'} );
			$island->{'comsfood'} = $value;

			$island->{'food'} -= $value;
			$Hspace->{'food'} += $value;
			logAid( $id, 999, $name, $SpaceName, $comName, "$value$HunitFood" );
		}
		elsif (( $kind == $HcomSMissileGM )
			|| ( $kind == $HcomSMissilePP )
			|| ( $kind == $HcomSMissile )
			|| ( $kind == $HcomSMissileMGM ) )
		{

			# ����ߥ�����ȯ��
			my ( $bx, $by, $tx, $ty, $err );

			my ( $count, $flag ) = ( 0, 0 );
			if ( $kind == $HcomSMissileMGM ) {
				$arg = 1;
			}
			else {
				$arg = 10000 if ( $arg <= 0 );
			}

			# ��
			if ( $kind == $HcomSMissile ) {
				$err = 19;
			}
			elsif ( $kind == $HcomSMissilePP ) {
				$err = 7;
			}
			else {
				$err = 1;
			}

			# ����⡼�ɤǤϤ�����Ѥ���ʼ������
			my $mcost = 'money';
			if ( ($HwarFlg) && ( $cost < 500 ) ) {
				$mcost = 'weapon';
				$cost  = int( $cost / 10 );
			}
			my ( $msCt, $mslogCtM, $mslogCtW, $mslogCtD ) = ( 0, 0, 0, 0 );

			while ( ( $arg > 0 ) && ( $island->{$mcost} >= $cost ) ) {

				# ���Ϥ򸫤Ĥ���ޤǥ롼��
				while ( $count < $HpointNumber ) {
					$bx = $Hrpx[$count];
					$by = $Hrpy[$count];
					last
					  if ( ( $land->[$bx][$by] == $HlandSpaceBase )
						&& ( $nation->[$bx][$by] == $id ) );
					$count++;
				}
				last
				  if ( $count >= $HpointNumber )
				  ;    # ���Ĥ���ʤ��ä��餽���ޤ�
				       # �����Ĵ��Ϥ����ä��Τǡ�flag��Ω�Ƥ�
				$flag = 1;

				# ���ϤΥ�٥�򻻽�
				my ($level) =
				  expToLevel( $land->[$bx][$by], $landValue->[$bx][$by] );

				# ������ǥ롼��
				while ( ( $level > 0 ) && ( $island->{$mcost} > $cost ) ) {
					last if ( $arg <= 0 );
					$level--;
					$arg--;
					$msCt++;    # ȯ�Ϳ���׻�
					if ( $kind == $HcomSMissileMGM ) {   # ����ͶƳ�Ƥλ�
						my ($Mcount);
						for ( $Mcount = 0 ;
							$Mcount < $HpointNumber ; $Mcount++ )
						{
							$x = $Hrpx[$Mcount];
							$y = $Hrpy[$Mcount];
							if ( $land->[$x][$y] == $HlandMonster ) {
								my ($special) =
								  $HmonsterSpecial[ (
									  monsterSpec( $landValue->[$x][$y] ) )[0]
								  ];
								if (
									(
										   ( $special == 3 )
										&& ( ( $HislandTurn % 2 ) == 1 )
									)
									|| (   ( $special == 4 )
										&& ( ( $HislandTurn % 2 ) == 0 ) )
								  )
								{

					  #								(($special == 4) && (($HislandTurn % 2) == 0)) ||
					  #								($special == 5)){
								}
								else {
									last;
								}
							}
						}
						if ( $Mcount >= $HpointNumber ) {
							logMiss( $id, $name, $comName,
								"Ŭ���ʲ��ä����ʤ��ä�" );
							return 0;
						}
						$HdefenceSpace[$id][$x][$y] = 1;
					}
					elsif ( random(2) == 0 ) {

						# 50%�ǳ���
						$mslogCtW++;
						next;
					}
					$island->{$mcost} -= $cost;

					# ����������
					my ($r) = random($err);
					$tx = $x + $ax[$r];
					$ty = $y + $ay[$r];
					$tx-- if ( !( $ty % 2 ) && ( $y % 2 ) );

					# �������ϰ��⳰�����å�
					if (   ( $tx < 0 )
						|| ( $tx >= $HislandSize )
						|| ( $ty < 0 )
						|| ( $ty >= $HislandSize ) )
					{
						$mslogCtM++;
						next;
					}

					# ���������Ϸ�������
					my ( $tL, $tLv, $tId ) = (
						$land->[$tx][$ty],
						$landValue->[$tx][$ty],
						$nation->[$tx][$ty]
					);
					my ( $tLname, $tPoint ) =
					  ( landName( $tL, $tLv ), "($tx, $ty)" );

					# ��ͭ��̾���ղ�
					if ( $tId > 0 ) {
						my ($tn)      = $HidToNumber{$tId};
						my ($tIsland) = $Hislands[$tn];
						my ($tName)   = $tIsland->{'name'};
						$tLname .= "(${tName}${AfterName})" if ( $tName ne '' );
					}

					# �ɱһ���Ƚ��
					if ( $HdefenceSpace[$id][$tx][$ty] != 1 ) {
						my ( $i, $sx, $sy );
						if ( $tL == $HlandSDefence ) {
							$HdefenceSpace[$id][$tx][$ty] = 1;
						}
						else {
							for ( $i = 1 ; $i < 19 ; $i++ ) {
								$sx = $x + $ax[$i];
								$sy = $y + $ay[$i];
								$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );
								if (   ( $sx < 0 )
									|| ( $sx >= $HislandSize )
									|| ( $sy < 0 )
									|| ( $sy >= $HislandSize ) )
								{
								}
								elsif ( $land->[$sx][$sy] == $HlandSDefence ) {
									if (   ( $tId == $nation->[$sx][$sy] )
										|| ( $tId == 0 )
										|| ( $nation->[$sx][$sy] == 0 ) )
									{
										last;
									}
								}
							}
							if ( $i < 19 ) {

								# �޷�
								$mslogCtD++;
								next;
							}
							else {
								HdebugOut("SA��$id��$tx��$ty");
								$HdefenceSpace[$id][$tx][$ty] = 1;
							}
						}
					}

					if ( $tL == $HlandSunit ) {
						if ( $tLv < 10 ) {

							# �˲�
							logMsSpace( $id, $tPoint, $tLname,
								"����οФˤʤ�", 999 );
							$land->[$tx][$ty]      = $HlandSea;
							$landValue->[$tx][$ty] = 0;
							$dis->[$tx][$ty]       = 0;
						}
						else {
							logMsSpace( $id, $tPoint, $tLname, "�˲�����",
								999 );
							$landValue->[$tx][$ty] = 20;
						}
						$nation->[$tx][$ty] = 0;
					}
					elsif (( $tL == $HlandSCity )
						|| ( $tL == $HlandSFarm )
						|| ( $tL == $HlandSFactory )
						|| ( $tL == $HlandSDefence )
						|| ( $tL == $HlandSAEisei )
						|| ( $tL == $HlandSpaceBase ) )
					{
						my ( $a, $b, $e ) = ( 10, 10, 0 );
						if ( $tL == $HlandSCity ) {
							$a = random(40) + 10;
						}
						elsif ( $tL == $HlandSFarm ) {
							$a = 5;
						}
						elsif ( $tL == $HlandSFactory ) {
							$a = 10;
							$b = 30;
						}
						elsif ( $tL == $HlandSAEisei ) {
							$a = 40;
							$b = 10;
							$e = int( $landValue->[$tx][$ty] / 1000 );
							$landValue->[$tx][$ty] -= $e * 1000;
						}
						$landValue->[$tx][$ty] -= $a;
						if ( $landValue->[$tx][$ty] < $b ) {
							logMsSpace( $id, $tPoint, $tLname, "�˲�����",
								999 );
							$land->[$tx][$ty]      = $HlandSunit;
							$landValue->[$tx][$ty] = 10;
							$dis->[$tx][$ty]       = 0;
							$nation->[$tx][$ty]    = 0;
						}
						else {
							logMsSpace( $id, $tPoint, $tLname,
								"�ﳲ�����", 999 );
							$dis->[$tx][$ty] += 8;
							if ( random(5) == 0 ) {
								$nation->[$tx][$ty] = 0;
							}
							$landValue->[$tx][$ty] += $e * 1000
							  if ( $tL == $HlandSAEisei );
						}

						# �и���
						if ( $land->[$bx][$by] == $HlandSpaceBase ) {
							$dis->[$bx][$by] -= 6;
							$landValue->[$bx][$by] += 2;
							$island->{'allex'}     += 2;
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
						}
					}
					elsif ( $tL == $HlandMonster ) {

						# ����
						my ( $mKind, $mName, $mHp ) = monsterSpec($tLv);
						my ($special) = $HmonsterSpecial[$mKind];
						if ( $mHp <= 1 ) {

							logMsMonKillSpace( $id, $name, $tPoint, $mName,
								999 );

							# ���ä��Ȥ᤿�Ȥ��ηи���
							if ( $land->[$bx][$by] == $HlandSpaceBase ) {
								$dis->[$bx][$by] -= 6;
								$landValue->[$bx][$by] += $HmonsterExp[$mKind];
								$island->{'allex'}     +=
								  $HmonsterExp[$mKind]
								  ;    # �и�����������
								$landValue->[$bx][$by] = $HmaxExpPoint
								  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
							}

							$island->{'displus'} = 200;

							# ���ñ¼����ե饰��Ω�Ƥ�
							$island->{'esa'} = $mKind;

							# ���ä�ä�
							$land->[$tx][$ty]      = $HlandSea;
							$landValue->[$tx][$ty] = 0;
							$nation->[$tx][$ty]    = 0;

							# ���äξ޴ط�
							monstersPrize( $mKind, $island );

							# ����
							my ($value) = $HmonsterValue[$mKind];
							if ( $value > 0 ) {
								$island->{'money'} += $value;
								logMsMonMoney( $id, $mName, $value );
							}
						}
						else {

							# ���������Ƥ�
							logMsMonSpace( $id, $tPoint, $mName, 999 );

							# HP��1����
							$landValue->[$tx][$ty]--;
							next;
						}
					}
					elsif ( $tL == $HlandEarth ) {

						# �ϵ�
						$mslogCtM++;
						$nation->[$tx][$ty] = 0;
					}
					else {
						$mslogCtM++;
						$land->[$tx][$ty]      = $HlandSea;
						$landValue->[$tx][$ty] = 0;
						$nation->[$tx][$ty]    = 0;
					}
				}
				$count++;
			}
			if ( $flag == 0 ) {
				logMsMiss( $id, $name, $comName );
				return 0;
			}
			logMissileSpace(
				$id,       $name,
				$comName,  $point,
				$msCt,     $msCt - $mslogCtM - $mslogCtW - $mslogCtD,
				$mslogCtM, $mslogCtW,
				$mslogCtD, $SpaceName,
				999
			);
			return 1;
		}
		elsif ( $kind == $HcomSOccupy ) {

			# ��������
			if (
				( $nation->[$x][$y] != $id )
				&& (   ( $l == $HlandSunit )
					|| ( $l == $HlandSCity )
					|| ( $l == $HlandSFarm )
					|| ( $l == $HlandSFactory )
					|| ( $l == $HlandSpaceBase )
					|| ( $l == $HlandSAEisei )
					|| ( $l == $HlandSDefence ) )
			  )
			{
			}
			else {

				# �����Բ�
				logMissS( $id, $name, $comName, $point,
					"���ΤǤ��ʤ��Ϸ���" );
				return 0;
			}
			my ($count) = 1;
			if ( $nation->[$x][$y] > 0 ) {
				my ( $i, $sx, $sy );
				for ( $i = 1 ; $i < 7 ; $i++ ) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];
					$sx--
					  if ( !( $sy % 2 ) && ( $y % 2 ) )
					  ;    # �Ԥˤ�����Ĵ��
					if (   ( $sx < 0 )
						|| ( $sx >= $HislandSize )
						|| ( $sy < 0 )
						|| ( $sy >= $HislandSize ) )
					{
					}
					elsif (( $nation->[$sx][$sy] > 0 )
						&& ( $nation->[$sx][$sy] == $nation->[$x][$y] ) )
					{
						if ( $land->[$sx][$sy] == $HlandSCity ) {
							logMissS( $id, $name, $comName, $point,
								"���ξ����������ʤ�" );
							return 0;
						}
						else {
							$count++;
						}
					}
				}
				$count = 5 if ( $count > 5 );
			}
			if ( random($count) == 0 ) {
				$dis->[$x][$y] -= 20;
				logLandSucS( $id, $name, $comName, $point );
				$nation->[$x][$y] = $id;
			}
			else {
				$dis->[$x][$y] += 20;
				logMissS2( $id, $name, $comName, $point, "�����Ϥ�" );
			}
		}
		else {
			if ( ( $nation->[$x][$y] != 0 ) && ( $nation->[$x][$y] != $id ) ) {
				logMissS( $id, $name, $comName, $point, "��ͭ�ʳ���" );
				return 0;
			}
			if ( $kind == $HcomSUnit ) {

				# �����˥åȷ���
				if ( ( $l != $HlandEarth ) && ( $l != $HlandMonster ) ) {
					if ( $l != $HlandSunit ) {
						$land->[$x][$y]      = $HlandSunit;
						$landValue->[$x][$y] = 0;
					}
					elsif ( $landValue->[$x][$y] == 0 ) {
						$landValue->[$x][$y] = 1;
					}
					else {
						$landValue->[$x][$y] = 10;
					}
				}
				else {
					logMissS( $id, $name, $comName, $point,
						"���ߤǤ��ʤ��Ϸ���" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSPioneer ) {

				# ��������
				if ( ( $l == $HlandSunit ) && ( $landValue->[$x][$y] == 10 ) ) {
					$land->[$x][$y]      = $HlandSCity;
					$landValue->[$x][$y] = 1;
				}
				elsif ( $l == $HlandSCity ) {
					$landValue->[$x][$y] += 30;
				}
				else {
					logMissS( $id, $name, $comName, $point,
						"���ߤǤ��ʤ��Ϸ���" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSDestroy ) {

				# �����˥å��˲�
				# �ѹ�����  <5.54e>
				#				if($l != $HlandEarth){
				if ( ( $l != $HlandEarth ) && ( $l != $HlandMonster ) ) {

					# �ѹ���λ  <5.54e>
					$land->[$x][$y]      = $HlandSea;
					$landValue->[$x][$y] = 0;
				}
				else {
					logMissS( $id, $name, $comName, $point,
						"���ߤǤ��ʤ��Ϸ���" );
					return 0;
				}
				$island->{'money'} -= $cost;
				logLandSucS( $id, $name, $comName, $point );
				if ( $nation->[$x][$y] == $id ) {

					# ����ξ��ϥ��������ʤ�
					$nation->[$x][$y] = 0;
					return 0;
				}
				else {
					return 1;
				}
			}
			elsif ( $kind == $HcomSpaceFarm ) {

				# �����������
				if ( $l == $HlandSFarm ) {
					$landValue->[$x][$y] += 5;    # ���� + 5000
					$landValue->[$x][$y] = 50
					  if ( $landValue->[$x][$y] > 50 );    # ���� 50000
				}
				elsif (
					( ( $l == $HlandSunit ) && ( $landValue->[$x][$y] == 10 ) )
					|| ( $l == $HlandSCity ) )
				{
					$land->[$x][$y]      = $HlandSFarm;
					$landValue->[$x][$y] = 10;             # ���� 10000
				}
				else {
					logMissS( $id, $name, $comName, $point,
						"���ߤǤ��ʤ��Ϸ���" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSFactory ) {

				# ���蹩�����
				if ( $l == $HlandSFactory ) {
					$landValue->[$x][$y] += 10;            # ���� + 10000
					$landValue->[$x][$y] = 100
					  if ( $landValue->[$x][$y] > 100 );    # ���� 100000
				}
				elsif (
					( ( $l == $HlandSunit ) && ( $landValue->[$x][$y] == 10 ) )
					|| ( $l == $HlandSCity ) )
				{
					$land->[$x][$y]      = $HlandSFactory;
					$landValue->[$x][$y] = 30;               # ���� 30000
				}
				else {
					logMissS( $id, $name, $comName, $point,
						"���ߤǤ��ʤ��Ϸ���" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSEisei ) {

				# �����������
				$arg = 0 if ( $arg < 0 );
				$arg = 5 if ( $arg > 5 );
				if ( $island->{'sfactory'} > 0 ) {
					if ( $l == $HlandSAEisei ) {

						# �ɲ÷���
						$arg = int( $landValue->[$x][$y] / 1000 );
						$landValue->[$x][$y] += 75;
						$landValue->[$x][$y] = $arg * 1000 + 200
						  if ( $landValue->[$x][$y] % 1000 > 200 );
					}
					elsif (
						(
							   ( $l == $HlandSunit )
							&& ( $landValue->[$x][$y] == 10 )
						)
						|| ( $l == $HlandSCity )
					  )
					{

						# ��������
						$land->[$x][$y]      = $HlandSAEisei;
						$landValue->[$x][$y] = $arg * 1000 + 100;
					}
					else {
						logMissS( $id, $name, $comName, $point,
							"���ߤǤ��ʤ��Ϸ���" );
						return 0;
					}
					$comName .= "(" . $HsEisei[$arg] . ")";
				}
				else {
					logMissS( $id, $name, $comName, $point, "�����­��" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSpaceBase ) {

				# ����ߥ�������Ϸ���
				if ( $island->{'sfactory'} > 0 ) {
					if ( $l == $HlandSpaceBase ) {
						$landValue->[$x][$y] += 4;
						$landValue->[$x][$y] = $HmaxExpPoint
						  if ( $landValue->[$x][$y] > $HmaxExpPoint );
					}
					elsif (
						(
							   ( $l == $HlandSunit )
							&& ( $landValue->[$x][$y] == 10 )
						)
						|| ( $l == $HlandSCity )
					  )
					{

						# ����ߥ��������
						$land->[$x][$y]      = $HlandSpaceBase;
						$landValue->[$x][$y] = 0;
					}
					else {
						logMissS( $id, $name, $comName, $point,
							"���ߤǤ��ʤ��Ϸ���" );
						return 0;
					}
				}
				else {
					logMissS( $id, $name, $comName, $point, "�����­��" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSDbase ) {

				# �����ɱһ���
				if ( ( ( $l == $HlandSunit ) && ( $landValue->[$x][$y] == 10 ) )
					|| ( $l == $HlandSCity ) )
				{
					$land->[$x][$y]      = $HlandSDefence;
					$landValue->[$x][$y] = 0;
				}
				else {
					logMissS( $id, $name, $comName, $point,
						"���ߤǤ��ʤ��Ϸ���" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSBuild ) {

				# ������߷�
				#	if($arg <= 0){
				#	}else{
				#	}
				return 0;
			}
			$dis->[$x][$y] -= 30;
			logLandSucS( $id, $name, $comName, $point );
			$nation->[$x][$y] = $id;

			#			HdebugOut("��ͭ�ѹ�:($x,$y) = ${id}");
		}
		$island->{'money'} -= $cost;

		# ����դ��ʤ顢���ޥ�ɤ��᤹
		if (   ( $kind == $HcomSUnit )
			|| ( $kind == $HcomSpaceFarm )
			|| ( $kind == $HcomSFactory )
			|| ( $kind == $HcomSpaceBase ) )
		{
			if ( $arg > 1 ) {
				$arg--;
				slideBack( $comArray, $cNo, $kind, $target, $x, $y, $arg );
			}
		}
		return 1;

	}
	elsif (( $kind == $HcomOMissilePP )
		|| ( $kind == $HcomOMissileSPP )
		|| ( $kind == $HcomOMissileNM ) )
	{

		# ����ߥ�����ȯ��

		my ( $bx, $by, $tx, $ty, $err );

		my ( $count, $flag ) = ( 0, 0 );

		#	if($kind == $HcomOMissileMGM){
		#		$arg = 1;
		#	}else{
		$arg = 10000 if ( $arg <= 0 );

		#	}

		# ��
		if ( $kind == $HcomOMissileNM ) {
			$err = 19;
		}
		elsif ( $kind == $HcomOMissileSPP ) {
			$err = 8;
		}
		elsif ( $kind == $HcomOMissilePP ) {
			$err = 7;
		}
		else {

			$err = 1;
		}

		# ����⡼�ɤǤϤ�����Ѥ���ʼ������
		my $mcost = 'money';
		if ( ($HwarFlg) && ( $cost < 500 ) ) {
			$mcost = 'weapon';
			$cost  = int( $cost / 10 );
		}
		my ( $msCt, $mslogCtM, $mslogCtW, $mslogCtD ) = ( 0, 0, 0, 0 );
		while ( ( $arg > 0 ) && ( $island->{$mcost} >= $cost ) ) {

			# ���Ϥ򸫤Ĥ���ޤǥ롼��
			while ( $count < $HpointNumber ) {
				$bx = $Hrpx[$count];
				$by = $Hrpy[$count];
				last
				  if (
					(
						   ( $land->[$bx][$by] == $HlandDefence )
						&& ( $landValue->[$bx][$by] == 3 )
					)
					|| ( $land->[$bx][$by] == $HlandBase )
					|| ( $land->[$bx][$by] == $HlandSbase )
					|| ( $land->[$bx][$by] == $HlandDokan )
				  );
				$count++;
			}
			last
			  if ( $count >= $HpointNumber )
			  ;    # ���Ĥ���ʤ��ä��餽���ޤ�

			# �����Ĵ��Ϥ����ä��Τǡ�flag��Ω�Ƥ�
			$flag = 1;

			# ���ϤΥ�٥�򻻽�
			my ($level) =
			  expToLevel( $land->[$bx][$by], $landValue->[$bx][$by] );

			# ������ǥ롼��
			while ( ( $level > 0 ) && ( $island->{$mcost} > $cost ) ) {
				last if ( $arg <= 0 );
				$level--;
				$arg--;
				$msCt++;    # ȯ�Ϳ���׻�
				$island->{$mcost} -= $cost;

				# ����������
				my ($r) = random($err);
				$r  = 0 if ( ( $kind == $HcomOMissileSPP ) && ( $r == 7 ) );
				$tx = $x + $ax[$r];
				$ty = $y + $ay[$r];
				$tx-- if ( !( $ty % 2 ) && ( $y % 2 ) );

				# �������ϰ��⳰�����å�
				if (   ( $tx < 0 )
					|| ( $tx >= $HoceanSize )
					|| ( $ty < 0 )
					|| ( $ty >= $HoceanSize ) )
				{
					$mslogCtM++;
					next;
				}

				# ���������Ϸ�������
				my ( $tLand, $tLandValue, $tLandValue2, $tNation ) = (
					$Hocean->{'land'},       $Hocean->{'landValue'},
					$Hocean->{'landValue2'}, $Hocean->{'nation'}
				);
				my ( $tL, $tLv, $tLv2, $tId ) = (
					$tLand->[$tx][$ty],       $tLandValue->[$tx][$ty],
					$tLandValue2->[$tx][$ty], $tNation->[$tx][$ty]
				);
				my ( $tLname, $tPoint ) =
				  ( landName( $tL, $tLv ), "($tx, $ty)" );
				my ( $tIsland, $tName );

				# ��ͭ��̾���ղ�
				if ( $tId > 0 ) {
					my ($tn) = $HidToNumber{$tId};
					$tIsland = $Hislands[$tn];
					$tName   = $tIsland->{'name'};
					$tLname .= "(${tName}${AfterName})" if ( $tName ne '' );
				}
				if ( $tL == $HlandOPlayer ) {
					if ( ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
						|| ( $tIsland->{'evil'} == 0 ) )
					{

						# ��꤬�Ӿ��
						$mslogCtD++;    # ��������
					}
					elsif ( $tLv2 <= 0 ) {
						logMsOPlayer( $id, $tPoint, $tLname, 888 );
						if ( random(100) == 0 ) {
							$tIsland->{'bigmissile'}++;
						}
						else {
							$tIsland->{'Meteo'} += 5;
						}
					}
					else {
						$tLandValue2->[$tx][$ty]--;
						$mslogCtD++;    # ��������
					}
				}
				elsif ( $tL == $HlandOcean ) {
					$mslogCtD++;        # ��������
				}
				elsif ( $tL == $HlandMonster ) {

					# ����
					my ( $mKind, $mName, $mHp ) = monsterSpec($tLv);
					my ($special) = $HmonsterSpecial[$mKind];

					if ( $mHp <= 1 ) {
						logMsMonKillSpace( $id, $name, $tPoint, $mName, 888 );

						# ���ä��Ȥ᤿�Ȥ��ηи���
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandSbase ) )
						{
							$landValue->[$bx][$by] += $HmonsterExp[$mKind];
							$island->{'allex'}     +=
							  $HmonsterExp[$mKind];   # �и�����������
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
						}
						$island->{'displus'} = 200;

						# ���ñ¼����ե饰��Ω�Ƥ�
						$island->{'esa'} = $mKind;

						# ���ä�ä�
						$tLand->[$tx][$ty]      = $HlandSea;
						$tLandValue->[$tx][$ty] = 0;
						$tNation->[$tx][$ty]    = 0;

						# ���äξ޴ط�
						monstersPrize( $mKind, $island );

						# ����
						my ($value) = $HmonsterValue[$mKind];
						if ( $value > 0 ) {
							$value *= 2;
							$island->{'money'} += $value;
							logMsMonMoney( $id, $mName, $value );
						}
					}
					else {

						# ���������Ƥ�
						logMsMonSpace( $id, $tPoint, $mName, 888 );

						# HP��1����
						$tLandValue->[$tx][$ty]--;
						next;
					}
				}
				else {
					$mslogCtM++;
					$tLand->[$tx][$ty]      = $HlandSea;
					$tLandValue->[$tx][$ty] = 0;
					$tNation->[$tx][$ty]    = 0;
				}
			}
			$count++;
		}
		if ( $flag == 0 ) {
			logMsMiss( $id, $name, $comName );
			return 0;
		}
		logMissileSpace( $id, $name, $comName, $point, $msCt,
			$msCt - $mslogCtM - $mslogCtW - $mslogCtD,
			$mslogCtM, $mslogCtW, $mslogCtD, $OceanName, 888 );
		return 1;
	}
	elsif (( $kind == $HcomMonsEgg )
		|| ( $kind == $HcomMonsEsa )
		|| ( $kind == $HcomMonsEnsei )
		|| ( $kind == $HcomMonsTettai )
		|| ( $kind == $HcomMonsEsaAid )
		|| ( $kind == $HcomMonsAid )
		|| ( $kind == $HcomMonsSell )
		|| ( $kind == $HcomMonsExer ) )
	{

		# ���åХȥ�
		my ($monster) = $island->{'monster'};
		my (
			$MBid,  $MBname, $MBtId, $MBsId, $MBmId,  $MBhp,  $MBmhp,
			$MBstr, $MBdef,  $MBagi, $MBskl, $MBwinh, $MBwin, $MBlose
		  )
		  = (
			$monster->[0],  $monster->[1], $monster->[2],  $monster->[3],
			$monster->[4],  $monster->[5], $monster->[6],  $monster->[7],
			$monster->[8],  $monster->[9], $monster->[10], $monster->[11],
			$monster->[12], $monster->[13]
		  );

		my ($mtn) = $HidToNumber{$MBtId};
		if ( $MBid == 0 ) {

			# ��ʬ�β��ä����ʤ�
		}
		elsif ( $id != $MBid ) {

			# ������
			if ( $mtn eq '' ) {
				$MBid = $id
				  ; # ��꤬���ʤ��ʤä��Τǲ��ä�ʬ������᤹��
				$MBhp  = $MBmhp;
				$MBtId = 0;
			}
		}
		elsif ( $mtn eq '' ) {
			$MBid =
			  $id;   # ��꤬���ʤ��Τǲ��ä�ʬ������᤹��
			$MBhp  = $MBmhp;
			$MBtId = 0;
		}

		if ( $kind == $HcomMonsTettai ) {

			# ����ű��
			# �������åȤ�ư���ꤹ��
			$target = $MBtId;
		}

		my ($tn) = $HidToNumber{$target};
		return 0 if ( $tn eq '' );
		my ($tIsland)  = $Hislands[$tn];
		my ($tName)    = $tIsland->{'name'};
		my ($tMonster) = $tIsland->{'monster'};
		my (
			$tMBid,  $tMBname, $tMBtId, $tMBsId, $tMBmId,  $tMBhp,  $tMBmhp,
			$tMBstr, $tMBdef,  $tMBagi, $tMBskl, $tMBwinh, $tMBwin, $tMBlose
		  )
		  = (
			$tMonster->[0],  $tMonster->[1],  $tMonster->[2],
			$tMonster->[3],  $tMonster->[4],  $tMonster->[5],
			$tMonster->[6],  $tMonster->[7],  $tMonster->[8],
			$tMonster->[9],  $tMonster->[10], $tMonster->[11],
			$tMonster->[12], $tMonster->[13]
		  );

		if ( $kind == $HcomMonsEsaAid ) {

			# ���ñ¾���
			if ( ( $MBsId == 0 ) || ( $tMBsId != 0 ) ) {

				# �¤�̵���ޤ��ϡ����˱¤�����Τ����
				logMonsCancel( $id, $name, $comName,
					"�¤�̵���ޤ��ϡ��������åȤ˱¤�����" );
				return 0;
			}
			$tMBsId = $MBsId;
			logMonsEsaAid( $id, $name, $target, $tName, $HmonsterName[$MBsId] );
			$MBsId = 0;
		}
		else {
			if ( $MBid == 0 ) {

				# ���ä����ʤ�
				if ( $kind == $HcomMonsEgg ) {

					# ���å��å�����
					logMonsEGG( $id, $name, $comName );
					$MBid   = $id;
					$MBname = "���Τ�(̾��̤����)";
					$MBtId  = 0;
					$MBsId  = $MBsId;
					$MBmId  = 1;                              # ���Τ�
					$MBhp   = 18 + random(8);
					$MBmhp  = $MBhp;
					$MBstr  = random(2);
					$MBdef  = random(2);
					$MBagi  = random(2);
					$MBskl  = random(2);
					$MBwinh = 0;
					$MBwin  = 0;
					$MBlose = 0;
					$island->{'money'} -= $cost;
				}
				else {
					logMonsCancel( $id, $name, $comName, "���ä����ʤ�" );
					return 0;
				}
			}
			else {

				# ���ä�����

				if ( $kind != $HcomMonsTettai ) {

					# ����ű��ʳ�
					if ( ( $id != $MBid ) || ( $MBtId != 0 ) ) {

						# ��ʬ�β��ä���ʬ����ˤ��ʤ�
						logMonsCancel( $id, $name, $comName, "��Ʈ���" );
						return 0;
					}
				}

				if ( $kind == $HcomMonsEsa ) {

					# ���ä˱¤򿩤٤�����
					if ( $MBsId == 0 ) {

						# �¤�̵���Τ����
						logMonsCancel( $id, $name, $comName, "�¤�̵��" );
						return 0;
					}
					elsif ( $MBsId == 1 ) {

						# �¤����Τ�
						$MBmId = 1;    # ���Τ�
						logMonsEvo( $id, $name, $MBname, $HmonsterName[$MBmId],
							$comName );
					}
					else {

						my ($MonGRP)    = $HmonsterGRP[$MBmId];
						my ($MonCLS)    = $HmonsterCLS[$MBmId];
						my ($EsaMonGRP) = $HmonsterGRP[$MBsId];
						my ($EsaMonCLS) = $HmonsterCLS[$MBsId];

						if ( $MonGRP == $EsaMonGRP ) {

							# �¤�Ʊ�����롼�פξ��
							if ( $MonCLS > $EsaMonCLS ) {

						   # �¤�곬�餬�㤤�ΤǱ¤β��ä˿ʲ�
								$MBmId = $MBsId;
								logMonsEvo( $id, $name, $MBname,
									$HmonsterName[$MBmId], $comName );
							}
							else {

								# ���餬���夬��
								my ($MonSea) = MonSeaCls( $MBmId, 1 );
								if ( $MonSea == 0 ) {

									# ����
									logMonsEvoF( $id, $name, $MBname,
										$comName );
								}
								else {
									$MBmId = $MonSea;
									logMonsEvo( $id, $name, $MBname,
										$HmonsterName[$MonSea], $comName );
								}
							}
						}
						else {
							if ( $MonCLS < $EsaMonCLS ) {

								# �¤Τۤ��γ��餬���ʾ�⤤���
								my ($MonSea) = MonSeaCls( $MBsId, 3 );
								if ( $MonSea == 0 ) {

									# ����
									logMonsEvoF( $id, $name, $MBname,
										$comName );
								}
								else {
									$MBmId = $MonSea;
									logMonsEvo( $id, $name, $MBname,
										$HmonsterName[$MonSea], $comName );
								}
							}
							else {
								my ($MonSea);
								if ( $HmonsterCLS[$MBmId] == 1 ) {
									$MonSea = MonSeaCls( $MBsId, 3 );
								}
								else {
									$MonSea = MonSeaCls( $MBmId, 2 );
								}
								if ( $MonSea == 0 ) {

									# ����
									logMonsEvoF( $id, $name, $MBname,
										$comName );
								}
								else {
									$MBmId = $MonSea;
									logMonsEvo( $id, $name, $MBname,
										$HmonsterName[$MonSea], $comName );
								}
							}
						}
					}
					$MBsId = 0;
					$island->{'money'} -= $cost;
				}
				elsif ( $kind == $HcomMonsEnsei ) {

					# ���ñ���
					if ( $tMBid != $target ) {

			# ���˲��ä����ʤ���������ΤȤ�̵�������
						logMonsCancel( $id, $name, $comName,
"�������åȤ˲��ä����ʤ����������"
						);
						return 0;
					}
					if ( $tMBtId != 0 ) {

						# ��꤬��Ʈ��ΤȤ�̵�������
						logMonsCancel( $id, $name, $comName,
							"�������åȤ���Ʈ���" );
						return 0;
					}
					if ( $tMBid == $id ) {

						# ��ʬ����
						logMonsCancel( $id, $name, $comName,
							"��ʬ������ä�" );
						return 0;
					}
					logMonsENSEI( $id, $name, $target, $tName, $comName );
					$MBid   = $target;
					$MBtId  = $target;
					$tMBtId = $id;
					$island->{'money'} -= $cost;
				}
				elsif ( $kind == $HcomMonsTettai ) {

					# ����ű��
					if ( $MBid == $id ) {

						# ��ʬ����
						if ( $MBtId == 0 ) {

							# ��꤬���ʤ��Ȥ��Ȥ�̵�������
							logMonsCancel( $id, $name, $comName,
								"��Ʈ��Ǥʤ�" );
							return 0;
						}
						$tMBid = $tMBtId;
					}
					else {

						# ������
						$MBid  = $MBtId;
						$tMBid = $tMBtId;
					}
					logMonsEND( $id, $name, $MBname, $tMBid,
						"�襤����ƨ���ޤ�����" );
					logMonsEND( $tMBid, $tName, $tMBname, $id,
						"�襤�˾������ޤ�����" );
					$MBtId  = 0;
					$tMBtId = 0;
					$MBhp   = $MBmhp;
					$tMBhp  = $tMBmhp;
					$tMBwinh++;    # ��������
					$tMBwin++;
					$MBlose++;
				}
				elsif ( $kind == $HcomMonsAid ) {

					# ���þ���
					if ( ( $tMBid != 0 ) || ( $tMBtId != 0 ) ) {

						# ���˴��˲��ä�����Ȥ�̵�������
						logMonsCancel( $id, $name, $comName,
							"�������åȤ˴��˲��ä�����" );
						return 0;
					}
					logMonsAid( $id, $name, $target, $tName );
					$tMBid   = $target;
					$tMBname = $MBname;
					$tMBtId  = 0;

					#		$tMBsId = 0;
					$tMBmId  = $MBmId;
					$tMBhp   = $MBhp;
					$tMBmhp  = $MBmhp;
					$tMBstr  = $MBstr;
					$tMBdef  = $MBdef;
					$tMBagi  = $MBagi;
					$tMBskl  = $MBskl;
					$tMBwinh = $MBwinh;
					$tMBwin  = $MBwin;
					$tMBlose = $MBlose;

					$MBid   = 0;
					$MBname = "";
					$MBtId  = 0;

					#		$MBsId = 0;
					$MBmId  = 0;
					$MBhp   = 0;
					$MBmhp  = 0;
					$MBstr  = 0;
					$MBdef  = 0;
					$MBagi  = 0;
					$MBskl  = 0;
					$MBwinh = 0;
					$MBwin  = 0;
					$MBlose = 0;
				}
				elsif ( $kind == $HcomMonsSell ) {

					# �������
					logMonsSell( $id, $name, $comName );
					$island->{'money'} += ( $MBwin + 1 ) * 1000;
					$MBid   = 0;
					$MBname = "";
					$MBtId  = 0;

					#		$MBsId = 0;
					$MBmId  = 0;
					$MBhp   = 0;
					$MBmhp  = 0;
					$MBstr  = 0;
					$MBdef  = 0;
					$MBagi  = 0;
					$MBskl  = 0;
					$MBwinh = 0;
					$MBwin  = 0;
					$MBlose = 0;
				}
				elsif ( $kind == $HcomMonsExer ) {

					# �����ϵ�����
					if ( $MBsId == 0 ) {

						# �¤�̵���Τ����
						logMonsCancel( $id, $name, $comName, "�¤�̵��" );
						return 0;
					}
					logMonsExer( $id, $name, $comName );
					$island->{'money'} -= $cost;
					my ($er) = random(10);
					if ( $er < 3 ) {
						$MBstr++;
					}
					elsif ( $er < 4 ) {
						$MBdef++;
					}
					elsif ( $er < 7 ) {
						$MBagi++;
					}
					else {
						$MBskl++;
					}
					$MBsId = 0;
				}
			}
		}

		my (@wmonster) = (
			$MBid,  $MBname, $MBtId, $MBsId, $MBmId,  $MBhp,  $MBmhp,
			$MBstr, $MBdef,  $MBagi, $MBskl, $MBwinh, $MBwin, $MBlose
		);
		$island->{'monster'} = \@wmonster;

		if ( $id != $target ) {
			my (@wtMonster) = (
				$tMBid,  $tMBname, $tMBtId, $tMBsId, $tMBmId,
				$tMBhp,  $tMBmhp,  $tMBstr, $tMBdef, $tMBagi,
				$tMBskl, $tMBwinh, $tMBwin, $tMBlose
			);
			$tIsland->{'monster'} = \@wtMonster;
		}

		if (   ( $kind == $HcomMonsEgg )
			|| ( $kind == $HcomMonsEsa )
			|| ( $kind == $HcomMonsExer ) )
		{
			return 1;
		}
		return 0;
	}
	return 1;
}    # doCommand()

# ���åХȥ���
# ��ĳ��餬��β��ä����
sub MonSeaCls {
	my ( $monid, $pattern ) = @_;
	my ( $MonsGRP, $MonsCLS );
	$MonsGRP = $HmonsterGRP[$monid];
	if ( $pattern == 1 ) {

		# $monid��Ʊ�����롼�פγ��餬���⤤���ä�õ��
		$MonsCLS = $HmonsterCLS[$monid] + 1;
	}
	elsif ( $pattern == 2 ) {

		# $monid��Ʊ�����롼�פγ��餬���㤤���ä�õ��
		$MonsCLS = $HmonsterCLS[$monid] - 1;
		if ( $MonsCLS < 1 ) {
			$MonsCLS = 1;
		}
	}
	else {

		# $monid��Ʊ�����롼�פγ��餬���β��ä�õ��
		$MonsCLS = 1;
	}
	my ( $i, $sx, $sy );
	for ( $i = 1 ; $i < $HmonsterNumber ; $i++ ) {
		if ( $MonsGRP == $HmonsterGRP[$i] ) {
			if ( $MonsCLS == $HmonsterCLS[$i] ) {
				return $i;
			}
		}
	}
	return 0;
}

# ���äξ޴ط��η׻�
sub monstersPrize {
	my ( $mKind, $island ) = @_;
	my ($prize) = $island->{'prize'};
	$prize =~ /([0-9]*),([0-9]*),(.*)/;
	my ( $flags, $monsters, $turns ) = ( $1, $2, $3 );
	my ( $i, $f );
	my $monsters2 = $monsters;
	for ( $i = $HmonsterNumber - 1 ; $i >= 0 ; $i-- ) {
		$f = 2**$i;
		if ( $monsters2 >= $f ) {
			$monsters2 -= $f;
		}
		elsif ( $i == $mKind ) {
			$monsters += $f;
			last;
		}
	}
	$island->{'prize'} = "$flags,$monsters,$turns";
}

#CL ������̿��
sub doCommandLate {
	my ( $i, $id, $kind, $target, $x, $y, $arg, $x2, $y2 );
	for ( $i = $#HcomL ; $i >= 0 ; $i-- ) {
		if ( $HcomL[$i]->{turn} == $HislandTurn ) {

			# �¹Ԥ��롦����
			$id     = $HcomL[$i]->{id};
			$kind   = $HcomL[$i]->{kind};
			$target = $HcomL[$i]->{target};
			$x      = $HcomL[$i]->{x};
			$y      = $HcomL[$i]->{y};
			$arg    = $HcomL[$i]->{arg};
			my ($tn) = $HidToNumber{$id};
			next if ( $tn eq '' );
			$tn = $HidToNumber{$target};
			next if ( $tn eq '' );
			my ($tIsland) = $Hislands[$tn];
			my ($tName)   = $tIsland->{'name'};
			my ($island)  = $Hislands[ $HidToNumber{$id} ];
			my ($name)    = $island->{'name'};

			if ( $kind == $HcomSendMonster ) {
				if ( $arg == 1 ) {
					$tIsland->{'monstersend1'}++;
				}
				elsif ( $arg == 2 ) {
					$tIsland->{'monstersend2'}++;
				}
				elsif ( $arg == 3 ) {
					$tIsland->{'monstersend3'}++;
				}
				else {
					$tIsland->{'monstersend'}++;
				}
				logEvent( $id, $name,
"���������������ä�${HtagName_}${tName}${AfterName}${H_tagName}�����夷�����͡���"
				);
			}
			elsif ( $kind == $HcomSSendMonster ) {
				$arg = $HmonsterNumber - 1 if ( $arg >= $HmonsterNumber );
				$tIsland->{'monsEnsei'} = $arg;
				logEvent( $id, $name,
"���������������ä�${HtagName_}${tName}${AfterName}${H_tagName}�����夷�����͡���"
				);
			}
			elsif ( $kind == $HcomSpy ) {
				if ( $arg == 0 ) {

					# ������ɸ����Ͽ�
					$HpunishInfo{$target}->{punish} = 1;
					$HpunishInfo{$target}->{x}      = $x;
					$HpunishInfo{$target}->{y}      = $y;
				}
				else {
					logEventP( $target, $tName, "($x, $y)",
"�����̤Υ��������äƤ������͡������إ����ǥߥ������ɱ��Բġ�"
					);
					my ( $j, $sx, $sy );
					for ( $j = 0 ; $j < 19 ; $j++ ) {
						$sx = $x + $ax[$j];
						$sy = $y + $ay[$j];
						$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );
						next
						  if ( ( $sx < 0 )
							|| ( $sx >= $HislandSize )
							|| ( $sy < 0 )
							|| ( $sy >= $HislandSize ) );    # �ϰϳ�Ƚ��

						$HdefenceHex[$target][$sx][$sy] = -1;
					}
				}
			}
			elsif ( $kind == $Hcomcolony ) {

				# ����ˡ��
				if ( $arg == 2 ) {
					logEvent( $id, $name,
"����<B>�����ѡ�������ɥ����ƥࣲ</B>��ȯư����"
					);
					$island->{'SSSystem'} = 1;
					$HdefenceHex[$id]     = 1;
					$island->{'Crime'}    = 1;
					$island->{'money'} -= $cost;
				}
				else {
					$tIsland->{'colony'}++;
					$tIsland->{'tunami'} = 2;
					logEvent( $id, $name,
"�����߲�������<B>���ڡ�������ˡ�</B>�����${HtagName_}${tName}${AfterName}${H_tagName}������ޤ�����"
					);
				}
			}
		}
	}
}

# ��Ĺ�����ñ�إå����ҳ�
sub doEachHex {
	my ($island) = @_;
	my ( $name, $id, $land, $landValue, $land2, $landValue2 ) = (
		$island->{'name'},      $island->{'id'},    $island->{'land'},
		$island->{'landValue'}, $island->{'land2'}, $island->{'landValue2'}
	);

	# ŷ���ѹ�
	$island->{'weather2'} = $island->{'weather'};
	my ( $wkind, $wname, $whp, $wkind2, $wkind3 ) =
	  weatherinfo( $island->{'weather'} );

	# �����ᤦ��
	if (   ( random(4) == 0 )
		&& ( ( $wkind == 3 ) || ( $wkind == 4 ) )
		&& ( $whp < 8 )
		&& ( $id <= 90 ) )
	{
		$island->{'Rain'} = 1;
		logEvent( $id, $name,
			"��<B>���Τ�������</B>���ڡ����ᤤ�ޤ�����" );
	}

	# ŷ�����ǡ���Ĵ��
	my ($pastweather) = $island->{'pastweather'};
	my (@pastw);
	my ( $w, $pw );
	push( @pastw, $wkind );
	for ( $w = 0 ; $w < 10 ; $w++ ) {
		$pw = $pastweather->[$w];
		push( @pastw, $pw );
	}
	$island->{'pastweather'} = \@pastw;

#	logWeather("${HtagName_}${name}${AfterName}${H_tagName}��ŷ����<B>$wname</B>�Ǥ���");
	$wkind  = ( random(10) < 9 )  ? $wkind2 : random(6);
	$wkind2 = ( random(10) < 7 )  ? $wkind3 : random(6);
	$wkind3 = ( random(12) == 0 ) ? 1       : random(6);

	if ( $id > 90 ) {

		# Battle Field�ΤȤ�
		$island->{'weather'} =
		  $wkind3 * 1000 + $wkind2 * 100 + $wkind * 10 + random(10);
		my ( $x, $y, $i );
		for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
			$x = $Hrpx[$i];
			$y = $Hrpy[$i];
			my ( $landKind, $lv ) = ( $land->[$x][$y], $landValue->[$x][$y] );
			if ( $landKind == $HlandTown ) {
				if (
					( random(500) == 0 )
					|| ( $island->{'monstersend'} + $island->{'monstersend1'} +
						$island->{'monstersend2'} + $island->{'monstersend3'} )
				  )
				{
					my $kind = $HmonsterL3[ random($HmonsterL3Num) ];

					# ��¤
					if ( $island->{'monstersend'} > 0 ) {
						$kind = 0;
						$island->{'monstersend'}--;
					}
					elsif ( $island->{'monstersend1'} > 0 ) {
						$kind = 11;
						$island->{'monstersend1'}--;
					}
					elsif ( $island->{'monstersend2'} > 0 ) {
						$kind = 22;
						$island->{'monstersend2'}--;
					}
					elsif ( $island->{'monstersend3'} > 0 ) {
						$kind = 25;
						$island->{'monstersend3'}--;
					}
					my $lv2 = $kind * 100 + $HmonsterBHP[$kind] +
					  random( $HmonsterDHP[$kind] );
					logMonsCome( $id, $name, ( monsterSpec($lv2) )[1],
						"($x, $y)", landName( $landKind, $lv ) );
					$land->[$x][$y]      = $HlandMonster;
					$landValue->[$x][$y] = $lv2;
				}
				else {
					$landValue->[$x][$y] += random(20);
					$landValue->[$x][$y] = 200
					  if ( $landValue->[$x][$y] > 200 );
				}
			}
			elsif ( $landKind == $HlandSlum ) {
				$land->[$x][$y] = $HlandTown if ( random(2) == 0 );
			}
			elsif ( $landKind == $HlandPlains ) {
				if ( random(5) == 0 ) {
					$land->[$x][$y]      = $HlandTown;
					$landValue->[$x][$y] = 1;
				}
			}
			elsif ( $landKind == $HlandWaste ) {
				if ( random(2) == 0 ) {
					$land->[$x][$y]      = $HlandPlains;
					$landValue->[$x][$y] = 0;
				}
			}
			elsif ( ( $landKind == $HlandSea ) && ( $kinoraFlg == 1 ) ) {
				next if ( chkAround( $land, $x, $y, $HlandKInora, 7 ) );

				# ���ۤ��Τ�
				$kinoraFlg = 0;
				$land->[$x][$y] = $HlandKInora;
				$landValue->[$x][$y] = 50000 + ( random(60) * 100 ) + 4000;
				logMonsCome( $id, $name, landName( $HlandKInora, 0 ),
					"($x, $y)", landName( $landKind, $lv ) );
				kinoraMake( $land, $landValue, $x, $y );
			}
			elsif ( $landKind == $HlandKInora ) {

				# ���ۤ��Τ�
				kinoraMove( $island, $x, $y );
			}
		}
		return;
	}

	# Ƴ����
	my ( @monsterMove, @shipMove );

	# ���ȼԤ���̱�ο��ǥ���೹��ȯ����Ψ����롣
	my ($unemployment) = $island->{'pop'} - (
		(
			$island->{'farm'} + $island->{'factory'} + $island->{'port'} +
			  $island->{'mountain'} + $island->{'tower'}
		) * 13
	) + $island->{'achive'} * 30;
	$unemployment = 0 if ( $unemployment < 0 );
	my ($p)       = ( $island->{'food'} < 0 ) ? 20000 : 100000;
	my ($oilFlag) = $island->{'oilfield'};

	# ���γ��ˤ���ݿ��Ϥ�Ĵ��
	my ( $wp, $fp ) = ( 2, $island->{'forest'} );
	$fp += 5 if ( $island->{'eis0'} );
	if ( $fp >= 10 ) {
		$wp = 1 if ( random(2) == 0 );
	}
	elsif ( $fp == 4 ) {
		$wp = 3;
	}
	elsif ( $fp < 2 ) {
		$wp = 5;
	}
	elsif ( $fp < 4 ) {
		$wp = 4;
	}
	$whp += $island->{'tenki'};    #�Ƥ�Ƥ뤤�Τ�ˤ������

	if ( $wkind == 5 ) {           # �籫
		$whp++ if ( $whp < 4 );
		$whp += $wp;
	}
	elsif ( $wkind == 4 ) {        # ��
		$whp++ if ( $whp < 4 );
		$whp += int( $wp / 2 );
	}
	elsif ( $wkind == 0 ) {        # ����
		$whp-- if ( $whp > 5 );
		$whp -= $wp;
	}
	elsif ( $wkind == 1 ) {        # ����
		$whp-- if ( $whp > 6 );
		$whp -= int( $wp / 2 );
	}
	else {
		if ( $whp > 6 ) {
			$whp--;
		}
		elsif ( $whp < 3 ) {
			$whp++;
		}
	}

	# ����������ʾ�������̤˼��٤���������
	if ( $fp >= 20 ) {
		if ( $whp > 6 ) {
			$whp--;
		}
		elsif ( $whp < 3 ) {
			$whp++;
		}
	}

	if ( $whp > 9 ) {
		$island->{'Kouzui'} = 1;
		$island->{'food'} -= int( $island->{'food'} * 0.1 );
		$whp = 8;
		logEvent2( $id, $name, '���夬ȯ������',
			'��ο͸�������ޤ���' );
		$island->{'TeruteruMons'} = 1
		  if ( ( $island->{'pop'} >= $HdisMonsBorder1 )
			&& ( random(12) == 0 ) );    # �Ƥ�Ƥ뤤�Τ�
	}
	elsif ( $whp < 0 ) {
		$island->{'Hideri'} = 1;
		$whp = 1;
		logEvent2( $id, $name, '���Ȥ꤬ȯ������',
			'�������ﳲ���Фޤ���' );
		$island->{'TeruteruMons'} = 2
		  if ( ( $island->{'pop'} >= $HdisMonsBorder1 )
			&& ( random(12) == 0 ) );    # �դ��Ƥ�Ƥ�
	}
	$island->{'weather'} = $wkind3 * 1000 + $wkind2 * 100 + $wkind * 10 + $whp;

	my ($Pol) = $HdisPollution * $island->{'pop'} * 0.001;
	$Pol = $HmaxdisPollution if ( $Pol > $HmaxdisPollution );

	if (   ( random(1000) < $Pol )
		&& ( $island->{'pop'} >= 3000 )
		&& ( $island->{'propaganda'} != 1 ) )
	{

	  # ����ȯ�� �͸�30��̤����Ͷ�׳�ư��λ���ȯ�����ʤ�
		$island->{'Pollution'} = 1;
		logEvent2( $id, $name, '����', '��ȯ�����Ƥ��ޤ�' );
	}
	if (
		(
			random($p) < (
				$HdisCrime *
				  ( $island->{'pop'} + $island->{'slum'} * 4 + $unemployment ) *
				  0.1
			)
		)
		&& ( $island->{'Police'} == 0 )
	  )
	{

		# �Ⱥ�¿ȯ
		$island->{'Crime'} = 1;
		logEvent2( $id, $name, '�Ⱥ᤬¿ȯ', '���Ƥ��ޤ�' );
	}
	if ( random(100) < 5 + $island->{'event'} ) {
		$island->{'event'} = 1;
		my ($eve) = random(100);
		if ( $eve < 10 ) {
			$island->{'wingdragon'} = 1;
			$eve = "����ε���и������Ѹ��Ҥ����ޤ�";
		}
		elsif ( $eve < 30 ) {
			$island->{'icefloe'} = 1;
			$eve = "��ήɹ���и������Ѹ��Ҥ����ޤ�";
		}
		elsif ( $eve < 50 ) {
			$island->{'couplerock'} = 1;
			$eve = "�����ش䤬�и������Ѹ��Ҥ����ޤ�";
		}
		elsif ( $eve < 52 ) {
			$eve = "����Φ�����̱ɺ�塪���͸�������";
		}
		elsif ( $eve < 63 ) {
			$island->{'present'}->[0]++;
			$eve =
			  "�ǡ����Τ����बͶ�פ��졢�Ѹ��Ҥ����ޤ�";
		}
		elsif ( $eve < 69 ) {
			$island->{'present'}->[1]++;
			$eve =
"�ǡ���Φ�Υ��ͥ��󤫤饹����������߻�����դ��졢�Ѹ��Ҥ����ޤ�";
		}
		elsif ( $eve < 72 ) {
			$island->{'present'}->[2]++;
			$eve =
"�ǡ��ɡ������ͽ���Ƥ��Ĳ�ǲķ褵�졢�Ѹ��Ҥ����ޤ�";
		}
		elsif ( $eve < 76 ) {
			$island->{'present'}->[3]++;
			$eve =
"�ǡ���Φ�λ񻺲Ȥ������η��ߤ���ꡢ�Ѹ��Ҥ����ޤ�";
		}
		elsif ( $eve < 80 ) {
			$island->{'present'}->[4]++;
			$eve =
"�ǡ���κ�ȶ��ͷ���Ϸ��ߤ���ꡢ�Ѹ��Ҥ����ޤ�";
		}
		elsif ( $eve < 89 ) {
			$island->{'present'}->[5]++;
			$eve =
"�ǡ���̱���ع��η��ߤ���˾�����ߤ����ꡢ��Φ���餿������ΰ�̱�Ԥ���äƤ�";
		}
		elsif ( $eve < 94 ) {
			$island->{'present'}->[6]++;
			$eve =
"�ǡ��������ߤ�ͽ�����Ȥޤ���ߤ��뤳�Ȥ����ꡢ��Φ���餿������ΰ�̱�Ԥ���äƤ�";
		}
		elsif ( $eve < 96 ) {
			$island->{'present'}->[7]++;
			$eve =
"�ǡ����ԻԤ���ߤ���Ȥ���������������Φ���餿������ΰ�̱�Ԥ���äƤ�";
		}
		else {
			$island->{'present'}->[8]++;
			$eve =
"�ǡ�ưʪ�����μ¶ȲȤ�ưʪ��򳫱����ꡢ�Ѹ��Ҥ����ޤ�";
		}
		logOut( "${HtagName_}${name}${AfterName}${H_tagName}${eve}�ޤ�����",
			$id );
	}
	else {
		$island->{'event'} = 0;
	}

	# ������͸��Υ����� ¼Į���Իԡ����Ի�
	my ( $pop1, $pop2, $pop3 ) = ( 10, 0, 0 );
	if ( $island->{'food'} < 0 ) {
		$pop1 = -30;    # ������­
		$pop2 = -10;
		$pop3 = -10;
	}
	elsif ( $island->{'propaganda'} == 1 ) {
		$pop1 = 30;     # Ͷ�׳�ư��
		$pop2 = 4;
		$pop3 = 4;
	}
	if ( $island->{'Kouzui'} == 1 ) {    # ����
		$pop1 -= random(30) + 5;
		$pop2 -= random(15) + 4;
		$pop3 -= random(10) + 4;
	}
	if ( $island->{'Hideri'} == 1 ) {    # ���Ȥ�
		$pop1 -= random(20) + 5;
		$pop2 -= 5;
		$pop3 -= 5;
	}
	if ( $island->{'Crime'} == 1 ) {     # �Ⱥ�¿ȯ��
		$pop1 -= random(10) + 5;
		$pop2 -= 4;
		$pop3 -= 5;
	}
	if ( $island->{'towerD'} > 0 ) {     # ���Ȳ���
		$pop1 -= 3;
		$pop2--;
		$pop3 -= 2;

	}
	if ( $island->{'event'} == 1 ) {     # �͸������٥��
		$pop1 += 30;
		$pop2 += 5;
		$pop3 += 5;
	}
	if ( $island->{'event2'} == 1 ) {    # �͸������٥��2
		$pop1 += 50;
		$pop2 += 15;
		$pop3 += 10;
	}
	if ( $island->{'treasure'} > 0 ) {    # ����
		$pop1 += 5;
		$pop2 += 2;
		$pop3++;
		$island->{'displus'} = 70;
	}
	if ( $island->{'gold'} > 0 ) {        # �����
		$pop1 += 20;
		$pop2 += 6;
		$pop3 += 4;
		$island->{'displus'} = 150;
	}

	# �롼��
	my ( $x, $y, $i, $osen );
	for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
		$x = $Hrpx[$i];
		$y = $Hrpy[$i];
		my ( $landKind, $lv ) = ( $land->[$x][$y], $landValue->[$x][$y] );

		if (   ( $landKind == $HlandTown )
			|| ( $landKind == $HlandSlum )
			|| ( $landKind == $HlandMegacity )
			|| ( $landKind == $HlandMegaFarm )
			|| ( $landKind == $HlandMegaFact )
			|| ( $landKind == $HlandMegatower )
			|| ( ( $landKind == $HlandOil ) && ( $lv >= 35 ) ) )
		{

			# Į��,�����Ի�,����೹,�����Ϸ�
			if (   ( ( $landKind == $HlandTown ) && ( $lv < 130 ) )
				&& ( random($p) < $unemployment + $island->{'towerD'} ) )
			{

				# ����೹���Ѳ������Ψ������
				logslum( $id, $name, landName( $landKind, $lv ), "($x, $y)" );
				$land->[$x][$y] = $HlandSlum;
				next;
			}
			elsif (( $landKind == $HlandSlum )
				&& ( $unemployment == 0 )
				&& ( random(3) == 0 ) )
			{

# ��̱���̣���ƿ���;�äƤ������33.3%�γ�Ψ�ǥ���೹��Į�ˤʤ롣
				$land->[$x][$y] = $HlandTown;
				next;
			}
			elsif (( $island->{'Pollution'} == 1 )
				&& ( $landKind == $HlandTown )
				&& ( $island->{'Hospital'} != 1 ) )
			{

				# �±���̵����硢����ȯ���� 31%��Ϣ��
				$island->{'Pollution'} = 0 if ( random(100) > 30 );
				logOsen( $id, $name, landName( $landKind, $lv ), "($x, $y)" );
				$land->[$x][$y] = $HlandOsen;
				if ( chkAround( $land, $x, $y, $HlandForest, 7 ) ) {
					$landValue->[$x][$y] = 1;
				}
				else {
					$landValue->[$x][$y] = random(3) + 1;
				}
				next;
			}

			# ���Ϥ��Ϸ��ǿ͸�����������Ĵ�᤹��
			my ( $addpop, $addpop2, $addpop3 ) = ( $pop1, $pop2, $pop3 );
			my $count = 0;
			my ( $j, $sx, $sy );
			for ( $j = 0 ; $j < 7 ; $j++ ) {
				$sx = $x + $ax[$j];
				$sy = $y + $ay[$j];
				$sx--
				  if ( !( $sy % 2 ) && ( $y % 2 ) );  # �Ԥˤ�����Ĵ��
				if (   ( $sx < 0 )
					|| ( $sx >= $HislandSize )
					|| ( $sy < 0 )
					|| ( $sy >= $HislandSize ) )
				{
				}
				elsif (
					   ( $land->[$sx][$sy] == $HlandMonument )
					|| ( $land->[$sx][$sy] == $HlandSMonument )
					|| ( $land->[$sx][$sy] == $HlandForest )
					|| (   ( $land->[$sx][$sy] == $HlandWaste )
						&& ( $landValue->[$sx][$sy] >= 10 ) )
				  )
				{

					# ��ǰ�ꡢ���쵭ǰ�ꡢ��������
					$addpop += 2;
					$addpop2++;
				}
				elsif ( $land->[$sx][$sy] == $HlandSchool ) {

					# �ع�
					$addpop  += 2;
					$addpop2 += 2;
					$count = -1;
				}
				elsif ( $land->[$sx][$sy] == $HlandSlum ) {
					$count = 1 if ( $count == 0 );
				}
				elsif ( $land->[$sx][$sy] == $HlandOsen ) {
					$addpop -= 15;
				}
			}
			if ($count) {

				# ���Ϥ˳ع���̵������೹�������
				$addpop  -= 3;
				$addpop2 -= 3;
				$addpop3 -= 3;
			}

			if ( $landKind == $HlandOil ) {
				if ( $lv >= 35 ) {

					# �����Ի�
					$island->{'money'}--;
					$island->{'food'} -= int( $lv * $HeatenFood );
					if ( $island->{'money'} < 0 ) {
						$addpop -= 20;
						$island->{'money'} = 0;
					}
					if ( $island->{'food'} < 0 ) {
						$addpop -= 20;
						$island->{'food'} = 0;
					}
				}
				elsif ( $lv >= 10 ) {

					#  ��������
					$island->{'money'} -= int( $lv / 5 );
					if ( $island->{'money'} < 0 ) {
						$land->[$x][$y]      = $HlandSea;
						$landValue->[$x][$y] = 0;
					}
				}
			}

			if (   ( $landKind == $HlandMegacity )
				|| ( $landKind == $HlandMegaFarm )
				|| ( $landKind == $HlandMegaFact )
				|| ( $landKind == $HlandMegatower ) )
			{

				# �����Ϸ��ξ��
				my ( $r1, $r2, $r3 ) = ( 3, -3, 0 );
				( $r1, $r2, $r3 ) = ( 0, -4, 1 )
				  if ( $island->{'Hospital'} == 1 );
				( $r1, $r2, $r3 ) = ( -1, -7, 2 )
				  if ( $landKind != $HlandMegacity );

				if (
					( random(5) > $r3 )
					&& (   ( $addpop < $r1 )
						|| ( $addpop2 < $r2 )
						|| ( $addpop3 < $r2 ) )
				  )
				{

					# �������
					my ($lName) = landName( $landKind, $lv );
					my ($lName2);
					if ( $landKind == $HlandMegaFact ) {
						$landKind            = $HlandFactory;
						$land->[$x][$y]      = $landKind;
						$lName2              = landName( $landKind, 90 );
						$landValue->[$x][$y] = 90;
					}
					elsif ( $landKind == $HlandMegaFarm ) {
						$landKind            = $HlandFarm;
						$land->[$x][$y]      = $landKind;
						$lName2              = landName( $landKind, 50 );
						$landValue->[$x][$y] = 50;
					}
					else {
						if ( $landKind == $HlandMegacity ) {
							$landKind = $HlandTown;
						}
						elsif ( $landKind == $HlandMegatower ) {
							$landKind = $HlandTower;
						}
						$land->[$x][$y] = $landKind;
						$lName2 = landName( $landKind, 190 );
						$landValue->[$x][$y] = 190;
					}
					logEventP( $id, $name, "($x, $y)",
"��${lName}��${lName2}����äƤ��ޤ��ޤ�����"
					);
				}
			}
			else {
				if ( $addpop < 0 ) {

					# ��­
					$lv -= ( random( -$addpop ) + 1 );
					if ( ( $landKind == $HlandOil ) && ( $lv < 35 ) ) {
						$land->[$x][$y]      = $HlandSea;
						$landValue->[$x][$y] = 0;
						next;
					}
					elsif (( ( $landKind == $HlandTown ) && ( $lv <= 0 ) )
						|| ( ( $landKind == $HlandSlum ) && ( $lv <= 0 ) ) )
					{

						# ʿ�Ϥ��᤹
						$land->[$x][$y]      = $HlandPlains;
						$landValue->[$x][$y] = 0;
						next;
					}
				}
				else {

					# ��Ĺ
					if ( $lv < 100 ) {
						$lv += random($addpop) + 1;
						$lv = 100 if ( $lv > 100 );
					}
					elsif ( $lv < 130 ) {

						# �ԻԤˤʤ����Ĺ�٤�
						if ( $addpop2 > 0 ) {
							$lv += random( $addpop2 + 1 );
							$lv = 130 if ( $lv > 130 );
						}
					}
					else {

						# ���ԻԤˤʤ����Ĺ��������٤�
						$lv += random($addpop3) if ( $addpop3 > 0 );
					}
				}

				#			if($lv > 200){
				#				$lv = 200;
				#			}
				$landValue->[$x][$y] = $lv;
			}
		}
		elsif ( ( $landKind == $HlandSea ) && ( $lv >= 10 ) ) {

			# �ܿ���
			#		$island->{'food'} += int($lv / 2);
			if ( ( $island->{'Hideri'} == 1 ) || ( $island->{'Kouzui'} == 1 ) )
			{
				$landValue->[$x][$y] -= 5;
				$landValue->[$x][$y] = 1 if ( $landValue->[$x][$y] < 10 );
			}
			elsif ( $lv < 200 ) {

				# �������䤹
				$landValue->[$x][$y]++;
			}
			else {
				$landValue->[$x][$y] = 200;
			}
		}
		elsif ( ( $landKind > 100 ) && ( $landKind < 120 ) ) {

			# ���Ϥξ��

			if (   ( $landKind == $HlandPirate )
				|| ( $landKind == $HlandGhostShip ) )
			{

				# ��±��ͩ�����Ϲ�Ϣ�������оݡ�
				if (   ( $island->{'turnsu'} + $island->{'evil'} < $HdisUN )
					|| ( $island->{'evil'} == 0 ) )
				{
					logUNShip( $id, $name, landName( $landKind, 0 ),
						"($x, $y)" );
					$land->[$x][$y]       = $land2->[$x][$y];
					$landValue->[$x][$y]  = $landValue2->[$x][$y];
					$land2->[$x][$y]      = $HlandSea;
					$landValue2->[$x][$y] = 0;
					next;
				}
			}

			my ( $order, $hp, $sId ) = shipSpec($lv);

			if ( $sId > 0 ) {
				my ($sn) = $HidToNumber{$sId};
				if ( $sn eq '' ) {

					# ����ͭ�礬¸�ߤ��ʤ������񤹤롣
					$land->[$x][$y]       = $land2->[$x][$y];
					$landValue->[$x][$y]  = $landValue2->[$x][$y];
					$land2->[$x][$y]      = $HlandSea;
					$landValue2->[$x][$y] = 0;
					logShipWreck( $id, $name, landName( $landKind, 0 ),
						"($x, $y)" );
					next;
				}
			}

			if ( $shipMove[$x][$y] == 2 ) {

				# ���Ǥ�ư������
				next;
			}
			elsif ( $shipMove[$x][$y] == 0 ) {

				# �����������ξ��ϲ�������
				if ( $HshipHP[ $landKind - $HlandPirate ] > $hp ) {
					$landValue->[$x][$y] +=
					  $HshipKAI[ $landKind - $HlandPirate ] * 1000;
					$hp += $HshipKAI[ $landKind - $HlandPirate ];
				}
			}

			# ����
			if (   ( $landKind == $HlandFishSShip )
				|| ( $landKind == $HlandFishMShip )
				|| ( $landKind == $HlandFishLShip )
				|| ( $landKind == $HlandTitanic ) )
			{
				my ($sIsland) = $Hislands[ $HidToNumber{$sId} ];
				if ( $landKind == $HlandFishSShip ) {
					$sIsland->{'food'} += 30;
				}
				elsif ( $landKind == $HlandTitanic ) {
					$sIsland->{'money'} += 5;
				}
				else {
					$sIsland->{'food'} += 50;
				}
			}

			# �ٽ� �Ȥꤢ��������ˤ����Ĥ���
			if ( ( $sId == $id ) && ( $shipMove[$x][$y] == 0 ) ) {

#			HdebugOut("���ϻٽ�:" . $island->{'name'} . $landKind . ":���:" . $HshipMoney[$landKind - $HlandPirate] . ":����:" . $HshipFood[$landKind - $HlandPirate]);
				$island->{'money'} -= $HshipMoney[ $landKind - $HlandPirate ];
				$island->{'food'}  -= $HshipFood[ $landKind - $HlandPirate ];
			}

			my ( $sx, $sy );
			if ( $order == 2 ) {

				# ���᤬�ɸ�ξ��
				# ����������
				$landValue->[$x][$y] += 1000
				  if ( $HshipHP[ $landKind - $HlandPirate ] > $hp );
				next;
			}
			else {

				# ��ư�ȹ�ư
				( $sx, $sy ) = shipAction( $island, $x, $y );
			}

			# ��ư�Ѥߥե饰
			if ( $sx == 100 ) {

				# �ä���
			}
			elsif ( $HshipSP[ $landKind - $HlandPirate ] == 2 ) {

				# �ȤƤ��ᤤ��
				$shipMove[$sx][$sy] = 1;
			}
			elsif ( $HshipSP[ $landKind - $HlandPirate ] == 1 ) {

				# ®����
				$shipMove[$sx][$sy] = $shipMove[$x][$y] + 1;
			}
			else {

				# ���̤���
				$shipMove[$sx][$sy] = 2;
			}
		}
		elsif ( $landKind == $HlandForest ) {

			# ��
			if ( $lv < 200 ) {

				# �ڤ����䤹
				if ( $island->{'Rain'} == 1 ) {
					$lv += 5;
				}
				elsif ( $island->{'Hideri'} == 1 ) {
					$lv -= 5;
					$lv = 1 if ( $lv < 1 );
				}
				else {
					$lv++;
				}
				$landValue->[$x][$y] = $lv;
			}
			elsif ( $lv >= 200 ) {
				$island->{'money'} += $HtreeValue * $lv;
				$landValue->[$x][$y] = 1;
				logAutoTree( $id, $name );
			}
		}
		elsif ( $landKind == $HlandMonument ) {

			# ��ǰ��
			if (   ( $island->{'pop'} >= 10000 )
				&& ( $island->{'evil'} > 0 )
				&& ( $island->{'tower'} > 450 )
				&& ( random(4) == 0 ) )
			{

				#	if($island->{'pop'} >= 100){
				my ( $i, $sx, $sy );
				for ( $i = 1 ; $i < 7 ; $i++ ) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];
					$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );
					last
					  if ( ( $sx < 0 )
						|| ( $sx >= $HislandSize )
						|| ( $sy < 0 )
						|| ( $sy >= $HislandSize ) );    # �ϰϳ�Ƚ��
					if (   ( $land->[$sx][$sy] == $HlandMegacity )
						|| ( $land->[$sx][$sy] == $HlandMegatower )
						|| ( $land->[$sx][$sy] == $HlandMegaFact )
						|| ( $land->[$sx][$sy] == $HlandMegaFarm ) )
					{
					}
					else {
						last;
					}
				}
				if ( $i >= 7 ) {

					# ȯŸ
					my ($lName) = landName( $landKind, $lv );
					logEventP( $id, $name, "($x, $y)",
"��${lName}����ˤȤ��Ƽ��Ϥ�Ķ�����ԻԤ�ȯŸ���ޤ�����"
					);
					$land->[$x][$y] = $HlandHugecity;
					for ( $i = 1 ; $i < 7 ; $i++ ) {
						$sx = $x + $ax[$i];
						$sy = $y + $ay[$i];
						$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );
						last
						  if ( ( $sx < 0 )
							|| ( $sx >= $HislandSize )
							|| ( $sy < 0 )
							|| ( $sy >= $HislandSize ) );    # �ϰϳ�Ƚ��
						if ( $land->[$sx][$sy] == $HlandMegaFact ) {
							$landValue->[$sx][$sy] = 60;
						}
						elsif ( $land->[$sx][$sy] == $HlandMegatower ) {
							$landValue->[$sx][$sy] = 70;
						}
						elsif ( $land->[$sx][$sy] == $HlandMegaFarm ) {
							$landValue->[$sx][$sy] = 80;
						}
						else {
							$landValue->[$sx][$sy] = 50;
						}
						$land->[$sx][$sy] = $HlandHugecity;
					}
				}
			}
			if ( random(10000) == 0 ) {

				# 1��ʬ��1�γ�Ψ�ǥ�����ɥ������Ȥˤʤ�
				$land->[$x][$y]      = $HlandMonster;
				$landValue->[$x][$y] =
				  3100 + $HmonsterBHP[31] + random( $HmonsterDHP[31] );
				logMonsCome( $id, $name,
					( monsterSpec( $landValue->[$x][$y] ) )[1],
					"($x, $y)", landName( $landKind, $lv ) );
			}
			elsif ( $lv == 9 ) {    # ������
				$island->{'money'} += 300;
				$island->{'GoldMonument'}++;
			}
		}
		elsif ( $landKind == $HlandOsen ) {

			# �����ھ�
			$landValue->[$x][$y] = 10 if ( $lv > 10 );
			if ( random(3) == 0 ) {
				$landValue->[$x][$y]--;
				if ( $landValue->[$x][$y] <= 0 ) {
					$land->[$x][$y]      = $HlandWaste;
					$landValue->[$x][$y] = 0;
				}
			}
		}
		elsif ( $landKind == $HlandDefence ) {
			if ( $lv == 1 ) {

				# �ɱһ��߼���
				logBombFire( $id, $name, landName( $landKind, $lv ),
					"($x, $y)" );

				# �����ﳲ�롼����
				wideDamage( $id, $name, $land, $landValue, $x, $y, 0 );
			}
			elsif ( ( $lv == 20 ) || ( $lv == 21 ) ) {

				# ̸�դ��ɱһ���
				if ( $island->{'money'} < 50 ) {
					logBombFire( $id, $name, landName( $landKind, $lv ),
						"($x, $y)" );
					wideDamage( $id, $name, $land, $landValue, $x, $y, 0 );
				}
				else {
					$island->{'money'} -= 50;
				}
			}
		}
		elsif ( $landKind == $HlandPort ) {

			# ��
			if ( ( seaAround( $land, $x, $y, 7 ) == 0 ) && ( random(3) == 0 ) )
			{

				# ���Ϥ˳��Ϥ�̵�����33%���ĺ�
				logClosedPort( $id, $name, landName( $landKind, $lv ),
					"($x, $y)" );
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
			}
		}
		elsif ( $landKind == $HlandBank ) {

			# ���
			if ( ( $lv >= 30 ) && ( random(1000) == 0 ) ) {
				logEventP( $id, $name, "(?, ?)",
"�ζ�Ԥ��ݻ��������ˤʤ�ޤ���������Ū��������ˤ�구�Ϥ�Ⱦʬ�ˤʤ�ޤ������ݻ����Ȥ�ޤ�����"
				);
				logSecret(
"�ݻ��������ˤʤä��Τ�${HtagName_}($x, $y)${H_tagName}�����ζ�ԤǤ���",
					$id
				);
				$landValue->[$x][$y] = int( $lv / 2 );
			}
			elsif ( ( $lv < 30 ) && ( random(1000) == 0 ) ) {
				logEventP( $id, $name, "($x, $y)",
					"�ζ�Ԥ��ݻ������Ϥˤʤ�ޤ�����" );
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
			}
			else {
				$island->{'money'} += $lv * ( random(3) + 1 );
			}
		}
		elsif ( ( $landKind == $HlandOil ) && ( ( $lv == 6 ) || ( $lv == 7 ) ) )
		{

			# ������ɽ𡢳���ǥ��ȥ�åפΰݻ���
			if ( $island->{'money'} < 5 ) {
				$land->[$x][$y]      = $HlandSea;
				$landValue->[$x][$y] = 0;
			}
			else {
				$island->{'money'} -= 5;
			}
		}
		elsif ( $landKind == $HlandFire ) {    # ���ɽ�ΰݻ���
			if ( $island->{'money'} < 3 ) {
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
			}
			else {
				$island->{'money'} -= 3;
				$landValue->[$x][$y] = 10
				  if ( random(100) < 1 );      # S���ɽ��ȯŸ
			}
		}
		elsif ( ( $landKind == $HlandOil ) && ( $lv == 0 ) ) {

			# ��������
			# �ϳ�Ƚ��
			if ( random(1000) < $HoilRatio ) {

				# �ϳ�
				logOilEnd( $id, $name, landName( $landKind, $lv ), "($x, $y)" );
				$land->[$x][$y]      = $HlandSea;
				$landValue->[$x][$y] = 0;
			}

			#���Ƥ����Ĥθϳ�Ƚ���Ԥä����ɤ���
			$oilFlag--;
			next if ( $oilFlag > 0 );
			if ( $island->{'order'} & 2048 ) {

				# ���Ĥϻ�����������
				my $value = $island->{'oilfield'} * $HoilMoney * 2;
				$island->{'money'} += $value;

				# ������
				logOilMoney( $id, $name, landName( $landKind, $lv ),
					"($x, $y)", $value );
			}
			else {
				my $value = $island->{'oilfield'} * $HoilMoney;
				$island->{'oil'} += $value;

				# ������
				my $lName = landName( $landKind, $lv );
				logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>$lName</B>���顢<B>$value$HunitOil</B>�μ��פ��夬��ޤ�����",
					$id
				);
			}
		}
		elsif ( ( $landKind == $HlandWaste ) && ( $lv >= 10 ) ) {

			# ����
			my $value = $lv * ( random(23) + 1 );
			$island->{'money'} += $value;

			# ������
			logOilMoney( $id, $name, landName( $landKind, $lv ),
				"($x, $y)", $value );

			# �ϳ�Ƚ��
			if ( random(10) < 6 ) {
				$landValue->[$x][$y] -= random(21);
				if ( $landValue->[$x][$y] < 10 ) {

					# �ϳ�
					logOilEnd( $id, $name, landName( $landKind, $lv ),
						"($x, $y)" );
					$land->[$x][$y]      = $HlandWaste;
					$landValue->[$x][$y] = 1;
				}
			}
			else {
				$landValue->[$x][$y] += random(21);
				$landValue->[$x][$y] = 200 if ( $landValue->[$x][$y] > 200 );
			}
		}
		elsif ( $landKind == $HlandPlains ) {

			# ʿ��
			if ( random(5) == 0 ) {

				# ��������졢Į������С�������Į�ˤʤ�
				if ( countGrow( $land, $landValue, $x, $y ) ) {
					$land->[$x][$y]      = $HlandTown;
					$landValue->[$x][$y] = 1;
				}
			}
		}
		elsif (( $landKind == $HlandExpo )
			|| ( $landKind == $HlandStadium )
			|| ( $landKind == $HlandDome )
			|| ( $landKind == $HlandAmusement )
			|| ( $landKind == $HlandAirport )
			|| ( $landKind == $HlandZoo ) )
		{

	  # �����񡢥��������ࡢ�ɡ��ࡢͷ���ϡ�������ưʪ��
			$island->{'money'} += 40;
		}
		elsif ( $landKind == $HlandCasino ) {

			# ������
			$island->{'money'} += random(150) - 50;
		}
		elsif ( $landKind == $HlandBigcity ) {

			# ���Ի�
			$island->{'food'} -= 400 if ( !$HbigcityFood );

			#	}elsif(($landKind == $HlandPark) || ($landKind == $HlandSchool)){
			#		# ���ࡢ�ع�
			#		$island->{'money'} += 10;
		}
		elsif (( $landKind == $HlandWindmill )
			|| ( $landKind == $HlandPolice )
			|| ( $landKind == $HlandHospital ) )
		{

			# ���֡��ٻ����±��ݻ���
			if ( $island->{'money'} < 5 ) {
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
			}
			else {
				$island->{'money'} -= 5;
			}
		}
		elsif ( ( $landKind == $HlandTower ) && ( $lv >= 200 ) ) {

# MAX���ȥӥ�
#		HdebugOut($island->{'name'} . "�����Ȥε��ϡ�" . $island->{'tower'} . ":�͸����ѥ飳��${pop3}��");
			if (   ( $island->{'pop'} >= 8000 )
				&& ( $island->{'tower'} > 450 )
				&& ( $pop3 > 2 )
				&& ( random(5) == 0 ) )
			{
				my $lName  = landName( $HlandTower, 200 );
				my $lName2 = landName( $HlandTcity, 200 );
				logOut(
"${HtagName_}${name}${AfterName}($x, $y)${H_tagName}��<B>$lName</B>����<B>$lName2</B>��ȯŸ���ޤ�����",
					$id
				);
				$land->[$x][$y]      = $HlandTcity;
				$landValue->[$x][$y] = 200;
			}
		}
		elsif ( $landKind == $HlandTcity ) {

# �����Ի�
#		HdebugOut($island->{'name'} . "�������Ի�:�͸����ѥ飳��${pop3}��");
			if (   ( $island->{'pop'} < 7000 )
				|| ( ( $pop3 < -3 ) && ( random(5) == 0 ) ) )
			{
				my $lName  = landName( $HlandTcity, 200 );
				my $lName2 = landName( $HlandTower, 200 );
				logOut(
"${HtagName_}${name}${AfterName}($x, $y)${H_tagName}��<B>$lName</B>����<B>$lName2</B>�˥�٥�����󤷤ޤ�����",
					$id
				);
				$land->[$x][$y]      = $HlandTower;
				$landValue->[$x][$y] = 200;
			}
		}
		elsif ( $landKind == $HlandSeisei ) {

			# ������
			my $value = $lv * 100;
			$island->{'money'} += $value;

			# ������
			logOilMoney( $id, $name, landName( $landKind, $lv ),
				"($x, $y)", $value );

			# �ϳ�Ƚ��
			if ( random(1000) < $HoilRatio ) {
				logOilEnd( $id, $name, landName( $landKind, $lv ), "($x, $y)" );
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
			}
		}
		elsif ( $landKind == $HlandMonster ) {

			# ����
			# �����Ǥμ��Ф�
			my ( $mKind, $mName, $mHp ) = monsterSpec( $landValue->[$x][$y] );
			my ($special) = $HmonsterSpecial[$mKind];

			if (   ( $island->{'turnsu'} + $island->{'evil'} < $HdisUN )
				|| ( $island->{'evil'} == 0 ) )
			{
				logUNMons( $id, $name, $mName, "($x, $y)" );
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
				next;
			}
			if ( $monsterMove[$x][$y] == 2 ) {

				# ���Ǥ�ư������
				next;
			}

			# �Ų���?
			if (
				   ( ( $special == 3 ) && ( ( $HislandTurn % 2 ) == 1 ) )
				|| ( ( $special == 4 ) && ( ( $HislandTurn % 2 ) == 0 ) )
				|| ( $special == 5 )
				|| (   ( $island->{'manipulate'} == 0 )
					&& ( ( $special == 6 ) || ( $special == 7 ) ) )
			  )
			{
				next;    # �Ų���
			}

			if ( $special == 9 ) {

				# ����������
				$landValue->[$x][$y] = $mKind * 100 + $HmonsterBHP[$mKind];
				logMonster( $id, $name, "($x, $y)", $mName,
"�ϡ��������椷�����ȸ�����Ȥߤ�ߤ�����������ޤ�����"
				);
			}

			# ��ư����
			my ( $sx, $sy ) = monmove( $island, $x, $y, 0 );

			# ��ư�Ѥߥե饰
			if ( $HmonsterSpecial[$mKind] == 2 ) {

				# ��ư�Ѥߥե饰��Ω�Ƥʤ�
			}
			elsif ( $HmonsterSpecial[$mKind] == 1 ) {

				# ®������
				$monsterMove[$sx][$sy] = $monsterMove[$x][$y] + 1;
			}
			else {

				# ���̤β���
				$monsterMove[$sx][$sy] = 2;
			}
		}
		elsif ( $landKind == $HlandKInora ) {

			# ���ۤ��Τ�
			if (   ( $island->{'turnsu'} + $island->{'evil'} < $HdisUN )
				|| ( $island->{'evil'} == 0 ) )
			{
				logUNMons( $id, $name, $mName, "($x, $y)" );
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
				next;
			}
			kinoraMove( $island, $x, $y );
		}
		elsif ( $land->[$x][$y] > 51 ) {

		 # ���ꤨ�ʤ��Ϸ��λ��ϡ��Ȥꤢ�������Ϥˤ��Ƥ���
			$land->[$x][$y]      = $HlandWaste;
			$landValue->[$x][$y] = 0;
		}
		if ($Htournament) {

			# �ʰץȡ��ʥ���
			if ( $HislandFightMode == 3 ) {

				# ��Ʈ��
			}
			else {

				# ����ʳ�
				if ( $landKind == $HlandWarp ) {

					# ž�����֤ϤȤꤢ�������֤ˤ��롣
					logEventP( $id, $name, "($x, $y)",
"��ž�����֤ϡ���Ʈ���֤Ǥʤ�����������줪�֤��������ޤ�����"
					);
					$land->[$x][$y]      = $HlandFlower;
					$landValue->[$x][$y] = random(13) + 1;
				}
			}
		}
		if ( ( $land->[$x][$y] > 100 ) || ( $landKind == $HlandKInora ) ) {

			# ���ϡ����ۤ��Τ�ΤȤ�
		}
		elsif (( $land->[$x][$y] == $HlandMonster )
			|| ( $land->[$x][$y] == $HlandHaribote ) )
		{
			if ( $landValue->[$x][$y] > 4000 ) {

			# ���ꤨ�ʤ��ͤʤΤǡ��Ȥꤢ�������Ϥˤ��Ƥ���
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
			}
		}
		elsif (( $land->[$x][$y] == $HlandBase )
			|| ( $land->[$x][$y] == $HlandSbase ) )
		{
			if ( $landValue->[$x][$y] > 250 ) {

			# 250�ʾ�Ϥ��ꤨ�ʤ��ΤǤȤꤢ����250�ˤ��Ƥ���
				$landValue->[$x][$y] = 250;
			}
		}
		elsif (( $landValue->[$x][$y] > 200 )
			&& ( $land->[$x][$y] != $HlandWarp ) )
		{

# 200�ʾ�Ϥ��ꤨ�ʤ��ΤǤȤꤢ����200�ˤ��Ƥ��� ž�����ְʳ�
#		HdebugOut("�Ϸ��ǡ����������ΰ٤Ȥꤢ�����������ˤ��ޤ���:LAND=" . $land->[$x][$y] . ":LV=" . $landValue->[$x][$y]);
			$landValue->[$x][$y] = 200;
		}

		# �����Ϸ��Ѳ�
		# �ѹ�����  <5.54e>
		#	($landKind,$lv) = ($land->[$x][$y],$landValue->[$x][$y]);
		$landKind = $land->[$x][$y];

		# �ѹ���λ  <5.54e>
		if (   ( ( $landKind == $HlandTown ) && ( $lv >= 201 ) )
			|| ( ( $landKind == $HlandFarm )    && ( $lv >= 50 ) )
			|| ( ( $landKind == $HlandFactory ) && ( $lv >= 90 ) )
			|| ( ( $landKind == $HlandTower )   && ( $lv >= 180 ) ) )
		{

			# 200���Իԡ����졢���졢���ȥӥ�ΤȤ�
			my ( $i, $j, $r, $sx, $sy );
			for ( $i = 1 ; $i < 7 ; $i++ ) {
				$sx = $x + $ax[$i];
				$sy = $y + $ay[$i];
				$sx--
				  if ( !( $sy % 2 ) && ( $y % 2 ) );  # �Ԥˤ�����Ĵ��
				if (   ( $sx < 0 )
					|| ( $sx >= $HislandSize )
					|| ( $sy < 0 )
					|| ( $sy >= $HislandSize ) )
				{

					# �ϰϳ��ξ�粿�⤷�ʤ�
				}
				elsif (
					(
						   ( $land->[$sx][$sy] == $landKind )
						&& ( $landValue->[$sx][$sy] >= 200 )
					)
					|| (   ( $landKind == $HlandFarm )
						&& ( $land->[$sx][$sy] == $HlandFarm )
						&& ( $landValue->[$sx][$sy] >= 50 ) )
					|| (   ( $landKind == $HlandFactory )
						&& ( $land->[$sx][$sy] == $HlandFactory )
						&& ( $landValue->[$sx][$sy] >= 100 ) )
				  )
				{

					# �ϰ���ξ��ǹ��β�ǽ�Ϸ������ä��Ȥ�

					# ��̣�����ʷ׻��򤷤�ʣ���ˤ��롣
					$r = 30;
					$r -= 20 if ( $island->{'propaganda'} == 1 ); # Ͷ�׳�ư
					$r += 170 if ( $island->{'evil'} == 0 );   # ��Ϣ�ݸ��
					$r -= 15
					  if ( $island->{'event'} == 1 ); # �͸����Υ��٥��
					if ( $island->{'Crime'} + $island->{'Pollution'} +
						$island->{'Kouzui'} + $island->{'Hideri'} >= 1 )
					{

						# �Ⱥᡢ���������塢���Ȥ�
						$r += 1000;
					}
					if ( $island->{'zyuni'} > 700 ) {    # �����
						$r -= 10;
					}
					elsif ( $island->{'zyuni'} > 500 ) {
						$r -= 7;
					}
					elsif ( $island->{'zyuni'} > 300 ) {
						$r -= 5;
					}
					elsif ( $island->{'zyuni'} > 100 ) {
						$r -= 3;
					}

					# ����޿���׻�
					my ( $k, $f, $flags, $kazu );
					$f     = 1;
					$kazu  = 0;
					$flags = $island->{'status'};
					for ( $k = 0 ; $k < $HturnPrizeNumber ; $k++ ) {
						$kazu++ if ( $flags & $f );
						$f *= 2;
					}
					$r -= $kazu * 8;
					$r = 2 if ( $r < 2 );
					if ( random($r) == 0 ) {

						# ��������Ϸ������������
						if ( $i < 4 ) {
							$j = $i + 3;
						}
						else {
							$j = $i - 3;
						}
						my ($lName) = landName( $landKind, $lv );
						my ($lName2);
						if ( $landKind == $HlandTown ) {

							# �ԻԤΤȤ�
							$lName2 = landName( $HlandMegacity, 0 );
							$land->[$x][$y]   = $HlandMegacity;
							$land->[$sx][$sy] = $HlandMegacity;
						}
						elsif ( $landKind == $HlandFarm ) {

							# ����ΤȤ�
							$lName2 = landName( $HlandMegaFarm, 0 );
							$land->[$x][$y]   = $HlandMegaFarm;
							$land->[$sx][$sy] = $HlandMegaFarm;
						}
						elsif ( $landKind == $HlandFactory ) {

							# ����ΤȤ�
							$lName2 = landName( $HlandMegaFact, 0 );
							$land->[$x][$y]   = $HlandMegaFact;
							$land->[$sx][$sy] = $HlandMegaFact;
						}
						elsif ( $landKind == $HlandTower ) {

							# ���ȥӥ�ΤȤ�
							$lName2 = landName( $HlandMegatower, 0 );
							$land->[$x][$y]   = $HlandMegatower;
							$land->[$sx][$sy] = $HlandMegatower;
						}
						logEventP( $id, $name, "($x, $y)",
"��${HtagName_}($sx, $sy)${H_tagName}��${lName}��${lName2}��ȯŸ���ޤ�����"
						);
						$landValue->[$x][$y]   = $i;
						$landValue->[$sx][$sy] = $j;
						last;
					}
				}
			}
		}
		( $landKind, $lv ) = ( $land->[$x][$y], $landValue->[$x][$y] );

		# �����Ȼ�
		if ( random(5) == 0 ) {

			# ʿ�ϡ����ϡ����������졢�����λ�
			if (   ( $landKind == $HlandWaste )
				|| ( $landKind == $HlandPlains )
				|| ( $landKind == $HlandFarm )
				|| ( $landKind == $HlandOsen ) )
			{
				if ( chkAround( $land, $x, $y, $HlandOsen, 7 ) ) {
					if ( ( $landKind == $HlandOsen ) && ( $lv < 10 ) ) {
						$landValue->[$x][$y]++;
					}
					elsif ( $landKind != $HlandOsen ) {
						if (   ( $landKind == $HlandFarm )
							|| ( ( $landKind == $HlandWaste ) && ( $lv >= 10 ) )
						  )
						{
							logOsen( $id, $name, landName( $landKind, $lv ),
								"($x, $y)" );
						}
						$land->[$x][$y]      = $HlandOsen;
						$landValue->[$x][$y] = 1;
					}
				}
			}
		}
		( $landKind, $lv ) = ( $land->[$x][$y], $landValue->[$x][$y] );

		# ������ˤ�����
		# ���ϡ����á�������������ǰ��ʳ�
		if (   ( $HseaChk[ $land->[$x][$y] ] == 0 )
			&& ( $land->[$x][$y] != $HlandMountain )
			&& ( $land->[$x][$y] != $HlandMonument )
			&& ( $land->[$x][$y] != $HlandOsen )
			&& ( $land->[$x][$y] != $HlandMyhome )
			&& ( $land->[$x][$y] != $HlandFuji )
			&& ( $land->[$x][$y] != $HlandKInora )
			&& ( $land->[$x][$y] != $HlandMonster ) )
		{
			if ( random(100) == 0 ) {
				if ( chkAround( $land, $x, $y, $HlandSeisei, 7 ) ) {
					$land->[$x][$y]      = $HlandOsen;
					$landValue->[$x][$y] = random(3) + 1;
					logOsen( $id, $name, landName( $landKind, $lv ),
						"($x, $y)" );
				}
			}
		}
		( $landKind, $lv ) = ( $land->[$x][$y], $landValue->[$x][$y] );

		# ���ˤ�뿹����
		if (   ( $island->{'Rain'} == 1 )
			&& ( random(2) == 0 )
			&& ( $landKind == $HlandPlains ) )
		{
			if ( chkAround( $land, $x, $y, $HlandForest, 7 ) ) {
				$land->[$x][$y]      = $HlandForest;
				$landValue->[$x][$y] = 1;

			}
		}
		( $landKind, $lv ) = ( $land->[$x][$y], $landValue->[$x][$y] );

		# �����ˤ����������Ƚ��
		if (   ( $HseaChk[ $land->[$x][$y] ] == 0 )
			&& ( $land->[$x][$y] != $HlandMountain )
			&& ( $land->[$x][$y] != $HlandMonument )
			&& ( $land->[$x][$y] != $HlandMyhome )
			&& ( $land->[$x][$y] != $HlandFuji )
			&& ( $land->[$x][$y] != $HlandKInora )
			&& ( $land->[$x][$y] != $HlandMonster ) )
		{
			if ( random(10000) <
				countAroundEX( $land, $landValue, $x, $y, $HlandWaste, 10, 19 )
				* $HdisTinka )
			{
				logFalldownLandO( $id, $name, landName( $landKind, $lv ),
					"($x, $y)" );
				$land->[$x][$y]      = $HlandSea;
				$landValue->[$x][$y] = 1;
			}
		}
		( $landKind, $lv ) = ( $land->[$x][$y], $landValue->[$x][$y] );

		# ��ʮ��Ƚ��
		if ( ( $landKind == $HlandMountain ) && ( $lv >= 1 ) ) {
			if ( random(1000) <
				countAroundEX( $land, $landValue, $x, $y, $HlandWaste, 10, 7 ) *
				$HdisAEruption )
			{
				$island->{'AEruption'}  = 1;
				$island->{'AEruptionX'} = $x;
				$island->{'AEruptionY'} = $y;
			}
		}
		( $landKind, $lv ) = ( $land->[$x][$y], $landValue->[$x][$y] );

		# ����ϲ�ꥷ�����Τ�Ƚ��
		if (
			( $island->{'kaitei'} > $HdisKLimit )
			&& (   ( $landKind == $HlandOil )
				|| ( $landKind == $HlandSbase )
				|| ( $landKind == $HlandSMonument ) )
		  )
		{
			my ($ks) = $island->{'kaitei'} - $HdisKLimit;
			if ( $ks > 30 ) { $ks = 30; }
			if ( random(1000) < $ks ) {
				$land->[$x][$y]      = $HlandMonster;
				$landValue->[$x][$y] = 905;
				logMonsCome( $id, $name, ( monsterSpec(905) )[1],
					"($x, $y)", landName( $landKind, $lv ) );
			}
		}
		( $landKind, $lv ) = ( $land->[$x][$y], $landValue->[$x][$y] );

		# ���Ω�Ƥ��Τ顢������Ƚ��
		if (   ( ( $landKind == $HlandSea ) && ( $lv <= 1 ) )
			&& ( $island->{'pop'} >= $HdisMonsBorder1 ) )
		{    # �����������͸������ͣ��ʾ�
			my $r = random($HdisMonsterU);
			if ( $r == 0 ) {
				if ( ($HsurvFlg) && ( $HdisMonster == 0 ) ) {

				 # ���Х��Х롢����ȯ��Ψ0�ξ��Ͻи����ʤ�
				}
				else {
					$land->[$x][$y]      = $HlandMonster;
					$landValue->[$x][$y] =
					  1600 + $HmonsterBHP[16] + random( $HmonsterDHP[16] );
					logMonsCome( $id, $name, ( monsterSpec(1605) )[1],
						"($x, $y)", landName( $landKind, $lv ) );
				}
			}
			elsif ( $r < 5 ) {
				$land->[$x][$y] = $HlandBalloonS;
				$landValue->[$x][$y] = 10000 + ( random(6) + 1 ) * 1000;
				logShipCome( $id, $name, landName( $HlandBalloonS, 0 ),
					"($x, $y)" );
			}
		}
		( $landKind, $lv ) = ( $land->[$x][$y], $landValue->[$x][$y] );

		# �к�Ƚ��
		if (   ( ( $landKind == $HlandTown ) && ( $lv > 30 ) )
			|| ( $landKind == $HlandMegacity )
			|| ( ( $landKind == $HlandSlum ) && ( $lv > 30 ) )
			|| ( ( $landKind == $HlandOil ) && ( $lv >= 5 ) )
			|| ( $landKind == $HlandHaribote )
			|| ( $landKind == $HlandFire )
			|| ( $landKind == $HlandPolice )
			|| ( $landKind == $HlandHospital )
			|| ( $landKind == $HlandFactory ) )
		{

			my ($wf) = 1000;
			if (   ( $HpunishInfo{$id}->{punish} == 11 )
				&& ( $HpunishInfo{$id}->{x} == $x )
				&& ( $HpunishInfo{$id}->{y} == $y ) )
			{
				$wf = 1;
			}
			else {
				if ( $landKind == $HlandOil ) {
					$wf = 1000;
				}
				elsif ( ( $whp < 2 ) && ( $wkind < 3 ) ) {
					$wf = 500;
				}
				elsif ( $wkind > 3 ) {    # ���λ�
					$wf = ( $whp > 7 ) ? 4000 : 2000;
				}
			}
			if ( random($wf) < $HdisFire ) {

				# ���Ϥο��ȵ�ǰ����������ࡢ���֤�
				my $s = chkAround( $land, $x, $y, $HlandSMonument, 7 );
				if (
					(
						(
							chkAround( $land, $x, $y, $HlandForest,   7 ) +
							chkAround( $land, $x, $y, $HlandMonument, 7 ) +
							chkAround( $land, $x, $y, $HlandFlower,   7 ) +
							chkAround( $land, $x, $y, $HlandWindmill, 7 ) +
							chkAround( $land, $x, $y, $HlandPark,     7 ) + $s
						) == 0
					)
					||    # ���Ϥ˲кҤ��ɤ��Ϸ���̵�����
					( ( $landKind == $HlandOil ) && ( $s == 0 ) )
					||    # ����ϤǼ��Ϥ˳��쵭ǰ�̵꤬�����
					( ( $landKind == $HlandOil ) && ( $lv == 7 ) )
					||    # ������ɽ�ξ��
					( $landKind == $HlandFire )
				  )
				{         # ���ɽ�ξ��
					my $fire1 =
					  chkAround( $land, $x, $y, $HlandFire, 19 );    # ���ɽ�
					my $fire2 =
					  chkAroundEX( $land, $landValue, $x, $y, $HlandFire, 10,
						37 );    # S���ɽ�
					my $fire3 =
					  chkAroundEX( $land, $landValue, $x, $y, $HlandOil, 7,
						19 );    # ������ɽ�

					if (   ( $fire1 + $fire2 )
						&& ( $landKind != $HlandFire )
						&& ( $landKind != $HlandOil ) )
					{            # Φ�βкҤ��ɤ����
						if ( $island->{'money'} > 50 ) {
							$island->{'money'} -= 50;
							logFireD( $id, $name, landName( $landKind, $lv ),
								"($x, $y)" );
						}
						else {
							$land->[$x][$y]      = $HlandWaste;
							$landValue->[$x][$y] = 0;
							logFire( $id, $name, landName( $landKind, $lv ),
								"($x, $y)" );
						}
					}
					elsif (( $fire2 + $fire3 )
						&& ( $lv != 7 )
						&& ( $landKind == $HlandOil ) )
					{    # ���βкҤ��ɤ����
						if ( $island->{'money'} > 100 ) {
							$island->{'money'} -= 100;
							logFireD( $id, $name, landName( $landKind, $lv ),
								"($x, $y)" );
						}
						else {
							$land->[$x][$y]      = $HlandSea;
							$landValue->[$x][$y] = 0;
							logFire( $id, $name, landName( $landKind, $lv ),
								"($x, $y)" );
						}
					}
					elsif ( $landKind == $HlandOil ) {
						if ( $island->{'order'} & 1024 ) {
							if ( $lv == 5 ) {
								slideBack( $island->{'command'}, 0, $HcomDbase,
									$id, $x, $y, 0 );
							}
							elsif ( $lv == 7 ) {
								slideBack( $island->{'command'}, 0, $HcomFire,
									$id, $x, $y, 0 );
							}
						}
						$land->[$x][$y]      = $HlandSea;
						$landValue->[$x][$y] = 0;
						logFire( $id, $name, landName( $landKind, $lv ),
							"($x, $y)" );
					}
					else {
						if (   ( $island->{'order'} & 1024 )
							&& ( $landKind == $HlandFire ) )
						{
							slideBack( $island->{'command'}, 0, $HcomFire, $id,
								$x, $y, 0 );
							slideBack( $island->{'command'}, 0, $HcomPrepare2,
								$id, $x, $y, 0 );
						}
						$land->[$x][$y]      = $HlandWaste;
						$landValue->[$x][$y] = 0;
						logFire( $id, $name, landName( $landKind, $lv ),
							"($x, $y)" );
					}
				}
			}
		}

	}
}    # doEachHex

# ������
sub doIslandProcess {
	my ( $number, $island ) = @_;

	# Ƴ����
	my ( $name, $id, $land, $landValue, $land2, $landValue2 ) = (
		$island->{'name'},      $island->{'id'},    $island->{'land'},
		$island->{'landValue'}, $island->{'land2'}, $island->{'landValue2'}
	);

	if ( $island->{'SSSystem'} ) {

#	logEvent($id, $name,"�ϡ�<B>�����ѡ�������ɥ����ƥ�</B>��ȯư�桪��");
	}
	else {

		# ���ۤ��Τ�Ƚ��(���ۤΤ�)
		if ( $HpunishInfo{$id}->{punish} == 10 ) {
			my ( $x, $y );
			$x        = $HpunishInfo{$id}->{x};
			$y        = $HpunishInfo{$id}->{y};
			$landKind = $land->[$x][$y];
			$lv       = $landValue->[$x][$y];
			logMonsCome( $id, $name, landName( $HlandKInora, 0 ),
				"($x, $y)", landName( $landKind, $lv ) );
			$land->[$x][$y] = $HlandKInora;
			$landValue->[$x][$y] = 50000 + ( random(60) * 100 ) + 4000;
			kinoraMake( $land, $landValue, $x, $y );
		}

		if ( $id > 90 ) {

			# Battle Field�ΤȤ�
			$island->{'tenki'}  = 0;
			$island->{'area'}   = 0;
			$island->{'forest'} = 0;

			$island->{'pop'}      = -$island->{'id'};
			$island->{'farm'}     = 0;
			$island->{'port'}     = 0;
			$island->{'factory'}  = 0;
			$island->{'tower'}    = 0;
			$island->{'mountain'} = 0;
			$island->{'yousyoku'} = 0;
			$island->{'kaitei'}   = 0;
			$island->{'MissileK'} = 0;

			$island->{'oilfield'} = 0;
			$island->{'mons'}     = 0;
			$island->{'forestV'}  = 0;
			$island->{'haribote'} = 0;
			$island->{'industry'} = 0;
			$island->{'monument'} = 0;

			$island->{'evil'}   = 200;
			$island->{'zyuni'}  = 0;
			$island->{'status'} = 0;
			$island->{'score'}  = 0;
			$island->{'absent'} = 0;
			$island->{'turnsu'} = 1000;

			$island->{'ship'}   = 0;
			$island->{'flower'} = 0;
			return;
		}

#	HdebugOut($island->{'name'} . "$AfterName ������" . $island->{'eis0'} . "��" . $island->{'eis1'} . "��" . $island->{'eis2'});
		my $disTyphoon =
		  ( $island->{'eis0'} ) ? int( $HdisTyphoon / 2 ) : $HdisTyphoon;
		my $disAkasio =
		  ( $island->{'eis0'} ) ? int( $HdisAkasio / 2 ) : $HdisAkasio;
		my $disEarthquake =
		  ( $island->{'eis1'} ) ? int( $HdisEarthquake / 2 ) : $HdisEarthquake;
		my $disTsunami =
		  ( $island->{'eis1'} ) ? int( $HdisTsunami / 2 ) : $HdisTsunami;
		my $disEruption =
		  ( $island->{'eis1'} ) ? int( $HdisEruption / 2 ) : $HdisEruption;
		my $disMeteo =
		  ( $island->{'eis2'} ) ? int( $HdisMeteo / 2 ) : $HdisMeteo;
		my $disHugeMeteo =
		  ( $island->{'eis2'} ) ? int( $HdisHugeMeteo / 2 ) : $HdisHugeMeteo;

		# �Ͽ�Ƚ��
		if (
			( $HpunishInfo{$id}->{punish} == 1 )
			|| ( random(1000) <
				( ( $island->{'prepare2'} + 1 ) * $disEarthquake ) )
		  )
		{

			# �Ͽ�ȯ��
			my ( $x, $y, $sx, $sy, $i );
			if ( $HpunishInfo{$id}->{punish} == 1 ) {
				$x = $HpunishInfo{$id}->{x};
				$y = $HpunishInfo{$id}->{y};
			}
			else {
				$x = random($HislandSize);
				$y = random($HislandSize);
			}
			if ( chkAround( $land, $x, $y, $HlandAmusement, $x ) ) {

				# ȯ�����ʤ���
			}
			else {
				logEarthquake( $id, $name, "($x, $y)" );

				# �̸������ʤ�����ȯ��
				$island->{'tunami'} = 1 if ( $HseaChk[ $land->[$x][$y] ] );

				# ����4�إå������ﳲ
				for ( $i = 0 ; $i < 61 ; $i++ ) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];
					$sx--
					  if ( !( $sy % 2 ) && ( $y % 2 ) )
					  ;    # �Ԥˤ�����Ĵ��
					my ($landKind) = $land->[$sx][$sy];
					my ($lv)       = $landValue->[$sx][$sy];
					my ($landName) = landName( $landKind, $lv );
					my ($point)    = "($sx, $sy)";
					next
					  if ( ( $sx < 0 )
						|| ( $sx >= $HislandSize )
						|| ( $sy < 0 )
						|| ( $sy >= $HislandSize ) );    # �ϰϳ�Ƚ��
					my ($d) = 0;

					if (   ( ( $landKind == $HlandTown ) && ( $lv >= 50 ) )
						|| ( ( $landKind == $HlandSlum ) && ( $lv >= 30 ) )
						|| ( $landKind == $HlandHaribote )
						|| ( $landKind == $HlandFactory ) )
					{

			 # 5��ʾ��Į��3��ʾ�Υ���ࡢ�ϥ�ܥơ�����
						if ( $i == 0 ) {
							$d = 200;
						}
						elsif ( $i < 7 ) {
							$d = ( random(5) + 3 ) * 10;
						}
						elsif ( $i < 19 ) {
							$d = ( random(4) + 1 ) * 10;
						}
						elsif ( $i < 37 ) {
							$d = random(3) * 10;
						}
						else {
							$d = random(2) * 10;
						}
						if (   ( $landKind == $HlandTown )
							|| ( $landKind == $HlandSlum ) )
						{
							$d = $d * 3;
						}
						if ( $d >= 150 ) {
							logEQDestroy( $id, $name, $landName, $point );
							$landKind = $HlandWaste;
							$lv       = 0;
						}
						elsif ( $d != 0 ) {
							if (
								   ( $lv <= $d )
								|| ( $landKind == $HlandHaribote )
								|| (   ( $landKind == $HlandFactory )
									&& ( $lv < $d + 30 ) )
							  )
							{
								logEQDestroy( $id, $name, $landName, $point );
								$landKind = $HlandWaste;
								$lv       = 0;
							}
							else {
								$lv -= $d;
								logEQDamage( $id, $name, $landName, $point );
							}
						}
						$land->[$sx][$sy]      = $landKind;
						$landValue->[$sx][$sy] = $lv;
					}
				}
			}
		}

		# ������­
		if ( $island->{'food'} <= 0 ) {

			# ��­��å�����
			logStarve( $id, $name );
			$island->{'food'} = 0;
			my ( $x, $y, $landKind, $lv, $i, $lName );
			for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
				$x        = $Hrpx[$i];
				$y        = $Hrpy[$i];
				$landKind = $land->[$x][$y];
				$lName    = landName( $landKind, $landValue->[$x][$y] );
				if (   ( $landKind == $HlandFarm )
					|| ( $landKind == $HlandFactory )
					|| ( $landKind == $HlandBase )
					|| ( $landKind == $HlandBigcity )
					|| ( $landKind == $HlandHugecity )
					|| ( $landKind == $HlandDefence ) )
				{

					# 1/4�ǲ���
					if ( random(4) == 0 ) {
						if ( $kind == $HlandHugecity ) {

							# Ķ�����Ի�
							my ($lName2) =
							  landName( $HlandMonument, $landValue->[$x][$y] );
							logEventP( $id, $island->{'name'}, "($x, $y)",
"��<B>$lName</B>��<B>��������ƽ�̱������</B>��<B>$lName</B>��<B>$lName2</B>����äƤ��ޤ��ޤ�����"
							);
							$land->[$x][$y] = $HlandMonument;
						}
						else {
							logSvDamage( $id, $name, $lName, "($x, $y)" );
							$land->[$x][$y]      = $HlandWaste;
							$landValue->[$x][$y] = 0;
						}
					}
				}
			}
		}

		# ����Ƚ��
		if ( ( $HpunishInfo{$id}->{punish} == 2 )
			|| (   ( random(1000) < $disTsunami )
				|| ( $island->{'tunami'} >= 1 ) ) )
		{

			# ����ȯ��
			my ( $x, $y, $landKind, $lv, $i, $p, $q );
			if ( $island->{'tunami'} == 1 ) {   # �����Ͽ̤ˤ��������
				logEvent( $id, $name,
"���Ͽ̤ϡ��̸��������ä�����${HtagDisaster_}������${H_tagDisaster}ȯ������"
				);
				$p = 10;
				$q = 25;
			}
			else {    # �̾�����ȡ�����ˡ��������
				logEvent( $id, $name,
"�ն��${HtagDisaster_}����${H_tagDisaster}ȯ������"
				);
				$p = 12;
				$q = 30;
			}
			for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
				$x        = $Hrpx[$i];
				$y        = $Hrpy[$i];
				$landKind = $land->[$x][$y];
				$lv       = $landValue->[$x][$y];

				if (   ( $landKind == $HlandTown )
					|| ( $landKind == $HlandSlum )
					|| ( $landKind == $HlandFarm )
					|| ( $landKind == $HlandFactory )
					|| ( $landKind == $HlandBase )
					|| ( $landKind == $HlandDefence )
					|| ( $landKind == $HlandPort )
					|| ( $landKind == $HlandHaribote ) )
				{
					if ( random($p) < ( seaAround( $land, $x, $y, 7, 1 ) - 1 ) )
					{
						if (   ( $landKind == $HlandTown )
							&& ( $lv >= 60 )
							&& ( random(2) == 0 ) )
						{
							logTsunamiDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "�ﳲ�����" );
							$landValue->[$x][$y] -= random(40) + 20;
						}
						elsif (( $landKind == $HlandBase )
							&& ( $lv > 0 )
							&& ( random(3) < 2 ) )
						{
							logTsunamiDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "�ﳲ�����" );
							$landValue->[$x][$y] = random($lv) + 1;
						}
						elsif (( $landKind == $HlandFarm )
							&& ( $lv > 10 )
							&& ( random(3) < 2 ) )
						{
							logTsunamiDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "�ﳲ�����" );
							$landValue->[$x][$y] = 10;
						}
						elsif (( $landKind == $HlandFactory )
							&& ( $lv > 30 )
							&& ( random(3) < 2 ) )
						{
							logTsunamiDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "�ﳲ�����" );
							$landValue->[$x][$y] = 30;
						}
						elsif (( $landKind == $HlandPort )
							&& ( $lv > 40 )
							&& ( random(3) < 2 ) )
						{
							logTsunamiDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "�ﳲ�����" );
							$landValue->[$x][$y] = 40;
						}
						else {
							logTsunamiDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "������" );
							$land->[$x][$y]      = $HlandWaste;
							$landValue->[$x][$y] = 0;
						}
					}
				}
				elsif ( ( $landKind == $HlandSea ) && ( $lv >= 10 ) ) {
					if ( random($q) < ( seaAround( $land, $x, $y, 7, 1 ) - 1 ) )
					{
						logTsunamiDamage( $id, $name,
							landName( $landKind, $lv ),
							"($x, $y)", "������" );
						$land->[$x][$y]      = $HlandSea;
						$landValue->[$x][$y] = 1;
					}
				}
			}
		}

		# ����Ƚ��
		my ($r) = random(10000);
		$r -= 100 if ( $island->{'towerD'} );
		my ($pop) = $island->{'pop'};
		$r = 0 if ( $HpunishInfo{$id}->{punish} == 3 );
		do {
			if (
				(
					   ( $r < ( $HdisMonster * $island->{'area'} ) )
					&& ( $pop >= $HdisMonsBorder1 )
				)
				|| ( $island->{'monstersend'} + $island->{'monstersend1'} +
					$island->{'monstersend2'} + $island->{'monstersend3'} +
					$island->{'TeruteruMons'} + $island->{'monsEnsei'} > 0 )
			  )
			{

				# ���ýи�
				# ��������
				my ( $lv, $kind, $human );
				$human = 0;
				if ( $island->{'monsEnsei'} > 0 ) {

					# S�����ɸ�
					$kind                  = $island->{'monsEnsei'};
					$human                 = 1;
					$island->{'monsEnsei'} = 0;
				}
				elsif ( $island->{'monstersend'} > 0 ) {

					# ��¤
					$kind  = 0;
					$human = 1;
					$island->{'monstersend'}--;
				}
				elsif ( $island->{'monstersend1'} > 0 ) {

					# ��¤
					$kind  = 11;
					$human = 1;
					$island->{'monstersend1'}--;
				}
				elsif ( $island->{'monstersend2'} > 0 ) {

					# ��¤
					$kind  = 22;
					$human = 1;
					$island->{'monstersend2'}--;
				}
				elsif ( $island->{'monstersend3'} > 0 ) {

					# ��¤
					$kind  = 25;
					$human = 1;
					$island->{'monstersend3'}--;
				}
				elsif ( $island->{'TeruteruMons'} > 0 ) {

					# �Ƥ�Ƥ뤤�Τ�(28)��# �դ��Ƥ�Ƥ�(29)
					$kind = ( $island->{'TeruteruMons'} == 1 ) ? 28 : 29;
					$island->{'TeruteruMons'} = 0;
				}
				elsif ( $pop >= $HdisMonsBorder5 ) {

					# level5�ޤ�
					$kind = $HmonsterL5[ random($HmonsterL5Num) ];
				}
				elsif ( $pop >= $HdisMonsBorder4 ) {

					# level4�ޤ�
					$kind = $HmonsterL4[ random($HmonsterL4Num) ];
				}
				elsif ( $pop >= $HdisMonsBorder3 ) {

					# level3�ޤ�
					$kind = $HmonsterL3[ random($HmonsterL3Num) ];
				}
				elsif ( $pop >= $HdisMonsBorder2 ) {

					# level2�ޤ�
					$kind = $HmonsterL2[ random($HmonsterL2Num) ];
				}
				else {

					# level1�Τ�
					$kind = $HmonsterL1[ random($HmonsterL1Num) ];
				}

				# lv���ͤ����
				$lv = $kind * 100 + $HmonsterBHP[$kind] +
				  random( $HmonsterDHP[$kind] );

				# �ɤ��˸���뤫����
				my ( $bx, $by, $i );
				for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
					$bx = $Hrpx[$i];
					$by = $Hrpy[$i];
					if ( $kind == 25 ) {

						# ����ᥫ���Τ�

						if (   ( $land->[$bx][$by] == $HlandOil )
							&& ( $landValue->[$bx][$by] >= 35 ) )
						{
							logMonsCome(
								$id, $name,
								( monsterSpec($lv) )[1],
								"($bx, $by)",
								landName(
									$land->[$bx][$by],
									$landValue->[$bx][$by]
								)
							);
							$land->[$bx][$by]      = $HlandMonster;
							$landValue->[$bx][$by] = $lv;
							last;
						}
					}
					elsif (
						   ( $land->[$bx][$by] == $HlandTown )
						|| ( $land->[$bx][$by] == $HlandSlum )
						|| (   ( $land->[$bx][$by] == $HlandBigcity )
							&& ($HbigCityMFlg) )
						|| ( $land->[$bx][$by] == $HlandWindmill )
					  )
					{

						# ���Υإå�������ä�
						if ( $human != 1 ) {
							if ( chkAround( $land, $bx, $by, $HlandZoo, 19 ) ) {
								$i += $HislandSize * 3;
								$human = 1;
								next;
							}
						}
						logMonsCome(
							$id, $name,
							( monsterSpec($lv) )[1],
							"($bx, $by)",
							landName(
								$land->[$bx][$by],
								$landValue->[$bx][$by]
							)
						);
						$land->[$bx][$by]      = $HlandMonster;
						$landValue->[$bx][$by] = $lv;
						last;
					}
				}
				if (
					( $i >= $HpointNumber )
					&& (   ( $island->{'kaiteipop'} == 1 )
						|| ( $HearthAttack > 0 ) )
				  )
				{

# ����ο͸���Φ����¿�����˽и������Ϸ����ʤ���(�ϵ并�����)�ϡ������ߥ�������ϤˤǤ롣
					for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
						$bx = $Hrpx[$i];
						$by = $Hrpy[$i];
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandForest ) )
						{

							# ���Υإå�������ä�
							logMonsCome(
								$id, $name,
								( monsterSpec($lv) )[1],
								"($bx, $by)",
								landName(
									$land->[$bx][$by],
									$landValue->[$bx][$by]
								)
							);

							$land->[$bx][$by]      = $HlandMonster;
							$landValue->[$bx][$by] = $lv;
							last;

						}
					}
				}
			}
		  } while ( $island->{'monstersend'} + $island->{'monstersend1'} +
			$island->{'monstersend2'} + $island->{'monstersend3'} > 0 );

		# �ߥ�������ˤ�����Ƚ��(r=0-9999)
		if (   ( $r > 9969 )
			&& ( $island->{'MissileK'} >= 30 )
			&& ( $HdisMonster > 0 ) )
		{
			my ( $lv, $kind );
			if ( $r > 9994 ) {
				$kind = 17;    # ������ܥ���
			}
			elsif ( $r > 9989 ) {
				$kind = 18;    # ȿ��
			}
			elsif ( $r > 9984 ) {
				$kind = 20;    # ���ڡ���
			}
			elsif ( $r > 9979 ) {
				$kind = 21;    # ������������
			}
			elsif ( $r > 9974 ) {
				$kind = 30;    # �������Τ�
			}
			else {
				$kind = 23;    # ���ͥ���
			}
			$lv =
			  $kind * 100 + $HmonsterBHP[$kind] + random( $HmonsterDHP[$kind] );
			my ( $mKind, $mName, $mHp ) = monsterSpec($lv);

			# �ɤ��˸���뤫����
			my ( $bx, $by, $i );
			for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
				$bx = $Hrpx[$i];
				$by = $Hrpy[$i];
				if ( $kind == 21 ) {

					# ������������
					if (   ( $land->[$bx][$by] == $HlandOil )
						&& ( $landValue->[$bx][$by] >= 35 ) )
					{
						logMonsCome(
							$id, $name, $mName,
							"($bx, $by)",
							landName(
								$land->[$bx][$by],
								$landValue->[$bx][$by]
							)
						);
						$land->[$bx][$by]      = $HlandMonster;
						$landValue->[$bx][$by] = $lv;
						$r                     = 100;
						last;
					}
				}
				elsif (( $land->[$bx][$by] == $HlandTown )
					|| ( $land->[$bx][$by] == $HlandSlum )
					|| ( $land->[$bx][$by] == $HlandWindmill ) )
				{
					logMonsCome( $id, $name, $mName, "($bx, $by)",
						landName( $land->[$bx][$by], $landValue->[$bx][$by] ) );
					$land->[$bx][$by]      = $HlandMonster;
					$landValue->[$bx][$by] = $lv;
					$r                     = 100;
					last;
				}
			}
		}

		# ��������Ƚ��
		if (
			(
				   ( $HpunishInfo{$id}->{punish} == 4 )
				|| ( random(1000) < $HdisFalldown )
			)
			&& ( $island->{'area'} > $HdisFallBorder )
		  )
		{

			# ��������ȯ��
			logFalldown( $id, $name );
			my ( $x, $y, $landKind, $lv, $i );
			for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
				$x        = $Hrpx[$i];
				$y        = $Hrpy[$i];
				$landKind = $land->[$x][$y];
				$lv       = $landValue->[$x][$y];
				if (   ( $HseaChk[$landKind] == 0 )
					&& ( $landKind != $HlandMountain ) )
				{

					# ���Ϥ˳�������С��ͤ�-1��
					if ( seaAround( $land, $x, $y, 7 ) ) {
						logFalldownLand( $id, $name, landName( $landKind, $lv ),
							"($x, $y)" );
						$land->[$x][$y]      = -1;
						$landValue->[$x][$y] = 0;
					}
				}
			}
			for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
				$x        = $Hrpx[$i];
				$y        = $Hrpy[$i];
				$landKind = $land->[$x][$y];
				if ( $landKind == -1 ) {

					# -1�ˤʤäƤ�����������
					$land->[$x][$y]      = $HlandSea;
					$landValue->[$x][$y] = 1;
				}
				elsif (( $landKind == $HlandSea )
					|| ( $landKind == $HlandBreakwater ) )
				{

					# ������������ϳ���
					$land->[$x][$y]      = $HlandSea;
					$landValue->[$x][$y] = 0;
				}
			}
		}

		# ����Ƚ��
		if (   ( $HpunishInfo{$id}->{punish} == 5 )
			|| ( random(1000) < $disTyphoon ) )
		{

			# ����ȯ��
			logTyphoon( $id, $name );
			$island->{'weather'} = 59;
			my ( $x, $y, $landKind, $i );
			for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
				$x        = $Hrpx[$i];
				$y        = $Hrpy[$i];
				$landKind = $land->[$x][$y];
				if (   ( $landKind == $HlandFarm )
					|| ( $landKind == $HlandHaribote )
					|| ( $landKind == $HlandWindmill )
					|| ( $landKind == $HlandBreakwater ) )
				{

					# 1d12 <= (6 - ���Ϥο�) ������
					my ( $j, $tx, $ty );
					my $count = 6;
					for ( $j = 0 ; $j < 7 ; $j++ ) {
						$tx = $x + $ax[$j];
						$ty = $y + $ay[$j];
						$tx-- if ( !( $ty % 2 ) && ( $y % 2 ) );
						if (   ( $tx < 0 )
							|| ( $tx >= $HislandSize )
							|| ( $ty < 0 )
							|| ( $ty >= $HislandSize ) )
						{
						}
						elsif (( $land->[$tx][$ty] == $HlandMonument )
							|| ( $land->[$tx][$ty] == $HlandSMonument )
							|| ( $land->[$tx][$ty] == $HlandForest )
							|| ( $land->[$tx][$ty] == $HlandFlower )
							|| ( $land->[$tx][$ty] == $HlandWindmill )
							|| ( $land->[$tx][$ty] == $HlandPark ) )
						{
							$count--;
						}
					}
					if ( random(12) < $count ) {

						# S���ɽ𤬤���������γ�ΨȾ��
						next
						  if (
							(
								chkAroundEX(
									$land, $landValue, $x, $y, $HlandFire, 10,
									37
								)
							)
							&& ( random(2) == 0 )
						  );
						my $lv = $landValue->[$x][$y];
						if ( $landKind == $HlandBreakwater ) {
							next unless ( random(10) == 0 );
							logTyphoonDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "�˲�����" );
							$land->[$x][$y]      = $HlandSea;
							$landValue->[$x][$y] = 1;
						}
						elsif ( ( $landKind == $HlandFarm ) && ( $lv > 21 ) ) {
							logTyphoonDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "�ﳲ�����" );
							$landValue->[$x][$y] = $lv - 10;
						}
						elsif ( ( $landKind == $HlandFarm ) && ( $lv > 13 ) ) {
							logTyphoonDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "�ﳲ�����" );
							$landValue->[$x][$y] = 10;
						}
						else {
							logTyphoonDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "���Ф���" );
							$land->[$x][$y]      = $HlandPlains;
							$landValue->[$x][$y] = 0;
						}
					}
				}
				elsif (( $landKind == $HlandFishSShip )
					|| ( $landKind == $HlandFishMShip ) )
				{

					# �������淿����
					if ( random(10) == 0 ) {
						logTyphoonDamage( $id, $name,
							landName( $landKind, $lv ),
							"($x, $y)", "���ˤ�" );
						if ( random(20) == 0 ) {

							# ͩ����
							$land->[$x][$y]      = $HlandGhostShip;
							$landValue->[$x][$y] =
							  $HshipHP[ $HlandGhostShip - $HlandPirate ] * 1000;
						}
						else {
							$land->[$x][$y]       = $land2->[$x][$y];
							$landValue->[$x][$y]  = $landValue2->[$x][$y];
							$land2->[$x][$y]      = $HlandSea;
							$landValue2->[$x][$y] = 0;
						}
					}
				}
			}
		}

		# ��ĬȽ��
		if ( ( random(1000) < $disAkasio + int( $island->{'yousyoku'} / 200 ) )
			&& ( $disAkasio != 0 ) )
		{
			if ( $island->{'yousyoku'} > 0 ) {

				# ��Ĭȯ��
				logEvent( $id, $name,
					"��${HtagDisaster_}��Ĭ${H_tagDisaster}ȯ������" );
				my ( $x, $y, $landKind, $lv, $i, $p );
				for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
					$x        = $Hrpx[$i];
					$y        = $Hrpy[$i];
					$landKind = $land->[$x][$y];
					if (   ( $landKind == $HlandSea )
						&& ( $landValue->[$x][$y] >= 10 ) )
					{

					 # 1d10 <= (����2�ޥ��ι���ޤ���Į��) ������
						$p =
						  countAround( $land, $x, $y, $HlandFactory, 19 ) +
						  countAround( $land, $x, $y, $HlandTown,    19 );
						$p = ( $p * 10 ) + int( $island->{'yousyoku'} / 300 );
						if ( random(100) < $p ) {
							logAkasioDamage( $id, $name,
								landName( $landKind, 10 ),
								"($x, $y)" );
							$land->[$x][$y]      = $HlandSea;
							$landValue->[$x][$y] = 1;
						}
					}
				}
			}
		}

		my ($pirate) = 1000;
		if ( $island->{'treasure'} > 0 ) {

			# ����¸�߻�����±���и���Ψ�����ܤˤʤ�
			$pirate = 500;
		}
		else {

# ������¸�ߤ��ʤ��Ȥ������и�Ƚ�ꡢ����������ۤɤǤ䤹���ʤ롣
			if ( random(1000) < $HdisTreasureS + $island->{'titanic'} * 0.4 ) {
				my ( $x, $y ) = shipAppear( $land, random(4) );

				# �Ϸ���¸
				$land2->[$x][$y]      = $land->[$x][$y];
				$landValue2->[$x][$y] = $landValue->[$x][$y];
				$land->[$x][$y]       = $HlandTreasureS;
				$landValue->[$x][$y]  =
				  10000 + $HshipHP[ $HlandTreasureS - $HlandPirate ] * 1000;

				logShipCome( $id, $name, landName( $HlandTreasureS, 0 ),
					"($x, $y)" );
			}
		}

# ��±����ͩ��������ε�и�Ƚ�� �����������ɰʾ���ȤǤ䤹���ʤ롣
		my $fishship = $island->{'fishShip'};
		$fishship = 0 if ( $fishship < 10 );
		my $ship = random($pirate);
		do {
			if (
				( $ship < $HdisPirate + $fishship * 0.1 )
				|| ( $island->{'piratesend'} + $island->{'ghost'} +
					$island->{'wingdragon'} + $island->{'icefloe'} +
					$island->{'couplerock'} > 0 )
			  )
			{
				my ( $x, $y ) = shipAppear( $land, random(4) );

				# �Ϸ���¸
				$land2->[$x][$y]      = $land->[$x][$y];
				$landValue2->[$x][$y] = $landValue->[$x][$y];

				my ( $newship, $point );
				if ( $island->{'wingdragon'} > 0 ) {

					# ��ε
					$newship = $HlandWingDragon;
					$landValue->[$x][$y] =
					  10000 + $HshipHP[ $newship - $HlandPirate ] * 1000;
					$island->{'wingdragon'} = 0;
					$point = "($x, $y)";
				}
				elsif ( $island->{'icefloe'} > 0 ) {

					# ήɹ
					$newship = $HlandIceFloe;
					$landValue->[$x][$y] =
					  10000 + $HshipHP[ $newship - $HlandPirate ] * 1000;
					$island->{'icefloe'} = 0;
					$point = "($x, $y)";
				}
				elsif ( $island->{'couplerock'} > 0 ) {

					# ���ش�
					$newship = $HlandCoupleRock;
					$landValue->[$x][$y] =
					  10000 + $HshipHP[ $newship - $HlandPirate ] * 1000;
					$island->{'couplerock'} = 0;
					$point = "($x, $y)";
				}
				elsif ( $island->{'ghost'} > 0 ) {

					# ͩ����
					$newship = $HlandGhostShip;
					$landValue->[$x][$y] =
					  $HshipHP[ $newship - $HlandPirate ] * 1000;
					$island->{'ghost'} = 0;
					$point = "(?, ?)";
				}
				else {

					# ��±��
					$newship = $HlandPirate;
					$landValue->[$x][$y] =
					  $HshipHP[ $newship - $HlandPirate ] * 1000 +
					  $island->{'piratesend'};
					$island->{'piratesend'} = 0;
					$point = "($x, $y)";
				}
				$land->[$x][$y] = $newship;
				logShipCome( $id, $name, landName( $newship, 0 ), $point );
			}
		  } while ( $island->{'piratesend'} + $island->{'ghost'} +
			$island->{'wingdragon'} + $island->{'icefloe'} +
			$island->{'couplerock'} > 0 );

		# �������Ƚ��
		if (   ( $HpunishInfo{$id}->{punish} == 6 )
			|| ( random(1000) < $disHugeMeteo ) )
		{
			my ( $x, $y );
			if ( $HpunishInfo{$id}->{punish} == 6 ) {
				$x = $HpunishInfo{$id}->{x};
				$y = $HpunishInfo{$id}->{y};
			}
			else {
				$x = random($HislandSize);
				$y = random($HislandSize);
			}

			# S,SS�ɱһ���
			if (
				( $land->[$x][$y] != $HlandDefence )
				&& (
					chkAroundEX( $land, $landValue, $x, $y, $HlandDefence, 2,
						19 ) + chkAroundEX(
						$land, $landValue, $x, $y, $HlandDefence, 3, 19
						)
				)
			  )
			{

				# S,SS�ɱһ��ߤ��ɤ���Ƭ��ʳ���
				logMeteoD( $id, $name,
					landName( $land->[$x][$y], $landValue->[$x][$y] ),
					"($x, $y)", '�������' );
			}
			else {
				logHugeMeteo( $id, $name, "($x, $y)" );
				wideDamage( $id, $name, $land, $landValue, $x, $y, 0 );
			}
		}

		# ����ߥ�����Ƚ��
		while ( $island->{'bigmissile'} > 0 ) {
			$island->{'bigmissile'}--;
			my $x = random($HislandSize);
			my $y = random($HislandSize);
			logMonDamage( $id, $name, "($x, $y)" );

			# �����ﳲ�롼����
			wideDamage( $id, $name, $land, $landValue, $x, $y, 0 );
		}

		# ����ˡ��Ƚ��
		while ( $island->{'colony'} > 0 ) {
			$island->{'colony'}--;
			my $x = random($HislandSize);
			my $y = random($HislandSize);
			logMonDamage( $id, $name, "($x, $y)" );

			# �����ﳲ�롼����
			SuperDamage( $id, $name, $land, $landValue, $x, $y );
		}

		# ���Ƚ��
		if (   ( $HpunishInfo{$id}->{punish} == 7 )
			|| ( random(1000) < ( ( $island->{'Meteo'} + 1 ) * $disMeteo ) ) )
		{
			my ( $x, $y, $landKind, $lv, $point, $first );
			$first = 1;
			while ( ( random(2) == 0 ) || ( $first == 1 ) ) {
				$first = 0;

				# �
				$x        = random($HislandSize);
				$y        = random($HislandSize);
				$landKind = $land->[$x][$y];
				$lv       = $landValue->[$x][$y];
				$point    = "($x, $y)";

				# S,SS�ɱһ���
				if (
					( $landKind != $HlandDefence )
					&& (
						chkAroundEX( $land, $landValue, $x, $y, $HlandDefence,
							2, 19 ) + chkAroundEX(
							$land, $landValue, $x, $y, $HlandDefence, 3, 19
							)
					)
				  )
				{

					# S,SS�ɱһ��ߤ��ɤ���Ƭ��ʳ���
					logMeteoD( $id, $name, landName( $landKind, $lv ),
						$point, '���' );
					next;
				}

				# ���������ϥ����å�
				if ( $island->{'aegis'} > 4 ) {
					$island->{'aegis'} -= 5;

			#				HdebugOut("���������Ϸ޷����:" . $island->{'money'});
					if ( ( random(3) == 0 ) && ( $island->{'money'} > 500 ) ) {
						$island->{'money'} -= 500;
						logMeteoD( $id, $name, landName( $landKind, $lv ),
							$point, '���' );
						next;
					}
				}

				if ( ( $landKind == $HlandSea ) && ( $lv == 0 ) ) {

					# ���ݥ���
					logMeteoSea( $id, $name, landName( $landKind, $lv ),
						$point );
				}
				elsif ( $landKind == $HlandMountain ) {

					# ���˲�
					logMeteoMountain( $id, $name, landName( $landKind, $lv ),
						$point );
					$land->[$x][$y]      = $HlandWaste;
					$landValue->[$x][$y] = 0;
					next;
				}
				elsif ( $landKind == $HlandSbase ) {
					logMeteoSbase( $id, $name, landName( $landKind, $lv ),
						$point );
				}
				elsif ( $landKind == $HlandMonster ) {
					logMeteoMonster( $id, $name, landName( $landKind, $lv ),
						$point );
				}
				elsif (( $landKind == $HlandSea )
					|| ( $landKind == $HlandBreakwater ) )
				{

					# ������������
					logMeteoSea1( $id, $name, landName( $landKind, $lv ),
						$point );
				}
				elsif ( $landKind == $HlandWarp ) {

					# ž��
					logWarpMeteo( $id, $name, landName( $landKind, $lv ),
						$point );

					#			$land->[$x][$y] = $HlandWaste;
					#			$landValue->[$x][$y] = 0;
					my ($st) = warp( $id, $name, 0, 0, "���", $lv, 12 );
					next;
				}
				else {
					logMeteoNormal( $id, $name, landName( $landKind, $lv ),
						$point );
				}
				$land->[$x][$y]      = $HlandSea;
				$landValue->[$x][$y] = 0;
			}
		}

		# ʮ��Ƚ��
		if (
			( $HpunishInfo{$id}->{punish} == 8 )
			|| (   ( random(1000) < $disEruption )
				|| ( $island->{'AEruption'} != 0 ) )
		  )
		{
			my ( $x, $y, $sx, $sy, $landKind, $lv );
			my ($i) = 1;
			if ( $island->{'AEruption'} == 0 ) {
				if ( $HpunishInfo{$id}->{punish} == 8 ) {
					$x = $HpunishInfo{$id}->{x};
					$y = $HpunishInfo{$id}->{y};
				}
				else {
					$x = random($HislandSize);
					$y = random($HislandSize);
				}
				if ( chkAround( $land, $x, $y, $HlandSchool, 7 ) ) {
					$i = 10;
				}
				logEruption( $id, $name,
					landName( $land->[$x][$y], $landValue->[$x][$y] ),
					"($x, $y)", "ʮ��" );
			}
			else {
				$x = $island->{'AEruptionX'};
				$y = $island->{'AEruptionY'};
				logEruption( $id, $name,
					landName( $land->[$x][$y], $landValue->[$x][$y] ),
					"($x, $y)", "��ʮ��" );
			}
			$land->[$x][$y]      = $HlandMountain;
			$landValue->[$x][$y] = 0;
			for ( ; $i < 7 ; $i++ ) {
				$sx = $x + $ax[$i];
				$sy = $y + $ay[$i];
				$sx--
				  if ( !( $sy % 2 ) && ( $y % 2 ) );  # �Ԥˤ�����Ĵ��
				$landKind = $land->[$sx][$sy];
				$lv       = $landValue->[$sx][$sy];
				if (   ( $sx < 0 )
					|| ( $sx >= $HislandSize )
					|| ( $sy < 0 )
					|| ( $sy >= $HislandSize ) )
				{
				}
				else {

					# �ϰ���ξ��
					$landKind = $land->[$sx][$sy];
					$lv       = $landValue->[$sx][$sy];
					if ( $HseaChk[$landKind] ) {

						# ���ξ��
						if (   ( ( $landKind == $HlandSea ) && ( $lv >= 1 ) )
							|| ( $landKind == $HlandBreakwater ) )
						{

							# ������������
							logEruptionSea1( $id, $name,
								landName( $landKind, $lv ),
								"($sx, $sy)" );
						}
						else {
							logEruptionSea( $id, $name,
								landName( $landKind, $lv ),
								"($sx, $sy)" );
							$land->[$sx][$sy]      = $HlandSea;
							$landValue->[$sx][$sy] = 1;
							next;
						}
					}
					elsif (( $landKind == $HlandMountain )
						|| ( $landKind == $HlandMonster )
						|| ( ( $landKind == $HlandWaste ) && ( $lv == 1 ) ) )
					{
						next;
					}
					else {

						# ����ʳ��ξ��
						logEruptionNormal( $id, $name,
							landName( $landKind, $lv ),
							"($sx, $sy)" );
					}
					$land->[$sx][$sy]      = $HlandWaste;
					$landValue->[$sx][$sy] = 0;
				}
			}
		}

	}    #SSSystem

	# ���åХȥ�

	# �����Ǥμ��Ф�
	my ($monster) = $island->{'monster'};
	my (
		$MBid,  $MBname, $MBtId, $MBsId, $MBmId,  $MBhp,  $MBmhp,
		$MBstr, $MBdef,  $MBagi, $MBskl, $MBwinh, $MBwin, $MBlose
	  )
	  = (
		$monster->[0],  $monster->[1], $monster->[2],  $monster->[3],
		$monster->[4],  $monster->[5], $monster->[6],  $monster->[7],
		$monster->[8],  $monster->[9], $monster->[10], $monster->[11],
		$monster->[12], $monster->[13]
	  );

	my ($tn) = $HidToNumber{$MBtId};
	my ($tMonster);
	my ($tIsland);
	my ($tName);
	my (
		$tMBid,  $tMBname, $tMBtId, $tMBsId, $tMBmId,  $tMBhp,  $tMBmhp,
		$tMBstr, $tMBdef,  $tMBagi, $tMBskl, $tMBwinh, $tMBwin, $tMBlose
	);

	if ( $island->{'esa'} > 0 ) {

		# ���ñ¼����ե饰��Ω�äƤ���

		$MBsId = $island->{'esa'};
		logMonsESA( $id, $name, $HmonsterName[$MBsId] );
	}

	if ( $MBid == 0 ) {

		# ��ʬ�β��ä����ʤ�
	}
	elsif ( $id != $MBid ) {

		# ������

		if ( $tn eq '' ) {
			$MBid = $id
			  ; # ��꤬���ʤ��ʤä��Τǲ��ä�ʬ������᤹��
			$MBhp  = $MBmhp;
			$MBtId = 0;
		}
	}
	elsif ( $tn eq '' ) {
		$MBid = $id; # ��꤬���ʤ��Τǲ��ä�ʬ������᤹��
		$MBhp  = $MBmhp;
		$MBtId = 0;
	}
	else {

		# ������꤬����Ȥ�
		$tIsland  = $Hislands[$tn];
		$tName    = $tIsland->{'name'};
		$tMonster = $tIsland->{'monster'};
		(
			$tMBid,  $tMBname, $tMBtId, $tMBsId, $tMBmId,  $tMBhp,  $tMBmhp,
			$tMBstr, $tMBdef,  $tMBagi, $tMBskl, $tMBwinh, $tMBwin, $tMBlose
		  )
		  = (
			$tMonster->[0],  $tMonster->[1],  $tMonster->[2],
			$tMonster->[3],  $tMonster->[4],  $tMonster->[5],
			$tMonster->[6],  $tMonster->[7],  $tMonster->[8],
			$tMonster->[9],  $tMonster->[10], $tMonster->[11],
			$tMonster->[12], $tMonster->[13]
		  );

		# ��Ʈ�롼����

		my ( $mId, $tmId );    # ��󥹥���ID
		if ( $MBmId == 19 ) {  # �������λ�
			$mId = random(25);
		}
		else {
			$mId = $MBmId;
		}
		if ( $tMBmId == 19 ) {    # �������λ�
			$tmId = random(25);
		}
		else {
			$tmId = $tMBmId;
		}

		my ( $speed,  $mei,  $kai,  $damage,  $sp,  $spskl );
		my ( $tspeed, $tmei, $tkai, $tdamage, $tsp, $tspskl );

		$speed  = $HmonsterAGI[$mId] + $MBagi + random(30);
		$mei    = $HmonsterSKL[$mId] + $MBskl + random(30);
		$kai    = $HmonsterAGI[$mId] + $MBagi + random(15);
		$damage =
		  ( $HmonsterSTR[$mId] + $MBstr + random(12) ) -
		  ( $HmonsterDEF[$tmId] + $tMBdef + random(5) );
		$damage = 0 if ( $damage < 0 );
		$sp     = $HmonsterSP[$mId];
		$spskl  = $MBagi + $MBskl;

		# �ü�ǽ�Ϥ�ȯư���뤫
		my ($ran100) = random(100);
		if ( $spskl + 20 > $ran100 ) {
			$spskl = 3;
		}
		elsif ( $spskl + 25 > $ran100 ) {
			$spskl = 2;
		}
		elsif ( $spskl + 40 > $ran100 ) {
			$spskl = 1;
		}
		else {
			$spskl = 0;
		}

		$tspeed  = $HmonsterAGI[$tmId] + $tMBagi + random(30);
		$tmei    = $HmonsterSKL[$tmId] + $tMBskl + random(30);
		$tkai    = $HmonsterAGI[$tmId] + $tMBagi + random(15);
		$tdamage =
		  ( $HmonsterSTR[$tmId] + $tMBstr + random(12) ) -
		  ( $HmonsterDEF[$mId] + $MBdef + random(5) );
		$tdamage = 0 if ( $tdamage < 0 );
		$tsp     = $HmonsterSP[$tmId];
		$tspskl  = $tMBagi + $tMBskl;

		# �ü�ǽ�Ϥ�ȯư���뤫
		$ran100 = random(100);
		if ( $tspskl + 20 > $ran100 ) {
			$tspskl = 3;
		}
		elsif ( $tspskl + 25 > $ran100 ) {
			$tspskl = 2;
		}
		elsif ( $tspskl + 40 > $ran100 ) {
			$tspskl = 1;
		}
		else {
			$tspskl = 0;
		}

		if ( ( $sp == 10 ) || ( $tsp == 10 ) ) {

		 # �Ұ����Ǥ������ü�ǽ��̵�������äƤ����硣
			$sp  = 0;
			$tsp = 0;
		}

		my ( $first, $end ) = ( 1, 3 );
		if ( $speed == $tspeed ) {

			# ξ��ư���ʤ��ä���
			logMonsNOATTACK( $MBtId, $tName, $tMBname, $id, $name, $MBname );
			$first = 3;
		}
		elsif ( $speed > $tspeed ) {

			# ��ʬ�β�����������

			$first = 0;
			$end   = 2;
		}
		else {

			# ������������

		}
		my ($special)  = $HmonsterSpecial[$mId];
		my ($special2) = $HmonsterSpecial[$tmId];

		my ($BattleEnd) = 0;

		while ( $first < $end ) {
			if ( $first == 1 ) {

				# ���ι���

				if (   ( ( $tsp == 1 ) && ( ( $HislandTurn % 2 ) == 0 ) )
					|| ( ( $tsp == 2 ) && ( ( $HislandTurn % 2 ) == 1 ) ) )
				{

					# �Ų���ǹ��⤷�ʤ�
					$first++;
					next;
				}
				if ( $tmei > $kai ) {

					# ���ι��⤬�����ä�
					if ( ( $sp == 5 ) && ( $spskl >= 2 ) ) {

						# �ü�ǽ�Ϥ��򤱤�
						logMonsATTACK(
							$MBtId,
							$tName,
							$tMBname,
							$id,
							$name,
							$MBname,
"�̾ﹶ�⡢�������褱���Ƥ��ޤä���"
						);
					}
					elsif ( ( $sp == 6 ) && ( $spskl >= 1 ) ) {

						# �ü�ǽ�Ϥ��ɸ椷��
						logMonsATTACK(
							$MBtId,
							$tName,
							$tMBname,
							$id,
							$name,
							$MBname,
"�̾ﹶ�⡢���������᡼���򤢤������ʤ���"
						);
					}
					elsif (
						(
							   ( ( $sp == 1 ) && ( ( $HislandTurn % 2 ) == 0 ) )
							|| ( ( $sp == 2 ) && ( ( $HislandTurn % 2 ) == 1 ) )
						)
						&& ( ( $tsp != 1 ) && ( $tsp != 2 ) )
					  )
					{

# �Ų���ǥ��᡼���򤯤��ʤ������������󥸥�ȥ�����Ͻ���
						logMonsATTACK(
							$MBtId,
							$tName,
							$tMBname,
							$id,
							$name,
							$MBname,
"�̾ﹶ�⡢���������᡼���򤢤������ʤ���"
						);
					}
					elsif ( ( $tsp == 8 ) && ( $tMBhp <= 10 ) ) {

						# ��������

						if ( random(2) == 0 ) {
							$tdamage = 100;
							$MBhp    = $MBhp - $tdamage;
							logMonsATTACK(
								$MBtId,
								$tName,
								$tMBname,
								$id,
								$name,
								$MBname,
"�������⡢${tdamage}�Υ��᡼���򤢤�������"
							);
						}
						else {
							logMonsATTACK(
								$MBtId,
								$tName,
								$tMBname,
								$id,
								$name,
								$MBname,
"�������⡢�������褱���Ƥ��ޤä���"
							);
							logMonsEND( $MBtId, $tName, $tMBname, $MBtId,
								"���Ǥ��ޤ�����" );
							logMonsEND( $id, $name, $MBname, $MBtId,
								"�襤�˾������ޤ�����" );

							$BattleEnd = 1;
							last;
						}
					}
					elsif ( ( $tsp == 7 ) && ( $tspskl >= 2 ) ) {

						# ɬ������

						$tdamage = $tdamage * 2;
						$MBhp    = $MBhp - $tdamage;
						logMonsATTACK(
							$MBtId,
							$tName,
							$tMBname,
							$id,
							$name,
							$MBname,
"ɬ���ΰ�⡢${tdamage}�Υ��᡼���򤢤�������"
						);
					}
					elsif ( ( $tsp == 9 ) && ( $tspskl >= 3 ) ) {

						# ����
						$tdamage = $tdamage * 3;
						$MBhp    = $MBhp - $tdamage;
						logMonsATTACK(
							$MBtId,
							$tName,
							$tMBname,
							$id,
							$name,
							$MBname,
"ɬ��������ȯư��${tdamage}�Υ��᡼���򤢤�������"
						);
					}
					else {

						# �̾ﹶ��

						$MBhp = $MBhp - $tdamage;
						logMonsATTACK(
							$MBtId,
							$tName,
							$tMBname,
							$id,
							$name,
							$MBname,
"�̾ﹶ�⡢${tdamage}�Υ��᡼���򤢤�������"
						);
					}
					if ( $MBhp < 1 ) {

						# �ޤ��Ƥ��ޤä���
						logMonsEND( $MBtId, $tName, $tMBname, $id,
							"�襤�˾������ޤ�����" );

						$BattleEnd = 2;
						last;
					}
				}
				else {

					# ���ι����褱��
					logMonsATTACK(
						$MBtId,
						$tName,
						$tMBname,
						$id,
						$name,
						$MBname,
						"�̾ﹶ�⡢�������褱���Ƥ��ޤä���"
					);
				}
			}
			else {

				# ��ʬ�ι���

				if (   ( ( $sp == 1 ) && ( ( $HislandTurn % 2 ) == 0 ) )
					|| ( ( $sp == 2 ) && ( ( $HislandTurn % 2 ) == 1 ) ) )
				{

					# �Ų���ǹ��⤷�ʤ�
					$first++;
					next;
				}
				if ( $mei > $tkai ) {

					# ��ʬ�ι��⤬�����ä�
					if ( ( $tsp == 5 ) && ( $tspskl >= 2 ) ) {

						# �ü�ǽ�Ϥ��򤱤�
						logMonsATTACK(
							$id,
							$name,
							$MBname,
							$MBtId,
							$tName,
							$tMBname,
"�̾ﹶ�⡢�������褱���Ƥ��ޤä���"
						);
					}
					elsif ( ( $tsp == 6 ) && ( $tspskl >= 1 ) ) {

						# �ü�ǽ�Ϥ��ɸ椷��
						logMonsATTACK(
							$id,
							$name,
							$MBname,
							$MBtId,
							$tName,
							$tMBname,
"�̾ﹶ�⡢���������᡼���򤢤������ʤ���"
						);
					}
					elsif (
						(
							( ( $tsp == 1 ) && ( ( $HislandTurn % 2 ) == 0 ) )
							|| (   ( $tsp == 2 )
								&& ( ( $HislandTurn % 2 ) == 1 ) )
						)
						&& ( ( $sp != 1 ) && ( $sp != 2 ) )
					  )
					{

# �Ų���ǥ��᡼���򤯤��ʤ������������󥸥�ȥ�����Ͻ���
						logMonsATTACK(
							$id,
							$name,
							$MBname,
							$MBtId,
							$tName,
							$tMBname,
"�̾ﹶ�⡢���������᡼���򤢤������ʤ���"
						);
					}
					elsif ( ( $sp == 8 ) && ( $MBhp <= 10 ) ) {

						# ��������

						if ( random(2) == 0 ) {
							$damage = 100;
							$tMBhp  = $tMBhp - $damage;
							logMonsATTACK(
								$id,
								$name,
								$MBname,
								$MBtId,
								$tName,
								$tMBname,
"�������⡢${damage}�Υ��᡼���򤢤�������"
							);
						}
						else {
							logMonsATTACK(
								$id,
								$name,
								$MBname,
								$MBtId,
								$tName,
								$tMBname,
"�������⡢�������褱���Ƥ��ޤä���"
							);
							logMonsEND( $id, $name, $MBname, $MBtId,
								"���Ǥ��ޤ�����" );
							logMonsEND( $id, $tName, $tMBname, $MBtId,
								"�襤�˾������ޤ�����" );

							$BattleEnd = 2;
							last;
						}
					}
					elsif ( ( $sp == 7 ) && ( $spskl >= 2 ) ) {

						# ɬ������

						$damage = $damage * 2;
						$tMBhp  = $tMBhp - $damage;
						logMonsATTACK(
							$id,
							$name,
							$MBname,
							$MBtId,
							$tName,
							$tMBname,
"ɬ���ΰ�⡢${damage}�Υ��᡼���򤢤�������"
						);
					}
					elsif ( ( $sp == 9 ) && ( $spskl >= 3 ) ) {

						# ����
						$damage = $damage * 3;
						$tMBhp  = $tMBhp - $damage;
						logMonsATTACK(
							$id,
							$name,
							$MBname,
							$MBtId,
							$tName,
							$tMBname,
"ɬ��������ȯư��${damage}�Υ��᡼���򤢤�������"
						);
					}
					else {

						# �̾ﹶ��

						$tMBhp = $tMBhp - $damage;
						logMonsATTACK(
							$id,
							$name,
							$MBname,
							$MBtId,
							$tName,
							$tMBname,
"�̾ﹶ�⡢${damage}�Υ��᡼���򤢤�������"
						);
					}
					if ( $tMBhp < 1 ) {

						# �ޤ��Ƥ��ޤä���
						logMonsEND( $id, $name, $MBname, $MBtId,
							"�襤�˾������ޤ�����" );

						$BattleEnd = 1;
						last;
					}
				}
				else {

					# ��ʬ�ι���褱��줿
					logMonsATTACK(
						$id,
						$name,
						$MBname,
						$MBtId,
						$tName,
						$tMBname,
						"�̾ﹶ�⡢�������褱���Ƥ��ޤä���"
					);
				}
			}
			$first++;
		}

		if ( $BattleEnd > 0 ) {

			# ��Ʈ��λ������Ʈ��ν���
			my (@up)  = ( 3, 3, 0, 3, 3 );
			my (@tup) = ( 3, 3, 0, 3, 3 );

			if ( $BattleEnd == 1 ) {
				if ( ( $tsp == 3 ) && ( random(3) == 0 ) ) {

					# �餱�����ˣ�����ǥ��Х��쥤�˿ʲ�
					$tMBmId = 15;
					logMonsEND( $MBtId, $tName, $tMBname, $id,
"��ˤ��줺�˥��Х��쥤�Ȥʤä�ž�����ޤ�����"
					);
				}
				@up = MonsterSei( 1, @up );    #��ĹΨ�û�

				$MBwinh++;                     # ��������
				$MBwin++;
				$tMBlose++;
				if ( $Htournament == 2 ) {
					my ($achive) = refugees( 500, $island );
					if ( $achive > 0 ) {
						logMsBoatPeople( $id, $name, $achive );
					}
				}
			}
			else {
				if ( ( $sp == 3 ) && ( random(3) == 0 ) ) {

					# �餱�����ˣ�����ǥ��Х��쥤�˿ʲ�
					$MBmId = 15;
					logMonsEND( $id, $name, $MBname, $MBtId,
"��ˤ��줺�˥��Х��쥤�Ȥʤä�ž�����ޤ�����"
					);
				}
				@tup = MonsterSei( 1, @tup );    #��ĹΨ�û�

				$tMBwinh++;                      # ��������
				$tMBwin++;
				$MBlose++;
				if ( $Htournament == 2 ) {
					my ($achive) = refugees( 500, $tIsland );
					if ( $achive > 0 ) {
						logMsBoatPeople( $MBtId, $tName, $achive );
					}
				}
			}

			@up  = MonsterSei( $HmonsterSEI[$mId],  @up );     #��ĹΨ�û�
			@tup = MonsterSei( $HmonsterSEI[$tmId], @tup );    #��ĹΨ�û�

			$MBmhp = $MBmhp + random( $up[0] - 1 );
			$MBmhp = $HmonsBtlMaxHp if ( $MBmhp > $HmonsBtlMaxHp );
			if ( ( $MBstr + $MBdef + $MBagi + $MBskl ) < $HmonsBtlMaxPa ) {
				$MBstr++ if ( random( $up[1] ) > 1 );
				$MBdef++ if ( random( $up[2] ) > 0 );
				$MBagi++ if ( random( $up[3] ) > 1 );
				$MBskl++ if ( random( $up[4] ) > 1 );
			}

			$tMBmhp = $tMBmhp + random( $tup[0] - 1 );
			$tMBmhp = $HmonsBtlMaxHp if ( $tMBmhp > $HmonsBtlMaxHp );
			if ( ( $tMBstr + $tMBdef + $tMBagi + $tMBskl ) < $HmonsBtlMaxPa ) {
				$tMBstr++ if ( random( $tup[1] ) > 1 );
				$tMBdef++ if ( random( $tup[2] ) > 0 );
				$tMBagi++ if ( random( $tup[3] ) > 1 );
				$tMBskl++ if ( random( $tup[4] ) > 1 );
			}

			$MBhp   = $MBmhp;
			$tMBhp  = $tMBmhp;
			$MBid   = $id;
			$tMBid  = $MBtId;
			$MBtId  = 0;
			$tMBtId = 0;
		}
		else {

			# ��³��

			my ($point) = 5;
			if ( $sp == 11 ) {

				# ����

				$MBhp = $MBhp + $point;
				if ( $MBhp > $MBmhp ) {
					$point -= $MBhp - $MBmhp;
					$MBhp = $MBmhp;
				}
				logMonsRrcovery( $id, $name, $MBname, $MBtId, $point );
			}
			elsif ( $tsp == 11 ) {

				# ����

				$tMBhp = $tMBhp + $point;
				if ( $tMBhp > $tMBmhp ) {
					$point -= $tMBhp - $tMBmhp;
					$tMBhp = $tMBmhp;
				}
				logMonsRrcovery( $MBtId, $tName, $tMBname, $id, $point );
			}
		}
	}

	# ���������оݥ�������ä��顢���ν���
	if ( ( $HislandTurn % $HturnPrizeUnit ) == 0 ) {
		if ( $MonsBattleTurn < $MBwinh ) {
			$MonsBattleTurn   = $MBwinh;
			$MonsBattleTurnID = $id;
		}
		$MBwinh = 0;
	}

	# �����ǳ�Ǽ
	my (@wmonster) = (
		$MBid,  $MBname, $MBtId, $MBsId, $MBmId,  $MBhp,  $MBmhp,
		$MBstr, $MBdef,  $MBagi, $MBskl, $MBwinh, $MBwin, $MBlose
	);
	$island->{'monster'} = \@wmonster;
	if ( $id != $target ) {
		my (@wtMonster) = (
			$tMBid,  $tMBname, $tMBtId, $tMBsId, $tMBmId,  $tMBhp,  $tMBmhp,
			$tMBstr, $tMBdef,  $tMBagi, $tMBskl, $tMBwinh, $tMBwin, $tMBlose
		);
		$tIsland->{'monster'} = \@wtMonster;
	}

	if ( $island->{'GoldMonument'} > 0 ) {
		logGoldMonu( $id, $name, $HmonumentName[9],
			int( $island->{'GoldMonument'} ) * 300 );
	}

	# �Ƽ���ͤ�׻�
	estimateE($number);

}    # doIslandProcess

# ��̩���˼��٤�ɽ��
sub doIslandProcess2 {
	my ($island) = @_;
	if ( $island->{'id'} > 90 ) {

		# Battle Field�ΤȤ�
		return;
	}
	my ( $name, $id, $moriw, $kaiteiw, $MiH ) = (
		$island->{'name'},   $island->{'id'}, $island->{'forest'},
		$island->{'kaitei'}, $island->{'MissileK'}
	);
	my ( $po, $mo, $fo );
	$po = $island->{'pop'} - $island->{'oldPop'};
	$mo = $island->{'money'} - $island->{'oldmoney'};
	$fo = $island->{'food'} - $island->{'oldfood'};

	# ���Ф����դ�Ƥ��鴹��
	if ( $island->{'ore'} > $MaxSigen ) {
		$island->{'money'} += ( $island->{'ore'} - $MaxSigen );
		$island->{'ore'} = $MaxSigen;
	}

	# ���������դ�Ƥ��鴹��
	if ( $island->{'oil'} > $MaxSigen ) {
		$island->{'money'} += ( $island->{'oil'} - $MaxSigen ) * 2;
		$island->{'oil'} = $MaxSigen;
	}

	# ʼ�郎���դ�Ƥ��鴹��
	if ( $island->{'weapon'} > $MaxSigen ) {
		$island->{'money'} += ( $island->{'weapon'} - $MaxSigen ) * 6;
		$island->{'weapon'} = $MaxSigen;
	}

	# ���������դ�Ƥ��鴹��
	if ( $island->{'food'} > $MaxFood ) {
		$island->{'money'} += int( ( $island->{'food'} - $MaxFood ) / 10 );
		$island->{'food'} = $MaxFood;
	}

	# �⤬���դ�Ƥ����ڤ�Τ�
	if ( $island->{'money'} > $MaxMoney ) {
		$island->{'money'} = $MaxMoney;
	}
	elsif ( $island->{'money'} < 0 ) {
		$island->{'money'} = 0;
	}

	my ( $iken, $iken2, $iken3 ) =
	  ( "", "", "(�����${kaiteiw}��${moriw}��)" );
	if ( ( $island->{'forest'} < 5 ) && ( random(5) == 0 ) ) {
		$iken = "�����ݸ����Τ������ݸ����Ƥ��ޤ���";
	}
	elsif ( ( $island->{'forest'} < 4 ) && ( random(3) == 0 ) ) {
		$iken =
"�����ݸ����Τ����Ӥ���ȹ��ĥǥ��ԤäƤ��ޤ���";
	}
	elsif ( $island->{'kaitei'} > $HdisKLimit ) {
		$iken =
"����Ϥη�¤ʪ��¿�����ޤ����������Τ餬�Ф뤫�⤷��ޤ���";
	}
	if ( $island->{'area'} > $HdisFallBorder ) {
		$iken2 = "Φ�����Ѥ��³��ͤ�Ķ���Ƥ��ޤ���";
	}
	elsif ( $island->{'towerD'} > 1000 ) {
		$iken2 = "�����Ϥ�¿�����ޤ���";
	}
	elsif ( $island->{'towerD'} > 0 ) {
		$iken2 = "��̱�����ȥӥ����˾���Ƥޤ���";
	}
	elsif ( ( $island->{'kaiteipop'} == 1 ) && ( $island->{'area'} > 0 ) ) {
		$iken2 =
"����͸����Ǥ��������ߥ�������Ϥ˲��ä��Ǥ뤫���Τ�ޤ���";
	}
	$moriw = 0 if ( $island->{'area'} == 0 );    # Φ��̵����

	if ( $po > 0 ) {
		$po = "${po}${HunitPop}";
	}
	elsif ( $po == 0 ) {
		$po = "����̵��";
	}
	else {

		# �ޥ��ʥ�
		$island->{'score'} += -$po;
		$po = "${HtagDisaster_}${po}${HunitPop}${H_tagDisaster}";
	}
	if ( $mo > 0 ) {
		$mo = "${mo}${HunitMoney}";
	}
	elsif ( $mo == 0 ) {
		$mo = "����̵��";
	}
	else {
		$mo = "${HtagDisaster_}${mo}${HunitMoney}${H_tagDisaster}";
	}
	if ( $fo > 0 ) {
		$fo = "${fo}${HunitFood}";
	}
	elsif ( $fo == 0 ) {
		$fo = "����̵��";
	}
	else {
		$fo = "${HtagDisaster_}${fo}${HunitFood}${H_tagDisaster}";
	}
	my $wname = ( weatherinfo( $island->{'weather2'} ) )[1];

	# ���٤ε�̩��
	push( @HsecretLogPool,
"1,$HislandTurn,$id,,�͸�<B>$po</B>�����<B>$mo</B>������<B>$fo</B>����������ŷ����<B>$wname</B>��${HtagDisaster_}${iken}${iken2}${H_tagDisaster}$iken3"
	);

	# ������оݥ�������ä����������롣
	if ( ( $HislandTurn % $HturnPrizeVarious ) == 0 ) {
		$island->{'status'} = 0;
		$island->{'score2'} = $island->{'score'};
		$island->{'score'}  = 0;
	}

	# �˱ɡ������
	$pop = $island->{'pop'};
	my ($damage) = $island->{'oldPop'} - $pop;
	my ($prize)  = $island->{'prize'};
	$prize =~ /([0-9]*),([0-9]*),(.*)/;
	my ( $flags, $monsters, $turns ) = ( $1, $2, $3 );

	# �˱ɾ�
	if ( ( !( $flags & 1 ) ) && $pop >= 3000 ) {
		$flags |= 1;
		logPrize( $id, $name, $Hprize[1] );
		$island->{'present'}->[9]++;    # ������������䤹
		logEvent( $id, $name,
"�ǣ�������ã����ǰ�������񤬳��Ť���뤳�Ȥ����ꤷ�ޤ�����"
		);
	}
	elsif ( ( !( $flags & 2 ) ) && $pop >= 5000 ) {
		$flags |= 2;
		logPrize( $id, $name, $Hprize[2] );
		$island->{'present'}->[9]++;    # ������������䤹
		logEvent( $id, $name,
"�ǣ�������ã����ǰ�������񤬳��Ť���뤳�Ȥ����ꤷ�ޤ�����"
		);
	}
	elsif ( ( !( $flags & 4 ) ) && $pop >= 10000 ) {
		$flags |= 4;
		logPrize( $id, $name, $Hprize[3] );
		$island->{'present'}->[9]++;    # ������������䤹
		logEvent( $id, $name,
"�ǣ���������ã����ǰ�������񤬳��Ť���뤳�Ȥ����ꤷ�ޤ�����"
		);
	}
	elsif ( ( !( $flags & 1024 ) ) && $pop >= 15000 ) {
		$flags |= 1024;
		$island->{'present'}->[9]++;    # ������������䤹
		logEvent( $id, $name,
"�ǣ���������ã����ǰ�������񤬳��Ť���뤳�Ȥ����ꤷ�ޤ�����"
		);
	}

	# �����
	if ( ( !( $flags & 64 ) ) && $damage >= 500 ) {
		$flags |= 64;
		logPrize( $id, $name, $Hprize[7] );
	}
	elsif ( ( !( $flags & 128 ) ) && $damage >= 1000 ) {
		$flags |= 128;
		logPrize( $id, $name, $Hprize[8] );
	}
	elsif ( ( !( $flags & 256 ) ) && $damage >= 2000 ) {
		$flags |= 256;
		logPrize( $id, $name, $Hprize[9] );
	}

	# ����ޤΥ�
	logPrize( $id, $name, $Hprize[10] ) if ( $island->{'space'} == 1 );

	# �����Υ�
	logGiveup( $id, $name ) if ( $island->{'giveup'} == 1 );

	$island->{'prize'} = "$flags,$monsters,$turns";
}    # doIslandProcess2

# ���Ϥ�Į�����줬���뤫Ƚ��
sub countGrow {
	my ( $land, $landValue, $x, $y ) = @_;
	my ( $i, $sx, $sy );
	for ( $i = 1 ; $i < 7 ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # �Ԥˤ�����Ĵ��
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{
		}
		elsif (( $land->[$sx][$sy] == $HlandTown )
			|| ( $land->[$sx][$sy] == $HlandFarm )
			|| ( $land->[$sx][$sy] == $HlandSFarm )
			|| ( $land->[$sx][$sy] == $HlandMegaFarm )
			|| ( $land->[$sx][$sy] == $HlandMegacity )
			|| ( $land->[$sx][$sy] == $HlandHugecity ) )
		{
			return 1 if ( $landValue->[$sx][$sy] != 1 );
		}
	}
	return 0;
}

# ���ۤ��Τ��ư���ޤ��Ͼõ
sub kinoraMove {
	my ( $island, $x, $y ) = @_;
	my ( $land, $landValue ) = ( $island->{'land'}, $island->{'landValue'} );
	my ( $i, $sx, $sy );
	for ( $i = 1 ; $i < 7 ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # �Ԥˤ�����Ĵ��
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{
		}
		elsif ( $land->[$sx][$sy] == $HlandKInora ) {
			last
			  if ( ( bigMonsterSpec( $landValue->[$sx][$sy] ) )[3] == 0 )
			  ;                                     # �濴�����ä��Ȥ�
		}
	}
	my ( $ld, $d ) = ( bigMonsterSpec( $landValue->[$x][$y] ) )[ 2, 3 ];
	if ( ( $d == 0 ) && ( $landValue->[$x][$y] > 0 ) ) {

# ��ư
#	HdebugOut("���ۤ��Τ飱($x,$y):" . $island->{'name'} . "�硧" . $landValue->[$x][$y]);
		return if ( $monsterMove[$x][$y] == 2 );
		( $sx, $sy ) = monmove( $island, $x, $y, 0 );
		$monsterMove[$sx][$sy] = 2;
	}
	elsif ( ( $i > 6 ) || ( $landValue->[$x][$y] == 0 ) ) {

		# �ä���

		if ( $ld == 0 ) {
			$land->[$x][$y]      = $HlandSea;
			$landValue->[$x][$y] = 0;
		}
		elsif ( $ld == 1 ) {
			$land->[$x][$y]      = $HlandSea;
			$landValue->[$x][$y] = 1;
		}
		else {
			$land->[$x][$y]      = $HlandWaste;
			$landValue->[$x][$y] = 0;

		}
	}
}

# ���ۤ��Τ����
sub kinoraMake {
	my ( $land, $landValue, $x, $y ) = @_;
	my ( $i, $sx, $sy );
	for ( $i = 1 ; $i < 7 ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{
		}
		else {
			if ( $land->[$sx][$sy] == $HlandKInora ) {
				my ( $ld, $d ) =
				  ( bigMonsterSpec( $landValue->[$x][$y] ) )[ 2, 3 ];
				$landValue->[$sx][$sy] = $ld * 10 + $d;
			}
			elsif ( $HseaChk[ $land->[$sx][$sy] ] ) {
				if (   ( $land->[$sx][$sy] == $HlandSea )
					&& ( $landValue->[$sx][$sy] > 0 ) )
				{
					$landValue->[$sx][$sy] = $i + 10;
				}
				else {
					$landValue->[$sx][$sy] = $i;
				}
			}
			else {
				$landValue->[$sx][$sy] = $i + 20;
			}
			$land->[$sx][$sy] = $HlandKInora;
		}
	}
}

# ���ۤ��Τ�õ�
sub kinoraDel {
	my ( $land, $landValue, $x, $y ) = @_;
	my ( $i, $sx, $sy );
	for ( $i = 0 ; $i < 7 ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{
		}
		else {
			my ($ld) = ( bigMonsterSpec( $landValue->[$sx][$sy] ) )[2];
			if ( $ld == 0 ) {
				$land->[$sx][$sy]      = $HlandSea;
				$landValue->[$sx][$sy] = 0;
			}
			elsif ( $ld == 1 ) {
				$land->[$sx][$sy]      = $HlandSea;
				$landValue->[$sx][$sy] = 1;
			}
			else {
				$land->[$sx][$sy]      = $HlandWaste;
				$landValue->[$sx][$sy] = 0;
			}
		}
	}
}

# ¿�Ѥ����countAround�Ͻ�����ǽ�̤�ʬ�̤�����ٷڸ�
# �ϰ�����Ϸ�������å�����
sub chkAround {
	my ( $land, $x, $y, $kind, $range ) = @_;
	my ( $i, $sx, $sy );
	for ( $i = 0 ; $i < $range ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # �Ԥˤ�����Ĵ��
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{

			# �ϰϳ��ξ�� ���ʤ�1
			return 1 if ( $kind == $HlandSea );
		}
		elsif ( $land->[$sx][$sy] == $kind ) {
			return 1;
		}
	}
	return 0;
}

# �ϰ�����Ϸ�������å����� $lv==0�λ���chkAround��Ȥ��褦��
sub chkAroundEX {
	my ( $land, $landValue, $x, $y, $kind, $lv, $range ) = @_;
	my ( $i, $sx, $sy );
	for ( $i = 0 ; $i < $range ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # �Ԥˤ�����Ĵ��
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{

			# �ϰϳ��ξ�� ���ʤ�û�
			return 1 if ( $kind == $HlandSea );
		}
		elsif ( $lv < 10 ) {
			return 1
			  if ( ( $land->[$sx][$sy] == $kind )
				&& ( $landValue->[$sx][$sy] == $lv ) );
		}
		elsif (( $land->[$sx][$sy] == $kind )
			&& ( $landValue->[$sx][$sy] >= $lv ) )
		{
			return 1;
		}
	}
	return 0;
}

# �ϰ�����Ϸ��������

sub countAround {
	my ( $land, $x, $y, $kind, $range ) = @_;
	my ( $i, $sx, $sy );
	my $count = 0;
	for ( $i = 0 ; $i < $range ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # �Ԥˤ�����Ĵ��
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{

			# �ϰϳ��ξ�� ���ʤ�û�
			$count++ if ( $kind == $HlandSea );
		}
		elsif ( $land->[$sx][$sy] == $kind ) {
			$count++;
		}
	}
	return $count;
}

# �ϰ�����Ϸ���������ĥ�� $lv==0�λ���countAround��Ȥ��褦��
sub countAroundEX {
	my ( $land, $landValue, $x, $y, $kind, $lv, $range ) = @_;
	my ( $i, $sx, $sy );
	my $count = 0;
	for ( $i = 0 ; $i < $range ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # �Ԥˤ�����Ĵ��
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{

			# �ϰϳ��ξ�� ���ʤ�û�
			$count++ if ( $kind == $HlandSea );
		}
		elsif ( $lv < 10 ) {
			$count++
			  if ( ( $land->[$sx][$sy] == $kind )
				&& ( $landValue->[$sx][$sy] == $lv ) );
		}
		elsif (( $land->[$sx][$sy] == $kind )
			&& ( $landValue->[$sx][$sy] >= $lv ) )
		{
			$count++;
		}
	}
	return $count;
}

# ���åХȥ���ĹΨ�׻���
sub MonsterSei {
	my ( $type, @sup ) = @_;
	if ( $type == 1 ) {    #���ƹ⤤
		$sup[0]++;
		$sup[1]++;
		$sup[3]++;
		$sup[4]++;
	}
	elsif ( $type == 2 ) {    #�㤤
		$sup[0]--;
		$sup[1]--;
		$sup[3]--;
		$sup[4]--;
	}
	elsif ( $type == 3 ) {    #����⤤
		$sup[1]++;
	}
	elsif ( $type == 4 ) {    #�����⤤
		$sup[2] = 2;
	}
	elsif ( $type == 5 ) {    #��̿�⤤
		$sup[3]++;
		$sup[4]++;
	}
	return @sup;
}

# ���Ͻи�����
sub shipAppear {
	my ( $land, $direction ) = @_;
	my ( $sx, $sy, $size, $i );
	$size = $HislandSize - 1;

	if ( $direction == 0 ) {

		# ���墪����
		$sx = $size;
		$sy = $size;
		for ( $i = 0 ; $i < $HislandSize ; $i++ ) {
			if ( $HseaChk[ $land->[$sx][$i] ] == 1 ) {

				# �����Ϸ��ξ�硢���ϤϽ���
				$sy = $i;
				last;
			}
		}
	}
	elsif ( $direction == 1 ) {

		# ����������
		$sx = $size;
		$sy = $size;
		for ( $i = $size ; $i >= 0 ; $i-- ) {
			if ( $HseaChk[ $land->[$i][$sy] ] == 1 ) {

				# �����Ϸ��ξ�硢���ϤϽ���
				$sx = $i;
				last;
			}
		}
	}
	elsif ( $direction == 2 ) {

		# ����������

		$sx = 0;
		$sy = $size;
		for ( $i = $size ; $i >= 0 ; $i-- ) {
			if ( $HseaChk[ $land->[$sx][$i] ] == 1 ) {

				# �����Ϸ��ξ�硢���ϤϽ���
				$sy = $i;
				last;
			}
		}
	}
	else {

		# ���墪����

		$sx = $size;
		$sy = 0;
		for ( $i = 0 ; $i < $HislandSize ; $i++ ) {
			if ( $HseaChk[ $land->[$i][$sy] ] == 1 ) {

				# �����Ϸ��ξ�硢���ϤϽ���
				$sx = $i;
				last;
			}
		}
	}
	return ( $sx, $sy );
}

# ű�����(���ʤ궯���ʤ��῿�����ʤ��褦��)
sub shipEvacuation {
	my ( $sx, $sy ) = @_;

	my ($center) = $HislandSize / 2 - 1;
	my (@direction);
	if ( ( $sx <= $center ) && ( $sy <= $center ) ) {

		# ����

		if ( $sx >= $sy ) {
			push( @direction, 1 );
			push( @direction, 6 );
			if ( $sx == $sy ) {
				push( @direction, 5 );
				push( @direction, 4 ) if ( ( $sy % 2 ) == 1 );
			}
		}
		else {
			push( @direction, 5 );
			if ( ( $sy % 2 ) == 1 ) {
				push( @direction, 4 );
				push( @direction, 6 );
			}
		}
	}
	elsif ( ( $sx > $center ) && ( $sy <= $center ) ) {

		# ����

		$sx = $HislandSize - $sx - 1;
		if ( $sx >= $sy ) {
			push( @direction, 1 );
			push( @direction, 6 );
			if ( $sx == $sy ) {
				push( @direction, 2 );
				push( @direction, 3 ) if ( ( $sy % 2 ) == 0 );
			}
		}
		else {
			push( @direction, 2 );
			if ( ( $sy % 2 ) == 0 ) {
				push( @direction, 1 );
				push( @direction, 3 );
			}
		}
	}
	elsif ( ( $sx <= $center ) && ( $sy > $center ) ) {

		# ����
		$sy = $HislandSize - $sy - 1;
		if ( $sx >= $sy ) {

			push( @direction, 3 );
			push( @direction, 4 );
			if ( $sx == $sy ) {
				push( @direction, 5 );
				push( @direction, 6 ) if ( ( $sy % 2 ) == 0 );
			}
		}
		else {
			push( @direction, 5 );
			if ( ( $sy % 2 ) == 0 ) {
				push( @direction, 4 );
				push( @direction, 6 );
			}
		}
	}
	else {

		# ����
		$sx = $HislandSize - $sx - 1;
		$sy = $HislandSize - $sy - 1;
		if ( $sx >= $sy ) {
			push( @direction, 3 );
			push( @direction, 4 );
			if ( $sx == $sy ) {
				push( @direction, 2 );
				push( @direction, 1 ) if ( ( $sy % 2 ) == 1 );
			}
		}
		else {
			push( @direction, 2 );
			if ( ( $sy % 2 ) == 1 ) {
				push( @direction, 1 );
				push( @direction, 3 );
			}
		}
	}

	# ����åե�

	my @new = ();
	for (@direction) {
		my $r = rand @new + 1;
		push( @new, $new[$r] );
		$new[$r] = $_;
	}

	return @new;
}

# �����ﳲ�롼����(����ޤȤ��ͽ��)
sub wideDamage {
	my ( $id, $name, $land, $landValue, $x, $y, $z ) = @_;
	my ( $sx, $sy, $i, $landKind, $lv );

	for ( $i = 0 ; $i < 19 ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );
		next
		  if ( ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) );

		$landKind = $land->[$sx][$sy];
		$lv       = $landValue->[$sx][$sy];

		# �ϰϤˤ��ʬ��

		if ( $i < 7 ) {

			# �濴�������1�إå���
			if ( ( $landKind == $HlandSea ) && ( $lv == 0 ) ) {

				# ��
				$landValue->[$sx][$sy] = 0;
			}
			elsif ( $HseaChk[$landKind] ) {

				# ����
				&logWideDamageSea2( $id, $name, landName( $landKind, $lv ),
					"($sx, $sy)" );
				$land->[$sx][$sy]      = $HlandSea;
				$landValue->[$sx][$sy] = 0;
			}
			else {
				if ( $landKind == $HlandMonster ) {
					&logWideDamageMonsterSea( $id, $name,
						landName( $landKind, $lv ),
						"($sx, $sy)" );
				}
				else {
					&logWideDamageSea( $id, $name, landName( $landKind, $lv ),
						"($sx, $sy)" );
				}
				$land->[$sx][$sy] = $HlandSea;

				# �濴�ϳ���¾������
				$landValue->[$sx][$sy] = ( $i == 0 ) ? 0 : 1;
			}
			next;
		}
		else {

			# 2�إå���
			if (   ( $HseaChk[$landKind] )
				|| ( $landKind == $HlandWaste )
				|| ( $landKind == $HlandMountain ) )
			{
				next;
			}
			elsif ( $landKind == $HlandMonster ) {
				&logWideDamageMonster( $id, $name, landName( $landKind, $lv ),
					"($sx, $sy)" );
			}
			else {
				&logWideDamageWaste( $id, $name, landName( $landKind, $lv ),
					"($sx, $sy)" );
			}
			$land->[$sx][$sy]      = $HlandWaste;
			$landValue->[$sx][$sy] = 0;
		}
		if ( ( $z == 1 ) && ( $land->[$sx][$sy] == $HlandWaste ) ) {
			&logWideDamageOsen( $id, $name, "����", "($sx, $sy)" );
			$land->[$sx][$sy]      = $HlandOsen;
			$landValue->[$sx][$sy] = 1;
		}
	}
}

# Ķ�����ﳲ�롼����(����ޤȤ��ͽ��)
sub SuperDamage {
	my ( $id, $name, $land, $landValue, $x, $y ) = @_;
	my ( $sx, $sy, $i, $landKind, $lv );

	for ( $i = 0 ; $i < 37 ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];

		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );
		next
		  if ( ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) );

		$landKind = $land->[$sx][$sy];
		$lv       = $landValue->[$sx][$sy];

		# �ϰϤˤ��ʬ��

		if ( $i == 0 ) {
			&logWideDamageSea2( $id, $name, landName( $landKind, $lv ),
				"($sx, $sy)" );
			$land->[$sx][$sy]      = $HlandMountain;
			$landValue->[$sx][$sy] = 0;
		}
		elsif ( $i < 7 ) {

			# 1�إå���
			&logWideDamageSea2( $id, $name, landName( $landKind, $lv ),
				"($sx, $sy)" );
			if ( $landKind == $HlandMountain ) {
				$land->[$sx][$sy]      = $HlandWaste;
				$landValue->[$sx][$sy] = 1;
			}
			else {
				$land->[$sx][$sy]      = $HlandSea;
				$landValue->[$sx][$sy] = 0;
			}
		}
		elsif ( $i < 19 ) {

			# 2�إå���
			if (   ( ( $landKind == $HlandSea ) && ( $lv == 0 ) )
				|| ( $landKind == $HlandMountain ) )
			{
				next;
			}
			else {
				&logWideDamageSea2( $id, $name, landName( $landKind, $lv ),
					"($sx, $sy)" );
				$land->[$sx][$sy]      = $HlandSea;
				$landValue->[$sx][$sy] = 1;
			}
		}
		else {

			# 3�إå���
			if (   ( $HseaChk[$landKind] )
				|| ( $landKind == $HlandWaste )
				|| ( $landKind == $HlandMountain ) )
			{
				next;
			}
			elsif ( $landKind == $HlandMonster ) {
				&logWideDamageMonster( $id, $name, landName( $landKind, $lv ),
					"($sx, $sy)" );
			}
			else {
				&logWideDamageWaste( $id, $name, landName( $landKind, $lv ),
					"($sx, $sy)" );
			}
			$land->[$sx][$sy]      = $HlandWaste;
			$landValue->[$sx][$sy] = 0;
		}
	}
}

# �����ﳲ����롼����
sub wideDamageSpace {
	my ( $id, $land, $landValue, $dis, $nation, $x, $y, $z, $mode ) = @_;
	my ( $sx, $sy, $i, $landKind, $lv );

	for ( $i = 0 ; $i < $z ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );
		next
		  if ( ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize )
			|| ( $land->[$sx][$sy] == $HlandEarth )
			|| ( $land->[$sx][$sy] == $HlandSea ) );

		$landKind = $land->[$sx][$sy];
		$lv       = $landValue->[$sx][$sy];
		if ( ( $mode == 0 ) || ( $i == 0 ) ) {

			# ����
			logWideDamageSpace( landName( $landKind, $lv ),
				"($sx, $sy)", "��̵" );
			$land->[$sx][$sy]      = $HlandSea;
			$landValue->[$sx][$sy] = 0;
		}
		else {

			# �˲�
			if ( ( $landKind == $HlandSunit ) && ( $lv == 20 ) ) {
			}
			else {
				logWideDamageSpace( landName( $landKind, $lv ),
					"($sx, $sy)", "ʴ��" );
			}
			$land->[$sx][$sy]      = $HlandSunit;
			$landValue->[$sx][$sy] = 20;
		}
		$dis->[$sx][$sy]    = 0;
		$nation->[$sx][$sy] = 0;
	}
}

# ����ޤȤ��
sub logMatome {
	my ( $island, $flag, $kind ) = @_;
	my ( $sno, $m, $i, $sArray, $spnt, $x, $y, $z, $point );
	my @ptn = (
		"����",                "���Ω��",
		"���ϡ����Ω��", "����",
		"���ϡ�����",       "���Ω�ơ�����",
		"���ϡ����Ω�ơ�����"
	);
	$sno   = $island->{$kind};
	$point = "";
	if ( $sno > 0 ) {
		if ( $flag == 1 ) {
			$kind .= 'pnt';

			$sArray = $island->{$kind};
			for ( $i = 0 ; $i < $sno ; $i++ ) {
				$spnt = $sArray->[$i];
				last if ( $spnt eq "" );
				( $x, $y, $z ) = ( $spnt->{x}, $spnt->{y}, $spnt->{z} );
				if ( $z eq '����' ) {
					$point .= " ��($x, $y)";
					$m |= 1 unless ( $m & 1 );
				}
				elsif ( $z eq '���Ω��' ) {
					$point .= " ��($x, $y)";
					$m |= 2 unless ( $m & 2 );
				}
				elsif ( $z eq '����' ) {
					$point .= " ��($x, $y)";
					$m |= 4 unless ( $m & 4 );
				}
				else {
					$point .= "($x, $y)";
				}
				$point .= "<br>������" unless ( ( $i + 1 ) % 20 );
			}
		}
		$point .= "��<B>$sno����</B>" if ( $i > 1 || $flag != 1 );
	}
	unless ( $point eq "" ) {
		if ( ( $flag == 1 ) && ( $m > 0 ) ) {
			logLandSucMatome(
				$island->{'id'}, $island->{'name'},
				@ptn[ $m - 1 ],  "$point"
			);
		}
		else {
			logLandSuc( $island->{'id'}, $island->{'name'}, $z, "($x, $y)" );
		}
	}
}

# ���ؤν���
# ��1����:��å�����
# ��2����:������
# ��3����:���

# �̾��
sub logOut {
	push( @HlogPool, "0,$HislandTurn,$_[1],$_[2],$_[0]" );
}

# �ٱ��
sub logLate {
	push( @HlateLogPool, "0,$HislandTurn,$_[1],$_[2],$_[0]" );
}

# ��̩��
sub logSecret {
	push( @HsecretLogPool, "1,$HislandTurn,$_[1],$_[2],$_[0]" );
}

# ŷ����
sub logWeather {
	open( HOUT, ">>${HlogdirName}/weather.his" );
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# ��Ͽ��
sub logHistory {
	open( HOUT, ">>${HlogdirName}/hakojima.his" );
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# ��Ͽ��Ĵ��
sub logHistoryTrim {
	my ( $logname, $Maxlog ) = @_;
	open( HIN, "${HlogdirName}/${logname}" );
	my ( @line, $l );
	my $count = 0;
	while ( $l = <HIN> ) {
		chomp($l);
		push( @line, $l );
		$count++;
	}
	close(HIN);

	if ( $count > $Maxlog ) {
		open( HOUT, ">${HlogdirName}/${logname}" );
		my ($i);
		for ( $i = ( $count - $Maxlog ) ; $i < $count ; $i++ ) {
			print HOUT "$line[$i]\n";
		}
		close(HOUT);
	}
}

# ���񤭽Ф�
sub logFlush {
	open( LOUT, ">${HlogdirName}/hakojima.log0" );

	# �����ս�ˤ��ƽ񤭽Ф�
	my ($i);
	for ( $i = $#HsecretLogPool ; $i >= 0 ; $i-- ) {
		print LOUT $HsecretLogPool[$i];
		print LOUT "\n";
	}
	for ( $i = $#HlateLogPool ; $i >= 0 ; $i-- ) {
		print LOUT $HlateLogPool[$i];
		print LOUT "\n";
	}
	for ( $i = $#HlogPool ; $i >= 0 ; $i-- ) {
		print LOUT $HlogPool[$i];
		print LOUT "\n";
	}
	close(LOUT);
}

#----------------------------------------------------------------------
# ���ƥ�ץ졼��
#----------------------------------------------------------------------

# ���ߡ�̿��
sub logDummy {
	my ( $id, $name, $comName, $point ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}�ϥ��ߡ�̿��Ǥ���",
		$id
	);
}

# ���ޥ�ɼ���
sub logMiss {
	logOut(
"${HtagName_}$_[1]$AfterName${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$_[2]${H_tagComName}�ϡ�$_[3]������ߤ���ޤ�����",
		$_[0]
	);
}

# ���ޥ�ɼ���(����)
sub logMissS {
	logOut(
"${HtagName_}${SpaceName}$_[3]${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$_[2]${H_tagComName}�ϡ�$_[4]������ߤ���ޤ�����",
		$_[0]
	);
}

# ���ޥ�ɼ��ԣ�(����)
sub logMissS2 {
	logOut(
"${HtagName_}${SpaceName}$_[3]${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$_[2]${H_tagComName}�ϡ�$_[4]���Ἲ�Ԥ��ޤ�����",
		$_[0], 999
	);
}

# �о��Ϸ��μ���ˤ�뼺��
sub logLandFail {
	my ( $id, $name, $comName, $landName, $point, $landKind, $lv ) = @_;
	if ( $landKind == $HlandGhostShip ) {

		# ͩ�����ϳ��˵���
		$landName = '��';
	}
	elsif ( $landKind == $HlandMonster ) {

		# �º̤��Τ�
		if ( ( monsterSpec($lv) )[0] == 26 ) {
			$landName = '����';
		}
	}
	logOut(
"${HtagName_}$name${AfterName}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$comName${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$point${H_tagName}��<B>$landName</B>���ä�������ߤ���ޤ�����",
		$id
	);
}

# ����˳���Φ���ʤ������Ω�Ƽ���
sub logNoLandAround {
	logOut(
"${HtagName_}$_[1]${AfterName}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$_[2]${H_tagComName}�ϡ�ͽ���Ϥ�${HtagName_}$_[4]${H_tagName}�μ��դ�$_[3]���ʤ��ä�������ߤ���ޤ�����",
		$_[0]
	);
}

# ���ĺ�
sub logClosedPort {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>���ĺ������褦�Ǥ���",
		$id
	);
}

# ���Ϸ�����
sub logLandSuc {
	my ( $id, $name, $comName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",
		$id
	);
}

# ���Ϸϥ��ޤȤ�
sub logLandSucMatome {
	my ( $id, $name, $comName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����<br>����<B>��</B> $point",
		$id
	);
}

# ���Ϸ�(����)����
sub logLandSucS {
	my ( $id, $name, $comName, $point ) = @_;
	logOut(
"${HtagName_}${SpaceName}${point}${H_tagName}��${HtagName_}$name$AfterName${H_tagName}�ˤ��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",
		$id, 999
	);
}

# �ץ쥼��ȼ���
sub logNoPresent {
	my ( $id, $name, $comName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}�ϳ����Υץ쥼��Ȥ�̵���١���ߤ���ޤ�����",
		$id
	);
}

# �ץ쥼��ȱ��
sub logPresent {
	my ( $id, $tId, $name, $tName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}���ץ쥼��Ȥ�${HtagName_}${tName}${AfterName}${H_tagName}�ؾ��Ϥ��ޤ�����",
		$id, $tId
	);
}

# ���μ�ưȲ��
sub logAutoTree {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>��</B>��${HtagComName_}Ȳ��${H_tagComName}��������${HtagComName_}����${H_tagComName}���ޤ�����",
		$id
	);
}

# Ĵ���ϥ�
sub logChosa {
	logOut(
"${HtagName_}$_[1]${AfterName}$_[2]${H_tagName}��<B>$_[4]</B>��ͽ����Ĥ������${HtagComName_}$_[3]${H_tagComName}���Ԥ��$_[5]������",
		$_[0]
	);
}

# ���Ĥ���μ���
sub logOilMoney {
	my ( $id, $name, $lName, $point, $value ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>���顢<B>$value$HunitMoney</B>�μ��פ��夬��ޤ�����",
		$id
	);

	#��󥭥��ѥ��ե�����񤭽Ф�
	open( MOUT, ">>${HlogdirName}/money.log" );
	print MOUT "$HislandTurn,$id,����,$value\n";
	close(MOUT);
}

# ���ĸϳ�
sub logOilEnd {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>�ϸϳ餷���褦�Ǥ���",
		$id
	);
}

# �ɱһ��ߡ��������å�
sub logBombSet {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��<B>�������֤����å�</B>����ޤ�����",
		$id
	);
}

# �ɱһ��ߡ�������ư
sub logBombFire {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�������ֺ�ư����${H_tagDisaster}",
		$id
	);
}

# ��ǰ�ꡢȯ��
sub logMonFly {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��<B>�첻�ȤȤ������Ω���ޤ���</B>��",
		$id
	);
}

# ��ǰ�ꡢ�
sub logMonDamage {
	my ( $id, $name, $point ) = @_;
	logOut(
"<B>�����ȤƤĤ�ʤ����</B>��${HtagName_}${name}${AfterName}$point${H_tagName}����������ޤ�������",
		$id
	);
}

# ����or�ߥ��������
sub logPBSuc {
	my ( $id, $name, $comName, $point ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",
		$id
	);
	logOut(
"������ʤ�����${HtagName_}${name}${AfterName}${H_tagName}��<B>��</B>���������褦�Ǥ���",
		$id
	);
}

# �ϥ�ܥ�
sub logHariSuc {
	my ( $id, $name, $comName, $comName2, $point ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}$point${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",
		$id
	);
	logLandSuc( $id, $name, $comName2, $point );
}

# ���å��Ǥ��夲����
sub logRocketF {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagComName_}���å�${H_tagComName}���Ǥ��夲�ޤ�������<B>����</B>���ޤ�����",
		$id
	);
}

# ���å��Ǥ��夲����

sub logRocketS {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagComName_}���å�${H_tagComName}���Ǥ��夲���ߤ���<B>����</B>���ޤ�����",
		$id
	);
}

# ��ά����
sub logSpyF {
	my ( $id, $tId, $name, $tName, $comName ) = @_;
	logLate(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${AfterName}${H_tagName}��${HtagComName_}$comName${H_tagComName}�򤷤ޤ����������Ԥ�����館���ޤ�����",
		$id, $tId
	);
}

# ����ȯ��
sub logBeseFind {
	my ( $id, $tName, $tPoint, $tLv, $tLname ) = @_;
	logSecret(
"${HtagName_}${tName}${AfterName}$tPoint${H_tagName}�����Ƿи���<B>$tLv</B>��<B>$tLname</B>ȯ������",
		$id
	);
}

# �ɱһ���Ƚ��
sub logLandTruth {
	my ( $id, $tName, $tPoint, $tLname, $truth ) = @_;
	logSecret(
"${HtagName_}${tName}${AfterName}$tPoint${H_tagName}������<B>$tLname</B>�Ϥɤ����<B>$truth</B>�Τ褦�Ǥ���",
		$id
	);
}

# ���ž�����֤������
sub logWarpMeteo {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"<B>���</B>��${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>�����<B>�����ζ��֤˵ۤ����ޤ�ޤ�������</B>",
		$id
	);
}

# ���á���Ϣ�����Ԥ���롣
sub logUNMons {
	my ( $id, $name, $mName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>����$mName</B>�Ϲ�Ϣ���ˤ�ä����Ԥ�����Ϥˤʤ�ޤ�����",
		$id
	);
}

# ���á�ž�����֤�Ƨ��
sub logWarpMons {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"<B>$mName</B>��${HtagName_}${name}${AfterName}$point${H_tagName}��<B>${lName}</B>����ã��<B>�����ζ��֤˵ۤ����ޤ�ޤ�������</B>",
		$id
	);
}

# ���á�ž�ܼ���
sub logWarpMonsMiss {
	my ( $id, $name, $point, $mName ) = @_;
	logOut(
"ž�������Ϥ���<B>$mName</B>��${HtagName_}${name}${AfterName}$point${H_tagName}��<B>�Ƥ�����äƤ��ޤ�������</B>",
		$id
	);
}

# ���á���С��ߥ�����ž��
sub logMWarp {
	my ( $id, $tId, $Name, $tName, $point, $lName ) = @_;
	logOut(
"${HtagName_}${tName}${AfterName}$point${H_tagName}�����ζ��֤��Ĥߡ�����<B>${lName}</B>���и����ޤ������ɤ����${HtagName_}${Name}${AfterName}${H_tagName}���Τ褦�Ǥ���",
		$id, $tId
	);
}

# �ߥ������Ȥ��Ȥ���(or �����ɸ����褦�Ȥ���)���������åȤ����ʤ�
sub logMsNoTarget {
	my ( $id, $name, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ���ɸ��${AfterName}�˿ͤ���������ʤ�������ߤ���ޤ�����",
		$id
	);
}

# �ߥ������Ȥ��Ȥ���(or �����ɸ����褦�Ȥ���)����Ϣ�ˤȤ��줿
sub logUNMiss {
	my ( $id, $tId, $name, $tName, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}${comName}${H_tagComName}�ϡ���ɸ��${HtagName_}${tName}${AfterName}${H_tagName}����Ϣ�ݸ���֤�����ߤ���ޤ�����",
		$id, $tId
	);
}

# �ɱһ��߿ʲ�
sub logDefenceS {
	my ( $id, $tId, $tName, $tLname, $tPoint ) = @_;
	logOut(
"--- ${HtagName_}$tPoint${H_tagName}��<B>${tLname}</B>��S${tLname}��ȯŸ���ޤ�����",
		$id, $tId
	);
}

# �ɱһ��ߥ�����

sub logDefenceD {
	my ( $id, $tId, $tName, $tLname, $tPoint ) = @_;
	logOut(
"--- ${HtagName_}$tPoint${H_tagName}��<B>S${tLname}</B>��${tLname}�˥�٥�����󤷤ޤ�����",
		$id, $tId
	);
}

# �ߥ�����ȯ�Ϳ��ʤ�ɽ��
sub logMissile {
	logOut(
"${HtagName_}$_[2]${AfterName}${H_tagName}��${HtagName_}$_[3]${AfterName}$_[5]${H_tagName}�����˸�����<b>$_[6]ȯ</b>��${HtagComName_}$_[4]${H_tagComName}��Ԥ��ޤ�����(̿��$_[7]��̵��$_[8]��ŷ��$_[9]���ɱ�$_[10])",
		$_[0], $_[1]
	);
}

sub logMissileS {
	logSecret(
"${HtagName_}$_[2]${AfterName}${H_tagName}��${HtagName_}$_[3]${AfterName}$_[5]${H_tagName}�����˸�����<b>$_[6]ȯ</b>��${HtagComName_}$_[4]${H_tagComName}��Ԥ��ޤ�����(̿��$_[7]��̵��$_[8]��ŷ��$_[9]���ɱ�$_[10])",
		$_[0], $_[1]
	);
	logLate(
"<B>���Ԥ�</B>��${HtagName_}$_[3]${AfterName}$_[5]${H_tagName}�����˸�����<b>$_[6]ȯ</b>��${HtagComName_}$_[4]${H_tagComName}��Ԥ��ޤ�����(̿��$_[7]��̵��$_[8]��ŷ��$_[9]���ɱ�$_[10])",
		$_[1]
	);
}

# �̾�ߥ������̾��Ϸ���̿��
sub logMsNormal {
	logOut(
"--- ${HtagName_}$_[3]${H_tagName}��<B>$_[2]</B>��̿�桢���Ӥ�$_[4]�ޤ�����",
		$_[0], $_[1]
	);
}

# ���ƥ륹�ߥ������̾��Ϸ���̿��
sub logMsNormalS {
	my ( $id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $result )
	  = @_;
	logSecret(
"--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ�$result�ޤ�����",
		$id, $tId
	);
	logLate(
"<B>���Ԥ�</B>��${HtagName_}${tName}${AfterName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�桢���Ӥ�${result}�ޤ�����",
		$tId
	);
}

# ���ƥ륹�ߥ������ɱһ��ߤ�Ƚ��
sub logMsCaughtH {
	my ( $tId, $name, $comName ) = @_;
	logSecret(
"�ɤ���${HtagComName_}${comName}${H_tagComName}���ä���ϡ�${HtagName_}${name}${AfterName}${H_tagName}�Τ褦�Ǥ���",
		$tId
	);
}

# �Х����ߥ�����
sub logBioMs {
	logOut(
"--- ${HtagName_}$_[3]${H_tagName}��<B>$_[2]</B>����������Ӥ�<B>����</B>���ޤ�����",
		$_[0], $_[1]
	);
}

# Φ���˲���̿��
sub logMsLD {
	logOut( "--- ${HtagName_}$_[2]${H_tagName}$_[3]�ޤ�����", $_[0],
		$_[1] );
}

# �̾�ߥ����롢���ä�̿�桢�Ų���ˤ�̵��
sub logMsMonNoDamage {
	logOut(
"--- ${HtagName_}$_[3]${H_tagName}��<B>����$_[2]</B>��̿�桢�������Ų����֤��ä�������̤�����ޤ���Ǥ�����",
		$_[0], $_[1]
	);
}

# ���ƥ륹�ߥ����롢���ä�̿�桢�Ų���ˤ�̵��
sub logMsMonNoDamageS {
	my ( $id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${AfterName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�桢�������Ų����֤��ä�������̤�����ޤ���Ǥ�����",
		$id, $tId
	);
	logLate(
"<B>���Ԥ�</B>��${HtagName_}${tName}${AfterName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�桢�������Ų����֤��ä�������̤�����ޤ���Ǥ�����",
		$tId
	);
}

# �̾�ߥ����롢���ä�̿�桢����
sub logMsMonKill {
	my ( $id, $tId, $name, $tName, $tLname, $tPoint ) = @_;
	logOut(
"--- ${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>���ϿԤ����ݤ�ޤ�����",
		$id, $tId
	);

	#��󥭥��ѥ��ե�����񤭽Ф�
	open( ROUT, ">>${HlogdirName}/ranking.log" );
	print ROUT "$HislandTurn,$id,$tId,$tLname\n";
	close(ROUT);
}

# ���ƥ륹�ߥ����롢���ä�̿�桢����
sub logMsMonKillS {
	my ( $id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${AfterName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>���ϿԤ����ݤ�ޤ�����",
		$id, $tId
	);
	logLate(
"<B>���Ԥ�</B>��${HtagName_}${tName}${AfterName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>���ϿԤ����ݤ�ޤ�����",
		$tId
	);
}

# �̾�ߥ����롢���ä�̿�桢���᡼��
sub logMsMonster {
	logOut(
"--- ${HtagName_}$_[3]${H_tagName}��<B>����$_[2]</B>��̿�档<B>����$_[2]</B>�϶줷��������Ӭ���ޤ�����",
		$_[0], $_[1]
	);
}

# ���ƥ륹�ߥ����롢���ä�̿�桢���᡼��
sub logMsMonsterS {
	my ( $id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${AfterName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>�϶줷��������Ӭ���ޤ�����",
		$id, $tId
	);
	logLate(
"<B>���Ԥ�</B>��${HtagName_}${tName}${AfterName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>�϶줷��������Ӭ���ޤ�����",
		$tId
	);
}

# �ߥ������Ϸ���̿��(���衢����)
sub logMsSpace {
	logOut(
"--- ${HtagName_}$_[1]${H_tagName}��<B>$_[2]</B>��̿�桢���Ӥ�$_[3]�ޤ�����",
		$_[0], $_[4]
	);
}

# �ߥ������Ϸ���̿��(����)
sub logMsOPlayer {
	logOut(
"--- ${HtagName_}$_[1]${H_tagName}��<B>$_[2]</B>�ն��������Ҥ��ߤ��������͡�",
		$_[0], $_[3]
	);
}

# �ߥ�������ä�̿��(���衢����)
sub logMsMonSpace {
	logOut(
"--- ${HtagName_}$_[1]${H_tagName}��<B>����$_[2]</B>��̿�桢<B>����$_[2]</B>�϶줷��������Ӭ���ޤ�����",
		$_[0], $_[3]
	);
}

# �ߥ����롢���ä�̿�桢����(���衢����)
sub logMsMonKillSpace {
	logOut(
"--- ${HtagName_}$_[2]${H_tagName}��<B>����$_[3]</B>��̿�桢<B>����$_[3]</B>���ϿԤ����ݤ�ޤ�����",
		$_[0], $_[4]
	);

	#��󥭥��ѥ��ե�����񤭽Ф�
	open( ROUT, ">>${HlogdirName}/ranking.log" );
	print ROUT "$HislandTurn,$_[0],$_[4],$_[3]\n";
	close(ROUT);
}

# �ߥ�����ȯ�Ϳ��ʤ�ɽ��(���衢����)
sub logMissileSpace {
	logOut(
"${HtagName_}$_[1]${AfterName}${H_tagName}��${HtagName_}$_[9]$_[3]${H_tagName}�����˸�����<b>$_[4]ȯ</b>��${HtagComName_}$_[2]${H_tagComName}��Ԥ��ޤ�����(̿��$_[5]��̵��$_[6]������$_[7]���ɱ�$_[8])",
		$_[0], $_[10]
	);
}

# ���äλ���
sub logMsMonMoney {
	my ( $tId, $mName, $value ) = @_;
	logOut(
"<B>����$mName</B>�λĳ��ˤϡ�<B>$value$HunitMoney</B>���ͤ��դ��ޤ�����",
		$tId
	);

	#��󥭥��ѥ��ե�����񤭽Ф�
	open( MOUT, ">>${HlogdirName}/money.log" );
	print MOUT "$HislandTurn,$tId,���÷���,$value\n";
	close(MOUT);
}

# �ߥ�����̿�����
sub logMsMiss {
	logOut(
"${HtagName_}$_[1]$AfterName${H_tagName}��ͽ�ꤵ��Ƥ���${HtagComName_}$_[2]${H_tagComName}�ϡ��ߥ�������������ͭ���Ƥ��ʤ������뤤�Ϥ���餬��ư�Ǥ��ʤ������Τ�����ߤ���ޤ�����",
		$_[0]
	);
}

# ���á���ʩ�Ǥ��ʤ�
sub logMonsRei {
	logOut(
"--- ${HtagName_}$_[3]${H_tagName}��<B>����$_[2]</B>��̿�档<B>����$_[2]</B>���ϿԤ��ޤ���������ʩ�Ǥ�����<B>���Х��쥤</B>�ˤʤ�ޤ�����",
		$_[0], $_[1]
	);
}

# ���á�������
sub logMonsGold {
	my ( $id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${AfterName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>����$tLname</B>��̿�档<B>����$tLname</B>���ϿԤ��ޤ��������ΤȤ��λĳ���<B>������</B>��¤���ޤ�����",
		$id, $tId
	);

	#��󥭥��ѥ��ե�����񤭽Ф�
	open( ROUT, ">>${HlogdirName}/ranking.log" );
	print ROUT "$HislandTurn,$id,$tId,$tLname\n";
	close(ROUT);
}

# ���á�ȿ��
sub logMonsCounter {
	logOut(
"--- ${HtagName_}$_[3]${H_tagName}��<B>����$_[2]</B>��̿�档���������̤�̵���Ф��꤫���֤��˱��褫��$_[4]",
		$_[0], $_[1]
	);
}

# �ߥ�������̱����
sub logMsBoatPeople {
	my ( $id, $name, $achive ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}�ˤɤ�����Ȥ�ʤ�<B>$achive${HunitPop}�����̱</B>��ɺ�夷�ޤ�����${HtagName_}${name}${AfterName}${H_tagName}�ϲ����������줿�褦�Ǥ���",
		$id
	);
}

# ���̿��
sub logMsBank {
	my ( $id, $name, $bank ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}�ˤɤ�����Ȥ�ʤ�<B>$bank${HunitMoney}��Τ���</B>��ɺ�夷�ޤ�����${HtagName_}${name}${AfterName}${H_tagName}�ϲ��������Ȥä��褦�Ǥ���",
		$id
	);
}

#--------���åХȥ�-------------
# �������
sub logMonsCancel {
	my ( $id, $name, $comName, $Result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}�ϡ�${Result}������ߤ���ޤ�����",
		$id
	);
}

# ���å��å�
sub logMonsEGG {
	my ( $id, $name, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ԥ����ä��Τ餬�������ޤ�����",
		$id
	);
}

# �������
sub logMonsSell {
	my ( $id, $name, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ԥ������äϤ��ʤ��ʤ�ޤ�����",
		$id
	);
}

# �����ϵ�����
sub logMonsExer {
	my ( $id, $name, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}�Ǳ¤�Ȥä�${HtagComName_}${comName}${H_tagComName}��Ԥ����¤��ʤ��ʤ�ޤ�����",
		$id
	);
}

# ���ñ���
sub logMonsENSEI {
	my ( $id, $name, $tId, $tName, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ԥ�${HtagName_}${tName}${AfterName}${H_tagName}�˽з⤷�ޤ�����",
		$id, $tId
	);
}

# �¥��ȥå�
sub logMonsESA {
	my ( $id, $name, $mName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}�ϡ�<B>����$mName</B>��¤Ȥ��ƥ��ȥå����ޤ�����",
		$id
	);
}

# �¾���
sub logMonsEsaAid {
	my ( $id, $name, $tId, $tName, $mName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}�ϡ�${HtagName_}${tName}${AfterName}${H_tagName}��<B>����$mName</B>��¤Ȥ��ƾ��Ϥ��ޤ�����",
		$id, $tId
	);
}

# ���þ���
sub logMonsAid {
	my ( $id, $name, $tId, $tName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}�ϡ�${HtagName_}${tName}${AfterName}${H_tagName}�˲��ä���Ϥ��ޤ�����",
		$id, $tId
	);
}

# ���ÿʲ�
sub logMonsEvo {
	my ( $id, $name, $mName, $mNameE, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ԥ�<B>����$mName</B>�θ����ä�<B>����$mNameE</B>�������Ѱۤ��ޤ�����",
		$id
	);
}

# ���ÿʲ�����
sub logMonsEvoF {
	my ( $id, $name, $mName, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ������������Ѳ�������ޤ���Ǥ�����",
		$id
	);
}

# ���ù���
sub logMonsATTACK {
	my ( $id, $name, $mName, $tId, $tName, $tmName, $Result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>����$mName</B>��${HtagName_}${tName}${AfterName}${H_tagName}��<B>����$tmName</B>��<B>${Result}</B>",
		$id, $tId
	);
}

# ξ�Ԥϴ֤�Ȥä�
sub logMonsNOATTACK {
	my ( $id, $name, $mName, $tId, $tName, $tmName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>����$mName</B>��${HtagName_}${tName}${AfterName}${H_tagName}��<B>����$tmName</B>�ϡ�ξ�Դ֤�Ȥ�ư���ޤ���Ǥ�����",
		$id, $tId
	);
}

# ���ò���
sub logMonsRrcovery {
	my ( $id, $name, $mName, $tId, $P ) = @_;
	if ( $P > 0 ) {
		logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>����$mName</B>�ϡ��������椷<B>${P}</B>�ݥ���ȼ��ʲ������ޤ�����",
			$id, $tId
		);
	}
}

# ���åХȥ뽪λ
sub logMonsEND {
	my ( $id, $name, $mName, $tId, $Result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>����$mName</B>�ϡ�<B>${Result}</B>",
		$id, $tId
	);
}

#-----------���ϥ�---------------
# ��ͭ�礬¸�ߤ��ʤ�������
sub logShipWreck {
	my ( $id, $name, $tLname, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}������<B>$tLname</B>�ϡ���ͭ�礬¸�ߤ��ʤ������񤷤ޤ�����",
		$id
	);
}

# ��±����Ϣ�����Ԥ���롣
sub logUNShip {
	my ( $id, $name, $mName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}������<B>$mName</B>�ϡ���Ϣ���ˤ�ä����Ԥ���ޤ�����",
		$id
	);
}

# �̾�ߥ����롢����̿�桢���᡼��������
sub logMsShip {
	my ( $id, $tId, $tLname, $tPoint, $tL, $result ) = @_;
	logOut(
"--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>��$result",
		$id, $tId
	);

	#��󥭥��ѥ��ե�����񤭽Ф�
	$tL -= $HlandPirate;
	open( ROUT, ">>${HlogdirName}/ship.log" );
	print ROUT "$HislandTurn,$id,99,$tL\n";
	close(ROUT);
}

# �̾�ߥ����롢����̿�桢���᡼��
sub logMsShipD {
	my ( $id, $tId, $tLname, $tPoint, $tL, $result ) = @_;
	logOut(
"--- ${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>��$result",
		$id, $tId
	);
}

# ���ƥ륹�ߥ����롢����̿�桢���᡼��������
sub logMsShipS {
	my ( $id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $result )
	  = @_;
	logSecret(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${AfterName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>��$result",
		$id, $tId
	);
	logLate(
"<B>���Ԥ�</B>��${HtagName_}${tName}${AfterName}$point${H_tagName}�����˸�����${HtagComName_}${comName}${H_tagComName}��Ԥ���${HtagName_}$tPoint${H_tagName}��<B>$tLname</B>��̿�档<B>$tLname</B>��$result",
		$tId
	);
}

# ��ư��
sub logShipMove {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>�ն��<B>$mName</B>����ư���ޤ�����",
		$id
	);
}

# ��άå
sub logShipPlunder {
	my ( $id, $tId, $name, $lName, $point, $mName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>�ն��<B>$mName</B>����ư���ޤ��������κݤ�άå��Ԥ�<B>$lName</B>���˲�����ޤ�����",
		$id, $tId
	);
}

# �������ѹ�
sub logShipOrderC {
	my ( $id, $name, $lName, $point, $result ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>�λ����<B>$result</B>���ѹ����ޤ�����",
		$id
	);
}

# ������
sub logShipCome {
	my ( $id, $name, $mName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${point}${H_tagName}��<B>$mName</B>�и�����",
		$id
	);
}

# ������
sub logShipComeIs {
	my ( $id, $name, $mName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${point}${H_tagName}��<B>$mName</B>�������äƤ��ޤ�������",
		$id
	);
}

# ���ä���
sub logShipDis {
	my ( $id, $name, $mName, $point, $result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${point}${H_tagName}��<B>$mName</B>${result}�ޤ�����",
		$id
	);
}

# ���ǥ��ȥ�åפ�Ƨ��
sub logShipMoveDeathtrap {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"<B>$mName</B>��${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>����ã��<B>${lName}</B>����ư��<B>$mName</B>�Ϸ������ޤ�������",
		$id
	);
}

#-----------�����ޤ�---------------

# ��ⷫ��
sub logDoNothing {
	my ( $id, $name, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",
		$id
	);
}

# ���
sub logSell {
	my ( $id, $name, $comName, $value ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>$value</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",
		$id
	);
}

# ���
sub logAid {
	my ( $id, $tId, $name, $tName, $comName, $str ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${H_tagName}��<B>$str</B>��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",
		$id, $tId
	);
}

# ��̱����
sub logRefugees {
	my ( $id, $tId, $name, $tName, $achive ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${AfterName}${H_tagName}��<B>$achive${HunitPop}��ΰ�̱</B>�����ꤳ�ߤޤ�����",
		$id, $tId
	);
}

# Ͷ�׳�ư
sub logPropaganda {
	my ( $id, $name, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}���Ԥ��ޤ�����",
		$id
	);
}

# ����
sub logGiveup {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}���������졢<B>̵��${AfterName}</B>�ˤʤ�ޤ�����",
		$id
	);
	logHistory(
"${HtagName_}${name}${AfterName}${H_tagName}����������<B>̵��${AfterName}</B>�Ȥʤ롣"
	);
}

# ����
sub logDead {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}����ͤ����ʤ��ʤꡢ<B>̵��${AfterName}</B>�ˤʤ�ޤ�����",
		$id
	);
	logHistory(
"${HtagName_}${name}${AfterName}${H_tagName}���ͤ����ʤ��ʤ�<B>̵��${AfterName}</B>�Ȥʤ롣"
	);
}

# ���ǣ�
sub logDead2 {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}�ϡ����̥롼��ˤ�ꡢ<B>����${AfterName}</B>���ޤ�����",
		$id
	);
	logHistory(
"${HtagName_}${name}${AfterName}${H_tagName}�����̥롼��ˤ��<B>����${AfterName}</B>�Ȥʤ롣"
	);
}

# ����
sub logStarve {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagDisaster_}��������­${H_tagDisaster}���Ƥ��ޤ�����",
		$id
	);
}

#---------���ôط��Υ�---------

# ���ø���
sub logMonsCome {
	my ( $id, $name, $mName, $point, $lName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>����$mName</B>�и�����${HtagName_}$point${H_tagName}��<B>$lName</B>��Ƨ�߹Ӥ餵��ޤ�����",
		$id
	);
}

# ���ø���(����)
sub logMonsComeSpace {
	my ( $mName, $point, $lName ) = @_;
	logOut(
"${HtagName_}${SpaceName}${H_tagName}��<B>����$mName</B>�и�����${HtagName_}$point${H_tagName}��<B>$lName</B>���׷���̵���˲�����ޤ�����",
		999
	);
}

# ���ø���(����)
sub logMonsComeOcean {
	my ( $mName, $point, $lName ) = @_;
	logOut(
"${HtagName_}${OceanName}${H_tagName}��<B>����$mName</B>�и�����${HtagName_}$point${H_tagName}��<B>$lName</B>���׷���̵���˲�����ޤ�����",
		888
	);
}

# ��������ù�(����)
sub logMonsMoveOcean {
	my ( $tId, $lName, $point, $mName ) = @_;
	logOut(
"<B>����$mName</B>��${HtagName_}${OceanName}$point${H_tagName}��<B>$lName</B>���ù����ޤ�����",
		888, $tId
	);
}

# ����ư��(���衢����)
sub logMonsMoveSpace {
	logOut(
"${HtagName_}$_[2]$_[0]${H_tagName}��<B>$_[3]</B>��<B>����$_[1]</B>���׷���̵���˲�����ޤ�����",
		$_[4]
	);
}

# ����ư����(���衢����)
sub logMonsMoveSpace2 {
	logOut(
"${HtagName_}$_[2]$_[0]${H_tagName}��<B>����$_[1]</B>����ư���ޤ�����",
		$_[3]
	);
}

# ���á��ɱһ��ߤ�Ƨ��(����)
sub logMonsMoveDefenceS {
	my ( $lName, $point, $mName ) = @_;
	logOut(
"<B>����$mName</B>��${HtagName_}${SpaceName}$point${H_tagName}��<B>$lName</B>����ã��<B>${lName}�μ������֤���ư����</B>",
		999
	);
}

# �����ϵ���ù�(����)
sub logMonsMoveEarth {
	my ( $lName, $point, $mName ) = @_;
	logOut(
"<B>����$mName</B>��${HtagName_}${SpaceName}$point${H_tagName}��<B>$lName</B>�ΰ��Ϥ˰���������ޤ��׷���̵���ä����ޤ�����",
		999
	);
}

# ����ư��
sub logMonsMove {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��<B>����$mName</B>��Ƨ�߹Ӥ餵��ޤ�����",
		$id
	);
}

# ���ö���Ȥ�
sub logMonsMoney {
	my ( $id, $name, $lName, $point, $mName, $result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��<B>����$mName</B>��Ƨ�߹Ӥ餵��ޤ�������<B>$result</B>����Ȥ��ޤ�����",
		$id
	);
}

# ���äޤȤ᤿��
sub logMonster {
	my ( $id, $name, $point, $mName, $result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>����$mName</B>${result}",
		$id
	);
}

# �����ɸ�
sub logMonsSend {
	my ( $id, $tId, $name, $tName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>��¤����</B>���¤��${HtagName_}${tName}${AfterName}${H_tagName}�����ꤳ�ߤޤ�����",
		$id, $tId
	);
}

# ���������Ѱ�
sub logMonsC {
	my ( $id, $name, $point, $mName, $afmName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>����$mName</B>�������αƶ���<B>����$afmName</B>�������Ѱۤ��ޤ�����",
		$id
	);
}

# ���á��ɱһ��ߤ�Ƨ��
sub logMonsMoveDefence {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"<B>����$mName</B>��${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>����ã��<B>${lName}�μ������֤���ư����</B>",
		$id
	);
}

# ���á��ǥ��ȥ�åפ�Ƨ��
sub logMonsMoveDeathtrap {
	my ( $id, $name, $lName, $point, $mName, $result ) = @_;
	logOut(
"<B>����$mName</B>��${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>����ã��<B>${lName}</B>����ư��<B>����$mName</B>��${result}�ޤ�������",
		$id
	);
}

# ���á��ǥ��ȥ�åפ�Ƨ����̤ʤ�
sub logMonsMoveDeathtrapM {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"<B>����$mName</B>��${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>����ã��<B>${lName}</B>����ư���ޤ�����<B>����$mName</B>�ϲ�����̵���ä��褦��Ƨ�߹Ӥ餷�ޤ�������",
		$id
	);
}

# ���á�����
sub logMonsZIBAKU {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"<B>����$mName</B>��${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>�ذ�ư�����ݡ������Ĥ줿���Ȼפ��Ȱ쵤��<B>��ȯ���ޤ�������</B>",
		$id
	);
}

# ���á������򿩤�
sub logMonsEAT {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"<B>����$mName</B>��${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>�ذ�ư�����ݡ��������ۤɤε۰��Ϥ�������߿����Σ����ۤ����߿��٤Ƥ��ޤ��ޤ�����",
		$id
	);
}

# �������
sub logManipulate {
	my ( $id, $tId, $name, $tName, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${AfterName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",
		$id, $tId
	);
}

# ������� ���ƥ륹
sub logManipulateS {
	my ( $id, $tId, $name, $tName, $comName ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagName_}${tName}${AfterName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}��Ԥ��ޤ�����",
		$id, $tId
	);
	logLate(
"<B>���Ԥ�</B>��${HtagName_}${tName}${AfterName}${H_tagName}��${HtagComName_}${comName}${H_tagComName}��ԤäƤ���褦�Ǥ���",
		$tId
	);
}

#-----------�����ޤ�---------------

# �к�
sub logFire {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�к�${H_tagDisaster}�ˤ����Ǥ��ޤ�����",
		$id
	);
}

# �кҤ�̤�����ɤ�
sub logFireD {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>�ǽвФ��ޤ���������������γ����ˤ��кҤ�̤�����ɤ��ޤ�����",
		$id
	);
}

# ����
sub logOsen {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}����${H_tagDisaster}������Ǥ��ޤ�����",
		$id
	);
}

# ����೹
sub logslum {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>���Ϻ��ˤ��${HtagDisaster_}����೹${H_tagDisaster}���Ѳ����ޤ�����",
		$id
	);
}

# ��¢��

sub logMaizo {
	my ( $id, $name, $comName, $value ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}�Ǥ�${HtagComName_}$comName${H_tagComName}��ˡ�<B>$value$HunitMoney�����¢��</B>��ȯ������ޤ�����",
		$id
	);

	#��󥭥��ѥ��ե�����񤭽Ф�
	open( MOUT, ">>${HlogdirName}/money.log" );
	print MOUT "$HislandTurn,$id,��¢��,$value\n";
	close(MOUT);
}

# ���̮
sub logGold {
	my ( $id, $name, $comName, $value ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}�Ǥ�${HtagComName_}$comName${H_tagComName}��˶��̮ȯ����<B>$value$HunitMoney�����ζ�</B>���η�����ޤ�����",
		$id
	);

	#��󥭥��ѥ��ե�����񤭽Ф�
	open( MOUT, ">>${HlogdirName}/money.log" );
	print MOUT "$HislandTurn,$id,��¢��,$value\n";
	close(MOUT);
}

# ������

sub logGoldMonu {
	my ( $id, $name, $lName, $arg ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>$lName</B>���顢<B>${arg}��</B>�ζ⤬������ޤ�����",
		$id
	);
}

# �Ͽ�ȯ��
sub logEarthquake {
	my ( $id, $name, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}���絬�Ϥ�${HtagDisaster_}�Ͽ�${H_tagDisaster}��ȯ�������̸���${HtagName_}$point${H_tagName}�ն�����͡�",
		$id
	);
}

# �Ͽ��ﳲ
sub logEQDamage {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�Ͽ�${H_tagDisaster}�ˤ���ﳲ������ޤ�����",
		$id
	);
}

# �Ͽ̲���
sub logEQDestroy {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}��$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}�Ͽ�${H_tagDisaster}�ˤ����Ǥ��ޤ�����",
		$id
	);
}

# ������­�ﳲ
sub logSvDamage {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��<B>��������ƽ�̱������</B>��<B>$lName</B>�ϲ��Ǥ��ޤ�����",
		$id
	);
}

# ��������
sub logTsunamiDamage {
	my ( $id, $name, $lName, $point, $result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}����${H_tagDisaster}�ˤ��$result�ޤ�����",
		$id
	);
}

# ����ȯ��
sub logTyphoon {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagDisaster_}����${H_tagDisaster}��Φ����",
		$id
	);
}

# �����ﳲ
sub logTyphoonDamage {
	my ( $id, $name, $lName, $point, $result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}����${H_tagDisaster}��${result}�ޤ�����",
		$id
	);
}

# ��Ĭ�ﳲ
sub logAkasioDamage {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}��Ĭ${H_tagDisaster}�����Ǥ��ޤ�����",
		$id
	);
}

# �����ʥ��٥��
sub logEvent {
	logOut( "${HtagName_}$_[1]${AfterName}${H_tagName}$_[2]", $_[0] );
}

# �����ʥ��٥��
sub logEventT {
	logOut( "${HtagName_}$_[2]${AfterName}${H_tagName}$_[3]", $_[0], $_[1] );
}

# �����ʥ��٥��
sub logEventP {
	logOut( "${HtagName_}$_[1]${AfterName}$_[2]${H_tagName}$_[3]", $_[0] );
}

# �����ʥ��٥�ȣ�
sub logEvent2 {
	my ( $id, $name, $result, $result2 ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagDisaster_}${result}${H_tagDisaster}${result2}��",
		$id
	);
}

# ����ҳ����٥��(����)
sub logSpaceDisEvent {
	logOut( "${HtagName_}${SpaceName}$_[1]${H_tagName}��<B>$_[2]</B>$_[3]",
		$_[0], 999 );
}

# ���襤�٥��(����)
sub logSpaceEvent {
	logOut( "${HtagName_}${SpaceName}${H_tagName}$_[0]", 999 );
}

# ��С��ɤ�
sub logMeteoD {
	my ( $id, $name, $lName, $point, $kind ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}${kind}${H_tagDisaster}������ޤ������������ʤ��Ϥˤ�������ȯ���ޤ�����",
		$id
	);
}

# ��С���
sub logMeteoSea {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}������ޤ�����",
		$id
	);
}

# ��С���
sub logMeteoMountain {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}�����<B>$lName</B>�Ͼä����Ӥޤ�����",
		$id
	);
}

# ��С��������
sub logMeteoSbase {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}�����<B>$lName</B>���������ޤ�����",
		$id
	);
}

# ��С�����
sub logMeteoMonster {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"<B>����$lName</B>������${HtagName_}${name}${AfterName}$point${H_tagName}������${HtagDisaster_}���${H_tagDisaster}�����Φ�Ϥ�<B>����$lName</B>���Ȥ���פ��ޤ�����",
		$id
	);
}

# ��С�����
sub logMeteoSea1 {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}������${HtagDisaster_}���${H_tagDisaster}��������줬�������ޤ�����",
		$id
	);
}

# ��С�����¾
sub logMeteoNormal {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}������<B>$lName</B>��${HtagDisaster_}���${H_tagDisaster}��������Ӥ����פ��ޤ�����",
		$id
	);
}

# ��С�����¾
sub logHugeMeteo {
	my ( $id, $name, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}������${HtagDisaster_}�������${H_tagDisaster}�������",
		$id
	);
}

# ʮ��
sub logEruption {
	my ( $id, $name, $lName, $point, $erup ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}������${HtagDisaster_}�л���$erup${H_tagDisaster}��<B>$lName</B>��<B>��</B>�ˤʤ�ޤ�����",
		$id
	);
}

# ʮ�С�����
sub logEruptionSea1 {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ���Φ�Ϥˤʤ�ޤ�����",
		$id
	);
}

# ʮ�С���or����
sub logEruptionSea {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ��ǳ��줬δ���������ˤʤ�ޤ�����",
		$id
	);
}

# ʮ�С�����¾
sub logEruptionNormal {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}������<B>$lName</B>�ϡ�${HtagDisaster_}ʮ��${H_tagDisaster}�αƶ��ǲ��Ǥ��ޤ�����",
		$id
	);
}

# ��������ȯ��
sub logFalldown {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��${HtagDisaster_}��������${H_tagDisaster}��ȯ�����ޤ�������",
		$id
	);
}

# ���������ﳲ
sub logFalldownLand {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>�ϳ���������ߤޤ�����",
		$id
	);
}

# ���������ﳲ����

sub logFalldownLandO {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>�ϲ����Τ��߾夲�����ˤ�곤��������ߤޤ�����",
		$id
	);
}

# �����ﳲ������
sub logWideDamageSea {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>��<B>����</B>���ޤ�����",
		$id
	);
}

# �����ﳲ�����η���
sub logWideDamageSea2 {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>���׷���ʤ��ʤ�ޤ�����",
		$id
	);
}

# �����ﳲ�����ÿ���
sub logWideDamageMonsterSea {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��Φ�Ϥ�<B>����$lName</B>���Ȥ���פ��ޤ�����",
		$id
	);
}

# �����ﳲ������
sub logWideDamageMonster {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>����$lName</B>�Ͼä����Ӥޤ�����",
		$id
	);
}

# �����ﳲ������
sub logWideDamageWaste {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>�ϰ�֤ˤ���<B>����</B>�Ȳ����ޤ�����",
		$id
	);
}

# �����ﳲ������
sub logWideDamageOsen {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}��<B>$lName</B>������ǽ��<B>����</B>���ޤ�����",
		$id
	);
}

# �����ﳲ(����)
sub logWideDamageSpace {
	logOut(
"${HtagName_}${SpaceName}$_[1]${H_tagName}��<B>$_[0]</B>�ϰ�֤ˤ���<B>$_[2]</B>�ˤʤ�ޤ�����",
		999
	);
}

# ����
sub logPrize {
	my ( $id, $name, $pName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>$pName</B>����ޤ��ޤ�����",
		$id
	);
	logHistory(
		"${HtagName_}${name}${AfterName}${H_tagName}��<B>$pName</B>�����");
}

# ����޼���
sub logPrizeV {
	my ( $id, $name, $pName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>$pName</B>����ޤ��ޤ�����",
		$id
	);

	#��󥭥��ѥ��ե�����񤭽Ф�
	open( MOUT, ">>${HlogdirName}/bumon.log" );
	print MOUT "$HislandTurn,$id,$pName,$name\n";
	close(MOUT);
}

# �Ϸ��θƤ���
sub landName {
	my ( $land, $lv ) = @_;
	if ( $land == $HlandSea ) {
		if ( $lv >= 10 ) {
			return '�ܿ���';
		}
		elsif ( $lv == 1 ) {
			return '����';
		}
		else {
			return '��';
		}
	}
	elsif ( $land == $HlandWaste ) {
		return ( $lv >= 10 ) ? '����' : '����';
	}
	elsif ( $land == $HlandPlains ) {
		return 'ʿ��';
	}
	elsif ( $land == $HlandTown ) {
		if ( $lv < 30 ) {
			return '¼';
		}
		elsif ( $lv < 100 ) {
			return 'Į';
		}
		else {
			return '�Ի�';
		}
	}
	elsif ( $land == $HlandSlum ) {
		return '����೹';
	}
	elsif ( $land == $HlandForest ) {
		return '��';
	}
	elsif ( $land == $HlandFarm ) {
		return '����';
	}
	elsif ( $land == $HlandFactory ) {
		return '����';
	}
	elsif ( $land == $HlandTower ) {
		return '���ȥӥ�';
	}
	elsif ( $land == $HlandBase ) {
		return '�ߥ��������';
	}
	elsif ( $land == $HlandDefence ) {
		if ( $lv == 2 ) {
			return 'S�ɱһ���';
		}
		elsif ( $lv == 3 ) {
			return 'SS�ɱһ���';
		}
		elsif ( $lv == 10 ) {
			return 'ST�ɱһ���';
		}
		elsif ( $lv == 11 ) {
			return 'SST�ɱһ���';
		}
		elsif ( $lv == 20 ) {
			return '̸�դ��ɱһ���';
		}
		elsif ( $lv == 21 ) {
			return 'S̸�դ��ɱһ���';
		}
		else {
			return '�ɱһ���';
		}
	}
	elsif ( $land == $HlandMountain ) {
		return '��';
	}
	elsif ( $land == $HlandMonster ) {
		return ( monsterSpec($lv) )[1];
	}
	elsif ( $land == $HlandSbase ) {
		return '�������';
	}
	elsif ( $land == $HlandOil ) {
		if ( $lv == 5 ) {
			return '�����ɱһ���';
		}
		elsif ( $lv == 6 ) {
			return '����ǥ��ȥ�å�';
		}
		elsif ( $lv == 7 ) {
			return '������ɽ�';
		}
		elsif ( $lv >= 35 ) {
			return '�����Ի�';
		}
		elsif ( $lv >= 10 ) {
			return '��������';
		}
		else {
			return '��������';
		}
	}
	elsif ( $land == $HlandDeathtrap ) {
		return '�ǥ��ȥ�å�';
	}
	elsif ( $land == $HlandWindmill ) {
		return '����';
	}
	elsif ( $land == $HlandMyhome ) {
		return '�ޥ��ۡ���';
	}
	elsif ( $land == $HlandPort ) {
		return '��';
	}
	elsif ( $land == $HlandPolice ) {
		return '�ٻ���';
	}
	elsif ( $land == $HlandHospital ) {
		return '�±�';
	}
	elsif ( $land == $HlandFlower ) {
		if ( $lv == 13 ) {
			return '���ܥƥ�';
		}
		else {
			return '����';
		}
	}
	elsif ( $land == $HlandDokan ) {
		return '�ڴ�';
	}
	elsif ( $land == $HlandTrump ) {
		if ( ( $lv < 1 ) || ( $lv > 14 ) ) {
			return "�ȥ���΢";
		}
		else {
			if ( $lv == 14 ) {
				return "�ȥ��ץ��硼����";
			}
			else {
				return "�ȥ���${lv}";
			}
		}
	}
	elsif ( $land == $HlandSeisei ) {
		if ( $lv == 10 ) {
			return 'Ƽ������';
		}
		elsif ( $lv == 30 ) {
			return '��������';
		}
		else {
			return '��ú������';
		}
	}
	elsif ( $land == $HlandMegacity ) {
		if ( $lv == 1 ) {
			return '�����Իԡ�����';
		}
		elsif ( $lv == 2 ) {
			return '�����Իԡ���';
		}
		elsif ( $lv == 3 ) {
			return '�����Իԡ�����';
		}
		elsif ( $lv == 4 ) {
			return '�����Իԡ�����';
		}
		elsif ( $lv == 5 ) {
			return '�����Իԡ���';
		}
		elsif ( $lv == 6 ) {
			return '�����Իԡ�����';
		}
		else {
			return '�����Ի�';
		}
	}
	elsif ( $land == $HlandMegatower ) {
		if ( $lv == 1 ) {
			return '����ӥ������';
		}
		elsif ( $lv == 2 ) {
			return '����ӥ����';
		}
		elsif ( $lv == 3 ) {
			return '����ӥ������';
		}
		elsif ( $lv == 4 ) {
			return '����ӥ������';
		}
		elsif ( $lv == 5 ) {
			return '����ӥ����';
		}
		elsif ( $lv == 6 ) {
			return '����ӥ������';
		}
		else {
			return '����ӥ�';
		}
	}
	elsif ( $land == $HlandMegaFact ) {
		if ( $lv == 1 ) {
			return '���繩�������';
		}
		elsif ( $lv == 2 ) {
			return '���繩�����';
		}
		elsif ( $lv == 3 ) {
			return '���繩�������';
		}
		elsif ( $lv == 4 ) {
			return '���繩�������';
		}
		elsif ( $lv == 5 ) {
			return '���繩�����';
		}
		elsif ( $lv == 6 ) {
			return '���繩�������';
		}
		else {
			return '���繩��';
		}
	}
	elsif ( $land == $HlandMegaFarm ) {
		if ( $lv == 1 ) {
			return '�������������';
		}
		elsif ( $lv == 2 ) {
			return '�����������';
		}
		elsif ( $lv == 3 ) {
			return '�������������';
		}
		elsif ( $lv == 4 ) {
			return '�������������';
		}
		elsif ( $lv == 5 ) {
			return '�����������';
		}
		elsif ( $lv == 6 ) {
			return '�������������';
		}
		else {
			return '��������';
		}
	}
	elsif ( $land == $HlandHugecity ) {
		if ( $lv < 50 ) {
			return 'Ķ�����Ի�(�濴)';
		}
		elsif ( $lv < 60 ) {
			return 'Ķ�����Ի�(�Ի�)';
		}
		elsif ( $lv < 70 ) {
			return 'Ķ�����Ի�(����)';
		}
		elsif ( $lv < 80 ) {
			return 'Ķ�����Ի�(����)';
		}
		else {
			return 'Ķ�����Ի�(����)';
		}
	}
	elsif ( $land == $HlandFuji ) {
		return '�ٻλ�';
	}
	elsif ( $land == $HlandTcity ) {
		return '�����Ի�';
	}
	elsif ( $land == $HlandMonument ) {
		return $HmonumentName[$lv];
	}
	elsif ( $land == $HlandSMonument ) {
		return $HsmonumentName[$lv];
	}
	elsif ( $land == $HlandHaribote ) {
		return ( $lv == 0 ) ? '�ϥ�ܥ�' : ( monsterSpec($lv) )[1];
	}
	elsif ( $land == $HlandOsen ) {
		return '�����ھ�';
	}
	elsif ( $land == $HlandBank ) {
		return '���';
	}
	elsif ( $land == $HlandStadium ) {
		return '����������';
	}
	elsif ( $land == $HlandAmusement ) {
		return 'ͷ����';
	}
	elsif ( $land == $HlandCasino ) {
		return '������';
	}
	elsif ( $land == $HlandPark ) {
		return '����';
	}
	elsif ( $land == $HlandSchool ) {
		return '�ع�';
	}
	elsif ( $land == $HlandDome ) {
		return '�ɡ���';
	}
	elsif ( $land == $HlandAirport ) {
		return '����';
	}
	elsif ( $land == $HlandZoo ) {
		return 'ưʪ��';
	}
	elsif ( $land == $HlandBigcity ) {
		return '���Ի�';
	}
	elsif ( $land == $HlandExpo ) {
		return '������';
	}
	elsif ( $land == $HlandWarp ) {
		return 'ž������';
	}
	elsif ( $land == $HlandWarpR ) {
		return 'ž��������';
	}
	elsif ( $land == $HlandBreakwater ) {
		return '������';
	}
	elsif ( $HseaChk[$land] == 2 ) {

		# ����
		my ($sId) = ( shipSpec($lv) )[2];
		if ( $sId > 0 ) {
			return $HshipName[ $land - $HlandPirate ]
			  . "(${HidToName{$sId}}${AfterName}��°)";
		}
		else {
			return $HshipName[ $land - $HlandPirate ];
		}
	}
	elsif ( $land == $HlandFire ) {
		return ( $lv >= 10 ) ? 'S���ɽ�' : '���ɽ�';
	}
	elsif ( $land == $HlandKInora ) {
		return '���ۤ��Τ�';
	}
	elsif ( $land == $HlandEarth ) {
		return '�ϵ�';
	}
	elsif ( $land == $HlandSunit ) {
		if ( $lv == 20 ) {
			return '�����˲���˥å�';
		}
		elsif ( $lv == 1 ) {
			return '����������˥å�';
		}
		elsif ( $lv == 10 ) {
			return '�����˥å�';
		}
		else {
			return '������å�˥å�';
		}
	}
	elsif ( $land == $HlandSCity ) {
		if ( $lv < 30 ) {
			return '����¼';
		}
		elsif ( $lv < 100 ) {
			return '����Į';
		}
		else {
			return '�����Ի�';
		}
	}
	elsif ( $land == $HlandSFarm ) {
		return '��������';
	}
	elsif ( $land == $HlandSFactory ) {
		return '���蹩��';
	}
	elsif ( $land == $HlandSAEisei ) {
		return $HsEisei[ int( $lv / 1000 ) ];    # �������
	}
	elsif ( $land == $HlandSpaceBase ) {
		return '����ߥ��������';
	}
	elsif ( $land == $HlandSDefence ) {
		return '�����ɱһ���';
	}
}

# ����η׻�
sub spaceEstimate {
	my ($mode) = @_;
	my ( $land, $landValue, $dis, $nation ) = (
		$Hspace->{'land'},       $Hspace->{'landValue'},
		$Hspace->{'landValue2'}, $Hspace->{'nation'}
	);
	my ( $pop, $area, $farm, $factory ) = ( 0, 0, 0, 0 );
	my ( $x, $y, $kind, $value, $id );

	if ( $mode == 0 ) {

		# ������
		$Hsolarwind = 0;
		if ( $Hspace->{'solarwind'} < 10 ) {
			$Hspace->{'solarwind'} = $HislandTurn + random(30) + 30;
		}
		elsif ( $Hspace->{'solarwind'} < $HislandTurn - 8 ) {

		 #			HdebugOut("��������������в�:" . $Hspace->{'solarwind'});
			if ( random(5) == 0 ) {

				# ��������λ
				logSpaceEvent("�������������ޤ�ޤ�����");
				$Hspace->{'solarwind'} = $HislandTurn + random(30) + 30;
			}
			else {
				$Hsolarwind = 1;
			}
		}
		elsif ( $Hspace->{'solarwind'} <= $HislandTurn ) {

			#			HdebugOut("������ȯ����:" . $Hspace->{'solarwind'});
			$Hsolarwind = 1;

#			logSpaceEvent("�����������㤷���᤭�Ӥ�Ƥ��ޤ������ޤ�ޤǰ��ڤα��賫ȯ���Ǥ��ޤ���");
		}
	}
	for ( $y = 0 ; $y < $HislandSize ; $y++ ) {
		for ( $x = 0 ; $x < $HislandSize ; $x++ ) {
			$kind  = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			$id    = $nation->[$x][$y];
			if ( ( $kind == $HlandSea ) || ( $kind == $HlandEarth ) ) {
				$nation->[$x][$y] = 0;
				$dis->[$x][$y]    = 0;
			}
			else {
				$area++;
			}
			my ($tn) = $HidToNumber{$id};
			$nation->[$x][$y] = 0 if ( $tn eq '' );
			my ($island) = $Hislands[$tn];

			if ( ( $mode == 1 ) && ( $Hsolarwind == 0 ) ) {

				# �����
				my ($di)    = 0;
				my ($tName) = $island->{'name'};
				if ( $tn ne '' ) {
					my ($spop) = int( $island->{'spop'} );
					if ( $island->{'pop'} < $spop * 3 ) {
						$di = 7;
					}
					elsif ( $island->{'pop'} < $spop * 4 ) {
						$di = 3;
					}
					elsif ( $island->{'pop'} < $spop * 5 ) {
						$di = 1;
					}
					elsif ( $spop < 1 ) {
						$di = 3;
					}
					if ( $island->{'sfarm'} != 1 ) {
						$di += 4;
					}
					if ( $island->{'comsfood'} ) {
						$di -= 6;
					}
					my ($damage) =
					  $island->{'oldPop'} -
					  ( $island->{'pop'} + $island->{'displus'} );
					if ( $damage >= 3000 ) {
						$di += 24;
					}
					elsif ( $damage >= 1000 ) {
						$di += 18;
					}
					elsif ( $damage >= 400 ) {
						$di += 12;
					}
					elsif ( $damage >= 200 ) {
						$di += 8;
					}
					elsif ( $damage >= 70 ) {
						$di += 4;
					}
					elsif ( $damage >= 30 ) {
						$di += 2;
					}
					elsif ( $damage > -50 ) {
						$di -= 3;
					}
					elsif ( $damage > -100 ) {
						$di -= 6;
					}
					elsif ( $damage > -200 ) {
						$di -= 10;
					}
					else {
						$di -= 15;
					}
					if ( $id == $island->{'id'} ) {
						$dis->[$x][$y] += $di;
					}
				}

#				HdebugOut("�͸��Ͼ屧����� (${di})(" . $island->{'oldPop'} . ")(" . $island->{'pop'} . ")(" . $island->{'spop'} . ")${tName}${AfterName}") if($tn ne '');
			}

			if ( ( $island->{'dead'} == 1 ) || ( $island->{'pop'} <= 0 ) ) {

				# ���������Ȥ��������礬�Ǥ����
				$tn = "";
				$nation->[$x][$y] = 0;
				$dis->[$x][$y] -= 30;
				$dis->[$x][$y] = 0 if ( $dis->[$x][$y] < 0 );
			}

			if ( $kind == $HlandSCity ) {
				$value = 200 if ( $value > 200 );
				$pop += $value;
				if ( $tn ne '' ) {

# ����ο͸�����ͤ�����͸���­����ϫƯ�ϤȤ��ˤʤ�ʤ�)
					if ( $mode == 1 ) {

						# ��λ����
						#						HdebugOut("��λ���� �͸��׻�");
						$island->{'popspace'} += $value;
					}
					else {

						# ���Ͻ���
						#						HdebugOut("���Ͻ��� �͸��׻�");
						$island->{'spop'}  += $value;
						$island->{'spop2'} += $value * $HspaceEfficiency;
					}
					$island->{'spa'} += $value + 20;
				}
				else {
					$nation->[$x][$y] = 0;
				}
			}
			elsif ( $kind == $HlandSunit ) {
				if ( $mode == 0 ) {

					# ����˷��ߤ��ʤ�
					if ( $landValue->[$x][$y] == 0 ) {
						$landValue->[$x][$y] = 1;
					}
					elsif ( $landValue->[$x][$y] == 20 ) {
					}
					else {
						$landValue->[$x][$y] = 10;
					}
				}
				$island->{'spa'} += 20 if ( $tn ne '' );
			}
			elsif ( $kind == $HlandSFarm ) {
				$farm += $value;
				if ( $tn ne '' ) {
					$island->{'sfarm'} = 1;
					$island->{'spa'} += $value * 5;
				}
				else {
					$nation->[$x][$y] = 0;
				}
			}
			elsif ( $kind == $HlandSFactory ) {
				$factory += $value;
				if ( $tn ne '' ) {
					$island->{'sfactory'} = 1;
					$island->{'spa'} += $value * 5;
				}
				else {
					$nation->[$x][$y] = 0;
				}
			}
			elsif ( ( $kind == $HlandSAEisei ) && ( $Hsolarwind == 0 ) ) {

				# �������
				if ( $tn ne '' ) {
					$island->{'spa'} += ( $value % 1000 ) * 2;
					my $nkind = 'eis' . int( $value / 1000 );
					$island->{$nkind} = 1;
				}
				else {
					$nation->[$x][$y] = 0;
				}
			}
			elsif ( $kind == $HlandSpaceBase ) {
				$island->{'spa'} += 150 if ( $tn ne '' );
			}
			elsif ( $kind == $HlandSDefence ) {
				$island->{'spa'} += 120 if ( $tn ne '' );
			}
			elsif ( $kind == $HlandMonster ) {
				$island->{'spacemonster'}++;
			}

			# �۾��ͤ�������ͤ�����
			if ( $land->[$x][$y] == $HlandMonster ) {
				if ( $landValue->[$x][$y] > 4000 ) {
					$land->[$x][$y]      = $HlandSunit;
					$landValue->[$x][$y] = 10;
					$dis->[$x][$y]       = 0;
					$nation->[$x][$y]    = 0;
				}
			}
			elsif ($landValue->[$x][$y] > 500
				&& $land->[$x][$y] != $HlandSAEisei )
			{
				$land->[$x][$y]      = $HlandSunit;
				$landValue->[$x][$y] = 10;
				$dis->[$x][$y]       = 0;
				$nation->[$x][$y]    = 0;
			}
			if ( $dis->[$x][$y] < 0 ) {
				$dis->[$x][$y] = 0;
			}
			elsif ( $dis->[$x][$y] > 200 ) {
				$dis->[$x][$y] = 200;
			}
		}
	}
	$Hspace->{'area'}    = $area;
	$Hspace->{'pop'}     = $pop;
	$Hspace->{'farm'}    = $farm;
	$Hspace->{'factory'} = $factory;

	if ( $mode == 0 ) {

		# �������
		# �����Ⱦ���
		$Hspace->{'foodP'} = $farm * 10;
		$Hspace->{'foodC'} = int( $pop * $HeatenFood );
		$Hspace->{'food'} += $Hspace->{'foodP'};

		# ��������
		$Hspace->{'food'} -= $Hspace->{'foodC'};
	}
	else {

		# ���������Ƥ����饫�åȤ���
		if ( $Hspace->{'food'} > $MaxFood ) {
			$Hspace->{'food'} = $MaxFood;
		}
		my @idx = ( 0 .. $#Hislands );
		@idx = sort {
			     $Hislands[$b]->{'spa'} <=> $Hislands[$a]->{'spa'}
			  || $a <=> $b
		} @idx;
		my $tIsland = $Hislands[ $idx[0] ];
		if ( $tIsland->{'spa'} > 0 ) {
			if ( ( $HislandTurn % $HturnPrizeVarious ) == 0 ) {

				# ����� ���貦
				$tIsland->{'status'} |= 4096;
				$tIsland->{'zyuni'} += $HturnPrizePoint;
				logPrizeV( $tIsland->{'id'}, $tIsland->{'name'}, $HprizeV[13] );
			}
			my ( @space, $i );
			for ( $i = 0 ; $i <= $#Hislands ; $i++ ) {
				push( @space, $Hislands[ $idx[$i] ]->{'id'} );
				push( @space, $Hislands[ $idx[$i] ]->{'spa'} );
			}

#			HdebugOut("$space[0],$space[1],$space[2],$space[3],$space[4],$space[5],$space[6],$space[7],$space[8],$space[9]");
			$Hspace->{'space'} =
"$space[0],$space[1],$space[2],$space[3],$space[4],$space[5],$space[6],$space[7],$space[8],$space[9]";
		}
		else {
			$Hspace->{'space'} = 0;
		}
	}
}

# ������Ĺ�����ñ�إå����ҳ�
sub spaceHex {
	my ( $land, $landValue, $dis, $nation ) = (
		$Hspace->{'land'},       $Hspace->{'landValue'},
		$Hspace->{'landValue2'}, $Hspace->{'nation'}
	);
	my ( $pop1, $pop2, $pop3, $di ) = ( 18, 9, 3, 0 );

	#	if($Hspace->{'food'} < 0){
	#		# ������­
	#		$pop1 -= 24;
	#		$pop2 -= 22;
	#		$pop3 -= 20;
	# 		$Hspace->{'food'} = 0;
	#	}
	my ( $x, $y, $i, @spaceMove );
	my ($p) =
	  ( $island->{'spacemonster'} > 0 )
	  ? $HdisSpaceMonster1
	  : $HdisSpaceMonster2;
	for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
		$x = $Hrpx[$i];
		$y = $Hrpy[$i];
		my ( $kind, $lv, $id ) =
		  ( $land->[$x][$y], $landValue->[$x][$y], $nation->[$x][$y] );

		my ($tn)     = $HidToNumber{$id};
		my ($island) = $Hislands[$tn];

		# ����
		if (   ( $id > 0 )
			&& ( ( $kind == $HlandSFarm ) || ( $kind == $HlandSFactory ) ) )
		{
			if ( $island->{'spop2'} > $lv ) {
				$island->{'money'} += $lv * $HspaceIncome;
				$island->{'spop2'} -= $lv;
			}
			else {
				$island->{'money'} += $island->{'spop2'} * $HspaceIncome;
				$island->{'spop2'} = 0;
			}
		}

		# ��Ĺ
		if ( $kind == $HlandSCity ) {
			if (   ( random($p) < $Hspace->{'area'} )
				&& ( $Hsolarwind == 0 )
				&& ( $HdisMonster > 0 ) )
			{

				# ���ý���
				my ( $lv, $kind );
				if ( $Hspace->{'area'} < 80 ) {
					$kind = $HmonsterS[0];
				}
				else {
					$kind = $HmonsterS[ random( $#HmonsterS + 1 ) ];
				}
				$lv = $kind * 100 + $HmonsterBHP[$kind] +
				  random( $HmonsterDHP[$kind] );

				logMonsComeSpace( ( monsterSpec($lv) )[1],
					"($x, $y)",
					landName( $land->[$x][$y], $landValue->[$x][$y] ) );
				$land->[$x][$y]      = $HlandMonster;
				$landValue->[$x][$y] = $lv;
			}
			else {
				if ( $lv < 100 ) {
					$lv += random($pop1);
				}
				elsif ( $lv < 150 ) {
					$lv += random($pop2);
				}
				else {
					$lv += random($pop3);
				}
				if ( $lv > 200 ) {
					$landValue->[$x][$y] = 200;
				}
				elsif ( $lv <= 0 ) {
					$land->[$x][$y]      = $HlandSunit;
					$landValue->[$x][$y] = 10;
				}
				else {
					$landValue->[$x][$y] = $lv;

				}
			}
		}
		elsif ( $kind == $HlandSAEisei ) {

			# �������
			if ( $lv % 1000 > 0 ) {
				my $e = int( $lv / 1000 );
				if ( $e == 4 && $island->{'eis4'} > 1 ) {
					if ( $lv % 1000 < $island->{'eis4'} ) {
						$landValue->[$x][$y] = 4000;
					}
					else {
						$landValue->[$x][$y] -=
						  $island->{'eis4'};    # ���ͥ륮������
					}
					$island->{'eis4'} = 1;
				}
				else {
					$landValue->[$x][$y]--;     # ���ͥ륮������
				}
				$island->{'money'} -= ( $e + 1 ) * 50;
				if ( $island->{'money'} < 0 ) {
					$island->{'money'} = 0;
					$landValue->[$x][$y] = 0;
				}
			}
			else {
				logSpaceDisEvent(
					$id,
					"($x, $y)",
					landName( $land->[$x][$y], $landValue->[$x][$y] ),
					"����ǳ���ڤ���ϵ�˸����߲����ޤ�����"
				);
				$land->[$x][$y]      = $HlandSea;
				$landValue->[$x][$y] = 0;
				$dis->[$x][$y]       = 0;
				$nation->[$x][$y]    = 0;

				# �Ͼ�����Ψ���åפϤ��ʤ���
				#	$HdisMeteo += 80; # ����+8%
			}
		}
		elsif ( ( $kind == $HlandMonster ) && ( $Hsolarwind == 0 ) ) {

			# ����
			# �����Ǥμ��Ф�
			my ( $mKind, $mName, $mHp ) = monsterSpec( $landValue->[$x][$y] );
			my ($special) = $HmonsterSpecial[$mKind];

			next if ( $spaceMove[$x][$y] >= 2 );    # ���Ǥ�ư������

			# ��ư����
			my ( $sx, $sy ) = monmove( $Hspace, $x, $y, 3 );

			# ��ư�Ѥߥե饰
			if ( $HmonsterSpecial[$mKind] == 2 ) {

				# ��ư�Ѥߥե饰��Ω�Ƥʤ�
			}
			elsif ( $HmonsterSpecial[$mKind] == 1 ) {

				# ®������
				$spaceMove[$sx][$sy] = $spaceMove[$x][$y] + 1;
			}
			else {

				# ���̤β���
				$spaceMove[$sx][$sy] = 2;
			}
		}
		elsif ( ( $kind == $HlandSFactory ) && ( $dis->[$x][$y] > 30 ) ) {
			if (   ( random(1000000) < $HdisSHugeMeteo * $Hspace->{'area'} )
				&& ( $Hsolarwind == 0 ) )
			{

				# �������
				logSpaceDisEvent( $id, "($x, $y)", landName( $kind, $lv ),
"�ն�Ƕ��֤��Ĥ���Ȼפ��������������Ф��и����ޤ�������"
				);
				wideDamageSpace( $id, $land, $landValue, $dis, $nation, $x, $y,
					7, 1 );
			}
		}
		elsif ( ( $kind == $HlandSunit ) && ( $lv == 10 ) ) {
			if ( random(10) == 0 ) {

				# ��������줢��С�������Į�ˤʤ�
				if ( countGrow( $land, $landValue, $x, $y ) ) {
					$land->[$x][$y]      = $HlandSCity;
					$landValue->[$x][$y] = 1;
					$dis->[$x][$y]       = 10;
				}
			}
		}

		# ��������ư
		if ( $kind == $HlandSunit ) {
			$dis->[$x][$y] = 20;
		}
		elsif ( $id > 0 ) {

		}
		else {
			$dis->[$x][$y] -= 4;
		}
		if ( ( $dis->[$x][$y] > 30 ) && ( $id > 0 ) ) {

			# ��������Ŀͤˤ��˪�����٥��
			my ($p);
			if ( $dis->[$x][$y] < 45 ) {
				$p = 1;
			}
			elsif ( $dis->[$x][$y] < 60 ) {
				$p = 3;
			}
			elsif ( $dis->[$x][$y] < 100 ) {
				$p = 8;
			}
			else {
				$p = 20;
			}
			if ( random(100) < $p ) {
				logSpaceDisEvent(
					$id,
					"($x, $y)",
					landName( $land->[$x][$y], $landValue->[$x][$y] ),
					"�������Ƥ�˪��������Ω���ޤ�����"
				);
				$dis->[$x][$y] -= 25;
				$nation->[$x][$y] = 0;

				# ���Ϥ������٤�夲��
				my ( $j, $sx, $sy );
				for ( $j = 1 ; $j < 7 ; $j++ ) {
					$sx = $x + $ax[$j];
					$sy = $y + $ay[$j];
					$sx--
					  if ( !( $sy % 2 ) && ( $y % 2 ) )
					  ;    # �Ԥˤ�����Ĵ��
					if (   ( $sx < 0 )
						|| ( $sx >= $HislandSize )
						|| ( $sy < 0 )
						|| ( $sy >= $HislandSize ) )
					{
					}
					elsif ( $nation->[$sx][$sy] == $id ) {

	 #						HdebugOut("���Ϥ������� Ʊ����°:" . $nation->[$sx][$sy]);
						$dis->[$sx][$sy] += 10;
					}
					elsif ( $nation->[$sx][$sy] > 0 ) {

	 #						HdebugOut("���Ϥ������� �㤦��°:" . $nation->[$sx][$sy]);
						$dis->[$sx][$sy] -= 5;
					}
				}
			}
		}
	}
}

# ������Ĺ�����ñ�إå����ҳ�
sub oceanHex {
	$wHislandSize = $HislandSize;
	$HislandSize  = $HoceanSize;
	my ( $land, $landValue, $dis, $nation ) = (
		$Hocean->{'land'},       $Hocean->{'landValue'},
		$Hocean->{'landValue2'}, $Hocean->{'nation'}
	);
	my ( $x, $y, $i, @oceanMove );
	for ( $i = 0 ; $i < $HpointOcean ; $i++ ) {
		$x = $HrpxO[$i];
		$y = $HrpyO[$i];
		my ( $kind, $lv, $id ) =
		  ( $land->[$x][$y], $landValue->[$x][$y], $nation->[$x][$y] );

		my ($tn)     = $HidToNumber{$id};
		my ($island) = $Hislands[$tn];
		if ( $kind == $HlandSea ) {
			if ( ( random($HdisSeaMonster) == 0 ) && ( $HdisMonster > 0 ) ) {

				# ���ý���
				my ( $lv, $kind );
				$kind = ( random(2) ) ? 9 : 21;
				$lv = $kind * 100 +
				  ( $HmonsterBHP[$kind] + random( $HmonsterDHP[$kind] ) ) * 3;
				logMonsComeOcean( ( monsterSpec($lv) )[1],
					"($x, $y)",
					landName( $land->[$x][$y], $landValue->[$x][$y] ) );
				$land->[$x][$y]      = $HlandMonster;
				$landValue->[$x][$y] = $lv;
			}
		}
		elsif ( $kind == $HlandMonster ) {

			# ����
			# �����Ǥμ��Ф�
			my ( $mKind, $mName, $mHp ) = monsterSpec( $landValue->[$x][$y] );
			my ($special) = $HmonsterSpecial[$mKind];
			next if ( $oceanMove[$x][$y] >= 2 );    # ���Ǥ�ư������

			# ��ư����
			my ( $sx, $sy ) = monmove( $Hocean, $x, $y, 4 );

			# ��ư�Ѥߥե饰
			if ( $HmonsterSpecial[$mKind] == 2 ) {

				# ��ư�Ѥߥե饰��Ω�Ƥʤ�
			}
			elsif ( $HmonsterSpecial[$mKind] == 1 ) {

				# ®������
				$oceanMove[$sx][$sy] = $oceanMove[$x][$y] + 1;
			}
			else {

				# ���̤β���
				$oceanMove[$sx][$sy] = 2;
			}
		}
	}
	$HislandSize = $wHislandSize;
}

# �͸�����¾���ͤ򻻽�(��ٷڸ��Τ���ʬ���Ƥߤ������ɤ��ޤ��̣���ʤ��ä�)
sub estimateS {
	my (
		$pop,     $popsea,   $area,   $factory,  $tower,
		$slum,    $forest,   $kaitei, $MissileK, $oil,
		$myhome,  $port,     $tenki,  $treasure, $fishShip,
		$titanic, $monsship, $aegis,  $oilfactory
	  )
	  = ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 );

	# �Ϸ������
	my ($island) = $Hislands[ $_[0] ];
	my ( $land, $landValue, $id ) =
	  ( $island->{'land'}, $island->{'landValue'}, $island->{'id'} );

	# �������
	if ( $island->{'kaisi'} == 0 ) {
		my $zanteisturn = $HislandTurn - $island->{'turnsu'} * 3;
		$zanteisturn = 1 if ( $zanteisturn < 1 );
		$island->{'kaisi'} = $zanteisturn;
	}

	# ������

	my ( $x, $y, $kind, $value, $i );
	for ( $y = 0 ; $y < $HislandSize ; $y++ ) {
		for ( $x = 0 ; $x < $HislandSize ; $x++ ) {
			$kind  = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			$area++ if ( $HseaChk[$kind] == 0 );    # ���ϤǤʤ��Ȥ�

			if (   ( $kind == $HlandSbase )
				|| ( $kind == $HlandOil )
				|| ( $kind == $HlandSMonument ) )
			{
				$kaitei++;
			}
			elsif ( $HseaChk[$kind] == 2 ) {

				# ����
				my ( $order, $hp, $sId ) = shipSpec($value);
				if ( $HpunishInfo{$id}->{punish} == 9 ) {

					# ���������Խ���
					if ( $sId > 0 ) {
						shipComeBack( $sId, $kind, $value );
						my ( $land2, $landValue2 ) =
						  ( $island->{'land2'}, $island->{'landValue2'} );
						$land->[$x][$y]       = $land2->[$x][$y];
						$landValue->[$x][$y]  = $landValue2->[$x][$y];
						$land2->[$x][$y]      = $HlandSea;
						$landValue2->[$x][$y] = 0;
					}
				}
				elsif ( $kind == $HlandTreasureS ) {
					$treasure++;    # ����
				}
				elsif (( $kind == $HlandFishSShip )
					|| ( $kind == $HlandFishMShip )
					|| ( $kind == $HlandFishLShip )
					|| ( $kind == $HlandTitanic ) )
				{
					$fishShip++;    # ������������

					$titanic++ if ( $kind == $HlandTitanic );    # ��ڵ���
				}
				elsif (( $kind == $HlandMonsShip )
					|| ( $kind == $HlandAegisShip )
					|| ( $kind == $HlandProbeShip ) )
				{
					$fishShip++;
					if (   ( $kind == $HlandMonsShip )
						&& ( $order == 0 )
						&& ( $sId == $id ) )
					{

						# ������Ƥ��

					  #						HdebugOut("����$order���ɣ�$sId��ɣ�$id");
						$monsship += 5;
					}
					elsif (( $kind == $HlandAegisShip )
						&& ( $order == 0 )
						&& ( $sId == $id ) )
					{

						# ����������
						$aegis += 5;
					}
				}
				elsif ( ( $kind == $HlandPirate ) && ( $sId != $id ) ) {

					# ��±��
					slideBack( $island->{'command'}, 0, $HcomSpecialSPP, $id,
						$x, $y, 5 );
				}
				next;
			}

			if ( $kind == $HlandTown ) {

				# Į
				$value = 200 if ( $value > 200 );
				$pop += $value;
			}
			elsif ( ( $kind == $HlandOil ) && ( $value >= 35 ) ) {

				# �����Ի�
				$popsea += $value;
			}
			elsif ( ( $kind == $HlandOil ) && ( $value == 0 ) ) {

				# ����
				$oil++;
			}
			elsif (( $kind == $HlandForest )
				|| ( $kind == $HlandMonument )
				|| ( $kind == $HlandSMonument )
				|| ( $kind == $HlandFlower )
				|| ( $kind == $HlandPark ) )
			{

				# ������ǰ��ϡ����ࡢ����
				$forest++;
			}
			elsif ( $kind == $HlandTower ) {

				# ���ȥӥ�
				$tower += $value;
			}
			elsif ( ( $kind == $HlandAirport ) || ( $kind == $HlandExpo ) ) {

				# ������������
				$tower += 50;
			}
			elsif ( $kind == $HlandPort ) {

				# ��
				$port += $value;
			}
			elsif ( $kind == $HlandFactory ) {

				# ����
				$factory += $value;
			}
			elsif ( $kind == $HlandMegacity ) {

				# �����Ի�
				if ( megaAround( $land, $landValue, $x, $y, $kind, $value ) ) {
					$pop += 300;
				}
				else {
					$land->[$x][$y]      = $HlandTown;
					$landValue->[$x][$y] = 190;
					$pop += 190;
				}
			}
			elsif ( $kind == $HlandHugecity ) {

				# Ķ�����Ի�
				if ( $value < 60 ) {
					$pop += 400;
				}
				elsif ( $value < 70 ) {
					$factory += 200;
				}
				elsif ( $value < 80 ) {
					$tower += 300;
				}
			}
			elsif ( $kind == $HlandMonster ) {

				# ����
				$island->{'monsmgmflg'} = 1;
				my $mKind = ( monsterSpec($value) )[0];
				if ( $mKind == 28 ) {

					# �Ƥ�Ƥ뤤�Τ�
					$tenki--;
				}
				elsif ( $mKind == 29 ) {

					# �դ��Ƥ�Ƥ�
					$tenki++;
				}
				elsif (( $HmonsterSpecial[$mKind] == 6 )
					|| ( $HmonsterSpecial[$mKind] == 7 ) )
				{

					# ��˰�ư������ä�����
					$island->{'smons'} = 1;
				}
				if ( $HmonsterDestroy[$mKind] == $HlandSea ) {

					# ����
					slideBack( $island->{'command'}, 0, $HcomSpecialSPP, $id,
						$x, $y, 5 );
				}
			}
			elsif ( $kind == $HlandSlum ) {

				# ����೹
				if ( $value < 130 ) {
					$slum += $value;
				}
				else {    # ���̤��ԻԤ����
					$land->[$x][$y] = $HlandTown;
					$pop += $value;
				}
			}
			elsif ( $kind == $HlandTcity ) {

				# �����Ի�
				$tower += 200;
				$pop   += 300;
			}
			elsif ( $kind == $HlandMegatower ) {

				# ����ӥ�
				if ( megaAround( $land, $landValue, $x, $y, $kind, $value ) ) {
					$tower += 300;
				}
				else {
					$land->[$x][$y]      = $HlandTower;
					$landValue->[$x][$y] = 190;
					$tower += 190;
				}
			}
			elsif ( $kind == $HlandMegaFact ) {

				# ���繩��
				if ( megaAround( $land, $landValue, $x, $y, $kind, $value ) ) {
					$factory += 200;
				}
				else {
					$land->[$x][$y]      = $HlandFactory;
					$landValue->[$x][$y] = 90;
					$factory += 90;
				}
			}
			elsif ( $kind == $HlandBigcity ) {

				# ���Ի�
				$pop += 1000;
			}
			elsif (( $kind == $HlandDefence )
				|| ( ( $kind == $HlandOil ) && ( $value == 5 ) ) )
			{

				# �ɱһ���
				$island->{'defence'} = 1;
			}
			elsif ( $kind == $HlandMyhome ) {

				# �ޥ��ۡ���
				$island->{'myhome'} = 1;
			}
			elsif ( $kind == $HlandPolice ) {

				# �ٻ���
				$island->{'Police'} = 1;
			}
			elsif ( $kind == $HlandHospital ) {

				# �±�
				$island->{'Hospital'} = 1;
			}
			elsif ( $kind == $HlandFuji ) {

				# �ٻλ�
				$island->{'event'} += 2;
			}
			elsif ( $kind == $HlandTrump ) {

				# �ȥ���
				$island->{'trump'}->[$value] = 1;
			}
		}
	}

	# �ϲ�
	my ( $ugL, $ugV, $ugX, $ugY ) =
	  ( $island->{'ugL'}, $island->{'ugV'}, $island->{'ugX'},
		$island->{'ugY'} );
	for ( $i = 0 ; $i < $HugMax ; $i++ ) {
		next
		  if ( $land->[ $ugX->[$i] ][ $ugY->[$i] ] != $HlandDokan )
		  ;    # �и�̵��
		for ( $x = 0 ; $x < 9 ; $x++ ) {
			if ( $ugL->[$i][$x] == $HugTosi ) {
				$pop += $ugV->[$i][$x];
			}
			elsif ( $ugL->[$i][$x] == $HugFarm ) {

				# ���⤷�ʤ�
			}
			elsif ( $ugL->[$i][$x] == $HugFact ) {
				$factory += $ugV->[$i][$x];
			}
			elsif ( $ugL->[$i][$x] == $HugKiti ) {

				# ���⤷�ʤ�
			}
			elsif ( $ugL->[$i][$x] == $HugOil ) {
				$oilfactory += $ugV->[$i][$x];
			}
		}
	}

	$pop += $slum;
	$island->{'kaiteipop'} = 1
	  if ( $pop < $popsea );    # ����ο͸�����¿����
	$pop += $popsea;

	if (   ( ( $factory + $port + $oilfactory ) * 2 < $tower )
		&& ( $pop >= 2000 ) )
	{
		$island->{'towerD'} = 1001 + $tower - $factory - $port;
	}
	elsif ( ( $tower == 0 ) && ( $pop >= 2000 ) ) {
		$island->{'towerD'} = 1000;
	}

	# ����
	$island->{'pop'}      = $pop;
	$island->{'slum'}     = $slum;
	$island->{'port'}     = $port;
	$island->{'factory'}  = $factory;
	$island->{'tower'}    = $tower;
	$island->{'tenki'}    = $tenki;
	$island->{'treasure'} = $treasure;
	$island->{'fishShip'} = $fishShip;
	$island->{'titanic'}  = $titanic;
	$island->{'oilfield'} = $oil;
	$island->{'kaitei'} = int( $kaitei * 100 / ( $HpointNumber + 1 - $area ) );
	$island->{'forest'} =
	  ( $area == 0 ) ? 7 : int( $forest * 100 / $area );    # Φ��̵����
	$island->{'monsship'} = $monsship;
	$island->{'aegis'}    = $aegis;

	$island->{'oilfactory'} = $oilfactory;

	$island->{'ship'} = 0;                                  # �����

	# ����񻺤�����
	$island->{'spa'}      = 0;
	$island->{'popspace'} = 0;
}

sub estimateE {
	my (
		$pop,    $popsea,   $area,     $farm,   $factory,
		$tower,  $mountain, $yousyoku, $forest, $forestV,
		$flower, $kaitei,   $MissileK, $mons,   $haribote,
		$oil,    $myhome,   $port,     $tenki,  $monument
	  )
	  = ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 );

	# �Ϸ������
	my ($island) = $Hislands[ $_[0] ];
	my ( $land, $landValue, $land2, $landValue2, $nation, $id ) = (
		$island->{'land'},       $island->{'landValue'}, $island->{'land2'},
		$island->{'landValue2'}, $island->{'nation'},    $island->{'id'}
	);
	my (%LandCount);

	# ������
	my ( $x, $y, $kind, $value, $i );
	for ( $y = 0 ; $y < $HislandSize ; $y++ ) {
		for ( $x = 0 ; $x < $HislandSize ; $x++ ) {
			$kind  = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			$LandCount{ $nation->[$x][$y] }++;
			if ( ( $HislandTurn % $HturnPrizeUnit ) == 0 ) {
				if ( $nation->[$x][$y] > 0 ) {
					my $tIsland =
					  $Hislands[ $HidToNumber{ $nation->[$x][$y] } ];
					$tIsland->{'winP'}++;
					$island->{'loseP'}++
					  if ( $nation->[$x][$y] != $island->{'id'} );
				}
				$nation->[$x][$y] = 0;    # �������դλ��˥��ꥢ
			}
			if ( $HseaChk[$kind] == 0 ) {

				# ���ϤǤʤ��Ȥ�
				$area++;
			}
			elsif ( $kind == $HlandSea ) {

				# ���λ�
				if (   ( $land2->[$x][$y] != $HlandSea )
					|| ( $landValue2->[$x][$y] != 0 ) )
				{

					# ��˱���Ƥ����Ϸ������Ǥʤ��Ȥ�
					$land->[$x][$y]       = $land2->[$x][$y];
					$landValue->[$x][$y]  = $landValue2->[$x][$y];
					$land2->[$x][$y]      = $HlandSea;
					$landValue2->[$x][$y] = 0;
				}
			}
			elsif (( $kind == $HlandSbase )
				|| ( $kind == $HlandOil )
				|| ( $kind == $HlandSMonument ) )
			{
				$kaitei++;
			}
			elsif ( $HseaChk[$kind] == 2 ) {

				# ����
				my $sId = ( shipSpec($value) )[2];
				if ( $sId > 0 ) {
					my $sIsland = $Hislands[ $HidToNumber{$sId} ];
					$sIsland->{'ship'}++;
				}
				next;
			}
			if ( $kind == $HlandTown ) {

				# Į
				$value = 200 if ( $value > 200 );
				$pop += $value;
			}
			elsif ( ( $kind == $HlandSea ) && ( $value >= 10 ) ) {

				# �ܿ���
				$yousyoku += $value;
			}
			elsif ( ( $kind == $HlandOil ) && ( $value >= 35 ) ) {

				# �����Ի�
				$popsea += $value;
			}
			elsif ( ( $kind == $HlandOil ) && ( $value == 0 ) ) {

				# ����
				$oil++;
			}
			elsif ( $kind == $HlandForest ) {

				# ��
				#	$forest++;
				$forestV += $value;
			}
			elsif ( $kind == $HlandFlower ) {

				# ��
				$flower++;
			}
			elsif ( $kind == $HlandMonument || $kind == $HlandSMonument ) {

				# ��ǰ���
				$monument++;
			}
			elsif (( $kind == $HlandFarm )
				|| ( $kind == $HlandMegaFarm )
				|| ( ( $kind == $HlandOil ) && ( $value >= 10 ) ) )
			{

				# ���� �������� ��������
				my $p = 0;
				if ( $kind == $HlandMegaFarm ) {
					if (
						megaAround( $land, $landValue, $x, $y, $kind, $value ) )
					{
						$p = 60;
					}
					else {
						$land->[$x][$y]      = $HlandFarm;
						$landValue->[$x][$y] = 50;
						$p                   = 50;
					}
				}
				else {
					$p = $value;
				}
				if ( $kind == $HlandFarm || $kind == $HlandMegaFarm ) {
					if ( chkAround( $land, $x, $y, $HlandWindmill, 19 ) ) {

  # Φ������ΤȤ�����2�إ��������֤�����У��ܤε��Ϥ�
						$farm += $p * 2;
					}
					else {
						$farm += $p;
					}
				}
				else {
					$farm += $p;
				}
			}
			elsif (( ( $kind == $HlandDefence ) && ( $value == 3 ) )
				|| ( $kind == $HlandBase )
				|| ( $kind == $HlandSbase )
				|| ( $kind == $HlandDokan ) )
			{

				# �ߥ�����ȯ�Ϳ�
				$landValue->[$x][$y] = int( $value / 100 )
				  if ( $kind == $HlandDokan );
				$MissileK += expToLevel( $kind, $value );
			}
			elsif ( $kind == $HlandTower ) {

				# ���ȥӥ�
				$tower += $value;
			}
			elsif ( ( $kind == $HlandAirport ) || ( $kind == $HlandExpo ) ) {

				# ������������
				$tower += 50;
			}
			elsif ( $kind == $HlandMountain ) {

				# ��
				$mountain += $value;
			}
			elsif ( $kind == $HlandPort ) {

				# ��
				$port += $value;
			}
			elsif ( $kind == $HlandFactory ) {

				# ����
				$factory += $value;
			}
			elsif ( $kind == $HlandMegacity ) {

				# �����Ի�
				if ( megaAround( $land, $landValue, $x, $y, $kind, $value ) ) {
					$pop += 300;
				}
				else {
					$land->[$x][$y]      = $HlandTown;
					$landValue->[$x][$y] = 190;
					$pop += 190;
				}
			}
			elsif ( $kind == $HlandHugecity ) {

				# Ķ�����Ի�
				my ($lName) = landName( $kind, $value );
				my ($lName2);
				if ( $value < 50 ) {

					# ���
					if ( countAround( $land, $x, $y, $HlandHugecity, 7 ) < 7 ) {

	  # ���ϣ��إ��������ĤǤ�Ķ�����Ϸ��Ǥʤ���硢����
						$land->[$x][$y] = $HlandMonument;
						$lName2 = landName( $HlandMonument, $value );
					}
					else {
						$pop += 400;
					}
				}
				else {

# ���ϣ��إ�����Ķ�����Ի�(�濴)�����뤫�ɤ��������å�����¸�ߤ��ʤ���������
					my ( $sx, $sy );
					my ($destroy) = 1;
					for ( $i = 1 ; $i < 7 ; $i++ ) {
						$sx = $x + $ax[$i];
						$sy = $y + $ay[$i];
						$sx--
						  if ( !( $sy % 2 ) && ( $y % 2 ) )
						  ;    # �Ԥˤ�����Ĵ��
						if (   ( $sx < 0 )
							|| ( $sx >= $HislandSize )
							|| ( $sy < 0 )
							|| ( $sy >= $HislandSize ) )
						{
						}
						elsif (( $land->[$sx][$sy] == $HlandHugecity )
							&& ( $landValue->[$sx][$sy] < 50 ) )
						{
							$destroy = 0;
						}
					}
					if ( $value < 60 ) {
						if ($destroy) {
							$land->[$x][$y]      = $HlandTown;
							$landValue->[$x][$y] = 200;
							$lName2 = landName( $HlandTown, 200 );
							$pop += 200;
						}
						else {
							$pop += 400;
						}
					}
					elsif ( $value < 70 ) {
						if ($destroy) {
							$land->[$x][$y]      = $HlandFactory;
							$landValue->[$x][$y] = 100;
							$lName2 = landName( $HlandFactory, 100 );
							$factory += 100;
						}
						else {
							$factory += 200;
						}
					}
					elsif ( $value < 80 ) {
						if ($destroy) {
							$land->[$x][$y]      = $HlandTower;
							$landValue->[$x][$y] = 200;
							$lName2 = landName( $HlandTower, 200 );
							$tower += 200;
						}
						else {
							$tower += 300;
						}
					}
					else {
						if ($destroy) {
							$land->[$x][$y]      = $HlandFarm;
							$landValue->[$x][$y] = 50;
							$lName2 = landName( $HlandFarm, 50 );
							$farm += 50;
						}
						else {
							if (
								chkAround( $land, $x, $y, $HlandWindmill, 19 ) )
							{

  # Φ������ΤȤ�����2�إ��������֤�����У��ܤε��Ϥ�
								$farm += 60 * 2;
							}
							else {
								$farm += 60;
							}
						}
					}
				}
				if ( $land->[$x][$y] != $HlandHugecity ) {
					logEventP( $id, $island->{'name'}, "($x, $y)",
"��${lName}�ϡ�${lName2}����äƤ��ޤ��ޤ�����"
					);
				}
			}
			elsif ( $kind == $HlandHaribote ) {

				# �ϥ�ܥ�
				$haribote++;
			}
			elsif ( $kind == $HlandMonster ) {

				# ����
				$mons++;
			}
			elsif ( $kind == $HlandSlum ) {

				# ����೹
				$pop += $value;
				$land->[$x][$y] = $HlandTown if ( $value >= 130 );
			}
			elsif ( $kind == $HlandTcity ) {

				# �����Ի�
				$tower += 200;
				$pop   += 300;
			}
			elsif ( $kind == $HlandMegatower ) {

				# ����ӥ�
				if ( megaAround( $land, $landValue, $x, $y, $kind, $value ) ) {
					$tower += 300;
				}
				else {
					$land->[$x][$y]      = $HlandTower;
					$landValue->[$x][$y] = 190;
					$tower += 190;
				}
			}
			elsif ( $kind == $HlandMegaFact ) {

				# ���繩��
				if ( megaAround( $land, $landValue, $x, $y, $kind, $value ) ) {
					$factory += 200;
				}
				else {
					$land->[$x][$y]      = $HlandFactory;
					$landValue->[$x][$y] = 90;
					$factory += 90;
				}
			}
			elsif ( $kind == $HlandBigcity ) {

				# ���Ի�
				$pop += 1000;
			}
			elsif ( $kind == $HlandBank ) {

				# ���
				$allBank += $value;
			}
			elsif ( $kind == $HlandFuji ) {

				# �ٻλ�
				fujiAround( $land, $landValue, $x, $y, $value );
			}
		}
	}

	# �ϲ�
	my ( $ugL, $ugV, $ugX, $ugY ) =
	  ( $island->{'ugL'}, $island->{'ugV'}, $island->{'ugX'},
		$island->{'ugY'} );
	for ( $i = 0 ; $i < $HugMax ; $i++ ) {
		next
		  if ( $land->[ $ugX->[$i] ][ $ugY->[$i] ] != $HlandDokan )
		  ;    # �и�̵��
		for ( $x = 0 ; $x < 9 ; $x++ ) {
			if ( $ugL->[$i][$x] == $HugTosi ) {
				if ( $island->{'food'} <= 0 ) {

					# ������­
					$ugV->[$i][$x] -= random(20);
				}
				else {
					$ugV->[$i][$x] += random(10);
				}
				if ( $ugV->[$i][$x] > 0 ) {
					$ugV->[$i][$x] = 100 if ( $ugV->[$i][$x] > 100 );
					$pop += $ugV->[$i][$x];
				}
				else {

					# ������­������
					$ugL->[$i][$x] = $HugRoad;
					$ugV->[$i][$x] = 0;
				}
			}
			elsif ( $ugL->[$i][$x] == $HugFarm ) {
				$farm += $ugV->[$i][$x];
			}
			elsif ( $ugL->[$i][$x] == $HugFact ) {
				$factory += $ugV->[$i][$x];
			}
			elsif ( $ugL->[$i][$x] == $HugKiti ) {
				$landValue->[ $ugX->[$i] ][ $ugY->[$i] ]++;
			}
			elsif ( $ugL->[$i][$x] == $HugOil ) {
				$factory += $ugV->[$i][$x];
			}
		}
	}
	$island->{'kaiteipop'} = 1
	  if ( $pop < $popsea );    # ����ο͸�����¿����
	$pop += $popsea;
	if ( ( ( $factory + $port ) * 2 < $tower ) && ( $pop >= 2000 ) ) {
		$island->{'towerD'} = 1001 + $tower - $factory - $port;
	}
	elsif ( ( $tower == 0 ) && ( $pop >= 2000 ) ) {
		$island->{'towerD'} = 1000;
	}

	# ��ͭΨ
	#	HdebugOut($island->{'id'} . " ������ͭ=" . $LandCount{0});
	if ( $LandCount{0} < $Hpossess ) {

		# ��������
		my ( $tIsland, $tName, $name );
		$i = 0;
		foreach ( sort { $LandCount{$b} <=> $LandCount{$a} } keys %LandCount ) {
			my $w = int( $LandCount{$_} * 10000 / $HpointNumber + 0.5 ) / 100;
			if ( ( $_ != 0 ) && ( $w > 1 ) ) {

				# ������
				my ($tn) = $HidToNumber{$_};
				next if ( $tn eq '' );
				$tIsland = $Hislands[$tn];
				$tName   = $tIsland->{'name'} . $AfterName;
				$name    = $island->{'name'};
				$tIsland->{'winP'} += int($w);
				$island->{'loseP'} += int($w);
				if ( $i == 0 ) {
					$tIsland->{'winP'} += int( $w * 2 );
					$tIsland->{'evil'} = 20000
					  if ( $tIsland->{'evil'} > 0 )
					  ;    # ��Ϣ�ݸ���̵�����
					$tIsland->{'money'}  += $HwinMoney;
					$tIsland->{'food'}   += $HwinFood;
					$tIsland->{'weapon'} += $HwinWeapon;
					$tIsland->{'money'} = $MaxMoney
					  if ( $tIsland->{'money'} > $MaxMoney );
					$tIsland->{'food'} = $MaxFood
					  if ( $tIsland->{'food'} > $MaxFood );
					$tIsland->{'weapon'} = $MaxSigen
					  if ( $tIsland->{'weapon'} > $MaxSigen );
					$island->{'loseP'} += int( $w * 2 );
					logEventT( $id, $_, $name,
"����${HtagName_}${tName}${H_tagName}(${w}��)��<b>�Ԥ�</b>�ޤ�����"
					);

					# �ɱһ���(�Ͼ�)���ߥ�������ߡ��ϲ��Ѵ�
					for ( $y = 0 ; $y < $HislandSize ; $y++ ) {
						for ( $x = 0 ; $x < $HislandSize ; $x++ ) {
							$kind             = $land->[$x][$y];
							$value            = $landValue->[$x][$y];
							$nation->[$x][$y] = 0;
							if (   ( $kind == $HlandDefence )
								|| ( $kind == $HlandBase )
								|| ( $kind == $HlandDokan ) )
							{
								$land->[$x][$y]      = $HlandFlower;
								$landValue->[$x][$y] = random(13) + 1;
							}
							elsif ( $kind == $HlandSbase ) {
								$land->[$x][$y]       = $HlandSea;
								$landValue->[$x][$y]  = 0;
								$land2->[$x][$y]      = $HlandSea;
								$landValue2->[$x][$y] = 0;
							}
						}
					}
					logEvent( $id, $name,
"�ϡ�����������<b>��Ϣ�ݸ</b>�ˤʤ�ޤ�����"
					);
					$island->{'evil'} = 0;
					$MissileK = 0;
				}
				$i++;
			}
		}
	}

	# ����
	$island->{'possess'}  = $LandCount{0};
	$island->{'tenki'}    = $tenki;
	$island->{'area'}     = $area;
	$island->{'pop'}      = $pop;
	$island->{'farm'}     = $farm;
	$island->{'port'}     = $port;
	$island->{'factory'}  = $factory;
	$island->{'tower'}    = $tower;
	$island->{'mountain'} = $mountain;
	$island->{'yousyoku'} = $yousyoku;
	$island->{'kaitei'} = int( $kaitei * 100 / ( $HpointNumber + 1 - $area ) );
	$island->{'MissileK'}  = $MissileK;
	$island->{'oilfield'}  = $oil;
	$island->{'monsfound'} = $mons;

	# �������
	$island->{'mons'}     = $mons;
	$island->{'forestV'}  = $forestV;
	$island->{'haribote'} = $haribote;
	$island->{'industry'} = $factory + $port + $mountain;
	$island->{'monument'} = $monument;
	$island->{'flower'}   = $flower;

	$allPop      += $pop;
	$allArea     += $area;
	$allMoney    += $island->{'money'};
	$allMissileA += $island->{'MissileA'};    #�ߥ�����ȯ�����
	$allFarm     += $farm;
	$allTower    += $tower;
	$allIndustry += $island->{'industry'};
	$allYousyoku += $yousyoku;
	$allForest   += $forestV;
}

# �����Ϸ��μ���
sub megaAround {
	my ( $land, $landValue, $x, $y, $kind, $lv ) = @_;

	# �����Ϸ��������Ƥ�������Ĵ�٤�($ax�ȹ�碌�Ƥ���)
	my $sx = $x + $ax[$lv];
	my $sy = $y + $ay[$lv];
	$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # �Ԥˤ�����Ĵ��
	if (   ( $sx < 0 )
		|| ( $sx >= $HislandSize )
		|| ( $sy < 0 )
		|| ( $sy >= $HislandSize ) )
	{

		# �ϰϳ��ξ��
	}
	else {

		# �ϰ���ξ��
		if ( $lv < 4 ) {
			$lv += 3;
		}
		else {
			$lv -= 3;
		}

		# �б����������Ϸ������ä�����
		return 1
		  if ( ( $land->[$sx][$sy] == $kind )
			&& ( $landValue->[$sx][$sy] == $lv ) );
	}
	return 0;
}

# �ٻλ��μ���
sub fujiAround {
	my ( $land, $landValue, $x, $y, $lv ) = @_;
	my ( $i, $sx, $sy );
	if ( $lv == 0 ) {
		for ( $i = 3 ; $i < 5 ; $i++ ) {
			$sx = $x + $ax[$i];
			$sy = $y + $ay[$i];
			$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );  # �Ԥˤ�����Ĵ��
			if (   ( $sx < 0 )
				|| ( $sx >= $HislandSize )
				|| ( $sy < 0 )
				|| ( $sy >= $HislandSize ) )
			{
			}
			else {
				$land->[$sx][$sy]      = $HlandFuji;
				$landValue->[$sx][$sy] = $i - 2;
			}
		}
	}
	elsif ( $lv == 1 ) {
		$sx = $x + $ax[6];
		$sy = $y + $ay[6];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # �Ԥˤ�����Ĵ��
		if ( $land->[$sx][$sy] != $HlandFuji ) {
			$land->[$x][$y]      = $HlandWaste;
			$landValue->[$x][$y] = 1;
		}
	}
	elsif ( $lv == 2 ) {
		$sx = $x + $ax[1];
		$sy = $y + $ay[1];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # �Ԥˤ�����Ĵ��
		if ( $land->[$sx][$sy] != $HlandFuji ) {
			$land->[$x][$y]      = $HlandWaste;
			$landValue->[$x][$y] = 1;
		}
	}
	return;
}

sub kinoraDamage {
	my ( $land, $landValue, $x, $y, $lv ) = @_;
	if ( $lv < 4 ) {
		$lv += 3;
	}
	else {
		$lv -= 3;
	}
	my $sx = $x + $ax[$lv];
	my $sy = $y + $ay[$lv];
	$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # �Ԥˤ�����Ĵ��
	if (   ( $sx < 0 )
		|| ( $sx >= $HislandSize )
		|| ( $sy < 0 )
		|| ( $sy >= $HislandSize ) )
	{
	}
	elsif ( $land->[$sx][$sy] == $HlandKInora ) {
		$landValue->[$sx][$sy] -= 100;
	}
	return;
}

# ή�������ͤ��Į�˿���ʬ���롣
sub refugees {
	my ( $boat, $tIsland ) = @_;
	my ( $bx, $by, $i );
	my ( $achive, $tLand, $tLandValue ) =
	  ( 0, $tIsland->{'land'}, $tIsland->{'landValue'} );

	for ( $i = 0 ; ( $i < $HpointNumber && $boat > 0 ) ; $i++ ) {
		$bx = $Hrpx[$i];
		$by = $Hrpy[$i];
		if (   ( $tLand->[$bx][$by] == $HlandTown )
			|| ( $tLand->[$bx][$by] == $HlandSlum ) )
		{

			# Į������೹�ξ��
			my ($lv) = $tLandValue->[$bx][$by];
			if ( $boat > 50 ) {
				$lv += 50;
				$boat -= 50;
				$achive += 50;
			}
			else {
				$lv     += $boat;
				$achive += $boat;
				$boat = 0;
			}
			if ( $lv > 200 ) {
				$boat += ( $lv - 200 );
				$achive -= ( $lv - 200 );
				$lv = 200;
			}
			$tLandValue->[$bx][$by] = $lv;
		}
		elsif ( $tLand->[$bx][$by] == $HlandPlains ) {

			# ʿ�Ϥξ��
			$tLand->[$bx][$by] = $HlandTown;
			if ( $boat > 10 ) {
				$tLandValue->[$bx][$by] = 5;
				$boat -= 10;
				$achive += 5;
			}
			elsif ( $boat > 5 ) {
				$tLandValue->[$bx][$by] = $boat - 5;
				$achive += $boat - 5;
				$boat = 0;
			}
		}
		last if ( $boat <= 0 );
	}
	return $achive;
}

# ���ð�ư
sub monmove {
	my ( $island, $x, $y, $mode ) = @_;

	# Ƴ����
	my ( $name, $id, $land, $landValue, $land2, $landValue2, $nation ) = (
		$island->{'name'},      $island->{'id'},    $island->{'land'},
		$island->{'landValue'}, $island->{'land2'}, $island->{'landValue2'},
		$island->{'nation'}
	);
	my ( $i, $d, $sx, $sy );

	if ( $land->[$x][$y] == $HlandKInora ) {

		# ���ۤ��Τ�

		my $kname = landName( $HlandKInora, 0 );

		# ���᡼���׻�����
		my $hp = ( bigMonsterSpec( $landValue->[$x][$y] ) )[1];
		my $damage;
		for ( $i = 1 ; $i < 7 ; $i++ ) {
			$sx = $x + $ax[$i];
			$sy = $y + $ay[$i];
			$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );
			if (   ( $sx < 0 )
				|| ( $sx >= $HislandSize )
				|| ( $sy < 0 )
				|| ( $sy >= $HislandSize ) )
			{
			}
			elsif ( $land->[$sx][$sy] == $HlandKInora ) {
				$damage += int( $landValue->[$sx][$sy] / 100 )
				  if ( $landValue->[$sx][$sy] > 100 );
			}
		}
		if ( $damage >= $hp ) {

			# �ݤ���
			my ($tn) = $HidToNumber{$lastDamage};
			if ( $tn eq '' ) {

				# �ݤ����礬�ʤ����ϻ�ʤʤ�
				$landValue->[$x][$y] -= ( $hp - 1 ) * 100 if ( $hp > 1 );
			}
			else {
				my $tIsland = $Hislands[$tn];
				my $tName   = $tIsland->{'name'};

				logOut(
"${HtagName_}${name}${AfterName}($x, $y)${H_tagName}��<B>����$kname</B>���ϿԤ����ݤ�ޤ�����",
					$lastDamage, $id
				);

				open( ROUT, ">>${HlogdirName}/ranking.log" );
				print ROUT "$HislandTurn,$lastDamage,$id,$kname\n";
				close(ROUT);

				$lastDamage = 0;
				$tIsland->{'money'} += 20000;
				my ($prize) = $tIsland->{'prize'};
				$prize =~ /([0-9]*),([0-9]*),(.*)/;
				my ( $flags, $monsters, $turns ) = ( $1, $2, $3 );
				if ( !( $flags & 2048 ) ) {
					$flags |= 2048;
					logPrize( $lastDamage, $tName, $Hprize[11] );
				}
				$tIsland->{'prize'} = "$flags,$monsters,$turns";
				$tIsland->{'evil'}  = 20000;                       # �����
				kinoraDel( $land, $landValue, $x, $y );
				return ( $x, $y );
			}
		}
		else {

			# ���᡼��
			$landValue->[$x][$y] -= $damage * 100;
		}
		$sx = random($HislandSize);
		$sy = random($HislandSize);
		my $lv = $landValue->[$x][$y];
		kinoraDel( $land, $landValue, $x, $y );
		if (   ( $i > 6 )
			&& ( chkAround( $land, $sx, $sy, $HlandKInora, 7 ) == 0 ) )
		{

			# �����פ���
			if ( $lv < 10000 ) {

				# ¾���������
				my @INumber = randomArray($HislandNumber);
				my $tIsland = $Hislands[ $INumber[ random($HislandNumber) ] ];
				my ( $tId, $tName, $tLand, $tLandValue ) = (
					$tIsland->{'id'},   $tIsland->{'name'},
					$tIsland->{'land'}, $tIsland->{'landValue'}
				);
				if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
					|| ( $tIsland->{'evil'} == 0 ) )
				{

					# ��꤬�Ӿ��ΰٰ�ư���ʤ�
				}
				else {
					logEventP( $id, $name, "($x, $y)",
"��<B>����$kname</B>�ϡ�${HtagName_}$tName$AfterName${H_tagName}������Ω���ޤ�����"
					);
					logMonsCome( $tId, $tName, $kname, "($sx, $sy)",
						landName( $tLand->[$sx][$sy], $tLandValue->[$sx][$sy] )
					);
					$tLand->[$sx][$sy]      = $HlandKInora;
					$tLandValue->[$sx][$sy] = $lv + 50000;
					kinoraMake( $tLand, $tLandValue, $sx, $sy );
					return ( $sx, $sy );
				}
			}
			elsif ( random(2) == 0 ) {

				$lv -= 10000;
			}
			$land->[$sx][$sy]      = $HlandKInora;
			$landValue->[$sx][$sy] = $lv;
			logEventP( $id, $name, "($sx, $sy)",
"��<B>����$kname</B>�������פ����ϣ��إ�����Ƨ�ߤĤ����ޤ�����"
			);
		}
		else {
			$sx                    = $x;
			$sy                    = $y;
			$land->[$sx][$sy]      = $HlandKInora;
			$landValue->[$sx][$sy] = $lv;
		}
		kinoraMake( $land, $landValue, $sx, $sy );
		return ( $sx, $sy );
	}

	my ( $mKind, $mName, $mHp ) = monsterSpec( $landValue->[$x][$y] );
	my ($special) = $HmonsterSpecial[$mKind];

	if ( $mode == 3 ) {
		if (
			( random(4) != 0 )
			&&

			( ( $mKind == 32 ) || ( $mKind == 33 ) || ( $mKind == 35 ) )
		  )
		{

			# ���� �ʤ�Ȥʤ��濴��
			my ($c) = $HislandSize / 2 - 1;
			if ( random(3) == 0 ) {
				if ( $x == $c ) {
				}
				elsif ( $x - $c > 0 ) {

					# ����
					$island->{'manipulate'} = 5;
				}
				else {

					# ����
					$island->{'manipulate'} = 2;
				}
			}
			else {
				if ( $y == $c ) {
				}
				elsif ( $y - $c > 0 ) {

					# ���
					$island->{'manipulate'} = ( random(2) == 0 ) ? 1 : 6;
				}
				else {

					# ����
					$island->{'manipulate'} = ( random(2) == 0 ) ? 3 : 4;
				}
			}
		}
		else {
			$island->{'manipulate'} = 0;
		}
	}

	# ư�����������
	for ( $i = 0 ; $i < 3 ; $i++ ) {
		if ( $island->{'manipulate'} == 0 ) {
			$d = random(6) + 1;
		}
		else {    # ����Ƥ����
			$d = $island->{'manipulate'};
		}
		$sx = $x + $ax[$d];
		$sy = $y + $ay[$d];

		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # �Ԥˤ�����Ĵ��
		next
		  if ( ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) );           # �ϰϳ�Ƚ��

		if (
			(
				   ( $land->[$sx][$sy] == $HlandDefence )
				&& ( $landValue->[$sx][$sy] == 3 )
			)
			|| ( $land->[$sx][$sy] == $HlandMountain )
			|| ( $land->[$sx][$sy] == $HlandKInora )
			|| ( $land->[$sx][$sy] == $HlandMyhome )
			|| ( $land->[$sx][$sy] == $HlandOcean )
			|| ( $land->[$sx][$sy] == $HlandFuji )
			|| ( $land->[$sx][$sy] == $HlandMonument )
			|| ( $land->[$sx][$sy] == $HlandSMonument )
			|| ( $land->[$sx][$sy] == $HlandMonster )
		  )
		{
			next;
		}
		if ( ( $mKind == 9 ) || ( $mKind == 21 ) || ( $mode == 3 ) ) {

			# �������Τ顢�����������ȡ�����
			last;
		}
		elsif ( $mKind == 16 ) {

			# ���Ω�Ƥ��Τ�
			last
			  if ( ( $HseaChk[ $land->[$sx][$sy] ] == 1 )
				|| ( $land->[$sx][$sy] == $HlandWarp ) );
		}
		else {

			# Φ�Ϥʤ��ư
			last if ( ( $HseaChk[ $land->[$sx][$sy] ] == 0 ) );
		}
	}
	next if ( $i == 3 );    # ư���ʤ��ä�

	# ư��������Ϸ��ˤ���å�����
	my ($l)     = $land->[$sx][$sy];
	my ($lv)    = $landValue->[$sx][$sy];
	my ($lName) = landName( $l, $lv );
	my ($point) = "($sx, $sy)";

	if ( $l == $HlandEarth ) {

		# �ϵ����ã
		$HearthAttack++;
		$HdisMonster *= 2;
	}
	elsif ( $l == $HlandOPlayer ) {

		# �����������ù�
		my ($tIsland) = $Hislands[ $HidToNumber{ $nation->[$sx][$sy] } ];
		my ( $tId, $tName, $tLand, $tLandValue ) = (
			$tIsland->{'id'},   $tIsland->{'name'},
			$tIsland->{'land'}, $tIsland->{'landValue'}
		);
		logMonsMoveOcean( $tId, "$tName$AfterName", $point, $mName );
		my ( $bx, $by ) = shipAppear( $tLand, random(4) );
		$tLand->[$bx][$by]      = $HlandMonster;
		$tLandValue->[$bx][$by] = $landValue->[$x][$y];
	}
	else {

		# ��ư
		$land->[$sx][$sy]      = $land->[$x][$y];
		$landValue->[$sx][$sy] = $landValue->[$x][$y];
	}

	# ��ȵ錄���֤���äˤ�ä��ѹ�
	if ( $mKind == 10 ) {

		# �ǥӥ뤤�Τ�
		$land->[$x][$y]      = $HlandOsen;
		$landValue->[$x][$y] = $mHp;
	}
	elsif ( $mKind == 27 ) {

		# ʬ�����Τ�
		if ( random(2) == 0 ) {

			my ($nhp) = int( $mHp / 2 );

			if ( $nhp > 0 ) {

				# ʬ��
				logMonster( $id, $name, "($x, $y)", $mName,
					"��ʬ�����ޤ�����" );
				$landValue->[$x][$y] = 2700 + $nhp;
				$landValue->[$sx][$sy] -= $nhp;
			}
			else {

				# ���ǡ���̵��
				$land->[$sx][$sy]      = $HmonsterDestroy[$mKind];
				$landValue->[$sx][$sy] = 0;

				$land->[$x][$y]      = $HmonsterDestroy[$mKind];
				$landValue->[$x][$y] = 0;
			}
		}
		else {
			$land->[$x][$y]      = $HmonsterDestroy[$mKind];
			$landValue->[$x][$y] = 0;
		}
	}
	else {
		$land->[$x][$y]      = $HmonsterDestroy[$mKind];
		$landValue->[$x][$y] = 0;
	}

	# ΢���Ϸ���õ�
	$land2->[$x][$y]      = $HlandSea;
	$landValue2->[$x][$y] = 0;

	if ( $mode == 3 ) {

		# ����
		$land2->[$sx][$sy]      = $HlandSea;
		$landValue2->[$sx][$sy] = 0;
		$nation->[$sx][$sy]     = 0;

		$nation->[$x][$y] = 0;

		if ( $l == $HlandSDefence ) {

			# �ɱһ���
			logMonsMoveDefenceS( $lName, $point, $mName );
			wideDamageSpace( $id, $land, $landValue, $dis, $nation, $sx, $sy, 7,
				0 );
		}
		elsif ( $l == $HlandEarth ) {
			logMonsMoveEarth( $lName, $point, $mName );
		}
		elsif ( $l == $HlandSea ) {
			logMonsMoveSpace2( $point, $mName, $SpaceName, 999 );
		}
		else {
			logMonsMoveSpace( $point, $mName, $SpaceName, $lName, 999 );
		}
		return ( $sx, $sy );
	}
	elsif ( $mode == 4 ) {

		# ����
		$land2->[$sx][$sy]      = $HlandSea;
		$landValue2->[$sx][$sy] = 0;
		if ( $l == $HlandSea ) {
			logMonsMoveSpace2( $point, $mName, $OceanName, 888 );
		}
		elsif ( $l == $HlandOPlayer ) {
		}
		else {
			logMonsMoveSpace( $point, $mName, $OceanName, $lName, 888 );
		}
		return ( $sx, $sy );
	}

	# ���ڡ������Τ�
	$island->{'Meteo'} += 20 if ( $mKind == 20 );

	# ���ڡ������Τ�
	$island->{'Meteo'} += 20 if ( $mKind == 20 );

	if ( ( ( $l == $HlandDefence ) || ( ( $l == $HlandOil ) && ( $lv == 5 ) ) )
		&& ( $HdBaseAuto == 1 ) )
	{

		# �ɱһ��ߤ�Ƨ���
		logMonsMoveDefence( $id, $name, $lName, $point, $mName );

		# �����ﳲ�롼����
		wideDamage( $id, $name, $land, $landValue, $sx, $sy, 0 );
	}
	elsif (( $l == $HlandDeathtrap )
		|| ( ( $l == $HlandOil ) && ( $lv == 6 ) ) )
	{

		# �ǥ��ȥ�åפ�Ƨ���
		if ( $l == $HlandOil ) {

			# ����
			logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
				"�׷���̵���ä����" );
			$land->[$sx][$sy]      = $HlandSea;
			$landValue->[$sx][$sy] = 0;
		}
		else {
			if ( $lv >= 3 ) {
				logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
					"�׷���̵���ä����" );
				$land->[$sx][$sy]      = $HlandWaste;
				$landValue->[$sx][$sy] = 1;
			}
			elsif ( $lv == 2 ) {
				if ( $mKind == 18 ) {

					# ȿ�⤤�Τ�
					logMonsMoveDeathtrapM( $id, $name, $lName, $point, $mName );
				}
				elsif ( $mHp > 3 ) {
					logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
						"���᡼�������" );
					$landValue->[$sx][$sy] -= 3;
				}
				else {
					logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
						"�׷���̵���ä����" );
					$land->[$sx][$sy]      = $HlandWaste;
					$landValue->[$sx][$sy] = 1;
				}
			}
			else {
				if (   ( $mKind == 17 )
					|| ( $mKind == 18 )
					|| ( $mKind == 19 )
					|| ( $mKind == 20 ) )
				{

					# �ߥ������ȯ���������
					logMonsMoveDeathtrapM( $id, $name, $lName, $point, $mName );
				}
				elsif ( $mHp > 3 ) {
					logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
						"���᡼�������" );
					$landValue->[$sx][$sy] -= 2;
				}
				elsif ( $mHp > 1 ) {
					logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
						"���᡼�������" );
					$landValue->[$sx][$sy]--;
				}
				else {
					logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
						"�׷���̵���ä����" );
					$land->[$sx][$sy]      = $HlandWaste;
					$landValue->[$sx][$sy] = 1;
				}
			}
		}
	}
	elsif ( $l == $HlandWarp ) {    # ž������
		logWarpMons( $id, $name, $lName, $point, "����${mName}" );
		if (
			warp(
				$id, $name,
				$land->[$sx][$sy],
				$landValue->[$sx][$sy],
				"����${mName}", $lv, 0
			) == 0
		  )
		{
			$land->[$sx][$sy]      = $HlandWarp;
			$landValue->[$sx][$sy] = $lv;
		}
		else {
			logWarpMonsMiss( $id, $name, $point, "����${mName}" );
		}
	}
	elsif ( ( $mKind == 17 ) && ( random(5) == 0 ) )
	{    # �������å�����ܥ���
		logMonsZIBAKU( $id, $name, $lName, $point, $mName );
		wideDamage( $id, $name, $land, $landValue, $sx, $sy, 0 );
	}
	elsif ( $mKind == 23 ) {

		# ���ͥ���
		if ( random(25) == 0 ) {
			logMonsZIBAKU( $id, $name, $lName, $point, $mName );
			wideDamage( $id, $name, $land, $landValue, $sx, $sy, 0 );
		}
		else {
			$island->{'money'} += 1000;
			logMonsMoney( $id, $name, $lName, $point, $mName,
				"1000${HunitMoney}" );
		}
	}
	elsif ( $mKind == 24 ) {

		# ��å����Τ�
		if ( $mHp <= 1 ) {
			if ( random(4) == 0 ) {

				# ���Ǥ���
				logMonsMove( $id, $name, $lName, $point, $mName );
				logMonster( $id, $name, $point, $mName,
					"�ϼ������Ǥ����褦�Ǥ���" );
				$land->[$sx][$sy]      = $HlandWaste;
				$landValue->[$sx][$sy] = 0;
			}
			else {
				$island->{'money'} += 2000;
				logMonsMoney( $id, $name, $lName, $point, $mName,
					"2000${HunitMoney}" );
			}
		}
		else {
			$island->{'money'} += 500;
			logMonsMoney( $id, $name, $lName, $point, $mName,
				"500${HunitMoney}" );
			if ( random(4) == 0 ) {

				# ���᡼���������
				$landValue->[$sx][$sy]--;
				logMonster( $id, $name, $point, $mName,
					"�ϼ�ä��褦�Ǥ���" );
			}
		}
	}
	elsif ( $mKind == 22 ) {

		# ����ƥͥ����Τ�
		logMonsMove( $id, $name, $lName, $point, $mName );
		logMonsEAT( $id, $name, $lName, $point, $mName );
		my $eatfood = int( $island->{'food'} * 0.05 );
		$eatfood = 1000 if ( $eatfood < 1000 );
		$island->{'food'} -= $eatfood;
	}
	elsif ( $mKind == 26 ) {

		# �º̤��Τ�
		# �Ԥ��褬���Ϥˤʤ�
		logMonsMove( $id, $name, $lName, "(?, ?)", $mName );
	}
	else {

		# �Ԥ��褬���Ϥˤʤ�
		logMonsMove( $id, $name, $lName, $point, $mName );
	}

	if (   ( $l == $HlandOsen )
		&& ( ( $mKind == 6 ) || ( $mKind == 7 ) || ( $mKind == 8 ) ) )
	{
		if ( random(4) == 0 ) {    # �����ˤ���ü��Ѱ�
			if ( random(2) == 0 ) {
				$landValue->[$sx][$sy] =
				  1300 + $HmonsterBHP[13] + random( $HmonsterDHP[13] );
			}
			else {
				$landValue->[$sx][$sy] =
				  1400 + $HmonsterBHP[14] + random( $HmonsterDHP[14] );
			}
			logMonsC( $id, $name, $point, $mName,
				( monsterSpec( $landValue->[$sx][$sy] ) )[1] );
		}
	}
	return ( $sx, $sy );
}

# ���ϰ�ư��ư
sub shipAction {
	my ( $island, $x, $y ) = @_;

	my ( $name, $id, $land, $landValue, $land2, $landValue2 ) = (
		$island->{'name'},      $island->{'id'},    $island->{'land'},
		$island->{'landValue'}, $island->{'land2'}, $island->{'landValue2'}
	);

	my ( $lx, $lvx ) = ( $land->[$x][$y], $landValue->[$x][$y] );
	my $sName = landName( $lx, $lvx );
	my ( $order, $hp, $sId ) = shipSpec($lvx);
	my @INumber = randomArray($HislandNumber);
	my $tIsland = $Hislands[ $INumber[ random($HislandNumber) ] ];
	my $tId     = $tIsland->{'id'};

	# ��ư���ι�ư
	my ( $i, $d, $sx, $sy, $j );
	if ( $order == 4 ) {

		# ����
		my $Katk = $HshipMATK[ $lx - $HlandPirate ];
		my $Satk = $HshipSATK[ $lx - $HlandPirate ];
		return ( $x, $y )
		  if ( $Katk + $Satk < 1 );    # ���⤷�ʤ���(��ư�⤷�ʤ�)
		for ( $j = 1 ; $j < 7 ; $j++ ) {
			$sx = $x + $ax[$j];
			$sy = $y + $ay[$j];
			$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );  # �Ԥˤ�����Ĵ��
			next
			  if ( ( $sx < 0 )
				|| ( $sx >= $HislandSize )
				|| ( $sy < 0 )
				|| ( $sy >= $HislandSize ) );         # �ϰϳ�Ƚ��

			if ( ( $land->[$sx][$sy] == $HlandMonster ) && ( $Katk > 0 ) ) {

				# ����ȯ�����⤹��
				my ( $mKind, $mName, $mHp ) =
				  monsterSpec( $landValue->[$sx][$sy] );
				my ($special) = $HmonsterSpecial[$mKind];

				# �Ų���?
				if (   ( ( $special == 3 ) && ( ( $HislandTurn % 2 ) == 1 ) )
					|| ( ( $special == 4 ) && ( ( $HislandTurn % 2 ) == 0 ) )
					|| ( ( $special == 5 ) && ( random(4) != 0 ) ) )
				{

					# �Ų���
					next;
				}
				else {
					$mHp - $Katk;
					if ( $mHp > 0 ) {

						# ���������Ƥ�
						logMonster( $id, $name, "($sx, $sy)", $mName,
"�ϡ��ɤ����餫���᡼��������ޤ�����"
						);
						$landValue->[$sx][$sy] -= $Katk;
					}
					else {

						# �ݤ���
						logMonster( $id, $name, "($sx, $sy)", $mName,
"�ϡ��ɤ����餫�ι���ˤ����Ǥ����褦�Ǥ���"
						);
						$land->[$sx][$sy]      = $HmonsterDestroy[$mKind];
						$landValue->[$sx][$sy] = 0;
					}
					last;
				}
			}
			elsif ( ( $HseaChk[ $land->[$sx][$sy] ] == 2 ) && ( $Satk > 0 ) ) {

				# ������ͽ�ꡩ

#
#				my($torder, $thp, $tsId) = shipSpec($landValue->[$sx][$sy]);
#
#				HdebugOut("�������⡩ Satk=${Satk} torder=${torder} thp=${thp} tsId=${tsId}");
#
#				if(($tsId > 0) && ($id != $tsId)){
#					# ¾����ν�°��(̵��°����)�ξ��
#
#					HdebugOut("¾����ν�°��(̵��°����)�ξ��");
#
#					my($p);
#					if($torder == 2){
#						# �ɸ���
#						$p = 3;
#					}elsif($torder == 1){
#						$p = 1;
#					}
#					if(random(5 - $p) == 0){
#						HdebugOut("����");
#
#					}else{
#
#						$thp - $Satk;
#						if($thp > 0){
#							HdebugOut("�����Ƥ���");
#							logShipDis($id, $name, landName($land->[$sx][$sy], 0), "($sx, $sy)","�ϡ��ɤ����餫�ι���ˤ����᡼�������");
#							$landValue->[$sx][$sy] -= $Satk;
#						}else{
#							# �ݤ���
#							HdebugOut("����");
#							logShipDis($id, $name, landName($land->[$sx][$sy], 0), "($sx, $sy)","�ϡ��ɤ����餫�ι���ˤ�����פ�");
#							$land->[$sx][$sy] = $HlandSea;
#							$landValue->[$sx][$sy] = 0;
#						}
#					}
#				}
				next;
			}
		}
	}
	if ( $lx == $HlandPirate ) {

		# ��±��
		for ( $j = 1 ; $j < 7 ; $j++ ) {
			$sx = $x + $ax[$j];
			$sy = $y + $ay[$j];
			$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );  # �Ԥˤ�����Ĵ��
			next
			  if ( ( $sx < 0 )
				|| ( $sx >= $HislandSize )
				|| ( $sy < 0 )
				|| ( $sy >= $HislandSize ) );
			if (   ( $land->[$sx][$sy] == $HlandFishSShip )
				|| ( $land->[$sx][$sy] == $HlandFishMShip )
				|| ( $land->[$sx][$sy] == $HlandFishLShip )
				|| ( $land->[$sx][$sy] == $HlandTitanic ) )
			{

				# ���Ϥ�̱������������硣
				next
				  if ( $sId == ( shipSpec( $landValue->[$sx][$sy] ) )[2] )
				  ;    # Ʊ����°�ξ��
				if ( $sId > 0 ) {

					# ������±��
					my $kIsland = $Hislands[ $HidToNumber{$sId} ];
					my $tname   = $kIsland->{'name'};
					logShipDis(
						$id,
						$name,
						landName( $land->[$sx][$sy], 0 ),
						"($sx, $sy)",
"����±����ˤ��${HtagName_}${tname}${AfterName}${H_tagName}�˾�ü���"
					);
					$landValue->[$sx][$sy] = 21000 + $sId;
				}
				else {
					logShipDis( $id, $name, landName( $land->[$sx][$sy], 0 ),
						"($sx, $sy)", "����±����ˤ�����פ�" );
					if ( random(20) == 0 ) {

						# ͩ����
						$land->[$sx][$sy]      = $HlandGhostShip;
						$landValue->[$sx][$sy] =
						  $HshipHP[ $HlandGhostShip - $HlandPirate ] * 1000;
					}
					else {
						$land->[$sx][$sy]      = $HlandSea;
						$landValue->[$sx][$sy] = 0;
					}
				}
				last;
			}
		}
	}
	elsif ( ( $lx == $HlandIceFloe ) && ( $island->{'titanic'} > 0 ) ) {

		# ��ڵ�����ήɹ�Ǥ�����(��)
		for ( $j = 1 ; $j < 7 ; $j++ ) {
			$sx = $x + $ax[$j];
			$sy = $y + $ay[$j];
			$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );  # �Ԥˤ�����Ĵ��
			next
			  if ( ( $sx < 0 )
				|| ( $sx >= $HislandSize )
				|| ( $sy < 0 )
				|| ( $sy >= $HislandSize ) );
			if ( $land->[$sx][$sy] == $HlandTitanic ) {
				next
				  if ( $sId == ( shipSpec( $landValue->[$sx][$sy] ) )[2] )
				  ;                                   # Ʊ����°�ξ��
				logShipDis( $id, $name, landName( $land->[$sx][$sy], 0 ),
					"($sx, $sy)", "��ɹ���Ⱦ��ͤ����פ�" );
				$land->[$sx][$sy]      = $HlandSea;
				$landValue->[$sx][$sy] = 0;
				last;
			}
		}
	}

	if ( $order == 0 ) {
		if (
			(
				   ( $lx == $HlandFishSShip )
				|| ( $lx == $HlandFishMShip )
				|| ( $lx == $HlandFishLShip )
			)
			&& ( $id == $sId )
		  )
		{

			# �����λ��᤬�ü�ξ���ٽ��
			for ( $j = 1 ; $j < 7 ; $j++ ) {
				$sx = $x + $ax[$j];
				$sy = $y + $ay[$j];
				$sx--
				  if ( !( $sy % 2 ) && ( $y % 2 ) );  # �Ԥˤ�����Ĵ��
				next
				  if ( ( $sx < 0 )
					|| ( $sx >= $HislandSize )
					|| ( $sy < 0 )
					|| ( $sy >= $HislandSize ) );
				if (   ( $land->[$sx][$sy] == $HlandIceFloe )
					|| ( $land->[$sx][$sy] == $HlandCoupleRock ) )
				{
					next
					  if ( $sId == ( shipSpec( $landValue->[$sx][$sy] ) )[2] )
					  ;                               # Ʊ����°�ξ��
					logShipDis( $id, $name, landName( $land->[$sx][$sy], 0 ),
						"($sx, $sy)", "��ٽ�ᤷ" );
					$landValue->[$sx][$sy] = 21000 + $id;
					last;
				}
			}
		}
	}

	# ��ư����
	if ( $order == 3 ) {

		# ű��
		if (   ( $x == 0 )
			|| ( $x == $HislandSize )
			|| ( $y == 0 )
			|| ( $y == $HislandSize ) )
		{

			# ű������
			$land->[$x][$y]       = $land2->[$x][$y];
			$landValue->[$x][$y]  = $landValue2->[$x][$y];
			$land2->[$x][$y]      = $HlandSea;
			$landValue2->[$x][$y] = 0;
			logShipDis( $id, $name, landName( $lx, 0 ),
				"($x, $y)", "������γ�����Υ��Ƥ���" );
			shipComeBack( $sId, $lx, $lvx );    # ���Խ���
			return ( 100, 100 );
		}
		else {
			$i = 3;
			my (@direction) = shipEvacuation( $x, $y );
			foreach $d (@direction) {
				$sx = $x + $ax[$d];
				$sy = $y + $ay[$d];
				$sx--
				  if ( !( $sy % 2 ) && ( $y % 2 ) );  # �Ԥˤ�����Ĵ��
				if ( $HseaChk[ $land->[$sx][$sy] ] == 1 ) {

					# �����Ϸ��ξ�硢���ϤϽ���
					$i = 0;
					last;
				}
			}
		}
	}
	else {
		for ( $i = 0 ; $i < 3 ; $i++ ) {

			# �����Ƚ��
			if (   ( $island->{'shipMoveMid'} == $sId )
				&& ( $island->{'shipMoveMt'} == $id ) )
			{
				$d = $island->{'shipMoveM'};
			}
			elsif (( $island->{'shipMoveTid'} == $sId )
				&& ( $island->{'shipMoveTt'} == $id ) )
			{
				$d = $island->{'shipMoveT'};
			}
			else {
				$d = random(6) + 1;
			}

			$sx = $x + $ax[$d];
			$sy = $y + $ay[$d];
			$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );  # �Ԥˤ�����Ĵ��
			                                          # �ϰϳ�Ƚ��
			if (   ( $sx < 0 )
				|| ( $sx >= $HislandSize )
				|| ( $sy < 0 )
				|| ( $sy >= $HislandSize ) )
			{
				if (   ( ( $lx == $HlandPirate ) && ( $id != $tId ) )
					|| ( $lx == $HlandWingDragon )
					|| ( $lx == $HlandIceFloe )
					|| ( $lx == $HlandBalloonS )
					|| ( $lx == $HlandCoupleRock ) )
				{
					$land->[$x][$y]       = $land2->[$x][$y];
					$landValue->[$x][$y]  = $landValue2->[$x][$y];
					$land2->[$x][$y]      = $HlandSea;
					$landValue2->[$x][$y] = 0;

   # ��±�ξ��ǰ㤦��ξ�����������Ф줿��˰�ư
					$tIsland->{'piratesend'} = $sId if ( $lx == $HlandPirate );
					logShipDis( $id, $name, landName( $lx, 0 ),
						"($x, $y)", "������γ�����Υ��Ƥ���" );
					return ( 100, 100 );
				}
				next;
			}

			# �����Ϸ���ž�����֤ξ�硢���ϤϽ���
			last
			  if ( ( $HseaChk[ $land->[$sx][$sy] ] == 1 )
				|| ( $land->[$sx][$sy] == $HlandWarp ) );
		}
	}

	# ư���ʤ��ä�
	return ( $x, $y ) if ( $i == 3 );

	# ư��������Ϸ��ˤ���å�����
	my ($l)     = $land->[$sx][$sy];
	my ($lv)    = $landValue->[$sx][$sy];
	my ($point) = "($sx, $sy)";

	if ( ( $l == $HlandDeathtrap ) || ( ( $l == $HlandOil ) && ( $lv == 6 ) ) )
	{

		# �ǥ��ȥ�åפ�Ƨ���
		logShipMoveDeathtrap( $id, $name, landName( $l, $lv ), $point, $sName );
		$land->[$sx][$sy]      = $HlandSea;
		$landValue->[$sx][$sy] = 0;

		# ��ư����Ϸ�������
		$land->[$x][$y]       = $land2->[$x][$y];
		$landValue->[$x][$y]  = $landValue2->[$x][$y];
		$land2->[$x][$y]      = $HlandSea;
		$landValue2->[$x][$y] = 0;
		return ( 100, 100 );
	}
	elsif ( $l == $HlandWarp ) {

		# ž������
		logWarpMons( $id, $name, landName( $l, $lv ), $point, $sName );
		if ( warp( $id, $name, $lx, $lvx, $sName, $lv, 1 ) == 0 ) {
			$land->[$sx][$sy]      = $HlandWarp;
			$landValue->[$sx][$sy] = $lv;

		}
		else {
			logWarpMonsMiss( $id, $name, $point, landName( $l, $lv ) );
		}

		# ��ư����Ϸ�������
		$land->[$x][$y]       = $land2->[$x][$y];
		$landValue->[$x][$y]  = $landValue2->[$x][$y];
		$land2->[$x][$y]      = $HlandSea;
		$landValue2->[$x][$y] = 0;
		return ( 100, 100 );
	}
	if ( $order == 0 ) {

		# ���᤬�ü�ξ��
		if (   ( ( $lx == $HlandPirate ) || ( $lx == $HlandGhostShip ) )
			&& ( $id != $sId ) )
		{

			# ��±����ͩ������άå
			if (   ( ( $l == $HlandOil ) && ( $lv >= 10 ) )
				|| ( ( $l == $HlandSea ) && ( $lv >= 10 ) ) )
			{

				# �����Իԡ��������졢�ܿ���
				if ( $sId > 0 ) {
					my ($sIsland) = $Hislands[ $HidToNumber{$sId} ];
					if ( ( $l == $HlandOil ) && ( $lv < 35 ) ) {

						# ��������
						$sIsland->{'money'} += $lv * 80;
						$sIsland->{'food'}  += $lv * 80;
					}
					else {
						$sIsland->{'money'} += $lv * 20;
						$sIsland->{'food'}  += $lv * 20;
					}
				}
				logShipPlunder( $id, $sId, $name, landName( $l, $lv ),
					$point, $sName );
				$order = 100;

				# �ܿ���ΤȤ���
				$lv = ( $l == $HlandSea ) ? 1 : 0;
				$l = $HlandSea;
			}
		}
		elsif ( $lx == $HlandProbeShip ) {

			# ����õ����
			my ($p) = random(100);
			if ( $p < 3 ) {
				if ( $land2->[$x][$y] != $HlandOil ) {
					$land2->[$x][$y]      = $HlandOil;
					$landValue2->[$x][$y] = 0;
					logOut(
"${HtagName_}${name}${AfterName}($x, $y)${H_tagName}��<B>����</B>��ȯ�����줿�褦�Ǥ���",
						$id
					);
				}
			}
			elsif ( $p == 81 ) {

				# �������Τ�
				$land2->[$x][$y]      = $HlandMonster;
				$landValue2->[$x][$y] = 905;
				logMonsCome( $id, $name, ( monsterSpec(905) )[1],
					"($x, $y)", landName( $HlandSea, 0 ) );
			}
			elsif ( $p == 82 ) {

				# ������������
				$land2->[$x][$y]      = $HlandMonster;
				$landValue2->[$x][$y] = 2105;
				logMonsCome( $id, $name, ( monsterSpec(2105) )[1],
					"($x, $y)", landName( $HlandSea, 0 ) );
			}
			elsif ( $p == 83 ) {

				# ʮ��(���ۥ��å�������)
				$HpunishInfo{$id}->{punish} = 8;
				$HpunishInfo{$id}->{x}      = $x;
				$HpunishInfo{$id}->{y}      = $y;
			}
		}
	}

	# �Ԥ�����Ϸ�����¸����ư
	$land2->[$sx][$sy]      = $l;
	$landValue2->[$sx][$sy] = $lv;

	$land->[$sx][$sy]      = $land->[$x][$y];
	$landValue->[$sx][$sy] = $landValue->[$x][$y];

	# ��ȵ錄�Ϸ�������
	$land->[$x][$y]       = $land2->[$x][$y];
	$landValue->[$x][$y]  = $landValue2->[$x][$y];
	$land2->[$x][$y]      = $HlandSea;
	$landValue2->[$x][$y] = 0;

	# �������Τ�ɽ�����ʤ�
	#	if($order < 100){
	#		# ��ư��
	#		logShipMove($id, $name, landName($l, $lv), $point, $sName);
	#	}

	return ( $sx, $sy );
}

# �����Խ���
sub shipComeBack {
	my ( $sId, $kind, $lv ) = @_;
	my ($island) = $Hislands[ $HidToNumber{$sId} ];
	my ( $land, $landValue ) = ( $island->{'land'}, $island->{'landValue'} );
	my ( $sx, $sy ) = shipAppear( $land, random(4) );
	$island->{'land2'}->[$sx][$sy]      = $land->[$sx][$sy];
	$island->{'landValue2'}->[$sx][$sy] = $landValue->[$sx][$sy];
	$land->[$sx][$sy]                   = $kind;
	my ($lv2) = $lv - ( int( $lv / 10000 ) * 10000 );
	$landValue->[$sx][$sy] = $lv2 + 20000;
	logShipComeIs(
		$island->{'id'}, $island->{'name'},
		landName( $kind, 0 ), "($sx, $sy)"
	);
}

# ž��
# ���ID  ̾��  ž�����Ƥ����Ϸ� ��  ž��ʪ̾  �������å�ID  ž��ʪ�μ���
sub warp {
	my ( $id, $name, $land, $landValue, $mName, $tid, $z ) = @_;

	# �������åȼ���
	my ($tn) = $HidToNumber{$tid};
	return 0 if ( $tn eq '' );
	my ($tIsland) = $Hislands[$tn];

	# ��꤬�Ӿ��ΰ����
	return 0
	  if ( ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
		|| ( $tIsland->{'evil'} == 0 ) );

	my ( $tName, $tLand, $tLandValue ) =
	  ( $tIsland->{'name'}, $tIsland->{'land'}, $tIsland->{'landValue'} );

	# ������ž�����֤����뤫������
	my ( $count, $x, $y, $tx, $ty, $i, $j );
	for ( $count = 0 ; $count < $HpointNumber ; $count++ ) {
		$x = $Hrpx[$count];
		$y = $Hrpy[$count];
		if (   ( $tLand->[$x][$y] == $HlandWarp )
			|| ( $tLand->[$x][$y] == $HlandWarpR ) )
		{

			#  ž������ȯ�������ΤǼ��Ϥξ㳲ʪ�򥵡���

			# ž�������֤ξ������������Ǥ���
			$j =
			  ( $tLand->[$x][$y] == $HlandWarpR ) ? $tLandValue->[$x][$y] : 1;

			for ( $i = $j ; $i < 61 ; $i++ ) {
				$tx = $x + $ax[$i];
				$ty = $y + $ay[$i];
				$tx--
				  if ( !( $ty % 2 ) && ( $y % 2 ) );  # �Ԥˤ�����Ĵ��
				                                      # �ϰ��⳰�����å�
				next
				  if ( ( $tx < 0 )
					|| ( $tx >= $HislandSize )
					|| ( $ty < 0 )
					|| ( $ty >= $HislandSize ) );
				if ( $z > 10 ) {                      # ���á����ϰʳ�
					$x = $tx;
					$y = $ty;
					last;
				}
				elsif ( $i > 6 )
				{    # ���Ϥ�ž���Ǥ��ʤ�����ž������
					return 1;
				}
				if ( $z == 1 ) {

					# ���Ϥϳ����Ϸ������ϤϽ���
					if ( $HseaChk[ $tLand->[$tx][$ty] ] == 1 ) {
						$x = $tx;
						$y = $ty;
						last;
					}
				}
				else {

					# ���ϡ����á�������ǰ��ʳ�
					if (   ( $HseaChk[ $tLand->[$tx][$ty] ] == 0 )
						&& ( $tLand->[$tx][$ty] != $HlandMountain )
						&& ( $tLand->[$tx][$ty] != $HlandMonument )
						&& ( $tLand->[$tx][$ty] != $HlandFuji )
						&& ( $tLand->[$tx][$ty] != $HlandMyhome )
						&& ( $tLand->[$tx][$ty] != $HlandKInora )
						&& ( $tLand->[$tx][$ty] != $HlandMonster ) )
					{
						$x = $tx;
						$y = $ty;
						last;
					}
				}
			}
			last;
		}
	}

	# ž�����֤��ʤ��ä����Υ����ϥ�����
	if ( $count >= $HpointNumber ) {
		$x = random($HislandSize);
		$y = random($HislandSize);
	}
	if ( $z < 10 ) {    # ����,����
		logMWarp( $id, $tid, $name, $tName, "($x, $y)", $mName );
		$tLand->[$x][$y]      = $land;
		$tLandValue->[$x][$y] = $landValue;
	}
	elsif ( $z == 11 ) {    # �ߥ�����
		logMWarp( $id, $tid, $name, $tName, "($x, $y)", "�ߥ�����" );
		$tLand->[$x][$y]      = $HlandSea;
		$tLandValue->[$x][$y] = 0;
	}
	elsif ( $z == 12 ) {    # ���
		logMWarp( $id, $tid, $name, $tName, "($x, $y)", $mName );
		$tLand->[$x][$y]      = $HlandSea;
		$tLandValue->[$x][$y] = 0;
	}
	return 0;
}

# 0����(n - 1)�ޤǤο��������ŤĽФƤ���������
sub randomArray {
	my ($n) = @_;
	my ( @list, $i );

	# �����
	$n    = 1 if ( $n == 0 );
	@list = ( 0 .. $n - 1 );

	# ����åե�
	for ( $i = $n ; --$i ; ) {
		my ($j) = int( rand( $i + 1 ) );
		next if ( $i == $j );
		@list[ $i, $j ] = @list[ $j, $i ];
	}

	return @list;
}

# neo_otacky�᤬����
sub islandReki {
	my ( $line, $i, $id, $pop, $turn, $name, $n, $island, @rekidai, $reki );
	my $j = 0;

	if ( !open( RIN, "<${HlogdirName}/rekidai.dat" ) ) {
		rename( "${HlogdirName}/rekidai.tmp", "${HlogdirName}/rekidai.dat" );
		if ( !open( RIN, "${HlogdirName}/rekidai.dat" ) ) {
			open( ROUT, ">${HlogdirName}/rekidai.tmp" );
			for ( $i = 0 ; $i < $HislandNumber ; $i++ )
			{    # ��¸�����礹�٤Ƥ�Ͽ
				$island = $Hislands[$i];
				$id     = $island->{'id'};
				$name   = $island->{'name'};
				$pop    = $island->{'pop'};
				print ROUT "$id,$pop,$HislandTurn,$name\n";
			}
			close(ROUT);
			rename( "${HlogdirName}/rekidai.tmp",
				"${HlogdirName}/rekidai.dat" );
			return;
		}
	}

	while ( $line = <RIN> ) {
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),(.*)$/;
		( $id, $pop, $turn, $name ) = ( $1, $2, $3, $4 );
		if ( defined $HidToNumber{$id} ) {
			$HidToNumberR{$id} = $j;
			$rekidai[$j]->{'id'} = $id;
		}
		$rekidai[$j]->{'pop'}  = $pop;
		$rekidai[$j]->{'turn'} = $turn;
		$rekidai[$j]->{'name'} = $name;
		$j++;
	}
	close(RIN);

	for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
		$island = $Hislands[$i];
		$id     = $island->{'id'};
		$name   = $island->{'name'};
		$pop    = $island->{'pop'};
		$n      = $HidToNumberR{$id};
		if ( defined $n ) {
			if ( $pop > $rekidai[$n]->{'pop'} ) {
				$rekidai[$n]->{'pop'}  = $pop;
				$rekidai[$n]->{'turn'} = $HislandTurn;
				$rekidai[$n]->{'name'} = $name;
			}
		}
		else {
			$rekidai[$j]->{'id'}   = $id;
			$rekidai[$j]->{'pop'}  = $pop;
			$rekidai[$j]->{'turn'} = $HislandTurn;
			$rekidai[$j]->{'name'} = $name;
			$j++;
		}
	}

	# �͸���Ʊ���Ȥ���ľ���Υ�����ν��֤Τޤ�
	my @idx = ( 0 .. $#rekidai );
	@idx =
	  sort { $rekidai[$b]->{'pop'} <=> $rekidai[$a]->{'pop'} || $a <=> $b }
	  @idx;
	@rekidai = @rekidai[@idx];

	open( ROUT, ">${HlogdirName}/rekidai.tmp" );
	my $recordNo = ( $HmaxIsland < 15 ) ? 15 : $HmaxIsland;
	for ( $i = 0 ; $i < $recordNo ; $i++ )
	{    # �������κ������Ʊ��������Ͽ�������15�硣
		$reki = $rekidai[$i];
		$n    = $i + 1;
		if ( defined $reki->{'pop'} ) {
			( $id, $pop, $turn, $name ) = (
				$reki->{'id'},   $reki->{'pop'},
				$reki->{'turn'}, $reki->{'name'}
			);
			print ROUT "$id,$pop,$turn,$name\n";
		}
	}
	close(ROUT);
	unlink("${HlogdirName}/rekidai.dat");
	rename( "${HlogdirName}/rekidai.tmp", "${HlogdirName}/rekidai.dat" );
}

#------------------------------------------------
# �ʰץȡ��ʥ���
# ����ε�Ͽ��
sub fihgt_log {
	open( FOUT, "${HdirName}/fight.log" );
	my ( $f, @offset );
	while ( $f = <FOUT> ) {
		chomp($f);
		push( @offset, "$f\n" );
	}
	close(FOUT);
	my $fight;

	# �����������
	my $fTurn = $HislandFightCount;

	# �辡��ξ��99�ˤ���
	$fTurn = 99 if ( $HislandFightMode == 9 );

	open( DOUT, ">$HdirName/fight.log.bak" );
	print DOUT "<${fTurn}>\n";
	print DOUT "<TABLE BORDER>\n";
	print DOUT
"<tr><TH colspan=3></th><th $HbgTitleCell colspan=1>${HtagTH_}����${H_tagTH}</th><TH colspan=1></th>\n";
	print DOUT
	  "<TH $HbgTitleCell colspan=1>${HtagTH_}�Լ�${H_tagTH}</th></tr>\n";
	print DOUT "<TR>\n";
	print DOUT
"<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>\n";
	print DOUT
"<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�Լ�${H_tagTH}</NOBR></TH>\n";

#	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}����߿�${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell width=15 nowrap=nowrap>��</TH>\n";

#	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�󽷶�${H_tagTH}</NOBR></TH>\n";
	print DOUT
"<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>\n";

#	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�˲��ߴ��${H_tagTH}</NOBR></TH>\n";
#	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�˲��ɻܿ�${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell width=15 nowrap=nowrap>��</TH>\n";
	print DOUT
"<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH>\n";

#	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�˲��ߴ��${H_tagTH}</NOBR></TH>\n";
#	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�˲��ɻܿ�${H_tagTH}</NOBR></TH>\n";
	print DOUT "</tr>\n";

	foreach $fight (@fight_log_flag) {
		my ( $name, $tName, $reward, $log, $pop, $tLog, $tPop, $fly, $id ) =
		  split( ",", $fight );
		$logD  = int( $log / 1000 ) . "��";
		$logM  = ( $log - $logD * 1000 ) . "��";
		$tLogD = int( $tLog / 1000 ) . "��";
		$tLogM = ( $tLog - $tLogD * 1000 ) . "��";

#		$tName	= "<A STYlE=\"text-decoration:none\" HREF=\"".$HthisFile."?LoseMap=".$id."\">".
#					$HtagName2_.$tName."${AfterName}".$H_tagName2."</A>";
		$tName = "${HtagName2_}$tName$AfterName${H_tagName2}";
		$tPop .= ${HunitPop};
		if ( $id == -1 ) {
			$tName = "${HtagName2_}���ﾡ${H_tagName2}";
			$tPop  = "��";
			$tLogM = "��";
			$tLogD = "��";
		}
		elsif ( $id == -2 ) {
			$tName = "${HtagName2_}����${H_tagName2}";
			$tPop  = "��";
			$tLogM = "��";
			$tLogD = "��";
		}
		print DOUT
"<TR><TD $HbgInfoCell align=right><NOBR>${HtagName_}${name}${AfterName}${H_tagName}</nobr></td>";
		print DOUT "<TD $HbgInfoCell align=center><NOBR>${tName}</nobr></td>\n";

		#		print DOUT "<TH $HbgInfoCell><NOBR>${fly}ȯ</nobr></TH>\n";
		print DOUT "<TD $HbgInfoCell><NOBR>��</nobr></td>\n";

	#		print DOUT "<TH $HbgInfoCell><NOBR>${reward}${HunitMoney}</nobr></TH>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${pop}${HunitPop}</nobr></TH>\n";

		#		print DOUT "<TH $HbgInfoCell><NOBR>${logM}</nobr></TH>\n";
		#		print DOUT "<TH $HbgInfoCell><NOBR>${logD}</nobr></TH>\n";
		print DOUT "<TD $HbgInfoCell><NOBR>��</nobr></td>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${tPop}</nobr></TH>\n";

		#		print DOUT "<TH $HbgInfoCell><NOBR>${tLogM}</nobr></TH>\n";
		#		print DOUT "<TH $HbgInfoCell><NOBR>${tLogD}</nobr></TH>\n";
		print DOUT "</tr>\n";
	}
	print DOUT "</TABLE>$consolationName\n";
	print DOUT @offset;
	close(DOUT);
	rename( "${HdirName}/fight.log.bak", "${HdirName}/fight.log" );
}

# ͽ�������
sub log_yosen {
	my $yosen;
	open( DOUT, ">${HdirName}/fight.log" );
	print DOUT "<0>\n";
	print DOUT "<TABLE BORDER>\n";
	print DOUT "<TR>\n";
	print DOUT
"<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}${AfterName}${H_tagTH}</NOBR></TH>\n";
	print DOUT
"<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}�͸�${H_tagTH}</NOBR></TH></tr>";
	foreach $yosen (@yosen_log) {
		my ( $pop, $name ) = split( ",", $yosen );
		print DOUT
"<TR><TD $HbgInfoCell align=right><NOBR>${HtagName_}${name}${AfterName}${H_tagName}</nobr></td>";
		print DOUT
"<TD $HbgInfoCell align=center><NOBR><B>${pop}$HunitPop</b></nobr></td></tr>\n";
	}
	print DOUT "</TABLE>\n";
	close(DOUT);
}

# ������
sub logWin {
	my ( $id, $name, $str, $money ) = @_;
	my $fTurn = $HislandFightCount + 1;
	if ( $HislandNumber <= 4 ) {
		$fTurn = '�辡��';
	}
	elsif ( $HislandNumber <= 8 ) {
		$fTurn = '��辡';
	}
	else {
		$fTurn .= '����';
	}
	if ( $HislandNumber == 2 ) {
		logOut(
"${HtagName_}${name}${AfterName}${H_tagName}${str}����<B>ͥ������</B>",
			$id
		);
		logHistory(
			"${HtagName_}${name}${AfterName}${H_tagName}��<B>ͥ������</B>"
		);
	}
	elsif ( $money == 0 ) {
		logOut(
"${HtagName_}${name}${AfterName}${H_tagName}${str}����<B>$fTurn�ʽС�</B>",
			$id
		);
	}
	else {
		logOut(
"${HtagName_}${name}${AfterName}${H_tagName}${str}����<B>$fTurn�ʽС���$money$HunitMoney</B>���󽷶⤬��ʧ���ޤ�����",
			$id
		);
	}
}

# ͽ�����
sub logLoseOut {
	my ( $id, $name ) = @_;
	logOut(
		"${HtagName_}${name}${AfterName}${H_tagName}��<B>ͽ�����</B>��",
		$id
	);
	logHistory(
"${HtagName_}${name}${AfterName}${H_tagName}��<B>ͽ�����������</B>��"
	);
}

#------------------------------------------------

1;
