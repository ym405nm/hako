#!/usr/local/bin/perl --
# ���ϥ����С��˹�碌���ѹ����Ʋ�������
# perl5�ѤǤ���
#----------------------------------------------------------------------
# Ȣ����� ver2.30
# �ᥤ�󥹥���ץ�(ver1.02)
# ���Ѿ�������ˡ���ϡ�hako-readme.txt�ե�����򻲾�
# Ȣ�����Υڡ���: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# ���ۤ�Ȣ��֤ߤ�ʤ����Ȣ��ʲ�����
$versionInfo = "version5.54e";
#----------------------------------------------------------------------
BEGIN {
########################################
# ���顼ɽ��
$SIG{__WARN__} =
sub {
	my($msg) = @_;

	print STDOUT <<END;
Content-type: text/html

<p><big><tt>WARNNING: $msg</tt></big></p>
END
};

$SIG{__DIE__} =
sub {
	my($msg) = @_;

	print STDOUT <<END;
Content-type: text/html

<p><big><tt>ERROR: $msg</tt></big></p>
END
exit(-1);
};

$SIG{KILL} =
sub {
	my($msg) = @_;

	print STDOUT <<END;
Content-type: text/html

<p><big><tt>KILL: $msg</tt></big></p>
END
exit(-1);
};
########################################
}
#----------------------------------------------------------------------
# �Ķ�������ʬ��"hako-init.cgi"�����"init-game.cgi"�ˤ���ޤ���
#----------------------------------------------------------------------
require './hako-init.cgi';
require './hako-io.cgi';
require './init-game.cgi';

# �۾ｪλ������
# (��å��岿�äǡ�����������뤫)
my($unlockTime) = 120;

#----------------------------------------------------------------------
# �ѿ�
#----------------------------------------------------------------------

# COOKIE
#my($defaultID);   # ���̾��
$defaultID;     # ���̾��
$defaultTarget; # �������åȤ�̾��


# ��κ�ɸ��
$HpointNumber = $HislandSize * $HislandSize;

# ����κ�ɸ��
$HpointOcean = $HoceanSize * $HoceanSize;

#----------------------------------------------------------------------
# �ᥤ��
#----------------------------------------------------------------------

get_host(0);

# �����ץ��
$HtempBack = "<A HREF=\"$HthisFile\">${HtagBig_}�ȥåפ����${H_tagBig}</A>";
$Body = "<BODY $htmlBody>";

# ��å��򤫤���
if(!hakolock()) {
	# ��å�����
	# �إå�����
	tempHeader();

	# ��å����ԥ�å�����
	tempLockFail();

	# �եå�����
	tempFooter();

	# ��λ
	exit(0);
}

# ����ν����
srand(time^$$);

# COOKIE�ɤߤ���
cookieInput();

# CGI�ɤߤ���
cgiInput();

if (-e $HpasswordFile) {
	# �ѥ���ɥե����뤬����
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword  = <PIN>); # �ޥ����ѥ���ɤ��ɤ߹���
	chomp($HspecialPassword = <PIN>); # �ü�ѥ���ɤ��ɤ߹���
	close(PIN);
} else {
	unlock();
	tempHeader();
	tempNoPasswordFile();
	tempFooter();
	exit(0);
}
# ľ��󥯶ػ�
if($Hlinkcheck){
unless(($HmainMode eq 'print') || ($HmainMode eq 'owner') || ($HmainMode eq 'landmap')){
L_LINK_CHECK:
{
	my($referer) = $ENV{HTTP_REFERER};
	local($_);
	for (@HokURL, $HthisFile) {
	    last L_LINK_CHECK if ($referer =~ /^$_/); # ���ĥڡ�������
	}
	# ���顼
	print "Location: $HjumpURL\n\n\n";
	exit;
}
}
}
# ���ƥ⡼��
if((-e "./mente_lock") && !checkMasterPassword($HdefaultPassword)) {
	cookieOutput();
	unlock();
	mente_mode(1);
}
# ��ǡ������ɤߤ���
if(readIslandsFile($HcurrentID) == 0) {
	unlock();
	tempHeader();
	tempNoDataFile();
	tempFooter();
	exit(0);
}

# �ƥ�ץ졼�Ȥ�����
tempInitialize();

# COOKIE�ˤ��ID�����å�
if($HmainMode eq 'owner') {
	# ������������
	axeslog() if($HtopAxes == 1);
	
	unless($ENV{'HTTP_COOKIE'}) {
		cookieOutput(); # COOKIE��������줿���ɤ����񤭹��ߥ����å�
		next if($ENV{'HTTP_COOKIE'}); # �񤭹���OK
		# ���å�����ͭ���ˤ��Ƥ��ʤ�
		unlock();
		tempHeader();
		tempWrong("���å�����ͭ���ˤ��Ƥ���������");
		tempFooter();
		exit(0);
	}
	if($checkID || $checkImg) {
		# id����������
		my($pcheck) = checkPassword($Hislands[$HidToNumber{$HcurrentID}]->{'password'},$HinputPassword);
		my $free = 0;
		foreach (@freepass){
			$free += 1 if(($_ == $defaultID) || ($_ == $HcurrentID));
		}
		my($icheck) = !($checkID && ($HcurrentID != $defaultID) && $defaultID);
		my($lcheck) = !($checkImg && ($HimgLine eq '' || $HimgLine eq $HimageDir));
		# �ѥ����
		if(($pcheck != 2) && ($free != 2) && (!$icheck || !$lcheck)) {
			# ���Ĥ����鿴���Ѥ˲���������ʤɤ� ($free != 2) ����ʬ�� !$free ���ѹ����Ʋ�������
			unlock();
			tempHeader();
			if(!$icheck) {
				tempWrong("��ʬ����ʳ��ˤ�����ޤ���"); # ID�㤤
			} else {
				tempWrong("�ֲ����Υ���������פ򤷤Ʋ�������"); # ���������ꤷ�Ƥ��ʤ�
			}
			tempFooter();
			exit(0);
		}
	}
}

# COOKIE����
cookieOutput();

if($HmainMode eq 'owner' && $HjavaMode eq 'java' ||
	$HmainMode eq 'monsedit' && $HjavaMode eq 'java' || # �����Խ�
	$HmainMode eq 'commandJava' || # ���ޥ�����ϥ⡼��
	$HmainMode eq 'command2' || # ���ޥ�����ϥ⡼�ɡ�ver1.1����ɲá���ư���ѡ�
	$HmainMode eq 'comment' && $HjavaMode eq 'java' || #���������ϥ⡼��
	$HmainMode eq 'lbbs' && $HjavaMode eq 'java') { #���������ϥ⡼��
	
	require('hako-js.cgi');
	require('hako-map.cgi');
	
	# �إå�����
	tempHeader(1);
	if($HmainMode eq 'commandJava') {
		# ��ȯ�⡼��
		commandJavaMain();
	} elsif($HmainMode eq 'monsedit') {
		# ��������
		monsMain();
	} elsif($HmainMode eq 'command2') {
		# ��ȯ�⡼�ɣ��ʼ�ư�ϥ��ޥ���ѡ�ver1.1����ɲá���ư���ѡˡ�
		commandMain();
	} elsif($HmainMode eq 'comment') {
		# ���������ϥ⡼��
#		if($Hrsswrite){require('hako-rss.cgi');rssMain();}
		commentMain();
	} elsif($HmainMode eq 'lbbs') {
		# ������Ǽ��ĥ⡼��
#		if($Hrsswrite){require('hako-rss.cgi');rssMain();}
		localBbsMain();
	}else{
	    ownerMain();
	}
	# �եå�����
	tempFooter();
	# ��λ
	exit(0);
}elsif($HmainMode eq 'landmap'){
	require('hako-js.cgi');
	require('hako-map.cgi');
	if($HcurrentID == 999){
		# ����
		$Body = "<BODY BGCOLOR=\"BLACK\" TEXT=\"WHITE\" LINK=\"#AAAAFF\" ALINK=\"GREEN\" VLINK=\"#AAAAFF\" BACKGROUND=\"star.gif\" BGPROPERTIES=FIXED>";
		$HskinName = 'space.css';
		tempHeader();
		printIslandJava(3);
	}elsif($HcurrentID == 888){
		# ����
		$Body = "<BODY BGCOLOR=\"BULE\" TEXT=\"WHITE\" LINK=\"#AAAAFF\" ALINK=\"GREEN\" VLINK=\"#AAAAFF\" BACKGROUND=\"land0.gif\" BGPROPERTIES=FIXED>";
		$HskinName = 'ocean.css';
		tempHeader();
		printIslandJava(4);
	}elsif($Hugmode){
		# �ϲ�
		tempHeader();
		printIslandJava(10);
	}else{
		tempHeader();
		printIslandJava(0);
	}
	# �եå�����
	tempFooter();
	# ��λ
	exit(0);
}elsif($HmainMode eq 'space'){
	$Body = "<BODY BGCOLOR=\"BLACK\" TEXT=\"WHITE\" LINK=\"#AAAAFF\" ALINK=\"GREEN\" VLINK=\"#AAAAFF\" BACKGROUND=\"star.gif\" BGPROPERTIES=FIXED>";
	$HskinName = 'space.css';
	tempHeader();
	require('hako-map.cgi');
	spaceMap();
	tempFooter();
	exit(0);
}elsif($HmainMode eq 'ocean'){
	$Body = "<BODY BGCOLOR=\"BULE\" TEXT=\"WHITE\" LINK=\"#AAAAFF\" ALINK=\"GREEN\" VLINK=\"#AAAAFF\" BACKGROUND=\"land0.gif\" BGPROPERTIES=FIXED>";
	$HskinName = 'ocean.css';
	tempHeader();
	require('hako-map.cgi');
	oceanMap();
	tempFooter();
	exit(0);
}elsif(($HmainMode eq 'new') || ($HmainMode eq 'bfield')) {
#	HdebugOut("�⡼��:$HmainMode");
}else{
	# �إå�����
	tempHeader();
}

