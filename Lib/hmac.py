'HMAC (Keyed-Hashing for Message Authentication) module.\n\nImplements the HMAC algorithm as described by RFC 2104.\n'
_B='block_size'
_A=None
import warnings as _warnings
try:import _hashlib as _hashopenssl
except ImportError:_hashopenssl=_A;_functype=_A;from _operator import _compare_digest as compare_digest
else:compare_digest=_hashopenssl.compare_digest;_functype=type(_hashopenssl.openssl_sha256)
import hashlib as _hashlib
trans_5C=bytes(A^92 for A in range(256))
trans_36=bytes(A^54 for A in range(256))
digest_size=_A
class HMAC:
	'RFC 2104 HMAC class.  Also complies with RFC 4231.\n\n    This supports the API for Cryptographic Hash Functions (PEP 247).\n    ';blocksize=64;__slots__='_hmac','_inner','_outer',_B,'digest_size'
	def __init__(C,key,msg=_A,digestmod=''):
		'Create a new HMAC object.\n\n        key: bytes or buffer, key for the keyed hash object.\n        msg: bytes or buffer, Initial input for the hash or None.\n        digestmod: A hash name suitable for hashlib.new(). *OR*\n                   A hashlib constructor returning a new hash object. *OR*\n                   A module supporting PEP 247.\n\n                   Required as of 3.8, despite its position after the optional\n                   msg argument.  Passing it as a keyword argument is\n                   recommended, though not required for legacy API reasons.\n        ';D=msg;A=digestmod;B=key
		if not isinstance(B,(bytes,bytearray)):raise TypeError('key: expected bytes or bytearray, but got %r'%type(B).__name__)
		if not A:raise TypeError("Missing required parameter 'digestmod'.")
		if _hashopenssl and isinstance(A,(str,_functype)):
			try:C._init_hmac(B,D,A)
			except _hashopenssl.UnsupportedDigestmodError:C._init_old(B,D,A)
		else:C._init_old(B,D,A)
	def _init_hmac(A,key,msg,digestmod):A._hmac=_hashopenssl.hmac_new(key,msg,digestmod=digestmod);A.digest_size=A._hmac.digest_size;A.block_size=A._hmac.block_size
	def _init_old(A,key,msg,digestmod):
		D=digestmod;B=key
		if callable(D):E=D
		elif isinstance(D,str):E=lambda d=b'':_hashlib.new(D,d)
		else:E=lambda d=b'':D.new(d)
		A._hmac=_A;A._outer=E();A._inner=E();A.digest_size=A._inner.digest_size
		if hasattr(A._inner,_B):
			C=A._inner.block_size
			if C<16:_warnings.warn('block_size of %d seems too small; using our default of %d.'%(C,A.blocksize),RuntimeWarning,2);C=A.blocksize
		else:_warnings.warn('No block_size attribute on given digest object; Assuming %d.'%A.blocksize,RuntimeWarning,2);C=A.blocksize
		if len(B)>C:B=E(B).digest()
		A.block_size=C;B=B.ljust(C,b'\x00');A._outer.update(B.translate(trans_5C));A._inner.update(B.translate(trans_36))
		if msg is not _A:A.update(msg)
	@property
	def name(self):
		A=self
		if A._hmac:return A._hmac.name
		else:return f"hmac-{A._inner.name}"
	def update(A,msg):'Feed data from msg into this hashing object.';B=A._hmac or A._inner;B.update(msg)
	def copy(B):
		"Return a separate copy of this hashing object.\n\n        An update to this copy won't affect the original object.\n        ";A=B.__class__.__new__(B.__class__);A.digest_size=B.digest_size
		if B._hmac:A._hmac=B._hmac.copy();A._inner=A._outer=_A
		else:A._hmac=_A;A._inner=B._inner.copy();A._outer=B._outer.copy()
		return A
	def _current(A):
		'Return a hash object for the current state.\n\n        To be used only internally with digest() and hexdigest().\n        '
		if A._hmac:return A._hmac
		else:B=A._outer.copy();B.update(A._inner.digest());return B
	def digest(A):'Return the hash value of this hashing object.\n\n        This returns the hmac value as bytes.  The object is\n        not altered in any way by this function; you can continue\n        updating the object after calling this function.\n        ';B=A._current();return B.digest()
	def hexdigest(A):'Like digest(), but returns a string of hexadecimal digits instead.\n        ';B=A._current();return B.hexdigest()
def new(key,msg=_A,digestmod=''):'Create a new hashing object and return it.\n\n    key: bytes or buffer, The starting key for the hash.\n    msg: bytes or buffer, Initial input for the hash, or None.\n    digestmod: A hash name suitable for hashlib.new(). *OR*\n               A hashlib constructor returning a new hash object. *OR*\n               A module supporting PEP 247.\n\n               Required as of 3.8, despite its position after the optional\n               msg argument.  Passing it as a keyword argument is\n               recommended, though not required for legacy API reasons.\n\n    You can now feed arbitrary bytes into the object using its update()\n    method, and can ask for the hash value at any time by calling its digest()\n    or hexdigest() methods.\n    ';return HMAC(key,msg,digestmod)
def digest(key,msg,digest):
	'Fast inline implementation of HMAC.\n\n    key: bytes or buffer, The key for the keyed hash object.\n    msg: bytes or buffer, Input message.\n    digest: A hash name suitable for hashlib.new() for best performance. *OR*\n            A hashlib constructor returning a new hash object. *OR*\n            A module supporting PEP 247.\n    ';B=digest;A=key
	if _hashopenssl is not _A and isinstance(B,(str,_functype)):
		try:return _hashopenssl.hmac_digest(A,msg,B)
		except _hashopenssl.UnsupportedDigestmodError:pass
	if callable(B):C=B
	elif isinstance(B,str):C=lambda d=b'':_hashlib.new(B,d)
	else:C=lambda d=b'':B.new(d)
	D=C();E=C();F=getattr(D,_B,64)
	if len(A)>F:A=C(A).digest()
	A=A+b'\x00'*(F-len(A));D.update(A.translate(trans_36));E.update(A.translate(trans_5C));D.update(msg);E.update(D.digest());return E.digest()