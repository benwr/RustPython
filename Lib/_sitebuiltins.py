'\nThe objects used by the site module to add custom builtins.\n'
_A=None
import sys
class Quitter:
	def __init__(A,name,eof):A.name=name;A.eof=eof
	def __repr__(A):return'Use %s() or %s to exit'%(A.name,A.eof)
	def __call__(A,code=_A):
		try:sys.stdin.close()
		except:pass
		raise SystemExit(code)
class _Printer:
	'interactive prompt objects for printing the license text, a list of\n    contributors and the copyright notice.';MAXLINES=23
	def __init__(A,name,data,files=(),dirs=()):import os;A.__name=name;A.__data=data;A.__lines=_A;A.__filenames=[os.path.join(dir,A)for dir in dirs for A in files]
	def __setup(A):
		if A.__lines:return
		B=_A
		for C in A.__filenames:
			try:
				with open(C,'r')as D:B=D.read()
				break
			except OSError:pass
		if not B:B=A.__data
		A.__lines=B.split('\n');A.__linecnt=len(A.__lines)
	def __repr__(A):
		A.__setup()
		if len(A.__lines)<=A.MAXLINES:return'\n'.join(A.__lines)
		else:return'Type %s() to see the full %s text'%((A.__name,)*2)
	def __call__(B):
		B.__setup();D='Hit Return for more, or q (and Return) to quit: ';C=0
		while 1:
			try:
				for E in range(C,C+B.MAXLINES):print(B.__lines[E])
			except IndexError:break
			else:
				C+=B.MAXLINES;A=_A
				while A is _A:
					A=input(D)
					if A not in('','q'):A=_A
				if A=='q':break
class _Helper:
	"Define the builtin 'help'.\n\n    This is a wrapper around pydoc.help that provides a helpful message\n    when 'help' is typed at the Python interactive prompt.\n\n    Calling help() at the Python prompt starts an interactive help session.\n    Calling help(thing) prints help for the python object 'thing'.\n    "
	def __repr__(A):return'Type help() for interactive help, or help(object) for help about object.'
	def __call__(C,*A,**B):import pydoc;return pydoc.help(*A,**B)