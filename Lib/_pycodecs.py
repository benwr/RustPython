'\n\n   _codecs -- Provides access to the codec registry and the builtin\n              codecs.\n\n   This module should never be imported directly. The standard library\n   module "codecs" wraps this builtin module for use within Python.\n\n   The codec registry is accessible via:\n\n     register(search_function) -> None\n\n     lookup(encoding) -> (encoder, decoder, stream_reader, stream_writer)\n\n   The builtin Unicode codecs use the following interface:\n\n     <encoding>_encode(Unicode_object[,errors=\'strict\']) -> \n         (string object, bytes consumed)\n\n     <encoding>_decode(char_buffer_obj[,errors=\'strict\']) -> \n        (Unicode object, bytes consumed)\n\n   <encoding>_encode() interfaces also accept non-Unicode object as\n   input. The objects are then converted to Unicode using\n   PyUnicode_FromObject() prior to applying the conversion.\n\n   These <encoding>s are available: utf_8, unicode_escape,\n   raw_unicode_escape, unicode_internal, latin_1, ascii (7-bit),\n   mbcs (on win32).\n\n\nWritten by Marc-Andre Lemburg (mal@lemburg.com).\n\nCopyright (c) Corporation for National Research Initiatives.\n\nFrom PyPy v1.0.0\n\n'
_R='ordinal not in range(128)'
_Q=b'\\u%04x'
_P='charmap'
_O=b'\\U%08x'
_N='character maps to <undefined>'
_M='latin-1'
_L=b'+'
_K=b'-'
_J='native'
_I='unicodeescape'
_H=True
_G=None
_F='0'
_E='big'
_D='\\'
_C='little'
_B=False
_A='strict'
__all__=['register','lookup','lookup_error','register_error','encode','decode','latin_1_encode','mbcs_decode','readbuffer_encode','escape_encode','utf_8_decode','raw_unicode_escape_decode','utf_7_decode','unicode_escape_encode','latin_1_decode','utf_16_decode','unicode_escape_decode','ascii_decode','charmap_encode','charmap_build','unicode_internal_encode','unicode_internal_decode','utf_16_ex_decode','escape_decode','charmap_decode','utf_7_encode','mbcs_encode','ascii_encode','utf_16_encode','raw_unicode_escape_encode','utf_8_encode','utf_16_le_encode','utf_16_be_encode','utf_16_le_decode','utf_16_be_decode']
import sys,warnings
from _codecs import*
def latin_1_encode(obj,errors=_A):'None\n    ';res=PyUnicode_EncodeLatin1(obj,len(obj),errors);res=bytes(res);return res,len(obj)
def mbcs_decode():'None\n    '
def readbuffer_encode(obj,errors=_A):
	'None\n    '
	if isinstance(obj,str):res=obj.encode()
	else:res=bytes(obj)
	return res,len(obj)
def escape_encode(obj,errors=_A):
	'None\n    '
	if not isinstance(obj,bytes):raise TypeError('must be bytes')
	s=repr(obj).encode();v=s[2:-1]
	if s[1]==ord('"'):v=v.replace(b"'",b"\\'").replace(b'\\"',b'"')
	return v,len(obj)
def raw_unicode_escape_decode(data,errors=_A,final=_B):'None\n    ';res=PyUnicode_DecodeRawUnicodeEscape(data,len(data),errors,final);res=''.join(res);return res,len(data)
def utf_7_decode(data,errors=_A):'None\n    ';res=PyUnicode_DecodeUTF7(data,len(data),errors);res=''.join(res);return res,len(data)
def unicode_escape_encode(obj,errors=_A):'None\n    ';res=unicodeescape_string(obj,len(obj),0);res=b''.join(res);return res,len(obj)
def latin_1_decode(data,errors=_A):'None\n    ';res=PyUnicode_DecodeLatin1(data,len(data),errors);res=''.join(res);return res,len(data)
def utf_16_decode(data,errors=_A,final=_B):
	'None\n    ';consumed=len(data)
	if final:consumed=0
	res,consumed,byteorder=PyUnicode_DecodeUTF16Stateful(data,len(data),errors,_J,final);res=''.join(res);return res,consumed
