'Random variable generators.\n\n    bytes\n    -----\n           uniform bytes (values between 0 and 255)\n\n    integers\n    --------\n           uniform within range\n\n    sequences\n    ---------\n           pick random element\n           pick random sample\n           pick weighted random sample\n           generate random permutation\n\n    distributions on the real line:\n    ------------------------------\n           uniform\n           triangular\n           normal (Gaussian)\n           lognormal\n           negative exponential\n           gamma\n           beta\n           pareto\n           Weibull\n\n    distributions on the circle (angles 0 to 2pi)\n    ---------------------------------------------\n           circular uniform\n           von Mises\n\nGeneral notes on the underlying Mersenne Twister core generator:\n\n* The period is 2**19937-1.\n* It is one of the most extensively tested generators in existence.\n* The random() method is implemented in C, executes in a single Python step,\n  and is, therefore, threadsafe.\n\n'
_F='random'
_E='getrandbits'
_D=True
_C=.0
_B=None
_A=1.
from warnings import warn as _warn
from math import log as _log,exp as _exp,pi as _pi,e as _e,ceil as _ceil
from math import sqrt as _sqrt,acos as _acos,cos as _cos,sin as _sin
from math import tau as TWOPI,floor as _floor,isfinite as _isfinite
try:from os import urandom as _urandom
except ImportError:
	def _urandom(*A,**B):raise NotImplementedError('urandom')
	_os=_B
