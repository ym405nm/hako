#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# ターン進行モジュール(ver1.02)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 究想の箱庭(ver5.54e)
#----------------------------------------------------------------------
# 2009/08/05 5.54e 巨大都市に発展しないバグと宇宙ユニット破壊で怪獣が破壊できるバグを修正。
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# ターン進行モード
#----------------------------------------------------------------------
# メイン
sub turnMain {
	my ( $i, $j );

	# 最終更新時間を更新
	if ( $HrepeatTurn > 0 ) {
		if ( $HislandTurn % $HrepeatTurn == ( $HrepeatTurn - 1 ) ) {
			$HislandLastTime += $HunitTime;
		}
	}
	else {
		$HislandLastTime += $HunitTime;
	}

	# 座標配列を作る
	makeRandomPointArray();
	makeRandomOceanPointArray();

	# ターン番号
	$HislandTurn++;

	# 季節処理
	$Hmonth = ( $HislandTurn % 12 ) + 1;

	# 順番決め
	my (@order) = randomArray($HislandNumber);

	# 資源取引のペナルティ処理
	penaltyExchange();

	$HmonsterSpecial[19] = random(7) + 2;    # アシュラの属性(2〜8)

	if ($Hdishangen) {

		# 災害半減期を導入する。
		if ( ( int( $HislandTurn / 100 ) % 2 ) == 0 ) {

			# 確率半減、全てではない。
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

	# 季節による変動
	if ( ( $Hmonth < 4 ) || ( 11 < $Hmonth ) ) {
		$HdisAkasio  = 0;
		$HdisTyphoon = 0;
	}

	# 参加島への制裁内容を読み込む
	readPunishData();

	# 収入、消費フェイズ
	for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
		estimateS( $order[$i] );
		$Hislands[ $order[$i] ]->{'oldmoney'} =
		  $Hislands[ $order[$i] ]->{'money'};
		$Hislands[ $order[$i] ]->{'oldfood'} =
		  $Hislands[ $order[$i] ]->{'food'};

		# ターン開始前の人口をメモる
		$Hislands[ $order[$i] ]->{'oldPop'} = $Hislands[ $order[$i] ]->{'pop'};
		next if ( $Hislands[ $order[$i] ]->{'predelete'} );
		income( $order[$i], $Hislands[ $order[$i] ] );
	}
	spaceEstimate(0);    # 宇宙処理

	doCommandLate();     # ターン差命令

	# コマンド処理
	for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
		$island = $Hislands[ $order[$i] ];
		next if ( $island->{'predelete'} );

		# 戻り値1になるまで繰り返し
		$Hwflg = 10;     # 天候による戻しの最大数(安全策)
		while ( !doCommand($island) ) { }

		# 整地ログ(まとめてログ出力)
		logMatome( $island, $HlogOmit2, 'seichi' ) if ($HlogOmit2);
	}

	# Battle Field用究想いのらフラグ
	if ( $HislandTurn > 250 ) {
		$kinoraFlg = 1 if ( ( $HislandTurn % $HturnPrizeUnit ) == 0 );
	}

	$HearthAttack = 0;    # 地球攻撃がされたか
	spaceHex();           # 宇宙成長処理
	oceanHex();           # 海域成長処理
	                      # 成長および単ヘックス災害
	for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
		next if ( $Hislands[ $order[$i] ]->{'predelete'} );
		doEachHex( $Hislands[ $order[$i] ] );
	}

	# 島全体処理
	my ($remainNumber) = $HislandNumber;
	my ($island);

	# 怪獣バトルターン杯用変数初期化
	$MonsBattleTurn   = 2;    # 最低でも３勝以上
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

		# 死滅判定
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

			# 死滅メッセージ
			my ($tmpid) = $island->{'id'};
			logDead( $tmpid, $island->{'name'} );
		}
	}

	# 資源取引のターン処理準備
	turnExchangeBegin();

	# 商人が取引をする？
	if ( rand(100) < 100 ) {    # 10%
		merchantInviteExchange();
	}

	# 資源取引のターン処理
	turnExchange();

	for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
		doIslandProcess2( $Hislands[ $order[$i] ] );
	}

	spaceEstimate(1);           # 宇宙処理

	# 人口処理・収支
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

	# 統計
	my $allBank2;
	if ( $allBank > 0 ) {
		$allBank2 = "、総預金 ${allBank}000${HunitMoney}";
	}
	else {
		$allBank2 = "";
	}
#	push( @HlogPool,
#"0,$HislandTurn,0,,箱庭諸島統計：総人口 ${allPop}${HunitPop}、総面積 ${allArea}${HunitArea}、総資金 $allMoney${HunitMoney}${allBank2}"
#	);

	if ( ( $HislandTurn % $HturnPrizeVarious ) == 0 ) {

		# 部門賞

		# 部門賞のターンに統計のログを取る
		open( POUT, ">>${HlogdirName}/statistical.log" );
		print POUT
"$HislandTurn,$allPop,$allMoney,$allArea,$allBank,$allMissileA,$allFarm,$allTower,$allIndustry,$allYousyoku,$allForest,$HislandNumber\n";
		close(POUT);

		# 農業王
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

		# 工業王
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

		# 商業王
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

		# 水産王
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

		# 森林王
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

		# ミサイル王
		# 森林王
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

		# ハリボテ王
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

		# 怪獣王
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

		# 石油王
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

		# 災害王
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

				# 累計30万人を超える減
				logEvent( $tIsland->{'id'}, $tIsland->{'name'},
"が災害王を獲得、多くの犠牲者の死を悼んで災害の碑が贈られました。"
				);
				$tIsland->{'present'}->[11]++;
			}
		}

		# 船舶王
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

		# 記念碑王
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

		# 園芸王
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

	# ターン杯対象ターンだったら、怪獣杯処理
	if (   ( ( $HislandTurn % $HturnPrizeUnit ) == 0 )
		&& ( $MonsBattleTurnID != 0 ) )
	{
		my ($island) = $Hislands[ $HidToNumber{$MonsBattleTurnID} ];
		$island->{'present'}->[10]++;    # 怪獣記念碑を一つ増やす
		logPrize( $island->{'id'}, $island->{'name'}, "怪獣杯" );
		logEvent( $island->{'id'}, $island->{'name'},
"が怪獣杯を獲得、怪獣記念碑をプレゼントされました。"
		);
	}

	# 戦闘期間への移行等
	my $tournamentflg = 0;
	if ($Htournament) {

		# 簡易トーナメント
		$HislandTurnCount++;
		if ( $HislandFightMode == 1 ) {

			# 予選
			if ( $HislandTurn == $HislandChangeTurn ) {

				# 開発ターンに移行
				$tournamentflg     = 1;
				$HislandFightMode  = 2;
				$HislandTurnCount  = 0;
				$HislandChangeTurn = $HislandTurn + $HdevelopeTurn;
			}
		}
		elsif ( $HislandFightMode == 2 ) {

			# 開発
			if ( $HislandTurn == $HislandChangeTurn ) {

				# 戦闘ターンに移行
				$tournamentflg =
				  2;    # 対戦相手決定処理は人口ソート後で
				$HislandFightMode = 3;
				$HislandFightCount++;
				$HislandTurnCount = 0;
				if ( $remainNumber > 2 ) {

					# 決勝戦以外は、時間を空ける
					$HislandLastTime += $HinterTime;
					$HislandChangeTurn = $HislandTurn + $HfightTurn;
				}
				else {

					# 決勝戦
					$HislandChangeTurn = $HislandTurn + $HfinalTurn;
				}
			}
		}
		elsif ( $HislandFightMode == 3 ) {

			# 戦闘
			if ( $HislandTurn == $HislandChangeTurn ) {

				# 勝敗決着　開発ターンに移行
				$tournamentflg = 3;
				if ( $remainNumber <= 2 ) {

					# 終了
					$HislandFightMode = 9;
				}
				else {
					$HislandTurnCount = 0;
					$HislandFightMode = 2;
				}
				$HislandChangeTurn = $HislandTurn + $HdevelopeTurn;
				my $HwinIsland     = 0;    # 勝利した島の数
				my $consolationPop = 0;    # 敗者復活対象島人口
				my $consolationID  = 0;    # 敗者復活対象島ＩＤ
				for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
					$island = $Hislands[$i];
					my $HcurrentNumber = $HidToNumber{ $island->{'fight_id'} };
					my $tIsland        = $Hislands[$HcurrentNumber];

					# 戦闘後の勝敗
					my $reward = $island->{'waste'};
					if (
						(
							    $HcurrentNumber ne ''
							and $island->{'pop'} >= $tIsland->{'pop'}
						)
						or ( $island->{'fight_id'} == -1 )
					  )
					{

						# 勝ち
						my $tPop = 0;
						$HwinIsland++;
						if ( $island->{'fight_id'} > 0 ) {
							logWin( $island->{'id'}, $island->{'name'},
								"勝利", $reward );
							$tPop = $tIsland->{'pop'};
							$tIsland->{'fight_id'} = 0;
							if ( $consolationPop <= $tPop ) {
								$consolationPop = $tPop;
								$consolationID  = $tIsland->{'id'};
							}
							$tIsland->{'lose'} = 1;
							logOut(
"${HtagName_}$tIsland->{'name'}${AfterName}${H_tagName}、<B>敗退</B>。",
								$tIsland->{'id'}
							);
						}
						else {

							# 不戦勝
							logWin( $island->{'id'}, $island->{'name'},
								"不戦勝" );
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
						logWin( $island->{'id'}, $island->{'name'}, "勝利",
							$reward );
						push( @fight_log_flag,
"$island->{'name'},,$reward,0,$island->{'pop'},0,0,0,-2"
						);
						$island->{'fight_id'} = 0;
					}
					$island->{'reward'} = 0;
				}

				# 敗退した島の除去
				$consolationName = "";
				if ( $HislandFightMode != 9 ) {

					# 終了時以外
					for ( $i = 0 ; $i < $HislandNumber ; $i++ ) {
						$island = $Hislands[$i];
						if ( $island->{'lose'} ) {
							if (   ( $consolationID == $island->{'id'} )
								&& ( ( $HwinIsland % 2 ) != 0 )
								&& ($HconsolationMatch) )
							{

		 # 敗者復活対象島で次回奇数の場合で敗者復活モード
								$consolationName =
"${HtagName_}$island->{'name'}${AfterName}${H_tagName}、<B>敗者復活！</B>";
								logOut( $consolationName, $island->{'id'} );
							}
							else {
								logHistory(
"${HtagName_}$island->{'name'}${AfterName}${H_tagName}、<B>敗退で沈没</B>。"
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

	# 人口順にソート
	# 人口が同じときは直前のターンの順番のまま
	my @idx = ( 0 .. $#Hislands );
	@idx =
	  sort { $Hislands[$b]->{'pop'} <=> $Hislands[$a]->{'pop'} || $a <=> $b }
	  @idx;
	@Hislands = @Hislands[@idx];

	islandReki();

	# ターン杯対象ターンだったら、その処理
	if ( ( $HislandTurn % $HturnPrizeUnit ) == 0 ) {
		my ($island) = $Hislands[0];
		logPrize( $island->{'id'}, $island->{'name'},
			"$HislandTurn${Hprize[0]}" );
		$island->{'prize'} .= "${HislandTurn},";
	}
	if ($Htournament) {

		# 簡易トーナメント
		if ( $tournamentflg == 1 ) {

			# 予選落ちを沈没させる
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

			# 対戦相手決定処理
			my ( $l, $r );
			$r = $remainNumber - 1;
			for ( $l = 0 ; $l <= $r ; $l++, $r-- ) {
				if ( $Hislands[$r]->{'id'} == $Hislands[$l]->{'id'} ) {

					# 不戦勝
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

		# 定めたターン間隔で最下位の島を強制削除
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

	# 島数カット
	$HislandNumber = $remainNumber;

	# 陣営 各勢力の統計履歴
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

# ターン,陣営ID,島数,総人口,総領土,総経済力,総軍事力,占有率
				print AOUT
"$HislandTurn,$_,$allyCount{$_},$allyPop{$_},$allyArea{$_},$allyGnp{$_},$allyPow{$_},$w\n";
				close(AOUT);
			}
		}
	}

	# バックアップターンであれば、書く前にrename
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

	# 資源取引のターン処理後始末
	turnExchangeEnd();

	if ($Htournament) {

		# 簡易トーナメント
		if ( $tournamentflg == 3 ) {
			fihgt_log();
		}
		elsif ( $tournamentflg == 1 ) {
			log_yosen();
		}
	}

	# ファイルに書き出し
	if ( !writeIslandsFile( -1, 0 ) ) {
		if ( ( $HislandTurn % $HbackupTurn ) == 0 ) {
			rmdir("${HdirName}");
			rename( "${HdirName}.bak0", "${HdirName}" );
		}
		unlock();
		tempFailWrite();
		return;
	}

	# ログファイルを後ろにずらす
	for ( $i = ( $HlogMax - 1 ) ; $i >= 0 ; $i-- ) {
		$j = $i + 1;
		unlink("${HlogdirName}/hakojima.log$j");
		rename( "${HlogdirName}/hakojima.log$i",
			"${HlogdirName}/hakojima.log$j" );
	}

##### 追加 親方20020307
	if ($Hperformance) {
		my ( $uti, $sti, $cuti, $csti ) = times();
		$uti += $cuti;
		$sti += $csti;
		my ($cpu) = $uti + $sti;

# ログファイル書き出し(テスト計測用　普段はコメントにしておいてください)
#		open(POUT,">>cpu-t.log");
#		print POUT "CPU($cpu) : user($uti) system($sti)\n";
#		close(POUT);

#		push( @HlogPool,
#"0,$HislandTurn,0,,<SMALL>負荷計測 CPU($cpu) : user($uti) system($sti)</SMALL>"
#	);
	}
#####

	# ログ書き出し
	logFlush();

	# 記録ログ調整
	logHistoryTrim( "hakojima.his", $HhistoryMax );
	logHistoryTrim( "weather.his",  $HWeatherMax );

	# トップへ
	topPageMain();
}

# 参加島への制裁内容を読み込む
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

	# 制裁データを削除する
	unlink("${HdirName}/punish.dat");
}

# 収入、消費フェイズ
sub income {
	my ( $number, $island ) = @_;

	my ( $name, $id, $land, $landValue, $p, $r ) = (
		$island->{'name'}, $island->{'id'}, $island->{'land'},
		$island->{'landValue'},
		1, random(1000)
	);

	if ( $island->{'id'} > 90 ) {

		# Battle Fieldのとき
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
			'slum'};    # スラム街の人の労働は収入にならない。

		my ( $wkind, $wname, $whp, $wkind2, $wkind3 ) =
		  weatherinfo( $island->{'weather'} );
		if ( ( $r < $HdisVGHarvest ) && ( $whp > 1 ) && ( $whp < 8 ) ) {
			logEvent2( $id, $name, '大豊作', 'です' );
			$p = 4;
		}
		elsif (( $r < $HdisGHarvest + $HdisVGHarvest )
			&& ( $whp > 1 )
			&& ( $whp < 8 ) )
		{
			logEvent2( $id, $name, '豊作', 'です' );
			$p = 2;
		}
		elsif ( $r < $HdisBHarvest + $HdisGHarvest + $HdisVGHarvest ) {
			logEvent2( $id, $name, '凶作', 'です' );
			$p = 0;
		}

		$island->{'turnsu'}++;    #島固有のターン数

		#w		if($HwarFlg){
		#w			# 戦争系
		#w			$island->{'evil'} = 10;
		#w		}elsif($island->{'MissileK'} == 0){ # ミサイル非保有島

		if ( $island->{'MissileK'} == 0 ) {    # ミサイル非保有島
			$island->{'evil'} -=
			  2;    # 0の時はターン数に関係なく保護国になる
			$island->{'evil'} = 0 if ( $island->{'evil'} < 0 );
		}
		elsif ( $island->{'evil'} < 10 ) {
			$island->{'evil'} = 10;
		}
		if ( $island->{'evil'} > 10000 ) {
			$island->{'evil'} -= 1000;
			$island->{'gold'} = 1;    # 黄金期
		}
		elsif ( $island->{'evil'} > 300 ) {
			$island->{'evil'} = 300;
		}

# 保護国で順位点が４０以上の島は地震の確率が０．５％ＵＰする
		$island->{'prepare2'}++
		  if ( ( $island->{'evil'} == 0 ) && ( $island->{'zyuni'} >= 40 ) );

		# 収入
		if ( $number < 5 ) {

			# 上位にボーナス
			$island->{'money'} += 100 - $number * 20 if ( $HislandTurn > 100 );
		}

		# 上位に点数を加算。
		$island->{'zyuni'} += 10 - $number if ( $number < 10 );

	  # ターン杯対象ターンだったら、点数をリセットする。
		$island->{'zyuni'} = 0 if ( ( $HislandTurn % $HturnPrizeUnit ) == 0 );

		# 人口10万未満の時は商業ビルは意味が無い
		$tower = 0 if ( $pop < 1000 );

		if ( $factory < $port ) {

			# 工場よりも港の方が多い時
			$factory += $factory;
		}
		else {
			$factory += $port;    # 港の値を工場の値にたす
		}
		if ( $island->{'order'} & 32 ) {

			# 採掘場は資金を生産する
			$tower += $mountain;
			$mountain = 0;
		}
		if ( $island->{'order'} & 128 ) {

			# 工場は資金を生産する
			$tower += $factory;
			$factory = 0;
		}
		if ( $pop > $farm ) {
			$island->{'food'} += $farm * $p;    # 農場フル稼働
			$pop -= $farm;
			if ( $pop > $mountain * 10 ) {

				# 鉱石
				$island->{'ore'} += $mountain;
				$pop -= $mountain * 10;
				if (   ( $pop > $oilfactory * 30 )
					&& ( $island->{'ore'} > $oilfactory ) )
				{

					# 合成石油
					$island->{'ore'} -= $oilfactory;
					$island->{'oil'} += $oilfactory;
					$pop -= $oilfactory * 30;
				}
				if ( $pop > $factory * 10 ) {

					# 兵器
					$factory = $island->{'ore'}
					  if ( $island->{'ore'} < $factory );
					$factory = $island->{'oil'}
					  if ( $island->{'oil'} < $factory );
					$island->{'ore'} -= $factory;
					$island->{'oil'} -= $factory;
					$island->{'weapon'} += $factory;

					# 資金
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
			$island->{'food'} += $pop * $p;    # 全員野良仕事
		}

		# 食料消費
		$island->{'food'} =
		  int( ( $island->{'food'} ) - ( $island->{'pop'} * $HeatenFood ) );
	}

	# 怪獣先移動
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

	# 荒地ぜ〜んぶ地ならし攻撃(地ならしの数値指定２２)
	my ( $comArray, $command, $cNo, $i, $sx, $sy );
	for ( $cNo = 0 ; $cNo < $HcommandMax ; $cNo++ ) {
		$comArray = $island->{'command'};
		$command  = $comArray->[$cNo];
		next if ( $command->{'kind'} == $HcomSpecialSPP );
		if (   ( $command->{'kind'} == $HcomPrepare2 )
			&& ( $command->{'arg'} == 22 ) )
		{
			slideFront( $island->{'command'}, $cNo );    # 以降を詰める
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

# コマンドフェイズ
sub doCommand {
	my ($island) = @_;

	# コマンド取り出し(天候等で中止された命令は空回し)
	my ( $comArray, $command, $cNo );
	for ( $cNo = 0 ; $cNo < $HcommandMax ; $cNo++ ) {
		$comArray = $island->{'command'};
		$command  = $comArray->[$cNo];
		last if ( $command->{'flg'} <= 0 );
	}

	if ($Htournament) {

		# 簡易トーナメント
		my $tName = $HidToName{ $island->{'fight_id'} };
		if ( $tName eq '' ) {

			# 無し
			$command->{'target'} = $island->{'id'};
		}
		elsif ( $command->{'target'} != $island->{'id'} ) {
			$command->{'target'} = $island->{'fight_id'};
		}
	}

	# 各要素の取り出し
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

		# 簡易トーナメント怪獣付き
		if ( $HislandFightMode == 3 ) {

			# 遠征？
			my ($tn) = $HidToNumber{ $island->{'fight_id'} };
			if ( $tn ne '' ) {

		# $id,$name,$tId,$sId,$mId,$hp,$mhp,$str,$def,$agi,$skl,$winh,$win,$lose
				my ($tIsland) = $Hislands[$tn];
				if (   $tIsland->{'monster'}->[0] == $island->{'fight_id'}
					|| $tIsland->{'monster'}->[2] == 0 )
				{

					# 相手がいるときは、勝手に遠征する。
					logMonsENSEI( $id, $name, $island->{'fight_id'},
						$tIsland->{'name'}, "怪獣遠征" );
					$island->{'monster'}->[0]  = $island->{'fight_id'};
					$island->{'monster'}->[2]  = $island->{'fight_id'};
					$tIsland->{'monster'}->[2] = $id;
				}
			}
		}
		else {

			# 撤退？
		}
		if (   $kind == $HcomMonsEgg
			|| $kind == $HcomMonsEnsei
			|| $kind == $HcomMonsTettai
			|| $kind == $HcomMonsEsaAid
			|| $kind == $HcomMonsAid
			|| $kind == $HcomMonsSell )
		{

			# 上記の命令はできない
			return 0;
		}
	}

	# 既にミサイルを撃った時
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

	# 移民は１ターンに１回まで。
	return 1
	  if ( ( $kind == $HcomEmigration ) && ( $island->{'AfEmigra'} == 1 ) );

	if (
		( $kind != $HcomSpecialSPP )
		&&    # 海獣掃討艇によるSPPではなく
		( $island->{'order'} & 16 ) &&    # 強制怪獣誘導弾設定
		( $island->{'monsmgmflg'} == 1 )
	  )
	{                                     # 怪獣がいる(いた？)
		                                  # 強制怪獣誘導弾
		$island->{'monsmgmflg'} = 0;
		( $kind, $target, $x, $y, $arg, $x2, $y2 ) =
		  ( $HcomMissileMGM, $island->{'id'}, 0, 0, 1, 0, 0 );
	}
	else {
		return 1
		  if ( ( $command->{'kind'} == $HcomPrepare2 )
			&& ( $command->{'arg'} == 22 ) );
		slideFront( $comArray, $cNo );    # 以降を詰める
	}

	# 特殊命令
	my $kind2;
	if ( $kind == $HcomSpecialSPP ) {

		# 海獣掃討艇によるSPP
		if (   ( $island->{'turnsu'} + $island->{'evil'} < $HdisUN )
			|| ( $island->{'evil'} == 0 )
			|| ( $island->{'monsship'} < 1 ) )
		{

			# 国連保護、海獣掃討艇が存在しない場合はカット
			return 0;
		}
		$kind  = $HcomMissileSPP;
		$kind2 = $HcomSpecialSPP;
	}

	if (   ( $kind == $HcomOMissilePP )
		|| ( $kind == $HcomOMissileSPP )
		|| ( $kind == $HcomOMissileNM ) )
	{

		# 海域系
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

	# 導出値
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
"$Hatkturnターンの間、攻撃系コマンドは自島以外禁止されている"
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

		# ターゲットが関係ない命令のとき
	}
	else {
		if ( $HdefenceHex[$target] == 1 ) {
			logOut(
"${HtagName_}$name$AfterName${H_tagName}の${HtagComName_}$comName${H_tagComName}は、目標がスーパーシールドシステム２発動中のため失敗しました。",
				$id, $target
			);
			return 1;
		}
		if ( $target > 90 ) {

			# Battle Fieldのとき
			if (   ( $kind < 50 )
				|| ( $kind == $HcomMissileNM )
				|| ( $kind == $HcomMissilePP )
				|| ( $kind == $HcomSendMonster )
				|| ( $kind == $HcomEmigration ) )
			{

				# 許可された命令
			}
			else {
				logMiss( $id, $name, $comName,
					"ターゲットがBattle Fieldの" );
				return 0;
			}
		}
	}

	if ( $kind == $HcomDoNothing ) {

		# 資金繰り
		$island->{'turnsu'}--;

		#	logDoNothing($id, $name, $comName);
		$island->{'money'} += 10;
		$island->{'absent'}++;

		# 自動放棄
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

	# コストチェック
	if ( $cost > 0 ) {

		# 金の場合
		if ( $island->{'money'} < $cost ) {
			logMiss( $id, $name, $comName, "資金不足の" );
			return 0;
		}
	}
	elsif ( $cost < 0 ) {

		# 食料の場合
		if ( $island->{'food'} < ( -$cost ) ) {
			logMiss( $id, $name, $comName, "備蓄食料不足の" );
			return 0;
		}
	}

	# コマンドで分岐
	if ( ( $kind == $HcomPrepare ) || ( $kind == $HcomPrepare2 ) ) {

		# 整地、地ならし
		if (   ( $landKind == $HlandSea )
			|| ( ( $landKind == $HlandOil ) && ( $lv == 0 ) )
			|| ( $landKind == $HlandOsen )
			|| ( $landKind == $HlandMountain )
			|| ( $landKind == $HlandMonster )
			|| ( $landKind == $HlandKInora )
			|| ( $landKind == $HlandBreakwater )
			|| ( $HseaChk[$landKind] == 2 ) )
		{

	  # 海、油田、山、怪獣、汚染土壌、船系は整地できない
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
			$land->[$x][$y] = $HlandPlains;  # 目的の場所を平地にする
		}
		$landValue->[$x][$y] = 0;

		if ($HlogOmit2) {
			my $sno = $island->{'seichi'};
			$island->{'seichi'}++;
			if ( $HlogOmit2 == 1 ) {
				my $seichipnt;
				( $seichipnt->{x}, $seichipnt->{y}, $seichipnt->{z} ) =
				  ( $x, $y, '整地' );
				$island->{'seichipnt'}->[$sno] = $seichipnt;
			}
		}
		else {
			logLandSuc( $id, $name, '整地', $point );
		}

		# 金を差し引く
		$island->{'money'} -= $cost;

		if ( $kind == $HcomPrepare2 ) {

			# 地ならし
			$island->{'prepare2'}++;
			return 0;
		}
		else {

			# 整地なら、埋蔵金の可能性あり
			if ( random(1000) < $HdisMaizo ) {
				my ($v) = 100 + random(901);
				$island->{'money'} += $v;
				logMaizo( $id, $name, $comName, $v );
			}
			return 1;
		}
	}
	elsif ( ( $kind == $HcomReclaim ) || ( $kind == $HcomReclaim2 ) ) {

		# 埋め立て、高速埋め立て

		# 周りに陸があるかチェック
		my ($seaCount) = seaAround( $land, $x, $y, 7 );

		if (   ( $landKind == $HlandPlains )
			&& ( $seaCount == 0 )
			&& ( $kind == $HcomReclaim )
			&& ( countAround( $land, $x, $y, $HlandMountain, 7 ) > 1 )
			&& ( chkAround( $land, $x, $y, $HlandFuji, 7 ) == 0 ) )
		{

# 平地で周囲１へクスに山が２つ以上で、周囲に海系、富士山が無い地形に埋め立て(高速はだめ)で、富士山ができる！？
			$land->[$x][$y]      = $HlandFuji;
			$landValue->[$x][$y] = 0;
			fujiAround( $land, $landValue, $x, $y, 0 );
			$island->{'money'} -= $cost;
			logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}で${HtagComName_}富士山造成${H_tagComName}が行われました。突如として周囲の地盤が隆起し富士山になりました。",
				$id
			);
			return 1;
		}

		if ( $HseaChk[$landKind] == 0 || $HseaChk[$landKind] == 2 ) {

		 # 海、海底基地、油田、防波堤しか埋め立てできない
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}

		if ( $seaCount == 7 ) {

			# 全部海だから埋め立て不能
			logNoLandAround( $id, $name, $comName, "陸地", $point );
			return 0;
		}

		if (   ( $landKind == $HlandSea ) && ( $lv >= 1 )
			|| ( $landKind == $HlandBreakwater ) && ( $lv >= 1 ) )
		{

			# 浅瀬か防波堤の場合
			# 目的の場所を荒地にする
			$land->[$x][$y]      = $HlandWaste;
			$landValue->[$x][$y] = 0;
			$island->{'area'}++;

			if ( $seaCount <= 4 ) {

				# 周りの海が3ヘックス以内なので、浅瀬にする
				my ( $i, $sx, $sy );
				for ( $i = 1 ; $i < 7 ; $i++ ) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];
					$sx--
					  if ( !( $sy % 2 ) && ( $y % 2 ) )
					  ;    # 行による位置調整
					if (   ( $sx < 0 )
						|| ( $sx >= $HislandSize )
						|| ( $sy < 0 )
						|| ( $sy >= $HislandSize ) )
					{
					}
					else {

						# 範囲内の場合
						$landValue->[$sx][$sy] = 1
						  if ( $land->[$sx][$sy] == $HlandSea );
					}
				}
			}
		}
		else {

			# 海なら、目的の場所を浅瀬にする
			$land->[$x][$y]      = $HlandSea;
			$landValue->[$x][$y] = 1;
		}
		if ($HlogOmit2) {
			my $sno = $island->{'seichi'};
			$island->{'seichi'}++;
			if ( $HlogOmit2 == 1 ) {
				my $seichipnt;
				( $seichipnt->{x}, $seichipnt->{y}, $seichipnt->{z} ) =
				  ( $x, $y, '埋め立て' );
				$island->{'seichipnt'}->[$sno] = $seichipnt;
			}
		}
		else {
			logLandSuc( $id, $name, $comName, $point );
		}

		# 金を差し引く
		$island->{'money'} -= $cost;
		if ( $kind == $HcomReclaim2 ) {

			# 高速
			$island->{'prepare2'} += 4;

			# ターン消費せず
			return 0;
		}
		else {
			return 1;
		}
	}
	elsif ( ( $kind == $HcomDestroy ) || ( $kind == $HcomDestroy2 ) ) {

		# 掘削
		if (   ( $landKind == $HlandSbase )
			|| ( $landKind == $HlandOil )
			|| ( $landKind == $HlandMonster )
			|| ( $landKind == $HlandKInora )
			|| ( $HseaChk[$landKind] == 2 ) )
		{

			# 海底基地、油田、怪獣、船系は掘削できない
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

# 海なら、油田探し 平地、町、荒地で回数がある時は温泉を掘る
# 投資額決定
				$arg = 1 if ( $arg == 0 );
				my ( $value, $str, $p );
				$value = min( $arg * ($cost), $island->{'money'} );
				$str   = "$value$HunitMoney";
				$p     = int( $value / $cost );
				$p     = 50 if ( $p > 50 );                          # 最高50%
				$island->{'money'} -= $p * $cost;

				if ( $landKind == $HlandSea ) {

					# 見つかるか判定
					if ( $p > random(100) ) {

						# 油田見つかる
						logChosa( $id, $name, $point, $comName, $str,
							"、<B>油田</B>が掘り当てられま" );
						$land->[$x][$y]      = $HlandOil;
						$landValue->[$x][$y] = 0;
						$island->{'oilfield'}++;
					}
					else {

						# 無駄撃ちに終わる
						logChosa( $id, $name, $point, $comName, $str,
							"ましたが、油田は見つかりませんで"
						);
					}
				}
				elsif ( $p +
					( countAround( $land, $x, $y, $HlandMountain, 7 ) * 10 ) >
					random(100) )
				{

					# 温泉見つかる
					logChosa( $id, $name, $point, $comName, $str,
						"、<B>温泉</B>が掘り当てられま" );
					$land->[$x][$y]      = $HlandWaste;
					$landValue->[$x][$y] = 20 + random( $p + 41 );
				}
				else {

					# 無駄撃ちに終わる
					logChosa( $id, $name, $point, $comName, $str,
"ましたが、温泉は見つからず荒地になりま"
					);
					$land->[$x][$y]      = $HlandWaste;
					$landValue->[$x][$y] = 1;
				}
				return 1;
			}
		}

   # 目的の場所を海にする。山なら荒地に。浅瀬なら海に。
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
				  ( $x, $y, '掘削' );
				$island->{'seichipnt'}->[$sno] = $seichipnt;
			}
		}
		else {
			logLandSuc( $id, $name, $comName, $point );
		}

		# 金を差し引く
		$island->{'money'} -= $cost;
		if ( $kind == $HcomDestroy2 ) {

			# 高速
			$island->{'prepare2'} += 4;
			return 0;
		}
		else {
			return 1;
		}
	}
	elsif ( $kind == $HcomSellTree ) {

		# 伐採
		if ( $landKind == $HlandForest ) {

			# 森の時は平地にする
			$land->[$x][$y]      = $HlandPlains;
			$landValue->[$x][$y] = 0;
		}
		elsif ( ( $landKind == $HlandSea ) && ( $lv >= 10 ) ) {

			# 養殖場の時は浅瀬にする
			$land->[$x][$y]      = $HlandSea;
			$landValue->[$x][$y] = 1;
			$comName             = '魚売却';
		}
		else {

			# 伐採できない時
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
		logLandSuc( $id, $name, $comName, $point );

		# 売却金を得る
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

		# 地上建設系
		if ( ( $landKind == $HlandForest ) && ( $kind != $HcomPlant ) ) {

			# 森は前処理で自動伐採
			$island->{'money'} += $HtreeValue * $lv;
			logLandSuc( $id, $name, "自動伐採", $point );
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

			# 不適当な地形
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}

		# 種類で分岐
		if ( $kind == $HcomPlant ) {

			# 浅瀬を養殖場にする
			if ( ( $landKind == $HlandSea ) && ( $lv == 1 ) ) {
				$landValue->[$x][$y] = 10;    # 魚は1000匹から
				logLandSuc( $id, $name, '養殖場整備', $point );
			}
			else {

				# 目的の場所を森にする。
				$land->[$x][$y]      = $HlandForest;
				$landValue->[$x][$y] = 1;              # 木は最低単位
				logPBSuc( $id, $name, $comName, $point );
			}
		}
		elsif ( $kind == $HcomFarm ) {

			# 農場
			if ( $landKind == $HlandFarm ) {

				# すでに農場の場合
				$landValue->[$x][$y] += 5;             # 規模 + 5000人
				$landValue->[$x][$y] = 50
				  if ( $landValue->[$x][$y] > 50 );    # 最大 50000人
			}
			else {

				# 目的の場所を農場に
				$land->[$x][$y]      = $HlandFarm;
				$landValue->[$x][$y] = 10;             # 規模 = 10000人
			}
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomFactory ) {

			# 工場
			if ( $landKind == $HlandFactory ) {

				# すでに工場の場合
				$landValue->[$x][$y] += 10;            # 規模 + 10000人
				$landValue->[$x][$y] = 100
				  if ( $landValue->[$x][$y] > 100 );    # 最大 100000人
			}
			else {

				# 目的の場所を工場に
				$land->[$x][$y]      = $HlandFactory;
				$landValue->[$x][$y] = 30;
			}
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomTower ) {

			# 商業ビル
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

			# 港
			if ( seaAround( $land, $x, $y, 7 ) == 0 ) {

				# 周囲に海系が無い場合建設不可
				logNoLandAround( $id, $name, $comName, "海", $point );
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

			# 目的の場所をミサイル基地にする。
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

			# 目的の場所をハリボテにする
			$island->{'Afmissile'} = 1;
			$land->[$x][$y]        = $HlandHaribote;
			$landValue->[$x][$y]   = 0;
			logHariSuc( $id, $name, $comName, $HcomName[$HcomDbase], $point );
			return 0;
		}
		elsif ( $kind == $HcomDokan ) {

			# 土管(地下)建設
			my ( $ugL, $ugV, $ugX, $ugY ) = (
				$island->{'ugL'}, $island->{'ugV'},
				$island->{'ugX'}, $island->{'ugY'}
			);
			my ($i);
			$arg = $HugMax;
			for ( $i = 0 ; $i < $HugMax ; $i++ ) {
				if ( ( $ugX->[$i] == $x ) && ( $ugY->[$i] == $y ) ) {

					# 既に地下がある
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

			# 銀行
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

				# 目的の場所を転移装置にする
				my ($tn) = $HidToNumber{$target};
				return 0 if ( $tn eq '' );
				$land->[$x][$y]      = $HlandWarp;
				$landValue->[$x][$y] = $target;
			}
			else {
				$land->[$x][$y]      = $HlandWarpR;
				$landValue->[$x][$y] = $arg;
				$comName             = '転移先装置建設';
			}
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomDbase ) {

			# 防衛施設
			$island->{'defence'} = 1;    # フラグON
			if ( $landKind == $HlandDefence ) {

				# すでに防衛施設の場合
				$landValue->[$x][$y] = 1;    # 自爆装置セット
				logBombSet( $id, $name, $landName, $point );
			}
			elsif ( $landKind == $HlandSea ) {
				$land->[$x][$y]      = $HlandOil;
				$landValue->[$x][$y] = 5;
				logLandSuc( $id, $name, $comName, $point );
			}
			else {

				# 目的の場所を防衛施設に
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

			# 消防署、海底消防署
			if ( $landKind == $HlandSea ) {
				$land->[$x][$y]      = $HlandOil;
				$landValue->[$x][$y] = 7;
				logLandSuc( $id, $name, "海底消防署建設", $point );
			}
			else {
				$land->[$x][$y]      = $HlandFire;
				$landValue->[$x][$y] = 0;
				$cost                = int( $cost / 2 );
				logLandSuc( $id, $name, $comName, $point );
			}
		}
		elsif ( $kind == $HcomMonument ) {

			# 記念碑
			if (   ( $landKind == $HlandMonument )
				&& ( $lv <= $HmonumentRocket )
				&& ( $lv != 3 ) )
			{

		# すでに記念碑の場合 ロケット台、廉価記念碑は除く
		# ターゲット取得
				my ($tn) = $HidToNumber{$target};
				return 0 if ( $tn eq '' );
				my ($tIsland) = $Hislands[$tn];
				if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
					|| ( $tIsland->{'evil'} == 0 ) )
				{

					# 相手が途上国の為中止。
					logUNMiss( $id, $target, $name, $tIsland->{'name'},
						$comName );
					return 0;
				}
				$island->{'evil'} += 60;

				# その場所は荒地に
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

				# ロケット発射
				my ( $wkind, $wname, $whp, $wkind2, $wkind3 ) =
				  weatherinfo( $island->{'weather'} );
				if ( $wkind > 1 ) {
					logMiss( $id, $name, "ロケット打ち上げ",
						"天候不順の" );
					if ( ( $island->{'order'} & 512 ) && ( $Hwflg > 0 ) )
					{    # 自信ないんで回数制減
						slideBack(
							$comArray, $cNo, $kind, $target, $x,
							$y,        $arg, $x2,   $y2,     $Hwflg
						);    # フラグ付きで命令戻す
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

# 宇宙賞受賞のログはターン処理の最後の方で出力　理由は途中で出力するとターン処理に失敗した時多重にでるから？
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

				# ミサイル基地の時、ロケット台建設
				$land->[$x][$y]      = $HlandMonument;
				$landValue->[$x][$y] = $HmonumentRocket + 1;
				logLandSuc( $id, $name, "ロケット台建設", $point );
			}
			else {

				# 目的の場所を記念碑に
				$land->[$x][$y] = $HlandMonument;
				if ( $arg == 3 ) {

					# 廉価記念碑
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

			# お花を植える
			$land->[$x][$y]      = $HlandFlower;
			$landValue->[$x][$y] = random(13) + 1;
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomTrump ) {

			# トランプ設置
			$land->[$x][$y]      = $HlandTrump;
			$landValue->[$x][$y] = 0;
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomPolice ) {

			# 警察署
			$land->[$x][$y]      = $HlandPolice;
			$landValue->[$x][$y] = 0;
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomHospital ) {

			# 病院
			$land->[$x][$y]      = $HlandHospital;
			$landValue->[$x][$y] = 0;
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomWindmill ) {

			# 風車
			$land->[$x][$y]      = $HlandWindmill;
			$landValue->[$x][$y] = 0;
			logLandSuc( $id, $name, $comName, $point );
		}
		elsif ( $kind == $HcomDeathtrap ) {

			# デストラップ
			if ( $landKind == $HlandSea ) {
				$land->[$x][$y]      = $HlandOil;
				$landValue->[$x][$y] = 6;
				$comName             = "海底デストラップ建設";
			}
			elsif ( $landKind == $HlandDeathtrap ) {

				# すでにデストラップの場合
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

			# マイホーム
			if ( $landKind == $HlandMyhome ) {
				$landValue->[$x][$y] += 3;
				$landValue->[$x][$y] = 12 if ( $landValue->[$x][$y] > 12 );
			}
			elsif ( $island->{'myhome'} == 1 ) {

				# すでにある 何も言わずに中止
				return 0;
			}
			else {
				$land->[$x][$y] = $HlandMyhome;

				$landValue->[$x][$y] = 0;
			}
			logLandSuc( $id, $name, $comName, $point );
		}

		# 金を差し引く
		$island->{'money'} -= $cost;

		# 回数付きなら、コマンドを戻す
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
		#w		# 戦争系は連続開発が可能
		#w		$island->{'dcount'}++;
		#w		return 0;
		#w	}else{
		#w		return 1;
		#w	}

	}
	elsif ( $kind == $HcomMountain ) {

		# 採掘場
		if ( $landKind != $HlandMountain ) {

			# 山以外には作れない
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
		$landValue->[$x][$y] += 10;    # 規模 + 10000人
		if ( $landValue->[$x][$y] > 200 ) {    # 最大 200000人
			$landValue->[$x][$y] = 200;
			logMiss( $id, $name, $comName, "既に最大規模の" );
			return 0;
		}
		if ( random(250) < $HdisMaizo ) {      # 金鉱脈発見の確率あり
			my ($v) = 200 + random(1001);
			$island->{'money'} += $v;
			logGold( $id, $name, $comName, $v );
		}
		logLandSuc( $id, $name, $comName, $point );

		# 金を差し引く
		$island->{'money'} -= $cost;
		if ( $arg > 1 ) {
			$arg--;
			slideBack( $comArray, $cNo, $kind, $target, $x, $y, $arg );
		}
		return 1;
	}
	elsif ( ( $kind == $HcomSFarm ) || ( $kind == $HcomPropaganda ) ) {

		# 海底農場,誘致活動
		if ( $kind == $HcomPropaganda ) {    # 誘致活動
			logPropaganda( $id, $name, $comName );
			$island->{'propaganda'} = 1;
		}
		else {                               # 海底農場
			if ( ( $landKind == $HlandOil ) && ( $lv >= 10 ) && ( $lv <= 30 ) )
			{

				# すでに海底農場の場合
				$landValue->[$x][$y] += 5;
				$landValue->[$x][$y] = 30 if ( $landValue->[$x][$y] > 30 );
			}
			elsif ( ( $landKind != $HlandSea ) || ( $lv != 0 ) ) {

				# 海以外には作れない
				logLandFail( $id, $name, $comName, $landName, $point, $landKind,
					$lv );
				return 0;
			}
			else {

				# 目的の場所を海底農場に
				$land->[$x][$y]      = $HlandOil;
				$landValue->[$x][$y] = 10;
			}
			logLandSuc( $id, $name, $comName, $point );
		}

		# 金を差し引く
		$island->{'money'} -= $cost;
		if ( $arg > 1 ) {
			$arg--;
			slideBack( $comArray, $cNo, $kind, $target, $x, $y, $arg );
		}
		return 1;
	}
	elsif ( ( $kind == $HcomSbase ) || ( $kind == $HcomScity ) ) {

		# 海底基地、海底都市
		if ( ( $landKind != $HlandSea ) || ( $lv != 0 ) ) {

			# 海以外には作れない
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
		if ( $kind == $HcomSbase ) {
			$land->[$x][$y]      = $HlandSbase;
			$landValue->[$x][$y] = 0;             # 経験値0
			logLandSuc( $id, $name, $comName, '(?, ?)' );
		}
		else {
			my ( $wkind, $wname, $whp, $wkind2, $wkind3 ) =
			  weatherinfo( $island->{'weather'} );
			if ( $wkind > 2 ) {
				logMiss( $id, $name, $comName, "天候不順の" );
				if ( ( $island->{'order'} & 512 ) && ( $Hwflg > 0 ) )
				{    # 自信ないんで回数制減
					slideBack(
						$comArray, $cNo, $kind, $target, $x,
						$y,        $arg, $x2,   $y2,     $Hwflg
					);    # フラグ付きで命令戻す
					$Hwflg--;
				}
				return 0;
			}
			$land->[$x][$y]      = $HlandOil;
			$landValue->[$x][$y] = 35;
			logLandSuc( $id, $name, $comName, $point );
		}

		# 金を差し引く
		$island->{'money'} -= $cost;
		return 1;
	}
	elsif ( $kind == $HcomSMonument ) {

		# 海底記念碑
		if ( $landKind == $HlandSMonument ) {

			# すでに海底記念碑の場合
			# ターゲット取得
			my ($tn) = $HidToNumber{$target};
			return 0 if ( $tn eq '' );
			my ($tIsland) = $Hislands[$tn];
			if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
				|| ( $tIsland->{'evil'} == 0 ) )
			{

				# 相手が途上国の為中止。
				logUNMiss( $id, $target, $name, $tIsland->{'name'}, $comName );
				return 0;
			}
			$island->{'evil'} += 70;

			# その場所は海に
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

			# 海以外には作れない
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
		else {

			# 目的の場所を記念碑に
			$land->[$x][$y] = $HlandSMonument;
			$arg = 0 if ( $arg >= $HsmonumentNumber );
			$landValue->[$x][$y] = $arg;
			logLandSuc( $id, $name, $comName, $point );
		}
		$island->{'money'} -= $cost;
		return 1;
	}
	elsif ( $kind == $HcomBreakwater ) {

		# 防波堤
		if ( ( $landKind != $HlandSea ) || ( $lv != 1 ) ) {

			# 浅瀬以外には作れない
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

		# 造船
		# 周囲２マスに港があるかチェック
		return 0 if ( !chkAround( $land, $x, $y, $HlandPort, 19 ) );

		# 浅瀬か、追加可能の自船かチェック
		if ( ( $landKind == $HlandSea ) && ( $lv > 0 ) ) {

			# 造船
			$land->[$x][$y]      = $HlandFishSShip;
			$landValue->[$x][$y] = 21000 + $id;       # 初期指令は防御
			$island->{'land2'}->[$x][$y]      = $HlandSea;
			$island->{'landValue2'}->[$x][$y] = 1;
			$comName                          = "漁船造船";
		}
		elsif (( $landKind == $HlandFishSShip )
			|| ( $landKind == $HlandFishMShip ) )
		{

			# 小型、中型漁船
			my ( $order, $hp, $sId ) = shipSpec($lv);
			return 0
			  if ( $sId != $id )
			  ;    # ターゲットが自船でないため中止
			if ( $landKind == $HlandFishMShip ) {
				if ( $arg == 1 ) {

					# 豪華客船
					$land->[$x][$y] = $HlandTitanic;
					$comName = "豪華客船造船";
				}
				elsif ( $arg == 2 ) {

					# イージス艦
					$land->[$x][$y] = $HlandAegisShip;
					$comName = "イージス艦造船";
				}
				else {
					$land->[$x][$y] = $HlandFishLShip;
					$comName = "漁船追加造船";
				}
			}
			else {

				# 小型
				if ( $arg == 1 ) {

					# 海底探査船
					$land->[$x][$y] = $HlandProbeShip;
					$comName = "海底探査船造船";
				}
				elsif ( $arg == 2 ) {

					# 海獣掃討艇
					$land->[$x][$y] = $HlandMonsShip;
					$comName = "海獣掃討艇造船";
				}
				else {
					$land->[$x][$y] = $HlandFishMShip;
					$comName = "漁船追加造船";
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

		# プレゼント,プレゼント譲渡
		my ( $tn, $tIsland, $tName );
		if ( $kind == $HcomPresent ) {
			if (
				!(
					( $landKind == $HlandPlains ) || ( $landKind == $HlandTown )
				)
			  )
			{

				# 不適当な地形
				logLandFail( $id, $name, $comName, $landName, $point, $landKind,
					$lv );
				return 0;
			}
		}
		else {
			$tn = $HidToNumber{$target};
			return 0 if ( $tn eq '' );    # 何も言わずに中止
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

				# ありえないけどとりあえず荒地にしとく
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

		# 工作員派遣、偵察
		my ($tn) = $HidToNumber{$target};
		return 0
		  if ( $tn eq '' )
		  ;    # ターゲットがすでにないため何も言わずに中止
		my ($tIsland) = $Hislands[$tn];
		if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
			|| ( $tIsland->{'evil'} == 0 ) )
		{

			# 相手が途上国の為中止。
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
			if ( random(5) == 0 ) {    # 失敗
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

			   #					HdebugOut("目標周囲３ヘクスに警察署は失敗");
					logSpyF( $id, $target, $name, $tName, $comName );
					return 1;
				}
				elsif (( $tLand->[$tx][$ty] == $HlandAegisShip )
					&& ( $HseaChk[ $tLand->[$x][$y] ] ) )
				{
					my ( $order, $hp, $sId ) =
					  shipSpec( $tLandValue->[$tx][$ty] );
					if ( $sId == $target ) {

#						HdebugOut("目標が海系で周囲３ヘクスにイージス艦は失敗");
						logSpyF( $id, $target, $name, $tName, $comName );
						return 1;
					}
				}
			}

			#			HdebugOut("工作員２次チェック成功！");
			if ( $arg == 0 ) {

				# 地震発生させる
				if ( ( $HseaChk[ $tLand->[$x][$y] ] ) && ( random(2) == 0 ) ) {

					# 海の場合は５０％で失敗
					logSpyF( $id, $target, $name, $tName, $comName );
					return 1;
				}
				$comName = "工作員派遣：地震";
				addCommandLate( 3, $HislandTurn, $id, $kind, $target, $x, $y,
					$arg, $x2, $y2 );    # ターン差命令
			}
			elsif ( $arg == 1 ) {

				# アルミ箔散布
				$comName = "工作員派遣：アルミ箔散布($x,$y)";
				addCommandLate( 1, $HislandTurn, $id, $kind, $target, $x, $y,
					$arg, $x2, $y2 );    # ターン差命令
			}
			else {

				# 食料焼き討ち
				$comName = "工作員派遣：食料焼き討ち";
				$tIsland->{'food'} -= int( $tIsland->{'food'} * 0.2 );
				logLate(
"${HtagName_}${tName}${AfterName}${H_tagName}の食糧の一部が何者かにより燃やされました。",
					$target
				);
			}
			logSecret(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${AfterName}${H_tagName}に${HtagComName_}$comName${H_tagComName}を行い見事成功しました。",
				$id
			);
			return 1;
		}
		else {

			#	$arg = 1 if($arg < 1);
			#	$arg = 37 if($arg > 36); # 最大37マス
			$arg = 37;
		}

		# 選んだ数量だけ調べる
		for ( $i = 0 ; $i < $arg ; $i++ ) {

			#	if(random(25) == 0){ # 失敗
			#		logSpyF($id, $target, $name, $tName, $comName);
			#		last;
			#	}
			$tx = $x + $ax[$i];
			$ty = $y + $ay[$i];
			$tx-- if ( !( $ty % 2 ) && ( $y % 2 ) );  # 行による位置調整
			next
			  if ( ( $tx < 0 )
				|| ( $tx >= $HislandSize )
				|| ( $ty < 0 )
				|| ( $ty >= $HislandSize ) );

			# 地形等算出
			my ($tL)     = $tLand->[$tx][$ty];
			my ($tLv)    = $tLandValue->[$tx][$ty];
			my ($tLname) = landName( $tL, $tLv );
			my ($tPoint) = "($tx, $ty)";
			if ( ( $tL == $HlandBase ) || ( $tL == $HlandSbase ) )
			{    # ミ基地、海底ミ基地の時
				logBeseFind( $id, $tName, $tPoint, $tLv, $tLname );
			}
			elsif ( ( $tL == $HlandForest ) || ( $tL == $HlandDefence ) ) {
				logLandTruth( $id, $tName, $tPoint, $tLname, '本物' );
			}
			elsif ( ( $tL == $HlandHaribote ) && ( $tLv == 0 ) ) {
				logLandTruth( $id, $tName, $tPoint, '防衛施設', $tLname );
			}
			elsif ( ( $tL == $HlandHaribote ) && ( $tLv > 0 ) ) {
				logLandTruth( $id, $tName, $tPoint, '防衛施設',
					'ハリボテいのら' );
			}
			elsif ( $tL == $HlandBank ) {
				logLandTruth( $id, $tName, $tPoint, '森', $tLname );
			}
			elsif ( $tL == $HlandGhostShip ) {
				logLandTruth( $id, $tName, $tPoint, '海', $tLname )
				  ;    # 幽霊船
			}
			elsif ( $tL == $HlandPirate ) {
				logLandTruth( $id, $tName, $tPoint, '海賊船', $tLname )
				  ;    # 海賊船
			}
		}
		$island->{'money'} -= $cost;
		return 1;
	}
	elsif ( $kind == $HcomPioneer ) {

		# 入植
		if ( $landKind != $HlandPlains ) {

			# 平地以外ではできない。
			logLandFail( $id, $name, $comName, $landName, $point, $landKind,
				$lv );
			return 0;
		}
		$land->[$x][$y]      = $HlandTown;
		$landValue->[$x][$y] = 1;
		logLandSuc( $id, $name, $comName, $point );

		# 食糧を差し引く
		$island->{'food'} += $cost;
		return 1;
	}
	elsif ( $kind == $HcomDummy ) {

		# ダミー命令
		if ( $arg == 1 ) {
			$comName = '採掘場整備';
		}
		elsif ( $arg == 2 ) {
			$comName = '埋め立て';
		}
		else {
			$comName = '農場整備';
		}
		if ( ( $arg == 2 ) && ($HlogOmit2) ) {
			my $sno = $island->{'seichi'};
			$island->{'seichi'}++;
			if ( $HlogOmit2 == 1 ) {
				my $seichipnt;
				( $seichipnt->{x}, $seichipnt->{y}, $seichipnt->{z} ) =
				  ( $x, $y, '埋め立て' );
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

		# 地下建設
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

			# 合成石油
			return 0;
		}
		$landValue->[$x][$y]--
		  if ( ( $ugL->[$i][$v] == $HugKiti ) && ( $landValue->[$x][$y] > 0 ) );
		if ( $arg <= 0 ) {
			$ugL->[$i][$v] = $HugTosi;
			$ugV->[$i][$v] = 1;
			$comName       = "地下都市建設";
		}
		elsif ( $arg == 1 ) {
			$ugL->[$i][$v] = $HugFarm;
			$ugV->[$i][$v] = 10;
			$comName       = "地下農場建設";
		}
		elsif ( $arg == 2 ) {
			$ugL->[$i][$v] = $HugFact;
			$ugV->[$i][$v] = 30;
			$comName       = "地下工場建設";
		}
		elsif ( $arg == 3 ) {
			$ugL->[$i][$v] = $HugKiti;
			$ugV->[$i][$v] = 0;
			$comName       = "地下ミサイル基地";
			$landValue->[$x][$y]++;
		}
		else {
			$ugL->[$i][$v] = $HugOil;
			$ugV->[$i][$v] = 30;
			$cost *= 3;
			$comName = "地下合成石油工場建設";
		}
		$island->{'money'} -= $cost;
		logPBSuc( $id, $name, $comName, "($x, $y)の($x2, $y2)" );
		return 1;
	}
	elsif ( $kind == $Hcomcolony ) {

		# コロニー落し
		if ( $arg == 1 ) {
			logEvent( $id, $name,
"が、<B>スーパーシールドシステム</B>を発動！！"
			);
			$island->{'SSSystem'} = 1;
			$island->{'Crime'}    = 1;
			$island->{'money'} -= $cost;
			return 1;
		}
		elsif ( $arg == 2 ) {
			$island->{'money'} -= $cost;
			addCommandLate( 1, $HislandTurn, $id, $kind, $target, $x, $y, $arg,
				$x2, $y2 );    # ターン差命令
			return 1;
		}
		my ($tn) = $HidToNumber{$target};
		return 0
		  if ( $tn eq '' )
		  ;    # ターゲットがすでにないため何も言わずに中止
		my ($prize) = $island->{'prize'};
		$prize =~ /([0-9]*),([0-9]*),(.*)/;
		my ( $flags, $monsters, $turns ) = ( $1, $2, $3 );
		if ( !( $flags & 512 ) ) {

			# 技術不足により中止
			logMiss( $id, $name, $comName, "技術不足の" );
			return 0;
		}
		my ($tIsland) = $Hislands[$tn];
		my ($tName)   = $tIsland->{'name'};
		if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
			|| ( $tIsland->{'evil'} == 0 ) )
		{

			# 相手が途上国の為中止。
			logUNMiss( $id, $target, $name, $tName, $comName );
			return 0;
		}

#	極悪なのでコメント・・・。あぁ一度は使いたい。。
#		if($arg == 49){
#			$HpunishInfo{$target}->{punish} = 10;
#			$HpunishInfo{$target}->{x} = $x;
#			$HpunishInfo{$target}->{y} = $y;
#			logEventT($id, $target, $name,"が<B>究想いのらを召喚し</B>${HtagName_}${tName}${AfterName}${H_tagName}に向けて出撃させました。");
#			return 1;
#		}elsif($arg == 48){
#			my($i);
#			my($tAlly) = $tIsland->{'ally'};
#			logEvent($id, $name,"が、<B>多弾頭核ミサイル</B>を$Hallygroup[$tAlly]陣営に向けて発射した模様！！");
#			for($i = 0; $i < $HislandNumber; $i++){
#				$tIsland = $Hislands[$i];
#				my($ttAlly) = $tIsland->{'ally'};
#				if($tAlly == $ttAlly){
#					$target = $tIsland->{'id'};
#					$tName = $tIsland->{'name'};
#					logOut("多弾頭核ミサイルは、${HtagName_}${tName}${AfterName}($x,$y)${H_tagName}に命中し周囲にも被害が出ました。",$id, $target);
#					wideDamage($target, $tName, $tIsland->{'land'}, $tIsland->{'landValue'}, $x, $y, 1);
#				}
#			}
#			return 1;
#		}elsif($arg == 47){
#			my($i);
#			my($tAlly) = $tIsland->{'ally'};
#			logEvent($id, $name,"が、<B>究想いのらを召喚し</B>$Hallygroup[$tAlly]陣営に向けて出撃させました。");
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
				"コロニー降下に必要な兵器不足の" );
			return 0;
		}
		my ( $wkind, $wname, $whp, $wkind2, $wkind3 ) =
		  weatherinfo( $tIsland->{'weather'} );
		if ( $wkind > 1 && $island->{'eis3'} != 1 ) {
			logMiss( $id, $name, $comName, "標的が天候不順の" );
			if ( ( $island->{'order'} & 512 ) && ( $Hwflg > 0 ) )
			{    # 自信ないんで回数制減
				slideBack(
					$comArray, $cNo, $kind, $target, $x,
					$y,        $arg, $x2,   $y2,     $Hwflg
				);    # フラグ付きで命令戻す
				$Hwflg--;
			}
			return 0;
		}
		$arg = 0;
		$island->{'weapon'} -= 200;
		$island->{'evil'} += 200;
		logEventT( $id, $target, $name,
"が<B>スペースコロニー</B>を${HtagName_}${tName}${AfterName}${H_tagName}に向けて降下させました。"
		);

		# 金を差し引く
		$island->{'money'} -= $cost;

		addCommandLate( $HcomcolonyTurn, $HislandTurn, $id, $kind, $target, $x,
			$y, $arg, $x2, $y2 );    # ターン差命令

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

		# ミサイル系

		# ターゲット取得
		my ($tn) = $HidToNumber{$target};
		if ( $tn eq '' ) {

			# ターゲットがすでにない
			logMsNoTarget( $id, $name, $comName );

			return 0;
		}

		# 撃てる数を算出
		if ( ( $kind == $HcomMissileGM ) || ( $kind == $HcomMissileMGM ) ) {
			$arg = 1;
		}
		elsif ( $arg == 0 ) {

			# 0の場合は撃てるだけ
			$arg = 10000;
		}

		# 事前準備
		my ($tIsland) = $Hislands[$tn];
		my ( $tName, $tLand, $tLandValue, $flag, $boat ) = (
			$tIsland->{'name'}, $tIsland->{'land'}, $tIsland->{'landValue'},
			0, 0
		);
		my ( $tx, $ty, $err );

		#		if($kind != $HcomMissileRM){ # 埋め立て弾以外
		$island->{'evil'} += 30 if ( $id != $target );
		if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
			|| ( $tIsland->{'evil'} == 0 ) )
		{

			# 相手が途上国の為中止。
			logUNMiss( $id, $target, $name, $tName, $comName );
			return 0;
		}

		#		}
		my $we            = 1;    # 兵器
		                          # 破壊ミサイル
		my ($DestMissile) = 0;
		if (   ( $kind == $HcomMissileLD )
			|| ( $kind == $HcomMissilePLD )
			|| ( $kind == $HcomMissileNCM ) )
		{
			$DestMissile = 1;
			$we          = 10;
		}

		# 誤差
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
					"ミサイル発射に必要な兵器不足の" );
				return 0;
			}
			$island->{'weapon'} -= $we;
		}

		my ( $renzoku, $rouryoku ) = ( 0, 0 );
		if ( ( $kind == $HcomMissilePP ) || ( $kind == $HcomMissileNM ) ) {
			$command = $comArray->[$cNo];    # 次の命令を調べる
			     # 連続に撃てる対象の命令のとき
			if (   ( $command->{'kind'} == $HcomMissilePP )
				|| ( $command->{'kind'} == $HcomMissileNM ) )
			{
				$renzoku = 1;
			}
		}

		if ( $kind == $HcomMissileNCM ) {    # 核ミサイル
			if (   ( $tIsland->{'MissileK'} < 30 )
				&& ( $id != $target )
				&& ( !$HwarFlg ) )
			{
				logOut(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${AfterName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行おうとしましたが、激しい反核運動のため中止されました。",
					$id
				);
				return 0;
			}
			$rouryoku = 9;
		}

		# 戦争モードではお金の変わりに兵器を消費
		my $mcost = 'money';
		if ( ($HwarFlg) && ( $id != $target ) && ( $cost < 500 ) ) {
			$mcost = 'weapon';
			$cost  = int( $cost / 10 );
		}

		# ログをまとめる
		my ( $msCt, $mslogCtM, $mslogCtW, $mslogCtD ) = ( 0, 0, 0, 0 );

# 金が尽きるか指定数に足りるか基地全部が撃つまでループ、連続の時は続ける。
		my ( $bx, $by, $count, $level ) = ( 0, 0, 0, 0 );
		while (( ( $arg > 0 ) && ( $island->{'money'} >= $cost ) )
			|| ( ( $renzoku == 1 ) && ( $island->{$mcost} >= $cost ) ) )
		{

			# 基地を見つけるまでループ
			if ( $kind2 == $HcomSpecialSPP ) {

				# 海獣掃討艇によるSPP
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
				  ;    # 見つからなかったらそこまで
				$level =
				  expToLevel( $land->[$bx][$by], $landValue->[$bx][$by] )
				  ;    # 基地のレベルを算出
			}

			# 最低一つ基地があったので、flagを立てる
			$flag = 1;

			# 基地内でループ
			while ( ( $level > 0 ) && ( $island->{$mcost} > $cost ) ) {

				last if ( ( $arg <= 0 ) && ( $renzoku == 0 ) );

				# 撃ったのが確定なので、各値を消耗させる
				$level--;
				if ( $rouryoku > 0 ) { $rouryoku--; next; }    # 労力消費

				if ( ( $arg <= 0 ) && ( $renzoku == 1 ) ) {    # 連続の時

					slideFront( $comArray, $cNo );    # 以降を詰める

					# ミサイル発射数などのログ
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

					# 次の目標を入力
					$kind   = $command->{'kind'};
					$target = $command->{'target'};

					# ターゲット取得
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

						# サバイバルでは制限無し
					}
					else {
						$arg = 5 if ( ( $id != $target ) && ( $arg > 5 ) );
					}
					$err = ( $kind == $HcomMissilePP ) ? 7 : 19;

					$cost    = $HcomCost[$kind];
					$comName = $HcomName[$kind];
					$point   = "($x, $y)";

					# 戦争モードではお金の変わりに兵器を消費
					$mcost = 'money';
					if ( ($HwarFlg) && ( $id != $target ) && ( $cost < 500 ) ) {
						$mcost = 'weapon';
						$cost  = int( $cost / 10 );
					}

					# 命令を進ませる
					$command = $comArray->[$cNo];    # 最初のを取り出し

					$island->{'evil'} += 30 if ( $id != $target );
					if ( ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
						|| ( $tIsland->{'evil'} == 0 ) )
					{

						# 相手が途上国の為中止。
						logUNMiss( $id, $target, $name, $tName, $comName );
						return 1;
					}

					# 連続に撃てる対象の命令のとき
					if (   ( $command->{'kind'} == $HcomMissilePP )
						|| ( $command->{'kind'} == $HcomMissileNM ) )
					{
						$renzoku = 1;
					}
					else {
						$renzoku = 0;
					}
					if ($HsurvFlg) {

						# サバイバルでは労力１
					}
					else {
						$rouryoku = 2;
					}
					next;
				}

				$msCt++;    # 発射数を計算

				$arg--;
				$island->{$mcost} -= $cost;

				if ( $kind == $HcomMissileNCM ) {    # 核ミサイルの時
					$ncm      = 1;                   # ミサイルを撃った
					$rouryoku = 9;                   # 労力
				}

				if ( $kind == $HcomMissileMGM ) {    # 怪獣誘導弾の時
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
							"適当な怪獣がいなかった" );
						$island->{$mcost} += $cost;
						return 0;
					}
				}

				# 着弾点算出
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
				{    # 怪獣誘導弾は外さない
					    # 天候チェック
					if (
						   ( $id != $target )
						&& ( $kind != $HcomMissileRM )
						&& # 自分の島と埋め立てミサイルは天候に左右されない。
						( $island->{'eis3'} != 1 ) &&    # 軍事衛星が無い
						(
							   ( ( $wkind >= 2 ) && ( random(6) == 0 ) )
							|| ( ( $twkind >= 2 ) && ( random(6) == 0 ) )
						)
					  )
					{
						$mslogCtW++;
						next;
					}

					# イージス艦チェック
					if ( ( $id != $target ) && ( $tIsland->{'aegis'} > 0 ) ) {
						$tIsland->{'aegis'}--;
						if (   ( random(3) == 0 )
							&& ( $tIsland->{'money'} > 100 ) )
						{

							#					HdebugOut("イージス艦で防いだ");
							$tIsland->{'money'} -= 100;
							$mslogCtD++;
							next;
						}
					}

					# 防衛衛星チェック
					if (   ( $id != $target )
						&& ( $tIsland->{'eis4'} )
						&& ( random(2) == 0 ) )
					{

						#				HdebugOut("防衛衛星で防いだ");
						$tIsland->{'eis4'}++;
						$mslogCtD++;
						next;
					}

					# 着弾点範囲内外チェック
					if (   ( $tx < 0 )
						|| ( $tx >= $HislandSize )
						|| ( $ty < 0 )
						|| ( $ty >= $HislandSize ) )
					{
						$mslogCtM++;
						next;
					}
				}

				# 着弾点の地形等算出
				my ( $tL, $tLv ) =
				  ( $tLand->[$tx][$ty], $tLandValue->[$tx][$ty] );
				my ( $tLname, $tPoint ) =
				  ( landName( $tL, $tLv ), "($tx, $ty)" );

				if ( $tIsland->{'defence'} > 0 ) {

					# 防衛施設がある場合 防衛施設判定
					my ($defence) = 0;
					if ( $HdefenceHex[$target][$tx][$ty] == 1 ) {
						$defence = 1;
					}
					elsif (( $tL == $HlandDefence )
						|| ( ( $tL == $HlandOil ) && ( $tLv == 5 ) ) )
					{

					 # 防衛施設に命中
					 #				HdebugOut("防衛施設に命中:($tx,$ty) = ${tLv}");
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

							# フラグをクリア
							my ( $i, $count, $sx, $sy );
							for ( $i = 0 ; $i < 19 ; $i++ ) {
								$sx = $tx + $ax[$i];
								$sy = $ty + $ay[$i];
								$sx--
								  if ( !( $sy % 2 ) && ( $ty % 2 ) )
								  ;    # 行による位置調整
								if (   ( $sx < 0 )
									|| ( $sx >= $HislandSize )
									|| ( $sy < 0 )
									|| ( $sy >= $HislandSize ) )
								{

									# 範囲外の場合何もしない
								}
								else {

									# 範囲内の場合
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

						# 空中爆破
						$mslogCtD++;
						if ( $kind == $HcomMissileST ) {    # ステルス
							logMsCaughtH( $target, $name, $comName )
							  if ( random(25) == 0 );
						}
						if ( random(25) == 0 ) {

							# S防衛施設に進化する。
							my ( $i, $sx, $sy );
							for ( $i = 1 ; $i < 19 ; $i++ ) {
								$sx = $tx + $ax[$i];
								$sy = $ty + $ay[$i];
								$sx--
								  if ( !( $sy % 2 ) && ( $ty % 2 ) )
								  ;    # 行による位置調整
								if (   ( $sx < 0 )
									|| ( $sx >= $HislandSize )
									|| ( $sy < 0 )
									|| ( $sy >= $HislandSize ) )
								{

									# 範囲外の場合何もしない
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

				# 転送装置に落ちた場合
				if ( $tL == $HlandWarp ) {
					logOut(
"--- ${HtagName_}$tPoint${H_tagName}の<B>${tLname}</B>に着弾。<B>時空の狭間に吸い込まれました！！</B>",
						$id, $target
					);

					#		$tLand->[$tx][$ty] = $HlandWaste;
					#		$tLandValue->[$tx][$ty] = 0;
					my ($st) = warp( $id, $name, 0, 0, $comName, $tLv, 11 );
					next;
				}

				# 埋め立て弾
				if ( $kind == $HcomMissileRM ) {
					if (   ( $tIsland->{'area'} < $HdisFallBorder )
						&& ( ( $tL == $HlandSea ) && ( $tLv <= 1 ) ) )
					{
						if ( ( $tL == $HlandSea ) && ( $tLv == 0 ) ) {
							$tLand->[$tx][$ty]      = $HlandSea;
							$tLandValue->[$tx][$ty] = 1;
							logMsNormal( $id, $target, $tLname, $tPoint,
								"隆起し" );
						}
						else {
							$tLand->[$tx][$ty]      = $HlandWaste;
							$tLandValue->[$tx][$ty] = 1;
							$tIsland->{'area'}++;
							logMsNormal( $id, $target, $tLname, $tPoint,
								"隆起し" );
						}
					}
					else {
						$mslogCtD++;
					}
					next;
				}

				# 戦争用埋め立て弾
				if ( $kind == $HcomMissileSRM ) {
					if ( ( $tL == $HlandSea ) && ( $tLv > 0 ) ) {

						# 浅瀬関係の時
						$tLand->[$tx][$ty]      = $HlandWaste;
						$tLandValue->[$tx][$ty] = 1;
						$tIsland->{'area'}++;
					}
					elsif ( $HseaChk[$tL] ) {

						# 海関係の時
						$tLand->[$tx][$ty]      = $HlandSea;
						$tLandValue->[$tx][$ty] = 1;
					}
					else {
						$tLand->[$tx][$ty]      = $HlandWaste;
						$tLandValue->[$tx][$ty] = 1;
					}
					logMsNormal( $id, $target, $tLname, $tPoint, "隆起し" );
					next;
				}

				# 核ミサイル
				if ( $kind == $HcomMissileNCM ) {
					logOut(
"核は、${HtagName_}${tName}${AfterName}$tPoint${H_tagName}の<B>$tLname</B>に命中し周囲にも被害が出ました。",
						$id, $target
					);
					wideDamage( $target, $tName, $tLand, $tLandValue, $tx, $ty,
						1 );
					$tIsland->{'trump'}->[15] =
					  1;    # トランプイベントキャンセル
					next;
				}

				# 「効果なし」hexを最初に判定
				if (
					( ( $tL == $HlandSea ) && ( $tLv == 0 ) ) ||    # 深い海
					(
						(
							( ( $tL == $HlandSea ) && ( $tLv <= 1 ) )
							|| (   ( $tL == $HlandOsen )
								&& ( $kind != $HcomBioMissile ) )
							|| (   ( $HmonumentMissile == 1 )
								&& ( $tL == $HlandMonument ) )
							||    # （記念碑設定よる)
							( $tL == $HlandSMonument )
							||    # 海底記念碑または・・・
							( $tL == $HlandSbase )
							||    # 海底基地または・・・
							( $tL == $HlandMountain )
						)         # 山で・・・
						&& ( $DestMissile == 0 )
					)
				  )
				{                 # 破壊ミサイル以外
					$mslogCtM++;    # 無効化
					next;
				}

				# 弾の種類で分岐
				if ( $DestMissile == 1 ) {

					# 破壊ミサイル系

					if ( $tL == $HlandMountain ) {

						# 山(荒地になる)
						logMsLD( $id, $target, $tPoint,
							"の<B>$tLname</B>に命中し荒地と化し" );
						$tLand->[$tx][$ty]      = $HlandWaste;
						$tLandValue->[$tx][$ty] = 0;
						next;

					}
					elsif ( $tL == $HlandSbase ) {

						# 海底基地
						logMsLD( $id, $target, $tPoint,
"に着水後爆発し<B>$tLname</B>は跡形もなくなり"
						);
					}
					elsif ( $tL == $HlandMonster ) {

						# 怪獣
						logMsLD( $id, $target, $tPoint,
"に着弾後爆発し<B>怪獣$tLname</B>もろとも水没し"
						);
					}
					elsif ( $tL == $HlandSea || $tL == $HlandBreakwater ) {

						# 浅瀬、防波堤
						logMsLD( $id, $target, $tPoint,
							"の<B>$tLname</B>に着弾。海底がえぐられ"
						);
					}
					elsif ( $tL == $HlandKInora ) {

						# 究想いのら
						$mslogCtD++;    # 空中爆破
						next;
					}
					else {

						# その他
						logMsLD( $id, $target, $tPoint,
							"の<B>$tLname</B>に着弾。陸地は水没し" );
					}

					# 経験値
					if ( $tL == $HlandTown ) {
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandSbase ) )
						{

							# まだ基地の場合のみ
							$landValue->[$bx][$by] += int( $tLv / 20 );
							$island->{'allex'}     +=
							  int( $tLv / 20 );    # 経験値総獲得件数
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
						}
					}

					# 浅瀬になる
					$tLand->[$tx][$ty] = $HlandSea;
					$tIsland->{'area'}--;
					$tLandValue->[$tx][$ty] = 1;
					$tIsland->{'nation'}->[$tx][$ty] = $id
					  if ( $id != $target );

					# でも海系地形なら海
					$tLandValue->[$tx][$ty] = 0 if ( $HseaChk[$tL] );

					$tIsland->{'trump'}->[$tLv] = 0 if ( $tL == $HlandTrump );
				}
				else {

					# その他ミサイル
					if ( ( $tL == $HlandWaste ) && ( $tLv <= 1 ) ) {

						# 荒地
						if ( $kind == $HcomBioMissile ) {
							logBioMs( $id, $target, $tLname, $tPoint );
						}
						else {

							# 被害なし
							$mslogCtM++;    # 無効ミサイルにカウント
						}
					}
					elsif ( $tL == $HlandHugecity ) {

						# 超巨大都市はミサイルが効かない。
						$mslogCtM++;        # 無効ミサイルにカウント
						next;
					}
					elsif ( $tL == $HlandMonster ) {

						# 怪獣
						my ( $mKind, $mName, $mHp ) = monsterSpec($tLv);
						my ($special) = $HmonsterSpecial[$mKind];

						# 反撃いのら(ST以外)
						if (   ( $mKind == 18 )
							&& ( random(2) == 0 )
							&& ( $kind != $HcomMissileST ) )
						{
							if ( random(20) == 0 ) {
								logMonsCounter( $id, $target, $mName, $tPoint,
									"巨大隕石を呼び寄せました。" );
								$island->{'bigmissile'}++;
							}
							else {
								logMonsCounter( $id, $target, $mName, $tPoint,
									"隕石を呼ぼうとしている。" );
								$island->{'Meteo'} += 10;
							}
							next;
						}

						# 硬化中?
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

							# 硬化中
							if ( $kind == $HcomMissileST ) {

								# ステルス
								logMsMonNoDamageS(
									$id,      $target, $name,  $tName,
									$comName, $mName,  $point, $tPoint
								);
							}
							else {

								# 通常弾
								logMsMonNoDamage( $id, $target, $mName,
									$tPoint );
							}
							next;
						}
						else {

							# 硬化中じゃない
							if ( $mHp == 1 ) {

								# いのらゴーストがジバクレイに
								if ( ( $mKind == 5 ) && ( random(5) == 0 ) ) {
									logMonsRei( $id, $target, $mName, $tPoint );
									$tLandValue->[$tx][$ty] =
									  1500 + $HmonsterBHP[15] +
									  random( $HmonsterDHP[15] );
									next;
								}

								# 怪獣しとめたときの経験値
								if (   ( $land->[$bx][$by] == $HlandBase )
									|| ( $land->[$bx][$by] == $HlandSbase ) )
								{
									$landValue->[$bx][$by] +=
									  $HmonsterExp[$mKind];
									$island->{'allex'} +=
									  $HmonsterExp[$mKind]
									  ;    # 経験値総獲得件数
									$landValue->[$bx][$by] = $HmaxExpPoint
									  if ( $landValue->[$bx][$by] >
										$HmaxExpPoint );
								}

								# 怪獣餌取得フラグを立てる

								$island->{'esa'}  = $mKind;
								$tIsland->{'esa'} = $mKind;

								# 怪獣の賞関係
								monstersPrize( $mKind, $island );

						   # ゴールドゴーストが純金の碑になる。
								if ( $mKind == 31 ) {
									logMonsGold(
										$id,      $target, $name,  $tName,
										$comName, $mName,  $point, $tPoint
									);
									$tLand->[$tx][$ty]      = $HlandMonument;
									$tLandValue->[$tx][$ty] = 9;
								}
								elsif ( $kind == $HcomMissileST ) {

									# ステルス
									logMsMonKillS(
										$id,      $target, $name,  $tName,
										$comName, $mName,  $point, $tPoint
									);
								}
								else {

									# 通常
									logMsMonKill(
										$id,    $target, $name,
										$tName, $mName,  $tPoint
									);
								}

								# 収入
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

								# 怪獣生きてる
								if ( $kind == $HcomMissileST ) {

									# ステルス
									logMsMonsterS(
										$id,      $target, $name,  $tName,
										$comName, $mName,  $point, $tPoint
									);
								}
								else {

									# 通常
									logMsMonster( $id, $target, $mName,
										$tPoint );
								}

								# HPが1減る
								$tLandValue->[$tx][$ty]--;
								if (
									( $kind == $HcomBioMissile )
									&& (   ( $mKind == 6 )
										|| ( $mKind == 7 )
										|| ( $mKind == 8 ) )
								  )
								{
									if ( random(4) == 0 )
									{    # 汚染による特殊変異
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

			   # 町、農場、工場、商業ビル、港、ミサイル基地
						my ($result) = "被害を受け";
						my ( $break, $Ept ) = ( 0, 2 );
						if ( $tL == $HlandFarm ) {    # 農場
							$tLandValue->[$tx][$ty] -= 5;
							$tLandValue->[$tx][$ty] -= 5
							  if ( $kind == $HcomMissileGM );
							if ( $tLandValue->[$tx][$ty] < 10 ) {
								$result = "壊滅し";
								$break  = 1;
								$Ept    = 4;
							}
						}
						elsif ( $tL == $HlandBase ) {
							$tLandValue->[$tx][$ty] -= 50;
							$tLandValue->[$tx][$ty] -= 50
							  if ( $kind == $HcomMissileGM );
							if ( $tLandValue->[$tx][$ty] < 0 ) {
								$result = "壊滅し";
								$break  = 1;
								$Ept    = 4;
							}
						}
						elsif ( $tL == $HlandPort ) {
							$tLandValue->[$tx][$ty] -= 40;
							$tLandValue->[$tx][$ty] -= 40
							  if ( $kind == $HcomMissileGM );
							if ( $tLandValue->[$tx][$ty] < 40 ) {
								$result = "壊滅し";
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
								$result = "壊滅し";
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
								$result = "壊滅し";
								$break  = 1;
								$Ept    = 4;
							}
						}
						if ( $kind == $HcomMissileST ) {    # ステルス
							logMsNormalS(
								$id,    $target,  $name,
								$tName, $comName, $tLname,
								$point, $tPoint,  $result
							);
						}
						elsif (( $kind == $HcomBioMissile )
							&& ( $break == 1 ) )
						{                                   # バイオ
							logBioMs( $id, $target, $tLname, $tPoint );
						}
						else {                              # 通常
							logMsNormal( $id, $target, $tLname, $tPoint,
								$result );
						}

						# 経験値
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandSbase ) )
						{
							$landValue->[$bx][$by] += $Ept;
							$island->{'allex'}     +=
							  $Ept;    # 経験値総獲得件数
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

						# 巨大地形のとき
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
								  ; # 通常ミサイルなので難民にプラス
							}
							elsif ( $tL == $HlandMegatower ) {
								$tL2 = $HlandTower;
							}
							$tLand->[$tx][$ty]      = $tL2;
							$tLandValue->[$tx][$ty] = 190;
							$tLname2 = landName( $tL2, 190 );
						}
						my ($result) =
						  "被害を受け${tLname2}に戻ってしまい";

						if ( $kind == $HcomMissileST ) {    # ステルス
							logMsNormalS(
								$id,    $target,  $name,
								$tName, $comName, $tLname,
								$point, $tPoint,  $result
							);
						}
						else {                              # 通常
							logMsNormal( $id, $target, $tLname, $tPoint,
								$result );
						}

						# 巨大地形のときの経験値
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandSbase ) )
						{
							$landValue->[$bx][$by] += 10;
							$island->{'allex'} += 10; # 経験値総獲得件数
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
						}
						next;
					}
					elsif ( ( $tL > 100 ) && ( $tL < 120 ) ) {

						# 船系の場合
						my ( $order, $hp, $sId ) = shipSpec($tLv);
						if ( ( $hp <= 1 ) || ( $tL == $HlandBalloonS ) ) {

							# 船沈没(海風船は一撃で割れる)
							if ( $tL == $HlandPirate ) {
								if ( random(5) == 0 ) {

									# 海賊船がいた島に幽霊船出現
									$tIsland->{'ghost'} = $target;
								}
								elsif (( $sId == 0 )
									&& ( $kind != $HcomMissileST ) )
								{

									# 海賊船 帰属させる
									logMsShip( $id, $target, $tLname, $tPoint,
										$tL, "観念しました。" );
									$tLandValue->[$tx][$ty] = 21000 + $id;
									next;
								}
							}
							elsif ( $tL == $HlandTreasureS ) {

								# 宝船
								$island->{'money'}  += 5000;
								$tIsland->{'money'} += 5000;

							   #ランキング用ログファイル書き出し
								open( MOUT, ">>${HlogdirName}/money.log" );
								print MOUT "$HislandTurn,$id,宝船,5000\n";
								print MOUT "$HislandTurn,$target,宝船,5000\n";
								close(MOUT);
							}
							elsif ( $tL == $HlandBalloonS ) {

								# 海風船
								if ( $kind == $HcomMissileST ) {
									logMsShipS(
										$id,      $target,
										$name,    $tName,
										$comName, $tLname,
										$point,   $tPoint,
										"割れました。"
									);
								}
								else {
									my $tLand2      = $tIsland->{'land2'};
									my $tLandValue2 = $tIsland->{'landValue2'};

									my $p = random(100);
									if ( $p < 20 ) {    # 資金
										my $r = random(10000);
										$tIsland->{'money'} += $r;
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}の海風船が割れ何故か中に入っていた$r$HunitMoneyが降ってきました。",
											$id, $target
										);

							   #ランキング用ログファイル書き出し
										open( MOUT,
											">>${HlogdirName}/money.log" );
										print MOUT
										  "$HislandTurn,$id,海風船,$r\n";
										close(MOUT);
									}
									elsif ( $p < 30 ) {    # 食料
										$tIsland->{'food'} += 10000;
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}の海風船が割れ何故か中に入っていた食料が降ってきました。",
											$id, $target
										);
									}
									elsif ( $p < 45 ) {    # お花
										$tLand->[$tx][$ty]      = $HlandFlower;
										$tLandValue->[$tx][$ty] =
										  random(13) + 1;
										$tLand2->[$tx][$ty]      = $HlandSea;
										$tLandValue2->[$tx][$ty] = 0;
										my $mName =
										  landName( $HlandFlower,
											$tLandValue->[$tx][$ty] );
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}の海風船が割れたと同時に中から大量の<B>$mName</B>が降ってきました！！",
											$id, $target
										);
									}
									elsif ( $p < 60 ) {    # 隕石
										$tIsland->{'Meteo'} += 10;
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}の海風船が割れました",
											$id, $target
										);
									}
									elsif ( $p < 68 ) {    # 巨大隕石
										$tIsland->{'bigmissile'}++;
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}の海風船が割れ突然出現した異空間から<b>巨大隕石</b>が現れました。",
											$id, $target
										);
									}
									elsif ( $p < 88 ) {    # 地震
										$tIsland->{'prepare2'} += 10;
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}の海風船が割れました",
											$id, $target
										);
									}
									elsif ( $p < 98 ) {    # シーゴースト
										$tLand->[$tx][$ty]      = $HlandMonster;
										$tLandValue->[$tx][$ty] = 2105;
										$tLand2->[$tx][$ty]     = $HlandSea;
										$tLandValue2->[$tx][$ty] = 0;
										my $mName = ( monsterSpec(2105) )[1];
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}の海風船が割れたと同時に異空間が突如として広がり中から<B>怪獣$mName</B>が出現しました！！",
											$id, $target
										);
									}
									else {    # ゴールドゴースト
										$tLand->[$tx][$ty]      = $HlandMonster;
										$tLandValue->[$tx][$ty] =
										  3100 + $HmonsterBHP[31] +
										  random( $HmonsterDHP[31] );
										$tLand2->[$tx][$ty]      = $HlandSea;
										$tLandValue2->[$tx][$ty] = 0;
										my $mName = ( monsterSpec(3100) )[1];
										logOut(
"--- ${HtagName_}($tx, $ty)${H_tagName}の海風船が割れたと同時に異空間が突如として広がり中から<B>怪獣$mName</B>が出現しました！！",
											$id, $target
										);
									}

							   #ランキング用ログファイル書き出し
									my $rL = $tL - $HlandPirate;
									open( ROUT, ">>${HlogdirName}/ship.log" );
									print ROUT "$HislandTurn,$id,99,$rL\n";
									close(ROUT);
								}
							}

							# 船沈めたときの経験値
							if (   ( $land->[$bx][$by] == $HlandBase )
								|| ( $land->[$bx][$by] == $HlandSbase ) )
							{
								$landValue->[$bx][$by] +=
								  $HshipEX[ $tL - $HlandPirate ];
								$island->{'allex'} +=
								  $HshipEX[ $tL - $HlandPirate ]
								  ;    # 経験値総獲得件数
								$landValue->[$bx][$by] = $HmaxExpPoint
								  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
							}

							if ( $tL == $HlandBalloonS ) {
								next
								  if ( $tLand->[$tx][$ty] != $HlandBalloonS );
							}
							elsif ( $kind == $HcomMissileST ) {

								# ステルス
								logMsShipS(
									$id,      $target,
									$name,    $tName,
									$comName, $tLname,
									$point,   $tPoint,
									"沈没しました。"
								);
							}
							else {

								# 通常
								logMsShip( $id, $target, $tLname, $tPoint, $tL,
									"沈没しました。" );
							}

						}
						else {

							# 船ダメージ
							if ( $kind == $HcomMissileST ) {

								# ステルス
								logMsShipS(
									$id,
									$target,
									$name,
									$tName,
									$comName,
									$tLname,
									$point,
									$tPoint,
									"ダメージを受けました。"
								);
							}
							else {

								# 通常
								logMsShipD( $id, $target, $tLname, $tPoint, $tL,
									"ダメージを受けました。" );
							}

							# HPが1減る
							$tLandValue->[$tx][$ty] -= 1000;
							next;
						}
					}
					elsif ( $tL == $HlandKInora ) {

						# 究想いのら
						my ( $limit, $hp, $ld, $d ) = bigMonsterSpec($tLv);
						if ( $kind == $HcomMissileST ) {
							$mslogCtD++;    # 空中爆破
							next;
						}
						$tLandValue->[$tx][$ty] += 100 if ( $hp < 100 );
						if ( $d == 0 ) {

							# 中心
							logOut(
"--- ${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中しましたが、効果が無いばかりか回復しているようだ。",
								$id, $target
							);
						}
						else {

							# 経験値
							if (   ( $land->[$bx][$by] == $HlandBase )
								|| ( $land->[$bx][$by] == $HlandSbase ) )
							{
								$landValue->[$bx][$by] += 2;
								$island->{'allex'}     += 2;
								$landValue->[$bx][$by] = $HmaxExpPoint
								  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
							}

							# ラストダメージ保存
							$lastDamage = $id;
							logOut(
"--- ${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中し、<B>怪獣$tLname</B>はダメージを受けました。",
								$id, $target
							);
						}
						next;
					}
					elsif ( ( $tL == $HlandTrump ) && ( $tLv == 0 ) ) {

						# トランプ
						my $tNumber = random(14) + 1;
						$tLandValue->[$tx][$ty] = $tNumber;
						my $tLname2 = landName( $tL, $tNumber );
						if ( $kind == $HcomMissileST ) {    # ステルス
							logMsNormalS( $id, $target, $name, $tName, $comName,
								$tLname, $point, $tPoint,
								"めくられ<b>${tLname2}</b>になり" );
						}
						else {                              # 通常
							logMsNormal( $id, $target, $tLname, $tPoint,
								"めくられ<b>${tLname2}</b>になり" );
						}
						if ( $tIsland->{'trump'}->[15] != 1 ) {

							# 核ミサイルが撃たれていない時
							my ($i);
							for ( $i = 1 ; $i < 14 ; $i++ ) {
								next if ( $tIsland->{'trump'}->[$i] != 1 );
								if ( $i == $tNumber ) {

									# 同じ番号
									my $str = "";
									my $r   = 0;
									if ( $i < 6 ) {
										$r   = 10000;
										$str =
"賞金を${r}${HunitMoney}ゲットし";
									}
									elsif ( $i < 10 ) {
										$r   = 5000;
										$str =
"賞金を${r}${HunitMoney}ゲットし";
										$island->{'event2'} = 1;
									}
									elsif ( $i < 13 ) {
										$r   = 4000;
										$str =
"賞金を${r}${HunitMoney}とプレゼントセットをゲットし";
										$island->{'present'}->[4]++;
										$island->{'present'}->[5]++;
										$island->{'present'}->[8]++;
									}
									if ( $r == 0 ) {
										$island->{'present'}->[7]++; # 大都市
										$str =
"何故か大都市が建設予定になり";
									}
									else {
										$island->{'money'} += $r;
										open( MOUT,
											">>${HlogdirName}/money.log" );
										print MOUT
										  "$HislandTurn,$id,トランプ,$r\n";
										close(MOUT);
									}
									logOut(
"${HtagName_}$name${AfterName}${H_tagName}は、引いたカードが揃い${str}ました。",
										$id, $target
									);
									$tLand->[$tx][$ty]      = $HlandWaste;
									$tLandValue->[$tx][$ty] = 1;
									last;
								}
							}
						}
						if ( $tLandValue->[$tx][$ty] == 14 ) {

							# 攻撃した島にグラテネス出現
							logOut(
"ジョーカーが<B>怪獣</B>を${HtagName_}${name}${AfterName}${H_tagName}に生み出そうとしている。",
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

						# 通常地形
						if ( $kind == $HcomMissileST ) {    # ステルス
							logMsNormalS(
								$id,    $target,  $name,
								$tName, $comName, $tLname,
								$point, $tPoint,  "壊滅し"
							);
						}
						elsif ( $kind == $HcomBioMissile ) {    # バイオ
							logBioMs( $id, $target, $tLname, $tPoint );
						}
						else {                                  # 通常
							logMsNormal( $id, $target, $tLname, $tPoint,
								"壊滅し" );
						}
						$tIsland->{'trump'}->[$tLv] = 0
						  if ( $tL == $HlandTrump );
					}

					# 経験値
					if (   ( ( $tL == $HlandTown ) || ( $tL == $HlandSlum ) )
						|| ( ( $tL == $HlandOil ) && ( $tLv >= 35 ) ) )
					{
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandSbase ) )
						{
							$landValue->[$bx][$by] += int( $tLv / 20 );
							$island->{'allex'}     +=
							  int( $tLv / 20 );    # 経験値総獲得件数
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );

		 # 海底以外のときは通常ミサイルなので難民にプラス
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
							  int( $tLv / 5 );    # 経験値総獲得件数
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
						}
					}

					if ( $kind != $HcomMissileST ) {

						# STミサイル以外
						if ( $tL == $HlandBank ) {

							# 銀行を破壊したとき
							$island->{'money'} += $tLv * 500;
							logMsBank( $id, $name, $tLv * 500 );
						}

						# STミサイル以外で占有
						$tIsland->{'nation'}->[$tx][$ty] = $id
						  if ( ( $tLand->[$tx][$ty] != $HlandWaste )
							&& ( $id != $target ) );
					}

					if (   ( $tL == $HlandOil )
						|| ( ( $tL > 100 ) && ( $tL < 120 ) ) )
					{

						# 油田、船系だったら海
						$tLand->[$tx][$ty]      = $HlandSea;
						$tLandValue->[$tx][$ty] = 0;
					}
					elsif (( ( $tL == $HlandSea ) && ( $tLv >= 10 ) )
						|| ( ( $tL == $HlandBreakwater ) && ( $tLv >= 1 ) ) )
					{

						# 養殖場、防波堤だったら浅瀬
						$tLand->[$tx][$ty]      = $HlandSea;
						$tLandValue->[$tx][$ty] = 1;
					}
					elsif ( $kind == $HcomBioMissile ) {

						# バイオミサイルの時は汚染
						if ( ( $tL == $HlandOsen ) && ( $tLv < 10 ) ) {
							$tLandValue->[$tx][$ty]++;
						}
						elsif ( $tL != $HlandOsen ) {
							$tLand->[$tx][$ty]      = $HlandOsen;
							$tLandValue->[$tx][$ty] = 1;
						}
					}
					else {

						# その他は荒地になる
						$tLand->[$tx][$ty]      = $HlandWaste;
						$tLandValue->[$tx][$ty] = 1;             # 着弾点
					}
				}
			}

			# カウント増やしとく
			$count++;
		}

		if ( $flag == 0 ) {

			# 基地が一つも無かった場合
			logMsMiss( $id, $name, $comName );
			return 0;
		}

		$island->{'MissileA'} += $msCt;   # 発射数を計算
		                                  # ミサイル発射数などのログ
		if ( $kind == $HcomMissileST ) {  # ステルス
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

		# 難民判定
		$boat = ($HwarFlg) ? $boat : int( $boat / 2 );

#	HdebugOut("難民デバック１=${id}=>${target} 命令=${kind} 数=${boat}");
		if (   ( $boat > 0 )
			&& ( $id != $target )
			&& ( $kind != $HcomMissileST ) )
		{
			my ($achive) = refugees( $boat, $island );

			#		HdebugOut("難民デバック２=${achive}");
			if ( $achive > 0 ) {

				# 少しでも到着した場合、ログを吐く
				logMsBoatPeople( $id, $name, $achive );
				$island->{'achive'} =
				  ($HwarFlg) ? 0 : $achive;    # 難民数保存
				   # 難民の数が一定数以上なら、平和賞の可能性あり
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
"${HtagName_}${name}${AfterName}${H_tagName}にどこからともなく難民が漂着しましたが、${HtagName_}${name}${AfterName}${H_tagName}は受け入れを拒絶したようです。",
					$id
				);
			}
		}

		if ( $kind2 == $HcomSpecialSPP ) {

			# 海獣掃討艇によるSPP
			return 0;
		}
		elsif ( ( $kind == $HcomMissileST ) || ( $kind == $HcomMissileNCM ) ) {

			# ステルス、核の場合は終了
			if ( ( $kind == $HcomMissileNCM ) && ( $ncm == 0 ) )
			{    # ミサイル基地不足で核が撃てなかった
				logOut(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${AfterName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行おうとしましたが、ミサイル基地の不足により中止されました。",
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

		# 怪獣派遣
		# ターゲット取得
		my ($tn)      = $HidToNumber{$target};
		my ($tIsland) = $Hislands[$tn];
		my ($tName)   = $tIsland->{'name'};

		if ( $tn eq '' ) {

			# ターゲットがすでにない
			logMsNoTarget( $id, $name, $comName );
			return 0;
		}
		if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
			|| ( $tIsland->{'evil'} == 0 ) )
		{

			# 相手が途上国の為中止。
			logUNMiss( $id, $target, $name, $tName, $comName );
			return 0;
		}
		my $we = 100;
		if ( $kind == $HcomSSendMonster ) {
			if ( ($HsurvFlg) && ( $HislandTurn > $Hsstartturn ) ) {

				# サバイバルの場合は制限無し
			}
			elsif (( $arg > 30 )
				|| ( ( 12 <= $arg ) && ( $arg <= 17 ) )
				|| ( $arg == 23 )
				|| ( $arg == 24 ) )
			{
				logMiss( $id, $name, $comName,
					"怪獣建造ができない怪獣の" );
				return 0;
			}
			$we = 200;
		}
		if ( ( $kind == $HcomSSendMonster ) || ( $arg == 2 ) ) {
			if ( $island->{'weapon'} < $we ) {
				logMiss( $id, $name, $comName,
					"怪獣建造に必要な兵器不足の" );
				return 0;
			}
			$island->{'weapon'} -= $we;
		}
		$island->{'evil'} += 40 if ( $id != $target );

		# メッセージ
		logMonsSend( $id, $target, $name, $tName );
		$island->{'money'} -= $cost;
		if ( $kind == $HcomSSendMonster ) {
			addCommandLate( $HcomSSendMonsterTurn, $HislandTurn, $id, $kind,
				$target, $x, $y, $arg, $x2, $y2 );    # ターン差命令
		}
		else {
			addCommandLate( $HcomSendMonsterTurn, $HislandTurn, $id, $kind,
				$target, $x, $y, $arg, $x2, $y2 );    # ターン差命令
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

		# 怪獣操作、ST怪獣操作、船操作
		my ($tn) = $HidToNumber{$target};
		return 0
		  if ( $tn eq '' )
		  ;    # ターゲットがすでにないため何も言わずに中止
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

				# 自島の場合
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

		# 船指令変更
		my ($tn) = $HidToNumber{$target};
		return 0
		  if ( $tn eq '' );    # ターゲットがすでにないため中止

		my ($tIsland)    = $Hislands[$tn];
		my ($tName)      = $tIsland->{'name'};
		my ($tLand)      = $tIsland->{'land'};
		my ($tLandValue) = $tIsland->{'landValue'};
		my ($tL)         = $tLand->[$x][$y];
		my ($tLv)        = $tLandValue->[$x][$y];

		return 0
		  if ( $HseaChk[$tL] != 2 )
		  ;                    # ターゲットが船でないため中止
		my ( $order, $hp, $sId ) = shipSpec($tLv);
		return 0
		  if ( $sId != $id );    # ターゲットが自船でないため中止
		if ( $arg < 0 ) {
			$arg = 0;
		}
		elsif ( $arg >= 4 ) {
			$arg = 4;
		}
		return 0
		  if ( $order == $arg );    # ターゲットが同じ指令ため中止
		logShipOrderC( $id, $tName, landName( $tL, $tLv ),
			"($x, $y)", $Hshiporder[$arg] );
		$tLandValue->[$x][$y] = $arg * 10000 + $hp * 1000 + $sId;
		$island->{'money'} -= $cost;
		return 0;
	}
	elsif ( $kind == $HcomShipSell ) {

		# 船売却
		return 0
		  if ( $HseaChk[$landKind] != 2 )
		  ;                         # ターゲットが船でないため中止
		my ( $order, $hp, $sId ) = shipSpec($lv);
		return 0
		  if ( $sId != $id );    # ターゲットが自船でないため中止
		$island->{'money'} += $HshipSell[ $landKind - $HlandPirate ];
		$land->[$x][$y]       = $land2->[$x][$y];
		$landValue->[$x][$y]  = $landValue2->[$x][$y];
		$land2->[$x][$y]      = $HlandSea;
		$landValue2->[$x][$y] = 0;
		logEventP( $id, $name, "($x, $y)",
			"の船が売却されました。" );
		return 0;
	}
	elsif ( $kind == $HcomEmigration ) {

		# 移民
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

		# 輸出量決定
		$arg = 1 if ( $arg == 0 );
		my ($value) = min( $arg * ( -$cost ), $island->{'food'} );

		# 輸出ログ
		logSell( $id, $name, $comName, "$value$HunitFood" );
		$island->{'food'} -= $value;
		$island->{'money'} += int( $value / 10 );
		return 0;
	}
	elsif (( $kind == $HcomOreSell )
		|| ( $kind == $HcomOilSell )
		|| ( $kind == $HcomWeponSell ) )
	{

		# 売却量決定
		$arg = 1 if ( $arg == 0 );
		my ($value);
		if ( $id != $target ) {

			# 援助の場合
			return 0 if ( $island->{'pop'} < $Haidpop );
			my ($tn) = $HidToNumber{$target};
			return 0 if ( $tn eq '' );
			my ($tIsland) = $Hislands[$tn];
			my ($tName)   = $tIsland->{'name'};

			# 援助量決定
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

			# 援助ログ
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

		# 売却ログ
		logSell( $id, $name, $comName, $value );
		return 0;
	}
	elsif (( $kind == $HcomOreBuy )
		|| ( $kind == $HcomOilBuy )
		|| ( $kind == $HcomWeponBuy ) )
	{

		# 購入量決定
		$arg = 1 if ( $arg == 0 );
		if ( $kind == $HcomOreBuy ) {
			if ( $island->{'money'} > $arg * 2 ) {
				$island->{'ore'} += $arg;
				$island->{'money'} -= ( $arg * 2 );
			}
			else {
				logMiss( $id, $name, $comName, "資金不足の" );
				return 0;
			}
		}
		elsif ( $kind == $HcomOilBuy ) {
			if ( $island->{'money'} > $arg * 5 ) {
				$island->{'oil'} += $arg;
				$island->{'money'} -= ( $arg * 5 );
			}
			else {
				logMiss( $id, $name, $comName, "資金不足の" );
				return 0;
			}
		}
		elsif ( $kind == $HcomWeponBuy ) {
			if ( $island->{'money'} > $arg * 24 ) {
				$island->{'weapon'} += $arg;
				$island->{'money'} -= ( $arg * 24 );
			}
			else {
				logMiss( $id, $name, $comName, "資金不足の" );
				return 0;
			}
		}
		logSell( $id, $name, $comName, $arg );
		return 1;
	}
	elsif ( ( $kind == $HcomFood ) || ( $kind == $HcomMoney ) ) {

		# 援助系
		if ( $island->{'pop'} < $Haidpop ) {

#			HdebugOut("人口が規定数に満たない場合は、援助命令はできません。")
			return 0;
		}

		# ターゲット取得
		my ($tn)      = $HidToNumber{$target};
		my ($tIsland) = $Hislands[$tn];
		my ($tName)   = $tIsland->{'name'};

		# 援助量決定
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

		# 援助ログ
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

		# 地質調査
		if (   ( $landKind == $HlandPlains )
			|| ( $landKind == $HlandTown )
			|| ( ( $landKind == $HlandWaste ) && ( $lv <= 1 ) ) )
		{

			# 投資額決定
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

			if ( $q < 3 * $p ) {    # 金鉱
				$land->[$x][$y]      = $HlandSeisei;
				$landValue->[$x][$y] = 30;
				logChosa( $id, $name, $point, $comName, $str,
					"、金鉱脈が発見されま" );
			}
			elsif ( $q < 17 * $p ) {    # 銅鉱
				$land->[$x][$y]      = $HlandSeisei;
				$landValue->[$x][$y] = 10;
				logChosa( $id, $name, $point, $comName, $str,
					"、銅鉱脈が発見されま" );
			}
			elsif ( $q < 50 * $p ) {    # 炭鉱
				$land->[$x][$y]      = $HlandSeisei;
				$landValue->[$x][$y] = 5;
				logChosa( $id, $name, $point, $comName, $str,
					"、炭鉱脈が発見されま" );
			}
			elsif ( $q < 60 * $p ) {    # 温泉
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 20 + random(51);
				logChosa( $id, $name, $point, $comName, $str,
					"、温泉が発見されま" );
			}
			elsif ( $q < 86 * $p ) {    # 地下水
				$land->[$x][$y]      = $HlandSea;
				$landValue->[$x][$y] = 1;
				logChosa( $id, $name, $point, $comName, $str,
					"、大量の地下水が噴出して浅瀬になりま" );
			}
			elsif ( $q < 90 * $p ) {    # 怪獣
				$land->[$x][$y]      = $HlandMonster;
				$landValue->[$x][$y] =
				  1200 + $HmonsterBHP[12] + random( $HmonsterDHP[12] );
				logChosa( $id, $name, $point, $comName, $str,
					"、太古の怪獣が発見されま" );
			}
			else {                      # 失敗
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
				logChosa( $id, $name, $point, $comName, $str,
					"ましたが何も見つからず荒地になりま" );
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

		# 放棄
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

		# 宇宙系
		my ($prize) = $island->{'prize'};
		$prize =~ /([0-9]*),([0-9]*),(.*)/;
		if ( !( $1 & 512 ) ) {

			# 技術不足により中止
			logMiss( $id, $name, $comName, "技術不足の" );
			return 0;
		}
		elsif ( $Hsolarwind == 1 ) {
			logMiss( $id, $name, $comName,
				"宇宙風が激しく吹き荒れている" );
			return 0;
		}
		my ( $land, $landValue, $dis, $nation ) = (
			$Hspace->{'land'},       $Hspace->{'landValue'},
			$Hspace->{'landValue2'}, $Hspace->{'nation'}
		);
		my $l      = $land->[$x][$y];
		my $tLname = landName( $l, $landValue->[$x][$y] );

		if ( $kind == $HcomSFood ) {

			# 宇宙食料打上げ　数量１=１万トン
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

			# 宇宙ミサイル発射
			my ( $bx, $by, $tx, $ty, $err );

			my ( $count, $flag ) = ( 0, 0 );
			if ( $kind == $HcomSMissileMGM ) {
				$arg = 1;
			}
			else {
				$arg = 10000 if ( $arg <= 0 );
			}

			# 誤差
			if ( $kind == $HcomSMissile ) {
				$err = 19;
			}
			elsif ( $kind == $HcomSMissilePP ) {
				$err = 7;
			}
			else {
				$err = 1;
			}

			# 戦争モードではお金の変わりに兵器を消費
			my $mcost = 'money';
			if ( ($HwarFlg) && ( $cost < 500 ) ) {
				$mcost = 'weapon';
				$cost  = int( $cost / 10 );
			}
			my ( $msCt, $mslogCtM, $mslogCtW, $mslogCtD ) = ( 0, 0, 0, 0 );

			while ( ( $arg > 0 ) && ( $island->{$mcost} >= $cost ) ) {

				# 基地を見つけるまでループ
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
				  ;    # 見つからなかったらそこまで
				       # 最低一つ基地があったので、flagを立てる
				$flag = 1;

				# 基地のレベルを算出
				my ($level) =
				  expToLevel( $land->[$bx][$by], $landValue->[$bx][$by] );

				# 基地内でループ
				while ( ( $level > 0 ) && ( $island->{$mcost} > $cost ) ) {
					last if ( $arg <= 0 );
					$level--;
					$arg--;
					$msCt++;    # 発射数を計算
					if ( $kind == $HcomSMissileMGM ) {   # 怪獣誘導弾の時
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
								"適当な怪獣がいなかった" );
							return 0;
						}
						$HdefenceSpace[$id][$x][$y] = 1;
					}
					elsif ( random(2) == 0 ) {

						# 50%で外す
						$mslogCtW++;
						next;
					}
					$island->{$mcost} -= $cost;

					# 着弾点算出
					my ($r) = random($err);
					$tx = $x + $ax[$r];
					$ty = $y + $ay[$r];
					$tx-- if ( !( $ty % 2 ) && ( $y % 2 ) );

					# 着弾点範囲内外チェック
					if (   ( $tx < 0 )
						|| ( $tx >= $HislandSize )
						|| ( $ty < 0 )
						|| ( $ty >= $HislandSize ) )
					{
						$mslogCtM++;
						next;
					}

					# 着弾点の地形等算出
					my ( $tL, $tLv, $tId ) = (
						$land->[$tx][$ty],
						$landValue->[$tx][$ty],
						$nation->[$tx][$ty]
					);
					my ( $tLname, $tPoint ) =
					  ( landName( $tL, $tLv ), "($tx, $ty)" );

					# 所有島名を付加
					if ( $tId > 0 ) {
						my ($tn)      = $HidToNumber{$tId};
						my ($tIsland) = $Hislands[$tn];
						my ($tName)   = $tIsland->{'name'};
						$tLname .= "(${tName}${AfterName})" if ( $tName ne '' );
					}

					# 防衛施設判定
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

								# 迎撃
								$mslogCtD++;
								next;
							}
							else {
								HdebugOut("SA　$id　$tx　$ty");
								$HdefenceSpace[$id][$tx][$ty] = 1;
							}
						}
					}

					if ( $tL == $HlandSunit ) {
						if ( $tLv < 10 ) {

							# 破壊
							logMsSpace( $id, $tPoint, $tLname,
								"宇宙の塵になり", 999 );
							$land->[$tx][$ty]      = $HlandSea;
							$landValue->[$tx][$ty] = 0;
							$dis->[$tx][$ty]       = 0;
						}
						else {
							logMsSpace( $id, $tPoint, $tLname, "破壊され",
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
							logMsSpace( $id, $tPoint, $tLname, "破壊され",
								999 );
							$land->[$tx][$ty]      = $HlandSunit;
							$landValue->[$tx][$ty] = 10;
							$dis->[$tx][$ty]       = 0;
							$nation->[$tx][$ty]    = 0;
						}
						else {
							logMsSpace( $id, $tPoint, $tLname,
								"被害を受け", 999 );
							$dis->[$tx][$ty] += 8;
							if ( random(5) == 0 ) {
								$nation->[$tx][$ty] = 0;
							}
							$landValue->[$tx][$ty] += $e * 1000
							  if ( $tL == $HlandSAEisei );
						}

						# 経験値
						if ( $land->[$bx][$by] == $HlandSpaceBase ) {
							$dis->[$bx][$by] -= 6;
							$landValue->[$bx][$by] += 2;
							$island->{'allex'}     += 2;
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
						}
					}
					elsif ( $tL == $HlandMonster ) {

						# 怪獣
						my ( $mKind, $mName, $mHp ) = monsterSpec($tLv);
						my ($special) = $HmonsterSpecial[$mKind];
						if ( $mHp <= 1 ) {

							logMsMonKillSpace( $id, $name, $tPoint, $mName,
								999 );

							# 怪獣しとめたときの経験値
							if ( $land->[$bx][$by] == $HlandSpaceBase ) {
								$dis->[$bx][$by] -= 6;
								$landValue->[$bx][$by] += $HmonsterExp[$mKind];
								$island->{'allex'}     +=
								  $HmonsterExp[$mKind]
								  ;    # 経験値総獲得件数
								$landValue->[$bx][$by] = $HmaxExpPoint
								  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
							}

							$island->{'displus'} = 200;

							# 怪獣餌取得フラグを立てる
							$island->{'esa'} = $mKind;

							# 怪獣を消す
							$land->[$tx][$ty]      = $HlandSea;
							$landValue->[$tx][$ty] = 0;
							$nation->[$tx][$ty]    = 0;

							# 怪獣の賞関係
							monstersPrize( $mKind, $island );

							# 収入
							my ($value) = $HmonsterValue[$mKind];
							if ( $value > 0 ) {
								$island->{'money'} += $value;
								logMsMonMoney( $id, $mName, $value );
							}
						}
						else {

							# 怪獣生きてる
							logMsMonSpace( $id, $tPoint, $mName, 999 );

							# HPが1減る
							$landValue->[$tx][$ty]--;
							next;
						}
					}
					elsif ( $tL == $HlandEarth ) {

						# 地球
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

			# 宇宙占領
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

				# 占領不可
				logMissS( $id, $name, $comName, $point,
					"占領できない地形の" );
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
					  ;    # 行による位置調整
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
								"占領条件を満たさない" );
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
				logMissS2( $id, $name, $comName, $point, "抵抗勢力の" );
			}
		}
		else {
			if ( ( $nation->[$x][$y] != 0 ) && ( $nation->[$x][$y] != $id ) ) {
				logMissS( $id, $name, $comName, $point, "所有以外の" );
				return 0;
			}
			if ( $kind == $HcomSUnit ) {

				# 宇宙ユニット建設
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
						"建設できない地形の" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSPioneer ) {

				# 宇宙入植
				if ( ( $l == $HlandSunit ) && ( $landValue->[$x][$y] == 10 ) ) {
					$land->[$x][$y]      = $HlandSCity;
					$landValue->[$x][$y] = 1;
				}
				elsif ( $l == $HlandSCity ) {
					$landValue->[$x][$y] += 30;
				}
				else {
					logMissS( $id, $name, $comName, $point,
						"建設できない地形の" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSDestroy ) {

				# 宇宙ユニット破壊
				# 変更開始  <5.54e>
				#				if($l != $HlandEarth){
				if ( ( $l != $HlandEarth ) && ( $l != $HlandMonster ) ) {

					# 変更終了  <5.54e>
					$land->[$x][$y]      = $HlandSea;
					$landValue->[$x][$y] = 0;
				}
				else {
					logMissS( $id, $name, $comName, $point,
						"建設できない地形の" );
					return 0;
				}
				$island->{'money'} -= $cost;
				logLandSucS( $id, $name, $comName, $point );
				if ( $nation->[$x][$y] == $id ) {

					# 自島の場合はターン消費なし
					$nation->[$x][$y] = 0;
					return 0;
				}
				else {
					return 1;
				}
			}
			elsif ( $kind == $HcomSpaceFarm ) {

				# 宇宙農場建設
				if ( $l == $HlandSFarm ) {
					$landValue->[$x][$y] += 5;    # 規模 + 5000
					$landValue->[$x][$y] = 50
					  if ( $landValue->[$x][$y] > 50 );    # 最大 50000
				}
				elsif (
					( ( $l == $HlandSunit ) && ( $landValue->[$x][$y] == 10 ) )
					|| ( $l == $HlandSCity ) )
				{
					$land->[$x][$y]      = $HlandSFarm;
					$landValue->[$x][$y] = 10;             # 規模 10000
				}
				else {
					logMissS( $id, $name, $comName, $point,
						"建設できない地形の" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSFactory ) {

				# 宇宙工場建設
				if ( $l == $HlandSFactory ) {
					$landValue->[$x][$y] += 10;            # 規模 + 10000
					$landValue->[$x][$y] = 100
					  if ( $landValue->[$x][$y] > 100 );    # 最大 100000
				}
				elsif (
					( ( $l == $HlandSunit ) && ( $landValue->[$x][$y] == 10 ) )
					|| ( $l == $HlandSCity ) )
				{
					$land->[$x][$y]      = $HlandSFactory;
					$landValue->[$x][$y] = 30;               # 規模 30000
				}
				else {
					logMissS( $id, $name, $comName, $point,
						"建設できない地形の" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSEisei ) {

				# 宇宙衛星建設
				$arg = 0 if ( $arg < 0 );
				$arg = 5 if ( $arg > 5 );
				if ( $island->{'sfactory'} > 0 ) {
					if ( $l == $HlandSAEisei ) {

						# 追加建設
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

						# 新規建設
						$land->[$x][$y]      = $HlandSAEisei;
						$landValue->[$x][$y] = $arg * 1000 + 100;
					}
					else {
						logMissS( $id, $name, $comName, $point,
							"建設できない地形の" );
						return 0;
					}
					$comName .= "(" . $HsEisei[$arg] . ")";
				}
				else {
					logMissS( $id, $name, $comName, $point, "資材不足の" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSpaceBase ) {

				# 宇宙ミサイル基地建設
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

						# 宇宙ミサイル基地
						$land->[$x][$y]      = $HlandSpaceBase;
						$landValue->[$x][$y] = 0;
					}
					else {
						logMissS( $id, $name, $comName, $point,
							"建設できない地形の" );
						return 0;
					}
				}
				else {
					logMissS( $id, $name, $comName, $point, "資材不足の" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSDbase ) {

				# 宇宙防衛施設
				if ( ( ( $l == $HlandSunit ) && ( $landValue->[$x][$y] == 10 ) )
					|| ( $l == $HlandSCity ) )
				{
					$land->[$x][$y]      = $HlandSDefence;
					$landValue->[$x][$y] = 0;
				}
				else {
					logMissS( $id, $name, $comName, $point,
						"建設できない地形の" );
					return 0;
				}
			}
			elsif ( $kind == $HcomSBuild ) {

				# 宇宙建設系
				#	if($arg <= 0){
				#	}else{
				#	}
				return 0;
			}
			$dis->[$x][$y] -= 30;
			logLandSucS( $id, $name, $comName, $point );
			$nation->[$x][$y] = $id;

			#			HdebugOut("所有変更:($x,$y) = ${id}");
		}
		$island->{'money'} -= $cost;

		# 回数付きなら、コマンドを戻す
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

		# 海域ミサイル発射

		my ( $bx, $by, $tx, $ty, $err );

		my ( $count, $flag ) = ( 0, 0 );

		#	if($kind == $HcomOMissileMGM){
		#		$arg = 1;
		#	}else{
		$arg = 10000 if ( $arg <= 0 );

		#	}

		# 誤差
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

		# 戦争モードではお金の変わりに兵器を消費
		my $mcost = 'money';
		if ( ($HwarFlg) && ( $cost < 500 ) ) {
			$mcost = 'weapon';
			$cost  = int( $cost / 10 );
		}
		my ( $msCt, $mslogCtM, $mslogCtW, $mslogCtD ) = ( 0, 0, 0, 0 );
		while ( ( $arg > 0 ) && ( $island->{$mcost} >= $cost ) ) {

			# 基地を見つけるまでループ
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
			  ;    # 見つからなかったらそこまで

			# 最低一つ基地があったので、flagを立てる
			$flag = 1;

			# 基地のレベルを算出
			my ($level) =
			  expToLevel( $land->[$bx][$by], $landValue->[$bx][$by] );

			# 基地内でループ
			while ( ( $level > 0 ) && ( $island->{$mcost} > $cost ) ) {
				last if ( $arg <= 0 );
				$level--;
				$arg--;
				$msCt++;    # 発射数を計算
				$island->{$mcost} -= $cost;

				# 着弾点算出
				my ($r) = random($err);
				$r  = 0 if ( ( $kind == $HcomOMissileSPP ) && ( $r == 7 ) );
				$tx = $x + $ax[$r];
				$ty = $y + $ay[$r];
				$tx-- if ( !( $ty % 2 ) && ( $y % 2 ) );

				# 着弾点範囲内外チェック
				if (   ( $tx < 0 )
					|| ( $tx >= $HoceanSize )
					|| ( $ty < 0 )
					|| ( $ty >= $HoceanSize ) )
				{
					$mslogCtM++;
					next;
				}

				# 着弾点の地形等算出
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

				# 所有島名を付加
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

						# 相手が途上国
						$mslogCtD++;    # 空中爆破
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
						$mslogCtD++;    # 空中爆破
					}
				}
				elsif ( $tL == $HlandOcean ) {
					$mslogCtD++;        # 空中爆破
				}
				elsif ( $tL == $HlandMonster ) {

					# 怪獣
					my ( $mKind, $mName, $mHp ) = monsterSpec($tLv);
					my ($special) = $HmonsterSpecial[$mKind];

					if ( $mHp <= 1 ) {
						logMsMonKillSpace( $id, $name, $tPoint, $mName, 888 );

						# 怪獣しとめたときの経験値
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandSbase ) )
						{
							$landValue->[$bx][$by] += $HmonsterExp[$mKind];
							$island->{'allex'}     +=
							  $HmonsterExp[$mKind];   # 経験値総獲得件数
							$landValue->[$bx][$by] = $HmaxExpPoint
							  if ( $landValue->[$bx][$by] > $HmaxExpPoint );
						}
						$island->{'displus'} = 200;

						# 怪獣餌取得フラグを立てる
						$island->{'esa'} = $mKind;

						# 怪獣を消す
						$tLand->[$tx][$ty]      = $HlandSea;
						$tLandValue->[$tx][$ty] = 0;
						$tNation->[$tx][$ty]    = 0;

						# 怪獣の賞関係
						monstersPrize( $mKind, $island );

						# 収入
						my ($value) = $HmonsterValue[$mKind];
						if ( $value > 0 ) {
							$value *= 2;
							$island->{'money'} += $value;
							logMsMonMoney( $id, $mName, $value );
						}
					}
					else {

						# 怪獣生きてる
						logMsMonSpace( $id, $tPoint, $mName, 888 );

						# HPが1減る
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

		# 怪獣バトル
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

			# 自分の怪獣がいない
		}
		elsif ( $id != $MBid ) {

			# 遠征中
			if ( $mtn eq '' ) {
				$MBid = $id
				  ; # 相手がいなくなったので怪獣を自分の島に戻す。
				$MBhp  = $MBmhp;
				$MBtId = 0;
			}
		}
		elsif ( $mtn eq '' ) {
			$MBid =
			  $id;   # 相手がいないので怪獣を自分の島に戻す。
			$MBhp  = $MBmhp;
			$MBtId = 0;
		}

		if ( $kind == $HcomMonsTettai ) {

			# 怪獣撤退
			# ターゲットを自動指定する
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

			# 怪獣餌譲渡
			if ( ( $MBsId == 0 ) || ( $tMBsId != 0 ) ) {

				# 餌が無いまたは、相手に餌があるので中止
				logMonsCancel( $id, $name, $comName,
					"餌が無いまたは、ターゲットに餌がある" );
				return 0;
			}
			$tMBsId = $MBsId;
			logMonsEsaAid( $id, $name, $target, $tName, $HmonsterName[$MBsId] );
			$MBsId = 0;
		}
		else {
			if ( $MBid == 0 ) {

				# 怪獣がいない
				if ( $kind == $HcomMonsEgg ) {

					# 怪獣エッグ購入
					logMonsEGG( $id, $name, $comName );
					$MBid   = $id;
					$MBname = "いのら(名前未設定)";
					$MBtId  = 0;
					$MBsId  = $MBsId;
					$MBmId  = 1;                              # いのら
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
					logMonsCancel( $id, $name, $comName, "怪獣がいない" );
					return 0;
				}
			}
			else {

				# 怪獣がいる

				if ( $kind != $HcomMonsTettai ) {

					# 怪獣撤退以外
					if ( ( $id != $MBid ) || ( $MBtId != 0 ) ) {

						# 自分の怪獣が自分の島にいない
						logMonsCancel( $id, $name, $comName, "戦闘中の" );
						return 0;
					}
				}

				if ( $kind == $HcomMonsEsa ) {

					# 怪獣に餌を食べさせる
					if ( $MBsId == 0 ) {

						# 餌が無いので中止
						logMonsCancel( $id, $name, $comName, "餌が無い" );
						return 0;
					}
					elsif ( $MBsId == 1 ) {

						# 餌がいのら
						$MBmId = 1;    # いのら
						logMonsEvo( $id, $name, $MBname, $HmonsterName[$MBmId],
							$comName );
					}
					else {

						my ($MonGRP)    = $HmonsterGRP[$MBmId];
						my ($MonCLS)    = $HmonsterCLS[$MBmId];
						my ($EsaMonGRP) = $HmonsterGRP[$MBsId];
						my ($EsaMonCLS) = $HmonsterCLS[$MBsId];

						if ( $MonGRP == $EsaMonGRP ) {

							# 餌と同じグループの場合
							if ( $MonCLS > $EsaMonCLS ) {

						   # 餌より階級が低いので餌の怪獣に進化
								$MBmId = $MBsId;
								logMonsEvo( $id, $name, $MBname,
									$HmonsterName[$MBmId], $comName );
							}
							else {

								# 階級が１上がる
								my ($MonSea) = MonSeaCls( $MBmId, 1 );
								if ( $MonSea == 0 ) {

									# 失敗
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

								# 餌のほうの階級が１以上高い場合
								my ($MonSea) = MonSeaCls( $MBsId, 3 );
								if ( $MonSea == 0 ) {

									# 失敗
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

									# 失敗
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

					# 怪獣遠征
					if ( $tMBid != $target ) {

			# 相手に怪獣がいない、遠征中のとき無条件で中止
						logMonsCancel( $id, $name, $comName,
"ターゲットに怪獣がいないか遠征中の"
						);
						return 0;
					}
					if ( $tMBtId != 0 ) {

						# 相手が戦闘中のとき無条件で中止
						logMonsCancel( $id, $name, $comName,
							"ターゲットが戦闘中の" );
						return 0;
					}
					if ( $tMBid == $id ) {

						# 自分の島
						logMonsCancel( $id, $name, $comName,
							"自分の島だった" );
						return 0;
					}
					logMonsENSEI( $id, $name, $target, $tName, $comName );
					$MBid   = $target;
					$MBtId  = $target;
					$tMBtId = $id;
					$island->{'money'} -= $cost;
				}
				elsif ( $kind == $HcomMonsTettai ) {

					# 怪獣撤退
					if ( $MBid == $id ) {

						# 自分の島
						if ( $MBtId == 0 ) {

							# 相手がいないときとき無条件で中止
							logMonsCancel( $id, $name, $comName,
								"戦闘中でない" );
							return 0;
						}
						$tMBid = $tMBtId;
					}
					else {

						# 遠征中
						$MBid  = $MBtId;
						$tMBid = $tMBtId;
					}
					logMonsEND( $id, $name, $MBname, $tMBid,
						"戦いから逃げました。" );
					logMonsEND( $tMBid, $tName, $tMBname, $id,
						"戦いに勝利しました。" );
					$MBtId  = 0;
					$tMBtId = 0;
					$MBhp   = $MBmhp;
					$tMBhp  = $tMBmhp;
					$tMBwinh++;    # 怪獣杯用
					$tMBwin++;
					$MBlose++;
				}
				elsif ( $kind == $HcomMonsAid ) {

					# 怪獣譲渡
					if ( ( $tMBid != 0 ) || ( $tMBtId != 0 ) ) {

						# 相手に既に怪獣がいるとき無条件で中止
						logMonsCancel( $id, $name, $comName,
							"ターゲットに既に怪獣がいる" );
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

					# 怪獣売却
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

					# 怪獣模擬訓練
					if ( $MBsId == 0 ) {

						# 餌が無いので中止
						logMonsCancel( $id, $name, $comName, "餌が無い" );
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

# 怪獣バトル用
# 一つ階級が上の怪獣を求める
sub MonSeaCls {
	my ( $monid, $pattern ) = @_;
	my ( $MonsGRP, $MonsCLS );
	$MonsGRP = $HmonsterGRP[$monid];
	if ( $pattern == 1 ) {

		# $monidと同じグループの階級が１高い怪獣を探す
		$MonsCLS = $HmonsterCLS[$monid] + 1;
	}
	elsif ( $pattern == 2 ) {

		# $monidと同じグループの階級が１低い怪獣を探す
		$MonsCLS = $HmonsterCLS[$monid] - 1;
		if ( $MonsCLS < 1 ) {
			$MonsCLS = 1;
		}
	}
	else {

		# $monidと同じグループの階級が１の怪獣を探す
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

# 怪獣の賞関係の計算
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

#CL ターン差命令
sub doCommandLate {
	my ( $i, $id, $kind, $target, $x, $y, $arg, $x2, $y2 );
	for ( $i = $#HcomL ; $i >= 0 ; $i-- ) {
		if ( $HcomL[$i]->{turn} == $HislandTurn ) {

			# 実行する・・。
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
"が、送り込んだ怪獣が${HtagName_}${tName}${AfterName}${H_tagName}に到着した模様！！"
				);
			}
			elsif ( $kind == $HcomSSendMonster ) {
				$arg = $HmonsterNumber - 1 if ( $arg >= $HmonsterNumber );
				$tIsland->{'monsEnsei'} = $arg;
				logEvent( $id, $name,
"が、送り込んだ怪獣が${HtagName_}${tName}${AfterName}${H_tagName}に到着した模様！！"
				);
			}
			elsif ( $kind == $HcomSpy ) {
				if ( $arg == 0 ) {

					# 工作員派遣：地震
					$HpunishInfo{$target}->{punish} = 1;
					$HpunishInfo{$target}->{x}      = $x;
					$HpunishInfo{$target}->{y}      = $y;
				}
				else {
					logEventP( $target, $tName, "($x, $y)",
"で大量のアルミ箔が舞っている模様！！２ヘクスでミサイル防衛不可。"
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
							|| ( $sy >= $HislandSize ) );    # 範囲外判定

						$HdefenceHex[$target][$sx][$sy] = -1;
					}
				}
			}
			elsif ( $kind == $Hcomcolony ) {

				# コロニー落し
				if ( $arg == 2 ) {
					logEvent( $id, $name,
"が、<B>スーパーシールドシステム２</B>を発動！！"
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
"が、降下させた<B>スペースコロニー</B>が遂に${HtagName_}${tName}${AfterName}${H_tagName}へ墜落しました。"
					);
				}
			}
		}
	}
}

# 成長および単ヘックス災害
sub doEachHex {
	my ($island) = @_;
	my ( $name, $id, $land, $landValue, $land2, $landValue2 ) = (
		$island->{'name'},      $island->{'id'},    $island->{'land'},
		$island->{'landValue'}, $island->{'land2'}, $island->{'landValue2'}
	);

	# 天気変更
	$island->{'weather2'} = $island->{'weather'};
	my ( $wkind, $wname, $whp, $wkind2, $wkind3 ) =
	  weatherinfo( $island->{'weather'} );

	# 森が潤う時
	if (   ( random(4) == 0 )
		&& ( ( $wkind == 3 ) || ( $wkind == 4 ) )
		&& ( $whp < 8 )
		&& ( $id <= 90 ) )
	{
		$island->{'Rain'} = 1;
		logEvent( $id, $name,
			"で<B>雨のおかげで</B>、木々が潤いました。" );
	}

	# 天気過去データ調整
	my ($pastweather) = $island->{'pastweather'};
	my (@pastw);
	my ( $w, $pw );
	push( @pastw, $wkind );
	for ( $w = 0 ; $w < 10 ; $w++ ) {
		$pw = $pastweather->[$w];
		push( @pastw, $pw );
	}
	$island->{'pastweather'} = \@pastw;

#	logWeather("${HtagName_}${name}${AfterName}${H_tagName}の天気は<B>$wname</B>です。");
	$wkind  = ( random(10) < 9 )  ? $wkind2 : random(6);
	$wkind2 = ( random(10) < 7 )  ? $wkind3 : random(6);
	$wkind3 = ( random(12) == 0 ) ? 1       : random(6);

	if ( $id > 90 ) {

		# Battle Fieldのとき
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

					# 人造
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

				# 究想いのら
				$kinoraFlg = 0;
				$land->[$x][$y] = $HlandKInora;
				$landValue->[$x][$y] = 50000 + ( random(60) * 100 ) + 4000;
				logMonsCome( $id, $name, landName( $HlandKInora, 0 ),
					"($x, $y)", landName( $landKind, $lv ) );
				kinoraMake( $land, $landValue, $x, $y );
			}
			elsif ( $landKind == $HlandKInora ) {

				# 究想いのら
				kinoraMove( $island, $x, $y );
			}
		}
		return;
	}

	# 導出値
	my ( @monsterMove, @shipMove );

	# 失業者と難民の数でスラム街の発生確率を決める。
	my ($unemployment) = $island->{'pop'} - (
		(
			$island->{'farm'} + $island->{'factory'} + $island->{'port'} +
			  $island->{'mountain'} + $island->{'tower'}
		) * 13
	) + $island->{'achive'} * 30;
	$unemployment = 0 if ( $unemployment < 0 );
	my ($p)       = ( $island->{'food'} < 0 ) ? 20000 : 100000;
	my ($oilFlag) = $island->{'oilfield'};

	# 森の割合による保水力の調整
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
	$whp += $island->{'tenki'};    #てるてるいのらによる増減

	if ( $wkind == 5 ) {           # 大雨
		$whp++ if ( $whp < 4 );
		$whp += $wp;
	}
	elsif ( $wkind == 4 ) {        # 雨
		$whp++ if ( $whp < 4 );
		$whp += int( $wp / 2 );
	}
	elsif ( $wkind == 0 ) {        # 快晴
		$whp-- if ( $whp > 5 );
		$whp -= $wp;
	}
	elsif ( $wkind == 1 ) {        # 晴れ
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

	# 森が２０％以上だと特別に湿度を増減する
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
		logEvent2( $id, $name, '洪水が発生！！',
			'島の人口が減りました' );
		$island->{'TeruteruMons'} = 1
		  if ( ( $island->{'pop'} >= $HdisMonsBorder1 )
			&& ( random(12) == 0 ) );    # てるてるいのら
	}
	elsif ( $whp < 0 ) {
		$island->{'Hideri'} = 1;
		$whp = 1;
		logEvent2( $id, $name, '日照りが発生！！',
			'いろんな被害が出ました' );
		$island->{'TeruteruMons'} = 2
		  if ( ( $island->{'pop'} >= $HdisMonsBorder1 )
			&& ( random(12) == 0 ) );    # 逆さてるてる
	}
	$island->{'weather'} = $wkind3 * 1000 + $wkind2 * 100 + $wkind * 10 + $whp;

	my ($Pol) = $HdisPollution * $island->{'pop'} * 0.001;
	$Pol = $HmaxdisPollution if ( $Pol > $HmaxdisPollution );

	if (   ( random(1000) < $Pol )
		&& ( $island->{'pop'} >= 3000 )
		&& ( $island->{'propaganda'} != 1 ) )
	{

	  # 公害発生 人口30万未満、誘致活動中の時は発生しない
		$island->{'Pollution'} = 1;
		logEvent2( $id, $name, '公害', 'が発生しています' );
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

		# 犯罪多発
		$island->{'Crime'} = 1;
		logEvent2( $id, $name, '犯罪が多発', 'しています' );
	}
	if ( random(100) < 5 + $island->{'event'} ) {
		$island->{'event'} = 1;
		my ($eve) = random(100);
		if ( $eve < 10 ) {
			$island->{'wingdragon'} = 1;
			$eve = "に翼竜が出現！！観光客が集まり";
		}
		elsif ( $eve < 30 ) {
			$island->{'icefloe'} = 1;
			$eve = "に流氷が出現！！観光客が集まり";
		}
		elsif ( $eve < 50 ) {
			$island->{'couplerock'} = 1;
			$eve = "に夫婦岩が出現！！観光客が集まり";
		}
		elsif ( $eve < 52 ) {
			$eve = "に大陸から移民漂着！！人口が増え";
		}
		elsif ( $eve < 63 ) {
			$island->{'present'}->[0]++;
			$eve =
			  "で、何故か公園が誘致され、観光客が集まり";
		}
		elsif ( $eve < 69 ) {
			$island->{'present'}->[1]++;
			$eve =
"で、大陸のゼネコンからスタジアム建設資金を寄付され、観光客が集まり";
		}
		elsif ( $eve < 72 ) {
			$island->{'present'}->[2]++;
			$eve =
"で、ドーム建設予算案が議会で可決され、観光客が集まり";
		}
		elsif ( $eve < 76 ) {
			$island->{'present'}->[3]++;
			$eve =
"で、大陸の資産家がカジノ建設を決定、観光客が集まり";
		}
		elsif ( $eve < 80 ) {
			$island->{'present'}->[4]++;
			$eve =
"で、島の財閥が遊園地建設を決定、観光客が集まり";
		}
		elsif ( $eve < 89 ) {
			$island->{'present'}->[5]++;
			$eve =
"で、住民が学校の建設を切望し建設が決定、大陸からたくさんの移民者がやってき";
		}
		elsif ( $eve < 94 ) {
			$island->{'present'}->[6]++;
			$eve =
"で、空港建設の予算が組まれ建設することが決定、大陸からたくさんの移民者がやってき";
		}
		elsif ( $eve < 96 ) {
			$island->{'present'}->[7]++;
			$eve =
"で、大都市を建設するという噂が広がり大陸からたくさんの移民者がやってき";
		}
		else {
			$island->{'present'}->[8]++;
			$eve =
"で、動物好きの実業家が動物園を開園を決定、観光客が集まり";
		}
		logOut( "${HtagName_}${name}${AfterName}${H_tagName}${eve}ました。",
			$id );
	}
	else {
		$island->{'event'} = 0;
	}

	# 増える人口のタネ値 村町、都市、大都市
	my ( $pop1, $pop2, $pop3 ) = ( 10, 0, 0 );
	if ( $island->{'food'} < 0 ) {
		$pop1 = -30;    # 食糧不足
		$pop2 = -10;
		$pop3 = -10;
	}
	elsif ( $island->{'propaganda'} == 1 ) {
		$pop1 = 30;     # 誘致活動中
		$pop2 = 4;
		$pop3 = 4;
	}
	if ( $island->{'Kouzui'} == 1 ) {    # 洪水
		$pop1 -= random(30) + 5;
		$pop2 -= random(15) + 4;
		$pop3 -= random(10) + 4;
	}
	if ( $island->{'Hideri'} == 1 ) {    # 日照り
		$pop1 -= random(20) + 5;
		$pop2 -= 5;
		$pop3 -= 5;
	}
	if ( $island->{'Crime'} == 1 ) {     # 犯罪多発時
		$pop1 -= random(10) + 5;
		$pop2 -= 4;
		$pop3 -= 5;
	}
	if ( $island->{'towerD'} > 0 ) {     # 商業過剰時
		$pop1 -= 3;
		$pop2--;
		$pop3 -= 2;

	}
	if ( $island->{'event'} == 1 ) {     # 人口増イベント
		$pop1 += 30;
		$pop2 += 5;
		$pop3 += 5;
	}
	if ( $island->{'event2'} == 1 ) {    # 人口増イベント2
		$pop1 += 50;
		$pop2 += 15;
		$pop3 += 10;
	}
	if ( $island->{'treasure'} > 0 ) {    # 宝船
		$pop1 += 5;
		$pop2 += 2;
		$pop3++;
		$island->{'displus'} = 70;
	}
	if ( $island->{'gold'} > 0 ) {        # 黄金期
		$pop1 += 20;
		$pop2 += 6;
		$pop3 += 4;
		$island->{'displus'} = 150;
	}

	# ループ
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

			# 町系,海底都市,スラム街,合体地形
			if (   ( ( $landKind == $HlandTown ) && ( $lv < 130 ) )
				&& ( random($p) < $unemployment + $island->{'towerD'} ) )
			{

				# スラム街に変化する確率がある
				logslum( $id, $name, landName( $landKind, $lv ), "($x, $y)" );
				$land->[$x][$y] = $HlandSlum;
				next;
			}
			elsif (( $landKind == $HlandSlum )
				&& ( $unemployment == 0 )
				&& ( random(3) == 0 ) )
			{

# 難民も加味して職が余っている時は33.3%の確率でスラム街が町になる。
				$land->[$x][$y] = $HlandTown;
				next;
			}
			elsif (( $island->{'Pollution'} == 1 )
				&& ( $landKind == $HlandTown )
				&& ( $island->{'Hospital'} != 1 ) )
			{

				# 病院が無い場合、公害発生中 31%で連鎖
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

			# 周囲の地形で人口の増え方を調節する
			my ( $addpop, $addpop2, $addpop3 ) = ( $pop1, $pop2, $pop3 );
			my $count = 0;
			my ( $j, $sx, $sy );
			for ( $j = 0 ; $j < 7 ; $j++ ) {
				$sx = $x + $ax[$j];
				$sy = $y + $ay[$j];
				$sx--
				  if ( !( $sy % 2 ) && ( $y % 2 ) );  # 行による位置調整
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

					# 記念碑、海底記念碑、森、温泉
					$addpop += 2;
					$addpop2++;
				}
				elsif ( $land->[$sx][$sy] == $HlandSchool ) {

					# 学校
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

				# 周囲に学校が無くスラム街がある時
				$addpop  -= 3;
				$addpop2 -= 3;
				$addpop3 -= 3;
			}

			if ( $landKind == $HlandOil ) {
				if ( $lv >= 35 ) {

					# 海底都市
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

					#  海底農場
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

				# 巨大地形の場合
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

					# 元に戻る
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
"の${lName}が${lName2}に戻ってしまいました。"
					);
				}
			}
			else {
				if ( $addpop < 0 ) {

					# 不足
					$lv -= ( random( -$addpop ) + 1 );
					if ( ( $landKind == $HlandOil ) && ( $lv < 35 ) ) {
						$land->[$x][$y]      = $HlandSea;
						$landValue->[$x][$y] = 0;
						next;
					}
					elsif (( ( $landKind == $HlandTown ) && ( $lv <= 0 ) )
						|| ( ( $landKind == $HlandSlum ) && ( $lv <= 0 ) ) )
					{

						# 平地に戻す
						$land->[$x][$y]      = $HlandPlains;
						$landValue->[$x][$y] = 0;
						next;
					}
				}
				else {

					# 成長
					if ( $lv < 100 ) {
						$lv += random($addpop) + 1;
						$lv = 100 if ( $lv > 100 );
					}
					elsif ( $lv < 130 ) {

						# 都市になると成長遅い
						if ( $addpop2 > 0 ) {
							$lv += random( $addpop2 + 1 );
							$lv = 130 if ( $lv > 130 );
						}
					}
					else {

						# 大都市になると成長がさらに遅い
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

			# 養殖場
			#		$island->{'food'} += int($lv / 2);
			if ( ( $island->{'Hideri'} == 1 ) || ( $island->{'Kouzui'} == 1 ) )
			{
				$landValue->[$x][$y] -= 5;
				$landValue->[$x][$y] = 1 if ( $landValue->[$x][$y] < 10 );
			}
			elsif ( $lv < 200 ) {

				# 魚を増やす
				$landValue->[$x][$y]++;
			}
			else {
				$landValue->[$x][$y] = 200;
			}
		}
		elsif ( ( $landKind > 100 ) && ( $landKind < 120 ) ) {

			# 船系の場合

			if (   ( $landKind == $HlandPirate )
				|| ( $landKind == $HlandGhostShip ) )
			{

				# 海賊、幽霊船は国連の成敗対象。
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

					# 船保有島が存在しないは遭難する。
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

				# すでに動いた後
				next;
			}
			elsif ( $shipMove[$x][$y] == 0 ) {

				# 回復する船の場合は回復する
				if ( $HshipHP[ $landKind - $HlandPirate ] > $hp ) {
					$landValue->[$x][$y] +=
					  $HshipKAI[ $landKind - $HlandPirate ] * 1000;
					$hp += $HshipKAI[ $landKind - $HlandPirate ];
				}
			}

			# 収入
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

			# 支出 とりあえず自島にいるやつだけ
			if ( ( $sId == $id ) && ( $shipMove[$x][$y] == 0 ) ) {

#			HdebugOut("船系支出:" . $island->{'name'} . $landKind . ":資金:" . $HshipMoney[$landKind - $HlandPirate] . ":食料:" . $HshipFood[$landKind - $HlandPirate]);
				$island->{'money'} -= $HshipMoney[ $landKind - $HlandPirate ];
				$island->{'food'}  -= $HshipFood[ $landKind - $HlandPirate ];
			}

			my ( $sx, $sy );
			if ( $order == 2 ) {

				# 指令が防御の場合
				# １回復する
				$landValue->[$x][$y] += 1000
				  if ( $HshipHP[ $landKind - $HlandPirate ] > $hp );
				next;
			}
			else {

				# 移動と行動
				( $sx, $sy ) = shipAction( $island, $x, $y );
			}

			# 移動済みフラグ
			if ( $sx == 100 ) {

				# 消えた
			}
			elsif ( $HshipSP[ $landKind - $HlandPirate ] == 2 ) {

				# とても早い船
				$shipMove[$sx][$sy] = 1;
			}
			elsif ( $HshipSP[ $landKind - $HlandPirate ] == 1 ) {

				# 速い船
				$shipMove[$sx][$sy] = $shipMove[$x][$y] + 1;
			}
			else {

				# 普通の船
				$shipMove[$sx][$sy] = 2;
			}
		}
		elsif ( $landKind == $HlandForest ) {

			# 森
			if ( $lv < 200 ) {

				# 木を増やす
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

			# 記念碑
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
						|| ( $sy >= $HislandSize ) );    # 範囲外判定
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

					# 発展
					my ($lName) = landName( $landKind, $lv );
					logEventP( $id, $name, "($x, $y)",
"の${lName}を中核として周囲が超巨大都市に発展しました。"
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
							|| ( $sy >= $HislandSize ) );    # 範囲外判定
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

				# 1万分の1の確率でゴールドゴーストになる
				$land->[$x][$y]      = $HlandMonster;
				$landValue->[$x][$y] =
				  3100 + $HmonsterBHP[31] + random( $HmonsterDHP[31] );
				logMonsCome( $id, $name,
					( monsterSpec( $landValue->[$x][$y] ) )[1],
					"($x, $y)", landName( $landKind, $lv ) );
			}
			elsif ( $lv == 9 ) {    # 純金の碑
				$island->{'money'} += 300;
				$island->{'GoldMonument'}++;
			}
		}
		elsif ( $landKind == $HlandOsen ) {

			# 汚染土壌
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

				# 防衛施設自爆
				logBombFire( $id, $name, landName( $landKind, $lv ),
					"($x, $y)" );

				# 広域被害ルーチン
				wideDamage( $id, $name, $land, $landValue, $x, $y, 0 );
			}
			elsif ( ( $lv == 20 ) || ( $lv == 21 ) ) {

				# 霧付き防衛施設
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

			# 港
			if ( ( seaAround( $land, $x, $y, 7 ) == 0 ) && ( random(3) == 0 ) )
			{

				# 周囲に海系が無い場合33%で閉鎖
				logClosedPort( $id, $name, landName( $landKind, $lv ),
					"($x, $y)" );
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
			}
		}
		elsif ( $landKind == $HlandBank ) {

			# 銀行
			if ( ( $lv >= 30 ) && ( random(1000) == 0 ) ) {
				logEventP( $id, $name, "(?, ?)",
"の銀行が倒産しそうになりましたが、公的資金投入により規模は半分になりましたが倒産を免れました。"
				);
				logSecret(
"倒産しそうになったのは${HtagName_}($x, $y)${H_tagName}地点の銀行です。",
					$id
				);
				$landValue->[$x][$y] = int( $lv / 2 );
			}
			elsif ( ( $lv < 30 ) && ( random(1000) == 0 ) ) {
				logEventP( $id, $name, "($x, $y)",
					"の銀行が倒産し荒地になりました。" );
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
			}
			else {
				$island->{'money'} += $lv * ( random(3) + 1 );
			}
		}
		elsif ( ( $landKind == $HlandOil ) && ( ( $lv == 6 ) || ( $lv == 7 ) ) )
		{

			# 海底消防署、海底デストラップの維持費
			if ( $island->{'money'} < 5 ) {
				$land->[$x][$y]      = $HlandSea;
				$landValue->[$x][$y] = 0;
			}
			else {
				$island->{'money'} -= 5;
			}
		}
		elsif ( $landKind == $HlandFire ) {    # 消防署の維持費
			if ( $island->{'money'} < 3 ) {
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
			}
			else {
				$island->{'money'} -= 3;
				$landValue->[$x][$y] = 10
				  if ( random(100) < 1 );      # S消防署に発展
			}
		}
		elsif ( ( $landKind == $HlandOil ) && ( $lv == 0 ) ) {

			# 海底油田
			# 枯渇判定
			if ( random(1000) < $HoilRatio ) {

				# 枯渇
				logOilEnd( $id, $name, landName( $landKind, $lv ), "($x, $y)" );
				$land->[$x][$y]      = $HlandSea;
				$landValue->[$x][$y] = 0;
			}

			#全ての油田の枯渇判定を行ったかどうか
			$oilFlag--;
			next if ( $oilFlag > 0 );
			if ( $island->{'order'} & 2048 ) {

				# 油田は資金を生産する
				my $value = $island->{'oilfield'} * $HoilMoney * 2;
				$island->{'money'} += $value;

				# 収入ログ
				logOilMoney( $id, $name, landName( $landKind, $lv ),
					"($x, $y)", $value );
			}
			else {
				my $value = $island->{'oilfield'} * $HoilMoney;
				$island->{'oil'} += $value;

				# 収入ログ
				my $lName = landName( $landKind, $lv );
				logOut(
"${HtagName_}${name}${AfterName}${H_tagName}の<B>$lName</B>から、<B>$value$HunitOil</B>の収益が上がりました。",
					$id
				);
			}
		}
		elsif ( ( $landKind == $HlandWaste ) && ( $lv >= 10 ) ) {

			# 温泉
			my $value = $lv * ( random(23) + 1 );
			$island->{'money'} += $value;

			# 収入ログ
			logOilMoney( $id, $name, landName( $landKind, $lv ),
				"($x, $y)", $value );

			# 枯渇判定
			if ( random(10) < 6 ) {
				$landValue->[$x][$y] -= random(21);
				if ( $landValue->[$x][$y] < 10 ) {

					# 枯渇
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

			# 平地
			if ( random(5) == 0 ) {

				# 周りに農場、町があれば、ここも町になる
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

	  # 博覧会、スタジアム、ドーム、遊園地、空港、動物園
			$island->{'money'} += 40;
		}
		elsif ( $landKind == $HlandCasino ) {

			# カジノ
			$island->{'money'} += random(150) - 50;
		}
		elsif ( $landKind == $HlandBigcity ) {

			# 大都市
			$island->{'food'} -= 400 if ( !$HbigcityFood );

			#	}elsif(($landKind == $HlandPark) || ($landKind == $HlandSchool)){
			#		# 公園、学校
			#		$island->{'money'} += 10;
		}
		elsif (( $landKind == $HlandWindmill )
			|| ( $landKind == $HlandPolice )
			|| ( $landKind == $HlandHospital ) )
		{

			# 風車、警察署、病院維持費
			if ( $island->{'money'} < 5 ) {
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
			}
			else {
				$island->{'money'} -= 5;
			}
		}
		elsif ( ( $landKind == $HlandTower ) && ( $lv >= 200 ) ) {

# MAX商業ビル
#		HdebugOut($island->{'name'} . "：商業の規模：" . $island->{'tower'} . ":人口増パラ３：${pop3}：");
			if (   ( $island->{'pop'} >= 8000 )
				&& ( $island->{'tower'} > 450 )
				&& ( $pop3 > 2 )
				&& ( random(5) == 0 ) )
			{
				my $lName  = landName( $HlandTower, 200 );
				my $lName2 = landName( $HlandTcity, 200 );
				logOut(
"${HtagName_}${name}${AfterName}($x, $y)${H_tagName}の<B>$lName</B>が、<B>$lName2</B>に発展しました。",
					$id
				);
				$land->[$x][$y]      = $HlandTcity;
				$landValue->[$x][$y] = 200;
			}
		}
		elsif ( $landKind == $HlandTcity ) {

# 商業都市
#		HdebugOut($island->{'name'} . "：商業都市:人口増パラ３：${pop3}：");
			if (   ( $island->{'pop'} < 7000 )
				|| ( ( $pop3 < -3 ) && ( random(5) == 0 ) ) )
			{
				my $lName  = landName( $HlandTcity, 200 );
				my $lName2 = landName( $HlandTower, 200 );
				logOut(
"${HtagName_}${name}${AfterName}($x, $y)${H_tagName}の<B>$lName</B>が、<B>$lName2</B>にレベルダウンしました。",
					$id
				);
				$land->[$x][$y]      = $HlandTower;
				$landValue->[$x][$y] = 200;
			}
		}
		elsif ( $landKind == $HlandSeisei ) {

			# 精製場
			my $value = $lv * 100;
			$island->{'money'} += $value;

			# 収入ログ
			logOilMoney( $id, $name, landName( $landKind, $lv ),
				"($x, $y)", $value );

			# 枯渇判定
			if ( random(1000) < $HoilRatio ) {
				logOilEnd( $id, $name, landName( $landKind, $lv ), "($x, $y)" );
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
			}
		}
		elsif ( $landKind == $HlandMonster ) {

			# 怪獣
			# 各要素の取り出し
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

				# すでに動いた後
				next;
			}

			# 硬化中?
			if (
				   ( ( $special == 3 ) && ( ( $HislandTurn % 2 ) == 1 ) )
				|| ( ( $special == 4 ) && ( ( $HislandTurn % 2 ) == 0 ) )
				|| ( $special == 5 )
				|| (   ( $island->{'manipulate'} == 0 )
					&& ( ( $special == 6 ) || ( $special == 7 ) ) )
			  )
			{
				next;    # 硬化中
			}

			if ( $special == 9 ) {

				# 全回復する
				$landValue->[$x][$y] = $mKind * 100 + $HmonsterBHP[$mKind];
				logMonster( $id, $name, "($x, $y)", $mName,
"は、精神を集中したかと見えるとみるみる傷が回復しました。"
				);
			}

			# 移動する
			my ( $sx, $sy ) = monmove( $island, $x, $y, 0 );

			# 移動済みフラグ
			if ( $HmonsterSpecial[$mKind] == 2 ) {

				# 移動済みフラグは立てない
			}
			elsif ( $HmonsterSpecial[$mKind] == 1 ) {

				# 速い怪獣
				$monsterMove[$sx][$sy] = $monsterMove[$x][$y] + 1;
			}
			else {

				# 普通の怪獣
				$monsterMove[$sx][$sy] = 2;
			}
		}
		elsif ( $landKind == $HlandKInora ) {

			# 究想いのら
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

		 # ありえない地形の時は、とりあえず荒地にしておく
			$land->[$x][$y]      = $HlandWaste;
			$landValue->[$x][$y] = 0;
		}
		if ($Htournament) {

			# 簡易トーナメント
			if ( $HislandFightMode == 3 ) {

				# 戦闘中
			}
			else {

				# それ以外
				if ( $landKind == $HlandWarp ) {

					# 転移装置はとりあえずお花にする。
					logEventP( $id, $name, "($x, $y)",
"の転移装置は、戦闘期間でないため取り壊されお花が植えられました。"
					);
					$land->[$x][$y]      = $HlandFlower;
					$landValue->[$x][$y] = random(13) + 1;
				}
			}
		}
		if ( ( $land->[$x][$y] > 100 ) || ( $landKind == $HlandKInora ) ) {

			# 船系、究想いのらのとき
		}
		elsif (( $land->[$x][$y] == $HlandMonster )
			|| ( $land->[$x][$y] == $HlandHaribote ) )
		{
			if ( $landValue->[$x][$y] > 4000 ) {

			# ありえない値なので、とりあえず荒地にしておく
				$land->[$x][$y]      = $HlandWaste;
				$landValue->[$x][$y] = 0;
			}
		}
		elsif (( $land->[$x][$y] == $HlandBase )
			|| ( $land->[$x][$y] == $HlandSbase ) )
		{
			if ( $landValue->[$x][$y] > 250 ) {

			# 250以上はありえないのでとりあえず250にしておく
				$landValue->[$x][$y] = 250;
			}
		}
		elsif (( $landValue->[$x][$y] > 200 )
			&& ( $land->[$x][$y] != $HlandWarp ) )
		{

# 200以上はありえないのでとりあえず200にしておく 転移装置以外
#		HdebugOut("地形データ値不正の為とりあえず２００にします。:LAND=" . $land->[$x][$y] . ":LV=" . $landValue->[$x][$y]);
			$landValue->[$x][$y] = 200;
		}

		# 巨大地形変化
		# 変更開始  <5.54e>
		#	($landKind,$lv) = ($land->[$x][$y],$landValue->[$x][$y]);
		$landKind = $land->[$x][$y];

		# 変更終了  <5.54e>
		if (   ( ( $landKind == $HlandTown ) && ( $lv >= 201 ) )
			|| ( ( $landKind == $HlandFarm )    && ( $lv >= 50 ) )
			|| ( ( $landKind == $HlandFactory ) && ( $lv >= 90 ) )
			|| ( ( $landKind == $HlandTower )   && ( $lv >= 180 ) ) )
		{

			# 200の都市、農場、工場、商業ビルのとき
			my ( $i, $j, $r, $sx, $sy );
			for ( $i = 1 ; $i < 7 ; $i++ ) {
				$sx = $x + $ax[$i];
				$sy = $y + $ay[$i];
				$sx--
				  if ( !( $sy % 2 ) && ( $y % 2 ) );  # 行による位置調整
				if (   ( $sx < 0 )
					|| ( $sx >= $HislandSize )
					|| ( $sy < 0 )
					|| ( $sy >= $HislandSize ) )
				{

					# 範囲外の場合何もしない
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

					# 範囲内の場合で合体可能地形があったとき

					# 意味不明な計算をして複雑にする。
					$r = 30;
					$r -= 20 if ( $island->{'propaganda'} == 1 ); # 誘致活動
					$r += 170 if ( $island->{'evil'} == 0 );   # 国連保護国
					$r -= 15
					  if ( $island->{'event'} == 1 ); # 人口増のイベント
					if ( $island->{'Crime'} + $island->{'Pollution'} +
						$island->{'Kouzui'} + $island->{'Hideri'} >= 1 )
					{

						# 犯罪、公害、洪水、日照り
						$r += 1000;
					}
					if ( $island->{'zyuni'} > 700 ) {    # 順位点
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

					# 部門賞数を計算
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

						# 合体先の地形の方向を求める
						if ( $i < 4 ) {
							$j = $i + 3;
						}
						else {
							$j = $i - 3;
						}
						my ($lName) = landName( $landKind, $lv );
						my ($lName2);
						if ( $landKind == $HlandTown ) {

							# 都市のとき
							$lName2 = landName( $HlandMegacity, 0 );
							$land->[$x][$y]   = $HlandMegacity;
							$land->[$sx][$sy] = $HlandMegacity;
						}
						elsif ( $landKind == $HlandFarm ) {

							# 農場のとき
							$lName2 = landName( $HlandMegaFarm, 0 );
							$land->[$x][$y]   = $HlandMegaFarm;
							$land->[$sx][$sy] = $HlandMegaFarm;
						}
						elsif ( $landKind == $HlandFactory ) {

							# 工場のとき
							$lName2 = landName( $HlandMegaFact, 0 );
							$land->[$x][$y]   = $HlandMegaFact;
							$land->[$sx][$sy] = $HlandMegaFact;
						}
						elsif ( $landKind == $HlandTower ) {

							# 商業ビルのとき
							$lName2 = landName( $HlandMegatower, 0 );
							$land->[$x][$y]   = $HlandMegatower;
							$land->[$sx][$sy] = $HlandMegatower;
						}
						logEventP( $id, $name, "($x, $y)",
"と${HtagName_}($sx, $sy)${H_tagName}の${lName}が${lName2}に発展しました。"
						);
						$landValue->[$x][$y]   = $i;
						$landValue->[$sx][$sy] = $j;
						last;
					}
				}
			}
		}
		( $landKind, $lv ) = ( $land->[$x][$y], $landValue->[$x][$y] );

		# 汚染拡散
		if ( random(5) == 0 ) {

			# 平地、荒地、温泉、農場、汚染の時
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

		# 精製場による汚染
		# 海系、怪獣、山、汚染、記念碑以外
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

		# 雨による森増殖
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

		# 温泉による地盤沈下判定
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

		# 再噴火判定
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

		# 海底系過剰シーいのら判定
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

		# 埋め立ていのら、海風船判定
		if (   ( ( $landKind == $HlandSea ) && ( $lv <= 1 ) )
			&& ( $island->{'pop'} >= $HdisMonsBorder1 ) )
		{    # 海、浅瀬、人口規定値１以上
			my $r = random($HdisMonsterU);
			if ( $r == 0 ) {
				if ( ($HsurvFlg) && ( $HdisMonster == 0 ) ) {

				 # サバイバル、怪獣発生率0の場合は出現しない
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

		# 火災判定
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
				elsif ( $wkind > 3 ) {    # 雨の時
					$wf = ( $whp > 7 ) ? 4000 : 2000;
				}
			}
			if ( random($wf) < $HdisFire ) {

				# 周囲の森と記念碑を数える公園、風車も
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
					||    # 周囲に火災を防ぐ地形が無い場合
					( ( $landKind == $HlandOil ) && ( $s == 0 ) )
					||    # 海底系で周囲に海底記念碑が無い場合
					( ( $landKind == $HlandOil ) && ( $lv == 7 ) )
					||    # 海底消防署の場合
					( $landKind == $HlandFire )
				  )
				{         # 消防署の場合
					my $fire1 =
					  chkAround( $land, $x, $y, $HlandFire, 19 );    # 消防署
					my $fire2 =
					  chkAroundEX( $land, $landValue, $x, $y, $HlandFire, 10,
						37 );    # S消防署
					my $fire3 =
					  chkAroundEX( $land, $landValue, $x, $y, $HlandOil, 7,
						19 );    # 海底消防署

					if (   ( $fire1 + $fire2 )
						&& ( $landKind != $HlandFire )
						&& ( $landKind != $HlandOil ) )
					{            # 陸の火災を防げる時
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
					{    # 海の火災を防げる時
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

# 島全体
sub doIslandProcess {
	my ( $number, $island ) = @_;

	# 導出値
	my ( $name, $id, $land, $landValue, $land2, $landValue2 ) = (
		$island->{'name'},      $island->{'id'},    $island->{'land'},
		$island->{'landValue'}, $island->{'land2'}, $island->{'landValue2'}
	);

	if ( $island->{'SSSystem'} ) {

#	logEvent($id, $name,"は、<B>スーパーシールドシステム</B>を発動中！！");
	}
	else {

		# 究想いのら判定(制裁のみ)
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

			# Battle Fieldのとき
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

#	HdebugOut($island->{'name'} . "$AfterName 衛星：" . $island->{'eis0'} . "：" . $island->{'eis1'} . "：" . $island->{'eis2'});
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

		# 地震判定
		if (
			( $HpunishInfo{$id}->{punish} == 1 )
			|| ( random(1000) <
				( ( $island->{'prepare2'} + 1 ) * $disEarthquake ) )
		  )
		{

			# 地震発生
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

				# 発生しない！
			}
			else {
				logEarthquake( $id, $name, "($x, $y)" );

				# 震源が海なら津波発生
				$island->{'tunami'} = 1 if ( $HseaChk[ $land->[$x][$y] ] );

				# 周囲4ヘックスに被害
				for ( $i = 0 ; $i < 61 ; $i++ ) {
					$sx = $x + $ax[$i];
					$sy = $y + $ay[$i];
					$sx--
					  if ( !( $sy % 2 ) && ( $y % 2 ) )
					  ;    # 行による位置調整
					my ($landKind) = $land->[$sx][$sy];
					my ($lv)       = $landValue->[$sx][$sy];
					my ($landName) = landName( $landKind, $lv );
					my ($point)    = "($sx, $sy)";
					next
					  if ( ( $sx < 0 )
						|| ( $sx >= $HislandSize )
						|| ( $sy < 0 )
						|| ( $sy >= $HislandSize ) );    # 範囲外判定
					my ($d) = 0;

					if (   ( ( $landKind == $HlandTown ) && ( $lv >= 50 ) )
						|| ( ( $landKind == $HlandSlum ) && ( $lv >= 30 ) )
						|| ( $landKind == $HlandHaribote )
						|| ( $landKind == $HlandFactory ) )
					{

			 # 5千以上の町、3千以上のスラム、ハリボテ、工場
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

		# 食料不足
		if ( $island->{'food'} <= 0 ) {

			# 不足メッセージ
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

					# 1/4で壊滅
					if ( random(4) == 0 ) {
						if ( $kind == $HlandHugecity ) {

							# 超巨大都市
							my ($lName2) =
							  landName( $HlandMonument, $landValue->[$x][$y] );
							logEventP( $id, $island->{'name'}, "($x, $y)",
"の<B>$lName</B>に<B>食料を求めて住民が殺到</B>。<B>$lName</B>は<B>$lName2</B>に戻ってしまいました。"
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

		# 津波判定
		if ( ( $HpunishInfo{$id}->{punish} == 2 )
			|| (   ( random(1000) < $disTsunami )
				|| ( $island->{'tunami'} >= 1 ) ) )
		{

			# 津波発生
			my ( $x, $y, $landKind, $lv, $i, $p, $q );
			if ( $island->{'tunami'} == 1 ) {   # 海底地震による大津波
				logEvent( $id, $name,
"の地震は、震源が海だったため${HtagDisaster_}大津波${H_tagDisaster}発生！！"
				);
				$p = 10;
				$q = 25;
			}
			else {    # 通常の津波、コロニー落しの津波
				logEvent( $id, $name,
"付近で${HtagDisaster_}津波${H_tagDisaster}発生！！"
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
								"($x, $y)", "被害を受け" );
							$landValue->[$x][$y] -= random(40) + 20;
						}
						elsif (( $landKind == $HlandBase )
							&& ( $lv > 0 )
							&& ( random(3) < 2 ) )
						{
							logTsunamiDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "被害を受け" );
							$landValue->[$x][$y] = random($lv) + 1;
						}
						elsif (( $landKind == $HlandFarm )
							&& ( $lv > 10 )
							&& ( random(3) < 2 ) )
						{
							logTsunamiDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "被害を受け" );
							$landValue->[$x][$y] = 10;
						}
						elsif (( $landKind == $HlandFactory )
							&& ( $lv > 30 )
							&& ( random(3) < 2 ) )
						{
							logTsunamiDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "被害を受け" );
							$landValue->[$x][$y] = 30;
						}
						elsif (( $landKind == $HlandPort )
							&& ( $lv > 40 )
							&& ( random(3) < 2 ) )
						{
							logTsunamiDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "被害を受け" );
							$landValue->[$x][$y] = 40;
						}
						else {
							logTsunamiDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "崩壊し" );
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
							"($x, $y)", "崩壊し" );
						$land->[$x][$y]      = $HlandSea;
						$landValue->[$x][$y] = 1;
					}
				}
			}
		}

		# 怪獣判定
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

				# 怪獣出現
				# 種類を決める
				my ( $lv, $kind, $human );
				$human = 0;
				if ( $island->{'monsEnsei'} > 0 ) {

					# S怪獣派遣
					$kind                  = $island->{'monsEnsei'};
					$human                 = 1;
					$island->{'monsEnsei'} = 0;
				}
				elsif ( $island->{'monstersend'} > 0 ) {

					# 人造
					$kind  = 0;
					$human = 1;
					$island->{'monstersend'}--;
				}
				elsif ( $island->{'monstersend1'} > 0 ) {

					# 人造
					$kind  = 11;
					$human = 1;
					$island->{'monstersend1'}--;
				}
				elsif ( $island->{'monstersend2'} > 0 ) {

					# 人造
					$kind  = 22;
					$human = 1;
					$island->{'monstersend2'}--;
				}
				elsif ( $island->{'monstersend3'} > 0 ) {

					# 人造
					$kind  = 25;
					$human = 1;
					$island->{'monstersend3'}--;
				}
				elsif ( $island->{'TeruteruMons'} > 0 ) {

					# てるてるいのら(28)、# 逆さてるてる(29)
					$kind = ( $island->{'TeruteruMons'} == 1 ) ? 28 : 29;
					$island->{'TeruteruMons'} = 0;
				}
				elsif ( $pop >= $HdisMonsBorder5 ) {

					# level5まで
					$kind = $HmonsterL5[ random($HmonsterL5Num) ];
				}
				elsif ( $pop >= $HdisMonsBorder4 ) {

					# level4まで
					$kind = $HmonsterL4[ random($HmonsterL4Num) ];
				}
				elsif ( $pop >= $HdisMonsBorder3 ) {

					# level3まで
					$kind = $HmonsterL3[ random($HmonsterL3Num) ];
				}
				elsif ( $pop >= $HdisMonsBorder2 ) {

					# level2まで
					$kind = $HmonsterL2[ random($HmonsterL2Num) ];
				}
				else {

					# level1のみ
					$kind = $HmonsterL1[ random($HmonsterL1Num) ];
				}

				# lvの値を決める
				$lv = $kind * 100 + $HmonsterBHP[$kind] +
				  random( $HmonsterDHP[$kind] );

				# どこに現れるか決める
				my ( $bx, $by, $i );
				for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
					$bx = $Hrpx[$i];
					$by = $Hrpy[$i];
					if ( $kind == 25 ) {

						# 海底メカいのら

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

						# そのヘックスを怪獣に
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

# 海底の人口が陸上より多い時に出現する地形がない時(地球攻撃時も)は、森かミサイル基地にでる。
					for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
						$bx = $Hrpx[$i];
						$by = $Hrpy[$i];
						if (   ( $land->[$bx][$by] == $HlandBase )
							|| ( $land->[$bx][$by] == $HlandForest ) )
						{

							# そのヘックスを怪獣に
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

		# ミサイル数による怪獣判定(r=0-9999)
		if (   ( $r > 9969 )
			&& ( $island->{'MissileK'} >= 30 )
			&& ( $HdisMonster > 0 ) )
		{
			my ( $lv, $kind );
			if ( $r > 9994 ) {
				$kind = 17;    # タイムボカン
			}
			elsif ( $r > 9989 ) {
				$kind = 18;    # 反撃
			}
			elsif ( $r > 9984 ) {
				$kind = 20;    # スペース
			}
			elsif ( $r > 9979 ) {
				$kind = 21;    # シーゴースト
			}
			elsif ( $r > 9974 ) {
				$kind = 30;    # 回復いのら
			}
			else {
				$kind = 23;    # カネゴン
			}
			$lv =
			  $kind * 100 + $HmonsterBHP[$kind] + random( $HmonsterDHP[$kind] );
			my ( $mKind, $mName, $mHp ) = monsterSpec($lv);

			# どこに現れるか決める
			my ( $bx, $by, $i );
			for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
				$bx = $Hrpx[$i];
				$by = $Hrpy[$i];
				if ( $kind == 21 ) {

					# シーゴースト
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

		# 地盤沈下判定
		if (
			(
				   ( $HpunishInfo{$id}->{punish} == 4 )
				|| ( random(1000) < $HdisFalldown )
			)
			&& ( $island->{'area'} > $HdisFallBorder )
		  )
		{

			# 地盤沈下発生
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

					# 周囲に海があれば、値を-1に
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

					# -1になっている所を浅瀬に
					$land->[$x][$y]      = $HlandSea;
					$landValue->[$x][$y] = 1;
				}
				elsif (( $landKind == $HlandSea )
					|| ( $landKind == $HlandBreakwater ) )
				{

					# 浅瀬、防波堤は海に
					$land->[$x][$y]      = $HlandSea;
					$landValue->[$x][$y] = 0;
				}
			}
		}

		# 台風判定
		if (   ( $HpunishInfo{$id}->{punish} == 5 )
			|| ( random(1000) < $disTyphoon ) )
		{

			# 台風発生
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

					# 1d12 <= (6 - 周囲の森) で崩壊
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

						# S消防署があると台風の確率半減
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
								"($x, $y)", "破壊され" );
							$land->[$x][$y]      = $HlandSea;
							$landValue->[$x][$y] = 1;
						}
						elsif ( ( $landKind == $HlandFarm ) && ( $lv > 21 ) ) {
							logTyphoonDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "被害を受け" );
							$landValue->[$x][$y] = $lv - 10;
						}
						elsif ( ( $landKind == $HlandFarm ) && ( $lv > 13 ) ) {
							logTyphoonDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "被害を受け" );
							$landValue->[$x][$y] = 10;
						}
						else {
							logTyphoonDamage( $id, $name,
								landName( $landKind, $lv ),
								"($x, $y)", "飛ばされ" );
							$land->[$x][$y]      = $HlandPlains;
							$landValue->[$x][$y] = 0;
						}
					}
				}
				elsif (( $landKind == $HlandFishSShip )
					|| ( $landKind == $HlandFishMShip ) )
				{

					# 小型、中型漁船
					if ( random(10) == 0 ) {
						logTyphoonDamage( $id, $name,
							landName( $landKind, $lv ),
							"($x, $y)", "難破し" );
						if ( random(20) == 0 ) {

							# 幽霊船
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

		# 赤潮判定
		if ( ( random(1000) < $disAkasio + int( $island->{'yousyoku'} / 200 ) )
			&& ( $disAkasio != 0 ) )
		{
			if ( $island->{'yousyoku'} > 0 ) {

				# 赤潮発生
				logEvent( $id, $name,
					"に${HtagDisaster_}赤潮${H_tagDisaster}発生！！" );
				my ( $x, $y, $landKind, $lv, $i, $p );
				for ( $i = 0 ; $i < $HpointNumber ; $i++ ) {
					$x        = $Hrpx[$i];
					$y        = $Hrpy[$i];
					$landKind = $land->[$x][$y];
					if (   ( $landKind == $HlandSea )
						&& ( $landValue->[$x][$y] >= 10 ) )
					{

					 # 1d10 <= (周囲2マスの工場または町系) で崩壊
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

			# 宝船存在時、海賊船出現確率が２倍になる
			$pirate = 500;
		}
		else {

# 宝船が存在しないとき宝船出現判定、客船があるほどでやすくなる。
			if ( random(1000) < $HdisTreasureS + $island->{'titanic'} * 0.4 ) {
				my ( $x, $y ) = shipAppear( $land, random(4) );

				# 地形保存
				$land2->[$x][$y]      = $land->[$x][$y];
				$landValue2->[$x][$y] = $landValue->[$x][$y];
				$land->[$x][$y]       = $HlandTreasureS;
				$landValue->[$x][$y]  =
				  10000 + $HshipHP[ $HlandTreasureS - $HlandPirate ] * 1000;

				logShipCome( $id, $name, landName( $HlandTreasureS, 0 ),
					"($x, $y)" );
			}
		}

# 海賊船、幽霊船、翼竜出現判定 漁船が１０隻以上だとでやすくなる。
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

				# 地形保存
				$land2->[$x][$y]      = $land->[$x][$y];
				$landValue2->[$x][$y] = $landValue->[$x][$y];

				my ( $newship, $point );
				if ( $island->{'wingdragon'} > 0 ) {

					# 翼竜
					$newship = $HlandWingDragon;
					$landValue->[$x][$y] =
					  10000 + $HshipHP[ $newship - $HlandPirate ] * 1000;
					$island->{'wingdragon'} = 0;
					$point = "($x, $y)";
				}
				elsif ( $island->{'icefloe'} > 0 ) {

					# 流氷
					$newship = $HlandIceFloe;
					$landValue->[$x][$y] =
					  10000 + $HshipHP[ $newship - $HlandPirate ] * 1000;
					$island->{'icefloe'} = 0;
					$point = "($x, $y)";
				}
				elsif ( $island->{'couplerock'} > 0 ) {

					# 夫婦岩
					$newship = $HlandCoupleRock;
					$landValue->[$x][$y] =
					  10000 + $HshipHP[ $newship - $HlandPirate ] * 1000;
					$island->{'couplerock'} = 0;
					$point = "($x, $y)";
				}
				elsif ( $island->{'ghost'} > 0 ) {

					# 幽霊船
					$newship = $HlandGhostShip;
					$landValue->[$x][$y] =
					  $HshipHP[ $newship - $HlandPirate ] * 1000;
					$island->{'ghost'} = 0;
					$point = "(?, ?)";
				}
				else {

					# 海賊船
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

		# 巨大隕石判定
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

			# S,SS防衛施設
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

				# S,SS防衛施設で防ぐ（頭上以外）
				logMeteoD( $id, $name,
					landName( $land->[$x][$y], $landValue->[$x][$y] ),
					"($x, $y)", '巨大隕石' );
			}
			else {
				logHugeMeteo( $id, $name, "($x, $y)" );
				wideDamage( $id, $name, $land, $landValue, $x, $y, 0 );
			}
		}

		# 巨大ミサイル判定
		while ( $island->{'bigmissile'} > 0 ) {
			$island->{'bigmissile'}--;
			my $x = random($HislandSize);
			my $y = random($HislandSize);
			logMonDamage( $id, $name, "($x, $y)" );

			# 広域被害ルーチン
			wideDamage( $id, $name, $land, $landValue, $x, $y, 0 );
		}

		# コロニー落し判定
		while ( $island->{'colony'} > 0 ) {
			$island->{'colony'}--;
			my $x = random($HislandSize);
			my $y = random($HislandSize);
			logMonDamage( $id, $name, "($x, $y)" );

			# 広域被害ルーチン
			SuperDamage( $id, $name, $land, $landValue, $x, $y );
		}

		# 隕石判定
		if (   ( $HpunishInfo{$id}->{punish} == 7 )
			|| ( random(1000) < ( ( $island->{'Meteo'} + 1 ) * $disMeteo ) ) )
		{
			my ( $x, $y, $landKind, $lv, $point, $first );
			$first = 1;
			while ( ( random(2) == 0 ) || ( $first == 1 ) ) {
				$first = 0;

				# 落下
				$x        = random($HislandSize);
				$y        = random($HislandSize);
				$landKind = $land->[$x][$y];
				$lv       = $landValue->[$x][$y];
				$point    = "($x, $y)";

				# S,SS防衛施設
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

					# S,SS防衛施設で防ぐ（頭上以外）
					logMeteoD( $id, $name, landName( $landKind, $lv ),
						$point, '隕石' );
					next;
				}

				# イージス艦チェック
				if ( $island->{'aegis'} > 4 ) {
					$island->{'aegis'} -= 5;

			#				HdebugOut("イージス艦迎撃準備:" . $island->{'money'});
					if ( ( random(3) == 0 ) && ( $island->{'money'} > 500 ) ) {
						$island->{'money'} -= 500;
						logMeteoD( $id, $name, landName( $landKind, $lv ),
							$point, '隕石' );
						next;
					}
				}

				if ( ( $landKind == $HlandSea ) && ( $lv == 0 ) ) {

					# 海ポチャ
					logMeteoSea( $id, $name, landName( $landKind, $lv ),
						$point );
				}
				elsif ( $landKind == $HlandMountain ) {

					# 山破壊
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

					# 浅瀬、防波堤
					logMeteoSea1( $id, $name, landName( $landKind, $lv ),
						$point );
				}
				elsif ( $landKind == $HlandWarp ) {

					# 転移
					logWarpMeteo( $id, $name, landName( $landKind, $lv ),
						$point );

					#			$land->[$x][$y] = $HlandWaste;
					#			$landValue->[$x][$y] = 0;
					my ($st) = warp( $id, $name, 0, 0, "隕石", $lv, 12 );
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

		# 噴火判定
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
					"($x, $y)", "噴火" );
			}
			else {
				$x = $island->{'AEruptionX'};
				$y = $island->{'AEruptionY'};
				logEruption( $id, $name,
					landName( $land->[$x][$y], $landValue->[$x][$y] ),
					"($x, $y)", "再噴火" );
			}
			$land->[$x][$y]      = $HlandMountain;
			$landValue->[$x][$y] = 0;
			for ( ; $i < 7 ; $i++ ) {
				$sx = $x + $ax[$i];
				$sy = $y + $ay[$i];
				$sx--
				  if ( !( $sy % 2 ) && ( $y % 2 ) );  # 行による位置調整
				$landKind = $land->[$sx][$sy];
				$lv       = $landValue->[$sx][$sy];
				if (   ( $sx < 0 )
					|| ( $sx >= $HislandSize )
					|| ( $sy < 0 )
					|| ( $sy >= $HislandSize ) )
				{
				}
				else {

					# 範囲内の場合
					$landKind = $land->[$sx][$sy];
					$lv       = $landValue->[$sx][$sy];
					if ( $HseaChk[$landKind] ) {

						# 海の場合
						if (   ( ( $landKind == $HlandSea ) && ( $lv >= 1 ) )
							|| ( $landKind == $HlandBreakwater ) )
						{

							# 浅瀬、防波堤
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

						# それ以外の場合
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

	# 怪獣バトル

	# 各要素の取り出し
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

		# 怪獣餌取得フラグが立っている

		$MBsId = $island->{'esa'};
		logMonsESA( $id, $name, $HmonsterName[$MBsId] );
	}

	if ( $MBid == 0 ) {

		# 自分の怪獣がいない
	}
	elsif ( $id != $MBid ) {

		# 遠征中

		if ( $tn eq '' ) {
			$MBid = $id
			  ; # 相手がいなくなったので怪獣を自分の島に戻す。
			$MBhp  = $MBmhp;
			$MBtId = 0;
		}
	}
	elsif ( $tn eq '' ) {
		$MBid = $id; # 相手がいないので怪獣を自分の島に戻す。
		$MBhp  = $MBmhp;
		$MBtId = 0;
	}
	else {

		# 対戦相手がいるとき
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

		# 戦闘ルーチン

		my ( $mId, $tmId );    # モンスターID
		if ( $MBmId == 19 ) {  # アシュラの時
			$mId = random(25);
		}
		else {
			$mId = $MBmId;
		}
		if ( $tMBmId == 19 ) {    # アシュラの時
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

		# 特殊能力が発動するか
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

		# 特殊能力が発動するか
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

		 # 片一方でも相手の特殊能力無効技持っている場合。
			$sp  = 0;
			$tsp = 0;
		}

		my ( $first, $end ) = ( 1, 3 );
		if ( $speed == $tspeed ) {

			# 両者動かなかった。
			logMonsNOATTACK( $MBtId, $tName, $tMBname, $id, $name, $MBname );
			$first = 3;
		}
		elsif ( $speed > $tspeed ) {

			# 自分の怪獣先制攻撃

			$first = 0;
			$end   = 2;
		}
		else {

			# 相手の先制攻撃

		}
		my ($special)  = $HmonsterSpecial[$mId];
		my ($special2) = $HmonsterSpecial[$tmId];

		my ($BattleEnd) = 0;

		while ( $first < $end ) {
			if ( $first == 1 ) {

				# 相手の攻撃

				if (   ( ( $tsp == 1 ) && ( ( $HislandTurn % 2 ) == 0 ) )
					|| ( ( $tsp == 2 ) && ( ( $HislandTurn % 2 ) == 1 ) ) )
				{

					# 硬化中で攻撃しない
					$first++;
					next;
				}
				if ( $tmei > $kai ) {

					# 相手の攻撃があたった
					if ( ( $sp == 5 ) && ( $spskl >= 2 ) ) {

						# 特殊能力で避けた
						logMonsATTACK(
							$MBtId,
							$tName,
							$tMBname,
							$id,
							$name,
							$MBname,
"通常攻撃、しかしよけられてしまった。"
						);
					}
					elsif ( ( $sp == 6 ) && ( $spskl >= 1 ) ) {

						# 特殊能力で防御した
						logMonsATTACK(
							$MBtId,
							$tName,
							$tMBname,
							$id,
							$name,
							$MBname,
"通常攻撃、しかしダメージをあたえられない。"
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

# 硬化中でダメージをくらわない、ただしサンジラとクジラは除く
						logMonsATTACK(
							$MBtId,
							$tName,
							$tMBname,
							$id,
							$name,
							$MBname,
"通常攻撃、しかしダメージをあたえられない。"
						);
					}
					elsif ( ( $tsp == 8 ) && ( $tMBhp <= 10 ) ) {

						# 自爆攻撃

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
"自爆攻撃、${tdamage}のダメージをあたえた。"
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
"自爆攻撃、しかしよけられてしまった。"
							);
							logMonsEND( $MBtId, $tName, $tMBname, $MBtId,
								"自滅しました。" );
							logMonsEND( $id, $name, $MBname, $MBtId,
								"戦いに勝利しました。" );

							$BattleEnd = 1;
							last;
						}
					}
					elsif ( ( $tsp == 7 ) && ( $tspskl >= 2 ) ) {

						# 必殺攻撃

						$tdamage = $tdamage * 2;
						$MBhp    = $MBhp - $tdamage;
						logMonsATTACK(
							$MBtId,
							$tName,
							$tMBname,
							$id,
							$name,
							$MBname,
"必殺の一撃、${tdamage}のダメージをあたえた。"
						);
					}
					elsif ( ( $tsp == 9 ) && ( $tspskl >= 3 ) ) {

						# 隕石落し
						$tdamage = $tdamage * 3;
						$MBhp    = $MBhp - $tdamage;
						logMonsATTACK(
							$MBtId,
							$tName,
							$tMBname,
							$id,
							$name,
							$MBname,
"必殺の隕石落し発動、${tdamage}のダメージをあたえた。"
						);
					}
					else {

						# 通常攻撃

						$MBhp = $MBhp - $tdamage;
						logMonsATTACK(
							$MBtId,
							$tName,
							$tMBname,
							$id,
							$name,
							$MBname,
"通常攻撃、${tdamage}のダメージをあたえた。"
						);
					}
					if ( $MBhp < 1 ) {

						# まけてしまった。
						logMonsEND( $MBtId, $tName, $tMBname, $id,
							"戦いに勝利しました。" );

						$BattleEnd = 2;
						last;
					}
				}
				else {

					# 相手の攻撃をよけた
					logMonsATTACK(
						$MBtId,
						$tName,
						$tMBname,
						$id,
						$name,
						$MBname,
						"通常攻撃、しかしよけられてしまった。"
					);
				}
			}
			else {

				# 自分の攻撃

				if (   ( ( $sp == 1 ) && ( ( $HislandTurn % 2 ) == 0 ) )
					|| ( ( $sp == 2 ) && ( ( $HislandTurn % 2 ) == 1 ) ) )
				{

					# 硬化中で攻撃しない
					$first++;
					next;
				}
				if ( $mei > $tkai ) {

					# 自分の攻撃があたった
					if ( ( $tsp == 5 ) && ( $tspskl >= 2 ) ) {

						# 特殊能力で避けた
						logMonsATTACK(
							$id,
							$name,
							$MBname,
							$MBtId,
							$tName,
							$tMBname,
"通常攻撃、しかしよけられてしまった。"
						);
					}
					elsif ( ( $tsp == 6 ) && ( $tspskl >= 1 ) ) {

						# 特殊能力で防御した
						logMonsATTACK(
							$id,
							$name,
							$MBname,
							$MBtId,
							$tName,
							$tMBname,
"通常攻撃、しかしダメージをあたえられない。"
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

# 硬化中でダメージをくらわない、ただしサンジラとクジラは除く
						logMonsATTACK(
							$id,
							$name,
							$MBname,
							$MBtId,
							$tName,
							$tMBname,
"通常攻撃、しかしダメージをあたえられない。"
						);
					}
					elsif ( ( $sp == 8 ) && ( $MBhp <= 10 ) ) {

						# 自爆攻撃

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
"自爆攻撃、${damage}のダメージをあたえた。"
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
"自爆攻撃、しかしよけられてしまった。"
							);
							logMonsEND( $id, $name, $MBname, $MBtId,
								"自滅しました。" );
							logMonsEND( $id, $tName, $tMBname, $MBtId,
								"戦いに勝利しました。" );

							$BattleEnd = 2;
							last;
						}
					}
					elsif ( ( $sp == 7 ) && ( $spskl >= 2 ) ) {

						# 必殺攻撃

						$damage = $damage * 2;
						$tMBhp  = $tMBhp - $damage;
						logMonsATTACK(
							$id,
							$name,
							$MBname,
							$MBtId,
							$tName,
							$tMBname,
"必殺の一撃、${damage}のダメージをあたえた。"
						);
					}
					elsif ( ( $sp == 9 ) && ( $spskl >= 3 ) ) {

						# 隕石落し
						$damage = $damage * 3;
						$tMBhp  = $tMBhp - $damage;
						logMonsATTACK(
							$id,
							$name,
							$MBname,
							$MBtId,
							$tName,
							$tMBname,
"必殺の隕石落し発動、${damage}のダメージをあたえた。"
						);
					}
					else {

						# 通常攻撃

						$tMBhp = $tMBhp - $damage;
						logMonsATTACK(
							$id,
							$name,
							$MBname,
							$MBtId,
							$tName,
							$tMBname,
"通常攻撃、${damage}のダメージをあたえた。"
						);
					}
					if ( $tMBhp < 1 ) {

						# まけてしまった。
						logMonsEND( $id, $name, $MBname, $MBtId,
							"戦いに勝利しました。" );

						$BattleEnd = 1;
						last;
					}
				}
				else {

					# 自分の攻撃よけられた
					logMonsATTACK(
						$id,
						$name,
						$MBname,
						$MBtId,
						$tName,
						$tMBname,
						"通常攻撃、しかしよけられてしまった。"
					);
				}
			}
			$first++;
		}

		if ( $BattleEnd > 0 ) {

			# 戦闘終了時は戦闘後の処理
			my (@up)  = ( 3, 3, 0, 3, 3 );
			my (@tup) = ( 3, 3, 0, 3, 3 );

			if ( $BattleEnd == 1 ) {
				if ( ( $tsp == 3 ) && ( random(3) == 0 ) ) {

					# 負けた時に３３％でジバクレイに進化
					$tMBmId = 15;
					logMonsEND( $MBtId, $tName, $tMBname, $id,
"死にきれずにジバクレイとなって転生しました。"
					);
				}
				@up = MonsterSei( 1, @up );    #成長率加算

				$MBwinh++;                     # 怪獣杯用
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

					# 負けた時に３３％でジバクレイに進化
					$MBmId = 15;
					logMonsEND( $id, $name, $MBname, $MBtId,
"死にきれずにジバクレイとなって転生しました。"
					);
				}
				@tup = MonsterSei( 1, @tup );    #成長率加算

				$tMBwinh++;                      # 怪獣杯用
				$tMBwin++;
				$MBlose++;
				if ( $Htournament == 2 ) {
					my ($achive) = refugees( 500, $tIsland );
					if ( $achive > 0 ) {
						logMsBoatPeople( $MBtId, $tName, $achive );
					}
				}
			}

			@up  = MonsterSei( $HmonsterSEI[$mId],  @up );     #成長率加算
			@tup = MonsterSei( $HmonsterSEI[$tmId], @tup );    #成長率加算

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

			# 継続中

			my ($point) = 5;
			if ( $sp == 11 ) {

				# 回復

				$MBhp = $MBhp + $point;
				if ( $MBhp > $MBmhp ) {
					$point -= $MBhp - $MBmhp;
					$MBhp = $MBmhp;
				}
				logMonsRrcovery( $id, $name, $MBname, $MBtId, $point );
			}
			elsif ( $tsp == 11 ) {

				# 回復

				$tMBhp = $tMBhp + $point;
				if ( $tMBhp > $tMBmhp ) {
					$point -= $tMBhp - $tMBmhp;
					$tMBhp = $tMBmhp;
				}
				logMonsRrcovery( $MBtId, $tName, $tMBname, $id, $point );
			}
		}
	}

	# ターン杯対象ターンだったら、その処理
	if ( ( $HislandTurn % $HturnPrizeUnit ) == 0 ) {
		if ( $MonsBattleTurn < $MBwinh ) {
			$MonsBattleTurn   = $MBwinh;
			$MonsBattleTurnID = $id;
		}
		$MBwinh = 0;
	}

	# 各要素格納
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

	# 各種の値を計算
	estimateE($number);

}    # doIslandProcess

# 機密ログに収支を表示
sub doIslandProcess2 {
	my ($island) = @_;
	if ( $island->{'id'} > 90 ) {

		# Battle Fieldのとき
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

	# 鉱石があふれてたら換金
	if ( $island->{'ore'} > $MaxSigen ) {
		$island->{'money'} += ( $island->{'ore'} - $MaxSigen );
		$island->{'ore'} = $MaxSigen;
	}

	# 原油があふれてたら換金
	if ( $island->{'oil'} > $MaxSigen ) {
		$island->{'money'} += ( $island->{'oil'} - $MaxSigen ) * 2;
		$island->{'oil'} = $MaxSigen;
	}

	# 兵器があふれてたら換金
	if ( $island->{'weapon'} > $MaxSigen ) {
		$island->{'money'} += ( $island->{'weapon'} - $MaxSigen ) * 6;
		$island->{'weapon'} = $MaxSigen;
	}

	# 食料があふれてたら換金
	if ( $island->{'food'} > $MaxFood ) {
		$island->{'money'} += int( ( $island->{'food'} - $MaxFood ) / 10 );
		$island->{'food'} = $MaxFood;
	}

	# 金があふれてたら切り捨て
	if ( $island->{'money'} > $MaxMoney ) {
		$island->{'money'} = $MaxMoney;
	}
	elsif ( $island->{'money'} < 0 ) {
		$island->{'money'} = 0;
	}

	my ( $iken, $iken2, $iken3 ) =
	  ( "", "", "(海底系${kaiteiw}％森${moriw}％)" );
	if ( ( $island->{'forest'} < 5 ) && ( random(5) == 0 ) ) {
		$iken = "自然保護団体が森林保護を求めています。";
	}
	elsif ( ( $island->{'forest'} < 4 ) && ( random(3) == 0 ) ) {
		$iken =
"自然保護団体が植林しろと抗議デモを行っています。";
	}
	elsif ( $island->{'kaitei'} > $HdisKLimit ) {
		$iken =
"海底系の建造物が多すぎます。シーいのらが出るかもしれません。";
	}
	if ( $island->{'area'} > $HdisFallBorder ) {
		$iken2 = "陸地面積が限界値を超えています。";
	}
	elsif ( $island->{'towerD'} > 1000 ) {
		$iken2 = "商業地が多すぎます。";
	}
	elsif ( $island->{'towerD'} > 0 ) {
		$iken2 = "住民が商業ビルを要望してます。";
	}
	elsif ( ( $island->{'kaiteipop'} == 1 ) && ( $island->{'area'} > 0 ) ) {
		$iken2 =
"海底人口過剰です。森かミサイル基地に怪獣がでるかも知れません。";
	}
	$moriw = 0 if ( $island->{'area'} == 0 );    # 陸が無い時

	if ( $po > 0 ) {
		$po = "${po}${HunitPop}";
	}
	elsif ( $po == 0 ) {
		$po = "増減無し";
	}
	else {

		# マイナス
		$island->{'score'} += -$po;
		$po = "${HtagDisaster_}${po}${HunitPop}${H_tagDisaster}";
	}
	if ( $mo > 0 ) {
		$mo = "${mo}${HunitMoney}";
	}
	elsif ( $mo == 0 ) {
		$mo = "増減無し";
	}
	else {
		$mo = "${HtagDisaster_}${mo}${HunitMoney}${H_tagDisaster}";
	}
	if ( $fo > 0 ) {
		$fo = "${fo}${HunitFood}";
	}
	elsif ( $fo == 0 ) {
		$fo = "増減無し";
	}
	else {
		$fo = "${HtagDisaster_}${fo}${HunitFood}${H_tagDisaster}";
	}
	my $wname = ( weatherinfo( $island->{'weather2'} ) )[1];

	# 収支の機密ログ
	push( @HsecretLogPool,
"1,$HislandTurn,$id,,人口<B>$po</B>、資金<B>$mo</B>、食糧<B>$fo</B>、処理した天気は<B>$wname</B>。${HtagDisaster_}${iken}${iken2}${H_tagDisaster}$iken3"
	);

	# 部門賞対象ターンだったら初期化する。
	if ( ( $HislandTurn % $HturnPrizeVarious ) == 0 ) {
		$island->{'status'} = 0;
		$island->{'score2'} = $island->{'score'};
		$island->{'score'}  = 0;
	}

	# 繁栄、災難賞
	$pop = $island->{'pop'};
	my ($damage) = $island->{'oldPop'} - $pop;
	my ($prize)  = $island->{'prize'};
	$prize =~ /([0-9]*),([0-9]*),(.*)/;
	my ( $flags, $monsters, $turns ) = ( $1, $2, $3 );

	# 繁栄賞
	if ( ( !( $flags & 1 ) ) && $pop >= 3000 ) {
		$flags |= 1;
		logPrize( $id, $name, $Hprize[1] );
		$island->{'present'}->[9]++;    # 博覧会を一つ増やす
		logEvent( $id, $name,
"で３０万人達成記念の博覧会が開催されることが決定しました。"
		);
	}
	elsif ( ( !( $flags & 2 ) ) && $pop >= 5000 ) {
		$flags |= 2;
		logPrize( $id, $name, $Hprize[2] );
		$island->{'present'}->[9]++;    # 博覧会を一つ増やす
		logEvent( $id, $name,
"で５０万人達成記念の博覧会が開催されることが決定しました。"
		);
	}
	elsif ( ( !( $flags & 4 ) ) && $pop >= 10000 ) {
		$flags |= 4;
		logPrize( $id, $name, $Hprize[3] );
		$island->{'present'}->[9]++;    # 博覧会を一つ増やす
		logEvent( $id, $name,
"で１００万人達成記念の博覧会が開催されることが決定しました。"
		);
	}
	elsif ( ( !( $flags & 1024 ) ) && $pop >= 15000 ) {
		$flags |= 1024;
		$island->{'present'}->[9]++;    # 博覧会を一つ増やす
		logEvent( $id, $name,
"で１５０万人達成記念の博覧会が開催されることが決定しました。"
		);
	}

	# 災難賞
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

	# 宇宙賞のログ
	logPrize( $id, $name, $Hprize[10] ) if ( $island->{'space'} == 1 );

	# 放棄のログ
	logGiveup( $id, $name ) if ( $island->{'giveup'} == 1 );

	$island->{'prize'} = "$flags,$monsters,$turns";
}    # doIslandProcess2

# 周囲の町、農場があるか判定
sub countGrow {
	my ( $land, $landValue, $x, $y ) = @_;
	my ( $i, $sx, $sy );
	for ( $i = 1 ; $i < 7 ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # 行による位置調整
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

# 究想いのら移動、または消去。
sub kinoraMove {
	my ( $island, $x, $y ) = @_;
	my ( $land, $landValue ) = ( $island->{'land'}, $island->{'landValue'} );
	my ( $i, $sx, $sy );
	for ( $i = 1 ; $i < 7 ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # 行による位置調整
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{
		}
		elsif ( $land->[$sx][$sy] == $HlandKInora ) {
			last
			  if ( ( bigMonsterSpec( $landValue->[$sx][$sy] ) )[3] == 0 )
			  ;                                     # 中心があったとき
		}
	}
	my ( $ld, $d ) = ( bigMonsterSpec( $landValue->[$x][$y] ) )[ 2, 3 ];
	if ( ( $d == 0 ) && ( $landValue->[$x][$y] > 0 ) ) {

# 移動
#	HdebugOut("究想いのら１($x,$y):" . $island->{'name'} . "島：" . $landValue->[$x][$y]);
		return if ( $monsterMove[$x][$y] == 2 );
		( $sx, $sy ) = monmove( $island, $x, $y, 0 );
		$monsterMove[$sx][$sy] = 2;
	}
	elsif ( ( $i > 6 ) || ( $landValue->[$x][$y] == 0 ) ) {

		# 消える

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

# 究想いのら作成
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

# 究想いのら消去
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

# 多用されるcountAround系処理を機能別に分別して負荷軽減
# 範囲内の地形をチェックする
sub chkAround {
	my ( $land, $x, $y, $kind, $range ) = @_;
	my ( $i, $sx, $sy );
	for ( $i = 0 ; $i < $range ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # 行による位置調整
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{

			# 範囲外の場合 海なら1
			return 1 if ( $kind == $HlandSea );
		}
		elsif ( $land->[$sx][$sy] == $kind ) {
			return 1;
		}
	}
	return 0;
}

# 範囲内の地形をチェックする $lv==0の時はchkAroundを使うように
sub chkAroundEX {
	my ( $land, $landValue, $x, $y, $kind, $lv, $range ) = @_;
	my ( $i, $sx, $sy );
	for ( $i = 0 ; $i < $range ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # 行による位置調整
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{

			# 範囲外の場合 海なら加算
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

# 範囲内の地形を数える

sub countAround {
	my ( $land, $x, $y, $kind, $range ) = @_;
	my ( $i, $sx, $sy );
	my $count = 0;
	for ( $i = 0 ; $i < $range ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # 行による位置調整
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{

			# 範囲外の場合 海なら加算
			$count++ if ( $kind == $HlandSea );
		}
		elsif ( $land->[$sx][$sy] == $kind ) {
			$count++;
		}
	}
	return $count;
}

# 範囲内の地形を数える拡張版 $lv==0の時はcountAroundを使うように
sub countAroundEX {
	my ( $land, $landValue, $x, $y, $kind, $lv, $range ) = @_;
	my ( $i, $sx, $sy );
	my $count = 0;
	for ( $i = 0 ; $i < $range ; $i++ ) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # 行による位置調整
		if (   ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) )
		{

			# 範囲外の場合 海なら加算
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

# 怪獣バトル成長率計算用
sub MonsterSei {
	my ( $type, @sup ) = @_;
	if ( $type == 1 ) {    #全て高い
		$sup[0]++;
		$sup[1]++;
		$sup[3]++;
		$sup[4]++;
	}
	elsif ( $type == 2 ) {    #低い
		$sup[0]--;
		$sup[1]--;
		$sup[3]--;
		$sup[4]--;
	}
	elsif ( $type == 3 ) {    #攻撃高い
		$sup[1]++;
	}
	elsif ( $type == 4 ) {    #守備高い
		$sup[2] = 2;
	}
	elsif ( $type == 5 ) {    #回命高い
		$sup[3]++;
		$sup[4]++;
	}
	return @sup;
}

# 船系出現位置
sub shipAppear {
	my ( $land, $direction ) = @_;
	my ( $sx, $sy, $size, $i );
	$size = $HislandSize - 1;

	if ( $direction == 0 ) {

		# 右上→右下
		$sx = $size;
		$sy = $size;
		for ( $i = 0 ; $i < $HislandSize ; $i++ ) {
			if ( $HseaChk[ $land->[$sx][$i] ] == 1 ) {

				# 海系地形の場合、船系は除く
				$sy = $i;
				last;
			}
		}
	}
	elsif ( $direction == 1 ) {

		# 右下→左下
		$sx = $size;
		$sy = $size;
		for ( $i = $size ; $i >= 0 ; $i-- ) {
			if ( $HseaChk[ $land->[$i][$sy] ] == 1 ) {

				# 海系地形の場合、船系は除く
				$sx = $i;
				last;
			}
		}
	}
	elsif ( $direction == 2 ) {

		# 左下→左上

		$sx = 0;
		$sy = $size;
		for ( $i = $size ; $i >= 0 ; $i-- ) {
			if ( $HseaChk[ $land->[$sx][$i] ] == 1 ) {

				# 海系地形の場合、船系は除く
				$sy = $i;
				last;
			}
		}
	}
	else {

		# 左上→右上

		$sx = $size;
		$sy = 0;
		for ( $i = 0 ; $i < $HislandSize ; $i++ ) {
			if ( $HseaChk[ $land->[$i][$sy] ] == 1 ) {

				# 海系地形の場合、船系は除く
				$sx = $i;
				last;
			}
		}
	}
	return ( $sx, $sy );
}

# 撤退処理(かなり強引なため真似しないように)
sub shipEvacuation {
	my ( $sx, $sy ) = @_;

	my ($center) = $HislandSize / 2 - 1;
	my (@direction);
	if ( ( $sx <= $center ) && ( $sy <= $center ) ) {

		# 左上

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

		# 右上

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

		# 左下
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

		# 右下
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

	# シャッフル

	my @new = ();
	for (@direction) {
		my $r = rand @new + 1;
		push( @new, $new[$r] );
		$new[$r] = $_;
	}

	return @new;
}

# 広域被害ルーチン(ログをまとめる予定)
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

		# 範囲による分岐

		if ( $i < 7 ) {

			# 中心、および1ヘックス
			if ( ( $landKind == $HlandSea ) && ( $lv == 0 ) ) {

				# 海
				$landValue->[$sx][$sy] = 0;
			}
			elsif ( $HseaChk[$landKind] ) {

				# 海系
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

				# 中心は海、他は浅瀬
				$landValue->[$sx][$sy] = ( $i == 0 ) ? 0 : 1;
			}
			next;
		}
		else {

			# 2ヘックス
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
			&logWideDamageOsen( $id, $name, "荒地", "($sx, $sy)" );
			$land->[$sx][$sy]      = $HlandOsen;
			$landValue->[$sx][$sy] = 1;
		}
	}
}

# 超広域被害ルーチン(ログをまとめる予定)
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

		# 範囲による分岐

		if ( $i == 0 ) {
			&logWideDamageSea2( $id, $name, landName( $landKind, $lv ),
				"($sx, $sy)" );
			$land->[$sx][$sy]      = $HlandMountain;
			$landValue->[$sx][$sy] = 0;
		}
		elsif ( $i < 7 ) {

			# 1ヘックス
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

			# 2ヘックス
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

			# 3ヘックス
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

# 広域被害宇宙ルーチン
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

			# 消滅
			logWideDamageSpace( landName( $landKind, $lv ),
				"($sx, $sy)", "虚無" );
			$land->[$sx][$sy]      = $HlandSea;
			$landValue->[$sx][$sy] = 0;
		}
		else {

			# 破壊
			if ( ( $landKind == $HlandSunit ) && ( $lv == 20 ) ) {
			}
			else {
				logWideDamageSpace( landName( $landKind, $lv ),
					"($sx, $sy)", "粉々" );
			}
			$land->[$sx][$sy]      = $HlandSunit;
			$landValue->[$sx][$sy] = 20;
		}
		$dis->[$sx][$sy]    = 0;
		$nation->[$sx][$sy] = 0;
	}
}

# ログをまとめる
sub logMatome {
	my ( $island, $flag, $kind ) = @_;
	my ( $sno, $m, $i, $sArray, $spnt, $x, $y, $z, $point );
	my @ptn = (
		"整地",                "埋め立て",
		"整地、埋め立て", "掘削",
		"整地、掘削",       "埋め立て、掘削",
		"整地、埋め立て、掘削"
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
				if ( $z eq '整地' ) {
					$point .= " 整($x, $y)";
					$m |= 1 unless ( $m & 1 );
				}
				elsif ( $z eq '埋め立て' ) {
					$point .= " 埋($x, $y)";
					$m |= 2 unless ( $m & 2 );
				}
				elsif ( $z eq '掘削' ) {
					$point .= " 掘($x, $y)";
					$m |= 4 unless ( $m & 4 );
				}
				else {
					$point .= "($x, $y)";
				}
				$point .= "<br>　　　" unless ( ( $i + 1 ) % 20 );
			}
		}
		$point .= "の<B>$snoケ所</B>" if ( $i > 1 || $flag != 1 );
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

# ログへの出力
# 第1引数:メッセージ
# 第2引数:当事者
# 第3引数:相手

# 通常ログ
sub logOut {
	push( @HlogPool, "0,$HislandTurn,$_[1],$_[2],$_[0]" );
}

# 遅延ログ
sub logLate {
	push( @HlateLogPool, "0,$HislandTurn,$_[1],$_[2],$_[0]" );
}

# 機密ログ
sub logSecret {
	push( @HsecretLogPool, "1,$HislandTurn,$_[1],$_[2],$_[0]" );
}

# 天気ログ
sub logWeather {
	open( HOUT, ">>${HlogdirName}/weather.his" );
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# 記録ログ
sub logHistory {
	open( HOUT, ">>${HlogdirName}/hakojima.his" );
	print HOUT "$HislandTurn,$_[0]\n";
	close(HOUT);
}

# 記録ログ調整
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

# ログ書き出し
sub logFlush {
	open( LOUT, ">${HlogdirName}/hakojima.log0" );

	# 全部逆順にして書き出す
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
# ログテンプレート
#----------------------------------------------------------------------

# ダミー命令
sub logDummy {
	my ( $id, $name, $comName, $point ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}$point${H_tagName}の${HtagComName_}${comName}${H_tagComName}はダミー命令です。",
		$id
	);
}

# コマンド失敗
sub logMiss {
	logOut(
"${HtagName_}$_[1]$AfterName${H_tagName}で予定されていた${HtagComName_}$_[2]${H_tagComName}は、$_[3]ため中止されました。",
		$_[0]
	);
}

# コマンド失敗(宇宙)
sub logMissS {
	logOut(
"${HtagName_}${SpaceName}$_[3]${H_tagName}で予定されていた${HtagComName_}$_[2]${H_tagComName}は、$_[4]ため中止されました。",
		$_[0]
	);
}

# コマンド失敗２(宇宙)
sub logMissS2 {
	logOut(
"${HtagName_}${SpaceName}$_[3]${H_tagName}で予定されていた${HtagComName_}$_[2]${H_tagComName}は、$_[4]ため失敗しました。",
		$_[0], 999
	);
}

# 対象地形の種類による失敗
sub logLandFail {
	my ( $id, $name, $comName, $landName, $point, $landKind, $lv ) = @_;
	if ( $landKind == $HlandGhostShip ) {

		# 幽霊船は海に擬装
		$landName = '海';
	}
	elsif ( $landKind == $HlandMonster ) {

		# 迷彩いのら
		if ( ( monsterSpec($lv) )[0] == 26 ) {
			$landName = '荒地';
		}
	}
	logOut(
"${HtagName_}$name${AfterName}${H_tagName}で予定されていた${HtagComName_}$comName${H_tagComName}は、予定地の${HtagName_}$point${H_tagName}が<B>$landName</B>だったため中止されました。",
		$id
	);
}

# 周りに海か陸がなくて埋め立て失敗
sub logNoLandAround {
	logOut(
"${HtagName_}$_[1]${AfterName}${H_tagName}で予定されていた${HtagComName_}$_[2]${H_tagComName}は、予定地の${HtagName_}$_[4]${H_tagName}の周辺に$_[3]がなかったため中止されました。",
		$_[0]
	);
}

# 港閉鎖
sub logClosedPort {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>は閉鎖したようです。",
		$id
	);
}

# 整地系成功
sub logLandSuc {
	my ( $id, $name, $comName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",
		$id
	);
}

# 整地系ログまとめ
sub logLandSucMatome {
	my ( $id, $name, $comName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。<br>　　<B>⇒</B> $point",
		$id
	);
}

# 整地系(宇宙)成功
sub logLandSucS {
	my ( $id, $name, $comName, $point ) = @_;
	logOut(
"${HtagName_}${SpaceName}${point}${H_tagName}で${HtagName_}$name$AfterName${H_tagName}による${HtagComName_}${comName}${H_tagComName}が行われました。",
		$id, 999
	);
}

# プレゼント失敗
sub logNoPresent {
	my ( $id, $name, $comName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}は該当のプレゼントが無い為、中止されました。",
		$id
	);
}

# プレゼント援助
sub logPresent {
	my ( $id, $tId, $name, $tName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}がプレゼントを${HtagName_}${tName}${AfterName}${H_tagName}へ譲渡しました。",
		$id, $tId
	);
}

# 森の自動伐採
sub logAutoTree {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}の<B>森</B>を${HtagComName_}伐採${H_tagComName}、新たに${HtagComName_}植林${H_tagComName}しました。",
		$id
	);
}

# 調査系ログ
sub logChosa {
	logOut(
"${HtagName_}$_[1]${AfterName}$_[2]${H_tagName}で<B>$_[4]</B>の予算をつぎ込んだ${HtagComName_}$_[3]${H_tagComName}が行われ$_[5]した。",
		$_[0]
	);
}

# 油田からの収入
sub logOilMoney {
	my ( $id, $name, $lName, $point, $value ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>から、<B>$value$HunitMoney</B>の収益が上がりました。",
		$id
	);

	#ランキング用ログファイル書き出し
	open( MOUT, ">>${HlogdirName}/money.log" );
	print MOUT "$HislandTurn,$id,温泉,$value\n";
	close(MOUT);
}

# 油田枯渇
sub logOilEnd {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>は枯渇したようです。",
		$id
	);
}

# 防衛施設、自爆セット
sub logBombSet {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>の<B>自爆装置がセット</B>されました。",
		$id
	);
}

# 防衛施設、自爆作動
sub logBombFire {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>、${HtagDisaster_}自爆装置作動！！${H_tagDisaster}",
		$id
	);
}

# 記念碑、発射
sub logMonFly {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>が<B>轟音とともに飛び立ちました</B>。",
		$id
	);
}

# 記念碑、落下
sub logMonDamage {
	my ( $id, $name, $point ) = @_;
	logOut(
"<B>何かとてつもないもの</B>が${HtagName_}${name}${AfterName}$point${H_tagName}地点に落下しました！！",
		$id
	);
}

# 植林orミサイル基地
sub logPBSuc {
	my ( $id, $name, $comName, $point ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",
		$id
	);
	logOut(
"こころなしか、${HtagName_}${name}${AfterName}${H_tagName}の<B>森</B>が増えたようです。",
		$id
	);
}

# ハリボテ
sub logHariSuc {
	my ( $id, $name, $comName, $comName2, $point ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}$point${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",
		$id
	);
	logLandSuc( $id, $name, $comName2, $point );
}

# ロケット打ち上げ失敗
sub logRocketF {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagComName_}ロケット${H_tagComName}を打ち上げましたが、<B>失敗</B>しました。",
		$id
	);
}

# ロケット打ち上げ成功

sub logRocketS {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagComName_}ロケット${H_tagComName}を打ち上げ、みごと<B>成功</B>しました。",
		$id
	);
}

# 謀略失敗
sub logSpyF {
	my ( $id, $tId, $name, $tName, $comName ) = @_;
	logLate(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${AfterName}${H_tagName}に${HtagComName_}$comName${H_tagComName}をしましたが、失敗して捕らえられました。",
		$id, $tId
	);
}

# 基地発見
sub logBeseFind {
	my ( $id, $tName, $tPoint, $tLv, $tLname ) = @_;
	logSecret(
"${HtagName_}${tName}${AfterName}$tPoint${H_tagName}地点で経験値<B>$tLv</B>の<B>$tLname</B>発見！！",
		$id
	);
}

# 防衛施設判別
sub logLandTruth {
	my ( $id, $tName, $tPoint, $tLname, $truth ) = @_;
	logSecret(
"${HtagName_}${tName}${AfterName}$tPoint${H_tagName}地点の<B>$tLname</B>はどうやら<B>$truth</B>のようです。",
		$id
	);
}

# 隕石転移装置に落ちる
sub logWarpMeteo {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"<B>隕石</B>が${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>へ落下、<B>時空の狭間に吸い込まれました！！</B>",
		$id
	);
}

# 怪獣、国連に成敗される。
sub logUNMons {
	my ( $id, $name, $mName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>怪獣$mName</B>は国連軍によって成敗され荒地になりました。",
		$id
	);
}

# 怪獣、転移装置を踏む
sub logWarpMons {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"<B>$mName</B>が${HtagName_}${name}${AfterName}$point${H_tagName}の<B>${lName}</B>へ到達、<B>時空の狭間に吸い込まれました！！</B>",
		$id
	);
}

# 怪獣、転移失敗
sub logWarpMonsMiss {
	my ( $id, $name, $point, $mName ) = @_;
	logOut(
"転送したはずの<B>$mName</B>が${HtagName_}${name}${AfterName}$point${H_tagName}に<B>再び舞い戻ってきました！！</B>",
		$id
	);
}

# 怪獣、隕石、ミサイル転移
sub logMWarp {
	my ( $id, $tId, $Name, $tName, $point, $lName ) = @_;
	logOut(
"${HtagName_}${tName}${AfterName}$point${H_tagName}地点の空間が歪み、突然<B>${lName}</B>が出現しました。どうやら${HtagName_}${Name}${AfterName}${H_tagName}産のようです。",
		$id, $tId
	);
}

# ミサイル撃とうとした(or 怪獣派遣しようとした)がターゲットがいない
sub logMsNoTarget {
	my ( $id, $name, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、目標の${AfterName}に人が見当たらないため中止されました。",
		$id
	);
}

# ミサイル撃とうとした(or 怪獣派遣しようとした)が国連にとめられた
sub logUNMiss {
	my ( $id, $tId, $name, $tName, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で予定されていた${HtagComName_}${comName}${H_tagComName}は、目標の${HtagName_}${tName}${AfterName}${H_tagName}が国連保護期間ため中止されました。",
		$id, $tId
	);
}

# 防衛施設進化
sub logDefenceS {
	my ( $id, $tId, $tName, $tLname, $tPoint ) = @_;
	logOut(
"--- ${HtagName_}$tPoint${H_tagName}の<B>${tLname}</B>はS${tLname}に発展しました。",
		$id, $tId
	);
}

# 防衛施設ダウン

sub logDefenceD {
	my ( $id, $tId, $tName, $tLname, $tPoint ) = @_;
	logOut(
"--- ${HtagName_}$tPoint${H_tagName}の<B>S${tLname}</B>は${tLname}にレベルダウンしました。",
		$id, $tId
	);
}

# ミサイル発射数など表示
sub logMissile {
	logOut(
"${HtagName_}$_[2]${AfterName}${H_tagName}が${HtagName_}$_[3]${AfterName}$_[5]${H_tagName}地点に向けて<b>$_[6]発</b>の${HtagComName_}$_[4]${H_tagComName}を行いました。(命中$_[7]、無害$_[8]、天候$_[9]、防衛$_[10])",
		$_[0], $_[1]
	);
}

sub logMissileS {
	logSecret(
"${HtagName_}$_[2]${AfterName}${H_tagName}が${HtagName_}$_[3]${AfterName}$_[5]${H_tagName}地点に向けて<b>$_[6]発</b>の${HtagComName_}$_[4]${H_tagComName}を行いました。(命中$_[7]、無害$_[8]、天候$_[9]、防衛$_[10])",
		$_[0], $_[1]
	);
	logLate(
"<B>何者か</B>が${HtagName_}$_[3]${AfterName}$_[5]${H_tagName}地点に向けて<b>$_[6]発</b>の${HtagComName_}$_[4]${H_tagComName}を行いました。(命中$_[7]、無害$_[8]、天候$_[9]、防衛$_[10])",
		$_[1]
	);
}

# 通常ミサイル通常地形に命中
sub logMsNormal {
	logOut(
"--- ${HtagName_}$_[3]${H_tagName}の<B>$_[2]</B>に命中、一帯が$_[4]ました。",
		$_[0], $_[1]
	);
}

# ステルスミサイル通常地形に命中
sub logMsNormalS {
	my ( $id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $result )
	  = @_;
	logSecret(
"--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が$resultました。",
		$id, $tId
	);
	logLate(
"<B>何者か</B>が${HtagName_}${tName}${AfterName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中、一帯が${result}ました。",
		$tId
	);
}

# ステルスミサイル防衛施設で判明
sub logMsCaughtH {
	my ( $tId, $name, $comName ) = @_;
	logSecret(
"防いだ${HtagComName_}${comName}${H_tagComName}を撃った島は、${HtagName_}${name}${AfterName}${H_tagName}のようです。",
		$tId
	);
}

# バイオミサイル
sub logBioMs {
	logOut(
"--- ${HtagName_}$_[3]${H_tagName}の<B>$_[2]</B>に落ち、一帯が<B>汚染</B>しました。",
		$_[0], $_[1]
	);
}

# 陸地破壊弾命中
sub logMsLD {
	logOut( "--- ${HtagName_}$_[2]${H_tagName}$_[3]ました。", $_[0],
		$_[1] );
}

# 通常ミサイル、怪獣に命中、硬化中にて無傷
sub logMsMonNoDamage {
	logOut(
"--- ${HtagName_}$_[3]${H_tagName}の<B>怪獣$_[2]</B>に命中、しかし硬化状態だったため効果がありませんでした。",
		$_[0], $_[1]
	);
}

# ステルスミサイル、怪獣に命中、硬化中にて無傷
sub logMsMonNoDamageS {
	my ( $id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${AfterName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中、しかし硬化状態だったため効果がありませんでした。",
		$id, $tId
	);
	logLate(
"<B>何者か</B>が${HtagName_}${tName}${AfterName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中、しかし硬化状態だったため効果がありませんでした。",
		$tId
	);
}

# 通常ミサイル、怪獣に命中、殺傷
sub logMsMonKill {
	my ( $id, $tId, $name, $tName, $tLname, $tPoint ) = @_;
	logOut(
"--- ${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は力尽き、倒れました。",
		$id, $tId
	);

	#ランキング用ログファイル書き出し
	open( ROUT, ">>${HlogdirName}/ranking.log" );
	print ROUT "$HislandTurn,$id,$tId,$tLname\n";
	close(ROUT);
}

# ステルスミサイル、怪獣に命中、殺傷
sub logMsMonKillS {
	my ( $id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${AfterName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は力尽き、倒れました。",
		$id, $tId
	);
	logLate(
"<B>何者か</B>が${HtagName_}${tName}${AfterName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は力尽き、倒れました。",
		$tId
	);
}

# 通常ミサイル、怪獣に命中、ダメージ
sub logMsMonster {
	logOut(
"--- ${HtagName_}$_[3]${H_tagName}の<B>怪獣$_[2]</B>に命中。<B>怪獣$_[2]</B>は苦しそうに咆哮しました。",
		$_[0], $_[1]
	);
}

# ステルスミサイル、怪獣に命中、ダメージ
sub logMsMonsterS {
	my ( $id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${AfterName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は苦しそうに咆哮しました。",
		$id, $tId
	);
	logLate(
"<B>何者か</B>が${HtagName_}${tName}${AfterName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は苦しそうに咆哮しました。",
		$tId
	);
}

# ミサイル地形に命中(宇宙、海域)
sub logMsSpace {
	logOut(
"--- ${HtagName_}$_[1]${H_tagName}の<B>$_[2]</B>に命中、一帯が$_[3]ました。",
		$_[0], $_[4]
	);
}

# ミサイル地形に命中(海域)
sub logMsOPlayer {
	logOut(
"--- ${HtagName_}$_[1]${H_tagName}の<B>$_[2]</B>付近に落下、破片が降り注いだ模様。",
		$_[0], $_[3]
	);
}

# ミサイル怪獣に命中(宇宙、海域)
sub logMsMonSpace {
	logOut(
"--- ${HtagName_}$_[1]${H_tagName}の<B>怪獣$_[2]</B>に命中、<B>怪獣$_[2]</B>は苦しそうに咆哮しました。",
		$_[0], $_[3]
	);
}

# ミサイル、怪獣に命中、殺傷(宇宙、海域)
sub logMsMonKillSpace {
	logOut(
"--- ${HtagName_}$_[2]${H_tagName}の<B>怪獣$_[3]</B>に命中、<B>怪獣$_[3]</B>は力尽き、倒れました。",
		$_[0], $_[4]
	);

	#ランキング用ログファイル書き出し
	open( ROUT, ">>${HlogdirName}/ranking.log" );
	print ROUT "$HislandTurn,$_[0],$_[4],$_[3]\n";
	close(ROUT);
}

# ミサイル発射数など表示(宇宙、海域)
sub logMissileSpace {
	logOut(
"${HtagName_}$_[1]${AfterName}${H_tagName}が${HtagName_}$_[9]$_[3]${H_tagName}地点に向けて<b>$_[4]発</b>の${HtagComName_}$_[2]${H_tagComName}を行いました。(命中$_[5]、無害$_[6]、失敗$_[7]、防衛$_[8])",
		$_[0], $_[10]
	);
}

# 怪獣の死体
sub logMsMonMoney {
	my ( $tId, $mName, $value ) = @_;
	logOut(
"<B>怪獣$mName</B>の残骸には、<B>$value$HunitMoney</B>の値が付きました。",
		$tId
	);

	#ランキング用ログファイル書き出し
	open( MOUT, ">>${HlogdirName}/money.log" );
	print MOUT "$HislandTurn,$tId,怪獣撃破,$value\n";
	close(MOUT);
}

# ミサイル命令中止
sub logMsMiss {
	logOut(
"${HtagName_}$_[1]$AfterName${H_tagName}で予定されていた${HtagComName_}$_[2]${H_tagComName}は、ミサイル設備を保有していない、あるいはそれらが稼動できない状況のため中止されました。",
		$_[0]
	);
}

# 怪獣、成仏できない
sub logMonsRei {
	logOut(
"--- ${HtagName_}$_[3]${H_tagName}の<B>怪獣$_[2]</B>に命中。<B>怪獣$_[2]</B>は力尽きましたが、成仏できずに<B>ジバクレイ</B>になりました。",
		$_[0], $_[1]
	);
}

# 怪獣、純金の碑
sub logMonsGold {
	my ( $id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${AfterName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>怪獣$tLname</B>に命中。<B>怪獣$tLname</B>は力尽きました。そのときの残骸で<B>純金の碑</B>が造られました。",
		$id, $tId
	);

	#ランキング用ログファイル書き出し
	open( ROUT, ">>${HlogdirName}/ranking.log" );
	print ROUT "$HislandTurn,$id,$tId,$tLname\n";
	close(ROUT);
}

# 怪獣、反撃
sub logMonsCounter {
	logOut(
"--- ${HtagName_}$_[3]${H_tagName}の<B>怪獣$_[2]</B>に命中。しかし効果が無いばかりか仕返しに宇宙から$_[4]",
		$_[0], $_[1]
	);
}

# ミサイル難民到着
sub logMsBoatPeople {
	my ( $id, $name, $achive ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}にどこからともなく<B>$achive${HunitPop}もの難民</B>が漂着しました。${HtagName_}${name}${AfterName}${H_tagName}は快く受け入れたようです。",
		$id
	);
}

# 銀行命中
sub logMsBank {
	my ( $id, $name, $bank ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}にどこからともなく<B>$bank${HunitMoney}ものお金</B>が漂着しました。${HtagName_}${name}${AfterName}${H_tagName}は快く受けとったようです。",
		$id
	);
}

#--------怪獣バトル-------------
# 中止全般
sub logMonsCancel {
	my ( $id, $name, $comName, $Result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}の${HtagComName_}${comName}${H_tagComName}は、${Result}ため中止されました。",
		$id
	);
}

# 怪獣エッグ
sub logMonsEGG {
	my ( $id, $name, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で${HtagComName_}${comName}${H_tagComName}を行い怪獣いのらが誕生しました。",
		$id
	);
}

# 怪獣売却
sub logMonsSell {
	my ( $id, $name, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で${HtagComName_}${comName}${H_tagComName}を行い、怪獣はいなくなりました。",
		$id
	);
}

# 怪獣模擬訓練
sub logMonsExer {
	my ( $id, $name, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で餌を使った${HtagComName_}${comName}${H_tagComName}を行い、餌がなくなりました。",
		$id
	);
}

# 怪獣遠征
sub logMonsENSEI {
	my ( $id, $name, $tId, $tName, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で${HtagComName_}${comName}${H_tagComName}を行い${HtagName_}${tName}${AfterName}${H_tagName}に出撃しました。",
		$id, $tId
	);
}

# 餌ストック
sub logMonsESA {
	my ( $id, $name, $mName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}は、<B>怪獣$mName</B>を餌としてストックしました。",
		$id
	);
}

# 餌譲渡
sub logMonsEsaAid {
	my ( $id, $name, $tId, $tName, $mName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}は、${HtagName_}${tName}${AfterName}${H_tagName}に<B>怪獣$mName</B>を餌として譲渡しました。",
		$id, $tId
	);
}

# 怪獣譲渡
sub logMonsAid {
	my ( $id, $name, $tId, $tName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}は、${HtagName_}${tName}${AfterName}${H_tagName}に怪獣を譲渡しました。",
		$id, $tId
	);
}

# 怪獣進化
sub logMonsEvo {
	my ( $id, $name, $mName, $mNameE, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で${HtagComName_}${comName}${H_tagComName}を行い<B>怪獣$mName</B>の元怪獣が<B>怪獣$mNameE</B>に突然変異しました。",
		$id
	);
}

# 怪獣進化失敗
sub logMonsEvoF {
	my ( $id, $name, $mName, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で${HtagComName_}${comName}${H_tagComName}を行いましたが、何も変化がありませんでした。",
		$id
	);
}

# 怪獣攻撃
sub logMonsATTACK {
	my ( $id, $name, $mName, $tId, $tName, $tmName, $Result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}の<B>怪獣$mName</B>が${HtagName_}${tName}${AfterName}${H_tagName}の<B>怪獣$tmName</B>に<B>${Result}</B>",
		$id, $tId
	);
}

# 両者は間をとった
sub logMonsNOATTACK {
	my ( $id, $name, $mName, $tId, $tName, $tmName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}の<B>怪獣$mName</B>と${HtagName_}${tName}${AfterName}${H_tagName}の<B>怪獣$tmName</B>は、両者間をとり動きませんでした。",
		$id, $tId
	);
}

# 怪獣回復
sub logMonsRrcovery {
	my ( $id, $name, $mName, $tId, $P ) = @_;
	if ( $P > 0 ) {
		logOut(
"${HtagName_}${name}${AfterName}${H_tagName}の<B>怪獣$mName</B>は、精神を集中し<B>${P}</B>ポイント自己回復しました。",
			$id, $tId
		);
	}
}

# 怪獣バトル終了
sub logMonsEND {
	my ( $id, $name, $mName, $tId, $Result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}の<B>怪獣$mName</B>は、<B>${Result}</B>",
		$id, $tId
	);
}

#-----------船系ログ---------------
# 保有島が存在しない為遭難
sub logShipWreck {
	my ( $id, $name, $tLname, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}地点の<B>$tLname</B>は、保有島が存在しない為遭難しました。",
		$id
	);
}

# 海賊、国連に成敗される。
sub logUNShip {
	my ( $id, $name, $mName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}地点の<B>$mName</B>は、国連軍によって成敗されました。",
		$id
	);
}

# 通常ミサイル、船に命中、ダメージ、沈没
sub logMsShip {
	my ( $id, $tId, $tLname, $tPoint, $tL, $result ) = @_;
	logOut(
"--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は$result",
		$id, $tId
	);

	#ランキング用ログファイル書き出し
	$tL -= $HlandPirate;
	open( ROUT, ">>${HlogdirName}/ship.log" );
	print ROUT "$HislandTurn,$id,99,$tL\n";
	close(ROUT);
}

# 通常ミサイル、船に命中、ダメージ
sub logMsShipD {
	my ( $id, $tId, $tLname, $tPoint, $tL, $result ) = @_;
	logOut(
"--- ${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は$result",
		$id, $tId
	);
}

# ステルスミサイル、船に命中、ダメージ、沈没
sub logMsShipS {
	my ( $id, $tId, $name, $tName, $comName, $tLname, $point, $tPoint, $result )
	  = @_;
	logSecret(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${AfterName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は$result",
		$id, $tId
	);
	logLate(
"<B>何者か</B>が${HtagName_}${tName}${AfterName}$point${H_tagName}地点に向けて${HtagComName_}${comName}${H_tagComName}を行い、${HtagName_}$tPoint${H_tagName}の<B>$tLname</B>に命中。<B>$tLname</B>は$result",
		$tId
	);
}

# 船動く
sub logShipMove {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>付近に<B>$mName</B>が移動しました。",
		$id
	);
}

# 船略奪
sub logShipPlunder {
	my ( $id, $tId, $name, $lName, $point, $mName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>付近に<B>$mName</B>が移動しました。その際に略奪を行い<B>$lName</B>は破壊されました。",
		$id, $tId
	);
}

# 船指令変更
sub logShipOrderC {
	my ( $id, $name, $lName, $point, $result ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>の指令を<B>$result</B>に変更しました。",
		$id
	);
}

# 船現る
sub logShipCome {
	my ( $id, $name, $mName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${point}${H_tagName}に<B>$mName</B>出現！！",
		$id
	);
}

# 船生還
sub logShipComeIs {
	my ( $id, $name, $mName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${point}${H_tagName}に<B>$mName</B>が、帰ってきました！！",
		$id
	);
}

# 船消える
sub logShipDis {
	my ( $id, $name, $mName, $point, $result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${point}${H_tagName}の<B>$mName</B>${result}ました。",
		$id
	);
}

# 船デストラップを踏む
sub logShipMoveDeathtrap {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"<B>$mName</B>が${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>へ到達、<B>${lName}</B>が作動し<B>$mName</B>は撃沈しました！！",
		$id
	);
}

#-----------ここまで---------------

# 資金繰り
sub logDoNothing {
	my ( $id, $name, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",
		$id
	);
}

# 売却
sub logSell {
	my ( $id, $name, $comName, $value ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}が<B>$value</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",
		$id
	);
}

# 援助
sub logAid {
	my ( $id, $tId, $name, $tName, $comName, $str ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${H_tagName}へ<B>$str</B>の${HtagComName_}${comName}${H_tagComName}を行いました。",
		$id, $tId
	);
}

# 移民到着
sub logRefugees {
	my ( $id, $tId, $name, $tName, $achive ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${AfterName}${H_tagName}に<B>$achive${HunitPop}もの移民</B>を送りこみました。",
		$id, $tId
	);
}

# 誘致活動
sub logPropaganda {
	my ( $id, $name, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で${HtagComName_}${comName}${H_tagComName}が行われました。",
		$id
	);
}

# 放棄
sub logGiveup {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}は放棄され、<B>無人${AfterName}</B>になりました。",
		$id
	);
	logHistory(
"${HtagName_}${name}${AfterName}${H_tagName}、放棄され<B>無人${AfterName}</B>となる。"
	);
}

# 死滅
sub logDead {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}から人がいなくなり、<B>無人${AfterName}</B>になりました。",
		$id
	);
	logHistory(
"${HtagName_}${name}${AfterName}${H_tagName}、人がいなくなり<B>無人${AfterName}</B>となる。"
	);
}

# 死滅２
sub logDead2 {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}は、特別ルールにより、<B>沈没${AfterName}</B>しました。",
		$id
	);
	logHistory(
"${HtagName_}${name}${AfterName}${H_tagName}、特別ルールにより<B>沈没${AfterName}</B>となる。"
	);
}

# 飢餓
sub logStarve {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}の${HtagDisaster_}食料が不足${H_tagDisaster}しています！！",
		$id
	);
}

#---------怪獣関係のログ---------

# 怪獣現る
sub logMonsCome {
	my ( $id, $name, $mName, $point, $lName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}に<B>怪獣$mName</B>出現！！${HtagName_}$point${H_tagName}の<B>$lName</B>が踏み荒らされました。",
		$id
	);
}

# 怪獣現る(宇宙)
sub logMonsComeSpace {
	my ( $mName, $point, $lName ) = @_;
	logOut(
"${HtagName_}${SpaceName}${H_tagName}に<B>怪獣$mName</B>出現！！${HtagName_}$point${H_tagName}の<B>$lName</B>が跡形も無く破壊されました。",
		999
	);
}

# 怪獣現る(海域)
sub logMonsComeOcean {
	my ( $mName, $point, $lName ) = @_;
	logOut(
"${HtagName_}${OceanName}${H_tagName}に<B>怪獣$mName</B>出現！！${HtagName_}$point${H_tagName}の<B>$lName</B>が跡形も無く破壊されました。",
		888
	);
}

# 怪獣島に特攻(海域)
sub logMonsMoveOcean {
	my ( $tId, $lName, $point, $mName ) = @_;
	logOut(
"<B>怪獣$mName</B>が${HtagName_}${OceanName}$point${H_tagName}の<B>$lName</B>へ特攻しました。",
		888, $tId
	);
}

# 怪獣動く(宇宙、海域)
sub logMonsMoveSpace {
	logOut(
"${HtagName_}$_[2]$_[0]${H_tagName}の<B>$_[3]</B>が<B>怪獣$_[1]</B>に跡形も無く破壊されました。",
		$_[4]
	);
}

# 怪獣動く２(宇宙、海域)
sub logMonsMoveSpace2 {
	logOut(
"${HtagName_}$_[2]$_[0]${H_tagName}に<B>怪獣$_[1]</B>が移動しました。",
		$_[3]
	);
}

# 怪獣、防衛施設を踏む(宇宙)
sub logMonsMoveDefenceS {
	my ( $lName, $point, $mName ) = @_;
	logOut(
"<B>怪獣$mName</B>が${HtagName_}${SpaceName}$point${H_tagName}の<B>$lName</B>へ到達、<B>${lName}の自爆装置が作動！！</B>",
		999
	);
}

# 怪獣地球に特攻(宇宙)
sub logMonsMoveEarth {
	my ( $lName, $point, $mName ) = @_;
	logOut(
"<B>怪獣$mName</B>が${HtagName_}${SpaceName}$point${H_tagName}の<B>$lName</B>の引力に引きずり込まれ跡形も無く消え去りました。",
		999
	);
}

# 怪獣動く
sub logMonsMove {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>が<B>怪獣$mName</B>に踏み荒らされました。",
		$id
	);
}

# 怪獣金落とす
sub logMonsMoney {
	my ( $id, $name, $lName, $point, $mName, $result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>が<B>怪獣$mName</B>に踏み荒らされましたが、<B>$result</B>を落としました。",
		$id
	);
}

# 怪獣まとめたログ
sub logMonster {
	my ( $id, $name, $point, $mName, $result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>怪獣$mName</B>${result}",
		$id
	);
}

# 怪獣派遣
sub logMonsSend {
	my ( $id, $tId, $name, $tName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}が<B>人造怪獣</B>を建造。${HtagName_}${tName}${AfterName}${H_tagName}へ送りこみました。",
		$id, $tId
	);
}

# 怪獣突然変異
sub logMonsC {
	my ( $id, $name, $point, $mName, $afmName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>怪獣$mName</B>が汚染の影響で<B>怪獣$afmName</B>に突然変異しました。",
		$id
	);
}

# 怪獣、防衛施設を踏む
sub logMonsMoveDefence {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"<B>怪獣$mName</B>が${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>へ到達、<B>${lName}の自爆装置が作動！！</B>",
		$id
	);
}

# 怪獣、デストラップを踏む
sub logMonsMoveDeathtrap {
	my ( $id, $name, $lName, $point, $mName, $result ) = @_;
	logOut(
"<B>怪獣$mName</B>が${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>へ到達、<B>${lName}</B>が作動し<B>怪獣$mName</B>は${result}ました！！",
		$id
	);
}

# 怪獣、デストラップを踏む効果なし
sub logMonsMoveDeathtrapM {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"<B>怪獣$mName</B>が${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>へ到達、<B>${lName}</B>が作動しましたが<B>怪獣$mName</B>は何事も無かったように踏み荒らしました！！",
		$id
	);
}

# 怪獣、自爆
sub logMonsZIBAKU {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"<B>怪獣$mName</B>が${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>へ移動した際、突然膨れたかと思うと一気に<B>爆発しました！！</B>",
		$id
	);
}

# 怪獣、食料を食う
sub logMonsEAT {
	my ( $id, $name, $lName, $point, $mName ) = @_;
	logOut(
"<B>怪獣$mName</B>が${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>へ移動した際、恐ろしいほどの吸引力で島の備蓄食料の５％を吸い込み食べてしまいました。",
		$id
	);
}

# 怪獣操る
sub logManipulate {
	my ( $id, $tId, $name, $tName, $comName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${AfterName}${H_tagName}で${HtagComName_}${comName}${H_tagComName}を行いました。",
		$id, $tId
	);
}

# 怪獣操る ステルス
sub logManipulateS {
	my ( $id, $tId, $name, $tName, $comName ) = @_;
	logSecret(
"${HtagName_}${name}${AfterName}${H_tagName}が${HtagName_}${tName}${AfterName}${H_tagName}で${HtagComName_}${comName}${H_tagComName}を行いました。",
		$id, $tId
	);
	logLate(
"<B>何者か</B>が${HtagName_}${tName}${AfterName}${H_tagName}で${HtagComName_}${comName}${H_tagComName}を行っているようです。",
		$tId
	);
}

#-----------ここまで---------------

# 火災
sub logFire {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>が${HtagDisaster_}火災${H_tagDisaster}により壊滅しました。",
		$id
	);
}

# 火災を未然に防ぐ
sub logFireD {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>で出火しましたが、消防隊員の活躍により火災は未然に防ぎました。",
		$id
	);
}

# 汚染
sub logOsen {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>が${HtagDisaster_}汚染${H_tagDisaster}され壊滅しました。",
		$id
	);
}

# スラム街
sub logslum {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>が貧困により${HtagDisaster_}スラム街${H_tagDisaster}に変化しました。",
		$id
	);
}

# 埋蔵金

sub logMaizo {
	my ( $id, $name, $comName, $value ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}での${HtagComName_}$comName${H_tagComName}中に、<B>$value$HunitMoneyもの埋蔵金</B>が発見されました。",
		$id
	);

	#ランキング用ログファイル書き出し
	open( MOUT, ">>${HlogdirName}/money.log" );
	print MOUT "$HislandTurn,$id,埋蔵金,$value\n";
	close(MOUT);
}

# 金鉱脈
sub logGold {
	my ( $id, $name, $comName, $value ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}での${HtagComName_}$comName${H_tagComName}中に金鉱脈発見、<B>$value$HunitMoney相当の金</B>が採掘されました。",
		$id
	);

	#ランキング用ログファイル書き出し
	open( MOUT, ">>${HlogdirName}/money.log" );
	print MOUT "$HislandTurn,$id,埋蔵金,$value\n";
	close(MOUT);
}

# 純金の碑

sub logGoldMonu {
	my ( $id, $name, $lName, $arg ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}の<B>$lName</B>から、<B>${arg}億</B>の金が削り取られました。",
		$id
	);
}

# 地震発生
sub logEarthquake {
	my ( $id, $name, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で大規模な${HtagDisaster_}地震${H_tagDisaster}が発生！！震源は${HtagName_}$point${H_tagName}付近の模様。",
		$id
	);
}

# 地震被害
sub logEQDamage {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}地震${H_tagDisaster}により被害を受けました。",
		$id
	);
}

# 地震壊滅
sub logEQDestroy {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}島$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}地震${H_tagDisaster}により壊滅しました。",
		$id
	);
}

# 食料不足被害
sub logSvDamage {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>に<B>食料を求めて住民が殺到</B>。<B>$lName</B>は壊滅しました。",
		$id
	);
}

# 津波崩壊
sub logTsunamiDamage {
	my ( $id, $name, $lName, $point, $result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}津波${H_tagDisaster}により$resultました。",
		$id
	);
}

# 台風発生
sub logTyphoon {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}に${HtagDisaster_}台風${H_tagDisaster}上陸！！",
		$id
	);
}

# 台風被害
sub logTyphoonDamage {
	my ( $id, $name, $lName, $point, $result ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}台風${H_tagDisaster}で${result}ました。",
		$id
	);
}

# 赤潮被害
sub logAkasioDamage {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>は${HtagDisaster_}赤潮${H_tagDisaster}で全滅しました。",
		$id
	);
}

# いろんなイベント
sub logEvent {
	logOut( "${HtagName_}$_[1]${AfterName}${H_tagName}$_[2]", $_[0] );
}

# いろんなイベント
sub logEventT {
	logOut( "${HtagName_}$_[2]${AfterName}${H_tagName}$_[3]", $_[0], $_[1] );
}

# いろんなイベント
sub logEventP {
	logOut( "${HtagName_}$_[1]${AfterName}$_[2]${H_tagName}$_[3]", $_[0] );
}

# いろんなイベント２
sub logEvent2 {
	my ( $id, $name, $result, $result2 ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で${HtagDisaster_}${result}${H_tagDisaster}${result2}。",
		$id
	);
}

# 宇宙災害イベント(宇宙)
sub logSpaceDisEvent {
	logOut( "${HtagName_}${SpaceName}$_[1]${H_tagName}の<B>$_[2]</B>$_[3]",
		$_[0], 999 );
}

# 宇宙イベント(宇宙)
sub logSpaceEvent {
	logOut( "${HtagName_}${SpaceName}${H_tagName}$_[0]", 999 );
}

# 隕石、防ぐ
sub logMeteoD {
	my ( $id, $name, $lName, $point, $kind ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}${kind}${H_tagDisaster}が落下しましたが、見えない力により空中爆発しました。",
		$id
	);
}

# 隕石、海
sub logMeteoSea {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下しました。",
		$id
	);
}

# 隕石、山
sub logMeteoMountain {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下、<B>$lName</B>は消し飛びました。",
		$id
	);
}

# 隕石、海底基地
sub logMeteoSbase {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下、<B>$lName</B>は崩壊しました。",
		$id
	);
}

# 隕石、怪獣
sub logMeteoMonster {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"<B>怪獣$lName</B>がいた${HtagName_}${name}${AfterName}$point${H_tagName}地点に${HtagDisaster_}隕石${H_tagDisaster}が落下、陸地は<B>怪獣$lName</B>もろとも水没しました。",
		$id
	);
}

# 隕石、浅瀬
sub logMeteoSea1 {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}地点に${HtagDisaster_}隕石${H_tagDisaster}が落下、海底がえぐられました。",
		$id
	);
}

# 隕石、その他
sub logMeteoNormal {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}地点の<B>$lName</B>に${HtagDisaster_}隕石${H_tagDisaster}が落下、一帯が水没しました。",
		$id
	);
}

# 隕石、その他
sub logHugeMeteo {
	my ( $id, $name, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}地点に${HtagDisaster_}巨大隕石${H_tagDisaster}が落下！！",
		$id
	);
}

# 噴火
sub logEruption {
	my ( $id, $name, $lName, $point, $erup ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}地点で${HtagDisaster_}火山が$erup${H_tagDisaster}、<B>$lName</B>が<B>山</B>になりました。",
		$id
	);
}

# 噴火、浅瀬
sub logEruptionSea1 {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で陸地になりました。",
		$id
	);
}

# 噴火、海or海基
sub logEruptionSea {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で海底が隆起、浅瀬になりました。",
		$id
	);
}

# 噴火、その他
sub logEruptionNormal {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}地点の<B>$lName</B>は、${HtagDisaster_}噴火${H_tagDisaster}の影響で壊滅しました。",
		$id
	);
}

# 地盤沈下発生
sub logFalldown {
	my ( $id, $name ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}で${HtagDisaster_}地盤沈下${H_tagDisaster}が発生しました！！",
		$id
	);
}

# 地盤沈下被害
sub logFalldownLand {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>は海の中へ沈みました。",
		$id
	);
}

# 地盤沈下被害温泉

sub logFalldownLandO {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>は温泉のくみ上げすぎにより海の中へ沈みました。",
		$id
	);
}

# 広域被害、水没
sub logWideDamageSea {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>は<B>水没</B>しました。",
		$id
	);
}

# 広域被害、海の建設
sub logWideDamageSea2 {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>は跡形もなくなりました。",
		$id
	);
}

# 広域被害、怪獣水没
sub logWideDamageMonsterSea {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の陸地は<B>怪獣$lName</B>もろとも水没しました。",
		$id
	);
}

# 広域被害、怪獣
sub logWideDamageMonster {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>怪獣$lName</B>は消し飛びました。",
		$id
	);
}

# 広域被害、荒地
sub logWideDamageWaste {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>は一瞬にして<B>荒地</B>と化しました。",
		$id
	);
}

# 広域被害、汚染
sub logWideDamageOsen {
	my ( $id, $name, $lName, $point ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}$point${H_tagName}の<B>$lName</B>は放射能で<B>汚染</B>しました。",
		$id
	);
}

# 広域被害(宇宙)
sub logWideDamageSpace {
	logOut(
"${HtagName_}${SpaceName}$_[1]${H_tagName}の<B>$_[0]</B>は一瞬にして<B>$_[2]</B>になりました。",
		999
	);
}

# 受賞
sub logPrize {
	my ( $id, $name, $pName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}が<B>$pName</B>を受賞しました。",
		$id
	);
	logHistory(
		"${HtagName_}${name}${AfterName}${H_tagName}、<B>$pName</B>を受賞");
}

# 部門賞受賞
sub logPrizeV {
	my ( $id, $name, $pName ) = @_;
	logOut(
"${HtagName_}${name}${AfterName}${H_tagName}が<B>$pName</B>を受賞しました。",
		$id
	);

	#ランキング用ログファイル書き出し
	open( MOUT, ">>${HlogdirName}/bumon.log" );
	print MOUT "$HislandTurn,$id,$pName,$name\n";
	close(MOUT);
}

# 地形の呼び方
sub landName {
	my ( $land, $lv ) = @_;
	if ( $land == $HlandSea ) {
		if ( $lv >= 10 ) {
			return '養殖場';
		}
		elsif ( $lv == 1 ) {
			return '浅瀬';
		}
		else {
			return '海';
		}
	}
	elsif ( $land == $HlandWaste ) {
		return ( $lv >= 10 ) ? '温泉' : '荒地';
	}
	elsif ( $land == $HlandPlains ) {
		return '平地';
	}
	elsif ( $land == $HlandTown ) {
		if ( $lv < 30 ) {
			return '村';
		}
		elsif ( $lv < 100 ) {
			return '町';
		}
		else {
			return '都市';
		}
	}
	elsif ( $land == $HlandSlum ) {
		return 'スラム街';
	}
	elsif ( $land == $HlandForest ) {
		return '森';
	}
	elsif ( $land == $HlandFarm ) {
		return '農場';
	}
	elsif ( $land == $HlandFactory ) {
		return '工場';
	}
	elsif ( $land == $HlandTower ) {
		return '商業ビル';
	}
	elsif ( $land == $HlandBase ) {
		return 'ミサイル基地';
	}
	elsif ( $land == $HlandDefence ) {
		if ( $lv == 2 ) {
			return 'S防衛施設';
		}
		elsif ( $lv == 3 ) {
			return 'SS防衛施設';
		}
		elsif ( $lv == 10 ) {
			return 'ST防衛施設';
		}
		elsif ( $lv == 11 ) {
			return 'SST防衛施設';
		}
		elsif ( $lv == 20 ) {
			return '霧付き防衛施設';
		}
		elsif ( $lv == 21 ) {
			return 'S霧付き防衛施設';
		}
		else {
			return '防衛施設';
		}
	}
	elsif ( $land == $HlandMountain ) {
		return '山';
	}
	elsif ( $land == $HlandMonster ) {
		return ( monsterSpec($lv) )[1];
	}
	elsif ( $land == $HlandSbase ) {
		return '海底基地';
	}
	elsif ( $land == $HlandOil ) {
		if ( $lv == 5 ) {
			return '海底防衛施設';
		}
		elsif ( $lv == 6 ) {
			return '海底デストラップ';
		}
		elsif ( $lv == 7 ) {
			return '海底消防署';
		}
		elsif ( $lv >= 35 ) {
			return '海底都市';
		}
		elsif ( $lv >= 10 ) {
			return '海底農場';
		}
		else {
			return '海底油田';
		}
	}
	elsif ( $land == $HlandDeathtrap ) {
		return 'デストラップ';
	}
	elsif ( $land == $HlandWindmill ) {
		return '風車';
	}
	elsif ( $land == $HlandMyhome ) {
		return 'マイホーム';
	}
	elsif ( $land == $HlandPort ) {
		return '港';
	}
	elsif ( $land == $HlandPolice ) {
		return '警察署';
	}
	elsif ( $land == $HlandHospital ) {
		return '病院';
	}
	elsif ( $land == $HlandFlower ) {
		if ( $lv == 13 ) {
			return 'サボテン';
		}
		else {
			return 'お花';
		}
	}
	elsif ( $land == $HlandDokan ) {
		return '土管';
	}
	elsif ( $land == $HlandTrump ) {
		if ( ( $lv < 1 ) || ( $lv > 14 ) ) {
			return "トランプ裏";
		}
		else {
			if ( $lv == 14 ) {
				return "トランプジョーカー";
			}
			else {
				return "トランプ${lv}";
			}
		}
	}
	elsif ( $land == $HlandSeisei ) {
		if ( $lv == 10 ) {
			return '銅精製場';
		}
		elsif ( $lv == 30 ) {
			return '金精製場';
		}
		else {
			return '石炭精製場';
		}
	}
	elsif ( $land == $HlandMegacity ) {
		if ( $lv == 1 ) {
			return '巨大都市−南西';
		}
		elsif ( $lv == 2 ) {
			return '巨大都市−西';
		}
		elsif ( $lv == 3 ) {
			return '巨大都市−北西';
		}
		elsif ( $lv == 4 ) {
			return '巨大都市−北東';
		}
		elsif ( $lv == 5 ) {
			return '巨大都市−東';
		}
		elsif ( $lv == 6 ) {
			return '巨大都市−南東';
		}
		else {
			return '巨大都市';
		}
	}
	elsif ( $land == $HlandMegatower ) {
		if ( $lv == 1 ) {
			return '巨大ビル−南西';
		}
		elsif ( $lv == 2 ) {
			return '巨大ビル−西';
		}
		elsif ( $lv == 3 ) {
			return '巨大ビル−北西';
		}
		elsif ( $lv == 4 ) {
			return '巨大ビル−北東';
		}
		elsif ( $lv == 5 ) {
			return '巨大ビル−東';
		}
		elsif ( $lv == 6 ) {
			return '巨大ビル−南東';
		}
		else {
			return '巨大ビル';
		}
	}
	elsif ( $land == $HlandMegaFact ) {
		if ( $lv == 1 ) {
			return '巨大工場−南西';
		}
		elsif ( $lv == 2 ) {
			return '巨大工場−西';
		}
		elsif ( $lv == 3 ) {
			return '巨大工場−北西';
		}
		elsif ( $lv == 4 ) {
			return '巨大工場−北東';
		}
		elsif ( $lv == 5 ) {
			return '巨大工場−東';
		}
		elsif ( $lv == 6 ) {
			return '巨大工場−南東';
		}
		else {
			return '巨大工場';
		}
	}
	elsif ( $land == $HlandMegaFarm ) {
		if ( $lv == 1 ) {
			return '巨大農場−南西';
		}
		elsif ( $lv == 2 ) {
			return '巨大農場−西';
		}
		elsif ( $lv == 3 ) {
			return '巨大農場−北西';
		}
		elsif ( $lv == 4 ) {
			return '巨大農場−北東';
		}
		elsif ( $lv == 5 ) {
			return '巨大農場−東';
		}
		elsif ( $lv == 6 ) {
			return '巨大農場−南東';
		}
		else {
			return '巨大農場';
		}
	}
	elsif ( $land == $HlandHugecity ) {
		if ( $lv < 50 ) {
			return '超巨大都市(中心)';
		}
		elsif ( $lv < 60 ) {
			return '超巨大都市(都市)';
		}
		elsif ( $lv < 70 ) {
			return '超巨大都市(工場)';
		}
		elsif ( $lv < 80 ) {
			return '超巨大都市(商業)';
		}
		else {
			return '超巨大都市(農場)';
		}
	}
	elsif ( $land == $HlandFuji ) {
		return '富士山';
	}
	elsif ( $land == $HlandTcity ) {
		return '商業都市';
	}
	elsif ( $land == $HlandMonument ) {
		return $HmonumentName[$lv];
	}
	elsif ( $land == $HlandSMonument ) {
		return $HsmonumentName[$lv];
	}
	elsif ( $land == $HlandHaribote ) {
		return ( $lv == 0 ) ? 'ハリボテ' : ( monsterSpec($lv) )[1];
	}
	elsif ( $land == $HlandOsen ) {
		return '汚染土壌';
	}
	elsif ( $land == $HlandBank ) {
		return '銀行';
	}
	elsif ( $land == $HlandStadium ) {
		return 'スタジアム';
	}
	elsif ( $land == $HlandAmusement ) {
		return '遊園地';
	}
	elsif ( $land == $HlandCasino ) {
		return 'カジノ';
	}
	elsif ( $land == $HlandPark ) {
		return '公園';
	}
	elsif ( $land == $HlandSchool ) {
		return '学校';
	}
	elsif ( $land == $HlandDome ) {
		return 'ドーム';
	}
	elsif ( $land == $HlandAirport ) {
		return '空港';
	}
	elsif ( $land == $HlandZoo ) {
		return '動物園';
	}
	elsif ( $land == $HlandBigcity ) {
		return '大都市';
	}
	elsif ( $land == $HlandExpo ) {
		return '博覧会';
	}
	elsif ( $land == $HlandWarp ) {
		return '転移装置';
	}
	elsif ( $land == $HlandWarpR ) {
		return '転移先装置';
	}
	elsif ( $land == $HlandBreakwater ) {
		return '防波堤';
	}
	elsif ( $HseaChk[$land] == 2 ) {

		# 船系
		my ($sId) = ( shipSpec($lv) )[2];
		if ( $sId > 0 ) {
			return $HshipName[ $land - $HlandPirate ]
			  . "(${HidToName{$sId}}${AfterName}所属)";
		}
		else {
			return $HshipName[ $land - $HlandPirate ];
		}
	}
	elsif ( $land == $HlandFire ) {
		return ( $lv >= 10 ) ? 'S消防署' : '消防署';
	}
	elsif ( $land == $HlandKInora ) {
		return '究想いのら';
	}
	elsif ( $land == $HlandEarth ) {
		return '地球';
	}
	elsif ( $land == $HlandSunit ) {
		if ( $lv == 20 ) {
			return '宇宙破壊ユニット';
		}
		elsif ( $lv == 1 ) {
			return '宇宙建設中ユニット';
		}
		elsif ( $lv == 10 ) {
			return '宇宙ユニット';
		}
		else {
			return '宇宙基礎ユニット';
		}
	}
	elsif ( $land == $HlandSCity ) {
		if ( $lv < 30 ) {
			return '宇宙村';
		}
		elsif ( $lv < 100 ) {
			return '宇宙町';
		}
		else {
			return '宇宙都市';
		}
	}
	elsif ( $land == $HlandSFarm ) {
		return '宇宙農場';
	}
	elsif ( $land == $HlandSFactory ) {
		return '宇宙工場';
	}
	elsif ( $land == $HlandSAEisei ) {
		return $HsEisei[ int( $lv / 1000 ) ];    # 宇宙衛星
	}
	elsif ( $land == $HlandSpaceBase ) {
		return '宇宙ミサイル基地';
	}
	elsif ( $land == $HlandSDefence ) {
		return '宇宙防衛施設';
	}
}

# 宇宙の計算
sub spaceEstimate {
	my ($mode) = @_;
	my ( $land, $landValue, $dis, $nation ) = (
		$Hspace->{'land'},       $Hspace->{'landValue'},
		$Hspace->{'landValue2'}, $Hspace->{'nation'}
	);
	my ( $pop, $area, $farm, $factory ) = ( 0, 0, 0, 0 );
	my ( $x, $y, $kind, $value, $id );

	if ( $mode == 0 ) {

		# 太陽風
		$Hsolarwind = 0;
		if ( $Hspace->{'solarwind'} < 10 ) {
			$Hspace->{'solarwind'} = $HislandTurn + random(30) + 30;
		}
		elsif ( $Hspace->{'solarwind'} < $HislandTurn - 8 ) {

		 #			HdebugOut("太陽風８ターン経過:" . $Hspace->{'solarwind'});
			if ( random(5) == 0 ) {

				# 太陽風終了
				logSpaceEvent("で太陽風が収まりました。");
				$Hspace->{'solarwind'} = $HislandTurn + random(30) + 30;
			}
			else {
				$Hsolarwind = 1;
			}
		}
		elsif ( $Hspace->{'solarwind'} <= $HislandTurn ) {

			#			HdebugOut("太陽風発生中:" . $Hspace->{'solarwind'});
			$Hsolarwind = 1;

#			logSpaceEvent("で太陽風が激しく吹き荒れています。収まるまで一切の宇宙開発ができません。");
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

				# 後処理
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

#				HdebugOut("人口地上宇宙比較 (${di})(" . $island->{'oldPop'} . ")(" . $island->{'pop'} . ")(" . $island->{'spop'} . ")${tName}${AfterName}") if($tn ne '');
			}

			if ( ( $island->{'dead'} == 1 ) || ( $island->{'pop'} <= 0 ) ) {

				# 放棄したとき、宗主島が滅んだ時
				$tn = "";
				$nation->[$x][$y] = 0;
				$dis->[$x][$y] -= 30;
				$dis->[$x][$y] = 0 if ( $dis->[$x][$y] < 0 );
			}

			if ( $kind == $HlandSCity ) {
				$value = 200 if ( $value > 200 );
				$pop += $value;
				if ( $tn ne '' ) {

# 宇宙の人口も数値だけ島人口に足す、労働力とかにならない)
					if ( $mode == 1 ) {

						# 終了処理
						#						HdebugOut("終了処理 人口計算");
						$island->{'popspace'} += $value;
					}
					else {

						# 開始処理
						#						HdebugOut("開始処理 人口計算");
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

					# 勝手に建設が進む
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

				# 宇宙衛星
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

			# 異常値に正常な値を代入
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

		# 初期処理
		# 生産と消費
		$Hspace->{'foodP'} = $farm * 10;
		$Hspace->{'foodC'} = int( $pop * $HeatenFood );
		$Hspace->{'food'} += $Hspace->{'foodP'};

		# 食料消費
		$Hspace->{'food'} -= $Hspace->{'foodC'};
	}
	else {

		# 食料が溢れていたらカットする
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

				# 部門賞 宇宙王
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

# 宇宙成長および単ヘックス災害
sub spaceHex {
	my ( $land, $landValue, $dis, $nation ) = (
		$Hspace->{'land'},       $Hspace->{'landValue'},
		$Hspace->{'landValue2'}, $Hspace->{'nation'}
	);
	my ( $pop1, $pop2, $pop3, $di ) = ( 18, 9, 3, 0 );

	#	if($Hspace->{'food'} < 0){
	#		# 食糧不足
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

		# 収入
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

		# 成長
		if ( $kind == $HlandSCity ) {
			if (   ( random($p) < $Hspace->{'area'} )
				&& ( $Hsolarwind == 0 )
				&& ( $HdisMonster > 0 ) )
			{

				# 怪獣処理
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

			# 宇宙衛星
			if ( $lv % 1000 > 0 ) {
				my $e = int( $lv / 1000 );
				if ( $e == 4 && $island->{'eis4'} > 1 ) {
					if ( $lv % 1000 < $island->{'eis4'} ) {
						$landValue->[$x][$y] = 4000;
					}
					else {
						$landValue->[$x][$y] -=
						  $island->{'eis4'};    # エネルギー消費
					}
					$island->{'eis4'} = 1;
				}
				else {
					$landValue->[$x][$y]--;     # エネルギー消費
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
					"が、燃料切れで地球に向け降下しました。"
				);
				$land->[$x][$y]      = $HlandSea;
				$landValue->[$x][$y] = 0;
				$dis->[$x][$y]       = 0;
				$nation->[$x][$y]    = 0;

				# 地上隕石落下率アップはしない。
				#	$HdisMeteo += 80; # 全島+8%
			}
		}
		elsif ( ( $kind == $HlandMonster ) && ( $Hsolarwind == 0 ) ) {

			# 怪獣
			# 各要素の取り出し
			my ( $mKind, $mName, $mHp ) = monsterSpec( $landValue->[$x][$y] );
			my ($special) = $HmonsterSpecial[$mKind];

			next if ( $spaceMove[$x][$y] >= 2 );    # すでに動いた後

			# 移動する
			my ( $sx, $sy ) = monmove( $Hspace, $x, $y, 3 );

			# 移動済みフラグ
			if ( $HmonsterSpecial[$mKind] == 2 ) {

				# 移動済みフラグは立てない
			}
			elsif ( $HmonsterSpecial[$mKind] == 1 ) {

				# 速い怪獣
				$spaceMove[$sx][$sy] = $spaceMove[$x][$y] + 1;
			}
			else {

				# 普通の怪獣
				$spaceMove[$sx][$sy] = 2;
			}
		}
		elsif ( ( $kind == $HlandSFactory ) && ( $dis->[$x][$y] > 30 ) ) {
			if (   ( random(1000000) < $HdisSHugeMeteo * $Hspace->{'area'} )
				&& ( $Hsolarwind == 0 ) )
			{

				# 巨大隕石
				logSpaceDisEvent( $id, "($x, $y)", landName( $kind, $lv ),
"付近で空間が歪んだと思うと突然巨大な隕石が出現しました！！"
				);
				wideDamageSpace( $id, $land, $landValue, $dis, $nation, $x, $y,
					7, 1 );
			}
		}
		elsif ( ( $kind == $HlandSunit ) && ( $lv == 10 ) ) {
			if ( random(10) == 0 ) {

				# 周りに農場あれば、ここも町になる
				if ( countGrow( $land, $landValue, $x, $y ) ) {
					$land->[$x][$y]      = $HlandSCity;
					$landValue->[$x][$y] = 1;
					$dis->[$x][$y]       = 10;
				}
			}
		}

		# 不満度変動
		if ( $kind == $HlandSunit ) {
			$dis->[$x][$y] = 20;
		}
		elsif ( $id > 0 ) {

		}
		else {
			$dis->[$x][$y] -= 4;
		}
		if ( ( $dis->[$x][$y] > 30 ) && ( $id > 0 ) ) {

			# 不満を持つ人による蜂起イベント
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
					"が、一斉に蜂起され独立しました。"
				);
				$dis->[$x][$y] -= 25;
				$nation->[$x][$y] = 0;

				# 周囲の不満度を上げる
				my ( $j, $sx, $sy );
				for ( $j = 1 ; $j < 7 ; $j++ ) {
					$sx = $x + $ax[$j];
					$sy = $y + $ay[$j];
					$sx--
					  if ( !( $sy % 2 ) && ( $y % 2 ) )
					  ;    # 行による位置調整
					if (   ( $sx < 0 )
						|| ( $sx >= $HislandSize )
						|| ( $sy < 0 )
						|| ( $sy >= $HislandSize ) )
					{
					}
					elsif ( $nation->[$sx][$sy] == $id ) {

	 #						HdebugOut("周囲の不満度 同じ所属:" . $nation->[$sx][$sy]);
						$dis->[$sx][$sy] += 10;
					}
					elsif ( $nation->[$sx][$sy] > 0 ) {

	 #						HdebugOut("周囲の不満度 違う所属:" . $nation->[$sx][$sy]);
						$dis->[$sx][$sy] -= 5;
					}
				}
			}
		}
	}
}

# 海域成長および単ヘックス災害
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

				# 怪獣処理
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

			# 怪獣
			# 各要素の取り出し
			my ( $mKind, $mName, $mHp ) = monsterSpec( $landValue->[$x][$y] );
			my ($special) = $HmonsterSpecial[$mKind];
			next if ( $oceanMove[$x][$y] >= 2 );    # すでに動いた後

			# 移動する
			my ( $sx, $sy ) = monmove( $Hocean, $x, $y, 4 );

			# 移動済みフラグ
			if ( $HmonsterSpecial[$mKind] == 2 ) {

				# 移動済みフラグは立てない
			}
			elsif ( $HmonsterSpecial[$mKind] == 1 ) {

				# 速い怪獣
				$oceanMove[$sx][$sy] = $oceanMove[$x][$y] + 1;
			}
			else {

				# 普通の怪獣
				$oceanMove[$sx][$sy] = 2;
			}
		}
	}
	$HislandSize = $wHislandSize;
}

# 人口その他の値を算出(負荷軽減のため分けてみただけどあまり意味がなかった)
sub estimateS {
	my (
		$pop,     $popsea,   $area,   $factory,  $tower,
		$slum,    $forest,   $kaitei, $MissileK, $oil,
		$myhome,  $port,     $tenki,  $treasure, $fishShip,
		$titanic, $monsship, $aegis,  $oilfactory
	  )
	  = ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 );

	# 地形を取得
	my ($island) = $Hislands[ $_[0] ];
	my ( $land, $landValue, $id ) =
	  ( $island->{'land'}, $island->{'landValue'}, $island->{'id'} );

	# 暫定処理
	if ( $island->{'kaisi'} == 0 ) {
		my $zanteisturn = $HislandTurn - $island->{'turnsu'} * 3;
		$zanteisturn = 1 if ( $zanteisturn < 1 );
		$island->{'kaisi'} = $zanteisturn;
	}

	# 数える

	my ( $x, $y, $kind, $value, $i );
	for ( $y = 0 ; $y < $HislandSize ; $y++ ) {
		for ( $x = 0 ; $x < $HislandSize ; $x++ ) {
			$kind  = $land->[$x][$y];
			$value = $landValue->[$x][$y];
			$area++ if ( $HseaChk[$kind] == 0 );    # 海系でないとき

			if (   ( $kind == $HlandSbase )
				|| ( $kind == $HlandOil )
				|| ( $kind == $HlandSMonument ) )
			{
				$kaitei++;
			}
			elsif ( $HseaChk[$kind] == 2 ) {

				# 船系
				my ( $order, $hp, $sId ) = shipSpec($value);
				if ( $HpunishInfo{$id}->{punish} == 9 ) {

					# 船強制生還処理
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
					$treasure++;    # 宝船
				}
				elsif (( $kind == $HlandFishSShip )
					|| ( $kind == $HlandFishMShip )
					|| ( $kind == $HlandFishLShip )
					|| ( $kind == $HlandTitanic ) )
				{
					$fishShip++;    # 漁船、客船等

					$titanic++ if ( $kind == $HlandTitanic );    # 豪華客船
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

						# 海獣掃討艇

					  #						HdebugOut("指令$order船ＩＤ$sId島ＩＤ$id");
						$monsship += 5;
					}
					elsif (( $kind == $HlandAegisShip )
						&& ( $order == 0 )
						&& ( $sId == $id ) )
					{

						# イージス艦
						$aegis += 5;
					}
				}
				elsif ( ( $kind == $HlandPirate ) && ( $sId != $id ) ) {

					# 海賊船
					slideBack( $island->{'command'}, 0, $HcomSpecialSPP, $id,
						$x, $y, 5 );
				}
				next;
			}

			if ( $kind == $HlandTown ) {

				# 町
				$value = 200 if ( $value > 200 );
				$pop += $value;
			}
			elsif ( ( $kind == $HlandOil ) && ( $value >= 35 ) ) {

				# 海底都市
				$popsea += $value;
			}
			elsif ( ( $kind == $HlandOil ) && ( $value == 0 ) ) {

				# 油田
				$oil++;
			}
			elsif (( $kind == $HlandForest )
				|| ( $kind == $HlandMonument )
				|| ( $kind == $HlandSMonument )
				|| ( $kind == $HlandFlower )
				|| ( $kind == $HlandPark ) )
			{

				# 森、記念碑系、公園、お花
				$forest++;
			}
			elsif ( $kind == $HlandTower ) {

				# 商業ビル
				$tower += $value;
			}
			elsif ( ( $kind == $HlandAirport ) || ( $kind == $HlandExpo ) ) {

				# 空港、博覧会
				$tower += 50;
			}
			elsif ( $kind == $HlandPort ) {

				# 港
				$port += $value;
			}
			elsif ( $kind == $HlandFactory ) {

				# 工場
				$factory += $value;
			}
			elsif ( $kind == $HlandMegacity ) {

				# 巨大都市
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

				# 超巨大都市
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

				# 怪獣
				$island->{'monsmgmflg'} = 1;
				my $mKind = ( monsterSpec($value) )[0];
				if ( $mKind == 28 ) {

					# てるてるいのら
					$tenki--;
				}
				elsif ( $mKind == 29 ) {

					# 逆さてるてる
					$tenki++;
				}
				elsif (( $HmonsterSpecial[$mKind] == 6 )
					|| ( $HmonsterSpecial[$mKind] == 7 ) )
				{

					# 先に移動する怪獣がいる
					$island->{'smons'} = 1;
				}
				if ( $HmonsterDestroy[$mKind] == $HlandSea ) {

					# 海獣
					slideBack( $island->{'command'}, 0, $HcomSpecialSPP, $id,
						$x, $y, 5 );
				}
			}
			elsif ( $kind == $HlandSlum ) {

				# スラム街
				if ( $value < 130 ) {
					$slum += $value;
				}
				else {    # 普通の都市に戻る
					$land->[$x][$y] = $HlandTown;
					$pop += $value;
				}
			}
			elsif ( $kind == $HlandTcity ) {

				# 商業都市
				$tower += 200;
				$pop   += 300;
			}
			elsif ( $kind == $HlandMegatower ) {

				# 巨大ビル
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

				# 巨大工場
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

				# 大都市
				$pop += 1000;
			}
			elsif (( $kind == $HlandDefence )
				|| ( ( $kind == $HlandOil ) && ( $value == 5 ) ) )
			{

				# 防衛施設
				$island->{'defence'} = 1;
			}
			elsif ( $kind == $HlandMyhome ) {

				# マイホーム
				$island->{'myhome'} = 1;
			}
			elsif ( $kind == $HlandPolice ) {

				# 警察署
				$island->{'Police'} = 1;
			}
			elsif ( $kind == $HlandHospital ) {

				# 病院
				$island->{'Hospital'} = 1;
			}
			elsif ( $kind == $HlandFuji ) {

				# 富士山
				$island->{'event'} += 2;
			}
			elsif ( $kind == $HlandTrump ) {

				# トランプ
				$island->{'trump'}->[$value] = 1;
			}
		}
	}

	# 地下
	my ( $ugL, $ugV, $ugX, $ugY ) =
	  ( $island->{'ugL'}, $island->{'ugV'}, $island->{'ugX'},
		$island->{'ugY'} );
	for ( $i = 0 ; $i < $HugMax ; $i++ ) {
		next
		  if ( $land->[ $ugX->[$i] ][ $ugY->[$i] ] != $HlandDokan )
		  ;    # 出口無し
		for ( $x = 0 ; $x < 9 ; $x++ ) {
			if ( $ugL->[$i][$x] == $HugTosi ) {
				$pop += $ugV->[$i][$x];
			}
			elsif ( $ugL->[$i][$x] == $HugFarm ) {

				# 何もしない
			}
			elsif ( $ugL->[$i][$x] == $HugFact ) {
				$factory += $ugV->[$i][$x];
			}
			elsif ( $ugL->[$i][$x] == $HugKiti ) {

				# 何もしない
			}
			elsif ( $ugL->[$i][$x] == $HugOil ) {
				$oilfactory += $ugV->[$i][$x];
			}
		}
	}

	$pop += $slum;
	$island->{'kaiteipop'} = 1
	  if ( $pop < $popsea );    # 海底の人口方が多い時
	$pop += $popsea;

	if (   ( ( $factory + $port + $oilfactory ) * 2 < $tower )
		&& ( $pop >= 2000 ) )
	{
		$island->{'towerD'} = 1001 + $tower - $factory - $port;
	}
	elsif ( ( $tower == 0 ) && ( $pop >= 2000 ) ) {
		$island->{'towerD'} = 1000;
	}

	# 代入
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
	  ( $area == 0 ) ? 7 : int( $forest * 100 / $area );    # 陸が無い時
	$island->{'monsship'} = $monsship;
	$island->{'aegis'}    = $aegis;

	$island->{'oilfactory'} = $oilfactory;

	$island->{'ship'} = 0;                                  # 初期化

	# 宇宙資産を初期化
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

	# 地形を取得
	my ($island) = $Hislands[ $_[0] ];
	my ( $land, $landValue, $land2, $landValue2, $nation, $id ) = (
		$island->{'land'},       $island->{'landValue'}, $island->{'land2'},
		$island->{'landValue2'}, $island->{'nation'},    $island->{'id'}
	);
	my (%LandCount);

	# 数える
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
				$nation->[$x][$y] = 0;    # ターン杯の時にクリア
			}
			if ( $HseaChk[$kind] == 0 ) {

				# 海系でないとき
				$area++;
			}
			elsif ( $kind == $HlandSea ) {

				# 海の時
				if (   ( $land2->[$x][$y] != $HlandSea )
					|| ( $landValue2->[$x][$y] != 0 ) )
				{

					# 後に隠れている地形が海でないとき
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

				# 船系
				my $sId = ( shipSpec($value) )[2];
				if ( $sId > 0 ) {
					my $sIsland = $Hislands[ $HidToNumber{$sId} ];
					$sIsland->{'ship'}++;
				}
				next;
			}
			if ( $kind == $HlandTown ) {

				# 町
				$value = 200 if ( $value > 200 );
				$pop += $value;
			}
			elsif ( ( $kind == $HlandSea ) && ( $value >= 10 ) ) {

				# 養殖場
				$yousyoku += $value;
			}
			elsif ( ( $kind == $HlandOil ) && ( $value >= 35 ) ) {

				# 海底都市
				$popsea += $value;
			}
			elsif ( ( $kind == $HlandOil ) && ( $value == 0 ) ) {

				# 油田
				$oil++;
			}
			elsif ( $kind == $HlandForest ) {

				# 森
				#	$forest++;
				$forestV += $value;
			}
			elsif ( $kind == $HlandFlower ) {

				# 花
				$flower++;
			}
			elsif ( $kind == $HlandMonument || $kind == $HlandSMonument ) {

				# 記念碑系
				$monument++;
			}
			elsif (( $kind == $HlandFarm )
				|| ( $kind == $HlandMegaFarm )
				|| ( ( $kind == $HlandOil ) && ( $value >= 10 ) ) )
			{

				# 農場 巨大農場 海底農場
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

  # 陸の農場のとき周囲2へクスに風車があれば２倍の規模に
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

				# ミサイル発射数
				$landValue->[$x][$y] = int( $value / 100 )
				  if ( $kind == $HlandDokan );
				$MissileK += expToLevel( $kind, $value );
			}
			elsif ( $kind == $HlandTower ) {

				# 商業ビル
				$tower += $value;
			}
			elsif ( ( $kind == $HlandAirport ) || ( $kind == $HlandExpo ) ) {

				# 空港、博覧会
				$tower += 50;
			}
			elsif ( $kind == $HlandMountain ) {

				# 山
				$mountain += $value;
			}
			elsif ( $kind == $HlandPort ) {

				# 港
				$port += $value;
			}
			elsif ( $kind == $HlandFactory ) {

				# 工場
				$factory += $value;
			}
			elsif ( $kind == $HlandMegacity ) {

				# 巨大都市
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

				# 超巨大都市
				my ($lName) = landName( $kind, $value );
				my ($lName2);
				if ( $value < 50 ) {

					# 中央
					if ( countAround( $land, $x, $y, $HlandHugecity, 7 ) < 7 ) {

	  # 周囲１ヘクスが１つでも超巨大地形でない場合、崩壊
						$land->[$x][$y] = $HlandMonument;
						$lName2 = landName( $HlandMonument, $value );
					}
					else {
						$pop += 400;
					}
				}
				else {

# 周囲１ヘクスに超巨大都市(中心)があるかどうかチェックし、存在しない場合は崩壊
					my ( $sx, $sy );
					my ($destroy) = 1;
					for ( $i = 1 ; $i < 7 ; $i++ ) {
						$sx = $x + $ax[$i];
						$sy = $y + $ay[$i];
						$sx--
						  if ( !( $sy % 2 ) && ( $y % 2 ) )
						  ;    # 行による位置調整
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

  # 陸の農場のとき周囲2へクスに風車があれば２倍の規模に
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
"の${lName}は、${lName2}に戻ってしまいました。"
					);
				}
			}
			elsif ( $kind == $HlandHaribote ) {

				# ハリボテ
				$haribote++;
			}
			elsif ( $kind == $HlandMonster ) {

				# 怪獣
				$mons++;
			}
			elsif ( $kind == $HlandSlum ) {

				# スラム街
				$pop += $value;
				$land->[$x][$y] = $HlandTown if ( $value >= 130 );
			}
			elsif ( $kind == $HlandTcity ) {

				# 商業都市
				$tower += 200;
				$pop   += 300;
			}
			elsif ( $kind == $HlandMegatower ) {

				# 巨大ビル
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

				# 巨大工場
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

				# 大都市
				$pop += 1000;
			}
			elsif ( $kind == $HlandBank ) {

				# 銀行
				$allBank += $value;
			}
			elsif ( $kind == $HlandFuji ) {

				# 富士山
				fujiAround( $land, $landValue, $x, $y, $value );
			}
		}
	}

	# 地下
	my ( $ugL, $ugV, $ugX, $ugY ) =
	  ( $island->{'ugL'}, $island->{'ugV'}, $island->{'ugX'},
		$island->{'ugY'} );
	for ( $i = 0 ; $i < $HugMax ; $i++ ) {
		next
		  if ( $land->[ $ugX->[$i] ][ $ugY->[$i] ] != $HlandDokan )
		  ;    # 出口無し
		for ( $x = 0 ; $x < 9 ; $x++ ) {
			if ( $ugL->[$i][$x] == $HugTosi ) {
				if ( $island->{'food'} <= 0 ) {

					# 食糧不足
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

					# 食糧不足で崩壊
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
	  if ( $pop < $popsea );    # 海底の人口方が多い時
	$pop += $popsea;
	if ( ( ( $factory + $port ) * 2 < $tower ) && ( $pop >= 2000 ) ) {
		$island->{'towerD'} = 1001 + $tower - $factory - $port;
	}
	elsif ( ( $tower == 0 ) && ( $pop >= 2000 ) ) {
		$island->{'towerD'} = 1000;
	}

	# 占有率
	#	HdebugOut($island->{'id'} . " 自島占有=" . $LandCount{0});
	if ( $LandCount{0} < $Hpossess ) {

		# 降伏！？
		my ( $tIsland, $tName, $name );
		$i = 0;
		foreach ( sort { $LandCount{$b} <=> $LandCount{$a} } keys %LandCount ) {
			my $w = int( $LandCount{$_} * 10000 / $HpointNumber + 0.5 ) / 100;
			if ( ( $_ != 0 ) && ( $w > 1 ) ) {

				# 勝利島
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
					  ;    # 国連保護国で無い場合
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
"が、${HtagName_}${tName}${H_tagName}(${w}％)に<b>敗れ</b>ました。"
					);

					# 防衛施設(地上)、ミサイル施設、地下廃棄
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
"は、武装放棄し<b>国連保護化</b>になりました。"
					);
					$island->{'evil'} = 0;
					$MissileK = 0;
				}
				$i++;
			}
		}
	}

	# 代入
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

	# 部門賞用
	$island->{'mons'}     = $mons;
	$island->{'forestV'}  = $forestV;
	$island->{'haribote'} = $haribote;
	$island->{'industry'} = $factory + $port + $mountain;
	$island->{'monument'} = $monument;
	$island->{'flower'}   = $flower;

	$allPop      += $pop;
	$allArea     += $area;
	$allMoney    += $island->{'money'};
	$allMissileA += $island->{'MissileA'};    #ミサイル発射総数
	$allFarm     += $farm;
	$allTower    += $tower;
	$allIndustry += $island->{'industry'};
	$allYousyoku += $yousyoku;
	$allForest   += $forestV;
}

# 巨大地形の周辺
sub megaAround {
	my ( $land, $landValue, $x, $y, $kind, $lv ) = @_;

	# 巨大地形が向いている方を調べる($axと合わせてある)
	my $sx = $x + $ax[$lv];
	my $sy = $y + $ay[$lv];
	$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # 行による位置調整
	if (   ( $sx < 0 )
		|| ( $sx >= $HislandSize )
		|| ( $sy < 0 )
		|| ( $sy >= $HislandSize ) )
	{

		# 範囲外の場合
	}
	else {

		# 範囲内の場合
		if ( $lv < 4 ) {
			$lv += 3;
		}
		else {
			$lv -= 3;
		}

		# 対応した巨大地形があった時。
		return 1
		  if ( ( $land->[$sx][$sy] == $kind )
			&& ( $landValue->[$sx][$sy] == $lv ) );
	}
	return 0;
}

# 富士山の周辺
sub fujiAround {
	my ( $land, $landValue, $x, $y, $lv ) = @_;
	my ( $i, $sx, $sy );
	if ( $lv == 0 ) {
		for ( $i = 3 ; $i < 5 ; $i++ ) {
			$sx = $x + $ax[$i];
			$sy = $y + $ay[$i];
			$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );  # 行による位置調整
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
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # 行による位置調整
		if ( $land->[$sx][$sy] != $HlandFuji ) {
			$land->[$x][$y]      = $HlandWaste;
			$landValue->[$x][$y] = 1;
		}
	}
	elsif ( $lv == 2 ) {
		$sx = $x + $ax[1];
		$sy = $y + $ay[1];
		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # 行による位置調整
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
	$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # 行による位置調整
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

# 流入した人を各町に振り分ける。
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

			# 町、スラム街の場合
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

			# 平地の場合
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

# 怪獣移動
sub monmove {
	my ( $island, $x, $y, $mode ) = @_;

	# 導出値
	my ( $name, $id, $land, $landValue, $land2, $landValue2, $nation ) = (
		$island->{'name'},      $island->{'id'},    $island->{'land'},
		$island->{'landValue'}, $island->{'land2'}, $island->{'landValue2'},
		$island->{'nation'}
	);
	my ( $i, $d, $sx, $sy );

	if ( $land->[$x][$y] == $HlandKInora ) {

		# 究想いのら

		my $kname = landName( $HlandKInora, 0 );

		# ダメージ計算処理
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

			# 倒した
			my ($tn) = $HidToNumber{$lastDamage};
			if ( $tn eq '' ) {

				# 倒した島がない場合は死なない
				$landValue->[$x][$y] -= ( $hp - 1 ) * 100 if ( $hp > 1 );
			}
			else {
				my $tIsland = $Hislands[$tn];
				my $tName   = $tIsland->{'name'};

				logOut(
"${HtagName_}${name}${AfterName}($x, $y)${H_tagName}の<B>怪獣$kname</B>は力尽き、倒れました。",
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
				$tIsland->{'evil'}  = 20000;                       # 黄金期
				kinoraDel( $land, $landValue, $x, $y );
				return ( $x, $y );
			}
		}
		else {

			# ダメージ
			$landValue->[$x][$y] -= $damage * 100;
		}
		$sx = random($HislandSize);
		$sy = random($HislandSize);
		my $lv = $landValue->[$x][$y];
		kinoraDel( $land, $landValue, $x, $y );
		if (   ( $i > 6 )
			&& ( chkAround( $land, $sx, $sy, $HlandKInora, 7 ) == 0 ) )
		{

			# ジャンプする
			if ( $lv < 10000 ) {

				# 他の島へ飛ぶ
				my @INumber = randomArray($HislandNumber);
				my $tIsland = $Hislands[ $INumber[ random($HislandNumber) ] ];
				my ( $tId, $tName, $tLand, $tLandValue ) = (
					$tIsland->{'id'},   $tIsland->{'name'},
					$tIsland->{'land'}, $tIsland->{'landValue'}
				);
				if (   ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
					|| ( $tIsland->{'evil'} == 0 ) )
				{

					# 相手が途上国の為移動しない
				}
				else {
					logEventP( $id, $name, "($x, $y)",
"の<B>怪獣$kname</B>は、${HtagName_}$tName$AfterName${H_tagName}へ飛び立ちました。"
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
"に<B>怪獣$kname</B>がジャンプし周囲１へクスが踏みつけられました。"
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

			# 宇宙 なんとなく中心へ
			my ($c) = $HislandSize / 2 - 1;
			if ( random(3) == 0 ) {
				if ( $x == $c ) {
				}
				elsif ( $x - $c > 0 ) {

					# 左に
					$island->{'manipulate'} = 5;
				}
				else {

					# 右に
					$island->{'manipulate'} = 2;
				}
			}
			else {
				if ( $y == $c ) {
				}
				elsif ( $y - $c > 0 ) {

					# 上に
					$island->{'manipulate'} = ( random(2) == 0 ) ? 1 : 6;
				}
				else {

					# 下に
					$island->{'manipulate'} = ( random(2) == 0 ) ? 3 : 4;
				}
			}
		}
		else {
			$island->{'manipulate'} = 0;
		}
	}

	# 動く方向を決定
	for ( $i = 0 ; $i < 3 ; $i++ ) {
		if ( $island->{'manipulate'} == 0 ) {
			$d = random(6) + 1;
		}
		else {    # 操られている時
			$d = $island->{'manipulate'};
		}
		$sx = $x + $ax[$d];
		$sy = $y + $ay[$d];

		$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );    # 行による位置調整
		next
		  if ( ( $sx < 0 )
			|| ( $sx >= $HislandSize )
			|| ( $sy < 0 )
			|| ( $sy >= $HislandSize ) );           # 範囲外判定

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

			# シーいのら、シーゴースト、宇宙
			last;
		}
		elsif ( $mKind == 16 ) {

			# 埋め立ていのら
			last
			  if ( ( $HseaChk[ $land->[$sx][$sy] ] == 1 )
				|| ( $land->[$sx][$sy] == $HlandWarp ) );
		}
		else {

			# 陸地なら移動
			last if ( ( $HseaChk[ $land->[$sx][$sy] ] == 0 ) );
		}
	}
	next if ( $i == 3 );    # 動かなかった

	# 動いた先の地形によりメッセージ
	my ($l)     = $land->[$sx][$sy];
	my ($lv)    = $landValue->[$sx][$sy];
	my ($lName) = landName( $l, $lv );
	my ($point) = "($sx, $sy)";

	if ( $l == $HlandEarth ) {

		# 地球に到達
		$HearthAttack++;
		$HdisMonster *= 2;
	}
	elsif ( $l == $HlandOPlayer ) {

		# 海域怪獣島へ特攻
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

		# 移動
		$land->[$sx][$sy]      = $land->[$x][$y];
		$landValue->[$sx][$sy] = $landValue->[$x][$y];
	}

	# もと居た位置を怪獣によって変更
	if ( $mKind == 10 ) {

		# デビルいのら
		$land->[$x][$y]      = $HlandOsen;
		$landValue->[$x][$y] = $mHp;
	}
	elsif ( $mKind == 27 ) {

		# 分裂いのら
		if ( random(2) == 0 ) {

			my ($nhp) = int( $mHp / 2 );

			if ( $nhp > 0 ) {

				# 分裂
				logMonster( $id, $name, "($x, $y)", $mName,
					"が分裂しました。" );
				$landValue->[$x][$y] = 2700 + $nhp;
				$landValue->[$sx][$sy] -= $nhp;
			}
			else {

				# 消滅　ログ無し
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

	# 裏の地形も消去
	$land2->[$x][$y]      = $HlandSea;
	$landValue2->[$x][$y] = 0;

	if ( $mode == 3 ) {

		# 宇宙
		$land2->[$sx][$sy]      = $HlandSea;
		$landValue2->[$sx][$sy] = 0;
		$nation->[$sx][$sy]     = 0;

		$nation->[$x][$y] = 0;

		if ( $l == $HlandSDefence ) {

			# 防衛施設
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

		# 海域
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

	# スペースいのら
	$island->{'Meteo'} += 20 if ( $mKind == 20 );

	# スペースいのら
	$island->{'Meteo'} += 20 if ( $mKind == 20 );

	if ( ( ( $l == $HlandDefence ) || ( ( $l == $HlandOil ) && ( $lv == 5 ) ) )
		&& ( $HdBaseAuto == 1 ) )
	{

		# 防衛施設を踏んだ
		logMonsMoveDefence( $id, $name, $lName, $point, $mName );

		# 広域被害ルーチン
		wideDamage( $id, $name, $land, $landValue, $sx, $sy, 0 );
	}
	elsif (( $l == $HlandDeathtrap )
		|| ( ( $l == $HlandOil ) && ( $lv == 6 ) ) )
	{

		# デストラップを踏んだ
		if ( $l == $HlandOil ) {

			# 海底
			logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
				"跡形も無く消え去り" );
			$land->[$sx][$sy]      = $HlandSea;
			$landValue->[$sx][$sy] = 0;
		}
		else {
			if ( $lv >= 3 ) {
				logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
					"跡形も無く消え去り" );
				$land->[$sx][$sy]      = $HlandWaste;
				$landValue->[$sx][$sy] = 1;
			}
			elsif ( $lv == 2 ) {
				if ( $mKind == 18 ) {

					# 反撃いのら
					logMonsMoveDeathtrapM( $id, $name, $lName, $point, $mName );
				}
				elsif ( $mHp > 3 ) {
					logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
						"ダメージを受け" );
					$landValue->[$sx][$sy] -= 3;
				}
				else {
					logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
						"跡形も無く消え去り" );
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

					# ミサイルで発生する怪獣
					logMonsMoveDeathtrapM( $id, $name, $lName, $point, $mName );
				}
				elsif ( $mHp > 3 ) {
					logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
						"ダメージを受け" );
					$landValue->[$sx][$sy] -= 2;
				}
				elsif ( $mHp > 1 ) {
					logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
						"ダメージを受け" );
					$landValue->[$sx][$sy]--;
				}
				else {
					logMonsMoveDeathtrap( $id, $name, $lName, $point, $mName,
						"跡形も無く消え去り" );
					$land->[$sx][$sy]      = $HlandWaste;
					$landValue->[$sx][$sy] = 1;
				}
			}
		}
	}
	elsif ( $l == $HlandWarp ) {    # 転移装置
		logWarpMons( $id, $name, $lName, $point, "怪獣${mName}" );
		if (
			warp(
				$id, $name,
				$land->[$sx][$sy],
				$landValue->[$sx][$sy],
				"怪獣${mName}", $lv, 0
			) == 0
		  )
		{
			$land->[$sx][$sy]      = $HlandWarp;
			$landValue->[$sx][$sy] = $lv;
		}
		else {
			logWarpMonsMiss( $id, $name, $point, "怪獣${mName}" );
		}
	}
	elsif ( ( $mKind == 17 ) && ( random(5) == 0 ) )
	{    # 神風怪獣タイムボカン
		logMonsZIBAKU( $id, $name, $lName, $point, $mName );
		wideDamage( $id, $name, $land, $landValue, $sx, $sy, 0 );
	}
	elsif ( $mKind == 23 ) {

		# カネゴン
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

		# リッチいのら
		if ( $mHp <= 1 ) {
			if ( random(4) == 0 ) {

				# 消滅する
				logMonsMove( $id, $name, $lName, $point, $mName );
				logMonster( $id, $name, $point, $mName,
					"は自然消滅したようです。" );
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

				# ダメージを受ける
				$landValue->[$sx][$sy]--;
				logMonster( $id, $name, $point, $mName,
					"は弱ったようです。" );
			}
		}
	}
	elsif ( $mKind == 22 ) {

		# グラテネスいのら
		logMonsMove( $id, $name, $lName, $point, $mName );
		logMonsEAT( $id, $name, $lName, $point, $mName );
		my $eatfood = int( $island->{'food'} * 0.05 );
		$eatfood = 1000 if ( $eatfood < 1000 );
		$island->{'food'} -= $eatfood;
	}
	elsif ( $mKind == 26 ) {

		# 迷彩いのら
		# 行き先が荒地になる
		logMonsMove( $id, $name, $lName, "(?, ?)", $mName );
	}
	else {

		# 行き先が荒地になる
		logMonsMove( $id, $name, $lName, $point, $mName );
	}

	if (   ( $l == $HlandOsen )
		&& ( ( $mKind == 6 ) || ( $mKind == 7 ) || ( $mKind == 8 ) ) )
	{
		if ( random(4) == 0 ) {    # 汚染による特殊変異
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

# 船系移動行動
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

	# 移動前の行動
	my ( $i, $d, $sx, $sy, $j );
	if ( $order == 4 ) {

		# 攻撃
		my $Katk = $HshipMATK[ $lx - $HlandPirate ];
		my $Satk = $HshipSATK[ $lx - $HlandPirate ];
		return ( $x, $y )
		  if ( $Katk + $Satk < 1 );    # 何もしない。(移動もしない)
		for ( $j = 1 ; $j < 7 ; $j++ ) {
			$sx = $x + $ax[$j];
			$sy = $y + $ay[$j];
			$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );  # 行による位置調整
			next
			  if ( ( $sx < 0 )
				|| ( $sx >= $HislandSize )
				|| ( $sy < 0 )
				|| ( $sy >= $HislandSize ) );         # 範囲外判定

			if ( ( $land->[$sx][$sy] == $HlandMonster ) && ( $Katk > 0 ) ) {

				# 怪獣発見攻撃する
				my ( $mKind, $mName, $mHp ) =
				  monsterSpec( $landValue->[$sx][$sy] );
				my ($special) = $HmonsterSpecial[$mKind];

				# 硬化中?
				if (   ( ( $special == 3 ) && ( ( $HislandTurn % 2 ) == 1 ) )
					|| ( ( $special == 4 ) && ( ( $HislandTurn % 2 ) == 0 ) )
					|| ( ( $special == 5 ) && ( random(4) != 0 ) ) )
				{

					# 硬化中
					next;
				}
				else {
					$mHp - $Katk;
					if ( $mHp > 0 ) {

						# 怪獣生きてる
						logMonster( $id, $name, "($sx, $sy)", $mName,
"は、どこからかダメージを受けました。"
						);
						$landValue->[$sx][$sy] -= $Katk;
					}
					else {

						# 倒した
						logMonster( $id, $name, "($sx, $sy)", $mName,
"は、どこからかの攻撃により消滅したようです。"
						);
						$land->[$sx][$sy]      = $HmonsterDestroy[$mKind];
						$landValue->[$sx][$sy] = 0;
					}
					last;
				}
			}
			elsif ( ( $HseaChk[ $land->[$sx][$sy] ] == 2 ) && ( $Satk > 0 ) ) {

				# 今後削除予定？

#
#				my($torder, $thp, $tsId) = shipSpec($landValue->[$sx][$sy]);
#
#				HdebugOut("対船攻撃？ Satk=${Satk} torder=${torder} thp=${thp} tsId=${tsId}");
#
#				if(($tsId > 0) && ($id != $tsId)){
#					# 他の島の所属船(無所属除く)の場合
#
#					HdebugOut("他の島の所属船(無所属除く)の場合");
#
#					my($p);
#					if($torder == 2){
#						# 防御中
#						$p = 3;
#					}elsif($torder == 1){
#						$p = 1;
#					}
#					if(random(5 - $p) == 0){
#						HdebugOut("回避");
#
#					}else{
#
#						$thp - $Satk;
#						if($thp > 0){
#							HdebugOut("生きている");
#							logShipDis($id, $name, landName($land->[$sx][$sy], 0), "($sx, $sy)","は、どこからかの攻撃によりダメージを受け");
#							$landValue->[$sx][$sy] -= $Satk;
#						}else{
#							# 倒した
#							HdebugOut("沈没");
#							logShipDis($id, $name, landName($land->[$sx][$sy], 0), "($sx, $sy)","は、どこからかの攻撃により沈没し");
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

		# 海賊船
		for ( $j = 1 ; $j < 7 ; $j++ ) {
			$sx = $x + $ax[$j];
			$sy = $y + $ay[$j];
			$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );  # 行による位置調整
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

				# 周囲に民間船がいた場合。
				next
				  if ( $sId == ( shipSpec( $landValue->[$sx][$sy] ) )[2] )
				  ;    # 同じ所属の場合
				if ( $sId > 0 ) {

					# 擬装海賊船
					my $kIsland = $Hislands[ $HidToNumber{$sId} ];
					my $tname   = $kIsland->{'name'};
					logShipDis(
						$id,
						$name,
						landName( $land->[$sx][$sy], 0 ),
						"($sx, $sy)",
"が海賊襲来により${HtagName_}${tname}${AfterName}${H_tagName}に乗っ取られ"
					);
					$landValue->[$sx][$sy] = 21000 + $sId;
				}
				else {
					logShipDis( $id, $name, landName( $land->[$sx][$sy], 0 ),
						"($sx, $sy)", "が海賊襲来により沈没し" );
					if ( random(20) == 0 ) {

						# 幽霊船
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

		# 豪華客船は流氷でも沈没(笑)
		for ( $j = 1 ; $j < 7 ; $j++ ) {
			$sx = $x + $ax[$j];
			$sy = $y + $ay[$j];
			$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );  # 行による位置調整
			next
			  if ( ( $sx < 0 )
				|| ( $sx >= $HislandSize )
				|| ( $sy < 0 )
				|| ( $sy >= $HislandSize ) );
			if ( $land->[$sx][$sy] == $HlandTitanic ) {
				next
				  if ( $sId == ( shipSpec( $landValue->[$sx][$sy] ) )[2] )
				  ;                                   # 同じ所属の場合
				logShipDis( $id, $name, landName( $land->[$sx][$sy], 0 ),
					"($sx, $sy)", "が氷山と衝突し沈没し" );
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

			# 漁船の指令が特殊の場合は拿捕
			for ( $j = 1 ; $j < 7 ; $j++ ) {
				$sx = $x + $ax[$j];
				$sy = $y + $ay[$j];
				$sx--
				  if ( !( $sy % 2 ) && ( $y % 2 ) );  # 行による位置調整
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
					  ;                               # 同じ所属の場合
					logShipDis( $id, $name, landName( $land->[$sx][$sy], 0 ),
						"($sx, $sy)", "を拿捕し" );
					$landValue->[$sx][$sy] = 21000 + $id;
					last;
				}
			}
		}
	}

	# 移動処理
	if ( $order == 3 ) {

		# 撤退
		if (   ( $x == 0 )
			|| ( $x == $HislandSize )
			|| ( $y == 0 )
			|| ( $y == $HislandSize ) )
		{

			# 撤退成功
			$land->[$x][$y]       = $land2->[$x][$y];
			$landValue->[$x][$y]  = $landValue2->[$x][$y];
			$land2->[$x][$y]      = $HlandSea;
			$landValue2->[$x][$y] = 0;
			logShipDis( $id, $name, landName( $lx, 0 ),
				"($x, $y)", "が島の領海から離れていき" );
			shipComeBack( $sId, $lx, $lvx );    # 生還処理
			return ( 100, 100 );
		}
		else {
			$i = 3;
			my (@direction) = shipEvacuation( $x, $y );
			foreach $d (@direction) {
				$sx = $x + $ax[$d];
				$sy = $y + $ay[$d];
				$sx--
				  if ( !( $sy % 2 ) && ( $y % 2 ) );  # 行による位置調整
				if ( $HseaChk[ $land->[$sx][$sy] ] == 1 ) {

					# 海系地形の場合、船系は除く
					$i = 0;
					last;
				}
			}
		}
	}
	else {
		for ( $i = 0 ; $i < 3 ; $i++ ) {

			# 船操作判定
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
			$sx-- if ( !( $sy % 2 ) && ( $y % 2 ) );  # 行による位置調整
			                                          # 範囲外判定
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

   # 海賊の場合で違う島の場合ランダムで選ばれた島に移動
					$tIsland->{'piratesend'} = $sId if ( $lx == $HlandPirate );
					logShipDis( $id, $name, landName( $lx, 0 ),
						"($x, $y)", "が島の領海から離れていき" );
					return ( 100, 100 );
				}
				next;
			}

			# 海系地形、転移装置の場合、船系は除く
			last
			  if ( ( $HseaChk[ $land->[$sx][$sy] ] == 1 )
				|| ( $land->[$sx][$sy] == $HlandWarp ) );
		}
	}

	# 動かなかった
	return ( $x, $y ) if ( $i == 3 );

	# 動いた先の地形によりメッセージ
	my ($l)     = $land->[$sx][$sy];
	my ($lv)    = $landValue->[$sx][$sy];
	my ($point) = "($sx, $sy)";

	if ( ( $l == $HlandDeathtrap ) || ( ( $l == $HlandOil ) && ( $lv == 6 ) ) )
	{

		# デストラップを踏んだ
		logShipMoveDeathtrap( $id, $name, landName( $l, $lv ), $point, $sName );
		$land->[$sx][$sy]      = $HlandSea;
		$landValue->[$sx][$sy] = 0;

		# 移動先の地形を復元
		$land->[$x][$y]       = $land2->[$x][$y];
		$landValue->[$x][$y]  = $landValue2->[$x][$y];
		$land2->[$x][$y]      = $HlandSea;
		$landValue2->[$x][$y] = 0;
		return ( 100, 100 );
	}
	elsif ( $l == $HlandWarp ) {

		# 転移装置
		logWarpMons( $id, $name, landName( $l, $lv ), $point, $sName );
		if ( warp( $id, $name, $lx, $lvx, $sName, $lv, 1 ) == 0 ) {
			$land->[$sx][$sy]      = $HlandWarp;
			$landValue->[$sx][$sy] = $lv;

		}
		else {
			logWarpMonsMiss( $id, $name, $point, landName( $l, $lv ) );
		}

		# 移動先の地形を復元
		$land->[$x][$y]       = $land2->[$x][$y];
		$landValue->[$x][$y]  = $landValue2->[$x][$y];
		$land2->[$x][$y]      = $HlandSea;
		$landValue2->[$x][$y] = 0;
		return ( 100, 100 );
	}
	if ( $order == 0 ) {

		# 指令が特殊の場合
		if (   ( ( $lx == $HlandPirate ) || ( $lx == $HlandGhostShip ) )
			&& ( $id != $sId ) )
		{

			# 海賊船、幽霊船は略奪
			if (   ( ( $l == $HlandOil ) && ( $lv >= 10 ) )
				|| ( ( $l == $HlandSea ) && ( $lv >= 10 ) ) )
			{

				# 海底都市、海底農場、養殖場
				if ( $sId > 0 ) {
					my ($sIsland) = $Hislands[ $HidToNumber{$sId} ];
					if ( ( $l == $HlandOil ) && ( $lv < 35 ) ) {

						# 海底農場
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

				# 養殖場のとき１
				$lv = ( $l == $HlandSea ) ? 1 : 0;
				$l = $HlandSea;
			}
		}
		elsif ( $lx == $HlandProbeShip ) {

			# 海底探査船
			my ($p) = random(100);
			if ( $p < 3 ) {
				if ( $land2->[$x][$y] != $HlandOil ) {
					$land2->[$x][$y]      = $HlandOil;
					$landValue2->[$x][$y] = 0;
					logOut(
"${HtagName_}${name}${AfterName}($x, $y)${H_tagName}で<B>油田</B>が発見されたようです。",
						$id
					);
				}
			}
			elsif ( $p == 81 ) {

				# シーいのら
				$land2->[$x][$y]      = $HlandMonster;
				$landValue2->[$x][$y] = 905;
				logMonsCome( $id, $name, ( monsterSpec(905) )[1],
					"($x, $y)", landName( $HlandSea, 0 ) );
			}
			elsif ( $p == 82 ) {

				# シーゴースト
				$land2->[$x][$y]      = $HlandMonster;
				$landValue2->[$x][$y] = 2105;
				logMonsCome( $id, $name, ( monsterSpec(2105) )[1],
					"($x, $y)", landName( $HlandSea, 0 ) );
			}
			elsif ( $p == 83 ) {

				# 噴火(制裁ロジックを利用)
				$HpunishInfo{$id}->{punish} = 8;
				$HpunishInfo{$id}->{x}      = $x;
				$HpunishInfo{$id}->{y}      = $y;
			}
		}
	}

	# 行き先の地形を保存し移動
	$land2->[$sx][$sy]      = $l;
	$landValue2->[$sx][$sy] = $lv;

	$land->[$sx][$sy]      = $land->[$x][$y];
	$landValue->[$sx][$sy] = $landValue->[$x][$y];

	# もと居た地形を復元
	$land->[$x][$y]       = $land2->[$x][$y];
	$landValue->[$x][$y]  = $landValue2->[$x][$y];
	$land2->[$x][$y]      = $HlandSea;
	$landValue2->[$x][$y] = 0;

	# うざいので表示しない
	#	if($order < 100){
	#		# 移動ログ
	#		logShipMove($id, $name, landName($l, $lv), $point, $sName);
	#	}

	return ( $sx, $sy );
}

# 船生還処理
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

# 転移
# 島のID  名前  転送してきた地形 値  転送物名  ターゲットID  転送物の種類
sub warp {
	my ( $id, $name, $land, $landValue, $mName, $tid, $z ) = @_;

	# ターゲット取得
	my ($tn) = $HidToNumber{$tid};
	return 0 if ( $tn eq '' );
	my ($tIsland) = $Hislands[$tn];

	# 相手が途上国の為中止
	return 0
	  if ( ( $tIsland->{'turnsu'} + $tIsland->{'evil'} < $HdisUN )
		|| ( $tIsland->{'evil'} == 0 ) );

	my ( $tName, $tLand, $tLandValue ) =
	  ( $tIsland->{'name'}, $tIsland->{'land'}, $tIsland->{'landValue'} );

	# ワープ先に転移装置があるかサーチ
	my ( $count, $x, $y, $tx, $ty, $i, $j );
	for ( $count = 0 ; $count < $HpointNumber ; $count++ ) {
		$x = $Hrpx[$count];
		$y = $Hrpy[$count];
		if (   ( $tLand->[$x][$y] == $HlandWarp )
			|| ( $tLand->[$x][$y] == $HlandWarpR ) )
		{

			#  転移装置発見したので周囲の障害物をサーチ

			# 転移先装置の場合は方向を指定できる
			$j =
			  ( $tLand->[$x][$y] == $HlandWarpR ) ? $tLandValue->[$x][$y] : 1;

			for ( $i = $j ; $i < 61 ; $i++ ) {
				$tx = $x + $ax[$i];
				$ty = $y + $ay[$i];
				$tx--
				  if ( !( $ty % 2 ) && ( $y % 2 ) );  # 行による位置調整
				                                      # 範囲内外チェック
				next
				  if ( ( $tx < 0 )
					|| ( $tx >= $HislandSize )
					|| ( $ty < 0 )
					|| ( $ty >= $HislandSize ) );
				if ( $z > 10 ) {                      # 怪獣、船系以外
					$x = $tx;
					$y = $ty;
					last;
				}
				elsif ( $i > 6 )
				{    # 周囲に転送できない時は転送失敗
					return 1;
				}
				if ( $z == 1 ) {

					# 船系は海系地形、船系は除く
					if ( $HseaChk[ $tLand->[$tx][$ty] ] == 1 ) {
						$x = $tx;
						$y = $ty;
						last;
					}
				}
				else {

					# 海系、怪獣、山、記念碑以外
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

	# 転移装置がなかった場合のワープ先はランダム
	if ( $count >= $HpointNumber ) {
		$x = random($HislandSize);
		$y = random($HislandSize);
	}
	if ( $z < 10 ) {    # 怪獣,船系
		logMWarp( $id, $tid, $name, $tName, "($x, $y)", $mName );
		$tLand->[$x][$y]      = $land;
		$tLandValue->[$x][$y] = $landValue;
	}
	elsif ( $z == 11 ) {    # ミサイル
		logMWarp( $id, $tid, $name, $tName, "($x, $y)", "ミサイル" );
		$tLand->[$x][$y]      = $HlandSea;
		$tLandValue->[$x][$y] = 0;
	}
	elsif ( $z == 12 ) {    # 隕石
		logMWarp( $id, $tid, $name, $tName, "($x, $y)", $mName );
		$tLand->[$x][$y]      = $HlandSea;
		$tLandValue->[$x][$y] = 0;
	}
	return 0;
}

# 0から(n - 1)までの数字が一回づつ出てくる数列を作る
sub randomArray {
	my ($n) = @_;
	my ( @list, $i );

	# 初期値
	$n    = 1 if ( $n == 0 );
	@list = ( 0 .. $n - 1 );

	# シャッフル
	for ( $i = $n ; --$i ; ) {
		my ($j) = int( rand( $i + 1 ) );
		next if ( $i == $j );
		@list[ $i, $j ] = @list[ $j, $i ];
	}

	return @list;
}

# neo_otacky氏が作成
sub islandReki {
	my ( $line, $i, $id, $pop, $turn, $name, $n, $island, @rekidai, $reki );
	my $j = 0;

	if ( !open( RIN, "<${HlogdirName}/rekidai.dat" ) ) {
		rename( "${HlogdirName}/rekidai.tmp", "${HlogdirName}/rekidai.dat" );
		if ( !open( RIN, "${HlogdirName}/rekidai.dat" ) ) {
			open( ROUT, ">${HlogdirName}/rekidai.tmp" );
			for ( $i = 0 ; $i < $HislandNumber ; $i++ )
			{    # 現存する島すべてを記録
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

	# 人口が同じときは直前のターンの順番のまま
	my @idx = ( 0 .. $#rekidai );
	@idx =
	  sort { $rekidai[$b]->{'pop'} <=> $rekidai[$a]->{'pop'} || $a <=> $b }
	  @idx;
	@rekidai = @rekidai[@idx];

	open( ROUT, ">${HlogdirName}/rekidai.tmp" );
	my $recordNo = ( $HmaxIsland < 15 ) ? 15 : $HmaxIsland;
	for ( $i = 0 ; $i < $recordNo ; $i++ )
	{    # 最大で島の最大数と同じだけ記録。最低で15島。
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
# 簡易トーナメント
# 対戦の記録ログ
sub fihgt_log {
	open( FOUT, "${HdirName}/fight.log" );
	my ( $f, @offset );
	while ( $f = <FOUT> ) {
		chomp($f);
		push( @offset, "$f\n" );
	}
	close(FOUT);
	my $fight;

	# 回戦数数代入
	my $fTurn = $HislandFightCount;

	# 決勝戦の場合99にする
	$fTurn = 99 if ( $HislandFightMode == 9 );

	open( DOUT, ">$HdirName/fight.log.bak" );
	print DOUT "<${fTurn}>\n";
	print DOUT "<TABLE BORDER>\n";
	print DOUT
"<tr><TH colspan=3></th><th $HbgTitleCell colspan=1>${HtagTH_}勝者${H_tagTH}</th><TH colspan=1></th>\n";
	print DOUT
	  "<TH $HbgTitleCell colspan=1>${HtagTH_}敗者${H_tagTH}</th></tr>\n";
	print DOUT "<TR>\n";
	print DOUT
"<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}勝者${H_tagTH}</NOBR></TH>\n";
	print DOUT
"<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}敗者${H_tagTH}</NOBR></TH>\n";

#	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}飛来ミ数${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell width=15 nowrap=nowrap>　</TH>\n";

#	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}報酬金${H_tagTH}</NOBR></TH>\n";
	print DOUT
"<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>\n";

#	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}破壊ミ基数${H_tagTH}</NOBR></TH>\n";
#	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}破壊防施数${H_tagTH}</NOBR></TH>\n";
	print DOUT "<TH $HbgTitleCell width=15 nowrap=nowrap>　</TH>\n";
	print DOUT
"<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>\n";

#	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}破壊ミ基数${H_tagTH}</NOBR></TH>\n";
#	print DOUT "<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}破壊防施数${H_tagTH}</NOBR></TH>\n";
	print DOUT "</tr>\n";

	foreach $fight (@fight_log_flag) {
		my ( $name, $tName, $reward, $log, $pop, $tLog, $tPop, $fly, $id ) =
		  split( ",", $fight );
		$logD  = int( $log / 1000 ) . "機";
		$logM  = ( $log - $logD * 1000 ) . "機";
		$tLogD = int( $tLog / 1000 ) . "機";
		$tLogM = ( $tLog - $tLogD * 1000 ) . "機";

#		$tName	= "<A STYlE=\"text-decoration:none\" HREF=\"".$HthisFile."?LoseMap=".$id."\">".
#					$HtagName2_.$tName."${AfterName}".$H_tagName2."</A>";
		$tName = "${HtagName2_}$tName$AfterName${H_tagName2}";
		$tPop .= ${HunitPop};
		if ( $id == -1 ) {
			$tName = "${HtagName2_}不戦勝${H_tagName2}";
			$tPop  = "−";
			$tLogM = "−";
			$tLogD = "−";
		}
		elsif ( $id == -2 ) {
			$tName = "${HtagName2_}沈没${H_tagName2}";
			$tPop  = "−";
			$tLogM = "−";
			$tLogD = "−";
		}
		print DOUT
"<TR><TD $HbgInfoCell align=right><NOBR>${HtagName_}${name}${AfterName}${H_tagName}</nobr></td>";
		print DOUT "<TD $HbgInfoCell align=center><NOBR>${tName}</nobr></td>\n";

		#		print DOUT "<TH $HbgInfoCell><NOBR>${fly}発</nobr></TH>\n";
		print DOUT "<TD $HbgInfoCell><NOBR>　</nobr></td>\n";

	#		print DOUT "<TH $HbgInfoCell><NOBR>${reward}${HunitMoney}</nobr></TH>\n";
		print DOUT "<TH $HbgInfoCell><NOBR>${pop}${HunitPop}</nobr></TH>\n";

		#		print DOUT "<TH $HbgInfoCell><NOBR>${logM}</nobr></TH>\n";
		#		print DOUT "<TH $HbgInfoCell><NOBR>${logD}</nobr></TH>\n";
		print DOUT "<TD $HbgInfoCell><NOBR>　</nobr></td>\n";
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

# 予選落ちログ
sub log_yosen {
	my $yosen;
	open( DOUT, ">${HdirName}/fight.log" );
	print DOUT "<0>\n";
	print DOUT "<TABLE BORDER>\n";
	print DOUT "<TR>\n";
	print DOUT
"<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}${AfterName}${H_tagTH}</NOBR></TH>\n";
	print DOUT
"<TH $HbgTitleCell nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH></tr>";
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

# 勝利ログ
sub logWin {
	my ( $id, $name, $str, $money ) = @_;
	my $fTurn = $HislandFightCount + 1;
	if ( $HislandNumber <= 4 ) {
		$fTurn = '決勝戦';
	}
	elsif ( $HislandNumber <= 8 ) {
		$fTurn = '準決勝';
	}
	else {
		$fTurn .= '回戦';
	}
	if ( $HislandNumber == 2 ) {
		logOut(
"${HtagName_}${name}${AfterName}${H_tagName}${str}し、<B>優勝！！</B>",
			$id
		);
		logHistory(
			"${HtagName_}${name}${AfterName}${H_tagName}、<B>優勝！！</B>"
		);
	}
	elsif ( $money == 0 ) {
		logOut(
"${HtagName_}${name}${AfterName}${H_tagName}${str}し、<B>$fTurn進出！</B>",
			$id
		);
	}
	else {
		logOut(
"${HtagName_}${name}${AfterName}${H_tagName}${str}し、<B>$fTurn進出！　$money$HunitMoney</B>の報酬金が支払われました。",
			$id
		);
	}
}

# 予選落ち
sub logLoseOut {
	my ( $id, $name ) = @_;
	logOut(
		"${HtagName_}${name}${AfterName}${H_tagName}、<B>予選落ち</B>。",
		$id
	);
	logHistory(
"${HtagName_}${name}${AfterName}${H_tagName}、<B>予選落ちで沈没</B>。"
	);
}

#------------------------------------------------

1;