if($HmainMode eq 'turn') {
	# ������ʹ�
	require('hako-turn.cgi');
	require('hako-top.cgi');
	require('exchange.cgi');
	turnMain();
} elsif($HmainMode eq 'new') {
	# ��ο�������
	require('hako-make.cgi');
	require('hako-map.cgi');
	newIslandMain(0);
} elsif($HmainMode eq 'rekidai') {
	# ����͸���Ͽ neo_otacky�᤬����
	require('hako-make.cgi');
	rekidaiPopMain();
} elsif($HmainMode eq 'print') {
	# �Ѹ��⡼��
	require('hako-map.cgi');
	printIslandMain();
} elsif($HmainMode eq 'owner') {
	# ��ȯ�⡼��
	require('hako-map.cgi');
	ownerMain();
} elsif($HmainMode eq 'command') {
	# ���ޥ�����ϥ⡼��
	require('hako-map.cgi');
	commandMain();
} elsif($HmainMode eq 'comment') {
	# ���������ϥ⡼��
#	if($Hrsswrite){require('hako-rss.cgi');rssMain();}
	require('hako-map.cgi');
	commentMain();
} elsif($HmainMode eq 'clbbs') {
	# �����ȡ��Ѹ����̿����ᶷ
	$HmainMode = 'owner';
	require('hako-map.cgi');
	clbbsMain();
} elsif($HmainMode eq 'custom') {
	# �������ޥ���
	$HmainMode = 'owner';
	require('hako-map.cgi');
	customMain();
} elsif($HmainMode eq 'custom2') {
	# �������ޥ���2
	$HmainMode = 'owner';
	require('hako-map.cgi');
	customMain(1);
} elsif($HmainMode eq 'lbbs') {
	# ������Ǽ��ĥ⡼��
#	if($Hrsswrite){require('hako-rss.cgi');rssMain();}
	require('hako-map.cgi');
	localBbsMain();
} elsif($HmainMode eq 'monsedit') {
	# ��������
	require('hako-map.cgi');
	monsMain();
} elsif($HmainMode eq 'change') {
	# �����ѹ��⡼��
	require('hako-make.cgi');
	changeMain();
} elsif($HmainMode eq 'FightIsland') {
	# �ʰץȡ��ʥ��� �ԼԤ���ɽ��
	require('hako-js.cgi');
	require('hako-map.cgi');
	fight_map();
} elsif($HmainMode eq 'FightView') {
	# �ʰץȡ��ʥ��� LOG�⡼��
	require('hako-js.cgi');
	require('hako-map.cgi');
	FightViewMain();
} elsif($HmainMode eq 'camp') {
	# �رĥ⡼��
	require('hako-map.cgi');
	require('hako-camp.cgi');
	campMain();
} elsif($HmainMode eq 'exchange') {
	# �񸻼���⡼��
	if(($HexchangeMode ne 'show') && ($HtopAxes == 1)){
		# ������������
		axeslog();
	}
	require('exchange.cgi');
	mainExchange();
} elsif($HmainMode eq 'kani') {
	# �ʰץȥåץڡ���ɽ���⡼��
	require('hako-top.cgi');
	topPageMain(1);
} elsif($HmainMode eq 'alist') {
	# �ʰץȥåץڡ���ɽ���⡼��
	require('hako-top.cgi');
	topPageAlist();
} elsif($HmainMode eq 'settei') { # �������������
	# ����ȥåץڡ���ɽ���⡼��
	require('hako-top.cgi');
	topPageMain(2);

} elsif($HmainMode eq 'list') {
	# �ܺ٥ꥹ��
	require('hako-top.cgi');
	topPageMain(3);
} elsif($HmainMode eq 'bfield') {
	# BattleField�����⡼��
	require('hako-make.cgi');
	require('hako-map.cgi');
	bfieldMain();
} elsif($HmainMode eq 'present') {
	# �����ͤˤ��ץ쥼��ȥ⡼��
	require('hako-make.cgi');
	presentMain();
} elsif($HmainMode eq 'punish') {
	# �����ͤˤ�����ۥ⡼��
	require('hako-make.cgi');
	punishMain();
} elsif($HmainMode eq 'lchange') {
	# �����ͤˤ���Ϸ��ѹ��⡼��
	require('hako-map.cgi');
	require('hako-make.cgi');
	lchangeMain();
} elsif($HmainMode eq 'predelete') {
	# �����ͤˤ�뤢������⡼��
	require('hako-make.cgi');
	preDeleteMain();
} elsif($HmainMode eq 'ichange') {
	# �����ͤˤ��Ƽ���ǡ����ѹ��⡼��
	require('hako-make.cgi');
	ichangeMain();
} elsif($HmainMode eq 'setupv') {
	# ��������ǧ�⡼��
	require('hako-make.cgi');
	setupValue();
} else {
	# ����¾�ξ��ϥȥåץڡ����⡼��
	require('hako-top.cgi');
	topPageMain(0);
}

# �եå�����
tempFooter();

# ��λ
exit(0);

# ���ޥ�ɤ����ˤ��餹
sub slideFront {
	my($command, $number) = @_;

	# ���줾�줺�餹
	splice(@$command, $number, 1);

#	HdebugOut("�Ǹ�˻�ⷫ��:" . $#$command);
	# �Ǹ�˻�ⷫ��
	$command->[$#$command + 1] = {
	'kind' => $HcomDoNothing,
	'target' => 0,
	'x' => 0,
	'y' => 0,
	'arg' => 0,
	'tx' => 0,
	'ty' => 0,
	'flg' => 0 # ���Ū���ΰ�
	};
}

# ���ޥ�ɤ��ˤ��餹
sub slideBack {
	my($command, $number, $kind, $target, $x, $y, $arg, $tx, $ty, $flg) = @_;
	$tx = 0 if($tx eq '');
	$ty = 0 if($ty eq '');
	# ���줾�줺�餹
	return if $number == $#$command;
#	pop(@$command);
	splice(@$command, $number, 0, $command->[$number]);
	if($kind > 0){
		$command->[$number] = {
		'kind' => $kind,
		'target' => $target,
		'x' => $x,
		'y' => $y,
		'arg' => $arg,
		'tx' => $tx,
		'ty' => $ty,
		'flg' => $flg # ���Ū���ΰ�
		};
	}
}

#----------------------------------------------------------------------
# ��ǡ���������
#----------------------------------------------------------------------

