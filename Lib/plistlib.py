'plistlib.py -- a tool to generate and parse MacOSX .plist files.\n\nThe property list (.plist) file format is a simple XML pickle supporting\nbasic object types, like dictionaries, lists, numbers and strings.\nUsually the top level object is a dictionary.\n\nTo write out a plist file, use the dump(value, file)\nfunction. \'value\' is the top level object, \'file\' is\na (writable) file object.\n\nTo parse a plist from a file, use the load(file) function,\nwith a (readable) file object as the only argument. It\nreturns the top level object (again, usually a dictionary).\n\nTo work with plist data in bytes objects, you can use loads()\nand dumps().\n\nValues can be strings, integers, floats, booleans, tuples, lists,\ndictionaries (but only with string keys), Data, bytes, bytearray, or\ndatetime.datetime objects.\n\nGenerate Plist example:\n\n    pl = dict(\n        aString = "Doodah",\n        aList = ["A", "B", 12, 32.1, [1, 2, 3]],\n        aFloat = 0.1,\n        anInt = 728,\n        aDict = dict(\n            anotherString = "<hello & hi there!>",\n            aUnicodeValue = "M\\xe4ssig, Ma\\xdf",\n            aTrueValue = True,\n            aFalseValue = False,\n        ),\n        someData = b"<binary gunk>",\n        someMoreData = b"<lots of binary gunk>" * 10,\n        aDate = datetime.datetime.fromtimestamp(time.mktime(time.gmtime())),\n    )\n    with open(fileName, \'wb\') as fp:\n        dump(pl, fp)\n\nParse Plist example:\n\n    with open(fileName, \'rb\') as fp:\n        pl = load(fp)\n    print(pl["aKey"])\n'
_K=b'bplist00'
_J='utf-16be'
_I='UIDs must be positive'
_H='ascii'
_G='keys must be strings'
_F=b'\t'
_E='utf-8'
_D='big'
_C=False
_B=True
_A=None
__all__=['InvalidFileException','FMT_XML','FMT_BINARY','load','dump','loads','dumps','UID']
import binascii,codecs,datetime,enum
from io import BytesIO
import itertools,os,re,struct
from xml.parsers.expat import ParserCreate
PlistFormat=enum.Enum('PlistFormat','FMT_XML FMT_BINARY',module=__name__)
globals().update(PlistFormat.__members__)
class UID:
	def __init__(self,data):
		if not isinstance(data,int):raise TypeError('data must be an int')
		if data>=1<<64:raise ValueError('UIDs cannot be >= 2**64')
		if data<0:raise ValueError(_I)
		self.data=data
	def __index__(self):return self.data
	def __repr__(self):return'%s(%s)'%(self.__class__.__name__,repr(self.data))
	def __reduce__(self):return self.__class__,(self.data,)
	def __eq__(self,other):
		if not isinstance(other,UID):return NotImplemented
		return self.data==other.data
	def __hash__(self):return hash(self.data)
PLISTHEADER=b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
_controlCharPat=re.compile('[\\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\x0b\\x0c\\x0e\\x0f\\x10\\x11\\x12\\x13\\x14\\x15\\x16\\x17\\x18\\x19\\x1a\\x1b\\x1c\\x1d\\x1e\\x1f]')
def _encode_base64(s,maxlinelength=76):
	maxbinsize=maxlinelength//4*3;pieces=[]
	for i in range(0,len(s),maxbinsize):chunk=s[i:i+maxbinsize];pieces.append(binascii.b2a_base64(chunk))
	return b''.join(pieces)
def _decode_base64(s):
	if isinstance(s,str):return binascii.a2b_base64(s.encode(_E))
	else:return binascii.a2b_base64(s)
_dateParser=re.compile('(?P<year>\\d\\d\\d\\d)(?:-(?P<month>\\d\\d)(?:-(?P<day>\\d\\d)(?:T(?P<hour>\\d\\d)(?::(?P<minute>\\d\\d)(?::(?P<second>\\d\\d))?)?)?)?)?Z',re.ASCII)
def _date_from_string(s):
	order='year','month','day','hour','minute','second';gd=_dateParser.match(s).groupdict();lst=[]
	for key in order:
		val=gd[key]
		if val is _A:break
		lst.append(int(val))
	return datetime.datetime(*lst)
