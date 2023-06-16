'Cache lines from Python source files.\n\nThis is intended to read lines from modules imported -- hence if a filename\nis not found, it will look down the module search path for a file by\nthat name.\n'
_A=None
import functools,sys
try:import os
except ImportError:import _dummy_os as os
import tokenize
__all__=['getline','clearcache','checkcache','lazycache']
cache={}
def clearcache():'Clear the cache entirely.';cache.clear()
def getline(filename,lineno,module_globals=_A):
	"Get a line for a Python source file from the cache.\n    Update the cache if it doesn't contain an entry for this file already.";A=lineno;B=getlines(filename,module_globals)
	if 1<=A<=len(B):return B[A-1]
	return''
def getlines(filename,module_globals=_A):
	"Get the lines for a Python source file from the cache.\n    Update the cache if it doesn't contain an entry for this file already.";A=filename
	if A in cache:
		B=cache[A]
		if len(B)!=1:return cache[A][2]
	try:return updatecache(A,module_globals)
	except MemoryError:clearcache();return[]
def checkcache(filename=_A):
	'Discard cache entries that are out of date.\n    (This is not checked upon each call!)';A=filename
	if A is _A:B=list(cache.keys())
	elif A in cache:B=[A]
	else:return
	for A in B:
		C=cache[A]
		if len(C)==1:continue
		F,D,H,G=C
		if D is _A:continue
		try:E=os.stat(G)
		except OSError:cache.pop(A,_A);continue
		if F!=E.st_size or D!=E.st_mtime:cache.pop(A,_A)
def updatecache(filename,module_globals=_A):
	"Update a cache entry and return its list of lines.\n    If something's wrong, print a message, discard the cache entry,\n    and return an empty list.";D='\n';A=filename
	if A in cache:
		if len(cache[A])!=1:cache.pop(A,_A)
	if not A or A.startswith('<')and A.endswith('>'):return[]
	B=A
	try:E=os.stat(B)
	except OSError:
		G=A
		if lazycache(A,module_globals):
			try:F=cache[A][0]()
			except(ImportError,OSError):pass
			else:
				if F is _A:return[]
				cache[A]=len(F),_A,[A+D for A in F.splitlines()],B;return cache[A][2]
		if os.path.isabs(A):return[]
		for H in sys.path:
			try:B=os.path.join(H,G)
			except(TypeError,AttributeError):continue
			try:E=os.stat(B);break
			except OSError:pass
		else:return[]
	try:
		with tokenize.open(B)as I:C=I.readlines()
	except(OSError,UnicodeDecodeError,SyntaxError):return[]
	if C and not C[-1].endswith(D):C[-1]+=D
	J,K=E.st_size,E.st_mtime;cache[A]=J,K,C,B;return C
def lazycache(filename,module_globals):
	'Seed the cache for filename with module_globals.\n\n    The module loader will be asked for the source only when getlines is\n    called, not immediately.\n\n    If there is an entry in the cache already, it is not altered.\n\n    :return: True if a lazy load is registered in the cache,\n        otherwise False. To register such a load a module loader with a\n        get_source method must be found, the filename must be a cacheable\n        filename, and the filename must not be already cached.\n    ';D='__name__';C=False;B=module_globals;A=filename
	if A in cache:
		if len(cache[A])==1:return True
		else:return C
	if not A or A.startswith('<')and A.endswith('>'):return C
	if B and D in B:
		E=B[D]
		if(F:=B.get('__loader__'))is _A:
			if(H:=B.get('__spec__')):
				try:F=H.loader
				except AttributeError:pass
		G=getattr(F,'get_source',_A)
		if E and G:I=functools.partial(G,E);cache[A]=I,;return True
	return C