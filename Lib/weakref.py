'Weak reference support for Python.\n\nThis module is an implementation of PEP 205:\n\nhttps://www.python.org/dev/peps/pep-0205/\n'
_D='<%s at %#x>'
_C=False
_B=True
_A=None
from _weakref import getweakrefcount,getweakrefs,ref,proxy,CallableProxyType,ProxyType,ReferenceType,_remove_dead_weakref
from _weakrefset import WeakSet,_IterationGuard
import _collections_abc,sys,itertools
ProxyTypes=ProxyType,CallableProxyType
__all__=['ref','proxy','getweakrefcount','getweakrefs','WeakKeyDictionary','ReferenceType','ProxyType','CallableProxyType','ProxyTypes','WeakValueDictionary','WeakSet','WeakMethod','finalize']
_collections_abc.Set.register(WeakSet)
_collections_abc.MutableSet.register(WeakSet)
class WeakMethod(ref):
	'\n    A custom `weakref.ref` subclass which simulates a weak reference to\n    a bound method, working around the lifetime problem of bound methods.\n    ';__slots__='_func_ref','_meth_type','_alive','__weakref__'
	def __new__(E,meth,callback=_A):
		C=callback;B=meth
		try:F=B.__self__;G=B.__func__
		except AttributeError:raise TypeError('argument should be a bound method, not {}'.format(type(B)))from _A
		def D(arg):
			A=H()
			if A._alive:
				A._alive=_C
				if C is not _A:C(A)
		A=ref.__new__(E,F,D);A._func_ref=ref(G,D);A._meth_type=type(B);A._alive=_B;H=ref(A);return A
	def __call__(A):
		B=super().__call__();C=A._func_ref()
		if B is _A or C is _A:return
		return A._meth_type(C,B)
	def __eq__(B,other):
		A=other
		if isinstance(A,WeakMethod):
			if not B._alive or not A._alive:return B is A
			return ref.__eq__(B,A)and B._func_ref==A._func_ref
		return NotImplemented
	def __ne__(B,other):
		A=other
		if isinstance(A,WeakMethod):
			if not B._alive or not A._alive:return B is not A
			return ref.__ne__(B,A)or B._func_ref!=A._func_ref
		return NotImplemented
	__hash__=ref.__hash__
class WeakValueDictionary(_collections_abc.MutableMapping):
	'Mapping class that references values weakly.\n\n    Entries in the dictionary will be discarded when no strong\n    reference to the value exists anymore\n    '
	def __init__(A,B=(),**C):
		def D(wr,selfref=ref(A),_atomic_removal=_remove_dead_weakref):
			A=selfref()
			if A is not _A:
				if A._iterating:A._pending_removals.append(wr.key)
				else:_atomic_removal(A.data,wr.key)
		A._remove=D;A._pending_removals=[];A._iterating=set();A.data={};A.update(B,**C)
	def _commit_removals(A,_atomic_removal=_remove_dead_weakref):
		B=A._pending_removals.pop;C=A.data
		while _B:
			try:D=B()
			except IndexError:return
			_atomic_removal(C,D)
	def __getitem__(A,key):
		if A._pending_removals:A._commit_removals()
		B=A.data[key]()
		if B is _A:raise KeyError(key)
		else:return B
	def __delitem__(A,key):
		if A._pending_removals:A._commit_removals()
		del A.data[key]
	def __len__(A):
		if A._pending_removals:A._commit_removals()
		return len(A.data)
	def __contains__(A,key):
		if A._pending_removals:A._commit_removals()
		try:B=A.data[key]()
		except KeyError:return _C
		return B is not _A
	def __repr__(A):return _D%(A.__class__.__name__,id(A))
	def __setitem__(A,key,value):
		if A._pending_removals:A._commit_removals()
		A.data[key]=KeyedRef(value,A._remove,key)
	def copy(A):
		if A._pending_removals:A._commit_removals()
		B=WeakValueDictionary()
		with _IterationGuard(A):
			for(D,E)in A.data.items():
				C=E()
				if C is not _A:B[D]=C
		return B
	__copy__=copy
	def __deepcopy__(A,memo):
		from copy import deepcopy as D
		if A._pending_removals:A._commit_removals()
		B=A.__class__()
		with _IterationGuard(A):
			for(E,F)in A.data.items():
				C=F()
				if C is not _A:B[D(E,memo)]=C
		return B
	def get(A,key,default=_A):
		B=default
		if A._pending_removals:A._commit_removals()
		try:D=A.data[key]
		except KeyError:return B
		else:
			C=D()
			if C is _A:return B
			else:return C
	def items(A):
		if A._pending_removals:A._commit_removals()
		with _IterationGuard(A):
			for(C,D)in A.data.items():
				B=D()
				if B is not _A:yield(C,B)
	def keys(A):
		if A._pending_removals:A._commit_removals()
		with _IterationGuard(A):
			for(B,C)in A.data.items():
				if C()is not _A:yield B
	__iter__=keys
	def itervaluerefs(A):
		"Return an iterator that yields the weak references to the values.\n\n        The references are not guaranteed to be 'live' at the time\n        they are used, so the result of calling the references needs\n        to be checked before being used.  This can be used to avoid\n        creating references that will cause the garbage collector to\n        keep the values around longer than needed.\n\n        "
		if A._pending_removals:A._commit_removals()
		with _IterationGuard(A):yield from A.data.values()
	def values(A):
		if A._pending_removals:A._commit_removals()
		with _IterationGuard(A):
			for C in A.data.values():
				B=C()
				if B is not _A:yield B
	def popitem(A):
		if A._pending_removals:A._commit_removals()
		while _B:
			C,D=A.data.popitem();B=D()
			if B is not _A:return C,B
	def pop(A,key,*C):
		if A._pending_removals:A._commit_removals()
		try:B=A.data.pop(key)()
		except KeyError:B=_A
		if B is _A:
			if C:return C[0]
			else:raise KeyError(key)
		else:return B
	def setdefault(A,key,default=_A):
		D=default;B=key
		try:C=A.data[B]()
		except KeyError:C=_A
		if C is _A:
			if A._pending_removals:A._commit_removals()
			A.data[B]=KeyedRef(D,A._remove,B);return D
		else:return C
	def update(A,B=_A,**F):
		if A._pending_removals:A._commit_removals()
		E=A.data
		if B is not _A:
			if not hasattr(B,'items'):B=dict(B)
			for(C,D)in B.items():E[C]=KeyedRef(D,A._remove,C)
		for(C,D)in F.items():E[C]=KeyedRef(D,A._remove,C)
	def valuerefs(A):
		"Return a list of weak references to the values.\n\n        The references are not guaranteed to be 'live' at the time\n        they are used, so the result of calling the references needs\n        to be checked before being used.  This can be used to avoid\n        creating references that will cause the garbage collector to\n        keep the values around longer than needed.\n\n        "
		if A._pending_removals:A._commit_removals()
		return list(A.data.values())
	def __ior__(A,other):A.update(other);return A
	def __or__(C,other):
		A=other
		if isinstance(A,_collections_abc.Mapping):B=C.copy();B.update(A);return B
		return NotImplemented
	def __ror__(B,other):
		C=other
		if isinstance(C,_collections_abc.Mapping):A=B.__class__();A.update(C);A.update(B);return A
		return NotImplemented
