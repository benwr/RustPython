'A pure Python implementation of import.'
_F='importlib._bootstrap_external'
_E='__init__.py'
_D='importlib'
_C='importlib._bootstrap'
_B='invalidate_caches'
_A=None
__all__=['__import__','import_module',_B,'reload']
import _imp,sys
try:import _frozen_importlib as _bootstrap
except ImportError:from.import _bootstrap;_bootstrap._setup(sys,_imp)
else:
	_bootstrap.__name__=_C;_bootstrap.__package__=_D
	try:_bootstrap.__file__=__file__.replace(_E,'_bootstrap.py')
	except NameError:pass
	sys.modules[_C]=_bootstrap
try:import _frozen_importlib_external as _bootstrap_external
except ImportError:from.import _bootstrap_external;_bootstrap_external._set_bootstrap_module(_bootstrap);_bootstrap._bootstrap_external=_bootstrap_external
else:
	_bootstrap_external.__name__=_F;_bootstrap_external.__package__=_D
	try:_bootstrap_external.__file__=__file__.replace(_E,'_bootstrap_external.py')
	except NameError:pass
	sys.modules[_F]=_bootstrap_external
_pack_uint32=_bootstrap_external._pack_uint32
_unpack_uint32=_bootstrap_external._unpack_uint32
import warnings
from._bootstrap import __import__
def invalidate_caches():
	'Call the invalidate_caches() method on all meta path finders stored in\n    sys.meta_path (where implemented).'
	for A in sys.meta_path:
		if hasattr(A,_B):A.invalidate_caches()
def find_loader(name,path=_A):
	'Return the loader for the specified module.\n\n    This is a backward-compatible wrapper around find_spec().\n\n    This function is deprecated in favor of importlib.util.find_spec().\n\n    ';A=name;warnings.warn('Deprecated since Python 3.4 and slated for removal in Python 3.12; use importlib.util.find_spec() instead',DeprecationWarning,stacklevel=2)
	try:
		C=sys.modules[A].__loader__
		if C is _A:raise ValueError('{}.__loader__ is None'.format(A))
		else:return C
	except KeyError:pass
	except AttributeError:raise ValueError('{}.__loader__ is not set'.format(A))from _A
	B=_bootstrap._find_spec(A,path)
	if B is _A:return
	if B.loader is _A:
		if B.submodule_search_locations is _A:raise ImportError('spec for {} missing loader'.format(A),name=A)
		raise ImportError('namespace packages do not have loaders',name=A)
	return B.loader
def import_module(name,package=_A):
	"Import a module.\n\n    The 'package' argument is required when performing a relative import. It\n    specifies the package to use as the anchor point from which to resolve the\n    relative import to an absolute import.\n\n    ";C=package;A=name;B=0
	if A.startswith('.'):
		if not C:D="the 'package' argument is required to perform a relative import for {!r}";raise TypeError(D.format(A))
		for E in A:
			if E!='.':break
			B+=1
	return _bootstrap._gcd_import(A[B:],C,B)
_RELOADING={}
def reload(module):
	'Reload the module and return it.\n\n    The module must have been successfully imported before.\n\n    ';B=module
	try:A=B.__spec__.name
	except AttributeError:
		try:A=B.__name__
		except AttributeError:raise TypeError('reload() argument must be a module')
	if sys.modules.get(A)is not B:D='module {} not in sys.modules';raise ImportError(D.format(A),name=A)
	if A in _RELOADING:return _RELOADING[A]
	_RELOADING[A]=B
	try:
		C=A.rpartition('.')[0]
		if C:
			try:G=sys.modules[C]
			except KeyError:D='parent {!r} not in sys.modules';raise ImportError(D.format(C),name=C)from _A
			else:E=G.__path__
		else:E=_A
		H=B;F=B.__spec__=_bootstrap._find_spec(A,E,H)
		if F is _A:raise ModuleNotFoundError(f"spec not found for the module {A!r}",name=A)
		_bootstrap._exec(F,B);return sys.modules[A]
	finally:
		try:del _RELOADING[A]
		except KeyError:pass