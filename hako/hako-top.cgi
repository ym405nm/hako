#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# トップモジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
# 究想の箱庭  (ver5.52c)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# トップページモード
#----------------------------------------------------------------------
# メイン

sub topPageMain {
	axeslog() if($HtopAxes == 2); #アクセスログ取得
	unlock();		# 開放

	if(-e "./mente_lock"){
		mente_mode(0);
	}else{
		tempTopPage($_[0]);	# テンプレート出力
	}
}

# トップページ
sub tempTopPage {
	my($mode) = @_;
	# flexTime処理
	if($Htournament){
		# 簡易トーナメント
		$HflexTimeSet = 1;
		if($HislandFightMode == 1){
			# 予選
			@HflexTime = @HtmTime1;
		}elsif($HislandFightMode == 2){
			# 開発
			@HflexTime = @HtmTime2;
			$HmaxIsland = 0;
		}elsif($HislandFightMode == 3){
			# 戦闘
			@HflexTime = @HtmTime3;
			$HmaxIsland = 0;
		}elsif($HislandFightMode == 9){
			# 終了
			$HlastTurn = $HislandTurn;
		}
		$HunitTime = 3600 * $HflexTime[($HislandTurnCount % ($#HflexTime + 1))] if($HflexTimeSet);
	}else{
		$HunitTime = 3600 * $HflexTime[($HislandTurn % ($#HflexTime + 1))] if($HflexTimeSet);
	}
	if($mode != 2){
	out(<<END);
${HtagTitle_}$Htitle${HtagTitle2_}$Htitle2${H_tagTitle}${H_tagTitle}
END
#${HthisFile}?Sight=${id}" class=\"M\" TARGET=_blank>
	# デバッグモードなら「ターンを進める」ボタン

	if($Hdebug == 1) {
		out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="ターンを進める" NAME="TurnButton">
</FORM>
END
	}
	# 次回更新時間表示
	my($now) = time;
	# 次回更新までの時間を計算する
	$aaa = $HislandLastTime + $HunitTime;
	my($sec, $min, $hour, $day, $sss);
	$sec = $aaa - $now;
	if($sec < 0) {
		$aaa += $HunitTime;
		if(-$sec < $HunitTime) {
			$sec += $HunitTime;
		} else {
			$sec = 0;
		}
	}
	$min  = int($sec  / 60); $sec  %= 60;
	$hour = int($min  / 60); $min  %= 60;
	$day  = int($hour / 24); $hour %= 24;
	if($day){
		$sss = "$day日と${hour}時間${min}分${sec}秒";
	}else{
		$sss = "${hour}時間${min}分${sec}秒";
	}
	
	my($min2, $hour2, $date2, $mon2) = (localtime($aaa))[1,2,3,4];
	$mon2++;
	my($bbb) = "${mon2}月${date2}日${hour2}時${min2}分";
	
	my $bb1 = "";
	if($HflexTimeSet) {
		my($i,$nnn,$ftime,$ct,$rt) = (0,0,0,0,0);
		$ct = $#HflexTime + 1;
		if($Htournament){
			$rt = ($HislandTurnCount % ($ct));
		}else{
			$rt = ($HislandTurn % ($ct));
		}
		$bb1 = "更新頻度　${ct}回／日(　";
		my $bb2;
		for($i = $rt;$i <= $#HflexTime;$i++){
			$ftime += $HflexTime[($i % ($#HflexTime + 1))];
			$nnn = $HislandLastTime + 3600 * $ftime;
			($min2, $hour2) = (localtime($nnn))[1,2];
			if($rt == $i){
				$bb2 .= "<b>${hour2}時${min2}分</b>　";
			}else{
				$bb2 .= "${hour2}時${min2}分　";
			}
		}
		for($i = 0;$i < $rt;$i++){
			$ftime += $HflexTime[($i % ($#HflexTime + 1))];
			$nnn = $HislandLastTime + 3600 * $ftime;
			($min2, $hour2) = (localtime($nnn))[1,2];
			$bb1 .= "${hour2}時${min2}分　";
		}
		$bb1 .= "${bb2})";
	}
	
	if ($HjavaModeSet eq 'cgi') {
		$radio = "CHECKED";	$radio2 = "";
	}else{
		$radio = ""; $radio2 = "CHECKED";
	}

	# ターン数表示
	my($HlastTurnS);
	if($HlastTurn == 0) {
		$HlastTurnS = "";
	} elsif($HislandTurn < $HlastTurn) {
		$HlastTurnS = "／${HlastTurn}";
	} else {
		$HlastTurnS = "　（ゲームは終了しました）";
		$bbb = "更新無し";
	}

	my($sinkiStr) = '';
	if($HislandNumber < $HmaxIsland + $HbattleNumber) {
		$sinkiStr = "[<A HREF=\"${HthisFile}?settei=0\" class=\"M\">新規参入、設定変更</A>]<br>";
	} else {
		# 最大数

		$sinkiStr = "[<A HREF=\"${HthisFile}?settei=0\" class=\"M\">新規参入、設定変更</A>（満杯）]<br>";
	}

	# フォーム

	$monthname = $Hmonthname[($HislandTurn % 12) + 1];
	
	my $fightmode = "";
	if($Htournament){
		# 簡易トーナメント
		my($tst1,$tst2);
		my $flog = "[<A href=\"$HthisFile?FightLog=0\" class=\"M\" TARGET=_blank>対戦の記録</A>]";
		if($HislandFightMode == 1){
			# 予選
			if($HislandNumber > $HfightMem){
				$tst2 = $HislandNumber - $HfightMem;
				$tst2 = "$tst2$AfterName沈没し";
			}
			$tst1 = "　予選終了後、$tst2開発期間に移行します。";
			$fightmode = "<font color=blue>予選期間中</font>　[$HislandTurn／$HislandChangeTurnターン]　($HislandNumber$AfterName／$HfightMem${AfterName})$tst1";
		}elsif($HislandFightMode == 2){
			# 開発
			$tst1 = $HislandChangeTurn + 1;
			$fightmode = "<font color=blue>開発期間中</font>　[$HislandTurn／$HislandChangeTurnターン]　($tst1ターンから攻撃開始)";
		}elsif($HislandFightMode == 3){
			# 戦闘
			$fightmode = "<font color=red>戦闘期間中</font>　[$HislandTurn／$HislandChangeTurnターン]";
		}elsif($HislandFightMode == 9){
			# 終了
			$fightmode = "トーナメントは終了しました。";
		}
		$fightmode = "<DIV ID='fightmode'><b>$fightmode $flog</b></DIV><br><br>";
	}
	out(<<END);
<DIV ID='Turn'>
<H1>ターン$HislandTurn$HlastTurnS　($monthname)</H1>
</DIV>
$fightmode
<DIV ID='nexttime'>
<font size=4>次回の更新時間：$bbb </FONT><font size=3>(残り $sss)</FONT>
<br>$bb1
</DIV>

<span class='attention'>


</span>

<HR><TABLE><TR><TD style="border-width:0px;">
<DIV ID='myIsland'>
<H1>自分の${AfterName}へ</H1>
<SCRIPT language="JavaScript">
<!--
function develope(){
	if(document.Island.DEVELOPEMODE[1].checked){
		document.Island.SIGHTMODE.value = "on";
	}
	document.Island.target = "";
}
function newdevelope(){
	if(document.Island.DEVELOPEMODE[1].checked){
		document.Island.SIGHTMODE.value = "on";
	}
//	newWindow = window.open("", "newWindow");
	document.Island.target = "newWindow";
	document.Island.submit();
}
//-->
</SCRIPT>
<FORM name="Island" action="$HthisFile" method="POST">
ログインする${AfterName}の名前は？<BR>
<SELECT NAME="ISLANDID">
<OPTION VALUE="0">-${AfterName}を選択して下さい-
$HislandList
</SELECT><BR>
あなたの${AfterName}の名前は？<BR>
<SELECT NAME="PISLANDID">
$HislandList
</SELECT><BR>
パスワードをどうぞ！！<BR>
<INPUT TYPE="hidden" NAME="OwnerButton">
<INPUT TYPE="password" NAME="PASSWORD" VALUE="${\htmlEscape($HdefaultPassword)}" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=cgi $radio>旧モード
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=java $radio2>Javaスクリプトモード<BR>
<INPUT TYPE="radio" NAME=DEVELOPEMODE VALUE=DEVELOPE CHECKED>開発モード
<INPUT TYPE="radio" NAME=DEVELOPEMODE VALUE=SIGHT>観光モード<BR>
<INPUT TYPE="hidden" NAME="SIGHTMODE" VALUE=off>
<INPUT TYPE="submit" VALUE="同じ画面" onClick="develope()">　
<INPUT TYPE="button" VALUE="新しい画面" onClick="newdevelope()">
</FORM></DIV></TD>
<TD WIDTH=40 style="border-width:0px;" >　</TD>
<TD VALIGN="top" style="border-width:0px;" >
<H1>設定変更や各種情報を表示</H1>
$sinkiStr<br>
[<A HREF="${HbaseDir}/history.cgi?saikin=99" class=\"M\" TARGET=_blank>過去の出来事のログ</A>　／
<A HREF="${HbaseDir}/history.cgi?tenki=0" class=\"M\" TARGET=_blank>過去の天気</A>　／
<A HREF="${HbaseDir}/history.cgi?statistical=0" class=\"M\" TARGET=_blank>統計</A>]<br>
<br>
[<A href="${HbaseDir}/profile.cgi" class=\"M\" TARGET=_blank>プロファイル(${AfterName}主の情報)</A> ／
<A href="$HthisFile?Exchange=0" class=\"M\" TARGET=_blank>資源取引所</A>]<br>
<br>
[<A href="${HbaseDir}/ranking.cgi" class=\"M\" TARGET=_blank>倒した怪獣数などのランキング</A> ／
<A href="$HthisFile?SUCCESSIVE=0" class=\"M\" TARGET=_blank>歴代最多人口のランキング表示</A>]<br>
<br>
END
	my $sftime = (-M "${HefileDir}/setup.html");
	my @Files = ('hako-main.cgi', 'hako-init.cgi', 'init-game.cgi', 'hako-make.cgi');
	my $sfFlag = 1;
	foreach (@Files) {
		if($sftime >= (-M "./$_")){
			$sfFlag = 0;
			last;
		}
	}
	if((-e "${HefileDir}/setup.html") && $sfFlag) {
		out("[<A href=\"${efileDir}/setup.html\" class=\"M\" TARGET=_blank>設定一覧</A>] ");
	} else {
		out("[<A href=\"$HthisFile?SetupV=0\" class=\"M\" TARGET=_blank>設定一覧</A>] ");
	}
	out("</TD></TR></TABLE>");
	}else{
		# 設定モード
		out("$Htitle新規参入、設定変更　　　<A HREF=\"${HthisFile}\" class=\"M\">通常の一覧画面に戻る</A>");
	}
	my $mStr1 = ($HhideMoneyMode != 0) ? "<TH $HbgTitleCell>${HtagTH_}資金${H_tagTH}</TH>" : '';
	if($mode == 1) {
		# 簡易表示モード
		return;
	} elsif($mode == 2) {
		# 設定モード
	} else {
		my $solarwind = ($Hspace->{'solarwind'} <= $HislandTurn) ? "(<b>太陽風発生中</b>)" : "";
		my $hangen = "";
		my $hmode = "";
		if($Hdishangen == 2) {
			# 災害半減期を表示する。
			if((int($HislandTurn / 100) % 2) == 0){
				# 確率半減
				$hangen = "　災害率半減中";
			}
		}
		if($mode == 3){
			# 詳細モード
			$hmode = "[<A href=\"$HthisFile\" class=\"M\">簡易一覧</A>]";
		}else{
			$hmode = "[<A href=\"$HthisFile?list=0\" class=\"M\">詳細一覧</A>]";
		}
		my $warstr = "";
		if($HwarFlg){
			$warstr = "<TH $HbgTitleCell>${HtagTH_}獲得経験値${H_tagTH}</TH>";
		}
		# 陣営表を表示?
		&campInfoList;
		my $vsith = "";
		if($Htournament){
			$vsith = "<TH $HbgTitleCell>${HtagTH_}対戦相手${H_tagTH}</TH>";
		}
		out(<<END);
<HR><DIV ID='islandView'>
<H1>諸${AfterName}の状況${hangen}</H1>
<P>${AfterName}の名前をクリックすると、<B>観光</B>することができます。$hmode
[<A href="${HbaseDir}/monsterlist.cgi" class=\"M\">怪獣バトル　所持怪獣一覧</A>]
</P>
[<A href=\"$HthisFile?Ocean=0" class=\"M\">諸島周辺の海域</A>]
[<A href=\"$HthisFile?space=0\" class=\"M\">宇宙へ</A>${solarwind}]
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>${HtagTH_}順位${H_tagTH}</TH>
<TH $HbgTitleCell COLSPAN=2>${HtagTH_}${AfterName}${H_tagTH}</TH>
$vsith
<TH $HbgTitleCell>${HtagTH_}座標${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}天気${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}人口${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}面積${H_tagTH}</TH>
$mStr1
<TH $HbgTitleCell>${HtagTH_}食料${H_tagTH}</TH>
$warstr
<TH $HbgTitleCell>${HtagTH_}意思表示${H_tagTH}</TH>
END
		if($mode == 3){
			# 詳細
	out(<<END);
<TH $HbgTitleCell>${HtagTH_}農業規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}工業規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}商業規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}採掘場規模${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}部門賞${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}プレゼント${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}勝Ｐ${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}負Ｐ${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}自占有数${H_tagTH}</TH></TR>
END
		}else{
			out("</TR>\n");
		}
	}
	
	if(($mode == 0) || ($mode == 3)) {
		# 通常、詳細モード

	my($island, $j, $food, $farm, $factory, $tower, $mountain, $ally, $amark, $name, $id, $prize, $vprize, $present, $ii, $monsfound);
	my $bcount = 0;
	for($ii = 0; $ii < $HislandNumber; $ii++) {

	$island = $Hislands[$ii];

	$id = $island->{'id'};
	
	if($id > 90) {
		$bcount++;
	}else{
		# 通常の島のとき
	
#	my($wkind, $wname, $whp, $wkind2, $wkind3) = weatherinfo($island->{'weather'});
#	my($wname2) = $WeatherName[$wkind2];
#	my($wname3) = $WeatherName[$wkind3];
	
	$j = $ii + 1 - $bcount;
	$farm = $island->{'farm'};
	$factory = $island->{'factory'} + $island->{'port'};
	$tower = $island->{'tower'};
	$mountain = $island->{'mountain'};
	$farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
	$tower = ($tower == 0) ? "保有せず" : "${tower}0$HunitPop";
	$mountain = ($mountain == 0) ? "保有せず" : "${mountain}0$HunitPop";
	my($turnsu)   = $island->{'turnsu'};
	my($zyuni) = $island->{'zyuni'};

	$prize = $island->{'prize'};
	my($flags, $monsters, $turns);
	$prize =~ /([0-9]*),([0-9]*),(.*)/;
	$flags = $1;
	$monsters= $2;
	$turns = $3;
	$prize = '';

	if($Hallyflg){
		# 各勢力の統計
		$ally = $island->{'ally'};
		$amark = "<b>$Hallymark[$ally]</b> ";
	}else{
		$amark = "";
	}
	# 保護国には保護を表示
	my($hogo) = '○';
	if(($turnsu + $island->{'evil'} < $HdisUN) || ($island->{'evil'} == 0)){
		$hogo = '×';
	} elsif(($island->{'evil'} < $HdisUN) && (!$HwarFlg)) {
		$hogo = '△';
	}

	# 怪獣がいる場合は表示
	if($island->{'monsfound'} > 0){
		$monsfound = "<b>(怪獣$island->{'monsfound'})</b>";
	}else{
		$monsfound = "";
	}

	# 天気
	my($wkind, $wname, $whp, $wkind2, $wkind3) = weatherinfo($island->{'weather'});
	my $tenki = "<img src =\"${imageDir}/$WeatherIcon[${wkind}]\">";

	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}${AfterName}${H_tagName}";
	} else {
		$name = "${HtagName2_}$island->{'name'}${AfterName}($island->{'absent'})${H_tagName2}";
	}
	$name = "<span class='attention'>【管理人あずかり】</span><BR>" . $name if($island->{'predelete'});
	
	# ターン杯の表示
	my($kazu) = 0;
	my($mTurnList) = '';
	while($turns =~ s/([0-9]*),//) {
		$kazu++;
		$mTurnList .= "[$1${Hprize[0]}] ";
	}
	if($kazu >= 5) {
		$prize .= "<IMG SRC=\"prize00.gif\" ALT=\"$mTurnList\" WIDTH=16 HEIGHT=16> ";
	} elsif($kazu >= 3) {
		$prize .= "<IMG SRC=\"prize.gif\" ALT=\"$mTurnList\" WIDTH=16 HEIGHT=16> ";
	} elsif($kazu != 0) {
		$prize .= "<IMG SRC=\"prize0.gif\" ALT=\"$mTurnList\" WIDTH=16 HEIGHT=16> ";
	}

	# 名前に賞の文字を追加
	my($f) = 1;
	my($i);
	for($i = 1; $i < 11; $i++) {
		$prize .= "<IMG SRC=\"prize${i}.gif\" ALT=\"${Hprize[$i]}\" WIDTH=16 HEIGHT=16> " if($flags & $f);
		$f *= 2;
	}
	$prize .= "<IMG SRC=\"prize11.gif\" ALT=\"${Hprize[11]}\" WIDTH=16 HEIGHT=16> " if($flags & 2048);
	
	# 倒した怪獣リスト
	$f = 1;
	my($max) = -1;
	my($mNameList) = '';
#	for($i = 0; $i < 32; $i++) {
#		if($monsters & $f) {
#			$mNameList .= "[$HmonsterName[$i]] ";
#			$max = $i;
#		}
#		$f *= 2;
#	}
	for($i = $HmonsterNumber-1; $i >= 0; $i--) {
		$f = 2 ** $i;
		if($monsters >= $f){
			$monsters -= $f;
			$mNameList .= "[$HmonsterName[$i]] ";
			$max = $i if($max == -1);
		}
	}
	$prize .= "<IMG SRC=\"${HmonsterImage[$max]}\" ALT=\"$mNameList\" WIDTH=16 HEIGHT=16> " if($max != -1);

	my($cspan,$comment,$popspace);
	if($mode == 3){
		# 詳細モード
		$popspace = $island->{'popspace'};
		$popspace = ($popspace > 0) ? "(${popspace}${HunitPop})" : "";
		$comment = $island->{'comment'};
		$cspan = 16;
		# プレゼントを表示
		$present = '';
		my $pre  = $island->{'present'};
		$present .= "<IMG SRC=\"land30.gif\" ALT=\"$pre->[0]\" WIDTH=16 HEIGHT=16> " if($pre->[0] > 0);
		$present .= "<IMG SRC=\"land27.gif\" ALT=\"$pre->[1]\" WIDTH=16 HEIGHT=16> " if($pre->[1] > 0);
		$present .= "<IMG SRC=\"land32.gif\" ALT=\"$pre->[2]\" WIDTH=16 HEIGHT=16> " if($pre->[2] > 0);
		$present .= "<IMG SRC=\"land29.gif\" ALT=\"$pre->[3]\" WIDTH=16 HEIGHT=16> " if($pre->[3] > 0);
		$present .= "<IMG SRC=\"land28.gif\" ALT=\"$pre->[4]\" WIDTH=16 HEIGHT=16> " if($pre->[4] > 0);
		$present .= "<IMG SRC=\"land31.gif\" ALT=\"$pre->[5]\" WIDTH=16 HEIGHT=16> " if($pre->[5] > 0);
		$present .= "<IMG SRC=\"land33.gif\" ALT=\"$pre->[6]\" WIDTH=16 HEIGHT=16> " if($pre->[6] > 0);
		$present .= "<IMG SRC=\"land39.gif\" ALT=\"$pre->[7]\" WIDTH=16 HEIGHT=16> " if($pre->[7] > 0);
		$present .= "<IMG SRC=\"land38.gif\" ALT=\"$pre->[8]\" WIDTH=16 HEIGHT=16> " if($pre->[8] > 0);
		$present .= "<IMG SRC=\"land40.gif\" ALT=\"$pre->[9]\" WIDTH=16 HEIGHT=16> " if($pre->[9] > 0);
		$present .= "<IMG SRC=\"monumentM.gif\" ALT=\"$pre->[10]\" WIDTH=16 HEIGHT=16> " if($pre->[10] > 0);
		$present .= "<IMG SRC=\"monumentP.gif\" ALT=\"$pre->[11]\" WIDTH=16 HEIGHT=16> " if($pre->[11] > 0);
		$present = '　' if($present eq '');

		# 各賞を表示
		$f = 1;
		$vprize = '';
		$flags = $island->{'status'};
		for($i = 1; $i < $HturnPrizeNumber + 1; $i++) {
			$vprize .= "<IMG SRC=\"Vprize${i}.gif\" ALT=\"${HprizeV[$i]}\" WIDTH=16 HEIGHT=16> " if($flags & $f);
			$f *= 2;
		}
		$vprize = '　' if($vprize eq '');
	}else{
		$comment = cutColumn($island->{'comment'}, 70);
		$cspan = 7;
	}
	
	#コメントラベル
	my($label0, $label1, $label2, $label3, $label4);
	my($label0_1n,$label0_2n) = split(/<>/,$HlabelName[0]);
	my($label0_1i,$label0_2i) = split(/<>/,$HlabelImage[0]);
	if($island->{'commentLabel0'}){
		$label0 = " <IMG SRC=\"$imageDir/$label0_1i\" ALT=\"$label0_1n\">" 
	}else{
		$label0 = " <IMG SRC=\"$imageDir/$label0_2i\" ALT=\"$label0_2n\">"
	}
	$label1 = " <IMG SRC=\"$imageDir/$HlabelImage[1]\" ALT=\"$HlabelName[1]\">" if($island->{'commentLabel1'});
	$label2 = " <IMG SRC=\"$imageDir/$HlabelImage[2]\" ALT=\"$HlabelName[2]\">" if($island->{'commentLabel2'});
	$label3 = " <IMG SRC=\"$imageDir/$HlabelImage[3]\" ALT=\"$HlabelName[3]\">" if($island->{'commentLabel3'});
	$label4 = " <IMG SRC=\"$imageDir/$HlabelImage[4]\" ALT=\"$HlabelName[4]\">" if($island->{'commentLabel4'});
	
	if($HwarFlg){
		# 戦争モード
		$warstr = "<TD $HbgInfoCell>" . $island->{'allex'} . "</TD>";
		$cspan++;
	}
	# 簡易トーナメント
	my $vsitd = "";
	if($Htournament){
		my $tName = "";
		if($HislandFightMode == 9){
			$tName = "　- 終了 -";
		}elsif($island->{'fight_id'} == -1){
			$tName = "　- 不戦勝 -";
		}else{
			$tName = $HidToName{$island->{'fight_id'}};
			$tName = ($tName eq '') ? "　- 未定 -" : "$tName$AfterName";
		}
		$vsitd = "<TD $HbgNameCell>$tName</TD>";
		$cspan++;
	}
	my($mStr1) = '';
	if($HhideMoneyMode == 1) {
		$mStr1 = "<TD $HbgInfoCell>$island->{'money'}$HunitMoney</TD>";
	} elsif($HhideMoneyMode == 2) {
		my($mTmp) = aboutMoney($island->{'money'});
		$mStr1 = "<TD $HbgInfoCell>$mTmp</TD>";
	}

	my($oStr) = ''; # オーナ名表示のため追加
	if($island->{'ownername'} eq ''){
		$oStr = "<TD $HbgCommentCell COLSPAN=$cspan>$amark${HtagTH_}コメント : ${H_tagTH}${comment}</TD>";
	} else {
		$oStr = "<TD $HbgCommentCell COLSPAN=$cspan>$amark<A HREF=\"$HbaseDir/profile.cgi?profile=${id}\" class=\"M\" TARGET=_blank>$island->{'ownername'}</A> : ${comment}</TD>";
	}
	out(<<END);
<TR>
<TD $HbgNumberCell ROWSPAN=2>${HtagNumber_}$j${H_tagNumber}($zyuni)</TD>
<TD $HbgNameCell ROWSPAN=2>
<A HREF="${HthisFile}?Sight=${id}" class=\"M\" TARGET=_blank>
$name$monsfound
</A><BR>
$prize
</TD>
<TD $HbgInfoCell>$hogo</TD>
$vsitd
<TD $HbgInfoCell>$island->{'x'},$island->{'y'}</TD>
<TD $HbgInfoCell>$tenki</TD>
<TD $HbgInfoCell>$island->{'pop'}$HunitPop$popspace</TD>
<TD $HbgInfoCell>$island->{'area'}$HunitArea</TD>
$mStr1
<TD $HbgInfoCell>$island->{'food'}$HunitFood</TD>
$warstr
<TD $HbgInfoCell>$label0$label1$label2$label3$label4</TD>
END
	if($mode == 3){
		out(<<END);
<TD $HbgInfoCell>$farm</TD>
<TD $HbgInfoCell>$factory</TD>
<TD $HbgInfoCell>$tower</TD>
<TD $HbgInfoCell>$mountain</TD>
<TD $HbgInfoCell>$vprize</TD>
<TD $HbgInfoCell>$present</TD>
<TD $HbgInfoCell>$island->{'winP'}</TD>
<TD $HbgInfoCell>$island->{'loseP'}</TD>
<TD $HbgInfoCell>$island->{'possess'}</TD></TR>
END
	}else{
		out("</TR>\n");
	}
	out(<<END);
<TR>
<TD $HbgInfoCell>$turnsu</TD>
$oStr
</TR>
END
	}
	}
	out(<<END);
</TABLE></DIV>
END
	my $bHeader = 1;
	for($ii = 0; $ii < $HislandNumber; $ii++) {
		$island = $Hislands[$ii];
		$id = $island->{'id'};
		if($id > 90) {
			# Battle Field
			if($island->{'ownername'} eq ''){
				$oStr = "<TD $HbgNameCell>$island->{'comment'}</TD>";
			} else {
				$oStr = "<TD $HbgNameCell><A HREF=\"$HbaseDir/profile.cgi?profile=${id}\" class=\"M\" TARGET=_blank>$island->{'ownername'}</A> : $island->{'comment'}</TD>";
			}
			if($bHeader){
				$bHeader = 0;
	out(<<END);
<DIV ID='islandViewBf'>
<H1>Battle Fieldの状況</H1>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>${HtagTH_}順位${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}ID${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}座標${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}コメント${H_tagTH}</TH>
</TR>
END
			}
	out(<<END);
<TR>
<TD $HbgNumberCell align=center><span class="star">★</span></TD>
<TD $HbgInfoCell>$island->{'id'}</TD>
<TD $HbgNameCell>
<A HREF="${HthisFile}?Sight=${id}" class=\"M\" TARGET=_blank>${HtagName_}$island->{'name'}${AfterName}${H_tagName}</A><BR></TD>
<TD $HbgInfoCell>$island->{'x'},$island->{'y'}</TD>
$oStr
</TR>
END
			}
		}
		if($bHeader){
			out("<HR>");
		}else{
			out("</TABLE></DIV><HR>");
		}
	} else {
		my $tournamentMons = "";
		if($Htournament == 2){
			$tournamentMons = "守護怪獣(怪獣バトル)は？<BR><SELECT NAME=TOURNAMENTMONS>\n";
			for($i = 1; $i < $HmonsterNumber; $i++) {
				$tournamentMons .= "<OPTION VALUE=$i>$HmonsterName[$i]\n";
			}
			$tournamentMons .= "</SELECT><BR>\n";
		}
		out(<<END);
<HR>
<TABLE><TR><TD style="border-width:0px;" >
<DIV ID='changeInfo'>
<H1>$AfterName名やパスワードの変更</H1>
<P>(注意)名前の変更には$HcostChangeName${HunitMoney}かかります。</P>
<FORM action="$HthisFile" method="POST">
どの$AfterNameですか？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT>
<BR>
どんな名前に変えますか？(変更する場合のみ)<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>$AfterName<BR>
どんなオーナー名に変えますか？(変更する場合のみ)<BR>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
パスワードは？(必須)<BR>
<INPUT TYPE="password" NAME="OLDPASS" SIZE=32 MAXLENGTH=32><BR>
新しいパスワードは？(変更する時のみ)<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
念のためパスワードをもう一回(変更する時のみ)<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="変更する" NAME="ChangeInfoButton">
</FORM></DIV></TD>
<TD WIDTH=40 style="border-width:0px;" >　</TD>
<TD VALIGN="top" style="border-width:0px;" >
<DIV ID='newIsland'>
<H1>新しい$AfterNameを探す</H1>
END
		if($HislandNumber < $HmaxIsland + $HbattleNumber) {
			if((!$HadminMode) || (checkPassword($HspecialPassword, $HdefaultPassword))){
				out(<<END);
<FORM action="$HthisFile" method="POST">
どんな名前をつける予定？<BR>
<INPUT TYPE="text" NAME="ISLANDNAME" SIZE=32 MAXLENGTH=32>$AfterName<BR>
オーナー名(省略可)<br>
<INPUT TYPE="text" NAME="OWNERNAME" SIZE=32 MAXLENGTH=32><BR>
$tournamentMons
パスワードは？<BR>
<INPUT TYPE="password" NAME="PASSWORD" SIZE=32 MAXLENGTH=32><BR>
念のためパスワードをもう一回<BR>
<INPUT TYPE="password" NAME="PASSWORD2" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="submit" VALUE="探しに行く" NAME="NewIslandButton">
</FORM>
END
			}else{
				# 管理モード
				out(<<END);
        当箱庭では不適当な${AfterName}名などの事前チェックを行っています。<BR>
        参加希望の方は、管理人まで「${AfterName}名」と「パスワード」を<BR>
        メールしてください。<BR>
END
			}
		}else{
			out(<<END);
        $AfterNameの数が最大数です・・・現在登録できません。
END
		}
		
		my($cookie) = jcode::euc($ENV{'HTTP_COOKIE'});
		if($cookie =~ /MYSHIP=\(([^\)]*)\)/) {
			if($1) {
				$radio = ""; $radio2 = "CHECKED";
			}else{
				$radio = "CHECKED";	$radio2 = "";
			}
		}
		out(<<END);
</DIV>
</TD></TR></TABLE>
<HR>
<FORM action="$HthisFile" method="POST">
<H1>自島の船の画像の周囲を透過させて区別しやすくするかどうかの設定</H1>
<INPUT TYPE="radio" NAME=RMYSHIP VALUE=0 $radio>透過させる

<INPUT TYPE="radio" NAME=RMYSHIP VALUE=1 $radio2>透過させない
<INPUT TYPE="submit" VALUE="変更する" NAME="MyShipImgMode">
</FORM>
END
	my($Hskinflag);
	if($HskinName eq '' || $HskinName eq "$HcssFile"){
		$Hskinflag = '<span class=attention>未設定</span>';
	} else {
		$Hskinflag = $HskinName;
	}
	my $select_list = "<OPTION value='del' selected>デフォルト\n";
	foreach(0 .. $#HskinList) {
		$Hskinflag = $HskinName[$_] if($HskinList[$_] eq $HskinName);
		$select_list .= "<OPTION value='$HskinList[$_]'>$HskinName[$_]\n";
	}
	out(<<END);
<hr><div id='hakoSkin'>
<h1>スタイルシートの設定</h1>
現在の設定<b>[</b> ${Hskinflag} <b>]</b>
<form action=$HthisFile method=POST>
<SELECT NAME="SKIN">$select_list</SELECT>
<INPUT TYPE="submit" VALUE="設定" name=SKINSET>
</form>
</div>
END
		if($Hlocalimage) {
			my $setsumei = ($Hlocalimagehtml ne '') ? "<p>詳しくは<a href=\"${Hlocalimagehtml}\"target=\"_blank\">説明のページ</a>をご覧下さい。 </p>" : "";
			my $dlimg = ($HlocalImg ne '') ? "画像は<B><a href=\"$HlocalImg\">ここ</a></B>からダウンロードして下さい。<br>" : "";
			my $Himfflag = ($HimgLine eq '') ? '<FONT COLOR=RED>未設定</FONT>' : $HimgLine;
			out(<<END);
<HR>
<TABLE><TR><TD style="border-width:0px;" >
<H1>画像のローカル設定</H1>
$dlimg
参照のボタンをクリックしパソコンのローカルディスクの箱庭画像保存フォルダのland0.gifを選んでください。<BR>
指定のフォルダまでのルートが全て英数字のみのフォルダ名を推奨します。<BR>
半角カナは使用不可能です。半角スペースは%20に自動置換されます。<BR>
また、空白を設定すると指定が解除されます。<BR><BR>
$setsumei
現在の設定<B>[</b> ${Himfflag} <B>]</B>
<form action=$HthisFile method=POST>
<INPUT TYPE=file NAME="IMGLINE" SIZE="80">
<INPUT TYPE="submit" VALUE="設定" name=IMGSET>
</form>

<form action=$HthisFile method=POST>
直接指定（Macユーザー用）<BR>
例(WIN) D:\\image\\hakogif<BR>
<INPUT TYPE=text NAME="IMGLINEMAC" SIZE="80">
<INPUT TYPE="submit" VALUE="設定" name=IMGSET><BR>
Macを触ったことがないのでよくわかりません<BR>
</form>

</TD></TR></TABLE>
END

			return;
		} else {
			return;
		}
	}
	out(<<END);
<DIV ID='RecentlyLog'>
<H1>最近の出来事</H1>
[<A HREF="${HbaseDir}/history.cgi?saikin=99" class=\"M\" TARGET=_blank>過去${HtopLogTurn}ターン分のログを表示</A>]<BR><BR>
</DIV>
END
	for($i=0; $i < $HrepeatTurn; $i++){
		logFilePrint($i, 0, 0);
	}
	out(<<END);
<DIV ID='RecentlyLog'>
<H1>発見の記録</H1>
END
	historyPrint();
	out("</DIV>");
}

# 陣営表を表示
sub campInfoList {
	if(($Hallyflg) && (open(LIN, "${HlogdirName}/ally.log"))){
	out(<<END);
<HR><DIV ID='campInfo'>
<H1>各陣営の状況</H1>
<TABLE BORDER>
<TR>
<TH $HbgTitleCell>${HtagTH_}順位${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}グループ${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}${AfterName}数${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}総人口${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}占有率${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}総領土${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}総経済力${H_tagTH}</TH>
<TH $HbgTitleCell>${HtagTH_}総軍事力${H_tagTH}</TH>
</TR>
END
	my($i, $line, @ally, @apop, $up);
	$i = 1;
	while($line = <LIN>){
		# ターン,陣営ID,島数,総人口,総領土,総経済力,総軍事力
		@ally = split(/,/, $line);
		if($ally[0] != $HislandTurn){
			$apop[$ally[1]] = $ally[3];
			next;
		}
		out("<TR><TD $HbgNumberCell align=center><a href=\"$HthisFile?alist=$ally[1]\" class=\"M\">${HtagNumber_}$i${H_tagNumber}</a></TD>");
		if($ally[1] == 0){
			out("<TD $HbgNameCell>$Hallygroup[$ally[1]]</TD>");
		}else{
			out("<TD $HbgNameCell>$Hallymark[$ally[1]]${HtagTH_}$Hallygroup[$ally[1]]${H_tagTH}</TD>");
		}
		out("<TD $HbgInfoCell>$ally[2]</TD>");
		if(($HislandTurn % $HturnPrizeVarious) == 0){
			$up = "";
		}else{
			if($apop[$ally[1]] > $ally[3] + 100){
				$up = "↓";
			}elsif($apop[$ally[1]] < $ally[3] - 100){
				$up = "↑";
			}else{
				$up = "→";
			}
		}
		out("<TD $HbgInfoCell>$ally[3]${HunitPop} <B>$up</B></TD>");
		out("<TD $HbgInfoCell>$ally[7]%</TD>");
		out("<TD $HbgInfoCell>$ally[4]${HunitArea}</TD>");
		out("<TD $HbgInfoCell>$ally[5]${HunitMoney}</TD>");
		out("<TD $HbgInfoCell>$ally[6]P</TD></TR>");
		$i++;
	}
	close(LIN);
	out("</TABLE>");
	out("[<A HREF=\"${HbaseDir}/history.cgi?ally=0\" class=\"M\" TARGET=_blank>過去のデータ</a>]</DIV>");
	}
}
sub topPageAlist {
	out(<<END);
${HtagTitle_}$Htitle${HtagTitle2_}$Htitle2${H_tagTitle}${H_tagTitle}
<br><br>
ちょぴり隠し機能だったりする・・・。(<A HREF="${HthisFile}" class="M">通常の一覧画面に戻る</A>)<br>
<h2>$Hallygroup[$Halistmode]　$Hallymark[$Halistmode]　所属一覧</h2>
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
<INPUT TYPE="button" VALUE="クリップボードにコピー" onClick="textcopy(searchID('ALIST').value)">
エクセルとかに貼り付けて使ってください。<br>
<textarea NAME="ALIST" cols="100" rows="10">
END

	my($i,$island,$id,$name,$pop,$money,$food,$weapon);
	out("島名\t人口\t資金\t食料\t兵器\n");
	for($i = 0; $i < $HislandNumber; $i++){
		$island = $Hislands[$i];
		my($tAlly) = $island->{'ally'};
		if($Halistmode == $tAlly){
			$id = $island->{'id'};
			$name = $island->{'name'};
			$pop = $island->{'pop'} . $HunitPop;
			if($HhideMoneyMode == 1) {
				$money = $island->{'money'} . $HunitMoney;
			} elsif($HhideMoneyMode == 2) {
				$money = aboutMoney($island->{'money'});
			} else {
				$money = '機密';
			}
			$food = $island->{'food'} . $HunitFood;
			$weapon = $island->{'weapon'} . $HunitWeapon;
			out("$name$AfterName\t$pop\t$money\t$food\t$weapon\n");
		}
	}
	out("</textarea>");
	# 陣営表を表示
	&campInfoList;
}

# 記録ファイル表示
sub historyPrint {
	open(HIN, "${HlogdirName}/hakojima.his");
	my(@line, $l);
	while($l = <HIN>) {
		chomp($l);
		push(@line, $l);
	}
	@line = reverse(@line);

	foreach $l (@line) {
		$l =~ /^([0-9]*),(.*)$/;
		out("${HtagNumber_}ターン${1}${H_tagNumber}：${2}<BR>\n");
	}
	close(HIN);
}

1;
