'Abstract Base Classes (ABCs) for collections, according to PEP 3119.\n\nUnit tests are in test_collections.\n'
_M='ParamSpec'
_L='typing'
_K='__parameters__'
_J='__contains__'
_I='__len__'
_H='__next__'
_G='__anext__'
_F='__await__'
_E='__aiter__'
_D='__iter__'
_C=False
_B=True
_A=None
from abc import ABCMeta,abstractmethod
import sys
GenericAlias=type(list[int])
EllipsisType=type(...)
def _f():0
FunctionType=type(_f)
del _f
__all__=['Awaitable','Coroutine','AsyncIterable','AsyncIterator','AsyncGenerator','Hashable','Iterable','Iterator','Generator','Reversible','Sized','Container','Callable','Collection','Set','MutableSet','Mapping','MutableMapping','MappingView','KeysView','ItemsView','ValuesView','Sequence','MutableSequence','ByteString']
__name__='collections.abc'
bytes_iterator=type(iter(b''))
bytearray_iterator=type(iter(bytearray()))
dict_keyiterator=type(iter({}.keys()))
dict_valueiterator=type(iter({}.values()))
dict_itemiterator=type(iter({}.items()))
list_iterator=type(iter([]))
list_reverseiterator=type(iter(reversed([])))
range_iterator=type(iter(range(0)))
longrange_iterator=type(iter(range(1<<1000)))
set_iterator=type(iter(set()))
str_iterator=type(iter(''))
tuple_iterator=type(iter(()))
zip_iterator=type(iter(zip()))
dict_keys=type({}.keys())
dict_values=type({}.values())
dict_items=type({}.items())
mappingproxy=type(type.__dict__)
generator=type((lambda:(yield))())
async def _coro():0
_coro=_coro()
coroutine=type(_coro)
_coro.close()
del _coro
async def _ag():yield
_ag=_ag()
async_generator=type(_ag)
del _ag
def _check_methods(C,*D):
	E=C.__mro__
	for A in D:
		for B in E:
			if A in B.__dict__:
				if B.__dict__[A]is _A:return NotImplemented
				break
		else:return NotImplemented
	return _B
class Hashable(metaclass=ABCMeta):
	__slots__=()
	@abstractmethod
	def __hash__(self):return 0
	@classmethod
	def __subclasshook__(A,C):
		if A is Hashable:return _check_methods(C,'__hash__')
		return NotImplemented
class Awaitable(metaclass=ABCMeta):
	__slots__=()
	@abstractmethod
	def __await__(self):yield
	@classmethod
	def __subclasshook__(A,C):
		if A is Awaitable:return _check_methods(C,_F)
		return NotImplemented
	__class_getitem__=classmethod(GenericAlias)
class Coroutine(Awaitable):
	__slots__=()
	@abstractmethod
	def send(self,value):'Send a value into the coroutine.\n        Return next yielded value or raise StopIteration.\n        ';raise StopIteration
	@abstractmethod
	def throw(self,typ,val=_A,tb=_A):
		'Raise an exception in the coroutine.\n        Return next yielded value or raise StopIteration.\n        ';A=val
		if A is _A:
			if tb is _A:raise typ
			A=typ()
		if tb is not _A:A=A.with_traceback(tb)
		raise A
	def close(A):
		'Raise GeneratorExit inside coroutine.\n        '
		try:A.throw(GeneratorExit)
		except(GeneratorExit,StopIteration):pass
		else:raise RuntimeError('coroutine ignored GeneratorExit')
	@classmethod
	def __subclasshook__(A,C):
		if A is Coroutine:return _check_methods(C,_F,'send','throw','close')
		return NotImplemented
Coroutine.register(coroutine)
class AsyncIterable(metaclass=ABCMeta):
	__slots__=()
	@abstractmethod
	def __aiter__(self):return AsyncIterator()
	@classmethod
	def __subclasshook__(A,C):
		if A is AsyncIterable:return _check_methods(C,_E)
		return NotImplemented
	__class_getitem__=classmethod(GenericAlias)
class AsyncIterator(AsyncIterable):
	__slots__=()
	@abstractmethod
	async def __anext__(self):'Return the next item or raise StopAsyncIteration when exhausted.';raise StopAsyncIteration
	def __aiter__(A):return A
	@classmethod
	def __subclasshook__(A,C):
		if A is AsyncIterator:return _check_methods(C,_G,_E)
		return NotImplemented
