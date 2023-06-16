"Stuff to parse Sun and NeXT audio files.\n\nAn audio file consists of a header followed by the data.  The structure\nof the header is as follows.\n\n        +---------------+\n        | magic word    |\n        +---------------+\n        | header size   |\n        +---------------+\n        | data size     |\n        +---------------+\n        | encoding      |\n        +---------------+\n        | sample rate   |\n        +---------------+\n        | # of channels |\n        +---------------+\n        | info          |\n        |               |\n        +---------------+\n\nThe magic word consists of the 4 characters '.snd'.  Apart from the\ninfo field, all header fields are 4 bytes in size.  They are all\n32-bit unsigned integers encoded in big-endian byte order.\n\nThe header size really gives the start of the data.\nThe data size is the physical size of the data.  From the other\nparameters the number of frames can be calculated.\nThe encoding gives the way in which audio samples are encoded.\nPossible values are listed below.\nThe info field currently consists of an ASCII string giving a\nhuman-readable description of the audio file.  The info field is\npadded with NUL bytes to the header size.\n\nUsage.\n\nReading audio files:\n        f = sunau.open(file, 'r')\nwhere file is either the name of a file or an open file pointer.\nThe open file pointer must have methods read(), seek(), and close().\nWhen the setpos() and rewind() methods are not used, the seek()\nmethod is not  necessary.\n\nThis returns an instance of a class with the following public methods:\n        getnchannels()  -- returns number of audio channels (1 for\n                           mono, 2 for stereo)\n        getsampwidth()  -- returns sample width in bytes\n        getframerate()  -- returns sampling frequency\n        getnframes()    -- returns number of audio frames\n        getcomptype()   -- returns compression type ('NONE' or 'ULAW')\n        getcompname()   -- returns human-readable version of\n                           compression type ('not compressed' matches 'NONE')\n        getparams()     -- returns a namedtuple consisting of all of the\n                           above in the above order\n        getmarkers()    -- returns None (for compatibility with the\n                           aifc module)\n        getmark(id)     -- raises an error since the mark does not\n                           exist (for compatibility with the aifc module)\n        readframes(n)   -- returns at most n frames of audio\n        rewind()        -- rewind to the beginning of the audio stream\n        setpos(pos)     -- seek to the specified position\n        tell()          -- return the current position\n        close()         -- close the instance (make it unusable)\nThe position returned by tell() and the position given to setpos()\nare compatible and have nothing to do with the actual position in the\nfile.\nThe close() method is called automatically when the class instance\nis destroyed.\n\nWriting audio files:\n        f = sunau.open(file, 'w')\nwhere file is either the name of a file or an open file pointer.\nThe open file pointer must have methods write(), tell(), seek(), and\nclose().\n\nThis returns an instance of a class with the following public methods:\n        setnchannels(n) -- set the number of channels\n        setsampwidth(n) -- set the sample width\n        setframerate(n) -- set the frame rate\n        setnframes(n)   -- set the number of frames\n        setcomptype(type, name)\n                        -- set the compression type and the\n                           human-readable compression type\n        setparams(tuple)-- set all parameters at once\n        tell()          -- return current position in output file\n        writeframesraw(data)\n                        -- write audio frames without pathing up the\n                           file header\n        writeframes(data)\n                        -- write audio frames and patch up the file header\n        close()         -- patch up the file header and close the\n                           output file\nYou should set the parameters before the first writeframesraw or\nwriteframes.  The total number of frames does not need to be set,\nbut when it is set to the correct value, the header does not have to\nbe patched up.\nIt is best to first set all parameters, perhaps possibly the\ncompression type, and then write audio frames using writeframesraw.\nWhen all frames have been written, either call writeframes(b'') or\nclose() to patch up the sizes in the header.\nThe close() method is called automatically when the class instance\nis destroyed.\n"
_I='sample width not specified'
_H='not compressed'
_G='CCITT G.711 A-law'
_F='CCITT G.711 u-law'
_E='cannot seek'
_D='NONE'
_C='cannot change parameters after starting to write'
_B='ULAW'
_A=None
from collections import namedtuple
import warnings
_sunau_params=namedtuple('_sunau_params','nchannels sampwidth framerate nframes comptype compname')
AUDIO_FILE_MAGIC=779316836
AUDIO_FILE_ENCODING_MULAW_8=1
AUDIO_FILE_ENCODING_LINEAR_8=2
AUDIO_FILE_ENCODING_LINEAR_16=3
AUDIO_FILE_ENCODING_LINEAR_24=4
AUDIO_FILE_ENCODING_LINEAR_32=5
AUDIO_FILE_ENCODING_FLOAT=6
AUDIO_FILE_ENCODING_DOUBLE=7
AUDIO_FILE_ENCODING_ADPCM_G721=23
AUDIO_FILE_ENCODING_ADPCM_G722=24
AUDIO_FILE_ENCODING_ADPCM_G723_3=25
AUDIO_FILE_ENCODING_ADPCM_G723_5=26
AUDIO_FILE_ENCODING_ALAW_8=27
AUDIO_UNKNOWN_SIZE=4294967295
_simple_encodings=[AUDIO_FILE_ENCODING_MULAW_8,AUDIO_FILE_ENCODING_LINEAR_8,AUDIO_FILE_ENCODING_LINEAR_16,AUDIO_FILE_ENCODING_LINEAR_24,AUDIO_FILE_ENCODING_LINEAR_32,AUDIO_FILE_ENCODING_ALAW_8]
class Error(Exception):0
def _read_u32(file):
	A=0
	for C in range(4):
		B=file.read(1)
		if not B:raise EOFError
		A=A*256+ord(B)
	return A
