#----------------------------------------------------------------------
# Ȣ����� ver2.30
# ����������⥸�塼��
# ���Ѿ�������ˡ���ϡ�qhako-readme.txt�ե�����򻲾�
#----------------------------------------------------------------------
# ���ۤ�Ȣ��  (ver5.53)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# �Ƽ�������
# (����ʹߤ���ʬ�γ������ͤ�Ŭ�ڤ��ͤ��ѹ����Ƥ�������)
#----------------------------------------------------------------------
#----------------------------------------
# ������οʹԤ�ե�����ʤ�
#----------------------------------------
# �ȥåץڡ�����ɽ��������Υ������
$HtopLogTurn = 12;

# ���ե������ݻ��������
$HlogMax = 12; 

# �Хå����åפ򲿥����󤪤��˼�뤫
$HbackupTurn = 1;

# �Хå����åפ򲿲�ʬ�Ĥ���
$HbackupTimes = 4;

# ȯ�����ݻ��Կ�
$HhistoryMax = 10;

# ŷ�����ݻ��Կ�(�Կ��λ��ꤷ������ޤ���)
$HWeatherMax = 400;

# �������ޥ�ɼ�ư���ϥ������
$HgiveupTurn = 28;

# write open �� retry ���
$HretryCount = 5;

#----------------------------------------
# �����԰��ɻߴط�
#----------------------------------------

# �ۥ���̾�����⡼��(�ۥ���̾�ϸ��߻��Ѥ��Ƥ��ޤ���)
#  --> 0 : $ENV{'REMOTE_HOST'} �Ǽ����Ǥ�����
#  --> 1 : gethostbyaddr �Ǽ����Ǥ�����
$get_remotehost = 1;

# COOKIE�ˤ��ID�����å��򤹤뤫��(0:���ʤ���1:����)
# �֤���פˤ���ȡ�Ʊ��Уä�ʣ�����������������COOKIE�������ʤ�����̤���γ�ȯ���̤�����ʤ��ʤ�ޤ���
# �ʰ׽�ʣ�к��ʤ櫓�Ǥ������礴�Ȥ˥֥饦�����Ѥ��뤳�ȤǤ����ˤ�֤����㤤�ޤ�(/_<��)
$checkID = 0;

# COOKIE�ˤ��ֲ����Υ���������פ�����å����롩(0:���ʤ���1:����)
$checkImg = 0;

# COOKIE�����å��ʾ�Σ��Ĥ�����ˤ��Ƚ��������ID
# �㡧@freepass = (2, 7, 12);
@freepass = ();

# ������������Ȥ뤫��(0:�Ȥ�ʤ���1:��ȯ���̤�������Ȼ񸻼������2:�ȥåץڡ���)
$HtopAxes = 1;
# 1�ˤ�����硢�ʲ�������
# ���ե�����̾
$HaxesLogfile = './axes.cgi';
# ���絭Ͽ���
$HaxesMax = 500;

# ¾�ͤ�����򸫤��ʤ����뤫
# 0 �����ʤ�
# 1 ������
# 2 100�ΰ̤ǻͼθ���
$HhideMoneyMode = 2;

# �ѥ���ɤΰŹ沽(0���ȰŹ沽���ʤ���1���ȰŹ沽����)
$cryptOn = 1;

#----------------------------------------
# �Ѹ����̿�(������Ǽ���)
#----------------------------------------

# ���Ѥ��뤫�ɤ���(0:���Ѥ��ʤ���1:���Ѥ���)
$HuseLbbs = 1;

# IPɽ��
# 1�ΤȤ��ϥ�����Ǽ��ǡ������������IP��ɽ�����롣�ޥ���������硢�Ѹ��Ԥ⺹��̵��ɽ��
$Hlipdisp = 0;

# ������Ǽ��ǤΥѥ����ǧ��
# ¾����Υ����ʡ����񤭹���Ȥ��˥ѥ���ɳ�ǧ��̵ͭ(0:̵��1:ͭ)
$HlbbsAuth = 1;

# ������Ǽ��Ǥ�ѥ����ǧ�ڤ����������
# ƿ̾ȯ��(�Ѹ�������)����Ĥ��뤫(0:�ػߡ�1:����)
$HlbbsAnon = 0;

# ������Ǽ��Ǥ�ѥ����ǧ�ڤ����������
# ȯ����ȯ���Ԥ�̾����ɽ�����뤫(0:ɽ�����ʤ���1:ɽ������)
$HlbbsSpeaker = 1;

# ���ϥ����ܲ����뤫��(0:���ʤ� 1:��ɸ���� 2:��ɸ�ʤ�)
$HlogOmit2 = 1;

#----------------------------------------
# ��⡢�����ʤɤ������ͤ�ñ��
#----------------------------------------
# ������
$MaxMoney = 99999;

# ���翩������
$MaxFood = 99999;

# �����(���������С�ʼ��)����
$MaxSigen = 9999;

# �����ñ��
$HunitMoney = '����';

# ������ñ��
$HunitFood = '00�ȥ�';

# ���Ф�ñ��
$HunitOre = '�ȥ�';

# ������ñ��
$HunitOil = '���Х��';

# ʼ���ñ��
$HunitWeapon = '���ȥ�';

# �͸���ñ��
$HunitPop = '00��';

# ������ñ��
$HunitArea = '00����';

# �ڤο���ñ��
$HunitTree = '00��';

# �ڤ�ñ�������������
$HtreeValue = 5;

# ̾���ѹ��Υ�����
$HcostChangeName = 0;

# �͸�1ñ�̤�����ο���������
$HeatenFood = 0.2;

# ���蹩�졢��������ϡ�����͸��β��ܤε���ʬ����Ư���뤫��
$HspaceEfficiency = 5; # ����

# ���蹩�졢��������β�Ư���Ƥ�����͵��Ϥ�������Ͼ����(��)
$HspaceIncome = 5;

#----------------------------------------
# �����ط�
#----------------------------------------

# <BODY>�����Υ��ץ����
$htmlBody = 'BGCOLOR="#EEFFFF"';
# �طʲ�������ꤹ���硣������Ȣ��β����ե���������֤��Ƥ�����������������ꤷ�Ƥ�����ϲ������դ��Ƥ���������
#$htmlBody = 'BGCOLOR="#EEFFFF" BACKGROUND="kabe.gif"';

$htmlBgColor = 'BGCOLOR="#EEFFFF"';

# ������Υ����ȥ�ʸ�� ��ͳ���ѹ����ƹ����ޤ���
$Htitle = '���ۤ�Ȣ��';
$Htitle2 = $versionInfo;

# ����
# �����ȥ�ʸ��
$HtagTitle_ = '<span class="title">';
$HtagTitle2_= '<span class="title2">';
$H_tagTitle = '</span>';

# �礭��ʸ��
$HtagBig_ = '<span class="big">';
$H_tagBig = '</span>';

# ���̾���ʤ�
$HtagName_ = '<span class="islName">';
$H_tagName = '</span>';

