#! /usr/bin/env python3
'Base16, Base32, Base64 (RFC 3548), Base85 and Ascii85 data encodings'
_E='base32hex'
_D='base32'
_C=b'+/'
_B=False
_A=None
import re,struct,binascii
__all__=['encode','decode','encodebytes','decodebytes','b64encode','b64decode','b32encode','b32decode','b32hexencode','b32hexdecode','b16encode','b16decode','b85encode','b85decode','a85encode','a85decode','standard_b64encode','standard_b64decode','urlsafe_b64encode','urlsafe_b64decode']
bytes_types=bytes,bytearray
def _bytes_from_decode_data(s):
	if isinstance(s,str):
		try:return s.encode('ascii')
		except UnicodeEncodeError:raise ValueError('string argument should contain only ASCII characters')
	if isinstance(s,bytes_types):return s
	try:return memoryview(s).tobytes()
	except TypeError:raise TypeError('argument should be a bytes-like object or ASCII string, not %r'%s.__class__.__name__)from _A
def b64encode(s,altchars=_A):
	"Encode the bytes-like object s using Base64 and return a bytes object.\n\n    Optional altchars should be a byte string of length 2 which specifies an\n    alternative alphabet for the '+' and '/' characters.  This allows an\n    application to e.g. generate url or filesystem safe Base64 strings.\n    ";A=altchars;B=binascii.b2a_base64(s,newline=_B)
	if A is not _A:assert len(A)==2,repr(A);return B.translate(bytes.maketrans(_C,A))
	return B
def b64decode(s,altchars=_A,validate=_B):
	"Decode the Base64 encoded bytes-like object or ASCII string s.\n\n    Optional altchars must be a bytes-like object or ASCII string of length 2\n    which specifies the alternative alphabet used instead of the '+' and '/'\n    characters.\n\n    The result is returned as a bytes object.  A binascii.Error is raised if\n    s is incorrectly padded.\n\n    If validate is False (the default), characters that are neither in the\n    normal base-64 alphabet nor the alternative alphabet are discarded prior\n    to the padding check.  If validate is True, these non-alphabet characters\n    in the input result in a binascii.Error.\n    For more information about the strict base64 check, see:\n\n    https://docs.python.org/3.11/library/binascii.html#binascii.a2b_base64\n    ";A=altchars;s=_bytes_from_decode_data(s)
	if A is not _A:A=_bytes_from_decode_data(A);assert len(A)==2,repr(A);s=s.translate(bytes.maketrans(A,_C))
	return binascii.a2b_base64(s,strict_mode=validate)
