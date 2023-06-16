"More comprehensive traceback formatting for Python scripts.\n\nTo enable this module, do:\n\n    import cgitb; cgitb.enable()\n\nat the top of your script.  The optional arguments to enable() are:\n\n    display     - if true, tracebacks are displayed in the web browser\n    logdir      - if set, tracebacks are written to files in this directory\n    context     - number of lines of source code to show for each stack frame\n    format      - 'text' or 'html' controls the output format\n\nBy default, tracebacks are displayed but not saved, the context is 5 lines\nand the output format is 'html' (for backwards compatibility with the\noriginal use of this module)\n\nAlternatively, if you have caught an exception and want cgitb to display it\nfor you, call cgitb.handler().  The optional argument to handler() is a\n3-item tuple (etype, evalue, etb) just like the value of sys.exc_info().\nThe default handler displays output as HTML.\n\n"
_H='<module>'
_G='Python '
_F='builtin'
_E='global'
_D='local'
_C='\n'
_B='html'
_A=None
import inspect,keyword,linecache,os,pydoc,sys,tempfile,time,tokenize,traceback
def reset():'Return a string that resets the CGI and browser to a known state.';return'<!--: spam\nContent-Type: text/html\n\n<body bgcolor="#f0f0f8"><font color="#f0f0f8" size="-5"> -->\n<body bgcolor="#f0f0f8"><font color="#f0f0f8" size="-5"> --> -->\n</font> </font> </font> </script> </object> </blockquote> </pre>\n</table> </table> </table> </table> </table> </font> </font> </font>'
__UNDEF__=[]
def small(text):
	if text:return'<small>'+text+'</small>'
	else:return''
def strong(text):
	if text:return'<strong>'+text+'</strong>'
	else:return''
def grey(text):
	if text:return'<font color="#909090">'+text+'</font>'
	else:return''
def lookup(name,frame,locals):
	'Find the value for a given name in the given environment.';D='__builtins__';C=frame;A=name
	if A in locals:return _D,locals[A]
	if A in C.f_globals:return _E,C.f_globals[A]
	if D in C.f_globals:
		B=C.f_globals[D]
		if type(B)is type({}):
			if A in B:return _F,B[A]
		elif hasattr(B,A):return _F,getattr(B,A)
	return _A,__UNDEF__
def scanvars(reader,frame,locals):
	'Scan one logical line of Python and look up values of variables used.';vars,E,C,D,B=[],_A,_A,'',__UNDEF__
	for(F,A,H,I,J)in tokenize.generate_tokens(reader):
		if F==tokenize.NEWLINE:break
		if F==tokenize.NAME and A not in keyword.kwlist:
			if E=='.':
				if C is not __UNDEF__:B=getattr(C,A,__UNDEF__);vars.append((D+A,D,B))
			else:G,B=lookup(A,frame,locals);vars.append((A,G,B))
		elif A=='.':D+=E+'.';C=B
		else:C,D=_A,''
		E=A
	return vars
def html(einfo,context=5):
	'Return a nice HTML document describing a given traceback.';N='<tr><td>%s</td></tr>';J='&nbsp;';C,E,O=einfo
	if isinstance(C,type):C=C.__name__
	Y=_G+sys.version.split()[0]+': '+sys.executable;Z=time.ctime(time.time());a='<body bgcolor="#f0f0f8">'+pydoc.html.heading('<big><big>%s</big></big>'%strong(pydoc.html.escape(str(C))),'#ffffff','#6622aa',Y+'<br>'+Z)+'\n<p>A problem occurred in a Python script.  Here is the sequence of\nfunction calls leading up to the error, in the order they occurred.</p>';b='<tt>'+small(J*5)+'&nbsp;</tt>';P=[];c=inspect.getinnerframes(O,context)
	for(Q,B,R,K,d,S)in c:
		if B:B=os.path.abspath(B);T='<a href="file://%s">%s</a>'%(B,pydoc.html.escape(B))
		else:B=T='?'
		e,f,g,locals=inspect.getargvalues(Q);L=''
		if K!='?':
			L='in '+strong(pydoc.html.escape(K))
			if K!=_H:L+=inspect.formatargvalues(e,f,g,locals,formatvalue=lambda value:'='+pydoc.html.repr(value))
		U={}
		def h(lnum=[R]):
			A=lnum;U[A[0]]=1
			try:return linecache.getline(B,A[0])
			finally:A[0]+=1
		vars=scanvars(h,Q,locals);F=['<tr><td bgcolor="#d8bbff">%s%s %s</td></tr>'%('<big>&nbsp;</big>',T,L)]
		if S is not _A:
			G=R-S
			for D in d:
				V=small(J*(5-len(str(G)))+str(G))+J
				if G in U:D='<tt>=&gt;%s%s</tt>'%(V,pydoc.html.preformat(D));F.append('<tr><td bgcolor="#ffccee">%s</td></tr>'%D)
				else:D='<tt>&nbsp;&nbsp;%s%s</tt>'%(V,pydoc.html.preformat(D));F.append(N%grey(D))
				G+=1
		W,M={},[]
		for(A,H,I)in vars:
			if A in W:continue
			W[A]=1
			if I is not __UNDEF__:
				if H in(_E,_F):A='<em>%s</em> '%H+strong(A)
				elif H==_D:A=strong(A)
				else:A=H+strong(A.split('.')[-1])
				M.append('%s&nbsp;= %s'%(A,pydoc.html.repr(I)))
			else:M.append(A+' <em>undefined</em>')
		F.append(N%small(grey(', '.join(M))));P.append('\n<table width="100%%" cellspacing=0 cellpadding=0 border=0>\n%s</table>'%_C.join(F))
	X=['<p>%s: %s'%(strong(pydoc.html.escape(str(C))),pydoc.html.escape(str(E)))]
	for A in dir(E):
		if A[:1]=='_':continue
		I=pydoc.html.repr(getattr(E,A));X.append('\n<br>%s%s&nbsp;=\n%s'%(b,A,I))
	return a+''.join(P)+''.join(X)+"\n\n\n<!-- The above is a description of an error in a Python program, formatted\n     for a Web browser because the 'cgitb' module was enabled.  In case you\n     are not reading this in a Web browser, here is the original traceback:\n\n%s\n-->\n"%pydoc.html.escape(''.join(traceback.format_exception(C,E,O)))