# �����ʤä����̾��
$HtagName2_ = '<span class="islName2">';
$H_tagName2 = '</span>';

# ��̤��ֹ�ʤ�
$HtagNumber_ = '<span class="number">';
$H_tagNumber = '</span>';

# ���ɽ�ˤ����븫����
$HtagTH_ = '<span class="head">';
$H_tagTH = '</span>';

# ��ȯ�ײ��̾��
$HtagComName_ = '<span class="command">';
$H_tagComName = '</span>';

# �ҳ�
$HtagDisaster_ = '<span class="disaster">';
$H_tagDisaster = '</span>';

# ������Ǽ��ġ��Ѹ��Ԥν񤤤�ʸ��
$HtagLbbsSS_ = '<span class="lbbsSS">';
$H_tagLbbsSS = '</span>';

# ������Ǽ��ġ����ν񤤤�ʸ��
$HtagLbbsOW_ = '<span class="lbbsOW">';
$H_tagLbbsOW = '</span>';

# �̾��ʸ����
$HnormalColor_ = '<span class="normal">';
$H_normalColor = '</span>';

# ���ɽ�������°��
$HbgTitleCell	= 'class=TitleCell';	# ���ɽ���Ф�
$HbgSubTCell	= 'class=SubTCell';		# ���ɽ���ָ��Ф�
$HbgNumberCell	= 'class=NumberCell';	# ���ɽ���
$HbgNameCell	= 'class=NameCell';		# ���ɽ���̾��
$HbgInfoCell	= 'class=InfoCell';		# ���ɽ��ξ���
$HbgCommentCell	= 'class=CommentCell';	# ���ɽ��������
$HbgInputCell	= 'class=InputCell';	# ��ȯ�ײ�ե�����
$HbgMapCell		= 'class=MapCell';		# ��ȯ�ײ��Ͽ�
$HbgCommandCell	= 'class=CommandCell';	# ��ȯ�ײ����ϺѤ߷ײ�
$HbgLbbsCell	= 'class=LbbsCell';		# �Ѹ����̿�ɽ����

#----------------------------------------
# ���Ϥηи���
#----------------------------------------

# �и��ͤκ�����
$HmaxExpPoint = 250;

# ��٥�κ�����
$maxBaseLevel = 6;  # �ߥ��������
$maxSBaseLevel = 4; # �������

# �и��ͤ������Ĥǥ�٥륢�åפ�
@baseLevelUp = (20, 60, 120, 200, 250); # �ߥ��������
@sBaseLevelUp = (50, 200, 250);         # �������

if($HwarFlg){
	$maxBaseLevel  = 9;
	$maxSBaseLevel = 6;
	@baseLevelUp  = (10, 30, 50, 70, 100, 150, 200, 250);
	@sBaseLevelUp = (20, 60, 120, 200, 250);
}

# �ɱһ��ߤμ��� �����ɱһ��ߤ�ޤޤ��
# ���ä�Ƨ�ޤ줿����������ʤ�1�����ʤ��ʤ�0
$HdBaseAuto = 1;

#----------------------------------------
# �ҳ�
#----------------------------------------
# �ҳ�Ⱦ������Ƴ�����뤫��������2(TOP��Ⱦ�����ɽ��) ����1 ���ʤ�0
# ɴ�ΰ̤������λ����ҳ�Ψ����Ⱦ�����ޤ���
$Hdishangen = 0;

# �̾�ҳ�ȯ��Ψ(��Ψ��0.1%ñ��)
$HdisEarthquake = 5;  # �Ͽ�
$HdisTsunami    = 15; # ����
$HdisTyphoon    = 20; # ����
$HdisMeteo      = 15; # ���
$HdisHugeMeteo  = 4;  # �������
$HdisEruption   = 10; # ʮ��
$HdisFire       = 10; # �к�
$HdisMaizo      = 10; # ��¢��
$HdisAkasio     = 30; # ��Ĭ
$HdisVGHarvest  = 10; # ��˭��
$HdisGHarvest   = 50; # ˭��
$HdisBHarvest   = 40; # ����
$HdisAEruption  = 4;  # ��ʮ��

$HdisPirate     = 20; # ��±��
$HdisTreasureS  = 1;  # ����

$HdisTinka      = 9; # �����ˤ����������(0.01%ñ��)

# �����(�������η�¤ʪ����)�³���(%)������ʾ�������ȥ������Τ餬�Фޤ���
$HdisKLimit = 50;

# �͸��������������ȯ��Ψ
$HdisPollution    = 1;  # ����(0.01%ñ��)
$HmaxdisPollution = 24; # ��������(0.1%ñ��)
$HdisCrime        = 10; # �Ⱥ�(0.01%ñ��)(�͸��ʳ������Ǥ⤢��ޤ�)

# ��������
$HdisFallBorder = 90; # �����³��ι���(Hex��)
$HdisFalldown   = 30; # ���ι�����Ķ�������γ�Ψ

# ���蹩�죱�Ĥ�����˵�����Ф�ȯ�������Ψ(0.0001%ñ��)
$HdisSHugeMeteo = 25; # �߳�ȯ����

# ŷ��
@WeatherName = ('����','����','�ޤ�','ǻ̸','��','�籫');
@WeatherIcon = ('weather/kaisei.gif','weather/hare.gif','weather/kumori.gif','weather/noumu.gif','weather/ame.gif','weather/ooame.gif');

#�����ȤΥ�٥���� (4̤���ѡ��ɲäˤ�hako-main.cgi�β�¤��ɬ��)by ShibaAni
@HlabelName = ('���ýи����˥ߥ����������ݤ���<>���ýи����˥ߥ����������Ĥ���','���åХȥ�Ǥα������������','������Ǥ��ޤ�','�����������ߤ���','ͽ��1');
@HlabelImage = ('label00_2.gif<>label00_1.gif','label01.gif','label02.gif','label03.gif','label04.gif');

# ����
$HdisMonsBorder1 = 1000; # �͸����1(���å�٥�1)
$HdisMonsBorder2 = 2500; # �͸����2(���å�٥�2)
$HdisMonsBorder3 = 4000; # �͸����3(���å�٥�3)
$HdisMonsBorder4 = 6000; # �͸����4(���å�٥�4)
$HdisMonsBorder5 = 8000; # �͸����5(���å�٥�5)
$HdisMonster     = 2.6;  # ñ�����Ѥ�����νи�Ψ(0.01%ñ��)

# ñ�����Ѥ���������Ω�Ƥ��Τ顢�������νи��͡ʾ��ʤ��ۤɳ�Ψ���⤤�����Х��Х�⡼�ɡ�$HdisMonster=0�ξ����ͤ˴ط��ʤ��и����ʤ���
$HdisMonsterU    = 20000;

# ����Ǥβ��äνи��͡ʾ��ʤ��ۤɳ�Ψ���⤤��$HdisMonster=0�ξ����ͤ˴ط��ʤ��и����ʤ�)
# ��ȯ���� �� $HdisSpaceMonster �� 100 = �и�Ψ(%)��(�西���󤳤γ�Ψ��Į�Ϥο�����Ƚ��)
$HdisSpaceMonster1 = 30000; # ����ͭ��
$HdisSpaceMonster2 = 10000; # ����̵��

