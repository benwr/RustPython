'Abstract base classes related to import.'
_B='find_spec'
_A=None
from.import _bootstrap_external,machinery
try:import _frozen_importlib
except ImportError as exc:
	if exc.name!='_frozen_importlib':raise
	_frozen_importlib=_A
try:import _frozen_importlib_external
except ImportError:_frozen_importlib_external=_bootstrap_external
from._abc import Loader
import abc,warnings
from.resources.abc import ResourceReader,Traversable,TraversableResources
__all__=['Loader','Finder','MetaPathFinder','PathEntryFinder','ResourceLoader','InspectLoader','ExecutionLoader','FileLoader','SourceLoader','ResourceReader','Traversable','TraversableResources']
def _register(abstract_cls,*D):
	B=abstract_cls
	for A in D:
		B.register(A)
		if _frozen_importlib is not _A:
			try:C=getattr(_frozen_importlib,A.__name__)
			except AttributeError:C=getattr(_frozen_importlib_external,A.__name__)
			B.register(C)
class Finder(metaclass=abc.ABCMeta):
	'Legacy abstract base class for import finders.\n\n    It may be subclassed for compatibility with legacy third party\n    reimplementations of the import system.  Otherwise, finder\n    implementations should derive from the more specific MetaPathFinder\n    or PathEntryFinder ABCs.\n\n    Deprecated since Python 3.3\n    '
	def __init__(A):warnings.warn('the Finder ABC is deprecated and slated for removal in Python 3.12; use MetaPathFinder or PathEntryFinder instead',DeprecationWarning)
	@abc.abstractmethod
	def find_module(self,fullname,path=_A):'An abstract method that should find a module.\n        The fullname is a str and the optional path is a str or None.\n        Returns a Loader object or None.\n        ';warnings.warn('importlib.abc.Finder along with its find_module() method are deprecated and slated for removal in Python 3.12; use MetaPathFinder.find_spec() or PathEntryFinder.find_spec() instead',DeprecationWarning)
class MetaPathFinder(metaclass=abc.ABCMeta):
	'Abstract base class for import finders on sys.meta_path.'
	def find_module(A,fullname,path):
		'Return a loader for the module.\n\n        If no module is found, return None.  The fullname is a str and\n        the path is a list of strings or None.\n\n        This method is deprecated since Python 3.4 in favor of\n        finder.find_spec(). If find_spec() exists then backwards-compatible\n        functionality is provided for this method.\n\n        ';warnings.warn('MetaPathFinder.find_module() is deprecated since Python 3.4 in favor of MetaPathFinder.find_spec() and is slated for removal in Python 3.12',DeprecationWarning,stacklevel=2)
		if not hasattr(A,_B):return
		B=A.find_spec(fullname,path);return B.loader if B is not _A else _A
	def invalidate_caches(A):"An optional method for clearing the finder's cache, if any.\n        This method is used by importlib.invalidate_caches().\n        "
_register(MetaPathFinder,machinery.BuiltinImporter,machinery.FrozenImporter,machinery.PathFinder,machinery.WindowsRegistryFinder)
class PathEntryFinder(metaclass=abc.ABCMeta):
	'Abstract base class for path entry finders used by PathFinder.'
	def find_loader(B,fullname):
		'Return (loader, namespace portion) for the path entry.\n\n        The fullname is a str.  The namespace portion is a sequence of\n        path entries contributing to part of a namespace package. The\n        sequence may be empty.  If loader is not None, the portion will\n        be ignored.\n\n        The portion will be discarded if another path entry finder\n        locates the module as a normal module or package.\n\n        This method is deprecated since Python 3.4 in favor of\n        finder.find_spec(). If find_spec() is provided than backwards-compatible\n        functionality is provided.\n        ';warnings.warn('PathEntryFinder.find_loader() is deprecated since Python 3.4 in favor of PathEntryFinder.find_spec() (available since 3.4)',DeprecationWarning,stacklevel=2)
		if not hasattr(B,_B):return _A,[]
		A=B.find_spec(fullname)
		if A is not _A:
			if not A.submodule_search_locations:C=[]
			else:C=A.submodule_search_locations
			return A.loader,C
		else:return _A,[]
	find_module=_bootstrap_external._find_module_shim
	def invalidate_caches(A):"An optional method for clearing the finder's cache, if any.\n        This method is used by PathFinder.invalidate_caches().\n        "