class AsyncGenerator(AsyncIterator):
	__slots__=()
	async def __anext__(A):'Return the next item from the asynchronous generator.\n        When exhausted, raise StopAsyncIteration.\n        ';return await A.asend(_A)
	@abstractmethod
	async def asend(self,value):'Send a value into the asynchronous generator.\n        Return next yielded value or raise StopAsyncIteration.\n        ';raise StopAsyncIteration
	@abstractmethod
	async def athrow(self,typ,val=_A,tb=_A):
		'Raise an exception in the asynchronous generator.\n        Return next yielded value or raise StopAsyncIteration.\n        ';A=val
		if A is _A:
			if tb is _A:raise typ
			A=typ()
		if tb is not _A:A=A.with_traceback(tb)
		raise A
	async def aclose(A):
		'Raise GeneratorExit inside coroutine.\n        '
		try:await A.athrow(GeneratorExit)
		except(GeneratorExit,StopAsyncIteration):pass
		else:raise RuntimeError('asynchronous generator ignored GeneratorExit')
	@classmethod
	def __subclasshook__(A,C):
		if A is AsyncGenerator:return _check_methods(C,_E,_G,'asend','athrow','aclose')
		return NotImplemented
AsyncGenerator.register(async_generator)
class Iterable(metaclass=ABCMeta):
	__slots__=()
	@abstractmethod
	def __iter__(self):
		while _C:yield _A
	@classmethod
	def __subclasshook__(A,C):
		if A is Iterable:return _check_methods(C,_D)
		return NotImplemented
	__class_getitem__=classmethod(GenericAlias)
class Iterator(Iterable):
	__slots__=()
	@abstractmethod
	def __next__(self):'Return the next item from the iterator. When exhausted, raise StopIteration';raise StopIteration
	def __iter__(A):return A
	@classmethod
	def __subclasshook__(A,C):
		if A is Iterator:return _check_methods(C,_D,_H)
		return NotImplemented
Iterator.register(bytes_iterator)
Iterator.register(bytearray_iterator)
Iterator.register(dict_keyiterator)
Iterator.register(dict_valueiterator)
Iterator.register(dict_itemiterator)
Iterator.register(list_iterator)
Iterator.register(list_reverseiterator)
Iterator.register(range_iterator)
Iterator.register(longrange_iterator)
Iterator.register(set_iterator)
Iterator.register(str_iterator)
Iterator.register(tuple_iterator)
Iterator.register(zip_iterator)
class Reversible(Iterable):
	__slots__=()
	@abstractmethod
	def __reversed__(self):
		while _C:yield _A
	@classmethod
	def __subclasshook__(A,C):
		if A is Reversible:return _check_methods(C,'__reversed__',_D)
		return NotImplemented
class Generator(Iterator):
	__slots__=()
	def __next__(A):'Return the next item from the generator.\n        When exhausted, raise StopIteration.\n        ';return A.send(_A)
	@abstractmethod
	def send(self,value):'Send a value into the generator.\n        Return next yielded value or raise StopIteration.\n        ';raise StopIteration
	@abstractmethod
	def throw(self,typ,val=_A,tb=_A):
		'Raise an exception in the generator.\n        Return next yielded value or raise StopIteration.\n        ';A=val
		if A is _A:
			if tb is _A:raise typ
			A=typ()
		if tb is not _A:A=A.with_traceback(tb)
		raise A
	def close(A):
		'Raise GeneratorExit inside generator.\n        '
		try:A.throw(GeneratorExit)
		except(GeneratorExit,StopIteration):pass
		else:raise RuntimeError('generator ignored GeneratorExit')
	@classmethod
	def __subclasshook__(A,C):
		if A is Generator:return _check_methods(C,_D,_H,'send','throw','close')
		return NotImplemented
Generator.register(generator)
class Sized(metaclass=ABCMeta):
	__slots__=()
	@abstractmethod
	def __len__(self):return 0
	@classmethod
	def __subclasshook__(A,C):
		if A is Sized:return _check_methods(C,_I)
		return NotImplemented
