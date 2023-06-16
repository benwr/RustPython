'Redo the builtin repr() (representation) but with limits on most sizes.'
_A='...'
__all__=['Repr','repr','recursive_repr']
import builtins
from itertools import islice
from _thread import get_ident
def recursive_repr(fillvalue=_A):
	'Decorator to make a repr function return fillvalue for a recursive call'
	def A(user_function):
		A=user_function;C=set()
		def B(self):
			B=id(self),get_ident()
			if B in C:return fillvalue
			C.add(B)
			try:D=A(self)
			finally:C.discard(B)
			return D
		B.__module__=getattr(A,'__module__');B.__doc__=getattr(A,'__doc__');B.__name__=getattr(A,'__name__');B.__qualname__=getattr(A,'__qualname__');B.__annotations__=getattr(A,'__annotations__',{});return B
	return A
class Repr:
	def __init__(A):A.maxlevel=6;A.maxtuple=6;A.maxlist=6;A.maxarray=5;A.maxdict=4;A.maxset=6;A.maxfrozenset=6;A.maxdeque=6;A.maxstring=30;A.maxlong=40;A.maxother=30
	def repr(A,x):return A.repr1(x,A.maxlevel)
	def repr1(B,x,level):
		C='repr_';D=level;A=type(x).__name__
		if' 'in A:E=A.split();A='_'.join(E)
		if hasattr(B,C+A):return getattr(B,C+A)(x,D)
		else:return B.repr_instance(x,D)
	def _repr_iterable(H,x,level,left,right,maxiter,trail=''):
		C=trail;D=maxiter;E=level;A=right;B=len(x)
		if E<=0 and B:F=_A
		else:
			I=E-1;J=H.repr1;G=[J(A,I)for A in islice(x,D)]
			if B>D:G.append(_A)
			F=', '.join(G)
			if B==1 and C:A=C+A
		return'%s%s%s'%(left,F,A)
	def repr_tuple(A,x,level):return A._repr_iterable(x,level,'(',')',A.maxtuple,',')
	def repr_list(A,x,level):return A._repr_iterable(x,level,'[',']',A.maxlist)
	def repr_array(A,x,level):
		if not x:return"array('%s')"%x.typecode
		B="array('%s', ["%x.typecode;return A._repr_iterable(x,level,B,'])',A.maxarray)
	def repr_set(A,x,level):
		if not x:return'set()'
		x=_possibly_sorted(x);return A._repr_iterable(x,level,'{','}',A.maxset)
	def repr_frozenset(A,x,level):
		if not x:return'frozenset()'
		x=_possibly_sorted(x);return A._repr_iterable(x,level,'frozenset({','})',A.maxfrozenset)
	def repr_deque(A,x,level):return A._repr_iterable(x,level,'deque([','])',A.maxdeque)
	def repr_dict(A,x,level):
		C=level;D=len(x)
		if D==0:return'{}'
		if C<=0:return'{...}'
		E=C-1;F=A.repr1;B=[]
		for G in islice(_possibly_sorted(x),A.maxdict):H=F(G,E);I=F(x[G],E);B.append('%s: %s'%(H,I))
		if D>A.maxdict:B.append(_A)
		J=', '.join(B);return'{%s}'%(J,)
	def repr_str(B,x,level):
		A=builtins.repr(x[:B.maxstring])
		if len(A)>B.maxstring:C=max(0,(B.maxstring-3)//2);D=max(0,B.maxstring-3-C);A=builtins.repr(x[:C]+x[len(x)-D:]);A=A[:C]+_A+A[len(A)-D:]
		return A
	def repr_int(B,x,level):
		A=builtins.repr(x)
		if len(A)>B.maxlong:C=max(0,(B.maxlong-3)//2);D=max(0,B.maxlong-3-C);A=A[:C]+_A+A[len(A)-D:]
		return A
	def repr_instance(B,x,level):
		try:A=builtins.repr(x)
		except Exception:return'<%s instance at %#x>'%(x.__class__.__name__,id(x))
		if len(A)>B.maxother:C=max(0,(B.maxother-3)//2);D=max(0,B.maxother-3-C);A=A[:C]+_A+A[len(A)-D:]
		return A
def _possibly_sorted(x):
	try:return sorted(x)
	except Exception:return list(x)
aRepr=Repr()
repr=aRepr.repr