'Helper class to quickly write a loop over all standard input files.\n\nTypical use is:\n\n    import fileinput\n    for line in fileinput.input(encoding="utf-8"):\n        process(line)\n\nThis iterates over the lines of all files listed in sys.argv[1:],\ndefaulting to sys.stdin if the list is empty.  If a filename is \'-\' it\nis also replaced by sys.stdin and the optional arguments mode and\nopenhook are ignored.  To specify an alternative list of filenames,\npass it as the argument to input().  A single file name is also allowed.\n\nFunctions filename(), lineno() return the filename and cumulative line\nnumber of the line that has just been read; filelineno() returns its\nline number in the current file; isfirstline() returns true iff the\nline just read is the first line of its file; isstdin() returns true\niff the line was read from sys.stdin.  Function nextfile() closes the\ncurrent file so that the next iteration will read the first line from\nthe next file (if any); lines not read from the file will not count\ntowards the cumulative line count; the filename is not changed until\nafter the first line of the next file has been read.  Function close()\ncloses the sequence.\n\nBefore any lines have been read, filename() returns None and both line\nnumbers are zero; nextfile() has no effect.  After all lines have been\nread, filename() and the line number functions return the values\npertaining to the last line read; nextfile() has no effect.\n\nAll files are opened in text mode by default, you can override this by\nsetting the mode parameter to input() or FileInput.__init__().\nIf an I/O error occurs during opening or reading a file, the OSError\nexception is raised.\n\nIf sys.stdin is used more than once, the second and further use will\nreturn no lines, except perhaps for interactive use, or if it has been\nexplicitly reset (e.g. using sys.stdin.seek(0)).\n\nEmpty files are opened and immediately closed; the only time their\npresence in the list of filenames is noticeable at all is when the\nlast file opened is empty.\n\nIt is possible that the last line of a file doesn\'t end in a newline\ncharacter; otherwise lines are returned including the trailing\nnewline.\n\nClass FileInput is the implementation; its methods filename(),\nlineno(), fileline(), isfirstline(), isstdin(), nextfile() and close()\ncorrespond to the functions in the module.  In addition it has a\nreadline() method which returns the next input line, and a\n__getitem__() method which implements the sequence behavior.  The\nsequence must be accessed in strictly sequential order; sequence\naccess and readline() cannot be mixed.\n\nOptional in-place filtering: if the keyword argument inplace=1 is\npassed to input() or to the FileInput constructor, the file is moved\nto a backup file and standard output is directed to the input file.\nThis makes it possible to write a filter that rewrites its input file\nin place.  If the keyword argument backup=".<some extension>" is also\ngiven, it specifies the extension for the backup file, and the backup\nfile remains around; by default, the extension is ".bak" and it is\ndeleted when the output file is closed.  In-place filtering is\ndisabled when standard input is read.  XXX The current implementation\ndoes not work for MS-DOS 8+3 filesystems.\n'
_E='locale'
_D=True
_C='no active input()'
_B=False
_A=None
import io,sys,os
from types import GenericAlias
__all__=['input','close','nextfile','filename','lineno','filelineno','fileno','isfirstline','isstdin','FileInput','hook_compressed','hook_encoded']
_state=_A
def input(files=_A,inplace=_B,backup='',*,mode='r',openhook=_A,encoding=_A,errors=_A):
	'Return an instance of the FileInput class, which can be iterated.\n\n    The parameters are passed to the constructor of the FileInput class.\n    The returned instance, in addition to being an iterator,\n    keeps global state for the functions of this module,.\n    ';global _state
	if _state and _state._file:raise RuntimeError('input() already active')
	_state=FileInput(files,inplace,backup,mode=mode,openhook=openhook,encoding=encoding,errors=errors);return _state
def close():
	'Close the sequence.';global _state;A=_state;_state=_A
	if A:A.close()
def nextfile():
	'\n    Close the current file so that the next iteration will read the first\n    line from the next file (if any); lines not read from the file will\n    not count towards the cumulative line count. The filename is not\n    changed until after the first line of the next file has been read.\n    Before the first line has been read, this function has no effect;\n    it cannot be used to skip the first file. After the last line of the\n    last file has been read, this function has no effect.\n    '
	if not _state:raise RuntimeError(_C)
	return _state.nextfile()
