"Generic output formatting.\n\nFormatter objects transform an abstract flow of formatting events into\nspecific output events on writer objects. Formatters manage several stack\nstructures to allow various properties of a writer object to be changed and\nrestored; writers need not be able to handle relative changes nor any sort\nof ``change back'' operation. Specific writer properties which may be\ncontrolled via formatter objects are horizontal alignment, font, and left\nmargin indentations. A mechanism is provided which supports providing\narbitrary, non-exclusive style settings to a writer as well. Additional\ninterfaces facilitate formatting events which are not reversible, such as\nparagraph separation.\n\nWriter objects encapsulate device interfaces. Abstract devices, such as\nfile formats, are supported as well as physical devices. The provided\nimplementations all work with abstract devices. The interface makes\navailable mechanisms for setting the properties which formatter objects\nmanage and inserting data into the output.\n"
_C=' '
_B='\n'
_A=None
import sys,warnings
warnings.warn('the formatter module is deprecated',DeprecationWarning,stacklevel=2)
AS_IS=_A
class NullFormatter:
	"A formatter which does nothing.\n\n    If the writer parameter is omitted, a NullWriter instance is created.\n    No methods of the writer are called by NullFormatter instances.\n\n    Implementations should inherit from this class if implementing a writer\n    interface but don't need to inherit any implementation.\n\n    "
	def __init__(B,writer=_A):
		A=writer
		if A is _A:A=NullWriter()
		B.writer=A
	def end_paragraph(A,blankline):0
	def add_line_break(A):0
	def add_hor_rule(A,*B,**C):0
	def add_label_data(A,format,counter,blankline=_A):0
	def add_flowing_data(A,data):0
	def add_literal_data(A,data):0
	def flush_softspace(A):0
	def push_alignment(A,align):0
	def pop_alignment(A):0
	def push_font(A,x):0
	def pop_font(A):0
	def push_margin(A,margin):0
	def pop_margin(A):0
	def set_spacing(A,spacing):0
	def push_style(A,*B):0
	def pop_style(A,n=1):0
	def assert_line_data(A,flag=1):0
