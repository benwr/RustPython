'Routine to "compile" a .py file to a .pyc file.\n\nThis module has intimate knowledge of the format of .pyc files.\n'
_A=None
import enum,importlib._bootstrap_external,importlib.machinery,importlib.util,os,os.path,sys,traceback
__all__=['compile','main','PyCompileError','PycInvalidationMode']
class PyCompileError(Exception):
	"Exception raised when an error occurs while attempting to\n    compile the file.\n\n    To raise this exception, use\n\n        raise PyCompileError(exc_type,exc_value,file[,msg])\n\n    where\n\n        exc_type:   exception type to be used in error message\n                    type name can be accesses as class variable\n                    'exc_type_name'\n\n        exc_value:  exception value to be used in error message\n                    can be accesses as class variable 'exc_value'\n\n        file:       name of file being compiled to be used in error message\n                    can be accesses as class variable 'file'\n\n        msg:        string message to be written as error message\n                    If no value is given, a default exception message will be\n                    given, consistent with 'standard' py_compile output.\n                    message (or default) can be accesses as class variable\n                    'msg'\n\n    "
	def __init__(A,exc_type,exc_value,file,msg=''):
		C=file;D=exc_type;B=exc_value;E=D.__name__
		if D is SyntaxError:G=''.join(traceback.format_exception_only(D,B));F=G.replace('File "<string>"','File "%s"'%C)
		else:F='Sorry: %s: %s'%(E,B)
		Exception.__init__(A,msg or F,E,B,C);A.exc_type_name=E;A.exc_value=B;A.file=C;A.msg=msg or F
	def __str__(A):return A.msg
class PycInvalidationMode(enum.Enum):TIMESTAMP=1;CHECKED_HASH=2;UNCHECKED_HASH=3
def _get_default_invalidation_mode():
	if os.environ.get('SOURCE_DATE_EPOCH'):return PycInvalidationMode.CHECKED_HASH
	else:return PycInvalidationMode.TIMESTAMP
def compile(file,cfile=_A,dfile=_A,doraise=False,optimize=-1,invalidation_mode=_A,quiet=0):
	"Byte-compile one Python source file to Python bytecode.\n\n    :param file: The source file name.\n    :param cfile: The target byte compiled file name.  When not given, this\n        defaults to the PEP 3147/PEP 488 location.\n    :param dfile: Purported file name, i.e. the file name that shows up in\n        error messages.  Defaults to the source file name.\n    :param doraise: Flag indicating whether or not an exception should be\n        raised when a compile error is found.  If an exception occurs and this\n        flag is set to False, a string indicating the nature of the exception\n        will be printed, and the function will return to the caller. If an\n        exception occurs and this flag is set to True, a PyCompileError\n        exception will be raised.\n    :param optimize: The optimization level for the compiler.  Valid values\n        are -1, 0, 1 and 2.  A value of -1 means to use the optimization\n        level of the current interpreter, as given by -O command line options.\n    :param invalidation_mode:\n    :param quiet: Return full output with False or 0, errors only with 1,\n        and no output with 2.\n\n    :return: Path to the resulting byte compiled file.\n\n    Note that it isn't necessary to byte-compile Python modules for\n    execution efficiency -- Python itself byte-compiles a module when\n    it is loaded, and if it can, writes out the bytecode to the\n    corresponding .pyc file.\n\n    However, if a Python installation is shared between users, it is a\n    good idea to byte-compile all modules upon installation, since\n    other users may not be able to write in the source directories,\n    and thus they won't be able to write the .pyc file, and then\n    they would be byte-compiling every module each time it is loaded.\n    This can slow down program start-up considerably.\n\n    See compileall.py for a script/module that uses this module to\n    byte-compile all installed files (or all files in selected\n    directories).\n\n    Do note that FileExistsError is raised if cfile ends up pointing at a\n    non-regular file or symlink. Because the compilation uses a file renaming,\n    the resulting file would be regular and thus not the same type of file as\n    it was previously.\n    ";G=dfile;C=invalidation_mode;D=optimize;B=file;A=cfile
	if C is _A:C=_get_default_invalidation_mode()
	if A is _A:
		if D>=0:O=D if D>=1 else'';A=importlib.util.cache_from_source(B,optimization=O)
		else:A=importlib.util.cache_from_source(B)
	if os.path.islink(A):E='{} is a symlink and will be changed into a regular file if import writes a byte-compiled file to it';raise FileExistsError(E.format(A))
	elif os.path.exists(A)and not os.path.isfile(A):E='{} is a non-regular file and will be changed into a regular one if import writes a byte-compiled file to it';raise FileExistsError(E.format(A))
	F=importlib.machinery.SourceFileLoader('<py_compile>',B);H=F.get_data(B)
	try:I=F.source_to_code(H,G or B,_optimize=D)
	except Exception as J:
		K=PyCompileError(J.__class__,J,G or B)
		if quiet<2:
			if doraise:raise K
			else:sys.stderr.write(K.msg+'\n')
		return
	try:
		L=os.path.dirname(A)
		if L:os.makedirs(L)
	except FileExistsError:pass
	if C==PycInvalidationMode.TIMESTAMP:M=F.path_stats(B);N=importlib._bootstrap_external._code_to_timestamp_pyc(I,M['mtime'],M['size'])
	else:P=importlib.util.source_hash(H);N=importlib._bootstrap_external._code_to_hash_pyc(I,P,C==PycInvalidationMode.CHECKED_HASH)
	Q=importlib._bootstrap_external._calc_mode(B);importlib._bootstrap_external._write_atomic(A,N,Q);return A
def main():
	import argparse as E;F='A simple command-line interface for py_compile module.';A=E.ArgumentParser(description=F);A.add_argument('-q','--quiet',action='store_true',help='Suppress error output');A.add_argument('filenames',nargs='+',help='Files to compile');B=A.parse_args()
	if B.filenames==['-']:D=[A.rstrip('\n')for A in sys.stdin.readlines()]
	else:D=B.filenames
	for G in D:
		try:compile(G,doraise=True)
		except PyCompileError as C:
			if B.quiet:A.exit(1)
			else:A.exit(1,C.msg)
		except OSError as C:
			if B.quiet:A.exit(1)
			else:A.exit(1,str(C))
if __name__=='__main__':main()