_register(PathEntryFinder,machinery.FileFinder)
class ResourceLoader(Loader):
	'Abstract base class for loaders which can return data from their\n    back-end storage.\n\n    This ABC represents one of the optional protocols specified by PEP 302.\n\n    '
	@abc.abstractmethod
	def get_data(self,path):'Abstract method which when implemented should return the bytes for\n        the specified path.  The path must be a str.';raise OSError
class InspectLoader(Loader):
	'Abstract base class for loaders which support inspection about the\n    modules they can load.\n\n    This ABC represents one of the optional protocols specified by PEP 302.\n\n    '
	def is_package(A,fullname):'Optional method which when implemented should return whether the\n        module is a package.  The fullname is a str.  Returns a bool.\n\n        Raises ImportError if the module cannot be found.\n        ';raise ImportError
	def get_code(A,fullname):
		'Method which returns the code object for the module.\n\n        The fullname is a str.  Returns a types.CodeType if possible, else\n        returns None if a code object does not make sense\n        (e.g. built-in module). Raises ImportError if the module cannot be\n        found.\n        ';B=A.get_source(fullname)
		if B is _A:return
		return A.source_to_code(B)
	@abc.abstractmethod
	def get_source(self,fullname):'Abstract method which should return the source code for the\n        module.  The fullname is a str.  Returns a str.\n\n        Raises ImportError if the module cannot be found.\n        ';raise ImportError
	@staticmethod
	def source_to_code(data,path='<string>'):"Compile 'data' into a code object.\n\n        The 'data' argument can be anything that compile() can handle. The'path'\n        argument should be where the data was retrieved (when applicable).";return compile(data,path,'exec',dont_inherit=True)
	exec_module=_bootstrap_external._LoaderBasics.exec_module;load_module=_bootstrap_external._LoaderBasics.load_module
_register(InspectLoader,machinery.BuiltinImporter,machinery.FrozenImporter,machinery.NamespaceLoader)
class ExecutionLoader(InspectLoader):
	'Abstract base class for loaders that wish to support the execution of\n    modules as scripts.\n\n    This ABC represents one of the optional protocols specified in PEP 302.\n\n    '
	@abc.abstractmethod
	def get_filename(self,fullname):'Abstract method which should return the value that __file__ is to be\n        set to.\n\n        Raises ImportError if the module cannot be found.\n        ';raise ImportError
	def get_code(A,fullname):
		'Method to return the code object for fullname.\n\n        Should return None if not applicable (e.g. built-in module).\n        Raise ImportError if the module cannot be found.\n        ';C=fullname;B=A.get_source(C)
		if B is _A:return
		try:D=A.get_filename(C)
		except ImportError:return A.source_to_code(B)
		else:return A.source_to_code(B,D)
_register(ExecutionLoader,machinery.ExtensionFileLoader)
class FileLoader(_bootstrap_external.FileLoader,ResourceLoader,ExecutionLoader):'Abstract base class partially implementing the ResourceLoader and\n    ExecutionLoader ABCs.'
_register(FileLoader,machinery.SourceFileLoader,machinery.SourcelessFileLoader)
class SourceLoader(_bootstrap_external.SourceLoader,ResourceLoader,ExecutionLoader):
	'Abstract base class for loading source code (and optionally any\n    corresponding bytecode).\n\n    To support loading from source code, the abstractmethods inherited from\n    ResourceLoader and ExecutionLoader need to be implemented. To also support\n    loading from bytecode, the optional methods specified directly by this ABC\n    is required.\n\n    Inherited abstractmethods not implemented in this ABC:\n\n        * ResourceLoader.get_data\n        * ExecutionLoader.get_filename\n\n    '
	def path_mtime(A,path):
		'Return the (int) modification time for the path (str).'
		if A.path_stats.__func__ is SourceLoader.path_stats:raise OSError
		return int(A.path_stats(path)['mtime'])
	def path_stats(A,path):
		"Return a metadata dict for the source pointed to by the path (str).\n        Possible keys:\n        - 'mtime' (mandatory) is the numeric timestamp of last source\n          code modification;\n        - 'size' (optional) is the size in bytes of the source code.\n        "
		if A.path_mtime.__func__ is SourceLoader.path_mtime:raise OSError
		return{'mtime':A.path_mtime(path)}
	def set_data(A,path,data):'Write the bytes to the path (if possible).\n\n        Accepts a str path and data as bytes.\n\n        Any needed intermediary directories are to be created. If for some\n        reason the file cannot be written because of permissions, fail\n        silently.\n        '
_register(SourceLoader,machinery.SourceFileLoader)