# ����Ǥβ��äνи��͡ʾ��ʤ��ۤɳ�Ψ���⤤��$HdisMonster=0�ξ����ͤ˴ط��ʤ��и����ʤ�)
# 1 �� $HdisSeaMonster �� 100 = �и�Ψ(%)��(�西���󤳤γ�Ψ�ǳ��ο�����Ƚ��)
$HdisSeaMonster = 8000;

# ����
$HmonsterNumber  = 36; 

# �ƴ��ˤ����ƽФƤ�����ÿ��ȼ���
$HmonsterL1Num = 2;
$HmonsterL2Num = 5;
$HmonsterL3Num = 7;
$HmonsterL4Num = 11;
$HmonsterL5Num = 12;
@HmonsterL1 = (1,2);
@HmonsterL2 = (1,2,3,4,5);
@HmonsterL3 = (1,2,3,4,5,6,7);
@HmonsterL4 = (1,3,4,5,6,7,8, 9,10,24,26);
@HmonsterL5 = (3,4,5,6,7,8,9,10,19,24,26,27);
# �������
@HmonsterS = (32,33,34,35);

# �������ϡ����Ϥ������ü�ǽ�ϡ��Ӥ餷������Ϸ����и��͡����Τ�����
                   # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35
@HmonsterBHP     = ( 2, 1, 1, 3, 2, 1, 4, 5, 2, 3, 6, 2, 2, 1, 2, 2, 2, 2, 5, 8, 5, 3, 2, 2, 2, 1, 3, 6, 2, 2, 5, 1, 2, 4, 2, 6);
@HmonsterDHP     = ( 3, 2, 2, 2, 2, 0, 2, 2, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 3, 4, 2, 2, 0, 3, 2, 2, 2, 3);
@HmonsterSpecial = ( 2, 0, 3, 0, 1, 2, 4, 0, 2, 0, 1, 5, 5, 6, 7, 2, 0, 0, 8, 0, 7, 7, 8, 0, 0, 5, 2, 0, 0, 0, 9, 5, 0, 1, 2, 0);
@HmonsterDestroy = ( 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,15, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0);
@HmonsterExp     = (10, 5,7,12,15,10,20,30,100,35,50,10,20,15,40,15,15,20,80,70,60,40,12,20,90,10,30,10,10,10,60,10,15,20,25,40);
                   # 0    1    2    3    4    5    6    7    8    9
@HmonsterValue   = (  0, 400, 500,1000, 800, 300,1500,2000,1000,2000,
                   3000, 100,3000,1000,2000,1000,1200,1500,6000,4000,
                   3500,2000, 200,4000, 300, 100,2000, 500,1000,1000,
                   5000,9999,2000,3000,3500,5000);

# �ü�ǽ�Ϥ����Ƥϡ�
# 0 �äˤʤ�
# 1 ­��®��(����2�⤢�뤯)
# 2 ­���ȤƤ�®��(���粿�⤢�뤯������)
# 3 ���������ϹŲ�
# 4 ����������ϹŲ�
# 5 ��˹Ų�����������Ǥ�����
# 6 ̿����������˰�ư(0-1��)
# 7 ̿����������˰�ư(���粿�⤢�뤯������)
# 8 ���ϣ��إ�����̸��Ф�
# 9 ����������西����MAX��

# ̾��(������ѹ�����ȥ�󥭥󥰤����������ʤ�ޤ�)
@HmonsterName = 
    (
     '�ᥫ���Τ�',     # 0(��¤)
     '���Τ�',         # 1
     '���󥸥�',       # 2
     '��åɤ��Τ�',   # 3
     '���������Τ�',   # 4
     '���Τ饴������', # 5
     '������',         # 6
     '���󥰤��Τ�',   # 7
     '�᥿�뤤�Τ�',   # 8
     '�������Τ�',     # 9
     '�ǥӥ뤤�Τ�',   # 10
     '�ᥫ����',       # 11(��¤)
 '���󥷥���Ȥ��Τ�', # 12(�ϼ�Ĵ��)
     '�����ƥ�',       # 13(����)
     '��ԥåȤ��Τ�', # 14(����)
     '���Х��쥤',     # 15(�������Ȥ��Ѳ�)
     '���Ω�Ƥ��Τ�', # 16(���˥�����)
     '������ܥ���',   # 17(�ߥ������)
     'ȿ�⤤�Τ�',     # 18(�ߥ������)
     '�������',       # 19(�ߥ������)
     '���ڡ������Τ�', # 20(�ߥ������)
     '������������',   # 21(�ߥ������)
    '����ƥͥ����Τ�',# 22(��¤)
     '���ͥ���',       # 23
     '��å����Τ�',   # 24
     '����ᥫ���Τ�', # 25
     '�º̤��Τ�',     # 26
     'ʬ�����Τ�',     # 27
     '�Ƥ�Ƥ뤤�Τ�', # 28
     '�դ��Ƥ�Ƥ�',   # 29
     '�������Τ�',     # 30
    '������ɥ�������',# 31
     '�������(��)',   # 32
     '�������(��)',   # 33
     '�������(��)',   # 34
     '�������(��)'    # 35
);

# ���åХȥ���
@HmonsterSP      = ( 7, 4, 1, 7, 7, 3, 2, 7, 6, 0,10, 6, 6, 5, 5, 5, 0, 8, 7, 0, 9, 5, 0, 8, 0, 6, 5, 5, 0, 0,11, 8, 0, 7, 7, 9); # �ü�
                   # 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35
@HmonsterSTR     = (10, 7, 7,10, 7, 2, 8,12, 4, 7,13, 3,11, 5, 7, 3, 8,12,15, 9, 9, 9, 7, 5,10,10, 7, 7, 7, 9,11,11, 7, 9,11,11); # ����
@HmonsterDEF     = ( 2, 3, 5, 2, 2, 0, 5, 3, 7, 3, 1, 5, 5, 0, 0, 0, 3, 5, 0, 3, 3, 1, 3, 2, 3, 5, 1, 1, 3, 3, 3, 5, 3, 3, 3, 3); # �ɸ�
@HmonsterAGI     = ( 6, 5, 2, 3, 9,14, 4, 5,11, 5, 5, 1, 2,15,17,19, 6,11, 5, 9,15,20, 5,10,10, 7,15,20, 5, 6, 9,15, 5, 6, 6,14); # ����
@HmonsterSKL     = ( 2, 7, 6, 5, 9, 9, 7, 4, 7, 7,10, 1, 5,10,13,13, 8,12,12, 9,10,16, 7,10,10, 7,12,10, 7, 7, 9,12, 7, 7, 8,12); # ̿��
       #  ��(����)  20 22 20 20 27 25 24 24 29 22 29 10 23 30 37 35 25 40 32 30 37 46 22 27 33 29 35 38 22 25 32 43 22 25 28 40

