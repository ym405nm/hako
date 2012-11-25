#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# 入出力用スクリプト(ver1.00)
# 使用条件、使用方法等は、qhako-readme.txtファイルを参照
#----------------------------------------------------------------------
# 究想の箱庭  (ver5.52c)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# ターン差命令
#----------------------------------------------------------------------
# ターン差命令読み込み
sub readCommandLate{
	if(open(Fcom, "<${HdirName}/command.dat")){
		local(@_);
		$HcomLateCt = 0;
		while (<Fcom>){
			chomp;
			@_ = split(',');
			my($obj);
			$obj->{turn} = shift;
			$obj->{turn2} = shift;
			$obj->{id} = shift;
			$obj->{kind} = shift;
			$obj->{target} = shift;
			$obj->{x} = shift;
			$obj->{y} = shift;
			$obj->{arg} = shift;
			$obj->{x2} = shift;
			$obj->{y2} = shift;
			$HcomL[$HcomLateCt] = $obj;
			$HcomLateCt++;
		}
		close(Fcom);
	}
}
# ターン差命令追記
sub addCommandLate{
	my($obj);
	$obj->{turn} = shift;
	$obj->{turn2} = shift;
	$obj->{id} = shift;
	$obj->{kind} = shift;
	$obj->{target} = shift;
	$obj->{x} = shift;
	$obj->{y} = shift;
	$obj->{arg} = shift;
	$obj->{x2} = shift;
	$obj->{y2} = shift;
	$obj->{turn} += $obj->{turn2};
	$HcomL[$HcomLateCt] = $obj;
	$HcomLateCt++;
#	HdebugOut(" ターン差命令追記  $HcomLateCt　" . $obj->{kind});
}
#---------------------------------------------------------------------
#	島データのプルダウンメニュー用
#---------------------------------------------------------------------
# 初期化
sub tempInitialize {
	# 島セレクト(デフォルト自分)
	$HislandList = getIslandList($defaultID);
#	$HtargetList = getIslandList($defaultTarget);
	$HtargetList = getIslandList($defaultID);
}
sub getIslandList {
	my($select) = @_;
	my($list, $list2, $name, $id, $s, $i, $ally);

	#島リストのメニュー
	$list = '';
	$list2 = '';
	$HbattleNumber = 0;
	for($i = 0; $i < $HislandNumber; $i++) {
		$name = $Hislands[$i]->{'name'};
		$id = $Hislands[$i]->{'id'};
		if($Hallyflg){
			$ally = $Hislands[$i]->{'ally'};
			$ally = $Hallymark[$ally] . " ";
		}else{
			$ally = "";
		}
		if($id eq $select) {
			$s = 'SELECTED';
		} else {
			$s = '';
		}
		if($id <= 90){
			$list .= "<OPTION VALUE=\"$id\" $s>${ally}${name}${AfterName}\n";
		}else{
			$HbattleNumber++;
			$list2 .= "<OPTION VALUE=\"$id\" $s>(BF)${name}${AfterName}\n";
		}
	}
	return $list . $list2;
}
#----------------------------------------------------------------------
# パスワードチェック
#----------------------------------------------------------------------
# パスワードエンコード
sub encode {
	if($cryptOn == 1) {
		return crypt($_[0], 'h2');
	} else {
		return $_[0];
	}
}

# マスタパスワードのチェック
sub checkMasterPassword {
	return (crypt($_[0], 'ma') eq $HmasterPassword);
}

# 特殊パスワードのチェック
sub checkSpecialPassword {
	return (crypt($_[0], 'sp') eq $HspecialPassword);
}

# パスワードチェック
sub checkPassword {
	my($p1, $p2) = @_;

	# nullチェック
	return 0 if($p2 eq '');

	# マスターパスワードチェック
	return 2 if(checkMasterPassword($p2));

	# 本来のチェック
	return 1 if($p1 eq encode($p2));

	return 0;
}

# パスワードチェックローカル掲示板用
sub checkPasslocalbbs {
	my($p1, $p2) = @_;
	# nullチェック
	return 0 if($p2 eq '');
	
	# マスターパスワードチェック
	return 3 if(checkMasterPassword($p2));
	
	# ローカル掲示板マスターパスワードチェック
	return 2 if($HbbsmasterPassword eq $p2);
	
	# 本来のチェック
	return 1 if($p1 eq encode($p2));

	return 0;
}

# パスワード間違い
sub tempWrongPassword {
	out(<<END);
${HtagBig_}パスワードが違います。${H_tagBig}$HtempBack
END
}
# ID違いorローカル設定していないorクッキー設定していない
sub tempWrong {
	out(<<END);
${HtagBig_}$_[0]${H_tagBig}$HtempBack
END
}
#----------------------------------------------------------------------
# IPアドレス取得
#----------------------------------------------------------------------
sub get_host {
	$host = "";
	$addr = "";
	if(($Hlipdisp) || ($_[0])) {
		$host = $ENV{'REMOTE_HOST'};
		$addr = $ENV{'REMOTE_ADDR'};

		if ($get_remotehost) {
			if ($host eq "" || $host eq "$addr") {
				$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
			}
		}
		$host = $addr if ($host eq "");
		
		$addr = "(${addr})";
	}
}
#----------------------------------------------------------------------
# アクセスログ取得
#----------------------------------------------------------------------
sub axeslog {
	my @lines;

	my $agent   = $ENV{'HTTP_USER_AGENT'};
	my $addr	= $ENV{'REMOTE_ADDR'};
	my $host	= $ENV{'REMOTE_HOST'};
	my $referer = $ENV{'HTTP_REFERER'} unless($HtopAxes == 1);
	if (($host eq $addr) || ($host eq '')) {
		$host = gethostbyaddr(pack('C4',split(/\./,$addr)),2) || $addr;
	}
	$ENV{'TZ'} = 'JST-9';
	my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	my $day = ('日','月','火','水','木','金','土')[$wday];
	$year = $year + 1900;
	$mon = $mon + 1;
	my $date = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",$year,$mon,$mday,$day,$hour,$min,$sec);

	open(IN, "$HaxesLogfile");
	my @lines = <IN>;
	close(IN);

	while ($HaxesMax <= @lines) { pop @lines; }
	my $id;
	if($HtopAxes == 1) {
		$id = ($defaultID eq $HcurrentID) ? $defaultID : "$defaultID=>$HcurrentID";
	} else {
		$id = $defaultID;
	}
	unshift(@lines, "[$date] - $referer - $host - $addr - $agent - $id\n");

	if(open(OUT, ">$HaxesLogfile")){
		foreach $line (@lines) {
			print OUT jcode::sjis($line);
		}
		close(OUT);
	} else {
		tempProblem();
		return;
	}
}
#----------------------------------------------------------------------
# 入出力
#----------------------------------------------------------------------

# 標準出力への出力
sub out {
#	print $_[0];
	print STDOUT jcode::sjis($_[0], 'euc');
}

# デバッグログ
sub HdebugOut {
	open(DOUT, ">>debug.log");
	print DOUT "$HislandTurn,$_[0]\n";
	close(DOUT);
}

# エスケープ文字の処理
sub htmlEscape {
	my($s) = @_;
	$s =~ s/&/&amp;/g;
	$s =~ s/</&lt;/g;
	$s =~ s/>/&gt;/g;
	$s =~ s/\"/&quot;/g; #"
	$s =~ s/'/&#39;/g;
	$s =~ s/ /&#32;/g;
	return $s;
}

1;