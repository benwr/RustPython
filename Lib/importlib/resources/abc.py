import abc,io,os
from typing import Any,BinaryIO,Iterable,Iterator,NoReturn,Text,Optional,runtime_checkable,Protocol,Union
StrPath=Union[str,os.PathLike[str]]
__all__=['ResourceReader','Traversable','TraversableResources']
class ResourceReader(metaclass=abc.ABCMeta):
	'Abstract base class for loaders to provide resource reading support.'
	@abc.abstractmethod
	def open_resource(self,resource):"Return an opened, file-like object for binary reading.\n\n        The 'resource' argument is expected to represent only a file name.\n        If the resource cannot be found, FileNotFoundError is raised.\n        ";raise FileNotFoundError
	@abc.abstractmethod
	def resource_path(self,resource):"Return the file system path to the specified resource.\n\n        The 'resource' argument is expected to represent only a file name.\n        If the resource does not exist on the file system, raise\n        FileNotFoundError.\n        ";raise FileNotFoundError
	@abc.abstractmethod
	def is_resource(self,path):"Return True if the named 'path' is a resource.\n\n        Files are resources, directories are not.\n        ";raise FileNotFoundError
	@abc.abstractmethod
	def contents(self):'Return an iterable of entries in `package`.';raise FileNotFoundError
@runtime_checkable
class Traversable(Protocol):
	'\n    An object with a subset of pathlib.Path methods suitable for\n    traversing directories and opening files.\n\n    Any exceptions that occur when accessing the backing resource\n    may propagate unaltered.\n    '
	@abc.abstractmethod
	def iterdir(self):'\n        Yield Traversable objects in self\n        '
	def read_bytes(A):
		'\n        Read contents of self as bytes\n        '
		with A.open('rb')as B:return B.read()
	def read_text(A,encoding=None):
		'\n        Read contents of self as text\n        '
		with A.open(encoding=encoding)as B:return B.read()
	@abc.abstractmethod
	def is_dir(self):'\n        Return True if self is a directory\n        '
	@abc.abstractmethod
	def is_file(self):'\n        Return True if self is a file\n        '
	@abc.abstractmethod
	def joinpath(self,*A):'\n        Return Traversable resolved with any descendants applied.\n\n        Each descendant should be a path segment relative to self\n        and each may contain multiple levels separated by\n        ``posixpath.sep`` (``/``).\n        '
	def __truediv__(A,child):'\n        Return Traversable child in self\n        ';return A.joinpath(child)
	@abc.abstractmethod
	def open(self,mode='r',*A,**B):"\n        mode may be 'r' or 'rb' to open as text or binary. Return a handle\n        suitable for reading (same as pathlib.Path.open).\n\n        When opening as text, accepts encoding parameters such as those\n        accepted by io.TextIOWrapper.\n        "
	@abc.abstractproperty
	def name(self):'\n        The base name of this object without any parent references.\n        '
class TraversableResources(ResourceReader):
	'\n    The required interface for providing traversable\n    resources.\n    '
	@abc.abstractmethod
	def files(self):'Return a Traversable object for the loaded package.'
	def open_resource(A,resource):return A.files().joinpath(resource).open('rb')
	def resource_path(A,resource):raise FileNotFoundError(resource)
	def is_resource(A,path):return A.files().joinpath(path).is_file()
	def contents(A):return(A.name for A in A.files().iterdir())