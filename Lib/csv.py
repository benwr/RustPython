'\ncsv.py - read/write/investigate CSV files\n'
_E='raise'
_D='excel'
_C=True
_B=False
_A=None
import re
from _csv import Error,writer,reader,QUOTE_MINIMAL,QUOTE_ALL,QUOTE_NONNUMERIC,QUOTE_NONE,__doc__
from collections import OrderedDict
from io import StringIO
__all__=['QUOTE_MINIMAL','QUOTE_ALL','QUOTE_NONNUMERIC','QUOTE_NONE','Error','Dialect','__doc__',_D,'excel_tab','field_size_limit','reader','writer','Sniffer','unregister_dialect','__version__','DictReader','DictWriter','unix_dialect']
class Dialect:
	'Describe a CSV dialect.\n\n    This must be subclassed (see csv.excel).  Valid attributes are:\n    delimiter, quotechar, escapechar, doublequote, skipinitialspace,\n    lineterminator, quoting.\n\n    ';_name='';_valid=_B;delimiter=_A;quotechar=_A;escapechar=_A;doublequote=_A;skipinitialspace=_A;lineterminator=_A;quoting=_A
	def __init__(A):
		if A.__class__!=Dialect:A._valid=_C
		A._validate()
	def _validate(A):
		try:_Dialect(A)
		except TypeError as B:raise Error(str(B))
class excel(Dialect):'Describe the usual properties of Excel-generated CSV files.';delimiter=',';quotechar='"';doublequote=_C;skipinitialspace=_B;lineterminator='\r\n';quoting=QUOTE_MINIMAL
class excel_tab(excel):'Describe the usual properties of Excel-generated TAB-delimited files.';delimiter='\t'
class unix_dialect(Dialect):'Describe the usual properties of Unix-generated CSV files.';delimiter=',';quotechar='"';doublequote=_C;skipinitialspace=_B;lineterminator='\n';quoting=QUOTE_ALL
class DictReader:
	def __init__(A,f,fieldnames=_A,restkey=_A,restval=_A,dialect=_D,*C,**D):B=dialect;A._fieldnames=fieldnames;A.restkey=restkey;A.restval=restval;A.reader=reader(f,B,*C,**D);A.dialect=B;A.line_num=0
	def __iter__(A):return A
	@property
	def fieldnames(self):
		A=self
		if A._fieldnames is _A:
			try:A._fieldnames=next(A.reader)
			except StopIteration:pass
		A.line_num=A.reader.line_num;return A._fieldnames
	@fieldnames.setter
	def fieldnames(self,value):self._fieldnames=value
	def __next__(A):
		if A.line_num==0:A.fieldnames
		B=next(A.reader);A.line_num=A.reader.line_num
		while B==[]:B=next(A.reader)
		C=OrderedDict(zip(A.fieldnames,B));D=len(A.fieldnames);E=len(B)
		if D<E:C[A.restkey]=B[D:]
		elif D>E:
			for F in A.fieldnames[E:]:C[F]=A.restval
		return C
class DictWriter:
	def __init__(A,f,fieldnames,restval='',extrasaction=_E,dialect=_D,*C,**D):
		B=extrasaction;A.fieldnames=fieldnames;A.restval=restval
		if B.lower()not in(_E,'ignore'):raise ValueError("extrasaction (%s) must be 'raise' or 'ignore'"%B)
		A.extrasaction=B;A.writer=writer(f,dialect,*C,**D)
	def writeheader(A):B=dict(zip(A.fieldnames,A.fieldnames));A.writerow(B)
	def _dict_to_list(A,rowdict):
		B=rowdict
		if A.extrasaction==_E:
			C=B.keys()-A.fieldnames
			if C:raise ValueError('dict contains fields not in fieldnames: '+', '.join([repr(A)for A in C]))
		return(B.get(C,A.restval)for C in A.fieldnames)
	def writerow(A,rowdict):return A.writer.writerow(A._dict_to_list(rowdict))
	def writerows(A,rowdicts):return A.writer.writerows(map(A._dict_to_list,rowdicts))