# ���åХȥ�ʲ���
@HmonsterGRP     = ( 0, 0, 1, 3, 2, 2, 1, 3, 1, 4, 3, 1, 1, 2, 2, 2, 4, 5, 3, 4, 4, 2, 5, 5, 5, 5, 4, 5, 3, 3, 4, 1, 6, 6, 6, 6); # ���롼��
@HmonsterCLS     = ( 0, 0, 1, 3, 1, 2, 2, 4, 4, 1, 5, 3, 5, 3, 4, 2, 2, 6, 6, 3, 6, 5, 1, 5, 2, 3, 4, 4, 1, 2, 5, 6, 1, 2, 3, 4); # ����
@HmonsterSEI     = ( 0, 1, 4, 2, 4, 5, 4, 2, 4, 4, 4, 2, 1, 5, 5, 5, 4, 3, 3, 0, 5, 3, 4, 5, 4, 4, 5, 5, 2, 2, 4, 1, 2, 4, 3, 5); # ��Ĺ

# ��Ĺ
# 0 ����
# 1 ��ĹΨ���⤤
# 2 ��ĹΨ���㤤
# 3 ����ο��Ӥ�����
# 4 �������夬��
# 5 ����̿��ο��Ӥ�����

# �����ե�����
@HmonsterImage =
    (
     'monster7.gif',
     'monster0.gif',
     'monster5.gif', # 2
     'monster1.gif',
     'monster2.gif',
     'monster8.gif',
     'monster6.gif', # 6
     'monster3.gif',
     'monster9.gif',
     'monster10.gif',
     'monster11.gif', # 10
     'monster12.gif',
     'monster13.gif',
     'monster14.gif',
     'monster15.gif', # 14
     'monster16.gif',
     'monster17.gif',
     'monster18.gif',
     'monster19.gif', # 18
     'monster20.gif',
     'monster21.gif',
     'monster22.gif',
     'monster23.gif', # 22
     'monster24.gif',
     'monster25.gif',
     'monster26.gif',
     'land1.gif',     # ����
     'monster27.gif',
     'monster28.gif',
     'monster29.gif',
     'monster30.gif', # 30
     'monster31.gif',
     'cmonster1.gif',
     'cmonster2.gif',
     'cmonster3.gif', # 34
     'cmonster4.gif'
     );

# �����ե����뤽��2(�Ų���)
@HmonsterImage2 =
  ('','','monster4.gif','','','','monster4.gif','','','','','','','','','','','','','','','','','','','','','','','','','','','','','');
 # 0  1         2       3  4  5        6        7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35

#----------------------------------------
# ����
#----------------------------------------
# ���Ĥμ���(��)
$HoilMoney = 400;

# ���Ĥθϳ��Ψ
$HoilRatio = 40;

#----------------------------------------
# ��ǰ��
#----------------------------------------
# �����ढ�뤫
$HmonumentNumber = 19;

# �̾�ߥ��������̤ʤ��ˤ����磱
$HmonumentMissile = 1;

# ���åȳ��ϰ���
$HmonumentRocket = 11;

# ̾��
@HmonumentName = 
    (
     '��Υꥹ',   #0
     'ʿ�µ�ǰ��',
     '�襤����',
     '������ǰ��',
     'ͽ����ǰ��',
     'ͽ����ǰ��', #5
     'ͽ����ǰ��',
     'ͽ����ǰ��',
     '�ҳ�����',
     '������',
     '���õ�ǰ��', #10
     '���åȵ�ǰ��',
     '���å���(LV1)',
     '���å���(LV2)',
     '���å���(LV3)',
     '���å���(LV4)', #15
     '���å���(LV5)',
     '���å���(LV6)',
     '���å���(LV7)'
    );

# �����ե�����
@HmonumentImage = 
    (
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monument0.gif',
     'monumentP.gif',
     'monumentG.gif',
     'monumentM.gif',
     'monument3.gif',
     'monument4.gif',
     'monument4.gif',
     'monument4.gif',
     'monument4.gif',
     'monument4.gif',
     'monument4.gif',
     'monument4.gif'
     );

#----------------------------------------
# ���쵭ǰ��
#----------------------------------------
# �����ढ�뤫
$HsmonumentNumber = 2;

# ̾��
@HsmonumentName = 
    (
     '���쵭ǰ��',
     '���쵭ǰ��'
    );

# �����ե�����
@HsmonumentImage = 
    (
     'smonument0.gif',
     'smonument1.gif'
     );

#----------------------------------------
# �޴ط�
#----------------------------------------
# �������դ򲿥�������˽Ф���
$HturnPrizeUnit = 100;

# �ޤ�̾��
@Hprize = ('��������','�˱ɾ�','Ķ�˱ɾ�','����˱ɾ�','ʿ�¾�',
			'Ķʿ�¾�','���ʿ�¾�','�����','Ķ�����','��˺����',
			'�����','���ۤ��Τ��');

# ����ޤ򲿥�������˽Ф���
$HturnPrizeVarious = 20;

# ����ޤβû������
$HturnPrizePoint = 50;

# ����ޤο�
$HturnPrizeNumber = 14;

# �ޤ�̾��
@HprizeV = ('','���Ȳ�','���Ȳ�','���Ȳ�','�建��',
			'���Ӳ�','�ߥ����벦','�ϥ�ܥƲ�','���ò�','������',
			'�ҳ���','������','��ǰ�겦','���貦','��ݲ�');

#----------------------------------------------------------------------
# ���ߤˤ�ä����ꤹ����ʬ�ϰʾ�
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# ����ʹߤΥ�����ץȤϡ��ѹ�����뤳�Ȥ����ꤷ�Ƥ��ޤ��󤬡�
# �����äƤ⤫�ޤ��ޤ���
# ���ޥ�ɤ�̾�������ʤʤɤϲ��䤹���Ȼפ��ޤ���
#----------------------------------------------------------------------

#----------------------------------------
# ����
#----------------------------------------
#              ± �� �� õ �� �� �� �� �� �� �� ε ή �� �� ��
@HshipHP    = ( 3, 2, 4, 2, 3, 3, 1, 1, 1, 2, 3, 4, 1, 2, 2, 6); # HP
@HshipKAI   = ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0); # ����
@HshipSP    = ( 1, 0, 1, 1, 0, 1, 2, 2, 0, 0, 0, 2, 0, 0, 0, 1); # ®��(���ä�Ʊ��)
@HshipMATK  = ( 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0); # �в�������
@HshipSATK  = ( 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); # �дϹ�����
@HshipEX    = (10, 5,12, 4,40,35,20,30, 2, 4, 6,60,10,10, 5, 5); # �и���
@HshipMoney = ( 0,50,50,100,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); # �ݻ���
@HshipFood  = ( 0, 0, 0,100,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); # �ݻ�����
@HshipMoneyE= ( 0,50,50,100,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); # �ݻ������
@HshipFoodE = ( 0, 0, 0,100,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); # �ݻ���������

@HshipSell =(2000, 800,1500, 600,4000,
			 2000,1000,9999, 300, 700,
			 1200,1000,2000,2000,1200,1000);

