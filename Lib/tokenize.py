'Tokenization help for Python programs.\n\ntokenize(readline) is a generator that breaks a stream of bytes into\nPython tokens.  It decodes the bytes according to PEP-0263 for\ndetermining source file encoding.\n\nIt accepts a readline-like method which is called repeatedly to get the\nnext line of input (or b"" for EOF).  It generates 5-tuples with these\nmembers:\n\n    the token type (see token.py)\n    the token (a string)\n    the starting (row, column) indices of the token (a 2-tuple of ints)\n    the ending (row, column) indices of the token (a 2-tuple of ints)\n    the original line (string)\n\nIt is designed to match the working of the Python tokenizer exactly, except\nthat it produces COMMENT tokens for comments and gives type OP for all\noperators.  Additionally, all token lists start with an ENCODING token\nwhich tells you which encoding was used to decode the bytes stream.\n'
_I='utf-8-sig'
_H='TokenInfo'
_G='"""'
_F="'''"
_E='\\\\\\r?\\n'
_D='utf-8'
_C=False
_B=True
_A=None
__author__='Ka-Ping Yee <ping@lfw.org>'
__credits__='GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, Skip Montanaro, Raymond Hettinger, Trent Nelson, Michael Foord'
try:from builtins import open as _builtin_open
except ImportError:pass
from codecs import lookup,BOM_UTF8
import collections,functools
from io import TextIOWrapper
import itertools as _itertools,re,sys
from token import*
from token import EXACT_TOKEN_TYPES
cookie_re=re.compile('^[ \\t\\f]*#.*?coding[:=][ \\t]*([-\\w.]+)',re.ASCII)
blank_re=re.compile(b'^[ \\t\\f]*(?:[#\\r\\n]|$)',re.ASCII)
import token
__all__=token.__all__+['tokenize','generate_tokens','detect_encoding','untokenize',_H]
del token
class TokenInfo(collections.namedtuple(_H,'type string start end line')):
	def __repr__(self):annotated_type='%d (%s)'%(self.type,tok_name[self.type]);return'TokenInfo(type=%s, string=%r, start=%r, end=%r, line=%r)'%self._replace(type=annotated_type)
	@property
	def exact_type(self):
		if self.type==OP and self.string in EXACT_TOKEN_TYPES:return EXACT_TOKEN_TYPES[self.string]
		else:return self.type
def group(*choices):return'('+'|'.join(choices)+')'
def any(*choices):return group(*choices)+'*'
def maybe(*choices):return group(*choices)+'?'
Whitespace='[ \\f\\t]*'
Comment='#[^\\r\\n]*'
Ignore=Whitespace+any(_E+Whitespace)+maybe(Comment)
Name='\\w+'
Hexnumber='0[xX](?:_?[0-9a-fA-F])+'
Binnumber='0[bB](?:_?[01])+'
Octnumber='0[oO](?:_?[0-7])+'
Decnumber='(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Intnumber=group(Hexnumber,Binnumber,Octnumber,Decnumber)
Exponent='[eE][-+]?[0-9](?:_?[0-9])*'
Pointfloat=group('[0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?','\\.[0-9](?:_?[0-9])*')+maybe(Exponent)
Expfloat='[0-9](?:_?[0-9])*'+Exponent
Floatnumber=group(Pointfloat,Expfloat)
Imagnumber=group('[0-9](?:_?[0-9])*[jJ]',Floatnumber+'[jJ]')
Number=group(Imagnumber,Floatnumber,Intnumber)
def _all_string_prefixes():
	_valid_string_prefixes=['b','r','u','f','br','fr'];result={''}
	for prefix in _valid_string_prefixes:
		for t in _itertools.permutations(prefix):
			for u in _itertools.product(*[(c,c.upper())for c in t]):result.add(''.join(u))
	return result
@functools.lru_cache
def _compile(expr):return re.compile(expr,re.UNICODE)
StringPrefix=group(*_all_string_prefixes())
Single="[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"
Double='[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'
Single3="[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''"
Double3='[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'
Triple=group(StringPrefix+_F,StringPrefix+_G)
String=group(StringPrefix+"'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*'",StringPrefix+'"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*"')
Special=group(*map(re.escape,sorted(EXACT_TOKEN_TYPES,reverse=_B)))
Funny=group('\\r?\\n',Special)
PlainToken=group(Number,Funny,String,Name)
Token=Ignore+PlainToken
ContStr=group(StringPrefix+"'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*"+group("'",_E),StringPrefix+'"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*'+group('"',_E))
PseudoExtras=group('\\\\\\r?\\n|\\Z',Comment,Triple)
PseudoToken=Whitespace+group(PseudoExtras,Number,Funny,ContStr,Name)
endpats={}
for _prefix in _all_string_prefixes():endpats[_prefix+"'"]=Single;endpats[_prefix+'"']=Double;endpats[_prefix+_F]=Single3;endpats[_prefix+_G]=Double3
single_quoted=set()
triple_quoted=set()
for t in _all_string_prefixes():
	for u in(t+'"',t+"'"):single_quoted.add(u)
	for u in(t+_G,t+_F):triple_quoted.add(u)
