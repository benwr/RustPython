'Utilities for comparing files and directories.\n\nClasses:\n    dircmp\n\nFunctions:\n    cmp(f1, f2, shallow=True) -> int\n    cmpfiles(a, b, common) -> ([], [], [])\n    clear_cache()\n\n'
_C=False
_B=True
_A=None
try:import os
except ImportError:import _dummy_os as os
import stat
from itertools import filterfalse
from types import GenericAlias
__all__=['clear_cache','cmp','dircmp','cmpfiles','DEFAULT_IGNORES']
_cache={}
BUFSIZE=8*1024
DEFAULT_IGNORES=['RCS','CVS','tags','.git','.hg','.bzr','_darcs','__pycache__']
def clear_cache():'Clear the filecmp cache.';_cache.clear()
def cmp(f1,f2,shallow=_B):
	'Compare two files.\n\n    Arguments:\n\n    f1 -- First file name\n\n    f2 -- Second file name\n\n    shallow -- treat files as identical if their stat signatures (type, size,\n               mtime) are identical. Otherwise, files are considered different\n               if their sizes or contents differ.  [default: True]\n\n    Return value:\n\n    True if the files are the same, False otherwise.\n\n    This function uses a cache for past comparisons and the results,\n    with cache entries invalidated if their stat information\n    changes.  The cache may be cleared by calling clear_cache().\n\n    ';A=_sig(os.stat(f1));B=_sig(os.stat(f2))
	if A[0]!=stat.S_IFREG or B[0]!=stat.S_IFREG:return _C
	if shallow and A==B:return _B
	if A[1]!=B[1]:return _C
	C=_cache.get((f1,f2,A,B))
	if C is _A:
		C=_do_cmp(f1,f2)
		if len(_cache)>100:clear_cache()
		_cache[f1,f2,A,B]=C
	return C
def _sig(st):return stat.S_IFMT(st.st_mode),st.st_size,st.st_mtime
def _do_cmp(f1,f2):
	A=BUFSIZE
	with open(f1,'rb')as C,open(f2,'rb')as D:
		while _B:
			B=C.read(A);E=D.read(A)
			if B!=E:return _C
			if not B:return _B