# ����
@Hshiporder = ('�ü�','��ư','�ɸ�','ű��','����');

# ̾��
@HshipName = ('��±��','������Ƥ��','����������','����õ����', 'ͽ��',
			'ͽ��','ͩ����','����','��������','�淿����',
			'�緿����','��ε','ήɹ','���ش�','��ڵ���',
			'������');

# �����ե�����
@HshipImage = ( 'ship01.gif','ship02.gif','ship03.gif','ship04.gif','ship05.gif',
				'ship06.gif','land0.gif','ship08.gif','ship09.gif','ship10.gif',
				'ship11.gif','ship12.gif','ship13.gif','ship14.gif','ship15.gif',
				'ship16');

# �����Ϸ����ɤ��������å�����(-1�к��ǺǸ��0�ˤ��뤳��)
# 1�ʾ峤�ϡ�2����3������
#           0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9
@HseaChk = (1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0, # 19
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, # 39
			0,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0, # 59
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, # 79
			0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, # 99
			0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2, #119
			2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0);#139

#----------------------------------------
# �ϲ���
#----------------------------------------

@Hunderground = ('�ϲ�����','�ϲ��и�','�ϲ�����','�ϲ�','�ϲ��Ի�',
				'�ϲ�����','�ϲ�����','�ϲ��ߥ��������','�ϲ�������������');

@HugImage = ('ug.gif','ug_dokan.gif','ug_hasigo.gif','ug_road.gif','ug_tosi.gif',
			'ug_farm.gif','ug_fact.gif','ug_kiti.gif','ug_oil.gif');

$HugSpace  = 0;
$HugDokan  = 1;
$HugHasigo = 2;
$HugRoad   = 3;
$HugTosi   = 4;
$HugFarm   = 5;
$HugFact   = 6;
$HugKiti   = 7;
$HugOil    = 8;

#----------------------------------------
# �ٻλ�
#----------------------------------------
@HfujiImage = ('fuji/fuji1.gif','fuji/fuji2.gif','fuji/fuji3.gif');

#----------------------------------------
# �������
#----------------------------------------
@HsEisei      = ('���ݱ���','��¬����','�޷����','��������','�ɱұ���');
@HsEiseiImage = ('cosmo20.gif','cosmo21.gif','cosmo22.gif','cosmo23.gif','cosmo24.gif');

#----------------------------------------
# ����4�إå����κ�ɸ 0-60
#----------------------------------------

@ax = (0, 1, 1, 1, 0,-1, 0, 1, 2, 2, 2, 1, 0,-1,-1,-2,-1,-1, 0,
		2, 2, 3, 3, 3, 2, 2, 1, 0,-1,-2,-2,-3,-2,-2,-1, 0, 1,
		2,3,3,4,4,4,3,3,2,1,0,-1,-2,-2,-3,-3,-4,-3,-3,-2,-2,-1,0,1);
@ay = (0,-1, 0, 1, 1, 0,-1,-2,-1, 0, 1, 2, 2, 2, 1, 0,-1,-2,-2,
		-3,-2,-1, 0, 1, 2, 3, 3, 3, 3, 2, 1, 0,-1,-2,-3,-3,-3,
		-4,-3,-2,-1,0,1,2,3,4,4,4,4,4,3,2,1,0,-1,-2,-3,-4,-4,-4,-4);

#----------------------------------------------------------------------
# �Ƽ����
#----------------------------------------------------------------------
# �Ϸ��ֹ�
$HlandSea      = 0;  # ��
$HlandWaste    = 1;  # ����
$HlandPlains   = 2;  # ʿ��
$HlandTown     = 3;  # Į��
$HlandForest   = 4;  # ��
$HlandFarm     = 5;  # ����
$HlandFactory  = 6;  # ����
$HlandBase     = 7;  # �ߥ��������
$HlandDefence  = 8;  # �ɱһ���
$HlandMountain = 9;  # ��
$HlandMonster  = 10; # ����
$HlandSbase    = 11; # �������
$HlandOil      = 12; # ��������
$HlandMonument = 13; # ��ǰ��
$HlandHaribote = 14; # �ϥ�ܥ�
$HlandOsen     = 15; # ����
$HlandSlum     = 16; # ����೹
$HlandTower    = 17; # ���ȥӥ�
$HlandSeisei   = 18; # ������
$HlandBank     = 19; # ���
$HlandStadium  = 20; # ����������
$HlandAmusement = 21; # ͷ����
$HlandCasino    = 22; # ������
$HlandPark      = 23; # ����
$HlandSchool    = 24; # �ع�
$HlandDome      = 25; # �ɡ���
$HlandAirport   = 26; # ����
$HlandFire      = 27; # ���ɽ�
$HlandWarp      = 28; # ž������
$HlandZoo       = 29; # ưʪ��
$HlandBigcity   = 30; # ���Ի�
$HlandExpo      = 31; # ������
$HlandMegacity  = 32; # �����Ի�
$HlandMegatower = 33; # ����ӥ�
$HlandMegaFact  = 34; # ���繩��
$HlandDeathtrap = 35; # �ǥ��ȥ�å�
$HlandWindmill  = 36; # ����
$HlandMyhome    = 37; # �ޥ��ۡ���
$HlandWarpR     = 38; # ž��������
$HlandPort      = 39; # ��
$HlandPolice    = 40; # �ٻ���
$HlandKInora    = 41; # ���ۤ��Τ�
$HlandTrump     = 42; # �ȥ���
$HlandFlower    = 43; # ��
$HlandDokan     = 44; # �ڴ�
$HlandFuji      = 45; # �ٻλ�
$HlandTcity     = 46; # �����Ի�
$HlandMegaFarm  = 47; # ��������
$HlandHugecity  = 48; # Ķ�����Ի�
$HlandBreakwater= 49; # ������
$HlandSMonument = 50; # ���쵭ǰ��
$HlandHospital  = 51; # �±�

# ������
$HlandOcean     = 71; # ̵����(�ѹ�������hako-mente.cgi��)
$HlandOPlayer   = 72; # �ץ쥤�䡼��
$HlandOmonster  = 73; # ��󥹥���(̤����)

# ����
$HlandPirate    = 101; # ��±��

$HlandMonsShip  = 102; # ������Ƥ��
$HlandAegisShip = 103; # ����������
$HlandProbeShip = 104; # ����õ����

$HlandGhostShip = 107; # ͩ����
$HlandTreasureS = 108; # ����
$HlandFishSShip = 109; # ��������
$HlandFishMShip = 110; # �淿����
$HlandFishLShip = 111; # �緿����
$HlandWingDragon= 112; # ��ε
$HlandIceFloe   = 113; # ήɹ
$HlandCoupleRock= 114; # ���ش�
$HlandTitanic   = 115; # ��ڵ���
$HlandBalloonS  = 116; # ������

# ������
$HlandEarth = 201; # �ϵ�
$HlandSunit = 202; # �����˥å�
$HlandSCity = 203; # �����Ի�

