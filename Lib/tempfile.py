"Temporary files.\n\nThis module provides generic, low- and high-level interfaces for\ncreating temporary files and directories.  All of the interfaces\nprovided by this module can be used without fear of race conditions\nexcept for 'mktemp'.  'mktemp' is subject to race conditions and\nshould not be used; it is provided for backward compatibility only.\n\nThe default path names are returned as str.  If you supply bytes as\ninput, all return values will be in bytes.  Ex:\n\n    >>> tempfile.mkstemp()\n    (4, '/tmp/tmptpu9nin8')\n    >>> tempfile.mkdtemp(suffix=b'')\n    b'/tmp/tmppbi8f0hy'\n\nThis module also provides some data items to the user:\n\n  TMP_MAX  - maximum number of names that will be tried before\n             giving up.\n  tempdir  - If this is set to a string before the first use of\n             any routine from this module, it will be considered as\n             another candidate location to store temporary files.\n"
_F='TMP_MAX'
_E='w+b'
_D='nt'
_C=True
_B=False
_A=None
__all__=['NamedTemporaryFile','TemporaryFile','SpooledTemporaryFile','TemporaryDirectory','mkstemp','mkdtemp','mktemp',_F,'gettempprefix','tempdir','gettempdir','gettempprefixb','gettempdirb']
import functools as _functools,warnings as _warnings,io as _io,os as _os,shutil as _shutil,errno as _errno
from random import Random as _Random
import sys as _sys,types as _types,weakref as _weakref,_thread
_allocate_lock=_thread.allocate_lock
_text_openflags=_os.O_RDWR|_os.O_CREAT|_os.O_EXCL
if hasattr(_os,'O_NOFOLLOW'):_text_openflags|=_os.O_NOFOLLOW
_bin_openflags=_text_openflags
if hasattr(_os,'O_BINARY'):_bin_openflags|=_os.O_BINARY
if hasattr(_os,_F):TMP_MAX=_os.TMP_MAX
else:TMP_MAX=10000
template='tmp'
_once_lock=_allocate_lock()
def _exists(fn):
	try:_os.lstat(fn)
	except OSError:return _B
	else:return _C
def _infer_return_type(*D):
	'Look at the type of all args and divine their implied return type.';C="Can't mix bytes and non-bytes in path components.";A=_A
	for B in D:
		if B is _A:continue
		if isinstance(B,_os.PathLike):B=_os.fspath(B)
		if isinstance(B,bytes):
			if A is str:raise TypeError(C)
			A=bytes
		else:
			if A is bytes:raise TypeError(C)
			A=str
	if A is _A:
		if tempdir is _A or isinstance(tempdir,str):return str
		else:return bytes
	return A
def _sanitize_params(prefix,suffix,dir):
	'Common parameter processing for most APIs in this module.';B=suffix;A=prefix;C=_infer_return_type(A,B,dir)
	if B is _A:B=C()
	if A is _A:
		if C is str:A=template
		else:A=_os.fsencode(template)
	if dir is _A:
		if C is str:dir=gettempdir()
		else:dir=gettempdirb()
	return A,B,dir,C
class _RandomNameSequence:
	'An instance of _RandomNameSequence generates an endless\n    sequence of unpredictable strings which can safely be incorporated\n    into file names.  Each string is eight characters long.  Multiple\n    threads can safely use the same instance at the same time.\n\n    _RandomNameSequence is an iterator.';characters='abcdefghijklmnopqrstuvwxyz0123456789_'
	@property
	def rng(self):
		A=self;B=_os.getpid()
		if B!=getattr(A,'_rng_pid',_A):A._rng=_Random();A._rng_pid=B
		return A._rng
	def __iter__(A):return A
	def __next__(A):return''.join(A.rng.choices(A.characters,k=8))
