'Filename globbing utility.'
_B=False
_A=None
import contextlib,os,re,fnmatch,itertools,stat,sys
__all__=['glob','iglob','escape']
def glob(pathname,*,root_dir=_A,dir_fd=_A,recursive=_B,include_hidden=_B):"Return a list of paths matching a pathname pattern.\n\n    The pattern may contain simple shell-style wildcards a la\n    fnmatch. Unlike fnmatch, filenames starting with a\n    dot are special cases that are not matched by '*' and '?'\n    patterns by default.\n\n    If `include_hidden` is true, the patterns '*', '?', '**'  will match hidden\n    directories.\n\n    If `recursive` is true, the pattern '**' will match any files and\n    zero or more directories and subdirectories.\n    ";return list(iglob(pathname,root_dir=root_dir,dir_fd=dir_fd,recursive=recursive,include_hidden=include_hidden))
def iglob(pathname,*,root_dir=_A,dir_fd=_A,recursive=_B,include_hidden=_B):
	"Return an iterator which yields the paths matching a pathname pattern.\n\n    The pattern may contain simple shell-style wildcards a la\n    fnmatch. However, unlike fnmatch, filenames starting with a\n    dot are special cases that are not matched by '*' and '?'\n    patterns.\n\n    If recursive is true, the pattern '**' will match any files and\n    zero or more directories and subdirectories.\n    ";E=dir_fd;C=recursive;A=root_dir;B=pathname;sys.audit('glob.glob',B,C);sys.audit('glob.glob/2',B,C,A,E)
	if A is not _A:A=os.fspath(A)
	else:A=B[:0]
	D=_iglob(B,A,E,C,_B,include_hidden=include_hidden)
	if not B or C and _isrecursive(B[:2]):
		try:
			F=next(D)
			if F:D=itertools.chain((F,),D)
		except StopIteration:pass
	return D
def _iglob(pathname,root_dir,dir_fd,recursive,dironly,include_hidden=_B):
	H=recursive;F=include_hidden;G=dironly;C=dir_fd;D=root_dir;E=pathname;A,B=os.path.split(E)
	if not has_magic(E):
		assert not G
		if B:
			if _lexists(_join(D,E),C):yield E
		elif _isdir(_join(D,A),C):yield E
		return
	if not A:
		if H and _isrecursive(B):yield from _glob2(D,B,C,G,include_hidden=F)
		else:yield from _glob1(D,B,C,G,include_hidden=F)
		return
	if A!=E and has_magic(A):J=_iglob(A,D,C,H,True,include_hidden=F)
	else:J=[A]
	if has_magic(B):
		if H and _isrecursive(B):I=_glob2
		else:I=_glob1
	else:I=_glob0
	for A in J:
		for K in I(_join(D,A),B,C,G,include_hidden=F):yield os.path.join(A,K)
def _glob1(dirname,pattern,dir_fd,dironly,include_hidden=_B):
	B=include_hidden;C=pattern;A=_listdir(dirname,dir_fd,dironly)
	if B or not _ishidden(C):A=(A for A in A if B or not _ishidden(A))
	return fnmatch.filter(A,C)
def _glob0(dirname,basename,dir_fd,dironly,include_hidden=_B):
	B=dir_fd;C=dirname;A=basename
	if A:
		if _lexists(_join(C,A),B):return[A]
	elif _isdir(C,B):return[A]
	return[]
def glob0(dirname,pattern):return _glob0(dirname,pattern,_A,_B)
def glob1(dirname,pattern):return _glob1(dirname,pattern,_A,_B)
def _glob2(dirname,pattern,dir_fd,dironly,include_hidden=_B):A=pattern;assert _isrecursive(A);yield A[:0];yield from _rlistdir(dirname,dir_fd,dironly,include_hidden=include_hidden)
def _iterdir(dirname,dir_fd,dironly):
	C=dir_fd;A=dirname
	try:
		D=_A;E=_A
		if C is not _A:
			if A:D=B=os.open(A,_dir_open_flags,dir_fd=C)
			else:B=C
			if isinstance(A,bytes):E=os.fsencode
		elif A:B=A
		elif isinstance(A,bytes):B=bytes(os.curdir,'ASCII')
		else:B=os.curdir
		try:
			with os.scandir(B)as G:
				for F in G:
					try:
						if not dironly or F.is_dir():
							if E is not _A:yield E(F.name)
							else:yield F.name
					except OSError:pass
		finally:
			if D is not _A:os.close(D)
	except OSError:return
def _listdir(dirname,dir_fd,dironly):
	with contextlib.closing(_iterdir(dirname,dir_fd,dironly))as A:return list(A)
def _rlistdir(dirname,dir_fd,dironly,include_hidden=_B):
	C=include_hidden;D=dironly;E=dir_fd;B=dirname;F=_listdir(B,E,D)
	for A in F:
		if C or not _ishidden(A):
			yield A;G=_join(B,A)if B else A
			for H in _rlistdir(G,E,D,include_hidden=C):yield _join(A,H)
def _lexists(pathname,dir_fd):
	A=dir_fd;B=pathname
	if A is _A:return os.path.lexists(B)
	try:os.lstat(B,dir_fd=A)
	except(OSError,ValueError):return _B
	else:return True
def _isdir(pathname,dir_fd):
	A=dir_fd;B=pathname
	if A is _A:return os.path.isdir(B)
	try:C=os.stat(B,dir_fd=A)
	except(OSError,ValueError):return _B
	else:return stat.S_ISDIR(C.st_mode)
def _join(dirname,basename):
	A=basename;B=dirname
	if not B or not A:return B or A
	return os.path.join(B,A)
magic_check=re.compile('([*?[])')
magic_check_bytes=re.compile(b'([*?[])')
def has_magic(s):
	if isinstance(s,bytes):A=magic_check_bytes.search(s)
	else:A=magic_check.search(s)
	return A is not _A
def _ishidden(path):return path[0]in('.',b'.'[0])
def _isrecursive(pattern):
	A=pattern
	if isinstance(A,bytes):return A==b'**'
	else:return A=='**'
def escape(pathname):
	'Escape all special characters.\n    ';A=pathname;B,A=os.path.splitdrive(A)
	if isinstance(A,bytes):A=magic_check_bytes.sub(b'[\\1]',A)
	else:A=magic_check.sub('[\\1]',A)
	return B+A
_dir_open_flags=os.O_RDONLY|getattr(os,'O_DIRECTORY',0)