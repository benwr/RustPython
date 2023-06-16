'Stuff to parse AIFF-C and AIFF files.\n\nUnless explicitly stated otherwise, the description below is true\nboth for AIFF-C files and AIFF files.\n\nAn AIFF-C file has the following structure.\n\n  +-----------------+\n  | FORM            |\n  +-----------------+\n  | <size>          |\n  +----+------------+\n  |    | AIFC       |\n  |    +------------+\n  |    | <chunks>   |\n  |    |    .       |\n  |    |    .       |\n  |    |    .       |\n  +----+------------+\n\nAn AIFF file has the string "AIFF" instead of "AIFC".\n\nA chunk consists of an identifier (4 bytes) followed by a size (4 bytes,\nbig endian order), followed by the data.  The size field does not include\nthe size of the 8 byte header.\n\nThe following chunk types are recognized.\n\n  FVER\n      <version number of AIFF-C defining document> (AIFF-C only).\n  MARK\n      <# of markers> (2 bytes)\n      list of markers:\n          <marker ID> (2 bytes, must be > 0)\n          <position> (4 bytes)\n          <marker name> ("pstring")\n  COMM\n      <# of channels> (2 bytes)\n      <# of sound frames> (4 bytes)\n      <size of the samples> (2 bytes)\n      <sampling frequency> (10 bytes, IEEE 80-bit extended\n          floating point)\n      in AIFF-C files only:\n      <compression type> (4 bytes)\n      <human-readable version of compression type> ("pstring")\n  SSND\n      <offset> (4 bytes, not used by this program)\n      <blocksize> (4 bytes, not used by this program)\n      <sound data>\n\nA pstring consists of 1 byte length, a string of characters, and 0 or 1\nbyte pad to make the total length even.\n\nUsage.\n\nReading AIFF files:\n  f = aifc.open(file, \'r\')\nwhere file is either the name of a file or an open file pointer.\nThe open file pointer must have methods read(), seek(), and close().\nIn some types of audio files, if the setpos() method is not used,\nthe seek() method is not necessary.\n\nThis returns an instance of a class with the following public methods:\n  getnchannels()  -- returns number of audio channels (1 for\n             mono, 2 for stereo)\n  getsampwidth()  -- returns sample width in bytes\n  getframerate()  -- returns sampling frequency\n  getnframes()    -- returns number of audio frames\n  getcomptype()   -- returns compression type (\'NONE\' for AIFF files)\n  getcompname()   -- returns human-readable version of\n             compression type (\'not compressed\' for AIFF files)\n  getparams() -- returns a namedtuple consisting of all of the\n             above in the above order\n  getmarkers()    -- get the list of marks in the audio file or None\n             if there are no marks\n  getmark(id) -- get mark with the specified id (raises an error\n             if the mark does not exist)\n  readframes(n)   -- returns at most n frames of audio\n  rewind()    -- rewind to the beginning of the audio stream\n  setpos(pos) -- seek to the specified position\n  tell()      -- return the current position\n  close()     -- close the instance (make it unusable)\nThe position returned by tell(), the position given to setpos() and\nthe position of marks are all compatible and have nothing to do with\nthe actual position in the file.\nThe close() method is called automatically when the class instance\nis destroyed.\n\nWriting AIFF files:\n  f = aifc.open(file, \'w\')\nwhere file is either the name of a file or an open file pointer.\nThe open file pointer must have methods write(), tell(), seek(), and\nclose().\n\nThis returns an instance of a class with the following public methods:\n  aiff()      -- create an AIFF file (AIFF-C default)\n  aifc()      -- create an AIFF-C file\n  setnchannels(n) -- set the number of channels\n  setsampwidth(n) -- set the sample width\n  setframerate(n) -- set the frame rate\n  setnframes(n)   -- set the number of frames\n  setcomptype(type, name)\n          -- set the compression type and the\n             human-readable compression type\n  setparams(tuple)\n          -- set all parameters at once\n  setmark(id, pos, name)\n          -- add specified mark to the list of marks\n  tell()      -- return current position in output file (useful\n             in combination with setmark())\n  writeframesraw(data)\n          -- write audio frames without pathing up the\n             file header\n  writeframes(data)\n          -- write audio frames and patch up the file header\n  close()     -- patch up the file header and close the\n             output file\nYou should set the parameters before the first writeframesraw or\nwriteframes.  The total number of frames does not need to be set,\nbut when it is set to the correct value, the header does not have to\nbe patched up.\nIt is best to first set all parameters, perhaps possibly the\ncompression type, and then write audio frames using writeframesraw.\nWhen all frames have been written, either call writeframes(b\'\') or\nclose() to patch up the sizes in the header.\nMarks can be added anytime.  If there are any marks, you must call\nclose() after all frames have been written.\nThe close() method is called automatically when the class instance\nis destroyed.\n\nWhen a file is opened with the extension \'.aiff\', an AIFF file is\nwritten, otherwise an AIFF-C file is written.  This default can be\nchanged by calling aiff() or aifc() before the first writeframes or\nwriteframesraw.\n'
_O=b'not compressed'
_N='bad # of channels'
_M='bad sample width'
_L='_adpcmstate'
_K='marker {0!r} does not exist'
_J='unsupported compression type'
_I=b'\x00'
_H=b'NONE'
_G=b'ALAW'
_F=b'alaw'
_E=b'ULAW'
_D=b'ulaw'
_C=b'G722'
_B='cannot change parameters after starting to write'
_A=None
import struct,builtins,warnings
__all__=['Error','open','openfp']
class Error(Exception):0
_AIFC_version=2726318400
def _read_long(file):
	try:return struct.unpack('>l',file.read(4))[0]
	except struct.error:raise EOFError from _A
