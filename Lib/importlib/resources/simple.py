'\nInterface adapters for low-level readers.\n'
import abc,io,itertools
from typing import BinaryIO,List
from.abc import Traversable,TraversableResources
class SimpleReader(abc.ABC):
	'\n    The minimum, low-level interface required from a resource\n    provider.\n    '
	@abc.abstractproperty
	def package(self):'\n        The name of the package for which this reader loads resources.\n        '
	@abc.abstractmethod
	def children(self):'\n        Obtain an iterable of SimpleReader for available\n        child containers (e.g. directories).\n        '
	@abc.abstractmethod
	def resources(self):'\n        Obtain available named resources for this virtual package.\n        '
	@abc.abstractmethod
	def open_binary(self,resource):'\n        Obtain a File-like for a named resource.\n        '
	@property
	def name(self):return self.package.split('.')[-1]
class ResourceHandle(Traversable):
	'\n    Handle to a named resource in a ResourceReader.\n    '
	def __init__(A,parent,name):A.parent=parent;A.name=name
	def is_file(A):return True
	def is_dir(A):return False
	def open(A,mode='r',*C,**D):
		B=A.parent.reader.open_binary(A.name)
		if'b'not in mode:B=io.TextIOWrapper(*C,**D)
		return B
	def joinpath(A,name):raise RuntimeError('Cannot traverse into a resource')
class ResourceContainer(Traversable):
	"\n    Traversable container for a package's resources via its reader.\n    "
	def __init__(A,reader):A.reader=reader
	def is_dir(A):return True
	def is_file(A):return False
	def iterdir(A):B=(ResourceHandle(A,B)for B in A.reader.resources);C=map(ResourceContainer,A.reader.children());return itertools.chain(B,C)
	def open(A,*B,**C):raise IsADirectoryError()
	@staticmethod
	def _flatten(compound_names):
		for A in compound_names:yield from A.split('/')
	def joinpath(A,*B):
		if not B:return A
		C=A._flatten(B);D=next(C);return next(A for A in A.iterdir()if A.name==D).joinpath(*C)
class TraversableReader(TraversableResources,SimpleReader):
	'\n    A TraversableResources based on SimpleReader. Resource providers\n    may derive from this class to provide the TraversableResources\n    interface by supplying the SimpleReader interface.\n    '
	def files(A):return ResourceContainer(A)