def standard_b64encode(s):'Encode bytes-like object s using the standard Base64 alphabet.\n\n    The result is returned as a bytes object.\n    ';return b64encode(s)
def standard_b64decode(s):'Decode bytes encoded with the standard Base64 alphabet.\n\n    Argument s is a bytes-like object or ASCII string to decode.  The result\n    is returned as a bytes object.  A binascii.Error is raised if the input\n    is incorrectly padded.  Characters that are not in the standard alphabet\n    are discarded prior to the padding check.\n    ';return b64decode(s)
_urlsafe_encode_translation=bytes.maketrans(_C,b'-_')
_urlsafe_decode_translation=bytes.maketrans(b'-_',_C)
def urlsafe_b64encode(s):"Encode bytes using the URL- and filesystem-safe Base64 alphabet.\n\n    Argument s is a bytes-like object to encode.  The result is returned as a\n    bytes object.  The alphabet uses '-' instead of '+' and '_' instead of\n    '/'.\n    ";return b64encode(s).translate(_urlsafe_encode_translation)
def urlsafe_b64decode(s):"Decode bytes using the URL- and filesystem-safe Base64 alphabet.\n\n    Argument s is a bytes-like object or ASCII string to decode.  The result\n    is returned as a bytes object.  A binascii.Error is raised if the input\n    is incorrectly padded.  Characters that are not in the URL-safe base-64\n    alphabet, and are not a plus '+' or slash '/', are discarded prior to the\n    padding check.\n\n    The alphabet uses '-' instead of '+' and '_' instead of '/'.\n    ";s=_bytes_from_decode_data(s);s=s.translate(_urlsafe_decode_translation);return b64decode(s)
_B32_ENCODE_DOCSTRING='\nEncode the bytes-like objects using {encoding} and return a bytes object.\n'
_B32_DECODE_DOCSTRING='\nDecode the {encoding} encoded bytes-like object or ASCII string s.\n\nOptional casefold is a flag specifying whether a lowercase alphabet is\nacceptable as input.  For security purposes, the default is False.\n{extra_args}\nThe result is returned as a bytes object.  A binascii.Error is raised if\nthe input is incorrectly padded or if there are non-alphabet\ncharacters present in the input.\n'
_B32_DECODE_MAP01_DOCSTRING='\nRFC 3548 allows for optional mapping of the digit 0 (zero) to the\nletter O (oh), and for optional mapping of the digit 1 (one) to\neither the letter I (eye) or letter L (el).  The optional argument\nmap01 when not None, specifies which letter the digit 1 should be\nmapped to (when map01 is not None, the digit 0 is always mapped to\nthe letter O).  For security purposes the default is None, so that\n0 and 1 are not allowed in the input.\n'
_b32alphabet=b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
_b32hexalphabet=b'0123456789ABCDEFGHIJKLMNOPQRSTUV'
_b32tab2={}
_b32rev={}
def _b32encode(alphabet,s):
	C=alphabet;global _b32tab2
	if C not in _b32tab2:F=[bytes((A,))for A in C];_b32tab2[C]=[A+B for A in F for B in F];F=_A
	if not isinstance(s,bytes_types):s=memoryview(s).tobytes()
	A=len(s)%5
	if A:s=s+b'\x00'*(5-A)
	B=bytearray();H=int.from_bytes;D=_b32tab2[C]
	for G in range(0,len(s),5):E=H(s[G:G+5]);B+=D[E>>30]+D[E>>20&1023]+D[E>>10&1023]+D[E&1023]
	if A==1:B[-6:]=b'======'
	elif A==2:B[-4:]=b'===='
	elif A==3:B[-3:]=b'==='
	elif A==4:B[-1:]=b'='
	return bytes(B)
def _b32decode(alphabet,s,casefold=_B,map01=_A):
	F='Incorrect padding';C=alphabet;A=map01;global _b32rev
	if C not in _b32rev:_b32rev[C]={B:A for(A,B)in enumerate(C)}
	s=_bytes_from_decode_data(s)
	if len(s)%8:raise binascii.Error(F)
	if A is not _A:A=_bytes_from_decode_data(A);assert len(A)==1,repr(A);s=s.translate(bytes.maketrans(b'01',b'O'+A))
	if casefold:s=s.upper()
	G=len(s);s=s.rstrip(b'=');D=G-len(s);E=bytearray();I=_b32rev[C]
	for H in range(0,len(s),8):
		J=s[H:H+8];B=0
		try:
			for K in J:B=(B<<5)+I[K]
		except KeyError:raise binascii.Error('Non-base32 digit found')from _A
		E+=B.to_bytes(5)
	if G%8 or D not in{0,1,3,4,6}:raise binascii.Error(F)
	if D and E:B<<=5*D;L=B.to_bytes(5);M=(43-5*D)//8;E[-5:]=L[:M]
	return bytes(E)
def b32encode(s):return _b32encode(_b32alphabet,s)
b32encode.__doc__=_B32_ENCODE_DOCSTRING.format(encoding=_D)
def b32decode(s,casefold=_B,map01=_A):return _b32decode(_b32alphabet,s,casefold,map01)
b32decode.__doc__=_B32_DECODE_DOCSTRING.format(encoding=_D,extra_args=_B32_DECODE_MAP01_DOCSTRING)
def b32hexencode(s):return _b32encode(_b32hexalphabet,s)
b32hexencode.__doc__=_B32_ENCODE_DOCSTRING.format(encoding=_E)
def b32hexdecode(s,casefold=_B):return _b32decode(_b32hexalphabet,s,casefold)
b32hexdecode.__doc__=_B32_DECODE_DOCSTRING.format(encoding=_E,extra_args='')
def b16encode(s):'Encode the bytes-like object s using Base16 and return a bytes object.\n    ';return binascii.hexlify(s).upper()
def b16decode(s,casefold=_B):
	'Decode the Base16 encoded bytes-like object or ASCII string s.\n\n    Optional casefold is a flag specifying whether a lowercase alphabet is\n    acceptable as input.  For security purposes, the default is False.\n\n    The result is returned as a bytes object.  A binascii.Error is raised if\n    s is incorrectly padded or if there are non-alphabet characters present\n    in the input.\n    ';s=_bytes_from_decode_data(s)
	if casefold:s=s.upper()
	if re.search(b'[^0-9A-F]',s):raise binascii.Error('Non-base16 digit found')
	return binascii.unhexlify(s)