def _candidate_tempdir_list():
	'Generate a list of candidate temporary directories which\n    _get_default_tempdir will try.';A=[]
	for C in('TMPDIR','TEMP','TMP'):
		B=_os.getenv(C)
		if B:A.append(B)
	if _os.name==_D:A.extend([_os.path.expanduser('~\\AppData\\Local\\Temp'),_os.path.expandvars('%SYSTEMROOT%\\Temp'),'c:\\temp','c:\\tmp','\\temp','\\tmp'])
	else:A.extend(['/tmp','/var/tmp','/usr/tmp'])
	try:A.append(_os.getcwd())
	except(AttributeError,OSError):A.append(_os.curdir)
	return A
def _get_default_tempdir():
	'Calculate the default directory to use for temporary files.\n    This routine should be called exactly once.\n\n    We determine whether or not a candidate temp dir is usable by\n    trying to create and write to a file in that directory.  If this\n    is successful, the test file is deleted.  To prevent denial of\n    service, the name of the test file must be randomized.';D=_RandomNameSequence();A=_candidate_tempdir_list()
	for dir in A:
		if dir!=_os.curdir:dir=_os.path.abspath(dir)
		for G in range(100):
			E=next(D);B=_os.path.join(dir,E)
			try:
				C=_os.open(B,_bin_openflags,384)
				try:
					try:
						with _io.open(C,'wb',closefd=_B)as F:F.write(b'blat')
					finally:_os.close(C)
				finally:_os.unlink(B)
				return dir
			except FileExistsError:pass
			except PermissionError:
				if _os.name==_D and _os.path.isdir(dir)and _os.access(dir,_os.W_OK):continue
				break
			except OSError:break
	raise FileNotFoundError(_errno.ENOENT,'No usable temporary directory found in %s'%A)
_name_sequence=_A
def _get_candidate_names():
	'Common setup sequence for all user-callable interfaces.';global _name_sequence
	if _name_sequence is _A:
		_once_lock.acquire()
		try:
			if _name_sequence is _A:_name_sequence=_RandomNameSequence()
		finally:_once_lock.release()
	return _name_sequence
def _mkstemp_inner(dir,pre,suf,flags,output_type):
	'Code common to mkstemp, TemporaryFile, and NamedTemporaryFile.';A=_get_candidate_names()
	if output_type is bytes:A=map(_os.fsencode,A)
	for E in range(TMP_MAX):
		C=next(A);B=_os.path.join(dir,pre+C+suf);_sys.audit('tempfile.mkstemp',B)
		try:D=_os.open(B,flags,384)
		except FileExistsError:continue
		except PermissionError:
			if _os.name==_D and _os.path.isdir(dir)and _os.access(dir,_os.W_OK):continue
			else:raise
		return D,_os.path.abspath(B)
	raise FileExistsError(_errno.EEXIST,'No usable temporary file name found')
def gettempprefix():'The default prefix for temporary directories as string.';return _os.fsdecode(template)
def gettempprefixb():'The default prefix for temporary directories as bytes.';return _os.fsencode(template)
tempdir=_A
def _gettempdir():
	'Private accessor for tempfile.tempdir.';global tempdir
	if tempdir is _A:
		_once_lock.acquire()
		try:
			if tempdir is _A:tempdir=_get_default_tempdir()
		finally:_once_lock.release()
	return tempdir
def gettempdir():'Returns tempfile.tempdir as str.';return _os.fsdecode(_gettempdir())
def gettempdirb():'Returns tempfile.tempdir as bytes.';return _os.fsencode(_gettempdir())
def mkstemp(suffix=_A,prefix=_A,dir=_A,text=_B):
	"User-callable function to create and return a unique temporary\n    file.  The return value is a pair (fd, name) where fd is the\n    file descriptor returned by os.open, and name is the filename.\n\n    If 'suffix' is not None, the file name will end with that suffix,\n    otherwise there will be no suffix.\n\n    If 'prefix' is not None, the file name will begin with that prefix,\n    otherwise a default prefix is used.\n\n    If 'dir' is not None, the file will be created in that directory,\n    otherwise a default directory is used.\n\n    If 'text' is specified and true, the file is opened in text\n    mode.  Else (the default) the file is opened in binary mode.\n\n    If any of 'suffix', 'prefix' and 'dir' are not None, they must be the\n    same type.  If they are bytes, the returned name will be bytes; str\n    otherwise.\n\n    The file is readable and writable only by the creating user ID.\n    If the operating system uses permission bits to indicate whether a\n    file is executable, the file is executable by no one. The file\n    descriptor is not inherited by children of this process.\n\n    Caller is responsible for deleting the file when done with it.\n    ";A=prefix;B=suffix;A,B,dir,D=_sanitize_params(A,B,dir)
	if text:C=_text_openflags
	else:C=_bin_openflags
	return _mkstemp_inner(dir,A,B,C,D)
