'functools.py - Tools for working with functions and callable objects\n'
_N='__abstractmethods__'
_M='__isabstractmethod__'
_L='__dict__'
_K='__annotations__'
_J='__name__'
_I='__get__'
_H=', '
_G='func'
_F='__ge__'
_E='__gt__'
_D='__le__'
_C='__lt__'
_B=False
_A=None
__all__=['update_wrapper','wraps','WRAPPER_ASSIGNMENTS','WRAPPER_UPDATES','total_ordering','cmp_to_key','lru_cache','reduce','partial','partialmethod','singledispatch','singledispatchmethod','cached_property']
from abc import get_cache_token
from collections import namedtuple
from reprlib import recursive_repr
from _thread import RLock
from types import GenericAlias
WRAPPER_ASSIGNMENTS='__module__',_J,'__qualname__','__doc__',_K
WRAPPER_UPDATES=_L,
def update_wrapper(wrapper,wrapped,assigned=WRAPPER_ASSIGNMENTS,updated=WRAPPER_UPDATES):
	'Update a wrapper function to look like the wrapped function\n\n       wrapper is the function to be updated\n       wrapped is the original function\n       assigned is a tuple naming the attributes assigned directly\n       from the wrapped function to the wrapper function (defaults to\n       functools.WRAPPER_ASSIGNMENTS)\n       updated is a tuple naming the attributes of the wrapper that\n       are updated with the corresponding attribute from the wrapped\n       function (defaults to functools.WRAPPER_UPDATES)\n    ';C=wrapped;B=wrapper
	for A in assigned:
		try:D=getattr(C,A)
		except AttributeError:pass
		else:setattr(B,A,D)
	for A in updated:getattr(B,A).update(getattr(C,A,{}))
	B.__wrapped__=C;return B
def wraps(wrapped,assigned=WRAPPER_ASSIGNMENTS,updated=WRAPPER_UPDATES):'Decorator factory to apply update_wrapper() to a wrapper function\n\n       Returns a decorator that invokes update_wrapper() with the decorated\n       function as the wrapper argument and the arguments to wraps() as the\n       remaining arguments. Default arguments are as for update_wrapper().\n       This is a convenience function to simplify applying partial() to\n       update_wrapper().\n    ';return partial(update_wrapper,wrapped=wrapped,assigned=assigned,updated=updated)
def _gt_from_lt(self,other,NotImplemented=NotImplemented):
	'Return a > b.  Computed by @total_ordering from (not a < b) and (a != b).';B=other;A=self.__lt__(B)
	if A is NotImplemented:return A
	return not A and self!=B
def _le_from_lt(self,other,NotImplemented=NotImplemented):'Return a <= b.  Computed by @total_ordering from (a < b) or (a == b).';A=other;B=self.__lt__(A);return B or self==A
def _ge_from_lt(self,other,NotImplemented=NotImplemented):
	'Return a >= b.  Computed by @total_ordering from (not a < b).';A=self.__lt__(other)
	if A is NotImplemented:return A
	return not A
def _ge_from_le(self,other,NotImplemented=NotImplemented):
	'Return a >= b.  Computed by @total_ordering from (not a <= b) or (a == b).';B=other;A=self.__le__(B)
	if A is NotImplemented:return A
	return not A or self==B
def _lt_from_le(self,other,NotImplemented=NotImplemented):
	'Return a < b.  Computed by @total_ordering from (a <= b) and (a != b).';B=other;A=self.__le__(B)
	if A is NotImplemented:return A
	return A and self!=B
def _gt_from_le(self,other,NotImplemented=NotImplemented):
	'Return a > b.  Computed by @total_ordering from (not a <= b).';A=self.__le__(other)
	if A is NotImplemented:return A
	return not A
def _lt_from_gt(self,other,NotImplemented=NotImplemented):
	'Return a < b.  Computed by @total_ordering from (not a > b) and (a != b).';B=other;A=self.__gt__(B)
	if A is NotImplemented:return A
	return not A and self!=B