def unicode_escape_decode(data,errors=_A,final=_B):'None\n    ';res=PyUnicode_DecodeUnicodeEscape(data,len(data),errors,final);res=''.join(res);return res,len(data)
def ascii_decode(data,errors=_A):'None\n    ';res=PyUnicode_DecodeASCII(data,len(data),errors);res=''.join(res);return res,len(data)
def charmap_encode(obj,errors=_A,mapping=_M):'None\n    ';res=PyUnicode_EncodeCharmap(obj,len(obj),mapping,errors);res=bytes(res);return res,len(obj)
def charmap_build(s):return{ord(c):i for(i,c)in enumerate(s)}
if sys.maxunicode==65535:unicode_bytes=2
else:unicode_bytes=4
def unicode_internal_encode(obj,errors=_A):
	'None\n    '
	if type(obj)==str:
		p=bytearray();t=[ord(x)for x in obj]
		for i in t:
			b=bytearray()
			for j in range(unicode_bytes):b.append(i%256);i>>=8
			if sys.byteorder==_E:b.reverse()
			p+=b
		res=bytes(p);return res,len(res)
	else:res='You can do better than this';return res,len(res)
def unicode_internal_decode(unistr,errors=_A):
	'None\n    '
	if type(unistr)==str:return unistr,len(unistr)
	else:
		p=[];i=0
		if sys.byteorder==_E:start=unicode_bytes-1;stop=-1;step=-1
		else:start=0;stop=unicode_bytes;step=1
		while i<len(unistr)-unicode_bytes+1:
			t=0;h=0
			for j in range(start,stop,step):t+=ord(unistr[i+j])<<h*8;h+=1
			i+=unicode_bytes;p+=chr(t)
		res=''.join(p);return res,len(res)
def utf_16_ex_decode(data,errors=_A,byteorder=0,final=0):
	'None\n    '
	if byteorder==0:bm=_J
	elif byteorder==-1:bm=_C
	else:bm=_E
	consumed=len(data)
	if final:consumed=0
	res,consumed,byteorder=PyUnicode_DecodeUTF16Stateful(data,len(data),errors,bm,final);res=''.join(res);return res,consumed,byteorder
def escape_decode(data,errors=_A):
	'None\n    ';l=len(data);i=0;res=bytearray()
	while i<l:
		if data[i]==_D:
			i+=1
			if i>=l:raise ValueError('Trailing \\ in string')
			elif data[i]==_D:res+=b'\\'
			elif data[i]=='n':res+=b'\n'
			elif data[i]=='t':res+=b'\t'
			elif data[i]=='r':res+=b'\r'
			elif data[i]=='b':res+=b'\x08'
			elif data[i]=="'":res+=b"'"
			elif data[i]=='"':res+=b'"'
			elif data[i]=='f':res+=b'\x0c'
			elif data[i]=='a':res+=b'\x07'
			elif data[i]=='v':res+=b'\x0b'
			elif _F<=data[i]<='9':octal=data[i:i+3];res.append(int(octal,8)&255);i+=2
			elif data[i]=='x':hexa=data[i+1:i+3];res.append(int(hexa,16));i+=2
		else:res.append(data[i])
		i+=1
	res=bytes(res);return res,len(res)
