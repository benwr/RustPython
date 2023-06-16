#! /usr/bin/env python3
'Conversions to/from quoted-printable transport encoding as per RFC 1521.'
_C=b'\n'
_B=False
_A=None
__all__=['encode','decode','encodestring','decodestring']
ESCAPE=b'='
MAXLINESIZE=76
HEX=b'0123456789ABCDEF'
EMPTYSTRING=b''
try:from binascii import a2b_qp,b2a_qp
except ImportError:a2b_qp=_A;b2a_qp=_A
def needsquoting(c,quotetabs,header):
	"Decide whether a particular byte ordinal needs to be quoted.\n\n    The 'quotetabs' flag indicates whether embedded tabs and spaces should be\n    quoted.  Note that line-ending tabs and spaces are always encoded, as per\n    RFC 1521.\n    ";assert isinstance(c,bytes)
	if c in b' \t':return quotetabs
	if c==b'_':return header
	return c==ESCAPE or not b' '<=c<=b'~'
def quote(c):'Quote a single character.';assert isinstance(c,bytes)and len(c)==1;c=ord(c);return ESCAPE+bytes((HEX[c//16],HEX[c%16]))
def encode(input,output,quotetabs,header=_B):
	"Read 'input', apply quoted-printable encoding, and write to 'output'.\n\n    'input' and 'output' are binary file objects. The 'quotetabs' flag\n    indicates whether embedded tabs and spaces should be quoted. Note that\n    line-ending tabs and spaces are always encoded, as per RFC 1521.\n    The 'header' flag indicates whether we are encoding spaces as _ as per RFC\n    1522.";H=quotetabs;I=output;E=header
	if b2a_qp is not _A:K=input.read();L=b2a_qp(K,quotetabs=H,header=E);I.write(L);return
	def F(s,output=I,lineEnd=_C):
		A=lineEnd;B=output
		if s and s[-1:]in b' \t':B.write(s[:-1]+quote(s[-1:])+A)
		elif s==b'.':B.write(quote(s)+A)
		else:B.write(s+A)
	B=_A
	while 1:
		C=input.readline()
		if not C:break
		G=[];J=b''
		if C[-1:]==_C:C=C[:-1];J=_C
		for A in C:
			A=bytes((A,))
			if needsquoting(A,H,E):A=quote(A)
			if E and A==b' ':G.append(b'_')
			else:G.append(A)
		if B is not _A:F(B)
		D=EMPTYSTRING.join(G)
		while len(D)>MAXLINESIZE:F(D[:MAXLINESIZE-1],lineEnd=b'=\n');D=D[MAXLINESIZE-1:]
		B=D
	if B is not _A:F(B,lineEnd=J)
def encodestring(s,quotetabs=_B,header=_B):
	A=header;B=quotetabs
	if b2a_qp is not _A:return b2a_qp(s,quotetabs=B,header=A)
	from io import BytesIO as C;E=C(s);D=C();encode(E,D,B,A);return D.getvalue()
def decode(input,output,header=_B):
	"Read 'input', apply quoted-printable decoding, and write to 'output'.\n    'input' and 'output' are binary file objects.\n    If 'header' is true, decode underscore as space (per RFC 1522).";H=header;G=output
	if a2b_qp is not _A:I=input.read();J=a2b_qp(I,header=H);G.write(J);return
	B=b''
	while 1:
		D=input.readline()
		if not D:break
		A,C=0,len(D)
		if C>0 and D[C-1:C]==_C:
			E=0;C=C-1
			while C>0 and D[C-1:C]in b' \t\r':C=C-1
		else:E=1
		while A<C:
			F=D[A:A+1]
			if F==b'_'and H:B=B+b' ';A=A+1
			elif F!=ESCAPE:B=B+F;A=A+1
			elif A+1==C and not E:E=1;break
			elif A+1<C and D[A+1:A+2]==ESCAPE:B=B+ESCAPE;A=A+2
			elif A+2<C and ishex(D[A+1:A+2])and ishex(D[A+2:A+3]):B=B+bytes((unhex(D[A+1:A+3]),));A=A+3
			else:B=B+F;A=A+1
		if not E:G.write(B+_C);B=b''
	if B:G.write(B)
def decodestring(s,header=_B):
	A=header
	if a2b_qp is not _A:return a2b_qp(s,header=A)
	from io import BytesIO as B;D=B(s);C=B();decode(D,C,header=A);return C.getvalue()
def ishex(c):"Return true if the byte ordinal 'c' is a hexadecimal digit in ASCII.";assert isinstance(c,bytes);return b'0'<=c<=b'9'or b'a'<=c<=b'f'or b'A'<=c<=b'F'
def unhex(s):
	'Get the integer value of a hexadecimal number.';B=0
	for A in s:
		A=bytes((A,))
		if b'0'<=A<=b'9':C=ord('0')
		elif b'a'<=A<=b'f':C=ord('a')-10
		elif b'A'<=A<=b'F':C=ord(b'A')-10
		else:assert _B,'non-hex digit '+repr(A)
		B=B*16+(ord(A)-C)
	return B
def main():
	D='-';import sys as A,getopt as J
	try:L,E=J.getopt(A.argv[1:],'td')
	except J.error as F:A.stdout=A.stderr;print(F);print('usage: quopri [-t | -d] [file] ...');print('-t: quote tabs');print('-d: decode; default encode');A.exit(2)
	G=_B;H=_B
	for(K,M)in L:
		if K=='-t':H=True
		if K=='-d':G=True
	if H and G:A.stdout=A.stderr;print('-t and -d are mutually exclusive');A.exit(2)
	if not E:E=[D]
	I=0
	for B in E:
		if B==D:C=A.stdin.buffer
		else:
			try:C=open(B,'rb')
			except OSError as F:A.stderr.write("%s: can't open (%s)\n"%(B,F));I=1;continue
		try:
			if G:decode(C,A.stdout.buffer)
			else:encode(C,A.stdout.buffer,H)
		finally:
			if B!=D:C.close()
	if I:A.exit(I)
if __name__=='__main__':main()