def mkdtemp(suffix=_A,prefix=_A,dir=_A):
	"User-callable function to create and return a unique temporary\n    directory.  The return value is the pathname of the directory.\n\n    Arguments are as for mkstemp, except that the 'text' argument is\n    not accepted.\n\n    The directory is readable, writable, and searchable only by the\n    creating user.\n\n    Caller is responsible for deleting the directory when done with it.\n    ";A=prefix;B=suffix;A,B,dir,E=_sanitize_params(A,B,dir);C=_get_candidate_names()
	if E is bytes:C=map(_os.fsencode,C)
	for G in range(TMP_MAX):
		F=next(C);D=_os.path.join(dir,A+F+B);_sys.audit('tempfile.mkdtemp',D)
		try:_os.mkdir(D,448)
		except FileExistsError:continue
		except PermissionError:
			if _os.name==_D and _os.path.isdir(dir)and _os.access(dir,_os.W_OK):continue
			else:raise
		return D
	raise FileExistsError(_errno.EEXIST,'No usable temporary directory name found')
def mktemp(suffix='',prefix=template,dir=_A):
	"User-callable function to return a unique temporary file name.  The\n    file is not created.\n\n    Arguments are similar to mkstemp, except that the 'text' argument is\n    not accepted, and suffix=None, prefix=None and bytes file names are not\n    supported.\n\n    THIS FUNCTION IS UNSAFE AND SHOULD NOT BE USED.  The file name may\n    refer to a file that did not exist at some point, but by the time\n    you get around to creating it, someone else may have beaten you to\n    the punch.\n    "
	if dir is _A:dir=gettempdir()
	B=_get_candidate_names()
	for D in range(TMP_MAX):
		C=next(B);A=_os.path.join(dir,prefix+C+suffix)
		if not _exists(A):return A
	raise FileExistsError(_errno.EEXIST,'No usable temporary filename found')
class _TemporaryFileCloser:
	"A separate object allowing proper closing of a temporary file's\n    underlying file object, without adding a __del__ method to the\n    temporary file.";file=_A;close_called=_B
	def __init__(A,file,name,delete=_C):A.file=file;A.name=name;A.delete=delete
	if _os.name!=_D:
		def close(A,unlink=_os.unlink):
			if not A.close_called and A.file is not _A:
				A.close_called=_C
				try:A.file.close()
				finally:
					if A.delete:unlink(A.name)
		def __del__(A):A.close()
	else:
		def close(A):
			if not A.close_called:A.close_called=_C;A.file.close()
class _TemporaryFileWrapper:
	'Temporary file wrapper\n\n    This class provides a wrapper around files opened for\n    temporary use.  In particular, it seeks to automatically\n    remove the file when it is no longer needed.\n    '
	def __init__(A,file,name,delete=_C):B=delete;A.file=file;A.name=name;A.delete=B;A._closer=_TemporaryFileCloser(file,name,B)
	def __getattr__(B,name):
		E=B.__dict__['file'];A=getattr(E,name)
		if hasattr(A,'__call__'):
			C=A
			@_functools.wraps(C)
			def D(*A,**B):return C(*A,**B)
			D._closer=B._closer;A=D
		if not isinstance(A,int):setattr(B,name,A)
		return A
	def __enter__(A):A.file.__enter__();return A
	def __exit__(A,exc,value,tb):B=A.file.__exit__(exc,value,tb);A.close();return B
	def close(A):'\n        Close the temporary file, possibly deleting it.\n        ';A._closer.close()
	def __iter__(A):
		for B in A.file:yield B
