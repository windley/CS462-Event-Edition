#!/usr/bin/perl

use Date::Calc qw(:all);

our(@start,@end,@date,@normal_classes,@last_class);

require "$ARGV[0].dat";

@date=@start;

my($i, $j, $month_text, $lectno);

$j = Delta_Days(@start,@end);
$lectno = 1;

print $page_start if (defined $page_start);

# print "$j\n";
for($i = 0; $i <= $j; $i++) {

    $dd = join(",",@date);
    # print a class date if this is a day the class meets or there's 
    # a special note on this day
    if ($normal_classes[Day_of_Week(@date)] || 
	(defined($special{$dd})) ||
	(defined($virtday{$dd}))) {
	$month_text = substr(Month_to_Text($date[1]),0,3);
	$lecture = "";
	$assn = "";
	$comments = "";
	if(Delta_Days(@date,@last_class) < 0) {
	    $lecture= "";
	} elsif(defined($holiday{$dd})) {
	    $lecture = "University Holiday";
	} elsif (defined($noclass{$dd})) {
	    $lecture = "No class";
	} elsif (defined($midterm{$dd})) {
	    $lecture = "Midterm, no class";
	    $comments = "Testing Center";
	} elsif ($normal_classes[Day_of_Week(@date)] ||
	         $virtday{$dd}) {

	    if(defined($lect_name[$lectno])) {
		$lecture = $lect_name[$lectno];
	    } else {
		$lecture = "Lecture $lectno";
	    }

	    my @l;

	    if (defined($wiki_url)) {
		@lectures = split("&", $lecture);
		foreach $lect (@lectures) {
		    $lect =~ s/^\s*($1)/$1/;
		    $lect =~ s/($1)\s*$/$1/;
		    $lecture_wiki = $lect;
		    $lecture_wiki =~ s/[\s:;,'"]//g;
		    push(@l, "<a href=\"$wiki_url$lecture_wiki\">$lect</a>");
                }
	    }
            $lecture = join(" &amp; ", @l);
	    $assn = "<a href=\"".$wiki_url."Homework$lectno\">HW$lectno" unless defined($noassign{$lectno}) || defined($noassignever);
	    $lectno++;
	} else {
	}

	if (defined($special{$dd})) {
	    $comments .= $special{$dd};
	}

	# print out the date if there's something there
	print <<EOF if (length($lecture . $assn . $comments) > 0);
<tr><td align="right">$month_text $date[2]</td>
    <td>$lecture</td>
    <td>$assn</td>
    <td>$comments</td>
</tr>
EOF
    }

    @date = Add_Delta_Days(@date,1);
}

print $page_end if (defined $page_end);

