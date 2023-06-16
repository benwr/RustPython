'Calendar printing functions\n\nNote when comparing these calendars to the ones printed by cal(1): By\ndefault, these calendars have Monday as the first day of the week, and\nSunday as the last (the European convention). Use setfirstweekday() to\nset the first day of the week (0=Monday, 6=Sunday).'
_I='calendar.css'
_H='</table>'
_G='<table border="0" cellpadding="0" cellspacing="0" class="%s">'
_F='<tr>%s</tr>'
_E='year'
_D='month'
_C=True
_B='\n'
_A=None
import sys,datetime,locale as _locale
from itertools import repeat
__all__=['IllegalMonthError','IllegalWeekdayError','setfirstweekday','firstweekday','isleap','leapdays','weekday','monthrange','monthcalendar','prmonth',_D,'prcal','calendar','timegm','month_name','month_abbr','day_name','day_abbr','Calendar','TextCalendar','HTMLCalendar','LocaleTextCalendar','LocaleHTMLCalendar','weekheader','MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']
error=ValueError
class IllegalMonthError(ValueError):
	def __init__(A,month):A.month=month
	def __str__(A):return'bad month number %r; must be 1-12'%A.month
class IllegalWeekdayError(ValueError):
	def __init__(A,weekday):A.weekday=weekday
	def __str__(A):return'bad weekday number %r; must be 0 (Monday) to 6 (Sunday)'%A.weekday
January=1
February=2
mdays=[0,31,28,31,30,31,30,31,31,30,31,30,31]
class _localized_month:
	_months=[datetime.date(2001,A+1,1).strftime for A in range(12)];_months.insert(0,lambda x:'')
	def __init__(A,format):A.format=format
	def __getitem__(A,i):
		B=A._months[i]
		if isinstance(i,slice):return[B(A.format)for B in B]
		else:return B(A.format)
	def __len__(A):return 13
class _localized_day:
	_days=[datetime.date(2001,1,A+1).strftime for A in range(7)]
	def __init__(A,format):A.format=format
	def __getitem__(A,i):
		B=A._days[i]
		if isinstance(i,slice):return[B(A.format)for B in B]
		else:return B(A.format)
	def __len__(A):return 7
day_name=_localized_day('%A')
day_abbr=_localized_day('%a')
month_name=_localized_month('%B')
month_abbr=_localized_month('%b')
MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY,SUNDAY=range(7)
def isleap(year):'Return True for leap years, False for non-leap years.';A=year;return A%4==0 and(A%100!=0 or A%400==0)
def leapdays(y1,y2):'Return number of leap years in range [y1, y2).\n       Assume y1 <= y2.';y1-=1;y2-=1;return y2//4-y1//4-(y2//100-y1//100)+(y2//400-y1//400)
def weekday(year,month,day):
	'Return weekday (0-6 ~ Mon-Sun) for year, month (1-12), day (1-31).';A=year
	if not datetime.MINYEAR<=A<=datetime.MAXYEAR:A=2000+A%400
	return datetime.date(A,month,day).weekday()
def monthrange(year,month):
	'Return weekday (0-6 ~ Mon-Sun) and number of days (28-31) for\n       year, month.';A=month
	if not 1<=A<=12:raise IllegalMonthError(A)
	B=weekday(year,A,1);C=mdays[A]+(A==February and isleap(year));return B,C
def _monthlen(year,month):A=month;return mdays[A]+(A==February and isleap(year))
def _prevmonth(year,month):
	A=month
	if A==1:return year-1,12
	else:return year,A-1
def _nextmonth(year,month):
	A=month
	if A==12:return year+1,1
	else:return year,A+1
