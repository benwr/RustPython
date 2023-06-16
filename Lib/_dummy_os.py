'\nA shim of the os module containing only simple path-related utilities\n'
_B='__fspath__'
_A='os.path'
try:from os import*
except ImportError:
	import abc
	def __getattr__(name):raise OSError('no os specific module found')
	def _shim():import _dummy_os,sys;sys.modules['os']=_dummy_os;sys.modules[_A]=_dummy_os.path
	import posixpath as path;import sys;sys.modules[_A]=path;del sys;sep=path.sep
	def fspath(path):
		'Return the path representation of a path-like object.\n\n        If str or bytes is passed in, it is returned unchanged. Otherwise the\n        os.PathLike interface is used to get the path representation. If the\n        path representation is not str or bytes, TypeError is raised. If the\n        provided path is not str, bytes, or os.PathLike, TypeError is raised.\n        '
		if isinstance(path,(str,bytes)):return path
		path_type=type(path)
		try:path_repr=path_type.__fspath__(path)
		except AttributeError:
			if hasattr(path_type,_B):raise
			else:raise TypeError('expected str, bytes or os.PathLike object, not '+path_type.__name__)
		if isinstance(path_repr,(str,bytes)):return path_repr
		else:raise TypeError('expected {}.__fspath__() to return str or bytes, not {}'.format(path_type.__name__,type(path_repr).__name__))
	class PathLike(abc.ABC):
		'Abstract base class for implementing the file system path protocol.'
		@abc.abstractmethod
		def __fspath__(self):'Return the file system path representation of the object.';raise NotImplementedError
		@classmethod
		def __subclasshook__(cls,subclass):return hasattr(subclass,_B)