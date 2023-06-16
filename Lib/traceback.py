'Extract, format and print information about Python stack traces.'
_D='    {}\n'
_C=False
_B=True
_A=None
import collections,itertools,linecache,sys
__all__=['extract_stack','extract_tb','format_exception','format_exception_only','format_list','format_stack','format_tb','print_exc','format_exc','print_exception','print_last','print_stack','print_tb','clear_frames','FrameSummary','StackSummary','TracebackException','walk_stack','walk_tb']
def print_list(extracted_list,file=_A):
	'Print the list of tuples as returned by extract_tb() or\n    extract_stack() as a formatted stack trace to the given file.';A=file
	if A is _A:A=sys.stderr
	for B in StackSummary.from_list(extracted_list).format():print(B,file=A,end='')
def format_list(extracted_list):'Format a list of tuples or FrameSummary objects for printing.\n\n    Given a list of tuples or FrameSummary objects as returned by\n    extract_tb() or extract_stack(), return a list of strings ready\n    for printing.\n\n    Each string in the resulting list corresponds to the item with the\n    same index in the argument list.  Each string ends in a newline;\n    the strings may contain internal newlines as well, for those items\n    whose source text line is not None.\n    ';return StackSummary.from_list(extracted_list).format()
def print_tb(tb,limit=_A,file=_A):"Print up to 'limit' stack trace entries from the traceback 'tb'.\n\n    If 'limit' is omitted or None, all entries are printed.  If 'file'\n    is omitted or None, the output goes to sys.stderr; otherwise\n    'file' should be an open file or file-like object with a write()\n    method.\n    ";print_list(extract_tb(tb,limit=limit),file=file)
def format_tb(tb,limit=_A):"A shorthand for 'format_list(extract_tb(tb, limit))'.";return extract_tb(tb,limit=limit).format()
def extract_tb(tb,limit=_A):"\n    Return a StackSummary object representing a list of\n    pre-processed entries from traceback.\n\n    This is useful for alternate formatting of stack traces.  If\n    'limit' is omitted or None, all entries are extracted.  A\n    pre-processed stack trace entry is a FrameSummary object\n    containing attributes filename, lineno, name, and line\n    representing the information that is usually printed for a stack\n    trace.  The line is a string with leading and trailing\n    whitespace stripped; if the source is not available it is None.\n    ";return StackSummary.extract(walk_tb(tb),limit=limit)
_cause_message='\nThe above exception was the direct cause of the following exception:\n\n'
_context_message='\nDuring handling of the above exception, another exception occurred:\n\n'
class _Sentinel:
	def __repr__(A):return'<implicit>'
_sentinel=_Sentinel()
def _parse_value_tb(exc,value,tb):
	A=value;B=exc
	if(A is _sentinel)!=(tb is _sentinel):raise ValueError('Both or neither of value and tb must be given')
	if A is tb is _sentinel:
		if B is not _A:return B,B.__traceback__
		else:return _A,_A
	return A,tb
def print_exception(C,value=_sentinel,tb=_sentinel,limit=_A,file=_A,chain=_B):
	'Print exception up to \'limit\' stack trace entries from \'tb\' to \'file\'.\n\n    This differs from print_tb() in the following ways: (1) if\n    traceback is not None, it prints a header "Traceback (most recent\n    call last):"; (2) it prints the exception type and value after the\n    stack trace; (3) if type is SyntaxError and value has the\n    appropriate format, it prints the line where the syntax error\n    occurred with a caret on the next line indicating the approximate\n    position of the error.\n    ';B=file;A=value;A,tb=_parse_value_tb(C,A,tb)
	if B is _A:B=sys.stderr
	D=TracebackException(type(A),A,tb,limit=limit,compact=_B)
	for E in D.format(chain=chain):print(E,file=B,end='')
