#!/usr/local/bin/perl --

#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# アクセス解析スクリプト(長猫さんのanalyzer.cgiを改造) ver1.01
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
#==================================================================
#	Log analyzer CGI
#
#  last update: 02/18/2002
#       author: 長猫
#          url: http://www.midnightroam.org/
#
#
#  miniBBS++専用アクセス解析CGIです。ログファイル名は
#  miniBBS++のアクセスログファイルを指定してください。
#
#	Copyright (c) 2000-2002  Twilight Heaven
#==================================================================
#  アクセスログを取得しているときに、それを管理目的でブラウザで見るためものです。
#  箱庭の設置に必須なものではないため設置は任意です。
#  通常は、hako-mente.cgiの管理人室から開いてください。
#  02/12/23 V0.01 neo_otackyさんが箱庭用に修正したのを一部究想用に修正。
#==================================================================

#use strict;

# 初期設定用ファイルを読み込む
require './hako-init.cgi';

#=========================
# 初期設定
#=========================
my $title        = 'Log analyzer CGI';	# タイトル
my $logfile      = './axes.cgi';	# ログファイル名（hako-main.cgiと同じ）

my $axeslog_no = 50;			# アクセス・ログ表示数（最大記録件数$HaxesMaxより小さい値）
my $referer_hide = 1;			# リファラを非表示にする(1 -> Yes, 0 -> No)
my $referer_sweep = 1;			# リンク先にリファラを渡さない(2 -> Yes[JavaScript(IEのみ)], 1 -> Yes[CGI], 0 -> No)
my $delaytime = 0;				# リファラを渡さない場合の、リフレッシュ時間

my $script       = './analyzer.cgi';	# このスクリプトの名前
my $separator    = ' - ';		# 各行の項目の分割文字
#=========================
# 初期設定ここまで
#=========================
my $copyright = "<DIV align=right>[ <A href=\"http://www.midnightroam.org/\">Log analyzer CGI</A> ]\n</DIV>";
my %CATEGORY = (
	'date'    => '日別',
	'hour'    => '時間帯',
	'referer' => 'リファラ',
	'host'    => 'ホスト名',
	'addr'    => 'IPアドレス',
	'agent'   => 'ブラウザ名',
	'id'   => 'ID',
	'a'   => 'アクセス・ログ',
);
my $rs = <<"END" if(!$referer_hide && $referer_sweep);
<script Language="JavaScript">
<!--
	function link(url){
		app = navigator.appName.charAt(0);
		if(app == 'M') { 
			w = window.open('','','');
			w.document.write("<html><head>");
			w.document.write("<meta HTTP-EQUIV='refresh' CONTENT='$delaytime; URL="+ url +"'></head>");
			w.document.write("<body>");
			w.document.write("</body>");
			w.document.write("</html>");
			w.location.reload();
		} else {
			document.write("<html><head>");
			document.write("<meta HTTP-EQUIV='refresh' CONTENT='$delaytime; URL="+ url +"'></head>");
			document.write("<body>");
			document.write("</body>");
			document.write("</html>");
		}
	}
//-->
</SCRIPT>
END

