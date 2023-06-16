'Shared support for scanning document type declarations in HTML and XHTML.\n\nThis module is used as a foundation for the html.parser module.  It has no\ndocumented public API and should not be used directly.\n\n'
_D='element'
_C='attlist'
_B='\'"'
_A='>'
import re
_declname_match=re.compile('[a-zA-Z][-_.a-zA-Z0-9]*\\s*').match
_declstringlit_match=re.compile('(\\\'[^\\\']*\\\'|"[^"]*")\\s*').match
_commentclose=re.compile('--\\s*>')
_markedsectionclose=re.compile(']\\s*]\\s*>')
_msmarkedsectionclose=re.compile(']\\s*>')
del re
class ParserBase:
	'Parser base class which provides some common support methods used\n    by the SGML/HTML and XHTML parsers.'
	def __init__(A):
		if A.__class__ is ParserBase:raise RuntimeError('_markupbase.ParserBase must be subclassed')
	def reset(A):A.lineno=1;A.offset=0
	def getpos(A):'Return current line number and offset.';return A.lineno,A.offset
	def updatepos(A,i,j):
		if i>=j:return j
		B=A.rawdata;C=B.count('\n',i,j)
		if C:A.lineno=A.lineno+C;D=B.rindex('\n',i,j);A.offset=j-(D+1)
		else:A.offset=A.offset+j-i
		return j
	_decl_otherchars=''
	def parse_declaration(B,i):
		F='doctype';C=B.rawdata;A=i+2;assert C[i:A]=='<!','unexpected call to parse_declaration'
		if C[A:A+1]==_A:return A+1
		if C[A:A+1]in('-',''):return-1
		I=len(C)
		if C[A:A+2]=='--':return B.parse_comment(i)
		elif C[A]=='[':return B.parse_marked_section(i)
		else:D,A=B._scan_name(A,i)
		if A<0:return A
		if D==F:B._decl_otherchars=''
		while A<I:
			E=C[A]
			if E==_A:
				G=C[i+2:A]
				if D==F:B.handle_decl(G)
				else:B.unknown_decl(G)
				return A+1
			if E in'"\'':
				H=_declstringlit_match(C,A)
				if not H:return-1
				A=H.end()
			elif E in'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':J,A=B._scan_name(A,i)
			elif E in B._decl_otherchars:A=A+1
			elif E=='[':
				if D==F:A=B._parse_doctype_subset(A+1,i)
				elif D in{_C,'linktype','link',_D}:raise AssertionError("unsupported '[' char in %s declaration"%D)
				else:raise AssertionError("unexpected '[' char in declaration")
			else:raise AssertionError('unexpected %r char in declaration'%C[A])
			if A<0:return A
		return-1
	def parse_marked_section(D,i,report=1):
		A=D.rawdata;assert A[i:i+3]=='<![','unexpected call to parse_marked_section()';E,B=D._scan_name(i+3,i)
		if B<0:return B
		if E in{'temp','cdata','ignore','include','rcdata'}:C=_markedsectionclose.search(A,i+3)
		elif E in{'if','else','endif'}:C=_msmarkedsectionclose.search(A,i+3)
		else:raise AssertionError('unknown status keyword %r in marked section'%A[i+3:B])
		if not C:return-1
		if report:B=C.start(0);D.unknown_decl(A[i+3:B])
		return C.end(0)
	def parse_comment(C,i,report=1):
		A=C.rawdata
		if A[i:i+4]!='<!--':raise AssertionError('unexpected call to parse_comment()')
		B=_commentclose.search(A,i+4)
		if not B:return-1
		if report:D=B.start(0);C.handle_comment(A[i+4:D])
		return B.end(0)
	def _parse_doctype_subset(B,i,declstartpos):
		C=declstartpos;D=B.rawdata;E=len(D);A=i
		while A<E:
			F=D[A]
			if F=='<':
				G=D[A:A+2]
				if G=='<':return-1
				if G!='<!':B.updatepos(C,A+1);raise AssertionError('unexpected char in internal subset (in %r)'%G)
				if A+2==E:return-1
				if A+4>E:return-1
				if D[A:A+4]=='<!--':
					A=B.parse_comment(A,report=0)
					if A<0:return A
					continue
				H,A=B._scan_name(A+2,C)
				if A==-1:return-1
				if H not in{_C,_D,'entity','notation'}:B.updatepos(C,A+2);raise AssertionError('unknown declaration %r in internal subset'%H)
				I=getattr(B,'_parse_doctype_'+H);A=I(A,C)
				if A<0:return A
			elif F=='%':
				if A+1==E:return-1
				G,A=B._scan_name(A+1,C)
				if A<0:return A
				if D[A]==';':A=A+1
			elif F==']':
				A=A+1
				while A<E and D[A].isspace():A=A+1
				if A<E:
					if D[A]==_A:return A
					B.updatepos(C,A);raise AssertionError('unexpected char after internal subset')
				else:return-1
			elif F.isspace():A=A+1
			else:B.updatepos(C,A);raise AssertionError('unexpected char %r in internal subset'%F)
		return-1
	def _parse_doctype_element(B,i,declstartpos):
		D,A=B._scan_name(i,declstartpos)
		if A==-1:return-1
		C=B.rawdata
		if _A in C[A:]:return C.find(_A,A)+1
		return-1
	def _parse_doctype_attlist(D,i,declstartpos):
		E=declstartpos;C=D.rawdata;F,A=D._scan_name(i,E);B=C[A:A+1]
		if B=='':return-1
		if B==_A:return A+1
		while 1:
			F,A=D._scan_name(A,E)
			if A<0:return A
			B=C[A:A+1]
			if B=='':return-1
			if B=='(':
				if')'in C[A:]:A=C.find(')',A)+1
				else:return-1
				while C[A:A+1].isspace():A=A+1
				if not C[A:]:return-1
			else:F,A=D._scan_name(A,E)
			B=C[A:A+1]
			if not B:return-1
			if B in _B:
				G=_declstringlit_match(C,A)
				if G:A=G.end()
				else:return-1
				B=C[A:A+1]
				if not B:return-1
			if B=='#':
				if C[A:]=='#':return-1
				F,A=D._scan_name(A+1,E)
				if A<0:return A
				B=C[A:A+1]
				if not B:return-1
			if B==_A:return A+1
	def _parse_doctype_notation(B,i,declstartpos):
		D=declstartpos;G,A=B._scan_name(i,D)
		if A<0:return A
		E=B.rawdata
		while 1:
			C=E[A:A+1]
			if not C:return-1
			if C==_A:return A+1
			if C in _B:
				F=_declstringlit_match(E,A)
				if not F:return-1
				A=F.end()
			else:
				G,A=B._scan_name(A,D)
				if A<0:return A
	def _parse_doctype_entity(C,i,declstartpos):
		E=declstartpos;D=C.rawdata
		if D[i:i+1]=='%':
			A=i+1
			while 1:
				B=D[A:A+1]
				if not B:return-1
				if B.isspace():A=A+1
				else:break
		else:A=i
		G,A=C._scan_name(A,E)
		if A<0:return A
		while 1:
			B=C.rawdata[A:A+1]
			if not B:return-1
			if B in _B:
				F=_declstringlit_match(D,A)
				if F:A=F.end()
				else:return-1
			elif B==_A:return A+1
			else:
				G,A=C._scan_name(A,E)
				if A<0:return A
	def _scan_name(D,i,declstartpos):
		A=declstartpos;B=D.rawdata;E=len(B)
		if i==E:return None,-1
		C=_declname_match(B,i)
		if C:
			F=C.group();G=F.strip()
			if i+len(F)==E:return None,-1
			return G.lower(),C.end()
		else:D.updatepos(A,i);raise AssertionError('expected name token at %r'%B[A:A+20])
	def unknown_decl(A,data):0