def format_exception(B,value=_sentinel,tb=_sentinel,limit=_A,chain=_B):'Format a stack trace and the exception information.\n\n    The arguments have the same meaning as the corresponding arguments\n    to print_exception().  The return value is a list of strings, each\n    ending in a newline and some containing internal newlines.  When\n    these lines are concatenated and printed, exactly the same text is\n    printed as does print_exception().\n    ';A=value;A,tb=_parse_value_tb(B,A,tb);C=TracebackException(type(A),A,tb,limit=limit,compact=_B);return list(C.format(chain=chain))
def format_exception_only(B,value=_sentinel):
	'Format the exception part of a traceback.\n\n    The return value is a list of strings, each ending in a newline.\n\n    Normally, the list contains a single string; however, for\n    SyntaxError exceptions, it contains several lines that (when\n    printed) display detailed information about where the syntax\n    error occurred.\n\n    The message indicating which exception occurred is always the last\n    string in the list.\n\n    ';A=value
	if A is _sentinel:A=B
	C=TracebackException(type(A),A,_A,compact=_B);return list(C.format_exception_only())
def _format_final_exc_line(etype,value):
	A=value;B=etype;C=_some_str(A)
	if A is _A or not C:D='%s\n'%B
	else:D='%s: %s\n'%(B,C)
	return D
def _some_str(value):
	A=value
	try:return str(A)
	except:return'<unprintable %s object>'%type(A).__name__
def print_exc(limit=_A,file=_A,chain=_B):"Shorthand for 'print_exception(*sys.exc_info(), limit, file)'.";print_exception(*sys.exc_info(),limit=limit,file=file,chain=chain)
def format_exc(limit=_A,chain=_B):'Like print_exc() but return a string.';return''.join(format_exception(*sys.exc_info(),limit=limit,chain=chain))
def print_last(limit=_A,file=_A,chain=_B):
	"This is a shorthand for 'print_exception(sys.last_type,\n    sys.last_value, sys.last_traceback, limit, file)'."
	if not hasattr(sys,'last_type'):raise ValueError('no last exception')
	print_exception(sys.last_type,sys.last_value,sys.last_traceback,limit,file,chain)
def print_stack(f=_A,limit=_A,file=_A):
	"Print a stack trace from its invocation point.\n\n    The optional 'f' argument can be used to specify an alternate\n    stack frame at which to start. The optional 'limit' and 'file'\n    arguments have the same meaning as for print_exception().\n    "
	if f is _A:f=sys._getframe().f_back
	print_list(extract_stack(f,limit=limit),file=file)
def format_stack(f=_A,limit=_A):
	"Shorthand for 'format_list(extract_stack(f, limit))'."
	if f is _A:f=sys._getframe().f_back
	return format_list(extract_stack(f,limit=limit))
def extract_stack(f=_A,limit=_A):
	"Extract the raw traceback from the current stack frame.\n\n    The return value has the same format as for extract_tb().  The\n    optional 'f' and 'limit' arguments have the same meaning as for\n    print_stack().  Each item in the list is a quadruple (filename,\n    line number, function name, text), and the entries are in order\n    from oldest to newest stack frame.\n    "
	if f is _A:f=sys._getframe().f_back
	A=StackSummary.extract(walk_stack(f),limit=limit);A.reverse();return A
def clear_frames(tb):
	'Clear all references to local variables in the frames of a traceback.'
	while tb is not _A:
		try:tb.tb_frame.clear()
		except RuntimeError:pass
		tb=tb.tb_next