from _collections_abc import Set as _Set,Sequence as _Sequence
from operator import index as _index
from itertools import accumulate as _accumulate,repeat as _repeat
from bisect import bisect as _bisect
try:import os as _os
except ImportError:_os=_B
import _random
try:from _sha512 import sha512 as _sha512
except ImportError:from hashlib import sha512 as _sha512
__all__=['Random','SystemRandom','betavariate','choice','choices','expovariate','gammavariate','gauss',_E,'getstate','lognormvariate','normalvariate','paretovariate','randbytes','randint',_F,'randrange','sample','seed','setstate','shuffle','triangular','uniform','vonmisesvariate','weibullvariate']
NV_MAGICCONST=4*_exp(-.5)/_sqrt(2.)
LOG4=_log(4.)
SG_MAGICCONST=_A+_log(4.5)
BPF=53
RECIP_BPF=2**-BPF
_ONE=1
class Random(_random.Random):
	"Random number generator base class used by bound module functions.\n\n    Used to instantiate instances of Random to get generators that don't\n    share state.\n\n    Class Random can also be subclassed if you want to use a different basic\n    generator of your own devising: in that case, override the following\n    methods:  random(), seed(), getstate(), and setstate().\n    Optionally, implement a getrandbits() method so that randrange()\n    can cover arbitrarily large ranges.\n\n    ";VERSION=3
	def __init__(A,x=_B):'Initialize an instance.\n\n        Optional argument x controls seeding, as for Random.seed().\n        ';A.seed(x);A.gauss_next=_B
	def seed(C,a=_B,version=2):
		'Initialize internal state from a seed.\n\n        The only supported seed types are None, int, float,\n        str, bytes, and bytearray.\n\n        None or no argument seeds from current time or from an operating\n        system specific randomness source if available.\n\n        If *a* is an int, all bits are used.\n\n        For version 2 (the default), all of the bits are used if *a* is a str,\n        bytes, or bytearray.  For version 1 (provided for reproducing random\n        sequences from older versions of Python), the algorithm for str and\n        bytes generates a narrower range of seeds.\n\n        ';B=version
		if B==1 and isinstance(a,(str,bytes)):
			a=a.decode('latin-1')if isinstance(a,bytes)else a;A=ord(a[0])<<7 if a else 0
			for D in map(ord,a):A=(1000003*A^D)&0xffffffffffffffff
			A^=len(a);a=-2 if A==-1 else A
		elif B==2 and isinstance(a,(str,bytes,bytearray)):
			if isinstance(a,str):a=a.encode()
			a=int.from_bytes(a+_sha512(a).digest())
		elif not isinstance(a,(type(_B),int,float,str,bytes,bytearray)):raise TypeError('The only supported seed types are: None,\nint, float, str, bytes, and bytearray.')
		super().seed(a);C.gauss_next=_B
	def getstate(A):'Return internal state; can be passed to setstate() later.';return A.VERSION,super().getstate(),A.gauss_next
	def setstate(C,state):
		'Restore internal state from object returned by getstate().';D=state;A=D[0]
		if A==3:A,B,C.gauss_next=D;super().setstate(B)
		elif A==2:
			A,B,C.gauss_next=D
			try:B=tuple(A%2**32 for A in B)
			except ValueError as E:raise TypeError from E
			super().setstate(B)
		else:raise ValueError('state with version %s passed to Random.setstate() of version %s'%(A,C.VERSION))
	def __getstate__(A):return A.getstate()
	def __setstate__(A,state):A.setstate(state)
	def __reduce__(A):return A.__class__,(),A.getstate()
	def __init_subclass__(A,**C):
		'Control how subclasses generate random integers.\n\n        The algorithm a subclass can use depends on the random() and/or\n        getrandbits() implementation available to it and determines\n        whether it can generate random integers from arbitrarily large\n        ranges.\n        '
		for B in A.__mro__:
			if'_randbelow'in B.__dict__:break
			if _E in B.__dict__:A._randbelow=A._randbelow_with_getrandbits;break
			if _F in B.__dict__:A._randbelow=A._randbelow_without_getrandbits;break
	def _randbelow_with_getrandbits(D,n):
		'Return a random int in the range [0,n).  Defined for n > 0.';B=D.getrandbits;C=n.bit_length();A=B(C)
		while A>=n:A=B(C)
		return A
	def _randbelow_without_getrandbits(D,n,maxsize=1<<BPF):
		'Return a random int in the range [0,n).  Defined for n > 0.\n\n        The implementation does not use getrandbits, but only random.\n        ';A=maxsize;B=D.random
		if n>=A:_warn('Underlying random() generator does not supply \nenough bits to choose from a population range this large.\nTo remove the range limitation, add a getrandbits() method.');return _floor(B()*n)
		E=A%n;F=(A-E)/A;C=B()
		while C>=F:C=B()
		return _floor(C*A)%n
	_randbelow=_randbelow_with_getrandbits
	def randbytes(A,n):'Generate n random bytes.';return A.getrandbits(n*8).to_bytes(n,'little')
	def randrange(G,start,stop=_B,step=_ONE):
		'Choose a random item from range(stop) or range(start, stop[, step]).\n\n        Roughly equivalent to ``choice(range(start, stop, step))`` but\n        supports arbitrarily large ranges and is optimized for common cases.\n\n        ';L='empty range for randrange()';H='non-integer arguments to randrange() have been deprecated since Python 3.10 and will be removed in a subsequent version';I='randrange() will raise TypeError in the future';J=start;D=step;E=stop
		try:B=_index(J)
		except TypeError:
			B=int(J)
			if B!=J:_warn(I,DeprecationWarning,2);raise ValueError('non-integer arg 1 for randrange()')
			_warn(H,DeprecationWarning,2)
		if E is _B:
			if D is not _ONE:raise TypeError('Missing a non-None stop argument')
			if B>0:return G._randbelow(B)
			raise ValueError(L)
		try:F=_index(E)
		except TypeError:
			F=int(E)
			if F!=E:_warn(I,DeprecationWarning,2);raise ValueError('non-integer stop for randrange()')
			_warn(H,DeprecationWarning,2)
		C=F-B
		try:A=_index(D)
		except TypeError:
			A=int(D)
			if A!=D:_warn(I,DeprecationWarning,2);raise ValueError('non-integer step for randrange()')
			_warn(H,DeprecationWarning,2)
		if A==1:
			if C>0:return B+G._randbelow(C)
			raise ValueError('empty range for randrange() (%d, %d, %d)'%(B,F,C))
		if A>0:K=(C+A-1)//A
		elif A<0:K=(C+A+1)//A
		else:raise ValueError('zero step for randrange()')
		if K<=0:raise ValueError(L)
		return B+A*G._randbelow(K)
	def randint(A,a,b):'Return random integer in range [a, b], including both end points.\n        ';return A.randrange(a,b+1)
	def choice(B,seq):
		'Choose a random element from a non-empty sequence.';A=seq
		if not len(A):raise IndexError('Cannot choose from an empty sequence')
		return A[B._randbelow(len(A))]
	def shuffle(C,x):
		'Shuffle list x in place, and return None.';D=C._randbelow
		for A in reversed(range(1,len(x))):B=D(A+1);x[A],x[B]=x[B],x[A]
	def sample(J,population,k,*,counts=_B):
		"Chooses k unique random elements from a population sequence.\n\n        Returns a new list containing elements from the population while\n        leaving the original population unchanged.  The resulting list is\n        in selection order so that all sub-slices will also be valid random\n        samples.  This allows raffle winners (the sample) to be partitioned\n        into grand prize and second place winners (the subslices).\n\n        Members of the population need not be hashable or unique.  If the\n        population contains repeats, then each occurrence is a possible\n        selection in the sample.\n\n        Repeated elements can be specified one at a time or with the optional\n        counts parameter.  For example:\n\n            sample(['red', 'blue'], counts=[4, 2], k=5)\n\n        is equivalent to:\n\n            sample(['red', 'red', 'red', 'red', 'blue', 'blue'], k=5)\n\n        To choose a sample from a range of integers, use range() for the\n        population argument.  This is especially fast and space efficient\n        for sampling from a large population:\n\n            sample(range(10000000), 60)\n\n        ";K=counts;C=population
		if not isinstance(C,_Sequence):raise TypeError('Population must be a sequence.  For dicts or sets, use sorted(d).')
		A=len(C)
		if K is not _B:
			E=list(_accumulate(K))
			if len(E)!=A:raise ValueError('The number of counts does not match the population')
			F=E.pop()
			if not isinstance(F,int):raise TypeError('Counts must be integers')
			if F<=0:raise ValueError('Total of counts must be greater than zero')
			N=J.sample(range(F),k=k);O=_bisect;return[C[O(E,A)]for A in N]
		G=J._randbelow
		if not 0<=k<=A:raise ValueError('Sample larger than population or is negative')
		H=[_B]*k;L=21
		if k>5:L+=4**_ceil(_log(k*3,4))
		if A<=L:
			I=list(C)
			for D in range(k):B=G(A-D);H[D]=I[B];I[B]=I[A-D-1]
		else:
			M=set();P=M.add
			for D in range(k):
				B=G(A)
				while B in M:B=G(A)
				P(B);H[D]=C[B]
		return H
	def choices(G,population,weights=_B,*,cum_weights=_B,k=1):
		'Return a k sized list of population elements chosen with replacement.\n\n        If the relative weights or cumulative weights are not specified,\n        the selections are made with equal probability.\n\n        ';D=population;A=cum_weights;B=weights;F=G.random;C=len(D)
		if A is _B:
			if B is _B:H=_floor;C+=_C;return[D[H(F()*C)]for A in _repeat(_B,k)]
			try:A=list(_accumulate(B))
			except TypeError:
				if not isinstance(B,int):raise
				k=B;raise TypeError(f"The number of choices must be a keyword argument: k={k!r}")from _B
		elif B is not _B:raise TypeError('Cannot specify both weights and cumulative weights')
		if len(A)!=C:raise ValueError('The number of weights does not match the population')
		E=A[-1]+_C
		if E<=_C:raise ValueError('Total of weights must be greater than zero')
		if not _isfinite(E):raise ValueError('Total of weights must be finite')
		I=_bisect;J=C-1;return[D[I(A,F()*E,0,J)]for B in _repeat(_B,k)]
	def uniform(A,a,b):'Get a random number in the range [a, b) or [a, b] depending on rounding.';return a+(b-a)*A.random()
	def triangular(E,low=_C,high=_A,mode=_B):
		'Triangular distribution.\n\n        Continuous distribution bounded by given lower and upper limits,\n        and having a given mode value in-between.\n\n        http://en.wikipedia.org/wiki/Triangular_distribution\n\n        ';B=high;A=low;C=E.random()
		try:D=.5 if mode is _B else(mode-A)/(B-A)
		except ZeroDivisionError:return A
		if C>D:C=_A-C;D=_A-D;A,B=B,A
		return A+(B-A)*_sqrt(C*D)
	def normalvariate(D,mu=_C,sigma=_A):
		'Normal distribution.\n\n        mu is the mean, and sigma is the standard deviation.\n\n        ';B=D.random
		while _D:
			E=B();C=_A-B();A=NV_MAGICCONST*(E-.5)/C;F=A*A/4.
			if F<=-_log(C):break
		return mu+A*sigma
	def gauss(A,mu=_C,sigma=_A):
		'Gaussian distribution.\n\n        mu is the mean, and sigma is the standard deviation.  This is\n        slightly faster than the normalvariate() function.\n\n        Not thread-safe without a lock around calls.\n\n        ';C=A.random;B=A.gauss_next;A.gauss_next=_B
		if B is _B:D=C()*TWOPI;E=_sqrt(-2.*_log(_A-C()));B=_cos(D)*E;A.gauss_next=_sin(D)*E
		return mu+B*sigma
	def lognormvariate(A,mu,sigma):"Log normal distribution.\n\n        If you take the natural logarithm of this distribution, you'll get a\n        normal distribution with mean mu and standard deviation sigma.\n        mu can have any value, and sigma must be greater than zero.\n\n        ";return _exp(A.normalvariate(mu,sigma))
	def expovariate(A,lambd):'Exponential distribution.\n\n        lambd is 1.0 divided by the desired mean.  It should be\n        nonzero.  (The parameter would be called "lambda", but that is\n        a reserved word in Python.)  Returned values range from 0 to\n        positive infinity if lambd is positive, and from negative\n        infinity to 0 if lambd is negative.\n\n        ';return-_log(_A-A.random())/lambd
	def vonmisesvariate(K,mu,kappa):
		'Circular data distribution.\n\n        mu is the mean angle, expressed in radians between 0 and 2*pi, and\n        kappa is the concentration parameter, which must be greater than or\n        equal to zero.  If kappa is equal to zero, this distribution reduces\n        to a uniform random angle over the range 0 to 2*pi.\n\n        ';E=kappa;A=K.random
		if E<=1e-06:return TWOPI*A()
		D=.5/E;F=D+_sqrt(_A+D*D)
		while _D:
			L=A();B=_cos(_pi*L);C=B/(F+B);G=A()
			if G<_A-C*C or G<=(_A-C)*_exp(C):break
		H=_A/F;I=(H+B)/(_A+H*B);M=A()
		if M>.5:J=(mu+_acos(I))%TWOPI
		else:J=(mu-_acos(I))%TWOPI
		return J
	def gammavariate(L,alpha,beta):
		'Gamma distribution.  Not the gamma function!\n\n        Conditions on the parameters are alpha > 0 and beta > 0.\n\n        The probability distribution function is:\n\n                    x ** (alpha - 1) * math.exp(-x / beta)\n          pdf(x) =  --------------------------------------\n                      math.gamma(alpha) * beta ** alpha\n\n        ';E=beta;A=alpha
		if A<=_C or E<=_C:raise ValueError('gammavariate: alpha and beta must be > 0.0')
		D=L.random
		if A>_A:
			G=_sqrt(2.*A-_A);M=A-LOG4;N=A+G
			while _D:
				B=D()
				if not 1e-07<B<.9999999:continue
				O=_A-D();H=_log(B/(_A-B))/G;C=A*_exp(H);I=B*B*O;J=M+N*H-C
				if J+SG_MAGICCONST-4.5*I>=_C or J>=_log(I):return C*E
		elif A==_A:return-_log(_A-D())*E
		else:
			while _D:
				P=D();K=(_e+A)/_e;F=K*P
				if F<=_A:C=F**(_A/A)
				else:C=-_log((K-F)/A)
				B=D()
				if F>_A:
					if B<=C**(A-_A):break
				elif B<=_exp(-C):break
			return C*E
	def betavariate(B,alpha,beta):
		'Beta distribution.\n\n        Conditions on the parameters are alpha > 0 and beta > 0.\n        Returned values range between 0 and 1.\n\n        ';A=B.gammavariate(alpha,_A)
		if A:return A/(A+B.gammavariate(beta,_A))
		return _C
	def paretovariate(A,alpha):'Pareto distribution.  alpha is the shape parameter.';B=_A-A.random();return B**(-_A/alpha)
	def weibullvariate(A,alpha,beta):'Weibull distribution.\n\n        alpha is the scale parameter and beta is the shape parameter.\n\n        ';B=_A-A.random();return alpha*(-_log(B))**(_A/beta)