def _read_ulong(file):
	try:return struct.unpack('>L',file.read(4))[0]
	except struct.error:raise EOFError from _A
def _read_short(file):
	try:return struct.unpack('>h',file.read(2))[0]
	except struct.error:raise EOFError from _A
def _read_ushort(file):
	try:return struct.unpack('>H',file.read(2))[0]
	except struct.error:raise EOFError from _A
def _read_string(file):
	A=file;B=ord(A.read(1))
	if B==0:C=b''
	else:C=A.read(B)
	if B&1==0:D=A.read(1)
	return C
_HUGE_VAL=1.79769313486231e308
def _read_float(f):
	A=_read_short(f);B=1
	if A<0:B=-1;A=A+32768
	C=_read_ulong(f);D=_read_ulong(f)
	if A==C==D==0:f=.0
	elif A==32767:f=_HUGE_VAL
	else:A=A-16383;f=(C*4294967296+D)*pow(2.,A-63)
	return B*f
def _write_short(f,x):f.write(struct.pack('>h',x))
def _write_ushort(f,x):f.write(struct.pack('>H',x))
def _write_long(f,x):f.write(struct.pack('>l',x))
def _write_ulong(f,x):f.write(struct.pack('>L',x))
def _write_string(f,s):
	if len(s)>255:raise ValueError('string exceeds maximum pstring length')
	f.write(struct.pack('B',len(s)));f.write(s)
	if len(s)&1==0:f.write(_I)
def _write_float(f,x):
	import math as C
	if x<0:E=32768;x=x*-1
	else:E=0
	if x==0:A=0;F=0;G=0
	else:
		B,A=C.frexp(x)
		if A>16384 or B>=1 or B!=B:A=E|32767;F=0;G=0
		else:
			A=A+16382
			if A<0:B=C.ldexp(B,A);A=0
			A=A|E;B=C.ldexp(B,32);D=C.floor(B);F=int(D);B=C.ldexp(B-D,32);D=C.floor(B);G=int(D)
	_write_ushort(f,A);_write_ulong(f,F);_write_ulong(f,G)