class AbstractFormatter:
	'The standard formatter.\n\n    This implementation has demonstrated wide applicability to many writers,\n    and may be used directly in most circumstances.  It has been used to\n    implement a full-featured World Wide Web browser.\n\n    '
	def __init__(A,writer):A.writer=writer;A.align=_A;A.align_stack=[];A.font_stack=[];A.margin_stack=[];A.spacing=_A;A.style_stack=[];A.nospace=1;A.softspace=0;A.para_end=1;A.parskip=0;A.hard_break=1;A.have_label=0
	def end_paragraph(A,blankline):
		B=blankline
		if not A.hard_break:A.writer.send_line_break();A.have_label=0
		if A.parskip<B and not A.have_label:A.writer.send_paragraph(B-A.parskip);A.parskip=B;A.have_label=0
		A.hard_break=A.nospace=A.para_end=1;A.softspace=0
	def add_line_break(A):
		if not(A.hard_break or A.para_end):A.writer.send_line_break();A.have_label=A.parskip=0
		A.hard_break=A.nospace=1;A.softspace=0
	def add_hor_rule(A,*B,**C):
		if not A.hard_break:A.writer.send_line_break()
		A.writer.send_hor_rule(*B,**C);A.hard_break=A.nospace=1;A.have_label=A.para_end=A.softspace=A.parskip=0
	def add_label_data(A,format,counter,blankline=_A):
		if A.have_label or not A.hard_break:A.writer.send_line_break()
		if not A.para_end:A.writer.send_paragraph(blankline and 1 or 0)
		if isinstance(format,str):A.writer.send_label_data(A.format_counter(format,counter))
		else:A.writer.send_label_data(format)
		A.nospace=A.have_label=A.hard_break=A.para_end=1;A.softspace=A.parskip=0
	def format_counter(D,format,counter):
		C=counter;A=''
		for B in format:
			if B=='1':A=A+'%d'%C
			elif B in'aA':
				if C>0:A=A+D.format_letter(B,C)
			elif B in'iI':
				if C>0:A=A+D.format_roman(B,C)
			else:A=A+B
		return A
	def format_letter(E,case,counter):
		A=counter;B=''
		while A>0:A,C=divmod(A-1,26);D=chr(ord(case)+C);B=D+B
		return B
	def format_roman(H,case,counter):
		F=counter;D=['i','x','c','m'];G=['v','l','d'];A,B='',0
		while F>0:
			F,C=divmod(F,10)
			if C==9:A=D[B]+D[B+1]+A
			elif C==4:A=D[B]+G[B]+A
			else:
				if C>=5:E=G[B];C=C-5
				else:E=''
				E=E+D[B]*C;A=E+A
			B=B+1
		if case=='I':return A.upper()
		return A
	def add_flowing_data(A,data):
		B=data
		if not B:return
		C=B[:1].isspace();D=B[-1:].isspace();B=_C.join(B.split())
		if A.nospace and not B:return
		elif C or A.softspace:
			if not B:
				if not A.nospace:A.softspace=1;A.parskip=0
				return
			if not A.nospace:B=_C+B
		A.hard_break=A.nospace=A.para_end=A.parskip=A.have_label=0;A.softspace=D;A.writer.send_flowing_data(B)
	def add_literal_data(A,data):
		B=data
		if not B:return
		if A.softspace:A.writer.send_flowing_data(_C)
		A.hard_break=B[-1:]==_B;A.nospace=A.para_end=A.softspace=A.parskip=A.have_label=0;A.writer.send_literal_data(B)
	def flush_softspace(A):
		if A.softspace:A.hard_break=A.para_end=A.parskip=A.have_label=A.softspace=0;A.nospace=1;A.writer.send_flowing_data(_C)
	def push_alignment(A,align):
		B=align
		if B and B!=A.align:A.writer.new_alignment(B);A.align=B;A.align_stack.append(B)
		else:A.align_stack.append(A.align)
	def pop_alignment(A):
		if A.align_stack:del A.align_stack[-1]
		if A.align_stack:A.align=B=A.align_stack[-1];A.writer.new_alignment(B)
		else:A.align=_A;A.writer.new_alignment(_A)
	def push_font(A,font):
		B=font;C,D,E,F=B
		if A.softspace:A.hard_break=A.para_end=A.softspace=0;A.nospace=1;A.writer.send_flowing_data(_C)
		if A.font_stack:
			G,H,I,J=A.font_stack[-1]
			if C is AS_IS:C=G
			if D is AS_IS:D=H
			if E is AS_IS:E=I
			if F is AS_IS:F=J
		B=C,D,E,F;A.font_stack.append(B);A.writer.new_font(B)
	def pop_font(A):
		if A.font_stack:del A.font_stack[-1]
		if A.font_stack:B=A.font_stack[-1]
		else:B=_A
		A.writer.new_font(B)
	def push_margin(B,margin):
		A=margin;B.margin_stack.append(A);C=[A for A in B.margin_stack if A]
		if not A and C:A=C[-1]
		B.writer.new_margin(A,len(C))
	def pop_margin(A):
		if A.margin_stack:del A.margin_stack[-1]
		B=[A for A in A.margin_stack if A]
		if B:C=B[-1]
		else:C=_A
		A.writer.new_margin(C,len(B))
	def set_spacing(A,spacing):B=spacing;A.spacing=B;A.writer.new_spacing(B)
	def push_style(A,*B):
		if A.softspace:A.hard_break=A.para_end=A.softspace=0;A.nospace=1;A.writer.send_flowing_data(_C)
		for C in B:A.style_stack.append(C)
		A.writer.new_styles(tuple(A.style_stack))
	def pop_style(A,n=1):del A.style_stack[-n:];A.writer.new_styles(tuple(A.style_stack))
	def assert_line_data(A,flag=1):A.nospace=A.hard_break=not flag;A.para_end=A.parskip=A.have_label=0
