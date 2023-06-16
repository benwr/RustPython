"This module provides the components needed to build your own __import__\nfunction.  Undocumented functions are obsolete.\n\nIn most cases it is preferred you consider using the importlib module's\nfunctionality over this module.\n\n"
_C='__init__'
_B='rb'
_A=None
from _imp import lock_held,acquire_lock,release_lock,get_frozen_object,is_frozen_package,init_frozen,is_builtin,is_frozen,_fix_co_filename
try:from _imp import create_dynamic
except ImportError:create_dynamic=_A
from importlib._bootstrap import _ERR_MSG,_exec,_load,_builtin_from_name
from importlib._bootstrap_external import SourcelessFileLoader
from importlib import machinery
from importlib import util
import importlib,os,sys,tokenize,types,warnings
warnings.warn("the imp module is deprecated in favour of importlib and slated for removal in Python 3.12; see the module's documentation for alternative uses",DeprecationWarning,stacklevel=2)
SEARCH_ERROR=0
PY_SOURCE=1
PY_COMPILED=2
C_EXTENSION=3
PY_RESOURCE=4
PKG_DIRECTORY=5
C_BUILTIN=6
PY_FROZEN=7
PY_CODERESOURCE=8
IMP_HOOK=9
def new_module(name):'**DEPRECATED**\n\n    Create a new module.\n\n    The module is not entered into sys.modules.\n\n    ';return types.ModuleType(name)
def get_magic():'**DEPRECATED**\n\n    Return the magic number for .pyc files.\n    ';return util.MAGIC_NUMBER
def get_tag():'Return the magic tag for .pyc files.';return sys.implementation.cache_tag
def cache_from_source(path,debug_override=_A):
	'**DEPRECATED**\n\n    Given the path to a .py file, return the path to its .pyc file.\n\n    The .py file does not need to exist; this simply returns the path to the\n    .pyc file calculated as if the .py file were imported.\n\n    If debug_override is not None, then it must be a boolean and is used in\n    place of sys.flags.optimize.\n\n    If sys.implementation.cache_tag is None then NotImplementedError is raised.\n\n    '
	with warnings.catch_warnings():warnings.simplefilter('ignore');return util.cache_from_source(path,debug_override)
def source_from_cache(path):'**DEPRECATED**\n\n    Given the path to a .pyc. file, return the path to its .py file.\n\n    The .pyc file does not need to exist; this simply returns the path to\n    the .py file calculated to correspond to the .pyc file.  If path does\n    not conform to PEP 3147 format, ValueError will be raised. If\n    sys.implementation.cache_tag is None then NotImplementedError is raised.\n\n    ';return util.source_from_cache(path)
def get_suffixes():'**DEPRECATED**';A=[(A,_B,C_EXTENSION)for A in machinery.EXTENSION_SUFFIXES];B=[(A,'r',PY_SOURCE)for A in machinery.SOURCE_SUFFIXES];C=[(A,_B,PY_COMPILED)for A in machinery.BYTECODE_SUFFIXES];return A+B+C
class NullImporter:
	'**DEPRECATED**\n\n    Null import object.\n\n    '
	def __init__(B,path):
		A=path
		if A=='':raise ImportError('empty pathname',path='')
		elif os.path.isdir(A):raise ImportError('existing directory',path=A)
	def find_module(A,fullname):'Always returns None.'
class _HackedGetData:
	"Compatibility support for 'file' arguments of various load_*()\n    functions."
	def __init__(A,fullname,path,file=_A):super().__init__(fullname,path);A.file=file
	def get_data(A,path):
		"Gross hack to contort loader to deal w/ load_*()'s bad API."
		if A.file and path==A.path:
			if not A.file.closed:
				B=A.file
				if'b'not in B.mode:B.close()
			if A.file.closed:A.file=B=open(A.path,_B)
			with B:return B.read()
		else:return super().get_data(path)
class _LoadSourceCompatibility(_HackedGetData,machinery.SourceFileLoader):'Compatibility support for implementing load_source().'
def load_source(name,pathname,file=_A):
	C=pathname;A=name;E=_LoadSourceCompatibility(A,C,file);D=util.spec_from_file_location(A,C,loader=E)
	if A in sys.modules:B=_exec(D,sys.modules[A])
	else:B=_load(D)
	B.__loader__=machinery.SourceFileLoader(A,C);B.__spec__.loader=B.__loader__;return B