# ����ǡ����ɤߤ���
sub readIslandsFile {
	my($num) = @_;  # 0�����Ϸ��ɤߤ��ޤ�
					# -1�������Ϸ����ɤ�
					# �ֹ���Ȥ�������Ϸ��������ɤߤ���

	# �ǡ����ե�����򳫤�
	return 0 if(!open(IN, "${HdirName}/hakojima.dat"));
	
	# �ƥѥ�᡼�����ɤߤ���
	$HislandTurn     = int(<IN>); # �������
	return 0 if($HislandTurn == 0);
	$HislandLastTime = int(<IN>); # �ǽ���������
	return 0 if($HislandLastTime == 0);
	$HislandNumber   = int(<IN>); # ������
	# ���˳�����Ƥ�ID�ȴ������¤������ID
	my $tmp = <IN>;
	chomp($tmp);
	($HislandNextID, @HpreDeleteID) = split(/,/, $tmp);

	if($Htournament){
		# �ʰץȡ��ʥ���
		$HflexTimeSet = 1;
		$Hallyflg = 0;
		$Hpossess = 0;
		# �ǡ����ե�����򳫤�
		return 0 if(!open(TIN, "${HdirName}/tournament.dat"));
		$HislandFightMode	= int(<TIN>);  # ���ߤ���Ʈ�⡼��
		$HislandChangeTurn	= int(<TIN>);  # �ڤ��ؤ�������
		$HislandFightCount	= int(<TIN>);  # �������ܤ�
		$HislandTurnCount	= int(<TIN>);  # �����󹹿���
		<TIN>;
		<TIN>;
		<TIN>;
		<TIN>;
		if($HislandFightMode == 1){
			# ͽ��
			@HflexTime = @HtmTime1;
		}elsif($HislandFightMode == 2){
			# ��ȯ
			@HflexTime = @HtmTime2;
		}elsif($HislandFightMode == 3){
			# ��Ʈ
			@HflexTime = @HtmTime3;
		}
		# flexTime����
		$HunitTime = 3600 * $HflexTime[($HislandTurnCount % ($#HflexTime + 1))] if($HflexTimeSet);
	}else{
		# flexTime����
		$HunitTime = 3600 * $HflexTime[($HislandTurn % ($#HflexTime + 1))] if($HflexTimeSet);
	}

	# ���������Ƚ��
	my($now) = time;
	if(((($Hdebug == 1) && ($HmainMode eq 'Hdebugturn')) ||
		(($now - $HislandLastTime) >= $HunitTime)) &&
		(($HlastTurn == 0)||($HislandTurn < $HlastTurn))) { # ��λ������
		$HmainMode = 'turn';
		$num = -1; # �����ɤߤ���
	}

	# ����ɤߤ���
	my($i);
	for($i = 0; $i < $HislandNumber; $i++) {
		$Hislands[$i] = readIsland($num);
		$HidToNumber{$Hislands[$i]->{'id'}} = $i;
		foreach (@HpreDeleteID) {
			if($Hislands[$i]->{'id'} == $_) {
				$Hislands[$i]->{'predelete'} = 1;
			}
		}
		$Hislands[$i]->{'predelete'} = 1 if($Hislands[$i]->{'fight_id'} == -1); # ���ﾡ���Ϥ��������Ʊ��ư��
	}
	readsubmap(0);#����ޥå��ɹ�
	readsubmap(1);#����ޥå��ɹ�
	readCommandLate(); #������̿��ǡ����ɹ�
	# �ե�������Ĥ���
	close(IN);
	close(TIN) if($Htournament);
	return 1;
}
# ���֥ޥåפҤȤ��ɤߤ���
sub readsubmap {
	my($num) = @_;
	# ���衢����ޥå��ɤߤ���
	if(open(IN, "${HdirName}/submap.$num")){
		# �Ϸ�
		my(@land, @landValue, @land2, @landValue2, @nation, $line, @lbbs);
		my($x, $y, $i);
		if($num == 0){
			#����
			$Hspacemap = 1;
			for($y = 0; $y < $HislandSize; $y++) {
				$line = <IN>;
				for($x = 0; $x < $HislandSize; $x++) {
					$line =~ s/^(..)(....)(..)(....)(..)//;
					$land[$x][$y] = hex($1);
					$landValue[$x][$y] = hex($2);
					$land2[$x][$y] = hex($3);
					$landValue2[$x][$y] = hex($4);
					$nation[$x][$y] = hex($5);
				}
			}
		}else{
			#����
			for($y = 0; $y < $HoceanSize; $y++) {
				$line = <IN>;
				for($x = 0; $x < $HoceanSize; $x++) {
					$line =~ s/^(..)(....)(..)(....)(..)//;
					$land[$x][$y] = hex($1);
					$landValue[$x][$y] = hex($2);
					$land2[$x][$y] = hex($3);
					$landValue2[$x][$y] = hex($4);
					$nation[$x][$y] = hex($5);
				}
			}
		}
		my $spaces = <IN>;# ����񻺾�̣���
		chomp($spaces);
		my $solarwind= int(<IN>); # ������������
		my $area	= int(<IN>); # ��ȯ����
		my $pop		= int(<IN>); # ����͸�
		my $farm	= int(<IN>); # ��������
		my $factory	= int(<IN>); # ���蹩��
		my $food	= <IN>; # ���迩��
		my @foods	= split(/,/, $food);
#		HdebugOut("$foods[0],$foods[1],$foods[2]");
		<IN>;# ��ĥ��
		<IN>;# ��ĥ��
		<IN>;# ��ĥ��
		<IN>;# ��ĥ��
		<IN>;# ��ĥ��
		# ������Ǽ���
		for($i = 0; $i < $HlbbsMax; $i++) {
			$line = <IN>;
			chomp($line);
			$lbbs[$i] = $line;
		}
		if($num == 0){
			#����
			$Hspace = {
			 'land' => \@land,
			 'landValue' => \@landValue,
			 'land2' => \@land2,
			 'landValue2' => \@landValue2,
			 'nation' => \@nation,
			 'solarwind' => $solarwind,
			 'space' => $spaces,
			 'area' => $area,
			 'pop' => $pop,
			 'farm' => $farm,
			 'factory' => $factory,
			 'food' => int($foods[0]),
			 'foodP' => int($foods[1]),
			 'foodC' => int($foods[2]),
			 'lbbs' => \@lbbs
			};
		}else{
			#����
			$Hocean = {
			 'land' => \@land,
			 'landValue' => \@landValue,
			 'land2' => \@land2,
			 'landValue2' => \@landValue2,
			 'nation' => \@nation,
			 'solarwind' => $solarwind,
			 'space' => $spaces,
			 'area' => $area,
			 'pop' => $pop,
			 'farm' => $farm,
			 'factory' => $factory,
			 'food' => int($foods[0]),
			 'foodP' => int($foods[1]),
			 'foodC' => int($foods[2]),
			 'lbbs' => \@lbbs
			};
		}
		close(IN);
	}
}

# ��ҤȤ��ɤߤ���
sub readIsland {
	my($num) = @_;
	my($name, $id, $ownername, $prize, $absent, $comment, $password, $money, $food,
		$pop, $area, $farm, $weather, $factory, $port, $mountain, $tower,
		$yousyoku, $turnsu, $ally, $MissileK, $MissileA, $present,
		$allex, $status , $evil, $order, $mons1, $monsurl, $score, $xy, $ore,$weapon,$oil,$oilfield,
		$monsfound,$cmdTurn,$cmdIp,$cmdId,$cmdtime);
	$name = <IN>; # ���̾��
	chomp($name);
	if($name =~ s/,(.*)$//g) {
		$score = int($1);
	} else {
		$score = 0;
	}
	$id = int(<IN>);       # ID�ֹ�
	$ownername= <IN>;      # ������̾
	chomp($ownername);
	$prize = <IN>;         # ����
	chomp($prize);
	$absent = int(<IN>);   # Ϣ³��ⷫ���
	$comment = <IN>;       # ������
	chomp($comment);
	my @comments = split(/<>/, $comment);
	$password = <IN>;      # �Ź沽�ѥ����
	chomp($password);
	$money = int(<IN>);    # ���
	$food = int(<IN>);     # ����
	$pop = <IN>; # �͸�
	my @pops = split(/,/, $pop);
	$area = int(<IN>);     # ����
	$farm = int(<IN>);     # ����
	$weather = <IN>;  # ŷ��
	my($neww,@pastw);
	my($w) = 0;
	$weather =~ s/([0-9]*),//;
	$neww = int($1);
	for($w = 0; $w < 10; $w++) {
		$weather =~ s/([0-9]*),//;
		$pastw[$w] = int($1);
	}
	$weather =~ s/([0-9]*)$//;
	$pastw[$w] = int($1);
	$factory = int(<IN>);  # ����
	$port     = int(<IN>); # ��
	$mountain = int(<IN>); # �η���
	$tower    = int(<IN>); # ������
	$yousyoku = int(<IN>); # �ܿ���
	$turnsu   = <IN>; # ���ۤ������������Υ������,�����,���ϥ�����
	my @hturn = split(/,/, $turnsu);
	my $winp  = <IN>; # �������餱�ݥ���ȡ����ä���
	my @win   = split(/,/, $winp);
	$MissileK = <IN>; # �ߥ�����ȯ�Ͳ�ǽ��,ȯ�ͥߥ��������
	$ally     = int(<IN>); # ��°ID
	$present  = <IN>;      # �ץ쥼���
	$allex    = int(<IN>); # �и�������
	$status   = int(<IN>); # �����
	$evil     = int(<IN>); # 
	$monsfound= int(<IN>); # ���߽и����Ƥ�����äο�
	$order    = int(<IN>); # ̿��
	$xy       = <IN>; # ��ɸ
	$ore      = int(<IN>); # ����
	$weapon   = int(<IN>); # ʼ��
	$oil      = int(<IN>); # ����
	$oilfield = int(<IN>); # ����������
	my @Missile = split(/,/, $MissileK);
	my @coordinate = split(/,/, $xy);
	
	$present =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*),([0-9]*)$/;
	my @prese = (int($1),int($2),int($3),int($4),int($5),int($6),int($7),int($8),int($9),int($10),int($11),int($12),int($13),int($14));
	
	# ���åХȥ���
	$mons1    = <IN>; # ��ʬ�β���
	$monsurl  = <IN>; # ����URL
	chomp($monsurl);
	my @monster = split(/,/, $mons1);

	# HidToName�ơ��֥����¸
	$HidToName{$id} = $name;

	# �Ϸ�
	my(@land, @landValue, @land2, @landValue2, @nation, $line, @command, @lbbs);
	my(@ugL, @ugV, @ugX, @ugY);# �ϲ�
	if(($num == -1) || ($num == $id)) {
		exit(0) if(!open(IIN, "${HdirName}/island.$id"));
		my($x, $y, $i);
		for($y = 0; $y < $HislandSize; $y++) {
			$line = <IIN>;
			for($x = 0; $x < $HislandSize; $x++) {
				$line =~ s/^(..)(....)(..)(....)(..)//;
				$land[$x][$y] = hex($1);
				$landValue[$x][$y] = hex($2);
				$land2[$x][$y] = hex($3);
				$landValue2[$x][$y] = hex($4);
				$nation[$x][$y] = hex($5);
			}
		}
		# �ϲ�
		for($i = 0; $i < $HugMax; $i++) {
			$line = <IIN>;
			for($x = 0; $x < 9; $x++) {
				$line =~ s/^(.)(..)//;
				$ugL[$i][$x] = hex($1);
				$ugV[$i][$x] = hex($2);
			}
			$line =~ /^,([0-9]*),([0-9]*)$/;
			$ugX[$i] = $1;
			$ugY[$i] = $2;
		}
		$cmdTurn	= int(<IIN>); # ������
		$cmdIp		= <IIN>;# IP
		chomp($cmdIp);
		$cmdId		= int(<IIN>);# ���å���ID
		$cmdtime	= int(<IIN>);# ���ϻ���
		<IIN>;# ��ĥ��
		# ���ޥ��
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

		# ������Ǽ���
		for($i = 0; $i < $HlbbsMax; $i++) {
			$line = <IIN>;
			chomp($line);
			$lbbs[$i] = $line;
		}

		close(IIN);
	}

	my($fight_id);
	if($Htournament){
		# �ʰץȡ��ʥ���
		$fight_id = int(<TIN>);	# �������ID
		<TIN>;
		<TIN>;
		<TIN>;
		<TIN>;
	}

	# �緿�ˤ����֤�
	return {
	 'name' => $name,
	 'ownername' => $ownername, # ������̾ɽ���Τ����ɲ�
	 'id' => $id,
	 'score' => $score,
	 'prize' => $prize,
	 'absent' => $absent,
	 'comment' => $comments[0],
	 'commentLabel0' => $comments[1],
	 'commentLabel1' => $comments[2],
	 'commentLabel2' => $comments[3],
	 'commentLabel3' => $comments[4],
	 'commentLabel4' => $comments[5],
	 'password' => $password,
	 'money' => $money,
	 'food' => $food,
	 'pop' => int($pops[0]),
	 'popspace' => int($pops[1]),
	 'spa' => int($pops[2]),
	 'area' => $area,
	 'farm' => $farm,
	 'weather' => $neww,
	 'pastweather' => \@pastw,
	 'factory' => $factory,
	 'port' => $port,
	 'mountain' => $mountain,
	 'tower' => $tower,
	 'yousyoku' => $yousyoku,
	 'turnsu' => int($hturn[0]),
	 'zyuni' => int($hturn[1]),
	 'winP' => int($win[0]),
	 'loseP' => int($win[1]),
	 'winS' => int($win[2]),
	 'possess' => int($win[3]),
	 'ally' => $ally,
	 'MissileK' => int($Missile[0]),
	 'MissileA' => int($Missile[1]),
	 'present' => \@prese,
	 'allex' => $allex,
	 'status' => $status,
	 'evil' => $evil,
	 'kaisi' => int($hturn[2]),
	 'order' => $order,
	 'x' => int($coordinate[0]),
	 'y' => int($coordinate[1]),
	 'ore' => $ore,
	 'weapon' => $weapon,
	 'oil' => $oil,
	 'oilfield' => $oilfield,
	 'land' => \@land,
	 'landValue' => \@landValue,
	 'land2' => \@land2,
	 'landValue2' => \@landValue2,
	 'nation' => \@nation,
	 'ugL' => \@ugL,
	 'ugV' => \@ugV,
	 'ugX' => \@ugX,
	 'ugY' => \@ugY,
	 'fight_id' => $fight_id,
	 'command' => \@command,
	 'lbbs' => \@lbbs,
	 'monsurl' => $monsurl,
	 'monster' => \@monster,
	 'monsfound' => $monsfound,
	 'cmdTurn' => $cmdTurn,
	 'cmdIp' => $cmdIp,
	 'cmdId' => $cmdId,
	 'cmdtime' => $cmdtime,
	};
}

# ����ǡ����񤭹���
sub writeIslandsFile {
	my($num, $mode) = @_;

	unless(-e "${HtempdirName}") { mkdir(${HtempdirName}, $HdirMode); }
	if(-e "deldata") { myrmtree("deldata"); }

	if(($mode == 0)||($mode == 1)) {
		# �ե�����򳫤�
		my($retry) = $HretryCount;
		while(!open(OUT, ">${HtempdirName}/hakojima.tmp")) {
			$retry--;
			if($retry <= 0) {
				$HerrorNum = '100';
				return 0;
			}
			# 0.2 �� sleep
			select undef, undef, undef, 0.2;
		}

		# �ƥѥ�᡼���񤭹���
		print OUT "$HislandTurn\n";
		print OUT "$HislandLastTime\n";
		print OUT "$HislandNumber\n";
		print OUT "$HislandNextID," . join(',', @HpreDeleteID) . "\n";
		
		if($Htournament){
			# �ե�����򳫤�
			my($retry) = $HretryCount;
			while(!open(TOUT, ">${HtempdirName}/tournament.tmp")) {
				$retry--;
				if($retry <= 0) {
					$HerrorNum = '100';
					return 0;
				}
				# 0.2 �� sleep
				select undef, undef, undef, 0.2;
			}
			print TOUT "$HislandFightMode\n";
			print TOUT "$HislandChangeTurn\n";
			print TOUT "$HislandFightCount\n";
			print TOUT "$HislandTurnCount\n";
			print TOUT "\n";
			print TOUT "\n";
			print TOUT "\n";
			print TOUT "\n";
			
		}
	}
	# ��ν񤭤���
	my($i);
	my($flag) = 1;
	for($i = 0; $i < $HislandNumber; $i++) {
		if(!writeIsland($Hislands[$i], $num, 0)) {
			$flag = 0;
			last;
		}
	}

	# ����ޥåפν񤭤���
	if($flag) {
		my($c) = $HislandSize / 2 - 1;
#		HdebugOut("����ޥåפκ��� $num �⡼�� $mode ����� $Hspacemap �ϵ� $c");
		$Hspace->{'land'}->[$c][$c] = $HlandEarth;
		if($Hspacemap != 1){
			# ����ޥå׽����
			$Hspace->{'solarwind'} = $HislandTurn + random(30) + 30;
			# ����Ǽ��Ĥ����
			my(@lbbs);
			for($i = 0; $i < $HlbbsMax; $i++) {
				$lbbs[$i] = "0<<0>>";
			}
			$Hspace->{'lbbs'} = \@lbbs;
		}
		$flag = 0 if(!writeIsland($Hspace, 0, 3));
	}

	# ����ޥåפν񤭤���
	if($flag) {
		$flag = 0 if(!writeIsland($Hocean, 0, 4));
	}

	# ������̿��ǡ����񤭹���
	open(COUT, ">${HtempdirName}/command.tmp");
	for($i = $#HcomL; $i >= 0; $i--){
		next if($HcomL[$i]->{turn} <= $HislandTurn);
		printf COUT ("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n",
			$HcomL[$i]->{turn},
			$HcomL[$i]->{turn2},
			$HcomL[$i]->{id},
			$HcomL[$i]->{kind},
			$HcomL[$i]->{target},
			$HcomL[$i]->{x},
			$HcomL[$i]->{y},
			$HcomL[$i]->{arg},
			$HcomL[$i]->{x2},
			$HcomL[$i]->{y2}
		);
	}
	close(COUT);

	# �ե�������Ĥ���
	if(($mode == 0)||($mode == 1)){
		close(OUT);
		close(TOUT) if($Htournament);
	}

	if(!$flag) {
		if(-e "${HtempdirName}/hakojima.tmp") { unlink("${HtempdirName}/hakojima.tmp"); }
		$HerrorNum = '200';
		return 0;
	}
	
	
	if($Htournament){
		rename("${HdirName}/fight.log","${HtempdirName}/fight.tmp");
	}

	# �����̾���ˤ���
	if($num <= -1) {
		if(!(-s "${HtempdirName}/hakojima.tmp")) { $HerrorNum = '111'; return 0; }
		if(!rename("${HtempdirName}/hakojima.tmp", "${HtempdirName}/hakojima.dat")) { $HerrorNum = '121'; return 0; }
		for($i = 0; $i < $HislandNumber; $i++) {
			if(!(-s "${HtempdirName}/islandtmp.$Hislands[$i]->{'id'}")) { $HerrorNum = '211'; return 0; }
			if(!rename("${HtempdirName}/islandtmp.$Hislands[$i]->{'id'}", "${HtempdirName}/island.$Hislands[$i]->{'id'}")) {
				$HerrorNum = '221';
				return 0;
			}
		}
		if(!(-s "${HtempdirName}/submaptmp.0")) { $HerrorNum = '511'; return 0; }
		if(!rename("${HtempdirName}/submaptmp.0", "${HtempdirName}/submap.0")) { $HerrorNum = '521'; return 0; }
		if(!(-s "${HtempdirName}/submaptmp.1")) { $HerrorNum = '611'; return 0; }
		if(!rename("${HtempdirName}/submaptmp.1", "${HtempdirName}/submap.1")) { $HerrorNum = '621'; return 0; }
		if(-s "${HtempdirName}/command.tmp") {
			if(!rename("${HtempdirName}/command.tmp", "${HtempdirName}/command.dat")) { $HerrorNum = '721'; return 0; }
		}
		if($Htournament){
			if(-s "${HtempdirName}/tournament.tmp") {
				if(!rename("${HtempdirName}/tournament.tmp", "${HtempdirName}/tournament.dat")) { $HerrorNum = '821'; return 0; }
			}
			if(-s "${HtempdirName}/fight.tmp") {
				if(!rename("${HtempdirName}/fight.tmp", "${HtempdirName}/fight.log")) { $HerrorNum = '921'; return 0; }
			}
		}
#		if($Hrsswrite){
#			rename("${HdirName}/rss.dat", "${HtempdirName}/rss.dat");
#		}
		
		if(!rename("${HdirName}", "deldata")) { $HerrorNum = '321'; return 0; }
		if(!rename("${HtempdirName}", "${HdirName}")) {
			rename("deldata", "${HdirName}");
			$HerrorNum = '421';
			return 0;
		}
		myrmtree("deldata");
		return 1;
	}

	if(($mode == 0)||($mode == 1)) {
		if(!(-s "${HtempdirName}/hakojima.tmp")) { $HerrorNum = '112'; return 0; }
		if(!rename("${HtempdirName}/hakojima.tmp", "${HdirName}/hakojima.dat")) { $HerrorNum = '122'; return 0; }
	}

	if(($mode == 0)||($mode == 2)) {
		for($i = 0; $i < $HislandNumber; $i++) {
			if (-e "${HtempdirName}/islandtmp.$Hislands[$i]->{'id'}") {
				if(!(-s "${HtempdirName}/islandtmp.$Hislands[$i]->{'id'}")) { $HerrorNum = '212'; return 0; }
				if(!rename("${HtempdirName}/islandtmp.$Hislands[$i]->{'id'}", "${HdirName}/island.$Hislands[$i]->{'id'}")) {
					$HerrorNum = '222';
					return 0;
				}
			}
		}
	}
	
	if(($mode == 0)||($mode == 3)) {
		if(!(-s "${HtempdirName}/submaptmp.0")) { $HerrorNum = '512'; return 0; }
		if(!rename("${HtempdirName}/submaptmp.0", "${HdirName}/submap.0")) { $HerrorNum = '522'; return 0; }
	}
	if(($mode == 0)||($mode == 4)) {
		if(!(-s "${HtempdirName}/submaptmp.1")) { $HerrorNum = '612'; return 0; }
		if(!rename("${HtempdirName}/submaptmp.1", "${HdirName}/submap.1")) { $HerrorNum = '622'; return 0; }
	}
	if(($mode == 0)||($mode == 4)) {
		if(-s "${HtempdirName}/command.tmp") {
			if(!rename("${HtempdirName}/command.tmp", "${HdirName}/command.dat")) { $HerrorNum = '722'; return 0; }
		}
	}
	if($Htournament){
		if(-s "${HtempdirName}/tournament.tmp") {
			if(!rename("${HtempdirName}/tournament.tmp", "${HdirName}/tournament.dat")) { $HerrorNum = '822'; return 0; }
		}
		if(-s "${HtempdirName}/fight.tmp") {
			if(!rename("${HtempdirName}/fight.tmp", "${HdirName}/fight.log")) { $HerrorNum = '922'; return 0; }
		}
	}
#	if(($mode == 0) && ($Hrsswrite)){
#		if(!(-s "${HtempdirName}/rss.tmp")) { $HerrorNum = '612'; return 0; }
#		if(!rename("${HtempdirName}/rss.tmp", "${HdirName}/rss.dat")) { $HerrorNum = '622'; return 0; }
#	}
	
	return 1;

}

# ��ҤȤĽ񤭹���
sub writeIsland {
	my($island, $num, $mode) = @_;
	if($mode == 0){
	my($score);
	$score = int($island->{'score'});
	print OUT $island->{'name'} . ",$score\n";
	print OUT $island->{'id'} . "\n";
	print OUT $island->{'ownername'} . "\n";
	print OUT $island->{'prize'} . "\n";
	print OUT $island->{'absent'} . "\n";
	my($comments) = "$island->{'comment'}<>$island->{'commentLabel0'}<>$island->{'commentLabel1'}<>$island->{'commentLabel2'}<>$island->{'commentLabel3'}<>$island->{'commentLabel4'}";
	print OUT $comments . "\n";
	print OUT $island->{'password'} . "\n";
	print OUT $island->{'money'} . "\n";
	print OUT $island->{'food'} . "\n";
	print OUT $island->{'pop'} . "," . $island->{'popspace'} . "," . $island->{'spa'} . "\n";
	print OUT $island->{'area'} . "\n";
	print OUT $island->{'farm'} . "\n";
	my($pastweather) = $island->{'pastweather'};
	printf OUT ("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n",
		$island->{'weather'},
		$pastweather->[0],
		$pastweather->[1],
		$pastweather->[2],
		$pastweather->[3],
		$pastweather->[4],
		$pastweather->[5],
		$pastweather->[6],
		$pastweather->[7],
		$pastweather->[8],
		$pastweather->[9],
		$pastweather->[10]
	);
	print OUT $island->{'factory'} . "\n";
	print OUT $island->{'port'} . "\n";
	print OUT $island->{'mountain'} . "\n";
	print OUT $island->{'tower'} . "\n";
	print OUT $island->{'yousyoku'} . "\n";
	print OUT $island->{'turnsu'} . "," . $island->{'zyuni'} . "," . $island->{'kaisi'} . "\n";
	print OUT $island->{'winP'} . "," . $island->{'loseP'} . "," . $island->{'winS'} . "," . $island->{'possess'} . "\n";
	print OUT $island->{'MissileK'} . "," . $island->{'MissileA'} . "\n";
	print OUT $island->{'ally'} . "\n";
	my($present) = $island->{'present'};
	printf OUT ("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n", 
		$present->[0],
		$present->[1],
		$present->[2],
		$present->[3],
		$present->[4],
		$present->[5],
		$present->[6],
		$present->[7],
		$present->[8],
		$present->[9],
		$present->[10],
		$present->[11],
		$present->[12],
		$present->[13]
	);
	
	print OUT $island->{'allex'} . "\n";
	print OUT $island->{'status'} . "\n";
	print OUT $island->{'evil'} . "\n";
	print OUT $island->{'monsfound'} . "\n";
	print OUT $island->{'order'} . "\n";
	print OUT $island->{'x'} . "," . $island->{'y'} . "\n";
	
	print OUT $island->{'ore'} . "\n";
	print OUT $island->{'weapon'} . "\n";
	print OUT $island->{'oil'} . "\n";
	print OUT $island->{'oilfield'} . "\n";
	
	# ���åХȥ���
	my($monster) = $island->{'monster'};
	printf OUT ("%d,%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n", 
		$monster->[0],
		$monster->[1],
		$monster->[2],
		$monster->[3],
		$monster->[4],
		$monster->[5],
		$monster->[6],
		$monster->[7],
		$monster->[8],
		$monster->[9],
		$monster->[10],
		$monster->[11],
		$monster->[12],
		$monster->[13]
	);
	print OUT $island->{'monsurl'} . "\n";

	
	if($Htournament){
		# �ʰץȡ��ʥ���
		print TOUT $island->{'fight_id'} . "\n";
		print TOUT "\n";
		print TOUT "\n";
		print TOUT "\n";
		print TOUT "\n";
	}
	}
	
	# �Ϸ�
	if(($num <= -1) || ($num == $island->{'id'})) {
		my($retry) = $HretryCount;
		if($mode == 3){
			# ����ޥå�
			while(!open(IOUT, ">${HtempdirName}/submaptmp.0")) {
				$retry--;
				return 0 if($retry <= 0);
				# 0.2 �� sleep
				select undef, undef, undef, 0.2;
			}
		}elsif($mode == 4){
			while(!open(IOUT, ">${HtempdirName}/submaptmp.1")) {
				$retry--;
				return 0 if($retry <= 0);
				# 0.2 �� sleep
				select undef, undef, undef, 0.2;
			}
		}else{
			while(!open(IOUT, ">${HtempdirName}/islandtmp.$island->{'id'}")) {
				$retry--;
				return 0 if($retry <= 0);
				# 0.2 �� sleep
				select undef, undef, undef, 0.2;
			}
		}

		my($land, $landValue, $land2, $landValue2, $nation);
		$land		= $island->{'land'};
		$landValue	= $island->{'landValue'};
		$land2		= $island->{'land2'};
		$landValue2	= $island->{'landValue2'};
		$nation		= $island->{'nation'};
		
		# �ϲ�
		my($ugL,$ugV,$ugX,$ugY) = ($island->{'ugL'},$island->{'ugV'},$island->{'ugX'},$island->{'ugY'});
		
		my($x, $y);
		if($mode == 3){
			# ����ޥå�
			for($y = 0; $y < $HislandSize; $y++) {
				for($x = 0; $x < $HislandSize; $x++) {
					printf IOUT ("%02x%04x%02x%04x%02x", $land->[$x][$y], $landValue->[$x][$y], $land2->[$x][$y], $landValue2->[$x][$y], $nation->[$x][$y]);
				}
				print IOUT "\n";
			}
			print IOUT $island->{'space'} . "\n";
			print IOUT $island->{'solarwind'} . "\n";
			print IOUT $island->{'area'} . "\n";
			print IOUT $island->{'pop'} . "\n";
			print IOUT $island->{'farm'} . "\n";
			print IOUT $island->{'factory'} . "\n";
			print IOUT $island->{'food'} . "," . $island->{'foodP'} . "," . $island->{'foodC'} . "\n";
			
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
		}elsif($mode == 4){
			# ����ޥå�
			for($y = 0; $y < $HoceanSize; $y++) {
				for($x = 0; $x < $HoceanSize; $x++) {
					printf IOUT ("%02x%04x%02x%04x%02x", $land->[$x][$y], $landValue->[$x][$y], $land2->[$x][$y], $landValue2->[$x][$y], $nation->[$x][$y]);
				}
				print IOUT "\n";
			}
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
			print IOUT "0\n";
		}else{
			# �̾�ޥå�
			for($y = 0; $y < $HislandSize; $y++) {
				for($x = 0; $x < $HislandSize; $x++) {
					printf IOUT ("%02x%04x%02x%04x%02x", $land->[$x][$y], $landValue->[$x][$y], $land2->[$x][$y], $landValue2->[$x][$y], $nation->[$x][$y]);
				}
				print IOUT "\n";
			}
			# �ϲ�
			my($i);
			for($i = 0; $i < $HugMax; $i++) {
				# �����å�
				if(($land->[$ugX->[$i]][$ugY->[$i]] != $HlandDokan) && ($land2->[$ugX->[$i]][$ugY->[$i]] != $HlandDokan)){
					# �и����ʤ��Τǥ��ꥢ����
					$ugX->[$i] = "";
					$ugY->[$i] = "";
				}
				for($x = 0; $x < 9; $x++) {
					printf IOUT ("%01x%02x", $ugL->[$i][$x], $ugV->[$i][$x]);
				}
				print IOUT "," . $ugX->[$i] . "," . $ugY->[$i] . "\n";
			}
			# ���ޥ��
			print IOUT $island->{'cmdTurn'} . "\n";
			print IOUT $island->{'cmdIp'} . "\n";
			print IOUT $island->{'cmdId'} . "\n";
			print IOUT $island->{'cmdtime'} . "\n";
			print IOUT "\n";
			my($command, $i);
			$command = $island->{'command'};
			for($i = 0; $i < $HcommandMax; $i++) {
				chomp($command->[$i]->{'ip'});
				printf IOUT ("%d,%d,%d,%d,%d,%d,%d\n", 
					 $command->[$i]->{'kind'},
					 $command->[$i]->{'target'},
					 $command->[$i]->{'x'},
					 $command->[$i]->{'y'},
					 $command->[$i]->{'arg'},
					 $command->[$i]->{'tx'},
					 $command->[$i]->{'ty'}
				);
			}
		}

		# ������Ǽ���
		my($lbbs) = $island->{'lbbs'};
		for($i = 0; $i < $HlbbsMax; $i++) {
			print IOUT $lbbs->[$i] . "\n";
		}

		close(IOUT);
	}
	return 1;
}

# �ǥ��쥯�ȥ�ä�
sub myrmtree {
	my($dn) = @_;
	opendir(DIN, "$dn/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		unlink("$dn/$fileName");
	}
	closedir(DIN);
	rmdir($dn);
}

#----------------------------------------------------------------------
# ������
#----------------------------------------------------------------------

# CGI���ɤߤ���
sub cgiInput {
	my($line, $getLine);

	# ���Ϥ������ä����ܸ쥳���ɤ�EUC��
	$line = <>;
	$line =~ tr/+/ /;
#	$line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	$line =~ s/%([a-fA-F0-9]{2})/pack(H2, $1)/eg;
#	$line = jcode::euc($line);
	jcode::convert(\$line, 'euc');
	$line =~ s/[\x00-\x1f\,]//g;

	# GET�Τ�Ĥ�������
	$getLine = $ENV{'QUERY_STRING'};

#	HdebugOut("POST=$line");
#	HdebugOut("GET =$getLine");

	# �оݤ���
	if($line =~ /CommandButton([0-9]+)=/) {
		# ���ޥ�������ܥ���ξ��
		$HcurrentID = $1;
	}

	if($line =~ /ISLANDNAME=([^\&]*)\&/){
		# ̾������ξ��
		$HcurrentName = cutColumn($1, 32);
	}

	if($line =~ /OWNERNAME=([^\&]*)\&/){
		# �����ʡ�̾�ξ��
		$HcurrentOwnerName = cutColumn($1, 32);
	}

	if($line =~ /ISLANDID=([0-9]+)\&/){
		# ����¾�ξ��
		$HcurrentID = $1;
	}

	if($line =~ /LBBSTYPE=([^\&]*)\&/){
		# �Ǽ��Ĥ��̿�����
		$HlbbsType = $1;
	}

	# �ѥ����
	if($line =~ /OLDPASS=([^\&]*)\&/) {
		$HoldPassword = $1;
		$HdefaultPassword = $1;
	}
	if($line =~ /PASSWORD=([^\&]*)\&/) {
		$HinputPassword = $1;
		$HdefaultPassword = $1;
	}
	if($line =~ /PASSWORD2=([^\&]*)\&/) {
		$HinputPassword2 = $1;
	}

	# ��å�����
	if($line =~ /MESSAGE=([^\&]*)\&/) {
		$Hmessage = cutColumn($1, 120);
	}

	# �����ȥ�٥�
	if($line =~ /COMMENT_LABEL0=([^\&]*)\&/) {
		$HcommentLabel0 = $1;
	}
	if($line =~ /COMMENT_LABEL1=([^\&]*)\&/) {
		$HcommentLabel1 = $1;
	}
	if($line =~ /COMMENT_LABEL2=([^\&]*)\&/) {
		$HcommentLabel2 = $1;
	}
	if($line =~ /COMMENT_LABEL3=([^\&]*)\&/) {
		$HcommentLabel3 = $1;
	}
	if($line =~ /COMMENT_LABEL4=([^\&]*)\&/) {
		$HcommentLabel4 = $1;
	}
	
	# ��������
	if($line =~ /MONSNAME=([^\&]*)\&/) {
		$Hmonsname = cutColumn($1, 32);
	}
	if($line =~ /MONSURL=([^\&]*)\&/) {
		$Hmonsurl = cutColumn($1, 80);
	}
	
	# �ʣ���᥹����ץȥ⡼��
	if($line =~ /JAVAMODE=(cgi|java)/) {
		$HjavaMode = $1;
	}
	if($getLine =~ /JAVAMODE=(cgi|java)/) {
		$HjavaMode = $1;
	}
	# ��Ʊ���̿��ե饰
	if($line =~ /async=true\&/) {
		$Hasync = 1;
	}
	if($line =~ /CommandJavaButton([0-9]+)=/) {
		# ���ޥ�������ܥ���ξ��ʣʣ���᥹����ץȡ�
		$HcurrentID = $1;
		$defaultID = $1;
	}

	# ������Ǽ���
	if($line =~ /LBBSNAME=([^\&]*)\&/) {
		$HlbbsName = $1;
		$HdefaultName = $1;
	}
	if($line =~ /LBBSMESSAGE=([^\&]*)\&/) {
		$HlbbsMessage = cutColumn($1, 100);
	}

	# �������������
	if($line =~ /IMGLINEMAC=([^&]*)\&/) {
		my($flag) = $1;
		if($flag eq ''){
			$flag = $imageDir;
		} else {
			$flag =~ s/ /%20/g;
			$flag = 'file:///' . $flag;
		}
		$HimgLine = $flag;
	} elsif($line =~ /IMGLINE=([^&]*)\&/) {
		my($flag) = substr($1, 0 , -10);
		$flag =~ tr/\\/\//;
		if($flag eq ''){
			$flag = $imageDir;
		} else {
			$flag =~ s/ /%20/g;
			$flag = 'file:///' . $flag;
		}
		$HimgLine = $flag;
	}

	# ���Ϥ�Ʃ���������Ѥ��뤫
	if($line =~ /RMYSHIP=([^&]*)\&/) {
		$HmyshipFlg = 1;
		$Hmyship = $1;
	}

	# main mode�μ���
	if($line =~ /TurnButton/) {
		if($Hdebug == 1) {
			$HmainMode = 'Hdebugturn';
		}
	} elsif($getLine =~ /kani/) {
		$HmainMode = 'kani';
	} elsif($getLine =~ /alist=([0-9]*)/) {
		$HmainMode = 'alist';
		$Halistmode = $1;
	} elsif($getLine =~ /$Hurlownermode=([0-9]*)/) {
		$HjavaMode = 'java';
		$defaultID = $1;
		$HcurrentID = $1;
		$HmainMode = 'owner';
		if($getLine =~ /PASSWORD=([^\&]*)\&/) {
			$HinputPassword = $1;
			$HdefaultPassword = $1;
		}
	} elsif($getLine =~ /settei=([^\&]*)/) { # �������������
		$HmainMode = 'settei';
		$HdefaultPassword = $1;
	} elsif($line =~ /SIGHTMODE=on/) {
		# ǧ�ڴѸ��⡼��
		if($line =~ /PISLANDID=([0-9]+)\&/){
			$HprintID = $1;# ��ʬ��ID
		}
		$HmainMode = 'print';
	} elsif($line =~ /OwnerButton/) {
		$HmainMode = 'owner';
	} elsif($getLine =~ /SUCCESSIVE=([0-9]*)/) { # neo_otacky�᤬����
		$HmainMode = 'rekidai';
	} elsif($getLine =~ /Sight=([0-9]*)/) {
		$HmainMode = 'print';
		$HcurrentID = $1;
	} elsif($getLine =~ /IslandMap=([0-9]*)/) {
		$HmainMode = 'landmap';
		if($1 >= 1000){
			# �ϲ�
			$Hugmode = 1;
			$HcurrentID = $1 - 1000;
		}else{
			$HcurrentID = $1;
		}
	} elsif($line =~ /NewIslandButton/) {
		$HmainMode = 'new';
		$line =~ /TOURNAMENTMONS=([0-9]*)/;
		$HtournamentmonsId = $1;
	} elsif($line =~ /LbbsButton(..)([0-9]*)/) {
		$HmainMode = 'lbbs';
		if($1 eq 'SS') {
			# �Ѹ���
			$HlbbsMode = 0;
		} elsif($1 eq 'OW') {
			# ���
			$HlbbsMode = 1;
		} elsif($1 eq 'FO') {
			# ¾�����
			$HlbbsMode = 3;
			$HforeignerID = $HcurrentID;
		} elsif($1 eq 'FD') {
			# ¾�������
			$HlbbsMode = 4;
			$HforeignerID = $HcurrentID;
		} else {
			# ���
			$HlbbsMode = 2;
		}
		$HcurrentID = $2;

		# ������⤷��ʤ��Τǡ��ֹ�����
		$line =~ /NUMBER=([^\&]*)\&/;
		$HcommandPlanNumber = $1;
		
		$line =~ /LBBSLIST=([^\&]*)\&/;
		$HlbbsMode2 = $1;
	} elsif($line =~ /ChangeInfoButton/) {
		$HmainMode = 'change';
	} elsif($line =~ /MessageButton([0-9]*)/) {
		$HmainMode = 'comment';
		$HcurrentID = $1;
	} elsif($line =~ /CLbbsRButton([0-9]*)/) {
		$HmainMode = 'clbbs';
		$HcurrentID = $1;
	} elsif($line =~ /customButton([0-9]*)/) {
		$HmainMode = 'custom';
		$HcurrentID = $1;
	} elsif($line =~ /customMButton([0-9]*)/) {
		$HmainMode = 'custom2';
		$HcurrentID = $1;
		$Hcustom[3] = 1  if($line =~ /custom3=on/);
		$Hcustom[4] = 1  if($line =~ /custom4=on/);
		$Hcustom[5] = 1  if($line =~ /custom5=on/);
		$Hcustom[6] = 1  if($line =~ /custom6=on/);
		$Hcustom[7] = 1  if($line =~ /custom7=on/);
		$Hcustom[8] = 1  if($line =~ /custom8=on/);
		$Hcustom[9] = 1  if($line =~ /custom9=on/);
		$Hcustom[10] = 1 if($line =~ /custom10=on/);
		$Hcustom[11] = 1 if($line =~ /custom11=on/);
	} elsif($line =~ /MonsButton([0-9]*)/) {
		$HmainMode = 'monsedit';
		$HcurrentID = $1;
	} elsif($line =~ /CommandJavaButton/) {
		$HmainMode = 'commandJava';
		$line =~ /COMARY=([^\&]*)\&/;
		$HcommandComary = $1;
		
		$line =~ /COMMAND=([^\&]*)\&/;
		$HcommandKind = $1;
		$HdefaultKind = $1;
		$line =~ /AMOUNT=([^\&]*)\&/;
		$HcommandArg = $1;
		$line =~ /TARGETID=([^\&]*)\&/;
		$HcommandTarget = $1;
		$defaultTarget = $1;
		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /POINTTX=([^\&]*)\&/;
		$HcommandTX = $1;
		$HdefaultTX = $1;
		$line =~ /POINTTY=([^\&]*)\&/;
		$HcommandTY = $1;
		$HdefaultTY = $1;
		
	} elsif($line =~ /CommandButton/) {
		if($HjavaMode eq 'java'){
			$HmainMode = 'command2';
		}else{
			$HmainMode = 'command';
		}
		# ���ޥ�ɥ⡼�ɤξ�硢���ޥ�ɤμ���
		$line =~ /NUMBER=([^\&]*)\&/;
		
		$HcommandPlanNumber = $1;
		$line =~ /COMMAND=([^\&]*)\&/;
		$HcommandKind = $1;
		$HdefaultKind = $1;
		$line =~ /AMOUNT=([^\&]*)\&/;
		$HcommandArg = $1;
		$line =~ /TARGETID=([^\&]*)\&/;
		$HcommandTarget = $1;
		$defaultTarget = $1;
		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /POINTTX=([^\&]*)\&/;
		$HcommandTX = $1;
		$HdefaultTX = $1;
		$line =~ /POINTTY=([^\&]*)\&/;
		$HcommandTY = $1;
		$HdefaultTY = $1;

		$line =~ /COMMANDMODE=(write|insert|delete)/;
		$HcommandMode = $1;
	} elsif ($line =~ /camp([0-9]*)/) {
		$HmainMode = 'camp';
		$HcurrentID = $1;
# �񸻼����
	} elsif($getLine =~ /Exchange=([0-9]*)/) {
		$HmainMode = 'exchange';
		$HexchangeMode = 'show';
	} elsif($line =~ /ExchangeButton/) {
		$HmainMode = 'exchange';
		$HexchangeMode = 'add';

		$line =~ /EXC_SELL=([^\&]*)\&/;
		$HexchangeSell = $1;
		$line =~ /EXC_SELL1=([^\&]*)\&/;
		$HexchangeSellCost = $1 * 100;
		$line =~ /EXC_SELL0=([^\&]*)\&/;
		$HexchangeSellCost += $1;
		$line =~ /EXC_BUY=([^\&]*)\&/;
		$HexchangeBuy = $1;
		$line =~ /EXC_BUY1=([^\&]*)\&/;
		$HexchangeBuyCost = $1 * 100;
		$line =~ /EXC_BUY0=([^\&]*)\&/;
		$HexchangeBuyCost += $1;
	} elsif($line =~ /ExchangeBidButton/) {
		$HmainMode = 'exchange';
		$HexchangeMode = 'bid';
		$line =~ /EXC_SELL1=([^\&]*)\&/;
		$HexchangeSellCost = $1 * 100;
		$line =~ /EXC_SELL0=([^\&]*)\&/;
		$HexchangeSellCost += $1;
		$line =~ /EXC_ID=([^\&]*)\&/;
		$HexchangeBidID = $1;
		$HexchangeCon = 1;
	} elsif($line =~ /ExchangeBid2Button/) {
		$HmainMode = 'exchange';
		$HexchangeMode = 'bid';
		$line =~ /EXC_SELL=([^\&]*)\&/;
		$HexchangeSellCost = $1;
		$line =~ /EXC_ID=([^\&]*)\&/;
		$HexchangeBidID = $1;
		$HexchangeCon = 0;
	} elsif($line =~ /ExchangeDelButton/) {
		$HmainMode = 'exchange';
		$HexchangeMode = 'del';

		$line =~ /EXC_ID=([^\&]*)\&/;
		$HexchangeDelID = $1;

# �ܺ�ɽ��
	} elsif($getLine =~ /list=([0-9]*)/) {
		$HlistID = $1;
		$HmainMode = 'list';

# ����ޥå�ɽ��
	} elsif($getLine =~ /space=([0-9]*)/) {
		$HspaceID = $1;
		$HmainMode = 'space';

# ����ޥå�ɽ��
	} elsif($getLine =~ /Ocean=([0-9]*)/) {
		$HmainMode = 'ocean';

# BattleField�����⡼��
	} elsif($getLine =~ /Bfield=([^\&]*)/) {
		# �ǽ�ε�ư
		$HmainMode = 'bfield';
		$HbfieldMode = 0;
		$HdefaultPassword = $1;
	} elsif($line =~ /Bfield=([^\&]*)\&/) {
		# BattleField�����ܥ��󤬲����줿��ư
		$HmainMode = 'bfield';
		if($line =~ /LBFIELD=([0-9]+)\&/){
			$HbfieldMode = $1;
		}else{
			$HbfieldMode = 0;
		}
		$HdefaultPassword = $1;
# ��������ǧ�⡼��
	} elsif($getLine =~ /SetupV=([^\&]*)/) {
		$HmainMode = 'setupv';
		$HdefaultPassword = $1;

# �ʰץȡ��ʥ���
} elsif($getLine =~ /LoseMap=([0-9]*)/) {
	$HmainMode = 'FightIsland';
	$HcurrentID = $1;
} elsif($getLine =~ /FightLog/) {
	$HmainMode = 'FightView';

# �����ͤˤ��ץ쥼��ȥ⡼��
	} elsif($getLine =~ /Present/) {
		# �ǽ�ε�ư
		$HmainMode = 'present';
		$HpresentMode = 0;
	} elsif($line =~ /Present/) {
		# �ץ쥼��ȥܥ��󤬲����줿��ư
		$HmainMode = 'present';
		$HpresentMode = 1;
		($HpresentMoney) = ($line =~ /PRESENTMONEY=([^\&]*)\&/);
		($HpresentFood ) = ($line =~ /PRESENTFOOD=([^\&]*)\&/);
		($HpresentLog)   = ($line =~ /PRESENTLOG=([^\&]*)\&/);

# �����ͤˤ�����ۥ⡼��
	} elsif($getLine =~ /Punish=([^\&]*)/) {
		# �ǽ�ε�ư
		$HmainMode = 'punish';
		$HpunishMode = 0;
		$HdefaultPassword = $1;
	} elsif($line =~ /Punish=([^\&]*)\&/) {
		# ���ۥܥ��󤬲����줿��ư
		$HmainMode = 'punish';
		$HpunishMode = 1;
		$HdefaultPassword = $1;

		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /PUNISHID=([^\&]*)\&/;
		$HpunishID = $1;
# �����ͤˤ���Ϸ��ѹ��⡼��
	} elsif($getLine =~ /Lchange=([^\&]*)/) {
		# �ǽ�ε�ư
		$HmainMode = 'lchange';
		$HlchangeMode = 0;
		$HdefaultPassword = $1;
	} elsif($line =~ /LchangeButtonM=([^\&]*)\&/) {
		# �ޥå��ѹ�
		$HmainMode = 'lchange';
		$HlchangeMode = 0;
		$line =~ /Lchange=([^\&]*)\&/;
		$HdefaultPassword = $1;
	} elsif($line =~ /Lchange=([^\&]*)\&/) {
		# �ѹ��ܥ��󤬲����줿��ư
		$HmainMode = 'lchange';
		$HlchangeMode = 1;
		$HdefaultPassword = $1;

		$line =~ /POINTX=([^\&]*)\&/;
		$HcommandX = $1;
		$HdefaultX = $1;
		$line =~ /POINTY=([^\&]*)\&/;
		$HcommandY = $1;
		$HdefaultY = $1;
		$line =~ /LCHANGEKIND=([^\&]*)\&/;
		$HlchangeKIND = $1;
		$line =~ /LCHANGEVALUE=([^\&]*)\&/;
		$HlchangeVALUE = $1;
# �����ͤˤ��Ƽ���ǡ����ѹ��⡼��
	} elsif($getLine =~ /Ichange=([^\&]*)/) {
		# �ǽ�ε�ư
		$HmainMode = 'ichange';
		$HichangeMode = 0;
		$HdefaultPassword = $1;
	} elsif($line =~ /Ichange=([^\&]*)\&/) {
		$HmainMode = 'ichange';
		$HichangeMode = 1;
		$HdefaultPassword = $1;
		$line =~ /ICID=([^\&]*)\&/;
		$HcurrentID = $1;
		$line =~ /ICMONEY=([^\&]*)\&/;
		$Hicmoney = $1;
		$line =~ /ICFOOD=([^\&]*)\&/;
		$Hicfood = $1;
		$line =~ /ICWEAPON=([^\&]*)\&/;
		$Hicweapon = $1;
		$line =~ /ICEVIL=([^\&]*)\&/;
		$Hicevil = $1;
		$Hicspace = 1 if($line =~ /ICSPACE=on/);
		$line =~ /ICALLY=([^\&]*)\&/;
		$Hically = $1;
# �����ͤˤ�뤢������⡼��
	} elsif($getLine =~ /Pdelete=([^\&]*)/) {
		# �ǽ�ε�ư
		$HmainMode = 'predelete';
		$HpreDeleteMode = 0;
		$HdefaultPassword = $1;
	} elsif($line =~ /Pdelete=([^\&]*)\&/) {
		# �ѹ��ܥ��󤬲����줿��ư
		$HmainMode = 'predelete';
		$HpreDeleteMode = 1;
		$HdefaultPassword = $1;
	} else {
		$HmainMode = 'top';
	}

	if($line =~ /SKIN=([^\&]*)\&/) {
		my($flag) = $1;
		if(($flag eq 'del') || ($flag eq '')){
			$flag = $HcssFile;
		}
		$HskinName = $flag;
	}

# �ǥХå�
	if($getLine =~ /debug=([0-9]*)/) {
		$HdebugMode = $1;
	}
}


#cookie����
sub cookieInput {
	my($cookie);

	$cookie = jcode::euc($ENV{'HTTP_COOKIE'});

	if($cookie =~ /${HthisFile}OWNISLANDID=\(([^\)]*)\)/) {
		$defaultID = $1;
	}
	if($cookie =~ /${HthisFile}OWNISLANDPASSWORD=\(([^\)]*)\)/) {
		$HdefaultPassword = $1;
	}
	if($cookie =~ /${HthisFile}TARGETISLANDID=\(([^\)]*)\)/) {
		$defaultTarget = $1;
	}
	if($cookie =~ /${HthisFile}LBBSNAME=\(([^\)]*)\)/) {
		$HdefaultName = $1;
	}
	if($cookie =~ /${HthisFile}POINTX=\(([^\)]*)\)/) {
		$HdefaultX = $1;
	}
	if($cookie =~ /${HthisFile}POINTY=\(([^\)]*)\)/) {
		$HdefaultY = $1;
	}
	if($cookie =~ /${HthisFile}POINTTX=\(([^\)]*)\)/) {
		$HdefaultTX = $1;
	}
	if($cookie =~ /${HthisFile}POINTTY=\(([^\)]*)\)/) {
		$HdefaultTY = $1;
	}
	if($cookie =~ /${HthisFile}KIND=\(([^\)]*)\)/) {
		$HdefaultKind = $1;
	}
	if($cookie =~ /${HthisFile}JAVAMODESET=\(([^\)]*)\)/) {
		$HjavaModeSet = $1;
	}
	# �������������
	if($cookie =~ /${HthisFile}IMGLINE=\(([^\)]*)\)/) {
		$HimgLine = $1;
	}
	# ���Ϥ�Ʃ���������Ѥ��뤫
	if($cookie =~ /${HthisFile}MYSHIP=\(([^\)]*)\)/) {
		$Hmyship = $1;
	}
	# �������륷����
	if($cookie =~ /${HthisFile}SKIN=\(([^\)]*)\)/) {
		$HskinName = $1;
	}
}

