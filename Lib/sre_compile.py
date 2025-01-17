'Internal support module for sre'
_C=False
_B=True
_A=None
import _sre,sre_parse
from sre_constants import*
assert _sre.MAGIC==MAGIC,'SRE module mismatch'
_LITERAL_CODES={LITERAL,NOT_LITERAL}
_REPEATING_CODES={REPEAT,MIN_REPEAT,MAX_REPEAT}
_SUCCESS_CODES={SUCCESS,FAILURE}
_ASSERT_CODES={ASSERT,ASSERT_NOT}
_UNIT_CODES=_LITERAL_CODES|{ANY,IN}
_equivalences=(105,305),(115,383),(181,956),(837,953,8126),(912,8147),(944,8163),(946,976),(949,1013),(952,977),(954,1008),(960,982),(961,1009),(962,963),(966,981),(7777,7835),(64261,64262)
_ignorecase_fixes={i:tuple(j for j in t if i!=j)for t in _equivalences for i in t}
def _combine_flags(flags,add_flags,del_flags,TYPE_FLAGS=sre_parse.TYPE_FLAGS):
	if add_flags&TYPE_FLAGS:flags&=~TYPE_FLAGS
	return(flags|add_flags)&~del_flags
def _compile(code,pattern,flags):
	emit=code.append;_len=len;LITERAL_CODES=_LITERAL_CODES;REPEATING_CODES=_REPEATING_CODES;SUCCESS_CODES=_SUCCESS_CODES;ASSERT_CODES=_ASSERT_CODES;iscased=_A;tolower=_A;fixes=_A
	if flags&SRE_FLAG_IGNORECASE and not flags&SRE_FLAG_LOCALE:
		if flags&SRE_FLAG_UNICODE:iscased=_sre.unicode_iscased;tolower=_sre.unicode_tolower;fixes=_ignorecase_fixes
		else:iscased=_sre.ascii_iscased;tolower=_sre.ascii_tolower
	for(op,av)in pattern:
		if op in LITERAL_CODES:
			if not flags&SRE_FLAG_IGNORECASE:emit(op);emit(av)
			elif flags&SRE_FLAG_LOCALE:emit(OP_LOCALE_IGNORE[op]);emit(av)
			elif not iscased(av):emit(op);emit(av)
			else:
				lo=tolower(av)
				if not fixes:emit(OP_IGNORE[op]);emit(lo)
				elif lo not in fixes:emit(OP_UNICODE_IGNORE[op]);emit(lo)
				else:
					emit(IN_UNI_IGNORE);skip=_len(code);emit(0)
					if op is NOT_LITERAL:emit(NEGATE)
					for k in(lo,)+fixes[lo]:emit(LITERAL);emit(k)
					emit(FAILURE);code[skip]=_len(code)-skip
		elif op is IN:
			charset,hascased=_optimize_charset(av,iscased,tolower,fixes)
			if flags&SRE_FLAG_IGNORECASE and flags&SRE_FLAG_LOCALE:emit(IN_LOC_IGNORE)
			elif not hascased:emit(IN)
			elif not fixes:emit(IN_IGNORE)
			else:emit(IN_UNI_IGNORE)
			skip=_len(code);emit(0);_compile_charset(charset,flags,code);code[skip]=_len(code)-skip
		elif op is ANY:
			if flags&SRE_FLAG_DOTALL:emit(ANY_ALL)
			else:emit(ANY)
		elif op in REPEATING_CODES:
			if flags&SRE_FLAG_TEMPLATE:raise error('internal: unsupported template operator %r'%(op,))
			if _simple(av[2]):
				if op is MAX_REPEAT:emit(REPEAT_ONE)
				else:emit(MIN_REPEAT_ONE)
				skip=_len(code);emit(0);emit(av[0]);emit(av[1]);_compile(code,av[2],flags);emit(SUCCESS);code[skip]=_len(code)-skip
			else:
				emit(REPEAT);skip=_len(code);emit(0);emit(av[0]);emit(av[1]);_compile(code,av[2],flags);code[skip]=_len(code)-skip
				if op is MAX_REPEAT:emit(MAX_UNTIL)
				else:emit(MIN_UNTIL)
		elif op is SUBPATTERN:
			group,add_flags,del_flags,p=av
			if group:emit(MARK);emit((group-1)*2)
			_compile(code,p,_combine_flags(flags,add_flags,del_flags))
			if group:emit(MARK);emit((group-1)*2+1)
		elif op in SUCCESS_CODES:emit(op)
		elif op in ASSERT_CODES:
			emit(op);skip=_len(code);emit(0)
			if av[0]>=0:emit(0)
			else:
				lo,hi=av[1].getwidth()
				if lo!=hi:raise error('look-behind requires fixed-width pattern')
				emit(lo)
			_compile(code,av[1],flags);emit(SUCCESS);code[skip]=_len(code)-skip
		elif op is CALL:emit(op);skip=_len(code);emit(0);_compile(code,av,flags);emit(SUCCESS);code[skip]=_len(code)-skip
		elif op is AT:
			emit(op)
			if flags&SRE_FLAG_MULTILINE:av=AT_MULTILINE.get(av,av)
			if flags&SRE_FLAG_LOCALE:av=AT_LOCALE.get(av,av)
			elif flags&SRE_FLAG_UNICODE:av=AT_UNICODE.get(av,av)
			emit(av)
		elif op is BRANCH:
			emit(op);tail=[];tailappend=tail.append
			for av in av[1]:skip=_len(code);emit(0);_compile(code,av,flags);emit(JUMP);tailappend(_len(code));emit(0);code[skip]=_len(code)-skip
			emit(FAILURE)
			for tail in tail:code[tail]=_len(code)-tail
		elif op is CATEGORY:
			emit(op)
			if flags&SRE_FLAG_LOCALE:av=CH_LOCALE[av]
			elif flags&SRE_FLAG_UNICODE:av=CH_UNICODE[av]
			emit(av)
		elif op is GROUPREF:
			if not flags&SRE_FLAG_IGNORECASE:emit(op)
			elif flags&SRE_FLAG_LOCALE:emit(GROUPREF_LOC_IGNORE)
			elif not fixes:emit(GROUPREF_IGNORE)
			else:emit(GROUPREF_UNI_IGNORE)
			emit(av-1)
		elif op is GROUPREF_EXISTS:
			emit(op);emit(av[0]-1);skipyes=_len(code);emit(0);_compile(code,av[1],flags)
			if av[2]:emit(JUMP);skipno=_len(code);emit(0);code[skipyes]=_len(code)-skipyes+1;_compile(code,av[2],flags);code[skipno]=_len(code)-skipno
			else:code[skipyes]=_len(code)-skipyes+1
		else:raise error('internal: unsupported operand type %r'%(op,))