def charmap_decode(data,errors=_A,mapping=_G):'None\n    ';res=PyUnicode_DecodeCharmap(data,len(data),mapping,errors);res=''.join(res);return res,len(data)
def utf_7_encode(obj,errors=_A):'None\n    ';res=PyUnicode_EncodeUTF7(obj,len(obj),0,0,errors);res=b''.join(res);return res,len(obj)
def mbcs_encode(obj,errors=_A):'None\n    '
def ascii_encode(obj,errors=_A):'None\n    ';res=PyUnicode_EncodeASCII(obj,len(obj),errors);res=bytes(res);return res,len(obj)
def utf_16_encode(obj,errors=_A):'None\n    ';res=PyUnicode_EncodeUTF16(obj,len(obj),errors,_J);res=bytes(res);return res,len(obj)
def raw_unicode_escape_encode(obj,errors=_A):'None\n    ';res=PyUnicode_EncodeRawUnicodeEscape(obj,len(obj));res=bytes(res);return res,len(obj)
def utf_16_le_encode(obj,errors=_A):'None\n    ';res=PyUnicode_EncodeUTF16(obj,len(obj),errors,_C);res=bytes(res);return res,len(obj)
def utf_16_be_encode(obj,errors=_A):'None\n    ';res=PyUnicode_EncodeUTF16(obj,len(obj),errors,_E);res=bytes(res);return res,len(obj)
def utf_16_le_decode(data,errors=_A,byteorder=0,final=0):
	'None\n    ';consumed=len(data)
	if final:consumed=0
	res,consumed,byteorder=PyUnicode_DecodeUTF16Stateful(data,len(data),errors,_C,final);res=''.join(res);return res,consumed
def utf_16_be_decode(data,errors=_A,byteorder=0,final=0):
	'None\n    ';consumed=len(data)
	if final:consumed=0
	res,consumed,byteorder=PyUnicode_DecodeUTF16Stateful(data,len(data),errors,_E,final);res=''.join(res);return res,consumed