class Container(metaclass=ABCMeta):
	__slots__=()
	@abstractmethod
	def __contains__(self,x):return _C
	@classmethod
	def __subclasshook__(A,C):
		if A is Container:return _check_methods(C,_J)
		return NotImplemented
	__class_getitem__=classmethod(GenericAlias)
class Collection(Sized,Iterable,Container):
	__slots__=()
	@classmethod
	def __subclasshook__(A,C):
		if A is Collection:return _check_methods(C,_I,_D,_J)
		return NotImplemented
class _CallableGenericAlias(GenericAlias):
	' Represent `Callable[argtypes, resulttype]`.\n\n    This sets ``__args__`` to a tuple containing the flattened ``argtypes``\n    followed by ``resulttype``.\n\n    Example: ``Callable[[int, str], float]`` sets ``__args__`` to\n    ``(int, str, float)``.\n    ';__slots__=()
	def __new__(C,origin,args):
		A=args
		if not(isinstance(A,tuple)and len(A)==2):raise TypeError('Callable must be used as Callable[[arg, ...], result].')
		B,D=A
		if isinstance(B,list):A=*B,D
		elif not _is_param_expr(B):raise TypeError(f"Expected a list of types, an ellipsis, ParamSpec, or Concatenate. Got {B}")
		return super().__new__(C,origin,A)
	@property
	def __parameters__(self):
		B=[]
		for A in self.__args__:
			if hasattr(A,_K)and isinstance(A.__parameters__,tuple):B.extend(A.__parameters__)
			elif _is_typevarlike(A):B.append(A)
		return tuple(dict.fromkeys(B))
	def __repr__(A):
		if len(A.__args__)==2 and _is_param_expr(A.__args__[0]):return super().__repr__()
		return f"collections.abc.Callable[[{', '.join([_type_repr(A)for A in A.__args__[:-1]])}], {_type_repr(A.__args__[-1])}]"
	def __reduce__(B):
		A=B.__args__
		if not(len(A)==2 and _is_param_expr(A[0])):A=list(A[:-1]),A[-1]
		return _CallableGenericAlias,(Callable,A)
	def __getitem__(C,item):
		B=item;E=len(C.__parameters__)
		if E==0:raise TypeError(f"{C} is not a generic class")
		if not isinstance(B,tuple):B=B,
		if E==1 and _is_param_expr(C.__parameters__[0])and B and not _is_param_expr(B[0]):B=list(B),
		F=len(B)
		if F!=E:raise TypeError(f"Too {'many'if F>E else'few'} arguments for {C}; actual {F}, expected {E}")
		G=dict(zip(C.__parameters__,B));D=[]
		for A in C.__args__:
			if _is_typevarlike(A):
				if _is_param_expr(A):
					A=G[A]
					if not _is_param_expr(A):raise TypeError(f"Expected a list of types, an ellipsis, ParamSpec, or Concatenate. Got {A}")
				else:A=G[A]
			elif hasattr(A,_K)and isinstance(A.__parameters__,tuple):
				H=A.__parameters__
				if H:I=tuple(G[A]for A in H);A=A[I]
			D.append(A)
		if not isinstance(D[0],list):J=D[-1];K=D[:-1];D=K,J
		return _CallableGenericAlias(Callable,tuple(D))
def _is_typevarlike(arg):A=type(arg);return A.__module__==_L and A.__name__ in{_M,'TypeVar'}
def _is_param_expr(obj):
	'Checks if obj matches either a list of types, ``...``, ``ParamSpec`` or\n    ``_ConcatenateGenericAlias`` from typing.py\n    ';A=obj
	if A is Ellipsis:return _B
	if isinstance(A,list):return _B
	A=type(A);B=_M,'_ConcatenateGenericAlias';return A.__module__==_L and any(A.__name__==B for B in B)
def _type_repr(obj):
	"Return the repr() of an object, special-casing types (internal helper).\n\n    Copied from :mod:`typing` since collections.abc\n    shouldn't depend on that module.\n    ";A=obj
	if isinstance(A,GenericAlias):return repr(A)
	if isinstance(A,type):
		if A.__module__=='builtins':return A.__qualname__
		return f"{A.__module__}.{A.__qualname__}"
	if A is Ellipsis:return'...'
	if isinstance(A,FunctionType):return A.__name__
	return repr(A)