$HlandSFarm    = 205; # ��������
$HlandSFactory = 206; # ���蹩��
$HlandSpaceBase= 207; # ����ߥ��������
$HlandSDefence = 208; # �����ɱһ���

$HlandSAEisei  = 210; # �������

# ���ޥ��
# �ߥ�����Ȱ��˽����Τ�0-19��90-
@HcommandDivido = 
	(
	'��ȯ,0,17',
	'����,18,49',
	'�ߥ�����,50,65',
	'����,66,89',
	'����,90,109',
	'����,110,119',
	'����,120,139',
	'����,140,149'
	);
# ��ա����ڡ���������ʤ��褦��
# ����	'��ȯ,0,10',  # �ײ��ֹ�00��10
# �ߢ�	'��ȯ, 0  ,10  ',  # �ײ��ֹ�00��10

# �ײ��ֹ������
# ���Ϸ� 9
$HcomPrepare  = 1; # ����
$HcomPrepare2 = 2; # �Ϥʤ餷
$HcomReclaim  = 3; # ���Ω��
$HcomReclaim2 = 4; # ��®���Ω��
$HcomDestroy  = 5; # ����
$HcomSellTree = 6; # Ȳ��
$HcomSearch   = 7; # �ϼ�Ĵ��
$HcomPioneer  = 8; # ����
$HcomDestroy2 = 9; # ��®����

# ���� 29
$HcomPlant    = 11; # ����
$HcomFarm     = 12; # ��������
$HcomFactory  = 13; # �������
$HcomMountain = 14; # �η�������
$HcomBank     = 15; # ���
$HcomPresent  = 16; # �ץ쥼��ȷ���

$HcomShipbuild	= 18; # ¤��
$HcomSMonument	= 20; # ���쵭ǰ���¤
$HcomBase		= 21; # �ߥ�������Ϸ���
$HcomDbase		= 22; # �ɱһ��߷���
$HcomSbase		= 23; # ������Ϸ���
$HcomMonument	= 24; # ��ǰ���¤

$HcomHaribote	= 25; # �ϥ�ܥ�����
$HcomScity		= 26; # �����ԻԷ���
$HcomSFarm		= 27; # ������������
$HcomTower		= 28; # ���ȥӥ�����
$HcomFire		= 29; # ���ɽ�
$HcomWarp		= 30; # ž�����ֺ���
$HcomWindmill	= 31; # ���ֺ���
$HcomMyhome		= 32; # �ޥ��ۡ������
$HcomDeathtrap	= 33; # �ǥ��ȥ�å׺���
$HcomPort		= 34; # ������
$HcomPolice		= 35; # �ٻ������
$HcomTrump		= 36; # �ȥ�������
$HcomFlower		= 37; # �֤򿢤���
$HcomBreakwater	= 38; # ����������
$HcomHospital	= 39; # �±�����

$HcomDokan		= 45; # �ڴ�(�ϲ�)����
$HcomUg			= 46; # �ϲ�����

# ����� 24
$HcomMissileNM	= 50; # �ߥ�����ȯ��
$HcomMissilePP	= 51; # PP�ߥ�����ȯ��
$HcomMissileSPP	= 52; # SPP�ߥ�����ȯ��
$HcomMissileDM	= 53; # �Ȼ���ȯ��
$HcomMissileST	= 54; # ST�ߥ�����ȯ��
$HcomMissileLD	= 55; # Φ���˲���ȯ��
$HcomMissilePLD	= 56; # �˲�PP��ȯ��
$HcomMissileRM	= 57; # ���Ω����ȯ��
$HcomMissileSRM	= 58; # S���Ω����ȯ��
$HcomBioMissile	= 59; # �Х����ߥ�����
$HcomMissileNCM	= 60; # �˥ߥ�����ȯ��
$HcomMissileMGM	= 61; # ����ͶƳ��ȯ��
$HcomMissileGM	= 62; # ͶƳ��ȯ��
$HcomMissileRNG	= 63; # ��󥰥ߥ�����ȯ��


$Hcomcolony			= 69; # ����ˡ��
$HcomSendMonster	= 70; # �����ɸ�
$HcomManipulate		= 71; # �������
$HcomSTManipulate	= 72; # ST�������
$HcomSpy			= 73; # �����
$HcomTeisatu		= 74; # �廡
$HcomDummy			= 75; # ���ߡ�̿��
$HcomSSendMonster	= 76; # S�����ɸ�
$HcomShip			= 80; # �������ѹ�
$HcomShipM			= 81; # ���������

# ���ķ� 15
$HcomShipSell	= 92; # �����
$HcomSell		= 93; # �������
$HcomMoney		= 94; # �����
$HcomFood		= 95; # �������
$HcomPropaganda	= 96; # Ͷ�׳�ư
$HcomDoNothing	= 97; # ��ⷫ��
$HcomPresentAid	= 98; # �ץ쥼��Ⱦ���
$HcomEmigration	= 99; # ��̱
$HcomGiveup		= 100; # �������
$HcomOreSell	= 101; # �������(���)
$HcomOilSell	= 102; # �������(���)
$HcomWeponSell	= 103; # ʼ�����(���)
$HcomOreBuy		= 104; # ���й���
$HcomOilBuy		= 105; # ��������
$HcomWeponBuy	= 106; # ʼ�����

# ���åХȥ�� 8 (���ƥ�����Ϥ�����ޤ���)
$HcomMonsEgg	= 110; # ���å��å�����
$HcomMonsEsa	= 111; # ���ä˱�
$HcomMonsEnsei	= 112; # ���ñ���
$HcomMonsTettai	= 113; # ����ű��
$HcomMonsEsaAid	= 114; # ���ñ¾���
$HcomMonsAid	= 115; # ���þ���
$HcomMonsSell	= 116; # �������
$HcomMonsExer	= 117; # �����ϵ�����

# ���賫ȯ��
$HcomSUnit		= 120; # �����˥åȷ���
$HcomSFood		= 121; # ���迩���Ǿ夲
$HcomSPioneer	= 122; # ��������
$HcomSBuild		= 123; # ������߷�
$HcomSpaceFarm	= 124; # �����������
$HcomSFactory	= 125; # ���蹩�����
$HcomSOccupy	= 126; # ��������
$HcomSMissileGM	= 127; # ����ͶƳ�ߥ�����ȯ��
$HcomSpaceBase	= 128; # ����ߴ��Ϸ���
$HcomSDestroy	= 129; # �����˥å��˲�
$HcomSMissileMGM= 130; # �������ͶƳ
$HcomSMissilePP	= 131; # ����PP�ߥ�����ȯ��
$HcomSMissile	= 132; # ����ߥ�����ȯ��
$HcomSDbase		= 133; # �����ɱһ��߷���
$HcomSEisei		= 134; # �����������

$HcomOMissileNM		= 140; # ����ߥ�����
$HcomOMissilePP		= 141; # ����PP�ߥ�����
$HcomOMissileSPP	= 142; # ����SPP�ߥ�����

