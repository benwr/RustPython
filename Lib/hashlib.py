_O='shake_256'
_N='shake_128'
_M='sha3_512'
_L='sha3_384'
_K='sha3_256'
_J='sha3_224'
_I='sha512'
_H='sha384'
_G='sha256'
_F='sha224'
_E='sha1'
_D='md5'
_C='blake2s'
_B='blake2b'
_A=None
__doc__='hashlib module - A common interface to many hash functions.\n\nnew(name, data=b\'\', **kwargs) - returns a new hash object implementing the\n                                given hash function; initializing the hash\n                                using the given binary data.\n\nNamed constructor functions are also available, these are faster\nthan using new(name):\n\nmd5(), sha1(), sha224(), sha256(), sha384(), sha512(), blake2b(), blake2s(),\nsha3_224, sha3_256, sha3_384, sha3_512, shake_128, and shake_256.\n\nMore algorithms may be available on your platform but the above are guaranteed\nto exist.  See the algorithms_guaranteed and algorithms_available attributes\nto find out what algorithm names can be passed to new().\n\nNOTE: If you want the adler32 or crc32 hash functions they are available in\nthe zlib module.\n\nChoose your hash function wisely.  Some have known collision weaknesses.\nsha384 and sha512 will be slow on 32 bit platforms.\n\nHash objects have these methods:\n - update(data): Update the hash object with the bytes in data. Repeated calls\n                 are equivalent to a single call with the concatenation of all\n                 the arguments.\n - digest():     Return the digest of the bytes passed to the update() method\n                 so far as a bytes object.\n - hexdigest():  Like digest() except the digest is returned as a string\n                 of double length, containing only hexadecimal digits.\n - copy():       Return a copy (clone) of the hash object. This can be used to\n                 efficiently compute the digests of datas that share a common\n                 initial substring.\n\nFor example, to obtain the digest of the byte string \'Nobody inspects the\nspammish repetition\':\n\n    >>> import hashlib\n    >>> m = hashlib.md5()\n    >>> m.update(b"Nobody inspects")\n    >>> m.update(b" the spammish repetition")\n    >>> m.digest()\n    b\'\\xbbd\\x9c\\x83\\xdd\\x1e\\xa5\\xc9\\xd9\\xde\\xc9\\xa1\\x8d\\xf0\\xff\\xe9\'\n\nMore condensed:\n\n    >>> hashlib.sha224(b"Nobody inspects the spammish repetition").hexdigest()\n    \'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2\'\n\n'
__always_supported=_D,_E,_F,_G,_H,_I,_B,_C,_J,_K,_L,_M,_N,_O
algorithms_guaranteed=set(__always_supported)
algorithms_available=set(__always_supported)
__all__=__always_supported+('new','algorithms_guaranteed','algorithms_available','pbkdf2_hmac','file_digest')
__builtin_constructor_cache={}
__block_openssl_constructor={_B,_C}
def __get_builtin_constructor(name):
	F='SHA384';E='SHA512';D='SHA224';C='SHA256';B='MD5';A='SHA1';cache=__builtin_constructor_cache;constructor=cache.get(name)
	if constructor is not _A:return constructor
	try:
		if name in{A,_E}:import _sha1;cache[A]=cache[_E]=_sha1.sha1
		elif name in{B,_D}:import _md5;cache[B]=cache[_D]=_md5.md5
		elif name in{C,_G,D,_F}:import _sha256;cache[D]=cache[_F]=_sha256.sha224;cache[C]=cache[_G]=_sha256.sha256
		elif name in{E,_I,F,_H}:import _sha512;cache[F]=cache[_H]=_sha512.sha384;cache[E]=cache[_I]=_sha512.sha512
		elif name in{_B,_C}:import _blake2;cache[_B]=_blake2.blake2b;cache[_C]=_blake2.blake2s
		elif name in{_J,_K,_L,_M}:import _sha3;cache[_J]=_sha3.sha3_224;cache[_K]=_sha3.sha3_256;cache[_L]=_sha3.sha3_384;cache[_M]=_sha3.sha3_512
		elif name in{_N,_O}:import _sha3;cache[_N]=_sha3.shake_128;cache[_O]=_sha3.shake_256
	except ImportError:pass
	constructor=cache.get(name)
	if constructor is not _A:return constructor
	raise ValueError('unsupported hash type '+name)
def __get_openssl_constructor(name):
	if name in __block_openssl_constructor:return __get_builtin_constructor(name)
	try:f=getattr(_hashlib,'openssl_'+name);f(usedforsecurity=False);return f
	except(AttributeError,ValueError):return __get_builtin_constructor(name)