def _ge_from_gt(self,other,NotImplemented=NotImplemented):'Return a >= b.  Computed by @total_ordering from (a > b) or (a == b).';A=other;B=self.__gt__(A);return B or self==A
def _le_from_gt(self,other,NotImplemented=NotImplemented):
	'Return a <= b.  Computed by @total_ordering from (not a > b).';A=self.__gt__(other)
	if A is NotImplemented:return A
	return not A
def _le_from_ge(self,other,NotImplemented=NotImplemented):
	'Return a <= b.  Computed by @total_ordering from (not a >= b) or (a == b).';B=other;A=self.__ge__(B)
	if A is NotImplemented:return A
	return not A or self==B
def _gt_from_ge(self,other,NotImplemented=NotImplemented):
	'Return a > b.  Computed by @total_ordering from (a >= b) and (a != b).';B=other;A=self.__ge__(B)
	if A is NotImplemented:return A
	return A and self!=B
def _lt_from_ge(self,other,NotImplemented=NotImplemented):
	'Return a < b.  Computed by @total_ordering from (not a >= b).';A=self.__ge__(other)
	if A is NotImplemented:return A
	return not A
_convert={_C:[(_E,_gt_from_lt),(_D,_le_from_lt),(_F,_ge_from_lt)],_D:[(_F,_ge_from_le),(_C,_lt_from_le),(_E,_gt_from_le)],_E:[(_C,_lt_from_gt),(_F,_ge_from_gt),(_D,_le_from_gt)],_F:[(_D,_le_from_ge),(_E,_gt_from_ge),(_C,_lt_from_ge)]}
def total_ordering(cls):
	'Class decorator that fills in missing ordering methods';A=cls;B={B for B in _convert if getattr(A,B,_A)is not getattr(object,B,_A)}
	if not B:raise ValueError('must define at least one ordering operation: < > <= >=')
	E=max(B)
	for(C,D)in _convert[E]:
		if C not in B:D.__name__=C;setattr(A,C,D)
	return A
def cmp_to_key(mycmp):
	'Convert a cmp= function into a key= function';A=mycmp
	class B:
		__slots__=['obj']
		def __init__(A,obj):A.obj=obj
		def __lt__(B,other):return A(B.obj,other.obj)<0
		def __gt__(B,other):return A(B.obj,other.obj)>0
		def __eq__(B,other):return A(B.obj,other.obj)==0
		def __le__(B,other):return A(B.obj,other.obj)<=0
		def __ge__(B,other):return A(B.obj,other.obj)>=0
		__hash__=_A
	return B
try:from _functools import cmp_to_key
except ImportError:pass
_initial_missing=object()
def reduce(function,sequence,initial=_initial_missing):
	'\n    reduce(function, sequence[, initial]) -> value\n\n    Apply a function of two arguments cumulatively to the items of a sequence,\n    from left to right, so as to reduce the sequence to a single value.\n    For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates\n    ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items\n    of the sequence in the calculation, and serves as a default when the\n    sequence is empty.\n    ';B=initial;C=iter(sequence)
	if B is _initial_missing:
		try:A=next(C)
		except StopIteration:raise TypeError('reduce() of empty sequence with no initial value')from _A
	else:A=B
	for D in C:A=function(A,D)
	return A