class dircmp:
	'A class that manages the comparison of 2 directories.\n\n    dircmp(a, b, ignore=None, hide=None)\n      A and B are directories.\n      IGNORE is a list of names to ignore,\n        defaults to DEFAULT_IGNORES.\n      HIDE is a list of names to hide,\n        defaults to [os.curdir, os.pardir].\n\n    High level usage:\n      x = dircmp(dir1, dir2)\n      x.report() -> prints a report on the differences between dir1 and dir2\n       or\n      x.report_partial_closure() -> prints report on differences between dir1\n            and dir2, and reports on common immediate subdirectories.\n      x.report_full_closure() -> like report_partial_closure,\n            but fully recursive.\n\n    Attributes:\n     left_list, right_list: The files in dir1 and dir2,\n        filtered by hide and ignore.\n     common: a list of names in both dir1 and dir2.\n     left_only, right_only: names only in dir1, dir2.\n     common_dirs: subdirectories in both dir1 and dir2.\n     common_files: files in both dir1 and dir2.\n     common_funny: names in both dir1 and dir2 where the type differs between\n        dir1 and dir2, or the name is not stat-able.\n     same_files: list of identical files.\n     diff_files: list of filenames which differ.\n     funny_files: list of files which could not be compared.\n     subdirs: a dictionary of dircmp instances (or MyDirCmp instances if this\n       object is of type MyDirCmp, a subclass of dircmp), keyed by names\n       in common_dirs.\n     '
	def __init__(A,a,b,ignore=_A,hide=_A):
		B=ignore;A.left=a;A.right=b
		if hide is _A:A.hide=[os.curdir,os.pardir]
		else:A.hide=hide
		if B is _A:A.ignore=DEFAULT_IGNORES
		else:A.ignore=B
	def phase0(A):A.left_list=_filter(os.listdir(A.left),A.hide+A.ignore);A.right_list=_filter(os.listdir(A.right),A.hide+A.ignore);A.left_list.sort();A.right_list.sort()
	def phase1(A):B=dict(zip(map(os.path.normcase,A.left_list),A.left_list));C=dict(zip(map(os.path.normcase,A.right_list),A.right_list));A.common=list(map(B.__getitem__,filter(C.__contains__,B)));A.left_only=list(map(B.__getitem__,filterfalse(C.__contains__,B)));A.right_only=list(map(C.__getitem__,filterfalse(B.__contains__,C)))
	def phase2(A):
		A.common_dirs=[];A.common_files=[];A.common_funny=[]
		for B in A.common:
			E=os.path.join(A.left,B);F=os.path.join(A.right,B);C=1
			try:G=os.stat(E)
			except OSError:C=0
			try:H=os.stat(F)
			except OSError:C=0
			if C:
				D=stat.S_IFMT(G.st_mode);I=stat.S_IFMT(H.st_mode)
				if D!=I:A.common_funny.append(B)
				elif stat.S_ISDIR(D):A.common_dirs.append(B)
				elif stat.S_ISREG(D):A.common_files.append(B)
				else:A.common_funny.append(B)
			else:A.common_funny.append(B)
	def phase3(A):B=cmpfiles(A.left,A.right,A.common_files);A.same_files,A.diff_files,A.funny_files=B
	def phase4(A):
		A.subdirs={}
		for B in A.common_dirs:C=os.path.join(A.left,B);D=os.path.join(A.right,B);A.subdirs[B]=A.__class__(C,D,A.ignore,A.hide)
	def phase4_closure(A):
		A.phase4()
		for B in A.subdirs.values():B.phase4_closure()
	def report(A):
		B='Only in';print('diff',A.left,A.right)
		if A.left_only:A.left_only.sort();print(B,A.left,':',A.left_only)
		if A.right_only:A.right_only.sort();print(B,A.right,':',A.right_only)
		if A.same_files:A.same_files.sort();print('Identical files :',A.same_files)
		if A.diff_files:A.diff_files.sort();print('Differing files :',A.diff_files)
		if A.funny_files:A.funny_files.sort();print('Trouble with common files :',A.funny_files)
		if A.common_dirs:A.common_dirs.sort();print('Common subdirectories :',A.common_dirs)
		if A.common_funny:A.common_funny.sort();print('Common funny cases :',A.common_funny)
	def report_partial_closure(A):
		A.report()
		for B in A.subdirs.values():print();B.report()
	def report_full_closure(A):
		A.report()
		for B in A.subdirs.values():print();B.report_full_closure()
	methodmap=dict(subdirs=phase4,same_files=phase3,diff_files=phase3,funny_files=phase3,common_dirs=phase2,common_files=phase2,common_funny=phase2,common=phase1,left_only=phase1,right_only=phase1,left_list=phase0,right_list=phase0)
	def __getattr__(A,attr):
		B=attr
		if B not in A.methodmap:raise AttributeError(B)
		A.methodmap[B](A);return getattr(A,B)
	__class_getitem__=classmethod(GenericAlias)
def cmpfiles(a,b,common,shallow=_B):
	"Compare common files in two directories.\n\n    a, b -- directory names\n    common -- list of file names found in both directories\n    shallow -- if true, do comparison based solely on stat() information\n\n    Returns a tuple of three lists:\n      files that compare equal\n      files that are different\n      filenames that aren't regular files.\n\n    ";B=[],[],[]
	for A in common:C=os.path.join(a,A);D=os.path.join(b,A);B[_cmp(C,D,shallow)].append(A)
	return B
def _cmp(a,b,sh,abs=abs,cmp=cmp):
	try:return not abs(cmp(a,b,sh))
	except OSError:return 2
def _filter(flist,skip):return list(filterfalse(skip.__contains__,flist))
def demo():
	import sys,getopt as B;D,A=B.getopt(sys.argv[1:],'r')
	if len(A)!=2:raise B.GetoptError('need exactly two args',_A)
	C=dircmp(A[0],A[1])
	if('-r','')in D:C.report_full_closure()
	else:C.report()
if __name__=='__main__':demo()