_a85chars=_A
_a85chars2=_A
_A85START=b'<~'
_A85END=b'~>'
def _85encode(b,chars,chars2,pad=_B,foldnuls=_B,foldspaces=_B):
	C=chars2;D=chars
	if not isinstance(b,bytes_types):b=memoryview(b).tobytes()
	B=-len(b)%4
	if B:b=b+b'\x00'*B
	E=struct.Struct('!%dI'%(len(b)//4)).unpack(b);A=[b'z'if foldnuls and not A else b'y'if foldspaces and A==538976288 else C[A//614125]+C[A//85%7225]+D[A%85]for A in E]
	if B and not pad:
		if A[-1]==b'z':A[-1]=D[0]*5
		A[-1]=A[-1][:-B]
	return b''.join(A)
def a85encode(b,*,foldspaces=_B,wrapcol=0,pad=_B,adobe=_B):
	'Encode bytes-like object b using Ascii85 and return a bytes object.\n\n    foldspaces is an optional flag that uses the special short sequence \'y\'\n    instead of 4 consecutive spaces (ASCII 0x20) as supported by \'btoa\'. This\n    feature is not supported by the "standard" Adobe encoding.\n\n    wrapcol controls whether the output should have newline (b\'\\n\') characters\n    added to it. If this is non-zero, each output line will be at most this\n    many characters long.\n\n    pad controls whether the input is padded to a multiple of 4 before\n    encoding. Note that the btoa implementation always pads.\n\n    adobe controls whether the encoded byte sequence is framed with <~ and ~>,\n    which is used by the Adobe implementation.\n    ';C=adobe;B=wrapcol;global _a85chars,_a85chars2
	if _a85chars2 is _A:_a85chars=[bytes((A,))for A in range(33,118)];_a85chars2=[A+B for A in _a85chars for B in _a85chars]
	A=_85encode(b,_a85chars,_a85chars2,pad,True,foldspaces)
	if C:A=_A85START+A
	if B:
		B=max(2 if C else 1,B);D=[A[C:C+B]for C in range(0,len(A),B)]
		if C:
			if len(D[-1])+2>B:D.append(b'')
		A=b'\n'.join(D)
	if C:A+=_A85END
	return A
def a85decode(b,*,foldspaces=_B,adobe=_B,ignorechars=b' \t\n\r\x0b'):
	'Decode the Ascii85 encoded bytes-like object or ASCII string b.\n\n    foldspaces is a flag that specifies whether the \'y\' short sequence should be\n    accepted as shorthand for 4 consecutive spaces (ASCII 0x20). This feature is\n    not supported by the "standard" Adobe encoding.\n\n    adobe controls whether the input sequence is in Adobe Ascii85 format (i.e.\n    is framed with <~ and ~>).\n\n    ignorechars should be a byte string containing characters to ignore from the\n    input. This should only contain whitespace characters, and by default\n    contains all whitespace characters in ASCII.\n\n    The result is returned as a bytes object.\n    ';b=_bytes_from_decode_data(b)
	if adobe:
		if not b.endswith(_A85END):raise ValueError('Ascii85 encoded byte sequences must end with {!r}'.format(_A85END))
		if b.startswith(_A85START):b=b[2:-2]
		else:b=b[:-2]
	H=struct.Struct('!I').pack;F=[];C=F.append;B=[];I=B.append;J=B.clear
	for A in b+b'u'*4:
		if b'!'[0]<=A<=b'u'[0]:
			I(A)
			if len(B)==5:
				D=0
				for A in B:D=85*D+(A-33)
				try:C(H(D))
				except struct.error:raise ValueError('Ascii85 overflow')from _A
				J()
		elif A==b'z'[0]:
			if B:raise ValueError('z inside Ascii85 5-tuple')
			C(b'\x00\x00\x00\x00')
		elif foldspaces and A==b'y'[0]:
			if B:raise ValueError('y inside Ascii85 5-tuple')
			C(b'    ')
		elif A in ignorechars:continue
		else:raise ValueError('Non-Ascii85 digit found: %c'%A)
	E=b''.join(F);G=4-len(B)
	if G:E=E[:-G]
	return E
_b85alphabet=b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'
_b85chars=_A
_b85chars2=_A
_b85dec=_A
def b85encode(b,pad=_B):
	"Encode bytes-like object b in base85 format and return a bytes object.\n\n    If pad is true, the input is padded with b'\\0' so its length is a multiple of\n    4 bytes before encoding.\n    ";global _b85chars,_b85chars2
	if _b85chars2 is _A:_b85chars=[bytes((A,))for A in _b85alphabet];_b85chars2=[A+B for A in _b85chars for B in _b85chars]
	return _85encode(b,_b85chars,_b85chars2,pad)
def b85decode(b):
	'Decode the base85-encoded bytes-like object or ASCII string b\n\n    The result is returned as a bytes object.\n    ';global _b85dec
	if _b85dec is _A:
		_b85dec=[_A]*256
		for(A,B)in enumerate(_b85alphabet):_b85dec[B]=A
	b=_bytes_from_decode_data(b);C=-len(b)%5;b=b+b'~'*C;F=[];H=struct.Struct('!I').pack
	for A in range(0,len(b),5):
		G=b[A:A+5];D=0
		try:
			for B in G:D=D*85+_b85dec[B]
		except TypeError:
			for(I,B)in enumerate(G):
				if _b85dec[B]is _A:raise ValueError('bad base85 character at position %d'%(A+I))from _A
			raise
		try:F.append(H(D))
		except struct.error:raise ValueError('base85 overflow in hunk starting at byte %d'%A)from _A
	E=b''.join(F)
	if C:E=E[:-C]
	return E
MAXLINESIZE=76
MAXBINSIZE=MAXLINESIZE//4*3
def encode(input,output):
	'Encode a file; input and output are binary files.'
	while True:
		A=input.read(MAXBINSIZE)
		if not A:break
		while len(A)<MAXBINSIZE:
			B=input.read(MAXBINSIZE-len(A))
			if not B:break
			A+=B
		C=binascii.b2a_base64(A);output.write(C)
def decode(input,output):
	'Decode a file; input and output are binary files.'
	while True:
		A=input.readline()
		if not A:break
		B=binascii.a2b_base64(A);output.write(B)
def _input_type_check(s):
	try:B=memoryview(s)
	except TypeError as C:A='expected bytes-like object, not %s'%s.__class__.__name__;raise TypeError(A)from C
	if B.format not in('c','b','B'):A='expected single byte elements, not %r from %s'%(B.format,s.__class__.__name__);raise TypeError(A)
	if B.ndim!=1:A='expected 1-D data, not %d-D data from %s'%(B.ndim,s.__class__.__name__);raise TypeError(A)
def encodebytes(s):
	'Encode a bytestring into a bytes object containing multiple lines\n    of base-64 data.';_input_type_check(s);A=[]
	for B in range(0,len(s),MAXBINSIZE):C=s[B:B+MAXBINSIZE];A.append(binascii.b2a_base64(C))
	return b''.join(A)
def decodebytes(s):'Decode a bytestring of base-64 data into a bytes object.';_input_type_check(s);return binascii.a2b_base64(s)
def main():
	'Small main program';import sys as A,getopt as E;F="usage: %s [-h|-d|-e|-u|-t] [file|-]\n        -h: print this help message and exit\n        -d, -u: decode\n        -e: encode (default)\n        -t: encode and decode string 'Aladdin:open sesame'"%A.argv[0]
	try:G,D=E.getopt(A.argv[1:],'hdeut')
	except E.error as H:A.stdout=A.stderr;print(H);print(F);A.exit(2)
	B=encode
	for(C,J)in G:
		if C=='-e':B=encode
		if C=='-d':B=decode
		if C=='-u':B=decode
		if C=='-t':test();return
		if C=='-h':print(F);return
	if D and D[0]!='-':
		with open(D[0],'rb')as I:B(I,A.stdout.buffer)
	else:B(A.stdin.buffer,A.stdout.buffer)
def test():A=b'Aladdin:open sesame';print(repr(A));B=encodebytes(A);print(repr(B));C=decodebytes(B);print(repr(C));assert A==C
if __name__=='__main__':main()