'Macintosh binhex compression/decompression.\n\neasy interface:\nbinhex(inputfilename, outputfilename)\nhexbin(inputfilename, outputfilename)\n'
_F=b'\x00'
_E='>h'
_D='rb'
_C=None
_B=True
_A=b''
import binascii,contextlib,io,os,struct,warnings
warnings.warn('the binhex module is deprecated',DeprecationWarning,stacklevel=2)
__all__=['binhex','hexbin','Error']
class Error(Exception):0
_DID_HEADER=0
_DID_DATA=1
REASONABLY_LARGE=32768
LINELEN=64
RUNCHAR=b'\x90'
class FInfo:
	def __init__(A):B='????';A.Type=B;A.Creator=B;A.Flags=0
def getfileinfo(name):
	C=FInfo()
	with io.open(name,_D)as A:
		D=A.read(512)
		if 0 not in D:C.Type='TEXT'
		A.seek(0,2);E=A.tell()
	dir,B=os.path.split(name);B=B.replace(':','-',1);return B,C,E,0
class openrsrc:
	def __init__(A,*B):0
	def read(A,*B):return _A
	def write(A,*B):0
	def close(A):0
@contextlib.contextmanager
def _ignore_deprecation_warning():
	with warnings.catch_warnings():warnings.filterwarnings('ignore','',DeprecationWarning);yield
class _Hqxcoderengine:
	'Write data to the coder in 3-byte chunks'
	def __init__(A,ofp):A.ofp=ofp;A.data=_A;A.hqxdata=_A;A.linelen=LINELEN-1
	def write(A,data):
		B=data;A.data=A.data+B;D=len(A.data);C=D//3*3;B=A.data[:C];A.data=A.data[C:]
		if not B:return
		with _ignore_deprecation_warning():A.hqxdata=A.hqxdata+binascii.b2a_hqx(B)
		A._flush(0)
	def _flush(A,force):
		B=0
		while B<=len(A.hqxdata)-A.linelen:C=B+A.linelen;A.ofp.write(A.hqxdata[B:C]+b'\r');A.linelen=LINELEN;B=C
		A.hqxdata=A.hqxdata[B:]
		if force:A.ofp.write(A.hqxdata+b':\r')
	def close(A):
		if A.data:
			with _ignore_deprecation_warning():A.hqxdata=A.hqxdata+binascii.b2a_hqx(A.data)
		A._flush(1);A.ofp.close();del A.ofp
class _Rlecoderengine:
	'Write data to the RLE-coder in suitably large chunks'
	def __init__(A,ofp):A.ofp=ofp;A.data=_A
	def write(A,data):
		A.data=A.data+data
		if len(A.data)<REASONABLY_LARGE:return
		with _ignore_deprecation_warning():B=binascii.rlecode_hqx(A.data)
		A.ofp.write(B);A.data=_A
	def close(A):
		if A.data:
			with _ignore_deprecation_warning():B=binascii.rlecode_hqx(A.data)
			A.ofp.write(B)
		A.ofp.close();del A.ofp
class BinHex:
	def __init__(A,name_finfo_dlen_rlen,ofp):
		B=ofp;E,C,F,G=name_finfo_dlen_rlen;D=False
		if isinstance(B,str):H=B;B=io.open(H,'wb');D=_B
		try:
			B.write(b'(This file must be converted with BinHex 4.0)\r\r:');I=_Hqxcoderengine(B);A.ofp=_Rlecoderengine(I);A.crc=0
			if C is _C:C=FInfo()
			A.dlen=F;A.rlen=G;A._writeinfo(E,C);A.state=_DID_HEADER
		except:
			if D:B.close()
			raise
	def _writeinfo(A,name,finfo):
		D='latin-1';E=finfo;F=len(name)
		if F>63:raise Error('Filename too long')
		G=bytes([F])+name.encode(D)+_F;B,C=E.Type,E.Creator
		if isinstance(B,str):B=B.encode(D)
		if isinstance(C,str):C=C.encode(D)
		H=B+C;I=struct.pack(_E,E.Flags);J=struct.pack('>ii',A.dlen,A.rlen);K=G+H+I+J;A._write(K);A._writecrc()
	def _write(A,data):A.crc=binascii.crc_hqx(data,A.crc);A.ofp.write(data)
	def _writecrc(A):
		if A.crc<0:B=_E
		else:B='>H'
		A.ofp.write(struct.pack(B,A.crc));A.crc=0
	def write(A,data):
		if A.state!=_DID_HEADER:raise Error('Writing data at the wrong time')
		A.dlen=A.dlen-len(data);A._write(data)
	def close_data(A):
		if A.dlen!=0:raise Error('Incorrect data size, diff=%r'%(A.rlen,))
		A._writecrc();A.state=_DID_DATA
	def write_rsrc(A,data):
		if A.state<_DID_DATA:A.close_data()
		if A.state!=_DID_DATA:raise Error('Writing resource data at the wrong time')
		A.rlen=A.rlen-len(data);A._write(data)
	def close(A):
		if A.state is _C:return
		try:
			if A.state<_DID_DATA:A.close_data()
			if A.state!=_DID_DATA:raise Error('Close at the wrong time')
			if A.rlen!=0:raise Error('Incorrect resource-datasize, diff=%r'%(A.rlen,))
			A._writecrc()
		finally:A.state=_C;B=A.ofp;del A.ofp;B.close()
