#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �Ͽޥ⡼�ɥ⥸�塼��(ver1.00)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
#
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# ���ۤ�Ȣ��  (ver5.53b)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# ��ȯ�˻Ȥ����
#----------------------------------------------------------------------

$HcommandTotal = 107; # ���ޥ�ɤμ���

# ����
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
     $HcomOreBuy,$HcomOilBuy,$HcomWeponBuy, #����̿��
     $HcomMoney, $HcomFood, $HcomEmigration, $HcomPropaganda, $HcomGiveup,
     $HcomAutoPrepare, $HcomAutoPrepare2, $HcomAutoSellTree, $HcomAutoDelete);

if($Hbuycommand){
	# �񸻹�����̿�����
	splice(@HcomList,95,3);# ̿���������餺���Τ����
	$HcommandTotal -= 3;
}

$HcomMsg[$HcomPrepare]   = '���ϡ���ʪ�Ϥ�ʿ�Ϥˤ��ޤ���(����Ϥϳ�)';
$HcomMsg[$HcomPrepare2]  = '���������ʤ������ϡ�����������ۤ��Ͽ̤γ�Ψ���徺';
$HcomMsg[$HcomReclaim]   = '�������������ϡ�Φ�μ��ϤΤ߲�ǽ�Ǥ���������ܿ��줬����Ȥ������';
$HcomMsg[$HcomReclaim2]  = '���������ʤ������Ω�ơ�����������ۤ��Ͽ̤γ�Ψ���徺';
$HcomMsg[$HcomDestroy]   = '���ϡ�ʿ�ϡ�Į�Ϥǿ��̻��ꤹ��Ȳ�������';
$HcomMsg[$HcomDestroy2]  = '���������ʤ��η������������ۤ��Ͽ̤γ�Ψ���徺';
$HcomMsg[$HcomSearch]    = '���ϡ�ʿ�ϡ�Į�ϤǼ¹Բ�ǽ����̮�ʤɤ�ȯ���Ǥ��ޤ�';
$HcomMsg[$HcomSellTree]  = '���������̵������(ʿ�Ϥ��Ѳ�)���ܿ���(�������Ѳ�)�Ǽ¹Բ�ǽ';
$HcomMsg[$HcomPlant]     = 'ʿ�ϡ�Į�ϤǼ¹Բ�ǽ�������ˤ����ܿ���';
$HcomMsg[$HcomBank]      = '���Ҥ��西�������롣�¤���������ʤ�(�ޤ���ݻ�)';
$HcomMsg[$HcomPioneer]   = 'ʿ�Ϥ�¼���Ǥ���';
$HcomMsg[$HcomFarm]      = '���Ȥ��뿦�졣����5����(ʣ����)';
$HcomMsg[$HcomFactory]   = '����10��(ʣ����)';
$HcomMsg[$HcomMountain]  = '�ҳ��˶���������20��(ʣ����)';
$HcomMsg[$HcomPresent]   = '�ץ쥼��Ȥ��ʤ��ȷ����Բġ�0����.1����������.2�ɡ���.3������.4ͷ����.5�ع�.6����.7���Ի�.8ưʪ��.9������.10���õ�ǰ��.11�ҳ�����';
$HcomMsg[$HcomPresentAid]= '�ץ쥼��Ȥ��ʤ����Բġ�0����.1����������.2�ɡ���.3������.4ͷ����.5�ع�.6����.7���Ի�.8ưʪ��.9������.10���õ�ǰ��.11�ҳ�����';
$HcomMsg[$HcomBase]      = '�ߥ�������ĤΤ�ɬ�ס�EX20�ޤǤ��ɲ÷��ߤ�5�����ޤ�������ʹߤ�1';
$HcomMsg[$HcomDbase]     = '���ϣ��ޥ��Υߥ�������ɤ�(���Ȥ����)�����ˤ�Ĥ���ޤ�(���ϲкҤ�ǳ����)';
$HcomMsg[$HcomSbase]     = '���˥ߥ�������Ϥ���';
$HcomMsg[$HcomMonument]  = '�ߥ�������Ϥ˺��ȥ��å����';
$HcomMsg[$HcomSMonument] = '�����Ǥε�ǰ��Ǥ�������˷��ߤ��ޤ����ɲ÷��ߤ���Ȥ�äѤ����Ӥޤ�����';
$HcomMsg[$HcomHaribote]  = '�����ܤ��ɱһ��ߡ���и��̰ʳ���̵̣��';
$HcomMsg[$HcomScity]     = '���˺��кҤ�ǳ���롢���Ȥ��ܾ���';
$HcomMsg[$HcomSFarm]     = '���˺��кҤ�ǳ���롢����3��(ʣ����)';
$HcomMsg[$HcomTower]     = '�ҳ��˶���������20��(ʣ����)';
$HcomMsg[$HcomFire]      = '�ϰϣ��ǲкҤ��ɤ�(���Ȥ����)�����ˤ����(Φ��Φ�λ��ߡ����ϳ��λ��ߤˤ�������̵����';
$HcomMsg[$HcomWindmill]  = '���ϣ��إ���������(Φ)�������̤��ܡ��ݻ��񣱣���';
$HcomMsg[$HcomMyhome]    = '�ɲ÷��ߤ�Ԥ����ѵ��Ϥ������ޤ�����˰�Ĥ������ޤ���';
$HcomMsg[$HcomPort]      = '���ȷϤο��졣����ͣ������Ϥ��ɲ÷��ߤ��ȣ����������磲����(ʣ����)';
$HcomMsg[$HcomPolice]    = '���ĤǤ���ߤ�����Ⱥ�¿ȯ�����������ʤ��ʤ�ޤ����ݻ����西���󣵲��ǲкҤ�ǳ���ޤ���';
$HcomMsg[$HcomHospital]  = '���ĤǤ���ߤ���ȸ��̤�����ޤ����ݻ����西���󣵲��ǲкҤ�ǳ���ޤ���';
$HcomMsg[$HcomTrump]     = '��뤳�Ȥ�̵���ʤä����ѤΥ��٥���Ϸ��Ǥ����ܤ��������������Ǥ͡�';
$HcomMsg[$HcomFlower]    = '������Ǥ��֤������ޤ���������̤Ϥ���ޤ���';
$HcomMsg[$HcomBreakwater]= '�����������к�������������';
$HcomMsg[$HcomDokan]     = '�ϲ������������';
$HcomMsg[$HcomUg]        = '�ϲ����ߡ����ͻ���';
$HcomMsg[$HcomShipbuild] = '�����飲�ޥ�����������Ǽ¹ԤǤ��롣�ϰ���ε������ɲü¹ԤǤ��롣';
$HcomMsg[$HcomManipulate]= '���̤��������ꡢʣ��������ϹŲ����Ƥʤ����٤Ƥβ��ä��о�';
$HcomMsg[$HcomSTManipulate]= '������̾��ɽ������ʤ�';
$HcomMsg[$HcomSpy]       = '¾������Ͽ̡���������ۡ������ξƤ�Ƥ���ʤɤ�Ԥ�';
$HcomMsg[$HcomTeisatu]   = '¾����λ����ɸ�Ȥ��μ��ϣ��إ������Ϸ�Ĵ��';
$HcomMsg[$HcomWarp]      = '�����˾�ä���Ρ��������Τ�Ǥ�դ����ž�ܤ����롣1��ǲ���롣';
$HcomMsg[$HcomDeathtrap] = '�������Ƥ������ä˥��᡼����Ϳ���롢�ޤ����ݤ����ɲ÷��߲�ǽ�����ˤ���롣';
$HcomMsg[$Hcomcolony]    = '����ޤ��äƤʤ��ȤǤ��ʤ�����ɸ�����Ǥ��ޤ��󤬤���Ȣ��Ƕ�ʼ��Ǥ���';
$HcomMsg[$HcomBioMissile]= '������������꤬�������ޤ���';
$HcomMsg[$HcomMissileNM] = '����';
$HcomMsg[$HcomMissilePP] = '����';
$HcomMsg[$HcomMissileSPP]= '�������濴����';
$HcomMsg[$HcomMissileST] = '���������ߤ˷�ĤΤϤ��ޤ��礦';
$HcomMsg[$HcomMissileLD] = '������Φ�˲�(�������Ϣ���������)';
$HcomMsg[$HcomMissileRNG] = '���Ф˸�������';
$HcomMsg[$HcomSendMonster]='���̤򣱥ᥫ���顢������ƥͥ����Τ顢������ᥫ���Τ�';
$HcomMsg[$HcomSSendMonster]='���̻����Ǥ�դβ��ä��ɸ����ޤ���';
$HcomMsg[$HcomMissileRM] = '�������������Ϥˡ�Φ�ϸ³��ͤλ��ϸ���̵��';
$HcomMsg[$HcomMissileSRM]= '���Ͻ���ޤ���';
$HcomMsg[$HcomMissileGM] = '���ʤ�����ȯ������Ƥޤ���';
$HcomMsg[$HcomMissileMGM]= '���ä˼�ư�Ǹ����äƤ�����ʣ����������';
$HcomMsg[$HcomMissileDM] = '����';
$HcomMsg[$HcomMissileNCM]= '1ȯ��10ȯʬ���񡢥ߥ������30̤������ؤ��Բġ������ε��������Ȥ��ץ饹����';
$HcomMsg[$HcomMissilePLD]= '������Φ���˲��ƤǤ�';
$HcomMsg[$HcomDummy]     = 'ST�Ϥ�ʻ�Ѥ��ޤ��礦';
$HcomMsg[$HcomShip]      = '0�ü�(���������ϤΤ�)��1��ư��2�ɸ�(��������)��3ű�ࡢ4����';
$HcomMsg[$HcomShipM]     = '���̤��������ꡢ�ɸ桢ű���������������åȤμ����°�������Ƥ��оݤǤ���';
$HcomMsg[$HcomShipSell]  = '���������ʤ�������°���������ޤ������ȳ��ˤʤ�ޤ������ʤ������񻲾ȡ�';
$HcomMsg[$HcomDoNothing] = '10������ޤ�';
$HcomMsg[$HcomSell]      = '���������ʤ�';
$HcomMsg[$HcomOreSell]   = '���������ʤ�';
$HcomMsg[$HcomOilSell]   = '���������ʤ�';
$HcomMsg[$HcomWeponSell] = '���������ʤ�';
$HcomMsg[$HcomOreBuy]    = '���������ͭ��';
$HcomMsg[$HcomOilBuy]    = '���������ͭ��';
$HcomMsg[$HcomWeponBuy]  = '���������ͭ��';
$HcomMsg[$HcomMoney]     = '���������ʤ�';
$HcomMsg[$HcomFood]      = '���������ʤ�';
$HcomMsg[$HcomEmigration]= '1��ޤǥ��������ʤ���Į����ꤹ��';
$HcomMsg[$HcomPropaganda]= '�͸��������ޤ�(ʣ����)';
$HcomMsg[$HcomMonsEgg]   = '���å��ޥ�ɡ����åХȥ뤹��ˤϤ�����㤤�ޤ��礦��';
$HcomMsg[$HcomMonsEsa]   = '���å��ޥ�ɡ��ݤ������äλĳ��򿩤٤����ƿʲ������ޤ��礦��';
$HcomMsg[$HcomMonsEnsei] = '���å��ޥ�ɡ��ɤ�ɤ���碌�ƶ��������ޤ��礦��';
$HcomMsg[$HcomMonsTettai]= '���å��ޥ�ɡ����������ʤ���ƨ���Ƥ��餱�Ǥ���������Ƥ���Ȥ������˵��äƤ�餤�ޤ���';
$HcomMsg[$HcomMonsEsaAid]= '���å��ޥ�ɡ����������ʤ�����ʬ�Υ��ȥå��¤���Ϥ��ޤ������������α¤�̵�����Τ�';
$HcomMsg[$HcomMonsAid]   = '���å��ޥ�ɡ����������ʤ�����ʬ�β��ä���Ϥ��ޤ������������˲��ä����ʤ��Ȥ��Τ�';
$HcomMsg[$HcomMonsSell]  = '���å��ޥ�ɡ����������ʤ����ʾ����ܣ��ˡߡ����������������ޤ������ȣ��٤����褷�ޤ���';
$HcomMsg[$HcomMonsExer]  = '���å��ޥ�ɡ��¤���Ѥ����ä������ޤ����¤���ˤ������Ȥ��˻Ȥ����¤ˤ�뷱���κ���̵����';

$HcomMsg[$HcomSUnit]      = '���襳�ޥ�ɡ��ɲ÷��߲ġ�����̵�����֤����¤ʪ��Į�Ϥ������������ޤ�������Ԥ�ɬ�פ�����ޤ���';
$HcomMsg[$HcomSMissileGM] = '���襳�ޥ�ɡ���̵���Υߥ���������ޤ�������ߥ�������Ϥ�ɬ�פǤ���';
$HcomMsg[$HcomSMissilePP] = '���襳�ޥ�ɡ������Υߥ���������ޤ�������ߥ�������Ϥ�ɬ�פǤ���';
$HcomMsg[$HcomSMissile]   = '���襳�ޥ�ɡ������Υߥ���������ޤ�������ߥ�������Ϥ�ɬ�פǤ���';
$HcomMsg[$HcomSMissileMGM]= '���襳�ޥ�ɡ���ȯ�Τߤǲ��ä˼�ư�Ǹ����äƤ�����ʣ���������ࡣ';
$HcomMsg[$HcomSOccupy]  = '���襳�ޥ�ɡ����Τ�Ԥ������°�ˤ��ޤ�����������������ǧ��';
$HcomMsg[$HcomSFood]    = '���襳�ޥ�ɡ������˥åȤ�¼��������ޤ���';
$HcomMsg[$HcomSPioneer] = '���襳�ޥ�ɡ������˥åȤ�¼��������ޤ���';
$HcomMsg[$HcomSBuild]   = '���襳�ޥ�ɡ�(���Ѥ��ʤ�����)';
$HcomMsg[$HcomSpaceFarm]= '���襳�ޥ�ɡ��ɲ÷��߲ġ��������ߡ�';
$HcomMsg[$HcomSFactory] = '���襳�ޥ�ɡ��ɲ÷��߲ġ��������ߡ�';
$HcomMsg[$HcomSpaceBase]= '���襳�ޥ�ɡ��ɲ÷��߲ġ�����ߴ��Ϥ���ߡ��ɲ÷��ߤǷи��ͲԤ�';
$HcomMsg[$HcomSDbase]   = '���襳�ޥ�ɡ����ϣ��ޥ��Υߥ�������ɤ�(���Ȥ����)';
$HcomMsg[$HcomSEisei]   = '���襳�ޥ�ɡ��ɲ÷��߲ġ��͡��ʸ��̤�����ޤ���';
$HcomMsg[$HcomSDestroy] = '���襳�ޥ�ɡ����硢̵��°�Ϸ��Σ��ޥ����̵���᤹������ξ��ϥ��������ʤ�';

