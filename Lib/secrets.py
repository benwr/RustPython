'Generate cryptographically strong pseudo-random numbers suitable for\nmanaging secrets such as account authentication, tokens, and similar.\n\nSee PEP 506 for more information.\nhttps://www.python.org/dev/peps/pep-0506/\n\n'
_A=None
__all__=['choice','randbelow','randbits','SystemRandom','token_bytes','token_hex','token_urlsafe','compare_digest']
import base64,binascii
from hmac import compare_digest
from random import SystemRandom
_sysrand=SystemRandom()
randbits=_sysrand.getrandbits
choice=_sysrand.choice
def randbelow(exclusive_upper_bound):
	'Return a random int in the range [0, n).';A=exclusive_upper_bound
	if A<=0:raise ValueError('Upper bound must be positive.')
	return _sysrand._randbelow(A)
DEFAULT_ENTROPY=32
def token_bytes(nbytes=_A):
	"Return a random byte string containing *nbytes* bytes.\n\n    If *nbytes* is ``None`` or not supplied, a reasonable\n    default is used.\n\n    >>> token_bytes(16)  #doctest:+SKIP\n    b'\\xebr\\x17D*t\\xae\\xd4\\xe3S\\xb6\\xe2\\xebP1\\x8b'\n\n    ";A=nbytes
	if A is _A:A=DEFAULT_ENTROPY
	return _sysrand.randbytes(A)
def token_hex(nbytes=_A):"Return a random text string, in hexadecimal.\n\n    The string has *nbytes* random bytes, each byte converted to two\n    hex digits.  If *nbytes* is ``None`` or not supplied, a reasonable\n    default is used.\n\n    >>> token_hex(16)  #doctest:+SKIP\n    'f9bf78b9a18ce6d46a0cd2b0b86df9da'\n\n    ";return binascii.hexlify(token_bytes(nbytes)).decode('ascii')
def token_urlsafe(nbytes=_A):"Return a random URL-safe text string, in Base64 encoding.\n\n    The string has *nbytes* random bytes.  If *nbytes* is ``None``\n    or not supplied, a reasonable default is used.\n\n    >>> token_urlsafe(16)  #doctest:+SKIP\n    'Drmhze6EPcv0fN_81Bj-nA'\n\n    ";A=token_bytes(nbytes);return base64.urlsafe_b64encode(A).rstrip(b'=').decode('ascii')