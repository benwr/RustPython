'Routines to help recognizing sound files.\n\nFunction whathdr() recognizes various types of sound file headers.\nIt understands almost all headers that SOX can decode.\n\nThe return tuple contains the following items, in this order:\n- file type (as SOX understands it)\n- sampling rate (0 if unknown or hard to decode)\n- number of channels (0 if unknown or hard to decode)\n- number of frames in the file (-1 if unknown or hard to decode)\n- number of bits/sample, or \'U\' for U-LAW, or \'A\' for A-LAW\n\nIf the file doesn\'t have a recognizable type, it returns None.\nIf the file can\'t be opened, OSError is raised.\n\nTo compute the total time, divide the number of frames by the\nsampling rate (a frame contains a sample for each channel).\n\nFunction what() calls whathdr().  (It used to also use some\nheuristics for raw data, but this doesn\'t work very well.)\n\nFinally, the function test() is a simple main program that calls\nwhat() for all files mentioned on the argument list.  For directory\narguments it calls what() for all files in that directory.  Default\nargument is "." (testing all files in the current directory).  The\noption -r tells it to recurse down directories found inside\nexplicitly given directories.\n'
__all__=['what','whathdr']
from collections import namedtuple
SndHeaders=namedtuple('SndHeaders','filetype framerate nchannels nframes sampwidth')
SndHeaders.filetype.__doc__="The value for type indicates the data type\nand will be one of the strings 'aifc', 'aiff', 'au','hcom',\n'sndr', 'sndt', 'voc', 'wav', '8svx', 'sb', 'ub', or 'ul'."
SndHeaders.framerate.__doc__='The sampling_rate will be either the actual\nvalue or 0 if unknown or difficult to decode.'
SndHeaders.nchannels.__doc__='The number of channels or 0 if it cannot be\ndetermined or if the value is difficult to decode.'
SndHeaders.nframes.__doc__='The value for frames will be either the number\nof frames or -1.'
SndHeaders.sampwidth.__doc__="Either the sample size in bits or\n'A' for A-LAW or 'U' for u-LAW."
def what(filename):'Guess the type of a sound file.';A=whathdr(filename);return A
def whathdr(filename):
	'Recognize sound headers.'
	with open(filename,'rb')as A:
		C=A.read(512)
		for D in tests:
			B=D(C,A)
			if B:return SndHeaders(*B)
		return
tests=[]
def test_aifc(h,f):
	import aifc as B
	if not h.startswith(b'FORM'):return
	if h[8:12]==b'AIFC':C='aifc'
	elif h[8:12]==b'AIFF':C='aiff'
	else:return
	f.seek(0)
	try:A=B.open(f,'r')
	except(EOFError,B.Error):return
	return C,A.getframerate(),A.getnchannels(),A.getnframes(),8*A.getsampwidth()
tests.append(test_aifc)
def test_au(h,f):
	if h.startswith(b'.snd'):A=get_long_be
	elif h[:4]in(b'\x00ds.',b'dns.'):A=get_long_le
	else:return
	H='au';K=A(h[4:8]);I=A(h[8:12]);C=A(h[12:16]);J=A(h[16:20]);D=A(h[20:24]);E=1
	if C==1:B='U'
	elif C==2:B=8
	elif C==3:B=16;E=2
	else:B='?'
	F=E*D
	if F:G=I/F
	else:G=-1
	return H,J,D,G,B
tests.append(test_au)
def test_hcom(h,f):
	if h[65:69]!=b'FSSD'or h[128:132]!=b'HCOM':return
	A=get_long_be(h[144:148])
	if A:B=22050/A
	else:B=0
	return'hcom',B,1,-1,8
tests.append(test_hcom)
def test_voc(h,f):
	if not h.startswith(b'Creative Voice File\x1a'):return
	A=get_short_le(h[20:22]);B=0
	if 0<=A<500 and h[A]==1:
		C=256-h[A+4]
		if C:B=int(1e6/C)
	return'voc',B,1,-1,8
tests.append(test_voc)
def test_wav(h,f):
	import wave as B
	if not h.startswith(b'RIFF')or h[8:12]!=b'WAVE'or h[12:16]!=b'fmt ':return
	f.seek(0)
	try:A=B.open(f,'r')
	except(EOFError,B.Error):return
	return'wav',A.getframerate(),A.getnchannels(),A.getnframes(),8*A.getsampwidth()
tests.append(test_wav)
def test_8svx(h,f):
	if not h.startswith(b'FORM')or h[8:12]!=b'8SVX':return
	return'8svx',0,1,0,8
tests.append(test_8svx)
def test_sndt(h,f):
	if h.startswith(b'SOUND'):A=get_long_le(h[8:12]);B=get_short_le(h[20:22]);return'sndt',B,1,A,8
tests.append(test_sndt)
def test_sndr(h,f):
	if h.startswith(b'\x00\x00'):
		A=get_short_le(h[2:4])
		if 4000<=A<=25000:return'sndr',A,1,-1,8
tests.append(test_sndr)
def get_long_be(b):return b[0]<<24|b[1]<<16|b[2]<<8|b[3]
def get_long_le(b):return b[3]<<24|b[2]<<16|b[1]<<8|b[0]
def get_short_be(b):return b[0]<<8|b[1]
def get_short_le(b):return b[1]<<8|b[0]
def test():
	import sys as A;B=0
	if A.argv[1:]and A.argv[1]=='-r':del A.argv[1:2];B=1
	try:
		if A.argv[1:]:testall(A.argv[1:],B,1)
		else:testall(['.'],B,1)
	except KeyboardInterrupt:A.stderr.write('\n[Interrupted]\n');A.exit(1)
def testall(list,recursive,toplevel):
	B=recursive;import sys,os
	for A in list:
		if os.path.isdir(A):
			print(A+'/:',end=' ')
			if B or toplevel:print('recursing down:');import glob;C=glob.glob(os.path.join(A,'*'));testall(C,B,0)
			else:print('*** directory (use -r) ***')
		else:
			print(A+':',end=' ');sys.stdout.flush()
			try:print(what(A))
			except OSError:print('*** not found ***')
if __name__=='__main__':test()