def filename():
	'\n    Return the name of the file currently being read.\n    Before the first line has been read, returns None.\n    '
	if not _state:raise RuntimeError(_C)
	return _state.filename()
def lineno():
	'\n    Return the cumulative line number of the line that has just been read.\n    Before the first line has been read, returns 0. After the last line\n    of the last file has been read, returns the line number of that line.\n    '
	if not _state:raise RuntimeError(_C)
	return _state.lineno()
def filelineno():
	'\n    Return the line number in the current file. Before the first line\n    has been read, returns 0. After the last line of the last file has\n    been read, returns the line number of that line within the file.\n    '
	if not _state:raise RuntimeError(_C)
	return _state.filelineno()
def fileno():
	'\n    Return the file number of the current file. When no file is currently\n    opened, returns -1.\n    '
	if not _state:raise RuntimeError(_C)
	return _state.fileno()
def isfirstline():
	'\n    Returns true the line just read is the first line of its file,\n    otherwise returns false.\n    '
	if not _state:raise RuntimeError(_C)
	return _state.isfirstline()
def isstdin():
	'\n    Returns true if the last line was read from sys.stdin,\n    otherwise returns false.\n    '
	if not _state:raise RuntimeError(_C)
	return _state.isstdin()
class FileInput:
	'FileInput([files[, inplace[, backup]]], *, mode=None, openhook=None)\n\n    Class FileInput is the implementation of the module; its methods\n    filename(), lineno(), fileline(), isfirstline(), isstdin(), fileno(),\n    nextfile() and close() correspond to the functions of the same name\n    in the module.\n    In addition it has a readline() method which returns the next\n    input line, and a __getitem__() method which implements the\n    sequence behavior. The sequence must be accessed in strictly\n    sequential order; random access and readline() cannot be mixed.\n    '
	def __init__(A,files=_A,inplace=_B,backup='',*,mode='r',openhook=_A,encoding=_A,errors=_A):
		G=encoding;H=inplace;E='U';D=openhook;C=mode;B=files
		if isinstance(B,str):B=B,
		elif isinstance(B,os.PathLike):B=os.fspath(B),
		else:
			if B is _A:B=sys.argv[1:]
			if not B:B='-',
			else:B=tuple(B)
		A._files=B;A._inplace=H;A._backup=backup;A._savestdout=_A;A._output=_A;A._filename=_A;A._startlineno=0;A._filelineno=0;A._file=_A;A._isstdin=_B;A._backupfilename=_A;A._encoding=G;A._errors=errors
		if sys.flags.warn_default_encoding and'b'not in C and G is _A and D is _A:import warnings as F;F.warn("'encoding' argument not specified.",EncodingWarning,2)
		if C not in('r','rU',E,'rb'):raise ValueError("FileInput opening mode must be one of 'r', 'rU', 'U' and 'rb'")
		if E in C:import warnings as F;F.warn("'U' mode is deprecated",DeprecationWarning,2)
		A._mode=C;A._write_mode=C.replace('r','w')if E not in C else'w'
		if D:
			if H:raise ValueError('FileInput cannot use an opening hook in inplace mode')
			if not callable(D):raise ValueError('FileInput openhook must be callable')
		A._openhook=D
	def __del__(A):A.close()
	def close(A):
		try:A.nextfile()
		finally:A._files=()
	def __enter__(A):return A
	def __exit__(A,type,value,traceback):A.close()
	def __iter__(A):return A
	def __next__(A):
		while _D:
			B=A._readline()
			if B:A._filelineno+=1;return B
			if not A._file:raise StopIteration
			A.nextfile()
	def __getitem__(A,i):
		import warnings as B;B.warn('Support for indexing FileInput objects is deprecated. Use iterator protocol instead.',DeprecationWarning,stacklevel=2)
		if i!=A.lineno():raise RuntimeError('accessing lines out of order')
		try:return A.__next__()
		except StopIteration:raise IndexError('end of input reached')
	def nextfile(A):
		B=A._savestdout;A._savestdout=_A
		if B:sys.stdout=B
		C=A._output;A._output=_A
		try:
			if C:C.close()
		finally:
			D=A._file;A._file=_A
			try:del A._readline
			except AttributeError:pass
			try:
				if D and not A._isstdin:D.close()
			finally:
				E=A._backupfilename;A._backupfilename=_A
				if E and not A._backup:
					try:os.unlink(E)
					except OSError:pass
				A._isstdin=_B
	def readline(A):
		while _D:
			B=A._readline()
			if B:A._filelineno+=1;return B
			if not A._file:return B
			A.nextfile()
	def _readline(A):
		if not A._files:
			if'b'in A._mode:return b''
			else:return''
		A._filename=A._files[0];A._files=A._files[1:];A._startlineno=A.lineno();A._filelineno=0;A._file=_A;A._isstdin=_B;A._backupfilename=0
		if'b'not in A._mode:B=A._encoding or _E
		else:B=_A
		if A._filename=='-':
			A._filename='<stdin>'
			if'b'in A._mode:A._file=getattr(sys.stdin,'buffer',sys.stdin)
			else:A._file=sys.stdin
			A._isstdin=_D
		elif A._inplace:
			A._backupfilename=os.fspath(A._filename)+(A._backup or'.bak')
			try:os.unlink(A._backupfilename)
			except OSError:pass
			os.rename(A._filename,A._backupfilename);A._file=open(A._backupfilename,A._mode,encoding=B,errors=A._errors)
			try:C=os.fstat(A._file.fileno()).st_mode
			except OSError:A._output=open(A._filename,A._write_mode,encoding=B,errors=A._errors)
			else:
				D=os.O_CREAT|os.O_WRONLY|os.O_TRUNC
				if hasattr(os,'O_BINARY'):D|=os.O_BINARY
				E=os.open(A._filename,D,C);A._output=os.fdopen(E,A._write_mode,encoding=B,errors=A._errors)
				try:os.chmod(A._filename,C)
				except OSError:pass
			A._savestdout=sys.stdout;sys.stdout=A._output
		elif A._openhook:
			if A._encoding is _A:A._file=A._openhook(A._filename,A._mode)
			else:A._file=A._openhook(A._filename,A._mode,encoding=A._encoding,errors=A._errors)
		else:A._file=open(A._filename,A._mode,encoding=B,errors=A._errors)
		A._readline=A._file.readline;return A._readline()
	def filename(A):return A._filename
	def lineno(A):return A._startlineno+A._filelineno
	def filelineno(A):return A._filelineno
	def fileno(A):
		if A._file:
			try:return A._file.fileno()
			except ValueError:return-1
		else:return-1
	def isfirstline(A):return A._filelineno==1
	def isstdin(A):return A._isstdin
	__class_getitem__=classmethod(GenericAlias)
def hook_compressed(filename,mode,*,encoding=_A,errors=_A):
	E=errors;A=encoding;B=mode;C=filename
	if A is _A:A=_E
	F=os.path.splitext(C)[1]
	if F=='.gz':import gzip;D=gzip.open(C,B)
	elif F=='.bz2':import bz2;D=bz2.BZ2File(C,B)
	else:return open(C,B,encoding=A,errors=E)
	if'b'not in B:D=io.TextIOWrapper(D,encoding=A,errors=E)
	return D
def hook_encoded(encoding,errors=_A):
	def A(filename,mode):return open(filename,mode,encoding=encoding,errors=errors)
	return A
def _test():
	import getopt as E;B=_B;C=_B;F,G=E.getopt(sys.argv[1:],'ib:')
	for(D,H)in F:
		if D=='-i':B=_D
		if D=='-b':C=H
	for A in input(G,inplace=B,backup=C):
		if A[-1:]=='\n':A=A[:-1]
		if A[-1:]=='\r':A=A[:-1]
		print('%d: %s[%d]%s %s'%(lineno(),filename(),filelineno(),isfirstline()and'*'or'',A))
	print('%d: %s[%d]'%(lineno(),filename(),filelineno()))
if __name__=='__main__':_test()