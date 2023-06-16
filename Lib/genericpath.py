'\nPath operations common to more than one OS\nDo not use directly.  The OS specific modules import the appropriate\nfunctions from this module themselves.\n'
_A=False
try:import os
except ImportError:import _dummy_os as os
import stat
__all__=['commonprefix','exists','getatime','getctime','getmtime','getsize','isdir','isfile','samefile','sameopenfile','samestat']
def exists(path):
	'Test whether a path exists.  Returns False for broken symbolic links'
	try:os.stat(path)
	except(OSError,ValueError):return _A
	return True
def isfile(path):
	'Test whether a path is a regular file'
	try:A=os.stat(path)
	except(OSError,ValueError):return _A
	return stat.S_ISREG(A.st_mode)
def isdir(s):
	'Return true if the pathname refers to an existing directory.'
	try:A=os.stat(s)
	except(OSError,ValueError):return _A
	return stat.S_ISDIR(A.st_mode)
def getsize(filename):'Return the size of a file, reported by os.stat().';return os.stat(filename).st_size
def getmtime(filename):'Return the last modification time of a file, reported by os.stat().';return os.stat(filename).st_mtime
def getatime(filename):'Return the last access time of a file, reported by os.stat().';return os.stat(filename).st_atime
def getctime(filename):'Return the metadata change time of a file, reported by os.stat().';return os.stat(filename).st_ctime
def commonprefix(m):
	'Given a list of pathnames, returns the longest common leading component'
	if not m:return''
	if not isinstance(m[0],(list,tuple)):m=tuple(map(os.fspath,m))
	A=min(m);C=max(m)
	for(B,D)in enumerate(A):
		if D!=C[B]:return A[:B]
	return A
def samestat(s1,s2):'Test whether two stat buffers reference the same file';return s1.st_ino==s2.st_ino and s1.st_dev==s2.st_dev
def samefile(f1,f2):'Test whether two pathnames reference the same actual file or directory\n\n    This is determined by the device number and i-node number and\n    raises an exception if an os.stat() call on either pathname fails.\n    ';A=os.stat(f1);B=os.stat(f2);return samestat(A,B)
def sameopenfile(fp1,fp2):'Test whether two open file objects reference the same file';A=os.fstat(fp1);B=os.fstat(fp2);return samestat(A,B)
def _splitext(p,sep,altsep,extsep):
	'Split the extension from a pathname.\n\n    Extension is everything from the last dot to the end, ignoring\n    leading dots.  Returns "(root, ext)"; ext may be empty.';D=extsep;E=altsep;A=p.rfind(sep)
	if E:F=p.rfind(E);A=max(A,F)
	B=p.rfind(D)
	if B>A:
		C=A+1
		while C<B:
			if p[C:C+1]!=D:return p[:B],p[B:]
			C+=1
	return p,p[:0]
def _check_arg_types(funcname,*D):
	B=C=_A
	for A in D:
		if isinstance(A,str):B=True
		elif isinstance(A,bytes):C=True
		else:raise TypeError(f"{funcname}() argument must be str, bytes, or os.PathLike object, not {A.__class__.__name__!r}")from None
	if B and C:raise TypeError("Can't mix strings and bytes in path components")from None