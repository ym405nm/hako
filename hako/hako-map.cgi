#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 地図モードモジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 究想の箱庭  (ver5.53b)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# 開発に使う定数
#----------------------------------------------------------------------

$HcommandTotal = 107; # コマンドの種類

# 順番
@HcomList =
    ($HcomPrepare, $HcomPrepare2, $HcomReclaim, $HcomReclaim2, $HcomDestroy, $HcomDestroy2, $HcomSearch,
     $HcomSellTree, $HcomPlant, $HcomBank, $HcomPioneer, $HcomFarm, $HcomFactory, $HcomMountain,
     $HcomBase, $HcomDbase, $HcomSbase, $HcomMonument, $HcomSMonument, $HcomShipbuild, $HcomDokan,$HcomUg, $HcomHaribote,
     $HcomScity, $HcomSFarm, $HcomTower, $HcomPort, $HcomBreakwater, $HcomFire, $HcomWindmill, $HcomMyhome, $HcomPolice, $HcomHospital,
     $HcomPresent, $HcomPresentAid, $HcomWarp, $HcomDeathtrap, $HcomTrump, $HcomFlower,
     $HcomManipulate, $HcomSTManipulate, $HcomSpy, $HcomTeisatu, $Hcomcolony, $HcomShip, $HcomShipM,
     $HcomShipSell, $HcomBioMissile, $HcomMissileNM, $HcomMissilePP, $HcomMissileSPP, $HcomMissileRNG,
     $HcomMissileST, $HcomMissileLD, $HcomSendMonster, $HcomSSendMonster,
     $HcomMissileRM, $HcomMissileSRM ,$HcomMissileGM, $HcomMissileMGM, $HcomMissileDM,
     $HcomMissilePLD, $HcomMissileNCM, $HcomDummy, $HcomDoNothing,
     $HcomMonsEgg,$HcomMonsEsa,$HcomMonsEnsei,$HcomMonsTettai,$HcomMonsEsaAid,$HcomMonsAid,$HcomMonsSell,$HcomMonsExer,
     $HcomSUnit,$HcomSPioneer,$HcomSBuild,$HcomSpaceFarm,$HcomSFactory,$HcomSpaceBase,$HcomSDbase,$HcomSEisei,
     $HcomSMissileGM,$HcomSMissilePP,$HcomSMissile,$HcomSMissileMGM,$HcomSOccupy,$HcomSFood,$HcomSDestroy,
     $HcomOMissileNM,$HcomOMissilePP,$HcomOMissileSPP,
     $HcomSell,$HcomOreSell,$HcomOilSell,$HcomWeponSell,
     $HcomOreBuy,$HcomOilBuy,$HcomWeponBuy, #購入命令
     $HcomMoney, $HcomFood, $HcomEmigration, $HcomPropaganda, $HcomGiveup,
     $HcomAutoPrepare, $HcomAutoPrepare2, $HcomAutoSellTree, $HcomAutoDelete);

if($Hbuycommand){
	# 資源購入系命令を削除
	splice(@HcomList,95,3);# 命令増えたらずれるので注意
	$HcommandTotal -= 3;
}

$HcomMsg[$HcomPrepare]   = '荒地、建物系を平地にします。(海底系は海)';
$HcomMsg[$HcomPrepare2]  = 'ターン消費なしの整地、たくさんやるほど地震の確率が上昇';
$HcomMsg[$HcomReclaim]   = '海→浅瀬→荒地。陸の周囲のみ可能です。周りに養殖場があるときは注意';
$HcomMsg[$HcomReclaim2]  = 'ターン消費なしの埋め立て、たくさんやるほど地震の確率が上昇';
$HcomMsg[$HcomDestroy]   = '荒地、平地、町系で数量指定すると温泉掘削';
$HcomMsg[$HcomDestroy2]  = 'ターン消費なしの掘削、たくさんやるほど地震の確率が上昇';
$HcomMsg[$HcomSearch]    = '荒地、平地、町系で実行可能、鉱脈などが発見できます';
$HcomMsg[$HcomSellTree]  = 'ターン消費無し、森(平地に変化)、養殖場(浅瀬に変化)で実行可能';
$HcomMsg[$HcomPlant]     = '平地、町系で実行可能、浅瀬にやると養殖場';
$HcomMsg[$HcomBank]      = '利子が毎ターン入る。預けた金は戻らない(まれに倒産)';
$HcomMsg[$HcomPioneer]   = '平地に村ができる';
$HcomMsg[$HcomFarm]      = '食糧を作る職場。最大5万。(複数可)';
$HcomMsg[$HcomFactory]   = '最大10万(複数可)';
$HcomMsg[$HcomMountain]  = '災害に強い、最大20万(複数可)';
$HcomMsg[$HcomPresent]   = 'プレゼントがないと建設不可。0公園.1スタジアム.2ドーム.3カジノ.4遊園地.5学校.6空港.7大都市.8動物園.9博覧会.10怪獣記念碑.11災害の碑';
$HcomMsg[$HcomPresentAid]= 'プレゼントがないと不可。0公園.1スタジアム.2ドーム.3カジノ.4遊園地.5学校.6空港.7大都市.8動物園.9博覧会.10怪獣記念碑.11災害の碑';
$HcomMsg[$HcomBase]      = 'ミサイルを撃つのに必要、EX20までは追加建設で5増えます。それ以降は1';
$HcomMsg[$HcomDbase]     = '周囲２マスのミサイルを防ぐ(自身を除く)、海にもつくれます(海は火災で燃える)';
$HcomMsg[$HcomSbase]     = '海にミサイル基地を作る';
$HcomMsg[$HcomMonument]  = 'ミサイル基地に作るとロケット台に';
$HcomMsg[$HcomSMonument] = '海底版の記念碑です。海底に建設します。追加建設するとやっぱり飛びます＾＾';
$HcomMsg[$HcomHaribote]  = '見た目が防衛施設、視覚効果以外意味無し';
$HcomMsg[$HcomScity]     = '海に作る火災で燃える、食糧を倍消費';
$HcomMsg[$HcomSFarm]     = '海に作る火災で燃える、最大3万(複数可)';
$HcomMsg[$HcomTower]     = '災害に強い、最大20万(複数可)';
$HcomMsg[$HcomFire]      = '範囲２で火災を防ぐ(自身を除く)、海にも作れる(陸は陸の施設、海は海の施設にしか効果無し）';
$HcomMsg[$HcomWindmill]  = '周囲１へクスの農場(陸)の生産量を２倍、維持費１０億';
$HcomMsg[$HcomMyhome]    = '追加建設を行うと耐久力が増します。島に一つしか作れません';
$HcomMsg[$HcomPort]      = '工業系の職場。初期値４万規模で追加建設ごと２万増、最大２０万(複数可)';
$HcomMsg[$HcomPolice]    = '１つでも建設すると犯罪多発が全く起きなくなります。維持費が毎ターン５億で火災で燃えます。';
$HcomMsg[$HcomHospital]  = '１つでも建設すると効果があります。維持費が毎ターン５億で火災で燃えます。';
$HcomMsg[$HcomTrump]     = 'やることが無くなった人用のイベント地形です。詳しくは説明書をよんでね。';
$HcomMsg[$HcomFlower]    = 'ランダムでお花が生えます。何も効果はありません。';
$HcomMsg[$HcomBreakwater]= '浅瀬に津波対策の防波堤を建設';
$HcomMsg[$HcomDokan]     = '地下の入り口建設';
$HcomMsg[$HcomUg]        = '地下建設、数値指定';
$HcomMsg[$HcomShipbuild] = '港から２マス以内の浅瀬で実行できる。範囲内の漁船に追加実行できる。';
$HcomMsg[$HcomManipulate]= '数量で方向指定、複数いる時は硬化してないすべての怪獣が対象';
$HcomMsg[$HcomSTManipulate]= 'ログに島名が表示されない';
$HcomMsg[$HcomSpy]       = '他の島に地震、アルミ箔散布、食料の焼き討ちなどを行う';
$HcomMsg[$HcomTeisatu]   = '他の島の指定座標とその周囲３ヘクスの地形調査';
$HcomMsg[$HcomWarp]      = 'ここに乗ったもの、落ちたものを任意の島に転移させる。1回で壊れる。';
$HcomMsg[$HcomDeathtrap] = '進入してきた怪獣にダメージを与える、または倒す。追加建設可能、海にも作れる。';
$HcomMsg[$Hcomcolony]    = '宇宙賞を取ってないとできない。座標を指定できませんがこの箱庭最強兵器です。';
$HcomMsg[$HcomBioMissile]= '誤差１、落ちた所が汚染します。';
$HcomMsg[$HcomMissileNM] = '誤差２';
$HcomMsg[$HcomMissilePP] = '誤差１';
$HcomMsg[$HcomMissileSPP]= '誤差１、中心２倍';
$HcomMsg[$HcomMissileST] = '誤差２、むやみに撃つのはやめましょう';
$HcomMsg[$HcomMissileLD] = '誤差２、陸破壊(山→荒地→浅瀬→海)';
$HcomMsg[$HcomMissileRNG] = '絶対に誤差３固定';
$HcomMsg[$HcomSendMonster]='数量を１メカジラ、２グラテネスいのら、３海底メカいのら';
$HcomMsg[$HcomSSendMonster]='数量指定で任意の怪獣を派遣します。';
$HcomMsg[$HcomMissileRM] = '海→浅瀬→荒地に、陸地限界値の時は効果無し';
$HcomMsg[$HcomMissileSRM]= '山は出来ません。';
$HcomMsg[$HcomMissileGM] = '誤差なし、１発しか撃てません';
$HcomMsg[$HcomMissileMGM]= '怪獣に自動で向かっていく、複数時ランダム';
$HcomMsg[$HcomMissileDM] = '誤差３';
$HcomMsg[$HcomMissileNCM]= '1発で10発分消費、ミサイル数30未満の島へは不可。誤差４の巨大隕石落としプラス汚染';
$HcomMsg[$HcomMissilePLD]= '誤差１の陸地破壊弾です';
$HcomMsg[$HcomDummy]     = 'ST系と併用しましょう';
$HcomMsg[$HcomShip]      = '0特殊(一部の船系のみ)、1移動、2防御(自然回復)、3撤退、4攻撃';
$HcomMsg[$HcomShipM]     = '数量で方向指定、防御、撤退を除いたターゲットの自島所属の船全てが対象です。';
$HcomMsg[$HcomShipSell]  = 'ターン消費なし、自所属の船を売ります。売ると海になります。値段は説明書参照。';
$HcomMsg[$HcomDoNothing] = '10億入ります';
$HcomMsg[$HcomSell]      = 'ターン消費なし';
$HcomMsg[$HcomOreSell]   = 'ターン消費なし';
$HcomMsg[$HcomOilSell]   = 'ターン消費なし';
$HcomMsg[$HcomWeponSell] = 'ターン消費なし';
$HcomMsg[$HcomOreBuy]    = 'ターン消費有り';
$HcomMsg[$HcomOilBuy]    = 'ターン消費有り';
$HcomMsg[$HcomWeponBuy]  = 'ターン消費有り';
$HcomMsg[$HcomMoney]     = 'ターン消費なし';
$HcomMsg[$HcomFood]      = 'ターン消費なし';
$HcomMsg[$HcomEmigration]= '1回までターン消費なし、町を指定する';
$HcomMsg[$HcomPropaganda]= '人口が増えます(複数可)';
$HcomMsg[$HcomMonsEgg]   = '怪獣コマンド、怪獣バトルするにはこれを買いましょう。';
$HcomMsg[$HcomMonsEsa]   = '怪獣コマンド、倒した怪獣の残骸を食べさせて進化させましょう。';
$HcomMsg[$HcomMonsEnsei] = '怪獣コマンド、どんどん戦わせて強くさせましょう。';
$HcomMsg[$HcomMonsTettai]= '怪獣コマンド、ターン消費なし、逃げても負けです。攻められているときは相手に帰ってもらいます。';
$HcomMsg[$HcomMonsEsaAid]= '怪獣コマンド、ターン消費なし、自分のストック餌を譲渡します。ただし相手の餌が無い時のみ';
$HcomMsg[$HcomMonsAid]   = '怪獣コマンド、ターン消費なし、自分の怪獣を譲渡します。ただし相手に怪獣がいないときのみ';
$HcomMsg[$HcomMonsSell]  = '怪獣コマンド、ターン消費なし、（勝数＋１）×　１０００億で売ります。売ると２度と復活しません。';
$HcomMsg[$HcomMonsExer]  = '怪獣コマンド、餌を使用し怪獣を訓練します。餌を空にしたいときに使う。餌による訓練の差は無し。';

$HcomMsg[$HcomSUnit]      = '宇宙コマンド、追加建設可、何も無い空間から建造物、町系の土台を作成します。３回行う必要があります。';
$HcomMsg[$HcomSMissileGM] = '宇宙コマンド、誤差無しのミサイルを撃ちます。宇宙ミサイル基地が必要です。';
$HcomMsg[$HcomSMissilePP] = '宇宙コマンド、誤差１のミサイルを撃ちます。宇宙ミサイル基地が必要です。';
$HcomMsg[$HcomSMissile]   = '宇宙コマンド、誤差２のミサイルを撃ちます。宇宙ミサイル基地が必要です。';
$HcomMsg[$HcomSMissileMGM]= '宇宙コマンド、１発のみで怪獣に自動で向かっていく、複数時ランダム。';
$HcomMsg[$HcomSOccupy]  = '宇宙コマンド、占領を行い自島所属にします。条件等は説明書確認。';
$HcomMsg[$HcomSFood]    = '宇宙コマンド、宇宙ユニットに村を作成します。';
$HcomMsg[$HcomSPioneer] = '宇宙コマンド、宇宙ユニットに村を作成します。';
$HcomMsg[$HcomSBuild]   = '宇宙コマンド、(使用しないこと)';
$HcomMsg[$HcomSpaceFarm]= '宇宙コマンド、追加建設可、農場を建設。';
$HcomMsg[$HcomSFactory] = '宇宙コマンド、追加建設可、工場を建設。';
$HcomMsg[$HcomSpaceBase]= '宇宙コマンド、追加建設可、宇宙ミ基地を建設。追加建設で経験値稼ぎ';
$HcomMsg[$HcomSDbase]   = '宇宙コマンド、周囲２マスのミサイルを防ぐ(自身を除く)';
$HcomMsg[$HcomSEisei]   = '宇宙コマンド、追加建設可、様々な効果があります。';
$HcomMsg[$HcomSDestroy] = '宇宙コマンド、自島、無所属地形の１マスを虚無に戻す。自島の場合はターン消費なし';

$HcomMsg[$HcomOMissileNM]    = '';
$HcomMsg[$HcomOMissilePP]    = '';
$HcomMsg[$HcomOMissileSPP]   = '';

$HcomMsg[$HcomGiveup]        = '島がなくなります';
$HcomMsg[$HcomAutoPrepare]   = '今ある荒地にすべて整地をセット';
$HcomMsg[$HcomAutoPrepare2]  = '今ある荒地にすべて地ならしをセット';
$HcomMsg[$HcomAutoSellTree]  = '数量の数(単位百)より少ない森が対象';
$HcomMsg[$HcomAutoDelete]    = '計画を全て入れなおしたい時に';

#----------------------------------------------------------------------
# 観光モード
#----------------------------------------------------------------------
# メイン

sub printIslandMain {
	# 開放

	unlock();

	# idから島番号を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID}; # 相手

	# なぜかその島がない場合

	if($HcurrentNumber eq '') {
		tempProblem();
		return;
	}

	# 名前の取得
	$HcurrentName = $Hislands[$HcurrentNumber]->{'name'};

	$HcurrentNumber2 = $HidToNumber{$HprintID}; # 観光しにいく本人
	$HprintAlly = 0;
	if($HcurrentNumber2 eq '') {
		$HprintID = 0;
	}else{
		my($chkpass) = $Hislands[$HcurrentNumber2]->{'password'};
		if(!checkPassword($chkpass,$HinputPassword)) {
			# passwordが違う
			$HprintID = 0;
		}else{
			$HprintAlly = $Hislands[$HcurrentNumber2]->{'ally'};
		}
	}

	# 観光画面
	if($Hislands[$HcurrentNumber]->{'id'} > 90){
		# Battle Fieldのとき
		$HmainMode = 'bfield';
		tempPrintIslandHead("(Battle Field)"); # ようこそ!!
		tempNavi();
	}else{
		tempPrintIslandHead(); # ようこそ!!
		tempNavi();
	}
	
	islandInfo(); # 島の情報

	islandMap(0, $HprintID); # 島の地図、観光モード
	ugMap($island,0);	# 地下
	islandJamp();   # 島の移動
	islandmonster(2);# 島の怪獣

	tempLocalbbs(0);	# ローカル掲示板
	tempRecent(0);		# 近況
	tempMapTotal();		# マップ集計
}