class Calendar:
	"\n    Base calendar class. This class doesn't do any formatting. It simply\n    provides data to subclasses.\n    "
	def __init__(A,firstweekday=0):A.firstweekday=firstweekday
	def getfirstweekday(A):return A._firstweekday%7
	def setfirstweekday(A,firstweekday):A._firstweekday=firstweekday
	firstweekday=property(getfirstweekday,setfirstweekday)
	def iterweekdays(A):
		'\n        Return an iterator for one week of weekday numbers starting with the\n        configured first one.\n        '
		for B in range(A.firstweekday,A.firstweekday+7):yield B%7
	def itermonthdates(A,year,month):
		'\n        Return an iterator for one month. The iterator will yield datetime.date\n        values and will always iterate through complete weeks, so it will yield\n        dates outside the specified month.\n        '
		for(B,C,D)in A.itermonthdays3(year,month):yield datetime.date(B,C,D)
	def itermonthdays(A,year,month):'\n        Like itermonthdates(), but will yield day numbers. For days outside\n        the specified month the day number is 0.\n        ';B,C=monthrange(year,month);D=(B-A.firstweekday)%7;yield from repeat(0,D);yield from range(1,C+1);E=(A.firstweekday-B-C)%7;yield from repeat(0,E)
	def itermonthdays2(A,year,month):
		'\n        Like itermonthdates(), but will yield (day number, weekday number)\n        tuples. For days outside the specified month the day number is 0.\n        '
		for(B,C)in enumerate(A.itermonthdays(year,month),A.firstweekday):yield(C,B%7)
	def itermonthdays3(F,year,month):
		'\n        Like itermonthdates(), but will yield (year, month, day) tuples.  Can be\n        used for dates outside of datetime.date range.\n        ';B=month;C=year;G,H=monthrange(C,B);J=(G-F.firstweekday)%7;K=(F.firstweekday-G-H)%7;D,E=_prevmonth(C,B);I=_monthlen(D,E)+1
		for A in range(I-J,I):yield(D,E,A)
		for A in range(1,H+1):yield(C,B,A)
		D,E=_nextmonth(C,B)
		for A in range(1,K+1):yield(D,E,A)
	def itermonthdays4(A,year,month):
		'\n        Like itermonthdates(), but will yield (year, month, day, day_of_week) tuples.\n        Can be used for dates outside of datetime.date range.\n        '
		for(B,(C,D,E))in enumerate(A.itermonthdays3(year,month)):yield(C,D,E,(A.firstweekday+B)%7)
	def monthdatescalendar(B,year,month):"\n        Return a matrix (list of lists) representing a month's calendar.\n        Each row represents a week; week entries are datetime.date values.\n        ";A=list(B.itermonthdates(year,month));return[A[B:B+7]for B in range(0,len(A),7)]
	def monthdays2calendar(B,year,month):"\n        Return a matrix representing a month's calendar.\n        Each row represents a week; week entries are\n        (day number, weekday number) tuples. Day numbers outside this month\n        are zero.\n        ";A=list(B.itermonthdays2(year,month));return[A[B:B+7]for B in range(0,len(A),7)]
	def monthdayscalendar(B,year,month):"\n        Return a matrix representing a month's calendar.\n        Each row represents a week; days outside this month are zero.\n        ";A=list(B.itermonthdays(year,month));return[A[B:B+7]for B in range(0,len(A),7)]
	def yeardatescalendar(C,year,width=3):'\n        Return the data for the specified year ready for formatting. The return\n        value is a list of month rows. Each month row contains up to width months.\n        Each month contains between 4 and 6 weeks and each week contains 1-7\n        days. Days are datetime.date objects.\n        ';A=width;B=[C.monthdatescalendar(year,A)for A in range(January,January+12)];return[B[C:C+A]for C in range(0,len(B),A)]
	def yeardays2calendar(C,year,width=3):'\n        Return the data for the specified year ready for formatting (similar to\n        yeardatescalendar()). Entries in the week lists are\n        (day number, weekday number) tuples. Day numbers outside this month are\n        zero.\n        ';A=width;B=[C.monthdays2calendar(year,A)for A in range(January,January+12)];return[B[C:C+A]for C in range(0,len(B),A)]
	def yeardayscalendar(C,year,width=3):'\n        Return the data for the specified year ready for formatting (similar to\n        yeardatescalendar()). Entries in the week lists are day numbers.\n        Day numbers outside this month are zero.\n        ';A=width;B=[C.monthdayscalendar(year,A)for A in range(January,January+12)];return[B[C:C+A]for C in range(0,len(B),A)]
