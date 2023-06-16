'Implementation of JSONEncoder\n'
_E='\\u{0:04x}'
_D='\n'
_C=False
_B=True
_A=None
import re
try:from _json import encode_basestring_ascii as c_encode_basestring_ascii
except ImportError:c_encode_basestring_ascii=_A
try:from _json import encode_basestring as c_encode_basestring
except ImportError:c_encode_basestring=_A
try:from _json import make_encoder as c_make_encoder
except ImportError:c_make_encoder=_A
ESCAPE=re.compile('[\\x00-\\x1f\\\\"\\b\\f\\n\\r\\t]')
ESCAPE_ASCII=re.compile('([\\\\"]|[^\\ -~])')
HAS_UTF8=re.compile(b'[\x80-\xff]')
ESCAPE_DCT={'\\':'\\\\','"':'\\"','\x08':'\\b','\x0c':'\\f',_D:'\\n','\r':'\\r','\t':'\\t'}
for i in range(32):ESCAPE_DCT.setdefault(chr(i),_E.format(i))
INFINITY=float('inf')
def py_encode_basestring(s):
	'Return a JSON representation of a Python string\n\n    '
	def A(match):return ESCAPE_DCT[match.group(0)]
	return'"'+ESCAPE.sub(A,s)+'"'
encode_basestring=c_encode_basestring or py_encode_basestring
def py_encode_basestring_ascii(s):
	'Return an ASCII-only JSON representation of a Python string\n\n    '
	def A(match):
		B=match.group(0)
		try:return ESCAPE_DCT[B]
		except KeyError:
			A=ord(B)
			if A<65536:return _E.format(A)
			else:A-=65536;C=55296|A>>10&1023;D=56320|A&1023;return'\\u{0:04x}\\u{1:04x}'.format(C,D)
	return'"'+ESCAPE_ASCII.sub(A,s)+'"'
encode_basestring_ascii=c_encode_basestring_ascii or py_encode_basestring_ascii
class JSONEncoder:
	'Extensible JSON <http://json.org> encoder for Python data structures.\n\n    Supports the following objects and types by default:\n\n    +-------------------+---------------+\n    | Python            | JSON          |\n    +===================+===============+\n    | dict              | object        |\n    +-------------------+---------------+\n    | list, tuple       | array         |\n    +-------------------+---------------+\n    | str               | string        |\n    +-------------------+---------------+\n    | int, float        | number        |\n    +-------------------+---------------+\n    | True              | true          |\n    +-------------------+---------------+\n    | False             | false         |\n    +-------------------+---------------+\n    | None              | null          |\n    +-------------------+---------------+\n\n    To extend this to recognize other objects, subclass and implement a\n    ``.default()`` method with another method that returns a serializable\n    object for ``o`` if possible, otherwise it should call the superclass\n    implementation (to raise ``TypeError``).\n\n    ';item_separator=', ';key_separator=': '
	def __init__(A,*,skipkeys=_C,ensure_ascii=_B,check_circular=_B,allow_nan=_B,sort_keys=_C,indent=_A,separators=_A,default=_A):
		"Constructor for JSONEncoder, with sensible defaults.\n\n        If skipkeys is false, then it is a TypeError to attempt\n        encoding of keys that are not str, int, float or None.  If\n        skipkeys is True, such items are simply skipped.\n\n        If ensure_ascii is true, the output is guaranteed to be str\n        objects with all incoming non-ASCII characters escaped.  If\n        ensure_ascii is false, the output can contain non-ASCII characters.\n\n        If check_circular is true, then lists, dicts, and custom encoded\n        objects will be checked for circular references during encoding to\n        prevent an infinite recursion (which would cause an RecursionError).\n        Otherwise, no such check takes place.\n\n        If allow_nan is true, then NaN, Infinity, and -Infinity will be\n        encoded as such.  This behavior is not JSON specification compliant,\n        but is consistent with most JavaScript based encoders and decoders.\n        Otherwise, it will be a ValueError to encode such floats.\n\n        If sort_keys is true, then the output of dictionaries will be\n        sorted by key; this is useful for regression tests to ensure\n        that JSON serializations can be compared on a day-to-day basis.\n\n        If indent is a non-negative integer, then JSON array\n        elements and object members will be pretty-printed with that\n        indent level.  An indent level of 0 will only insert newlines.\n        None is the most compact representation.\n\n        If specified, separators should be an (item_separator, key_separator)\n        tuple.  The default is (', ', ': ') if *indent* is ``None`` and\n        (',', ': ') otherwise.  To get the most compact JSON representation,\n        you should specify (',', ':') to eliminate whitespace.\n\n        If specified, default is a function that gets called for objects\n        that can't otherwise be serialized.  It should return a JSON encodable\n        version of the object or raise a ``TypeError``.\n\n        ";B=default;C=separators;D=indent;A.skipkeys=skipkeys;A.ensure_ascii=ensure_ascii;A.check_circular=check_circular;A.allow_nan=allow_nan;A.sort_keys=sort_keys;A.indent=D
		if C is not _A:A.item_separator,A.key_separator=C
		elif D is not _A:A.item_separator=','
		if B is not _A:A.default=B
	def default(A,o):'Implement this method in a subclass such that it returns\n        a serializable object for ``o``, or calls the base implementation\n        (to raise a ``TypeError``).\n\n        For example, to support arbitrary iterators, you could\n        implement default like this::\n\n            def default(self, o):\n                try:\n                    iterable = iter(o)\n                except TypeError:\n                    pass\n                else:\n                    return list(iterable)\n                # Let the base class default method raise the TypeError\n                return JSONEncoder.default(self, o)\n\n        ';raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")
	def encode(B,o):
		'Return a JSON string representation of a Python data structure.\n\n        >>> from json.encoder import JSONEncoder\n        >>> JSONEncoder().encode({"foo": ["bar", "baz"]})\n        \'{"foo": ["bar", "baz"]}\'\n\n        '
		if isinstance(o,str):
			if B.ensure_ascii:return encode_basestring_ascii(o)
			else:return encode_basestring(o)
		A=B.iterencode(o,_one_shot=_B)
		if not isinstance(A,(list,tuple)):A=list(A)
		return''.join(A)
	def iterencode(A,o,_one_shot=_C):
		'Encode the given object and yield each string\n        representation as available.\n\n        For example::\n\n            for chunk in JSONEncoder().iterencode(bigobject):\n                mysocket.write(chunk)\n\n        ';D=_one_shot
		if A.check_circular:B={}
		else:B=_A
		if A.ensure_ascii:C=encode_basestring_ascii
		else:C=encode_basestring
		def F(o,allow_nan=A.allow_nan,_repr=float.__repr__,_inf=INFINITY,_neginf=-INFINITY):
			if o!=o:A='NaN'
			elif o==_inf:A='Infinity'
			elif o==_neginf:A='-Infinity'
			else:return _repr(o)
			if not allow_nan:raise ValueError('Out of range float values are not JSON compliant: '+repr(o))
			return A
		if D and c_make_encoder is not _A and A.indent is _A:E=c_make_encoder(B,A.default,C,A.indent,A.key_separator,A.item_separator,A.sort_keys,A.skipkeys,A.allow_nan)
		else:E=_make_iterencode(B,A.default,C,A.indent,F,A.key_separator,A.item_separator,A.sort_keys,A.skipkeys,D)
		return E(o,0)