# ��ư���Ϸϡ����� 4
$HcomAutoPrepare	= 184; # �ե�����
$HcomAutoPrepare2	= 185; # �ե��Ϥʤ餷
$HcomAutoSellTree	= 186; # �ե�Ȳ��
$HcomAutoDelete		= 188; # �����ޥ�ɾõ�

# �ü�̿��($HcommandTotal�ˤϴޤ�ʤ�����)
$HcomSpecialSPP	= 200;

# �ײ��̾��������
$HcomName[$HcomPrepare]  = '����';
$HcomCost[$HcomPrepare]  = 5;
$HcomName[$HcomPrepare2] = '�Ϥʤ餷';
$HcomCost[$HcomPrepare2] = 100;
$HcomName[$HcomReclaim]  = '���Ω��';
$HcomCost[$HcomReclaim]  = 150;
$HcomName[$HcomReclaim2] = '��®���Ω��';
$HcomCost[$HcomReclaim2] = 800;
$HcomName[$HcomDestroy]  = '����';
$HcomCost[$HcomDestroy]  = 200;
$HcomName[$HcomDestroy2]  = '��®����';
$HcomCost[$HcomDestroy2]  = 800;
$HcomName[$HcomSearch]   = '�ϼ�Ĵ��';
$HcomCost[$HcomSearch]   = 1000;
$HcomName[$HcomSellTree] = 'Ȳ��';
$HcomCost[$HcomSellTree] = 0;
$HcomName[$HcomPlant]    = '����';
$HcomCost[$HcomPlant]    = 50;
$HcomName[$HcomBank]     = '������';
$HcomCost[$HcomBank]     = 1000;
$HcomName[$HcomPioneer]  = '����';
$HcomCost[$HcomPioneer]  = -500;
$HcomName[$HcomFarm]     = '��������';
$HcomCost[$HcomFarm]     = 20;
$HcomName[$HcomFactory]  = '�������';
$HcomCost[$HcomFactory]  = 100;
$HcomName[$HcomMountain] = '�η�������';
$HcomCost[$HcomMountain] = 300;
$HcomName[$HcomPresent]  = '�ץ쥼��ȷ���';
$HcomCost[$HcomPresent]  = 0;
$HcomName[$HcomPresentAid] = '�ץ쥼��Ⱦ���';
$HcomCost[$HcomPresentAid] = 0;
$HcomName[$HcomBase]     = '�ߥ�������Ϸ���';
$HcomCost[$HcomBase]     = 300;
$HcomName[$HcomDbase]    = '�ɱһ��߷���';
$HcomCost[$HcomDbase]    = 500;
$HcomName[$HcomSbase]    = '������Ϸ���';
$HcomCost[$HcomSbase]    = 8000;
$HcomName[$HcomMonument] = '��ǰ���¤';
$HcomCost[$HcomMonument] = 9999;
$HcomName[$HcomSMonument] = '���쵭ǰ���¤';
$HcomCost[$HcomSMonument] = 19999;
$HcomName[$HcomHaribote] = '�ϥ�ܥ�����';
$HcomCost[$HcomHaribote] = 100;
$HcomName[$HcomScity]    = '�����ԻԷ���';
$HcomCost[$HcomScity]    = 1000;
$HcomName[$HcomSFarm]    = '������������';
$HcomCost[$HcomSFarm]    = 600;
$HcomName[$HcomTower]    = '���ȥӥ�����';
$HcomCost[$HcomTower]    = 400;
$HcomName[$HcomFire]     = '���ɽ����';
$HcomCost[$HcomFire]     = 600;
$HcomName[$HcomWindmill] = '���ַ���';
$HcomCost[$HcomWindmill] = 3000;
$HcomName[$HcomMyhome]   = '�ޥ��ۡ������';
$HcomCost[$HcomMyhome]   = 500;
$HcomName[$HcomPort]     = '������';
$HcomCost[$HcomPort]     = 800;
$HcomName[$HcomPolice]   = '�ٻ������';
$HcomCost[$HcomPolice]   = 1000;
$HcomName[$HcomHospital] = '�±�����';
$HcomCost[$HcomHospital] = 1000;
$HcomName[$HcomTrump]    = '�ȥ�������';
$HcomCost[$HcomTrump]    = 1500;
$HcomName[$HcomFlower]   = '���֤򿢤���';
$HcomCost[$HcomFlower]   = 100;
$HcomName[$HcomBreakwater]= '���������';
$HcomCost[$HcomBreakwater]= 300;
$HcomName[$HcomDokan]	= '�ڴ�(�ϲ�)����';
$HcomCost[$HcomDokan]	= 1000;
$HcomName[$HcomUg]		= '�ϲ�����';
$HcomCost[$HcomUg]		= 800;
$HcomName[$HcomShipbuild]  = '¤��';
$HcomCost[$HcomShipbuild]  = 500;
$HcomName[$HcomManipulate] = '�������';
$HcomCost[$HcomManipulate] = 700;
$HcomName[$HcomSTManipulate] = 'ST�������';
$HcomCost[$HcomSTManipulate] = 1500;
$HcomName[$HcomSpy]          = '������ɸ�';
$HcomCost[$HcomSpy]          = 3800;
$HcomName[$HcomTeisatu]      = '�廡';
$HcomCost[$HcomTeisatu]      = 300;
$HcomName[$HcomWarp]         = 'ž�����ַ���';
$HcomCost[$HcomWarp]         = 1800;
$HcomName[$HcomDeathtrap]    = '�ǥ��ȥ�å׷���';
$HcomCost[$HcomDeathtrap]    = 350;
$HcomName[$Hcomcolony]       = '����ˡ��';
$HcomCost[$Hcomcolony]       = ($HwarFlg) ? 26000 : 34000;
$HcomName[$HcomBioMissile]   = '�Х����ߥ�����';
$HcomCost[$HcomBioMissile]   = 170;
$HcomName[$HcomMissileNM]    = '�ߥ�����ȯ��';
$HcomCost[$HcomMissileNM]    = 20;
$HcomName[$HcomMissilePP]    = 'PP�ߥ�����ȯ��';
$HcomCost[$HcomMissilePP]    = 40;
$HcomName[$HcomMissileSPP]   = 'SPP�ߥ�����ȯ��';
$HcomCost[$HcomMissileSPP]   = 50;
$HcomName[$HcomMissileRNG]   = '��󥰥ߥ�����ȯ��';
$HcomCost[$HcomMissileRNG]   = 60;
$HcomName[$HcomMissileST]    = 'ST�ߥ�����ȯ��';
$HcomCost[$HcomMissileST]    = 150;
$HcomName[$HcomMissileLD]    = 'Φ���˲���ȯ��';
$HcomCost[$HcomMissileLD]    = 180;
$HcomName[$HcomSendMonster]  = '�����ɸ�';
$HcomCost[$HcomSendMonster]  = 3000;
$HcomName[$HcomSSendMonster] = 'S�����ɸ�';
$HcomCost[$HcomSSendMonster] = 6000;
$HcomName[$HcomMissileRM]    = '���Ω����ȯ��';
$HcomCost[$HcomMissileRM]    = 100;
$HcomName[$HcomMissileSRM]   = 'S���Ω����ȯ��';
$HcomCost[$HcomMissileSRM]   = ($HwarFlg) ? 800 : 3000;
$HcomName[$HcomMissileGM]    = 'ͶƳ��ȯ��';
$HcomCost[$HcomMissileGM]    = 1000;
$HcomName[$HcomMissileMGM]   = '����ͶƳ��ȯ��';
$HcomCost[$HcomMissileMGM]   = 1000;
$HcomName[$HcomMissileDM]    = '�Ȼ���ȯ��';
$HcomCost[$HcomMissileDM]    = 30;
$HcomName[$HcomMissileNCM]   = '�˥ߥ�����ȯ��';
$HcomCost[$HcomMissileNCM]   = ($HwarFlg) ? 6000 : 9800;
$HcomName[$HcomMissilePLD]   = '�˲�PP��ȯ��';
$HcomCost[$HcomMissilePLD]   = 200;
$HcomName[$HcomDummy]        = '���ߡ�̿��';
$HcomCost[$HcomDummy]        = 10;
$HcomName[$HcomShip]         = '�������ѹ�';
$HcomCost[$HcomShip]         = 100;
$HcomName[$HcomShipM]        = '�����ΰ�ư';
$HcomCost[$HcomShipM]        = 300;
$HcomName[$HcomDoNothing]    = '��ⷫ��';
$HcomCost[$HcomDoNothing]    = 0;
$HcomName[$HcomShipSell]     = '�����';
$HcomCost[$HcomShipSell]     = 0;
$HcomName[$HcomSell]         = '�������';
$HcomCost[$HcomSell]         = -100;
$HcomName[$HcomOreSell]      = '������ѡ����';
$HcomCost[$HcomOreSell]      = 0;
$HcomName[$HcomOilSell]      = '������ѡ����';
$HcomCost[$HcomOilSell]      = 0;
$HcomName[$HcomWeponSell]    = 'ʼ����ѡ����';
$HcomCost[$HcomWeponSell]    = 0;
$HcomName[$HcomOreBuy]       = '���й���';
$HcomCost[$HcomOreBuy]       = 2;
$HcomName[$HcomOilBuy]       = '��������';
$HcomCost[$HcomOilBuy]       = 5;
$HcomName[$HcomWeponBuy]     = 'ʼ�����';
$HcomCost[$HcomWeponBuy]     = 24;
$HcomName[$HcomMoney]        = '�����';
$HcomCost[$HcomMoney]        = 100;
$HcomName[$HcomFood]         = '�������';
$HcomCost[$HcomFood]         = -100;
$HcomName[$HcomEmigration]   = '��̱';
$HcomCost[$HcomEmigration]   = -100;
$HcomName[$HcomPropaganda]   = 'Ͷ�׳�ư';
$HcomCost[$HcomPropaganda]   = 1000;
$HcomName[$HcomMonsEgg]      = '���å��å�����';
$HcomCost[$HcomMonsEgg]      = 3000;
$HcomName[$HcomMonsEsa]      = '���ä˱�';
$HcomCost[$HcomMonsEsa]      = 500;
$HcomName[$HcomMonsEnsei]    = '���ñ���';
$HcomCost[$HcomMonsEnsei]    = 500;
$HcomName[$HcomMonsTettai]   = '����ű��';
$HcomCost[$HcomMonsTettai]   = 0;
$HcomName[$HcomMonsEsaAid]   = '���ñ¾���';
$HcomCost[$HcomMonsEsaAid]   = 0;
$HcomName[$HcomMonsAid]      = '���þ���';
$HcomCost[$HcomMonsAid]      = 0;
$HcomName[$HcomMonsSell]     = '�������';
$HcomCost[$HcomMonsSell]     = 0;
$HcomName[$HcomMonsExer]     = '�����ϵ�����';
$HcomCost[$HcomMonsExer]     = 500;