class KeyedRef(ref):
	"Specialized reference that includes a key corresponding to the value.\n\n    This is used in the WeakValueDictionary to avoid having to create\n    a function object for each key stored in the mapping.  A shared\n    callback object can use the 'key' attribute of a KeyedRef instead\n    of getting a reference to the key from an enclosing scope.\n\n    ";__slots__='key',
	def __new__(type,ob,callback,key):A=ref.__new__(type,ob,callback);A.key=key;return A
	def __init__(A,ob,callback,key):super().__init__(ob,callback)
class WeakKeyDictionary(_collections_abc.MutableMapping):
	' Mapping class that references keys weakly.\n\n    Entries in the dictionary will be discarded when there is no\n    longer a strong reference to the key. This can be used to\n    associate additional data with an object owned by other parts of\n    an application without adding attributes to those objects. This\n    can be especially useful with objects that override attribute\n    accesses.\n    '
	def __init__(A,dict=_A):
		A.data={}
		def B(k,selfref=ref(A)):
			A=selfref()
			if A is not _A:
				if A._iterating:A._pending_removals.append(k)
				else:
					try:del A.data[k]
					except KeyError:pass
		A._remove=B;A._pending_removals=[];A._iterating=set();A._dirty_len=_C
		if dict is not _A:A.update(dict)
	def _commit_removals(A):
		B=A._pending_removals.pop;C=A.data
		while _B:
			try:D=B()
			except IndexError:return
			try:del C[D]
			except KeyError:pass
	def _scrub_removals(A):B=A.data;A._pending_removals=[A for A in A._pending_removals if A in B];A._dirty_len=_C
	def __delitem__(A,key):A._dirty_len=_B;del A.data[ref(key)]
	def __getitem__(A,key):return A.data[ref(key)]
	def __len__(A):
		if A._dirty_len and A._pending_removals:A._scrub_removals()
		return len(A.data)-len(A._pending_removals)
	def __repr__(A):return _D%(A.__class__.__name__,id(A))
	def __setitem__(A,key,value):A.data[ref(key,A._remove)]=value
	def copy(A):
		B=WeakKeyDictionary()
		with _IterationGuard(A):
			for(D,E)in A.data.items():
				C=D()
				if C is not _A:B[C]=E
		return B
	__copy__=copy
	def __deepcopy__(A,memo):
		from copy import deepcopy as D;B=A.__class__()
		with _IterationGuard(A):
			for(E,F)in A.data.items():
				C=E()
				if C is not _A:B[C]=D(F,memo)
		return B
	def get(A,key,default=_A):return A.data.get(ref(key),default)
	def __contains__(A,key):
		try:B=ref(key)
		except TypeError:return _C
		return B in A.data
	def items(A):
		with _IterationGuard(A):
			for(C,D)in A.data.items():
				B=C()
				if B is not _A:yield(B,D)
	def keys(A):
		with _IterationGuard(A):
			for C in A.data:
				B=C()
				if B is not _A:yield B
	__iter__=keys
	def values(A):
		with _IterationGuard(A):
			for(B,C)in A.data.items():
				if B()is not _A:yield C
	def keyrefs(A):"Return a list of weak references to the keys.\n\n        The references are not guaranteed to be 'live' at the time\n        they are used, so the result of calling the references needs\n        to be checked before being used.  This can be used to avoid\n        creating references that will cause the garbage collector to\n        keep the keys around longer than needed.\n\n        ";return list(A.data)
	def popitem(A):
		A._dirty_len=_B
		while _B:
			C,D=A.data.popitem();B=C()
			if B is not _A:return B,D
	def pop(A,key,*B):A._dirty_len=_B;return A.data.pop(ref(key),*B)
	def setdefault(A,key,default=_A):return A.data.setdefault(ref(key,A._remove),default)
	def update(A,dict=_A,**B):
		C=A.data
		if dict is not _A:
			if not hasattr(dict,'items'):dict=type({})(dict)
			for(D,E)in dict.items():C[ref(D,A._remove)]=E
		if len(B):A.update(B)
	def __ior__(A,other):A.update(other);return A
	def __or__(C,other):
		A=other
		if isinstance(A,_collections_abc.Mapping):B=C.copy();B.update(A);return B
		return NotImplemented
	def __ror__(B,other):
		C=other
		if isinstance(C,_collections_abc.Mapping):A=B.__class__();A.update(C);A.update(B);return A
		return NotImplemented
