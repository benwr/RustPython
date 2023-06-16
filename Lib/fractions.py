'Fraction, infinite-precision, real numbers.'
_B=None
_A=False
from decimal import Decimal
import math,numbers,operator,re,sys
__all__=['Fraction','gcd']
def gcd(a,b):
	'Calculate the Greatest Common Divisor of a and b.\n\n    Unless b==0, the result will have the same sign as b (so that when\n    b is divided by it, the result comes out positive).\n    ';import warnings as A;A.warn('fractions.gcd() is deprecated. Use math.gcd() instead.',DeprecationWarning,2)
	if type(a)is int is type(b):
		if(b or a)<0:return-math.gcd(a,b)
		return math.gcd(a,b)
	return _gcd(a,b)
def _gcd(a,b):
	while b:a,b=b,a%b
	return a
_PyHASH_MODULUS=sys.hash_info.modulus
_PyHASH_INF=sys.hash_info.inf
_RATIONAL_FORMAT=re.compile('\n    \\A\\s*                      # optional whitespace at the start, then\n    (?P<sign>[-+]?)            # an optional sign, then\n    (?=\\d|\\.\\d)                # lookahead for digit or .digit\n    (?P<num>\\d*)               # numerator (possibly empty)\n    (?:                        # followed by\n       (?:/(?P<denom>\\d+))?    # an optional denominator\n    |                          # or\n       (?:\\.(?P<decimal>\\d*))? # an optional fractional part\n       (?:E(?P<exp>[-+]?\\d+))? # and optional exponent\n    )\n    \\s*\\Z                      # and optional whitespace to finish\n',re.VERBOSE|re.IGNORECASE)
class Fraction(numbers.Rational):
	"This class implements rational numbers.\n\n    In the two-argument form of the constructor, Fraction(8, 6) will\n    produce a rational number equivalent to 4/3. Both arguments must\n    be Rational. The numerator defaults to 0 and the denominator\n    defaults to 1 so that Fraction(3) == 3 and Fraction() == 0.\n\n    Fractions can also be constructed from:\n\n      - numeric strings similar to those accepted by the\n        float constructor (for example, '-2.3' or '1e10')\n\n      - strings of the form '123/456'\n\n      - float and Decimal instances\n\n      - other Rational instances (including integers)\n\n    ";__slots__='_numerator','_denominator'
	def __new__(H,numerator=0,denominator=_B,*,_normalize=True):
		"Constructs a Rational.\n\n        Takes a string like '3/2' or '1.5', another Rational instance, a\n        numerator/denominator pair, or a float.\n\n        Examples\n        --------\n\n        >>> Fraction(10, -8)\n        Fraction(-5, 4)\n        >>> Fraction(Fraction(1, 7), 5)\n        Fraction(1, 35)\n        >>> Fraction(Fraction(1, 7), Fraction(2, 3))\n        Fraction(3, 14)\n        >>> Fraction('314')\n        Fraction(314, 1)\n        >>> Fraction('-35/4')\n        Fraction(-35, 4)\n        >>> Fraction('3.1415') # conversion from numeric string\n        Fraction(6283, 2000)\n        >>> Fraction('-47e-2') # string may include a decimal exponent\n        Fraction(-47, 100)\n        >>> Fraction(1.47)  # direct construction from float (exact conversion)\n        Fraction(6620291452234629, 4503599627370496)\n        >>> Fraction(2.25)\n        Fraction(9, 4)\n        >>> Fraction(Decimal('1.47'))\n        Fraction(147, 100)\n\n        ";B=denominator;A=numerator;C=super(Fraction,H).__new__(H)
		if B is _B:
			if type(A)is int:C._numerator=A;C._denominator=1;return C
			elif isinstance(A,numbers.Rational):C._numerator=A.numerator;C._denominator=A.denominator;return C
			elif isinstance(A,(float,Decimal)):C._numerator,C._denominator=A.as_integer_ratio();return C
			elif isinstance(A,str):
				D=_RATIONAL_FORMAT.match(A)
				if D is _B:raise ValueError('Invalid literal for Fraction: %r'%A)
				A=int(D.group('num')or'0');I=D.group('denom')
				if I:B=int(I)
				else:
					B=1;G=D.group('decimal')
					if G:J=10**len(G);A=A*J+int(G);B*=J
					E=D.group('exp')
					if E:
						E=int(E)
						if E>=0:A*=10**E
						else:B*=10**-E
				if D.group('sign')=='-':A=-A
			else:raise TypeError('argument should be a string or a Rational instance')
		elif type(A)is int is type(B):0
		elif isinstance(A,numbers.Rational)and isinstance(B,numbers.Rational):A,B=A.numerator*B.denominator,B.numerator*A.denominator
		else:raise TypeError('both arguments should be Rational instances')
		if B==0:raise ZeroDivisionError('Fraction(%s, 0)'%A)
		if _normalize:
			if type(A)is int is type(B):
				F=math.gcd(A,B)
				if B<0:F=-F
			else:F=_gcd(A,B)
			A//=F;B//=F
		C._numerator=A;C._denominator=B;return C
	@classmethod
	def from_float(A,f):
		'Converts a finite float to a rational number, exactly.\n\n        Beware that Fraction.from_float(0.3) != Fraction(3, 10).\n\n        '
		if isinstance(f,numbers.Integral):return A(f)
		elif not isinstance(f,float):raise TypeError('%s.from_float() only takes floats, not %r (%s)'%(A.__name__,f,type(f).__name__))
		return A(*f.as_integer_ratio())
	@classmethod
	def from_decimal(B,dec):
		'Converts a finite Decimal instance to a rational number, exactly.';A=dec;from decimal import Decimal as C
		if isinstance(A,numbers.Integral):A=C(int(A))
		elif not isinstance(A,C):raise TypeError('%s.from_decimal() only takes Decimals, not %r (%s)'%(B.__name__,A,type(A).__name__))
		return B(*A.as_integer_ratio())
	def as_integer_ratio(A):'Return the integer ratio as a tuple.\n\n        Return a tuple of two integers, whose ratio is equal to the\n        Fraction and with a positive denominator.\n        ';return A._numerator,A._denominator
	def limit_denominator(A,max_denominator=1000000):
		"Closest Fraction to self with denominator at most max_denominator.\n\n        >>> Fraction('3.141592653589793').limit_denominator(10)\n        Fraction(22, 7)\n        >>> Fraction('3.141592653589793').limit_denominator(100)\n        Fraction(311, 99)\n        >>> Fraction(4321, 8765).limit_denominator(10000)\n        Fraction(4321, 8765)\n\n        ";D=max_denominator
		if D<1:raise ValueError('max_denominator should be at least 1')
		if A._denominator<=D:return Fraction(A)
		G,E,C,B=0,1,1,0;H,F=A._numerator,A._denominator
		while True:
			I=H//F;J=E+I*B
			if J>D:break
			G,E,C,B=C,B,G+I*C,J;H,F=F,H-I*F
		K=(D-E)//B;L=Fraction(G+K*C,E+K*B);M=Fraction(C,B)
		if abs(M-A)<=abs(L-A):return M
		else:return L
	@property
	def numerator(a):return a._numerator
	@property
	def denominator(a):return a._denominator
	def __repr__(A):'repr(self)';return'%s(%s, %s)'%(A.__class__.__name__,A._numerator,A._denominator)
	def __str__(A):
		'str(self)'
		if A._denominator==1:return str(A._numerator)
		else:return'%s/%s'%(A._numerator,A._denominator)
	def _operator_fallbacks(B,fallback_operator):
		'Generates forward and reverse operators given a purely-rational\n        operator and a function from the operator module.\n\n        Use this like:\n        __op__, __rop__ = _operator_fallbacks(just_rational_op, operator.op)\n\n        In general, we want to implement the arithmetic operations so\n        that mixed-mode operations either call an implementation whose\n        author knew about the types of both arguments, or convert both\n        to the nearest built in type and do the operation there. In\n        Fraction, that means that we define __add__ and __radd__ as:\n\n            def __add__(self, other):\n                # Both types have numerators/denominator attributes,\n                # so do the operation directly\n                if isinstance(other, (int, Fraction)):\n                    return Fraction(self.numerator * other.denominator +\n                                    other.numerator * self.denominator,\n                                    self.denominator * other.denominator)\n                # float and complex don\'t have those operations, but we\n                # know about those types, so special case them.\n                elif isinstance(other, float):\n                    return float(self) + other\n                elif isinstance(other, complex):\n                    return complex(self) + other\n                # Let the other type take over.\n                return NotImplemented\n\n            def __radd__(self, other):\n                # radd handles more types than add because there\'s\n                # nothing left to fall back to.\n                if isinstance(other, numbers.Rational):\n                    return Fraction(self.numerator * other.denominator +\n                                    other.numerator * self.denominator,\n                                    self.denominator * other.denominator)\n                elif isinstance(other, Real):\n                    return float(other) + float(self)\n                elif isinstance(other, Complex):\n                    return complex(other) + complex(self)\n                return NotImplemented\n\n\n        There are 5 different cases for a mixed-type addition on\n        Fraction. I\'ll refer to all of the above code that doesn\'t\n        refer to Fraction, float, or complex as "boilerplate". \'r\'\n        will be an instance of Fraction, which is a subtype of\n        Rational (r : Fraction <: Rational), and b : B <:\n        Complex. The first three involve \'r + b\':\n\n            1. If B <: Fraction, int, float, or complex, we handle\n               that specially, and all is well.\n            2. If Fraction falls back to the boilerplate code, and it\n               were to return a value from __add__, we\'d miss the\n               possibility that B defines a more intelligent __radd__,\n               so the boilerplate should return NotImplemented from\n               __add__. In particular, we don\'t handle Rational\n               here, even though we could get an exact answer, in case\n               the other type wants to do something special.\n            3. If B <: Fraction, Python tries B.__radd__ before\n               Fraction.__add__. This is ok, because it was\n               implemented with knowledge of Fraction, so it can\n               handle those instances before delegating to Real or\n               Complex.\n\n        The next two situations describe \'b + r\'. We assume that b\n        didn\'t know about Fraction in its implementation, and that it\n        uses similar boilerplate code:\n\n            4. If B <: Rational, then __radd_ converts both to the\n               builtin rational type (hey look, that\'s us) and\n               proceeds.\n            5. Otherwise, __radd__ tries to find the nearest common\n               base ABC, and fall back to its builtin type. Since this\n               class doesn\'t subclass a concrete type, there\'s no\n               implementation to fall back to, so we need to try as\n               hard as possible to return an actual value, or the user\n               will get a TypeError.\n\n        ';C='__';A=fallback_operator
		def D(a,b):
			if isinstance(b,(int,Fraction)):return B(a,b)
			elif isinstance(b,float):return A(float(a),b)
			elif isinstance(b,complex):return A(complex(a),b)
			else:return NotImplemented
		D.__name__=C+A.__name__+C;D.__doc__=B.__doc__
		def E(b,a):
			if isinstance(a,numbers.Rational):return B(a,b)
			elif isinstance(a,numbers.Real):return A(float(a),float(b))
			elif isinstance(a,numbers.Complex):return A(complex(a),complex(b))
			else:return NotImplemented
		E.__name__='__r'+A.__name__+C;E.__doc__=B.__doc__;return D,E
	def _add(A,b):'a + b';B,C=A.denominator,b.denominator;return Fraction(A.numerator*C+b.numerator*B,B*C)
	__add__,__radd__=_operator_fallbacks(_add,operator.add)
	def _sub(A,b):'a - b';B,C=A.denominator,b.denominator;return Fraction(A.numerator*C-b.numerator*B,B*C)
	__sub__,__rsub__=_operator_fallbacks(_sub,operator.sub)
	def _mul(A,b):'a * b';return Fraction(A.numerator*b.numerator,A.denominator*b.denominator)
	__mul__,__rmul__=_operator_fallbacks(_mul,operator.mul)
	def _div(A,b):'a / b';return Fraction(A.numerator*b.denominator,A.denominator*b.numerator)
	__truediv__,__rtruediv__=_operator_fallbacks(_div,operator.truediv)
	def _floordiv(A,b):'a // b';return A.numerator*b.denominator//(A.denominator*b.numerator)
	__floordiv__,__rfloordiv__=_operator_fallbacks(_floordiv,operator.floordiv)
	def _divmod(A,b):'(a // b, a % b)';B,C=A.denominator,b.denominator;D,E=divmod(A.numerator*C,B*b.numerator);return D,Fraction(E,B*C)
	__divmod__,__rdivmod__=_operator_fallbacks(_divmod,divmod)
	def _mod(A,b):'a % b';B,C=A.denominator,b.denominator;return Fraction(A.numerator*C%(b.numerator*B),B*C)
	__mod__,__rmod__=_operator_fallbacks(_mod,operator.mod)
	def __pow__(A,b):
		'a ** b\n\n        If b is not an integer, the result will be a float or complex\n        since roots are generally irrational. If b is an integer, the\n        result will be rational.\n\n        '
		if isinstance(b,numbers.Rational):
			if b.denominator==1:
				B=b.numerator
				if B>=0:return Fraction(A._numerator**B,A._denominator**B,_normalize=_A)
				elif A._numerator>=0:return Fraction(A._denominator**-B,A._numerator**-B,_normalize=_A)
				else:return Fraction((-A._denominator)**-B,(-A._numerator)**-B,_normalize=_A)
			else:return float(A)**float(b)
		else:return float(A)**b
	def __rpow__(A,a):
		'a ** b'
		if A._denominator==1 and A._numerator>=0:return a**A._numerator
		if isinstance(a,numbers.Rational):return Fraction(a.numerator,a.denominator)**A
		if A._denominator==1:return a**A._numerator
		return a**float(A)
	def __pos__(A):'+a: Coerces a subclass instance to Fraction';return Fraction(A._numerator,A._denominator,_normalize=_A)
	def __neg__(A):'-a';return Fraction(-A._numerator,A._denominator,_normalize=_A)
	def __abs__(A):'abs(a)';return Fraction(abs(A._numerator),A._denominator,_normalize=_A)
	def __trunc__(A):
		'trunc(a)'
		if A._numerator<0:return-(-A._numerator//A._denominator)
		else:return A._numerator//A._denominator
	def __floor__(A):'math.floor(a)';return A.numerator//A.denominator
	def __ceil__(A):'math.ceil(a)';return-(-A.numerator//A.denominator)
	def __round__(A,ndigits=_B):
		'round(self, ndigits)\n\n        Rounds half toward even.\n        ';D=ndigits
		if D is _B:
			B,E=divmod(A.numerator,A.denominator)
			if E*2<A.denominator:return B
			elif E*2>A.denominator:return B+1
			elif B%2==0:return B
			else:return B+1
		C=10**abs(D)
		if D>0:return Fraction(round(A*C),C)
		else:return Fraction(round(A/C)*C)
	def __hash__(A):
		'hash(self)';C=pow(A._denominator,_PyHASH_MODULUS-2,_PyHASH_MODULUS)
		if not C:B=_PyHASH_INF
		else:B=abs(A._numerator)*C%_PyHASH_MODULUS
		D=B if A>=0 else-B;return-2 if D==-1 else D
	def __eq__(A,b):
		'a == b'
		if type(b)is int:return A._numerator==b and A._denominator==1
		if isinstance(b,numbers.Rational):return A._numerator==b.numerator and A._denominator==b.denominator
		if isinstance(b,numbers.Complex)and b.imag==0:b=b.real
		if isinstance(b,float):
			if math.isnan(b)or math.isinf(b):return .0==b
			else:return A==A.from_float(b)
		else:return NotImplemented
	def _richcmp(B,other,op):
		'Helper for comparison operators, for internal use only.\n\n        Implement comparison between a Rational instance `self`, and\n        either another Rational instance or a float `other`.  If\n        `other` is not a Rational instance or a float, return\n        NotImplemented. `op` should be one of the six standard\n        comparison operators.\n\n        ';A=other
		if isinstance(A,numbers.Rational):return op(B._numerator*A.denominator,B._denominator*A.numerator)
		if isinstance(A,float):
			if math.isnan(A)or math.isinf(A):return op(.0,A)
			else:return op(B,B.from_float(A))
		else:return NotImplemented
	def __lt__(A,b):'a < b';return A._richcmp(b,operator.lt)
	def __gt__(A,b):'a > b';return A._richcmp(b,operator.gt)
	def __le__(A,b):'a <= b';return A._richcmp(b,operator.le)
	def __ge__(A,b):'a >= b';return A._richcmp(b,operator.ge)
	def __bool__(A):'a != 0';return bool(A._numerator)
	def __reduce__(A):return A.__class__,(str(A),)
	def __copy__(A):
		if type(A)==Fraction:return A
		return A.__class__(A._numerator,A._denominator)
	def __deepcopy__(A,memo):
		if type(A)==Fraction:return A
		return A.__class__(A._numerator,A._denominator)