def NamedTemporaryFile(mode=_E,buffering=-1,encoding=_A,newline=_A,suffix=_A,prefix=_A,dir=_A,delete=_C,*,errors=_A):
	'Create and return a temporary file.\n    Arguments:\n    \'prefix\', \'suffix\', \'dir\' -- as for mkstemp.\n    \'mode\' -- the mode argument to io.open (default "w+b").\n    \'buffering\' -- the buffer size argument to io.open (default -1).\n    \'encoding\' -- the encoding argument to io.open (default None)\n    \'newline\' -- the newline argument to io.open (default None)\n    \'delete\' -- whether the file is deleted on close (default True).\n    \'errors\' -- the errors argument to io.open (default None)\n    The file is created as mkstemp() would do it.\n\n    Returns an object with a file-like interface; the name of the file\n    is accessible as its \'name\' attribute.  The file will be automatically\n    deleted when it is closed unless the \'delete\' argument is set to False.\n    ';D=delete;A=prefix;B=suffix;C=encoding;A,B,dir,H=_sanitize_params(A,B,dir);E=_bin_openflags
	if _os.name==_D and D:E|=_os.O_TEMPORARY
	if'b'not in mode:C=_io.text_encoding(C)
	F,G=_mkstemp_inner(dir,A,B,E,H)
	try:I=_io.open(F,mode,buffering=buffering,newline=newline,encoding=C,errors=errors);return _TemporaryFileWrapper(I,G,D)
	except BaseException:_os.unlink(G);_os.close(F);raise
if _os.name!='posix'or _sys.platform=='cygwin':TemporaryFile=NamedTemporaryFile
else:
	_O_TMPFILE_WORKS=hasattr(_os,'O_TMPFILE')
	def TemporaryFile(mode=_E,buffering=-1,encoding=_A,newline=_A,suffix=_A,prefix=_A,dir=_A,*,errors=_A):
		'Create and return a temporary file.\n        Arguments:\n        \'prefix\', \'suffix\', \'dir\' -- as for mkstemp.\n        \'mode\' -- the mode argument to io.open (default "w+b").\n        \'buffering\' -- the buffer size argument to io.open (default -1).\n        \'encoding\' -- the encoding argument to io.open (default None)\n        \'newline\' -- the newline argument to io.open (default None)\n        \'errors\' -- the errors argument to io.open (default None)\n        The file is created as mkstemp() would do it.\n\n        Returns an object with a file-like interface.  The file has no\n        name, and will cease to exist when it is closed.\n        ';F=errors;G=newline;H=buffering;C=prefix;D=suffix;E=mode;B=encoding;global _O_TMPFILE_WORKS
		if'b'not in E:B=_io.text_encoding(B)
		C,D,dir,J=_sanitize_params(C,D,dir);I=_bin_openflags
		if _O_TMPFILE_WORKS:
			try:K=(I|_os.O_TMPFILE)&~_os.O_CREAT;A=_os.open(dir,K,384)
			except IsADirectoryError:_O_TMPFILE_WORKS=_B
			except OSError:pass
			else:
				try:return _io.open(A,E,buffering=H,newline=G,encoding=B,errors=F)
				except:_os.close(A);raise
		A,L=_mkstemp_inner(dir,C,D,I,J)
		try:_os.unlink(L);return _io.open(A,E,buffering=H,newline=G,encoding=B,errors=F)
		except:_os.close(A);raise