#cookie����
sub cookieOutput {
	my($cookie, $info);

	# �ä�����¤�����
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	gmtime(time + 30 * 86400); # ���� + 30��

	# 2������
	$year += 1900;
	$date = "0$date" if($date < 10);
	$hour = "0$hour" if($hour < 10);
	$min  = "0$min" if($min < 10);
	$sec  = "0$sec" if($sec < 10);

	# ������ʸ����
	$day = ("Sunday", "Monday", "Tuesday", "Wednesday",
			"Thursday", "Friday", "Saturday")[$day];

	# ���ʸ����
	$mon = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
			"Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[$mon];

	# �ѥ��ȴ��¤Υ��å�
	$info = "; expires=$day, $date\-$mon\-$year $hour:$min:$sec GMT\n";
	$cookie = '';

	if(($HcurrentID) && ($HmainMode eq 'owner')){
		$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDID=($HcurrentID) $info";
	}
	if($HinputPassword) {
		$cookie .= "Set-Cookie: ${HthisFile}OWNISLANDPASSWORD=($HinputPassword) $info";
	}
	if($HcommandTarget) {
		$cookie .= "Set-Cookie: ${HthisFile}TARGETISLANDID=($HcommandTarget) $info";
	}
	if($HlbbsName) {
		$cookie .= "Set-Cookie: ${HthisFile}LBBSNAME=($HlbbsName) $info";
	}
	if($HcommandX) {
		$cookie .= "Set-Cookie: ${HthisFile}POINTX=($HcommandX) $info";
	}
	if($HcommandY) {
		$cookie .= "Set-Cookie: ${HthisFile}POINTY=($HcommandY) $info";
	}
	if($HcommandTX) {
		$cookie .= "Set-Cookie: ${HthisFile}POINTTX=($HcommandTX) $info";
	}
	if($HcommandTY) {
		$cookie .= "Set-Cookie: ${HthisFile}POINTTY=($HcommandTY) $info";
	}
	if($HcommandKind) {
		# ��ư�ϰʳ�
		$cookie .= "Set-Cookie: ${HthisFile}KIND=($HcommandKind) $info";
	}
	if($HjavaMode) {
		$cookie .= "Set-Cookie: ${HthisFile}JAVAMODESET=($HjavaMode) $info";
	}
	# �������������
	if($HimgLine) {
		$cookie .= "Set-Cookie: ${HthisFile}IMGLINE=($HimgLine) $info";
	}
	# ���Ϥ�Ʃ���������Ѥ��뤫
	if($HmyshipFlg) {
		$cookie .= "Set-Cookie: ${HthisFile}MYSHIP=($Hmyship) $info";
	}
	# �������륷����
	if($HskinName) {
		$cookie .= "Set-Cookie: ${HthisFile}SKIN=($HskinName) $info";
	}
	out($cookie);
}