try:from _functools import reduce
except ImportError:pass
class partial:
	'New function with partial application of the given arguments\n    and keywords.\n    ';__slots__=_G,'args','keywords',_L,'__weakref__'
	def __new__(E,A,*C,**D):
		if not callable(A):raise TypeError('the first argument must be callable')
		if hasattr(A,_G):C=A.args+C;D={**A.keywords,**D};A=A.func
		B=super(partial,E).__new__(E);B.func=A;B.args=C;B.keywords=D;return B
	def __call__(A,*C,**B):B={**A.keywords,**B};return A.func(*A.args,*C,**B)
	@recursive_repr()
	def __repr__(self):
		A=self;C=type(A).__qualname__;B=[repr(A.func)];B.extend(repr(A)for A in A.args);B.extend(f"{A}={B!r}"for(A,B)in A.keywords.items())
		if type(A).__module__=='functools':return f"functools.{C}({_H.join(B)})"
		return f"{C}({_H.join(B)})"
	def __reduce__(A):return type(A),(A.func,),(A.func,A.args,A.keywords or _A,A.__dict__ or _A)
	def __setstate__(C,state):
		D=state
		if not isinstance(D,tuple):raise TypeError('argument to __setstate__ must be a tuple')
		if len(D)!=4:raise TypeError(f"expected 4 items in state, got {len(D)}")
		F,E,A,B=D
		if not callable(F)or not isinstance(E,tuple)or A is not _A and not isinstance(A,dict)or B is not _A and not isinstance(B,dict):raise TypeError('invalid partial state')
		E=tuple(E)
		if A is _A:A={}
		elif type(A)is not dict:A=dict(A)
		if B is _A:B={}
		C.__dict__=B;C.func=F;C.args=E;C.keywords=A
try:from _functools import partial
except ImportError:pass
class partialmethod:
	'Method descriptor with partial application of the given arguments\n    and keywords.\n\n    Supports wrapping existing descriptors and handles non-descriptor\n    callables as instance methods.\n    '
	def __init__(*A,**D):
		if len(A)>=2:C,B,*A=A
		elif not A:raise TypeError("descriptor '__init__' of partialmethod needs an argument")
		elif _G in D:B=D.pop(_G);C,*A=A;import warnings as E;E.warn("Passing 'func' as keyword argument is deprecated",DeprecationWarning,stacklevel=2)
		else:raise TypeError("type 'partialmethod' takes at least one argument, got %d"%(len(A)-1))
		A=tuple(A)
		if not callable(B)and not hasattr(B,_I):raise TypeError('{!r} is not callable or a descriptor'.format(B))
		if isinstance(B,partialmethod):C.func=B.func;C.args=B.args+A;C.keywords={**B.keywords,**D}
		else:C.func=B;C.args=A;C.keywords=D
	__init__.__text_signature__='($self, func, /, *args, **keywords)'
	def __repr__(A):B=_H.join(map(repr,A.args));C=_H.join('{}={!r}'.format(A,B)for(A,B)in A.keywords.items());D='{module}.{cls}({func}, {args}, {keywords})';return D.format(module=A.__class__.__module__,cls=A.__class__.__qualname__,func=A.func,args=B,keywords=C)
	def _make_unbound_method(A):
		def B(C,*D,**B):B={**A.keywords,**B};return A.func(C,*A.args,*D,**B)
		B.__isabstractmethod__=A.__isabstractmethod__;B._partialmethod=A;return B
	def __get__(A,obj,cls=_A):
		D=getattr(A.func,_I,_A);B=_A
		if D is not _A:
			C=D(obj,cls)
			if C is not A.func:
				B=partial(C,*A.args,**A.keywords)
				try:B.__self__=C.__self__
				except AttributeError:pass
		if B is _A:B=A._make_unbound_method().__get__(obj,cls)
		return B
	@property
	def __isabstractmethod__(self):return getattr(self.func,_M,_B)
	__class_getitem__=classmethod(GenericAlias)
def _unwrap_partial(func):
	A=func
	while isinstance(A,partial):A=A.func
	return A
_CacheInfo=namedtuple('CacheInfo',['hits','misses','maxsize','currsize'])
class _HashedSeq(list):
	' This class guarantees that hash() will be called no more than once\n        per element.  This is important because the lru_cache() will hash\n        the key multiple times on a cache miss.\n\n    ';__slots__='hashvalue'
	def __init__(A,tup,hash=hash):A[:]=tup;A.hashvalue=hash(tup)
	def __hash__(A):return A.hashvalue