def _make_iterencode(markers,_default,_encoder,_indent,_floatstr,_key_separator,_item_separator,_sort_keys,_skipkeys,_one_shot,ValueError=ValueError,dict=dict,float=float,id=id,int=int,isinstance=isinstance,list=list,str=str,tuple=tuple,_intstr=int.__repr__):
	P='Circular reference detected';G='false';H='true';I='null';J=_intstr;K=_item_separator;L=_floatstr;M=_encoder;D=_indent;A=markers
	if D is not _A and not isinstance(D,str):D=' '*D
	def Q(lst,_current_indent_level):
		F=lst;E=_current_indent_level
		if not F:yield'[]';return
		if A is not _A:
			S=id(F)
			if S in A:raise ValueError(P)
			A[S]=F
		C='['
		if D is not _A:E+=1;O=_D+D*E;U=K+O;C+=O
		else:O=_A;U=K
		V=_B
		for B in F:
			if V:V=_C
			else:C=U
			if isinstance(B,str):yield C+M(B)
			elif B is _A:yield C+I
			elif B is _B:yield C+H
			elif B is _C:yield C+G
			elif isinstance(B,int):yield C+J(B)
			elif isinstance(B,float):yield C+L(B)
			else:
				yield C
				if isinstance(B,(list,tuple)):T=Q(B,E)
				elif isinstance(B,dict):T=R(B,E)
				else:T=N(B,E)
				yield from T
		if O is not _A:E-=1;yield _D+D*E
		yield']'
		if A is not _A:del A[S]
	def R(dct,_current_indent_level):
		F=dct;E=_current_indent_level
		if not F:yield'{}';return
		if A is not _A:
			S=id(F)
			if S in A:raise ValueError(P)
			A[S]=F
		yield'{'
		if D is not _A:E+=1;O=_D+D*E;U=K+O;yield O
		else:O=_A;U=K
		V=_B
		if _sort_keys:W=sorted(F.items())
		else:W=F.items()
		for(B,C)in W:
			if isinstance(B,str):0
			elif isinstance(B,float):B=L(B)
			elif B is _B:B=H
			elif B is _C:B=G
			elif B is _A:B=I
			elif isinstance(B,int):B=J(B)
			elif _skipkeys:continue
			else:raise TypeError(f"keys must be str, int, float, bool or None, not {B.__class__.__name__}")
			if V:V=_C
			else:yield U
			yield M(B);yield _key_separator
			if isinstance(C,str):yield M(C)
			elif C is _A:yield I
			elif C is _B:yield H
			elif C is _C:yield G
			elif isinstance(C,int):yield J(C)
			elif isinstance(C,float):yield L(C)
			else:
				if isinstance(C,(list,tuple)):T=Q(C,E)
				elif isinstance(C,dict):T=R(C,E)
				else:T=N(C,E)
				yield from T
		if O is not _A:E-=1;yield _D+D*E
		yield'}'
		if A is not _A:del A[S]
	def N(o,_current_indent_level):
		B=_current_indent_level
		if isinstance(o,str):yield M(o)
		elif o is _A:yield I
		elif o is _B:yield H
		elif o is _C:yield G
		elif isinstance(o,int):yield J(o)
		elif isinstance(o,float):yield L(o)
		elif isinstance(o,(list,tuple)):yield from Q(o,B)
		elif isinstance(o,dict):yield from R(o,B)
		else:
			if A is not _A:
				C=id(o)
				if C in A:raise ValueError(P)
				A[C]=o
			o=_default(o);yield from N(o,B)
			if A is not _A:del A[C]
	return N