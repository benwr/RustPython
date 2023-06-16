'Manage shelves of pickled objects.\n\nA "shelf" is a persistent, dictionary-like object.  The difference\nwith dbm databases is that the values (not the keys!) in a shelf can\nbe essentially arbitrary Python objects -- anything that the "pickle"\nmodule can handle.  This includes most class instances, recursive data\ntypes, and objects containing lots of shared sub-objects.  The keys\nare ordinary strings.\n\nTo summarize the interface (key is a string, data is an arbitrary\nobject):\n\n        import shelve\n        d = shelve.open(filename) # open, with (g)dbm filename -- no suffix\n\n        d[key] = data   # store data at key (overwrites old data if\n                        # using an existing key)\n        data = d[key]   # retrieve a COPY of the data at key (raise\n                        # KeyError if no such key) -- NOTE that this\n                        # access returns a *copy* of the entry!\n        del d[key]      # delete data stored at key (raises KeyError\n                        # if no such key)\n        flag = key in d # true if the key exists\n        list = d.keys() # a list of all existing keys (slow!)\n\n        d.close()       # close it\n\nDependent on the implementation, closing a persistent dictionary may\nor may not be necessary to flush changes to disk.\n\nNormally, d[key] returns a COPY of the entry.  This needs care when\nmutable entries are mutated: for example, if d[key] is a list,\n        d[key].append(anitem)\ndoes NOT modify the entry d[key] itself, as stored in the persistent\nmapping -- it only modifies the copy, which is then immediately\ndiscarded, so that the append has NO effect whatsoever.  To append an\nitem to d[key] in a way that will affect the persistent mapping, use:\n        data = d[key]\n        data.append(anitem)\n        d[key] = data\n\nTo avoid the problem with mutable entries, you may pass the keyword\nargument writeback=True in the call to shelve.open.  When you use:\n        d = shelve.open(filename, writeback=True)\nthen d keeps a cache of all entries you access, and writes them all back\nto the persistent mapping when you call d.close().  This ensures that\nsuch usage as d[key].append(anitem) works as intended.\n\nHowever, using keyword argument writeback=True may consume vast amount\nof memory for the cache, and it may make d.close() very slow, if you\naccess many of d\'s entries after opening it in this way: d has no way to\ncheck which of the entries you access are mutable and/or which ones you\nactually mutate, so it must cache, and write back at close, all of the\nentries that you access.  You can call d.sync() to write back all the\nentries in the cache, and empty the cache (d.sync() also synchronizes\nthe persistent dictionary on disk, if feasible).\n'
_B=False
_A=None
from pickle import Pickler,Unpickler
from io import BytesIO
import collections.abc
__all__=['Shelf','BsdDbShelf','DbfilenameShelf','open']
class _ClosedDict(collections.abc.MutableMapping):
	'Marker for a closed dict.  Access attempts raise a ValueError.'
	def closed(A,*B):raise ValueError('invalid operation on closed shelf')
	__iter__=__len__=__getitem__=__setitem__=__delitem__=keys=closed
	def __repr__(A):return'<Closed Dictionary>'
class Shelf(collections.abc.MutableMapping):
	"Base class for shelf implementations.\n\n    This is initialized with a dictionary-like object.\n    See the module's __doc__ string for an overview of the interface.\n    "
	def __init__(A,dict,protocol=_A,writeback=_B,keyencoding='utf-8'):
		B=protocol;A.dict=dict
		if B is _A:B=3
		A._protocol=B;A.writeback=writeback;A.cache={};A.keyencoding=keyencoding
	def __iter__(A):
		for B in A.dict.keys():yield B.decode(A.keyencoding)
	def __len__(A):return len(A.dict)
	def __contains__(A,key):return key.encode(A.keyencoding)in A.dict
	def get(A,key,default=_A):
		if key.encode(A.keyencoding)in A.dict:return A[key]
		return default
	def __getitem__(A,key):
		B=key
		try:C=A.cache[B]
		except KeyError:
			D=BytesIO(A.dict[B.encode(A.keyencoding)]);C=Unpickler(D).load()
			if A.writeback:A.cache[B]=C
		return C
	def __setitem__(A,key,value):
		B=value
		if A.writeback:A.cache[key]=B
		C=BytesIO();D=Pickler(C,A._protocol);D.dump(B);A.dict[key.encode(A.keyencoding)]=C.getvalue()
	def __delitem__(A,key):
		del A.dict[key.encode(A.keyencoding)]
		try:del A.cache[key]
		except KeyError:pass
	def __enter__(A):return A
	def __exit__(A,type,value,traceback):A.close()
	def close(A):
		if A.dict is _A:return
		try:
			A.sync()
			try:A.dict.close()
			except AttributeError:pass
		finally:
			try:A.dict=_ClosedDict()
			except:A.dict=_A
	def __del__(A):
		if not hasattr(A,'writeback'):return
		A.close()
	def sync(A):
		if A.writeback and A.cache:
			A.writeback=_B
			for(B,C)in A.cache.items():A[B]=C
			A.writeback=True;A.cache={}
		if hasattr(A.dict,'sync'):A.dict.sync()
class BsdDbShelf(Shelf):
	'Shelf implementation using the "BSD" db interface.\n\n    This adds methods first(), next(), previous(), last() and\n    set_location() that have no counterpart in [g]dbm databases.\n\n    The actual database must be opened using one of the "bsddb"\n    modules "open" routines (i.e. bsddb.hashopen, bsddb.btopen or\n    bsddb.rnopen) and passed to the constructor.\n\n    See the module\'s __doc__ string for an overview of the interface.\n    '
	def __init__(A,dict,protocol=_A,writeback=_B,keyencoding='utf-8'):Shelf.__init__(A,dict,protocol,writeback,keyencoding)
	def set_location(B,key):A=key;A,C=B.dict.set_location(A);D=BytesIO(C);return A.decode(B.keyencoding),Unpickler(D).load()
	def next(A):B,C=next(A.dict);D=BytesIO(C);return B.decode(A.keyencoding),Unpickler(D).load()
	def previous(A):B,C=A.dict.previous();D=BytesIO(C);return B.decode(A.keyencoding),Unpickler(D).load()
	def first(A):B,C=A.dict.first();D=BytesIO(C);return B.decode(A.keyencoding),Unpickler(D).load()
	def last(A):B,C=A.dict.last();D=BytesIO(C);return B.decode(A.keyencoding),Unpickler(D).load()
class DbfilenameShelf(Shelf):
	'Shelf implementation using the "dbm" generic dbm interface.\n\n    This is initialized with the filename for the dbm database.\n    See the module\'s __doc__ string for an overview of the interface.\n    '
	def __init__(A,filename,flag='c',protocol=_A,writeback=_B):import dbm;Shelf.__init__(A,dbm.open(filename,flag),protocol,writeback)
def open(filename,flag='c',protocol=_A,writeback=_B):"Open a persistent dictionary for reading and writing.\n\n    The filename parameter is the base filename for the underlying\n    database.  As a side-effect, an extension may be added to the\n    filename and more than one file may be created.  The optional flag\n    parameter has the same interpretation as the flag parameter of\n    dbm.open(). The optional protocol parameter specifies the\n    version of the pickle protocol.\n\n    See the module's __doc__ string for an overview of the interface.\n    ";return DbfilenameShelf(filename,flag,protocol,writeback)