def _make_key(args,kwds,typed,kwd_mark=(object(),),fasttypes={int,str},tuple=tuple,type=type,len=len):
	'Make a cache key from optionally typed positional and keyword arguments\n\n    The key is constructed in a way that is flat as possible rather than\n    as a nested structure that would take more memory.\n\n    If there is only a single argument and its data type is known to cache\n    its hash value, then that argument is returned without a wrapper.  This\n    saves space and improves lookup speed.\n\n    ';B=kwds;A=args
	if B:
		A+=kwd_mark
		for C in B.items():A+=C
	if typed:
		A+=tuple(type(A)for A in args)
		if B:A+=tuple(type(A)for A in B.values())
	elif len(A)==1 and type(A[0])in fasttypes:return A[0]
	return _HashedSeq(A)
def lru_cache(maxsize=128,typed=_B):
	'Least-recently-used cache decorator.\n\n    If *maxsize* is set to None, the LRU features are disabled and the cache\n    can grow without bound.\n\n    If *typed* is True, arguments of different types will be cached separately.\n    For example, f(3.0) and f(3) will be treated as distinct calls with\n    distinct results.\n\n    Arguments to the cached function must be hashable.\n\n    View the cache statistics named tuple (hits, misses, maxsize, currsize)\n    with f.cache_info().  Clear the cache and statistics with f.cache_clear().\n    Access the underlying function with f.__wrapped__.\n\n    See:  http://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)\n\n    ';B=typed;A=maxsize
	if isinstance(A,int):
		if A<0:A=0
	elif callable(A)and isinstance(B,bool):C,A=A,128;D=_lru_cache_wrapper(C,A,B,_CacheInfo);return update_wrapper(D,C)
	elif A is not _A:raise TypeError('Expected first argument to be an integer, a callable, or None')
	def E(user_function):C=user_function;D=_lru_cache_wrapper(C,A,B,_CacheInfo);return update_wrapper(D,C)
	return E
def _lru_cache_wrapper(user_function,maxsize,typed,_CacheInfo):
	R=typed;O=user_function;L=maxsize;G=object();S=_make_key;F,H,P,Q=0,1,2,3;C={};D=B=0;I=_B;T=C.get;U=C.__len__;M=RLock();A=[];A[:]=[A,A,_A,_A]
	if L==0:
		def E(*A,**C):nonlocal B;B+=1;D=O(*A,**C);return D
	elif L is _A:
		def E(*E,**F):
			nonlocal D,B;H=S(E,F,R);A=T(H,G)
			if A is not G:D+=1;return A
			B+=1;A=O(*E,**F);C[H]=A;return A
	else:
		def E(*V,**W):
			nonlocal A,D,B,I;G=S(V,W,R)
			with M:
				E=T(G)
				if E is not _A:X,Y,a,J=E;X[H]=Y;Y[F]=X;K=A[F];K[H]=A[F]=E;E[F]=K;E[H]=A;D+=1;return J
				B+=1
			J=O(*V,**W)
			with M:
				if G in C:0
				elif I:N=A;N[P]=G;N[Q]=J;A=N[H];Z=A[P];b=A[Q];A[P]=A[Q]=_A;del C[Z];C[G]=N
				else:K=A[F];E=[K,A,G,J];K[H]=A[F]=C[G]=E;I=U()>=L
			return J
	def J():
		'Report cache statistics'
		with M:return _CacheInfo(D,B,L,U())
	def K():
		'Clear the cache and cache statistics';nonlocal D,B,I
		with M:C.clear();A[:]=[A,A,_A,_A];D=B=0;I=_B
	E.cache_info=J;E.cache_clear=K;return E
