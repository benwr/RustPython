_A=None
from reprlib import recursive_repr as _recursive_repr
class defaultdict(dict):
	def __init__(C,*A,**D):
		if len(A)>=1:
			B=A[0]
			if B is not _A and not callable(B):raise TypeError('first argument must be callable or None')
			A=A[1:]
		else:B=_A
		super().__init__(*A,**D);C.default_factory=B
	def __missing__(A,key):
		if A.default_factory is not _A:B=A.default_factory()
		else:raise KeyError(key)
		A[key]=B;return B
	@_recursive_repr()
	def __repr_factory(factory):return repr(factory)
	def __repr__(A):return f"{type(A).__name__}({defaultdict.__repr_factory(A.default_factory)}, {dict.__repr__(A)})"
	def copy(A):return type(A)(A.default_factory,A)
	__copy__=copy
	def __reduce__(A):
		if A.default_factory is not _A:B=A.default_factory,
		else:B=()
		return type(A),B,_A,_A,iter(A.items())
	def __or__(A,other):
		B=other
		if not isinstance(B,dict):return NotImplemented
		C=defaultdict(A.default_factory,A);C.update(B);return C
	def __ror__(A,other):
		B=other
		if not isinstance(B,dict):return NotImplemented
		C=defaultdict(A.default_factory,B);C.update(A);return C
defaultdict.__module__='collections'