class NullWriter:
	'Minimal writer interface to use in testing & inheritance.\n\n    A writer which only provides the interface definition; no actions are\n    taken on any methods.  This should be the base class for all writers\n    which do not need to inherit any implementation methods.\n\n    '
	def __init__(A):0
	def flush(A):0
	def new_alignment(A,align):0
	def new_font(A,font):0
	def new_margin(A,margin,level):0
	def new_spacing(A,spacing):0
	def new_styles(A,styles):0
	def send_paragraph(A,blankline):0
	def send_line_break(A):0
	def send_hor_rule(A,*B,**C):0
	def send_label_data(A,data):0
	def send_flowing_data(A,data):0
	def send_literal_data(A,data):0
class AbstractWriter(NullWriter):
	'A writer which can be used in debugging formatters, but not much else.\n\n    Each method simply announces itself by printing its name and\n    arguments on standard output.\n\n    '
	def new_alignment(A,align):print('new_alignment(%r)'%(align,))
	def new_font(A,font):print('new_font(%r)'%(font,))
	def new_margin(A,margin,level):print('new_margin(%r, %d)'%(margin,level))
	def new_spacing(A,spacing):print('new_spacing(%r)'%(spacing,))
	def new_styles(A,styles):print('new_styles(%r)'%(styles,))
	def send_paragraph(A,blankline):print('send_paragraph(%r)'%(blankline,))
	def send_line_break(A):print('send_line_break()')
	def send_hor_rule(A,*B,**C):print('send_hor_rule()')
	def send_label_data(A,data):print('send_label_data(%r)'%(data,))
	def send_flowing_data(A,data):print('send_flowing_data(%r)'%(data,))
	def send_literal_data(A,data):print('send_literal_data(%r)'%(data,))
class DumbWriter(NullWriter):
	'Simple writer class which writes output on the file object passed in\n    as the file parameter or, if file is omitted, on standard output.  The\n    output is simply word-wrapped to the number of columns specified by\n    the maxcol parameter.  This class is suitable for reflowing a sequence\n    of paragraphs.\n\n    '
	def __init__(A,file=_A,maxcol=72):A.file=file or sys.stdout;A.maxcol=maxcol;NullWriter.__init__(A);A.reset()
	def reset(A):A.col=0;A.atbreak=0
	def send_paragraph(A,blankline):A.file.write(_B*blankline);A.col=0;A.atbreak=0
	def send_line_break(A):A.file.write(_B);A.col=0;A.atbreak=0
	def send_hor_rule(A,*B,**C):A.file.write(_B);A.file.write('-'*A.maxcol);A.file.write(_B);A.col=0;A.atbreak=0
	def send_literal_data(B,data):
		A=data;B.file.write(A);C=A.rfind(_B)
		if C>=0:B.col=0;A=A[C+1:]
		A=A.expandtabs();B.col=B.col+len(A);B.atbreak=0
	def send_flowing_data(B,data):
		C=data
		if not C:return
		F=B.atbreak or C[0].isspace();A=B.col;G=B.maxcol;D=B.file.write
		for E in C.split():
			if F:
				if A+len(E)>=G:D(_B);A=0
				else:D(_C);A=A+1
			D(E);A=A+len(E);F=1
		B.col=A;B.atbreak=C[-1].isspace()
def test(file=_A):
	D=DumbWriter();B=AbstractFormatter(D)
	if file is not _A:A=open(file)
	elif sys.argv[1:]:A=open(sys.argv[1])
	else:A=sys.stdin
	try:
		for C in A:
			if C==_B:B.end_paragraph(1)
			else:B.add_flowing_data(C)
	finally:
		if A is not sys.stdin:A.close()
	B.end_paragraph(0)
if __name__=='__main__':test()