#----------------------------------------------------------------------
# �桼�ƥ���ƥ�
#----------------------------------------------------------------------
sub hakolock {
	if($lockMode == 1) {
		# directory����å�
		return hakolock1();
	} elsif($lockMode == 2) {
		# flock����å�
		return hakolock2();
	} elsif($lockMode == 3) {
		# symlink����å�
		return hakolock3();
	} elsif($lockMode == 4) {
		# �̾�ե����뼰��å�
		return hakolock4();
	} else {
		# rename����å�
		$lfh = hakolock5() or die return 0;
		return 1;
	}
}

sub hakolock1 {
	# ��å���
	if(mkdir('hakojimalock', $HdirMode)) {
		# ����
		return 1;
	} else {
		# ����
		my($b) = (stat('hakojimalock'))[9];
		if(($b > 0) && ((time() -  $b)> $unlockTime)) {
			# �������
			unlock();

			# �إå�����
			tempHeader();

			# ���������å�����
			tempUnlock();

			# �եå�����
			tempFooter();

			# ��λ
			exit(0);
		}
		return 0;
	}
}

sub hakolock2 {
	open(LOCKID, '>>hakojimalockflock');
	if(flock(LOCKID, 2)) {
		# ����
		return 1;
	} else {
		# ����
		return 0;
	}
}

