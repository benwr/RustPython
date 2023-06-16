"Module/script to byte-compile all .py files to .pyc files.\n\nWhen called as a script with arguments, this compiles the directories\ngiven as arguments recursively; the -l option prevents it from\nrecursing into directories.\n\nWithout arguments, if compiles all modules on sys.path, without\nrecursing into subdirectories.  (Even though it should do so for\npackages -- for now, you'll have to deal with packages separately.)\n\nSee module py_compile for details of the actual byte-compilation.\n"
_C=True
_B=False
_A=None
import os,sys,importlib.util,py_compile,struct
try:from concurrent.futures import ProcessPoolExecutor
except ImportError:ProcessPoolExecutor=_A
from functools import partial
__all__=['compile_dir','compile_file','compile_path']
def _walk_dir(dir,ddir=_A,maxlevels=10,quiet=0):
	E=maxlevels;C=quiet
	if C<2 and isinstance(dir,os.PathLike):dir=os.fspath(dir)
	if not C:print('Listing {!r}...'.format(dir))
	try:D=os.listdir(dir)
	except OSError:
		if C<2:print("Can't list {!r}".format(dir))
		D=[]
	D.sort()
	for A in D:
		if A=='__pycache__':continue
		B=os.path.join(dir,A)
		if ddir is not _A:F=os.path.join(ddir,A)
		else:F=_A
		if not os.path.isdir(B):yield B
		elif E>0 and A!=os.curdir and A!=os.pardir and os.path.isdir(B)and not os.path.islink(B):yield from _walk_dir(B,ddir=F,maxlevels=E-1,quiet=C)
def compile_dir(dir,maxlevels=10,ddir=_A,force=_B,rx=_A,quiet=0,legacy=_B,optimize=-1,workers=1):
	'Byte-compile all modules in the given directory tree.\n\n    Arguments (only dir is required):\n\n    dir:       the directory to byte-compile\n    maxlevels: maximum recursion level (default 10)\n    ddir:      the directory that will be prepended to the path to the\n               file as it is compiled into each byte-code file.\n    force:     if True, force compilation, even if timestamps are up-to-date\n    quiet:     full output with False or 0, errors only with 1,\n               no output with 2\n    legacy:    if True, produce legacy pyc paths instead of PEP 3147 paths\n    optimize:  optimization level or -1 for level of the interpreter\n    workers:   maximum number of parallel workers\n    ';E=optimize;F=legacy;G=force;B=quiet;C=ddir;A=workers
	if A is not _A and A<0:raise ValueError('workers must be greater or equal to 0')
	H=_walk_dir(dir,quiet=B,maxlevels=maxlevels,ddir=C);D=_C
	if A is not _A and A!=1 and ProcessPoolExecutor is not _A:
		A=A or _A
		with ProcessPoolExecutor(max_workers=A)as I:J=I.map(partial(compile_file,ddir=C,force=G,rx=rx,quiet=B,legacy=F,optimize=E),H);D=min(J,default=_C)
	else:
		for K in H:
			if not compile_file(K,C,G,rx,B,F,E):D=_B
	return D
def compile_file(fullname,ddir=_A,force=_B,rx=_A,quiet=0,legacy=_B,optimize=-1):
	'Byte-compile one file.\n\n    Arguments (only fullname is required):\n\n    fullname:  the file to byte-compile\n    ddir:      if given, the directory name compiled in to the\n               byte-code file.\n    force:     if True, force compilation, even if timestamps are up-to-date\n    quiet:     full output with False or 0, errors only with 1,\n               no output with 2\n    legacy:    if True, produce legacy pyc paths instead of PEP 3147 paths\n    optimize:  optimization level or -1 for level of the interpreter\n    ';H='*** ';I='*** Error compiling {!r}...';E=optimize;C=quiet;A=fullname;B=_C
	if C<2 and isinstance(A,os.PathLike):A=os.fspath(A)
	F=os.path.basename(A)
	if ddir is not _A:J=os.path.join(ddir,F)
	else:J=_A
	if rx is not _A:
		L=rx.search(A)
		if L:return B
	if os.path.isfile(A):
		if legacy:D=A+'c'
		else:
			if E>=0:M=E if E>=1 else'';D=importlib.util.cache_from_source(A,optimization=M)
			else:D=importlib.util.cache_from_source(A)
			U=os.path.dirname(D)
		V,N=F[:-3],F[-3:]
		if N=='.py':
			if not force:
				try:
					O=int(os.stat(A).st_mtime);P=struct.pack('<4sl',importlib.util.MAGIC_NUMBER,O)
					with open(D,'rb')as Q:R=Q.read(8)
					if P==R:return B
				except OSError:pass
			if not C:print('Compiling {!r}...'.format(A))
			try:S=py_compile.compile(A,D,J,_C,optimize=E)
			except py_compile.PyCompileError as T:
				B=_B
				if C>=2:return B
				elif C:print(I.format(A))
				else:print(H,end='')
				G=T.msg.encode(sys.stdout.encoding,errors='backslashreplace');G=G.decode(sys.stdout.encoding);print(G)
			except(SyntaxError,UnicodeError,OSError)as K:
				B=_B
				if C>=2:return B
				elif C:print(I.format(A))
				else:print(H,end='')
				print(K.__class__.__name__+':',K)
			else:
				if S==0:B=_B
	return B
