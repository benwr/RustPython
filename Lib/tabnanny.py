#! /usr/bin/env python3
'The Tab Nanny despises ambiguous indentation.  She knows no mercy.\n\ntabnanny -- Detection of ambiguous indentation\n\nFor the time being this module is intended to be called as a script.\nHowever it is possible to import it into an IDE and use the function\ncheck() described below.\n\nWarning: The API provided by this module is likely to change in future\nreleases; such changes may not be backward compatible.\n'
__version__='6'
import os,sys,tokenize
if not hasattr(tokenize,'NL'):raise ValueError("tokenize.NL doesn't exist -- tokenize module too old")
__all__=['check','NannyNag','process_tokens']
verbose=0
filename_only=0
def errprint(*B):
	A=''
	for C in B:sys.stderr.write(A+str(C));A=' '
	sys.stderr.write('\n')
def main():
	import getopt as A;global verbose,filename_only
	try:D,B=A.getopt(sys.argv[1:],'qv')
	except A.error as E:errprint(E);return
	for(C,G)in D:
		if C=='-q':filename_only=filename_only+1
		if C=='-v':verbose=verbose+1
	if not B:errprint('Usage:',sys.argv[0],'[-v] file_or_directory ...');return
	for F in B:check(F)
class NannyNag(Exception):
	'\n    Raised by process_tokens() if detecting an ambiguous indent.\n    Captured and handled in check().\n    '
	def __init__(A,lineno,msg,line):A.lineno,A.msg,A.line=lineno,msg,line
	def get_lineno(A):return A.lineno
	def get_msg(A):return A.msg
	def get_line(A):return A.line
def check(file):
	'check(file_or_dir)\n\n    If file_or_dir is a directory and not a symbolic link, then recursively\n    descend the directory tree named by file_or_dir, checking all .py files\n    along the way. If file_or_dir is an ordinary Python source file, it is\n    checked for whitespace related problems. The diagnostic messages are\n    written to standard output using the print statement.\n    ';A=file
	if os.path.isdir(A)and not os.path.islink(A):
		if verbose:print('%r: listing directory'%(A,))
		I=os.listdir(A)
		for E in I:
			C=os.path.join(A,E)
			if os.path.isdir(C)and not os.path.islink(C)or os.path.normcase(E[-3:])=='.py':check(C)
		return
	try:F=tokenize.open(A)
	except OSError as B:errprint('%r: I/O Error: %s'%(A,B));return
	if verbose>1:print('checking %r ...'%A)
	try:process_tokens(tokenize.generate_tokens(F.readline))
	except tokenize.TokenError as B:errprint('%r: Token Error: %s'%(A,B));return
	except IndentationError as B:errprint('%r: Indentation Error: %s'%(A,B));return
	except NannyNag as D:
		G=D.get_lineno();H=D.get_line()
		if verbose:print('%r: *** Line %d: trouble in tab city! ***'%(A,G));print('offending line: %r'%(H,));print(D.get_msg())
		else:
			if' 'in A:A='"'+A+'"'
			if filename_only:print(A)
			else:print(A,G,repr(H))
		return
	finally:F.close()
	if verbose:print('%r: Clean bill of health.'%(A,))
class Whitespace:
	S,T=' \t'
	def __init__(C,ws):
		C.raw=ws;G,H=Whitespace.S,Whitespace.T;A=[];B=D=E=0
		for F in C.raw:
			if F==G:D=D+1;B=B+1
			elif F==H:
				D=D+1;E=E+1
				if B>=len(A):A=A+[0]*(B-len(A)+1)
				A[B]=A[B]+1;B=0
			else:break
		C.n=D;C.nt=E;C.norm=tuple(A),B;C.is_simple=len(A)<=1
	def longest_run_of_spaces(A):B,C=A.norm;return max(len(B)-1,C)
	def indent_level(C,tabsize):
		A=tabsize;D,F=C.norm;B=0
		for E in range(A,len(D)):B=B+E//A*D[E]
		return F+A*(B+C.nt)
	def equal(A,other):return A.norm==other.norm
	def not_equal_witness(B,other):
		C=other;E=max(B.longest_run_of_spaces(),C.longest_run_of_spaces())+1;D=[]
		for A in range(1,E+1):
			if B.indent_level(A)!=C.indent_level(A):D.append((A,B.indent_level(A),C.indent_level(A)))
		return D
	def less(A,other):
		C=False;B=other
		if A.n>=B.n:return C
		if A.is_simple and B.is_simple:return A.nt<=B.nt
		E=max(A.longest_run_of_spaces(),B.longest_run_of_spaces())+1
		for D in range(2,E+1):
			if A.indent_level(D)>=B.indent_level(D):return C
		return True
	def not_less_witness(B,other):
		C=other;E=max(B.longest_run_of_spaces(),C.longest_run_of_spaces())+1;D=[]
		for A in range(1,E+1):
			if B.indent_level(A)>=C.indent_level(A):D.append((A,B.indent_level(A),C.indent_level(A)))
		return D
def format_witnesses(w):
	B=(str(A[0])for A in w);A='at tab size'
	if len(w)>1:A=A+'s'
	return A+' '+', '.join(B)
def process_tokens(tokens):
	H=tokenize.INDENT;I=tokenize.DEDENT;J=tokenize.NEWLINE;K=tokenize.COMMENT,tokenize.NL;A=[Whitespace('')];C=0
	for(type,L,G,M,D)in tokens:
		if type==J:C=1
		elif type==H:
			C=0;B=Whitespace(L)
			if not A[-1].less(B):E=A[-1].not_less_witness(B);F='indent not greater e.g. '+format_witnesses(E);raise NannyNag(G[0],F,D)
			A.append(B)
		elif type==I:C=1;del A[-1]
		elif C and type not in K:
			C=0;B=Whitespace(D)
			if not A[-1].equal(B):E=A[-1].not_equal_witness(B);F='indent not equal e.g. '+format_witnesses(E);raise NannyNag(G[0],F,D)
if __name__=='__main__':main()