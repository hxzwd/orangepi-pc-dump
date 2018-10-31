#!/usr/bin/perl


#print "perl_code [test_perl project:main.pl]\n"


$name = shift();
print("shift arg: $name\n");

$a = 123;
$b = 3.14159265358979323846;
$c = 0xFF;
$d = ($a + $b)/$c;
$d *= $a;

$str1 = "str one";
$str2 = "$str1 ; str two";
$str3 = $a."\n".$str2;
$str4 = '$str1';

print("$a\n$b\n$c\n$d\n\n$str1\n$str2\n$str3\n$str4\n");


$a = 2 ** 10;
$int1 = '12' * 2;
$str1 = '13'.37;

print("\n$a\t$int1\t$str1\n");


$str1 = 0 . 'abc';
$int1 = 'aaa' + 1;
$int2 = '12FF' + 1;

print("\n$str1\t$int1\t$int2\n");


$text1 = q {
first string
second string $15 ?
};

$text2 = qq {
	first string
	second string ( $name )
};

print("\n\n$text1\n\n$text2\n\n");

$scalar = "scalar";
($a, $b) = (15, 25);
@arr = ("aaa", 1337, $scalar, $a + $b);

print $arr[1]."\n";

push @arr, $a;

print pop(@arr)."\n";


@arr = qw/string1 string2 string3/;


%hash = (
	"x" => 12,
	y => 3.14159265358979323846,
	"z" => "HUI",
);

$hash{"x"}++;
$hash{y}/=2;

print "x = $hash{x}, y = $hash{y}, z = $hash{z}\n\n";


$a = shift;

if ($a > 1337) {
	print "a > 1337\n";
} else {
	print "a <= 1337\n";
}

if ($a > 0) {
	print "a > 0\n";
} elsif ($a == 0) {
	print "a == 0\n";
} else {
	print "a < 0\n";
}

unless ($a == 0) {
	print "$a != 0\n";
}