class TextCalendar(Calendar):
	'\n    Subclass of Calendar that outputs a calendar as a simple plain text\n    similar to the UNIX program cal.\n    '
	def prweek(A,theweek,width):'\n        Print a single week (no newline).\n        ';print(A.formatweek(theweek,width),end='')
	def formatday(B,day,weekday,width):
		'\n        Returns a formatted day.\n        '
		if day==0:A=''
		else:A='%2i'%day
		return A.center(width)
	def formatweek(A,theweek,width):'\n        Returns a single week in a string (no newline).\n        ';return' '.join(A.formatday(B,C,width)for(B,C)in theweek)
	def formatweekday(C,day,width):
		'\n        Returns a formatted week day name.\n        ';A=width
		if A>=9:B=day_name
		else:B=day_abbr
		return B[day][:A].center(A)
	def formatweekheader(A,width):'\n        Return a header for a week.\n        ';return' '.join(A.formatweekday(B,width)for B in A.iterweekdays())
	def formatmonthname(B,theyear,themonth,width,withyear=_C):
		'\n        Return a formatted month name.\n        ';A=month_name[themonth]
		if withyear:A='%s %r'%(A,theyear)
		return A.center(width)
	def prmonth(A,theyear,themonth,w=0,l=0):"\n        Print a month's calendar.\n        ";print(A.formatmonth(theyear,themonth,w,l),end='')
	def formatmonth(B,theyear,themonth,w=0,l=0):
		"\n        Return a month's calendar string (multi-line).\n        ";C=themonth;D=theyear;w=max(2,w);l=max(1,l);A=B.formatmonthname(D,C,7*(w+1)-1);A=A.rstrip();A+=_B*l;A+=B.formatweekheader(w).rstrip();A+=_B*l
		for E in B.monthdays2calendar(D,C):A+=B.formatweek(E,w).rstrip();A+=_B*l
		return A
	def formatyear(C,theyear,w=2,l=1,c=6,m=3):
		"\n        Returns a year's calendar as a multi-line string.\n        ";D=theyear;w=max(2,w);l=max(1,l);c=max(2,c);B=(w+1)*7-1;F=[];A=F.append;A(repr(D).center(B*m+c*(m-1)).rstrip());A(_B*l);L=C.formatweekheader(w)
		for(G,H)in enumerate(C.yeardays2calendar(D,m)):
			I=range(m*G+1,min(m*(G+1)+1,13));A(_B*l);M=(C.formatmonthname(D,A,B,False)for A in I);A(formatstring(M,B,c).rstrip());A(_B*l);N=(L for A in I);A(formatstring(N,B,c).rstrip());A(_B*l);O=max(len(A)for A in H)
			for J in range(O):
				E=[]
				for K in H:
					if J>=len(K):E.append('')
					else:E.append(C.formatweek(K[J],w))
				A(formatstring(E,B,c).rstrip());A(_B*l)
		return''.join(F)
	def pryear(A,theyear,w=0,l=0,c=6,m=3):"Print a year's calendar.";print(A.formatyear(theyear,w,l,c,m),end='')