def compile_path(skip_curdir=1,maxlevels=0,force=_B,quiet=0,legacy=_B,optimize=-1):
	'Byte-compile all module on sys.path.\n\n    Arguments (all optional):\n\n    skip_curdir: if true, skip current directory (default True)\n    maxlevels:   max recursion level (default 0)\n    force: as for compile_dir() (default False)\n    quiet: as for compile_dir() (default 0)\n    legacy: as for compile_dir() (default False)\n    optimize: as for compile_dir() (default -1)\n    ';B=quiet;A=_C
	for dir in sys.path:
		if(not dir or dir==os.curdir)and skip_curdir:
			if B<2:print('Skipping current directory')
		else:A=A and compile_dir(dir,maxlevels,_A,force,quiet=B,legacy=legacy,optimize=optimize)
	return A
def main():
	'Script main program.';F='store_true';import argparse as H;B=H.ArgumentParser(description='Utilities to support installing Python libraries.');B.add_argument('-l',action='store_const',const=0,default=10,dest='maxlevels',help="don't recurse into subdirectories");B.add_argument('-r',type=int,dest='recursion',help='control the maximum recursion level. if `-l` and `-r` options are specified, then `-r` takes precedence.');B.add_argument('-f',action=F,dest='force',help='force rebuild even if timestamps are up to date');B.add_argument('-q',action='count',dest='quiet',default=0,help='output only error messages; -qq will suppress the error messages as well.');B.add_argument('-b',action=F,dest='legacy',help='use legacy (pre-PEP3147) compiled file locations');B.add_argument('-d',metavar='DESTDIR',dest='ddir',default=_A,help='directory to prepend to file paths for use in compile-time tracebacks and in runtime tracebacks in cases where the source file is unavailable');B.add_argument('-x',metavar='REGEXP',dest='rx',default=_A,help='skip files matching the regular expression; the regexp is searched for in the full path of each file considered for compilation');B.add_argument('-i',metavar='FILE',dest='flist',help='add all the files and directories listed in FILE to the list considered for compilation; if "-", names are read from stdin');B.add_argument('compile_dest',metavar='FILE|DIR',nargs='*',help='zero or more file and directory names to compile; if no arguments given, defaults to the equivalent of -l sys.path');B.add_argument('-j','--workers',default=1,type=int,help='Run compileall concurrently');A=B.parse_args();C=A.compile_dest
	if A.rx:import re;A.rx=re.compile(A.rx)
	if A.recursion is not _A:G=A.recursion
	else:G=A.maxlevels
	if A.flist:
		try:
			with sys.stdin if A.flist=='-'else open(A.flist)as I:
				for J in I:C.append(J.strip())
		except OSError:
			if A.quiet<2:print('Error reading file list {}'.format(A.flist))
			return _B
	if A.workers is not _A:A.workers=A.workers or _A
	D=_C
	try:
		if C:
			for E in C:
				if os.path.isfile(E):
					if not compile_file(E,A.ddir,A.force,A.rx,A.quiet,A.legacy):D=_B
				elif not compile_dir(E,G,A.ddir,A.force,A.rx,A.quiet,A.legacy,workers=A.workers):D=_B
			return D
		else:return compile_path(legacy=A.legacy,force=A.force,quiet=A.quiet)
	except KeyboardInterrupt:
		if A.quiet<2:print('\n[interrupted]')
		return _B
	return _C
if __name__=='__main__':exit_status=int(not main());sys.exit(exit_status)