def text(einfo,context=5):
	'Return a plain text document describing a given traceback.';B,D,K=einfo
	if isinstance(B,type):B=B.__name__
	S=_G+sys.version.split()[0]+': '+sys.executable;T=time.ctime(time.time());U='%s\n%s\n%s\n'%(str(B),S,T)+'\nA problem occurred in a Python script.  Here is the sequence of\nfunction calls leading up to the error, in the order they occurred.\n';L=[];V=inspect.getinnerframes(K,context)
	for(M,C,N,F,W,O)in V:
		C=C and os.path.abspath(C)or'?';X,Y,Z,locals=inspect.getargvalues(M);G=''
		if F!='?':
			G='in '+F
			if F!=_H:G+=inspect.formatargvalues(X,Y,Z,locals,formatvalue=lambda value:'='+pydoc.text.repr(value))
		a={}
		def b(lnum=[N]):
			A=lnum;a[A[0]]=1
			try:return linecache.getline(C,A[0])
			finally:A[0]+=1
		vars=scanvars(b,M,locals);H=[' %s %s'%(C,G)]
		if O is not _A:
			P=N-O
			for c in W:d='%5d '%P;H.append(d+c.rstrip());P+=1
		Q,I={},[]
		for(A,J,E)in vars:
			if A in Q:continue
			Q[A]=1
			if E is not __UNDEF__:
				if J==_E:A='global '+A
				elif J!=_D:A=J+A.split('.')[-1]
				I.append('%s = %s'%(A,pydoc.text.repr(E)))
			else:I.append(A+' undefined')
		H.append(_C.join(I));L.append('\n%s\n'%_C.join(H))
	R=['%s: %s'%(str(B),str(D))]
	for A in dir(D):E=pydoc.text.repr(getattr(D,A));R.append('\n%s%s = %s'%(' '*4,A,E))
	return U+''.join(L)+''.join(R)+'\n\nThe above is a description of an error in a Python program.  Here is\nthe original traceback:\n\n%s\n'%''.join(traceback.format_exception(B,D,K))
class Hook:
	'A hook to replace sys.excepthook that shows tracebacks in HTML.'
	def __init__(A,display=1,logdir=_A,context=5,file=_A,format=_B):A.display=display;A.logdir=logdir;A.context=context;A.file=file or sys.stdout;A.format=format
	def __call__(A,etype,evalue,etb):A.handle((etype,evalue,etb))
	def handle(A,info=_A):
		C=info;C=C or sys.exc_info()
		if A.format==_B:A.file.write(reset())
		G=A.format==_B and html or text;E=False
		try:B=G(C,A.context)
		except:B=''.join(traceback.format_exception(*C));E=True
		if A.display:
			if E:B=pydoc.html.escape(B);A.file.write('<pre>'+B+'</pre>\n')
			else:A.file.write(B+_C)
		else:A.file.write('<p>A problem occurred in a Python script.\n')
		if A.logdir is not _A:
			H=['.txt','.html'][A.format==_B];I,F=tempfile.mkstemp(suffix=H,dir=A.logdir)
			try:
				with os.fdopen(I,'w')as J:J.write(B)
				D='%s contains the description of this error.'%F
			except:D='Tried to save traceback to %s, but failed.'%F
			if A.format==_B:A.file.write('<p>%s</p>\n'%D)
			else:A.file.write(D+_C)
		try:A.file.flush()
		except:pass
handler=Hook().handle
def enable(display=1,logdir=_A,context=5,format=_B):"Install an exception handler that formats tracebacks as HTML.\n\n    The optional argument 'display' can be set to 0 to suppress sending the\n    traceback to the browser, and 'logdir' can be set to a directory to cause\n    tracebacks to be written to files there.";sys.excepthook=Hook(display=display,logdir=logdir,context=context,format=format)