class HTMLCalendar(Calendar):
	'\n    This calendar returns complete HTML pages.\n    ';cssclasses=['mon','tue','wed','thu','fri','sat','sun'];cssclasses_weekday_head=cssclasses;cssclass_noday='noday';cssclass_month_head=_D;cssclass_month=_D;cssclass_year_head=_E;cssclass_year=_E
	def formatday(A,day,weekday):
		'\n        Return a day as a table cell.\n        '
		if day==0:return'<td class="%s">&nbsp;</td>'%A.cssclass_noday
		else:return'<td class="%s">%d</td>'%(A.cssclasses[weekday],day)
	def formatweek(A,theweek):'\n        Return a complete week as a table row.\n        ';B=''.join(A.formatday(B,C)for(B,C)in theweek);return _F%B
	def formatweekday(A,day):'\n        Return a weekday name as a table header.\n        ';return'<th class="%s">%s</th>'%(A.cssclasses_weekday_head[day],day_abbr[day])
	def formatweekheader(A):'\n        Return a header for a week as a table row.\n        ';B=''.join(A.formatweekday(B)for B in A.iterweekdays());return _F%B
	def formatmonthname(C,theyear,themonth,withyear=_C):
		'\n        Return a month name as a table row.\n        ';A=themonth
		if withyear:B='%s %s'%(month_name[A],theyear)
		else:B='%s'%month_name[A]
		return'<tr><th colspan="7" class="%s">%s</th></tr>'%(C.cssclass_month_head,B)
	def formatmonth(B,theyear,themonth,withyear=_C):
		'\n        Return a formatted month as a table.\n        ';C=themonth;D=theyear;E=[];A=E.append;A(_G%B.cssclass_month);A(_B);A(B.formatmonthname(D,C,withyear=withyear));A(_B);A(B.formatweekheader());A(_B)
		for F in B.monthdays2calendar(D,C):A(B.formatweek(F));A(_B)
		A(_H);A(_B);return''.join(E)
	def formatyear(C,theyear,width=3):
		'\n        Return a formatted year as a table of tables.\n        ';D=theyear;B=width;E=[];A=E.append;B=max(B,1);A(_G%C.cssclass_year);A(_B);A('<tr><th colspan="%d" class="%s">%s</th></tr>'%(B,C.cssclass_year_head,D))
		for F in range(January,January+12,B):
			G=range(F,min(F+B,13));A('<tr>')
			for H in G:A('<td>');A(C.formatmonth(D,H,withyear=False));A('</td>')
			A('</tr>')
		A(_H);return''.join(E)
	def formatyearpage(E,theyear,width=3,css=_I,encoding=_A):
		'\n        Return a formatted year as a complete HTML page.\n        ';C=theyear;B=encoding
		if B is _A:B=sys.getdefaultencoding()
		D=[];A=D.append;A('<?xml version="1.0" encoding="%s"?>\n'%B);A('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n');A('<html>\n');A('<head>\n');A('<meta http-equiv="Content-Type" content="text/html; charset=%s" />\n'%B)
		if css is not _A:A('<link rel="stylesheet" type="text/css" href="%s" />\n'%css)
		A('<title>Calendar for %d</title>\n'%C);A('</head>\n');A('<body>\n');A(E.formatyear(C,width));A('</body>\n');A('</html>\n');return''.join(D).encode(B,'xmlcharrefreplace')
class different_locale:
	def __init__(A,locale):A.locale=locale;A.oldlocale=_A
	def __enter__(A):A.oldlocale=_locale.setlocale(_locale.LC_TIME,_A);_locale.setlocale(_locale.LC_TIME,A.locale)
	def __exit__(A,*B):
		if A.oldlocale is _A:return
		_locale.setlocale(_locale.LC_TIME,A.oldlocale)
def _get_default_locale():
	A=_locale.setlocale(_locale.LC_TIME,_A)
	if A=='C':
		with different_locale(''):A=_locale.setlocale(_locale.LC_TIME,_A)
	return A
class LocaleTextCalendar(TextCalendar):
	'\n    This class can be passed a locale name in the constructor and will return\n    month and weekday names in the specified locale.\n    '
	def __init__(B,firstweekday=0,locale=_A):
		A=locale;TextCalendar.__init__(B,firstweekday)
		if A is _A:A=_get_default_locale()
		B.locale=A
	def formatweekday(A,day,width):
		with different_locale(A.locale):return super().formatweekday(day,width)
	def formatmonthname(A,theyear,themonth,width,withyear=_C):
		with different_locale(A.locale):return super().formatmonthname(theyear,themonth,width,withyear)