class _LoadCompiledCompatibility(_HackedGetData,SourcelessFileLoader):'Compatibility support for implementing load_compiled().'
def load_compiled(name,pathname,file=_A):
	'**DEPRECATED**';C=pathname;A=name;E=_LoadCompiledCompatibility(A,C,file);D=util.spec_from_file_location(A,C,loader=E)
	if A in sys.modules:B=_exec(D,sys.modules[A])
	else:B=_load(D)
	B.__loader__=SourcelessFileLoader(A,C);B.__spec__.loader=B.__loader__;return B
def load_package(name,path):
	'**DEPRECATED**';B=name;A=path
	if os.path.isdir(A):
		E=machinery.SOURCE_SUFFIXES[:]+machinery.BYTECODE_SUFFIXES[:]
		for F in E:
			C=os.path.join(A,_C+F)
			if os.path.exists(C):A=C;break
		else:raise ValueError('{!r} is not a package'.format(A))
	D=util.spec_from_file_location(B,A,submodule_search_locations=[])
	if B in sys.modules:return _exec(D,sys.modules[B])
	else:return _load(D)
def load_module(name,file,filename,details):
	'**DEPRECATED**\n\n    Load a module, given information returned by find_module().\n\n    The module name must include the full package name, if any.\n\n    ';D=file;C=filename;A=name;H,E,B=details
	if E and(not E.startswith(('r','U'))or'+'in E):raise ValueError('invalid file open mode {!r}'.format(E))
	elif D is _A and B in{PY_SOURCE,PY_COMPILED}:F='file object required for import (type code {})'.format(B);raise ValueError(F)
	elif B==PY_SOURCE:return load_source(A,C,D)
	elif B==PY_COMPILED:return load_compiled(A,C,D)
	elif B==C_EXTENSION and load_dynamic is not _A:
		if D is _A:
			with open(C,_B)as G:return load_dynamic(A,C,G)
		else:return load_dynamic(A,C,D)
	elif B==PKG_DIRECTORY:return load_package(A,C)
	elif B==C_BUILTIN:return init_builtin(A)
	elif B==PY_FROZEN:return init_frozen(A)
	else:F="Don't know how to import {} (type code {})".format(A,B);raise ImportError(F,name=A)
def find_module(name,path=_A):
	"**DEPRECATED**\n\n    Search for a module.\n\n    If path is omitted or None, search for a built-in, frozen or special\n    module and continue search in sys.path. The module name cannot\n    contain '.'; to search for a submodule of a package, pass the\n    submodule name and the package's __path__.\n\n    ";C=path;A=name
	if not isinstance(A,str):raise TypeError("'name' must be a str, not {}".format(type(A)))
	elif not isinstance(C,(type(_A),list)):raise RuntimeError("'path' must be None or a list, not {}".format(type(C)))
	if C is _A:
		if is_builtin(A):return _A,_A,('','',C_BUILTIN)
		elif is_frozen(A):return _A,_A,('','',PY_FROZEN)
		else:C=sys.path
	for G in C:
		H=os.path.join(G,A)
		for D in['.py',machinery.BYTECODE_SUFFIXES[0]]:
			J=_C+D;B=os.path.join(H,J)
			if os.path.isfile(B):return _A,H,('','',PKG_DIRECTORY)
		for(D,E,K)in get_suffixes():
			L=A+D;B=os.path.join(G,L)
			if os.path.isfile(B):break
		else:continue
		break
	else:raise ImportError(_ERR_MSG.format(A),name=A)
	I=_A
	if'b'not in E:
		with open(B,_B)as F:I=tokenize.detect_encoding(F.readline)[0]
	F=open(B,E,encoding=I);return F,B,(D,E,K)
def reload(module):'**DEPRECATED**\n\n    Reload the module and return it.\n\n    The module must have been successfully imported before.\n\n    ';return importlib.reload(module)
def init_builtin(name):
	"**DEPRECATED**\n\n    Load and return a built-in module by name, or None is such module doesn't\n    exist\n    "
	try:return _builtin_from_name(name)
	except ImportError:return
if create_dynamic:
	def load_dynamic(name,path,file=_A):'**DEPRECATED**\n\n        Load an extension module.\n        ';import importlib.machinery;A=importlib.machinery.ExtensionFileLoader(name,path);B=importlib.machinery.ModuleSpec(name=name,loader=A,origin=path);return _load(B)
else:load_dynamic=_A