sub hakolock3 {
	# ��å���
	if(symlink('hakojimalockdummy', 'hakojimalock')) {
		# ����
		return 1;
	} else {
		# ����
		my($b) = (lstat('hakojimalock'))[9];
		if(($b > 0) && ((time() -  $b)> $unlockTime)) {
			# �������
			unlock();

			# �إå�����
			tempHeader();

			# ���������å�����
			tempUnlock();

			# �եå�����
			tempFooter();

			# ��λ
			exit(0);
		}
		return 0;
	}
}

sub hakolock4 {
	# ��å���
	if(unlink('lockfile')) {
		# ����
		open(OUT, '>lockfile.lock');
		print OUT time;
		close(OUT);
		return 1;
	} else {
		# ��å����֥����å�
		if(!open(IN, 'lockfile.lock')) {
			return 0;
		}
		my($t);
		$t = <IN>;
		close(IN);
		if(($t != 0) && (($t + $unlockTime) < time)) {
			# 120�ðʾ�вᤷ�Ƥ��顢����Ū�˥�å��򳰤�
			unlock();

			# �إå�����
			tempHeader();

			# ���������å�����
			tempUnlock();

			# �եå�����
			tempFooter();

			# ��λ
			exit(0);
		}
		return 0;
	}
}

# rename��(Perl��� http://www.din.or.jp/~ohzaki/perl.htm#File_Lock)
sub hakolock5 {
	my %lfh = (dir => "./", basename => "lockfile", timeout => $unlockTime, trytime => 3, @_);
	$lfh{path} = $lfh{dir}.$lfh{basename};

	for (my $i = 0; $i < $lfh{trytime}; $i++, sleep 1) {
		return \%lfh if (rename($lfh{path}, $lfh{current} = $lfh{path} . time));
	}

	opendir(LOCKDIR, $lfh{dir});
	my @filelist = readdir(LOCKDIR);
	closedir(LOCKDIR);

	foreach (@filelist) {
		if (/^$lfh{basename}(\d+)/) {
			return \%lfh if (time - $1 > $lfh{timeout} and
			rename($lfh{dir} . $_, $lfh{current} = $lfh{path} . time));
			last;
		}
	}
	undef;
}