class FrameSummary:
	'A single frame from a traceback.\n\n    - :attr:`filename` The filename for the frame.\n    - :attr:`lineno` The line within filename for the frame that was\n      active when the frame was captured.\n    - :attr:`name` The name of the function or method that was executing\n      when the frame was captured.\n    - :attr:`line` The text from the linecache module for the\n      of code that was running when the frame was captured.\n    - :attr:`locals` Either None if locals were not supplied, or a dict\n      mapping the name to the repr() of the variable.\n    ';__slots__='filename','lineno','name','_line','locals'
	def __init__(A,filename,lineno,name,*,lookup_line=_B,locals=_A,line=_A):
		'Construct a FrameSummary.\n\n        :param lookup_line: If True, `linecache` is consulted for the source\n            code line. Otherwise, the line will be looked up when first needed.\n        :param locals: If supplied the frame locals, which will be captured as\n            object representations.\n        :param line: If provided, use this instead of looking up the line in\n            the linecache.\n        ';A.filename=filename;A.lineno=lineno;A.name=name;A._line=line
		if lookup_line:A.line
		A.locals={A:repr(B)for(A,B)in locals.items()}if locals else _A
	def __eq__(A,other):
		B=other
		if isinstance(B,FrameSummary):return A.filename==B.filename and A.lineno==B.lineno and A.name==B.name and A.locals==B.locals
		if isinstance(B,tuple):return(A.filename,A.lineno,A.name,A.line)==B
		return NotImplemented
	def __getitem__(A,pos):return(A.filename,A.lineno,A.name,A.line)[pos]
	def __iter__(A):return iter([A.filename,A.lineno,A.name,A.line])
	def __repr__(A):return'<FrameSummary file {filename}, line {lineno} in {name}>'.format(filename=A.filename,lineno=A.lineno,name=A.name)
	def __len__(A):return 4
	@property
	def line(self):
		A=self
		if A._line is _A:
			if A.lineno is _A:return
			A._line=linecache.getline(A.filename,A.lineno)
		return A._line.strip()
def walk_stack(f):
	'Walk a stack yielding the frame and line number for each frame.\n\n    This will follow f.f_back from the given frame. If no frame is given, the\n    current stack is used. Usually used with StackSummary.extract.\n    '
	if f is _A:f=sys._getframe().f_back.f_back
	while f is not _A:yield(f,f.f_lineno);f=f.f_back
def walk_tb(tb):
	'Walk a traceback yielding the frame and line number for each frame.\n\n    This will follow tb.tb_next (and thus is in the opposite order to\n    walk_stack). Usually used with StackSummary.extract.\n    ';A=tb
	while A is not _A:yield(A.tb_frame,A.tb_lineno);A=A.tb_next
_RECURSIVE_CUTOFF=3
class StackSummary(list):
	'A stack of frames.'
	@classmethod
	def extract(I,frame_gen,*,limit=_A,lookup_lines=_B,capture_locals=_C):
		'Create a StackSummary from a traceback or stack object.\n\n        :param frame_gen: A generator that yields (frame, lineno) tuples to\n            include in the stack.\n        :param limit: None to include all frames or the number of frames to\n            include.\n        :param lookup_lines: If True, lookup lines for each frame immediately,\n            otherwise lookup is deferred until the frame is rendered.\n        :param capture_locals: If True, the local variables from each frame will\n            be captured as object representations into the FrameSummary.\n        ';B=frame_gen;A=limit
		if A is _A:
			A=getattr(sys,'tracebacklimit',_A)
			if A is not _A and A<0:A=0
		if A is not _A:
			if A>=0:B=itertools.islice(B,A)
			else:B=collections.deque(B,maxlen=-A)
		E=I();F=set()
		for(C,J)in B:
			G=C.f_code;D=G.co_filename;K=G.co_name;F.add(D);linecache.lazycache(D,C.f_globals)
			if capture_locals:H=C.f_locals
			else:H=_A
			E.append(FrameSummary(D,J,K,lookup_line=_C,locals=H))
		for D in F:linecache.checkcache(D)
		if lookup_lines:
			for C in E:C.line
		return E
	@classmethod
	def from_list(G,a_list):
		'\n        Create a StackSummary object from a supplied list of\n        FrameSummary objects or old-style list of tuples.\n        ';A=StackSummary()
		for B in a_list:
			if isinstance(B,FrameSummary):A.append(B)
			else:C,D,E,F=B;A.append(FrameSummary(C,D,E,line=F))
		return A
	def format(H):
		'Format the stack ready for printing.\n\n        Returns a list of strings ready for printing.  Each string in the\n        resulting list corresponds to a single frame from the stack.\n        Each string ends in a newline; the strings may contain internal\n        newlines as well, for those items with source text lines.\n\n        For long sequences of the same frame and line, the first few\n        repetitions are shown, followed by a summary line stating the exact\n        number of further repetitions.\n        ';C=[];E=_A;F=_A;G=_A;B=0
		for A in H:
			if E is _A or E!=A.filename or F is _A or F!=A.lineno or G is _A or G!=A.name:
				if B>_RECURSIVE_CUTOFF:B-=_RECURSIVE_CUTOFF;C.append(f"  [Previous line repeated {B} more time{'s'if B>1 else''}]\n")
				E=A.filename;F=A.lineno;G=A.name;B=0
			B+=1
			if B>_RECURSIVE_CUTOFF:continue
			D=[];D.append('  File "{}", line {}, in {}\n'.format(A.filename,A.lineno,A.name))
			if A.line:D.append(_D.format(A.line.strip()))
			if A.locals:
				for(I,J)in sorted(A.locals.items()):D.append('    {name} = {value}\n'.format(name=I,value=J))
			C.append(''.join(D))
		if B>_RECURSIVE_CUTOFF:B-=_RECURSIVE_CUTOFF;C.append(f"  [Previous line repeated {B} more time{'s'if B>1 else''}]\n")
		return C