def _date_to_string(d):return'%04d-%02d-%02dT%02d:%02d:%02dZ'%(d.year,d.month,d.day,d.hour,d.minute,d.second)
def _escape(text):
	m=_controlCharPat.search(text)
	if m is not _A:raise ValueError("strings can't contains control characters; use bytes instead")
	text=text.replace('\r\n','\n');text=text.replace('\r','\n');text=text.replace('&','&amp;');text=text.replace('<','&lt;');text=text.replace('>','&gt;');return text
class _PlistParser:
	def __init__(self,dict_type):self.stack=[];self.current_key=_A;self.root=_A;self._dict_type=dict_type
	def parse(self,fileobj):self.parser=ParserCreate();self.parser.StartElementHandler=self.handle_begin_element;self.parser.EndElementHandler=self.handle_end_element;self.parser.CharacterDataHandler=self.handle_data;self.parser.EntityDeclHandler=self.handle_entity_decl;self.parser.ParseFile(fileobj);return self.root
	def handle_entity_decl(self,entity_name,is_parameter_entity,value,base,system_id,public_id,notation_name):raise InvalidFileException('XML entity declarations are not supported in plist files')
	def handle_begin_element(self,element,attrs):
		self.data=[];handler=getattr(self,'begin_'+element,_A)
		if handler is not _A:handler(attrs)
	def handle_end_element(self,element):
		handler=getattr(self,'end_'+element,_A)
		if handler is not _A:handler()
	def handle_data(self,data):self.data.append(data)
	def add_object(self,value):
		A='unexpected element at line %d'
		if self.current_key is not _A:
			if not isinstance(self.stack[-1],type({})):raise ValueError(A%self.parser.CurrentLineNumber)
			self.stack[-1][self.current_key]=value;self.current_key=_A
		elif not self.stack:self.root=value
		else:
			if not isinstance(self.stack[-1],type([])):raise ValueError(A%self.parser.CurrentLineNumber)
			self.stack[-1].append(value)
	def get_data(self):data=''.join(self.data);self.data=[];return data
	def begin_dict(self,attrs):d=self._dict_type();self.add_object(d);self.stack.append(d)
	def end_dict(self):
		if self.current_key:raise ValueError("missing value for key '%s' at line %d"%(self.current_key,self.parser.CurrentLineNumber))
		self.stack.pop()
	def end_key(self):
		if self.current_key or not isinstance(self.stack[-1],type({})):raise ValueError('unexpected key at line %d'%self.parser.CurrentLineNumber)
		self.current_key=self.get_data()
	def begin_array(self,attrs):a=[];self.add_object(a);self.stack.append(a)
	def end_array(self):self.stack.pop()
	def end_true(self):self.add_object(_B)
	def end_false(self):self.add_object(_C)
	def end_integer(self):
		raw=self.get_data()
		if raw.startswith('0x')or raw.startswith('0X'):self.add_object(int(raw,16))
		else:self.add_object(int(raw))
	def end_real(self):self.add_object(float(self.get_data()))
	def end_string(self):self.add_object(self.get_data())
	def end_data(self):self.add_object(_decode_base64(self.get_data()))
	def end_date(self):self.add_object(_date_from_string(self.get_data()))
class _DumbXMLWriter:
	def __init__(self,file,indent_level=0,indent='\t'):self.file=file;self.stack=[];self._indent_level=indent_level;self.indent=indent
	def begin_element(self,element):self.stack.append(element);self.writeln('<%s>'%element);self._indent_level+=1
	def end_element(self,element):assert self._indent_level>0;assert self.stack.pop()==element;self._indent_level-=1;self.writeln('</%s>'%element)
	def simple_element(self,element,value=_A):
		if value is not _A:value=_escape(value);self.writeln('<%s>%s</%s>'%(element,value,element))
		else:self.writeln('<%s/>'%element)
	def writeln(self,line):
		if line:
			if isinstance(line,str):line=line.encode(_E)
			self.file.write(self._indent_level*self.indent);self.file.write(line)
		self.file.write(b'\n')