try:complex
except NameError:complex=float
class Sniffer:
	'\n    "Sniffs" the format of a CSV file (i.e. delimiter, quotechar)\n    Returns a Dialect object.\n    '
	def __init__(A):A.preferred=[',','\t',';',' ',':']
	def sniff(C,sample,delimiters=_A):
		'\n        Returns a dialect (or None) corresponding to the sample\n        ';D=delimiters;E=sample;G,H,B,F=C._guess_quote_and_delimiter(E,D)
		if not B:B,F=C._guess_delimiter(E,D)
		if not B:raise Error('Could not determine delimiter')
		class A(Dialect):_name='sniffed';lineterminator='\r\n';quoting=QUOTE_MINIMAL
		A.doublequote=H;A.delimiter=B;A.quotechar=G or'"';A.skipinitialspace=F;return A
	def _guess_quote_and_delimiter(S,data,delimiters):
		"\n        Looks for text enclosed between two identical quotes\n        (the probable quotechar) which are preceded and followed\n        by the same character (the probable delimiter).\n        For example:\n                         ,'some text',\n        The quote with the most wins, same with the delimiter.\n        If there is no quotechar the delimiter can't be determined\n        this way.\n        ";I='delim';J='quote';K=delimiters;E=[]
		for Q in('(?P<delim>[^\\w\\n"\\\'])(?P<space> ?)(?P<quote>["\\\']).*?(?P=quote)(?P=delim)','(?:^|\\n)(?P<quote>["\\\']).*?(?P=quote)(?P<delim>[^\\w\\n"\\\'])(?P<space> ?)','(?P<delim>[^\\w\\n"\\\'])(?P<space> ?)(?P<quote>["\\\']).*?(?P=quote)(?:$|\\n)','(?:^|\\n)(?P<quote>["\\\']).*?(?P=quote)(?:$|\\n)'):
			L=re.compile(Q,re.DOTALL|re.MULTILINE);E=L.findall(data)
			if E:break
		if not E:return'',_B,_A,0
		F={};B={};M=0;G=L.groupindex
		for H in E:
			D=G[J]-1;A=H[D]
			if A:F[A]=F.get(A,0)+1
			try:D=G[I]-1;A=H[D]
			except KeyError:continue
			if A and(K is _A or A in K):B[A]=B.get(A,0)+1
			try:D=G['space']-1
			except KeyError:continue
			if H[D]:M+=1
		N=max(F,key=F.get)
		if B:
			C=max(B,key=B.get);O=B[C]==M
			if C=='\n':C=''
		else:C='';O=0
		R=re.compile('((%(delim)s)|^)\\W*%(quote)s[^%(delim)s\\n]*%(quote)s[^%(delim)s\\n]*%(quote)s\\W*((%(delim)s)|$)'%{I:re.escape(C),J:N},re.MULTILINE)
		if R.search(data):P=_C
		else:P=_B
		return N,P,C,O
	def _guess_delimiter(U,data,delimiters):
		"\n        The delimiter /should/ occur the same number of times on\n        each row. However, due to malformed data, it may not. We don't want\n        an all or nothing approach, so we allow for small variations in this\n        number.\n          1) build a table of the frequency of each character on every line.\n          2) build a table of frequencies of this frequency (meta-frequency?),\n             e.g.  'x occurred 5 times in 10 rows, 6 times in 1000 rows,\n             7 times in 2 rows'\n          3) use the mode of the meta-frequency to determine the /expected/\n             frequency for that character\n          4) find out how often the character actually meets that goal\n          5) the character that best meets its goal is the delimiter\n        For performance reasons, the data is evaluated in chunks, so it can\n        try and evaluate the smallest portion of the data possible, evaluating\n        additional chunks as necessary.\n        ";Q=delimiters;K='%c ';A=data;A=list(filter(_A,A.split('\n')));ascii=[chr(A)for A in range(127)];L=min(10,len(A));R=0;H={};E={};D={};M,N=0,L
		while M<len(A):
			R+=1
			for V in A[M:N]:
				for B in ascii:O=H.get(B,{});S=V.count(B);O[S]=O.get(S,0)+1;H[B]=O
			for B in H.keys():
				C=list(H[B].items())
				if len(C)==1 and C[0][0]==0:continue
				if len(C)>1:E[B]=max(C,key=lambda x:x[1]);C.remove(E[B]);E[B]=E[B][0],E[B][1]-sum(A[1]for A in C)
				else:E[B]=C[0]
			W=E.items();X=float(min(L*R,len(A)));P=1.;Y=.9
			while len(D)==0 and P>=Y:
				for(T,I)in W:
					if I[0]>0 and I[1]>0:
						if I[1]/X>=P and(Q is _A or T in Q):D[T]=I
				P-=.01
			if len(D)==1:F=list(D.keys())[0];G=A[0].count(F)==A[0].count(K%F);return F,G
			M=N;N+=L
		if not D:return'',0
		if len(D)>1:
			for J in U.preferred:
				if J in D.keys():G=A[0].count(J)==A[0].count(K%J);return J,G
		C=[(B,A)for(A,B)in D.items()];C.sort();F=C[-1][1];G=A[0].count(F)==A[0].count(K%F);return F,G
	def has_header(L,sample):
		H=sample;I=reader(StringIO(H),L.sniff(H));E=next(I);J=len(E);B={}
		for M in range(J):B[M]=_A
		K=0
		for F in I:
			if K>20:break
			K+=1
			if len(F)!=J:continue
			for A in list(B.keys()):
				for D in[int,float,complex]:
					try:D(F[A]);break
					except(ValueError,OverflowError):pass
				else:D=len(F[A])
				if D!=B[A]:
					if B[A]is _A:B[A]=D
					else:del B[A]
		C=0
		for(A,G)in B.items():
			if type(G)==type(0):
				if len(E[A])!=G:C+=1
				else:C-=1
			else:
				try:G(E[A])
				except(ValueError,TypeError):C+=1
				else:C-=1
		return C>0