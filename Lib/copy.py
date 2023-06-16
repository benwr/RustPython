'Generic (shallow and deep) copying operations.\n\nInterface summary:\n\n        import copy\n\n        x = copy.copy(y)        # make a shallow copy of y\n        x = copy.deepcopy(y)    # make a deep copy of y\n\nFor module specific errors, copy.Error is raised.\n\nThe difference between shallow and deep copying is only relevant for\ncompound objects (objects that contain other objects, like lists or\nclass instances).\n\n- A shallow copy constructs a new compound object and then (to the\n  extent possible) inserts *the same objects* into it that the\n  original contains.\n\n- A deep copy constructs a new compound object and then, recursively,\n  inserts *copies* into it of the objects found in the original.\n\nTwo problems often exist with deep copy operations that don\'t exist\nwith shallow copy operations:\n\n a) recursive objects (compound objects that, directly or indirectly,\n    contain a reference to themselves) may cause a recursive loop\n\n b) because deep copy copies *everything* it may copy too much, e.g.\n    administrative data structures that should be shared even between\n    copies\n\nPython\'s deep copy operation avoids these problems by:\n\n a) keeping a table of objects already copied during the current\n    copying pass\n\n b) letting user-defined classes override the copying operation or the\n    set of components copied\n\nThis version does not copy types like module, class, function, method,\nnor stack trace, stack frame, nor file, socket, window, nor any\nsimilar types.\n\nClasses can use the same interfaces to control copying that they use\nto control pickling: they can define methods called __getinitargs__(),\n__getstate__() and __setstate__().  See the documentation for module\n"pickle" for information on these methods.\n'
_C='__reduce__'
_B='__reduce_ex__'
_A=None
import types,weakref
from copyreg import dispatch_table
class Error(Exception):0
error=Error
try:from org.python.core import PyStringMap
except ImportError:PyStringMap=_A
__all__=['Error','copy','deepcopy']
def copy(x):
	"Shallow copy operation on arbitrary Python objects.\n\n    See the module's __doc__ string for more info.\n    ";B=type(x);C=_copy_dispatch.get(B)
	if C:return C(x)
	if issubclass(B,type):return _copy_immutable(x)
	C=getattr(B,'__copy__',_A)
	if C is not _A:return C(x)
	A=dispatch_table.get(B)
	if A is not _A:D=A(x)
	else:
		A=getattr(x,_B,_A)
		if A is not _A:D=A(4)
		else:
			A=getattr(x,_C,_A)
			if A:D=A()
			else:raise Error('un(shallow)copyable object of type %s'%B)
	if isinstance(D,str):return x
	return _reconstruct(x,_A,*D)
_copy_dispatch=d={}
def _copy_immutable(x):return x
for t in(type(_A),int,float,bool,complex,str,tuple,bytes,frozenset,type,range,slice,property,types.BuiltinFunctionType,type(Ellipsis),type(NotImplemented),types.FunctionType,weakref.ref):d[t]=_copy_immutable
t=getattr(types,'CodeType',_A)
if t is not _A:d[t]=_copy_immutable
d[list]=list.copy
d[dict]=dict.copy
d[set]=set.copy
d[bytearray]=bytearray.copy
if PyStringMap is not _A:d[PyStringMap]=PyStringMap.copy
del d,t
def deepcopy(x,memo=_A,_nil=[]):
	"Deep copy operation on arbitrary Python objects.\n\n    See the module's __doc__ string for more info.\n    ";B=memo
	if B is _A:B={}
	G=id(x);A=B.get(G,_nil)
	if A is not _nil:return A
	E=type(x);D=_deepcopy_dispatch.get(E)
	if D is not _A:A=D(x,B)
	elif issubclass(E,type):A=_deepcopy_atomic(x,B)
	else:
		D=getattr(x,'__deepcopy__',_A)
		if D is not _A:A=D(B)
		else:
			C=dispatch_table.get(E)
			if C:F=C(x)
			else:
				C=getattr(x,_B,_A)
				if C is not _A:F=C(4)
				else:
					C=getattr(x,_C,_A)
					if C:F=C()
					else:raise Error('un(deep)copyable object of type %s'%E)
			if isinstance(F,str):A=x
			else:A=_reconstruct(x,B,*F)
	if A is not x:B[G]=A;_keep_alive(x,B)
	return A
