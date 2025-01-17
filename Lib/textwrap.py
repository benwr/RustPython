'Text wrapping and filling.\n'
_B=True
_A=None
import re
__all__=['TextWrapper','wrap','fill','dedent','indent','shorten']
_whitespace='\t\n\x0b\x0c\r '
class TextWrapper:
	'\n    Object for wrapping/filling text.  The public interface consists of\n    the wrap() and fill() methods; the other methods are just there for\n    subclasses to override in order to tweak the default behaviour.\n    If you want to completely replace the main wrapping algorithm,\n    you\'ll probably have to override _wrap_chunks().\n\n    Several instance attributes control various aspects of wrapping:\n      width (default: 70)\n        the maximum width of wrapped lines (unless break_long_words\n        is false)\n      initial_indent (default: "")\n        string that will be prepended to the first line of wrapped\n        output.  Counts towards the line\'s width.\n      subsequent_indent (default: "")\n        string that will be prepended to all lines save the first\n        of wrapped output; also counts towards each line\'s width.\n      expand_tabs (default: true)\n        Expand tabs in input text to spaces before further processing.\n        Each tab will become 0 .. \'tabsize\' spaces, depending on its position\n        in its line.  If false, each tab is treated as a single character.\n      tabsize (default: 8)\n        Expand tabs in input text to 0 .. \'tabsize\' spaces, unless\n        \'expand_tabs\' is false.\n      replace_whitespace (default: true)\n        Replace all whitespace characters in the input text by spaces\n        after tab expansion.  Note that if expand_tabs is false and\n        replace_whitespace is true, every tab will be converted to a\n        single space!\n      fix_sentence_endings (default: false)\n        Ensure that sentence-ending punctuation is always followed\n        by two spaces.  Off by default because the algorithm is\n        (unavoidably) imperfect.\n      break_long_words (default: true)\n        Break words longer than \'width\'.  If false, those words will not\n        be broken, and some lines might be longer than \'width\'.\n      break_on_hyphens (default: true)\n        Allow breaking hyphenated words. If true, wrapping will occur\n        preferably on whitespaces and right after hyphens part of\n        compound words.\n      drop_whitespace (default: true)\n        Drop leading and trailing whitespace from lines.\n      max_lines (default: None)\n        Truncate wrapped lines.\n      placeholder (default: \' [...]\')\n        Append to the last line of truncated text.\n    ';unicode_whitespace_trans={};uspace=ord(' ')
	for x in _whitespace:unicode_whitespace_trans[ord(x)]=uspace
	word_punct='[\\w!"\\\'&.,?]';letter='[^\\d\\W]';whitespace='[%s]'%re.escape(_whitespace);nowhitespace='[^'+whitespace[1:];wordsep_re=re.compile('\n        ( # any whitespace\n          %(ws)s+\n        | # em-dash between words\n          (?<=%(wp)s) -{2,} (?=\\w)\n        | # word, possibly hyphenated\n          %(nws)s+? (?:\n            # hyphenated word\n              -(?: (?<=%(lt)s{2}-) | (?<=%(lt)s-%(lt)s-))\n              (?= %(lt)s -? %(lt)s)\n            | # end of word\n              (?=%(ws)s|\\Z)\n            | # em-dash\n              (?<=%(wp)s) (?=-{2,}\\w)\n            )\n        )'%{'wp':word_punct,'lt':letter,'ws':whitespace,'nws':nowhitespace},re.VERBOSE);del word_punct,letter,nowhitespace;wordsep_simple_re=re.compile('(%s+)'%whitespace);del whitespace;sentence_end_re=re.compile('[a-z][\\.\\!\\?][\\"\\\']?\\Z')
	def __init__(A,width=70,initial_indent='',subsequent_indent='',expand_tabs=_B,replace_whitespace=_B,fix_sentence_endings=False,break_long_words=_B,drop_whitespace=_B,break_on_hyphens=_B,tabsize=8,*,max_lines=_A,placeholder=' [...]'):A.width=width;A.initial_indent=initial_indent;A.subsequent_indent=subsequent_indent;A.expand_tabs=expand_tabs;A.replace_whitespace=replace_whitespace;A.fix_sentence_endings=fix_sentence_endings;A.break_long_words=break_long_words;A.drop_whitespace=drop_whitespace;A.break_on_hyphens=break_on_hyphens;A.tabsize=tabsize;A.max_lines=max_lines;A.placeholder=placeholder
	def _munge_whitespace(B,text):
		'_munge_whitespace(text : string) -> string\n\n        Munge whitespace in text: expand tabs and convert all other\n        whitespace characters to spaces.  Eg. " foo\\tbar\\n\\nbaz"\n        becomes " foo    bar  baz".\n        ';A=text
		if B.expand_tabs:A=A.expandtabs(B.tabsize)
		if B.replace_whitespace:A=A.translate(B.unicode_whitespace_trans)
		return A
	def _split(B,text):
		"_split(text : string) -> [string]\n\n        Split the text to wrap into indivisible chunks.  Chunks are\n        not quite the same as words; see _wrap_chunks() for full\n        details.  As an example, the text\n          Look, goof-ball -- use the -b option!\n        breaks into the following chunks:\n          'Look,', ' ', 'goof-', 'ball', ' ', '--', ' ',\n          'use', ' ', 'the', ' ', '-b', ' ', 'option!'\n        if break_on_hyphens is True, or in:\n          'Look,', ' ', 'goof-ball', ' ', '--', ' ',\n          'use', ' ', 'the', ' ', '-b', ' ', option!'\n        otherwise.\n        "
		if B.break_on_hyphens is _B:A=B.wordsep_re.split(text)
		else:A=B.wordsep_simple_re.split(text)
		A=[A for A in A if A];return A
	def _fix_sentence_endings(C,chunks):
		'_fix_sentence_endings(chunks : [string])\n\n        Correct for sentence endings buried in \'chunks\'.  Eg. when the\n        original text contains "... foo.\\nBar ...", munge_whitespace()\n        and split() will convert that to [..., "foo.", " ", "Bar", ...]\n        which has one too few spaces; this method simply changes the one\n        space to two.\n        ';B=chunks;A=0;D=C.sentence_end_re.search
		while A<len(B)-1:
			if B[A+1]==' 'and D(B[A]):B[A+1]='  ';A+=2
			else:A+=1
	def _handle_long_word(G,reversed_chunks,cur_line,cur_len,width):
		'_handle_long_word(chunks : [string],\n                             cur_line : [string],\n                             cur_len : int, width : int)\n\n        Handle a chunk of text (most likely a word, not whitespace) that\n        is too long to fit in any line.\n        ';H=width;C=cur_line;D=reversed_chunks
		if H<1:B=1
		else:B=H-cur_len
		if G.break_long_words:
			E=B;A=D[-1]
			if G.break_on_hyphens and len(A)>B:
				F=A.rfind('-',0,B)
				if F>0 and any(A!='-'for A in A[:F]):E=F+1
			C.append(A[:E]);D[-1]=A[E:]
		elif not C:C.append(D.pop())
	def _wrap_chunks(A,chunks):
		'_wrap_chunks(chunks : [string]) -> [string]\n\n        Wrap a sequence of text chunks and return a list of lines of\n        length \'self.width\' or less.  (If \'break_long_words\' is false,\n        some lines may be longer than this.)  Chunks correspond roughly\n        to words and the whitespace between them: each chunk is\n        indivisible (modulo \'break_long_words\'), but a line break can\n        come between any two chunks.  Chunks should not have internal\n        whitespace; ie. a chunk is either all whitespace or a "word".\n        Whitespace chunks will be removed from the beginning and end of\n        lines, but apart from that whitespace is preserved.\n        ';C=chunks;D=[]
		if A.width<=0:raise ValueError('invalid width %r (must be > 0)'%A.width)
		if A.max_lines is not _A:
			if A.max_lines>1:E=A.subsequent_indent
			else:E=A.initial_indent
			if len(E)+len(A.placeholder.lstrip())>A.width:raise ValueError('placeholder too large for max width')
		C.reverse()
		while C:
			B=[];F=0
			if D:E=A.subsequent_indent
			else:E=A.initial_indent
			G=A.width-len(E)
			if A.drop_whitespace and C[-1].strip()==''and D:del C[-1]
			while C:
				H=len(C[-1])
				if F+H<=G:B.append(C.pop());F+=H
				else:break
			if C and len(C[-1])>G:A._handle_long_word(C,B,F,G);F=sum(map(len,B))
			if A.drop_whitespace and B and B[-1].strip()=='':F-=len(B[-1]);del B[-1]
			if B:
				if A.max_lines is _A or len(D)+1<A.max_lines or(not C or A.drop_whitespace and len(C)==1 and not C[0].strip())and F<=G:D.append(E+''.join(B))
				else:
					while B:
						if B[-1].strip()and F+len(A.placeholder)<=G:B.append(A.placeholder);D.append(E+''.join(B));break
						F-=len(B[-1]);del B[-1]
					else:
						if D:
							I=D[-1].rstrip()
							if len(I)+len(A.placeholder)<=A.width:D[-1]=I+A.placeholder;break
						D.append(E+A.placeholder.lstrip())
					break
		return D
	def _split_chunks(B,text):A=text;A=B._munge_whitespace(A);return B._split(A)
	def wrap(A,text):
		"wrap(text : string) -> [string]\n\n        Reformat the single paragraph in 'text' so it fits in lines of\n        no more than 'self.width' columns, and return a list of wrapped\n        lines.  Tabs in 'text' are expanded with string.expandtabs(),\n        and all other whitespace characters (including newline) are\n        converted to space.\n        ";B=A._split_chunks(text)
		if A.fix_sentence_endings:A._fix_sentence_endings(B)
		return A._wrap_chunks(B)
	def fill(A,text):"fill(text : string) -> string\n\n        Reformat the single paragraph in 'text' to fit in lines of no\n        more than 'self.width' columns, and return a new string\n        containing the entire wrapped paragraph.\n        ";return'\n'.join(A.wrap(text))