class _PlistWriter(_DumbXMLWriter):
	def __init__(self,file,indent_level=0,indent=_F,writeHeader=1,sort_keys=_B,skipkeys=_C):
		if writeHeader:file.write(PLISTHEADER)
		_DumbXMLWriter.__init__(self,file,indent_level,indent);self._sort_keys=sort_keys;self._skipkeys=skipkeys
	def write(self,value):self.writeln('<plist version="1.0">');self.write_value(value);self.writeln('</plist>')
	def write_value(self,value):
		if isinstance(value,str):self.simple_element('string',value)
		elif value is _B:self.simple_element('true')
		elif value is _C:self.simple_element('false')
		elif isinstance(value,int):
			if-1<<63<=value<1<<64:self.simple_element('integer','%d'%value)
			else:raise OverflowError(value)
		elif isinstance(value,float):self.simple_element('real',repr(value))
		elif isinstance(value,dict):self.write_dict(value)
		elif isinstance(value,(bytes,bytearray)):self.write_bytes(value)
		elif isinstance(value,datetime.datetime):self.simple_element('date',_date_to_string(value))
		elif isinstance(value,(tuple,list)):self.write_array(value)
		else:raise TypeError('unsupported type: %s'%type(value))
	def write_bytes(self,data):
		A='data';self.begin_element(A);self._indent_level-=1;maxlinelength=max(16,76-len(self.indent.replace(_F,b' '*8)*self._indent_level))
		for line in _encode_base64(data,maxlinelength).split(b'\n'):
			if line:self.writeln(line)
		self._indent_level+=1;self.end_element(A)
	def write_dict(self,d):
		A='dict'
		if d:
			self.begin_element(A)
			if self._sort_keys:items=sorted(d.items())
			else:items=d.items()
			for(key,value)in items:
				if not isinstance(key,str):
					if self._skipkeys:continue
					raise TypeError(_G)
				self.simple_element('key',key);self.write_value(value)
			self.end_element(A)
		else:self.simple_element(A)
	def write_array(self,array):
		A='array'
		if array:
			self.begin_element(A)
			for value in array:self.write_value(value)
			self.end_element(A)
		else:self.simple_element(A)
def _is_fmt_xml(header):
	prefixes=b'<?xml',b'<plist'
	for pfx in prefixes:
		if header.startswith(pfx):return _B
	for(bom,encoding)in((codecs.BOM_UTF8,_E),(codecs.BOM_UTF16_BE,'utf-16-be'),(codecs.BOM_UTF16_LE,'utf-16-le')):
		if not header.startswith(bom):continue
		for start in prefixes:
			prefix=bom+start.decode(_H).encode(encoding)
			if header[:len(prefix)]==prefix:return _B
	return _C
class InvalidFileException(ValueError):
	def __init__(self,message='Invalid file'):ValueError.__init__(self,message)
_BINARY_FORMAT={1:'B',2:'H',4:'L',8:'Q'}
_undefined=object()
class _BinaryPlistParser:
	'\n    Read or write a binary plist file, following the description of the binary\n    format.  Raise InvalidFileException in case of error, otherwise return the\n    root object.\n\n    see also: http://opensource.apple.com/source/CF/CF-744.18/CFBinaryPList.c\n    '
	def __init__(self,dict_type):self._dict_type=dict_type
	def parse(self,fp):
		try:
			self._fp=fp;self._fp.seek(-32,os.SEEK_END);trailer=self._fp.read(32)
			if len(trailer)!=32:raise InvalidFileException()
			offset_size,self._ref_size,num_objects,top_object,offset_table_offset=struct.unpack('>6xBBQQQ',trailer);self._fp.seek(offset_table_offset);self._object_offsets=self._read_ints(num_objects,offset_size);self._objects=[_undefined]*num_objects;return self._read_object(top_object)
		except(OSError,IndexError,struct.error,OverflowError,ValueError):raise InvalidFileException()
	def _get_size(self,tokenL):
		' return the size of the next object.'
		if tokenL==15:m=self._fp.read(1)[0]&3;s=1<<m;f='>'+_BINARY_FORMAT[s];return struct.unpack(f,self._fp.read(s))[0]
		return tokenL
	def _read_ints(self,n,size):
		data=self._fp.read(size*n)
		if size in _BINARY_FORMAT:return struct.unpack(f">{n}{_BINARY_FORMAT[size]}",data)
		else:
			if not size or len(data)!=size*n:raise InvalidFileException()
			return tuple(int.from_bytes(data[i:i+size],_D)for i in range(0,size*n,size))
	def _read_refs(self,n):return self._read_ints(n,self._ref_size)
	def _read_object(self,ref):
		'\n        read the object by reference.\n\n        May recursively read sub-objects (content of an array/dict/set)\n        ';result=self._objects[ref]
		if result is not _undefined:return result
		offset=self._object_offsets[ref];self._fp.seek(offset);token=self._fp.read(1)[0];tokenH,tokenL=token&240,token&15
		if token==0:result=_A
		elif token==8:result=_C
		elif token==9:result=_B
		elif token==15:result=b''
		elif tokenH==16:result=int.from_bytes(self._fp.read(1<<tokenL),_D,signed=tokenL>=3)
		elif token==34:result=struct.unpack('>f',self._fp.read(4))[0]
		elif token==35:result=struct.unpack('>d',self._fp.read(8))[0]
		elif token==51:f=struct.unpack('>d',self._fp.read(8))[0];result=datetime.datetime(2001,1,1)+datetime.timedelta(seconds=f)
		elif tokenH==64:
			s=self._get_size(tokenL);result=self._fp.read(s)
			if len(result)!=s:raise InvalidFileException()
		elif tokenH==80:
			s=self._get_size(tokenL);data=self._fp.read(s)
			if len(data)!=s:raise InvalidFileException()
			result=data.decode(_H)
		elif tokenH==96:
			s=self._get_size(tokenL)*2;data=self._fp.read(s)
			if len(data)!=s:raise InvalidFileException()
			result=data.decode(_J)
		elif tokenH==128:result=UID(int.from_bytes(self._fp.read(1+tokenL),_D))
		elif tokenH==160:s=self._get_size(tokenL);obj_refs=self._read_refs(s);result=[];self._objects[ref]=result;result.extend(self._read_object(x)for x in obj_refs)
		elif tokenH==208:
			s=self._get_size(tokenL);key_refs=self._read_refs(s);obj_refs=self._read_refs(s);result=self._dict_type();self._objects[ref]=result
			try:
				for(k,o)in zip(key_refs,obj_refs):result[self._read_object(k)]=self._read_object(o)
			except TypeError:raise InvalidFileException()
		else:raise InvalidFileException()
		self._objects[ref]=result;return result