_deepcopy_dispatch=d={}
def _deepcopy_atomic(x,memo):return x
d[type(_A)]=_deepcopy_atomic
d[type(Ellipsis)]=_deepcopy_atomic
d[type(NotImplemented)]=_deepcopy_atomic
d[int]=_deepcopy_atomic
d[float]=_deepcopy_atomic
d[bool]=_deepcopy_atomic
d[complex]=_deepcopy_atomic
d[bytes]=_deepcopy_atomic
d[str]=_deepcopy_atomic
d[types.CodeType]=_deepcopy_atomic
d[type]=_deepcopy_atomic
d[range]=_deepcopy_atomic
d[types.BuiltinFunctionType]=_deepcopy_atomic
d[types.FunctionType]=_deepcopy_atomic
d[weakref.ref]=_deepcopy_atomic
d[property]=_deepcopy_atomic
def _deepcopy_list(x,memo,deepcopy=deepcopy):
	A=[];memo[id(x)]=A;B=A.append
	for C in x:B(deepcopy(C,memo))
	return A
d[list]=_deepcopy_list
def _deepcopy_tuple(x,memo,deepcopy=deepcopy):
	A=[deepcopy(A,memo)for A in x]
	try:return memo[id(x)]
	except KeyError:pass
	for(B,C)in zip(x,A):
		if B is not C:A=tuple(A);break
	else:A=x
	return A
d[tuple]=_deepcopy_tuple
def _deepcopy_dict(x,memo,deepcopy=deepcopy):
	C=deepcopy;A=memo;B={};A[id(x)]=B
	for(D,E)in x.items():B[C(D,A)]=C(E,A)
	return B
d[dict]=_deepcopy_dict
if PyStringMap is not _A:d[PyStringMap]=_deepcopy_dict
def _deepcopy_method(x,memo):return type(x)(x.__func__,deepcopy(x.__self__,memo))
d[types.MethodType]=_deepcopy_method
del d
def _keep_alive(x,memo):
	'Keeps a reference to the object x in the memo.\n\n    Because we remember objects by their id, we have\n    to assure that possibly temporary objects are kept\n    alive by referencing them.\n    We store a reference at the id of the memo, which should\n    normally not be used unless someone tries to deepcopy\n    the memo itself...\n    ';A=memo
	try:A[id(A)].append(x)
	except KeyError:A[id(A)]=[x]
def _reconstruct(x,memo,func,args,state=_A,listiter=_A,dictiter=_A,*,deepcopy=deepcopy):
	J=dictiter;K=listiter;I=args;F=deepcopy;C=memo;A=state;G=C is not _A
	if G and I:I=(F(A,C)for A in I)
	B=func(*I)
	if G:C[id(x)]=B
	if A is not _A:
		if G:A=F(A,C)
		if hasattr(B,'__setstate__'):B.__setstate__(A)
		else:
			if isinstance(A,tuple)and len(A)==2:A,L=A
			else:L=_A
			if A is not _A:B.__dict__.update(A)
			if L is not _A:
				for(D,E)in L.items():setattr(B,D,E)
	if K is not _A:
		if G:
			for H in K:H=F(H,C);B.append(H)
		else:
			for H in K:B.append(H)
	if J is not _A:
		if G:
			for(D,E)in J:D=F(D,C);E=F(E,C);B[D]=E
		else:
			for(D,E)in J:B[D]=E
	return B
del types,weakref,PyStringMap