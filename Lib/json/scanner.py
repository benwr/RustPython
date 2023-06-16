'JSON token scanner\n'
_A=None
import re
try:from _json import make_scanner as c_make_scanner
except ImportError:c_make_scanner=_A
__all__=['make_scanner']
NUMBER_RE=re.compile('(-?(?:0|[1-9]\\d*))(\\.\\d+)?([eE][-+]?\\d+)?',re.VERBOSE|re.MULTILINE|re.DOTALL)
def py_make_scanner(context):
	A=context;P=A.parse_object;Q=A.parse_array;R=A.parse_string;S=NUMBER_RE.match;G=A.strict;T=A.parse_float;U=A.parse_int;D=A.parse_constant;V=A.object_hook;W=A.object_pairs_hook;H=A.memo
	def E(string,idx):
		I='-Infinity';J='Infinity';K='NaN';B=string;A=idx
		try:C=B[A]
		except IndexError:raise StopIteration(A)from _A
		if C=='"':return R(B,A+1,G)
		elif C=='{':return P((B,A+1),G,E,V,W,H)
		elif C=='[':return Q((B,A+1),E)
		elif C=='n'and B[A:A+4]=='null':return _A,A+4
		elif C=='t'and B[A:A+4]=='true':return True,A+4
		elif C=='f'and B[A:A+5]=='false':return False,A+5
		F=S(B,A)
		if F is not _A:
			L,M,N=F.groups()
			if M or N:O=T(L+(M or'')+(N or''))
			else:O=U(L)
			return O,F.end()
		elif C=='N'and B[A:A+3]==K:return D(K),A+3
		elif C=='I'and B[A:A+8]==J:return D(J),A+8
		elif C=='-'and B[A:A+9]==I:return D(I),A+9
		else:raise StopIteration(A)
	def B(string,idx):
		try:return E(string,idx)
		finally:H.clear()
	return B
make_scanner=c_make_scanner or py_make_scanner