def __py_new(name,data=b'',**kwargs):"new(name, data=b'', **kwargs) - Return a new hashing object using the\n    named algorithm; optionally initialized with data (which must be\n    a bytes-like object).\n    ";return __get_builtin_constructor(name)(data,**kwargs)
def __hash_new(name,data=b'',**kwargs):
	"new(name, data=b'') - Return a new hashing object using the named algorithm;\n    optionally initialized with data (which must be a bytes-like object).\n    "
	if name in __block_openssl_constructor:return __get_builtin_constructor(name)(data,**kwargs)
	try:return _hashlib.new(name,data,**kwargs)
	except ValueError:return __get_builtin_constructor(name)(data)
try:import _hashlib;new=__hash_new;__get_hash=__get_openssl_constructor;'algorithms_available = algorithms_available.union(\n            _hashlib.openssl_md_meth_names)'
except ImportError:_hashlib=_A;new=__py_new;__get_hash=__get_builtin_constructor
try:from _hashlib import pbkdf2_hmac
except ImportError:
	from warnings import warn as _warn;_trans_5C=bytes(x^92 for x in range(256));_trans_36=bytes(x^54 for x in range(256))
	def pbkdf2_hmac(hash_name,password,salt,iterations,dklen=_A):
		"Password based key derivation function 2 (PKCS #5 v2.0)\n\n        This Python implementations based on the hmac module about as fast\n        as OpenSSL's PKCS5_PBKDF2_HMAC for short passwords and much faster\n        for long passwords.\n        ";_warn('Python implementation of pbkdf2_hmac() is deprecated.',category=DeprecationWarning,stacklevel=2)
		if not isinstance(hash_name,str):raise TypeError(hash_name)
		if not isinstance(password,(bytes,bytearray)):password=bytes(memoryview(password))
		if not isinstance(salt,(bytes,bytearray)):salt=bytes(memoryview(salt))
		inner=new(hash_name);outer=new(hash_name);blocksize=getattr(inner,'block_size',64)
		if len(password)>blocksize:password=new(hash_name,password).digest()
		password=password+b'\x00'*(blocksize-len(password));inner.update(password.translate(_trans_36));outer.update(password.translate(_trans_5C))
		def prf(msg,inner=inner,outer=outer):icpy=inner.copy();ocpy=outer.copy();icpy.update(msg);ocpy.update(icpy.digest());return ocpy.digest()
		if iterations<1:raise ValueError(iterations)
		if dklen is _A:dklen=outer.digest_size
		if dklen<1:raise ValueError(dklen)
		dkey=b'';loop=1;from_bytes=int.from_bytes
		while len(dkey)<dklen:
			prev=prf(salt+loop.to_bytes(4));rkey=from_bytes(prev)
			for i in range(iterations-1):prev=prf(prev);rkey^=from_bytes(prev)
			loop+=1;dkey+=rkey.to_bytes(inner.digest_size)
		return dkey[:dklen]
try:from _hashlib import scrypt
except ImportError:pass
def file_digest(fileobj,digest,*,_bufsize=2**18):
	"Hash the contents of a file-like object. Returns a digest object.\n\n    *fileobj* must be a file-like object opened for reading in binary mode.\n    It accepts file objects from open(), io.BytesIO(), and SocketIO objects.\n    The function may bypass Python's I/O and use the file descriptor *fileno*\n    directly.\n\n    *digest* must either be a hash algorithm name as a *str*, a hash\n    constructor, or a callable that returns a hash object.\n    "
	if isinstance(digest,str):digestobj=new(digest)
	else:digestobj=digest()
	if hasattr(fileobj,'getbuffer'):digestobj.update(fileobj.getbuffer());return digestobj
	if not(hasattr(fileobj,'readinto')and hasattr(fileobj,'readable')and fileobj.readable()):raise ValueError(f"'{fileobj!r}' is not a file-like object in binary reading mode.")
	buf=bytearray(_bufsize);view=memoryview(buf)
	while True:
		size=fileobj.readinto(buf)
		if size==0:break
		digestobj.update(view[:size])
	return digestobj
for __func_name in __always_supported:
	try:globals()[__func_name]=__get_hash(__func_name)
	except ValueError:import logging;logging.exception('code for hash %s was not found.',__func_name)
del __always_supported,__func_name,__get_hash
del __py_new,__hash_new,__get_openssl_constructor