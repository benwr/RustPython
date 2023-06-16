"Support to pretty-print lists, tuples, & dictionaries recursively.\n\nVery simple, but useful, especially in debugging data structures.\n\nClasses\n-------\n\nPrettyPrinter()\n    Handle pretty-printing operations onto a stream using a configured\n    set of formatting parameters.\n\nFunctions\n---------\n\npformat()\n    Format a Python object into a pretty-printed representation.\n\npprint()\n    Pretty-print a Python object to a stream [default is sys.stdout].\n\nsaferepr()\n    Generate a 'standard' repr()-like value, but protect against recursive\n    data structures.\n\n"
_G=',\n'
_F='('
_E=')'
_D=' '
_C=None
_B=True
_A=False
import collections as _collections,dataclasses as _dataclasses,re,sys as _sys,types as _types
from io import StringIO as _StringIO
__all__=['pprint','pformat','isreadable','isrecursive','saferepr','PrettyPrinter','pp']
def pprint(object,stream=_C,indent=1,width=80,depth=_C,*,compact=_A,sort_dicts=_B,underscore_numbers=_A):'Pretty-print a Python object to a stream [default is sys.stdout].';A=PrettyPrinter(stream=stream,indent=indent,width=width,depth=depth,compact=compact,sort_dicts=sort_dicts,underscore_numbers=underscore_numbers);A.pprint(object)
def pformat(object,indent=1,width=80,depth=_C,*,compact=_A,sort_dicts=_B,underscore_numbers=_A):'Format a Python object into a pretty-printed representation.';return PrettyPrinter(indent=indent,width=width,depth=depth,compact=compact,sort_dicts=sort_dicts,underscore_numbers=underscore_numbers).pformat(object)
def pp(object,*A,sort_dicts=_A,**B):'Pretty-print a Python object';pprint(object,*A,sort_dicts=sort_dicts,**B)
def saferepr(object):'Version of repr() which can handle recursive data structures.';return PrettyPrinter()._safe_repr(object,{},_C,0)[0]
def isreadable(object):'Determine if saferepr(object) is readable by eval().';return PrettyPrinter()._safe_repr(object,{},_C,0)[1]
def isrecursive(object):'Determine if object requires a recursive representation.';return PrettyPrinter()._safe_repr(object,{},_C,0)[2]
class _safe_key:
	'Helper function for key functions when sorting unorderable objects.\n\n    The wrapped-object will fallback to a Py2.x style comparison for\n    unorderable types (sorting first comparing the type name and then by\n    the obj ids).  Does not work recursively, so dict.items() must have\n    _safe_key applied to both the key and the value.\n\n    ';__slots__=['obj']
	def __init__(A,obj):A.obj=obj
	def __lt__(A,other):
		B=other
		try:return A.obj<B.obj
		except TypeError:return(str(type(A.obj)),id(A.obj))<(str(type(B.obj)),id(B.obj))