class Callable(metaclass=ABCMeta):
	__slots__=()
	@abstractmethod
	def __call__(self,*A,**B):return _C
	@classmethod
	def __subclasshook__(A,C):
		if A is Callable:return _check_methods(C,'__call__')
		return NotImplemented
	__class_getitem__=classmethod(_CallableGenericAlias)
class Set(Collection):
	'A set is a finite, iterable container.\n\n    This class provides concrete generic implementations of all\n    methods except for __contains__, __iter__ and __len__.\n\n    To override the comparisons (presumably for speed, as the\n    semantics are fixed), redefine __le__ and __ge__,\n    then the other operations will automatically follow suit.\n    ';__slots__=()
	def __le__(B,other):
		A=other
		if not isinstance(A,Set):return NotImplemented
		if len(B)>len(A):return _C
		for C in B:
			if C not in A:return _C
		return _B
	def __lt__(B,other):
		A=other
		if not isinstance(A,Set):return NotImplemented
		return len(B)<len(A)and B.__le__(A)
	def __gt__(B,other):
		A=other
		if not isinstance(A,Set):return NotImplemented
		return len(B)>len(A)and B.__ge__(A)
	def __ge__(B,other):
		A=other
		if not isinstance(A,Set):return NotImplemented
		if len(B)<len(A):return _C
		for C in A:
			if C not in B:return _C
		return _B
	def __eq__(B,other):
		A=other
		if not isinstance(A,Set):return NotImplemented
		return len(B)==len(A)and B.__le__(A)
	@classmethod
	def _from_iterable(A,it):'Construct an instance of the class from any iterable input.\n\n        Must override this method if the class constructor signature\n        does not accept an iterable for an input.\n        ';return A(it)
	def __and__(A,other):
		B=other
		if not isinstance(B,Iterable):return NotImplemented
		return A._from_iterable(B for B in B if B in A)
	__rand__=__and__
	def isdisjoint(A,other):
		'Return True if two sets have a null intersection.'
		for B in other:
			if B in A:return _C
		return _B
	def __or__(A,other):
		B=other
		if not isinstance(B,Iterable):return NotImplemented
		C=(B for A in(A,B)for B in A);return A._from_iterable(C)
	__ror__=__or__
	def __sub__(B,other):
		A=other
		if not isinstance(A,Set):
			if not isinstance(A,Iterable):return NotImplemented
			A=B._from_iterable(A)
		return B._from_iterable(B for B in B if B not in A)
	def __rsub__(B,other):
		A=other
		if not isinstance(A,Set):
			if not isinstance(A,Iterable):return NotImplemented
			A=B._from_iterable(A)
		return B._from_iterable(A for A in A if A not in B)
	def __xor__(B,other):
		A=other
		if not isinstance(A,Set):
			if not isinstance(A,Iterable):return NotImplemented
			A=B._from_iterable(A)
		return B-A|A-B
	__rxor__=__xor__
	def _hash(C):
		"Compute the hash value of a set.\n\n        Note that we don't define __hash__: not all sets are hashable.\n        But if you define a hashable set type, its __hash__ should\n        call this function.\n\n        This must be compatible __eq__.\n\n        All sets ought to compare equal if they contain the same\n        elements, regardless of how they are implemented, and\n        regardless of the order of the elements; so there's not much\n        freedom for __eq__ or __hash__.  We match the algorithm used\n        by the built-in frozenset type.\n        ";D=sys.maxsize;B=2*D+1;F=len(C);A=1927868237*(F+1);A&=B
		for G in C:E=hash(G);A^=(E^E<<16^89869747)*3644798167;A&=B
		A^=A>>11^A>>25;A=A*69069+907133923;A&=B
		if A>D:A-=B+1
		if A==-1:A=590923713
		return A