# ��å��򳰤�
sub unlock {
	if($lockMode == 1) {
		# directory����å�
		rmdir('hakojimalock');
	} elsif($lockMode == 2) {
		# flock����å�
		close(LOCKID);
	} elsif($lockMode == 3) {
		# symlink����å�
		unlink('hakojimalock');
	} elsif($lockMode == 4) {
		# �̾�ե����뼰��å�
		my($i);
		$i = rename('lockfile.lock', 'lockfile');
	} else {
		# rename����å�
		rename($lfh->{current}, $lfh->{path});
	}
}

# �����������֤�
sub min {
	return ($_[0] < $_[1]) ? $_[0] : $_[1];
}

# 1000��ñ�̴ݤ�롼����
sub aboutMoney {
	my($m) = @_;
	if($m < 500) {
		return "����500${HunitMoney}̤��";
	} else {
		$m = int(($m + 500) / 1000);
		return "����${m}000${HunitMoney}";
	}
}

# �ڤ�·��
sub cutColumn {
	my($s, $c) = @_;
	if(length($s) <= $c) {
		return $s;
	} else {
		# ���$c�����ˤʤ�ޤ��ڤ���
		my($ss) = '';
		my($count) = 0;
		while($count < $c) {
			$s =~ s/(^[\x80-\xFF][\x80-\xFF])|(^[\x00-\x7F])//;
			if($1) {
				$ss .= $1;
				$count ++;
			} else {
				$ss .= $2;
			}
			$count ++;
		}
		return $ss;
	}
}

# ���̾�������ֹ������(ID����ʤ����ֹ�)
sub nameToNumber {
	# ���礫��õ��
	my($i);
	for($i = 0; $i < $HislandNumber; $i++) {
		return $i if($Hislands[$i]->{'name'} eq $_[0]);
	}
	return -1; # ���Ĥ���ʤ��ä����
}

# ���äξ���
sub monsterSpec {
	my($kind) = int($_[0] / 100);
	# ����,̾��,����
	return ($kind, $HmonsterName[$kind], $_[0] - ($kind * 100));
}

# ������äξ���
sub bigMonsterSpec {
	my($limit) = int($_[0] / 10000);
	my($d) = $_[0] - ($limit * 10000);
	my($hp) = int($d / 100);
	$d = $d - ($hp * 100);
	my($ld) = int($d / 10);
	# ���»���,HP,�Ϸ�,����
	return ($limit, $hp, $ld, $d - ($ld * 10));
}

# ���ξ���
sub shipSpec {
	my($order) = int($_[0] / 10000);
	my($lv2) = $_[0] - ($order * 10000);
	my($hp) = int($lv2 / 1000);
	# ����,�ѵ���,ID
	return ($order, $hp, $lv2 - ($hp * 1000));
}

# ŷ���ξ���
sub weatherinfo {
	my($lv) = @_;

	$lv = 1114 if($lv > 5559); # �����ʿ����λ�

	# ��������ŷ��
	my($kind3) = int($lv / 1000);
	$kind3 = 1 if($kind3 >= 6); # �����ʿ����λ�

	my($lv2) = $lv - ($kind3 * 1000);

	# ������ŷ��
	my($kind2) = int($lv2 / 100);
	$kind2 = 1 if($kind2 >= 6); # �����ʿ����λ�

	my($lv3) = $lv2 - ($kind2 * 100);

	# ŷ��
	my($kind) = int($lv3 / 10);
	$kind = 1 if($kind >= 6); # �����ʿ����λ�

	my($name) = $WeatherName[$kind];# ̾��
	my($hp) = $lv3 - ($kind * 10);# ���פξ���
	return ($kind, $name, $hp, $kind2, $kind3);
}

# �и��Ϥ����٥�򻻽�
sub expToLevel {
	my($kind, $exp) = @_;
	my($i);
	if(($kind == $HlandBase) || ($kind == $HlandSpaceBase)) {
		# �ߥ��������
		for($i = $maxBaseLevel; $i > 1; $i--) {
			return $i if($exp >= $baseLevelUp[$i - 2]);
		}
	}elsif($kind == $HlandDokan){
		# �ϲ� �ڴ�
		return $exp % 100;
	}else{
		# ������Ϥʤ�
		for($i = $maxSBaseLevel; $i > 1; $i--) {
			return $i if($exp >= $sBaseLevelUp[$i - 2]);
		}
	}
	return 1;
}

# ���Ϥγ����Ϸ��ο��������
sub seaAround {
	my($land, $x, $y, $range, $mode) = @_;
	my($i, $count, $sx, $sy);
	$count = 0;
	for($i = 0; $i < $range; $i++) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];
		
		# �Ԥˤ�����Ĵ��
		$sx-- if(!($sy % 2) && ($y % 2));
		
		if(($sx < 0) || ($sx >= $HislandSize) || ($sy < 0) || ($sy >= $HislandSize)) {
			# �ϰϳ��ξ��
			$count++;
		} elsif(($HseaChk[$land->[$sx][$sy]] == 3) && ($mode)){
			# ������Ͻ���
			next;
		} elsif($HseaChk[$land->[$sx][$sy]]) {
			# �����Ϸ��ξ��
			$count++;
		}
	}
	return $count;
}

