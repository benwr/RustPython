'Internationalization and localization support.\n\nThis module provides internationalization (I18N) and localization (L10N)\nsupport for your Python programs by providing an interface to the GNU gettext\nmessage catalog library.\n\nI18N refers to the operation by which a program is made aware of multiple\nlanguages.  L10N refers to the adaptation of your program, once\ninternationalized, to the local language and cultural habits.\n\n'
_E='ngettext'
_D='lngettext'
_C='lgettext'
_B='gettext'
_A=None
import locale,os,re,sys
__all__=['NullTranslations','GNUTranslations','Catalog','find','translation','install','textdomain','bindtextdomain','bind_textdomain_codeset','dgettext','dngettext',_B,_C,'ldgettext','ldngettext',_D,_E]
_default_localedir=os.path.join(sys.base_prefix,'share','locale')
_token_pattern=re.compile('\n        (?P<WHITESPACES>[ \\t]+)                    | # spaces and horizontal tabs\n        (?P<NUMBER>[0-9]+\\b)                       | # decimal integer\n        (?P<NAME>n\\b)                              | # only n is allowed\n        (?P<PARENTHESIS>[()])                      |\n        (?P<OPERATOR>[-*/%+?:]|[><!]=?|==|&&|\\|\\|) | # !, *, /, %, +, -, <, >,\n                                                     # <=, >=, ==, !=, &&, ||,\n                                                     # ? :\n                                                     # unary and bitwise ops\n                                                     # not allowed\n        (?P<INVALID>\\w+|.)                           # invalid token\n    ',re.VERBOSE|re.DOTALL)
def _tokenize(plural):
	for mo in re.finditer(_token_pattern,plural):
		kind=mo.lastgroup
		if kind=='WHITESPACES':continue
		value=mo.group(kind)
		if kind=='INVALID':raise ValueError('invalid token in plural form: %s'%value)
		yield value
	yield''
def _error(value):
	if value:return ValueError('unexpected token in plural form: %s'%value)
	else:return ValueError('unexpected end of plural form')
_binary_ops=('||',),('&&',),('==','!='),('<','>','<=','>='),('+','-'),('*','/','%')
_binary_ops={op:i for(i,ops)in enumerate(_binary_ops,1)for op in ops}
_c2py_ops={'||':'or','&&':'and','/':'//'}
def _parse(tokens,priority=-1):
	A='(%s)';result='';nexttok=next(tokens)
	while nexttok=='!':result+='not ';nexttok=next(tokens)
	if nexttok=='(':
		sub,nexttok=_parse(tokens);result='%s(%s)'%(result,sub)
		if nexttok!=')':raise ValueError('unbalanced parenthesis in plural form')
	elif nexttok=='n':result='%s%s'%(result,nexttok)
	else:
		try:value=int(nexttok,10)
		except ValueError:raise _error(nexttok)from _A
		result='%s%d'%(result,value)
	nexttok=next(tokens);j=100
	while nexttok in _binary_ops:
		i=_binary_ops[nexttok]
		if i<priority:break
		if i in(3,4)and j in(3,4):result=A%result
		op=_c2py_ops.get(nexttok,nexttok);right,nexttok=_parse(tokens,i+1);result='%s %s %s'%(result,op,right);j=i
	if j==priority==4:result=A%result
	if nexttok=='?'and priority<=0:
		if_true,nexttok=_parse(tokens,0)
		if nexttok!=':':raise _error(nexttok)
		if_false,nexttok=_parse(tokens);result='%s if %s else %s'%(if_true,result,if_false)
		if priority==0:result=A%result
	return result,nexttok
def _as_int(n):
	A='Plural value must be an integer, got %s'
	try:i=round(n)
	except TypeError:raise TypeError(A%(n.__class__.__name__,))from _A
	import warnings;warnings.warn(A%(n.__class__.__name__,),DeprecationWarning,4);return n
def c2py(plural):
	'Gets a C expression as used in PO files for plural forms and returns a\n    Python function that implements an equivalent expression.\n    ';A='plural form expression is too complex'
	if len(plural)>1000:raise ValueError('plural form expression is too long')
	try:
		result,nexttok=_parse(_tokenize(plural))
		if nexttok:raise _error(nexttok)
		depth=0
		for c in result:
			if c=='(':
				depth+=1
				if depth>20:raise ValueError(A)
			elif c==')':depth-=1
		ns={'_as_int':_as_int};exec('if True:\n            def func(n):\n                if not isinstance(n, int):\n                    n = _as_int(n)\n                return int(%s)\n            '%result,ns);return ns['func']
	except RecursionError:raise ValueError(A)