Set.register(frozenset)
class MutableSet(Set):
	'A mutable set is a finite, iterable container.\n\n    This class provides concrete generic implementations of all\n    methods except for __contains__, __iter__, __len__,\n    add(), and discard().\n\n    To override the comparisons (presumably for speed, as the\n    semantics are fixed), all you have to do is redefine __le__ and\n    then the other operations will automatically follow suit.\n    ';__slots__=()
	@abstractmethod
	def add(self,value):'Add an element.';raise NotImplementedError
	@abstractmethod
	def discard(self,value):'Remove an element.  Do not raise an exception if absent.';raise NotImplementedError
	def remove(B,value):
		'Remove an element. If not a member, raise a KeyError.';A=value
		if A not in B:raise KeyError(A)
		B.discard(A)
	def pop(A):
		'Return the popped value.  Raise KeyError if empty.';C=iter(A)
		try:B=next(C)
		except StopIteration:raise KeyError from _A
		A.discard(B);return B
	def clear(A):
		'This is slow (creates N new iterators!) but effective.'
		try:
			while _B:A.pop()
		except KeyError:pass
	def __ior__(A,it):
		for B in it:A.add(B)
		return A
	def __iand__(A,it):
		for B in A-it:A.discard(B)
		return A
	def __ixor__(A,it):
		B=it
		if B is A:A.clear()
		else:
			if not isinstance(B,Set):B=A._from_iterable(B)
			for C in B:
				if C in A:A.discard(C)
				else:A.add(C)
		return A
	def __isub__(A,it):
		if it is A:A.clear()
		else:
			for B in it:A.discard(B)
		return A
MutableSet.register(set)
class Mapping(Collection):
	'A Mapping is a generic container for associating key/value\n    pairs.\n\n    This class provides concrete generic implementations of all\n    methods except for __getitem__, __iter__, and __len__.\n    ';__slots__=();__abc_tpflags__=1<<6
	@abstractmethod
	def __getitem__(self,key):raise KeyError
	def get(A,key,default=_A):
		'D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.'
		try:return A[key]
		except KeyError:return default
	def __contains__(A,key):
		try:A[key]
		except KeyError:return _C
		else:return _B
	def keys(A):"D.keys() -> a set-like object providing a view on D's keys";return KeysView(A)
	def items(A):"D.items() -> a set-like object providing a view on D's items";return ItemsView(A)
	def values(A):"D.values() -> an object providing a view on D's values";return ValuesView(A)
	def __eq__(B,other):
		A=other
		if not isinstance(A,Mapping):return NotImplemented
		return dict(B.items())==dict(A.items())
	__reversed__=_A
Mapping.register(mappingproxy)
class MappingView(Sized):
	__slots__='_mapping',
	def __init__(A,mapping):A._mapping=mapping
	def __len__(A):return len(A._mapping)
	def __repr__(A):return'{0.__class__.__name__}({0._mapping!r})'.format(A)
	__class_getitem__=classmethod(GenericAlias)
class KeysView(MappingView,Set):
	__slots__=()
	@classmethod
	def _from_iterable(A,it):return set(it)
	def __contains__(A,key):return key in A._mapping
	def __iter__(A):yield from A._mapping
KeysView.register(dict_keys)
class ItemsView(MappingView,Set):
	__slots__=()
	@classmethod
	def _from_iterable(A,it):return set(it)
	def __contains__(C,item):
		D,A=item
		try:B=C._mapping[D]
		except KeyError:return _C
		else:return B is A or B==A
	def __iter__(A):
		for B in A._mapping:yield(B,A._mapping[B])
ItemsView.register(dict_items)
class ValuesView(MappingView,Collection):
	__slots__=()
	def __contains__(A,value):
		B=value
		for D in A._mapping:
			C=A._mapping[D]
			if C is B or C==B:return _B
		return _C
	def __iter__(A):
		for B in A._mapping:yield A._mapping[B]