def binhex(inp,out):
	'binhex(infilename, outfilename): create binhex-encoded copy of a file';D=inp;E=getfileinfo(D);B=BinHex(E,out)
	with io.open(D,_D)as C:
		while _B:
			A=C.read(128000)
			if not A:break
			B.write(A)
		B.close_data()
	C=openrsrc(D,_D)
	while _B:
		A=C.read(128000)
		if not A:break
		B.write_rsrc(A)
	B.close();C.close()
class _Hqxdecoderengine:
	'Read data via the decoder in 4-byte chunks'
	def __init__(A,ifp):A.ifp=ifp;A.eof=0
	def read(B,totalwtd):
		'Read at least wtd bytes (or until EOF)';E='Premature EOF on binhex file';F=totalwtd;A=_A;C=F
		while C>0:
			if B.eof:return A
			C=(C+2)//3*4;D=B.ifp.read(C)
			while _B:
				try:
					with _ignore_deprecation_warning():H,B.eof=binascii.a2b_hqx(D)
					break
				except binascii.Incomplete:pass
				G=B.ifp.read(1)
				if not G:raise Error(E)
				D=D+G
			A=A+H;C=F-len(A)
			if not A and not B.eof:raise Error(E)
		return A
	def close(A):A.ifp.close()
class _Rledecoderengine:
	'Read data via the RLE-coder'
	def __init__(A,ifp):A.ifp=ifp;A.pre_buffer=_A;A.post_buffer=_A;A.eof=0
	def read(A,wtd):
		B=wtd
		if B>len(A.post_buffer):A._fill(B-len(A.post_buffer))
		C=A.post_buffer[:B];A.post_buffer=A.post_buffer[B:];return C
	def _fill(A,wtd):
		A.pre_buffer=A.pre_buffer+A.ifp.read(wtd+4)
		if A.ifp.eof:
			with _ignore_deprecation_warning():A.post_buffer=A.post_buffer+binascii.rledecode_hqx(A.pre_buffer)
			A.pre_buffer=_A;return
		B=len(A.pre_buffer)
		if A.pre_buffer[-3:]==RUNCHAR+_F+RUNCHAR:B=B-3
		elif A.pre_buffer[-1:]==RUNCHAR:B=B-2
		elif A.pre_buffer[-2:]==RUNCHAR+_F:B=B-2
		elif A.pre_buffer[-2:-1]==RUNCHAR:0
		else:B=B-1
		with _ignore_deprecation_warning():A.post_buffer=A.post_buffer+binascii.rledecode_hqx(A.pre_buffer[:B])
		A.pre_buffer=A.pre_buffer[B:]
	def close(A):A.ifp.close()
class HexBin:
	def __init__(B,ifp):
		A=ifp
		if isinstance(A,str):A=io.open(A,_D)
		while _B:
			C=A.read(1)
			if not C:raise Error('No binhex data found')
			if C==b'\r':continue
			if C==b':':break
		D=_Hqxdecoderengine(A);B.ifp=_Rledecoderengine(D);B.crc=0;B._readheader()
	def _read(A,len):B=A.ifp.read(len);A.crc=binascii.crc_hqx(B,A.crc);return B
	def _checkcrc(A):
		B=struct.unpack(_E,A.ifp.read(2))[0]&65535;A.crc=A.crc&65535
		if B!=A.crc:raise Error('CRC error, computed %x, read %x'%(A.crc,B))
		A.crc=0
	def _readheader(A):len=A._read(1);C=A._read(ord(len));B=A._read(1+4+4+2+4+4);A._checkcrc();type=B[1:5];D=B[5:9];E=struct.unpack(_E,B[9:11])[0];A.dlen=struct.unpack('>l',B[11:15])[0];A.rlen=struct.unpack('>l',B[15:19])[0];A.FName=C;A.FInfo=FInfo();A.FInfo.Creator=D;A.FInfo.Type=type;A.FInfo.Flags=E;A.state=_DID_HEADER
	def read(B,*A):
		if B.state!=_DID_HEADER:raise Error('Read data at wrong time')
		if A:A=A[0];A=min(A,B.dlen)
		else:A=B.dlen
		C=_A
		while len(C)<A:C=C+B._read(A-len(C))
		B.dlen=B.dlen-A;return C
	def close_data(A):
		if A.state!=_DID_HEADER:raise Error('close_data at wrong time')
		if A.dlen:B=A._read(A.dlen)
		A._checkcrc();A.state=_DID_DATA
	def read_rsrc(A,*B):
		if A.state==_DID_HEADER:A.close_data()
		if A.state!=_DID_DATA:raise Error('Read resource data at wrong time')
		if B:B=B[0];B=min(B,A.rlen)
		else:B=A.rlen
		A.rlen=A.rlen-B;return A._read(B)
	def close(A):
		if A.state is _C:return
		try:
			if A.rlen:B=A.read_rsrc(A.rlen)
			A._checkcrc()
		finally:A.state=_C;A.ifp.close()
def hexbin(inp,out):
	'hexbin(infilename, outfilename) - Decode binhexed file';D=out;B=HexBin(inp);E=B.FInfo
	if not D:D=B.FName
	with io.open(D,'wb')as C:
		while _B:
			A=B.read(128000)
			if not A:break
			C.write(A)
	B.close_data();A=B.read_rsrc(128000)
	if A:
		C=openrsrc(D,'wb');C.write(A)
		while _B:
			A=B.read_rsrc(128000)
			if not A:break
			C.write(A)
		C.close()
	B.close()