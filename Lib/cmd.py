'A generic class to build line-oriented command interpreters.\n\nInterpreters constructed with this class obey the following conventions:\n\n1. End of file on input is processed as the command \'EOF\'.\n2. A command is parsed out of each line by collecting the prefix composed\n   of characters in the identchars member.\n3. A command `foo\' is dispatched to a method \'do_foo()\'; the do_ method\n   is passed a single argument consisting of the remainder of the line.\n4. Typing an empty line repeats the last command.  (Actually, it calls the\n   method `emptyline\', which may be overridden in a subclass.)\n5. There is a predefined `help\' method.  Given an argument `topic\', it\n   calls the command `help_topic\'.  With no arguments, it lists all topics\n   with defined help_ functions, broken into up to three topics; documented\n   commands, miscellaneous help topics, and undocumented commands.\n6. The command \'?\' is a synonym for `help\'.  The command \'!\' is a synonym\n   for `shell\', if a do_shell method exists.\n7. If completion is enabled, completing commands will be done automatically,\n   and completing of commands args is done by calling complete_foo() with\n   arguments text, line, begidx, endidx.  text is string we are matching\n   against, all returned matches must begin with it.  line is the current\n   input line (lstripped), begidx and endidx are the beginning and end\n   indexes of the text being matched, which could be used to provide\n   different completion depending upon which position the argument is in.\n\nThe `default\' method may be overridden to intercept commands for which there\nis no do_ method.\n\nThe `completedefault\' method may be overridden to intercept completions for\ncommands that have no complete_ method.\n\nThe data member `self.ruler\' sets the character used to draw separator lines\nin the help messages.  If empty, no ruler line is drawn.  It defaults to "=".\n\nIf the value of `self.intro\' is nonempty when the cmdloop method is called,\nit is printed out on interpreter startup.  This value may be overridden\nvia an optional argument to the cmdloop() method.\n\nThe data members `self.doc_header\', `self.misc_header\', and\n`self.undoc_header\' set the headers used for the help function\'s\nlistings of documented functions, miscellaneous topics, and undocumented\nfunctions respectively.\n'
_E='help_'
_D='EOF'
_C='do_'
_B='%s\n'
_A=None
import string,sys
__all__=['Cmd']
PROMPT='(Cmd) '
IDENTCHARS=string.ascii_letters+string.digits+'_'
class Cmd:
	"A simple framework for writing line-oriented command interpreters.\n\n    These are often useful for test harnesses, administrative tools, and\n    prototypes that will later be wrapped in a more sophisticated interface.\n\n    A Cmd instance or subclass instance is a line-oriented interpreter\n    framework.  There is no good reason to instantiate Cmd itself; rather,\n    it's useful as a superclass of an interpreter class you define yourself\n    in order to inherit Cmd's methods and encapsulate action methods.\n\n    ";prompt=PROMPT;identchars=IDENTCHARS;ruler='=';lastcmd='';intro=_A;doc_leader='';doc_header='Documented commands (type help <topic>):';misc_header='Miscellaneous help topics:';undoc_header='Undocumented commands:';nohelp='*** No help on %s';use_rawinput=1
	def __init__(A,completekey='tab',stdin=_A,stdout=_A):
		"Instantiate a line-oriented interpreter framework.\n\n        The optional argument 'completekey' is the readline name of a\n        completion key; it defaults to the Tab key. If completekey is\n        not None and the readline module is available, command completion\n        is done automatically. The optional arguments stdin and stdout\n        specify alternate input and output file objects; if not specified,\n        sys.stdin and sys.stdout are used.\n\n        ";B=stdout;C=stdin
		if C is not _A:A.stdin=C
		else:A.stdin=sys.stdin
		if B is not _A:A.stdout=B
		else:A.stdout=sys.stdout
		A.cmdqueue=[];A.completekey=completekey
	def cmdloop(A,intro=_A):
		'Repeatedly issue a prompt, accept input, parse an initial prefix\n        off the received input, and dispatch to action methods, passing them\n        the remainder of the line as argument.\n\n        ';E=intro;A.preloop()
		if A.use_rawinput and A.completekey:
			try:import readline as C;A.old_completer=C.get_completer();C.set_completer(A.complete);C.parse_and_bind(A.completekey+': complete')
			except ImportError:pass
		try:
			if E is not _A:A.intro=E
			if A.intro:A.stdout.write(str(A.intro)+'\n')
			D=_A
			while not D:
				if A.cmdqueue:B=A.cmdqueue.pop(0)
				elif A.use_rawinput:
					try:B=input(A.prompt)
					except EOFError:B=_D
				else:
					A.stdout.write(A.prompt);A.stdout.flush();B=A.stdin.readline()
					if not len(B):B=_D
					else:B=B.rstrip('\r\n')
				B=A.precmd(B);D=A.onecmd(B);D=A.postcmd(D,B)
			A.postloop()
		finally:
			if A.use_rawinput and A.completekey:
				try:import readline as C;C.set_completer(A.old_completer)
				except ImportError:pass
	def precmd(A,line):'Hook method executed just before the command line is\n        interpreted, but after the input prompt is generated and issued.\n\n        ';return line
	def postcmd(A,stop,line):'Hook method executed just after a command dispatch is finished.';return stop
	def preloop(A):'Hook method executed once when the cmdloop() method is called.'
	def postloop(A):'Hook method executed once when the cmdloop() method is about to\n        return.\n\n        '
	def parseline(C,line):
		"Parse the line into a command name and a string containing\n        the arguments.  Returns a tuple containing (command, args, line).\n        'command' and 'args' may be None if the line couldn't be parsed.\n        ";A=line;A=A.strip()
		if not A:return _A,_A,A
		elif A[0]=='?':A='help '+A[1:]
		elif A[0]=='!':
			if hasattr(C,'do_shell'):A='shell '+A[1:]
			else:return _A,_A,A
		B,D=0,len(A)
		while B<D and A[B]in C.identchars:B=B+1
		E,F=A[:B],A[B:].strip();return E,F,A
	def onecmd(A,line):
		'Interpret the argument as though it had been typed in response\n        to the prompt.\n\n        This may be overridden, but should not normally need to be;\n        see the precmd() and postcmd() methods for useful execution hooks.\n        The return value is a flag indicating whether interpretation of\n        commands by the interpreter should stop.\n\n        ';B=line;C,D,B=A.parseline(B)
		if not B:return A.emptyline()
		if C is _A:return A.default(B)
		A.lastcmd=B
		if B==_D:A.lastcmd=''
		if C=='':return A.default(B)
		else:
			try:E=getattr(A,_C+C)
			except AttributeError:return A.default(B)
			return E(D)
	def emptyline(A):
		'Called when an empty line is entered in response to the prompt.\n\n        If this method is not overridden, it repeats the last nonempty\n        command entered.\n\n        '
		if A.lastcmd:return A.onecmd(A.lastcmd)
	def default(A,line):'Called on an input line when the command prefix is not recognized.\n\n        If this method is not overridden, it prints an error message and\n        returns.\n\n        ';A.stdout.write('*** Unknown syntax: %s\n'%line)
	def completedefault(A,*B):'Method called to complete an input line when no command-specific\n        complete_*() method is available.\n\n        By default, it returns an empty list.\n\n        ';return[]
	def completenames(A,text,*C):B=_C+text;return[A[3:]for A in A.get_names()if A.startswith(B)]
	def complete(A,text,state):
		"Return the next possible completion for 'text'.\n\n        If a command has not been entered, then complete against command list.\n        Otherwise try to call complete_<command> to get list of completions.\n        ";E=state
		if E==0:
			import readline as C;F=C.get_line_buffer();D=F.lstrip();G=len(F)-len(D);H=C.get_begidx()-G;J=C.get_endidx()-G
			if H>0:
				I,K,L=A.parseline(D)
				if I=='':B=A.completedefault
				else:
					try:B=getattr(A,'complete_'+I)
					except AttributeError:B=A.completedefault
			else:B=A.completenames
			A.completion_matches=B(text,D,H,J)
		try:return A.completion_matches[E]
		except IndexError:return
	def get_names(A):return dir(A.__class__)
	def complete_help(A,*B):C=set(A.completenames(*B));D=set(A[5:]for A in A.get_names()if A.startswith(_E+B[0]));return list(C|D)
	def do_help(A,arg):
		'List available commands with "help" or detailed help with "help cmd".';D=arg
		if D:
			try:J=getattr(A,_E+D)
			except AttributeError:
				try:
					G=getattr(A,_C+D).__doc__
					if G:A.stdout.write(_B%str(G));return
				except AttributeError:pass
				A.stdout.write(_B%str(A.nohelp%(D,)));return
			J()
		else:
			E=A.get_names();F=[];H=[];help={}
			for B in E:
				if B[:5]==_E:help[B[5:]]=1
			E.sort();I=''
			for B in E:
				if B[:3]==_C:
					if B==I:continue
					I=B;C=B[3:]
					if C in help:F.append(C);del help[C]
					elif getattr(A,B).__doc__:F.append(C)
					else:H.append(C)
			A.stdout.write(_B%str(A.doc_leader));A.print_topics(A.doc_header,F,15,80);A.print_topics(A.misc_header,list(help.keys()),15,80);A.print_topics(A.undoc_header,H,15,80)
	def print_topics(A,header,cmds,cmdlen,maxcol):
		B=header
		if cmds:
			A.stdout.write(_B%str(B))
			if A.ruler:A.stdout.write(_B%str(A.ruler*len(B)))
			A.columnize(cmds,maxcol-1);A.stdout.write('\n')
	def columnize(H,list,displaywidth=80):
		'Display a list of strings as a compact set of columns.\n\n        Each column is only as wide as necessary.\n        Columns are separated by two spaces (one was not legible enough).\n        ';M=displaywidth
		if not list:H.stdout.write('<empty>\n');return
		N=[A for A in range(len(list))if not isinstance(list[A],str)]
		if N:raise TypeError('list[i] not a string for i in %s'%', '.join(map(str,N)))
		E=len(list)
		if E==1:H.stdout.write(_B%str(list[0]));return
		for B in range(1,len(list)):
			I=(E+B-1)//B;J=[];K=-2
			for C in range(I):
				F=0
				for L in range(B):
					D=L+B*C
					if D>=E:break
					G=list[D];F=max(F,len(G))
				J.append(F);K+=F+2
				if K>M:break
			if K<=M:break
		else:B=len(list);I=1;J=[0]
		for L in range(B):
			A=[]
			for C in range(I):
				D=L+B*C
				if D>=E:G=''
				else:G=list[D]
				A.append(G)
			while A and not A[-1]:del A[-1]
			for C in range(len(A)):A[C]=A[C].ljust(J[C])
			H.stdout.write(_B%str('  '.join(A)))