def _expand_lang(loc):
	loc=locale.normalize(loc);COMPONENT_CODESET=1<<0;COMPONENT_TERRITORY=1<<1;COMPONENT_MODIFIER=1<<2;mask=0;pos=loc.find('@')
	if pos>=0:modifier=loc[pos:];loc=loc[:pos];mask|=COMPONENT_MODIFIER
	else:modifier=''
	pos=loc.find('.')
	if pos>=0:codeset=loc[pos:];loc=loc[:pos];mask|=COMPONENT_CODESET
	else:codeset=''
	pos=loc.find('_')
	if pos>=0:territory=loc[pos:];loc=loc[:pos];mask|=COMPONENT_TERRITORY
	else:territory=''
	language=loc;ret=[]
	for i in range(mask+1):
		if not i&~mask:
			val=language
			if i&COMPONENT_TERRITORY:val+=territory
			if i&COMPONENT_CODESET:val+=codeset
			if i&COMPONENT_MODIFIER:val+=modifier
			ret.append(val)
	ret.reverse();return ret
class NullTranslations:
	def __init__(self,fp=_A):
		self._info={};self._charset=_A;self._output_charset=_A;self._fallback=_A
		if fp is not _A:self._parse(fp)
	def _parse(self,fp):0
	def add_fallback(self,fallback):
		if self._fallback:self._fallback.add_fallback(fallback)
		else:self._fallback=fallback
	def gettext(self,message):
		if self._fallback:return self._fallback.gettext(message)
		return message
	def lgettext(self,message):
		if self._fallback:return self._fallback.lgettext(message)
		if self._output_charset:return message.encode(self._output_charset)
		return message.encode(locale.getpreferredencoding())
	def ngettext(self,msgid1,msgid2,n):
		if self._fallback:return self._fallback.ngettext(msgid1,msgid2,n)
		if n==1:return msgid1
		else:return msgid2
	def lngettext(self,msgid1,msgid2,n):
		if self._fallback:return self._fallback.lngettext(msgid1,msgid2,n)
		if n==1:tmsg=msgid1
		else:tmsg=msgid2
		if self._output_charset:return tmsg.encode(self._output_charset)
		return tmsg.encode(locale.getpreferredencoding())
	def info(self):return self._info
	def charset(self):return self._charset
	def output_charset(self):return self._output_charset
	def set_output_charset(self,charset):self._output_charset=charset
	def install(self,names=_A):
		import builtins;builtins.__dict__['_']=self.gettext
		if hasattr(names,'__contains__'):
			if _B in names:builtins.__dict__[_B]=builtins.__dict__['_']
			if _E in names:builtins.__dict__[_E]=self.ngettext
			if _C in names:builtins.__dict__[_C]=self.lgettext
			if _D in names:builtins.__dict__[_D]=self.lngettext
class GNUTranslations(NullTranslations):
	LE_MAGIC=2500072158;BE_MAGIC=3725722773;VERSIONS=0,1
	def _get_versions(self,version):'Returns a tuple of major version, minor version';return version>>16,version&65535
	def _parse(self,fp):
		'Override this method to support alternative .mo formats.';A=b'\x00';from struct import unpack;filename=getattr(fp,'name','');self._catalog=catalog={};self.plural=lambda n:int(n!=1);buf=fp.read();buflen=len(buf);magic=unpack('<I',buf[:4])[0]
		if magic==self.LE_MAGIC:version,msgcount,masteridx,transidx=unpack('<4I',buf[4:20]);ii='<II'
		elif magic==self.BE_MAGIC:version,msgcount,masteridx,transidx=unpack('>4I',buf[4:20]);ii='>II'
		else:raise OSError(0,'Bad magic number',filename)
		major_version,minor_version=self._get_versions(version)
		if major_version not in self.VERSIONS:raise OSError(0,'Bad version number '+str(major_version),filename)
		for i in range(0,msgcount):
			mlen,moff=unpack(ii,buf[masteridx:masteridx+8]);mend=moff+mlen;tlen,toff=unpack(ii,buf[transidx:transidx+8]);tend=toff+tlen
			if mend<buflen and tend<buflen:msg=buf[moff:mend];tmsg=buf[toff:tend]
			else:raise OSError(0,'File is corrupt',filename)
			if mlen==0:
				lastk=_A
				for b_item in tmsg.split(b'\n'):
					item=b_item.decode().strip()
					if not item:continue
					k=v=_A
					if':'in item:k,v=item.split(':',1);k=k.strip().lower();v=v.strip();self._info[k]=v;lastk=k
					elif lastk:self._info[lastk]+='\n'+item
					if k=='content-type':self._charset=v.split('charset=')[1]
					elif k=='plural-forms':v=v.split(';');plural=v[1].split('plural=')[1];self.plural=c2py(plural)
			charset=self._charset or'ascii'
			if A in msg:
				msgid1,msgid2=msg.split(A);tmsg=tmsg.split(A);msgid1=str(msgid1,charset)
				for(i,x)in enumerate(tmsg):catalog[msgid1,i]=str(x,charset)
			else:catalog[str(msg,charset)]=str(tmsg,charset)
			masteridx+=8;transidx+=8
	def lgettext(self,message):
		missing=object();tmsg=self._catalog.get(message,missing)
		if tmsg is missing:
			if self._fallback:return self._fallback.lgettext(message)
			tmsg=message
		if self._output_charset:return tmsg.encode(self._output_charset)
		return tmsg.encode(locale.getpreferredencoding())
	def lngettext(self,msgid1,msgid2,n):
		try:tmsg=self._catalog[msgid1,self.plural(n)]
		except KeyError:
			if self._fallback:return self._fallback.lngettext(msgid1,msgid2,n)
			if n==1:tmsg=msgid1
			else:tmsg=msgid2
		if self._output_charset:return tmsg.encode(self._output_charset)
		return tmsg.encode(locale.getpreferredencoding())
	def gettext(self,message):
		missing=object();tmsg=self._catalog.get(message,missing)
		if tmsg is missing:
			if self._fallback:return self._fallback.gettext(message)
			return message
		return tmsg
	def ngettext(self,msgid1,msgid2,n):
		try:tmsg=self._catalog[msgid1,self.plural(n)]
		except KeyError:
			if self._fallback:return self._fallback.ngettext(msgid1,msgid2,n)
			if n==1:tmsg=msgid1
			else:tmsg=msgid2
		return tmsg
