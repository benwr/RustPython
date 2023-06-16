'Convert a NT pathname to a file URL and vice versa.'
_A='\\'
def url2pathname(url):
	"OS-specific conversion from a relative URL of the 'file' scheme\n    to a file system path; not recommended for general use.";D='|';A=url;import string as F,urllib.parse;A=A.replace(':',D)
	if not D in A:
		if A[:4]=='////':A=A[2:]
		E=A.split('/');return urllib.parse.unquote(_A.join(E))
	B=A.split(D)
	if len(B)!=2 or B[0][-1]not in F.ascii_letters:G='Bad URL: '+A;raise OSError(G)
	H=B[0][-1].upper();E=B[1].split('/');C=H+':'
	for B in E:
		if B:C=C+_A+urllib.parse.unquote(B)
	if C.endswith(':')and A.endswith('/'):C+=_A
	return C
def pathname2url(p):
	"OS-specific conversion from a file system path to a relative URL\n    of the 'file' scheme; not recommended for general use.";D='\\\\';import urllib.parse
	if not':'in p:
		if p[:2]==D:p=D+p
		B=p.split(_A);return urllib.parse.quote('/'.join(B))
	A=p.split(':')
	if len(A)!=2 or len(A[0])>1:E='Bad path: '+p;raise OSError(E)
	F=urllib.parse.quote(A[0].upper());B=A[1].split(_A);C='///'+F+':'
	for A in B:
		if A:C=C+'/'+urllib.parse.quote(A)
	return C