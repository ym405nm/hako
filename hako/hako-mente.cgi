#!/usr/local/bin/perl --
# ↑はサーバーに合わせて変更して下さい。

#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# メンテナンスツール(ver1.01)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 究想の箱庭  (ver5.42b)
#----------------------------------------------------------------------

# ――――――――――――――――――――――――――――――
# 各種設定値
# ――――――――――――――――――――――――――――――
# hako-init.cgiをrequire
require './hako-init.cgi';

# use Time::Localが使えない環境では、'use Time::Local'の行を消して下さい。
# ただし、更新時間の変更が'秒指定で変更'しかできなくなります。
use Time::Local;

# 取引データのファイル(exchange.cgiで指定した内容と同じにする)
$HexchangeFile = "exchange.dat";

# ――――――――――――――――――――――――――――――
# 設定項目は以上
# ――――――――――――――――――――――――――――――

# 各種変数
my($mainMode,$inputPass,$deleteID,$currentID,$ctYear,$ctMon,$ctDate,$ctHour,$ctMin,$ctSec, $mpass1, $mpass2, $spass1, $spass2, $dpass1, $dpass2);

print <<END;
Content-type: text/html

<HTML><HEAD><TITLE>箱庭メンテナンスツール</TITLE></HEAD><BODY>
END

cgiInput();

if (-e $HpasswordFile) {
	# パスワードファイルがある
	open(PIN, "<$HpasswordFile") || die $!;
	chomp($HmasterPassword = <PIN>); # マスタパスワードを読み込む
	close(PIN);
}

if($mainMode eq 'delete') {
	deleteMode() if(passCheck());
} elsif($mainMode eq 'current') {
	currentMode() if(passCheck());
} elsif($mainMode eq 'time') {
	timeMode() if(passCheck());
} elsif($mainMode eq 'stime') {
	stimeMode() if(passCheck());
} elsif($mainMode eq 'new') {
	newMode() if(passCheck());
### ----- add -----
} elsif($mainMode eq 'change') {
	if(passCheck()) {
		if(changeMode()) {
			print <<END;
<FONT SIZE=7>ログデータ移行に成功しました。</FONT>
END
		} else {
	print <<END;
<FONT SIZE=7>ログデータ移行に失敗しました。</FONT>
END
		}
	}
} elsif($mainMode eq 'setup') {
	setupMode();
} elsif($mainMode eq 'mente') {
	menteMode() if(passCheck());
} elsif($mainMode eq 'unmente') {
	unmenteMode() if(passCheck());
}
if(($mainMode eq 'admin') && (passCheck())) {
	adminMode();
} else {
	mainMode();
}

print <<END;
</FORM></BODY></HTML>
END

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

sub currentMode {
	myrmtree "${HdirName}";
	mkdir("${HdirName}", $HdirMode);
### ----- add -----
	unless (-e "$HlogdirName") { mkdir($HlogdirName, $HdirMode); }

	opendir(DIN, "${HdirName}.bak$currentID/");
	my($fileName);
	while($fileName = readdir(DIN)) {
		fileCopy("${HdirName}.bak$currentID/$fileName", "${HdirName}/$fileName");
	}
	closedir(DIN);
}

sub deleteMode {
	if($deleteID eq '') {
		myrmtree "${HdirName}";
### ----- add -----
		myrmtree("${HlogdirName}") if(-e "${HlogdirName}");
		myrmtree("${HtempdirName}") if(-e "${HtempdirName}");
		myrmtree("${HprofileDir}") if(-e "${HprofileDir}");
		myrmtree("deldata") if(-e "deldata");
	} else {
		myrmtree "${HdirName}.bak$deleteID";
	}
	unlink "hakojimalockflock";
}