def _compile_charset(charset,flags,code):
	emit=code.append
	for(op,av)in charset:
		emit(op)
		if op is NEGATE:0
		elif op is LITERAL:emit(av)
		elif op is RANGE or op is RANGE_UNI_IGNORE:emit(av[0]);emit(av[1])
		elif op is CHARSET:code.extend(av)
		elif op is BIGCHARSET:code.extend(av)
		elif op is CATEGORY:
			if flags&SRE_FLAG_LOCALE:emit(CH_LOCALE[av])
			elif flags&SRE_FLAG_UNICODE:emit(CH_UNICODE[av])
			else:emit(av)
		else:raise error('internal: unsupported set operator %r'%(op,))
	emit(FAILURE)
def _optimize_charset(charset,iscased=_A,fixup=_A,fixes=_A):
	out=[];tail=[];charmap=bytearray(256);hascased=_C
	for(op,av)in charset:
		while _B:
			try:
				if op is LITERAL:
					if fixup:
						lo=fixup(av);charmap[lo]=1
						if fixes and lo in fixes:
							for k in fixes[lo]:charmap[k]=1
						if not hascased and iscased(av):hascased=_B
					else:charmap[av]=1
				elif op is RANGE:
					r=range(av[0],av[1]+1)
					if fixup:
						if fixes:
							for i in map(fixup,r):
								charmap[i]=1
								if i in fixes:
									for k in fixes[i]:charmap[k]=1
						else:
							for i in map(fixup,r):charmap[i]=1
						if not hascased:hascased=any(map(iscased,r))
					else:
						for i in r:charmap[i]=1
				elif op is NEGATE:out.append((op,av))
				else:tail.append((op,av))
			except IndexError:
				if len(charmap)==256:charmap+=b'\x00'*65280;continue
				if fixup:
					hascased=_B
					if op is RANGE:op=RANGE_UNI_IGNORE
				tail.append((op,av))
			break
	runs=[];q=0
	while _B:
		p=charmap.find(1,q)
		if p<0:break
		if len(runs)>=2:runs=_A;break
		q=charmap.find(0,p)
		if q<0:runs.append((p,len(charmap)));break
		runs.append((p,q))
	if runs is not _A:
		for(p,q)in runs:
			if q-p==1:out.append((LITERAL,p))
			else:out.append((RANGE,(p,q-1)))
		out+=tail
		if hascased or len(out)<len(charset):return out,hascased
		return charset,hascased
	if len(charmap)==256:data=_mk_bitmap(charmap);out.append((CHARSET,data));out+=tail;return out,hascased
	charmap=bytes(charmap);comps={};mapping=bytearray(256);block=0;data=bytearray()
	for i in range(0,65536,256):
		chunk=charmap[i:i+256]
		if chunk in comps:mapping[i//256]=comps[chunk]
		else:mapping[i//256]=comps[chunk]=block;block+=1;data+=chunk
	data=_mk_bitmap(data);data[0:0]=[block]+_bytes_to_codes(mapping);out.append((BIGCHARSET,data));out+=tail;return out,hascased
_CODEBITS=_sre.CODESIZE*8
MAXCODE=(1<<_CODEBITS)-1
_BITS_TRANS=b'0'+b'1'*255
def _mk_bitmap(bits,_CODEBITS=_CODEBITS,_int=int):s=bits.translate(_BITS_TRANS)[::-1];return[_int(s[i-_CODEBITS:i],2)for i in range(len(s),0,-_CODEBITS)]
def _bytes_to_codes(b):a=memoryview(b).cast('I');assert a.itemsize==_sre.CODESIZE;assert len(a)*a.itemsize==len(b);return a.tolist()
def _simple(p):
	if len(p)!=1:return _C
	op,av=p[0]
	if op is SUBPATTERN:return av[0]is _A and _simple(av[-1])
	return op in _UNIT_CODES
def _generate_overlap_table(prefix):
	"\n    Generate an overlap table for the following prefix.\n    An overlap table is a table of the same size as the prefix which\n    informs about the potential self-overlap for each index in the prefix:\n    - if overlap[i] == 0, prefix[i:] can't overlap prefix[0:...]\n    - if overlap[i] == k with 0 < k <= i, prefix[i-k+1:i+1] overlaps with\n      prefix[0:k]\n    ";table=[0]*len(prefix)
	for i in range(1,len(prefix)):
		idx=table[i-1]
		while prefix[i]!=prefix[idx]:
			if idx==0:table[i]=0;break
			idx=table[idx-1]
		else:table[i]=idx+1
	return table
def _get_iscased(flags):
	if not flags&SRE_FLAG_IGNORECASE:return
	elif flags&SRE_FLAG_UNICODE:return _sre.unicode_iscased
	else:return _sre.ascii_iscased
def _get_literal_prefix(pattern,flags):
	prefix=[];prefixappend=prefix.append;prefix_skip=_A;iscased=_get_iscased(flags)
	for(op,av)in pattern.data:
		if op is LITERAL:
			if iscased and iscased(av):break
			prefixappend(av)
		elif op is SUBPATTERN:
			group,add_flags,del_flags,p=av;flags1=_combine_flags(flags,add_flags,del_flags)
			if flags1&SRE_FLAG_IGNORECASE and flags1&SRE_FLAG_LOCALE:break
			prefix1,prefix_skip1,got_all=_get_literal_prefix(p,flags1)
			if prefix_skip is _A:
				if group is not _A:prefix_skip=len(prefix)
				elif prefix_skip1 is not _A:prefix_skip=len(prefix)+prefix_skip1
			prefix.extend(prefix1)
			if not got_all:break
		else:break
	else:return prefix,prefix_skip,_B
	return prefix,prefix_skip,_C
def _get_charset_prefix(pattern,flags):
	while _B:
		if not pattern.data:return
		op,av=pattern.data[0]
		if op is not SUBPATTERN:break
		group,add_flags,del_flags,pattern=av;flags=_combine_flags(flags,add_flags,del_flags)
		if flags&SRE_FLAG_IGNORECASE and flags&SRE_FLAG_LOCALE:return
	iscased=_get_iscased(flags)
	if op is LITERAL:
		if iscased and iscased(av):return
		return[(op,av)]
	elif op is BRANCH:
		charset=[];charsetappend=charset.append
		for p in av[1]:
			if not p:return
			op,av=p[0]
			if op is LITERAL and not(iscased and iscased(av)):charsetappend((op,av))
			else:return
		return charset
	elif op is IN:
		charset=av
		if iscased:
			for(op,av)in charset:
				if op is LITERAL:
					if iscased(av):return
				elif op is RANGE:
					if av[1]>65535:return
					if any(map(iscased,range(av[0],av[1]+1))):return
		return charset
def _compile_info(code,pattern,flags):
	lo,hi=pattern.getwidth()
	if hi>MAXCODE:hi=MAXCODE
	if lo==0:code.extend([INFO,4,0,lo,hi]);return
	prefix=[];prefix_skip=0;charset=[]
	if not(flags&SRE_FLAG_IGNORECASE and flags&SRE_FLAG_LOCALE):
		prefix,prefix_skip,got_all=_get_literal_prefix(pattern,flags)
		if not prefix:charset=_get_charset_prefix(pattern,flags)
	emit=code.append;emit(INFO);skip=len(code);emit(0);mask=0
	if prefix:
		mask=SRE_INFO_PREFIX
		if prefix_skip is _A and got_all:mask=mask|SRE_INFO_LITERAL
	elif charset:mask=mask|SRE_INFO_CHARSET
	emit(mask)
	if lo<MAXCODE:emit(lo)
	else:emit(MAXCODE);prefix=prefix[:MAXCODE]
	emit(min(hi,MAXCODE))
	if prefix:
		emit(len(prefix))
		if prefix_skip is _A:prefix_skip=len(prefix)
		emit(prefix_skip);code.extend(prefix);code.extend(_generate_overlap_table(prefix))
	elif charset:charset,hascased=_optimize_charset(charset);assert not hascased;_compile_charset(charset,flags,code)
	code[skip]=len(code)-skip
def isstring(obj):return isinstance(obj,(str,bytes))
def _code(p,flags):flags=p.state.flags|flags;code=[];_compile_info(code,p,flags);_compile(code,p.data,flags);code.append(SUCCESS);return code
def _hex_code(code):return'[%s]'%', '.join('%#0*x'%(_sre.CODESIZE*2+2,x)for x in code)
def dis(code):
	import sys;labels=set();level=0;offset_width=len(str(len(code)-1))
	def dis_(start,end):
		A='MAXREPEAT'
		def print_(*args,to=_A):
			if to is not _A:labels.add(to);args+='(to %d)'%(to,),
			print('%*d%s '%(offset_width,start,':'if start in labels else'.'),end='  '*(level-1));print(*args)
		def print_2(*args):print(end=' '*(offset_width+2*level));print(*args)
		nonlocal level;level+=1;i=start
		while i<end:
			start=i;op=code[i];i+=1;op=OPCODES[op]
			if op in(SUCCESS,FAILURE,ANY,ANY_ALL,MAX_UNTIL,MIN_UNTIL,NEGATE):print_(op)
			elif op in(LITERAL,NOT_LITERAL,LITERAL_IGNORE,NOT_LITERAL_IGNORE,LITERAL_UNI_IGNORE,NOT_LITERAL_UNI_IGNORE,LITERAL_LOC_IGNORE,NOT_LITERAL_LOC_IGNORE):arg=code[i];i+=1;print_(op,'%#02x (%r)'%(arg,chr(arg)))
			elif op is AT:arg=code[i];i+=1;arg=str(ATCODES[arg]);assert arg[:3]=='AT_';print_(op,arg[3:])
			elif op is CATEGORY:arg=code[i];i+=1;arg=str(CHCODES[arg]);assert arg[:9]=='CATEGORY_';print_(op,arg[9:])
			elif op in(IN,IN_IGNORE,IN_UNI_IGNORE,IN_LOC_IGNORE):skip=code[i];print_(op,skip,to=i+skip);dis_(i+1,i+skip);i+=skip
			elif op in(RANGE,RANGE_UNI_IGNORE):lo,hi=code[i:i+2];i+=2;print_(op,'%#02x %#02x (%r-%r)'%(lo,hi,chr(lo),chr(hi)))
			elif op is CHARSET:print_(op,_hex_code(code[i:i+256//_CODEBITS]));i+=256//_CODEBITS
			elif op is BIGCHARSET:
				arg=code[i];i+=1;mapping=list(b''.join(x.to_bytes(_sre.CODESIZE,sys.byteorder)for x in code[i:i+256//_sre.CODESIZE]));print_(op,arg,mapping);i+=256//_sre.CODESIZE;level+=1
				for j in range(arg):print_2(_hex_code(code[i:i+256//_CODEBITS]));i+=256//_CODEBITS
				level-=1
			elif op in(MARK,GROUPREF,GROUPREF_IGNORE,GROUPREF_UNI_IGNORE,GROUPREF_LOC_IGNORE):arg=code[i];i+=1;print_(op,arg)
			elif op is JUMP:skip=code[i];print_(op,skip,to=i+skip);i+=1
			elif op is BRANCH:
				skip=code[i];print_(op,skip,to=i+skip)
				while skip:
					dis_(i+1,i+skip);i+=skip;start=i;skip=code[i]
					if skip:print_('branch',skip,to=i+skip)
					else:print_(FAILURE)
				i+=1
			elif op in(REPEAT,REPEAT_ONE,MIN_REPEAT_ONE):
				skip,min,max=code[i:i+3]
				if max==MAXREPEAT:max=A
				print_(op,skip,min,max,to=i+skip);dis_(i+3,i+skip);i+=skip
			elif op is GROUPREF_EXISTS:arg,skip=code[i:i+2];print_(op,arg,skip,to=i+skip);i+=2
			elif op in(ASSERT,ASSERT_NOT):skip,arg=code[i:i+2];print_(op,skip,arg,to=i+skip);dis_(i+2,i+skip);i+=skip
			elif op is INFO:
				skip,flags,min,max=code[i:i+4]
				if max==MAXREPEAT:max=A
				print_(op,skip,bin(flags),min,max,to=i+skip);start=i+4
				if flags&SRE_INFO_PREFIX:prefix_len,prefix_skip=code[i+4:i+6];print_2('  prefix_skip',prefix_skip);start=i+6;prefix=code[start:start+prefix_len];print_2('  prefix','[%s]'%', '.join('%#02x'%x for x in prefix),'(%r)'%''.join(map(chr,prefix)));start+=prefix_len;print_2('  overlap',code[start:start+prefix_len]);start+=prefix_len
				if flags&SRE_INFO_CHARSET:level+=1;print_2('in');dis_(start,i+skip);level-=1
				i+=skip
			else:raise ValueError(op)
		level-=1
	dis_(0,len(code))
def compile(p,flags=0):
	if isstring(p):pattern=p;p=sre_parse.parse(p,flags)
	else:pattern=_A
	code=_code(p,flags)
	if flags&SRE_FLAG_DEBUG:print();dis(code)
	groupindex=p.state.groupdict;indexgroup=[_A]*p.state.groups
	for(k,i)in groupindex.items():indexgroup[i]=k
	return _sre.compile(pattern,flags|p.state.flags,code,p.state.groups-1,groupindex,tuple(indexgroup))