'Internal support module for sre'
_Q='undefined character name %r'
_P='character name'
_O='missing {'
_N='unknown group name %r'
_M='octal escape value %s outside of range 0-0o377'
_L='cannot refer to an open group'
_K='bad character in group name %r'
_J='group name'
_I='invalid group reference %d'
_H='bad escape %s'
_G=False
_F='incomplete escape %s'
_E='\\'
_D='-'
_C=')'
_B=True
_A=None
from sre_constants import*
SPECIAL_CHARS='.\\[{()*+?^$|'
REPEAT_CHARS='*+?{'
DIGITS=frozenset('0123456789')
OCTDIGITS=frozenset('01234567')
HEXDIGITS=frozenset('0123456789abcdefABCDEF')
ASCIILETTERS=frozenset('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
WHITESPACE=frozenset(' \t\n\r\x0b\x0c')
_REPEATCODES=frozenset({MIN_REPEAT,MAX_REPEAT})
_UNITCODES=frozenset({ANY,RANGE,IN,LITERAL,NOT_LITERAL,CATEGORY})
ESCAPES={'\\a':(LITERAL,ord('\x07')),'\\b':(LITERAL,ord('\x08')),'\\f':(LITERAL,ord('\x0c')),'\\n':(LITERAL,ord('\n')),'\\r':(LITERAL,ord('\r')),'\\t':(LITERAL,ord('\t')),'\\v':(LITERAL,ord('\x0b')),'\\\\':(LITERAL,ord(_E))}
CATEGORIES={'\\A':(AT,AT_BEGINNING_STRING),'\\b':(AT,AT_BOUNDARY),'\\B':(AT,AT_NON_BOUNDARY),'\\d':(IN,[(CATEGORY,CATEGORY_DIGIT)]),'\\D':(IN,[(CATEGORY,CATEGORY_NOT_DIGIT)]),'\\s':(IN,[(CATEGORY,CATEGORY_SPACE)]),'\\S':(IN,[(CATEGORY,CATEGORY_NOT_SPACE)]),'\\w':(IN,[(CATEGORY,CATEGORY_WORD)]),'\\W':(IN,[(CATEGORY,CATEGORY_NOT_WORD)]),'\\Z':(AT,AT_END_STRING)}
FLAGS={'i':SRE_FLAG_IGNORECASE,'L':SRE_FLAG_LOCALE,'m':SRE_FLAG_MULTILINE,'s':SRE_FLAG_DOTALL,'x':SRE_FLAG_VERBOSE,'a':SRE_FLAG_ASCII,'t':SRE_FLAG_TEMPLATE,'u':SRE_FLAG_UNICODE}
TYPE_FLAGS=SRE_FLAG_ASCII|SRE_FLAG_LOCALE|SRE_FLAG_UNICODE
GLOBAL_FLAGS=SRE_FLAG_DEBUG|SRE_FLAG_TEMPLATE
class Verbose(Exception):0
class State:
	def __init__(self):self.flags=0;self.groupdict={};self.groupwidths=[_A];self.lookbehindgroups=_A
	@property
	def groups(self):return len(self.groupwidths)
	def opengroup(self,name=_A):
		gid=self.groups;self.groupwidths.append(_A)
		if self.groups>MAXGROUPS:raise error('too many groups')
		if name is not _A:
			ogid=self.groupdict.get(name,_A)
			if ogid is not _A:raise error('redefinition of group name %r as group %d; was group %d'%(name,gid,ogid))
			self.groupdict[name]=gid
		return gid
	def closegroup(self,gid,p):self.groupwidths[gid]=p.getwidth()
	def checkgroup(self,gid):return gid<self.groups and self.groupwidths[gid]is not _A
	def checklookbehindgroup(self,gid,source):
		if self.lookbehindgroups is not _A:
			if not self.checkgroup(gid):raise source.error(_L)
			if gid>=self.lookbehindgroups:raise source.error('cannot refer to group defined in the same lookbehind subpattern')
class SubPattern:
	def __init__(self,state,data=_A):
		self.state=state
		if data is _A:data=[]
		self.data=data;self.width=_A
	def dump(self,level=0):
		A='  ';nl=_B;seqtypes=tuple,list
		for(op,av)in self.data:
			print(level*A+str(op),end='')
			if op is IN:
				print()
				for(op,a)in av:print((level+1)*A+str(op),a)
			elif op is BRANCH:
				print()
				for(i,a)in enumerate(av[1]):
					if i:print(level*A+'OR')
					a.dump(level+1)
			elif op is GROUPREF_EXISTS:
				condgroup,item_yes,item_no=av;print('',condgroup);item_yes.dump(level+1)
				if item_no:print(level*A+'ELSE');item_no.dump(level+1)
			elif isinstance(av,seqtypes):
				nl=_G
				for a in av:
					if isinstance(a,SubPattern):
						if not nl:print()
						a.dump(level+1);nl=_B
					else:
						if not nl:print(' ',end='')
						print(a,end='');nl=_G
				if not nl:print()
			else:print('',av)
	def __repr__(self):return repr(self.data)
	def __len__(self):return len(self.data)
	def __delitem__(self,index):del self.data[index]
	def __getitem__(self,index):
		if isinstance(index,slice):return SubPattern(self.state,self.data[index])
		return self.data[index]
	def __setitem__(self,index,code):self.data[index]=code
	def insert(self,index,code):self.data.insert(index,code)
	def append(self,code):self.data.append(code)
	def getwidth(self):
		if self.width is not _A:return self.width
		lo=hi=0
		for(op,av)in self.data:
			if op is BRANCH:
				i=MAXREPEAT-1;j=0
				for av in av[1]:l,h=av.getwidth();i=min(i,l);j=max(j,h)
				lo=lo+i;hi=hi+j
			elif op is CALL:i,j=av.getwidth();lo=lo+i;hi=hi+j
			elif op is SUBPATTERN:i,j=av[-1].getwidth();lo=lo+i;hi=hi+j
			elif op in _REPEATCODES:i,j=av[2].getwidth();lo=lo+i*av[0];hi=hi+j*av[1]
			elif op in _UNITCODES:lo=lo+1;hi=hi+1
			elif op is GROUPREF:i,j=self.state.groupwidths[av];lo=lo+i;hi=hi+j
			elif op is GROUPREF_EXISTS:
				i,j=av[1].getwidth()
				if av[2]is not _A:l,h=av[2].getwidth();i=min(i,l);j=max(j,h)
				else:i=0
				lo=lo+i;hi=hi+j
			elif op is SUCCESS:break
		self.width=min(lo,MAXREPEAT-1),min(hi,MAXREPEAT);return self.width
class Tokenizer:
	def __init__(self,string):
		self.istext=isinstance(string,str);self.string=string
		if not self.istext:string=str(string,'latin1')
		self.decoded_string=string;self.index=0;self.next=_A;self.__next()
	def __next(self):
		index=self.index
		try:char=self.decoded_string[index]
		except IndexError:self.next=_A;return
		if char==_E:
			index+=1
			try:char+=self.decoded_string[index]
			except IndexError:raise error('bad escape (end of pattern)',self.string,len(self.string)-1)from _A
		self.index=index+1;self.next=char
	def match(self,char):
		if char==self.next:self.__next();return _B
		return _G
	def get(self):this=self.next;self.__next();return this
	def getwhile(self,n,charset):
		result=''
		for _ in range(n):
			c=self.next
			if c not in charset:break
			result+=c;self.__next()
		return result
	def getuntil(self,terminator,name):
		A='missing ';result=''
		while _B:
			c=self.next;self.__next()
			if c is _A:
				if not result:raise self.error(A+name)
				raise self.error('missing %s, unterminated name'%terminator,len(result))
			if c==terminator:
				if not result:raise self.error(A+name,1)
				break
			result+=c
		return result
	@property
	def pos(self):return self.index-len(self.next or'')
	def tell(self):return self.index-len(self.next or'')
	def seek(self,index):self.index=index;self.__next()
	def error(self,msg,offset=0):return error(msg,self.string,self.tell()-offset)
def _class_escape(source,escape):
	code=ESCAPES.get(escape)
	if code:return code
	code=CATEGORIES.get(escape)
	if code and code[0]is IN:return code
	try:
		c=escape[1:2]
		if c=='x':
			escape+=source.getwhile(2,HEXDIGITS)
			if len(escape)!=4:raise source.error(_F%escape,len(escape))
			return LITERAL,int(escape[2:],16)
		elif c=='u'and source.istext:
			escape+=source.getwhile(4,HEXDIGITS)
			if len(escape)!=6:raise source.error(_F%escape,len(escape))
			return LITERAL,int(escape[2:],16)
		elif c=='U'and source.istext:
			escape+=source.getwhile(8,HEXDIGITS)
			if len(escape)!=10:raise source.error(_F%escape,len(escape))
			c=int(escape[2:],16);chr(c);return LITERAL,c
		elif c=='N'and source.istext:
			import unicodedata
			if not source.match('{'):raise source.error(_O)
			charname=source.getuntil('}',_P)
			try:c=ord(unicodedata.lookup(charname))
			except KeyError:raise source.error(_Q%charname,len(charname)+len('\\N{}'))
			return LITERAL,c
		elif c in OCTDIGITS:
			escape+=source.getwhile(2,OCTDIGITS);c=int(escape[1:],8)
			if c>255:raise source.error(_M%escape,len(escape))
			return LITERAL,c
		elif c in DIGITS:raise ValueError
		if len(escape)==2:
			if c in ASCIILETTERS:raise source.error(_H%escape,len(escape))
			return LITERAL,ord(escape[1])
	except ValueError:pass
	raise source.error(_H%escape,len(escape))
def _escape(source,escape,state):
	code=CATEGORIES.get(escape)
	if code:return code
	code=ESCAPES.get(escape)
	if code:return code
	try:
		c=escape[1:2]
		if c=='x':
			escape+=source.getwhile(2,HEXDIGITS)
			if len(escape)!=4:raise source.error(_F%escape,len(escape))
			return LITERAL,int(escape[2:],16)
		elif c=='u'and source.istext:
			escape+=source.getwhile(4,HEXDIGITS)
			if len(escape)!=6:raise source.error(_F%escape,len(escape))
			return LITERAL,int(escape[2:],16)
		elif c=='U'and source.istext:
			escape+=source.getwhile(8,HEXDIGITS)
			if len(escape)!=10:raise source.error(_F%escape,len(escape))
			c=int(escape[2:],16);chr(c);return LITERAL,c
		elif c=='N'and source.istext:
			import unicodedata
			if not source.match('{'):raise source.error(_O)
			charname=source.getuntil('}',_P)
			try:c=ord(unicodedata.lookup(charname))
			except KeyError:raise source.error(_Q%charname,len(charname)+len('\\N{}'))
			return LITERAL,c
		elif c=='0':escape+=source.getwhile(2,OCTDIGITS);return LITERAL,int(escape[1:],8)
		elif c in DIGITS:
			if source.next in DIGITS:
				escape+=source.get()
				if escape[1]in OCTDIGITS and escape[2]in OCTDIGITS and source.next in OCTDIGITS:
					escape+=source.get();c=int(escape[1:],8)
					if c>255:raise source.error(_M%escape,len(escape))
					return LITERAL,c
			group=int(escape[1:])
			if group<state.groups:
				if not state.checkgroup(group):raise source.error(_L,len(escape))
				state.checklookbehindgroup(group,source);return GROUPREF,group
			raise source.error(_I%group,len(escape)-1)
		if len(escape)==2:
			if c in ASCIILETTERS:raise source.error(_H%escape,len(escape))
			return LITERAL,ord(escape[1])
	except ValueError:pass
	raise source.error(_H%escape,len(escape))
def _uniq(items):return list(dict.fromkeys(items))
def _parse_sub(source,state,verbose,nested):
	items=[];itemsappend=items.append;sourcematch=source.match;start=source.tell()
	while _B:
		itemsappend(_parse(source,state,verbose,nested+1,not nested and not items))
		if not sourcematch('|'):break
	if len(items)==1:return items[0]
	subpattern=SubPattern(state)
	while _B:
		prefix=_A
		for item in items:
			if not item:break
			if prefix is _A:prefix=item[0]
			elif item[0]!=prefix:break
		else:
			for item in items:del item[0]
			subpattern.append(prefix);continue
		break
	set=[]
	for item in items:
		if len(item)!=1:break
		op,av=item[0]
		if op is LITERAL:set.append((op,av))
		elif op is IN and av[0][0]is not NEGATE:set.extend(av)
		else:break
	else:subpattern.append((IN,_uniq(set)));return subpattern
	subpattern.append((BRANCH,(_A,items)));return subpattern
def _parse(source,state,verbose,nested,first=_G):
	F='the repetition number is too large';E='bad character range %s-%s';D='unterminated character set';C='missing ), unterminated subpattern';B='unexpected end of pattern';A='?';subpattern=SubPattern(state);subpatternappend=subpattern.append;sourceget=source.get;sourcematch=source.match;_len=len;_ord=ord
	while _B:
		this=source.next
		if this is _A:break
		if this in'|)':break
		sourceget()
		if verbose:
			if this in WHITESPACE:continue
			if this=='#':
				while _B:
					this=sourceget()
					if this is _A or this=='\n':break
				continue
		if this[0]==_E:code=_escape(source,this,state);subpatternappend(code)
		elif this not in SPECIAL_CHARS:subpatternappend((LITERAL,_ord(this)))
		elif this=='[':
			here=source.tell()-1;set=[];setappend=set.append
			if source.next=='[':import warnings;warnings.warn('Possible nested set at position %d'%source.tell(),FutureWarning,stacklevel=nested+6)
			negate=sourcematch('^')
			while _B:
				this=sourceget()
				if this is _A:raise source.error(D,source.tell()-here)
				if this==']'and set:break
				elif this[0]==_E:code1=_class_escape(source,this)
				else:
					if set and this in'-&~|'and source.next==this:import warnings;warnings.warn('Possible set %s at position %d'%('difference'if this==_D else'intersection'if this=='&'else'symmetric difference'if this=='~'else'union',source.tell()-1),FutureWarning,stacklevel=nested+6)
					code1=LITERAL,_ord(this)
				if sourcematch(_D):
					that=sourceget()
					if that is _A:raise source.error(D,source.tell()-here)
					if that==']':
						if code1[0]is IN:code1=code1[1][0]
						setappend(code1);setappend((LITERAL,_ord(_D)));break
					if that[0]==_E:code2=_class_escape(source,that)
					else:
						if that==_D:import warnings;warnings.warn('Possible set difference at position %d'%(source.tell()-2),FutureWarning,stacklevel=nested+6)
						code2=LITERAL,_ord(that)
					if code1[0]!=LITERAL or code2[0]!=LITERAL:msg=E%(this,that);raise source.error(msg,len(this)+1+len(that))
					lo=code1[1];hi=code2[1]
					if hi<lo:msg=E%(this,that);raise source.error(msg,len(this)+1+len(that))
					setappend((RANGE,(lo,hi)))
				else:
					if code1[0]is IN:code1=code1[1][0]
					setappend(code1)
			set=_uniq(set)
			if _len(set)==1 and set[0][0]is LITERAL:
				if negate:subpatternappend((NOT_LITERAL,set[0][1]))
				else:subpatternappend(set[0])
			else:
				if negate:set.insert(0,(NEGATE,_A))
				subpatternappend((IN,set))
		elif this in REPEAT_CHARS:
			here=source.tell()
			if this==A:min,max=0,1
			elif this=='*':min,max=0,MAXREPEAT
			elif this=='+':min,max=1,MAXREPEAT
			elif this=='{':
				if source.next=='}':subpatternappend((LITERAL,_ord(this)));continue
				min,max=0,MAXREPEAT;lo=hi=''
				while source.next in DIGITS:lo+=sourceget()
				if sourcematch(','):
					while source.next in DIGITS:hi+=sourceget()
				else:hi=lo
				if not sourcematch('}'):subpatternappend((LITERAL,_ord(this)));source.seek(here);continue
				if lo:
					min=int(lo)
					if min>=MAXREPEAT:raise OverflowError(F)
				if hi:
					max=int(hi)
					if max>=MAXREPEAT:raise OverflowError(F)
					if max<min:raise source.error('min repeat greater than max repeat',source.tell()-here)
			else:raise AssertionError('unsupported quantifier %r'%(char,))
			if subpattern:item=subpattern[-1:]
			else:item=_A
			if not item or item[0][0]is AT:raise source.error('nothing to repeat',source.tell()-here+len(this))
			if item[0][0]in _REPEATCODES:raise source.error('multiple repeat',source.tell()-here+len(this))
			if item[0][0]is SUBPATTERN:
				group,add_flags,del_flags,p=item[0][1]
				if group is _A and not add_flags and not del_flags:item=p
			if sourcematch(A):subpattern[-1]=MIN_REPEAT,(min,max,item)
			else:subpattern[-1]=MAX_REPEAT,(min,max,item)
		elif this=='.':subpatternappend((ANY,_A))
		elif this=='(':
			start=source.tell()-1;group=_B;name=_A;add_flags=0;del_flags=0
			if sourcematch(A):
				char=sourceget()
				if char is _A:raise source.error(B)
				if char=='P':
					if sourcematch('<'):
						name=source.getuntil('>',_J)
						if not name.isidentifier():msg=_K%name;raise source.error(msg,len(name)+1)
					elif sourcematch('='):
						name=source.getuntil(_C,_J)
						if not name.isidentifier():msg=_K%name;raise source.error(msg,len(name)+1)
						gid=state.groupdict.get(name)
						if gid is _A:msg=_N%name;raise source.error(msg,len(name)+1)
						if not state.checkgroup(gid):raise source.error(_L,len(name)+1)
						state.checklookbehindgroup(gid,source);subpatternappend((GROUPREF,gid));continue
					else:
						char=sourceget()
						if char is _A:raise source.error(B)
						raise source.error('unknown extension ?P'+char,len(char)+2)
				elif char==':':group=_A
				elif char=='#':
					while _B:
						if source.next is _A:raise source.error('missing ), unterminated comment',source.tell()-start)
						if sourceget()==_C:break
					continue
				elif char in'=!<':
					dir=1
					if char=='<':
						char=sourceget()
						if char is _A:raise source.error(B)
						if char not in'=!':raise source.error('unknown extension ?<'+char,len(char)+2)
						dir=-1;lookbehindgroups=state.lookbehindgroups
						if lookbehindgroups is _A:state.lookbehindgroups=state.groups
					p=_parse_sub(source,state,verbose,nested+1)
					if dir<0:
						if lookbehindgroups is _A:state.lookbehindgroups=_A
					if not sourcematch(_C):raise source.error(C,source.tell()-start)
					if char=='=':subpatternappend((ASSERT,(dir,p)))
					else:subpatternappend((ASSERT_NOT,(dir,p)))
					continue
				elif char=='(':
					condname=source.getuntil(_C,_J)
					if condname.isidentifier():
						condgroup=state.groupdict.get(condname)
						if condgroup is _A:msg=_N%condname;raise source.error(msg,len(condname)+1)
					else:
						try:
							condgroup=int(condname)
							if condgroup<0:raise ValueError
						except ValueError:msg=_K%condname;raise source.error(msg,len(condname)+1)from _A
						if not condgroup:raise source.error('bad group number',len(condname)+1)
						if condgroup>=MAXGROUPS:msg=_I%condgroup;raise source.error(msg,len(condname)+1)
					state.checklookbehindgroup(condgroup,source);item_yes=_parse(source,state,verbose,nested+1)
					if source.match('|'):
						item_no=_parse(source,state,verbose,nested+1)
						if source.next=='|':raise source.error('conditional backref with more than two branches')
					else:item_no=_A
					if not source.match(_C):raise source.error(C,source.tell()-start)
					subpatternappend((GROUPREF_EXISTS,(condgroup,item_yes,item_no)));continue
				elif char in FLAGS or char==_D:
					flags=_parse_flags(source,state,char)
					if flags is _A:
						if not first or subpattern:import warnings;warnings.warn('Flags not at the start of the expression %r%s'%(source.string[:20],' (truncated)'if len(source.string)>20 else''),DeprecationWarning,stacklevel=nested+6)
						if state.flags&SRE_FLAG_VERBOSE and not verbose:raise Verbose
						continue
					add_flags,del_flags=flags;group=_A
				else:raise source.error('unknown extension ?'+char,len(char)+1)
			if group is not _A:
				try:group=state.opengroup(name)
				except error as err:raise source.error(err.msg,len(name)+1)from _A
			sub_verbose=(verbose or add_flags&SRE_FLAG_VERBOSE)and not del_flags&SRE_FLAG_VERBOSE;p=_parse_sub(source,state,sub_verbose,nested+1)
			if not source.match(_C):raise source.error(C,source.tell()-start)
			if group is not _A:state.closegroup(group,p)
			subpatternappend((SUBPATTERN,(group,add_flags,del_flags,p)))
		elif this=='^':subpatternappend((AT,AT_BEGINNING))
		elif this=='$':subpatternappend((AT,AT_END))
		else:raise AssertionError('unsupported special character %r'%(char,))
	for i in range(len(subpattern))[::-1]:
		op,av=subpattern[i]
		if op is SUBPATTERN:
			group,add_flags,del_flags,p=av
			if group is _A and not add_flags and not del_flags:subpattern[i:i+1]=p
	return subpattern
def _parse_flags(source,state,char):
	D='missing :';C='missing flag';B='missing -, : or )';A='unknown flag';sourceget=source.get;add_flags=0;del_flags=0
	if char!=_D:
		while _B:
			flag=FLAGS[char]
			if source.istext:
				if char=='L':msg="bad inline flags: cannot use 'L' flag with a str pattern";raise source.error(msg)
			elif char=='u':msg="bad inline flags: cannot use 'u' flag with a bytes pattern";raise source.error(msg)
			add_flags|=flag
			if flag&TYPE_FLAGS and add_flags&TYPE_FLAGS!=flag:msg="bad inline flags: flags 'a', 'u' and 'L' are incompatible";raise source.error(msg)
			char=sourceget()
			if char is _A:raise source.error(B)
			if char in')-:':break
			if char not in FLAGS:msg=A if char.isalpha()else B;raise source.error(msg,len(char))
	if char==_C:state.flags|=add_flags;return
	if add_flags&GLOBAL_FLAGS:raise source.error('bad inline flags: cannot turn on global flag',1)
	if char==_D:
		char=sourceget()
		if char is _A:raise source.error(C)
		if char not in FLAGS:msg=A if char.isalpha()else C;raise source.error(msg,len(char))
		while _B:
			flag=FLAGS[char]
			if flag&TYPE_FLAGS:msg="bad inline flags: cannot turn off flags 'a', 'u' and 'L'";raise source.error(msg)
			del_flags|=flag;char=sourceget()
			if char is _A:raise source.error(D)
			if char==':':break
			if char not in FLAGS:msg=A if char.isalpha()else D;raise source.error(msg,len(char))
	assert char==':'
	if del_flags&GLOBAL_FLAGS:raise source.error('bad inline flags: cannot turn off global flag',1)
	if add_flags&del_flags:raise source.error('bad inline flags: flag turned on and off',1)
	return add_flags,del_flags
def fix_flags(src,flags):
	if isinstance(src,str):
		if flags&SRE_FLAG_LOCALE:raise ValueError('cannot use LOCALE flag with a str pattern')
		if not flags&SRE_FLAG_ASCII:flags|=SRE_FLAG_UNICODE
		elif flags&SRE_FLAG_UNICODE:raise ValueError('ASCII and UNICODE flags are incompatible')
	else:
		if flags&SRE_FLAG_UNICODE:raise ValueError('cannot use UNICODE flag with a bytes pattern')
		if flags&SRE_FLAG_LOCALE and flags&SRE_FLAG_ASCII:raise ValueError('ASCII and LOCALE flags are incompatible')
	return flags
def parse(str,flags=0,state=_A):
	source=Tokenizer(str)
	if state is _A:state=State()
	state.flags=flags;state.str=str
	try:p=_parse_sub(source,state,flags&SRE_FLAG_VERBOSE,0)
	except Verbose:state=State();state.flags=flags|SRE_FLAG_VERBOSE;state.str=str;source.seek(0);p=_parse_sub(source,state,_B,0)
	p.state.flags=fix_flags(str,p.state.flags)
	if source.next is not _A:assert source.next==_C;raise source.error('unbalanced parenthesis')
	if flags&SRE_FLAG_DEBUG:p.dump()
	return p
def parse_template(source,state):
	s=Tokenizer(source);sget=s.get;groups=[];literals=[];literal=[];lappend=literal.append
	def addgroup(index,pos):
		if index>state.groups:raise s.error(_I%index,pos)
		if literal:literals.append(''.join(literal));del literal[:]
		groups.append((len(literals),index));literals.append(_A)
	groupindex=state.groupindex
	while _B:
		this=sget()
		if this is _A:break
		if this[0]==_E:
			c=this[1]
			if c=='g':
				name=''
				if not s.match('<'):raise s.error('missing <')
				name=s.getuntil('>',_J)
				if name.isidentifier():
					try:index=groupindex[name]
					except KeyError:raise IndexError(_N%name)
				else:
					try:
						index=int(name)
						if index<0:raise ValueError
					except ValueError:raise s.error(_K%name,len(name)+1)from _A
					if index>=MAXGROUPS:raise s.error(_I%index,len(name)+1)
				addgroup(index,len(name)+1)
			elif c=='0':
				if s.next in OCTDIGITS:
					this+=sget()
					if s.next in OCTDIGITS:this+=sget()
				lappend(chr(int(this[1:],8)&255))
			elif c in DIGITS:
				isoctal=_G
				if s.next in DIGITS:
					this+=sget()
					if c in OCTDIGITS and this[2]in OCTDIGITS and s.next in OCTDIGITS:
						this+=sget();isoctal=_B;c=int(this[1:],8)
						if c>255:raise s.error(_M%this,len(this))
						lappend(chr(c))
				if not isoctal:addgroup(int(this[1:]),len(this)-1)
			else:
				try:this=chr(ESCAPES[this][1])
				except KeyError:
					if c in ASCIILETTERS:raise s.error(_H%this,len(this))
				lappend(this)
		else:lappend(this)
	if literal:literals.append(''.join(literal))
	if not isinstance(source,str):literals=[_A if s is _A else s.encode('latin-1')for s in literals]
	return groups,literals
def expand_template(template,match):
	g=match.group;empty=match.string[:0];groups,literals=template;literals=literals[:]
	try:
		for(index,group)in groups:literals[index]=g(group)or empty
	except IndexError:raise error(_I%index)
	return empty.join(literals)