#!/usr/bin/perl

use Getopt::Std;
use Date::Calc qw(:all);
use YAML::XS;
use Data::Dumper;

use constant DEFAULT_CONFIG_FILE => 'class.dat';
use constant DEFAULT_LECTURES_FILE => 'lectures.yml';

# global options
use vars qw/ %clopt /;
my $opt_string = 'c:f:?h';
getopts( "$opt_string", \%clopt ) or usage();

usage() if $clopt{'h'} || $clopt{'?'};

warn "No config file specified. Using " . DEFAULT_CONFIG_FILE . "\n" unless $clopt{'c'};
my $config = ($clopt{'c'} || DEFAULT_CONFIG_FILE) ;

print "No lecture file specified. Using " . DEFAULT_LECTURE_FILE . "\n" unless $clopt{'f'};
my $lectures_top = read_config($clopt{'f'});
my $lectures = $lectures_top->{"Lectures"};

#print Dumper $lectures;

our(@start,@end,@date,@normal_classes,@last_class);

require $config;

@date=@start;

my($i, $j, $month_text, $lectno);

$j = Delta_Days(@start,@end);
$lectno = 0;

print $page_start if (defined $page_start);

# print "$j\n";
for($i = 0; $i <= $j; $i++) {

    my $lecture_html = "";
    my $lecture_title = "";
    my $reading_html = "";
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
	    $lecture_title = "University Holiday";
	} elsif (defined($noclass{$dd})) {
	    $lecture_title = "No class";
	} elsif (defined($midterm{$dd})) {
	    $lecture_title = "Midterm, no class";
	    $comments = "Testing Center";
	} elsif ($normal_classes[Day_of_Week(@date)] ||
	         $virtday{$dd}) {
	    
	    if(defined($lectures->[$lectno]->{"title"})) {
		$lecture_title = $lectures->[$lectno]->{"title"};
	    } else {
		$lecture_title = "Lecture $lectno";
	    }

	    my $lecture_url = $lectures->[$lectno]->{"url"};

	    if ($lecture_url eq "wiki") {
		$lecture_wiki = $lecture_title;
		$lecture_wiki =~ s/[\s:;,'"]//g;
		$lecture_wiki .= $wiki_ext if defined $wiki_ext;
		$lecture_url = $wiki_url . $lecture_wiki;
	    }

	    if (defined $lecture_url) {
		$lecture_html .= "<a href='$lecture_url'>$lecture_title</a>";
	    } else {
		$lecture_html .= $lecture_title;
	    }
	    
	    my $lecture_reading = $lectures->[$lectno]->{"reading"};

	    if (defined $lecture_reading) {
		my @reading = ();
		foreach my $ri (@{ $lecture_reading }) {
		      my $this_html = "";
		      if (defined $ri->{"title"}) {
			  $this_html .= $ri->{"title"};
			  if (defined $ri->{"url"}) {
			      $this_html = "<a href='" . $ri->{"url"} . "'>$this_html</a>";
			  }
			  # if (defined $ri->{"author"}) {
			  #     $this_html .= " by " . $ri->{"author"};
			  # }
			  push @reading, $this_html
		      } 
		}
		$reading_html = join("<br/>", @reading);

	    } else {
		$reading_html = "No assigned reading";
	    }
	    
	    $reading_html = "<div style='margin-top: 5px'>$reading_html</div>";

	    $assn = "<a href=\"".$wiki_url."Homework$lectno\">HW$lectno" unless defined($noassign{$lectno}) || defined($noassignever);
	    $lectno++;
	} else {
	}

	$lecture_html = $lecture_title unless ($lecture_html);


	if (defined($special{$dd})) {
	    $comments .= $special{$dd};
	}

	# print out the date if there's something there
	print <<EOF if (length($lecture_title . $assn . $comments) > 0);
<tr><td valign="top" align="right">$month_text $date[2]</td>
    <td valign="top">$lecture_html$reading_html</td>
    <td valign="top">$assn</td>
    <td valign="top">$comments</td>
</tr>
EOF
    }

    @date = Add_Delta_Days(@date,1);
}

print $page_end if (defined $page_end);

1;

#
# Message about this program and how to use it
#
sub usage {
    print STDERR << "EOF";

prepares a set of rulesets for deployment

usage: $0 [-h?] -v version

 -h|?       : this (help) message
 -c         : configuration file with (default: DEFAULT_CONFIG_FILE)
 -f         : lecture file (default: DEFAULT_LECTURE_FILE)

example: $0 -v v1 -c 462-config.dat -f 462-lectures.yml

EOF
    exit;
}

sub read_config {
    my ($filename) = @_;

    $filename ||= DEFAULT_LECTURE_FILE;

#    print "File ", $filename;
    my $config;
    if ( -e $filename ) {
      $config = YAML::XS::LoadFile($filename) ||
	warn "Can't open configuration file $filename: $!";
    }

    return $config;
}

sub read_file {
    my ($filename) = @_;
    local $/ = undef;
    open FILE, $filename or die "Couldn't open file: $!";
    $string = <FILE>;
    close FILE;
    return $string
}