$HcomName[$HcomSUnit]		= '�����˥åȷ���';
$HcomCost[$HcomSUnit]		= 400;
$HcomName[$HcomSFood]		= '���迩���Ǿ夲';
$HcomCost[$HcomSFood]		= 1000;
$HcomName[$HcomSPioneer]	= '��������';
$HcomCost[$HcomSPioneer]	= 1000;
$HcomName[$HcomSBuild]		= '������߷�';
$HcomCost[$HcomSBuild]		= 1000;
$HcomName[$HcomSMissileGM]	= '����ͶƳ�ߥ�����ȯ��';
$HcomCost[$HcomSMissileGM]	= 200;
$HcomName[$HcomSMissilePP]	= '����PP�ߥ�����ȯ��';
$HcomCost[$HcomSMissilePP]	= 200;
$HcomName[$HcomSMissile]	= '����ߥ�����ȯ��';
$HcomCost[$HcomSMissile]	= 300;
$HcomName[$HcomSMissileMGM]	= '�������ͶƳ��ȯ��';
$HcomCost[$HcomSMissileMGM]	= 1400;
$HcomName[$HcomSOccupy]		= '��������';
$HcomCost[$HcomSOccupy]		= 1000;
$HcomName[$HcomSpaceFarm]	= '�����������';
$HcomCost[$HcomSpaceFarm]	= 500;
$HcomName[$HcomSFactory]	= '���蹩�����';
$HcomCost[$HcomSFactory]	= 1000;
$HcomName[$HcomSpaceBase]	= '����ߴ��Ϸ���';
$HcomCost[$HcomSpaceBase]	= 1000;
$HcomName[$HcomSDbase]		= '�����ɱһ��߷���';
$HcomCost[$HcomSDbase]		= 1000;
$HcomName[$HcomSEisei]		= '�����������';
$HcomCost[$HcomSEisei]		= 2000;
$HcomName[$HcomSDestroy]	= '�����˥å��˲�';
$HcomCost[$HcomSDestroy]	= 200;

$HcomName[$HcomOMissileNM]	= '����ߥ�����';
$HcomCost[$HcomOMissileNM]	= 40;
$HcomName[$HcomOMissilePP]	= '����PP�ߥ�����';
$HcomCost[$HcomOMissilePP]	= 50;
$HcomName[$HcomOMissileSPP]	= '����SPP�ߥ�����';
$HcomCost[$HcomOMissileSPP]	= 60;

$HcomName[$HcomGiveup]		= '�������';
$HcomCost[$HcomGiveup]		= 0;
$HcomName[$HcomAutoPrepare]	= '���ϼ�ư����';
$HcomCost[$HcomAutoPrepare]	= 0;
$HcomName[$HcomAutoPrepare2]= '�Ϥʤ餷��ư����';
$HcomCost[$HcomAutoPrepare2]= 0;
$HcomName[$HcomAutoSellTree]= 'Ȳ�μ�ư����';
$HcomCost[$HcomAutoSellTree]= 0;
$HcomName[$HcomAutoDelete]	= '���ײ�����ű��';
$HcomCost[$HcomAutoDelete]	= 0;

1;