def find(domain,localedir=_A,languages=_A,all=False):
	B='LC_MESSAGES';A='C'
	if localedir is _A:localedir=_default_localedir
	if languages is _A:
		languages=[]
		for envar in('LANGUAGE','LC_ALL',B,'LANG'):
			val=os.environ.get(envar)
			if val:languages=val.split(':');break
		if A not in languages:languages.append(A)
	nelangs=[]
	for lang in languages:
		for nelang in _expand_lang(lang):
			if nelang not in nelangs:nelangs.append(nelang)
	if all:result=[]
	else:result=_A
	for lang in nelangs:
		if lang==A:break
		mofile=os.path.join(localedir,lang,B,'%s.mo'%domain)
		if os.path.exists(mofile):
			if all:result.append(mofile)
			else:return mofile
	return result
_translations={}
def translation(domain,localedir=_A,languages=_A,class_=_A,fallback=False,codeset=_A):
	if class_ is _A:class_=GNUTranslations
	mofiles=find(domain,localedir,languages,all=True)
	if not mofiles:
		if fallback:return NullTranslations()
		from errno import ENOENT;raise FileNotFoundError(ENOENT,'No translation file found for domain',domain)
	result=_A
	for mofile in mofiles:
		key=class_,os.path.abspath(mofile);t=_translations.get(key)
		if t is _A:
			with open(mofile,'rb')as fp:t=_translations.setdefault(key,class_(fp))
		import copy;t=copy.copy(t)
		if codeset:t.set_output_charset(codeset)
		if result is _A:result=t
		else:result.add_fallback(t)
	return result
def install(domain,localedir=_A,codeset=_A,names=_A):t=translation(domain,localedir,fallback=True,codeset=codeset);t.install(names)
_localedirs={}
_localecodesets={}
_current_domain='messages'
def textdomain(domain=_A):
	global _current_domain
	if domain is not _A:_current_domain=domain
	return _current_domain
def bindtextdomain(domain,localedir=_A):
	global _localedirs
	if localedir is not _A:_localedirs[domain]=localedir
	return _localedirs.get(domain,_default_localedir)
def bind_textdomain_codeset(domain,codeset=_A):
	global _localecodesets
	if codeset is not _A:_localecodesets[domain]=codeset
	return _localecodesets.get(domain)
def dgettext(domain,message):
	try:t=translation(domain,_localedirs.get(domain,_A),codeset=_localecodesets.get(domain))
	except OSError:return message
	return t.gettext(message)
def ldgettext(domain,message):
	codeset=_localecodesets.get(domain)
	try:t=translation(domain,_localedirs.get(domain,_A),codeset=codeset)
	except OSError:return message.encode(codeset or locale.getpreferredencoding())
	return t.lgettext(message)
def dngettext(domain,msgid1,msgid2,n):
	try:t=translation(domain,_localedirs.get(domain,_A),codeset=_localecodesets.get(domain))
	except OSError:
		if n==1:return msgid1
		else:return msgid2
	return t.ngettext(msgid1,msgid2,n)
def ldngettext(domain,msgid1,msgid2,n):
	codeset=_localecodesets.get(domain)
	try:t=translation(domain,_localedirs.get(domain,_A),codeset=codeset)
	except OSError:
		if n==1:tmsg=msgid1
		else:tmsg=msgid2
		return tmsg.encode(codeset or locale.getpreferredencoding())
	return t.lngettext(msgid1,msgid2,n)
def gettext(message):return dgettext(_current_domain,message)
def lgettext(message):return ldgettext(_current_domain,message)
def ngettext(msgid1,msgid2,n):return dngettext(_current_domain,msgid1,msgid2,n)
def lngettext(msgid1,msgid2,n):return ldngettext(_current_domain,msgid1,msgid2,n)
Catalog=translation