tabsize=8
class TokenError(Exception):0
class StopTokenizing(Exception):0
class Untokenizer:
	def __init__(self):self.tokens=[];self.prev_row=1;self.prev_col=0;self.encoding=_A
	def add_whitespace(self,start):
		row,col=start
		if row<self.prev_row or row==self.prev_row and col<self.prev_col:raise ValueError('start ({},{}) precedes previous end ({},{})'.format(row,col,self.prev_row,self.prev_col))
		row_offset=row-self.prev_row
		if row_offset:self.tokens.append('\\\n'*row_offset);self.prev_col=0
		col_offset=col-self.prev_col
		if col_offset:self.tokens.append(' '*col_offset)
	def untokenize(self,iterable):
		it=iter(iterable);indents=[];startline=_C
		for t in it:
			if len(t)==2:self.compat(t,it);break
			tok_type,token,start,end,line=t
			if tok_type==ENCODING:self.encoding=token;continue
			if tok_type==ENDMARKER:break
			if tok_type==INDENT:indents.append(token);continue
			elif tok_type==DEDENT:indents.pop();self.prev_row,self.prev_col=end;continue
			elif tok_type in(NEWLINE,NL):startline=_B
			elif startline and indents:
				indent=indents[-1]
				if start[1]>=len(indent):self.tokens.append(indent);self.prev_col=len(indent)
				startline=_C
			self.add_whitespace(start);self.tokens.append(token);self.prev_row,self.prev_col=end
			if tok_type in(NEWLINE,NL):self.prev_row+=1;self.prev_col=0
		return''.join(self.tokens)
	def compat(self,token,iterable):
		indents=[];toks_append=self.tokens.append;startline=token[0]in(NEWLINE,NL);prevstring=_C
		for tok in _itertools.chain([token],iterable):
			toknum,tokval=tok[:2]
			if toknum==ENCODING:self.encoding=tokval;continue
			if toknum in(NAME,NUMBER):tokval+=' '
			if toknum==STRING:
				if prevstring:tokval=' '+tokval
				prevstring=_B
			else:prevstring=_C
			if toknum==INDENT:indents.append(tokval);continue
			elif toknum==DEDENT:indents.pop();continue
			elif toknum in(NEWLINE,NL):startline=_B
			elif startline and indents:toks_append(indents[-1]);startline=_C
			toks_append(tokval)
def untokenize(iterable):
	'Transform tokens back into Python source code.\n    It returns a bytes object, encoded using the ENCODING\n    token, which is the first token sequence output by tokenize.\n\n    Each element returned by the iterable must be a token sequence\n    with at least two elements, a token number and token value.  If\n    only two tokens are passed, the resulting output is poor.\n\n    Round-trip invariant for full input:\n        Untokenized source will match input source exactly\n\n    Round-trip invariant for limited input:\n        # Output bytes will tokenize back to the input\n        t1 = [tok[:2] for tok in tokenize(f.readline)]\n        newcode = untokenize(t1)\n        readline = BytesIO(newcode).readline\n        t2 = [tok[:2] for tok in tokenize(readline)]\n        assert t1 == t2\n    ';ut=Untokenizer();out=ut.untokenize(iterable)
	if ut.encoding is not _A:out=out.encode(ut.encoding)
	return out
def _get_normal_name(orig_enc):
	'Imitates get_normal_name in tokenizer.c.';A='iso-8859-1';enc=orig_enc[:12].lower().replace('_','-')
	if enc==_D or enc.startswith('utf-8-'):return _D
	if enc in('latin-1',A,'iso-latin-1')or enc.startswith(('latin-1-','iso-8859-1-','iso-latin-1-')):return A
	return orig_enc
