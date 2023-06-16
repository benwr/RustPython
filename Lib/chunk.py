'Simple class to read IFF chunks.\n\nAn IFF chunk (used in formats such as AIFF, TIFF, RMFF (RealMedia File\nFormat)) has the following structure:\n\n+----------------+\n| ID (4 bytes)   |\n+----------------+\n| size (4 bytes) |\n+----------------+\n| data           |\n| ...            |\n+----------------+\n\nThe ID is a 4-byte string which identifies the type of chunk.\n\nThe size field (a 32-bit value, encoded using big-endian byte order)\ngives the size of the whole chunk, including the 8-byte header.\n\nUsually an IFF-type file consists of one or more chunks.  The proposed\nusage of the Chunk class defined here is to instantiate an instance at\nthe start of each chunk and read from the instance until it reaches\nthe end, after which a new instance can be instantiated.  At the end\nof the file, creating a new instance will fail with an EOFError\nexception.\n\nUsage:\nwhile True:\n    try:\n        chunk = Chunk(file)\n    except EOFError:\n        break\n    chunktype = chunk.getname()\n    while True:\n        data = chunk.read(nbytes)\n        if not data:\n            pass\n        # do something with data\n\nThe interface is file-like.  The implemented methods are:\nread, close, seek, tell, isatty.\nExtra methods are: skip() (called by close, skips to the end of the chunk),\ngetname() (returns the name (ID) of the chunk)\n\nThe __init__ method has one required argument, a file-like object\n(including a chunk instance), and one optional argument, a flag which\nspecifies whether or not chunks are aligned on 2-byte boundaries.  The\ndefault is 1, i.e. aligned.\n'
_C=False
_B=True
_A='I/O operation on closed file'
class Chunk:
	def __init__(A,file,align=_B,bigendian=_B,inclheader=_C):
		B=file;import struct as C;A.closed=_C;A.align=align
		if bigendian:D='>'
		else:D='<'
		A.file=B;A.chunkname=B.read(4)
		if len(A.chunkname)<4:raise EOFError
		try:A.chunksize=C.unpack_from(D+'L',B.read(4))[0]
		except C.error:raise EOFError
		if inclheader:A.chunksize=A.chunksize-8
		A.size_read=0
		try:A.offset=A.file.tell()
		except(AttributeError,OSError):A.seekable=_C
		else:A.seekable=_B
	def getname(A):'Return the name (ID) of the current chunk.';return A.chunkname
	def getsize(A):'Return the size of the current chunk.';return A.chunksize
	def close(A):
		if not A.closed:
			try:A.skip()
			finally:A.closed=_B
	def isatty(A):
		if A.closed:raise ValueError(_A)
		return _C
	def seek(A,pos,whence=0):
		'Seek to specified position into the chunk.\n        Default position is 0 (start of chunk).\n        If the file is not seekable, this will result in an error.\n        ';C=whence;B=pos
		if A.closed:raise ValueError(_A)
		if not A.seekable:raise OSError('cannot seek')
		if C==1:B=B+A.size_read
		elif C==2:B=B+A.chunksize
		if B<0 or B>A.chunksize:raise RuntimeError
		A.file.seek(A.offset+B,0);A.size_read=B
	def tell(A):
		if A.closed:raise ValueError(_A)
		return A.size_read
	def read(A,size=-1):
		'Read at most size bytes from the chunk.\n        If size is omitted or negative, read until the end\n        of the chunk.\n        ';B=size
		if A.closed:raise ValueError(_A)
		if A.size_read>=A.chunksize:return b''
		if B<0:B=A.chunksize-A.size_read
		if B>A.chunksize-A.size_read:B=A.chunksize-A.size_read
		C=A.file.read(B);A.size_read=A.size_read+len(C)
		if A.size_read==A.chunksize and A.align and A.chunksize&1:D=A.file.read(1);A.size_read=A.size_read+len(D)
		return C
	def skip(A):
		'Skip the rest of the chunk.\n        If you are not interested in the contents of the chunk,\n        this method should be called so that the file points to\n        the start of the next chunk.\n        '
		if A.closed:raise ValueError(_A)
		if A.seekable:
			try:
				B=A.chunksize-A.size_read
				if A.align and A.chunksize&1:B=B+1
				A.file.seek(B,1);A.size_read=A.size_read+B;return
			except OSError:pass
		while A.size_read<A.chunksize:
			B=min(8192,A.chunksize-A.size_read);C=A.read(B)
			if not C:raise EOFError