$HcomMsg[$HcomOMissileNM]    = '';
$HcomMsg[$HcomOMissilePP]    = '';
$HcomMsg[$HcomOMissileSPP]   = '';

$HcomMsg[$HcomGiveup]        = '�礬�ʤ��ʤ�ޤ�';
$HcomMsg[$HcomAutoPrepare]   = '��������Ϥˤ��٤����Ϥ򥻥å�';
$HcomMsg[$HcomAutoPrepare2]  = '��������Ϥˤ��٤��Ϥʤ餷�򥻥å�';
$HcomMsg[$HcomAutoSellTree]  = '���̤ο�(ñ��ɴ)��꾯�ʤ������о�';
$HcomMsg[$HcomAutoDelete]    = '�ײ����������ʤ�����������';

#----------------------------------------------------------------------
# �Ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��

sub printIslandMain {
	# ����

	unlock();

	# id�������ֹ�����
	$HcurrentNumber = $HidToNumber{$HcurrentID}; # ���

	# �ʤ��������礬�ʤ����

	if($HcurrentNumber eq '') {
		tempProblem();
		return;
	}

	# ̾���μ���
	$HcurrentName = $Hislands[$HcurrentNumber]->{'name'};

	$HcurrentNumber2 = $HidToNumber{$HprintID}; # �Ѹ����ˤ����ܿ�
	$HprintAlly = 0;
	if($HcurrentNumber2 eq '') {
		$HprintID = 0;
	}else{
		my($chkpass) = $Hislands[$HcurrentNumber2]->{'password'};
		if(!checkPassword($chkpass,$HinputPassword)) {
			# password���㤦
			$HprintID = 0;
		}else{
			$HprintAlly = $Hislands[$HcurrentNumber2]->{'ally'};
		}
	}

	# �Ѹ�����
	if($Hislands[$HcurrentNumber]->{'id'} > 90){
		# Battle Field�ΤȤ�
		$HmainMode = 'bfield';
		tempPrintIslandHead("(Battle Field)"); # �褦����!!
		tempNavi();
	}else{
		tempPrintIslandHead(); # �褦����!!
		tempNavi();
	}
	
	islandInfo(); # ��ξ���

	islandMap(0, $HprintID); # ����Ͽޡ��Ѹ��⡼��
	ugMap($island,0);	# �ϲ�
	islandJamp();   # ��ΰ�ư
	islandmonster(2);# ��β���

	tempLocalbbs(0);	# ������Ǽ���
	tempRecent(0);		# �ᶷ
	tempMapTotal();		# �ޥå׽���
}

#----------------------------------------------------------------------
# ��ȯ�⡼��
#----------------------------------------------------------------------
# �ᥤ��

sub ownerMain {
	# ����

	unlock();

	# �⡼�ɤ�����
	$HmainMode = 'owner';

	# id����������
	if($HcurrentID < 1){
		tempWrongPassword();
		Dummyfunction() if($HjavaMode eq 'java');
		return;
	}
	
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	# �ѥ����
	if(!checkPassword($island->{'password'},$HinputPassword)) {
		# password�ְ㤤
		tempWrongPassword();
		Dummyfunction() if($HjavaMode eq 'java');
		return;
	}

	if($Htournament){
		# �ʰץȡ��ʥ���
		my $tName = $HidToName{$island->{'fight_id'}};
		if($tName eq ''){
			# ̵��
		}else{
			# ͭ��
			$HtargetList = "<OPTION VALUE=\"$island->{'fight_id'}\">${tName}${AfterName}\n";
			$HtargetList .= "<OPTION VALUE=\"$island->{'id'}\">${HcurrentName}${AfterName}\n";
		}
	}

	# ��ȯ����
	if($HjavaMode eq 'java') {
		tempOwnerJava(); # ��Java������ץȳ�ȯ�ײ��
	}else{
		tempOwner();     # ���̾�⡼�ɳ�ȯ�ײ��
	}

	if($island->{'order'} & 256){
		tempCLbbs();
	}else{
		ugMap($island,2);	# �ϲ�
		if($island->{'order'} & 64){
			tempLocalbbs(1);	# ������Ǽ���
			tempRecent(1);		# �ᶷ
		}else{
			tempRecent(1);		# �ᶷ
			tempLocalbbs(1);	# ������Ǽ���
		}
		tempCommentInput();	# ���������ϥե�����

		tempMapTotal();		# �ޥå׽���
	}
}
#----------------------------------------------------------------------
# ����ޥå�ɽ��
#----------------------------------------------------------------------
sub spaceMap {
	unlock();# ����


	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}��<ruby><rb>����<rp>��<rt>����<rp>��</ruby>�ޥåס�${H_tagName}${H_tagBig}(���綦ͭ)<BR>
$HtempBack<BR>
</CENTER>
END
	$HcurrentID = 999;
	$HcurrentName = $SpaceName;
	tempNavi(3);
	spaceInfo();  # ��ξ���

	$sAfterName = $AfterName;
	$AfterName = "";
	islandMap(3); # ����Ͽޡ�����⡼��
	spaceInfo2(); # ��ξ���


	tempLocalbbs(3);	# ������Ǽ���
	tempRecent(0);		# �ᶷ
	tempMapTotal();		# �ޥå׽���
}
#----------------------------------------------------------------------
# ����ޥå�ɽ��
#----------------------------------------------------------------------
sub oceanMap {
	unlock();# ����


	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}�ֳ���ޥåס�${H_tagName}${H_tagBig}(���綦ͭ)<BR>
$HtempBack<BR>
</CENTER>
END
	$HcurrentID = 888;
	$HcurrentName = $OceanName;
	tempNavi(4);
#	spaceInfo();  # ��ξ���

	$sAfterName = $AfterName;
	$AfterName = "";
	$HislandSize = $HoceanSize;
	islandMap(4); # ����Ͽ�
	
	tempLocalbbs(4);	# ������Ǽ���
	tempRecent(0);		# �ᶷ
	tempMapTotal();		# �ޥå׽���
}

#----------------------------------------------------------------------
# ���ޥ�ɥ⡼��
#----------------------------------------------------------------------
# �ᥤ��

sub commandMain {
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

	# �⡼�ɤ�ʬ��

	my($command) = $island->{'command'};
	
	my($tempCommandFlag);

	if($HcommandMode eq 'delete') {
		slideFront($command, $HcommandPlanNumber);
		$tempCommandFlag = 0;
	} elsif(($HcommandKind == $HcomAutoPrepare) ||
		($HcommandKind == $HcomAutoPrepare2) ||
		($HcommandKind == $HcomAutoSellTree)) {

		# �ե����ϡ��ե��Ϥʤ餷���ե�Ȳ��
		# ��ɸ�������

		makeRandomPointArray();
		my($land) = $island->{'land'};
		my($landValue) = $island->{'landValue'};

		my($Arg) = $HcommandArg;
		$Arg = 1 if($Arg == 0);

		# ���ޥ�ɤμ������

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
					# �º̤��Τ�

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
		# ���ä�
		my($i);
		for($i = 0; $i < $HcommandMax; $i++) {
			slideFront($command, $HcommandPlanNumber);
		}
		$tempCommandFlag = 0;
	} else {
		slideBack($command, $HcommandPlanNumber, 0) if($HcommandMode eq 'insert');
		$tempCommandFlag = 1;
		# ���ޥ�ɤ���Ͽ
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

	$island->{'cmdTurn'} = $HislandTurn;		# ������
	$island->{'cmdIp'}   = $ENV{'REMOTE_ADDR'};	# IP
	$island->{'cmdId'}   = $defaultID;			# ���å���ID
	$island->{'cmdtime'} = time;	# ���ϻ���

	# �ǡ����ν񤭽Ф�
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

	# owner mode��
	ownerMain();

}

#----------------------------------------------------------------------
# ���������ϥ⡼��
#----------------------------------------------------------------------
# �ᥤ��

sub commentMain {
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

	# ��å������򹹿�
	$island->{'comment'} = htmlEscape($Hmessage);
	$island->{'commentLabel0'} = "$HcommentLabel0";
	$island->{'commentLabel1'} = "$HcommentLabel1";
	$island->{'commentLabel2'} = "$HcommentLabel2";
	$island->{'commentLabel3'} = "$HcommentLabel3";
	$island->{'commentLabel4'} = "$HcommentLabel4";

	# �ǡ����ν񤭽Ф�
	if(!writeIslandsFile($HcurrentID, 1)) {
		unlock();
		tempFailWrite();
		return;
	}

	# �����ȹ�����å�����
	tempComment();

	# owner mode��
	ownerMain();
}

#----------------------------------------------------------------------
# ������Ǽ��ĥ⡼��
#----------------------------------------------------------------------
# �ᥤ��


sub localBbsMain {
	# id�������ֹ�����
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
		# �ʤ��������礬�ʤ����

		if($HcurrentNumber eq '') {
			unlock();
			tempProblem();
			return;
		}
		$wmode = 2;
	}

	# ����⡼�ɤ���ʤ���̾������å��������ʤ����

	if(($HlbbsMode == 0) && ($HlbbsMode == 1) && ($HlbbsMode == 3)){
		if(($HlbbsName eq '') || ($HlbbsMessage eq '')) {
			unlock();
			tempLbbsNoMessage();
			return;
		}
	}

	# �Ѹ��ԥ⡼�ɤ���ʤ����ϥѥ���ɥ����å�
	if($HlbbsMode != 0) {
		if (($HlbbsMode == 3) || ($HlbbsMode == 4)) {
			# ����ԥ⡼��
			my($foreignNumber) = $HidToNumber{$HforeignerID};
			if ($foreignNumber eq '') {
				unlock();
				tempProblem();
				return;
			}
			my($foreignIsland) = $Hislands[$foreignNumber];
			if($HlbbsType eq 'ANON'){
				$foreignName = 'ƿ̾';
			} else {
				my $passCheck = checkPasslocalbbs($foreignIsland->{'password'},$HinputPassword);
				if($passCheck == 0) {
					unlock();
					tempWrongPassword();
					return;
				} elsif($passCheck == 3) {
					$foreignName = '������';
				} elsif($passCheck == 2) {
					$foreignName = 'GUEST';
				}
			}
			
			# ȯ���Ԥ򵭲�����

			if ($HlbbsType ne 'ANON') {
				# �����ȶ���

				if($foreignName eq '') {
					$speaker = $foreignIsland->{'name'} . "$AfterName$addr," .$HforeignerID;
				}else{
					$speaker = $foreignName . "$addr";
				}
			} else {
				# ƿ̾
				$speaker = $ENV{'REMOTE_HOST'};
				$speaker = $ENV{'REMOTE_ADDR'} if ($speaker eq '');
			}
			if ($HlbbsType ne 'SECRET') {
				# ������ƿ̾
				$speaker = "0<$speaker";
			} else {
				# ����

				$speaker = "1<$speaker";
			}
		} else {
			# ���⡼��
			if(!checkPassword($island->{'password'},$HinputPassword)) {
				# password�ְ㤤
				unlock();
				tempWrongPassword();
				return;
			}
			$speaker = "0<$addr";
		}
	}

	my($lbbs) = $island->{'lbbs'};

	# �⡼�ɤ�ʬ��

	if($HlbbsMode == 2) {
		# ����⡼��
		# ��å����������ˤ��餹
		slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
	} elsif($HlbbsMode == 4) {
		# ����Ժ���⡼��
		$line = $lbbs->[$HcommandPlanNumber];
		if($line =~ /([0-9]*)\<(.*)\<([0-9]*)\>(.*)\>(.*)$/) {
			my($sName, $sID) = split(/,/, $2);
			if((($sID != 0) && ($sID == $HforeignerID)) || ($foreignName eq '������')){
				# ��å����������ˤ��餹
				slideBackLbbsMessage($lbbs, $HcommandPlanNumber);
			}else{
				unlock();
				tempWrongPassword();
				return;
			}
		}
	} else {
		# ��Ģ�⡼��
		# ��å���������ˤ��餹
		slideLbbsMessage($lbbs);

		# ��å������񤭹���
		my $message = ($HlbbsMode == 1) ? '1' : '0';

		$HlbbsName = "$HislandTurn��" . htmlEscape($HlbbsName);
		$HlbbsMessage = htmlEscape($HlbbsMessage);
		$lbbs->[0] = "$speaker<$message>$HlbbsName>$HlbbsMessage";
	}

	# �ǡ����񤭽Ф�
	if(!writeIslandsFile($HcurrentID, $wmode)) {
		unlock();
		tempFailWrite();
		return;
	}

	if($HlbbsMode2 eq 'lbbslist'){
		# lbbslist.cgi����ν񤭹��ߡ�
		$HlbbsMode2 = 0;
		tempLbbsAdd();
		out("<meta HTTP-EQUIV=\"refresh\" CONTENT=\"0; URL=$HbaseDir/lbbslist.cgi?pass=$HdefaultPassword&id=$HforeignerID\#$HcurrentID\">");
		return if(($wmode == 3) || ($wmode == 4));
	}elsif($wmode == 3){
		# ����ޥå�
		if(($HlbbsMode == 2) || ($HlbbsMode == 4)) {
			tempLbbsDelete();
		}else{
			tempLbbsAdd();
		}
		out("${HtagBig_}<A href=\"$HthisFile?space=0\">��ư�Ǳ���ޥåפ����Ӥޤ��������������Ԥ�����������</A>${H_tagBig}");
		out("<meta HTTP-EQUIV=\"refresh\" CONTENT=\"0; URL=$HthisFile?space=0\">");
		return;
	}elsif($wmode == 4){
		# ����ޥå�
		if(($HlbbsMode == 2) || ($HlbbsMode == 4)) {
			tempLbbsDelete();
		}else{
			tempLbbsAdd();
		}
		out("${HtagBig_}<A href=\"$HthisFile?Ocean=0\">��ư�ǳ���ޥåפ����Ӥޤ��������������Ԥ�����������</A>${H_tagBig}");
		out("<meta HTTP-EQUIV=\"refresh\" CONTENT=\"0; URL=$HthisFile?Ocean=0\">");
		return;
	}elsif(($HlbbsMode == 2) || ($HlbbsMode == 4)) {
		tempLbbsDelete();
	} else {
		tempLbbsAdd();
	}

	# ��ȤΥ⡼�ɤ�
	if(($HlbbsMode == 1) || ($HlbbsMode == 2)) {
		ownerMain();
	} else {
		printIslandMain();
	}
}