ValuesView.register(dict_values)
class MutableMapping(Mapping):
	'A MutableMapping is a generic container for associating\n    key/value pairs.\n\n    This class provides concrete generic implementations of all\n    methods except for __getitem__, __setitem__, __delitem__,\n    __iter__, and __len__.\n    ';__slots__=()
	@abstractmethod
	def __setitem__(self,key,value):raise KeyError
	@abstractmethod
	def __delitem__(self,key):raise KeyError
	__marker=object()
	def pop(A,key,default=__marker):
		'D.pop(k[,d]) -> v, remove specified key and return the corresponding value.\n          If key is not found, d is returned if given, otherwise KeyError is raised.\n        ';B=default
		try:C=A[key]
		except KeyError:
			if B is A.__marker:raise
			return B
		else:del A[key];return C
	def popitem(A):
		'D.popitem() -> (k, v), remove and return some (key, value) pair\n           as a 2-tuple; but raise KeyError if D is empty.\n        '
		try:B=next(iter(A))
		except StopIteration:raise KeyError from _A
		C=A[B];del A[B];return B,C
	def clear(A):
		'D.clear() -> None.  Remove all items from D.'
		try:
			while _B:A.popitem()
		except KeyError:pass
	def update(C,B=(),**E):
		' D.update([E, ]**F) -> None.  Update D from mapping/iterable E and F.\n            If E present and has a .keys() method, does:     for k in E: D[k] = E[k]\n            If E present and lacks .keys() method, does:     for (k, v) in E: D[k] = v\n            In either case, this is followed by: for k, v in F.items(): D[k] = v\n        '
		if isinstance(B,Mapping):
			for A in B:C[A]=B[A]
		elif hasattr(B,'keys'):
			for A in B.keys():C[A]=B[A]
		else:
			for(A,D)in B:C[A]=D
		for(A,D)in E.items():C[A]=D
	def setdefault(A,key,default=_A):
		'D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D';B=default
		try:return A[key]
		except KeyError:A[key]=B
		return B
MutableMapping.register(dict)
class Sequence(Reversible,Collection):
	'All the operations on a read-only sequence.\n\n    Concrete subclasses must override __new__ or __init__,\n    __getitem__, and __len__.\n    ';__slots__=();__abc_tpflags__=1<<5
	@abstractmethod
	def __getitem__(self,index):raise IndexError
	def __iter__(B):
		A=0
		try:
			while _B:C=B[A];yield C;A+=1
		except IndexError:return
	def __contains__(C,value):
		A=value
		for B in C:
			if B is A or B==A:return _B
		return _C
	def __reversed__(A):
		for B in reversed(range(len(A))):yield A[B]
	def index(D,value,start=0,stop=_A):
		'S.index(value, [start, [stop]]) -> integer -- return first index of value.\n           Raises ValueError if the value is not present.\n\n           Supporting start and stop arguments is optional, but\n           recommended.\n        ';E=value;A=stop;B=start
		if B is not _A and B<0:B=max(len(D)+B,0)
		if A is not _A and A<0:A+=len(D)
		C=B
		while A is _A or C<A:
			try:
				F=D[C]
				if F is E or F==E:return C
			except IndexError:break
			C+=1
		raise ValueError
	def count(B,value):'S.count(value) -> integer -- return number of occurrences of value';A=value;return sum(1 for B in B if B is A or B==A)
Sequence.register(tuple)
Sequence.register(str)
Sequence.register(range)
Sequence.register(memoryview)
class ByteString(Sequence):'This unifies bytes and bytearray.\n\n    XXX Should add all their methods.\n    ';__slots__=()
ByteString.register(bytes)
ByteString.register(bytearray)
class MutableSequence(Sequence):
	'All the operations on a read-write sequence.\n\n    Concrete subclasses must provide __new__ or __init__,\n    __getitem__, __setitem__, __delitem__, __len__, and insert().\n    ';__slots__=()
	@abstractmethod
	def __setitem__(self,index,value):raise IndexError
	@abstractmethod
	def __delitem__(self,index):raise IndexError
	@abstractmethod
	def insert(self,index,value):'S.insert(index, value) -- insert value before index';raise IndexError
	def append(A,value):'S.append(value) -- append value to the end of the sequence';A.insert(len(A),value)
	def clear(A):
		'S.clear() -> None -- remove all items from S'
		try:
			while _B:A.pop()
		except IndexError:pass
	def reverse(A):
		'S.reverse() -- reverse *IN PLACE*';C=len(A)
		for B in range(C//2):A[B],A[C-B-1]=A[C-B-1],A[B]
	def extend(B,values):
		'S.extend(iterable) -- extend sequence by appending elements from the iterable';A=values
		if A is B:A=list(A)
		for C in A:B.append(C)
	def pop(A,index=-1):'S.pop([index]) -> item -- remove and return item at index (default last).\n           Raise IndexError if list is empty or index is out of range.\n        ';B=index;C=A[B];del A[B];return C
	def remove(A,value):'S.remove(value) -- remove first occurrence of value.\n           Raise ValueError if the value is not present.\n        ';del A[A.index(value)]
	def __iadd__(A,values):A.extend(values);return A
MutableSequence.register(list)
MutableSequence.register(bytearray)