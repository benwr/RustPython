import collections,operator,pathlib,zipfile
from.import abc
from._itertools import unique_everseen
def remove_duplicates(items):return iter(collections.OrderedDict.fromkeys(items))
class FileReader(abc.TraversableResources):
	def __init__(A,loader):A.path=pathlib.Path(loader.path).parent
	def resource_path(A,resource):'\n        Return the file system path to prevent\n        `resources.path()` from creating a temporary\n        copy.\n        ';return str(A.path.joinpath(resource))
	def files(A):return A.path
class ZipReader(abc.TraversableResources):
	def __init__(A,loader,module):B=loader;C,C,D=module.rpartition('.');A.prefix=B.prefix.replace('\\','/')+D+'/';A.archive=B.archive
	def open_resource(B,resource):
		try:return super().open_resource(resource)
		except KeyError as A:raise FileNotFoundError(A.args[0])
	def is_resource(B,path):A=B.files().joinpath(path);return A.is_file()and A.exists()
	def files(A):return zipfile.Path(A.archive,A.prefix)
class MultiplexedPath(abc.Traversable):
	'\n    Given a series of Traversable objects, implement a merged\n    version of the interface across all objects. Useful for\n    namespace packages which may be multihomed at a single\n    name.\n    '
	def __init__(A,*B):
		A._paths=list(map(pathlib.Path,remove_duplicates(B)))
		if not A._paths:C='MultiplexedPath must contain at least one path';raise FileNotFoundError(C)
		if not all(A.is_dir()for A in A._paths):raise NotADirectoryError('MultiplexedPath only supports directories')
	def iterdir(A):B=(B for A in A._paths for B in A.iterdir());return unique_everseen(B,key=operator.attrgetter('name'))
	def read_bytes(A):raise FileNotFoundError(f"{A} is not a file")
	def read_text(A,*B,**C):raise FileNotFoundError(f"{A} is not a file")
	def is_dir(A):return True
	def is_file(A):return False
	def joinpath(A,child):
		B=child
		for C in A.iterdir():
			if C.name==B:return C
		return A._paths[0]/B
	__truediv__=joinpath
	def open(A,*B,**C):raise FileNotFoundError(f"{A} is not a file")
	@property
	def name(self):return self._paths[0].name
	def __repr__(A):B=', '.join(f"'{A}'"for A in A._paths);return f"MultiplexedPath({B})"
class NamespaceReader(abc.TraversableResources):
	def __init__(B,namespace_path):
		A=namespace_path
		if'NamespacePath'not in str(A):raise ValueError('Invalid path')
		B.path=MultiplexedPath(*list(A))
	def resource_path(A,resource):'\n        Return the file system path to prevent\n        `resources.path()` from creating a temporary\n        copy.\n        ';return str(A.path.joinpath(resource))
	def files(A):return A.path