from chunk import Chunk
from collections import namedtuple
_aifc_params=namedtuple('_aifc_params','nchannels sampwidth framerate nframes comptype compname')
_aifc_params.nchannels.__doc__='Number of audio channels (1 for mono, 2 for stereo)'
_aifc_params.sampwidth.__doc__='Sample width in bytes'
_aifc_params.framerate.__doc__='Sampling frequency'
_aifc_params.nframes.__doc__='Number of audio frames'
_aifc_params.comptype.__doc__='Compression type ("NONE" for AIFF files)'
_aifc_params.compname.__doc__="A human-readable version of the compression type\n('not compressed' for AIFF files)"
class Aifc_read:
	_file=_A
	def initfp(A,file):
		A._version=0;A._convert=_A;A._markers=[];A._soundpos=0;A._file=file;B=Chunk(file)
		if B.getname()!=b'FORM':raise Error('file does not start with FORM id')
		D=B.read(4)
		if D==b'AIFF':A._aifc=0
		elif D==b'AIFC':A._aifc=1
		else:raise Error('not an AIFF or AIFF-C file')
		A._comm_chunk_read=0;A._ssnd_chunk=_A
		while 1:
			A._ssnd_seek_needed=1
			try:B=Chunk(A._file)
			except EOFError:break
			C=B.getname()
			if C==b'COMM':A._read_comm_chunk(B);A._comm_chunk_read=1
			elif C==b'SSND':A._ssnd_chunk=B;E=B.read(8);A._ssnd_seek_needed=0
			elif C==b'FVER':A._version=_read_ulong(B)
			elif C==b'MARK':A._readmark(B)
			B.skip()
		if not A._comm_chunk_read or not A._ssnd_chunk:raise Error('COMM chunk and/or SSND chunk missing')
	def __init__(A,f):
		if isinstance(f,str):
			B=builtins.open(f,'rb')
			try:A.initfp(B)
			except:B.close();raise
		else:A.initfp(f)
	def __enter__(A):return A
	def __exit__(A,*B):A.close()
	def getfp(A):return A._file
	def rewind(A):A._ssnd_seek_needed=1;A._soundpos=0
	def close(A):
		B=A._file
		if B is not _A:A._file=_A;B.close()
	def tell(A):return A._soundpos
	def getnchannels(A):return A._nchannels
	def getnframes(A):return A._nframes
	def getsampwidth(A):return A._sampwidth
	def getframerate(A):return A._framerate
	def getcomptype(A):return A._comptype
	def getcompname(A):return A._compname
	def getparams(A):return _aifc_params(A.getnchannels(),A.getsampwidth(),A.getframerate(),A.getnframes(),A.getcomptype(),A.getcompname())
	def getmarkers(A):
		if len(A._markers)==0:return
		return A._markers
	def getmark(B,id):
		for A in B._markers:
			if id==A[0]:return A
		raise Error(_K.format(id))
	def setpos(A,pos):
		B=pos
		if B<0 or B>A._nframes:raise Error('position not in range')
		A._soundpos=B;A._ssnd_seek_needed=1
	def readframes(A,nframes):
		C=nframes
		if A._ssnd_seek_needed:
			A._ssnd_chunk.seek(0);E=A._ssnd_chunk.read(8);D=A._soundpos*A._framesize
			if D:A._ssnd_chunk.seek(D+8)
			A._ssnd_seek_needed=0
		if C==0:return b''
		B=A._ssnd_chunk.read(C*A._framesize)
		if A._convert and B:B=A._convert(B)
		A._soundpos=A._soundpos+len(B)//(A._nchannels*A._sampwidth);return B
	def _alaw2lin(B,data):import audioop as A;return A.alaw2lin(data,2)
	def _ulaw2lin(B,data):import audioop as A;return A.ulaw2lin(data,2)
	def _adpcm2lin(A,data):
		B=data;import audioop as C
		if not hasattr(A,_L):A._adpcmstate=_A
		B,A._adpcmstate=C.adpcm2lin(B,2,A._adpcmstate);return B
	def _read_comm_chunk(A,chunk):
		B=chunk;A._nchannels=_read_short(B);A._nframes=_read_long(B);A._sampwidth=(_read_short(B)+7)//8;A._framerate=int(_read_float(B))
		if A._sampwidth<=0:raise Error(_M)
		if A._nchannels<=0:raise Error(_N)
		A._framesize=A._nchannels*A._sampwidth
		if A._aifc:
			D=0
			if B.chunksize==18:D=1;warnings.warn('Warning: bad COMM chunk size');B.chunksize=23
			A._comptype=B.read(4)
			if D:
				C=ord(B.file.read(1))
				if C&1==0:C=C+1
				B.chunksize=B.chunksize+C;B.file.seek(-1,1)
			A._compname=_read_string(B)
			if A._comptype!=_H:
				if A._comptype==_C:A._convert=A._adpcm2lin
				elif A._comptype in(_D,_E):A._convert=A._ulaw2lin
				elif A._comptype in(_F,_G):A._convert=A._alaw2lin
				else:raise Error(_J)
				A._sampwidth=2
		else:A._comptype=_H;A._compname=_O
	def _readmark(B,chunk):
		A=chunk;C=_read_short(A)
		try:
			for G in range(C):
				id=_read_short(A);D=_read_long(A);E=_read_string(A)
				if D or E:B._markers.append((id,D,E))
		except EOFError:F='Warning: MARK chunk contains only %s marker%s instead of %s'%(len(B._markers),''if len(B._markers)==1 else's',C);warnings.warn(F)
