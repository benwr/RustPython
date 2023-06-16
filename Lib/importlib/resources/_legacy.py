_A='strict'
import functools,os,pathlib,types,warnings
from typing import Union,Iterable,ContextManager,BinaryIO,TextIO,Any
from.import _common
Package=Union[types.ModuleType,str]
Resource=str
def deprecated(func):
	A=func
	@functools.wraps(A)
	def B(*B,**C):warnings.warn(f"{A.__name__} is deprecated. Use files() instead. Refer to https://importlib-resources.readthedocs.io/en/latest/using.html#migrating-from-legacy for migration advice.",DeprecationWarning,stacklevel=2);return A(*B,**C)
	return B
def normalize_path(path):
	'Normalize a path by ensuring it is a string.\n\n    If the resulting string contains path separators, an exception is raised.\n    ';A=str(path);B,C=os.path.split(A)
	if B:raise ValueError(f"{path!r} must be only a file name")
	return C
@deprecated
def open_binary(package,resource):'Return a file-like object opened for binary reading of the resource.';return(_common.files(package)/normalize_path(resource)).open('rb')
@deprecated
def read_binary(package,resource):'Return the binary contents of the resource.';return(_common.files(package)/normalize_path(resource)).read_bytes()
@deprecated
def open_text(package,resource,encoding='utf-8',errors=_A):'Return a file-like object opened for text reading of the resource.';return(_common.files(package)/normalize_path(resource)).open('r',encoding=encoding,errors=errors)
@deprecated
def read_text(package,resource,encoding='utf-8',errors=_A):
	'Return the decoded string of the resource.\n\n    The decoding-related arguments have the same semantics as those of\n    bytes.decode().\n    '
	with open_text(package,resource,encoding,errors)as A:return A.read()
@deprecated
def contents(package):'Return an iterable of entries in `package`.\n\n    Note that not all entries are resources.  Specifically, directories are\n    not considered resources.  Use `is_resource()` on each entry returned here\n    to check if it is a resource or not.\n    ';return[A.name for A in _common.files(package).iterdir()]
@deprecated
def is_resource(package,name):'True if `name` is a resource inside `package`.\n\n    Directories are *not* resources.\n    ';B=normalize_path(name);return any(A.name==B and A.is_file()for A in _common.files(package).iterdir())
@deprecated
def path(package,resource):'A context manager providing a file path object to the resource.\n\n    If the resource does not already exist on its own on the file system,\n    a temporary file will be created. If the file was created, the file\n    will be deleted upon exiting the context manager (no exception is\n    raised if the file was deleted prior to the context manager\n    exiting).\n    ';return _common.as_file(_common.files(package)/normalize_path(resource))