_B=True
_A=False
from _weakrefset import WeakSet
def get_cache_token():'Returns the current ABC cache token.\n\n    The token is an opaque object (supporting equality testing) identifying the\n    current version of the ABC cache for virtual subclasses. The token changes\n    with every call to ``register()`` on any ABC.\n    ';return ABCMeta._abc_invalidation_counter
class ABCMeta(type):
	"Metaclass for defining Abstract Base Classes (ABCs).\n\n    Use this metaclass to create an ABC.  An ABC can be subclassed\n    directly, and then acts as a mix-in class.  You can also register\n    unrelated concrete classes (even built-in classes) and unrelated\n    ABCs as 'virtual subclasses' -- these and their descendants will\n    be considered subclasses of the registering ABC by the built-in\n    issubclass() function, but the registering ABC won't show up in\n    their MRO (Method Resolution Order) nor will method\n    implementations defined by the registering ABC be callable (not\n    even via super()).\n    ";_abc_invalidation_counter=0
	def __new__(G,B,C,D,**H):
		E='__isabstractmethod__';A=super().__new__(G,B,C,D,**H);F={A for(A,B)in D.items()if getattr(B,E,_A)}
		for I in C:
			for B in getattr(I,'__abstractmethods__',set()):
				J=getattr(A,B,None)
				if getattr(J,E,_A):F.add(B)
		A.__abstractmethods__=frozenset(F);A._abc_registry=WeakSet();A._abc_cache=WeakSet();A._abc_negative_cache=WeakSet();A._abc_negative_cache_version=ABCMeta._abc_invalidation_counter;return A
	def register(B,subclass):
		'Register a virtual subclass of an ABC.\n\n        Returns the subclass, to allow usage as a class decorator.\n        ';A=subclass
		if not isinstance(A,type):raise TypeError('Can only register classes')
		if issubclass(A,B):return A
		if issubclass(B,A):raise RuntimeError('Refusing to create an inheritance cycle')
		B._abc_registry.add(A);ABCMeta._abc_invalidation_counter+=1;return A
	def _dump_registry(A,file=None):
		'Debug helper to print the ABC registry.';C=file;print(f"Class: {A.__module__}.{A.__qualname__}",file=C);print(f"Inv. counter: {get_cache_token()}",file=C)
		for D in A.__dict__:
			if D.startswith('_abc_'):
				B=getattr(A,D)
				if isinstance(B,WeakSet):B=set(B)
				print(f"{D}: {B!r}",file=C)
	def _abc_registry_clear(A):'Clear the registry (for debugging or testing).';A._abc_registry.clear()
	def _abc_caches_clear(A):'Clear the caches (for debugging or testing).';A._abc_cache.clear();A._abc_negative_cache.clear()
	def __instancecheck__(A,instance):
		'Override for isinstance(instance, cls).';C=instance;B=C.__class__
		if B in A._abc_cache:return _B
		D=type(C)
		if D is B:
			if A._abc_negative_cache_version==ABCMeta._abc_invalidation_counter and B in A._abc_negative_cache:return _A
			return A.__subclasscheck__(B)
		return any(A.__subclasscheck__(B)for B in(B,D))
	def __subclasscheck__(A,subclass):
		'Override for issubclass(subclass, cls).';B=subclass
		if not isinstance(B,type):raise TypeError('issubclass() arg 1 must be a class')
		if B in A._abc_cache:return _B
		if A._abc_negative_cache_version<ABCMeta._abc_invalidation_counter:A._abc_negative_cache=WeakSet();A._abc_negative_cache_version=ABCMeta._abc_invalidation_counter
		elif B in A._abc_negative_cache:return _A
		C=A.__subclasshook__(B)
		if C is not NotImplemented:
			assert isinstance(C,bool)
			if C:A._abc_cache.add(B)
			else:A._abc_negative_cache.add(B)
			return C
		if A in getattr(B,'__mro__',()):A._abc_cache.add(B);return _B
		for D in A._abc_registry:
			if issubclass(B,D):A._abc_cache.add(B);return _B
		for E in A.__subclasses__():
			if issubclass(B,E):A._abc_cache.add(B);return _B
		A._abc_negative_cache.add(B);return _A