class finalize:
	'Class for finalization of weakrefable objects\n\n    finalize(obj, func, *args, **kwargs) returns a callable finalizer\n    object which will be called when obj is garbage collected. The\n    first time the finalizer is called it evaluates func(*arg, **kwargs)\n    and returns the result. After this the finalizer is dead, and\n    calling it just returns None.\n\n    When the program exits any remaining finalizers for which the\n    atexit attribute is true will be run in reverse order of creation.\n    By default atexit is true.\n    ';__slots__=();_registry={};_shutdown=_C;_index_iter=itertools.count();_dirty=_C;_registered_with_atexit=_C
	class _Info:__slots__='weakref','func','args','kwargs','atexit','index'
	def __init__(A,C,D,*E,**F):
		if not A._registered_with_atexit:import atexit as G;G.register(A._exitfunc);finalize._registered_with_atexit=_B
		B=A._Info();B.weakref=ref(C,A);B.func=D;B.args=E;B.kwargs=F or _A;B.atexit=_B;B.index=next(A._index_iter);A._registry[A]=B;finalize._dirty=_B
	def __call__(B,_=_A):
		'If alive then mark as dead and return func(*args, **kwargs);\n        otherwise return None';A=B._registry.pop(B,_A)
		if A and not B._shutdown:return A.func(*A.args,**A.kwargs or{})
	def detach(B):
		'If alive then mark as dead and return (obj, func, args, kwargs);\n        otherwise return None';A=B._registry.get(B);C=A and A.weakref()
		if C is not _A and B._registry.pop(B,_A):return C,A.func,A.args,A.kwargs or{}
	def peek(B):
		'If alive then return (obj, func, args, kwargs);\n        otherwise return None';A=B._registry.get(B);C=A and A.weakref()
		if C is not _A:return C,A.func,A.args,A.kwargs or{}
	@property
	def alive(self):'Whether finalizer is alive';return self in self._registry
	@property
	def atexit(self):'Whether finalizer should be called at exit';A=self._registry.get(self);return bool(A)and A.atexit
	@atexit.setter
	def atexit(self,value):
		A=self._registry.get(self)
		if A:A.atexit=bool(value)
	def __repr__(A):
		C=A._registry.get(A);B=C and C.weakref()
		if B is _A:return'<%s object at %#x; dead>'%(type(A).__name__,id(A))
		else:return'<%s object at %#x; for %r at %#x>'%(type(A).__name__,id(A),type(B).__name__,id(B))
	@classmethod
	def _select_for_exit(B):A=[(B,A)for(B,A)in B._registry.items()if A.atexit];A.sort(key=lambda item:item[1].index);return[A for(A,B)in A]
	@classmethod
	def _exitfunc(B):
		C=_C
		try:
			if B._registry:
				import gc
				if gc.isenabled():C=_B;gc.disable()
				A=_A
				while _B:
					if A is _A or finalize._dirty:A=B._select_for_exit();finalize._dirty=_C
					if not A:break
					D=A.pop()
					try:D()
					except Exception:sys.excepthook(*sys.exc_info())
					assert D not in B._registry
		finally:
			finalize._shutdown=_B
			if C:gc.enable()