def detect_encoding(readline):
	"\n    The detect_encoding() function is used to detect the encoding that should\n    be used to decode a Python source file.  It requires one argument, readline,\n    in the same way as the tokenize() generator.\n\n    It will call readline a maximum of twice, and return the encoding used\n    (as a string) and a list of any lines (left as bytes) it has read in.\n\n    It detects the encoding from the presence of a utf-8 bom or an encoding\n    cookie as specified in pep-0263.  If both a bom and a cookie are present,\n    but disagree, a SyntaxError will be raised.  If the encoding cookie is an\n    invalid charset, raise a SyntaxError.  Note that if a utf-8 bom is found,\n    'utf-8-sig' is returned.\n\n    If no encoding is specified, then the default of 'utf-8' will be returned.\n    "
	try:filename=readline.__self__.name
	except AttributeError:filename=_A
	bom_found=_C;encoding=_A;default=_D
	def read_or_stop():
		try:return readline()
		except StopIteration:return b''
	def find_cookie(line):
		try:line_string=line.decode(_D)
		except UnicodeDecodeError:
			msg='invalid or missing encoding declaration'
			if filename is not _A:msg='{} for {!r}'.format(msg,filename)
			raise SyntaxError(msg)
		match=cookie_re.match(line_string)
		if not match:return
		encoding=_get_normal_name(match.group(1))
		try:codec=lookup(encoding)
		except LookupError:
			if filename is _A:msg='unknown encoding: '+encoding
			else:msg='unknown encoding for {!r}: {}'.format(filename,encoding)
			raise SyntaxError(msg)
		if bom_found:
			if encoding!=_D:
				if filename is _A:msg='encoding problem: utf-8'
				else:msg='encoding problem for {!r}: utf-8'.format(filename)
				raise SyntaxError(msg)
			encoding+='-sig'
		return encoding
	first=read_or_stop()
	if first.startswith(BOM_UTF8):bom_found=_B;first=first[3:];default=_I
	if not first:return default,[]
	encoding=find_cookie(first)
	if encoding:return encoding,[first]
	if not blank_re.match(first):return default,[first]
	second=read_or_stop()
	if not second:return default,[first]
	encoding=find_cookie(second)
	if encoding:return encoding,[first,second]
	return default,[first,second]
def open(filename):
	'Open a file in read only mode using the encoding detected by\n    detect_encoding().\n    ';buffer=_builtin_open(filename,'rb')
	try:encoding,lines=detect_encoding(buffer.readline);buffer.seek(0);text=TextIOWrapper(buffer,encoding,line_buffering=_B);text.mode='r';return text
	except:buffer.close();raise