# ������Ǽ��ĤΥ�å��������ĸ��ˤ��餹
sub slideLbbsMessage {
	my($lbbs) = @_;
	pop(@$lbbs);
	unshift(@$lbbs, $lbbs->[0]);
}

# ������Ǽ��ĤΥ�å������������ˤ��餹
sub slideBackLbbsMessage {
	my($lbbs, $number) = @_;
	splice(@$lbbs, $number, 1);
	$lbbs->[$HlbbsMax - 1] = '0<<0>>';
}

#----------------------------------------------------------------------
# ����Ͽ�
#----------------------------------------------------------------------

# �����ɽ��
sub islandInfo {
	$island = $Hislands[$HcurrentNumber];
	
	# ����ɽ��
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
	
	$farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
	$port = ($port == 0) ? "��ͭ����" : "${port}0$HunitPop";
	$factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
	$mountain = ($mountain == 0) ? "��ͭ����" : "${mountain}0$HunitPop";
	$tower = ($tower == 0) ? "��ͭ����" : "${tower}0$HunitPop";
	$ore = ($ore == 0) ? "��ͭ����" : "${ore}$HunitOre";
	$oil = ($oil == 0) ? "��ͭ����" : "${oil}$HunitOil";
	$weapon = ($weapon == 0) ? "��ͭ����" : "${weapon}$HunitWeapon";
	$soukei = ($soukei == 0) ? "��ͭ����" : "${soukei}$HunitPop";
	if($yousyoku == 0) {
		$yousyoku = "��ͭ����"
	} else {
		$seisan += $yousyoku;
		$yousyoku = "${yousyoku}00ɤ";
	}
	$seisan = ($seisan == 0) ? "̵��" : "${seisan}$HunitFood";
	my($mStr0) = '';
	my($mStr1) = '';
	my($mStr3) = '';
	if(($HhideMoneyMode == 1) || ($HmainMode eq 'owner')) {
		# ̵���ޤ���owner�⡼��
		$mStr0 = "<TD $HbgInfoCell>$MissileK</TD>";
		$mStr1 = "<TD $HbgInfoCell>$MissileA</TD>";
		$mStr3 = "<TD $HbgInfoCell>$island->{'money'}$HunitMoney</TD>";
	} elsif($HhideMoneyMode == 2) {
		my($mTmp) = aboutMoney($island->{'money'});
		my($mTmp2) = '��̩';
		$mStr0 = "<TD $HbgInfoCell>$mTmp2</TD>";
		$mStr1 = "<TD $HbgInfoCell>$mTmp2</TD>";
		# 1000��ñ�̥⡼��
		$mStr3 = "<TD $HbgInfoCell>$mTmp</TD>";
	} else {
		my($mTmp2) = '��̩';
		$mStr0 = "<TD $HbgInfoCell>$mTmp2</TD>";
		$mStr1 = "<TD $HbgInfoCell>$mTmp2</TD>";
		$mStr3 = "<TD $HbgInfoCell>$mTmp2</TD>";
	}
	my($popspace) = $island->{'popspace'};
	$popspace = ($popspace > 0) ? "${popspace}${HunitPop}" : "��";
	
	if($HmainMode eq 'bfield'){
	out(<<END);
<DIV ID='islandInfo'><TABLE BORDER><TR>
<TD $HbgTitleCell>${HtagTH_}ID${H_tagTH}</TD>
<TD $HbgInfoCell>$island->{'id'}</TD>
<TD $HbgTitleCell>${HtagTH_}ŷ��${H_tagTH}</TD>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>$wname</TD>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>$wname2</TD>
<TD $HbgSubTCell>������</TD>
<TD $HbgInfoCell>$wname3</TD>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>$whp</TD>
</TR></TABLE>
��ա�Battle Field�ؤΥΡ��ޥ롢PP�ߥ����롢��ǰ�������̱�������ɸ��ʳ���̿���̵�뤵��ޤ���<BR>
</DIV>
END
		return;
	}
	out(<<END);
<DIV ID='islandInfo'><TABLE BORDER>
<TR>
<TH $HbgTitleCell colspan=2>${HtagTH_}����${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}ŷ��${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}��${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}�켡����${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}�󼡻���${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}��������${H_tagTH}</TH>
<TH $HbgTitleCell colspan=2>${HtagTH_}������${H_tagTH}</TH>
</TR>
<TR>
<TD $HbgSubTCell>�硡��</TD>
<TD $HbgInfoCell>${HtagNumber_}$rank${H_tagNumber}($zyuni)</TD>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>$wname</TD>
<TD $HbgSubTCell>���</TD>
$mStr3
<TD $HbgSubTCell>���ȵ���</TD>
<TD $HbgInfoCell>${farm}</TD>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>${factory}</TD>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>${tower}</TD>
<TD $HbgSubTCell>�ߥ�����ȯ�Ͳ�ǽ��</TD>
$mStr0
</TR>
<TR>
<TD $HbgSubTCell>��͸�</TD>
<TD $HbgInfoCell>$island->{'pop'}$HunitPop</TD>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>$wname2</TD>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>$island->{'food'}$HunitFood</TD>
<TD $HbgSubTCell>�ܿ��쵬��</TD>
<TD $HbgInfoCell>${yousyoku}</TD>
<TD $HbgSubTCell>��</TD>
<TD $HbgInfoCell>${port}</TD>
<TD $HbgSubTCell>��</TD>
<TD $HbgInfoCell>��</TD>
<TD $HbgSubTCell>ʼ����</TD>
<TD $HbgInfoCell>$weapon</TD>
</TR>
<TR>
<TD $HbgSubTCell>����̱</TD>
<TD $HbgInfoCell>$popspace</TD>
<TD $HbgSubTCell>������</TD>
<TD $HbgInfoCell>$wname3</TD>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>$ore</TD>
<TD $HbgSubTCell>��</TD>
<TD $HbgInfoCell>��</TD>
<TD $HbgSubTCell>�η���</TD>
<TD $HbgInfoCell>${mountain}</TD>
<TD $HbgSubTCell>��</TD>
<TD $HbgInfoCell>��</TD>
<TD $HbgSubTCell>ȯ�ͥߥ������</TD>
$mStr1
</TR>
<TR>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>$island->{'area'}$HunitArea</TD>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>$whp</TD>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>$oil</TD>
<TD $HbgSubTCell>������������</TD>
<TD $HbgInfoCell>$seisan</TD>
<TD $HbgSubTCell>��</TD>
<TD $HbgInfoCell>��</TD>
<TD $HbgSubTCell>����</TD>
<TD $HbgInfoCell>$soukei</TD>
<TD $HbgSubTCell>������и���</TD>
<TD $HbgInfoCell>$allex</TD>
</TR></TABLE></DIV>
END
}
# ��������ɽ��
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
	$farm = ($farm == 0) ? "��ͭ����" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "��ͭ����" : "${factory}0$HunitPop";
	my($solarwind);
	if($Hspace->{'solarwind'} <= $HislandTurn){
		$solarwind = "<b>ȯ����</b>";
	}else{
		$solarwind = $Hspace->{'solarwind'} . "�����󤫤�";
	}
	out(<<END);
<DIV ID='islandInfo'><TABLE BORDER><TR>
<TD>${HtagTH_}������${H_tagTH}</TD>
<TD>${HtagTH_}��ȯ����${H_tagTH}</TD>
<TD>${HtagTH_}����͸�${H_tagTH}</TD>
<TD>${HtagTH_}���쵬��${H_tagTH}</TD>
<TD>${HtagTH_}���쵬��${H_tagTH}</TD>
<TD>${HtagTH_}������ͽ��${H_tagTH}</TD>
</TR>
<TR>
<TD>${HislandTurn}������</TD>
<TD>$Hspace->{'area'}Hex</TD>
<TD>$Hspace->{'pop'}$HunitPop</TD>
<TD>${farm}</TD>
<TD>${factory}</TD>
<TD>${solarwind}</TD>
</TR>
</TABLE></DIV>
END
}
# ������󣲤�ɽ��
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
<TD>${HtagTH_}����񻺡�����${H_tagTH}</TD>
<TD>${HtagTH_}����${H_tagTH}</TD>
<TD>${HtagTH_}����${H_tagTH}</TD>
<TD>${HtagTH_}����${H_tagTH}</TD>
<TD>${HtagTH_}����${H_tagTH}</TD>
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

# �Ͽޤ�ɽ��
# ������1�ʤ顢�ߥ�����������򤽤Τޤ�ɽ��
sub islandMap {
	my($mode, $pId) = @_;
	my($island);
	if($mode == 3){
		# ����ޥå�
		$island = $Hspace;
	}elsif($mode == 4){
		# ����ޥå�
		$island = $Hocean;
	}else{
		$island = $Hislands[$HcurrentNumber];
	}
	
	# �Ϸ����Ϸ��ͤ����
	my($land) = $island->{'land'};
	my($landValue) = $island->{'landValue'};
	my($nation) = $island->{'nation'};
	my($dis) = $island->{'landValue2'};
	my($l, $lv);
	$pId = $island->{'id'} if($mode == 1);

	# ���ޥ�ɼ���
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
	
	# ��ɸ(��)�����
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
	# ̸��ȯ����������á��ϥ�ܥ�õ����̸�ξ�����¸�������
	SearchKiriMons($land, $landValue);
	# ���Ϸ�����Ӳ��Ԥ����
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		out("<table border=0 cellspacing=0 cellpadding=0><tr>");

		# �������ܤʤ��ֹ�����
		if(($y % 2) == 0){
			if($mode == 3){
				out("<td class=s><img src=\"sspace${y}.gif\" width=16 height=32></td>");
			}elsif($mode == 4){
				out("<td class=b><img src=\"space${y}.gif\" width=16 height=32></td>");
			}else{
				out("<td class=b><img src=\"space${y}.gif\" width=16 height=32></td>");
			}
		}

		# ���Ϸ������
		for($x = 0; $x < $HislandSize; $x++) {
			if(($Kiri->[$x][$y] == 1) || (($Kiri->[$x][$y] == 2) && ($mode != 1))) {
				landString2($land->[$x][$y], $landValue->[$x][$y], $x, $y, $mode, $comStr[$x][$y], $nation->[$x][$y],0);
			} else {
				landString($land->[$x][$y], $landValue->[$x][$y], $x, $y, $mode, $comStr[$x][$y], $nation->[$x][$y], $dis->[$x][$y], $pId,0);
			}
		}
		
		# ������ܤʤ��ֹ�����
		if(($y % 2) == 1){
			if($mode == 3){
				out("<td class=s><img src=\"sspace${y}.gif\" width=16 height=32></td>");
			}elsif($mode == 4){
				out("<td class=b><img src=\"space${y}.gif\" width=16 height=32></td>");
			}else{
				out("<td class=b><img src=\"space${y}.gif\" width=16 height=32></td>");
			}
		}

		# ���Ԥ����
		out("</tr></table>");
	}
	out("<div id='NaviView'></div>");
	out("</table></div>\n");

	# �ƥ��ȥ⡼�ɻ���
	if($Htestflg){
		HdebugOut("�ƥ��ȥ⡼�ɻ���${mId}");
	}
}