def _write_u32(file,x):
	A=[]
	for D in range(4):B,C=divmod(x,256);A.insert(0,int(C));x=B
	file.write(bytes(A))
class Au_read:
	def __init__(A,f):
		if type(f)==type(''):import builtins as B;f=B.open(f,'rb');A._opened=True
		else:A._opened=False
		A.initfp(f)
	def __del__(A):
		if A._file:A.close()
	def __enter__(A):return A
	def __exit__(A,*B):A.close()
	def initfp(A,file):
		B=file;A._file=B;A._soundpos=0;C=int(_read_u32(B))
		if C!=AUDIO_FILE_MAGIC:raise Error('bad magic number')
		A._hdr_size=int(_read_u32(B))
		if A._hdr_size<24:raise Error('header size too small')
		if A._hdr_size>100:raise Error('header size ridiculously large')
		A._data_size=_read_u32(B)
		if A._data_size!=AUDIO_UNKNOWN_SIZE:A._data_size=int(A._data_size)
		A._encoding=int(_read_u32(B))
		if A._encoding not in _simple_encodings:raise Error('encoding not (yet) supported')
		if A._encoding in(AUDIO_FILE_ENCODING_MULAW_8,AUDIO_FILE_ENCODING_ALAW_8):A._sampwidth=2;A._framesize=1
		elif A._encoding==AUDIO_FILE_ENCODING_LINEAR_8:A._framesize=A._sampwidth=1
		elif A._encoding==AUDIO_FILE_ENCODING_LINEAR_16:A._framesize=A._sampwidth=2
		elif A._encoding==AUDIO_FILE_ENCODING_LINEAR_24:A._framesize=A._sampwidth=3
		elif A._encoding==AUDIO_FILE_ENCODING_LINEAR_32:A._framesize=A._sampwidth=4
		else:raise Error('unknown encoding')
		A._framerate=int(_read_u32(B));A._nchannels=int(_read_u32(B))
		if not A._nchannels:raise Error('bad # of channels')
		A._framesize=A._framesize*A._nchannels
		if A._hdr_size>24:A._info=B.read(A._hdr_size-24);A._info,D,D=A._info.partition(b'\x00')
		else:A._info=b''
		try:A._data_pos=B.tell()
		except(AttributeError,OSError):A._data_pos=_A
	def getfp(A):return A._file
	def getnchannels(A):return A._nchannels
	def getsampwidth(A):return A._sampwidth
	def getframerate(A):return A._framerate
	def getnframes(A):
		if A._data_size==AUDIO_UNKNOWN_SIZE:return AUDIO_UNKNOWN_SIZE
		if A._encoding in _simple_encodings:return A._data_size//A._framesize
		return 0
	def getcomptype(A):
		if A._encoding==AUDIO_FILE_ENCODING_MULAW_8:return _B
		elif A._encoding==AUDIO_FILE_ENCODING_ALAW_8:return'ALAW'
		else:return _D
	def getcompname(A):
		if A._encoding==AUDIO_FILE_ENCODING_MULAW_8:return _F
		elif A._encoding==AUDIO_FILE_ENCODING_ALAW_8:return _G
		else:return _H
	def getparams(A):return _sunau_params(A.getnchannels(),A.getsampwidth(),A.getframerate(),A.getnframes(),A.getcomptype(),A.getcompname())
	def getmarkers(A):0
	def getmark(A,id):raise Error('no marks')
	def readframes(A,nframes):
		C=nframes
		if A._encoding in _simple_encodings:
			if C==AUDIO_UNKNOWN_SIZE:B=A._file.read()
			else:B=A._file.read(C*A._framesize)
			A._soundpos+=len(B)//A._framesize
			if A._encoding==AUDIO_FILE_ENCODING_MULAW_8:import audioop as D;B=D.ulaw2lin(B,A._sampwidth)
			return B
	def rewind(A):
		if A._data_pos is _A:raise OSError(_E)
		A._file.seek(A._data_pos);A._soundpos=0
	def tell(A):return A._soundpos
	def setpos(A,pos):
		B=pos
		if B<0 or B>A.getnframes():raise Error('position not in range')
		if A._data_pos is _A:raise OSError(_E)
		A._file.seek(A._data_pos+B*A._framesize);A._soundpos=B
	def close(A):
		B=A._file
		if B:
			A._file=_A
			if A._opened:B.close()