if (-e $HpasswordFile) {
    # パスワードファイルがある
    open(PIN, "<$HpasswordFile") || die $!;
    chomp($HmasterPassword = <PIN>); # マスタパスワードを読み込む
    close(PIN);
}

	
my $url = $ENV{'QUERY_STRING'};
$url =~ s/^url\=(.*)/$1/;
if ($url eq ''){
	# フォームからの投稿をデコード
	%FORM = &form_decode;
	$referer_hide = 1 if(!passCheck());

	if ($FORM{'mode'} eq 'analyze') {
		&analyze($FORM{'category'});
	}
	else {
		&html();
	}
} else{
	print <<"EOF";
Content-type: text/html

<html>
<head>
<title>Referrer-Sweeper</title>
<meta HTTP-EQUIV="refresh" CONTENT="$delaytime; URL=$url">
$rs
</head>
<body>
<h1>
アクセス中...  しばらくお待ちください...
<hr>
<center>
<a href="javascript:link($url);">$url</a>
</center>
</h1>
</body>
</html>
EOF
}
#===============================
# デコード処理
#===============================
sub form_decode {
	
	my(
		$data,
		@pairs,
		%FORM,
	);
	
	# 通常リクエストメソッドは「GET」,「POST」のように大文字。でも念のため(汗
	if (uc($ENV{'REQUEST_METHOD'}) eq 'POST') {
		read(STDIN, $data, $ENV{'CONTENT_LENGTH'});
		@pairs = split(/&/, $data);
		foreach (@pairs) {
			my($name,$value) = split(/=/, $_);
			$value =~ tr/+/ /;
			$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
			&jcode'convert(\$value,'sjis');
			$value =~ s/&/&amp;/g;
			$value =~ s/\r\n/\n/g;
			$value =~ s/\r|\n/<BR>/g;
			$FORM{$name} = $value;
			
			# 不正な入力を排除
			$FORM{'select_date'} =~ s/\"|\@|\/|\`|\\//g;
		}
	}
	
	return %FORM;
}
#=========================
# 解析っぽい処理。
#=========================
sub analyze {
	
	my $category = shift;
	my(
		
		$tmp,
		$item,
		$all,
		$per,
		$result,
		%DATA,
	);

	open(LOG, "$logfile");
	while ( <LOG> ) {
		if (!$_) {
			last;
		}
		if ($category eq 'date') {
			$tmp = (split $separator)[0];
			$item = substr($tmp, 1, 14);
		}
		elsif ($category eq 'hour') {
			$tmp = (split $separator)[0];
			$item = substr($tmp, 16, 2) . '時';
			$item =~ s/^0/&nbsp;/;
		}
		elsif ($category eq 'referer') {
			if ($referer_hide) {
				&html('<DIV align=center>リファラは現在非表示設定になっています。</DIV>');
			}
			$item = (split $separator)[1];
 			if($referer_sweep == 1) {
				$item =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#]+)/$1<A href=\"$script\?$2" target=\"_blank\">$2<\/A>/g;
			}
			elsif($referer_sweep == 2) {
				$item =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#]+)/$1<A href=\"javascript:link(\'$2\')\;\">$2<\/A>/g;
			}
			else {
				$item =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#]+)/$1<A href=$2 target=\"_blank\">$2<\/A>/g;
			}
		}
		elsif ($category eq 'host') {
			$item = (split $separator)[2];
			if ($item =~ /^.+\.(.+)\.(ac|ne|go|gr|co|or|ad)\.jp$/i) {
				$item = "*\.$1\.$2\.jp";
			}
			elsif ($item =~ /^YahooBB(\d+)\.bbtec\.net$/i) {
				$item = "YahooBB***.bbtec.net";
			}
		}
		elsif ($category eq 'addr') {
			$item = (split $separator)[3];
		}
		elsif ($category eq 'agent') {
			$item = (split $separator)[4];
		}
		elsif ($category eq 'id') {
			$item = (split $separator)[5];
		}
		elsif ($category eq 'a'){
			$tmp = (split $separator)[0];
			$item .= '<TR><TD><nobr>' . substr($tmp, 1, 23) . '</nobr></TD>';
			$tmp = (split $separator)[5];
			chomp $tmp;
			$item .= '<TD align=right><nobr>' . $tmp . '</nobr></TD>';
			$item .= '<TD><nobr>' . (split $separator)[2] . '</nobr></TD>';
			$item .= '<TD><nobr>' . (split $separator)[3] . '</nobr></TD>';
			$item .= '<TD><nobr>' . (split $separator)[4] . '</nobr></TD>';
			if (!$referer_hide) {
				$tmp = (split $separator)[1];
 				if($referer_sweep == 1) {
					$tmp =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#]+)/$1<A href=\"$script\?$2" target=\"_blank\">$2<\/A>/g;
				}
				elsif($referer_sweep == 2) {
					$tmp =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#]+)/$1<A href=\"javascript:link(\'$2\')\;\">$2<\/A>/g;
				}
				else {
					$tmp =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#]+)/$1<A href=$2 target=\"_blank\">$2<\/A>/g;
				}
				$item .= '<TD><nobr>' . $tmp . '</nobr></TD></TR>';
			}
		}
		
		chomp $item;
		$DATA{$item}++;
		$all++;
		last if(($category eq 'a') && ($all > $axeslog_no - 1));
	}
	
	close(LOG);
	
	if($category ne 'a'){
		$result  = "<DIV align=center>\n<TABLE border=0 cellPadding=2 cellSpacing=5>\n";
		$result .= "<TR><TD align=center>$CATEGORY{$category}</TD><TD align=center>回数</TD><TD align=center>割合</TD></TR>\n";
	
		foreach (sort { $DATA{$b} <=> $DATA{$a} } keys %DATA) {
			if ($_ eq '') {
				$DATA{'none'} = $DATA{$_};
				$_ = 'none';
			}
			$per = sprintf("%.1f", ($DATA{$_} / $all)*100);
			$result .= "<TR><TD>$_</TD><TD align=center>$DATA{$_}</TD><TD align=center>( $per\% )</TD></TR>\n";
		}

		$result .= "<TR><TD colSpan=3><HR color=#FFFFFF size=1 noShade></TD></TR>\n";
		$result .= "<TR><TD><BR></TD><TD align=center>$all</TD><TD align=center><BR></TD></TR>\n";
		$result .= "</TABLE>\n</DIV>";
	} else {
		$result = "<TABLE border=1 cellpadding=1 cellspacing=0><TBODY>\n";
		$result .= "<TR>";
		$result .= "<TH>Date</TH>";
		$result .= "<TH>ID</TH>";
		$result .= "<TH>Host</TH>";
		$result .= "<TH>Ip</TH>";
		$result .= "<TH>Agent</TH>";
		$result .= "<TH>Referer</TH>" if (!$referer_hide);
		$result .= "</TR>\n";
		$result .= $item;
		$result .= "</TBODY></TABLE>";
	}
	
	&html($result);
}
#=========================
# パスワード関連
#=========================
# パスチェック
sub passCheck {
    if(checkMasterPassword($FORM{'password'})) {
		return 1;
    } else {
	print "${HtagBig_}パスワードが違います${H_tagBig}";
        return 0;
    }
}