class SpooledTemporaryFile:
	'Temporary file wrapper, specialized to switch from BytesIO\n    or StringIO to a real file when it exceeds a certain size or\n    when a fileno is needed.\n    ';_rolled=_B
	def __init__(A,max_size=0,mode=_E,buffering=-1,encoding=_A,newline=_A,suffix=_A,prefix=_A,dir=_A,*,errors=_A):
		C=errors;D=newline;B=encoding
		if'b'in mode:A._file=_io.BytesIO()
		else:B=_io.text_encoding(B);A._file=_io.TextIOWrapper(_io.BytesIO(),encoding=B,errors=C,newline=D)
		A._max_size=max_size;A._rolled=_B;A._TemporaryFileArgs={'mode':mode,'buffering':buffering,'suffix':suffix,'prefix':prefix,'encoding':B,'newline':D,'dir':dir,'errors':C}
	__class_getitem__=classmethod(_types.GenericAlias)
	def _check(A,file):
		if A._rolled:return
		B=A._max_size
		if B and file.tell()>B:A.rollover()
	def rollover(A):
		if A._rolled:return
		C=A._file;B=A._file=TemporaryFile(**A._TemporaryFileArgs);del A._TemporaryFileArgs;D=C.tell()
		if hasattr(B,'buffer'):B.buffer.write(C.detach().getvalue())
		else:B.write(C.getvalue())
		B.seek(D,0);A._rolled=_C
	def __enter__(A):
		if A._file.closed:raise ValueError('Cannot enter context with closed file')
		return A
	def __exit__(A,exc,value,tb):A._file.close()
	def __iter__(A):return A._file.__iter__()
	def close(A):A._file.close()
	@property
	def closed(self):return self._file.closed
	@property
	def encoding(self):return self._file.encoding
	@property
	def errors(self):return self._file.errors
	def fileno(A):A.rollover();return A._file.fileno()
	def flush(A):A._file.flush()
	def isatty(A):return A._file.isatty()
	@property
	def mode(self):
		try:return self._file.mode
		except AttributeError:return self._TemporaryFileArgs['mode']
	@property
	def name(self):
		try:return self._file.name
		except AttributeError:return
	@property
	def newlines(self):return self._file.newlines
	def read(A,*B):return A._file.read(*B)
	def readline(A,*B):return A._file.readline(*B)
	def readlines(A,*B):return A._file.readlines(*B)
	def seek(A,*B):return A._file.seek(*B)
	def tell(A):return A._file.tell()
	def truncate(A,size=_A):
		B=size
		if B is _A:A._file.truncate()
		else:
			if B>A._max_size:A.rollover()
			A._file.truncate(B)
	def write(A,s):B=A._file;C=B.write(s);A._check(B);return C
	def writelines(A,iterable):B=A._file;C=B.writelines(iterable);A._check(B);return C
class TemporaryDirectory:
	'Create and return a temporary directory.  This has the same\n    behavior as mkdtemp but can be used as a context manager.  For\n    example:\n\n        with TemporaryDirectory() as tmpdir:\n            ...\n\n    Upon exiting the context, the directory and everything contained\n    in it are removed.\n    '
	def __init__(A,suffix=_A,prefix=_A,dir=_A,ignore_cleanup_errors=_B):A.name=mkdtemp(suffix,prefix,dir);A._ignore_cleanup_errors=ignore_cleanup_errors;A._finalizer=_weakref.finalize(A,A._cleanup,A.name,warn_message='Implicitly cleaning up {!r}'.format(A),ignore_errors=A._ignore_cleanup_errors)
	@classmethod
	def _rmtree(E,name,ignore_errors=_B):
		B=ignore_errors
		def A(func,path,exc_info):
			C=exc_info;A=path
			if issubclass(C[0],PermissionError):
				def D(path):
					try:_os.chflags(path,0)
					except AttributeError:pass
					_os.chmod(path,448)
				try:
					if A!=name:D(_os.path.dirname(A))
					D(A)
					try:_os.unlink(A)
					except(IsADirectoryError,PermissionError):E._rmtree(A,ignore_errors=B)
				except FileNotFoundError:pass
			elif issubclass(C[0],FileNotFoundError):0
			elif not B:raise
		_shutil.rmtree(name,onerror=A)
	@classmethod
	def _cleanup(A,name,warn_message,ignore_errors=_B):A._rmtree(name,ignore_errors=ignore_errors);_warnings.warn(warn_message,ResourceWarning)
	def __repr__(A):return'<{} {!r}>'.format(A.__class__.__name__,A.name)
	def __enter__(A):return A.name
	def __exit__(A,exc,value,tb):A.cleanup()
	def cleanup(A):
		if A._finalizer.detach()or _os.path.exists(A.name):A._rmtree(A.name,ignore_errors=A._ignore_cleanup_errors)
	__class_getitem__=classmethod(_types.GenericAlias)