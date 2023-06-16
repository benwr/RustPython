'Filename matching with shell patterns.\n\nfnmatch(FILENAME, PATTERN) matches according to the local convention.\nfnmatchcase(FILENAME, PATTERN) always takes case in account.\n\nThe functions operate by translating the pattern into a regular\nexpression.  They cache the compiled regular expressions for speed.\n\nThe function translate(PATTERN) returns a regular expression\ncorresponding to PATTERN.  (It does not compile it.)\n'
import os,posixpath,re,functools
__all__=['filter','fnmatch','fnmatchcase','translate']
from itertools import count
_nextgroupnum=count().__next__
del count
def fnmatch(name,pat):"Test whether FILENAME matches PATTERN.\n\n    Patterns are Unix shell style:\n\n    *       matches everything\n    ?       matches any single character\n    [seq]   matches any character in seq\n    [!seq]  matches any char not in seq\n\n    An initial period in FILENAME is not special.\n    Both FILENAME and PATTERN are first case-normalized\n    if the operating system requires it.\n    If you don't want this, use fnmatchcase(FILENAME, PATTERN).\n    ";A=pat;B=name;B=os.path.normcase(B);A=os.path.normcase(A);return fnmatchcase(B,A)
@functools.lru_cache(maxsize=256,typed=True)
def _compile_pattern(pat):
	B='ISO-8859-1';A=pat
	if isinstance(A,bytes):D=str(A,B);E=translate(D);C=bytes(E,B)
	else:C=translate(A)
	return re.compile(C).match
def filter(names,pat):
	'Construct a list from those elements of the iterable NAMES that match PAT.';D=names;B=pat;C=[];B=os.path.normcase(B);E=_compile_pattern(B)
	if os.path is posixpath:
		for A in D:
			if E(A):C.append(A)
	else:
		for A in D:
			if E(os.path.normcase(A)):C.append(A)
	return C
def fnmatchcase(name,pat):"Test whether FILENAME matches PATTERN, including case.\n\n    This is a version of fnmatch() which doesn't case-normalize\n    its arguments.\n    ";A=_compile_pattern(pat);return A(name)is not None
def translate(pat):
	'Translate a shell PATTERN to a regular expression.\n\n    There is no way to quote meta-characters.\n    ';Q='\\\\';P='\\';N='!';L='-';H=pat;K=object();I=[];E=I.append;A,F=0,len(H)
	while A<F:
		O=H[A];A=A+1
		if O=='*':
			if not I or I[-1]is not K:E(K)
		elif O=='?':E('.')
		elif O=='[':
			B=A
			if B<F and H[B]==N:B=B+1
			if B<F and H[B]==']':B=B+1
			while B<F and H[B]!=']':B=B+1
			if B>=F:E('\\[')
			else:
				C=H[A:B]
				if L not in C:C=C.replace(P,Q)
				else:
					G=[];D=A+2 if H[A]==N else A+1
					while True:
						D=H.find(L,D,B)
						if D<0:break
						G.append(H[A:D]);A=D+1;D=D+3
					R=H[A:B]
					if R:G.append(R)
					else:G[-1]+=L
					for D in range(len(G)-1,0,-1):
						if G[D-1][-1]>G[D][0]:G[D-1]=G[D-1][:-1]+G[D][1:];del G[D]
					C=L.join(A.replace(P,Q).replace(L,'\\-')for A in G)
				C=re.sub('([&~|])','\\\\\\1',C);A=B+1
				if not C:E('(?!)')
				elif C==N:E('.')
				else:
					if C[0]==N:C='^'+C[1:]
					elif C[0]in('^','['):C=P+C
					E(f"[{C}]")
		else:E(re.escape(O))
	assert A==F;J=I;I=[];E=I.append;A,F=0,len(J)
	while A<F and J[A]is not K:E(J[A]);A+=1
	while A<F:
		assert J[A]is K;A+=1
		if A==F:E('.*');break
		assert J[A]is not K;M=[]
		while A<F and J[A]is not K:M.append(J[A]);A+=1
		M=''.join(M)
		if A==F:E('.*');E(M)
		else:S=_nextgroupnum();E(f"(?=(?P<g{S}>.*?{M}))(?P=g{S})")
	assert A==F;I=''.join(I);return f"(?s:{I})\\Z"