try:from _functools import _lru_cache_wrapper
except ImportError:pass
def _c3_merge(sequences):
	'Merges MROs in *sequences* to a single MRO using the C3 algorithm.\n\n    Adapted from http://www.python.org/download/releases/2.3/mro/.\n\n    ';A=sequences;C=[]
	while True:
		A=[A for A in A if A]
		if not A:return C
		for E in A:
			B=E[0]
			for F in A:
				if B in F[1:]:B=_A;break
			else:break
		if B is _A:raise RuntimeError('Inconsistent hierarchy')
		C.append(B)
		for D in A:
			if D[0]==B:del D[0]
def _c3_mro(cls,abcs=_A):
	"Computes the method resolution order using extended C3 linearization.\n\n    If no *abcs* are given, the algorithm works exactly like the built-in C3\n    linearization used for method resolution.\n\n    If given, *abcs* is a list of abstract base classes that should be inserted\n    into the resulting MRO. Unrelated ABCs are ignored and don't end up in the\n    result. The algorithm inserts ABCs where their functionality is introduced,\n    i.e. issubclass(cls, abc) returns True for the class itself but returns\n    False for all its direct base classes. Implicit ABCs for a given class\n    (either registered or inferred from the presence of a special method like\n    __len__) are inserted directly after the last ABC explicitly listed in the\n    MRO of said class. If two implicit ABCs end up next to each other in the\n    resulting MRO, their ordering depends on the order of types in *abcs*.\n\n    ";B=cls;A=abcs
	for(H,C)in enumerate(reversed(B.__bases__)):
		if hasattr(C,_N):E=len(B.__bases__)-H;break
	else:E=0
	A=list(A)if A else[];F=list(B.__bases__[:E]);D=[];G=list(B.__bases__[E:])
	for C in A:
		if issubclass(B,C)and not any(issubclass(A,C)for A in B.__bases__):D.append(C)
	for C in D:A.remove(C)
	I=[_c3_mro(B,abcs=A)for B in F];J=[_c3_mro(B,abcs=A)for B in D];K=[_c3_mro(B,abcs=A)for B in G];return _c3_merge([[B]]+I+J+K+[F]+[D]+[G])
def _compose_mro(cls,types):
	'Calculates the method resolution order for a given class *cls*.\n\n    Includes relevant abstract base classes (with their respective bases) from\n    the *types* iterable. Uses a modified C3 linearization algorithm.\n\n    ';C=cls;A=types;F=set(C.__mro__)
	def I(typ):A=typ;return A not in F and hasattr(A,'__mro__')and issubclass(C,A)
	A=[A for A in A if I(A)]
	def J(typ):
		for B in A:
			if typ!=B and typ in B.__mro__:return True
		return _B
	A=[A for A in A if not J(A)];K=set(A);D=[]
	for G in A:
		E=[]
		for B in G.__subclasses__():
			if B not in F and issubclass(C,B):E.append([A for A in B.__mro__ if A in K])
		if not E:D.append(G);continue
		E.sort(key=len,reverse=True)
		for B in E:
			for H in B:
				if H not in D:D.append(H)
	return _c3_mro(C,abcs=D)
def _find_impl(cls,registry):
	'Returns the best matching implementation from *registry* for type *cls*.\n\n    Where there is no registered implementation for a specific type, its method\n    resolution order is used to find a more generic implementation.\n\n    Note: if *registry* does not contain an implementation for the base\n    *object* type, this function may return None.\n\n    ';D=cls;C=registry;E=_compose_mro(D,C.keys());A=_A
	for B in E:
		if A is not _A:
			if B in C and B not in D.__mro__ and A not in D.__mro__ and not issubclass(A,B):raise RuntimeError('Ambiguous dispatch: {} or {}'.format(A,B))
			break
		if B in C:A=B
	return C.get(A)
