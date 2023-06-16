'Implementation of JSONDecoder\n'
_E="Expecting ',' delimiter"
_D='Expecting value'
_C=True
_B='\n'
_A=None
import re
from json import scanner
try:from _json import scanstring as c_scanstring
except ImportError:c_scanstring=_A
__all__=['JSONDecoder','JSONDecodeError']
FLAGS=re.VERBOSE|re.MULTILINE|re.DOTALL
NaN=float('nan')
PosInf=float('inf')
NegInf=float('-inf')
class JSONDecodeError(ValueError):
	'Subclass of ValueError with the following additional properties:\n\n    msg: The unformatted error message\n    doc: The JSON document being parsed\n    pos: The start index of doc where parsing failed\n    lineno: The line corresponding to pos\n    colno: The column corresponding to pos\n\n    '
	@classmethod
	def _from_serde(C,msg,doc,line,col):
		B=line;A=0;B-=1;col-=1
		while B>0:D=doc.index(_B,A);B-=1;A=D
		A+=col;return C(msg,doc,A)
	def __init__(A,msg,doc,pos):C=doc;B=pos;D=C.count(_B,0,B)+1;E=B-C.rfind(_B,0,B);F='%s: line %d column %d (char %d)'%(msg,D,E,B);ValueError.__init__(A,F);A.msg=msg;A.doc=C;A.pos=B;A.lineno=D;A.colno=E
	def __reduce__(A):return A.__class__,(A.msg,A.doc,A.pos)
_CONSTANTS={'-Infinity':NegInf,'Infinity':PosInf,'NaN':NaN}
STRINGCHUNK=re.compile('(.*?)(["\\\\\\x00-\\x1f])',FLAGS)
BACKSLASH={'"':'"','\\':'\\','/':'/','b':'\x08','f':'\x0c','n':_B,'r':'\r','t':'\t'}
def _decode_uXXXX(s,pos):
	A=pos;B=s[A+1:A+5]
	if len(B)==4 and B[1]not in'xX':
		try:return int(B,16)
		except ValueError:pass
	C='Invalid \\uXXXX escape';raise JSONDecodeError(C,s,A)
def py_scanstring(s,end,strict=_C,_b=BACKSLASH,_m=STRINGCHUNK.match):
	'Scan the string s for a JSON string. End is the index of the\n    character in s after the quote that started the JSON string.\n    Unescapes all valid JSON string escape sequences and raises ValueError\n    on attempt to decode an invalid string. If strict is False then literal\n    control characters are allowed in the string.\n\n    Returns a tuple of the decoded string and the index of the character in s\n    after the end quote.';H='Unterminated string starting at';A=end;I=[];D=I.append;J=A-1
	while 1:
		E=_m(s,A)
		if E is _A:raise JSONDecodeError(H,s,J)
		A=E.end();K,B=E.groups()
		if K:D(K)
		if B=='"':break
		elif B!='\\':
			if strict:F='Invalid control character {0!r} at'.format(B);raise JSONDecodeError(F,s,A)
			else:D(B);continue
		try:G=s[A]
		except IndexError:raise JSONDecodeError(H,s,J)from _A
		if G!='u':
			try:L=_b[G]
			except KeyError:F='Invalid \\escape: {0!r}'.format(G);raise JSONDecodeError(F,s,A)
			A+=1
		else:
			C=_decode_uXXXX(s,A);A+=5
			if 55296<=C<=56319 and s[A:A+2]=='\\u':
				M=_decode_uXXXX(s,A+1)
				if 56320<=M<=57343:C=65536+(C-55296<<10|M-56320);A+=6
			L=chr(C)
		D(L)
	return''.join(I),A
scanstring=c_scanstring or py_scanstring
WHITESPACE=re.compile('[ \\t\\n\\r]*',FLAGS)
WHITESPACE_STR=' \t\n\r'
def JSONObject(s_and_end,strict,scan_once,object_hook,object_pairs_hook,memo=_A,_w=WHITESPACE.match,_ws=WHITESPACE_STR):
	L='Expecting property name enclosed in double quotes';J=memo;F=_ws;G=object_pairs_hook;H=object_hook;E=_w;B,A=s_and_end;D=[];M=D.append
	if J is _A:J={}
	N=J.setdefault;C=B[A:A+1]
	if C!='"':
		if C in F:A=E(B,A).end();C=B[A:A+1]
		if C=='}':
			if G is not _A:K=G(D);return K,A+1
			D={}
			if H is not _A:D=H(D)
			return D,A+1
		elif C!='"':raise JSONDecodeError(L,B,A)
	A+=1
	while _C:
		I,A=scanstring(B,A,strict);I=N(I,I)
		if B[A:A+1]!=':':
			A=E(B,A).end()
			if B[A:A+1]!=':':raise JSONDecodeError("Expecting ':' delimiter",B,A)
		A+=1
		try:
			if B[A]in F:
				A+=1
				if B[A]in F:A=E(B,A+1).end()
		except IndexError:pass
		try:O,A=scan_once(B,A)
		except StopIteration as P:raise JSONDecodeError(_D,B,P.value)from _A
		M((I,O))
		try:
			C=B[A]
			if C in F:A=E(B,A+1).end();C=B[A]
		except IndexError:C=''
		A+=1
		if C=='}':break
		elif C!=',':raise JSONDecodeError(_E,B,A-1)
		A=E(B,A).end();C=B[A:A+1];A+=1
		if C!='"':raise JSONDecodeError(L,B,A-1)
	if G is not _A:K=G(D);return K,A
	D=dict(D)
	if H is not _A:D=H(D)
	return D,A