class Aifc_write:
	_file=_A
	def __init__(A,f):
		if isinstance(f,str):
			B=builtins.open(f,'wb')
			try:A.initfp(B)
			except:B.close();raise
			if f.endswith('.aiff'):A._aifc=0
		else:A.initfp(f)
	def initfp(A,file):A._file=file;A._version=_AIFC_version;A._comptype=_H;A._compname=_O;A._convert=_A;A._nchannels=0;A._sampwidth=0;A._framerate=0;A._nframes=0;A._nframeswritten=0;A._datawritten=0;A._datalength=0;A._markers=[];A._marklength=0;A._aifc=1
	def __del__(A):A.close()
	def __enter__(A):return A
	def __exit__(A,*B):A.close()
	def aiff(A):
		if A._nframeswritten:raise Error(_B)
		A._aifc=0
	def aifc(A):
		if A._nframeswritten:raise Error(_B)
		A._aifc=1
	def setnchannels(A,nchannels):
		B=nchannels
		if A._nframeswritten:raise Error(_B)
		if B<1:raise Error(_N)
		A._nchannels=B
	def getnchannels(A):
		if not A._nchannels:raise Error('number of channels not set')
		return A._nchannels
	def setsampwidth(B,sampwidth):
		A=sampwidth
		if B._nframeswritten:raise Error(_B)
		if A<1 or A>4:raise Error(_M)
		B._sampwidth=A
	def getsampwidth(A):
		if not A._sampwidth:raise Error('sample width not set')
		return A._sampwidth
	def setframerate(A,framerate):
		B=framerate
		if A._nframeswritten:raise Error(_B)
		if B<=0:raise Error('bad frame rate')
		A._framerate=B
	def getframerate(A):
		if not A._framerate:raise Error('frame rate not set')
		return A._framerate
	def setnframes(A,nframes):
		if A._nframeswritten:raise Error(_B)
		A._nframes=nframes
	def getnframes(A):return A._nframeswritten
	def setcomptype(A,comptype,compname):
		B=comptype
		if A._nframeswritten:raise Error(_B)
		if B not in(_H,_D,_E,_F,_G,_C):raise Error(_J)
		A._comptype=B;A._compname=compname
	def getcomptype(A):return A._comptype
	def getcompname(A):return A._compname
	def setparams(A,params):
		C,D,E,F,B,G=params
		if A._nframeswritten:raise Error(_B)
		if B not in(_H,_D,_E,_F,_G,_C):raise Error(_J)
		A.setnchannels(C);A.setsampwidth(D);A.setframerate(E);A.setnframes(F);A.setcomptype(B,G)
	def getparams(A):
		if not A._nchannels or not A._sampwidth or not A._framerate:raise Error('not all parameters set')
		return _aifc_params(A._nchannels,A._sampwidth,A._framerate,A._nframes,A._comptype,A._compname)
	def setmark(A,id,pos,name):
		B=name;C=pos
		if id<=0:raise Error('marker ID must be > 0')
		if C<0:raise Error('marker position must be >= 0')
		if not isinstance(B,bytes):raise Error('marker name must be bytes')
		for D in range(len(A._markers)):
			if id==A._markers[D][0]:A._markers[D]=id,C,B;return
		A._markers.append((id,C,B))
	def getmark(B,id):
		for A in B._markers:
			if id==A[0]:return A
		raise Error(_K.format(id))
	def getmarkers(A):
		if len(A._markers)==0:return
		return A._markers
	def tell(A):return A._nframeswritten
	def writeframesraw(A,data):
		B=data
		if not isinstance(B,(bytes,bytearray)):B=memoryview(B).cast('B')
		A._ensure_header_written(len(B));C=len(B)//(A._sampwidth*A._nchannels)
		if A._convert:B=A._convert(B)
		A._file.write(B);A._nframeswritten=A._nframeswritten+C;A._datawritten=A._datawritten+len(B)
	def writeframes(A,data):
		A.writeframesraw(data)
		if A._nframeswritten!=A._nframes or A._datalength!=A._datawritten:A._patchheader()
	def close(A):
		if A._file is _A:return
		try:
			A._ensure_header_written(0)
			if A._datawritten&1:A._file.write(_I);A._datawritten=A._datawritten+1
			A._writemarkers()
			if A._nframeswritten!=A._nframes or A._datalength!=A._datawritten or A._marklength:A._patchheader()
		finally:A._convert=_A;B=A._file;A._file=_A;B.close()
	def _lin2alaw(B,data):import audioop as A;return A.lin2alaw(data,2)
	def _lin2ulaw(B,data):import audioop as A;return A.lin2ulaw(data,2)
	def _lin2adpcm(A,data):
		B=data;import audioop as C
		if not hasattr(A,_L):A._adpcmstate=_A
		B,A._adpcmstate=C.lin2adpcm(B,2,A._adpcmstate);return B
	def _ensure_header_written(A,datasize):
		if not A._nframeswritten:
			if A._comptype in(_E,_D,_G,_F,_C):
				if not A._sampwidth:A._sampwidth=2
				if A._sampwidth!=2:raise Error('sample width must be 2 when compressing with ulaw/ULAW, alaw/ALAW or G7.22 (ADPCM)')
			if not A._nchannels:raise Error('# channels not specified')
			if not A._sampwidth:raise Error('sample width not specified')
			if not A._framerate:raise Error('sampling rate not specified')
			A._write_header(datasize)
	def _init_compression(A):
		if A._comptype==_C:A._convert=A._lin2adpcm
		elif A._comptype in(_D,_E):A._convert=A._lin2ulaw
		elif A._comptype in(_F,_G):A._convert=A._lin2alaw
	def _write_header(A,initlength):
		if A._aifc and A._comptype!=_H:A._init_compression()
		A._file.write(b'FORM')
		if not A._nframes:A._nframes=initlength//(A._nchannels*A._sampwidth)
		A._datalength=A._nframes*A._nchannels*A._sampwidth
		if A._datalength&1:A._datalength=A._datalength+1
		if A._aifc:
			if A._comptype in(_D,_E,_F,_G):
				A._datalength=A._datalength//2
				if A._datalength&1:A._datalength=A._datalength+1
			elif A._comptype==_C:
				A._datalength=(A._datalength+3)//4
				if A._datalength&1:A._datalength=A._datalength+1
		try:A._form_length_pos=A._file.tell()
		except(AttributeError,OSError):A._form_length_pos=_A
		B=A._write_form_length(A._datalength)
		if A._aifc:A._file.write(b'AIFC');A._file.write(b'FVER');_write_ulong(A._file,4);_write_ulong(A._file,A._version)
		else:A._file.write(b'AIFF')
		A._file.write(b'COMM');_write_ulong(A._file,B);_write_short(A._file,A._nchannels)
		if A._form_length_pos is not _A:A._nframes_pos=A._file.tell()
		_write_ulong(A._file,A._nframes)
		if A._comptype in(_E,_D,_G,_F,_C):_write_short(A._file,8)
		else:_write_short(A._file,A._sampwidth*8)
		_write_float(A._file,A._framerate)
		if A._aifc:A._file.write(A._comptype);_write_string(A._file,A._compname)
		A._file.write(b'SSND')
		if A._form_length_pos is not _A:A._ssnd_length_pos=A._file.tell()
		_write_ulong(A._file,A._datalength+8);_write_ulong(A._file,0);_write_ulong(A._file,0)
	def _write_form_length(B,datalength):
		if B._aifc:
			A=18+5+len(B._compname)
			if A&1:A=A+1
			C=12
		else:A=18;C=0
		_write_ulong(B._file,4+C+B._marklength+8+A+16+datalength);return A
	def _patchheader(A):
		C=A._file.tell()
		if A._datawritten&1:B=A._datawritten+1;A._file.write(_I)
		else:B=A._datawritten
		if B==A._datalength and A._nframes==A._nframeswritten and A._marklength==0:A._file.seek(C,0);return
		A._file.seek(A._form_length_pos,0);D=A._write_form_length(B);A._file.seek(A._nframes_pos,0);_write_ulong(A._file,A._nframeswritten);A._file.seek(A._ssnd_length_pos,0);_write_ulong(A._file,B+8);A._file.seek(C,0);A._nframes=A._nframeswritten;A._datalength=B
	def _writemarkers(A):
		if len(A._markers)==0:return
		A._file.write(b'MARK');B=2
		for D in A._markers:
			id,E,C=D;B=B+len(C)+1+6
			if len(C)&1==0:B=B+1
		_write_ulong(A._file,B);A._marklength=B+8;_write_short(A._file,len(A._markers))
		for D in A._markers:id,E,C=D;_write_short(A._file,id);_write_ulong(A._file,E);_write_string(A._file,C)
def open(f,mode=_A):
	A=mode
	if A is _A:
		if hasattr(f,'mode'):A=f.mode
		else:A='rb'
	if A in('r','rb'):return Aifc_read(f)
	elif A in('w','wb'):return Aifc_write(f)
	else:raise Error("mode must be 'r', 'rb', 'w', or 'wb'")
def openfp(f,mode=_A):warnings.warn('aifc.openfp is deprecated since Python 3.7. Use aifc.open instead.',DeprecationWarning,stacklevel=2);return open(f,mode=mode)
if __name__=='__main__':
	import sys
	if not sys.argv[1:]:sys.argv.append('/usr/demos/data/audio/bach.aiff')
	fn=sys.argv[1]
	with open(fn,'r')as f:
		print('Reading',fn);print('nchannels =',f.getnchannels());print('nframes   =',f.getnframes());print('sampwidth =',f.getsampwidth());print('framerate =',f.getframerate());print('comptype  =',f.getcomptype());print('compname  =',f.getcompname())
		if sys.argv[2:]:
			gn=sys.argv[2];print('Writing',gn)
			with open(gn,'w')as g:
				g.setparams(f.getparams())
				while 1:
					data=f.readframes(1024)
					if not data:break
					g.writeframes(data)
			print('Done.')