class Au_write:
	def __init__(A,f):
		if type(f)==type(''):import builtins as B;f=B.open(f,'wb');A._opened=True
		else:A._opened=False
		A.initfp(f)
	def __del__(A):
		if A._file:A.close()
		A._file=_A
	def __enter__(A):return A
	def __exit__(A,*B):A.close()
	def initfp(A,file):A._file=file;A._framerate=0;A._nchannels=0;A._sampwidth=0;A._framesize=0;A._nframes=AUDIO_UNKNOWN_SIZE;A._nframeswritten=0;A._datawritten=0;A._datalength=0;A._info=b'';A._comptype=_B
	def setnchannels(A,nchannels):
		B=nchannels
		if A._nframeswritten:raise Error(_C)
		if B not in(1,2,4):raise Error('only 1, 2, or 4 channels supported')
		A._nchannels=B
	def getnchannels(A):
		if not A._nchannels:raise Error('number of channels not set')
		return A._nchannels
	def setsampwidth(A,sampwidth):
		B=sampwidth
		if A._nframeswritten:raise Error(_C)
		if B not in(1,2,3,4):raise Error('bad sample width')
		A._sampwidth=B
	def getsampwidth(A):
		if not A._framerate:raise Error(_I)
		return A._sampwidth
	def setframerate(A,framerate):
		if A._nframeswritten:raise Error(_C)
		A._framerate=framerate
	def getframerate(A):
		if not A._framerate:raise Error('frame rate not set')
		return A._framerate
	def setnframes(A,nframes):
		B=nframes
		if A._nframeswritten:raise Error(_C)
		if B<0:raise Error('# of frames cannot be negative')
		A._nframes=B
	def getnframes(A):return A._nframeswritten
	def setcomptype(A,type,name):
		if type in(_D,_B):A._comptype=type
		else:raise Error('unknown compression type')
	def getcomptype(A):return A._comptype
	def getcompname(A):
		if A._comptype==_B:return _F
		elif A._comptype=='ALAW':return _G
		else:return _H
	def setparams(A,params):B,C,D,E,F,G=params;A.setnchannels(B);A.setsampwidth(C);A.setframerate(D);A.setnframes(E);A.setcomptype(F,G)
	def getparams(A):return _sunau_params(A.getnchannels(),A.getsampwidth(),A.getframerate(),A.getnframes(),A.getcomptype(),A.getcompname())
	def tell(A):return A._nframeswritten
	def writeframesraw(A,data):
		B=data
		if not isinstance(B,(bytes,bytearray)):B=memoryview(B).cast('B')
		A._ensure_header_written()
		if A._comptype==_B:import audioop as C;B=C.lin2ulaw(B,A._sampwidth)
		D=len(B)//A._framesize;A._file.write(B);A._nframeswritten=A._nframeswritten+D;A._datawritten=A._datawritten+len(B)
	def writeframes(A,data):
		A.writeframesraw(data)
		if A._nframeswritten!=A._nframes or A._datalength!=A._datawritten:A._patchheader()
	def close(A):
		if A._file:
			try:
				A._ensure_header_written()
				if A._nframeswritten!=A._nframes or A._datalength!=A._datawritten:A._patchheader()
				A._file.flush()
			finally:
				B=A._file;A._file=_A
				if A._opened:B.close()
	def _ensure_header_written(A):
		if not A._nframeswritten:
			if not A._nchannels:raise Error('# of channels not specified')
			if not A._sampwidth:raise Error(_I)
			if not A._framerate:raise Error('frame rate not specified')
			A._write_header()
	def _write_header(A):
		E='internal error'
		if A._comptype==_D:
			if A._sampwidth==1:B=AUDIO_FILE_ENCODING_LINEAR_8;A._framesize=1
			elif A._sampwidth==2:B=AUDIO_FILE_ENCODING_LINEAR_16;A._framesize=2
			elif A._sampwidth==3:B=AUDIO_FILE_ENCODING_LINEAR_24;A._framesize=3
			elif A._sampwidth==4:B=AUDIO_FILE_ENCODING_LINEAR_32;A._framesize=4
			else:raise Error(E)
		elif A._comptype==_B:B=AUDIO_FILE_ENCODING_MULAW_8;A._framesize=1
		else:raise Error(E)
		A._framesize=A._framesize*A._nchannels;_write_u32(A._file,AUDIO_FILE_MAGIC);C=25+len(A._info);C=C+7&~7;_write_u32(A._file,C)
		if A._nframes==AUDIO_UNKNOWN_SIZE:D=AUDIO_UNKNOWN_SIZE
		else:D=A._nframes*A._framesize
		try:A._form_length_pos=A._file.tell()
		except(AttributeError,OSError):A._form_length_pos=_A
		_write_u32(A._file,D);A._datalength=D;_write_u32(A._file,B);_write_u32(A._file,A._framerate);_write_u32(A._file,A._nchannels);A._file.write(A._info);A._file.write(b'\x00'*(C-len(A._info)-24))
	def _patchheader(A):
		if A._form_length_pos is _A:raise OSError(_E)
		A._file.seek(A._form_length_pos);_write_u32(A._file,A._datawritten);A._datalength=A._datawritten;A._file.seek(0,2)
def open(f,mode=_A):
	A=mode
	if A is _A:
		if hasattr(f,'mode'):A=f.mode
		else:A='rb'
	if A in('r','rb'):return Au_read(f)
	elif A in('w','wb'):return Au_write(f)
	else:raise Error("mode must be 'r', 'rb', 'w', or 'wb'")
def openfp(f,mode=_A):warnings.warn('sunau.openfp is deprecated since Python 3.7. Use sunau.open instead.',DeprecationWarning,stacklevel=2);return open(f,mode=mode)