def singledispatch(func):
	'Single-dispatch generic function decorator.\n\n    Transforms a function into a generic function, which can have different\n    behaviours depending upon the type of its first argument. The decorated\n    function acts as the default implementation, and additional\n    implementations can be registered using the register() attribute of the\n    generic function.\n    ';E=func;import types,weakref as H;C={};D=H.WeakKeyDictionary();B=_A
	def F(cls):
		'generic_func.dispatch(cls) -> <function implementation>\n\n        Runs the dispatch algorithm to return the best available implementation\n        for the given *cls* registered on *generic_func*.\n\n        ';A=cls;nonlocal B
		if B is not _A:
			F=get_cache_token()
			if B!=F:D.clear();B=F
		try:E=D[A]
		except KeyError:
			try:E=C[A]
			except KeyError:E=_find_impl(A,C)
			D[A]=E
		return E
	def G(cls,func=_A):
		'generic_func.register(cls, func) -> func\n\n        Registers a new implementation for the given *cls* on a *generic_func*.\n\n        ';E=func;A=cls;nonlocal B
		if E is _A:
			if isinstance(A,type):return lambda f:G(A,f)
			F=getattr(A,_K,{})
			if not F:raise TypeError(f"Invalid first argument to `register()`: {A!r}. Use either `@register(some_class)` or plain `@register` on an annotated function.")
			E=A;from typing import get_type_hints as H;I,A=next(iter(H(E).items()))
			if not isinstance(A,type):raise TypeError(f"Invalid annotation for {I!r}. {A!r} is not a class.")
		C[A]=E
		if B is _A and hasattr(A,_N):B=get_cache_token()
		D.clear();return E
	def A(*A,**B):
		if not A:raise TypeError(f"{I} requires at least 1 positional argument")
		return F(A[0].__class__)(*A,**B)
	I=getattr(E,_J,'singledispatch function');C[object]=E;A.register=G;A.dispatch=F;A.registry=types.MappingProxyType(C);A._clear_cache=D.clear;update_wrapper(A,E);return A
class singledispatchmethod:
	'Single-dispatch generic method descriptor.\n\n    Supports wrapping existing descriptors and handles non-descriptor\n    callables as instance methods.\n    '
	def __init__(B,func):
		A=func
		if not callable(A)and not hasattr(A,_I):raise TypeError(f"{A!r} is not callable or a descriptor")
		B.dispatcher=singledispatch(A);B.func=A
	def register(A,cls,method=_A):'generic_method.register(cls, func) -> func\n\n        Registers a new implementation for the given *cls* on a *generic_method*.\n        ';return A.dispatcher.register(cls,func=method)
	def __get__(A,obj,cls=_A):
		def B(*B,**C):D=A.dispatcher.dispatch(B[0].__class__);return D.__get__(obj,cls)(*B,**C)
		B.__isabstractmethod__=A.__isabstractmethod__;B.register=A.register;update_wrapper(B,A.func);return B
	@property
	def __isabstractmethod__(self):return getattr(self.func,_M,_B)
_NOT_FOUND=object()
class cached_property:
	def __init__(A,func):A.func=func;A.attrname=_A;A.__doc__=func.__doc__;A.lock=RLock()
	def __set_name__(A,owner,name):
		B=name
		if A.attrname is _A:A.attrname=B
		elif B!=A.attrname:raise TypeError(f"Cannot assign the same cached_property to two different names ({A.attrname!r} and {B!r}).")
	def __get__(A,instance,owner=_A):
		C=instance
		if C is _A:return A
		if A.attrname is _A:raise TypeError('Cannot use cached_property instance without calling __set_name__ on it.')
		try:D=C.__dict__
		except AttributeError:E=f"No '__dict__' attribute on {type(C).__name__!r} instance to cache {A.attrname!r} property.";raise TypeError(E)from _A
		B=D.get(A.attrname,_NOT_FOUND)
		if B is _NOT_FOUND:
			with A.lock:
				B=D.get(A.attrname,_NOT_FOUND)
				if B is _NOT_FOUND:
					B=A.func(C)
					try:D[A.attrname]=B
					except TypeError:E=f"The '__dict__' attribute on {type(C).__name__!r} instance does not support item assignment for caching {A.attrname!r} property.";raise TypeError(E)from _A
		return B
	__class_getitem__=classmethod(GenericAlias)