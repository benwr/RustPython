'Helper to provide extensibility for pickle.\n\nThis is only useful to add pickle support for extension types defined in\nC, not for instances of user-defined classes.\n'
_B='__slots__'
_A=None
__all__=['pickle','constructor','add_extension','remove_extension','clear_extension_cache']
dispatch_table={}
def pickle(ob_type,pickle_function,constructor_ob=_A):
	B=constructor_ob;A=pickle_function
	if not callable(A):raise TypeError('reduction functions must be callable')
	dispatch_table[ob_type]=A
	if B is not _A:constructor(B)
def constructor(object):
	if not callable(object):raise TypeError('constructors must be callable')
try:complex
except NameError:pass
else:
	def pickle_complex(c):return complex,(c.real,c.imag)
	pickle(complex,pickle_complex,complex)
def _reconstructor(cls,base,state):
	C=state;A=base
	if A is object:B=object.__new__(cls)
	else:
		B=A.__new__(cls,C)
		if A.__init__!=object.__init__:A.__init__(B,C)
	return B
_HEAPTYPE=1<<9
def _reduce_ex(self,proto):
	D=proto;B=self;assert D<2;C=B.__class__
	for A in C.__mro__:
		if hasattr(A,'__flags__')and not A.__flags__&_HEAPTYPE:break
	else:A=object
	if A is object:E=_A
	else:
		if A is C:raise TypeError(f"cannot pickle {C.__name__!r} object")
		E=A(B)
	F=C,A,E
	try:G=B.__getstate__
	except AttributeError:
		if getattr(B,_B,_A):raise TypeError(f"cannot pickle {C.__name__!r} object: a class that defines __slots__ without defining __getstate__ cannot be pickled with protocol {D}")from _A
		try:dict=B.__dict__
		except AttributeError:dict=_A
	else:dict=G()
	if dict:return _reconstructor,F,dict
	else:return _reconstructor,F
def __newobj__(cls,*A):return cls.__new__(cls,*A)
def __newobj_ex__(cls,args,kwargs):'Used by pickle protocol 4, instead of __newobj__ to allow classes with\n    keyword-only arguments to be pickled correctly.\n    ';return cls.__new__(cls,*args,**kwargs)
def _slotnames(cls):
	"Return a list of slot names for a given class.\n\n    This needs to find slots defined by the class and its bases, so we\n    can't simply return the __slots__ attribute.  We must walk down\n    the Method Resolution Order and concatenate the __slots__ of each\n    class found there.  (This assumes classes don't modify their\n    __slots__ attribute to misrepresent their slots after the class is\n    defined.)\n    ";C=cls;A=C.__dict__.get('__slotnames__')
	if A is not _A:return A
	A=[]
	if not hasattr(C,_B):0
	else:
		for E in C.__mro__:
			if _B in E.__dict__:
				D=E.__dict__[_B]
				if isinstance(D,str):D=D,
				for B in D:
					if B in('__dict__','__weakref__'):continue
					elif B.startswith('__')and not B.endswith('__'):
						F=E.__name__.lstrip('_')
						if F:A.append('_%s%s'%(F,B))
						else:A.append(B)
					else:A.append(B)
	try:C.__slotnames__=A
	except:pass
	return A
_extension_registry={}
_inverted_registry={}
_extension_cache={}
def add_extension(module,name,code):
	'Register an extension code.';A=code;A=int(A)
	if not 1<=A<=2147483647:raise ValueError('code out of range')
	B=module,name
	if _extension_registry.get(B)==A and _inverted_registry.get(A)==B:return
	if B in _extension_registry:raise ValueError('key %s is already registered with code %s'%(B,_extension_registry[B]))
	if A in _inverted_registry:raise ValueError('code %s is already in use for key %s'%(A,_inverted_registry[A]))
	_extension_registry[B]=A;_inverted_registry[A]=B
def remove_extension(module,name,code):
	'Unregister an extension code.  For testing only.';A=code;B=module,name
	if _extension_registry.get(B)!=A or _inverted_registry.get(A)!=B:raise ValueError('key %s is not registered with code %s'%(B,A))
	del _extension_registry[B];del _inverted_registry[A]
	if A in _extension_cache:del _extension_cache[A]
def clear_extension_cache():_extension_cache.clear()