class LocaleHTMLCalendar(HTMLCalendar):
	'\n    This class can be passed a locale name in the constructor and will return\n    month and weekday names in the specified locale.\n    '
	def __init__(B,firstweekday=0,locale=_A):
		A=locale;HTMLCalendar.__init__(B,firstweekday)
		if A is _A:A=_get_default_locale()
		B.locale=A
	def formatweekday(A,day):
		with different_locale(A.locale):return super().formatweekday(day)
	def formatmonthname(A,theyear,themonth,withyear=_C):
		with different_locale(A.locale):return super().formatmonthname(theyear,themonth,withyear)
c=TextCalendar()
firstweekday=c.getfirstweekday
def setfirstweekday(firstweekday):
	A=firstweekday
	if not MONDAY<=A<=SUNDAY:raise IllegalWeekdayError(A)
	c.firstweekday=A
monthcalendar=c.monthdayscalendar
prweek=c.prweek
week=c.formatweek
weekheader=c.formatweekheader
prmonth=c.prmonth
month=c.formatmonth
calendar=c.formatyear
prcal=c.pryear
_colwidth=7*3-1
_spacing=6
def format(cols,colwidth=_colwidth,spacing=_spacing):'Prints multi-column formatting for year calendars';print(formatstring(cols,colwidth,spacing))
def formatstring(cols,colwidth=_colwidth,spacing=_spacing):'Returns a string formatted from n strings, centered within n columns.';A=spacing;A*=' ';return A.join(A.center(colwidth)for A in cols)
EPOCH=1970
_EPOCH_ORD=datetime.date(EPOCH,1,1).toordinal()
def timegm(tuple):'Unrelated but handy function to calculate Unix timestamp from GMT.';A,B,C,D,E,F=tuple[:6];G=datetime.date(A,B,1).toordinal()-_EPOCH_ORD+C-1;H=G*24+D;I=H*60+E;J=I*60+F;return J
def main(args):
	I='html';J='text';import argparse as L;B=L.ArgumentParser();G=B.add_argument_group('text only arguments');M=B.add_argument_group('html only arguments');G.add_argument('-w','--width',type=int,default=2,help='width of date column (default 2)');G.add_argument('-l','--lines',type=int,default=1,help='number of lines for each week (default 1)');G.add_argument('-s','--spacing',type=int,default=6,help='spacing between months (default 6)');G.add_argument('-m','--months',type=int,default=3,help='months per row (default 3)');M.add_argument('-c','--css',default=_I,help='CSS to use for page');B.add_argument('-L','--locale',default=_A,help='locale to be used from month and weekday names');B.add_argument('-e','--encoding',default=_A,help='encoding to use for output');B.add_argument('-t','--type',default=J,choices=(J,I),help='output type (text or html)');B.add_argument(_E,nargs='?',type=int,help='year number (1-9999)');B.add_argument(_D,nargs='?',type=int,help='month number (1-12, text only)');A=B.parse_args(args[1:])
	if A.locale and not A.encoding:B.error('if --locale is specified --encoding is required');sys.exit(1)
	K=A.locale,A.encoding
	if A.type==I:
		if A.locale:C=LocaleHTMLCalendar(locale=K)
		else:C=HTMLCalendar()
		H=A.encoding
		if H is _A:H=sys.getdefaultencoding()
		D=dict(encoding=H,css=A.css);E=sys.stdout.buffer.write
		if A.year is _A:E(C.formatyearpage(datetime.date.today().year,**D))
		elif A.month is _A:E(C.formatyearpage(A.year,**D))
		else:B.error('incorrect number of arguments');sys.exit(1)
	else:
		if A.locale:C=LocaleTextCalendar(locale=K)
		else:C=TextCalendar()
		D=dict(w=A.width,l=A.lines)
		if A.month is _A:D['c']=A.spacing;D['m']=A.months
		if A.year is _A:F=C.formatyear(datetime.date.today().year,**D)
		elif A.month is _A:F=C.formatyear(A.year,**D)
		else:F=C.formatmonth(A.year,A.month,**D)
		E=sys.stdout.write
		if A.encoding:F=F.encode(A.encoding);E=sys.stdout.buffer.write
		E(F)
if __name__=='__main__':main(sys.argv)