class TracebackException:
	'An exception ready for rendering.\n\n    The traceback module captures enough attributes from the original exception\n    to this intermediary form to ensure that no references are held, while\n    still being able to fully print or format it.\n\n    Use `from_exception` to create TracebackException instances from exception\n    objects, or the constructor to create TracebackException instances from\n    individual components.\n\n    - :attr:`__cause__` A TracebackException of the original *__cause__*.\n    - :attr:`__context__` A TracebackException of the original *__context__*.\n    - :attr:`__suppress_context__` The *__suppress_context__* value from the\n      original exception.\n    - :attr:`stack` A `StackSummary` representing the traceback.\n    - :attr:`exc_type` The class of the original traceback.\n    - :attr:`filename` For syntax errors - the filename where the error\n      occurred.\n    - :attr:`lineno` For syntax errors - the linenumber where the error\n      occurred.\n    - :attr:`end_lineno` For syntax errors - the end linenumber where the error\n      occurred. Can be `None` if not present.\n    - :attr:`text` For syntax errors - the text where the error\n      occurred.\n    - :attr:`offset` For syntax errors - the offset into the text where the\n      error occurred.\n    - :attr:`end_offset` For syntax errors - the offset into the text where the\n      error occurred. Can be `None` if not present.\n    - :attr:`msg` For syntax errors - the compiler error message.\n    '
	def __init__(B,exc_type,exc_value,exc_traceback,*,limit=_A,lookup_lines=_B,capture_locals=_C,compact=_C,_seen=_A):
		I=capture_locals;J=limit;K=exc_type;E=lookup_lines;D=_seen;C=exc_value;P=D is not _A
		if D is _A:D=set()
		D.add(id(C));B.stack=StackSummary.extract(walk_tb(exc_traceback),limit=J,lookup_lines=E,capture_locals=I);B.exc_type=K;B._str=_some_str(C)
		if K and issubclass(K,SyntaxError):B.filename=C.filename;M=C.lineno;B.lineno=str(M)if M is not _A else _A;N=C.end_lineno;B.end_lineno=str(N)if N is not _A else _A;B.text=C.text;B.offset=C.offset;B.end_offset=C.end_offset;B.msg=C.msg
		if E:B._load_lines()
		B.__suppress_context__=C.__suppress_context__ if C is not _A else _C
		if not P:
			F=[(B,C)]
			while F:
				G,A=F.pop()
				if A and A.__cause__ is not _A and id(A.__cause__)not in D:H=TracebackException(type(A.__cause__),A.__cause__,A.__cause__.__traceback__,limit=J,lookup_lines=E,capture_locals=I,_seen=D)
				else:H=_A
				if compact:O=H is _A and A is not _A and not A.__suppress_context__
				else:O=_B
				if A and A.__context__ is not _A and O and id(A.__context__)not in D:L=TracebackException(type(A.__context__),A.__context__,A.__context__.__traceback__,limit=J,lookup_lines=E,capture_locals=I,_seen=D)
				else:L=_A
				G.__cause__=H;G.__context__=L
				if H:F.append((G.__cause__,A.__cause__))
				if L:F.append((G.__context__,A.__context__))
	@classmethod
	def from_exception(B,exc,*C,**D):'Create a TracebackException from an exception.';A=exc;return B(type(A),A,A.__traceback__,*C,**D)
	def _load_lines(A):
		'Private API. force all lines in the stack to be loaded.'
		for B in A.stack:B.line
	def __eq__(B,other):
		A=other
		if isinstance(A,TracebackException):return B.__dict__==A.__dict__
		return NotImplemented
	def __str__(A):return A._str
	def format_exception_only(A):
		'Format the exception part of the traceback.\n\n        The return value is a generator of strings, each ending in a newline.\n\n        Normally, the generator emits a single string; however, for\n        SyntaxError exceptions, it emits several lines that (when\n        printed) display detailed information about where the syntax\n        error occurred.\n\n        The message indicating which exception occurred is always the last\n        string in the output.\n        '
		if A.exc_type is _A:yield _format_final_exc_line(_A,A._str);return
		B=A.exc_type.__qualname__;C=A.exc_type.__module__
		if C not in('__main__','builtins'):
			if not isinstance(C,str):C='<unknown>'
			B=C+'.'+B
		if not issubclass(A.exc_type,SyntaxError):yield _format_final_exc_line(B,A._str)
		else:yield from A._format_syntax_error(B)
	def _format_syntax_error(A,stype):
		'Format SyntaxError exceptions (internal helper).';F=''
		if A.lineno is not _A:yield'  File "{}", line {}\n'.format(A.filename or'<string>',A.lineno)
		elif A.filename is not _A:F=' ({})'.format(A.filename)
		G=A.text
		if G is not _A:
			H=G.rstrip('\n');D=H.lstrip(' \n\x0c');I=len(H)-len(D);yield _D.format(D)
			if A.offset is not _A:
				B=A.offset;C=A.end_offset if A.end_offset not in{_A,0}else B
				if B==C or C==-1:C=B+1
				E=B-1-I;J=C-1-I
				if E>=0:K=(A if A.isspace()else' 'for A in D[:E]);yield'    {}{}'.format(''.join(K),'^'*(J-E)+'\n')
		L=A.msg or'<no detail available>';yield'{}: {}{}\n'.format(stype,L,F)
	def format(F,*,chain=_B):
		'Format the exception.\n\n        If chain is not *True*, *__cause__* and *__context__* will not be formatted.\n\n        The return value is a generator of strings, each ending in a newline and\n        some containing internal newlines. `print_exception` is a wrapper around\n        this method which just prints the lines to a file.\n\n        The message indicating which exception occurred is always the last\n        string in the output.\n        ';B=[];A=F
		while A:
			if chain:
				if A.__cause__ is not _A:C=_cause_message;D=A.__cause__
				elif A.__context__ is not _A and not A.__suppress_context__:C=_context_message;D=A.__context__
				else:C=_A;D=_A
				B.append((C,A));A=D
			else:B.append((_A,A));A=_A
		for(E,A)in reversed(B):
			if E is not _A:yield E
			if A.stack:yield'Traceback (most recent call last):\n';yield from A.stack.format()
			yield from A.format_exception_only()