class SystemRandom(Random):
	'Alternate random number generator using sources provided\n    by the operating system (such as /dev/urandom on Unix or\n    CryptGenRandom on Windows).\n\n     Not available on all systems (see os.urandom() for details).\n\n    '
	def random(A):'Get the next random number in the range 0.0 <= X < 1.0.';return(int.from_bytes(_urandom(7))>>3)*RECIP_BPF
	def getrandbits(C,k):
		'getrandbits(k) -> x.  Generates an int with k random bits.'
		if k<0:raise ValueError('number of bits must be non-negative')
		A=(k+7)//8;B=int.from_bytes(_urandom(A));return B>>A*8-k
	def randbytes(A,n):'Generate n random bytes.';return _urandom(n)
	def seed(A,*B,**C):'Stub method.  Not used for a system random number generator.'
	def _notimplemented(A,*B,**C):'Method should not be called for a system random number generator.';raise NotImplementedError('System entropy source does not have state.')
	getstate=setstate=_notimplemented
_inst=Random()
seed=_inst.seed
random=_inst.random
uniform=_inst.uniform
triangular=_inst.triangular
randint=_inst.randint
choice=_inst.choice
randrange=_inst.randrange
sample=_inst.sample
shuffle=_inst.shuffle
choices=_inst.choices
normalvariate=_inst.normalvariate
lognormvariate=_inst.lognormvariate
expovariate=_inst.expovariate
vonmisesvariate=_inst.vonmisesvariate
gammavariate=_inst.gammavariate
gauss=_inst.gauss
betavariate=_inst.betavariate
paretovariate=_inst.paretovariate
weibullvariate=_inst.weibullvariate
getstate=_inst.getstate
setstate=_inst.setstate
getrandbits=_inst.getrandbits
randbytes=_inst.randbytes
def _test_generator(n,func,args):from statistics import stdev,fmean as D;from time import perf_counter as B;E=B();A=[func(*args)for A in _repeat(_B,n)];F=B();C=D(A);G=stdev(A,C);H=min(A);I=max(A);print(f"{F-E:.3f} sec, {n} times {func.__name__}");print('avg %g, stddev %g, min %g, max %g\n'%(C,G,H,I))
def _test(N=2000):_test_generator(N,random,());_test_generator(N,normalvariate,(_C,_A));_test_generator(N,lognormvariate,(_C,_A));_test_generator(N,vonmisesvariate,(_C,_A));_test_generator(N,gammavariate,(.01,_A));_test_generator(N,gammavariate,(.1,_A));_test_generator(N,gammavariate,(.1,2.));_test_generator(N,gammavariate,(.5,_A));_test_generator(N,gammavariate,(.9,_A));_test_generator(N,gammavariate,(_A,_A));_test_generator(N,gammavariate,(2.,_A));_test_generator(N,gammavariate,(2e1,_A));_test_generator(N,gammavariate,(2e2,_A));_test_generator(N,gauss,(_C,_A));_test_generator(N,betavariate,(3.,3.));_test_generator(N,triangular,(_C,_A,_A/3.))
if hasattr(_os,'fork'):_os.register_at_fork(after_in_child=_inst.seed)
if __name__=='__main__':_test()