sub landString {
	my($l, $lv, $x, $y, $mode, $comStr, $nation, $dis, $pId, $js) = @_;
	my($point) = "($x,$y)";
	my($image, $alt, $sflg, $myship, $tIsland, $tName);
	my($naviTitle);
	my($naviText);
	my($naviExp) = "''";

#	# ���å������鼫ʬ��ID����
#	# ���ξ���Ǽ�ʬ�ν�°������ɽ�����Ƥ��ޤ������å������Ѥ��ƥ���������ʤ��褦��
	my($lcookie) = jcode::euc($ENV{'HTTP_COOKIE'});
#	if($lcookie =~ /OWNISLANDID=\(([^\)]*)\)/) {
#		$mId = $1;
#	}
	if($lcookie =~ /MYSHIP=\(([^\)]*)\)/) {
		$myship = $1;
	}

	# ��ʬ��ID
	$mId = $pId;

	my($tn) = $HidToNumber{$nation};
	if($tn eq ''){
		$tName = "��°����";
		$sflg = $nation;
	}else{
		$tIsland = $Hislands[$tn];
		$tName = $tIsland->{'name'};
		$sflg = $tIsland->{'id'};
	}

	if($l == $HlandSea) {
		if($mode == 3){
			$image = 'cosmo1.gif';
			$alt = '��̵';
			$naviTitle = '��̵';
		}elsif($mode == 4) {
			$image = 'land0.gif';
			if($nation > 0){
				$alt = "��(${tName}${sAfterName})";
			}else{
				$alt = "��";
			}
			$naviTitle = $alt;
		}elsif($lv >= 10) {
			# �ܿ���

			$image = 'land17.gif';
			$alt = "�ܿ���(${lv}00ɤ)";
			$naviTitle = '�ܿ���';
			$naviText = "${lv}00ɤ";
		} elsif($lv == 1) {
			# ����
			$image = 'land14.gif';
			$alt = '��(����)';
			$naviTitle = '����';
		} else {
			# ��
			$image = 'land0.gif';
			$alt = '��';
			$naviTitle = '��';
		}
	} elsif($l == $HlandWaste) {
		# ����
		if($lv >= 10) {
			# ����

			$image = 'land18.gif';
			$alt = "����(����${lv}��åȥ�)";
			$naviTitle = '����';
			$naviText = "����${lv}��åȥ�";
		} elsif($lv == 1) {
			$image = 'land13.gif'; # ������
			$alt = '����';
			$naviTitle = '����';
		} else {
			$image = 'land1.gif';
			$alt = '����';
			$naviTitle = '����';
		}
	} elsif($l == $HlandPlains) {
		# ʿ��
		$image = 'land2.gif';
		$alt = 'ʿ��';
		$naviTitle = 'ʿ��';
	} elsif($l == $HlandForest) {
		# ��
		if($mode == 0) {
			# �Ѹ��Ԥξ����ڤ��ܿ�����
			$image = 'land6.gif';
			$alt = '��';
			$naviTitle = '��';
		} else {
			$image = 'land6.gif';
			$alt = "��(${lv}$HunitTree)";
			$naviTitle = '��';
			$naviText = "${lv}$HunitTree";
		}
	} elsif($l == $HlandTown) {
		# Į
		my($p);
		if($lv < 30) {
			$p = 3;
			$naviTitle = '¼';
		} elsif($lv < 100) {
			$p = 4;
			$naviTitle = 'Į';
		} else {
			$p = 5;
			$naviTitle = '�Ի�';
		}
		$image = "land${p}.gif";
		$alt = "$naviTitle(${lv}$HunitPop)";
		$naviText = "${lv}$HunitPop";
	} elsif($l == $HlandSlum) {
		# ����೹
		$image = "land22.gif";
		$alt = "����೹(${lv}$HunitPop)";
		$naviTitle = '����೹';
		$naviText = "${lv}$HunitPop";
	} elsif($l == $HlandFarm) {
		# ����
		$image = 'land7.gif';
		$alt = "����(${lv}0${HunitPop}����)";
		$naviTitle = '����';
		$naviText = "${lv}0${HunitPop}����";
	} elsif($l == $HlandFactory) {
		# ����
		$image = 'land8.gif';
		$alt = "����(${lv}0${HunitPop}����)";
		$naviTitle = '����';
		$naviText = "${lv}0${HunitPop}����";
	} elsif($l == $HlandTower) {
		# ���ȥӥ�
		$image = 'land23.gif';
		$alt = "���ȥӥ�(${lv}0${HunitPop}����)";
		$naviTitle = '����';
		$naviText = "${lv}0${HunitPop}����";
	} elsif($l == $HlandPort) {
		$image = 'land55.gif';
		$alt = "��(${lv}0${HunitPop}����)";
		$naviTitle = '��';
		$naviText = "${lv}0${HunitPop}����";
	} elsif($l == $HlandPolice) {
		$image = 'land56.gif';
		$alt = '�ٻ���';
		$naviTitle = '�ٻ���';
	} elsif($l == $HlandHospital) {
		$image = 'land66.gif';
		$alt = '�±�';
		$naviTitle = '�±�';
	} elsif($l == $HlandBase) {
		if($mode == 0) {
			# �Ѹ��Ԥξ��Ͽ��Τդ�
			$image = 'land6.gif';
			$alt = '��';
			$naviTitle = '��';
		} else {
			# �ߥ��������
			my($level) = expToLevel($l, $lv);
			$image = 'land9.gif';
			$alt = "�ߥ�������� (��٥� ${level}/�и��� $lv)";
			$naviTitle = '�ߥ��������';
			$naviText = "��٥� ${level}/�и��� $lv";
		}
	} elsif($l == $HlandSbase) {
		# �������
		if($mode == 0) {
			# �Ѹ��Ԥξ��ϳ��Τդ�
			$image = 'land0.gif';
			$alt = '��';
			$naviTitle = '��';
		} else {
			my($level) = expToLevel($l, $lv);
			$image = 'land12.gif';
			$alt = "������� (��٥� ${level}/�и��� $lv)";
			$naviTitle = '�������';
			$naviText = "��٥� ${level}/�и��� $lv";
		}
	} elsif(($l == $HlandWarp) || ($l == $HlandWarpR)) {
		# ž������
		$image = 'land36.gif';
		if($l == $HlandWarpR) {
			# ��������
			if($mode == 0) {
				$alt = "ž������";
			}else{
				if($lv == 1) {
					$alt = "ž�������� (����)";
				} elsif($lv == 2) {
					$alt = "ž�������� (��)";
				} elsif($lv == 3) {
					$alt = "ž�������� (����)";
				} elsif($lv == 4) {
					$alt = "ž�������� (����)";
				} elsif($lv == 5) {
					$alt = "ž�������� (��)";
				} elsif($lv == 6) {
					$alt = "ž�������� (����)";
				} else {
					$alt = "ž��������";
				}
			}
			$naviTitle = $alt;
		} else {
			if($mode == 0) {
				$alt = "ž������";
			} else {
				$alt = "ž������ (${HidToName{$lv}}${AfterName})";
				$naviText = "${HidToName{$lv}}${AfterName}";
			}
			$naviTitle = "ž������";
		}
	} elsif($l == $HlandDefence) {
		# �ɱһ���
		$image = 'land10.gif';
		if($lv == 2) {
			$alt = 'S�ɱһ���';
		} elsif($lv == 3) {
			$alt = 'SS�ɱһ���';
		} elsif($lv == 10 || $lv == 11) {
			if($mode == 0) {
				$image = 'land6.gif';
				$alt = '��';
			} else {
				if($lv == 10){
					$alt = 'ST�ɱһ���';
				}else{
					$alt = 'SST�ɱһ���';
				}
			}
		} elsif($lv == 20) {
			$alt = '̸�դ��ɱһ���';
		} elsif($lv == 21) {
			$alt = 'S̸�դ��ɱһ���';
		} else {
			$alt = '�ɱһ���';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandHaribote) {
		# �ϥ�ܥơ��ϥ�ܥƤ��Τ�

		if($lv == 0) {
			$image = 'land10.gif';
			if($mode == 0) {
				# �Ѹ��Ԥξ����ɱһ��ߤΤդ�

				$alt = '�ɱһ���';
			} else {
				$alt = '�ϥ�ܥ�';
			}
			$naviTitle = $alt;
		} else {
			my($kind, $name, $hp) = monsterSpec($lv);
			my($special) = $HmonsterSpecial[$kind];
			$image = $HmonsterImage[$kind];
			# �Ų���?
			if((($special == 3) && (($HislandTurn % 2) == 1)) ||
				(($special == 4) && (($HislandTurn % 2) == 0))) {
				$image = $HmonsterImage2[$kind];
			}
			$alt = "����$name(����${hp})";
			$naviTitle = $name;
			$naviText = "����${hp}";
			$naviExp = "\'MONSTER$kind\'";
		}
	} elsif($l == $HlandOil) {
		# ��������
		if($lv == 5) {
			$image = 'land25.gif';
			$alt = '�����ɱһ���';
			$naviTitle = '�����ɱһ���';
		} elsif($lv == 6) {
			$image = 'land49.gif';
			$alt = '����ǥ��ȥ�å�';
			$naviTitle = '����ǥ��ȥ�å�';
		} elsif($lv == 7) {
			$image = 'land35.gif';
			$alt = '������ɽ�';
			$naviTitle = '������ɽ�';
		} elsif($lv >= 35) {
			$image = 'land19.gif';
			$alt = "�����Ի�(${lv}$HunitPop)";
			$naviTitle = '�����Ի�';
			$naviText = "${lv}${HunitPop}����";
		} elsif($lv >= 10) {
			$image = 'land20.gif';
			$alt = "��������(${lv}0${HunitPop}����)";
			$naviTitle = '��������';
			$naviText = "${lv}0${HunitPop}����";
		} else {
			$image = 'land16.gif';
			$alt = '��������';
			$naviTitle = '��������';
		}
	} elsif($l == $HlandDeathtrap) {
		$image = 'land48.gif';
		$alt = "�ǥ��ȥ�å�(LV${lv})";
		$naviTitle = '�ǥ��ȥ�å�';
		$naviText = "LV${lv}";
	} elsif($l == $HlandWindmill) {
		$image = 'land50.gif';
		$alt = '����';
		$naviTitle = '����';
	} elsif($l == $HlandMyhome) {
		if($lv > 10) {
			$image = 'land53.gif';
			$alt = '�ޥ��ۡ���(��š)';
		} elsif($lv > 5) {
			$image = 'land52.gif';
			$alt = '�ޥ��ۡ���(����)';
		} else {
			$image = 'land51.gif';
			$alt = '�ޥ��ۡ���(������)';
		}
		$naviTitle = $alt;
		readProfileMAP($HcurrentID);
		$image = $Hprofile{'MyHomeImage'} if(substr($Hprofile{'MyHomeImage'},0,7) eq 'http://');
	} elsif($l == $HlandOsen) {
		$image = 'land21.gif';
		$alt = "�����ھ�(LV${lv})";
		$naviTitle = '�����ھ�';
		$naviText = "LV${lv}";
	} elsif($l == $HlandStadium) {
		$image = 'land27.gif';
		$alt = '����������';
		$naviTitle = $alt;
	} elsif($l == $HlandAmusement) {
		$image = 'land28.gif';
		$alt = 'ͷ����';
		$naviTitle = $alt;
	} elsif($l == $HlandCasino) {
		$image = 'land29.gif';
		$alt = '������';
		$naviTitle = $alt;
	} elsif($l == $HlandPark) {
		$image = 'land30.gif';
		$alt = '����';
		$naviTitle = $alt;
	} elsif($l == $HlandSchool) {
		$image = 'land31.gif';
		$alt = '�ع�';
		$naviTitle = $alt;
	} elsif($l == $HlandDome) {
		$image = 'land32.gif';
		$alt = '�ɡ���';
		$naviTitle = $alt;
	} elsif($l == $HlandAirport) {
		$image = 'land33.gif';
		$alt = '����';
		$naviTitle = $alt;
	} elsif($l == $HlandZoo) {
		$image = 'land38.gif';
		$alt = 'ưʪ��';
		$naviTitle = $alt;
	} elsif($l == $HlandBigcity) {
		$image = 'land39.gif';
		$alt = '���Ի�';
		$naviTitle = $alt;
	} elsif($l == $HlandExpo) {
		$image = 'land40.gif';
		$alt = '������';
		$naviTitle = $alt;
	} elsif($l == $HlandMegacity) {
		if($lv == 1) {
			$image = 'land42.gif';
			$alt = '�����Իԡ�����';
		} elsif($lv == 2) {
			$image = 'land41.gif';
			$alt = '�����Իԡ���';
		} elsif($lv == 3) {
			$image = 'land43.gif';
			$alt = '�����Իԡ�����';
		} elsif($lv == 4) {
			$image = 'land42.gif';
			$alt = '�����Իԡ�����';
		} elsif($lv == 5) {
			$image = 'land41.gif';
			$alt = '�����Իԡ���';
		} elsif($lv == 6) {
			$image = 'land43.gif';
			$alt = '�����Իԡ�����';
		} else {
			$image = 'land41.gif';
			$alt = '�����Ի�';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandMegatower) {
		if($lv == 1) {
			$image = 'land46.gif';
			$alt = '����ӥ������';
		} elsif($lv == 2) {
			$image = 'land45.gif';
			$alt = '����ӥ����';
		} elsif($lv == 3) {
			$image = 'land46.gif';
			$alt = '����ӥ������';
		} elsif($lv == 4) {
			$image = 'land46.gif';
			$alt = '����ӥ������';
		} elsif($lv == 5) {
			$image = 'land44.gif';
			$alt = '����ӥ����';
		} elsif($lv == 6) {
			$image = 'land46.gif';
			$alt = '����ӥ������';
		} else {
			$image = 'land46.gif';
			$alt = '����ӥ�';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandMegaFact) {
		if($lv == 1) {
			$image = 'land47.gif';
			$alt = '���繩�������';
		} elsif($lv == 2) {
			$image = 'land47.gif';
			$alt = '���繩�����';
		} elsif($lv == 3) {
			$image = 'land47.gif';
			$alt = '���繩�������';
		} elsif($lv == 4) {
			$image = 'land47.gif';
			$alt = '���繩�������';
		} elsif($lv == 5) {
			$image = 'land47.gif';
			$alt = '���繩�����';
		} elsif($lv == 6) {
			$image = 'land47.gif';
			$alt = '���繩�������';
		} else {
			$image = 'land47.gif';
			$alt = '���繩��';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandMegaFarm) {
		if($lv == 1) {
			$image = 'land65.gif';
			$alt = '�������������';
		} elsif($lv == 2) {
			$image = 'land65.gif';
			$alt = '�����������';
		} elsif($lv == 3) {
			$image = 'land65.gif';
			$alt = '�������������';
		} elsif($lv == 4) {
			$image = 'land65.gif';
			$alt = '�������������';
		} elsif($lv == 5) {
			$image = 'land65.gif';
			$alt = '�����������';
		} elsif($lv == 6) {
			$image = 'land65.gif';
			$alt = '�������������';
		} else {
			$image = 'land65.gif';
			$alt = '��������';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandFuji) {
		$image = $HfujiImage[$lv];
		$alt = '�ٻλ�';
		$naviTitle = $alt;
	} elsif($l == $HlandTcity) {
		$image = 'land58.gif';
		$alt = "�����Ի�(300${HunitPop} ${lv}0${HunitPop}����)";
		$naviTitle = '�����Ի�';
		$naviText = "300${HunitPop} ${lv}0${HunitPop}����";
	} elsif($l == $HlandHugecity) {
		if($lv < 50) {
			$image = 'land60.gif';
			$alt = 'Ķ�����Ի�(�濴)';
		} elsif($lv < 60) {
			$image = 'land61.gif';
			$alt = 'Ķ�����Ի�(�Ի�)';
		} elsif($lv < 70) {
			$image = 'land62.gif';
			$alt = 'Ķ�����Ի�(����)';
		} elsif($lv < 80) {
			$image = 'land63.gif';
			$alt = 'Ķ�����Ի�(����)';
		} else {
			$image = 'land64.gif';
			$alt = 'Ķ�����Ի�(����)';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandBreakwater) {
		# ������
		if($lv == 1) {
			$image = 'land59.gif';
		}else{
			# ̤����
			$image = 'land59_2.gif';
		}
		$alt = '������';
		$naviTitle = '������';
	} elsif($l == $HlandFire) {
		if($lv >= 10) {
			$image = 'land37.gif';
			$alt = 'S���ɽ�';
		} else {
			$image = 'land34.gif';
			$alt = '���ɽ�';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandSeisei) {
		# ������
		if($lv == 10) {
			$image = 'land24.gif';
			$alt = 'Ƽ������';
		} elsif($lv == 30) {
			$image = 'land24.gif';
			$alt = '��������';
		} else {
			$image = 'land24.gif';
			$alt = '��ú������';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandMountain) {
		# ��
		my $str = '';
		$naviTitle = '��';
		if($lv > 0) {
			$image = 'land15.gif';
			$alt = "��(�η���${lv}0${HunitPop}����)";
			$naviText = "�η���${lv}0${HunitPop}����";
		} else {
			$image = 'land11.gif';
			$alt = '��';
		}
	} elsif($l == $HlandMonument) {
		# ��ǰ��
		$image = $HmonumentImage[$lv];
		$alt = $HmonumentName[$lv];
		$naviTitle = $alt;
	} elsif($l == $HlandSMonument) {
		# ���쵭ǰ��
		$image = $HsmonumentImage[$lv];
		$alt = $HsmonumentName[$lv];
		$naviTitle = $alt;
	} elsif($l == $HlandBank) {
		if($mode == 0) { # �Ѹ��Ԥξ��
			$image = 'land6.gif';
			$alt = '��';
			$naviTitle = '��';
		} else {
			$image = 'land26.gif';
			$alt = "���(����${lv}000$HunitMoney)";
			$naviTitle = '���';
			$naviText = "����${lv}000$HunitMoney";
		}
	} elsif($HseaChk[$l] == 2) {
		# ����
		$image = $HshipImage[$l - $HlandPirate];
		my($order, $hp, $sId) = shipSpec($lv);
		$naviTitle = $HshipName[$l - $HlandPirate];
		if($l == $HlandGhostShip) {
			$alt = '��';
			$naviTitle = '��';
		#	$alt = "$naviTitle(H${hp})"; # �ǥХå���
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
		# ����
		my($kind, $name, $hp) = monsterSpec($lv);
		my($special) = $HmonsterSpecial[$kind];
		$image = $HmonsterImage[$kind];

		# �Ų���?
		if((($special == 3) && (($HislandTurn % 2) == 1)) ||
		   (($special == 4) && (($HislandTurn % 2) == 0))) {
			# �Ų���

			$image = $HmonsterImage2[$kind];
		}
		if($kind == 26) {
			# �º̤��Τ�
			$alt = '����';
			$naviTitle = $alt;
		} else {
			$alt = "����$name(����${hp})";
			$naviTitle = $name;
			$naviText = "����${hp}";
			$naviExp = "\'MONSTER$kind\'";
		}
	} elsif($l == $HlandKInora) {
		# ���ۤ��Τ�
		my($limit, $hp, $ld, $d) = bigMonsterSpec($lv);
		$image = "kinora${ld}${d}.gif";
		if($d == 0){
			$alt = "���õ��ۤ��Τ�(����${hp})(��$limit)";
			$naviText = "����${hp} ��$limit";
		}else{
			$alt = "���õ��ۤ��Τ�";
		}
		$naviTitle = '���õ��ۤ��Τ�';
	} elsif($l == $HlandTrump) {
		# �ȥ���
		if(($lv < 1) || ($lv > 14)){
			$image = 'trump0.gif';
			$alt = '�ȥ���΢';
		}else{
			$image = "trump${lv}.gif";
			if($lv == 14){
				$alt = '�ȥ��ץ��硼����';
			}else{
				$alt = "�ȥ���${lv}";
			}
		}
		$naviTitle = $alt;
	} elsif($l == $HlandFlower) {
		# ����
		$lv = 1 if(($lv < 1) || ($lv > 13));
		$image = "flower${lv}.gif";
		if($lv == 13){
			$alt = '���ܥƥ�';
		}else{
			$alt = '��';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandDokan) {
		# �ϲ�
		if($mode == 0) { # �Ѹ��Ԥξ��
			$image = 'land6.gif';
			$alt = '��';
		} else {
			$image = 'land57.gif';
			$alt = '�ڴ�';
		}
		$naviTitle = $alt;
	} elsif($l == $HlandOcean) {
		# ����̵����
		$image = 'ocean_10.gif';
		$alt = '̵����';
		$naviTitle = $alt;
	} elsif($l == $HlandOPlayer){
		# ����
		if($l == $HlandOPlayer){
			$image = 'ocean_20.gif';
			$alt = "${tName}${sAfterName}";
		}
		$naviTitle = $alt;
	} elsif($l == $HlandEarth) {
		# �ϵ�
		$image = 'cosmo2.gif';
		$alt = '�ϵ�';
		$naviTitle = $alt;
	}elsif( ($l == $HlandSunit) || ($l == $HlandSCity) ||
			($l == $HlandSFarm) || ($l == $HlandSFactory) ||
			($l == $HlandSpaceBase) || ($l == $HlandSDefence) ||
			($l == $HlandSAEisei)){
		if($l == $HlandSunit) {
			if($lv == 20) {
				$image = 'cosmo6.gif';
				$alt = '�����˲���˥å�';
				$naviTitle = '�����˲���˥å�';
			} elsif($lv == 1) {
				$image = 'cosmo4.gif';
				$alt = '����������˥å�';
				$naviTitle = '����������˥å�';
			} elsif($lv == 10) {
				$image = 'cosmo5.gif';
				$alt = '�����˥å�';
				$naviTitle = '�����˥å�';
			} else {
				$image = 'cosmo3.gif';
				$alt = '������å�˥å�';
				$naviTitle = '������å�˥å�';
			}
		} elsif($l == $HlandSCity) {
			# �����Ի�
			my($p, $n);
			if($lv < 30) {
				$p = 7;
				$n = '����¼';
				$naviTitle = '����¼';
			} elsif($lv < 100) {
				$p = 8;
				$n = '����Į';
				$naviTitle = '����Į';
			} else {
				$p = 9;
				$n = '�����Ի�';
				$naviTitle = '�����Ի�';
			}
			$naviText = "${lv}$HunitPop";
			$image = "cosmo${p}.gif";
			$alt = "$n(${lv}$HunitPop)";
		} elsif($l == $HlandSFarm) {
			# ��������
			$image = 'cosmo10.gif';
			$alt = "��������(${lv}0${HunitPop}����)";
			$naviTitle = '��������';
			$naviText = "${lv}0${HunitPop}����";
		} elsif($l == $HlandSFactory) {
			# ���蹩��
			$image = 'cosmo11.gif';
			$alt = "���蹩��(${lv}0${HunitPop}����)";
			$naviTitle = '���蹩��';
			$naviText = "${lv}0${HunitPop}����";
		} elsif($l == $HlandSpaceBase) {
			# ����ߥ��������
			my($level) = expToLevel($l, $lv);
			$image = 'cosmo12.gif';
			$alt = "����ߥ�������� (��٥� ${level}/�и��� $lv)";
			$naviTitle = "����ߥ��������";
			$naviText = "��٥� ${level}/�и��� $lv";
		} elsif($l == $HlandSDefence) {
			# �����ɱһ���
			$image = 'cosmo14.gif';
			$alt = "�����ɱһ���";
			$naviTitle = "�����ɱһ���";
		} elsif($l == $HlandSAEisei) {
			# �������
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
			$alt .= "(����ĺ��)";
			$naviText .= "(����ĺ��)";
		}elsif($dis > 45){
			$alt .= "(����)";
			$naviText .= "(����)";
		}elsif($dis > 30){
			$alt .= "(�������)";
			$naviText .= "(�������)";
		}
	}

	if($js == 1){
		# js�⡼��
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
		# ��ȯ���̤ξ��ϡ���ɸ����

		if($mode == 1){
			out("<td class=e><A HREF=\"JavaScript:void(0);\" onclick=\"ps($x,$y)\">");
		}elsif($mode == 3){
#			if(($HspaceID >= 5261) && ($HspaceID <= 5264)){
#				# �ƥ��ȥ⡼��
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
			# �������

			out("<td class=e>");
			out("<A HREF=\"${HthisFile}?Sight=${sflg}\" target=\"_blank\" \"JavaScript:void(0);\" onMouseOver=\"Navi($x, $y,'$image', '$naviTitle', '$naviText', $naviExp);\" onMouseOut=\"NaviClose(); return false\">");
		}else{
			out("<td class=e>");
			out("<A HREF=\"JavaScript:void(0);\" onMouseOver=\"Navi($x, $y,'$image', '$naviTitle', '$naviText', $naviExp);\" onMouseOut=\"NaviClose(); return false\">");
		}
		my $ntmp = "";
		if(($HdebugMode > 0) && ($nation > 0)){
			my $ntmp2 = ($HdebugMode == $nation) ? "��" : $nation;
			$ntmp = "<span style=\"position:absolute;text-decoration:none;color:#ff0000;font-weight : bold;font-size:12pt;\">$ntmp2</span>";
		}
		out("$ntmp<IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" width=32 height=32 BORDER=0>");

		# ��ɸ�����Ĥ�
		if(($mode == 1) || ($mode == 3)){
			out("</A></td>");
		}else{
			out("</td>");
		}
	}
	$LandCount{$nation}++;
	$LandCount2{$naviTitle}++;
}# landString

# ̸��ɽ������

sub landString2 {
	my($l, $lv, $x, $y, $mode, $comStr, $nation, $js) = @_;
	my($point) = "($x,$y)";

	my $image = 'land54.gif';
	my $alt = 'ǻ̸';

	if($js == 1){
		# js�⡼��
		out(qq#<td class=e><A HREF="JavaScript:void(0);" onclick="ps$point" #);
		if($mode == 1 && $HmainMode ne 'landmap') {
			out(qq#onMouseOver="set_com($x, $y, '$point $alt');window.status = '$point $alt $comStr'; return true;" onMouseOut="not_com();window.status = '';">#);
		}elsif($HmainMode eq 'landmap') {
			out(qq#onMouseOver="window.status = '$point $alt $comStr'; return true;" onMouseOut="window.status = '';">#);
		}
		out("<IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" TITLE=\"$point $alt $comStr\" width=32 height=32 BORDER=0></A></td>");
	}else{
		# ��ȯ���̤ξ��ϡ���ɸ����

		out("<A HREF=\"JavaScript:void(0);\" onclick=\"ps$point\">") if($mode == 1);
		out("<td class=e><IMG SRC=\"$image\" ALT=\"$point $alt $comStr\" width=32 height=32 BORDER=0></td>");
		out("</A>") if($mode == 1); # ��ɸ�����Ĥ�
	}
	$LandCount{$nation}++;
	$LandCount2{$alt}++;
}

# ̸��ɽ��������֤���¸
sub SearchKiriMons {
	my($land, $landValue) = @_;
	my($special) = 8;
	my($i ,$s , $x, $y, $sx, $sy, $range, $k);
	for($y = 0; $y < $HislandSize; $y++) {
		for($x = 0; $x < $HislandSize; $x++) {
			if((($land->[$x][$y] == $HlandMonster) || ($land->[$x][$y] == $HlandHaribote)) && ($HmonsterSpecial[(monsterSpec($landValue->[$x][$y]))[0]] == $special)) {
				# ̸��ȯ����������á��ϥ�ܥƤΤȤ�
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
			# $i = 0;�Ȥ���м��Ȥ�̸�˱����

			for($i = $s; $i < $range; $i++) {
				$sx = $x + $ax[$i];
				$sy = $y + $ay[$i];
				$sx-- if(!($sy % 2) && ($y % 2)); # �Ԥˤ�����Ĵ��
				unless(($sx < 0) || ($sx >= $HislandSize) || ($sy < 0) || ($sy >= $HislandSize)){
					$Kiri->[$sx][$sy] = $k if($Kiri->[$sx][$sy] != 1);
				}
			}
		}
	}
}


#----------------------------------------------------------------------
# �ƥ�ץ졼�Ȥ���¾
#----------------------------------------------------------------------
# ������ؤ褦��������
sub tempPrintIslandHead {
	my $mId = $Hislands[$HcurrentNumber]->{'id'};
	out(<<END);
<CENTER>
${HtagBig_}${HtagName_}��${HcurrentName}${AfterName}��${H_tagName}�ؤ褦��������$_[0]${H_tagBig}<BR>
$HtempBack<BR>
</CENTER>
END
}
# �ʥӥ�������������ɥ�
sub tempNavi {
	my($mode) = @_;
	if($mode == 3){
		# ����ޥå�
		$tHislandSize = $HislandSize;
	}elsif($mode == 4){
		# ����ޥå�
		$tHislandSize = $HoceanSize;
	}else{
		$tHislandSize = $HislandSize;
	}
	out(<<END);
<SCRIPT Language="JavaScript">
<!--

MONSTER0 = "��¤����";
MONSTER1 = "";
MONSTER2 = "�����������ϹŲ�";
MONSTER3 = "";
MONSTER4 = "������2���ư����";
MONSTER5 = "�����粿���ư���뤫����";
MONSTER6 = "������������ϹŲ�";
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
MONSTER32 ="����������Ū�ʱ������";
MONSTER33 ="��ư�������᤯���������ѵ��Ϥ����뱧�����";
MONSTER34 ="��ư�����ȤƤ����ᤤ�������";
MONSTER35 ="���ѵ��Ϥ��⤤�������";

function Navi(x, y, img, title, text, exp) {
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "visible";
	if(x + 1 > $tHislandSize / 2) {
		// ��¦
		StyElm.style.marginLeft = (x - 5) * 32 -10;
	} else {
		// ��¦
		StyElm.style.marginLeft = (x + 1) * 32;
	}
	if(y + 1 == $tHislandSize) {
		// ��¦
		StyElm.style.marginTop = (y - $tHislandSize - 1.5) * 32;
	} else if(y + 1 > $tHislandSize / 2) {
		// ��¦
		StyElm.style.marginTop = (y - $tHislandSize - 1) * 32;
	} else {
		// ��¦
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

# �����糫ȯ�ײ�إå�
sub tempOwnerHeader {
	$monthname = $Hmonthname[($HislandTurn % 12) + 1];
	my $ownername = $Hislands[$HcurrentNumber]->{'ownername'};
	out(<<END);
<CENTER>
${HtagBig_}${HtagNumber_}������$HislandTurn��($monthname)${H_tagNumber}${H_tagBig}��${HtagBig_}${HtagName_}${HcurrentName}${AfterName}${H_tagName}��ȯ�ײ�${H_tagBig}<BR>
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
[<A HREF="$HthisFile">�ȥåפ����</A>]��
[<A href="$HthisFile?Ocean=0" target=_blank>�����</A>]��
[<A href="$HthisFile?space=0" target=_blank>�����</A>${solarwind}]��
[<A HREF="JavaScript:void(0);" onClick="openCUSTOM();return false;">��ͭ������̤�</A>]��
END
	if($Hallyflg && $HallyDisp){
		out("[<A HREF=\"JavaScript:void(0);\" onClick=\"openCAMP();return false;\">�رĲ��̤�</A>]��");
		out("[<A HREF=\"JavaScript:void(0);\" onClick=\"openBBS();return false;\">�رķǼ��Ĥ�</A>]��") if($Hcampbbs);
		out("[<A HREF=\"JavaScript:void(0);\" onClick=\"openCHAT();return false;\">�رĲ�ļ���</A>]") if($Hcampchat);
	}
	out("</CENTER>");
	unless($Hislands[$HcurrentNumber]->{'order'} & 8){
		require('exchange.cgi');
		readExchange();
		infoExchange2($Hislands[$HcurrentNumber]->{'cmdtime'});
	}
}

# �����糫ȯ�ײ�

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
<B>�ѥ����</B></BR>
<INPUT TYPE=password NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}">
<HR>
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
<HR>
<B>�ײ��ֹ�</B><SELECT NAME=NUMBER>
END
	# �ײ��ֹ�

	my($j);
	for($i = 0; $i < $HcommandMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}

	out(<<END);
</SELECT><BR>
<HR>
<B>��ȯ�ײ�</B><BR>
<SELECT NAME=COMMAND onChange=StatusMsg(this.options[this.selectedIndex].value) onClick=StatusMsg(this.options[this.selectedIndex].value)>
END

	#���ޥ��
	my($kind, $cost, $s);
	for($i = 0; $i < $HcommandTotal; $i++) {
		$kind = $HcomList[$i];
		$cost = $HcomCost[$kind];
		if($cost == 0) {
			$cost = '̵��'
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
	out("</SELECT><HR><B>��ɸ��(</B><SELECT NAME=POINTX>");
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
	out("</SELECT><B>)</B><INPUT TYPE=\"checkbox\" NAME=\"xy1\" CHECKED><br><B>��ɸ��(</B><SELECT NAME=POINTTX>");
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
	out("<HR><B>����</B><SELECT NAME=AMOUNT>");
	# ����
	for($i = 0; $i < 50; $i++) {
		out("<OPTION VALUE=$i>$i\n");
	}
	for($i = 50; $i < 999; $i += 50) {
		out("<OPTION VALUE=$i>$i\n");
	}
	out(<<END);
</SELECT>
<HR><B>��ɸ��${AfterName}</B>��
<B><A HREF=JavaScript:void(0); onClick="jump(myForm, '$HjavaMode')"> ɽ\�� </A></B><BR>
<SELECT NAME=TARGETID>$HtargetList<BR></SELECT>
<HR><B>ư��</B><BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=insert CHECKED>����
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=write>���<BR>
<INPUT TYPE=radio NAME=COMMANDMODE VALUE=delete>���<HR>
<INPUT TYPE=submit VALUE="�ײ�����" NAME=CommandButton$Hislands[$HcurrentNumber]->{'id'}>
</CENTER></FORM></TD>
<TD $HbgMapCell>
END
	islandMap(1);	# ����Ͽޡ���ͭ�ԥ⡼��
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

# ���ϺѤߥ��ޥ��ɽ��
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
	$target = "̵��" if($target eq '');
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

	my($j) = sprintf("%02d��", $number + 1);

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
		# �ߥ������
		$arg = 1 if($kind == $HcomMissileGM);
		my($n) = ($arg == 0 ? '̵����' : "${arg}ȯ");
		out("$target$point��$name($HtagName_$n$H_tagName)");
	} elsif($kind == $HcomMissileMGM) {
		out("$target��$name");
	} elsif($kind == $Hcomcolony){
		if(($arg == 1) || ($arg == 2)) {
			out("�����ѡ�������ɥ����ƥ�ȯư����($arg)");
		}else{
			out("$target��$name");
		}
	} elsif(($kind == $HcomTeisatu) ||
			($kind == $HcomSpy)) {
		# ��������廡
		out("$target$point��$name");
	} elsif($kind == $HcomSendMonster) {
		# �����ɸ�
		if($arg == 1) {
			out("$target�إᥫ�����ɸ�");
		} elsif($arg == 2) {
			out("$target�إ���ƥͥ����Τ��ɸ�");
		} elsif($arg == 3) {
			out("$target�س���ᥫ���Τ��ɸ�");
		} else {
			out("$target�إᥫ���Τ��ɸ�");
		}
	} elsif($kind == $HcomSSendMonster) {
		# S�����ɸ�
		$arg = $HmonsterNumber - 1 if($arg >= $HmonsterNumber);
		out("$target��$name($HmonsterName[$arg])");
	} elsif($kind == $HcomSell) {
		# �������
		out("$name$value");
	} elsif(($kind == $HcomOreSell) || ($kind == $HcomOilSell) || ($kind == $HcomWeponSell)){
		# ���
		$arg = 1 if($arg <= 0);
		out("$target��$name($arg)");
	} elsif(($kind == $HcomOreBuy) || ($kind == $HcomOilBuy) || ($kind == $HcomWeponBuy)){
		# ����
		$arg = 1 if($arg <= 0);
		out("$name($arg)");
	} elsif($kind == $HcomWarp) {
		# ž������
		if($arg == 0) {
			out("$point��$name(${target}�Ԥ�)");
		} else {
			# ž�������ֺ���
			my($s);
			if($arg == 1) {
				$s = '����';
			} elsif($arg == 2) {
				$s = '��';
			} elsif($arg == 3) {
				$s = '����';
			} elsif($arg == 4) {
				$s = '����';
			} elsif($arg == 5) {
				$s = '��';
			} else {
				$arg = 6;
				$s = '����';
			}
			$name = "${HtagComName_}ž�������ַ���${H_tagComName}";
			out("$point��$name($s)");
		}
	} elsif($kind == $HcomPropaganda) {
		# Ͷ�׳�ư
		if($arg == 0) {
			out("$name");
		} else {
			out("$name($arg��)");
		}
	} elsif(($kind == $HcomMoney) || ($kind == $HcomFood)) {
		# ���

		out("$target��$name$value");
	} elsif($kind == $HcomEmigration) { # ��̱
		out("$point�οͤ�$target��$name");
	} elsif($kind == $HcomDestroy) {
		# ����

		if($arg != 0) {
			out("$point��$name(ͽ��${value})");
		} else {
			out("$point��$name");
		}
	} elsif(($kind == $HcomSearch) || ($kind == $HcomBank)) {
		# �ϼ�Ĵ��,������

		out("$point��$name(ͽ��${value})");
	} elsif($kind == $HcomDummy) {
		if($arg == 1) {
			out("$point�ǥ��ߡ��η���");
		} elsif($arg == 2) {
			out("$point�ǥ��ߡ����Ω��");
		} else {
			out("$point�ǥ��ߡ�����");
		}
	} elsif(($kind == $HcomManipulate) || ($kind == $HcomSTManipulate) || ($kind == $HcomShipM)) {
		# ������ST�����������
		my($s);
		if($arg <= 1) {
			$arg = 1;
			$s = '����';
		} elsif($arg == 2) {
			$s = '��';
		} elsif($arg == 3) {
			$s = '����';
		} elsif($arg == 4) {
			$s = '����';
		} elsif($arg == 5) {
			$s = '��';
		} else {
			$arg = 6;
			$s = '����';
		}
		if($kind == $HcomMonsEnsei){
			out("$name($s)");
		}else{
			out("$target��$name($s)");
		}
	} elsif($kind == $HcomMonument) {
		# ��ǰ��
		if($arg <= 3) {
			out("$point��${name}($HmonumentName[$arg])");
		} else {
			out("$point��$name");
		}
	} elsif($kind == $HcomSMonument) {
		# ���쵭ǰ��
		if($arg <= 3) {
			out("$point��${name}($HsmonumentName[$arg])");
		} else {
			out("$point��$name");
		}
	} elsif($kind == $HcomDbase) {
		if($arg == 1) {
			out("$point��${name}(ST)");
		} elsif($arg == 2) {
			out("$point��${name}(̸)");
		} else {
			out("$point��$name");
		}
	} elsif(($kind == $HcomFarm) ||
		 ($kind == $HcomSFarm) ||
		 ($kind == $HcomFactory) ||
		 ($kind == $HcomTower) ||
		 ($kind == $HcomPort) ||
		 ($kind == $HcomBase) ||
		 ($kind == $HcomMountain)) {
		# ����դ�
		if($arg == 0) {
			out("$point��$name");
		} else {
			out("$point��$name($arg��)");
		}
	} elsif(($kind == $HcomPresent) ||
		 ($kind == $HcomPresentAid)) {
		# �ץ쥼��ȡ��ץ쥼��Ⱦ���
		my($s);
		if($arg <= 0) {
			$arg = 0;
			$s = '����';
		} elsif($arg == 1) {
			$s = '����������';
		} elsif($arg == 2) {
			$s = '�ɡ���';
		} elsif($arg == 3) {
			$s = '������';
		} elsif($arg == 4) {
			$s = 'ͷ����';
		} elsif($arg == 5) {
			$s = '�ع�';
		} elsif($arg == 6) {
			$s = '����';
		} elsif($arg == 7) {
			$s = '���Ի�';
		} elsif($arg == 8) {
			$s = 'ưʪ��';
		} elsif($arg == 9) {
			$s = '������';
		} elsif($arg == 10) {
			$s = '���õ�ǰ��';
		} else {
			$arg = 11;
			$s = '�ҳ�����';
		}
		if($kind == $HcomPresent) { 
			out("$point��$name($s)");
		} else {
			out("$target��$name($s)");
		}
	# ���åХȥ�

	} elsif(($kind == $HcomMonsEgg) ||
		 ($kind == $HcomMonsEsa) ||
		 ($kind == $HcomMonsTettai) ||
		 ($kind == $HcomMonsExer) ||
		 ($kind == $HcomMonsSell)) {
		out("$name");
	} elsif(($kind == $HcomMonsEnsei) ||
		 ($kind == $HcomMonsEsaAid) ||
		 ($kind == $HcomMonsAid)) {
		out("$target��$name");
	} elsif($kind == $HcomShip) {
		# �������ѹ�
		my($s);
		if($arg <= 0) {
			$arg = 0;
			$s = '�ü�';
		} elsif($arg == 1) {
			$s = '��ư';
		} elsif($arg == 2) {
			$s = '�ɸ�';
		} elsif($arg == 3) {
			$s = 'ű��';
		} elsif($arg >= 4) {
			$s = '����';
			$arg = 4;
		}
		out("$target$point��$name($s)");
	} elsif($kind == $HcomShipbuild) {
		# ¤��
		out("$point��$name($arg)");
	} elsif($kind == $HcomSBuild) {
		# ������߷�
		out("�����ĥͽ��̿��(���⤪���ޤ���)");
	} elsif(($kind == $HcomSUnit) ||
			($kind == $HcomSpaceFarm) ||
			($kind == $HcomSFactory) ||
			($kind == $HcomSEisei) ||
			($kind == $HcomSpaceBase)) {
		$target = "$HtagName_$SpaceName$H_tagName";
		# ����դ�
		if($arg == 0) {
			out("$target$point��$name");
		} else {
			out("$target$point��$name($arg��)");
		}
	} elsif(($kind == $HcomSPioneer) ||
			($kind == $HcomSDestroy) ||
			($kind == $HcomSDbase) ||
			($kind == $HcomSOccupy)) {
		$target = "$HtagName_$SpaceName$H_tagName";
		out("$target$point��$name");
	} elsif(($kind == $HcomSMissileGM) ||
			($kind == $HcomSMissilePP) ||
			($kind == $HcomSMissile)){
		my($n) = ($arg == 0 ? '̵����' : "${arg}ȯ");
		$target = "$HtagName_$SpaceName$H_tagName";
		out("$target$point��$name($HtagName_$n$H_tagName)");
	} elsif(($kind == $HcomOMissileNM) ||
			($kind == $HcomOMissilePP) ||
			($kind == $HcomOMissileSPP)){
		my($n) = ($arg == 0 ? '̵����' : "${arg}ȯ");
		$target = "$HtagName_$OceanName$H_tagName";
		out("$target$point��$name($HtagName_$n$H_tagName)");
	} elsif($kind == $HcomSFood) {
		# ���迩���Ǿ夲
		$value = ($arg < 1)? 100 : $arg * 100;
		$value = "$HtagName_$value$HunitFood$H_tagName";
		out("$name$value");
	} else {
		# ��ɸ�դ�
		out("$point��$name");
	}
	out("${H_normalColor}</A><BR>");
}

# �����ȡ�������Ǽ��ĥ����å�
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
<INPUT TYPE=submit value="�����ȡ��Ѹ����̿����ᶷ�����åХȥ롦�ϲ�ɽ��" NAME=CLbbsRButton$Hislands[$HcurrentNumber]->{'id'} onClick="clbbsSubmit()">
</FORM>
END
	my($comment) = $Hislands[$HcurrentNumber]->{'comment'};
	out("�����ȡ�$comment<br>");
	my $lbbs = $Hislands[$HcurrentNumber]->{'lbbs'};
	$line = $lbbs->[0];
	if($line =~ /([0-9]*)\<(.*)\<([0-9]*)\>(.*)\>(.*)$/) {
		my($bbs1,$bbs2,$bbs3,$bbs4,$bbs5) = ($1,$2,$3,$4,$5);
		if($bbs4){
			$bbs4 =~ /([0-9]*)/;
			out("�ǿ��δѸ����̿��񤭹���: $1 ��������<br>");
		}
	}
	my($monster) = ($island->{'monster'});
	if($monster->[0] != 0) {
		my($tn) = $HidToNumber{$monster->[2]};
		my($mname) = $monster->[1];
		if($tn ne '') {
			out("���åХȥ������桪��<br>");
		}else{
			out("������á�$mname<br>");
		}
	}
}

# �����ȡ��Ѹ����̿����ᶷ��ɽ��
sub clbbsMain {
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};
	$monthname = $Hmonthname[($HislandTurn % 12) + 1];
	out(<<END);
<CENTER>
${HtagBig_}${HtagNumber_}������$HislandTurn��($monthname)${H_tagNumber}${H_tagBig}��${HtagBig_}${HtagName_}${HcurrentName}${AfterName}${H_tagName}${H_tagBig}<BR>
<a href="Javascript:void(0);" onclick="window.close()">���̤��Ĥ���</A>
</CENTER>
END
	ugMap($island,2);	# �ϲ�
	if($island->{'order'} & 64){
		tempLocalbbs(1);	# ������Ǽ���
		tempRecent(1);		# �ᶷ
	}else{
		tempRecent(1);		# �ᶷ
		tempLocalbbs(1);	# ������Ǽ���
	}
	tempCommentInput();	# ���������ϥե�����

	tempMapTotal();		# �ޥå׽���
}

# �������ޥ������̤�ɽ��
sub customMain {
	my($mode) = @_;
	# id����������
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};
	$monthname = $Hmonthname[($HislandTurn % 12) + 1];
	my($i,@ccbx);
	if($mode){
		# ��å������򹹿�
		for($i = 0; $i < 12; $i++) {
			if($Hcustom[$i]){
				$island->{'order'} |= 2 ** $i;
			}else{
				$island->{'order'} ^= 2 ** $i if($island->{'order'} & 2 ** $i);
			}
		}
		# �ǡ����ν񤭽Ф�
		if(!writeIslandsFile($HcurrentID, 1)) {
			unlock();
			tempFailWrite();
			return;
		}
		out("${HtagBig_}�ǡ����򹹿����ޤ���${H_tagBig}<HR>");
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
${HtagBig_}${HtagNumber_}������$HislandTurn��($monthname)${H_tagNumber}${H_tagBig}��${HtagBig_}${HtagName_}${HcurrentName}${AfterName}${H_tagName}${H_tagBig}<BR>
$HtempBack<br>
<h1>��${AfterName}���Ȥθ�ͭ����</h1>
<FORM name="customMain" action="$HthisFile" method="POST">
<table>
<INPUT TYPE="checkbox" NAME="custom4"$ccbx[4]>��ư����ͶƳ��ȯ��(���ä�����ȶ���Ū�˲���ͶƳ��ȯ��)<br>
<INPUT TYPE="checkbox" NAME="custom5"$ccbx[5]>�η���ϻ����������롣(�����å���Ϥ����ȹ��Ф�����)<br>
<INPUT TYPE="checkbox" NAME="custom7"$ccbx[7]>����ϻ����������롣(�����å���Ϥ�����ʼ�������)<br>
<INPUT TYPE="checkbox" NAME="custom11"$ccbx[11]>���Ĥϻ����������롣(�����å���Ϥ����ȸ���������)<br>
<INPUT TYPE="checkbox" NAME="custom3"$ccbx[3]>�������줿��������ɽ�����ʤ���<br>
<INPUT TYPE="checkbox" NAME="custom8"$ccbx[8]>��ȯ�⡼�ɤǴѸ����̿����Ƕ�Υ������̲��̲�(�Ѳ����줿���ͤ餷��������)<br>
<INPUT TYPE="checkbox" NAME="custom6"$ccbx[6]>��ȯ�⡼�ɤǴѸ����̿����ᶷ�ν��֤ˤ��롣<br>
<INPUT TYPE="checkbox" NAME="custom9"$ccbx[9]>ŷ���Խ����ߤ��줿̿���Ĥ�(���磱����ޤ�)<br>
<INPUT TYPE="checkbox" NAME="custom10"$ccbx[10]>���ɽ�кҼ�ư���쵡ǽ��Ȥ�<br>
</table>
<INPUT TYPE=submit value="����" NAME=customMButton$Hislands[$HcurrentNumber]->{'id'}">
</FORM>
</CENTER>
<h2>��ư����ͶƳ��ȯ��</h2>
�����󳫻ϻ��ˤɤ�ʲ��ä����ȼ���ˣ�ɤ�ʾ�β��ä�����ȡ�<br>
̿��Σ����˶���Ū�˲���ͶƳ��ȯ�ͤ���������¹Ԥ���ޤ���<br>
����ͶƳ��ȯ�ͤ���ưȯ�ͤ��줿��硢����Σ�����̿��ϡ��¹Ԥ���ޤ���(�����ʤ�м¹Ԥ���ޤ�)<br>
���餫�θ����Ǵ��˲��ä����ʤ����ϡ���ߤΥ���ή��ޤ���������Σ�����̿�᤬�¹Ԥ���ޤ���<br>
�西��������å��Ǥ��ʤ��ͤˤ䤵���������⤷��ʤ���ǽ�Ǥ���<br>

<h2>ŷ���Խ����ߤ��줿̿���Ĥ�</h2>
�����ԻԷ��ߡ����å��Ǥ��夲������ˡ���Ȥ���ŷ���Խ�ˤ����ߤ���Ƥ⡢<br>
����ǽ����Ѥ���ȡ�̿��ͽ����ܤ���ä��ޤ��󡣤�����������ޤǤǤ���<br>
(���˳����ԻԤ��������¤�Ǥ����Ȥ����飱�����ܤϾä���)<br>
̿�᤬�Ԥ��ʤ��ƻ�ⷫ��ˤʤ��礬����ޤ��������ʤ��鵬�꥿�������ⷫ�ꤷ����硢<br>
̿�᤬���ä��Ȥ��Ƥ⼫ư������̿�����Ƭ�˾�񤭤���ޤ���<br>
<h2>���ɽ�кҼ�ư���쵡ǽ</h2>
�кҤǾ��ɽ𼫿Ȥ�ǳ������ä�������ˡ������ä���ɸ�˼�ư�Ƿ���̿�᤬���־�����Ϥ���ޤ���<br>
(�Ͼ�ξ����Ϥʤ餷��)̿�᤬���å���ͤޤäƤ����顢����ڤ���㤤�ޤ���<br>
��������ä��Ȥ��Ƥ�����̵�Ѥ�̿�᤬���־�����ä���äƤ����ä������⡦������<br>
�褦����ˡ�Ⱦ���֥ץ쥤���Ƥ��뤷�Ƥ��������������⡪������ʤ���ǽ�Ǥ���<br>
END
}

# �ϲ���ɽ��
sub ugMap {
	my($island,$mode) = @_;

	# �Ϸ����Ϸ��ͤ����
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
		out("<td colspan=3>�ϲ�${i}($ugX,$ugY)</td></tr><tr>");
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
# �ϲ���ɽ��
sub ugString {
	my($l, $lv, $x, $y, $mode, $xx, $yy) = @_;
	my $image = $HugImage[$l];
	my $alt = $Hunderground[$l];
	$alt .= "(${lv}$HunitPop)" if($l == $HugTosi);
	out("<td class=e>");
	# ��ȯ���̤ξ��ϡ���ɸ����

	out(qq#<A HREF="JavaScript:void(0);" onclick="ps($x,$y,$xx,$yy)" onMouseOver="window.status = '($x,$y) $alt'; return true;" onMouseOut="window.status = '';">#) if($mode == 1);

	out("<IMG SRC=\"$image\" ALT=\"($x,$y) $alt\" width=32 height=32 BORDER=0>");

	# ��ɸ�����Ĥ�
	out("</A>") if($mode == 1);
	out("</td>");
}

# ���������ϥե�����

sub tempCommentInput {
	out("<DIV ID='CommentBox'>");
	islandmonster(0);# ��β���
	my($comment) = $Hislands[$HcurrentNumber]->{'comment'};
	my($select0, $select1, $select2, $select3, $select4);
	$select0 = ' CHECKED' if($Hislands[$HcurrentNumber]->{'commentLabel0'});
	$select1 = ' CHECKED' if($Hislands[$HcurrentNumber]->{'commentLabel1'});
	$select2 = ' CHECKED' if($Hislands[$HcurrentNumber]->{'commentLabel2'});
	$select3 = ' CHECKED' if($Hislands[$HcurrentNumber]->{'commentLabel3'});
	$select4 = ' CHECKED' if($Hislands[$HcurrentNumber]->{'commentLabel4'});

	#��٥�򥹥��å������ˤ����������
	my($label0_1n,$label0_2n) = split(/<>/,$HlabelName[0]);
#	my($label1_1n,$label1_2n) = split(/<>/,$HlabelName[1]);
#	my($label2_1n,$label2_2n) = split(/<>/,$HlabelName[2]);
#	my($label3_1n,$label3_2n) = split(/<>/,$HlabelName[3]);
#	my($label4_1n,$label4_2n) = split(/<>/,$HlabelName[4]);
	
	#�����ȥ�٥�4̤���ѡ����Ѥ�����ϰʲ���HTML��Checkbox���ɲä��� by ShibaAni
	out(<<END);
<HR>
${HtagBig_}�����ȹ���${H_tagBig}<BR>
<FORM action="$HthisFile" method="POST">
<TABLE BORDER><TR>
<TH $HbgTitleCell>������</TH><TD $HbgNameCell colspan="3"><INPUT TYPE=text NAME=MESSAGE SIZE=110 VALUE="$comment"></TD>
</TR><TR>
<TH $HbgTitleCell rowspan=2>�ջ�ɽ��</TH><TD $HbgNameCell rowspan=2>
<INPUT TYPE=checkbox NAME="COMMENT_LABEL0" VALUE="1"$select0>$label0_1n<br>
<INPUT TYPE=checkbox NAME="COMMENT_LABEL1" VALUE="1"$select1>$HlabelName[1]<br>
<INPUT TYPE=checkbox NAME="COMMENT_LABEL2" VALUE="1"$select2>$HlabelName[2]<br>
<INPUT TYPE=checkbox NAME="COMMENT_LABEL3" VALUE="1"$select3>$HlabelName[3]
</TD>
<TH $HbgTitleCell>�ѥ����</TH><TD $HbgNameCell><INPUT TYPE=password NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}"></TD>
</TR><TR>
<TD $HbgTitleCell colspan=2 align=center><INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
<INPUT TYPE=submit VALUE="�����ȹ���" NAME=MessageButton$Hislands[$HcurrentNumber]->{'id'}>
</TD></TR></TABLE>
�����ջ�ɽ���˶����ϤϤʤ���${AfterName}��ε�������ɽ�����ʤΰ�Ĥˤ����ޤ���
</FORM></DIV>
END
}

# �����������Ǽ���
sub tempLocalbbs {
	my($mode) = @_;
	if($HuseLbbs) {
		out("<DIV ID='localBBS'><HR>");
		if($mode == 0){
			out("${HtagBig_}${HtagName_}${HcurrentName}${AfterName}${H_tagName}�Ѹ����̿�${H_tagBig}<BR>");
			tempLbbsInput();   # �񤭹��ߥե�����

			tempLbbsContents(); # �Ǽ�������
		}elsif($mode == 1){
			out("${HtagBig_}${HtagName_}${HcurrentName}${AfterName}${H_tagName}�Ѹ����̿�${H_tagBig}<BR>");
			tempLbbsInputOW();
			tempLbbsContents(); # �Ǽ�������
		}elsif($mode == 3){
			out("${HtagBig_}${HtagName_}�ֱ���ޥåס�${H_tagName}�Ѹ����̿�${H_tagBig}<BR>");
			tempLbbsInput();   # �񤭹��ߥե�����

			tempLbbsContents(3); # �Ǽ�������
		}elsif($mode == 4){
			out("${HtagBig_}${HtagName_}�ֳ���ޥåס�${H_tagName}�Ѹ����̿�${H_tagBig}<BR>");
			tempLbbsInput();   # �񤭹��ߥե�����

			tempLbbsContents(4); # �Ǽ�������
		}
		out("</DIV>");
	}
}


# ������Ǽ������ϥե�����

sub tempLbbsInput {
	if ($HlbbsAuth) {
	out(<<END);
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>̾��</TH>
<TH $HbgTitleCell>����</TH>
</TR>
<TR>
<TD $HbgInfoCell><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD $HbgInfoCell><INPUT TYPE="text" SIZE=100 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TD $HbgInfoCell colspan="2">��ʬ���硧<SELECT NAME="ISLANDID">$HislandList</SELECT>
END
	out(<<END) if($HlbbsAnon);
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="ANON">�Ѹ���
END
	out(<<END);
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="PUBLIC" CHECKED>����
<INPUT TYPE="radio" NAME="LBBSTYPE" VALUE="SECRET"><FONT COLOR="red">����</FONT>
���ѥ���ɡ�<INPUT TYPE="password" SIZE=16 MAXLENGTH=32 NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}">
<INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonFO$HcurrentID">
�ֹ�<SELECT NAME=NUMBER>
END
	# ȯ���ֹ�

	my($j, $i);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}
	out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="�������" NAME="LbbsButtonFD$HcurrentID">
</TD></TR>
</TABLE>
</FORM>
END
	}else{
	out(<<END);
<FORM action="$HthisFile" method="POST">
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>̾��</TH>
<TH $HbgTitleCell>����</TH>
<TH $HbgTitleCell>ư��</TH>
</TR>
<TR>
<TD $HbgInfoCell><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD $HbgInfoCell><INPUT TYPE="text" SIZE=100 NAME="LBBSMESSAGE"></TD>
<TD $HbgInfoCell><INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonSS$HcurrentID"></TD>
</TR>
</TABLE>
</FORM>
END
	}
}

# ������Ǽ������ϥե����� owner mode��
sub tempLbbsInputOW {
	out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>̾��</TH>
<TH $HbgTitleCell colspan=2>����</TH>
</TR>
<TR>
<TD $HbgInfoCell><INPUT TYPE="text" SIZE=32 MAXLENGTH=32 NAME="LBBSNAME" VALUE="$HdefaultName"></TD>
<TD $HbgInfoCell colspan=2><INPUT TYPE="text" SIZE=100 NAME="LBBSMESSAGE"></TD>
</TR>
<TR>
<TH $HbgTitleCell>�ѥ����</TH>
<TH $HbgTitleCell colspan=2>ư��</TH>
</TR>
<TR>
<TD $HbgInfoCell><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="${\htmlEscape($HdefaultPassword)}"></TD>
<TD $HbgInfoCell align=right>
<INPUT TYPE="submit" VALUE="��Ģ����" NAME="LbbsButtonOW$HcurrentID">
</TD>
<TD $HbgInfoCell align=right>
�ֹ�

<SELECT NAME=NUMBER>
END
	# ȯ���ֹ�

	my($j, $i);
	for($i = 0; $i < $HlbbsMax; $i++) {
		$j = $i + 1;
		out("<OPTION VALUE=$i>$j\n");
	}
	out(<<END);
</SELECT>
<INPUT TYPE="submit" VALUE="�������" NAME="LbbsButtonDL$HcurrentID">
</TD>
</TR>
</TABLE>
</FORM>
END
}

# ������Ǽ�������
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
<TH $HbgTitleCell>�ֹ�</TH>
<TH $HbgTitleCell>��Ģ����</TH>
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
			# �Ѹ���
			if ($1 == 0) {
				# ����
				out("<TD $HbgLbbsCell>$HtagLbbsSS_$4 > $5$H_tagLbbsSS $speaker</TD></TR>");
			} else {
				# ����

				if(($Hallybbs) && ($HprintAlly == $ally) && ($HprintAlly > 0)){
					out("<TD $HbgLbbsCell>$HtagLbbsSS_$4 >(��) $5$H_tagLbbsSS $speaker</TD></TR>");
				}else{
					if(($HmainMode ne 'owner') && (($HprintID != $sID) || ($sID == 0))) {
						# �Ѹ���
						out("<TD $HbgLbbsCell><CENTER><FONT COLOR=gray>- ���� -</FONT></CENTER></TD></TR>");
					} else {
						# �����ʡ�
						out("<TD $HbgLbbsCell>$HtagLbbsSS_$4 >(��) $5$H_tagLbbsSS $speaker</TD></TR>");
					}
				}
			}
		} else {
			# ���

			$speaker = "<FONT COLOR=gray><B><SMALL>$2</SMALL></B></FONT>" if($HlbbsSpeaker && ($2 ne ''));
			out("<TD $HbgLbbsCell>$HtagLbbsOW_$4 > $5$H_tagLbbsOW $speaker</TD></TR>");
		}
	}
	}

	out(<<END);
</TD></TR></TABLE>
END
}

# ������Ǽ��Ĥ�̾������å��������ʤ����

sub tempLbbsNoMessage {
	out(<<END);
${HtagBig_}̾���ޤ������Ƥ��󤬶���Ǥ���${H_tagBig}$HtempBack
END
}

# �񤭤��ߺ��

sub tempLbbsDelete {
	out(<<END);
${HtagBig_}��Ģ���Ƥ������ޤ���${H_tagBig}<HR>
END
}

# ���ޥ����Ͽ
sub tempLbbsAdd {
	out(<<END);
${HtagBig_}��Ģ��Ԥ��ޤ���${H_tagBig}<HR>
END
}

# ���ޥ�ɺ��

sub tempCommandDelete {
	out(<<END);
${HtagBig_}���ޥ�ɤ������ޤ���${H_tagBig}<HR>
END
}

# ���ޥ����Ͽ
sub tempCommandAdd {
	out(<<END);
${HtagBig_}���ޥ�ɤ���Ͽ���ޤ���${H_tagBig}<HR>
END
}

# �������ѹ�����

sub tempComment {
	out(<<END);
${HtagBig_}�����Ȥ򹹿����ޤ���${H_tagBig}<HR>
END
}
# ���������ѹ�����

sub tempmonsedit {
	out(<<END);
${HtagBig_}��������򹹿����ޤ���${H_tagBig}<HR>
END
}

# �ᶷ
sub tempRecent {
	my($mode) = @_;
	out(<<END);
<HR><DIV ID='RecentlyLog2'>
${HtagBig_}${HtagName_}${HcurrentName}${AfterName}${H_tagName}�ζᶷ${H_tagBig}<BR>
END
	my($i);
	for($i = 0; $i < $HlogMax; $i++) {
		logFilePrint($i, $HcurrentID, $mode);
	}
	out("</DIV>");
}
# �ޥå׽���ɽ
sub tempMapTotal {
	if($HdebugMode > 0){
		out("<hr><DIV ID='mapStatistics'>��̾�ν���ɽ");
		out("<table border=0 cellspacing=0 cellpadding=0>");
		out("<tr><td $HbgTitleCell>��̾</td><td $HbgTitleCell>�Ŀ�</td><td $HbgTitleCell>���</td></tr>");
		foreach (sort { $LandCount2{$b} <=> $LandCount2{$a} } keys %LandCount2) {
			my $w = int($LandCount2{$_} * 10000 / $HpointNumber + 0.5) / 100;
			out("<tr><td $HbgTitleCell>$_ </td><td $HbgInfoCell>$LandCount2{$_}</td><td $HbgInfoCell>��${w}��</td></tr>");
		}
		out("</table></DIV>\n");
	}
	out("<br><DIV ID='mapStatistics'>${AfterName}��ͭ��ɽ");
	out("<table border=0 cellspacing=0 cellpadding=0>");
	out("<tr><td $HbgTitleCell>${AfterName}̾</td><td $HbgTitleCell>�Ŀ�</td><td $HbgTitleCell>���</td></tr>");
	foreach (sort { $LandCount{$b} <=> $LandCount{$a} } keys %LandCount) {
		my $w = int($LandCount{$_} * 10000 / $HpointNumber + 0.5) / 100;
		my($island,$name);
		if($_ > 0){
			$island = $Hislands[$HidToNumber{$_}];
			if($HidToNumber{$_} eq ''){
				$name = "����";
			}else{
				$name = $island->{'name'} . $AfterName;
			}
		}else{
			$name = "����";
		}
		out("<tr><td $HbgTitleCell>${name}</td><td $HbgInfoCell>$LandCount{$_}</td><td $HbgInfoCell>��${w}��</td></tr>");
	}
	out("</table></DIV>\n");
}
# ��ΰ�ư
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

# JS�⡼�ɤǥѥ���ɴְ㤤���˴ؿ���̵���ƥ��顼���Ф�������
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
	# �����Ǥμ��Ф�
	
	$HcurrentNumber = $HidToNumber{$HcurrentID};
	my($island) = $Hislands[$HcurrentNumber];
	my($name,$monster) = ($island->{'name'},$island->{'monster'});
	my($MBsId,$MBmId) = ($monster->[3],$monster->[4]);
	
	my($tn) = $HidToNumber{$monster->[2]};
	my($tMonster,$tIsland,$tName,$tMBsId, $tMBmId);

	if($tn eq '') {
	} else {
		# ������꤬����Ȥ�
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

	# ���ò�������
	my $image = $HmonsterImage[$MBmId];
	my $special = $HmonsterSpecial[$MBmId];
	# �Ų���?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
		(($special == 4) && (($HislandTurn % 2) == 0))) {
		$image = $HmonsterImage2[$MBmId];
	}
	$image = $island->{'monsurl'} if(substr($island->{'monsurl'},0,7) eq 'http://');
	
	my $image2 = $HmonsterImage[$tMBmId];
	$special = $HmonsterSpecial[$tMBmId];
	# �Ų���?
	if((($special == 3) && (($HislandTurn % 2) == 1)) ||
		(($special == 4) && (($HislandTurn % 2) == 0))) {
		$image2 = $HmonsterImage2[$tMBmId];
	}
	$image2 = $tIsland->{'monsurl'} if(substr($tIsland->{'monsurl'},0,7) eq 'http://');
	
	my($seityou) = $monster->[7] + $monster->[8] + $monster->[9] + $monster->[10];
	my($tseityou) = $tMonster->[7] + $tMonster->[8] + $tMonster->[9] + $tMonster->[10];

	$MBmId = ($MBmId == 0) ? "��" : $HmonsterName[$MBmId];
	$MBsId = ($MBsId == 0) ? "̵" : $HmonsterName[$MBsId];
	$tMBmId = ($tMBmId == 0) ? "��" : $HmonsterName[$tMBmId];
	$tMBsId = ($tMBsId == 0) ? "̵" : $HmonsterName[$tMBsId];
	
	if($seityou < 12) {
		$seityou = "��ǯ";
	} elsif($seityou < 25) {
		$seityou = "��ǯ";
	} else {
		$seityou = "Ϸǯ";
	}
	if($tseityou < 12) {
		$tseityou = "��ǯ";
	} elsif($tseityou < 25) {
		$tseityou = "��ǯ";
	} else {
		$tseityou = "Ϸǯ";
	}

	out(<<END);
<hr>
<center>
<table border>
<tr>
<th $HbgTitleCell colspan=14>${HtagTH_}���åХȥ�${H_tagTH}</th>
</tr>
<tr>
<td $HbgSubTCell>��</td>
<td $HbgSubTCell>����̾</td>
<td $HbgSubTCell>����</td>
<td $HbgSubTCell>������</td>
<td $HbgSubTCell>����</td>
<td $HbgSubTCell>���</td>
<td $HbgSubTCell>��Ĺ</td>
<td $HbgSubTCell>HP</td>
<td $HbgSubTCell>����</td>
<td $HbgSubTCell>����</td>
<td $HbgSubTCell>����</td>
<td $HbgSubTCell>̿��</td>
<td $HbgSubTCell>����</td>
<td $HbgSubTCell>��</td>
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
		# ��꤬���ʤ���
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
		# ��ȯ���̤λ�
		monstersetup($MBname, $HdefaultPassword, $island->{'monsurl'});
	}
}
#----------------------------------------------------------------------
# ���������ѹ��ե�����

#----------------------------------------------------------------------
sub monstersetup {
	my($MBname, $HdefaultPassword, $HdefaultMonsUrl) = @_;
	out(<<END);
<form action="$HthisFile" method="POST">
<INPUT TYPE="hidden" NAME=JAVAMODE VALUE="$HjavaMode">
<table border>
<tr>
<td $HbgTitleCell>��̾����̾��</td>
<td $HbgInfoCell><input type="text" size=32 maxlength=32 name="MONSNAME" value="$MBname"></td>
<td $HbgTitleCell>�ѥ����</td>
<td $HbgInfoCell><input type=password size=32 maxlength=32 name=PASSWORD value="${\htmlEscape($HdefaultPassword)}"></td>
<td $HbgTitleCell>��</td>
</tr>
<tr>
<td $HbgTitleCell>���ò���URL</td>
<td $HbgInfoCell colspan=3><input type=text size=80 maxlength=80 name="MONSURL" value="$HdefaultMonsUrl"></td>
<td $HbgTitleCell><input type="submit" value="�¹�" name="MonsButton$HcurrentID"></td>
</tr>
</table>
</form>
END
}

#----------------------------------------------------------------------
# ���������ѹ��⡼��
#----------------------------------------------------------------------
# �ᥤ��

sub monsMain {
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

	# ��������򹹿�
	$island->{'monster'}->[1] = htmlEscape($Hmonsname);
	$island->{'monsurl'} = htmlEscape($Hmonsurl);

	# �ǡ����ν񤭽Ф�
	writeIslandsFile($HcurrentID);

	# ������å�����
	tempmonsedit();

	# owner mode��
	ownerMain();
}

#------------------------------------------------
# �ʰץȡ��ʥ���
# ����ε�Ͽ
sub FightViewMain {

	if(!open(IN, "$HdirName/fight.log")){
		return;
	}
	my @lines = <IN>;
	close(IN);
	unlock();

#	out ("${HtagTitle_}����ε�Ͽ${H_tagTitle}<BR><DIV ALIGN=right>*�ԼԤ���̾�򥯥�å������������ξ���������ޤ�</DIV>\n");
	out ("<DIV ID='fightlog'>${HtagTitle_}����ε�Ͽ${H_tagTitle}</DIV><BR>\n");

	foreach $line(@lines) {
		chop($line);
		if($line =~ /<[0-9]*>/) {
			out("<hr><DIV ID='fightlogS'><H1>");
			$line =~ s/<|>//g;
			my $msg = ($line == 0) ? "ͽ�����" : ($line == 99) ? "�辡��" : $line."����";
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
${HtagBig_}${HtagName_}��${islandName}���${H_tagName}��������ͻ�${H_tagBig}<BR>
<a href=${HthisFile}?FightLog=0>${HtagBig_}���${H_tagBig}</a><BR>
<BR>
<TABLE BORDER><TR><TD>
END
	# ��ɸ(��)�����
	out("<IMG SRC=\"xbar.gif\" width=400 height=16><BR>");

	# ���Ϸ�����Ӳ��Ԥ����
	my($x, $y);
	for($y = 0; $y < $HislandSize; $y++) {
		# �������ܤʤ��ֹ�����
		if(($y % 2) == 0) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# ���Ϸ������
		for($x = 0; $x < $HislandSize; $x++) {
			$l = $land->[$x][$y];
			$lv = $landValue->[$x][$y];
			landString($l, $lv, $x, $y, 1, $comStr[$x][$y]);
		}

		# ������ܤʤ��ֹ�����
		if(($y % 2) == 1) {
			out("<IMG SRC=\"space${y}.gif\" width=16 height=32>");
		}

		# ���Ԥ����
		out("<BR>");
	}
	out("</TD></TR></TABLE></CENTER>\n");
}

1;