#----------------------------------------------------------------------
# 開発モード
#----------------------------------------------------------------------
# メイン

sub ownerMain {
	# 開放

	unlock();

	# モードを明示
	$HmainMode = 'owner';

	# idから島を取得
	if($HcurrentID < 1){
		tempWrongPassword();
		Dummyfunction() if($HjavaMode eq 'java');
		return;
	}
	
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# パスワード
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password間違い
		tempWrongPassword();
		Dummyfunction() if($HjavaMode eq 'java');
		return;
	}

	if($Htournament){
		# 簡易トーナメント
		my $tName = $HidToName{$island->{'fight_id'}};
		if($tName eq ''){
			# 無し
		}else{
			# 有り
			$HtargetList = "<OPTION VALUE=\"$island->{'fight_id'}\">${tName}${AfterName}\n";
			$HtargetList .= "<OPTION VALUE=\"$island->{'id'}\">${HcurrentName}${AfterName}\n";
		}
	}

	# 開発画面
	if($HjavaMode eq 'java') {
		tempOwnerJava(); # 「Javaスクリプト開発計画」
	}else{
		tempOwner();     # 「通常モード開発計画」
	}

	if($island->{'order'} & 256){
		tempCLbbs();
	}else{
		ugMap($island,2);	# 地下
		if($island->{'order'} & 64){
			tempLocalbbs(1);	# ローカル掲示板
			tempRecent(1);		# 近況
		}else{
			tempRecent(1);		# 近況
			tempLocalbbs(1);	# ローカル掲示板
		}
		tempCommentInput();	# コメント入力フォーム

		tempMapTotal();		# マップ集計
	}
}
#----------------------------------------------------------------------
# 宇宙マップ表示
#----------------------------------------------------------------------
sub spaceMap {
	unlock();# 開放


	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}「<ruby><rb>宇宙<rp>（<rt>そら<rp>）</ruby>マップ」${H_tagName}${H_tagBig}(各島共有)<BR>
$HtempBack<BR>
</CENTER>
END
	$HcurrentID = 999;
	$HcurrentName = $SpaceName;
	tempNavi(3);
	spaceInfo();  # 島の情報

	$sAfterName = $AfterName;
	$AfterName = "";
	islandMap(3); # 島の地図、宇宙モード
	spaceInfo2(); # 島の情報


	tempLocalbbs(3);	# ローカル掲示板
	tempRecent(0);		# 近況
	tempMapTotal();		# マップ集計
}
#----------------------------------------------------------------------
# 海域マップ表示
#----------------------------------------------------------------------
sub oceanMap {
	unlock();# 開放


	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}「海域マップ」${H_tagName}${H_tagBig}(各島共有)<BR>
$HtempBack<BR>
</CENTER>
END
	$HcurrentID = 888;
	$HcurrentName = $OceanName;
	tempNavi(4);
#	spaceInfo();  # 島の情報

	$sAfterName = $AfterName;
	$AfterName = "";
	$HislandSize = $HoceanSize;
	islandMap(4); # 島の地図
	
	tempLocalbbs(4);	# ローカル掲示板
	tempRecent(0);		# 近況
	tempMapTotal();		# マップ集計
}

#----------------------------------------------------------------------
# コマンドモード
#----------------------------------------------------------------------
# メイン

