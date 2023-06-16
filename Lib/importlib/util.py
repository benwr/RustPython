'Utility code for constructing importers, etc.'
_F='__dict__'
_E='__path__'
_D='{}.__spec__ is None'
_C='{}.__spec__ is not set'
_B='The import system now takes care of this automatically; this decorator is slated for removal in Python 3.12'
_A=None
from._abc import Loader
from._bootstrap import module_from_spec
from._bootstrap import _resolve_name
from._bootstrap import spec_from_loader
from._bootstrap import _find_spec
from._bootstrap_external import MAGIC_NUMBER
from._bootstrap_external import _RAW_MAGIC_NUMBER
from._bootstrap_external import cache_from_source
from._bootstrap_external import decode_source
from._bootstrap_external import source_from_cache
from._bootstrap_external import spec_from_file_location
from contextlib import contextmanager
import _imp,functools,sys,types,warnings
def source_hash(source_bytes):'Return the hash of *source_bytes* as used in hash-based pyc files.';return _imp.source_hash(_RAW_MAGIC_NUMBER,source_bytes)
def resolve_name(name,package):
	'Resolve a relative module name to an absolute one.';C=package;A=name
	if not A.startswith('.'):return A
	elif not C:raise ImportError(f"no package specified for {repr(A)} (required for relative module names)")
	B=0
	for D in A:
		if D!='.':break
		B+=1
	return _resolve_name(A[B:],C,B)
def _find_spec_from_path(name,path=_A):
	"Return the spec for the specified module.\n\n    First, sys.modules is checked to see if the module was already imported. If\n    so, then sys.modules[name].__spec__ is returned. If that happens to be\n    set to None, then ValueError is raised. If the module is not in\n    sys.modules, then sys.meta_path is searched for a suitable spec with the\n    value of 'path' given to the finders. None is returned if no spec could\n    be found.\n\n    Dotted names do not have their parent packages implicitly imported. You will\n    most likely need to explicitly import all parent packages in the proper\n    order for a submodule to get the correct spec.\n\n    ";A=name
	if A not in sys.modules:return _find_spec(A,path)
	else:
		B=sys.modules[A]
		if B is _A:return
		try:C=B.__spec__
		except AttributeError:raise ValueError(_C.format(A))from _A
		else:
			if C is _A:raise ValueError(_D.format(A))
			return C
def find_spec(name,package=_A):
	"Return the spec for the specified module.\n\n    First, sys.modules is checked to see if the module was already imported. If\n    so, then sys.modules[name].__spec__ is returned. If that happens to be\n    set to None, then ValueError is raised. If the module is not in\n    sys.modules, then sys.meta_path is searched for a suitable spec with the\n    value of 'path' given to the finders. None is returned if no spec could\n    be found.\n\n    If the name is for submodule (contains a dot), the parent module is\n    automatically imported.\n\n    The name and package arguments work the same as importlib.import_module().\n    In other words, relative module names (with leading dots) work.\n\n    ";B=name;A=resolve_name(B,package)if B.startswith('.')else B
	if A not in sys.modules:
		C=A.rpartition('.')[0]
		if C:
			G=__import__(C,fromlist=[_E])
			try:D=G.__path__
			except AttributeError as H:raise ModuleNotFoundError(f"__path__ attribute not found on {C!r} while trying to find {A!r}",name=A)from H
		else:D=_A
		return _find_spec(A,D)
	else:
		E=sys.modules[A]
		if E is _A:return
		try:F=E.__spec__
		except AttributeError:raise ValueError(_C.format(B))from _A
		else:
			if F is _A:raise ValueError(_D.format(B))
			return F
@contextmanager
def _module_to_load(name):
	A=name;C=A in sys.modules;B=sys.modules.get(A)
	if not C:B=type(sys)(A);B.__initializing__=True;sys.modules[A]=B
	try:yield B
	except Exception:
		if not C:
			try:del sys.modules[A]
			except KeyError:pass
	finally:B.__initializing__=False
def set_package(fxn):
	'Set __package__ on the returned module.\n\n    This function is deprecated.\n\n    '
	@functools.wraps(fxn)
	def A(*B,**C):
		warnings.warn(_B,DeprecationWarning,stacklevel=2);A=fxn(*B,**C)
		if getattr(A,'__package__',_A)is _A:
			A.__package__=A.__name__
			if not hasattr(A,_E):A.__package__=A.__package__.rpartition('.')[0]
		return A
	return A
def set_loader(fxn):
	'Set __loader__ on the returned module.\n\n    This function is deprecated.\n\n    '
	@functools.wraps(fxn)
	def A(self,*B,**C):
		warnings.warn(_B,DeprecationWarning,stacklevel=2);A=fxn(self,*B,**C)
		if getattr(A,'__loader__',_A)is _A:A.__loader__=self
		return A
	return A
def module_for_loader(fxn):
	'Decorator to handle selecting the proper module for loaders.\n\n    The decorated function is passed the module to use instead of the module\n    name. The module passed in to the function is either from sys.modules if\n    it already exists or is a new module. If the module is new, then __name__\n    is set the first argument to the method, __loader__ is set to self, and\n    __package__ is set accordingly (if self.is_package() is defined) will be set\n    before it is passed to the decorated function (if self.is_package() does\n    not work for the module it will be set post-load).\n\n    If an exception is raised and the decorator created the module it is\n    subsequently removed from sys.modules.\n\n    The decorator assumes that the decorated function takes the module name as\n    the second argument.\n\n    ';warnings.warn(_B,DeprecationWarning,stacklevel=2)
	@functools.wraps(fxn)
	def A(self,fullname,*D,**E):
		C=self;A=fullname
		with _module_to_load(A)as B:
			B.__loader__=C
			try:F=C.is_package(A)
			except(ImportError,AttributeError):pass
			else:
				if F:B.__package__=A
				else:B.__package__=A.rpartition('.')[0]
			return fxn(C,B,*D,**E)
	return A
class _LazyModule(types.ModuleType):
	'A subclass of the module type which triggers loading upon attribute access.'
	def __getattribute__(A,attr):
		'Trigger the load of the module and return the attribute.';A.__class__=types.ModuleType;C=A.__spec__.name;E=A.__spec__.loader_state[_F];F=A.__dict__;D={}
		for(B,G)in F.items():
			if B not in E:D[B]=G
			elif id(F[B])!=id(E[B]):D[B]=G
		A.__spec__.loader.exec_module(A)
		if C in sys.modules:
			if id(A)!=id(sys.modules[C]):raise ValueError(f"module object for {C!r} substituted in sys.modules during a lazy load")
		A.__dict__.update(D);return getattr(A,attr)
	def __delattr__(A,attr):'Trigger the load and then perform the deletion.';A.__getattribute__(attr);delattr(A,attr)
class LazyLoader(Loader):
	'A loader that creates a module which defers loading until attribute access.'
	@staticmethod
	def __check_eager_loader(loader):
		if not hasattr(loader,'exec_module'):raise TypeError('loader must define exec_module()')
	@classmethod
	def factory(A,loader):'Construct a callable which returns the eager loader made lazy.';B=loader;A.__check_eager_loader(B);return lambda*C,**D:A(B(*C,**D))
	def __init__(A,loader):B=loader;A.__check_eager_loader(B);A.loader=B
	def create_module(A,spec):return A.loader.create_module(spec)
	def exec_module(C,module):'Make the module load lazily.';A=module;A.__spec__.loader=C.loader;A.__loader__=C.loader;B={};B[_F]=A.__dict__.copy();B['__class__']=A.__class__;A.__spec__.loader_state=B;A.__class__=_LazyModule