sub newMode {
	mkdir($HdirName, $HdirMode);
### ----- add -----
	mkdir($HlogdirName, $HdirMode);
	mkdir($HprofileDir, $HdirMode);
	unlink($HexchangeFile);

	# 現在の時間を取得
	$ENV{'TZ'} = "JST-9";
	my($now) = time;
	$now = $now - ($now % ($HunitTime));

	open(OUT, ">$HdirName/hakojima.dat"); # ファイルを開く
	if($Htournament){
		print OUT "2\n";     # ターン数2
	}else{
		print OUT "1\n";     # ターン数1
	}
	print OUT "$now\n";      # 開始時間
	print OUT "0\n";         # 島の数
	print OUT "1\n";         # 次に割り当てるID

	# ファイルを閉じる
	close(OUT);
	if($Htournament){
		# 簡易トーナメント
		open(OUT, ">$HdirName/tournament.dat"); # ファイルを開く
		print OUT "1\n";          # 現在の戦闘モード
		print OUT "$HyosenTurn\n";# 切り替えターン
		print OUT "0\n";          # 何回戦目か
		print OUT "0\n";          # ターン更新数
		# ファイルを閉じる
		close(OUT);
	}

	# 海域を作成する
	my($maxOcean) = $HoceanSize * $HoceanSize;
	my(@field, $i, $x, $y, $tm);

	# 海
	for ($i = 0; $i < $maxOcean; $i++) {
		push(@field, $HlandSea);
	}

	# 無人島
	$tm = 0;
	for ($i = 0; $i < $HmaxIsland; $i++) {
		do {
		$x = int(rand(1) * $HoceanSize - 2) + 1;
		$y = int(rand(1) * $HoceanSize - 2) + 1;
		if (++$tm > $maxOcean) {
			# 海域サイズに対して島が多すぎる
			print <<END;
<H1>エラー発生</H1>
<B>島の配置に失敗しました。</B><BR><BR>
海域サイズに対して島が多すぎます。<BR>
再度試みてください、何回行っても失敗する場合は、<BR>
海域を広げるか、島を減らしてください。<BR>
END
			exit(0);
		}
		} until (countAroundSea(\@field, $x, $y) >= 6);

		$field[$y * $HoceanSize + $x] = 71; # 必ず$HlandOceanと同じにすること
	}

	# マップデータ作成
	open(IOUT, ">$HdirName/submap.1"); # 海域マップファイルを開く
	for ($i = 0; $i < $maxOcean; $i++) {
		$HcurrentField = $field[$i];
		$HcurrentX = $i % $HoceanSize;
		$HcurrentY = int($i / $HoceanSize);
		printf IOUT ("%02x%04x%02x%04x%02x", $HcurrentField, 0, 0, 0, 0);
		print IOUT "\n" if($HcurrentX == $HoceanSize-1);
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
	# ローカル掲示板
	for($i = 0; $i < $HlbbsMax; $i++) {
		print IOUT "0<<0>>\n";
	}
	close(IOUT);
	print <<END;
<H1><A href="hako-main.cgi?Ocean=0" target="_blank">海域を確認する</A></H1>
偏った配置になっている場合は、データを削除してから作り直してください。<BR>
<HR>
END
if($Htournament){
	print "<H1>簡易トーナメント機能は、最初からターン２になっています。</H1>";
	print "ターン更新の都合上、ターン２から始めてください。<HR>";
}
}

sub setupMode {
	if(!($mpass1 && $mpass2) || ($mpass1 ne $mpass2)) {
		print "${HtagBig_}マスタパスワードが入力されていないか間違っています${H_tagBig}";
		return;
	}
	if(!($spass1 && $spass2) || ($spass1 ne $spass2)) {
		print "${HtagBig_}特殊パスワードが入力されていないか間違っています${H_tagBig}";
		return;
	}
#	if(!($dpass1 && $dpass2) || ($dpass1 ne $dpass2)) {
#		print "${HtagBig_}直開発モードパスワードが入力されていないか間違っています${H_tagBig}";
#		return;
#	}
	if(-e $HpasswordFile) {
		# セキュリティーホールのチェック
		print "${HtagBig_}すでにパスワードが設定されています${H_tagBig}";
		return;
	}

	$mpass1 = crypt($mpass1, 'ma');
	$spass1 = crypt($spass1, 'sp');
#	$dpass1 = crypt($dpass1, 'dp');

	open(OUT, ">$HpasswordFile") || die $!;
	print OUT <<END;
$mpass1
$spass1
END
#$dpass1
	close(OUT);
	print "${HtagBig_}パスワードを設定しました${H_tagBig}";
}


sub timeMode {
	$ctMon--;
	$ctYear -= 1900;
	$ctSec = timelocal($ctSec, $ctMin, $ctHour, $ctDate, $ctMon, $ctYear);
	stimeMode();
}

sub stimeMode {
	my($t) = $ctSec;
	open(IN, "${HdirName}/hakojima.dat");
	my(@lines);
	@lines = <IN>;
	close(IN);

	$lines[1] = "$t\n";

	open(OUT, ">${HdirName}/hakojima.dat");
	print OUT @lines;
	close(OUT);
}

### ----- add -----
sub changeMode {
	mkdir($HlogdirName, $HdirMode);

	opendir(DIN, "./${HdirName}");
	my($dn);
	while($dn = readdir(DIN)) {
		if($dn =~ /^hakojima.log(.*)/) {
		    return 0 if(!rename("${HdirName}/hakojima.log$1", "${HlogdirName}/hakojima.log$1"));
		}
	}
	closedir(DIN);

	if (-e "${HdirName}/hakojima.his") {
		return 0 if(!rename("${HdirName}/hakojima.his", "${HlogdirName}/hakojima.his"));
	}

	if (-e "${HdirName}/weather.his") {
		return 0 if(!rename("${HdirName}/weather.his", "${HlogdirName}/weather.his"));
	}

    return 1;
}

sub mainMode {
	print <<END;
<FORM action="$HmenteFile" method="POST">
<h1>究想の箱庭５　メンテナンスツール</h1>
END
	unless (-e $HpasswordFile) {
		# パスワードファイルがない
		print <<END;
<h2>各パスワードを決めてください。</h2>
<p>※入力ミスを防ぐために、それぞれ２回ずつ入力してください。<br>
修正する場合は生成されたファイル(passwd.cgi)をFTPソフトなどで直接消して再度入力してください。</p>
<b>マスタパスワード：</b><br>
(1) <INPUT type="password" name="MPASS1" value="$mpass1">&nbsp;&nbsp;(2) <INPUT type="password" name="MPASS2" value="$mpass2"><br><br>
<b>特殊パスワード：</b><br>
(1) <INPUT type="password" name="SPASS1" value="$spass1">&nbsp;&nbsp;(2) <INPUT type="password" name="SPASS2" value="$spass2"><br><br>
<INPUT type="submit" value="パスワードを設定する" name="SETUP">
<p>※マスターパスワードとは「他の島のパスワード変更」等、すべてのすべての島のパスワードを代用できます。<br>
※特殊パスワードとはこのパスワードで「名前変更」を行うと、その島の資金、食料が最大値になります。(実際に名前を変える必要はありません。)<br>
END

#<b>直開発モードパスワード：</b><br>
#(1) <INPUT type="password" name="DPASS1" value="$dpass1">&nbsp;&nbsp;(2) <INPUT type="password" name="DPASS2" value="$dpass2"><br><br>
#<p>※直開発モードパスワードとは直にURL指定するといきなりJS開発モードに入るモードに使用するパスワードです。<br>
#詳しくは"管理者へ.txt"を参照してください。</p>

		return;
	}
	print <<END;
<B>マスタパスワード：</B><INPUT TYPE=password SIZE=32 MAXLENGTH=32 NAME=PASSWORD VALUE="$inputPass">
<INPUT type="submit" value="管理人室に入る" name="ADMIN">
END
	opendir(DIN, "./");

### ----- add -----
	# ログデータ移行
	if((-e "${HdirName}/hakojima.his")||(-e "${HdirName}/hakojima.log0")){
		print <<END;
<HR><INPUT TYPE="submit" VALUE="ログデータを移行" NAME="CHANGE">
END
	}

	# 現役データ
	if(-d "${HdirName}") {
		dataPrint("");
	} else {
		print <<END;
<HR><INPUT TYPE="submit" VALUE="新しいデータを作る" NAME="NEW">
END
	}

	# バックアップデータ
	my($dn);
	while($dn = readdir(DIN)){
		dataPrint($1) if($dn =~ /^${HdirName}.bak(.*)/);
	}
	closedir(DIN);
}

# 管理人室 neo_otacky氏が作成
sub adminMode {
	my $tmp = "";
	$tmp = "<A HREF=\"${HthisFile}?settei=${inputPass}\" target=\"_blank\"><H2>${AfterName}を作成する</H2></A>" if($HadminMode);
	print <<END;
<H1>究想の箱庭５ 管理人室</H1>
<H3><FONT COLOR="red">※以下の作業は、ターン更新前後に行うのは非常に危険なため行わないこと！！</FONT></H3>
<FORM action="$HmenteFile" method="POST">
<INPUT type=hidden name=PASSWORD value="${inputPass}">
<INPUT type=hidden name=ADMIN value=1>
END
	if(-e "./mente_lock") {
		print qq#<INPUT TYPE="submit" VALUE="メンテナンスモード解除" NAME="UNMENTE">\n#;
	} else {
		print qq#<INPUT TYPE="submit" VALUE="メンテナンスモード" NAME="MENTE">\n#;
	}
	print <<END;
</FORM>
$tmp
<A HREF="${HbaseDir}/hako-main.cgi?Present=" target="_blank"><H2>参加${AfterName}にプレゼントを贈る</H2></A>
<A HREF="${HbaseDir}/hako-main.cgi?Pdelete=${inputPass}" target="_blank"><H2>参加${AfterName}を管理人あずかりにする</H2></A>
<A HREF="${HbaseDir}/hako-main.cgi?Punish=${inputPass}" target="_blank"><H2>参加${AfterName}に制裁を加える</H2></A>
<A HREF="${HbaseDir}/hako-main.cgi?Lchange=${inputPass}" target="_blank"><H2>参加${AfterName}の地形データを変更する</H2></A>
<UL>
<LI>荒らしの被害や、サーバートラブル、スクリプトのバグなどで、地形データが不本意な状態になってしまった${AfterName}を救済します。
<LI>人口、農場規模などの数値データへの反映はターン更新処理が行われてからになるので、注意してください。
</UL>
<A HREF="${HbaseDir}/hako-main.cgi?Ichange=${inputPass}" target="_blank"><H2>各種島データを強制変更する</H2></A>
<UL>
<LI>主に、デバック用です。所属を変更する目的以外で使用しないで下さい。
</UL>
<A HREF="${HbaseDir}/hako-main.cgi?settei=${inputPass}" target="_blank"><H2>参加${AfterName}を強制削除する</H2></A>
<UL>
<LI>「島名とパスワードの変更」の入力フォームで、該当の${AfterName}の名前を「無人」${AfterName}にしてください。
<LI>その際、パスワード欄には「特殊パスワード」を入力してください。(新しいパスとパス確認欄は空)
</UL><BR>
<A HREF="${HbaseDir}/hako-main.cgi?Bfield=${inputPass}" target="_blank"><H2>Battle Fieldを作成する</H2></A>
<UL>
<LI>まだ作成途中です。今後仕様が変更される可能性はあります。
<LI>人口０になっても放棄されない${AfterName}を作成します。いわば「演習${AfterName}」ですが、経験値や難民稼ぎにはなります。
<LI>${AfterName}の登録数には関係なく作成できますが、最大９${AfterName}までしか作成できません。(仕様)
<LI>処理はできるだけ簡略化してますが、作成するほど負荷が増えるので注意してください。
<LI><B>Battle Fieldの仕様</B>
<UL>
<LI>島単位のイベントは全て処理されません。(制裁なども発生しません)
<LI>ノーマル、PPミサイル、移民、怪獣派遣以外は受け付けません。
<LI>荒れ地はかなり高確率で平地になり、平地は森や都市に接していなくても村が発生します。
<LI>自然出現する怪獣は、キングいのらまでで移動等はしません。(硬化はする)
<LI>怪獣を倒した時の報奨金は、倒した島の資金になります。
</UL>
</UL><BR>
<FORM action="${HbaseDir}/analyzer.cgi" method=POST>
<INPUT type=hidden name=password value="${inputPass}">
<INPUT type=hidden name=mode value="analyze">
<INPUT type=hidden name=category value="a">
<INPUT type=submit value='アクセスログを見る'>
</FORM>
<UL>
<LI>メインスクリプト(hako-main.cgi)の設定で「アクセスログをとる」ようにしていなければ、見ることができません。
<LI>ログを残す動作による負荷増はバカになりませんので、箱庭本体の動作にも影響があることを覚悟して下さい。
</UL><BR>
<A HREF="${HbaseDir}/hako-main.cgi?SetupV=${inputPass}" target="_blank"><H2>設定一覧表示</H2></A>
END
}

# 表示モード
sub dataPrint {
	my($suf) = @_;
	print "<HR>";
	if($suf eq "") {
		open(IN, "${HdirName}/hakojima.dat");
		print "<H1>現役データ</H1>";
	} else {
		open(IN, "${HdirName}.bak$suf/hakojima.dat");
		print "<H1>バックアップ$suf</H1>";
	}
	my $lastTurn = int(<IN>);
	my $lastTime = int(<IN>);
	my $islandNumber = int(<IN>);
	my $timeString = timeToString($lastTime);
	print <<END;
<B>ターン$lastTurn</B><BR>
<B>最終更新時間</B>:$timeString<BR>
<B>最終更新時間(秒数表示)</B>:1970年1月1日から$lastTime 秒<BR>
<INPUT TYPE="submit" VALUE="このデータを削除" NAME="DELETE$suf">
END
	if($suf eq "") {
		my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
		localtime($lastTime);
		$mon++;
		$year += 1900;
		print <<END;
<H2>最終更新時間の変更</H2>
<INPUT TYPE="text" SIZE=4 NAME="YEAR" VALUE="$year">年
<INPUT TYPE="text" SIZE=2 NAME="MON" VALUE="$mon">月
<INPUT TYPE="text" SIZE=2 NAME="DATE" VALUE="$date">日
<INPUT TYPE="text" SIZE=2 NAME="HOUR" VALUE="$hour">時
<INPUT TYPE="text" SIZE=2 NAME="MIN" VALUE="$min">分
<INPUT TYPE="text" SIZE=2 NAME="NSEC" VALUE="$sec">秒
<INPUT TYPE="submit" VALUE="変更" NAME="NTIME"><BR>
1970年1月1日から<INPUT TYPE="text" SIZE=32 NAME="SSEC" VALUE="$lastTime">秒
<INPUT TYPE="submit" VALUE="秒指定で変更" NAME="STIME">
<br><br><a href="$HthisFile">[ゲーム画面へ]</a><br>
END
		if($Htournament){
			if(($mainMode eq 'tournamenttime') && (passCheck())) {
				# 簡易トーナメント　ターン更新時間早見表
				print <<END;
<SCRIPT LANGUAGE="JavaScript">
<!--
function textcopy(mapdata){
	window.clipboardData.setData("text",mapdata);
}
function searchID(url){
	if(document.getElementById){
		return document.getElementById(url);
	} else if(document.all){
		return document.all(url);
	} else if(document.layers){
		return document.layers[url];
	}
}
//-->
</SCRIPT>
<br><INPUT TYPE="button" VALUE="クリップボードにコピー" onClick="textcopy(searchID('ALIST').value)">
エクセルとかに貼り付けて使ってください。<br>
<textarea NAME="ALIST" cols="100" rows="5">
END
				open(HIN, "${HdirName}/tournament.dat");
				my $islandFightMode = int(<HIN>);
				<HIN>;
				<HIN>;
				my $turnCount = int(<HIN>);
				close(HIN);
				my $fturn = 0;
				$HfightTurn = $HfinalTurn if($islandNumber <= 2);
				while($lastTurn >= $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn){
					$fturn += $HdevelopeTurn + $HfightTurn;
				}
				print "ターン\t$AfterName数\t進行状態\t更新時間\n";
				while($islandNumber > 1){
					if($lastTurn < $HyosenTurn){
						# 予選
						$islandFightMode = 1;
						$lastTime += 3600 * $HtmTime1[($turnCount % ($#HtmTime1 + 1))];
						$timeString = timeToString($lastTime);
						print "$lastTurn\t$islandNumber\t予選\t$timeString\n";
					}elsif($lastTurn < $HyosenTurn + $HdevelopeTurn + $fturn){
						# 開発
						$islandNumber = $HfightMem if(($islandFightMode == 1) && ($islandNumber > $HfightMem));
						$islandFightMode = 2;
						$lastTime += 3600 * $HtmTime2[($turnCount % ($#HtmTime2 + 1))];
						$timeString = timeToString($lastTime);
						$HfightTurn = $HfinalTurn if($islandNumber <= 2);
						print "$lastTurn\t$islandNumber\t開発\t$timeString\n";
					}elsif($lastTurn < $HyosenTurn + $HdevelopeTurn + $HfightTurn + $fturn){
						# 戦闘
						$turnCount = 0 if($islandFightMode != 3);
						$lastTime += $HinterTime if($islandFightMode != 3 && $islandNumber > 2);
						$islandFightMode = 3;
						$lastTime += 3600 * $HtmTime3[($turnCount % ($#HtmTime3 + 1))];
						$timeString = timeToString($lastTime);
						print "$lastTurn\t$islandNumber\t戦闘♪\t$timeString\n";
					}else{
						$turnCount = 0;
						$lastTime += $HinterTime2 if($islandFightMode != 2);
						$islandFightMode = 2;
						$lastTime += 3600 * $HtmTime2[($turnCount % ($#HtmTime2 + 1))];
						$timeString = timeToString($lastTime);
						$fturn += $HdevelopeTurn + $HfightTurn;
						$islandNumber = int($islandNumber / 2 + 0.5);
						$islandNumber++ if(($islandNumber > 2) && (($islandNumber % 2) != 0) && ($HconsolationMatch));
						$HfightTurn = $HfinalTurn if($islandNumber <= 2);
						print "$lastTurn\t$islandNumber\t開発\t$timeString\n" if($islandNumber > 1);
					}
					$turnCount++;
					$lastTurn++;
				}
				print "</textarea>";
			}else{
				print "<br><INPUT TYPE=\"submit\" VALUE=\"トーナメント更新時間早見表\" NAME=\"TOURNAMENTTIME\">";
			}
		}
	} else {
		print <<END;
<INPUT TYPE="submit" VALUE="このデータを現役に" NAME="CURRENT$suf">
END
	}
}

sub timeToString {
	my($sec, $min, $hour, $date, $mon, $year, $day, $yday, $dummy) =
	localtime($_[0]);
	$mon++;
	$year += 1900;
	return "${year}年 ${mon}月 ${date}日 ${hour}時 ${min}分 ${sec}秒";
}

# CGIの読みこみ
sub cgiInput {
	my($line);

	# 入力を受け取る
	$line = <>;
	$line =~ tr/+/ /;
	$line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

	# GETのやつも受け取る
	$getLine = $ENV{'QUERY_STRING'};

	if($line =~ /DELETE([0-9]*)/) {
		$mainMode = 'delete';
		$deleteID = $1;
	} elsif($line =~ /CURRENT([0-9]*)/) {
		$mainMode = 'current';
		$currentID = $1;
	} elsif($line =~ /NEW/) {
		$mainMode = 'new';
	} elsif($line =~ /UNMENTE/) {
		$mainMode = 'unmente';
		if($line =~ /ADMIN=([0-9])\&/) {
			$dellcheck = $1;
		}
	} elsif($line =~ /MENTE/) {
		$mainMode = 'mente';
		if($line =~ /ADMIN=([0-9])\&/) {
			$dellcheck = $1;
		}
	} elsif($line =~ /ADMIN/) {
		$mainMode = 'admin';
	} elsif($getLine =~ /ADMIN=([^\&]*)/) {
		$mainMode = 'admin';
		$inputPass = $1;
	} elsif($line =~ /SETUP/) {
		$mainMode = 'setup';
		$mpass1 = $1 if($line =~ /MPASS1=([^\&]*)\&/);
		$mpass2 = $1 if($line =~ /MPASS2=([^\&]*)\&/);
		$spass1 = $1 if($line =~ /SPASS1=([^\&]*)\&/);
		$spass2 = $1 if($line =~ /SPASS2=([^\&]*)\&/);
		$dpass1 = $1 if($line =~ /DPASS1=([^\&]*)\&/);
		$dpass2 = $1 if($line =~ /DPASS2=([^\&]*)\&/);
	} elsif($line =~ /NTIME/) {
		$mainMode = 'time';
		$ctYear = $1 if($line =~ /YEAR=([0-9]*)/);
		$ctMon = $1 if($line =~ /MON=([0-9]*)/);
		$ctDate = $1 if($line =~ /DATE=([0-9]*)/);
		$ctHour = $1 if($line =~ /HOUR=([0-9]*)/);
		$ctMin = $1 if($line =~ /MIN=([0-9]*)/);
		$ctSec = $1 if($line =~ /NSEC=([0-9]*)/);
	} elsif($line =~ /STIME/) {
		$mainMode = 'stime';
		$ctSec = $1 if($line =~ /SSEC=([0-9]*)/);
	} elsif($line =~ /TOURNAMENTTIME/) {
		$mainMode = 'tournamenttime';
### ----- add -----
	} elsif($line =~ /CHANGE/) {
		$mainMode = 'change';
	}

	$inputPass = $1 if($line =~ /PASSWORD=([^\&]*)\&/);
}

# ファイルのコピー
sub fileCopy {
	my($src, $dist) = @_;
	open(IN, $src);
	open(OUT, ">$dist");
	while(<IN>) {
		print OUT;
	}
	close(IN);
	close(OUT);
}

# パスチェック
sub passCheck {
	if(crypt($inputPass, 'ma') eq $HmasterPassword) {
		return 1;
	} else {
		print "${HtagBig_}パスワードが違います${H_tagBig}";
		return 0;
	}
}
# メンテナンスモード
sub menteMode {
    mkdir("./mente_lock", $HdirMode);
}

# メンテモード解除
sub unmenteMode {
	rmdir("./mente_lock");
}

# 範囲内の海を数える
sub countAroundSea {
	my($field, $x, $y) = @_;

	my @ax = (0,1,1,1,0,-1,0); # 周囲１ヘックスの座標
	my @ay = (0,-1,0,1,1,0,-1);

	my($i, $count, $sx, $sy, $idx);

	$sx = $x + $ax[0];
	$sy = $y + $ay[0];
	$sx-- if(!($sy % 2) && ($y % 2));
	$idx = $sy * $HoceanSize + $sx;
	return 0 unless ($field->[$idx] == $HlandSea); # 中央が海でなければならない

	$count = 0;
	for($i = 1; $i < 7; $i++) {
		$sx = $x + $ax[$i];
		$sy = $y + $ay[$i];

		$sx-- if(!($sy % 2) && ($y % 2));

		if(($sx < 0) || ($sx >= $HoceanSize) || ($sy < 0) || ($sy >= $HoceanSize)) {
			# 範囲外
		} else {
			# 範囲内
			$idx = $sy * $HoceanSize + $sx;
			$count++ if ($field->[$idx] == $HlandSea);
		}
	}

	return $count;
}


1;