def tokenize(readline):"\n    The tokenize() generator requires one argument, readline, which\n    must be a callable object which provides the same interface as the\n    readline() method of built-in file objects.  Each call to the function\n    should return one line of input as bytes.  Alternatively, readline\n    can be a callable function terminating with StopIteration:\n        readline = open(myfile, 'rb').__next__  # Example of alternate readline\n\n    The generator produces 5-tuples with these members: the token type; the\n    token string; a 2-tuple (srow, scol) of ints specifying the row and\n    column where the token begins in the source; a 2-tuple (erow, ecol) of\n    ints specifying the row and column where the token ends in the source;\n    and the line on which the token was found.  The line passed is the\n    physical line.\n\n    The first token sequence will always be an ENCODING token\n    which tells you which encoding was used to decode the bytes stream.\n    ";encoding,consumed=detect_encoding(readline);empty=_itertools.repeat(b'');rl_gen=_itertools.chain(consumed,iter(readline,b''),empty);return _tokenize(rl_gen.__next__,encoding)
def _tokenize(readline,encoding):
	B='\r\n';A='#';lnum=parenlev=continued=0;numchars='0123456789';contstr,needcont='',0;contline=_A;indents=[0]
	if encoding is not _A:
		if encoding==_I:encoding=_D
		yield TokenInfo(ENCODING,encoding,(0,0),(0,0),'')
	last_line=b'';line=b''
	while _B:
		try:last_line=line;line=readline()
		except StopIteration:line=b''
		if encoding is not _A:line=line.decode(encoding)
		lnum+=1;pos,max=0,len(line)
		if contstr:
			if not line:raise TokenError('EOF in multi-line string',strstart)
			endmatch=endprog.match(line)
			if endmatch:pos=end=endmatch.end(0);yield TokenInfo(STRING,contstr+line[:end],strstart,(lnum,end),contline+line);contstr,needcont='',0;contline=_A
			elif needcont and line[-2:]!='\\\n'and line[-3:]!='\\\r\n':yield TokenInfo(ERRORTOKEN,contstr+line,strstart,(lnum,len(line)),contline);contstr='';contline=_A;continue
			else:contstr=contstr+line;contline=contline+line;continue
		elif parenlev==0 and not continued:
			if not line:break
			column=0
			while pos<max:
				if line[pos]==' ':column+=1
				elif line[pos]=='\t':column=(column//tabsize+1)*tabsize
				elif line[pos]=='\x0c':column=0
				else:break
				pos+=1
			if pos==max:break
			if line[pos]in'#\r\n':
				if line[pos]==A:comment_token=line[pos:].rstrip(B);yield TokenInfo(COMMENT,comment_token,(lnum,pos),(lnum,pos+len(comment_token)),line);pos+=len(comment_token)
				yield TokenInfo(NL,line[pos:],(lnum,pos),(lnum,len(line)),line);continue
			if column>indents[-1]:indents.append(column);yield TokenInfo(INDENT,line[:pos],(lnum,0),(lnum,pos),line)
			while column<indents[-1]:
				if column not in indents:raise IndentationError('unindent does not match any outer indentation level',('<tokenize>',lnum,pos,line))
				indents=indents[:-1];yield TokenInfo(DEDENT,'',(lnum,pos),(lnum,pos),line)
		else:
			if not line:raise TokenError('EOF in multi-line statement',(lnum,0))
			continued=0
		while pos<max:
			pseudomatch=_compile(PseudoToken).match(line,pos)
			if pseudomatch:
				start,end=pseudomatch.span(1);spos,epos,pos=(lnum,start),(lnum,end),end
				if start==end:continue
				token,initial=line[start:end],line[start]
				if initial in numchars or initial=='.'and token!='.'and token!='...':yield TokenInfo(NUMBER,token,spos,epos,line)
				elif initial in B:
					if parenlev>0:yield TokenInfo(NL,token,spos,epos,line)
					else:yield TokenInfo(NEWLINE,token,spos,epos,line)
				elif initial==A:assert not token.endswith('\n');yield TokenInfo(COMMENT,token,spos,epos,line)
				elif token in triple_quoted:
					endprog=_compile(endpats[token]);endmatch=endprog.match(line,pos)
					if endmatch:pos=endmatch.end(0);token=line[start:pos];yield TokenInfo(STRING,token,spos,(lnum,pos),line)
					else:strstart=lnum,start;contstr=line[start:];contline=line;break
				elif initial in single_quoted or token[:2]in single_quoted or token[:3]in single_quoted:
					if token[-1]=='\n':strstart=lnum,start;endprog=_compile(endpats.get(initial)or endpats.get(token[1])or endpats.get(token[2]));contstr,needcont=line[start:],1;contline=line;break
					else:yield TokenInfo(STRING,token,spos,epos,line)
				elif initial.isidentifier():yield TokenInfo(NAME,token,spos,epos,line)
				elif initial=='\\':continued=1
				else:
					if initial in'([{':parenlev+=1
					elif initial in')]}':parenlev-=1
					yield TokenInfo(OP,token,spos,epos,line)
			else:yield TokenInfo(ERRORTOKEN,line[pos],(lnum,pos),(lnum,pos+1),line);pos+=1
	if last_line and last_line[-1]not in B and not last_line.strip().startswith(A):yield TokenInfo(NEWLINE,'',(lnum-1,len(last_line)),(lnum-1,len(last_line)+1),'')
	for indent in indents[1:]:yield TokenInfo(DEDENT,'',(lnum,0),(lnum,0),'')
	yield TokenInfo(ENDMARKER,'',(lnum,0),(lnum,0),'')
def generate_tokens(readline):'Tokenize a source reading Python code as unicode strings.\n\n    This has the same API as tokenize(), except that it expects the *readline*\n    callable to return str objects instead of bytes.\n    ';return _tokenize(readline,_A)
def main():
	import argparse
	def perror(message):sys.stderr.write(message);sys.stderr.write('\n')
	def error(message,filename=_A,location=_A):
		if location:args=(filename,)+location+(message,);perror('%s:%d:%d: error: %s'%args)
		elif filename:perror('%s: error: %s'%(filename,message))
		else:perror('error: %s'%message)
		sys.exit(1)
	parser=argparse.ArgumentParser(prog='python -m tokenize');parser.add_argument(dest='filename',nargs='?',metavar='filename.py',help='the file to tokenize; defaults to stdin');parser.add_argument('-e','--exact',dest='exact',action='store_true',help='display token names using the exact type');args=parser.parse_args()
	try:
		if args.filename:
			filename=args.filename
			with _builtin_open(filename,'rb')as f:tokens=list(tokenize(f.readline))
		else:filename='<stdin>';tokens=_tokenize(sys.stdin.readline,_A)
		for token in tokens:
			token_type=token.type
			if args.exact:token_type=token.exact_type
			token_range='%d,%d-%d,%d:'%(token.start+token.end);print('%-20s%-15s%-15r'%(token_range,tok_name[token_type],token.string))
	except IndentationError as err:line,column=err.args[1][1:3];error(err.args[0],filename,(line,column))
	except TokenError as err:line,column=err.args[1];error(err.args[0],filename,(line,column))
	except SyntaxError as err:error(err,filename)
	except OSError as err:error(err)
	except KeyboardInterrupt:print('interrupted\n')
	except Exception as err:perror('unexpected error: %s'%err);raise
if __name__=='__main__':main()