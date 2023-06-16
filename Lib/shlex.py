'A lexical analyzer class for simple shell-like syntaxes.'
_D=True
_C=False
_B=' '
_A=None
import os,re,sys
from collections import deque
from io import StringIO
__all__=['shlex','split','quote','join']
class shlex:
	'A lexical analyzer class for simple shell-like syntaxes.'
	def __init__(A,instream=_A,infile=_A,posix=_C,punctuation_chars=_C):
		D=posix;C=instream;B=punctuation_chars
		if isinstance(C,str):C=StringIO(C)
		if C is not _A:A.instream=C;A.infile=infile
		else:A.instream=sys.stdin;A.infile=_A
		A.posix=D
		if D:A.eof=_A
		else:A.eof=''
		A.commenters='#';A.wordchars='abcdfeghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
		if A.posix:A.wordchars+='ßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ'
		A.whitespace=' \t\r\n';A.whitespace_split=_C;A.quotes='\'"';A.escape='\\';A.escapedquotes='"';A.state=_B;A.pushback=deque();A.lineno=1;A.debug=0;A.token='';A.filestack=deque();A.source=_A
		if not B:B=''
		elif B is _D:B='();<>|&'
		A._punctuation_chars=B
		if B:A._pushback_chars=deque();A.wordchars+='~-./*?=';E=A.wordchars.maketrans(dict.fromkeys(B));A.wordchars=A.wordchars.translate(E)
	@property
	def punctuation_chars(self):return self._punctuation_chars
	def push_token(A,tok):
		'Push a token onto the stack popped by the get_token method'
		if A.debug>=1:print('shlex: pushing token '+repr(tok))
		A.pushback.appendleft(tok)
	def push_source(A,newstream,newfile=_A):
		"Push an input source onto the lexer's input source stack.";C=newfile;B=newstream
		if isinstance(B,str):B=StringIO(B)
		A.filestack.appendleft((A.infile,A.instream,A.lineno));A.infile=C;A.instream=B;A.lineno=1
		if A.debug:
			if C is not _A:print('shlex: pushing to file %s'%(A.infile,))
			else:print('shlex: pushing to stream %s'%(A.instream,))
	def pop_source(A):
		'Pop the input source stack.';A.instream.close();A.infile,A.instream,A.lineno=A.filestack.popleft()
		if A.debug:print('shlex: popping to %s, line %d'%(A.instream,A.lineno))
		A.state=_B
	def get_token(A):
		"Get a token from the input stream (or from stack if it's nonempty)"
		if A.pushback:
			C=A.pushback.popleft()
			if A.debug>=1:print('shlex: popping token '+repr(C))
			return C
		B=A.read_token()
		if A.source is not _A:
			while B==A.source:
				D=A.sourcehook(A.read_token())
				if D:E,F=D;A.push_source(F,E)
				B=A.get_token()
		while B==A.eof:
			if not A.filestack:return A.eof
			else:A.pop_source();B=A.get_token()
		if A.debug>=1:
			if B!=A.eof:print('shlex: token='+repr(B))
			else:print('shlex: token=EOF')
		return B
	def read_token(A):
		G='c';D='a';C=_C;E=_B
		while _D:
			if A.punctuation_chars and A._pushback_chars:B=A._pushback_chars.pop()
			else:B=A.instream.read(1)
			if B=='\n':A.lineno+=1
			if A.debug>=3:print('shlex: in state %r I see character: %r'%(A.state,B))
			if A.state is _A:A.token='';break
			elif A.state==_B:
				if not B:A.state=_A;break
				elif B in A.whitespace:
					if A.debug>=2:print('shlex: I see whitespace in whitespace state')
					if A.token or A.posix and C:break
					else:continue
				elif B in A.commenters:A.instream.readline();A.lineno+=1
				elif A.posix and B in A.escape:E=D;A.state=B
				elif B in A.wordchars:A.token=B;A.state=D
				elif B in A.punctuation_chars:A.token=B;A.state=G
				elif B in A.quotes:
					if not A.posix:A.token=B
					A.state=B
				elif A.whitespace_split:A.token=B;A.state=D
				else:
					A.token=B
					if A.token or A.posix and C:break
					else:continue
			elif A.state in A.quotes:
				C=_D
				if not B:
					if A.debug>=2:print('shlex: I see EOF in quotes state')
					raise ValueError('No closing quotation')
				if B==A.state:
					if not A.posix:A.token+=B;A.state=_B;break
					else:A.state=D
				elif A.posix and B in A.escape and A.state in A.escapedquotes:E=A.state;A.state=B
				else:A.token+=B
			elif A.state in A.escape:
				if not B:
					if A.debug>=2:print('shlex: I see EOF in escape state')
					raise ValueError('No escaped character')
				if E in A.quotes and B!=A.state and B!=E:A.token+=A.state
				A.token+=B;A.state=E
			elif A.state in(D,G):
				if not B:A.state=_A;break
				elif B in A.whitespace:
					if A.debug>=2:print('shlex: I see whitespace in word state')
					A.state=_B
					if A.token or A.posix and C:break
					else:continue
				elif B in A.commenters:
					A.instream.readline();A.lineno+=1
					if A.posix:
						A.state=_B
						if A.token or A.posix and C:break
						else:continue
				elif A.state==G:
					if B in A.punctuation_chars:A.token+=B
					else:
						if B not in A.whitespace:A._pushback_chars.append(B)
						A.state=_B;break
				elif A.posix and B in A.quotes:A.state=B
				elif A.posix and B in A.escape:E=D;A.state=B
				elif B in A.wordchars or B in A.quotes or A.whitespace_split and B not in A.punctuation_chars:A.token+=B
				else:
					if A.punctuation_chars:A._pushback_chars.append(B)
					else:A.pushback.appendleft(B)
					if A.debug>=2:print('shlex: I see punctuation in word state')
					A.state=_B
					if A.token or A.posix and C:break
					else:continue
		F=A.token;A.token=''
		if A.posix and not C and F=='':F=_A
		if A.debug>1:
			if F:print('shlex: raw token='+repr(F))
			else:print('shlex: raw token=EOF')
		return F
	def sourcehook(B,newfile):
		'Hook called on a filename to be sourced.';A=newfile
		if A[0]=='"':A=A[1:-1]
		if isinstance(B.infile,str)and not os.path.isabs(A):A=os.path.join(os.path.dirname(B.infile),A)
		return A,open(A,'r')
	def error_leader(C,infile=_A,lineno=_A):
		'Emit a C-compiler-like, Emacs-friendly error-message leader.';A=lineno;B=infile
		if B is _A:B=C.infile
		if A is _A:A=C.lineno
		return'"%s", line %d: '%(B,A)
	def __iter__(A):return A
	def __next__(A):
		B=A.get_token()
		if B==A.eof:raise StopIteration
		return B
def split(s,comments=_C,posix=_D):
	'Split the string *s* using shell-like syntax.'
	if s is _A:import warnings as B;B.warn("Passing None for 's' to shlex.split() is deprecated.",DeprecationWarning,stacklevel=2)
	A=shlex(s,posix=posix);A.whitespace_split=_D
	if not comments:A.commenters=''
	return list(A)
def join(split_command):'Return a shell-escaped string from *split_command*.';return _B.join(quote(A)for A in split_command)
_find_unsafe=re.compile('[^\\w@%+=:,./-]',re.ASCII).search
def quote(s):
	'Return a shell-escaped version of the string *s*.';A="'"
	if not s:return"''"
	if _find_unsafe(s)is _A:return s
	return A+s.replace(A,'\'"\'"\'')+A
def _print_tokens(lexer):
	while 1:
		A=lexer.get_token()
		if not A:break
		print('Token: '+repr(A))
if __name__=='__main__':
	if len(sys.argv)==1:_print_tokens(shlex())
	else:
		fn=sys.argv[1]
		with open(fn)as f:_print_tokens(shlex(f,fn))