utf7_special=[1,1,1,1,1,1,1,1,1,2,2,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,3,3,3,3,3,3,0,0,0,3,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,1,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,1,1]
unicode_latin1=[_G]*256
def SPECIAL(c,encodeO,encodeWS):c=ord(c);return(c>127 or utf7_special[c]==1)or encodeWS and utf7_special[c]==2 or encodeO and utf7_special[c]==3
def B64(n):return bytes([b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'[n&63]])
def B64CHAR(c):return c.isalnum()or c==_L or c==b'/'
def UB64(c):
	if c==_L:return 62
	elif c==b'/':return 63
	elif c>=b'a':return ord(c)-71
	elif c>=b'A':return ord(c)-65
	else:return ord(c)+4
def ENCODE(ch,bits):
	out=[]
	while bits>=6:out+=B64(ch>>bits-6);bits-=6
	return out,bits
def PyUnicode_DecodeUTF7(s,size,errors):
	B='unexpected special character';A='utf-7';starts=s;errmsg='';inShift=0;bitsleft=0;charsleft=0;surrogate=0;p=[];errorHandler=_G;exc=_G
	if size==0:return''
	i=0
	while i<size:
		ch=bytes([s[i]])
		if inShift:
			if ch==_K or not B64CHAR(ch):
				inShift=0;i+=1
				while bitsleft>=16:
					outCh=charsleft>>bitsleft-16&65535;bitsleft-=16
					if surrogate:surrogate=0
					elif 56320<=outCh and outCh<=57343:surrogate=1;msg='code pairs are not supported';out,x=unicode_call_errorhandler(errors,A,msg,s,i-1,i);p.append(out);bitsleft=0;break
					else:p.append(chr(outCh))
				if bitsleft>=6:msg='partial character in shift sequence';out,x=unicode_call_errorhandler(errors,A,msg,s,i-1,i)
				if ch==_K:
					if i<size and s[i]=='-':p+='-';inShift=1
				elif SPECIAL(ch,0,0):raise UnicodeDecodeError(B)
				else:p.append(chr(ord(ch)))
			else:charsleft=charsleft<<6|UB64(ch);bitsleft+=6;i+=1
		elif ch==_L:
			startinpos=i;i+=1
			if i<size and s[i]=='-':i+=1;p.append(_L)
			else:inShift=1;bitsleft=0
		elif SPECIAL(ch,0,0):i+=1;raise UnicodeDecodeError(B)
		else:p.append(chr(ord(ch)));i+=1
	if inShift:endinpos=size;raise UnicodeDecodeError('unterminated shift sequence')
	return p
def PyUnicode_EncodeUTF7(s,size,encodeSetO,encodeWhiteSpace,errors):
	inShift=_B;i=0;bitsleft=0;charsleft=0;out=[]
	for ch in s:
		if not inShift:
			if ch=='+':out.append(b'+-')
			elif SPECIAL(ch,encodeSetO,encodeWhiteSpace):charsleft=ord(ch);bitsleft=16;out.append(_L);p,bitsleft=ENCODE(charsleft,bitsleft);out.append(p);inShift=bitsleft>0
			else:out.append(bytes([ord(ch)]))
		elif not SPECIAL(ch,encodeSetO,encodeWhiteSpace):
			out.append(B64(charsleft<<6-bitsleft));charsleft=0;bitsleft=0
			if B64CHAR(ch)or ch=='-':out.append(_K)
			inShift=_B;out.append(bytes([ord(ch)]))
		else:
			bitsleft+=16;charsleft=charsleft<<16|ord(ch);p,bitsleft=ENCODE(charsleft,bitsleft);out.append(p)
			if bitsleft==0:
				if i+1<size:
					ch2=s[i+1]
					if SPECIAL(ch2,encodeSetO,encodeWhiteSpace):0
					elif B64CHAR(ch2)or ch2=='-':out.append(_K);inShift=_B
					else:inShift=_B
				else:out.append(_K);inShift=_B
		i+=1
	if bitsleft:out.append(B64(charsleft<<6-bitsleft));out.append(_K)
	return out
unicode_empty=''
def unicodeescape_string(s,size,quotes):
	p=[]
	if quotes:
		if s.find("'")!=-1 and s.find('"')==-1:p.append(b'"')
		else:p.append(b"'")
	pos=0
	while pos<size:
		ch=s[pos]
		if quotes and(ch==p[1]or ch==_D):p.append(b'\\%c'%ord(ch));pos+=1;continue
		elif ord(ch)>=65536:p.append(_O%ord(ch));pos+=1;continue
		elif ord(ch)>=55296 and ord(ch)<56320:
			pos+=1;ch2=s[pos]
			if ord(ch2)>=56320 and ord(ch2)<=57343:ucs=((ord(ch)&1023)<<10|ord(ch2)&1023)+65536;p.append(_O%ucs);pos+=1;continue
			pos-=1
		if ord(ch)>=256:p.append(_Q%ord(ch))
		elif ch=='\t':p.append(b'\\t')
		elif ch=='\n':p.append(b'\\n')
		elif ch=='\r':p.append(b'\\r')
		elif ch==_D:p.append(b'\\\\')
		elif ch<' 'or ch>=chr(127):p.append(b'\\x%02x'%ord(ch))
		else:p.append(bytes([ord(ch)]))
		pos+=1
	if quotes:p.append(p[0])
	return p
def PyUnicode_DecodeASCII(s,size,errors):
	if size==1 and ord(s)<128:return[chr(ord(s))]
	if size==0:return['']
	p=[];pos=0
	while pos<len(s):
		c=s[pos]
		if c<128:p+=chr(c);pos+=1
		else:res=unicode_call_errorhandler(errors,'ascii',_R,s,pos,pos+1);p+=res[0];pos=res[1]
	return p
def PyUnicode_EncodeASCII(p,size,errors):return unicode_encode_ucs1(p,size,errors,128)
def PyUnicode_AsASCIIString(unistr):
	if not type(unistr)==str:raise TypeError
	return PyUnicode_EncodeASCII(str(unistr),len(str),_G)
def PyUnicode_DecodeUTF16Stateful(s,size,errors,byteorder=_J,final=_H):
	A='utf-16';bo=0;consumed=0;errmsg=''
	if sys.byteorder==_C:ihi=1;ilo=0
	else:ihi=0;ilo=1
	q=0;p=[]
	if byteorder==_J:
		if size>=2:
			bom=s[ihi]<<8|s[ilo]
			if sys.byteorder==_C:
				if bom==65279:q+=2;bo=-1
				elif bom==65534:q+=2;bo=1
			elif bom==65279:q+=2;bo=1
			elif bom==65534:q+=2;bo=-1
	elif byteorder==_C:bo=-1
	else:bo=1
	if size==0:return[''],0,bo
	if bo==-1:ihi=1;ilo=0
	elif bo==1:ihi=0;ilo=1
	while q<len(s):
		if len(s)-q<2:
			if not final:break
			errmsg='truncated data';startinpos=q;endinpos=len(s);unicode_call_errorhandler(errors,A,errmsg,s,startinpos,endinpos,_H)
		ch=s[q+ihi]<<8|s[q+ilo];q+=2
		if ch<55296 or ch>57343:p.append(chr(ch));continue
		if q>=len(s):errmsg='unexpected end of data';startinpos=q-2;endinpos=len(s);unicode_call_errorhandler(errors,A,errmsg,s,startinpos,endinpos,_H)
		if 55296<=ch and ch<=56319:
			ch2=s[q+ihi]<<8|s[q+ilo];q+=2
			if 56320<=ch2 and ch2<=57343:
				if sys.maxunicode<65536:p+=[chr(ch),chr(ch2)]
				else:p.append(chr(((ch&1023)<<10|ch2&1023)+65536))
				continue
			else:errmsg='illegal UTF-16 surrogate';startinpos=q-4;endinpos=startinpos+2;unicode_call_errorhandler(errors,A,errmsg,s,startinpos,endinpos,_H)
		errmsg='illegal encoding';startinpos=q-2;endinpos=startinpos+2;unicode_call_errorhandler(errors,A,errmsg,s,startinpos,endinpos,_H)
	return p,q,bo
def STORECHAR(CH,byteorder):
	hi=CH>>8&255;lo=CH&255
	if byteorder==_C:return[lo,hi]
	else:return[hi,lo]
def PyUnicode_EncodeUTF16(s,size,errors,byteorder=_C):
	p=[];bom=sys.byteorder
	if byteorder==_J:bom=sys.byteorder;p+=STORECHAR(65279,bom)
	if size==0:return''
	if byteorder==_C:bom=_C
	elif byteorder==_E:bom=_E
	for c in s:
		ch=ord(c);ch2=0
		if ch>=65536:ch2=56320|ch-65536&1023;ch=55296|ch-65536>>10
		p+=STORECHAR(ch,bom)
		if ch2:p+=STORECHAR(ch2,bom)
	return p
def PyUnicode_DecodeMBCS(s,size,errors):0
def PyUnicode_EncodeMBCS(p,size,errors):0
def unicode_call_errorhandler(errors,encoding,reason,input,startinpos,endinpos,decode=_H):
	errorHandler=lookup_error(errors)
	if decode:exceptionObject=UnicodeDecodeError(encoding,input,startinpos,endinpos,reason)
	else:exceptionObject=UnicodeEncodeError(encoding,input,startinpos,endinpos,reason)
	res=errorHandler(exceptionObject)
	if isinstance(res,tuple)and isinstance(res[0],str)and isinstance(res[1],int):
		newpos=res[1]
		if newpos<0:newpos=len(input)+newpos
		if newpos<0 or newpos>len(input):raise IndexError('position %d from error handler out of bounds'%newpos)
		return res[0],newpos
	else:raise TypeError('encoding error handler must return (unicode, int) tuple, not %s'%repr(res))
def PyUnicode_DecodeLatin1(s,size,errors):
	pos=0;p=[]
	while pos<size:p+=chr(s[pos]);pos+=1
	return p
def unicode_encode_ucs1(p,size,errors,limit):
	if limit==256:reason='ordinal not in range(256)';encoding=_M
	else:reason=_R;encoding='ascii'
	if size==0:return[]
	res=bytearray();pos=0
	while pos<len(p):
		ch=p[pos]
		if ord(ch)<limit:res.append(ord(ch));pos+=1
		else:
			collstart=pos;collend=pos+1
			while collend<len(p)and ord(p[collend])>=limit:collend+=1
			x=unicode_call_errorhandler(errors,encoding,reason,p,collstart,collend,_B);res+=x[0].encode();pos=x[1]
	return res
def PyUnicode_EncodeLatin1(p,size,errors):res=unicode_encode_ucs1(p,size,errors,256);return res
hexdigits=[ord(hex(i)[-1])for i in range(16)]+[ord(hex(i)[-1].upper())for i in range(10,16)]
def hex_number_end(s,pos,digits):
	target_end=pos+digits
	while pos<target_end and pos<len(s)and s[pos]in hexdigits:pos+=1
	return pos
def hexescape(s,pos,digits,message,errors):
	ch=0;p=[];number_end=hex_number_end(s,pos,digits)
	if number_end-pos!=digits:x=unicode_call_errorhandler(errors,_I,message,s,pos-2,number_end);p.append(x[0]);pos=x[1]
	else:
		ch=int(s[pos:pos+digits],16)
		if ch<=sys.maxunicode:p.append(chr(ch));pos+=digits
		elif ch<=1114111:ch-=65536;p.append(chr(55296+(ch>>10)));p.append(chr(56320+(ch&1023)));pos+=digits
		else:message='illegal Unicode character';x=unicode_call_errorhandler(errors,_I,message,s,pos-2,pos+digits);p.append(x[0]);pos=x[1]
	res=p;return res,pos
def PyUnicode_DecodeUnicodeEscape(s,size,errors,final):
	A='7'
	if size==0:return''
	if isinstance(s,str):s=s.encode()
	found_invalid_escape=_B;p=[];pos=0
	while pos<size:
		if chr(s[pos])!=_D:p.append(chr(s[pos]));pos+=1;continue
		else:
			pos+=1
			if pos>=len(s):errmessage='\\ at end of string';unicode_call_errorhandler(errors,_I,errmessage,s,pos-1,size)
			ch=chr(s[pos]);pos+=1
			if ch=='\n':0
			elif ch==_D:p+=_D
			elif ch=="'":p+="'"
			elif ch=='"':p+='"'
			elif ch=='b':p+='\x08'
			elif ch=='f':p+='\x0c'
			elif ch=='t':p+='\t'
			elif ch=='n':p+='\n'
			elif ch=='r':p+='\r'
			elif ch=='v':p+='\x0b'
			elif ch=='a':p+='\x07'
			elif _F<=ch<=A:
				x=ord(ch)-ord(_F)
				if pos<size:
					ch=chr(s[pos])
					if _F<=ch<=A:
						pos+=1;x=(x<<3)+ord(ch)-ord(_F)
						if pos<size:
							ch=chr(s[pos])
							if _F<=ch<=A:pos+=1;x=(x<<3)+ord(ch)-ord(_F)
				p.append(chr(x))
			elif ch=='x':digits=2;message='truncated \\xXX escape';x=hexescape(s,pos,digits,message,errors);p+=x[0];pos=x[1]
			elif ch=='u':digits=4;message='truncated \\uXXXX escape';x=hexescape(s,pos,digits,message,errors);p+=x[0];pos=x[1]
			elif ch=='U':digits=8;message='truncated \\UXXXXXXXX escape';x=hexescape(s,pos,digits,message,errors);p+=x[0];pos=x[1]
			elif ch=='N':
				message='malformed \\N character escape';look=pos
				try:import unicodedata
				except ImportError:message="\\N escapes not supported (can't load unicodedata module)";unicode_call_errorhandler(errors,_I,message,s,pos-1,size)
				if look<size and chr(s[look])=='{':
					while look<size and chr(s[look])!='}':look+=1
					if look>pos+1 and look<size and chr(s[look])=='}':
						message='unknown Unicode character name';st=s[pos+1:look]
						try:chr_codec=unicodedata.lookup('%s'%st)
						except LookupError as e:x=unicode_call_errorhandler(errors,_I,message,s,pos-1,look+1)
						else:x=chr_codec,look+1
						p.append(x[0]);pos=x[1]
					else:x=unicode_call_errorhandler(errors,_I,message,s,pos-1,look+1)
				else:x=unicode_call_errorhandler(errors,_I,message,s,pos-1,look+1)
			else:
				if not found_invalid_escape:found_invalid_escape=_H;warnings.warn("invalid escape sequence '\\%c'"%ch,DeprecationWarning,2)
				p.append(_D);p.append(ch)
	return p
def PyUnicode_EncodeRawUnicodeEscape(s,size):
	if size==0:return b''
	p=bytearray()
	for ch in s:
		if ord(ch)>=65536:p+=_O%ord(ch)
		elif ord(ch)>=256:p+=_Q%ord(ch)
		else:p.append(ord(ch))
	return p
def charmapencode_output(c,mapping):
	rep=mapping[c]
	if isinstance(rep,int)or isinstance(rep,int):
		if rep<256:return rep
		else:raise TypeError('character mapping must be in range(256)')
	elif isinstance(rep,str):return ord(rep)
	elif rep==_G:raise KeyError(_N)
	else:raise TypeError('character mapping must return integer, None or str')
def PyUnicode_EncodeCharmap(p,size,mapping=_M,errors=_A):
	if mapping==_M:return PyUnicode_EncodeLatin1(p,size,errors)
	if size==0:return b''
	inpos=0;res=[]
	while inpos<size:
		try:x=charmapencode_output(ord(p[inpos]),mapping);res+=[x]
		except KeyError:
			x=unicode_call_errorhandler(errors,_P,_N,p,inpos,inpos+1,_B)
			try:res+=[charmapencode_output(ord(y),mapping)for y in x[0]]
			except KeyError:raise UnicodeEncodeError(_P,p,inpos,inpos+1,_N)
		inpos+=1
	return res
def PyUnicode_DecodeCharmap(s,size,mapping,errors):
	if mapping==_G:return PyUnicode_DecodeLatin1(s,size,errors)
	if size==0:return''
	p=[];inpos=0
	while inpos<len(s):
		ch=s[inpos]
		try:
			x=mapping[ch]
			if isinstance(x,int):
				if x<65536:p+=chr(x)
				else:raise TypeError('character mapping must be in range(65536)')
			elif isinstance(x,str):p+=x
			elif not x:raise KeyError
			else:raise TypeError
		except KeyError:x=unicode_call_errorhandler(errors,_P,_N,s,inpos,inpos+1);p+=x[0]
		inpos+=1
	return p
def PyUnicode_DecodeRawUnicodeEscape(s,size,errors,final):
	B='\\Uxxxxxxxx out of range';A='rawunicodeescape'
	if size==0:return''
	if isinstance(s,str):s=s.encode()
	pos=0;p=[]
	while pos<len(s):
		ch=chr(s[pos])
		if ch!=_D:p.append(ch);pos+=1;continue
		startinpos=pos;bs=pos
		while pos<size:
			if s[pos]!=ord(_D):break
			p.append(chr(s[pos]));pos+=1
		if pos>=size:break
		if pos-bs&1==0 or s[pos]!=ord('u')and s[pos]!=ord('U'):p.append(chr(s[pos]));pos+=1;continue
		p.pop(-1)
		if s[pos]==ord('u'):count=4
		else:count=8
		pos+=1;number_end=hex_number_end(s,pos,count)
		if number_end-pos!=count:res=unicode_call_errorhandler(errors,A,'truncated \\uXXXX',s,pos-2,number_end);p.append(res[0]);pos=res[1]
		else:
			x=int(s[pos:pos+count],16)
			if sys.maxunicode>65535:
				if x>sys.maxunicode:res=unicode_call_errorhandler(errors,A,B,s,pos-2,pos+count);pos=res[1];p.append(res[0])
				else:p.append(chr(x));pos+=count
			elif x>65536:res=unicode_call_errorhandler(errors,A,B,s,pos-2,pos+count);pos=res[1];p.append(res[0])
			else:p.append(chr(x));pos+=count
	return p