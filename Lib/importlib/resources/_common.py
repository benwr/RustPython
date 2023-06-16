import os,pathlib,tempfile,functools,contextlib,types,importlib
from typing import Union,Optional
from.abc import ResourceReader,Traversable
from._adapters import wrap_spec
Package=Union[types.ModuleType,str]
def files(package):'\n    Get a Traversable resource from a package\n    ';return from_package(get_package(package))
def get_resource_reader(package):
	"\n    Return the package's loader if it's a ResourceReader.\n    ";A=package.__spec__;B=getattr(A.loader,'get_resource_reader',None)
	if B is None:return
	return B(A.name)
def resolve(cand):A=cand;return A if isinstance(A,types.ModuleType)else importlib.import_module(A)
def get_package(package):
	'Take a package name or module object and return the module.\n\n    Raise an exception if the resolved module is not a package.\n    ';A=package;B=resolve(A)
	if wrap_spec(B).submodule_search_locations is None:raise TypeError(f"{A!r} is not a package")
	return B
def from_package(package):'\n    Return a Traversable object for the given package.\n\n    ';A=wrap_spec(package);B=A.loader.get_resource_reader(A.name);return B.files()
@contextlib.contextmanager
def _tempfile(reader,suffix='',*,_os_remove=os.remove):
	A=reader;B,C=tempfile.mkstemp(suffix=suffix)
	try:
		try:os.write(B,A())
		finally:os.close(B)
		del A;yield pathlib.Path(C)
	finally:
		try:_os_remove(C)
		except FileNotFoundError:pass
@functools.singledispatch
def as_file(path):'\n    Given a Traversable object, return that object as a\n    path on the local file system in a context manager.\n    ';return _tempfile(path.read_bytes,suffix=path.name)
@as_file.register(pathlib.Path)
@contextlib.contextmanager
def _(path):'\n    Degenerate behavior for pathlib.Path objects.\n    ';yield path