# マスタパスワードのチェック
sub checkMasterPassword {
    my $pass = shift;
    return (crypt($pass, 'ma') eq $HmasterPassword);
}
#=========================
# HTMLを出力。
#=========================
sub html {
	my $result = shift;
	my $i = 0;
	my $option_list;
	
	foreach (sort keys %CATEGORY) {
		next if(!passCheck() && ($_ eq 'a' || $_ eq 'addr' || $_ eq 'id'));
		if ($i == 0) {
			$option_list .= "<OPTION value=\"$_\" selected>$CATEGORY{$_}\n";
			$i++;
		}
		else {
			$option_list .= "<OPTION value=\"$_\">$CATEGORY{$_}\n";
		}
	}
	
	chomp $option_list;
	
	print "Content-Type: text/html\n\n";
	print <<"__HTML__";
<HTML>
<HEAD>
<TITLE>$title</TITLE>
<META http-equiv="Content-Style-Type" content="text/css">
<META http-equiv="Content-Type" content="text/html;charset=Shift_JIS">
<STYLE type="text/css">
<!--
A			{ text-decoration:none }
A:link			{ color:#FF0000 }
A:visited		{ color:#FFFF00 }
A:hover			{ text-decoration:underline; color:#00FF00 }
BODY,TD			{ font-size:12px; }
BODY			{
				scrollbar-Track-Color:      #000000;
				scrollbar-Face-Color:       #000000;
				scrollbar-Shadow-Color:     #778899;
				scrollbar-DarkShadow-Color: #333333;
				scrollbar-Highlight-Color:  #FFFFFF;
				scrollbar-3dLight-Color:    #606060;
				scrollbar-Arrow-Color:      #FFFFFF;
			}
INPUT,SELECT,TEXTAREA	{
				color:#778899;
				border-color:#333333;
				background:#000000;
			}
-->
</STYLE>
__HTML__

	print "$rs" if(!$referer_hide && ($referer_sweep == 2));

	print <<"__HTML__";
</HEAD>
<BODY bgColor=#000000 text=#CCCCCC>
$title
<HR size=1 color=#FFFFFF width=100% noShade>
<BR>
<BR>
<FORM action="$script" method=POST>
<B>マスタパスワード：</B><INPUT type=password size=16 maxlength=32 name=password value="$FORM{'password'}">
<BR>
<INPUT type=hidden name=mode value="analyze">
<SELECT name=category>
$option_list
</SELECT>
<INPUT type=submit value='集計'>
</FORM>
<BR>
<BR>
<BR>
<BR>
$result
<BR>
$copyright
</BODY>
</HTML>
__HTML__
	
	exit;
}