def _safe_tuple(t):'Helper function for comparing 2-tuples';return _safe_key(t[0]),_safe_key(t[1])
class PrettyPrinter:
	def __init__(A,indent=1,width=80,depth=_C,stream=_C,*,compact=_A,sort_dicts=_B,underscore_numbers=_A):
		'Handle pretty printing operations onto a stream using a set of\n        configured parameters.\n\n        indent\n            Number of spaces to indent for each level of nesting.\n\n        width\n            Attempted maximum number of columns in the output.\n\n        depth\n            The maximum depth to print out nested structures.\n\n        stream\n            The desired output stream.  If omitted (or false), the standard\n            output stream available at construction will be used.\n\n        compact\n            If true, several items will be combined in one line.\n\n        sort_dicts\n            If true, dict keys are sorted.\n\n        ';E=stream;D=depth;B=width;C=indent;C=int(C);B=int(B)
		if C<0:raise ValueError('indent must be >= 0')
		if D is not _C and D<=0:raise ValueError('depth must be > 0')
		if not B:raise ValueError('width must be != 0')
		A._depth=D;A._indent_per_level=C;A._width=B
		if E is not _C:A._stream=E
		else:A._stream=_sys.stdout
		A._compact=bool(compact);A._sort_dicts=sort_dicts;A._underscore_numbers=underscore_numbers
	def pprint(A,object):
		if A._stream is not _C:A._format(object,A._stream,0,0,{},0);A._stream.write('\n')
	def pformat(B,object):A=_StringIO();B._format(object,A,0,0,{},0);return A.getvalue()
	def isrecursive(A,object):return A.format(object,{},0,0)[2]
	def isreadable(A,object):D,B,C=A.format(object,{},0,0);return B and not C
	def _format(B,object,stream,indent,allowance,context,level):
		E=level;F=allowance;G=indent;D=stream;A=context;C=id(object)
		if C in A:D.write(_recursion(object));B._recursive=_B;B._readable=_A;return
		H=B._repr(object,A,E);J=B._width-G-F
		if len(H)>J:
			I=B._dispatch.get(type(object).__repr__,_C)
			if I is not _C:A[C]=1;I(B,object,D,G,F,A,E+1);del A[C];return
			elif _dataclasses.is_dataclass(object)and not isinstance(object,type)and object.__dataclass_params__.repr and hasattr(object.__repr__,'__wrapped__')and'__create_fn__'in object.__repr__.__wrapped__.__qualname__:A[C]=1;B._pprint_dataclass(object,D,G,F,A,E+1);del A[C];return
		D.write(H)
	def _pprint_dataclass(D,object,stream,indent,allowance,context,level):B=indent;A=stream;C=object.__class__.__name__;B+=len(C)+1;E=[(A.name,getattr(object,A.name))for A in _dataclasses.fields(object)if A.repr];A.write(C+_F);D._format_namespace_items(E,A,B,allowance,context,level);A.write(_E)
	_dispatch={}
	def _pprint_dict(A,object,stream,indent,allowance,context,level):
		C=stream;B=C.write;B('{')
		if A._indent_per_level>1:B((A._indent_per_level-1)*_D)
		E=len(object)
		if E:
			if A._sort_dicts:D=sorted(object.items(),key=_safe_tuple)
			else:D=object.items()
			A._format_dict_items(D,C,indent,allowance+1,context,level)
		B('}')
	_dispatch[dict.__repr__]=_pprint_dict
	def _pprint_ordered_dict(C,object,stream,indent,allowance,context,level):
		A=stream
		if not len(object):A.write(repr(object));return
		B=object.__class__;A.write(B.__name__+_F);C._format(list(object.items()),A,indent+len(B.__name__)+1,allowance+1,context,level);A.write(_E)
	_dispatch[_collections.OrderedDict.__repr__]=_pprint_ordered_dict
	def _pprint_list(B,object,stream,indent,allowance,context,level):A=stream;A.write('[');B._format_items(object,A,indent,allowance+1,context,level);A.write(']')
	_dispatch[list.__repr__]=_pprint_list
	def _pprint_tuple(C,object,stream,indent,allowance,context,level):A=stream;A.write(_F);B=',)'if len(object)==1 else _E;C._format_items(object,A,indent,allowance+len(B),context,level);A.write(B)
	_dispatch[tuple.__repr__]=_pprint_tuple
	def _pprint_set(E,object,stream,indent,allowance,context,level):
		D=indent;A=stream
		if not len(object):A.write(repr(object));return
		B=object.__class__
		if B is set:A.write('{');C='}'
		else:A.write(B.__name__+'({');C='})';D+=len(B.__name__)+1
		object=sorted(object,key=_safe_key);E._format_items(object,A,D,allowance+len(C),context,level);A.write(C)
	_dispatch[set.__repr__]=_pprint_set;_dispatch[frozenset.__repr__]=_pprint_set
	def _pprint_str(P,object,stream,indent,allowance,context,level):
		G=level;H=allowance;I=indent;B=stream.write
		if not len(object):B(repr(object));return
		C=[];J=object.splitlines(_B)
		if G==1:I+=1;H+=1
		K=Q=P._width-I
		for(F,L)in enumerate(J):
			D=repr(L)
			if F==len(J)-1:K-=H
			if len(D)<=K:C.append(D)
			else:
				E=re.findall('\\S*\\s*',L);assert E;assert not E[-1];E.pop();M=Q;A=''
				for(R,N)in enumerate(E):
					O=A+N
					if R==len(E)-1 and F==len(J)-1:M-=H
					if len(repr(O))>M:
						if A:C.append(repr(A))
						A=N
					else:A=O
				if A:C.append(repr(A))
		if len(C)==1:B(D);return
		if G==1:B(_F)
		for(F,D)in enumerate(C):
			if F>0:B('\n'+_D*I)
			B(D)
		if G==1:B(_E)
	_dispatch[str.__repr__]=_pprint_str
	def _pprint_bytes(F,object,stream,indent,allowance,context,level):
		D=allowance;B=indent;A=stream.write
		if len(object)<=4:A(repr(object));return
		E=level==1
		if E:B+=1;D+=1;A(_F)
		C=''
		for G in _wrap_bytes_repr(object,F._width-B,D):
			A(C);A(G)
			if not C:C='\n'+_D*B
		if E:A(_E)
	_dispatch[bytes.__repr__]=_pprint_bytes
	def _pprint_bytearray(C,object,stream,indent,allowance,context,level):A=stream;B=A.write;B('bytearray(');C._pprint_bytes(bytes(object),A,indent+10,allowance+1,context,level+1);B(_E)
	_dispatch[bytearray.__repr__]=_pprint_bytearray
	def _pprint_mappingproxy(B,object,stream,indent,allowance,context,level):A=stream;A.write('mappingproxy(');B._format(object.copy(),A,indent+13,allowance+1,context,level);A.write(_E)
	_dispatch[_types.MappingProxyType.__repr__]=_pprint_mappingproxy
	def _pprint_simplenamespace(D,object,stream,indent,allowance,context,level):
		C=indent;A=stream
		if type(object)is _types.SimpleNamespace:B='namespace'
		else:B=object.__class__.__name__
		C+=len(B)+1;E=object.__dict__.items();A.write(B+_F);D._format_namespace_items(E,A,C,allowance,context,level);A.write(_E)
	_dispatch[_types.SimpleNamespace.__repr__]=_pprint_simplenamespace
	def _format_dict_items(A,items,stream,indent,allowance,context,level):
		D=level;E=context;F=stream;G=items;B=indent;C=F.write;B+=A._indent_per_level;J=_G+_D*B;K=len(G)-1
		for(L,(M,N))in enumerate(G):
			H=L==K;I=A._repr(M,E,D);C(I);C(': ');A._format(N,F,B+len(I)+2,allowance if H else 1,E,D)
			if not H:C(J)
	def _format_namespace_items(I,items,stream,indent,allowance,context,level):
		B=context;C=indent;D=stream;E=items;A=D.write;J=_G+_D*C;K=len(E)-1
		for(L,(F,G))in enumerate(E):
			H=L==K;A(F);A('=')
			if id(G)in B:A('...')
			else:I._format(G,D,C+len(F)+1,allowance if H else 1,B,level)
			if not H:A(J)
	def _format_items(A,items,stream,indent,allowance,context,level):
		I=level;J=context;K=stream;F=allowance;D=indent;E=K.write;D+=A._indent_per_level
		if A._indent_per_level>1:E((A._indent_per_level-1)*_D)
		L=_G+_D*D;B='';C=M=A._width-D+1;N=iter(items)
		try:O=next(N)
		except StopIteration:return
		G=_A
		while not G:
			P=O
			try:O=next(N)
			except StopIteration:G=_B;M-=F;C-=F
			if A._compact:
				Q=A._repr(P,J,I);H=len(Q)+2
				if C<H:
					C=M
					if B:B=L
				if C>=H:C-=H;E(B);B=', ';E(Q);continue
			E(B);B=L;A._format(P,K,D,F if G else 1,J,I)
	def _repr(A,object,context,level):
		repr,B,C=A.format(object,context.copy(),A._depth,level)
		if not B:A._readable=_A
		if C:A._recursive=_B
		return repr
	def format(A,object,context,maxlevels,level):"Format object for a specific context, returning a string\n        and flags indicating whether the representation is 'readable'\n        and whether the object represents a recursive construct.\n        ";return A._safe_repr(object,context,maxlevels,level)
	def _pprint_default_dict(C,object,stream,indent,allowance,context,level):
		D=level;E=context;B=indent;A=stream
		if not len(object):A.write(repr(object));return
		G=C._repr(object.default_factory,E,D);F=object.__class__;B+=len(F.__name__)+1;A.write('%s(%s,\n%s'%(F.__name__,G,_D*B));C._pprint_dict(object,A,B,allowance+1,E,D);A.write(_E)
	_dispatch[_collections.defaultdict.__repr__]=_pprint_default_dict
	def _pprint_counter(B,object,stream,indent,allowance,context,level):
		A=stream
		if not len(object):A.write(repr(object));return
		C=object.__class__;A.write(C.__name__+'({')
		if B._indent_per_level>1:A.write((B._indent_per_level-1)*_D)
		D=object.most_common();B._format_dict_items(D,A,indent+len(C.__name__)+1,allowance+2,context,level);A.write('})')
	_dispatch[_collections.Counter.__repr__]=_pprint_counter
	def _pprint_chain_map(C,object,stream,indent,allowance,context,level):
		D=level;E=context;B=indent;A=stream
		if not len(object.maps):A.write(repr(object));return
		F=object.__class__;A.write(F.__name__+_F);B+=len(F.__name__)+1
		for(H,G)in enumerate(object.maps):
			if H==len(object.maps)-1:C._format(G,A,B,allowance+1,E,D);A.write(_E)
			else:C._format(G,A,B,1,E,D);A.write(_G+_D*B)
	_dispatch[_collections.ChainMap.__repr__]=_pprint_chain_map
	def _pprint_deque(C,object,stream,indent,allowance,context,level):
		D=level;E=context;B=indent;A=stream
		if not len(object):A.write(repr(object));return
		F=object.__class__;A.write(F.__name__+_F);B+=len(F.__name__)+1;A.write('[')
		if object.maxlen is _C:C._format_items(object,A,B,allowance+2,E,D);A.write('])')
		else:C._format_items(object,A,B,2,E,D);G=C._repr(object.maxlen,E,D);A.write('],\n%smaxlen=%s)'%(_D*B,G))
	_dispatch[_collections.deque.__repr__]=_pprint_deque
	def _pprint_user_dict(A,object,stream,indent,allowance,context,level):A._format(object.data,stream,indent,allowance,context,level-1)
	_dispatch[_collections.UserDict.__repr__]=_pprint_user_dict
	def _pprint_user_list(A,object,stream,indent,allowance,context,level):A._format(object.data,stream,indent,allowance,context,level-1)
	_dispatch[_collections.UserList.__repr__]=_pprint_user_list
	def _pprint_user_string(A,object,stream,indent,allowance,context,level):A._format(object.data,stream,indent,allowance,context,level-1)
	_dispatch[_collections.UserString.__repr__]=_pprint_user_string
	def _safe_repr(G,object,context,maxlevels,level):
		C=level;D=maxlevels;A=context;E=type(object)
		if E in _builtin_scalars:return repr(object),_B,_A
		J=getattr(E,'__repr__',_C)
		if issubclass(E,int)and J is int.__repr__:
			if G._underscore_numbers:return f"{object:_d}",_B,_A
			else:return repr(object),_B,_A
		if issubclass(E,dict)and J is dict.__repr__:
			if not object:return'{}',_B,_A
			B=id(object)
			if D and C>=D:return'{...}',_A,B in A
			if B in A:return _recursion(object),_A,_B
			A[B]=1;F=_B;H=_A;I=[];K=I.append;C+=1
			if G._sort_dicts:M=sorted(object.items(),key=_safe_tuple)
			else:M=object.items()
			for(N,O)in M:
				P,Q,R=G.format(N,A,D,C);S,T,U=G.format(O,A,D,C);K('%s: %s'%(P,S));F=F and Q and T
				if R or U:H=_B
			del A[B];return'{%s}'%', '.join(I),F,H
		if issubclass(E,list)and J is list.__repr__ or issubclass(E,tuple)and J is tuple.__repr__:
			if issubclass(E,list):
				if not object:return'[]',_B,_A
				format='[%s]'
			elif len(object)==1:format='(%s,)'
			else:
				if not object:return'()',_B,_A
				format='(%s)'
			B=id(object)
			if D and C>=D:return format%'...',_A,B in A
			if B in A:return _recursion(object),_A,_B
			A[B]=1;F=_B;H=_A;I=[];K=I.append;C+=1
			for V in object:
				W,X,Y=G.format(V,A,D,C);K(W)
				if not X:F=_A
				if Y:H=_B
			del A[B];return format%', '.join(I),F,H
		L=repr(object);return L,L and not L.startswith('<'),_A
_builtin_scalars=frozenset({str,bytes,bytearray,float,complex,bool,type(_C)})
def _recursion(object):return'<Recursion on %s with id=%s>'%(type(object).__name__,id(object))
def _wrap_bytes_repr(object,width,allowance):
	C=width;A=b'';F=len(object)//4*4
	for B in range(0,len(object),4):
		D=object[B:B+4];E=A+D
		if B==F:C-=allowance
		if len(repr(E))>C:
			if A:yield repr(A)
			A=D
		else:A=E
	if A:yield repr(A)