def wrap(text,width=70,**A):"Wrap a single paragraph of text, returning a list of wrapped lines.\n\n    Reformat the single paragraph in 'text' so it fits in lines of no\n    more than 'width' columns, and return a list of wrapped lines.  By\n    default, tabs in 'text' are expanded with string.expandtabs(), and\n    all other whitespace characters (including newline) are converted to\n    space.  See TextWrapper class for available keyword args to customize\n    wrapping behaviour.\n    ";B=TextWrapper(width=width,**A);return B.wrap(text)
def fill(text,width=70,**A):"Fill a single paragraph of text, returning a new string.\n\n    Reformat the single paragraph in 'text' to fit in lines of no more\n    than 'width' columns, and return a new string containing the entire\n    wrapped paragraph.  As with wrap(), tabs are expanded and other\n    whitespace characters converted to space.  See TextWrapper class for\n    available keyword args to customize wrapping behaviour.\n    ";B=TextWrapper(width=width,**A);return B.fill(text)
def shorten(text,width,**A):'Collapse and truncate the given text to fit in the given width.\n\n    The text first has its whitespace collapsed.  If it then fits in\n    the *width*, it is returned as is.  Otherwise, as many words\n    as possible are joined and then the placeholder is appended::\n\n        >>> textwrap.shorten("Hello  world!", width=12)\n        \'Hello world!\'\n        >>> textwrap.shorten("Hello  world!", width=11)\n        \'Hello [...]\'\n    ';B=TextWrapper(width=width,max_lines=1,**A);return B.fill(' '.join(text.strip().split()))
_whitespace_only_re=re.compile('^[ \t]+$',re.MULTILINE)
_leading_whitespace_re=re.compile('(^[ \t]*)(?:[^ \t\n])',re.MULTILINE)
def dedent(text):
	'Remove any common leading whitespace from every line in `text`.\n\n    This can be used to make triple-quoted strings line up with the left\n    edge of the display, while still presenting them in the source code\n    in indented form.\n\n    Note that tabs and spaces are both treated as whitespace, but they\n    are not equal: the lines "  hello" and "\\thello" are\n    considered to have no common leading whitespace.\n\n    Entirely blank lines are normalized to a newline character.\n    ';B=text;A=_A;B=_whitespace_only_re.sub('',B);E=_leading_whitespace_re.findall(B)
	for C in E:
		if A is _A:A=C
		elif C.startswith(A):0
		elif A.startswith(C):A=C
		else:
			for(F,(G,H))in enumerate(zip(A,C)):
				if G!=H:A=A[:F];break
	if 0 and A:
		for D in B.split('\n'):assert not D or D.startswith(A),'line = %r, margin = %r'%(D,A)
	if A:B=re.sub('(?m)^'+A,'',B)
	return B
def indent(text,prefix,predicate=_A):
	"Adds 'prefix' to the beginning of selected lines in 'text'.\n\n    If 'predicate' is provided, 'prefix' will only be added to the lines\n    where 'predicate(line)' is True. If 'predicate' is not provided,\n    it will default to adding 'prefix' to all non-empty lines that do not\n    consist solely of whitespace characters.\n    ";A=predicate
	if A is _A:
		def A(line):return line.strip()
	def B():
		for B in text.splitlines(_B):yield prefix+B if A(B)else B
	return''.join(B())
if __name__=='__main__':print(dedent('Hello there.\n  This is indented.'))