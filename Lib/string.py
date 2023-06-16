'A collection of string constants.\n\nPublic module variables:\n\nwhitespace -- a string containing all ASCII whitespace\nascii_lowercase -- a string containing all ASCII lowercase letters\nascii_uppercase -- a string containing all ASCII uppercase letters\nascii_letters -- a string containing all ASCII letters\ndigits -- a string containing all ASCII decimal digits\nhexdigits -- a string containing all ASCII hexadecimal digits\noctdigits -- a string containing all ASCII octal digits\npunctuation -- a string containing all ASCII punctuation characters\nprintable -- a string containing all ASCII characters considered printable\n\n'
_E='Unrecognized named group in pattern'
_D='escaped'
_C='braced'
_B='invalid'
_A=None
__all__=['ascii_letters','ascii_lowercase','ascii_uppercase','capwords','digits','hexdigits','octdigits','printable','punctuation','whitespace','Formatter','Template']
import _string
whitespace=' \t\n\r\x0b\x0c'
ascii_lowercase='abcdefghijklmnopqrstuvwxyz'
ascii_uppercase='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters=ascii_lowercase+ascii_uppercase
digits='0123456789'
hexdigits=digits+'abcdef'+'ABCDEF'
octdigits='01234567'
punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
printable=digits+ascii_letters+punctuation+whitespace
def capwords(s,sep=_A):'capwords(s [,sep]) -> string\n\n    Split the argument into words using split, capitalize each\n    word using capitalize, and join the capitalized words using\n    join.  If the optional second argument sep is absent or None,\n    runs of whitespace characters are replaced by a single space\n    and leading and trailing whitespace are removed, otherwise\n    sep is used to split and join the words.\n\n    ';return(sep or' ').join(A.capitalize()for A in s.split(sep))
import re as _re
from collections import ChainMap as _ChainMap
_sentinel_dict={}
class Template:
	'A string class for supporting $-substitutions.';delimiter='$';idpattern='(?a:[_a-z][_a-z0-9]*)';braceidpattern=_A;flags=_re.IGNORECASE
	def __init_subclass__(A):
		super().__init_subclass__()
		if'pattern'in A.__dict__:B=A.pattern
		else:C=_re.escape(A.delimiter);id=A.idpattern;D=A.braceidpattern or A.idpattern;B=f"""
            {C}(?:
              (?P<escaped>{C})  |   # Escape sequence of two delimiters
              (?P<named>{id})       |   # delimiter and a Python identifier
              {{(?P<braced>{D})}} |   # delimiter and a braced identifier
              (?P<invalid>)             # Other ill-formed delimiter exprs
            )
            """
		A.pattern=_re.compile(B,A.flags|_re.VERBOSE)
	def __init__(A,template):A.template=template
	def _invalid(E,mo):
		B=mo.start(_B);A=E.template[:B].splitlines(keepends=True)
		if not A:C=1;D=1
		else:C=B-len(''.join(A[:-1]));D=len(A)
		raise ValueError('Invalid placeholder in string: line %d, col %d'%(D,C))
	def substitute(A,B=_sentinel_dict,**C):
		if B is _sentinel_dict:B=C
		elif C:B=_ChainMap(C,B)
		def D(mo):
			C=mo;D=C.group('named')or C.group(_C)
			if D is not _A:return str(B[D])
			if C.group(_D)is not _A:return A.delimiter
			if C.group(_B)is not _A:A._invalid(C)
			raise ValueError(_E,A.pattern)
		return A.pattern.sub(D,A.template)
	def safe_substitute(C,B=_sentinel_dict,**A):
		if B is _sentinel_dict:B=A
		elif A:B=_ChainMap(A,B)
		def D(mo):
			A=mo;D=A.group('named')or A.group(_C)
			if D is not _A:
				try:return str(B[D])
				except KeyError:return A.group()
			if A.group(_D)is not _A:return C.delimiter
			if A.group(_B)is not _A:return A.group()
			raise ValueError(_E,C.pattern)
		return C.pattern.sub(D,C.template)
Template.__init_subclass__()
class Formatter:
	def format(A,B,*C,**D):return A.vformat(B,C,D)
	def vformat(A,format_string,args,kwargs):B=kwargs;C=set();D,E=A._vformat(format_string,args,B,C,2);A.check_unused_args(C,args,B);return D
	def _vformat(B,format_string,args,kwargs,used_args,recursion_depth,auto_arg_index=0):
		G='cannot switch from manual field specification to automatic field numbering';H=False;I=recursion_depth;J=used_args;K=kwargs;A=auto_arg_index
		if I<0:raise ValueError('Max string recursion exceeded')
		D=[]
		for(L,C,E,M)in B.parse(format_string):
			if L:D.append(L)
			if C is not _A:
				if C=='':
					if A is H:raise ValueError(G)
					C=str(A);A+=1
				elif C.isdigit():
					if A:raise ValueError(G)
					A=H
				F,N=B.get_field(C,args,K);J.add(N);F=B.convert_field(F,M);E,A=B._vformat(E,args,K,J,I-1,auto_arg_index=A);D.append(B.format_field(F,E))
		return''.join(D),A
	def get_value(B,key,args,kwargs):
		A=key
		if isinstance(A,int):return args[A]
		else:return kwargs[A]
	def check_unused_args(A,used_args,args,kwargs):0
	def format_field(A,value,format_spec):return format(value,format_spec)
	def convert_field(C,value,conversion):
		B=value;A=conversion
		if A is _A:return B
		elif A=='s':return str(B)
		elif A=='r':return repr(B)
		elif A=='a':return ascii(B)
		raise ValueError('Unknown conversion specifier {0!s}'.format(A))
	def parse(A,format_string):return _string.formatter_parser(format_string)
	def get_field(D,field_name,args,kwargs):
		B,E=_string.formatter_field_name_split(field_name);A=D.get_value(B,args,kwargs)
		for(F,C)in E:
			if F:A=getattr(A,C)
			else:A=A[C]
		return A,B