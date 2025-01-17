"\nDefine names for built-in types that aren't directly accessible as a builtin.\n"
_B=False
_A=None
import sys
def _f():0
FunctionType=type(_f)
LambdaType=type(lambda:_A)
CodeType=type(_f.__code__)
MappingProxyType=type(type.__dict__)
SimpleNamespace=type(sys.implementation)
def _cell_factory():
	a=1
	def f():nonlocal a
	return f.__closure__[0]
CellType=type(_cell_factory())
def _g():yield 1
GeneratorType=type(_g())
async def _c():0
_c=_c()
CoroutineType=type(_c)
_c.close()
async def _ag():yield
_ag=_ag()
AsyncGeneratorType=type(_ag)
class _C:
	def _m(self):0
MethodType=type(_C()._m)
BuiltinFunctionType=type(len)
BuiltinMethodType=type([].append)
WrapperDescriptorType=type(object.__init__)
MethodWrapperType=type(object().__str__)
MethodDescriptorType=type(str.join)
ClassMethodDescriptorType=type(dict.__dict__['fromkeys'])
ModuleType=type(sys)
try:raise TypeError
except TypeError:tb=sys.exc_info()[2];TracebackType=type(tb);FrameType=type(tb.tb_frame);tb=_A;del tb
GetSetDescriptorType=type(FunctionType.__code__)
MemberDescriptorType=type(FunctionType.__globals__)
del sys,_f,_g,_C,_c,_ag
def new_class(name,bases=(),kwds=_A,exec_body=_A):
	'Create a class object dynamically using the appropriate metaclass.';resolved_bases=resolve_bases(bases);meta,ns,kwds=prepare_class(name,resolved_bases,kwds)
	if exec_body is not _A:exec_body(ns)
	if resolved_bases is not bases:ns['__orig_bases__']=bases
	return meta(name,resolved_bases,ns,**kwds)
def resolve_bases(bases):
	'Resolve MRO entries dynamically as specified by PEP 560.';new_bases=list(bases);updated=_B;shift=0
	for(i,base)in enumerate(bases):
		if isinstance(base,type)and not isinstance(base,GenericAlias):continue
		if not hasattr(base,'__mro_entries__'):continue
		new_base=base.__mro_entries__(bases);updated=True
		if not isinstance(new_base,tuple):raise TypeError('__mro_entries__ must return a tuple')
		else:new_bases[i+shift:i+shift+1]=new_base;shift+=len(new_base)-1
	if not updated:return bases
	return tuple(new_bases)
def prepare_class(name,bases=(),kwds=_A):
	"Call the __prepare__ method of the appropriate metaclass.\n\n    Returns (metaclass, namespace, kwds) as a 3-tuple\n\n    *metaclass* is the appropriate metaclass\n    *namespace* is the prepared class namespace\n    *kwds* is an updated copy of the passed in kwds argument with any\n    'metaclass' entry removed. If no kwds argument is passed in, this will\n    be an empty dict.\n    ";A='metaclass'
	if kwds is _A:kwds={}
	else:kwds=dict(kwds)
	if A in kwds:meta=kwds.pop(A)
	elif bases:meta=type(bases[0])
	else:meta=type
	if isinstance(meta,type):meta=_calculate_meta(meta,bases)
	if hasattr(meta,'__prepare__'):ns=meta.__prepare__(name,bases,**kwds)
	else:ns={}
	return meta,ns,kwds
def _calculate_meta(meta,bases):
	'Calculate the most derived metaclass.';winner=meta
	for base in bases:
		base_meta=type(base)
		if issubclass(winner,base_meta):continue
		if issubclass(base_meta,winner):winner=base_meta;continue
		raise TypeError('metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases')
	return winner