def JSONArray(s_and_end,scan_once,_w=WHITESPACE.match,_ws=WHITESPACE_STR):
	D=_ws;B,A=s_and_end;E=[];C=B[A:A+1]
	if C in D:A=_w(B,A+1).end();C=B[A:A+1]
	if C==']':return E,A+1
	F=E.append
	while _C:
		try:G,A=scan_once(B,A)
		except StopIteration as H:raise JSONDecodeError(_D,B,H.value)from _A
		F(G);C=B[A:A+1]
		if C in D:A=_w(B,A+1).end();C=B[A:A+1]
		A+=1
		if C==']':break
		elif C!=',':raise JSONDecodeError(_E,B,A-1)
		try:
			if B[A]in D:
				A+=1
				if B[A]in D:A=_w(B,A+1).end()
		except IndexError:pass
	return E,A
class JSONDecoder:
	'Simple JSON <http://json.org> decoder\n\n    Performs the following translations in decoding by default:\n\n    +---------------+-------------------+\n    | JSON          | Python            |\n    +===============+===================+\n    | object        | dict              |\n    +---------------+-------------------+\n    | array         | list              |\n    +---------------+-------------------+\n    | string        | str               |\n    +---------------+-------------------+\n    | number (int)  | int               |\n    +---------------+-------------------+\n    | number (real) | float             |\n    +---------------+-------------------+\n    | true          | True              |\n    +---------------+-------------------+\n    | false         | False             |\n    +---------------+-------------------+\n    | null          | None              |\n    +---------------+-------------------+\n\n    It also understands ``NaN``, ``Infinity``, and ``-Infinity`` as\n    their corresponding ``float`` values, which is outside the JSON spec.\n\n    '
	def __init__(A,*,object_hook=_A,parse_float=_A,parse_int=_A,parse_constant=_A,strict=_C,object_pairs_hook=_A):"``object_hook``, if specified, will be called with the result\n        of every JSON object decoded and its return value will be used in\n        place of the given ``dict``.  This can be used to provide custom\n        deserializations (e.g. to support JSON-RPC class hinting).\n\n        ``object_pairs_hook``, if specified will be called with the result of\n        every JSON object decoded with an ordered list of pairs.  The return\n        value of ``object_pairs_hook`` will be used instead of the ``dict``.\n        This feature can be used to implement custom decoders.\n        If ``object_hook`` is also defined, the ``object_pairs_hook`` takes\n        priority.\n\n        ``parse_float``, if specified, will be called with the string\n        of every JSON float to be decoded. By default this is equivalent to\n        float(num_str). This can be used to use another datatype or parser\n        for JSON floats (e.g. decimal.Decimal).\n\n        ``parse_int``, if specified, will be called with the string\n        of every JSON int to be decoded. By default this is equivalent to\n        int(num_str). This can be used to use another datatype or parser\n        for JSON integers (e.g. float).\n\n        ``parse_constant``, if specified, will be called with one of the\n        following strings: -Infinity, Infinity, NaN.\n        This can be used to raise an exception if invalid JSON numbers\n        are encountered.\n\n        If ``strict`` is false (true is the default), then control\n        characters will be allowed inside strings.  Control characters in\n        this context are those with character codes in the 0-31 range,\n        including ``'\\t'`` (tab), ``'\\n'``, ``'\\r'`` and ``'\\0'``.\n        ";A.object_hook=object_hook;A.parse_float=parse_float or float;A.parse_int=parse_int or int;A.parse_constant=parse_constant or _CONSTANTS.__getitem__;A.strict=strict;A.object_pairs_hook=object_pairs_hook;A.parse_object=JSONObject;A.parse_array=JSONArray;A.parse_string=scanstring;A.memo={};A.scan_once=scanner.make_scanner(A)
	def decode(B,s,_w=WHITESPACE.match):
		'Return the Python representation of ``s`` (a ``str`` instance\n        containing a JSON document).\n\n        ';C,A=B.raw_decode(s,idx=_w(s,0).end());A=_w(s,A).end()
		if A!=len(s):raise JSONDecodeError('Extra data',s,A)
		return C
	def raw_decode(A,s,idx=0):
		'Decode a JSON document from ``s`` (a ``str`` beginning with\n        a JSON document) and return a 2-tuple of the Python\n        representation and the index in ``s`` where the document ended.\n\n        This can be used to decode a JSON document from a string that may\n        have extraneous data at the end.\n\n        '
		try:B,C=A.scan_once(s,idx)
		except StopIteration as D:raise JSONDecodeError(_D,s,D.value)from _A
		return B,C