# (0,0)����(size - 1, size - 1)�ޤǤο��������ŤĽФƤ���褦��
# (@Hrpx, @Hrpy)������
sub makeRandomPointArray {
	# �����
	my($y,$i,$j);
	@Hrpx = (0..$HislandSize-1) x $HislandSize;
	for($y = 0; $y < $HislandSize; $y++) {
		push(@Hrpy, ($y) x $HislandSize);
	}

	# ����åե�
	for ($i = $HpointNumber; --$i; ) {
		$j = int(rand($i+1)); 
		next if($i == $j);
		@Hrpx[$i,$j] = @Hrpx[$j,$i];
		@Hrpy[$i,$j] = @Hrpy[$j,$i];
	}
}
sub makeRandomOceanPointArray {
	# �����
	my($y,$i,$j);
	@HrpxO = (0..$HoceanSize-1) x $HoceanSize;
	for($y = 0; $y < $HoceanSize; $y++) {
		push(@HrpyO, ($y) x $HoceanSize);
	}
	# ����åե�
	for ($i = $HpointOcean; --$i; ) {
		$j = int(rand($i+1)); 
		next if($i == $j);
		@HrpxO[$i,$j] = @HrpxO[$j,$i];
		@HrpyO[$i,$j] = @HrpyO[$j,$i];
	}
}

# 0����(n - 1)�����
sub random {
	return int(rand(1) * $_[0]);
}

# ���������
sub OceanMente {
	my($id) = @_;
	my($x,$y,$i,$j);
	for($y = 0; $y < $HoceanSize; $y++) {
		for($x = 0; $x < $HoceanSize; $x++) {
			if($Hocean->{'nation'}->[$x][$y] == $id){
				if(($Hocean->{'land'}->[$x][$y] == $HlandOPlayer) ||
				   ($Hocean->{'land'}->[$x][$y] == $HlandOcean)){
					$Hocean->{'land'}->[$x][$y] = $HlandOcean;
				}else{
					$Hocean->{'land'}->[$x][$y] = $HlandSea;
				}
				$Hocean->{'landValue'}->[$x][$y] = 0;
				$Hocean->{'land2'}->[$x][$y] = 0;
				$Hocean->{'landValue2'}->[$x][$y] = 0;
				$Hocean->{'nation'}->[$x][$y] = 0;
			}
		}
	}
}

#----------------------------------------------------------------------
# ��ɽ��
#----------------------------------------------------------------------
# �ե������ֹ����ǥ�ɽ��
sub logFilePrint {
	my($fileNumber, $id, $mode) = @_;
	open(LIN, "${HlogdirName}/hakojima.log$_[0]");
	my($line, $m, $turn, $id1, $id2, $message);
	my($set_turn) = 0;
	while($line = <LIN>) {
		$line =~ /^([0-9]*),([0-9]*),([0-9]*),([0-9]*),(.*)$/;
		($m, $turn, $id1, $id2, $message) = ($1, $2, $3, $4, $5);

		# ��̩�ط�
		if($m == 1) {
			next if(($mode == 0) || ($id1 != $id)); # ��̩ɽ�������ʤ�
			$m = "${HtagNumber_}<B>(��̩)</B>${H_tagNumber}��";
		} else {
			$m = '';
		}

		# ɽ��Ū�Τ�
		if($id != 0) {
			next if(($id != $id1) && ($id != $id2));
		}
		
		if($set_turn == 0){
			out("<NOBR><B>=====[<span class=number><FONT SIZE=4> ������$turn </FONT></span>]================================================</B><NOBR><BR>\n");
			$set_turn++;
		}

		# ɽ��
		out("<NOBR>${m}${message}</NOBR><BR>\n");
	}
	close(LIN);
}

#----------------------------------------------------------------------
# �ץ�ե����뤫��������
#----------------------------------------------------------------------
#
# �ץ�ե�������ɤ�ǻ��ꤵ�줿��ID���طʲ���URL���֤�
sub getBGImageUrl {
	my($bgimageid) = @_;

	# ���å������鼫ʬ��ID����
	my($bgcookie, $myId);
	$bgcookie = jcode::euc($ENV{'HTTP_COOKIE'});
	if($bgcookie =~ /OWNISLANDID=\(([^\)]*)\)/) {
		$myId = $1;
		&readProfileMAP($myId);
	}
	if($Hprofile{'BackgroundUse'} == 2) {
		# �طʲ�����ɽ�����ʤ���
		return '';
	}
	if($myId == $bgimageid) {
		# ��ʬ����ξ��
		return $Hprofile{'BackgroundImage'};
	}
	
	&readProfileMAP($bgimageid);
	return $Hprofile{'BackgroundImage'};
}

sub readProfileMAP {
	my($proid) = @_;
	if(!open(PIN, "$HprofileDir/profile${proid}.dat")){
		$Hprofile{'MyHomeImage'} = '';
		$Hprofile{'BackgroundImage'} = '';
		$Hprofile{'BackgroundUse'} = '';
		return 0;
	}

	<PIN>;#lastModify
	<PIN>;#photo
	<PIN>;#address
	<PIN>;#age
	<PIN>;#sex
	<PIN>;#job
	<PIN>;#email
	<PIN>;#icq
	<PIN>;#webtitle
	<PIN>;#webaddr
	<PIN>;#comment
	<PIN>;#bestweb1
	<PIN>;#bestweb2
	<PIN>;#bestweb3
	
	my($HomeImage, $BGImage, $BGImageUse);
	$HomeImage = <PIN>;
	$BGImage   = <PIN>;
	$BGImageUse = int(<PIN>);
	
	chomp($HomeImage);
	chomp($BGImage);
	
	$Hprofile{'MyHomeImage'} = $HomeImage;
	$Hprofile{'BackgroundImage'} = $BGImage;
	$Hprofile{'BackgroundUse'} = $BGImageUse;

	close(PIN);
	return 1;
}

#----------------------------------------------------------------------
# �ƥ�ץ졼��
#----------------------------------------------------------------------
# �إå�
sub tempHeader {
	my($js) = @_;
	# �������������
	$baseIMG = ($HimgLine ne '') ? $HimgLine : $imageDir;
	$baseSKIN = ($HskinName ne '') ? "$imageDir/$HskinName" : "$imageDir/$HcssFile";
	out("Content-type: text/html\n\n");
	return if($Hasync);
	out(<<END);
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<TITLE>$Htitle</TITLE>
<BASE HREF="$baseIMG/">
END
	if($js == 1){
		# js�⡼��
		$Body = "<BODY onload=\"SelectList('');init()\">";
		my($MyImage) = getBGImageUrl($HcurrentID);
		if(substr($MyImage,0,7) eq 'http://'){
			if($MyImage =~ /\.css$/){
				$baseSKIN = $MyImage;
			}else{
				$Body = "<BODY onload=\"SelectList('');init()\" $htmlBgColor BACKGROUND=${MyImage}>";
			}
		}
	}else{
		if(($HmainMode eq 'print') || ($HmainMode eq 'command') ||
			($HmainMode eq 'owner') || ($HmainMode eq 'comment') || ($HmainMode eq 'lbbs')) {
			# ��Υޥåפ�ƤӽФ���
			my($MyImage) = getBGImageUrl($HcurrentID);
			if(substr($MyImage,0,7) eq 'http://'){
				if($MyImage =~ /\.css$/){
					$Body = "<BODY>";
					$baseSKIN = $MyImage;
				}else{
					$Body = "<BODY $htmlBgColor BACKGROUND=${MyImage}>";
				}
			}
		}
	}
	out(<<END);
<link rel="stylesheet" type="text/css" href="$baseSKIN">
</HEAD>
$Body
<DIV ID='BodySpecial'><DIV ID='LinkHead'>
<A HREF="http://t.pos.to/hako/" target="_blank">Ȣ����祹����ץ����۸�</A> /
<A HREF="http://appoh.execweb.cx/hakoniwa/" target="_blank">Ȣ��Java������ץ��� ���۸�</A> /
<A HREF="$HbaseDir/history.cgi?saikin=0" target="_blank"> �Ƕ�ν����</A> /
<A HREF="$HbaseDir/ranking.cgi" target="_blank"> ��󥭥�</A> /
<A HREF="$HbaseDir/profile.cgi" target="_blank"> �ץ�ե�����</A> /
<A HREF="$helpDir" target="_blank">�إ��</A> /
<A HREF="$bbs" target="_blank">�Ǽ���</A> /
<A HREF="$toppage">�ȥåץڡ���</A> /
</DIV><HR>
END
}
# �եå�
sub tempFooter {
	out(<<END);
<HR>
<DIV ID='LinkFoot'>
���ۤ�Ȣ��֤ߤ�ʤ����Ȣ��ʲ�����${versionInfo}<BR>
�����ԡ�$adminName(<A HREF="mailto:$email">$email</A>)<BR>
��¤�������ۤ�Ȣ��ȯ(<A HREF="http://www8.plala.or.jp/nayupon/">http://www8.plala.or.jp/nayupon/</A>)<BR>
Ȣ�����Υڡ���(<A HREF="http://t.pos.to/hako/">http://t.pos.to/hako/</A>)<BR>
�������۸���<A HREF="http://www.propel.ne.jp/~yysky/">K.Y studio</A>/
<A HREF="http://www5b.biglobe.ne.jp/~k-e-i/i.html">Hakoniwa R.A.</A>/
<A HREF="http://www.qoonet.com/hakoniwa.html">Ȣ��QooLand</A>/
<A HREF="http://color.2.pro.tok2.com/">P L U S +</A><BR>
</DIV>
END
##### �ɲ� ����20020307
	if($Hperformance) {
		my($uti, $sti, $cuti, $csti) = times();
		$uti += $cuti;
		$sti += $csti;
		my($cpu) = $uti + $sti;

		# ���ե�����񤭽Ф�(�ƥ��ȷ�¬�ѡ����ʤϥ����Ȥˤ��Ƥ����Ƥ�������)
#		open(POUT,">>cpu-h.log");
#		print POUT "CPU($cpu) : user($uti) system($sti)\n";
#		close(POUT);

		out(<<END);
<DIV align="right">
<SMALL>CPU($cpu) : user($uti) system($sti)</SMALL>
</DIV>
END
	}
#####
	out(<<END);
</BODY>
</HTML>
END
}

# ��å�����
sub tempLockFail {
	# �����ȥ�
	out(<<END);
${HtagBig_}Ʊ�������������顼�Ǥ���<BR>
�֥饦���Ρ����ץܥ���򲡤���<BR>
���Ф餯�ԤäƤ�����٤����������${H_tagBig}$HtempBack
END
}

# �������
sub tempUnlock {
	# �����ȥ�
	out(<<END);
${HtagBig_}����Υ����������۾ｪλ���ä��褦�Ǥ���<BR>
��å�����������ޤ�����${H_tagBig}$HtempBack

END
}

# �ѥ���ɥե����뤬�ʤ�
sub tempNoPasswordFile {
	out(<<END);
${HtagBig_}�ѥ���ɥե����뤬�����ޤ���${H_tagBig}$HtempBack
END
}

# hakojima.dat���ʤ�
sub tempNoDataFile {
	out(<<END);
${HtagBig_}�ǡ����ե����뤬�����ޤ���${H_tagBig}$HtempBack
END
}

# ��������ȯ��
sub tempProblem {
	out(<<END);
${HtagBig_}����ȯ�����Ȥꤢ������äƤ���������${H_tagBig}$HtempBack
END
}

# �񤭹��߼���
sub tempFailWrite {
	out(<<END);
${HtagBig_}�ǡ����ե�����ν񤭹��ߤ˼��Ԥ��ޤ�����(���顼�ֹ� ${HerrorNum})${H_tagBig}$HtempBack
END
}

# ���ƥʥ���
sub mente_mode {
	# �إå�����
	tempHeader() if($_[0]);

	# ��å�����
	out("${HtagBig_}�������ƥʥ���Ǥ���<BR>�ä����Ԥ���������${H_tagBig}");

	# �եå�����
	tempFooter();

	# ��λ
	exit(0);
}