class DynamicClassAttribute:
	"Route attribute access on a class to __getattr__.\n\n    This is a descriptor, used to define attributes that act differently when\n    accessed through an instance and through a class.  Instance access remains\n    normal, but access to an attribute through a class will be routed to the\n    class's __getattr__ method; this is done by raising AttributeError.\n\n    This allows one to have properties active on an instance, and have virtual\n    attributes on the class with the same name.  (Enum used this between Python\n    versions 3.4 - 3.9 .)\n\n    Subclass from this to use a different method of accessing virtual atributes\n    and still be treated properly by the inspect module. (Enum uses this since\n    Python 3.10 .)\n\n    "
	def __init__(self,fget=_A,fset=_A,fdel=_A,doc=_A):self.fget=fget;self.fset=fset;self.fdel=fdel;self.__doc__=doc or fget.__doc__;self.overwrite_doc=doc is _A;self.__isabstractmethod__=bool(getattr(fget,'__isabstractmethod__',_B))
	def __get__(self,instance,ownerclass=_A):
		if instance is _A:
			if self.__isabstractmethod__:return self
			raise AttributeError()
		elif self.fget is _A:raise AttributeError('unreadable attribute')
		return self.fget(instance)
	def __set__(self,instance,value):
		if self.fset is _A:raise AttributeError("can't set attribute")
		self.fset(instance,value)
	def __delete__(self,instance):
		if self.fdel is _A:raise AttributeError("can't delete attribute")
		self.fdel(instance)
	def getter(self,fget):fdoc=fget.__doc__ if self.overwrite_doc else _A;result=type(self)(fget,self.fset,self.fdel,fdoc or self.__doc__);result.overwrite_doc=self.overwrite_doc;return result
	def setter(self,fset):result=type(self)(self.fget,fset,self.fdel,self.__doc__);result.overwrite_doc=self.overwrite_doc;return result
	def deleter(self,fdel):result=type(self)(self.fget,self.fset,fdel,self.__doc__);result.overwrite_doc=self.overwrite_doc;return result
class _GeneratorWrapper:
	def __init__(self,gen):self.__wrapped=gen;self.__isgen=gen.__class__ is GeneratorType;self.__name__=getattr(gen,'__name__',_A);self.__qualname__=getattr(gen,'__qualname__',_A)
	def send(self,val):return self.__wrapped.send(val)
	def throw(self,tp,*rest):return self.__wrapped.throw(tp,*rest)
	def close(self):return self.__wrapped.close()
	@property
	def gi_code(self):return self.__wrapped.gi_code
	@property
	def gi_frame(self):return self.__wrapped.gi_frame
	@property
	def gi_running(self):return self.__wrapped.gi_running
	@property
	def gi_yieldfrom(self):return self.__wrapped.gi_yieldfrom
	cr_code=gi_code;cr_frame=gi_frame;cr_running=gi_running;cr_await=gi_yieldfrom
	def __next__(self):return next(self.__wrapped)
	def __iter__(self):
		if self.__isgen:return self.__wrapped
		return self
	__await__=__iter__
def coroutine(func):
	'Convert regular generator function to a coroutine.'
	if not callable(func):raise TypeError('types.coroutine() expects a callable')
	if _B and func.__class__ is FunctionType and getattr(func,'__code__',_A).__class__ is CodeType:
		co_flags=func.__code__.co_flags
		if co_flags&384:return func
		if co_flags&32:co=func.__code__;func.__code__=co.replace(co_flags=co.co_flags|256);return func
	import functools,_collections_abc
	@functools.wraps(func)
	def wrapped(*args,**kwargs):
		coro=func(*args,**kwargs)
		if coro.__class__ is CoroutineType or coro.__class__ is GeneratorType and coro.gi_code.co_flags&256:return coro
		if isinstance(coro,_collections_abc.Generator)and not isinstance(coro,_collections_abc.Coroutine):return _GeneratorWrapper(coro)
		return coro
	return wrapped
GenericAlias=type(list[int])
UnionType=type(int|str)
EllipsisType=type(Ellipsis)
NoneType=type(_A)
NotImplementedType=type(NotImplemented)
__all__=[n for n in globals()if n[:1]!='_']