sub commandMain {
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
	
	my($tempCommandFlag);

	if($HcommandMode eq 'delete') {
		slideFront($command, $HcommandPlanNumber);
		$tempCommandFlag = 0;
	} elsif(($HcommandKind == $HcomAutoPrepare) ||
		($HcommandKind == $HcomAutoPrepare2) ||
		($HcommandKind == $HcomAutoSellTree)) {

		# フル整地、フル地ならし、フル伐採
		# 座標配列を作る

		makeRandomPointArray();
		my($land) = $island->{'land'};
		my($landValue) = $island->{'landValue'};

		my($Arg) = $HcommandArg;
		$Arg = 1 if($Arg == 0);

		# コマンドの種類決定

		my($kind) = $HcomPrepare;
		if($HcommandKind == $HcomAutoPrepare2) {
			$kind = $HcomPrepare2;
		} elsif($HcommandKind == $HcomAutoSellTree) {
			$kind = $HcomSellTree;
		}

		my($i,$j) = (0,0);
		while(($j < $HpointNumber) && ($i < $HcommandMax)) {
			my($x) = $Hrpx[$j];
			my($y) = $Hrpy[$j];
			my($landKind) = $land->[$x][$y];
			my($lv) = $landValue->[$x][$y];
			if($landKind == $HlandMonster) {
				if((monsterSpec($lv))[0] == 26){
					# 迷彩いのら

					$landKind = $HlandWaste;
					$lv = 0;
				}
			}
			if((($kind == $HcomSellTree) &&



				(($landKind == $HlandForest) && ($lv <= $Arg))) ||
				((($kind == $HcomPrepare) || ($kind == $HcomPrepare2)) &&
				(($landKind == $HlandWaste) && ($lv <= 1)))) {
				slideBack($command, $HcommandPlanNumber, $kind, 0, $x, $y, 0);
				$i++;
			}
			$j++;
		}
		$tempCommandFlag = 1;
	} elsif($HcommandKind == $HcomAutoDelete) {
		# 全消し
		my($i);
		for($i = 0; $i < $HcommandMax; $i++) {
			slideFront($command, $HcommandPlanNumber);
		}
		$tempCommandFlag = 0;
	} else {
		slideBack($command, $HcommandPlanNumber, 0) if($HcommandMode eq 'insert');
		$tempCommandFlag = 1;
		# コマンドを登録
		$command->[$HcommandPlanNumber] = {
			'kind' => $HcommandKind,
			'target' => $HcommandTarget,
			'x' => $HcommandX,
			'y' => $HcommandY,
			'arg' => $HcommandArg,
			'tx' => $HcommandTX,
			'ty' => $HcommandTY
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

	if($tempCommandFlag) {
		tempCommandAdd();
	} else {
		tempCommandDelete();
	}

	# owner modeへ
	ownerMain();

}

#----------------------------------------------------------------------
# コメント入力モード
#----------------------------------------------------------------------
# メイン

sub commentMain {
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

	# メッセージを更新
	$island->{'comment'} = htmlEscape($Hmessage);
	$island->{'commentLabel0'} = "$HcommentLabel0";
	$island->{'commentLabel1'} = "$HcommentLabel1";
	$island->{'commentLabel2'} = "$HcommentLabel2";
	$island->{'commentLabel3'} = "$HcommentLabel3";
	$island->{'commentLabel4'} = "$HcommentLabel4";

	# データの書き出し
	if(!writeIslandsFile($HcurrentID, 1)) {
		unlock();
		tempFailWrite();
		return;
	}

	# コメント更新メッセージ
	tempComment();

	# owner modeへ
	ownerMain();
}

#----------------------------------------------------------------------
# ローカル掲示板モード
#----------------------------------------------------------------------
# メイン


sub localBbsMain {
	# idから島番号を取得
	my($island, $foreignName,$wmode);
	my($speaker) = "0<";
	if($HcurrentID == 999){
		$island = $Hspace;
		$wmode = 3;
	}elsif($HcurrentID == 888){
		$island = $Hocean;
		$wmode = 4;
	}else{
		$HcurrentNumber = $HidToNumber{$HcurrentID};
		$island = $Hislands[$HcurrentNumber];
		# なぜかその島がない場合

		if($HcurrentNumber eq '') {
			unlock();
			tempProblem();
			return;
		}
		$wmode = 2;
	}

	# 削除モードじゃなくて名前かメッセージがない場合

	if(($HlbbsMode == 0) && ($HlbbsMode == 1) && ($HlbbsMode == 3)){
		if(($HlbbsName eq '') || ($HlbbsMessage eq '')) {
			unlock();
			tempLbbsNoMessage();
			return;
		}
	}

	# 観光者モードじゃない時はパスワードチェック
	if($HlbbsMode != 0) {
		if (($HlbbsMode == 3) || ($HlbbsMode == 4)) {
			# 外国者モード
			my($foreignNumber) = $HidToNumber{$HforeignerID};
			if ($foreignNumber eq '') {
				unlock();
				tempProblem();
				return;
			}
			my($foreignIsland) = $Hislands[$foreignNumber];
			if($HlbbsType eq 'ANON'){
				$foreignName = '匿名';
			} else {
				my $passCheck = checkPasslocalbbs($foreignIsland->{'password'},$HinputPassword);
				if($passCheck == 0) {
					unlock();
					tempWrongPassword();
					return;
				} elsif($passCheck == 3) {
					$foreignName = '管理人';
				} elsif($passCheck == 2) {
					$foreignName = 'GUEST';
				}
			}
			
			# 発言者を記憶する

			if ($HlbbsType ne 'ANON') {
				# 公開と極秘

				if($foreignName eq '') {
					$speaker = $foreignIsland->{'name'} . "$AfterName$addr," .$HforeignerID;
				}else{
					$speaker = $foreignName . "$addr";
				}
			} else {
				# 匿名
				$speaker = $ENV{'REMOTE_HOST'};
				$speaker = $ENV{'REMOTE_ADDR'} if ($speaker eq '');
			}
			if ($HlbbsType ne 'SECRET') {
				# 公開と匿名
				$speaker = "0<$speaker";
			} else {
				# 極秘

				$speaker = "1<$speaker";
			}
		} else {
			# 島主モード
			if(!checkPassword($island->{'password'},$HinputPassword)) {
				# password間違い
				unlock();
				tempWrongPassword();
				return;
			}
			$speaker = "0<$addr";
		}
	}

	my($lbbs) = $island->{'lbbs'};

	# モードで分岐

	if($HlbbsMode == 2) {
		# 削除モード
		# メッセージを前にずらす
		slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
	} elsif($HlbbsMode == 4) {
		# 外国者削除モード
		$line = $lbbs->[$HcommandPlanNumber];
		if($line =~ /([0-9]*)\<(.*)\<([0-9]*)\>(.*)\>(.*)$/) {
			my($sName, $sID) = split(/,/, $2);
			if((($sID != 0) && ($sID == $HforeignerID)) || ($foreignName eq '管理人')){
				# メッセージを前にずらす
				slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
			}else{
				unlock();
				tempWrongPassword();
				return;
			}
		}
	} else {
		# 記帳モード
		# メッセージを後ろにずらす
		slideLbbsMessage($lbbs);

		# メッセージ書き込み
		my $message = ($HlbbsMode == 1) ? '1' : '0';

		$HlbbsName = "$HislandTurn：" . htmlEscape($HlbbsName);
		$HlbbsMessage = htmlEscape($HlbbsMessage);
		$lbbs->[0] = "$speaker<$message>$HlbbsName>$HlbbsMessage";
	}

	# データ書き出し
	if(!writeIslandsFile($HcurrentID, $wmode)) {
		unlock();
		tempFailWrite();
		return;
	}

	if($HlbbsMode2 eq 'lbbslist'){
		# lbbslist.cgiからの書き込み？
		$HlbbsMode2 = 0;
		tempLbbsAdd();
		out("<meta HTTP-EQUIV=\"refresh\" CONTENT=\"0; URL=$HbaseDir/lbbslist.cgi?pass=$HdefaultPassword&id=$HforeignerID\#$HcurrentID\">");
		return if(($wmode == 3) || ($wmode == 4));
	}elsif($wmode == 3){
		# 宇宙マップ
		if(($HlbbsMode == 2) || ($HlbbsMode == 4)) {
			tempLbbsDelete();
		}else{
			tempLbbsAdd();
		}
		out("${HtagBig_}<A href=\"$HthisFile?space=0\">自動で宇宙マップへ飛びます・・・少々お待ちください。</A>${H_tagBig}");
		out("<meta HTTP-EQUIV=\"refresh\" CONTENT=\"0; URL=$HthisFile?space=0\">");
		return;
	}elsif($wmode == 4){
		# 海域マップ
		if(($HlbbsMode == 2) || ($HlbbsMode == 4)) {
			tempLbbsDelete();
		}else{
			tempLbbsAdd();
		}
		out("${HtagBig_}<A href=\"$HthisFile?Ocean=0\">自動で海域マップへ飛びます・・・少々お待ちください。</A>${H_tagBig}");
		out("<meta HTTP-EQUIV=\"refresh\" CONTENT=\"0; URL=$HthisFile?Ocean=0\">");
		return;
	}elsif(($HlbbsMode == 2) || ($HlbbsMode == 4)) {
		tempLbbsDelete();
	} else {
		tempLbbsAdd();
	}

	# もとのモードへ
	if(($HlbbsMode == 1) || ($HlbbsMode == 2)) {
		ownerMain();
	} else {
		printIslandMain();
	}
}

# ローカル掲示板のメッセージを一つ後ろにずらす
sub slideLbbsMessage {
	my($lbbs) = @_;
	pop(@$lbbs);
	unshift(@$lbbs, $lbbs->[0]);
}

# ローカル掲示板のメッセージを一つ前にずらす
sub slideBackLbbsMessage {
	my($lbbs, $number) = @_;
	splice(@$lbbs, $number, 1);
	$lbbs->[$HlbbsMax - 1] = '0<<0>>';
}

#----------------------------------------------------------------------
# 島の地図
#----------------------------------------------------------------------

# 情報の表示
sub islandInfo {
	$island = $Hislands[$HcurrentNumber];
	
	# 情報表示
	my($turnsu) = $island->{'turnsu'};
	my($rank) = $HcurrentNumber + 1;
	$rank = '-' if(($turnsu == 0) && ($island->{'pop'} == 10));
	
	my($wkind, $wname, $whp, $wkind2, $wkind3) = weatherinfo($island->{'weather'});
	my($wname2) = $WeatherName[$wkind2];
	my($wname3) = $WeatherName[$wkind3];
	
	my($farm) = $island->{'farm'};
	my($factory) = $island->{'factory'};
	my($port) = $island->{'port'};
	my($mountain) = $island->{'mountain'};
	my($ore) = $island->{'ore'};
	my($oil) = $island->{'oil'};
	my($weapon) = $island->{'weapon'};
	
	my($zyuni) = $island->{'zyuni'};
	
	my($allex) = $island->{'allex'};
	my($tower) = $island->{'tower'};
	my($yousyoku) = $island->{'yousyoku'};
	
	my($MissileK) = $island->{'MissileK'};
	my($MissileA) = $island->{'MissileA'};
	my($soukei) = int(($factory + $port + $mountain + $tower + $farm + ($yousyoku / 10)) * 10);
	my($seisan) = $farm * 10;
	
	$farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
	$port = ($port == 0) ? "保有せず" : "${port}0$HunitPop";
	$factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
	$mountain = ($mountain == 0) ? "保有せず" : "${mountain}0$HunitPop";
	$tower = ($tower == 0) ? "保有せず" : "${tower}0$HunitPop";
	$ore = ($ore == 0) ? "保有せず" : "${ore}$HunitOre";
	$oil = ($oil == 0) ? "保有せず" : "${oil}$HunitOil";
	$weapon = ($weapon == 0) ? "保有せず" : "${weapon}$HunitWeapon";
	$soukei = ($soukei == 0) ? "保有せず" : "${soukei}$HunitPop";
	if($yousyoku == 0) {
		$yousyoku = "保有せず"
	} else {
		$seisan += $yousyoku;
		$yousyoku = "${yousyoku}00匹";
	}
	$seisan = ($seisan == 0) ? "無し" : "${seisan}$HunitFood";
	my($mStr0) = '';
	my($mStr1) = '';
	my($mStr3) = '';
	if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
		# 無条件またはownerモード
		$mStr0 = "<TD $HbgInfoCell>$MissileK</TD>";
		$mStr1 = "<TD $HbgInfoCell>$MissileA</TD>";
		$mStr3 = "<TD $HbgInfoCell>$island->{'money'}$HunitMoney</TD>";
	} elsif($HhideMoneyMode == 2) {
		my($mTmp) = aboutMoney($island->{'money'});
		my($mTmp2) = '機密';
		$mStr0 = "<TD $HbgInfoCell>$mTmp2</TD>";
		$mStr1 = "<TD $HbgInfoCell>$mTmp2</TD>";
		# 1000億単位モード
		$mStr3 = "<TD $HbgInfoCell>$mTmp</TD>";
	} else {
		my($mTmp2) = '機密';
		$mStr0 = "<TD $HbgInfoCell>$mTmp2</TD>";
		$mStr1 = "<TD $HbgInfoCell>$mTmp2</TD>";
		$mStr3 = "<TD $HbgInfoCell>$mTmp2</TD>";
	}
	my($popspace) = $island->{'popspace'};
	$popspace = ($popspace > 0) ? "${popspace}${HunitPop}" : "　";
	
	if($HmainMode eq 'bfield'){
	out(<<END);
<DIV ID='islandInfo'><TABLE BORDER><TR>
<TD $HbgTitleCell>${HtagTH_}ID${H_tagTH}</TD>
<TD $HbgInfoCell>$island->{'id'}</TD>
<TD $HbgTitleCell>${HtagTH_}天候${H_tagTH}</TD>
<TD $HbgSubTCell>今日</TD>
<TD $HbgInfoCell>$wname</TD>
<TD $HbgSubTCell>明日</TD>
<TD $HbgInfoCell>$wname2</TD>
<TD $HbgSubTCell>明後日</TD>
<TD $HbgInfoCell>$wname3</TD>
<TD $HbgSubTCell>湿度</TD>
<TD $HbgInfoCell>$whp</TD>
</TR></TABLE>
注意：Battle Fieldへのノーマル、PPミサイル、記念碑落し、移民、怪獣派遣以外の命令は無視されます。<BR>
</DIV>
END
		return;
	}
	out(<<END);
<DIV ID='islandInfo'><TABLE BORDER>
<TR>
<TH $HbgTitleCell colspan=2>${HtagTH_}成績${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}天候${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}資産${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}一次産業${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}二次産業${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}三次産業${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}軍事力${H_tagTH}</TH>
</TR>
<TR>
<TD $HbgSubTCell>順　位</TD>
<TD $HbgInfoCell>${HtagNumber_}$rank${H_tagNumber}($zyuni)</TD>
<TD $HbgSubTCell>今日</TD>
<TD $HbgInfoCell>$wname</TD>
<TD $HbgSubTCell>資金</TD>
$mStr3
<TD $HbgSubTCell>農業規模</TD>
<TD $HbgInfoCell>${farm}</TD>
<TD $HbgSubTCell>工場</TD>
<TD $HbgInfoCell>${factory}</TD>
<TD $HbgSubTCell>商業</TD>
<TD $HbgInfoCell>${tower}</TD>
<TD $HbgSubTCell>ミサイル発射可能数</TD>
$mStr0
</TR>
<TR>
<TD $HbgSubTCell>総人口</TD>
<TD $HbgInfoCell>$island->{'pop'}$HunitPop</TD>
<TD $HbgSubTCell>明日</TD>
<TD $HbgInfoCell>$wname2</TD>
<TD $HbgSubTCell>食料</TD>
<TD $HbgInfoCell>$island->{'food'}$HunitFood</TD>
<TD $HbgSubTCell>養殖場規模</TD>
<TD $HbgInfoCell>${yousyoku}</TD>
<TD $HbgSubTCell>港</TD>
<TD $HbgInfoCell>${port}</TD>
<TD $HbgSubTCell>　</TD>
<TD $HbgInfoCell>　</TD>
<TD $HbgSubTCell>兵器量</TD>
<TD $HbgInfoCell>$weapon</TD>
</TR>
<TR>
<TD $HbgSubTCell>宇宙民</TD>
<TD $HbgInfoCell>$popspace</TD>
<TD $HbgSubTCell>明後日</TD>
<TD $HbgInfoCell>$wname3</TD>
<TD $HbgSubTCell>鉱石</TD>
<TD $HbgInfoCell>$ore</TD>
<TD $HbgSubTCell>　</TD>
<TD $HbgInfoCell>　</TD>
<TD $HbgSubTCell>採掘場</TD>
<TD $HbgInfoCell>${mountain}</TD>
<TD $HbgSubTCell>　</TD>
<TD $HbgInfoCell>　</TD>
<TD $HbgSubTCell>発射ミサイル数</TD>
$mStr1
</TR>
<TR>
<TD $HbgSubTCell>面積</TD>
<TD $HbgInfoCell>$island->{'area'}$HunitArea</TD>
<TD $HbgSubTCell>湿度</TD>
<TD $HbgInfoCell>$whp</TD>
<TD $HbgSubTCell>原油</TD>
<TD $HbgInfoCell>$oil</TD>
<TD $HbgSubTCell>食料最大生産</TD>
<TD $HbgInfoCell>$seisan</TD>
<TD $HbgSubTCell>　</TD>
<TD $HbgInfoCell>　</TD>
<TD $HbgSubTCell>総職数</TD>
<TD $HbgInfoCell>$soukei</TD>
<TD $HbgSubTCell>総獲得経験値</TD>
<TD $HbgInfoCell>$allex</TD>
</TR></TABLE></DIV>
END
}
# 宇宙情報の表示
sub spaceInfo {
	my($food) = $Hspace->{'food'};
	my($foodP) = $Hspace->{'foodP'};
	my($foodC) = $Hspace->{'foodC'};
	my($foodB) = $foodP - $foodC;
	my($farm) = $Hspace->{'farm'};
	my($factory) = $Hspace->{'factory'};
	$food = ($food <= 0) ? "0" : "${food}$HunitFood";
#	$foodP = ($foodP == 0) ? "0" : "${foodP}$HunitFood";
#	$foodC = ($foodC == 0) ? "0" : "${foodC}$HunitFood";
#	$foodB = ($foodB == 0) ? "0" : "${foodB}$HunitFood";
	$farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
	my($solarwind);
	if($Hspace->{'solarwind'} <= $HislandTurn){
		$solarwind = "<b>発生中</b>";
	}else{
		$solarwind = $Hspace->{'solarwind'} . "ターンから";
	}
	out(<<END);
<DIV ID='islandInfo'><TABLE BORDER><TR>
<TD>${HtagTH_}宇宙歴${H_tagTH}</TD>
<TD>${HtagTH_}開発面積${H_tagTH}</TD>
<TD>${HtagTH_}宇宙人口${H_tagTH}</TD>
<TD>${HtagTH_}農場規模${H_tagTH}</TD>
<TD>${HtagTH_}工場規模${H_tagTH}</TD>
<TD>${HtagTH_}太陽風予報${H_tagTH}</TD>
</TR>
<TR>
<TD>${HislandTurn}ターン</TD>
<TD>$Hspace->{'area'}Hex</TD>
<TD>$Hspace->{'pop'}$HunitPop</TD>
<TD>${farm}</TD>
<TD>${factory}</TD>
<TD>${solarwind}</TD>
</TR>
</TABLE></DIV>
END
}
# 宇宙情報２の表示
sub spaceInfo2 {
	my(@spa,$i,$tmp);
	my @spa2 = split(/,/, $Hspace->{'space'});
	for($i = 0;$i < 9;$i++){
		$tmp = $spa2[$i];
		my $sIsland = $Hislands[$HidToNumber{$tmp}];
		$spa[$i] = $sIsland->{'id'};
		$i++;
		$tmp = $spa2[$i];
		if(($sIsland->{'name'} eq '') || ($tmp <= 0)){
			$spa[$i] = "-";
		}else{
			$spa[$i] = $sIsland->{'name'} . "${AfterName}(${tmp})";
		}
	}
	out(<<END);
<DIV ID='islandInfo'><TABLE BORDER><TR>
<TD>${HtagTH_}宇宙資産　１位${H_tagTH}</TD>
<TD>${HtagTH_}２位${H_tagTH}</TD>
<TD>${HtagTH_}３位${H_tagTH}</TD>
<TD>${HtagTH_}４位${H_tagTH}</TD>
<TD>${HtagTH_}５位${H_tagTH}</TD>
</TR>
<TR>
<TD><A href=\"$HthisFile?space=$spa[0]\" class=\"M\">$spa[1]</a></TD>
<TD><A href=\"$HthisFile?space=$spa[2]\" class=\"M\">$spa[3]</a></TD>
<TD><A href=\"$HthisFile?space=$spa[4]\" class=\"M\">$spa[5]</a></TD>
<TD><A href=\"$HthisFile?space=$spa[6]\" class=\"M\">$spa[7]</a></TD>
<TD><A href=\"$HthisFile?space=$spa[8]\" class=\"M\">$spa[9]</a></TD>
</TR></TABLE></DIV>
END
}

# 地図の表示
# 引数が1なら、ミサイル基地等をそのまま表示
sub islandMap {
	my($mode, $pId) = @_;
	my($island);
	if($mode == 3){
		# 宇宙マップ
		$island = $Hspace;
	}elsif($mode == 4){
		# 海域マップ
		$island = $Hocean;
	}else{
		$island = $Hislands[$HcurrentNumber];
	}
	
	# 地形、地形値を取得
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($nation) = $island->{'nation'};
	my($dis) = $island->{'landValue2'};
	my($l, $lv);
	$pId = $island->{'id'} if($mode == 1);

	# コマンド取得
	my($com, @comStr, $i);
	if($HmainMode eq 'owner') {
		my($command) = $island->{'command'};
		for($i = 0; $i < $HcommandMax; $i++) {
			my($j) = $i + 1;
			$com = $command->[$i];
			if($com->{'kind'} < 50) {
				$comStr[$com->{'x'}][$com->{'y'}] .=
				" [${j}]$HcomName[$com->{'kind'}]";
			}
		}
	}
	
	# 座標(上)を出力
	my $widthsize = $HislandSize * 32 + 16;
	my $cspan = $HislandSize + 1;
	
	if($mode == 3){
		out("<div id='islandMap'><table border=1><tr>");
		out("<td colspan=$cspan class=s><img src=$HspaceSizeImage width=$widthsize height=16>");
	}elsif($mode == 4){
		out("<div id='islandMap'><table border=1><tr>");
		out("<td colspan=$cspan class=b><img src=$HoceanSizeImage width=$widthsize height=16>");
	}else{
		out("<div id='islandMap'><table border><tr>");
		out("<td colspan=$cspan class=b><img src=$HislandSizeImage width=$widthsize height=16>");
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
			if(($Kiri->[$x][$y] == 1) || (($Kiri->[$x][$y] == 2) && ($mode != 1))) {
				landString2($land->[$x][$y], $landValue->[$x][$y], $x, $y, $mode, $comStr[$x][$y], $nation->[$x][$y],0);
			} else {
				landString($land->[$x][$y], $landValue->[$x][$y], $x, $y, $mode, $comStr[$x][$y], $nation->[$x][$y], $dis->[$x][$y], $pId,0);
			}
		}
		
		# 奇数行目なら番号を出力
		if(($y % 2) == 1){
			if($mode == 3){
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
	out("<div id='NaviView'></div>");
	out("</table></div>\n");

	# テストモード参照
	if($Htestflg){
		HdebugOut("テストモード参照${mId}");
	}
}

sub landString {
	my($l, $lv, $x, $y, $mode, $comStr, $nation, $dis, $pId, $js) = @_;
	my($point) = "($x,$y)";
	my($image, $alt, $sflg, $myship, $tIsland, $tName);
	my($naviTitle);
	my($naviText);
	my($naviExp) = "''";

#	# クッキーから自分のID取得
#	# この情報で自分の所属の船を表示しています。クッキー改変してインチキしないように
	my($lcookie) = jcode::euc($ENV{'HTTP_COOKIE'});
#	if($lcookie =~ /OWNISLANDID=\(([^\)]*)\)/) {
#		$mId = $1;
#	}
	if($lcookie =~ /MYSHIP=\(([^\)]*)\)/) {
		$myship = $1;
	}

	# 自分のID
	$mId = $pId;

	my($tn) = $HidToNumber{$nation};
	if($tn eq ''){
		$tName = "所属不明";
		$sflg = $nation;
	}else{
		$tIsland = $Hislands[$tn];
		$tName = $tIsland->{'name'};
		$sflg = $tIsland->{'id'};
	}

	if($l == $HlandSea) {
		if($mode == 3){
			$image = 'cosmo1.gif';
			$alt = '虚無';
			$naviTitle = '虚無';
		}elsif($mode == 4) {
			$image = 'land0.gif';
			if($nation > 0){
				$alt = "海(${tName}${sAfterName})";
			}else{
				$alt = "海";
			}
			$naviTitle = $alt;
		}elsif($lv >= 10) {
			# 養殖場

			$image = 'land17.gif';
			$alt = "養殖場(${lv}00匹)";
			$naviTitle = '養殖場';
			$naviText = "${lv}00匹";
		} elsif($lv == 1) {
			# 浅瀬
			$image = 'land14.gif';
			$alt = '海(浅瀬)';
			$naviTitle = '浅瀬';
		} else {
			# 海
			$image = 'land0.gif';
			$alt = '海';
			$naviTitle = '海';
		}
	} elsif($l == $HlandWaste) {
		# 荒地
		if($lv >= 10) {
			# 温泉

			$image = 'land18.gif';
			$alt = "温泉(毎秒${lv}リットル)";
			$naviTitle = '温泉';
			$naviText = "毎秒${lv}リットル";
		} elsif($lv == 1) {
			$image = 'land13.gif'; # 着弾点
			$alt = '荒地';
			$naviTitle = '荒地';
		} else {
			$image = 'land1.gif';
			$alt = '荒地';
			$naviTitle = '荒地';
		}
	} elsif($l == $HlandPlains) {
		# 平地
		$image = 'land2.gif';
		$alt = '平地';
		$naviTitle = '平地';
	} elsif($l == $HlandForest) {
		# 森
		if($mode == 0) {
			# 観光者の場合は木の本数隠す
			$image = 'land6.gif';
			$alt = '森';
			$naviTitle = '森';
		} else {
			$image = 'land6.gif';
			$alt = "森(${lv}$HunitTree)";
			$naviTitle = '森';
			$naviText = "${lv}$HunitTree";
		}
	} elsif($l == $HlandTown) {
		# 町
		my($p);
		if($lv < 30) {
			$p = 3;
			$naviTitle = '村';
		} elsif($lv < 100) {
			$p = 4;
			$naviTitle = '町';
		} else {
			$p = 5;
			$naviTitle = '都市';
		}
		$image = "land${p}.gif";
		$alt = "$naviTitle(${lv}$HunitPop)";
		$naviText = "${lv}$HunitPop";
	} elsif($l == $HlandSlum) {
		# スラム街
		$image = "land22.gif";
		$alt = "スラム街(${lv}$HunitPop)";
		$naviTitle = 'スラム街';
		$naviText = "${lv}$HunitPop";
	} elsif($l == $HlandFarm) {
		# 農場
		$image = 'land7.gif';
		$alt = "農場(${lv}0${HunitPop}規模)";
		$naviTitle = '農場';
		$naviText = "${lv}0${HunitPop}規模";
	} elsif($l == $HlandFactory) {
		# 工場
		$image = 'land8.gif';
		$alt = "工場(${lv}0${HunitPop}規模)";
		$naviTitle = '工場';
		$naviText = "${lv}0${HunitPop}規模";
	} elsif($l == $HlandTower) {
		# 商業ビル
		$image = 'land23.gif';
		$alt = "商業ビル(${lv}0${HunitPop}規模)";
		$naviTitle = '商業';
		$naviText = "${lv}0${HunitPop}規模";
	} elsif($l == $HlandPort) {
		$image = 'land55.gif';
		$alt = "港(${lv}0${HunitPop}規模)";
		$naviTitle = '港';
		$naviText = "${lv}0${HunitPop}規模";
	} elsif($l == $HlandPolice) {
		$image = 'land56.gif';
		$alt = '警察署';
		$naviTitle = '警察署';
	} elsif($l == $HlandHospital) {
		$image = 'land66.gif';
		$alt = '病院';
		$naviTitle = '病院';
	} elsif($l == $HlandBase) {
		if($mode == 0) {
			# 観光者の場合は森のふり
			$image = 'land6.gif';
			$alt = '森';
			$naviTitle = '森';
		} else {
			# ミサイル基地
			my($level) = expToLevel($l, $lv);
			$image = 'land9.gif';
			$alt = "ミサイル基地 (レベル ${level}/経験値 $lv)";
			$naviTitle = 'ミサイル基地';
			$naviText = "レベル ${level}/経験値 $lv";
		}
	} elsif($l == $HlandSbase) {
		# 海底基地
		if($mode == 0) {
			# 観光者の場合は海のふり
			$image = 'land0.gif';
			$alt = '海';
			$naviTitle = '海';
		} else {
			my($level) = expToLevel($l, $lv);
			$image = 'land12.gif';
			$alt = "海底基地 (レベル ${level}/経験値 $lv)";
			$naviTitle = '海底基地';
			$naviText = "レベル ${level}/経験値 $lv";
		}
	} elsif(($l == $HlandWarp) || ($l == $HlandWarpR)) {
		# 転移装置
		$image = 'land36.gif';
		if($l == $HlandWarpR) {
			# 受信専門
			if($mode == 0) {
				$alt = "転移装置";
			}else{
				if($lv == 1) {
					$alt = "転移先装置 (右上)";
				} elsif($lv == 2) {
					$alt = "転移先装置 (右)";
				} elsif($lv == 3) {
					$alt = "転移先装置 (右下)";
				} elsif($lv == 4) {
					$alt = "転移先装置 (左下)";
				} elsif($lv == 5) {
					$alt = "転移先装置 (左)";
				} elsif($lv == 6) {
					$alt = "転移先装置 (左上)";
				} else {
					$alt = "転移先装置";
				}
			}
			$naviTitle = $alt;
		} else {
			if($mode == 0) {
				$alt = "転移装置";
			} else {
				$alt = "転移装置 (${HidToName{$lv}}${AfterName})";
				$naviText = "${HidToName{$lv}}${AfterName}";
			}
			$naviTitle = "転移装置";
		}
	} elsif($l == $HlandDefence) {
		# 防衛施設
		$image = 'land10.gif';
		if($lv == 2) {
			$alt = 'S防衛施設';
		} elsif($lv == 3) {
			$alt = 'SS防衛施設';
		} elsif($lv == 10 || $lv == 11) {
			if($mode == 0) {
				$image = 'land6.gif';
				$alt = '森';
			} else {
				if($lv == 10){
					$alt = 'ST防衛施設';
				}else{
					$alt = 'SST防衛施設';
				}
			}
		} elsif($lv == 20) {
			$alt = '霧付き防衛施設';
		} elsif($lv == 21) {
			$alt = 'S霧付き防衛施設';
		} else {
			$alt = '防衛施設';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandHaribote) {
		# ハリボテ、ハリボテいのら

		if($lv == 0) {
			$image = 'land10.gif';
			if($mode == 0) {
				# 観光者の場合は防衛施設のふり

				$alt = '防衛施設';
			} else {
				$alt = 'ハリボテ';
			}
			$naviTitle = $alt;
		} else {
			my($kind, $name, $hp) = monsterSpec($lv);
			my($special) = $HmonsterSpecial[$kind];
			$image = $HmonsterImage[$kind];
			# 硬化中?
			if((($special == 3) && (($HislandTurn % 2) == 1)) ||
				(($special == 4) && (($HislandTurn % 2) == 0))) {
				$image = $HmonsterImage2[$kind];
			}
			$alt = "怪獣$name(体力${hp})";
			$naviTitle = $name;
			$naviText = "体力${hp}";
			$naviExp = "\'MONSTER$kind\'";
		}
	} elsif($l == $HlandOil) {
		# 海底油田
		if($lv == 5) {
			$image = 'land25.gif';
			$alt = '海底防衛施設';
			$naviTitle = '海底防衛施設';
		} elsif($lv == 6) {
			$image = 'land49.gif';
			$alt = '海底デストラップ';
			$naviTitle = '海底デストラップ';
		} elsif($lv == 7) {
			$image = 'land35.gif';
			$alt = '海底消防署';
			$naviTitle = '海底消防署';
		} elsif($lv >= 35) {
			$image = 'land19.gif';
			$alt = "海底都市(${lv}$HunitPop)";
			$naviTitle = '海底都市';
			$naviText = "${lv}${HunitPop}規模";
		} elsif($lv >= 10) {
			$image = 'land20.gif';
			$alt = "海底農場(${lv}0${HunitPop}規模)";
			$naviTitle = '海底農場';
			$naviText = "${lv}0${HunitPop}規模";
		} else {
			$image = 'land16.gif';
			$alt = '海底油田';
			$naviTitle = '海底油田';
		}
	} elsif($l == $HlandDeathtrap) {
		$image = 'land48.gif';
		$alt = "デストラップ(LV${lv})";
		$naviTitle = 'デストラップ';
		$naviText = "LV${lv}";
	} elsif($l == $HlandWindmill) {
		$image = 'land50.gif';
		$alt = '風車';
		$naviTitle = '風車';
	} elsif($l == $HlandMyhome) {
		if($lv > 10) {
			$image = 'land53.gif';
			$alt = 'マイホーム(豪邸)';
		} elsif($lv > 5) {
			$image = 'land52.gif';
			$alt = 'マイホーム(池付)';
		} else {
			$image = 'land51.gif';
			$alt = 'マイホーム(２階建)';
		}
		$naviTitle = $alt;
		readProfileMAP($HcurrentID);
		$image = $Hprofile{'MyHomeImage'} if(substr($Hprofile{'MyHomeImage'},0,7) eq 'http://');
	} elsif($l == $HlandOsen) {
		$image = 'land21.gif';
		$alt = "汚染土壌(LV${lv})";
		$naviTitle = '汚染土壌';
		$naviText = "LV${lv}";
	} elsif($l == $HlandStadium) {
		$image = 'land27.gif';
		$alt = 'スタジアム';
		$naviTitle = $alt;
	} elsif($l == $HlandAmusement) {
		$image = 'land28.gif';
		$alt = '遊園地';
		$naviTitle = $alt;
	} elsif($l == $HlandCasino) {
		$image = 'land29.gif';
		$alt = 'カジノ';
		$naviTitle = $alt;
	} elsif($l == $HlandPark) {
		$image = 'land30.gif';
		$alt = '公園';
		$naviTitle = $alt;
	} elsif($l == $HlandSchool) {
		$image = 'land31.gif';
		$alt = '学校';
		$naviTitle = $alt;
	} elsif($l == $HlandDome) {
		$image = 'land32.gif';
		$alt = 'ドーム';
		$naviTitle = $alt;
	} elsif($l == $HlandAirport) {
		$image = 'land33.gif';
		$alt = '空港';
		$naviTitle = $alt;
	} elsif($l == $HlandZoo) {
		$image = 'land38.gif';
		$alt = '動物園';
		$naviTitle = $alt;
	} elsif($l == $HlandBigcity) {
		$image = 'land39.gif';
		$alt = '大都市';
		$naviTitle = $alt;
	} elsif($l == $HlandExpo) {
		$image = 'land40.gif';
		$alt = '博覧会';
		$naviTitle = $alt;
	} elsif($l == $HlandMegacity) {
		if($lv == 1) {
			$image = 'land42.gif';
			$alt = '巨大都市−南西';
		} elsif($lv == 2) {
			$image = 'land41.gif';
			$alt = '巨大都市−西';
		} elsif($lv == 3) {
			$image = 'land43.gif';
			$alt = '巨大都市−北西';
		} elsif($lv == 4) {
			$image = 'land42.gif';
			$alt = '巨大都市−北東';
		} elsif($lv == 5) {
			$image = 'land41.gif';
			$alt = '巨大都市−東';
		} elsif($lv == 6) {
			$image = 'land43.gif';
			$alt = '巨大都市−南東';
		} else {
			$image = 'land41.gif';
			$alt = '巨大都市';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandMegatower) {
		if($lv == 1) {
			$image = 'land46.gif';
			$alt = '巨大ビル−南西';
		} elsif($lv == 2) {
			$image = 'land45.gif';
			$alt = '巨大ビル−西';
		} elsif($lv == 3) {
			$image = 'land46.gif';
			$alt = '巨大ビル−北西';
		} elsif($lv == 4) {
			$image = 'land46.gif';
			$alt = '巨大ビル−北東';
		} elsif($lv == 5) {
			$image = 'land44.gif';
			$alt = '巨大ビル−東';
		} elsif($lv == 6) {
			$image = 'land46.gif';
			$alt = '巨大ビル−南東';
		} else {
			$image = 'land46.gif';
			$alt = '巨大ビル';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandMegaFact) {
		if($lv == 1) {
			$image = 'land47.gif';
			$alt = '巨大工場−南西';
		} elsif($lv == 2) {
			$image = 'land47.gif';
			$alt = '巨大工場−西';
		} elsif($lv == 3) {
			$image = 'land47.gif';
			$alt = '巨大工場−北西';
		} elsif($lv == 4) {
			$image = 'land47.gif';
			$alt = '巨大工場−北東';
		} elsif($lv == 5) {
			$image = 'land47.gif';
			$alt = '巨大工場−東';
		} elsif($lv == 6) {
			$image = 'land47.gif';
			$alt = '巨大工場−南東';
		} else {
			$image = 'land47.gif';
			$alt = '巨大工場';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandMegaFarm) {
		if($lv == 1) {
			$image = 'land65.gif';
			$alt = '巨大農場−南西';
		} elsif($lv == 2) {
			$image = 'land65.gif';
			$alt = '巨大農場−西';
		} elsif($lv == 3) {
			$image = 'land65.gif';
			$alt = '巨大農場−北西';
		} elsif($lv == 4) {
			$image = 'land65.gif';
			$alt = '巨大農場−北東';
		} elsif($lv == 5) {
			$image = 'land65.gif';
			$alt = '巨大農場−東';
		} elsif($lv == 6) {
			$image = 'land65.gif';
			$alt = '巨大農場−南東';
		} else {
			$image = 'land65.gif';
			$alt = '巨大農場';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandFuji) {
		$image = $HfujiImage[$lv];
		$alt = '富士山';
		$naviTitle = $alt;
	} elsif($l == $HlandTcity) {
		$image = 'land58.gif';
		$alt = "商業都市(300${HunitPop} ${lv}0${HunitPop}規模)";
		$naviTitle = '商業都市';
		$naviText = "300${HunitPop} ${lv}0${HunitPop}規模";
	} elsif($l == $HlandHugecity) {
		if($lv < 50) {
			$image = 'land60.gif';
			$alt = '超巨大都市(中心)';
		} elsif($lv < 60) {
			$image = 'land61.gif';
			$alt = '超巨大都市(都市)';
		} elsif($lv < 70) {
			$image = 'land62.gif';
			$alt = '超巨大都市(工場)';
		} elsif($lv < 80) {
			$image = 'land63.gif';
			$alt = '超巨大都市(商業)';
		} else {
			$image = 'land64.gif';
			$alt = '超巨大都市(農場)';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandBreakwater) {
		# 防波堤
		if($lv == 1) {
			$image = 'land59.gif';
		}else{
			# 未使用
			$image = 'land59_2.gif';
		}
		$alt = '防波堤';
		$naviTitle = '防波堤';
	} elsif($l == $HlandFire) {
		if($lv >= 10) {
			$image = 'land37.gif';
			$alt = 'S消防署';
		} else {
			$image = 'land34.gif';
			$alt = '消防署';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandSeisei) {
		# 精製場
		if($lv == 10) {
			$image = 'land24.gif';
			$alt = '銅精製場';
		} elsif($lv == 30) {
			$image = 'land24.gif';
			$alt = '金精製場';
		} else {
			$image = 'land24.gif';
			$alt = '石炭精製場';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandMountain) {
		# 山
		my $str = '';
		$naviTitle = '山';
		if($lv > 0) {
			$image = 'land15.gif';
			$alt = "山(採掘場${lv}0${HunitPop}規模)";
			$naviText = "採掘場${lv}0${HunitPop}規模";
		} else {
			$image = 'land11.gif';
			$alt = '山';
		}
	} elsif($l == $HlandMonument) {
		# 記念碑
		$image = $HmonumentImage[$lv];
		$alt = $HmonumentName[$lv];
		$naviTitle = $alt;
	} elsif($l == $HlandSMonument) {
		# 海底記念碑
		$image = $HsmonumentImage[$lv];
		$alt = $HsmonumentName[$lv];
		$naviTitle = $alt;
	} elsif($l == $HlandBank) {
		if($mode == 0) { # 観光者の場合
			$image = 'land6.gif';
			$alt = '森';
			$naviTitle = '森';
		} else {
			$image = 'land26.gif';
			$alt = "銀行(投資額${lv}000$HunitMoney)";
			$naviTitle = '銀行';
			$naviText = "投資額${lv}000$HunitMoney";
		}
	} elsif($HseaChk[$l] == 2) {
		# 船系
		$image = $HshipImage[$l - $HlandPirate];
		my($order, $hp, $sId) = shipSpec($lv);
		$naviTitle = $HshipName[$l - $HlandPirate];
		if($l == $HlandGhostShip) {
			$alt = '海';
			$naviTitle = '海';
		#	$alt = "$naviTitle(H${hp})"; # デバック用
		} elsif($l == $HlandBalloonS) {
			$alt = "$naviTitle";
			$image = "${image}${hp}.gif";
		} elsif(($sId eq $mId) && ($sId != 0)) {
			$alt = "$naviTitle(${HidToName{$sId}}${AfterName} H${hp})($Hshiporder[$order])";
			$image = "m${image}" if(!$myship);
		} else {
			$alt = "$naviTitle(H${hp})($Hshiporder[$order])";
		}
		$naviText = $alt;
	} elsif($l == $HlandMonster) {
		# 怪獣
		my($kind, $name, $hp) = monsterSpec($lv);
		my($special) = $HmonsterSpecial[$kind];
		$image = $HmonsterImage[$kind];

		# 硬化中?
		if((($special == 3) && (($HislandTurn % 2) == 1)) ||
		   (($special == 4) && (($HislandTurn % 2) == 0))) {
			# 硬化中

			$image = $HmonsterImage2[$kind];
		}
		if($kind == 26) {
			# 迷彩いのら
			$alt = '荒地';
			$naviTitle = $alt;
		} else {
			$alt = "怪獣$name(体力${hp})";
			$naviTitle = $name;
			$naviText = "体力${hp}";
			$naviExp = "\'MONSTER$kind\'";
		}
	} elsif($l == $HlandKInora) {
		# 究想いのら
		my($limit, $hp, $ld, $d) = bigMonsterSpec($lv);
		$image = "kinora${ld}${d}.gif";
		if($d == 0){
			$alt = "怪獣究想いのら(体力${hp})(残$limit)";
			$naviText = "体力${hp} 残$limit";
		}else{
			$alt = "怪獣究想いのら";
		}
		$naviTitle = '怪獣究想いのら';
	} elsif($l == $HlandTrump) {
		# トランプ
		if(($lv < 1) || ($lv > 14)){
			$image = 'trump0.gif';
			$alt = 'トランプ裏';
		}else{
			$image = "trump${lv}.gif";
			if($lv == 14){
				$alt = 'トランプジョーカー';
			}else{
				$alt = "トランプ${lv}";
			}
		}
		$naviTitle = $alt;
	} elsif($l == $HlandFlower) {
		# お花
		$lv = 1 if(($lv < 1) || ($lv > 13));
		$image = "flower${lv}.gif";
		if($lv == 13){
			$alt = 'サボテン';
		}else{
			$alt = '花';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandDokan) {
		# 地下
		if($mode == 0) { # 観光者の場合
			$image = 'land6.gif';
			$alt = '森';
		} else {
			$image = 'land57.gif';
			$alt = '土管';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandOcean) {
		# 海域無人島
		$image = 'ocean_10.gif';
		$alt = '無人島';
		$naviTitle = $alt;
	} elsif($l == $HlandOPlayer){
		# 海域
		if($l == $HlandOPlayer){
			$image = 'ocean_20.gif';
			$alt = "${tName}${sAfterName}";
		}
		$naviTitle = $alt;
	} elsif($l == $HlandEarth) {
		# 地球
		$image = 'cosmo2.gif';
		$alt = '地球';
		$naviTitle = $alt;
	}elsif( ($l == $HlandSunit) || ($l == $HlandSCity) ||
			($l == $HlandSFarm) || ($l == $HlandSFactory) ||
			($l == $HlandSpaceBase) || ($l == $HlandSDefence) ||
			($l == $HlandSAEisei)){
		if($l == $HlandSunit) {
			if($lv == 20) {
				$image = 'cosmo6.gif';
				$alt = '宇宙破壊ユニット';
				$naviTitle = '宇宙破壊ユニット';
			} elsif($lv == 1) {
				$image = 'cosmo4.gif';
				$alt = '宇宙建設中ユニット';
				$naviTitle = '宇宙建設中ユニット';
			} elsif($lv == 10) {
				$image = 'cosmo5.gif';
				$alt = '宇宙ユニット';
				$naviTitle = '宇宙ユニット';
			} else {
				$image = 'cosmo3.gif';
				$alt = '宇宙基礎ユニット';
				$naviTitle = '宇宙基礎ユニット';
			}
		} elsif($l == $HlandSCity) {
			# 宇宙都市
			my($p, $n);
			if($lv < 30) {
				$p = 7;
				$n = '宇宙村';
				$naviTitle = '宇宙村';
			} elsif($lv < 100) {
				$p = 8;
				$n = '宇宙町';
				$naviTitle = '宇宙町';
			} else {
				$p = 9;
				$n = '宇宙都市';
				$naviTitle = '宇宙都市';
			}
			$naviText = "${lv}$HunitPop";
			$image = "cosmo${p}.gif";
			$alt = "$n(${lv}$HunitPop)";
		} elsif($l == $HlandSFarm) {
			# 宇宙農場
			$image = 'cosmo10.gif';
			$alt = "宇宙農場(${lv}0${HunitPop}規模)";
			$naviTitle = '宇宙農場';
			$naviText = "${lv}0${HunitPop}規模";
		} elsif($l == $HlandSFactory) {
			# 宇宙工場
			$image = 'cosmo11.gif';
			$alt = "宇宙工場(${lv}0${HunitPop}規模)";
			$naviTitle = '宇宙工場';
			$naviText = "${lv}0${HunitPop}規模";
		} elsif($l == $HlandSpaceBase) {
			# 宇宙ミサイル基地
			my($level) = expToLevel($l, $lv);
			$image = 'cosmo12.gif';
			$alt = "宇宙ミサイル基地 (レベル ${level}/経験値 $lv)";
			$naviTitle = "宇宙ミサイル基地";
			$naviText = "レベル ${level}/経験値 $lv";
		} elsif($l == $HlandSDefence) {
			# 宇宙防衛施設
			$image = 'cosmo14.gif';
			$alt = "宇宙防衛施設";
			$naviTitle = "宇宙防衛施設";
		} elsif($l == $HlandSAEisei) {
			# 宇宙衛星
			$image = $HsEiseiImage[int($lv / 1000)];
			my $en = $lv % 1000;
			$alt = $HsEisei[int($lv / 1000)];
			$alt .= "(${en}EN)";
			$naviTitle = $HsEisei[int($lv / 1000)];
			$naviText = "${en}EN";
		}
		if($nation > 0){
			$alt .= "(${tName}${sAfterName})";
			$naviText .= "(${tName}${sAfterName})";
		}
		
		if($dis > 100){
			$alt .= "(不満頂点)";
			$naviText .= "(不満頂点)";
		}elsif($dis > 45){
			$alt .= "(不満)";
			$naviText .= "(不満)";
		}elsif($dis > 30){
			$alt .= "(やや不満)";
			$naviText .= "(やや不満)";
		}
	}

	if($js == 1){
		# jsモード
		if($mode == 3){
	#		HdebugOut("$sflg,$mId");
			if(($sflg == $mId) && ($sflg > 0) && ($nation > 0) && (!$myship)){
				out(qq#<td class=b><A HREF="JavaScript:void(0);" onclick="ps($x,$y)" #);
			}elsif((($l != $HlandSea) && ($l != $HlandEarth)) && ($nation == 0) && (!$myship)){
				out(qq#<td class=i><A HREF="JavaScript:void(0);" onclick="ps($x,$y)" #);
			}else{
				out(qq#<td class=s><A HREF="JavaScript:void(0);" onclick="ps($x,$y)" #);
			}
		}else{
			out(qq#<td class=e><A HREF="JavaScript:void(0);" onclick="ps($x,$y)" #);
		}
		if($mode == 1 && $HmainMode ne 'landmap') {
			out(qq#onMouseOver="set_com($x, $y, '$point $alt');window.status = '$point $alt $comStr'; return true;" onMouseOut="not_com();window.status = '';">#);
		}elsif($HmainMode eq 'landmap') {
			out(qq#onMouseOver="window.status = '$point $alt $comStr'; return true;" onMouseOut="window.status = '';">#);
		}
		out("<IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" TITLE=\"$point $alt $comStr\" width=32 height=32 BORDER=0></A></td>");
	}else{
		# 開発画面の場合は、座標設定

		if($mode == 1){
			out("<td class=e><A HREF=\"JavaScript:void(0);\" onclick=\"ps($x,$y)\">");
		}elsif($mode == 3){
#			if(($HspaceID >= 5261) && ($HspaceID <= 5264)){
#				# テストモード
#				$Htestflg = 1;
#				my($test) = $l;
#				if($HspaceID == 5262){
#					$test = $lv;
#				}elsif($HspaceID == 5263){
#					$test = $dis;
#				}elsif($HspaceID == 5264){
#					$test = $nation;
#				}
#				if(($sflg == $mId) && ($sflg > 0) && ($nation > 0)){
#					out("<td bgcolor=#000088 width=60 height=32 style=\"border-style:outset;border-color:#ccccff;border-width:1px;\">${test}");
#				}elsif(($sflg == $HspaceID) && ($sflg > 0) && ($nation > 0)){
#					out("<td bgcolor=#880000 width=60 height=32 style=\"border-style:outset;border-color:#ccccff;border-width:1px;\">${test}");
#				}elsif((($l != $HlandSea) && ($l != $HlandEarth)) && ($nation == 0)){
#					out("<td bgcolor=#666666 width=60 height=32 style=\"border-style:outset;border-color:#ccccff;border-width:1px;\">${test}");
#				}else{
#					out("<td width=60 height=32 style=\"border-style:outset;border-color:#ccccff;border-width:1px;\">${test}");
#				}
#			}elsif($HspaceID == 0){
			if($HspaceID == 0){
				out("<td class=s>");
			}elsif(($sflg == $mId) && ($sflg > 0) && ($nation > 0) && (!$myship)){
				out("<td class=b>");
			}elsif(($sflg == $HspaceID) && ($sflg > 0) && ($nation > 0) && (!$myship)){
				out("<td class=e>");
			}elsif((($l != $HlandSea) && ($l != $HlandEarth)) && ($nation == 0) && (!$myship)){
				out("<td class=i>");
			}else{
				out("<td class=s>");
			}
			out("<A HREF=\"JavaScript:void(0);\" onMouseOver=\"Navi($x, $y,'$image', '$naviTitle', '$naviText', $naviExp);\" onMouseOut=\"NaviClose(); return false\">");
		}elsif($l == $HlandOPlayer){
			# 海域の島

			out("<td class=e>");
			out("<A HREF=\"${HthisFile}?Sight=${sflg}\" target=\"_blank\" \"JavaScript:void(0);\" onMouseOver=\"Navi($x, $y,'$image', '$naviTitle', '$naviText', $naviExp);\" onMouseOut=\"NaviClose(); return false\">");
		}else{
			out("<td class=e>");
			out("<A HREF=\"JavaScript:void(0);\" onMouseOver=\"Navi($x, $y,'$image', '$naviTitle', '$naviText', $naviExp);\" onMouseOut=\"NaviClose(); return false\">");
		}
		my $ntmp = "";
		if(($HdebugMode > 0) && ($nation > 0)){
			my $ntmp2 = ($HdebugMode == $nation) ? "★" : $nation;
			$ntmp = "<span style=\"position:absolute;text-decoration:none;color:#ff0000;font-weight : bold;font-size:12pt;\">$ntmp2</span>";
		}
		out("$ntmp<IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" width=32 height=32 BORDER=0>");

		# 座標設定閉じ
		if(($mode == 1) || ($mode == 3)){
			out("</A></td>");
		}else{
			out("</td>");
		}
	}
	$LandCount{$nation}++;
	$LandCount2{$naviTitle}++;
}# landString

# 霧を表示する

sub landString2 {
	my($l, $lv, $x, $y, $mode, $comStr, $nation, $js) = @_;
	my($point) = "($x,$y)";

	my $image = 'land54.gif';
	my $alt = '濃霧';

	if($js == 1){
		# jsモード
		out(qq#<td class=e><A HREF="JavaScript:void(0);" onclick="ps$point" #);
		if($mode == 1 && $HmainMode ne 'landmap') {
			out(qq#onMouseOver="set_com($x, $y, '$point $alt');window.status = '$point $alt $comStr'; return true;" onMouseOut="not_com();window.status = '';">#);
		}elsif($HmainMode eq 'landmap') {
			out(qq#onMouseOver="window.status = '$point $alt $comStr'; return true;" onMouseOut="window.status = '';">#);
		}
		out("<IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" TITLE=\"$point $alt $comStr\" width=32 height=32 BORDER=0></A></td>");
	}else{
		# 開発画面の場合は、座標設定

		out("<A HREF=\"JavaScript:void(0);\" onclick=\"ps$point\">") if($mode == 1);
		out("<td class=e><IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" width=32 height=32 BORDER=0></td>");
		out("</A>") if($mode == 1); # 座標設定閉じ
	}
	$LandCount{$nation}++;
	$LandCount2{$alt}++;
}

# 霧を表示する位置を保存
sub SearchKiriMons {
	my($land, $landValue) = @_;
	my($special) = 8;
	my($i ,$s , $x, $y, $sx, $sy, $range, $k);
	for($y = 0; $y < $HislandSize; $y++) {
		for($x = 0; $x < $HislandSize; $x++) {
			if((($land->[$x][$y] == $HlandMonster) || ($land->[$x][$y] == $HlandHaribote)) && ($HmonsterSpecial[(monsterSpec($landValue->[$x][$y]))[0]] == $special)) {
				# 霧を発生させる怪獣、ハリボテのとき
				$range = 7;
				$k = 1;
				$s = 1;
			}elsif($land->[$x][$y] == $HlandDefence){
				if($landValue->[$x][$y] == 20){
					$range = 7;
				}elsif($landValue->[$x][$y] == 21){
					$range = 19;
				}else{
					next;
				}
				$k = 2;
				$s = 0;
			}else{
				next;
			}
			# $i = 0;とすれば自身も霧に隠れる

			for($i = $s; $i < $range; $i++) {
				$sx = $x + $ax[$i];
				$sy = $y + $ay[$i];
				$sx-- if(!($sy % 2) && ($y % 2)); # 行による位置調整
				unless(($sx < 0) || ($sx >= $HislandSize) || ($sy < 0) || ($sy >= $HislandSize)){
					$Kiri->[$sx][$sy] = $k if($Kiri->[$sx][$sy] != 1);
				}
			}
		}
	}
}


#----------------------------------------------------------------------
# テンプレートその他
#----------------------------------------------------------------------
# ○○島へようこそ！！
sub tempPrintIslandHead {
	my $mId = $Hislands[$HcurrentNumber]->{'id'};
	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}「${HcurrentName}${AfterName}」${H_tagName}へようこそ！！$_[0]${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}
# ナビゲータ・ウィンドウ
sub tempNavi {
	my($mode) = @_;
	if($mode == 3){
		# 宇宙マップ
		$tHislandSize = $HislandSize;
	}elsif($mode == 4){
		# 海域マップ
		$tHislandSize = $HoceanSize;
	}else{
		$tHislandSize = $HislandSize;
	}
	out(<<END);
<SCRIPT Language="JavaScript">
<!--

MONSTER0 = "人造怪獣";
MONSTER1 = "";
MONSTER2 = "　奇数ターンは硬化";
MONSTER3 = "";
MONSTER4 = "　最大2歩移動する";
MONSTER5 = "　最大何歩移動するか不明";
MONSTER6 = "　偶数ターンは硬化";
MONSTER7 = "";
MONSTER8 = "";
MONSTER9 = "";
MONSTER10 ="";
MONSTER11 ="";
MONSTER12 ="";
MONSTER13 ="";
MONSTER14 ="";
MONSTER15 ="";
MONSTER16 ="";
MONSTER17 ="";
MONSTER18 ="";
MONSTER19 ="";
MONSTER20 ="";
MONSTER21 ="";
MONSTER22 ="";
MONSTER23 ="";
MONSTER24 ="";
MONSTER25 ="";
MONSTER26 ="";
MONSTER27 ="";
MONSTER28 ="";
MONSTER29 ="";
MONSTER30 ="";
MONSTER31 ="";
MONSTER32 ="　ごく一般的な宇宙怪獣";
MONSTER33 ="　動きが素早くそこそこ耐久力がある宇宙怪獣";
MONSTER34 ="　動きがとても素早い宇宙怪獣";
MONSTER35 ="　耐久力が高い宇宙怪獣";

function Navi(x, y, img, title, text, exp) {
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "visible";
	if(x + 1 > $tHislandSize / 2) {
		// 左側
		StyElm.style.marginLeft = (x - 5) * 32 -10;
	} else {
		// 右側
		StyElm.style.marginLeft = (x + 1) * 32;
	}
	if(y + 1 == $tHislandSize) {
		// 下側
		StyElm.style.marginTop = (y - $tHislandSize - 1.5) * 32;
	} else if(y + 1 > $tHislandSize / 2) {
		// 下側
		StyElm.style.marginTop = (y - $tHislandSize - 1) * 32;
	} else {
		// 上側
		StyElm.style.marginTop = (y - $tHislandSize) * 32;
	}
	StyElm.innerHTML = "<table><tr><td class='M'><img class='NaviImg' src=" + img + "><\\/td><td class='M'><div class='NaviTitle'>" + title + " (" + x + "," + y + ")<\\/div><div class='NaviText'>" + text + "<\\/div>";
	if(exp) {
		StyElm.innerHTML += "<br><div class='NaviText'>" + eval(exp) + "<\\/div>";
	}
	StyElm.innerHTML += "<\\/td><\\/tr><\\/table>";
}
function NaviClose() {
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "hidden";
}
//-->
</SCRIPT>
END
}

# ○○島開発計画ヘッダ
sub tempOwnerHeader {
	$monthname = $Hmonthname[($HislandTurn % 12) + 1];
	my $ownername = $Hislands[$HcurrentNumber]->{'ownername'};
	out(<<END);
<CENTER>
${HtagBig_}${HtagNumber_}ターン$HislandTurn　($monthname)${H_tagNumber}${H_tagBig}　${HtagBig_}${HtagName_}${HcurrentName}${AfterName}${H_tagName}開発計画${H_tagBig}<BR>
<FORM name="customform" action="$HthisFile" method="POST" target=_blank>
<INPUT TYPE=HIDDEN NAME=customButton$Hislands[$HcurrentNumber]->{'id'}">
</FORM>
<FORM name="campform" action="$HthisFile" method="POST" target=_blank>
<INPUT TYPE=HIDDEN NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}">
<INPUT TYPE=HIDDEN NAME=camp$Hislands[$HcurrentNumber]->{'id'}">
</FORM>
<FORM name="bbsform" action="$HcampbbsPath" method="POST" target=_blank>
<INPUT TYPE=HIDDEN NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}">
<INPUT TYPE=HIDDEN NAME=campPASS VALUE="$campPass[$Hislands[$HcurrentNumber]->{'ally'}]">
<INPUT TYPE=HIDDEN NAME=campID   VALUE="$Hislands[$HcurrentNumber]->{'ally'}">
</FORM>
<FORM name="chatform" action="$HcampchatPath" method="POST" target=_blank>
<INPUT TYPE=HIDDEN NAME=mode VALUE="top">
<INPUT TYPE=HIDDEN NAME=oNAME VALUE="$Hislands[$HcurrentNumber]->{'ownername'}">
<INPUT TYPE=HIDDEN NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}">
<INPUT TYPE=HIDDEN NAME=campPASS VALUE="$campPass[$Hislands[$HcurrentNumber]->{'ally'}]">
<INPUT TYPE=HIDDEN NAME=campID   VALUE="$Hislands[$HcurrentNumber]->{'ally'}">
</FORM>
[<A HREF="$HthisFile">トップへ戻る</A>]　
[<A href="$HthisFile?Ocean=0" target=_blank>海域へ</A>]　
[<A href="$HthisFile?space=0" target=_blank>宇宙へ</A>${solarwind}]　
[<A HREF="JavaScript:void(0);" onClick="openCUSTOM();return false;">固有設定画面へ</A>]　
END
	if($Hallyflg && $HallyDisp){
		out("[<A HREF=\"JavaScript:void(0);\" onClick=\"openCAMP();return false;\">陣営画面へ</A>]　");
		out("[<A HREF=\"JavaScript:void(0);\" onClick=\"openBBS();return false;\">陣営掲示板へ</A>]　") if($Hcampbbs);
		out("[<A HREF=\"JavaScript:void(0);\" onClick=\"openCHAT();return false;\">陣営会議室へ</A>]") if($Hcampchat);
	}
	out("</CENTER>");
	unless($Hislands[$HcurrentNumber]->{'order'} & 8){
		require('exchange.cgi');
		readExchange();
		infoExchange2($Hislands[$HcurrentNumber]->{'cmdtime'});
	}
}

# ○○島開発計画

sub tempOwner {
	$mapSize = ($HislandSize > $HoceanSize) ? $HislandSize : $HoceanSize;
	tempOwnerHeader();
	out(<<END);
<SCRIPT Language="JavaScript">
<!--
function ps(x, y) {
	if(document.myForm.xy1.checked){
		document.myForm.POINTX.options[x].selected = true;
		document.myForm.POINTY.options[y].selected = true;
	}
	if(document.myForm.xy2.checked){
		document.myForm.POINTTX.options[x].selected = true;
		document.myForm.POINTTY.options[y].selected = true;
	}
	return true;
}

function ns(x) {
	document.myForm.NUMBER.options[x].selected = true;
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
function jump(theForm, j_mode) {
	var sIndex = theForm.TARGETID.selectedIndex;
	var url = theForm.TARGETID.options[sIndex].value;
	if (url != "" ) window.open("$HthisFile?IslandMap=" +url+"&JAVAMODE="+j_mode, "", "menubar=yes,toolbar=no,location=no,directories=no,status=yes,scrollbars=yes,resizable=yes,width=570,height=600");
}

function cn(x, y) {
	for(i=0; i<y; i++) {
		if(document.myForm.COMMAND.options[i].value == x.options[x.selectedIndex].value) {
			document.myForm.COMMAND.options[i].selected = true;
			StatusMsg(x.options[x.selectedIndex].value);
			return true;
		}
	}
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

//-->
</SCRIPT>
END

	islandInfo();

	out(<<END);
<CENTER>
<TABLE BORDER>
<TR>
<TD $HbgInputCell >
<CENTER>
<FORM name="myForm" action="$HthisFile" method=POST>
<B>パスワード</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}">
<HR>
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
<HR>
<B>計画番号</B><SELECT NAME=NUMBER>
END
	# 計画番号

	my($j);
	for($i = 0; $i < $HcommandMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}

	out(<<END);
</SELECT><BR>
<HR>
<B>開発計画</B><BR>
<SELECT NAME=COMMAND onChange=StatusMsg(this.options[this.selectedIndex].value) onClick=StatusMsg(this.options[this.selectedIndex].value)>
END

	#コマンド
	my($kind, $cost, $s);
	for($i = 0; $i < $HcommandTotal; $i++) {
		$kind = $HcomList[$i];
		$cost = $HcomCost[$kind];
		if($cost == 0) {
			$cost = '無料'
		} elsif($cost < 0) {
			$cost = - $cost;
			$cost .= $HunitFood;
		} else {
			$cost .= $HunitMoney;
		}
		if($kind == $HdefaultKind) {
			$s = 'SELECTED';
		} else {
			$s = '';
		}
		out("<OPTION VALUE=$kind $s>$HcomName[$kind]($cost)\n");
	}
	out("</SELECT><HR><B>座標１(</B><SELECT NAME=POINTX>");
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
	out("</SELECT><B>)</B><INPUT TYPE=\"checkbox\" NAME=\"xy2\">");
	out("<HR><B>数量</B><SELECT NAME=AMOUNT>");
	# 数量
	for($i = 0; $i < 50; $i++) {
		out("<OPTION VALUE=$i>$i\n");
	}
	for($i = 50; $i < 999; $i += 50) {
		out("<OPTION VALUE=$i>$i\n");
	}
	out(<<END);
</SELECT>
<HR><B>目標の${AfterName}</B>：
<B><A HREF=JavaScript:void(0); onClick="jump(myForm, '$HjavaMode')"> 表\示 </A></B><BR>
<SELECT NAME=TARGETID>$HtargetList<BR></SELECT>
<HR><B>動作</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>挿入
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>上書き<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>削除<HR>
<INPUT TYPE=submit VALUE="計画送信" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
</CENTER></FORM></TD>
<TD $HbgMapCell>
END
	islandMap(1);	# 島の地図、所有者モード
	out(<<END);
</TD>
<TD $HbgCommandCell>
END
	for($i = 0; $i < $HcommandMax; $i++) {
		tempCommand($i, $Hislands[$HcurrentNumber]->{'command'}->[$i]);
	}
	out(<<END);

</TD>
</TR>
</TABLE></CENTER>
END
}

# 入力済みコマンド表示
sub tempCommand {
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
	$target = $HidToName{$target};
	$target = "無人" if($target eq '');
	$target = "$HtagName_${target}${AfterName}$H_tagName";
	my($value) = $arg * $HcomCost[$kind];
	$value = $HcomCost[$kind] if($value == 0);
	if($value < 0) {
		$value = -$value;
		$value = "$value$HunitFood";
	} else {
		$value = "$value$HunitMoney";
	}
	$value = "$HtagName_$value$H_tagName";

	my($j) = sprintf("%02d：", $number + 1);

	out("<A STYlE=\"text-decoration:none;\" HREF=\"JavaScript:void(0);\" onClick=\"ns($number)\">$HtagNumber_$j$H_tagNumber$HnormalColor_");

	if(($kind == $HcomDoNothing) || ($kind == $HcomGiveup) || ($kind == $HcomSMissileMGM)) {
		out("$name");
	} elsif(($kind == $HcomBioMissile) ||
			($kind == $HcomMissileNM) ||
			($kind == $HcomMissilePP) ||
			($kind == $HcomMissileSPP) ||
			($kind == $HcomMissileST) ||
			($kind == $HcomMissileLD) ||
			($kind == $HcomMissileRM) ||
			($kind == $HcomMissileSRM) ||
			($kind == $HcomMissileGM) ||
			($kind == $HcomMissilePLD) ||
			($kind == $HcomMissileNCM) ||
			($kind == $HcomMissileRNG) ||
			($kind == $HcomMissileDM)) {
		# ミサイル系
		$arg = 1 if($kind == $HcomMissileGM);
		my($n) = ($arg == 0 ? '無制限' : "${arg}発");
		out("$target$pointへ$name($HtagName_$n$H_tagName)");
	} elsif($kind == $HcomMissileMGM) {
		out("$targetへ$name");
	} elsif($kind == $Hcomcolony){
		if(($arg == 1) || ($arg == 2)) {
			out("スーパーシールドシステム発動！！($arg)");
		}else{
			out("$targetへ$name");
		}
	} elsif(($kind == $HcomTeisatu) ||
			($kind == $HcomSpy)) {
		# 工作員、偵察
		out("$target$pointへ$name");
	} elsif($kind == $HcomSendMonster) {
		# 怪獣派遣
		if($arg == 1) {
			out("$targetへメカジラ派遣");
		} elsif($arg == 2) {
			out("$targetへグラテネスいのら派遣");
		} elsif($arg == 3) {
			out("$targetへ海底メカいのら派遣");
		} else {
			out("$targetへメカいのら派遣");
		}
	} elsif($kind == $HcomSSendMonster) {
		# S怪獣派遣
		$arg = $HmonsterNumber - 1 if($arg >= $HmonsterNumber);
		out("$targetへ$name($HmonsterName[$arg])");
	} elsif($kind == $HcomSell) {
		# 食料売却
		out("$name$value");
	} elsif(($kind == $HcomOreSell) || ($kind == $HcomOilSell) || ($kind == $HcomWeponSell)){
		# 売却
		$arg = 1 if($arg <= 0);
		out("$targetへ$name($arg)");
	} elsif(($kind == $HcomOreBuy) || ($kind == $HcomOilBuy) || ($kind == $HcomWeponBuy)){
		# 購入
		$arg = 1 if($arg <= 0);
		out("$name($arg)");
	} elsif($kind == $HcomWarp) {
		# 転移装置
		if($arg == 0) {
			out("$pointで$name(${target}行き)");
		} else {
			# 転移先装置作成
			my($s);
			if($arg == 1) {
				$s = '右上';
			} elsif($arg == 2) {
				$s = '右';
			} elsif($arg == 3) {
				$s = '右下';
			} elsif($arg == 4) {
				$s = '左下';
			} elsif($arg == 5) {
				$s = '左';
			} else {
				$arg = 6;
				$s = '左上';
			}
			$name = "${HtagComName_}転移先装置建設${H_tagComName}";
			out("$pointで$name($s)");
		}
	} elsif($kind == $HcomPropaganda) {
		# 誘致活動
		if($arg == 0) {
			out("$name");
		} else {
			out("$name($arg回)");
		}
	} elsif(($kind == $HcomMoney) || ($kind == $HcomFood)) {
		# 援助

		out("$targetへ$name$value");
	} elsif($kind == $HcomEmigration) { # 移民
		out("$pointの人を$targetへ$name");
	} elsif($kind == $HcomDestroy) {
		# 掘削

		if($arg != 0) {
			out("$pointで$name(予算${value})");
		} else {
			out("$pointで$name");
		}
	} elsif(($kind == $HcomSearch) || ($kind == $HcomBank)) {
		# 地質調査,銀行投資

		out("$pointで$name(予算${value})");
	} elsif($kind == $HcomDummy) {
		if($arg == 1) {
			out("$pointでダミー採掘場");
		} elsif($arg == 2) {
			out("$pointでダミー埋め立て");
		} else {
			out("$pointでダミー農場");
		}
	} elsif(($kind == $HcomManipulate) || ($kind == $HcomSTManipulate) || ($kind == $HcomShipM)) {
		# 怪獣操作、ST怪獣操作、船操作
		my($s);
		if($arg <= 1) {
			$arg = 1;
			$s = '右上';
		} elsif($arg == 2) {
			$s = '右';
		} elsif($arg == 3) {
			$s = '右下';
		} elsif($arg == 4) {
			$s = '左下';
		} elsif($arg == 5) {
			$s = '左';
		} else {
			$arg = 6;
			$s = '左上';
		}
		if($kind == $HcomMonsEnsei){
			out("$name($s)");
		}else{
			out("$targetへ$name($s)");
		}
	} elsif($kind == $HcomMonument) {
		# 記念碑
		if($arg <= 3) {
			out("$pointで${name}($HmonumentName[$arg])");
		} else {
			out("$pointで$name");
		}
	} elsif($kind == $HcomSMonument) {
		# 海底記念碑
		if($arg <= 3) {
			out("$pointで${name}($HsmonumentName[$arg])");
		} else {
			out("$pointで$name");
		}
	} elsif($kind == $HcomDbase) {
		if($arg == 1) {
			out("$pointで${name}(ST)");
		} elsif($arg == 2) {
			out("$pointで${name}(霧)");
		} else {
			out("$pointで$name");
		}
	} elsif(($kind == $HcomFarm) ||
		 ($kind == $HcomSFarm) ||
		 ($kind == $HcomFactory) ||
		 ($kind == $HcomTower) ||
		 ($kind == $HcomPort) ||
		 ($kind == $HcomBase) ||
		 ($kind == $HcomMountain)) {
		# 回数付き
		if($arg == 0) {
			out("$pointで$name");
		} else {
			out("$pointで$name($arg回)");
		}
	} elsif(($kind == $HcomPresent) ||
		 ($kind == $HcomPresentAid)) {
		# プレゼント、プレゼント譲渡
		my($s);
		if($arg <= 0) {
			$arg = 0;
			$s = '公園';
		} elsif($arg == 1) {
			$s = 'スタジアム';
		} elsif($arg == 2) {
			$s = 'ドーム';
		} elsif($arg == 3) {
			$s = 'カジノ';
		} elsif($arg == 4) {
			$s = '遊園地';
		} elsif($arg == 5) {
			$s = '学校';
		} elsif($arg == 6) {
			$s = '空港';
		} elsif($arg == 7) {
			$s = '大都市';
		} elsif($arg == 8) {
			$s = '動物園';
		} elsif($arg == 9) {
			$s = '博覧会';
		} elsif($arg == 10) {
			$s = '怪獣記念碑';
		} else {
			$arg = 11;
			$s = '災害の碑';
		}
		if($kind == $HcomPresent) { 
			out("$pointで$name($s)");
		} else {
			out("$targetへ$name($s)");
		}
	# 怪獣バトル

	} elsif(($kind == $HcomMonsEgg) ||
		 ($kind == $HcomMonsEsa) ||
		 ($kind == $HcomMonsTettai) ||
		 ($kind == $HcomMonsExer) ||
		 ($kind == $HcomMonsSell)) {
		out("$name");
	} elsif(($kind == $HcomMonsEnsei) ||
		 ($kind == $HcomMonsEsaAid) ||
		 ($kind == $HcomMonsAid)) {
		out("$targetへ$name");
	} elsif($kind == $HcomShip) {
		# 船指令変更
		my($s);
		if($arg <= 0) {
			$arg = 0;
			$s = '特殊';
		} elsif($arg == 1) {
			$s = '移動';
		} elsif($arg == 2) {
			$s = '防御';
		} elsif($arg == 3) {
			$s = '撤退';
		} elsif($arg >= 4) {
			$s = '攻撃';
			$arg = 4;
		}
		out("$target$pointに$name($s)");
	} elsif($kind == $HcomShipbuild) {
		# 造船
		out("$pointで$name($arg)");
	} elsif($kind == $HcomSBuild) {
		# 宇宙建設系
		out("今後拡張予定命令(何もおきません)");
	} elsif(($kind == $HcomSUnit) ||
			($kind == $HcomSpaceFarm) ||
			($kind == $HcomSFactory) ||
			($kind == $HcomSEisei) ||
			($kind == $HcomSpaceBase)) {
		$target = "$HtagName_$SpaceName$H_tagName";
		# 回数付き
		if($arg == 0) {
			out("$target$pointで$name");
		} else {
			out("$target$pointで$name($arg回)");
		}
	} elsif(($kind == $HcomSPioneer) ||
			($kind == $HcomSDestroy) ||
			($kind == $HcomSDbase) ||
			($kind == $HcomSOccupy)) {
		$target = "$HtagName_$SpaceName$H_tagName";
		out("$target$pointで$name");
	} elsif(($kind == $HcomSMissileGM) ||
			($kind == $HcomSMissilePP) ||
			($kind == $HcomSMissile)){
		my($n) = ($arg == 0 ? '無制限' : "${arg}発");
		$target = "$HtagName_$SpaceName$H_tagName";
		out("$target$pointへ$name($HtagName_$n$H_tagName)");
	} elsif(($kind == $HcomOMissileNM) ||
			($kind == $HcomOMissilePP) ||
			($kind == $HcomOMissileSPP)){
		my($n) = ($arg == 0 ? '無制限' : "${arg}発");
		$target = "$HtagName_$OceanName$H_tagName";
		out("$target$pointへ$name($HtagName_$n$H_tagName)");
	} elsif($kind == $HcomSFood) {
		# 宇宙食料打上げ
		$value = ($arg < 1)? 100 : $arg * 100;
		$value = "$HtagName_$value$HunitFood$H_tagName";
		out("$name$value");
	} else {
		# 座標付き
		out("$pointで$name");
	}
	out("${H_normalColor}</A><BR>");
}

# コメント、ローカル掲示板チェック
sub tempCLbbs {
	out(<<END);
<SCRIPT Language="JavaScript">
<!--
function clbbsSubmit(){
	newClbbs = window.open("", "newClbbs");
	document.clbbsForm.target = "newClbbs";
//	document.clbbsForm.submit();
}
//-->
</SCRIPT>
<hr>
<FORM name="clbbsForm" action="$HthisFile" method="POST">
<INPUT TYPE=submit value="コメント・観光者通信・近況・怪獣バトル・地下表示" NAME=CLbbsRButton$Hislands[$HcurrentNumber]->{'id'} onClick="clbbsSubmit()">
</FORM>
END
	my($comment) = $Hislands[$HcurrentNumber]->{'comment'};
	out("コメント：$comment<br>");
	my $lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
	$line = $lbbs->[0];
	if($line =~ /([0-9]*)\<(.*)\<([0-9]*)\>(.*)\>(.*)$/) {
		my($bbs1,$bbs2,$bbs3,$bbs4,$bbs5) = ($1,$2,$3,$4,$5);
		if($bbs4){
			$bbs4 =~ /([0-9]*)/;
			out("最新の観光者通信書き込み: $1 ターン目<br>");
		}
	}
	my($monster) = ($island->{'monster'});
	if($monster->[0] != 0) {
		my($tn) = $HidToNumber{$monster->[2]};
		my($mname) = $monster->[1];
		if($tn ne '') {
			out("怪獣バトル対戦中！！<br>");
		}else{
			out("飼育怪獣：$mname<br>");
		}
	}
}

# コメント・観光者通信・近況を表示
sub clbbsMain {
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};
	$monthname = $Hmonthname[($HislandTurn % 12) + 1];
	out(<<END);
<CENTER>
${HtagBig_}${HtagNumber_}ターン$HislandTurn　($monthname)${H_tagNumber}${H_tagBig}　${HtagBig_}${HtagName_}${HcurrentName}${AfterName}${H_tagName}${H_tagBig}<BR>
<a href="Javascript:void(0);" onclick="window.close()">画面を閉じる</A>
</CENTER>
END
	ugMap($island,2);	# 地下
	if($island->{'order'} & 64){
		tempLocalbbs(1);	# ローカル掲示板
		tempRecent(1);		# 近況
	}else{
		tempRecent(1);		# 近況
		tempLocalbbs(1);	# ローカル掲示板
	}
	tempCommentInput();	# コメント入力フォーム

	tempMapTotal();		# マップ集計
}

# カスタマイズ画面を表示
sub customMain {
	my($mode) = @_;
	# idから島を取得
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};
	$monthname = $Hmonthname[($HislandTurn % 12) + 1];
	my($i,@ccbx);
	if($mode){
		# メッセージを更新
		for($i = 0; $i < 12; $i++) {
			if($Hcustom[$i]){
				$island->{'order'} |= 2 ** $i;
			}else{
				$island->{'order'} ^= 2 ** $i if($island->{'order'} & 2 ** $i);
			}
		}
		# データの書き出し
		if(!writeIslandsFile($HcurrentID, 1)) {
			unlock();
			tempFailWrite();
			return;
		}
		out("${HtagBig_}データを更新しました${H_tagBig}<HR>");
	}
	for($i = 0; $i < 12; $i++) {
		if($island->{'order'} & 2 ** $i){
			$ccbx[$i] = " CHECKED";
		}else{
			$ccbx[$i] = "";
		}
	}
	out(<<END);
<CENTER>
${HtagBig_}${HtagNumber_}ターン$HislandTurn　($monthname)${H_tagNumber}${H_tagBig}　${HtagBig_}${HtagName_}${HcurrentName}${AfterName}${H_tagName}${H_tagBig}<BR>
$HtempBack<br>
<h1>各${AfterName}ごとの固有設定</h1>
<FORM name="customMain" action="$HthisFile" method="POST">
<table>
<INPUT TYPE="checkbox" NAME="custom4"$ccbx[4]>自動怪獣誘導弾発射(怪獣がいると強制的に怪獣誘導弾発射)<br>
<INPUT TYPE="checkbox" NAME="custom5"$ccbx[5]>採掘場は資金を生産する。(チェックをはずすと鉱石を生産)<br>
<INPUT TYPE="checkbox" NAME="custom7"$ccbx[7]>工場は資金を生産する。(チェックをはずすと兵器を生産)<br>
<INPUT TYPE="checkbox" NAME="custom11"$ccbx[11]>油田は資金を生産する。(チェックをはずすと原油を生産)<br>
<INPUT TYPE="checkbox" NAME="custom3"$ccbx[3]>更新された取引情報を表示しない。<br>
<INPUT TYPE="checkbox" NAME="custom8"$ccbx[8]>開発モードで観光者通信・最近のログ等を別画面化(却下された仕様らしい・・・)<br>
<INPUT TYPE="checkbox" NAME="custom6"$ccbx[6]>開発モードで観光者通信→近況の順番にする。<br>
<INPUT TYPE="checkbox" NAME="custom9"$ccbx[9]>天候不順で中止された命令を残す(最大１０回まで)<br>
<INPUT TYPE="checkbox" NAME="custom10"$ccbx[10]>消防署火災自動復旧機能を使う<br>
</table>
<INPUT TYPE=submit value="更新" NAME=customMButton$Hislands[$HcurrentNumber]->{'id'}">
</FORM>
</CENTER>
<h2>自動怪獣誘導弾発射</h2>
ターン開始時にどんな怪獣だろうと自島に１匹以上の怪獣がいると、<br>
命令の０１に強制的に怪獣誘導弾発射が挿入され実行されます。<br>
怪獣誘導弾発射が自動発射された場合、本来の０１の命令は、実行されません。(内政ならば実行されます)<br>
何らかの原因で既に怪獣がいない場合は、中止のログが流れますが、本来の０１の命令が実行されます。<br>
毎ターンチェックできない人にやさしい？かもしれない機能です。<br>

<h2>天候不順で中止された命令を残す</h2>
海底都市建設、ロケット打ち上げ、コロニー落としが天候不順により中止されても、<br>
当機能を使用すると、命令予定項目から消えません。ただし１０回までです。<br>
(仮に海底都市が１１個並んでいたとしたら１１個目は消える)<br>
命令が行われなくて資金繰りになる場合があります。当然ながら規定ターン数資金繰りした場合、<br>
命令があったとしても自動放棄が命令の先頭に上書きされます。<br>
<h2>消防署火災自動復旧機能</h2>
火災で消防署自身が燃えちゃったターンに、元あった座標に自動で建設命令が一番上に入力されます。<br>
(地上の場合は地ならしも)命令がギッシリ詰まっていたら、後ろが切れちゃいます。<br>
戦争中だったとしても問答無用で命令が一番上に入っちゃってうざったいかも・・・。<br>
ようするに、半放置プレイしているしている方に便利かも！？しれない機能です。<br>
END
}

# 地下の表示
sub ugMap {
	my($island,$mode) = @_;

	# 地形、地形値を取得
	my($ugL,$ugV) = ($island->{'ugL'},$island->{'ugV'});
	my($i);
	out("<div id='islandMap'><table border=0 cellspacing=0 cellpadding=0><tr>");
	for($i = 0; $i < $HugMax; $i++) {
		my($ugX) = $island->{'ugX'}->[$i];
		my($ugY) = $island->{'ugY'}->[$i];
		if($island->{'land'}->[$ugX][$ugY] != $HlandDokan){
			next;
		}
		if($mode == 0){
			$ugX = "?";
			$ugY = "?";
		}
		out("<td><table border=0 cellspacing=0 cellpadding=0><tr>");
		out("<td colspan=3>地下${i}($ugX,$ugY)</td></tr><tr>");
		ugString($ugL->[$i][0], $ugV->[$i][0], 0, 0, $mode, $ugX, $ugY);
		ugString($ugL->[$i][1], $ugV->[$i][1], 1, 0, $mode, $ugX, $ugY);
		ugString($ugL->[$i][2], $ugV->[$i][2], 2, 0, $mode, $ugX, $ugY);
		out("</tr><tr>");
		ugString($ugL->[$i][3], $ugV->[$i][3], 0, 1, $mode, $ugX, $ugY);
		ugString($ugL->[$i][4], $ugV->[$i][4], 1, 1, $mode, $ugX, $ugY);
		ugString($ugL->[$i][5], $ugV->[$i][5], 2, 1, $mode, $ugX, $ugY);
		out("</tr><tr>");
		ugString($ugL->[$i][6], $ugV->[$i][6], 0, 2, $mode, $ugX, $ugY);
		ugString($ugL->[$i][7], $ugV->[$i][7], 1, 2, $mode, $ugX, $ugY);
		ugString($ugL->[$i][8], $ugV->[$i][8], 2, 2, $mode, $ugX, $ugY);
		out("</tr></table></td>");
	}
	out("</td></tr></table></div>");
}
# 地下を表示
sub ugString {
	my($l, $lv, $x, $y, $mode, $xx, $yy) = @_;
	my $image = $HugImage[$l];
	my $alt = $Hunderground[$l];
	$alt .= "(${lv}$HunitPop)" if($l == $HugTosi);
	out("<td class=e>");
	# 開発画面の場合は、座標設定

	out(qq#<A HREF="JavaScript:void(0);" onclick="ps($x,$y,$xx,$yy)" onMouseOver="window.status = '($x,$y) $alt'; return true;" onMouseOut="window.status = '';">#) if($mode == 1);

	out("<IMG SRC=\"$image\" ALT=\"($x,$y) $alt\" width=32 height=32 BORDER=0>");

	# 座標設定閉じ
	out("</A>") if($mode == 1);
	out("</td>");
}

# コメント入力フォーム

sub tempCommentInput {
	out("<DIV ID='CommentBox'>");
	islandmonster(0);# 島の怪獣
	my($comment) = $Hislands[$HcurrentNumber]->{'comment'};
	my($select0, $select1, $select2, $select3, $select4);
	$select0 = ' CHECKED' if($Hislands[$HcurrentNumber]->{'commentLabel0'});
	$select1 = ' CHECKED' if($Hislands[$HcurrentNumber]->{'commentLabel1'});
	$select2 = ' CHECKED' if($Hislands[$HcurrentNumber]->{'commentLabel2'});
	$select3 = ' CHECKED' if($Hislands[$HcurrentNumber]->{'commentLabel3'});
	$select4 = ' CHECKED' if($Hislands[$HcurrentNumber]->{'commentLabel4'});

	#ラベルをスイッチ形式にする場合に整形
	my($label0_1n,$label0_2n) = split(/<>/,$HlabelName[0]);
#	my($label1_1n,$label1_2n) = split(/<>/,$HlabelName[1]);
#	my($label2_1n,$label2_2n) = split(/<>/,$HlabelName[2]);
#	my($label3_1n,$label3_2n) = split(/<>/,$HlabelName[3]);
#	my($label4_1n,$label4_2n) = split(/<>/,$HlabelName[4]);
	
	#コメントラベル4未使用。利用する場合は以下のHTMLでCheckboxを追加する by ShibaAni
	out(<<END);
<HR>
${HtagBig_}コメント更新${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER><TR>
<TH $HbgTitleCell>コメント</TH><TD $HbgNameCell colspan="3"><INPUT TYPE=text NAME=MESSAGE SIZE=110 VALUE="$comment"></TD>
</TR><TR>
<TH $HbgTitleCell rowspan=2>意志表示</TH><TD $HbgNameCell rowspan=2>
<INPUT TYPE=checkbox NAME="COMMENT_LABEL0" VALUE="1"$select0>$label0_1n<br>
<INPUT TYPE=checkbox NAME="COMMENT_LABEL1" VALUE="1"$select1>$HlabelName[1]<br>
<INPUT TYPE=checkbox NAME="COMMENT_LABEL2" VALUE="1"$select2>$HlabelName[2]<br>
<INPUT TYPE=checkbox NAME="COMMENT_LABEL3" VALUE="1"$select3>$HlabelName[3]
</TD>
<TH $HbgTitleCell>パスワード</TH><TD $HbgNameCell><INPUT TYPE=password NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}"></TD>
</TR><TR>
<TD $HbgTitleCell colspan=2 align=center><INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
<INPUT TYPE=submit VALUE="コメント更新" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
</TD></TR></TABLE>
※　意志表示に強制力はなく、${AfterName}主の気持ちを表す手段の一つにすぎません。
</FORM></DIV>
END
}

# ○○島ローカル掲示板
sub tempLocalbbs {
	my($mode) = @_;
	if($HuseLbbs) {
		out("<DIV ID='localBBS'><HR>");
		if($mode == 0){
			out("${HtagBig_}${HtagName_}${HcurrentName}${AfterName}${H_tagName}観光者通信${H_tagBig}<BR>");
			tempLbbsInput();   # 書き込みフォーム

			tempLbbsContents(); # 掲示板内容
		}elsif($mode == 1){
			out("${HtagBig_}${HtagName_}${HcurrentName}${AfterName}${H_tagName}観光者通信${H_tagBig}<BR>");
			tempLbbsInputOW();
			tempLbbsContents(); # 掲示板内容
		}elsif($mode == 3){
			out("${HtagBig_}${HtagName_}「宇宙マップ」${H_tagName}観光者通信${H_tagBig}<BR>");
			tempLbbsInput();   # 書き込みフォーム

			tempLbbsContents(3); # 掲示板内容
		}elsif($mode == 4){
			out("${HtagBig_}${HtagName_}「海域マップ」${H_tagName}観光者通信${H_tagBig}<BR>");
			tempLbbsInput();   # 書き込みフォーム

			tempLbbsContents(4); # 掲示板内容
		}
		out("</DIV>");
	}
}


# ローカル掲示板入力フォーム

sub tempLbbsInput {
	if ($HlbbsAuth) {
	out(<<END);
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>名前</TH>
<TH $HbgTitleCell>内容</TH>
</TR>
<TR>
<TD $HbgInfoCell><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD $HbgInfoCell><INPUT TYPE="text" SIZE=100 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TD $HbgInfoCell colspan="2">自分の島：<SELECT NAME="ISLANDID">$HislandList</SELECT>
END
	out(<<END) if($HlbbsAnon);
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="ANON">観光客
END
	out(<<END);
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="PUBLIC" CHECKED>公開
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="SECRET"><FONT COLOR="red">極秘</FONT>
　パスワード：<INPUT TYPE="password" SIZE=16 MAXLENGTH=32 NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}">
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonFO$HcurrentID">
番号<SELECT NAME=NUMBER>
END
	# 発言番号

	my($j, $i);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}
	out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="削除する" NAME="LbbsButtonFD$HcurrentID">
</TD></TR>
</TABLE>
</FORM>
END
	}else{
	out(<<END);
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>名前</TH>
<TH $HbgTitleCell>内容</TH>
<TH $HbgTitleCell>動作</TH>
</TR>
<TR>
<TD $HbgInfoCell><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD $HbgInfoCell><INPUT TYPE="text" SIZE=100 NAME="LBBSMESSAGE"></TD>
<TD $HbgInfoCell><INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonSS$HcurrentID"></TD>
</TR>
</TABLE>
</FORM>
END
	}
}

# ローカル掲示板入力フォーム owner mode用
sub tempLbbsInputOW {
	out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>名前</TH>
<TH $HbgTitleCell colspan=2>内容</TH>
</TR>
<TR>
<TD $HbgInfoCell><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD $HbgInfoCell colspan=2><INPUT TYPE="text" SIZE=100 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH $HbgTitleCell>パスワード</TH>
<TH $HbgTitleCell colspan=2>動作</TH>
</TR>
<TR>
<TD $HbgInfoCell><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}"></TD>
<TD $HbgInfoCell align=right>
<INPUT TYPE="submit" VALUE="記帳する" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD $HbgInfoCell align=right>
番号

<SELECT NAME=NUMBER>
END
	# 発言番号

	my($j, $i);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}
	out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="削除する" NAME="LbbsButtonDL$HcurrentID">
</TD>
</TR>
</TABLE>
</FORM>
END
}

# ローカル掲示板内容
sub tempLbbsContents {
	my($lbbs, $line, $ally);
	if($_[0] == 3){
		$lbbs = $Hspace->{'lbbs'};
	}elsif($_[0] == 4){
		$lbbs = $Hocean->{'lbbs'};
	}else{
		$lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
		$ally = $Hislands[$HcurrentNumber]->{'ally'};
	}
	out(<<END);
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>番号</TH>
<TH $HbgTitleCell>記帳内容</TH>
</TR>
END

	my($i);
	for($i = 0; $i < $HlbbsMax; $i++) {
	$line = $lbbs->[$i];
	if($line =~ /([0-9]*)\<(.*)\<([0-9]*)\>(.*)\>(.*)$/) {
		my($j) = $i + 1;
		out("<TR><TD $HbgSubTCell>$HtagNumber_$j$H_tagNumber</TD>");
		my $speaker;
		if($3 == 0){
			my($sName, $sID) = split(/,/, $2);
			my $sNo = $HidToNumber{$sID};
			if($HlbbsSpeaker && ($sName ne '')){
				if(defined $sNo){
					$speaker = "<FONT COLOR=gray><B><SMALL>(<A HREF=\"$HthisFile?Sight=$sID\" class=\"M\">$sName</A>)</SMALL></B></FONT>";
				} else {
					$speaker = "<FONT COLOR=gray><B><SMALL>($sName)</SMALL></B></FONT>";
				}
			}
			# 観光者
			if ($1 == 0) {
				# 公開
				out("<TD $HbgLbbsCell>$HtagLbbsSS_$4 > $5$H_tagLbbsSS $speaker</TD></TR>");
			} else {
				# 極秘

				if(($Hallybbs) && ($HprintAlly == $ally) && ($HprintAlly > 0)){
					out("<TD $HbgLbbsCell>$HtagLbbsSS_$4 >(陣) $5$H_tagLbbsSS $speaker</TD></TR>");
				}else{
					if(($HmainMode ne 'owner') && (($HprintID != $sID) || ($sID == 0))) {
						# 観光客
						out("<TD $HbgLbbsCell><CENTER><FONT COLOR=gray>- 極秘 -</FONT></CENTER></TD></TR>");
					} else {
						# オーナー
						out("<TD $HbgLbbsCell>$HtagLbbsSS_$4 >(秘) $5$H_tagLbbsSS $speaker</TD></TR>");
					}
				}
			}
		} else {
			# 島主

			$speaker = "<FONT COLOR=gray><B><SMALL>$2</SMALL></B></FONT>" if($HlbbsSpeaker && ($2 ne ''));
			out("<TD $HbgLbbsCell>$HtagLbbsOW_$4 > $5$H_tagLbbsOW $speaker</TD></TR>");
		}
	}
	}

	out(<<END);
</TD></TR></TABLE>
END
}

# ローカル掲示板で名前かメッセージがない場合

sub tempLbbsNoMessage {
	out(<<END);
${HtagBig_}名前または内容の欄が空欄です。${H_tagBig}$HtempBack
END
}

# 書きこみ削除

sub tempLbbsDelete {
	out(<<END);
${HtagBig_}記帳内容を削除しました${H_tagBig}<HR>
END
}

# コマンド登録
sub tempLbbsAdd {
	out(<<END);
${HtagBig_}記帳を行いました${H_tagBig}<HR>
END
}

# コマンド削除

sub tempCommandDelete {
	out(<<END);
${HtagBig_}コマンドを削除しました${H_tagBig}<HR>
END
}

# コマンド登録
sub tempCommandAdd {
	out(<<END);
${HtagBig_}コマンドを登録しました${H_tagBig}<HR>
END
}

# コメント変更成功

sub tempComment {
	out(<<END);
${HtagBig_}コメントを更新しました${H_tagBig}<HR>
END
}
# 怪獣設定変更成功

sub tempmonsedit {
	out(<<END);
${HtagBig_}怪獣設定を更新しました${H_tagBig}<HR>
END
}

# 近況
sub tempRecent {
	my($mode) = @_;
	out(<<END);
<HR><DIV ID='RecentlyLog2'>
${HtagBig_}${HtagName_}${HcurrentName}${AfterName}${H_tagName}の近況${H_tagBig}<BR>
END
	my($i);
	for($i = 0; $i < $HlogMax; $i++) {
		logFilePrint($i, $HcurrentID, $mode);
	}
	out("</DIV>");
}
# マップ集計表
sub tempMapTotal {
	if($HdebugMode > 0){
		out("<hr><DIV ID='mapStatistics'>地名の集計表");
		out("<table border=0 cellspacing=0 cellpadding=0>");
		out("<tr><td $HbgTitleCell>地名</td><td $HbgTitleCell>個数</td><td $HbgTitleCell>割合</td></tr>");
		foreach (sort { $LandCount2{$b} <=> $LandCount2{$a} } keys %LandCount2) {
			my $w = int($LandCount2{$_} * 10000 / $HpointNumber + 0.5) / 100;
			out("<tr><td $HbgTitleCell>$_ </td><td $HbgInfoCell>$LandCount2{$_}</td><td $HbgInfoCell>　${w}％</td></tr>");
		}
		out("</table></DIV>\n");
	}
	out("<br><DIV ID='mapStatistics'>${AfterName}占有数表");
	out("<table border=0 cellspacing=0 cellpadding=0>");
	out("<tr><td $HbgTitleCell>${AfterName}名</td><td $HbgTitleCell>個数</td><td $HbgTitleCell>割合</td></tr>");
	foreach (sort { $LandCount{$b} <=> $LandCount{$a} } keys %LandCount) {
		my $w = int($LandCount{$_} * 10000 / $HpointNumber + 0.5) / 100;
		my($island,$name);
		if($_ > 0){
			$island = $Hislands[$HidToNumber{$_}];
			if($HidToNumber{$_} eq ''){
				$name = "不明";
			}else{
				$name = $island->{'name'} . $AfterName;
			}
		}else{
			$name = "自島";
		}
		out("<tr><td $HbgTitleCell>${name}</td><td $HbgInfoCell>$LandCount{$_}</td><td $HbgInfoCell>　${w}％</td></tr>");
	}
	out("</table></DIV>\n");
}
# 島の移動
sub islandJamp {
	$HtargetList = getIslandList($HcurrentID);
	out(<<END);
<CENTER>
<SCRIPT LANGUAGE="JavaScript">
function jump(theForm) {
	var sIndex = theForm.urlsel.selectedIndex;
	var url = theForm.urlsel.options[sIndex].value;
	if (url != "" ) location.href = "$HthisFile?Sight=" +url;
}
</SCRIPT>
<TABLE align=center border=0>
<TR><TD>
<FORM name="urlForm">
<SELECT NAME="urlsel">
$HtargetList<BR>
</SELECT>
</TD>
<TD><input type="button" value=" GO " onClick="jump(this.form)"></TD>
</TR></TABLE>
</form>
</CENTER>
END
}

# JSモードでパスワード間違い時に関数が無くてエラーが出る問題用
sub Dummyfunction {
	out(<<END);
<SCRIPT LANGUAGE="JavaScript">
function SelectList(theForm){}
function init() {}
</SCRIPT>
END
}

sub islandmonster {
	my($mode) = @_;
	# 各要素の取り出し
	
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($name,$monster) = ($island->{'name'},$island->{'monster'});
	my($MBsId,$MBmId) = ($monster->[3],$monster->[4]);
	
	my($tn) = $HidToNumber{$monster->[2]};
	my($tMonster,$tIsland,$tName,$tMBsId, $tMBmId);

	if($tn eq '') {
	} else {
		# 対戦相手がいるとき
		$tIsland = $Hislands[$tn];
		$tName = $tIsland->{'name'};
		$tMonster = $tIsland->{'monster'};
		($tMBsId, $tMBmId) = ($tMonster->[3],$tMonster->[4]);
	}

	my($MBidName);
	if($monster->[0] == 0) {
		return;
	} else {
		my($monsIsland) = $Hislands[$HidToNumber{$monster->[0]}];
		$MBidName = $monsIsland->{'name'};
		$MBidName = "$MBidName$AfterName";
	}

	# 怪獣画像処理
	my $image = $HmonsterImage[$MBmId];
	my $special = $HmonsterSpecial[$MBmId];
	# 硬化中?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
		(($special == 4) && (($HislandTurn % 2) == 0))) {
		$image = $HmonsterImage2[$MBmId];
	}
	$image = $island->{'monsurl'} if(substr($island->{'monsurl'},0,7) eq 'http://');
	
	my $image2 = $HmonsterImage[$tMBmId];
	$special = $HmonsterSpecial[$tMBmId];
	# 硬化中?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
		(($special == 4) && (($HislandTurn % 2) == 0))) {
		$image2 = $HmonsterImage2[$tMBmId];
	}
	$image2 = $tIsland->{'monsurl'} if(substr($tIsland->{'monsurl'},0,7) eq 'http://');
	
	my($seityou) = $monster->[7] + $monster->[8] + $monster->[9] + $monster->[10];
	my($tseityou) = $tMonster->[7] + $tMonster->[8] + $tMonster->[9] + $tMonster->[10];

	$MBmId = ($MBmId == 0) ? "　" : $HmonsterName[$MBmId];
	$MBsId = ($MBsId == 0) ? "無" : $HmonsterName[$MBsId];
	$tMBmId = ($tMBmId == 0) ? "　" : $HmonsterName[$tMBmId];
	$tMBsId = ($tMBsId == 0) ? "無" : $HmonsterName[$tMBsId];
	
	if($seityou < 12) {
		$seityou = "幼年";
	} elsif($seityou < 25) {
		$seityou = "壮年";
	} else {
		$seityou = "老年";
	}
	if($tseityou < 12) {
		$tseityou = "幼年";
	} elsif($tseityou < 25) {
		$tseityou = "壮年";
	} else {
		$tseityou = "老年";
	}

	out(<<END);
<hr>
<center>
<table border>
<tr>
<th $HbgTitleCell colspan=14>${HtagTH_}怪獣バトル${H_tagTH}</th>
</tr>
<tr>
<td $HbgSubTCell>島</td>
<td $HbgSubTCell>怪獣名</td>
<td $HbgSubTCell>外観</td>
<td $HbgSubTCell>元怪獣</td>
<td $HbgSubTCell>勝数</td>
<td $HbgSubTCell>負数</td>
<td $HbgSubTCell>成長</td>
<td $HbgSubTCell>HP</td>
<td $HbgSubTCell>攻撃</td>
<td $HbgSubTCell>守備</td>
<td $HbgSubTCell>回避</td>
<td $HbgSubTCell>命中</td>
<td $HbgSubTCell>居場所</td>
<td $HbgSubTCell>餌</td>
</tr>
<tr>

<td $HbgInfoCell>$name$AfterName</td>
<td $HbgInfoCell>$monster->[1]</td>
<td $HbgInfoCell><IMG SRC=\"$image\" width=32 height=32 BORDER=0></td>
<td $HbgInfoCell>$MBmId</td>
<td $HbgInfoCell>$monster->[12]</td>
<td $HbgInfoCell>$monster->[13]</td>
<td $HbgInfoCell>$seityou</td>
<td $HbgInfoCell>$monster->[5]/$monster->[6]</td>
<td $HbgInfoCell>$monster->[7]</td>
<td $HbgInfoCell>$monster->[8]</td>
<td $HbgInfoCell>$monster->[9]</td>
<td $HbgInfoCell>$monster->[10]</td>
<td $HbgInfoCell>$MBidName</td>
<td $HbgInfoCell>$MBsId</td>

</tr>
END
	if($tMonster->[0] == 0) {
		# 相手がいない。
	out(<<END);
</TABLE></CENTER>
END
	} else {
	out(<<END);
<tr>
<td $HbgSubTCell colspan=14>${HtagDisaster_}VERSUS${H_tagDisaster}</td>
</tr>
<tr>
<td $HbgInfoCell>$tName$AfterName</td>
<td $HbgInfoCell>$tMonster->[1]</td>
<td $HbgInfoCell><IMG SRC=\"$image2\" width=32 height=32 BORDER=0></td>
<td $HbgInfoCell>$tMBmId</td>
<td $HbgInfoCell>$tMonster->[12]</td>
<td $HbgInfoCell>$tMonster->[13]</td>
<td $HbgInfoCell>$tseityou</td>
<td $HbgInfoCell>$tMonster->[5]/$tMonster->[6]</td>
<td $HbgInfoCell>$tMonster->[7]</td>
<td $HbgInfoCell>$tMonster->[8]</td>
<td $HbgInfoCell>$tMonster->[9]</td>
<td $HbgInfoCell>$tMonster->[10]</td>
<td $HbgInfoCell>$MBidName</td>
<td $HbgInfoCell>$tMBsId</td>

</tr></table></center>
END
	}
	if($mode != 2) {
		# 開発画面の時
		monstersetup($MBname, $HdefaultPassword, $island->{'monsurl'});
	}
}
#----------------------------------------------------------------------
# 怪獣設定変更フォーム

#----------------------------------------------------------------------
sub monstersetup {
	my($MBname, $HdefaultPassword, $HdefaultMonsUrl) = @_;
	out(<<END);
<form action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
<table border>
<tr>
<td $HbgTitleCell>改名する名前</td>
<td $HbgInfoCell><input type="text" size=32 maxlength=32 name="MONSNAME" value="$MBname"></td>
<td $HbgTitleCell>パスワード</td>
<td $HbgInfoCell><input type=password size=32 maxlength=32 name=PASSWORD value="${\htmlEscape($HdefaultPassword)}"></td>
<td $HbgTitleCell>　</td>
</tr>
<tr>
<td $HbgTitleCell>怪獣画像URL</td>
<td $HbgInfoCell colspan=3><input type=text size=80 maxlength=80 name="MONSURL" value="$HdefaultMonsUrl"></td>
<td $HbgTitleCell><input type="submit" value="実行" name="MonsButton$HcurrentID"></td>
</tr>
</table>
</form>
END
}

#----------------------------------------------------------------------
# 怪獣設定変更モード
#----------------------------------------------------------------------
# メイン

sub monsMain {
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

	# 怪獣設定を更新
	$island->{'monster'}->[1] = htmlEscape($Hmonsname);
	$island->{'monsurl'} = htmlEscape($Hmonsurl);

	# データの書き出し
	writeIslandsFile($HcurrentID);

	# 更新メッセージ
	tempmonsedit();

	# owner modeへ
	ownerMain();
}

#------------------------------------------------
# 簡易トーナメント
# 対戦の記録
sub FightViewMain {

	if(!open(IN, "$HdirName/fight.log")){
		return;
	}
	my @lines = <IN>;
	close(IN);
	unlock();

#	out ("${HtagTitle_}対戦の記録${H_tagTitle}<BR><DIV ALIGN=right>*敗者の島名をクリックすると敗戦時の状況が見れます</DIV>\n");
	out ("<DIV ID='fightlog'>${HtagTitle_}対戦の記録${H_tagTitle}</DIV><BR>\n");

	foreach $line(@lines) {
		chop($line);
		if($line =~ /<[0-9]*>/) {
			out("<hr><DIV ID='fightlogS'><H1>");
			$line =~ s/<|>//g;
			my $msg = ($line == 0) ? "予選落ち" : ($line == 99) ? "決勝戦" : $line."回戦";
			out(${HtagHeader_}.$msg.${H_tagHeader}."</H1></DIV>");
		} else {
			out($line);
		}
	}
}

sub fight_map {
    my($l, $lv);
    my($land, $landValue, $line);

	open(LIN, "${Hdirfdata}/island.${HcurrentID}");
	$islandName = <LIN>;
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		$line = <LIN>;
		for($x = 0; $x < $HislandSize; $x++) {
			$line =~ s/^(.)(..)//;
			$land->[$x][$y] = hex($1);
			$landValue->[$x][$y] = hex($2);
		}
	}
    close(LIN);
	unlock();
    out (<<END);
<SCRIPT Language="JavaScript">
<!--
function ps(x, y) {
    return true;
}

function ns(x) {
    return true;
}

function ShowMsg(n){
	window.status = n;
}
//-->
</SCRIPT>
<CENTER>
${HtagBig_}${HtagName_}「${islandName}島」${H_tagName}敗戦時の様子${H_tagBig}<BR>
<a href=${HthisFile}?FightLog=0>${HtagBig_}戻る${H_tagBig}</a><BR>
<BR>
<TABLE BORDER><TR><TD>
END
	# 座標(上)を出力
	out("<IMG SRC=\"xbar.gif\" width=400 height=16><BR>");

	# 各地形および改行を出力
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		# 偶数行目なら番号を出力
		if(($y % 2) == 0) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# 各地形を出力
		for($x = 0; $x < $HislandSize; $x++) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			landString($l, $lv, $x, $y, 1, $comStr[$x][$y]);
		}

		# 奇数行目なら番号を出力
		if(($y % 2) == 1) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# 改行を出力
		out("<BR>");
	}
	out("</TD></TR></TABLE></CENTER>\n");
}

1;
