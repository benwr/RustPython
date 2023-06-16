'Internal classes used by the gzip, lzma and bz2 modules'
import io,sys
BUFFER_SIZE=io.DEFAULT_BUFFER_SIZE
class BaseStream(io.BufferedIOBase):
	'Mode-checking helper functions.'
	def _check_not_closed(A):
		if A.closed:raise ValueError('I/O operation on closed file')
	def _check_can_read(A):
		if not A.readable():raise io.UnsupportedOperation('File not open for reading')
	def _check_can_write(A):
		if not A.writable():raise io.UnsupportedOperation('File not open for writing')
	def _check_can_seek(A):
		if not A.readable():raise io.UnsupportedOperation('Seeking is only supported on files open for reading')
		if not A.seekable():raise io.UnsupportedOperation('The underlying file object does not support seeking')
class DecompressReader(io.RawIOBase):
	'Adapts the decompressor API to a RawIOBase reader API'
	def readable(A):return True
	def __init__(A,fp,decomp_factory,trailing_error=(),**B):A._fp=fp;A._eof=False;A._pos=0;A._size=-1;A._decomp_factory=decomp_factory;A._decomp_args=B;A._decompressor=A._decomp_factory(**A._decomp_args);A._trailing_error=trailing_error
	def close(A):A._decompressor=None;return super().close()
	def seekable(A):return A._fp.seekable()
	def readinto(C,b):
		with memoryview(b)as D,D.cast('B')as B:A=C.read(len(B));B[:len(A)]=A
		return len(A)
	def read(A,size=-1):
		D=size
		if D<0:return A.readall()
		if not D or A._eof:return b''
		B=None
		while True:
			if A._decompressor.eof:
				C=A._decompressor.unused_data or A._fp.read(BUFFER_SIZE)
				if not C:break
				A._decompressor=A._decomp_factory(**A._decomp_args)
				try:B=A._decompressor.decompress(C,D)
				except A._trailing_error:break
			else:
				if A._decompressor.needs_input:
					C=A._fp.read(BUFFER_SIZE)
					if not C:raise EOFError('Compressed file ended before the end-of-stream marker was reached')
				else:C=b''
				B=A._decompressor.decompress(C,D)
			if B:break
		if not B:A._eof=True;A._size=A._pos;return b''
		A._pos+=len(B);return B
	def readall(B):
		A=[]
		while(C:=B.read(sys.maxsize)):A.append(C)
		return b''.join(A)
	def _rewind(A):A._fp.seek(0);A._eof=False;A._pos=0;A._decompressor=A._decomp_factory(**A._decomp_args)
	def seek(A,offset,whence=io.SEEK_SET):
		C=whence;B=offset
		if C==io.SEEK_SET:0
		elif C==io.SEEK_CUR:B=A._pos+B
		elif C==io.SEEK_END:
			if A._size<0:
				while A.read(io.DEFAULT_BUFFER_SIZE):0
			B=A._size+B
		else:raise ValueError('Invalid value for whence: {}'.format(C))
		if B<A._pos:A._rewind()
		else:B-=A._pos
		while B>0:
			D=A.read(min(io.DEFAULT_BUFFER_SIZE,B))
			if not D:break
			B-=len(D)
		return A._pos
	def tell(A):'Return the current file position.';return A._pos