def _count_to_size(count):
	if count<1<<8:return 1
	elif count<1<<16:return 2
	elif count<1<<32:return 4
	else:return 8
_scalars=str,int,float,datetime.datetime,bytes
class _BinaryPlistWriter:
	def __init__(self,fp,sort_keys,skipkeys):self._fp=fp;self._sort_keys=sort_keys;self._skipkeys=skipkeys
	def write(self,value):
		self._objlist=[];self._objtable={};self._objidtable={};self._flatten(value);num_objects=len(self._objlist);self._object_offsets=[0]*num_objects;self._ref_size=_count_to_size(num_objects);self._ref_format=_BINARY_FORMAT[self._ref_size];self._fp.write(_K)
		for obj in self._objlist:self._write_object(obj)
		top_object=self._getrefnum(value);offset_table_offset=self._fp.tell();offset_size=_count_to_size(offset_table_offset);offset_format='>'+_BINARY_FORMAT[offset_size]*num_objects;self._fp.write(struct.pack(offset_format,*self._object_offsets));sort_version=0;trailer=sort_version,offset_size,self._ref_size,num_objects,top_object,offset_table_offset;self._fp.write(struct.pack('>5xBBBQQQ',*trailer))
	def _flatten(self,value):
		if isinstance(value,_scalars):
			if(type(value),value)in self._objtable:return
		elif id(value)in self._objidtable:return
		refnum=len(self._objlist);self._objlist.append(value)
		if isinstance(value,_scalars):self._objtable[type(value),value]=refnum
		else:self._objidtable[id(value)]=refnum
		if isinstance(value,dict):
			keys=[];values=[];items=value.items()
			if self._sort_keys:items=sorted(items)
			for(k,v)in items:
				if not isinstance(k,str):
					if self._skipkeys:continue
					raise TypeError(_G)
				keys.append(k);values.append(v)
			for o in itertools.chain(keys,values):self._flatten(o)
		elif isinstance(value,(list,tuple)):
			for o in value:self._flatten(o)
	def _getrefnum(self,value):
		if isinstance(value,_scalars):return self._objtable[type(value),value]
		else:return self._objidtable[id(value)]
	def _write_size(self,token,size):
		if size<15:self._fp.write(struct.pack('>B',token|size))
		elif size<1<<8:self._fp.write(struct.pack('>BBB',token|15,16,size))
		elif size<1<<16:self._fp.write(struct.pack('>BBH',token|15,17,size))
		elif size<1<<32:self._fp.write(struct.pack('>BBL',token|15,18,size))
		else:self._fp.write(struct.pack('>BBQ',token|15,19,size))
	def _write_object(self,value):
		E='>Bd';D='>BQ';C='>BL';B='>BH';A='>BB';ref=self._getrefnum(value);self._object_offsets[ref]=self._fp.tell()
		if value is _A:self._fp.write(b'\x00')
		elif value is _C:self._fp.write(b'\x08')
		elif value is _B:self._fp.write(_F)
		elif isinstance(value,int):
			if value<0:
				try:self._fp.write(struct.pack('>Bq',19,value))
				except struct.error:raise OverflowError(value)from _A
			elif value<1<<8:self._fp.write(struct.pack(A,16,value))
			elif value<1<<16:self._fp.write(struct.pack(B,17,value))
			elif value<1<<32:self._fp.write(struct.pack(C,18,value))
			elif value<1<<63:self._fp.write(struct.pack(D,19,value))
			elif value<1<<64:self._fp.write(b'\x14'+value.to_bytes(16,_D,signed=_B))
			else:raise OverflowError(value)
		elif isinstance(value,float):self._fp.write(struct.pack(E,35,value))
		elif isinstance(value,datetime.datetime):f=(value-datetime.datetime(2001,1,1)).total_seconds();self._fp.write(struct.pack(E,51,f))
		elif isinstance(value,(bytes,bytearray)):self._write_size(64,len(value));self._fp.write(value)
		elif isinstance(value,str):
			try:t=value.encode(_H);self._write_size(80,len(value))
			except UnicodeEncodeError:t=value.encode(_J);self._write_size(96,len(t)//2)
			self._fp.write(t)
		elif isinstance(value,UID):
			if value.data<0:raise ValueError(_I)
			elif value.data<1<<8:self._fp.write(struct.pack(A,128,value))
			elif value.data<1<<16:self._fp.write(struct.pack(B,129,value))
			elif value.data<1<<32:self._fp.write(struct.pack(C,131,value))
			elif value.data<1<<64:self._fp.write(struct.pack(D,135,value))
			else:raise OverflowError(value)
		elif isinstance(value,(list,tuple)):refs=[self._getrefnum(o)for o in value];s=len(refs);self._write_size(160,s);self._fp.write(struct.pack('>'+self._ref_format*s,*refs))
		elif isinstance(value,dict):
			keyRefs,valRefs=[],[]
			if self._sort_keys:rootItems=sorted(value.items())
			else:rootItems=value.items()
			for(k,v)in rootItems:
				if not isinstance(k,str):
					if self._skipkeys:continue
					raise TypeError(_G)
				keyRefs.append(self._getrefnum(k));valRefs.append(self._getrefnum(v))
			s=len(keyRefs);self._write_size(208,s);self._fp.write(struct.pack('>'+self._ref_format*s,*keyRefs));self._fp.write(struct.pack('>'+self._ref_format*s,*valRefs))
		else:raise TypeError(value)
def _is_fmt_binary(header):return header[:8]==_K
_FORMATS={FMT_XML:dict(detect=_is_fmt_xml,parser=_PlistParser,writer=_PlistWriter),FMT_BINARY:dict(detect=_is_fmt_binary,parser=_BinaryPlistParser,writer=_BinaryPlistWriter)}
def load(fp,*,fmt=_A,dict_type=dict):
	"Read a .plist file. 'fp' should be a readable and binary file object.\n    Return the unpacked root object (which usually is a dictionary).\n    ";A='parser'
	if fmt is _A:
		header=fp.read(32);fp.seek(0)
		for info in _FORMATS.values():
			if info['detect'](header):P=info[A];break
		else:raise InvalidFileException()
	else:P=_FORMATS[fmt][A]
	p=P(dict_type=dict_type);return p.parse(fp)
def loads(value,*,fmt=_A,dict_type=dict):'Read a .plist file from a bytes object.\n    Return the unpacked root object (which usually is a dictionary).\n    ';fp=BytesIO(value);return load(fp,fmt=fmt,dict_type=dict_type)
def dump(value,fp,*,fmt=FMT_XML,sort_keys=_B,skipkeys=_C):
	"Write 'value' to a .plist file. 'fp' should be a writable,\n    binary file object.\n    "
	if fmt not in _FORMATS:raise ValueError('Unsupported format: %r'%(fmt,))
	writer=_FORMATS[fmt]['writer'](fp,sort_keys=sort_keys,skipkeys=skipkeys);writer.write(value)
def dumps(value,*,fmt=FMT_XML,skipkeys=_C,sort_keys=_B):'Return a bytes object with the contents for a .plist file.\n    ';fp=BytesIO();dump(value,fp,fmt=fmt,skipkeys=skipkeys,sort_keys=sort_keys);return fp.getvalue()