'Implements (a subset of) Sun XDR -- eXternal Data Representation.\n\nSee: RFC 1014\n\n'
_A='fstring size must be nonnegative'
import struct
from io import BytesIO
from functools import wraps
__all__=['Error','Packer','Unpacker','ConversionError']
class Error(Exception):
	'Exception class for this module. Use:\n\n    except xdrlib.Error as var:\n        # var has the Error instance for the exception\n\n    Public ivars:\n        msg -- contains the message\n\n    '
	def __init__(A,msg):A.msg=msg
	def __repr__(A):return repr(A.msg)
	def __str__(A):return str(A.msg)
class ConversionError(Error):0
def raise_conversion_error(function):
	' Wrap any raised struct.errors in a ConversionError. ';A=function
	@wraps(A)
	def B(self,value):
		try:return A(self,value)
		except struct.error as B:raise ConversionError(B.args[0])from None
	return B
class Packer:
	'Pack various data representations into a buffer.'
	def __init__(A):A.reset()
	def reset(A):A.__buf=BytesIO()
	def get_buffer(A):return A.__buf.getvalue()
	get_buf=get_buffer
	@raise_conversion_error
	def pack_uint(self,x):self.__buf.write(struct.pack('>L',x))
	@raise_conversion_error
	def pack_int(self,x):self.__buf.write(struct.pack('>l',x))
	pack_enum=pack_int
	def pack_bool(A,x):
		if x:A.__buf.write(b'\x00\x00\x00\x01')
		else:A.__buf.write(b'\x00\x00\x00\x00')
	def pack_uhyper(B,x):
		try:B.pack_uint(x>>32&4294967295)
		except(TypeError,struct.error)as A:raise ConversionError(A.args[0])from None
		try:B.pack_uint(x&4294967295)
		except(TypeError,struct.error)as A:raise ConversionError(A.args[0])from None
	pack_hyper=pack_uhyper
	@raise_conversion_error
	def pack_float(self,x):self.__buf.write(struct.pack('>f',x))
	@raise_conversion_error
	def pack_double(self,x):self.__buf.write(struct.pack('>d',x))
	def pack_fstring(B,n,s):
		if n<0:raise ValueError(_A)
		A=s[:n];n=(n+3)//4*4;A=A+(n-len(A))*b'\x00';B.__buf.write(A)
	pack_fopaque=pack_fstring
	def pack_string(A,s):B=len(s);A.pack_uint(B);A.pack_fstring(B,s)
	pack_opaque=pack_string;pack_bytes=pack_string
	def pack_list(A,list,pack_item):
		for B in list:A.pack_uint(1);pack_item(B)
		A.pack_uint(0)
	def pack_farray(B,n,list,pack_item):
		if len(list)!=n:raise ValueError('wrong array size')
		for A in list:pack_item(A)
	def pack_array(A,list,pack_item):B=len(list);A.pack_uint(B);A.pack_farray(B,list,pack_item)
class Unpacker:
	'Unpacks various data representations from the given buffer.'
	def __init__(A,data):A.reset(data)
	def reset(A,data):A.__buf=data;A.__pos=0
	def get_position(A):return A.__pos
	def set_position(A,position):A.__pos=position
	def get_buffer(A):return A.__buf
	def done(A):
		if A.__pos<len(A.__buf):raise Error('unextracted data remains')
	def unpack_uint(A):
		B=A.__pos;A.__pos=D=B+4;C=A.__buf[B:D]
		if len(C)<4:raise EOFError
		return struct.unpack('>L',C)[0]
	def unpack_int(A):
		B=A.__pos;A.__pos=D=B+4;C=A.__buf[B:D]
		if len(C)<4:raise EOFError
		return struct.unpack('>l',C)[0]
	unpack_enum=unpack_int
	def unpack_bool(A):return bool(A.unpack_int())
	def unpack_uhyper(A):B=A.unpack_uint();C=A.unpack_uint();return int(B)<<32|C
	def unpack_hyper(B):
		A=B.unpack_uhyper()
		if A>=0x8000000000000000:A=A-0x10000000000000000
		return A
	def unpack_float(A):
		B=A.__pos;A.__pos=D=B+4;C=A.__buf[B:D]
		if len(C)<4:raise EOFError
		return struct.unpack('>f',C)[0]
	def unpack_double(A):
		B=A.__pos;A.__pos=D=B+8;C=A.__buf[B:D]
		if len(C)<8:raise EOFError
		return struct.unpack('>d',C)[0]
	def unpack_fstring(A,n):
		if n<0:raise ValueError(_A)
		B=A.__pos;C=B+(n+3)//4*4
		if C>len(A.__buf):raise EOFError
		A.__pos=C;return A.__buf[B:B+n]
	unpack_fopaque=unpack_fstring
	def unpack_string(A):B=A.unpack_uint();return A.unpack_fstring(B)
	unpack_opaque=unpack_string;unpack_bytes=unpack_string
	def unpack_list(B,unpack_item):
		list=[]
		while 1:
			A=B.unpack_uint()
			if A==0:break
			if A!=1:raise ConversionError('0 or 1 expected, got %r'%(A,))
			C=unpack_item();list.append(C)
		return list
	def unpack_farray(A,n,unpack_item):
		list=[]
		for B in range(n):list.append(unpack_item())
		return list
	def unpack_array(A,unpack_item):B=A.unpack_uint();return A.unpack_farray(B,unpack_item)