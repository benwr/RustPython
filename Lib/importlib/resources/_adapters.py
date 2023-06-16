from contextlib import suppress
from io import TextIOWrapper
from.import abc
class SpecLoaderAdapter:
	'\n    Adapt a package spec to adapt the underlying loader.\n    '
	def __init__(A,spec,adapter=lambda spec:spec.loader):A.spec=spec;A.loader=adapter(spec)
	def __getattr__(A,name):return getattr(A.spec,name)
class TraversableResourcesLoader:
	'\n    Adapt a loader to provide TraversableResources.\n    '
	def __init__(A,spec):A.spec=spec
	def get_resource_reader(A,name):return CompatibilityFiles(A.spec)._native()
def _io_wrapper(file,mode='r',*B,**C):
	A=mode
	if A=='r':return TextIOWrapper(file,*B,**C)
	elif A=='rb':return file
	raise ValueError("Invalid mode value '{}', only 'r' and 'rb' are supported".format(A))
class CompatibilityFiles:
	'\n    Adapter for an existing or non-existent resource reader\n    to provide a compatibility .files().\n    '
	class SpecPath(abc.Traversable):
		'\n        Path tied to a module spec.\n        Can be read and exposes the resource reader children.\n        '
		def __init__(A,spec,reader):A._spec=spec;A._reader=reader
		def iterdir(A):
			if not A._reader:return iter(())
			return iter(CompatibilityFiles.ChildPath(A._reader,B)for B in A._reader.contents())
		def is_file(A):return False
		is_dir=is_file
		def joinpath(A,other):
			B=other
			if not A._reader:return CompatibilityFiles.OrphanPath(B)
			return CompatibilityFiles.ChildPath(A._reader,B)
		@property
		def name(self):return self._spec.name
		def open(A,mode='r',*B,**C):return _io_wrapper(A._reader.open_resource(None),mode,*B,**C)
	class ChildPath(abc.Traversable):
		"\n        Path tied to a resource reader child.\n        Can be read but doesn't expose any meaningful children.\n        "
		def __init__(A,reader,name):A._reader=reader;A._name=name
		def iterdir(A):return iter(())
		def is_file(A):return A._reader.is_resource(A.name)
		def is_dir(A):return not A.is_file()
		def joinpath(A,other):return CompatibilityFiles.OrphanPath(A.name,other)
		@property
		def name(self):return self._name
		def open(A,mode='r',*B,**C):return _io_wrapper(A._reader.open_resource(A.name),mode,*B,**C)
	class OrphanPath(abc.Traversable):
		"\n        Orphan path, not tied to a module spec or resource reader.\n        Can't be read and doesn't expose any meaningful children.\n        "
		def __init__(B,*A):
			if len(A)<1:raise ValueError('Need at least one path part to construct a path')
			B._path=A
		def iterdir(A):return iter(())
		def is_file(A):return False
		is_dir=is_file
		def joinpath(A,other):return CompatibilityFiles.OrphanPath(*A._path,other)
		@property
		def name(self):return self._path[-1]
		def open(A,mode='r',*B,**C):raise FileNotFoundError("Can't open orphan path")
	def __init__(A,spec):A.spec=spec
	@property
	def _reader(self):
		with suppress(AttributeError):return self.spec.loader.get_resource_reader(self.spec.name)
	def _native(A):'\n        Return the native reader if it supports files().\n        ';B=A._reader;return B if hasattr(B,'files')else A
	def __getattr__(A,attr):return getattr(A._reader,attr)
	def files(A):return CompatibilityFiles.SpecPath(A.spec,A._reader)
def wrap_spec(package):'\n    Construct a package spec with traversable compatibility\n    on the spec/loader/reader.\n    ';return SpecLoaderAdapter(package.__spec__,TraversableResourcesLoader)