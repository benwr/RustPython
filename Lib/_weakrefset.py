_A=None
from _weakref import ref
from types import GenericAlias
__all__=['WeakSet']
class _IterationGuard:
	def __init__(A,weakcontainer):A.weakcontainer=ref(weakcontainer)
	def __enter__(A):
		B=A.weakcontainer()
		if B is not _A:B._iterating.add(A)
		return A
	def __exit__(B,e,t,b):
		A=B.weakcontainer()
		if A is not _A:
			C=A._iterating;C.remove(B)
			if not C:A._commit_removals()
class WeakSet:
	def __init__(A,data=_A):
		A.data=set()
		def B(item,selfref=ref(A)):
			A=selfref()
			if A is not _A:
				if A._iterating:A._pending_removals.append(item)
				else:A.data.discard(item)
		A._remove=B;A._pending_removals=[];A._iterating=set()
		if data is not _A:A.update(data)
	def _commit_removals(A):
		B=A._pending_removals.pop;C=A.data.discard
		while True:
			try:D=B()
			except IndexError:return
			C(D)
	def __iter__(A):
		with _IterationGuard(A):
			for C in A.data:
				B=C()
				if B is not _A:yield B
	def __len__(A):return len(A.data)-len(A._pending_removals)
	def __contains__(A,item):
		try:B=ref(item)
		except TypeError:return False
		return B in A.data
	def __reduce__(A):return A.__class__,(list(A),),getattr(A,'__dict__',_A)
	def add(A,item):
		if A._pending_removals:A._commit_removals()
		A.data.add(ref(item,A._remove))
	def clear(A):
		if A._pending_removals:A._commit_removals()
		A.data.clear()
	def copy(A):return A.__class__(A)
	def pop(A):
		if A._pending_removals:A._commit_removals()
		while True:
			try:C=A.data.pop()
			except KeyError:raise KeyError('pop from empty WeakSet')from _A
			B=C()
			if B is not _A:return B
	def remove(A,item):
		if A._pending_removals:A._commit_removals()
		A.data.remove(ref(item))
	def discard(A,item):
		if A._pending_removals:A._commit_removals()
		A.data.discard(ref(item))
	def update(A,other):
		if A._pending_removals:A._commit_removals()
		for B in other:A.add(B)
	def __ior__(A,other):A.update(other);return A
	def difference(B,other):A=B.copy();A.difference_update(other);return A
	__sub__=difference
	def difference_update(A,other):A.__isub__(other)
	def __isub__(A,other):
		B=other
		if A._pending_removals:A._commit_removals()
		if A is B:A.data.clear()
		else:A.data.difference_update(ref(A)for A in B)
		return A
	def intersection(A,other):return A.__class__(B for B in other if B in A)
	__and__=intersection
	def intersection_update(A,other):A.__iand__(other)
	def __iand__(A,other):
		if A._pending_removals:A._commit_removals()
		A.data.intersection_update(ref(A)for A in other);return A
	def issubset(A,other):return A.data.issubset(ref(A)for A in other)
	__le__=issubset
	def __lt__(A,other):return A.data<set(map(ref,other))
	def issuperset(A,other):return A.data.issuperset(ref(A)for A in other)
	__ge__=issuperset
	def __gt__(A,other):return A.data>set(map(ref,other))
	def __eq__(A,other):
		B=other
		if not isinstance(B,A.__class__):return NotImplemented
		return A.data==set(map(ref,B))
	def symmetric_difference(B,other):A=B.copy();A.symmetric_difference_update(other);return A
	__xor__=symmetric_difference
	def symmetric_difference_update(A,other):A.__ixor__(other)
	def __ixor__(A,other):
		B=other
		if A._pending_removals:A._commit_removals()
		if A is B:A.data.clear()
		else:A.data.symmetric_difference_update(ref(B,A._remove)for B in B)
		return A
	def union(A,other):return A.__class__(B for A in(A,other)for B in A)
	__or__=union
	def isdisjoint(A,other):return len(A.intersection(other))==0
	def __repr__(A):return repr(A.data)
	__class_getitem__=classmethod(GenericAlias)