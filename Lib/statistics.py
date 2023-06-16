'\nBasic statistics module.\n\nThis module provides functions for calculating statistics of data, including\naverages, variance, and standard deviation.\n\nCalculating averages\n--------------------\n\n==================  ==================================================\nFunction            Description\n==================  ==================================================\nmean                Arithmetic mean (average) of data.\nfmean               Fast, floating point arithmetic mean.\ngeometric_mean      Geometric mean of data.\nharmonic_mean       Harmonic mean of data.\nmedian              Median (middle value) of data.\nmedian_low          Low median of data.\nmedian_high         High median of data.\nmedian_grouped      Median, or 50th percentile, of grouped data.\nmode                Mode (most common value) of data.\nmultimode           List of modes (most common values of data).\nquantiles           Divide data into intervals with equal probability.\n==================  ==================================================\n\nCalculate the arithmetic mean ("the average") of data:\n\n>>> mean([-1.0, 2.5, 3.25, 5.75])\n2.625\n\n\nCalculate the standard median of discrete data:\n\n>>> median([2, 3, 4, 5])\n3.5\n\n\nCalculate the median, or 50th percentile, of data grouped into class intervals\ncentred on the data values provided. E.g. if your data points are rounded to\nthe nearest whole number:\n\n>>> median_grouped([2, 2, 3, 3, 3, 4])  #doctest: +ELLIPSIS\n2.8333333333...\n\nThis should be interpreted in this way: you have two data points in the class\ninterval 1.5-2.5, three data points in the class interval 2.5-3.5, and one in\nthe class interval 3.5-4.5. The median of these data points is 2.8333...\n\n\nCalculating variability or spread\n---------------------------------\n\n==================  =============================================\nFunction            Description\n==================  =============================================\npvariance           Population variance of data.\nvariance            Sample variance of data.\npstdev              Population standard deviation of data.\nstdev               Sample standard deviation of data.\n==================  =============================================\n\nCalculate the standard deviation of sample data:\n\n>>> stdev([2.5, 3.25, 5.5, 11.25, 11.75])  #doctest: +ELLIPSIS\n4.38961843444...\n\nIf you have previously calculated the mean, you can pass it as the optional\nsecond argument to the four "spread" functions to avoid recalculating it:\n\n>>> data = [1, 2, 2, 4, 4, 4, 5, 6]\n>>> mu = mean(data)\n>>> pvariance(data, mu)\n2.5\n\n\nStatistics for relations between two inputs\n-------------------------------------------\n\n==================  ====================================================\nFunction            Description\n==================  ====================================================\ncovariance          Sample covariance for two variables.\ncorrelation         Pearson\'s correlation coefficient for two variables.\nlinear_regression   Intercept and slope for simple linear regression.\n==================  ====================================================\n\nCalculate covariance, Pearson\'s correlation, and simple linear regression\nfor two inputs:\n\n>>> x = [1, 2, 3, 4, 5, 6, 7, 8, 9]\n>>> y = [1, 2, 3, 1, 2, 3, 1, 2, 3]\n>>> covariance(x, y)\n0.75\n>>> correlation(x, y)  #doctest: +ELLIPSIS\n0.31622776601...\n>>> linear_regression(x, y)  #doctest:\nLinearRegression(slope=0.1, intercept=1.5)\n\n\nExceptions\n----------\n\nA single exception is defined: StatisticsError is a subclass of ValueError.\n\n'
_D='exclusive'
_C='no median for empty data'
_B=1.
_A=None
__all__=['NormalDist','StatisticsError','correlation','covariance','fmean','geometric_mean','harmonic_mean','linear_regression','mean','median','median_grouped','median_high','median_low','mode','multimode','pstdev','pvariance','quantiles','stdev','variance']
import math,numbers,random
from fractions import Fraction
from decimal import Decimal
from itertools import groupby,repeat
from bisect import bisect_left,bisect_right
from math import hypot,sqrt,fabs,exp,erf,tau,log,fsum
from operator import itemgetter
from collections import Counter,namedtuple
class StatisticsError(ValueError):0
def _sum(data):
	'_sum(data) -> (type, sum, count)\n\n    Return a high-precision sum of the given numeric data as a fraction,\n    together with the type to be converted to and the count of items.\n\n    Examples\n    --------\n\n    >>> _sum([3, 2.25, 4.5, -0.5, 0.25])\n    (<class \'float\'>, Fraction(19, 2), 5)\n\n    Some sources of round-off error will be avoided:\n\n    # Built-in sum returns zero.\n    >>> _sum([1e50, 1, -1e50] * 1000)\n    (<class \'float\'>, Fraction(1000, 1), 3000)\n\n    Fractions and Decimals are also supported:\n\n    >>> from fractions import Fraction as F\n    >>> _sum([F(2, 3), F(7, 5), F(1, 4), F(5, 6)])\n    (<class \'fractions.Fraction\'>, Fraction(63, 20), 4)\n\n    >>> from decimal import Decimal as D\n    >>> data = [D("0.1375"), D("0.2108"), D("0.3061"), D("0.0419")]\n    >>> _sum(data)\n    (<class \'decimal.Decimal\'>, Fraction(6963, 10000), 4)\n\n    Mixed types are currently treated as an error, except that int is\n    allowed.\n    ';D=0;A={};F=A.get;B=int
	for(G,H)in groupby(data,type):
		B=_coerce(B,G)
		for(I,E)in map(_exact_ratio,H):D+=1;A[E]=F(E,0)+I
	if _A in A:C=A[_A];assert not _isfinite(C)
	else:C=sum(Fraction(B,A)for(A,B)in A.items())
	return B,C,D
def _isfinite(x):
	try:return x.is_finite()
	except AttributeError:return math.isfinite(x)
def _coerce(T,S):
	'Coerce types T and S to a common type, or raise TypeError.\n\n    Coercion rules are currently an implementation detail. See the CoerceTest\n    test class in test_statistics for details.\n    ';assert T is not bool,'initial type T is bool'
	if T is S:return T
	if S is int or S is bool:return T
	if T is int:return S
	if issubclass(S,T):return S
	if issubclass(T,S):return T
	if issubclass(T,int):return S
	if issubclass(S,int):return T
	if issubclass(T,Fraction)and issubclass(S,float):return S
	if issubclass(T,float)and issubclass(S,Fraction):return T
	A="don't know how to coerce %s and %s";raise TypeError(A%(T.__name__,S.__name__))
def _exact_ratio(x):
	'Return Real number x to exact (numerator, denominator) pair.\n\n    >>> _exact_ratio(0.25)\n    (1, 4)\n\n    x is expected to be an int, Fraction, Decimal or float.\n    '
	try:return x.as_integer_ratio()
	except AttributeError:pass
	except(OverflowError,ValueError):assert not _isfinite(x);return x,_A
	try:return x.numerator,x.denominator
	except AttributeError:A=f"can't convert type '{type(x).__name__}' to numerator/denominator";raise TypeError(A)
def _convert(value,T):
	'Convert value to given numeric type T.';A=value
	if type(A)is T:return A
	if issubclass(T,int)and A.denominator!=1:T=float
	try:return T(A)
	except TypeError:
		if issubclass(T,Decimal):return T(A.numerator)/T(A.denominator)
		else:raise
def _find_lteq(a,x):
	'Locate the leftmost value exactly equal to x';A=bisect_left(a,x)
	if A!=len(a)and a[A]==x:return A
	raise ValueError
def _find_rteq(a,l,x):
	'Locate the rightmost value exactly equal to x';A=bisect_right(a,x,lo=l)
	if A!=len(a)+1 and a[A-1]==x:return A-1
	raise ValueError
def _fail_neg(values,errmsg='negative value'):
	'Iterate over values, failing if any are less than zero.'
	for A in values:
		if A<0:raise StatisticsError(errmsg)
		yield A
def mean(data):
	'Return the sample arithmetic mean of data.\n\n    >>> mean([1, 2, 3, 4, 4])\n    2.8\n\n    >>> from fractions import Fraction as F\n    >>> mean([F(3, 7), F(1, 21), F(5, 3), F(1, 3)])\n    Fraction(13, 21)\n\n    >>> from decimal import Decimal as D\n    >>> mean([D("0.5"), D("0.75"), D("0.625"), D("0.375")])\n    Decimal(\'0.5625\')\n\n    If ``data`` is empty, StatisticsError will be raised.\n    ';A=data
	if iter(A)is A:A=list(A)
	B=len(A)
	if B<1:raise StatisticsError('mean requires at least one data point')
	C,D,E=_sum(A);assert E==B;return _convert(D/B,C)
def fmean(data):
	'Convert data to floats and compute the arithmetic mean.\n\n    This runs faster than the mean() function and it always returns a float.\n    If the input dataset is empty, it raises a StatisticsError.\n\n    >>> fmean([3.5, 4.0, 5.25])\n    4.25\n    ';B=data
	try:A=len(B)
	except TypeError:
		A=0
		def D(iterable):
			nonlocal A
			for(A,B)in enumerate(iterable,start=1):yield B
		C=fsum(D(B))
	else:C=fsum(B)
	try:return C/A
	except ZeroDivisionError:raise StatisticsError('fmean requires at least one data point')from _A
def geometric_mean(data):
	'Convert data to floats and compute the geometric mean.\n\n    Raises a StatisticsError if the input dataset is empty,\n    if it contains a zero, or if it contains a negative value.\n\n    No special efforts are made to achieve exact results.\n    (However, this may change in the future.)\n\n    >>> round(geometric_mean([54, 24, 36]), 9)\n    36.0\n    '
	try:return exp(fmean(map(log,data)))
	except ValueError:raise StatisticsError('geometric mean requires a non-empty dataset containing positive numbers')from _A
def harmonic_mean(data,weights=_A):
	'Return the harmonic mean of data.\n\n    The harmonic mean is the reciprocal of the arithmetic mean of the\n    reciprocals of the data.  It can be used for averaging ratios or\n    rates, for example speeds.\n\n    Suppose a car travels 40 km/hr for 5 km and then speeds-up to\n    60 km/hr for another 5 km. What is the average speed?\n\n        >>> harmonic_mean([40, 60])\n        48.0\n\n    Suppose a car travels 40 km/hr for 5 km, and when traffic clears,\n    speeds-up to 60 km/hr for the remaining 30 km of the journey. What\n    is the average speed?\n\n        >>> harmonic_mean([40, 60], weights=[5, 30])\n        56.0\n\n    If ``data`` is empty, or any element is less than zero,\n    ``harmonic_mean`` will raise ``StatisticsError``.\n    ';B=data;A=weights
	if iter(B)is B:B=list(B)
	D='harmonic mean does not support negative values';C=len(B)
	if C<1:raise StatisticsError('harmonic_mean requires at least one data point')
	elif C==1 and A is _A:
		E=B[0]
		if isinstance(E,(numbers.Real,Decimal)):
			if E<0:raise StatisticsError(D)
			return E
		else:raise TypeError('unsupported type')
	if A is _A:A=repeat(1,C);F=C
	else:
		if iter(A)is A:A=list(A)
		if len(A)!=C:raise StatisticsError('Number of weights does not match data size')
		H,F,H=_sum(A for A in _fail_neg(A,D))
	try:B=_fail_neg(B,D);I,G,J=_sum(A/B if A else 0 for(A,B)in zip(A,B))
	except ZeroDivisionError:return 0
	if G<=0:raise StatisticsError('Weighted sum must be positive')
	return _convert(F/G,I)
def median(data):
	'Return the median (middle value) of numeric data.\n\n    When the number of data points is odd, return the middle data point.\n    When the number of data points is even, the median is interpolated by\n    taking the average of the two middle values:\n\n    >>> median([1, 3, 5])\n    3\n    >>> median([1, 3, 5, 7])\n    4.0\n\n    ';A=data;A=sorted(A);B=len(A)
	if B==0:raise StatisticsError(_C)
	if B%2==1:return A[B//2]
	else:C=B//2;return(A[C-1]+A[C])/2
def median_low(data):
	'Return the low median of numeric data.\n\n    When the number of data points is odd, the middle value is returned.\n    When it is even, the smaller of the two middle values is returned.\n\n    >>> median_low([1, 3, 5])\n    3\n    >>> median_low([1, 3, 5, 7])\n    3\n\n    ';A=data;A=sorted(A);B=len(A)
	if B==0:raise StatisticsError(_C)
	if B%2==1:return A[B//2]
	else:return A[B//2-1]
def median_high(data):
	'Return the high median of data.\n\n    When the number of data points is odd, the middle value is returned.\n    When it is even, the larger of the two middle values is returned.\n\n    >>> median_high([1, 3, 5])\n    3\n    >>> median_high([1, 3, 5, 7])\n    5\n\n    ';A=data;A=sorted(A);B=len(A)
	if B==0:raise StatisticsError(_C)
	return A[B//2]
def median_grouped(data,interval=1):
	'Return the 50th percentile (median) of grouped continuous data.\n\n    >>> median_grouped([1, 2, 2, 3, 4, 4, 4, 4, 4, 5])\n    3.7\n    >>> median_grouped([52, 52, 53, 54])\n    52.5\n\n    This calculates the median as the 50th percentile, and should be\n    used when your data is continuous and grouped. In the above example,\n    the values 1, 2, 3, etc. actually represent the midpoint of classes\n    0.5-1.5, 1.5-2.5, 2.5-3.5, etc. The middle value falls somewhere in\n    class 3.5-4.5, and interpolation is used to estimate it.\n\n    Optional argument ``interval`` represents the class interval, and\n    defaults to 1. Changing the class interval naturally will change the\n    interpolated 50th percentile value:\n\n    >>> median_grouped([1, 3, 3, 5, 7], interval=1)\n    3.25\n    >>> median_grouped([1, 3, 3, 5, 7], interval=2)\n    3.5\n\n    This function does not check whether the data points are at least\n    ``interval`` apart.\n    ';C=interval;A=data;A=sorted(A);D=len(A)
	if D==0:raise StatisticsError(_C)
	elif D==1:return A[0]
	B=A[D//2]
	for F in(B,C):
		if isinstance(F,(str,bytes)):raise TypeError('expected number but got %r'%F)
	try:G=B-C/2
	except TypeError:G=float(B)-float(C)/2
	E=_find_lteq(A,B);H=_find_rteq(A,E,B);I=E;J=H-E+1;return G+C*(D/2-I)/J
def mode(data):
	'Return the most common data point from discrete or nominal data.\n\n    ``mode`` assumes discrete data, and returns a single value. This is the\n    standard treatment of the mode as commonly taught in schools:\n\n        >>> mode([1, 1, 2, 3, 3, 3, 3, 4])\n        3\n\n    This also works with nominal (non-numeric) data:\n\n        >>> mode(["red", "blue", "blue", "red", "green", "red", "red"])\n        \'red\'\n\n    If there are multiple modes with same frequency, return the first one\n    encountered:\n\n        >>> mode([\'red\', \'red\', \'green\', \'blue\', \'blue\'])\n        \'red\'\n\n    If *data* is empty, ``mode``, raises StatisticsError.\n\n    ';A=Counter(iter(data)).most_common(1)
	try:return A[0][0]
	except IndexError:raise StatisticsError('no mode for empty data')from _A
def multimode(data):"Return a list of the most frequently occurring values.\n\n    Will return more than one result if there are multiple modes\n    or an empty list if *data* is empty.\n\n    >>> multimode('aabbbbbbbbcc')\n    ['b']\n    >>> multimode('aabbbbccddddeeffffgg')\n    ['b', 'd', 'f']\n    >>> multimode('')\n    []\n    ";A=Counter(iter(data)).most_common();C,B=next(groupby(A,key=itemgetter(1)),(0,[]));return list(map(itemgetter(0),B))
def quantiles(data,*,n=4,method=_D):
	'Divide *data* into *n* continuous intervals with equal probability.\n\n    Returns a list of (n - 1) cut points separating the intervals.\n\n    Set *n* to 4 for quartiles (the default).  Set *n* to 10 for deciles.\n    Set *n* to 100 for percentiles which gives the 99 cuts points that\n    separate *data* in to 100 equal sized groups.\n\n    The *data* can be any iterable containing sample.\n    The cut points are linearly interpolated between data points.\n\n    If *method* is set to *inclusive*, *data* is treated as population\n    data.  The minimum value is treated as the 0th percentile and the\n    maximum value is treated as the 100th percentile.\n    ';H=method;B=data
	if n<1:raise StatisticsError('n must be at least 1')
	B=sorted(B);C=len(B)
	if C<2:raise StatisticsError('must have at least two data points')
	if H=='inclusive':
		F=C-1;D=[]
		for G in range(1,n):A,E=divmod(G*F,n);I=(B[A]*(n-E)+B[A+1]*E)/n;D.append(I)
		return D
	if H==_D:
		F=C+1;D=[]
		for G in range(1,n):A=G*F//n;A=1 if A<1 else C-1 if A>C-1 else A;E=G*F-A*n;I=(B[A-1]*(n-E)+B[A]*E)/n;D.append(I)
		return D
	raise ValueError(f"Unknown method: {H!r}")
def _ss(data,c=_A):
	'Return sum of square deviations of sequence data.\n\n    If ``c`` is None, the mean is calculated in one pass, and the deviations\n    from the mean are calculated in a second pass. Otherwise, deviations are\n    calculated from ``c`` as given. Use the second case with care, as it can\n    lead to garbage results.\n    ';C=data
	if c is not _A:D,A,E=_sum((A-c)**2 for A in C);return D,A
	D,A,E=_sum(C);J,F=(A/E).as_integer_ratio();B=Counter()
	for(K,G)in map(_exact_ratio,C):H=K*F-G*J;I=G*F;B[I*I]+=H*H
	if _A in B:A=B[_A];assert not _isfinite(A)
	else:A=sum(Fraction(B,A)for(A,B)in B.items())
	return D,A
def variance(data,xbar=_A):
	'Return the sample variance of data.\n\n    data should be an iterable of Real-valued numbers, with at least two\n    values. The optional argument xbar, if given, should be the mean of\n    the data. If it is missing or None, the mean is automatically calculated.\n\n    Use this function when your data is a sample from a population. To\n    calculate the variance from the entire population, see ``pvariance``.\n\n    Examples:\n\n    >>> data = [2.75, 1.75, 1.25, 0.25, 0.5, 1.25, 3.5]\n    >>> variance(data)\n    1.3720238095238095\n\n    If you have already calculated the mean of your data, you can pass it as\n    the optional second argument ``xbar`` to avoid recalculating it:\n\n    >>> m = mean(data)\n    >>> variance(data, m)\n    1.3720238095238095\n\n    This function does not check that ``xbar`` is actually the mean of\n    ``data``. Giving arbitrary values for ``xbar`` may lead to invalid or\n    impossible results.\n\n    Decimals and Fractions are supported:\n\n    >>> from decimal import Decimal as D\n    >>> variance([D("27.5"), D("30.25"), D("30.25"), D("34.5"), D("41.75")])\n    Decimal(\'31.01875\')\n\n    >>> from fractions import Fraction as F\n    >>> variance([F(1, 6), F(1, 2), F(5, 3)])\n    Fraction(67, 108)\n\n    ';A=data
	if iter(A)is A:A=list(A)
	B=len(A)
	if B<2:raise StatisticsError('variance requires at least two data points')
	C,D=_ss(A,xbar);return _convert(D/(B-1),C)
def pvariance(data,mu=_A):
	'Return the population variance of ``data``.\n\n    data should be a sequence or iterable of Real-valued numbers, with at least one\n    value. The optional argument mu, if given, should be the mean of\n    the data. If it is missing or None, the mean is automatically calculated.\n\n    Use this function to calculate the variance from the entire population.\n    To estimate the variance from a sample, the ``variance`` function is\n    usually a better choice.\n\n    Examples:\n\n    >>> data = [0.0, 0.25, 0.25, 1.25, 1.5, 1.75, 2.75, 3.25]\n    >>> pvariance(data)\n    1.25\n\n    If you have already calculated the mean of the data, you can pass it as\n    the optional second argument to avoid recalculating it:\n\n    >>> mu = mean(data)\n    >>> pvariance(data, mu)\n    1.25\n\n    Decimals and Fractions are supported:\n\n    >>> from decimal import Decimal as D\n    >>> pvariance([D("27.5"), D("30.25"), D("30.25"), D("34.5"), D("41.75")])\n    Decimal(\'24.815\')\n\n    >>> from fractions import Fraction as F\n    >>> pvariance([F(1, 4), F(5, 4), F(1, 2)])\n    Fraction(13, 72)\n\n    ';A=data
	if iter(A)is A:A=list(A)
	B=len(A)
	if B<1:raise StatisticsError('pvariance requires at least one data point')
	C,D=_ss(A,mu);return _convert(D/B,C)
def stdev(data,xbar=_A):
	'Return the square root of the sample variance.\n\n    See ``variance`` for arguments and other details.\n\n    >>> stdev([1.5, 2.5, 2.5, 2.75, 3.25, 4.75])\n    1.0810874155219827\n\n    ';A=variance(data,xbar)
	try:return A.sqrt()
	except AttributeError:return math.sqrt(A)
def pstdev(data,mu=_A):
	'Return the square root of the population variance.\n\n    See ``pvariance`` for arguments and other details.\n\n    >>> pstdev([1.5, 2.5, 2.5, 2.75, 3.25, 4.75])\n    0.986893273527251\n\n    ';A=pvariance(data,mu)
	try:return A.sqrt()
	except AttributeError:return math.sqrt(A)
def covariance(B,C):
	'Covariance\n\n    Return the sample covariance of two inputs *x* and *y*. Covariance\n    is a measure of the joint variability of two inputs.\n\n    >>> x = [1, 2, 3, 4, 5, 6, 7, 8, 9]\n    >>> y = [1, 2, 3, 1, 2, 3, 1, 2, 3]\n    >>> covariance(x, y)\n    0.75\n    >>> z = [9, 8, 7, 6, 5, 4, 3, 2, 1]\n    >>> covariance(x, z)\n    -7.5\n    >>> covariance(z, x)\n    -7.5\n\n    ';A=len(B)
	if len(C)!=A:raise StatisticsError('covariance requires that both inputs have same number of data points')
	if A<2:raise StatisticsError('covariance requires at least two data points')
	D=fsum(B)/A;E=fsum(C)/A;F=fsum((A-D)*(B-E)for(A,B)in zip(B,C));return F/(A-1)
def correlation(A,B):
	"Pearson's correlation coefficient\n\n    Return the Pearson's correlation coefficient for two inputs. Pearson's\n    correlation coefficient *r* takes values between -1 and +1. It measures the\n    strength and direction of the linear relationship, where +1 means very\n    strong, positive linear relationship, -1 very strong, negative linear\n    relationship, and 0 no linear relationship.\n\n    >>> x = [1, 2, 3, 4, 5, 6, 7, 8, 9]\n    >>> y = [9, 8, 7, 6, 5, 4, 3, 2, 1]\n    >>> correlation(x, x)\n    1.0\n    >>> correlation(x, y)\n    -1.0\n\n    ";C=len(A)
	if len(B)!=C:raise StatisticsError('correlation requires that both inputs have same number of data points')
	if C<2:raise StatisticsError('correlation requires at least two data points')
	D=fsum(A)/C;E=fsum(B)/C;F=fsum((A-D)*(B-E)for(A,B)in zip(A,B));G=fsum((A-D)**2. for A in A);H=fsum((A-E)**2. for A in B)
	try:return F/sqrt(G*H)
	except ZeroDivisionError:raise StatisticsError('at least one of the inputs is constant')
LinearRegression=namedtuple('LinearRegression',('slope','intercept'))
def linear_regression(A,C):
	'Slope and intercept for simple linear regression.\n\n    Return the slope and intercept of simple linear regression\n    parameters estimated using ordinary least squares. Simple linear\n    regression describes relationship between an independent variable\n    *x* and a dependent variable *y* in terms of linear function:\n\n        y = slope * x + intercept + noise\n\n    where *slope* and *intercept* are the regression parameters that are\n    estimated, and noise represents the variability of the data that was\n    not explained by the linear regression (it is equal to the\n    difference between predicted and actual values of the dependent\n    variable).\n\n    The parameters are returned as a named tuple.\n\n    >>> x = [1, 2, 3, 4, 5]\n    >>> noise = NormalDist().samples(5, seed=42)\n    >>> y = [3 * x[i] + 2 + noise[i] for i in range(5)]\n    >>> linear_regression(x, y)  #doctest: +ELLIPSIS\n    LinearRegression(slope=3.09078914170..., intercept=1.75684970486...)\n\n    ';B=len(A)
	if len(C)!=B:raise StatisticsError('linear regression requires that both inputs have same number of data points')
	if B<2:raise StatisticsError('linear regression requires at least two data points')
	D=fsum(A)/B;E=fsum(C)/B;G=fsum((A-D)*(B-E)for(A,B)in zip(A,C));H=fsum((A-D)**2. for A in A)
	try:F=G/H
	except ZeroDivisionError:raise StatisticsError('x is constant')
	I=E-F*D;return LinearRegression(slope=F,intercept=I)
def _normal_dist_inv_cdf(p,mu,sigma):
	F=sigma;B=p-.5
	if fabs(B)<=.425:A=.180625-B*B;D=(((((((2509.0809287301227*A+33430.57558358813)*A+67265.7709270087)*A+45921.95393154987)*A+13731.69376550946)*A+1971.5909503065513)*A+133.14166789178438)*A+3.3871328727963665)*B;E=((((((5226.495278852854*A+28729.085735721943)*A+39307.89580009271)*A+21213.794301586597)*A+5394.196021424751)*A+687.1870074920579)*A+42.31333070160091)*A+_B;C=D/E;return mu+C*F
	A=p if B<=.0 else _B-p;A=sqrt(-log(A))
	if A<=5.:A=A-1.6;D=((((((.0007745450142783414*A+.022723844989269184)*A+.2417807251774506)*A+1.2704582524523684)*A+3.6478483247632045)*A+5.769497221460691)*A+4.630337846156546)*A+1.4234371107496835;E=((((((1.0507500716444169e-09*A+.0005475938084995345)*A+.015198666563616457)*A+.14810397642748008)*A+.6897673349851)*A+1.6763848301838038)*A+2.053191626637759)*A+_B
	else:A=A-5.;D=((((((2.0103343992922881e-07*A+2.7115555687434876e-05)*A+.0012426609473880784)*A+.026532189526576124)*A+.29656057182850487)*A+1.7848265399172913)*A+5.463784911164114)*A+6.657904643501103;E=((((((2.0442631033899397e-15*A+1.421511758316446e-07)*A+1.8463183175100548e-05)*A+.0007868691311456133)*A+.014875361290850615)*A+.1369298809227358)*A+.599832206555888)*A+_B
	C=D/E
	if B<.0:C=-C
	return mu+C*F
try:from _statistics import _normal_dist_inv_cdf
except ImportError:pass
class NormalDist:
	'Normal distribution of a random variable';__slots__={'_mu':'Arithmetic mean of a normal distribution','_sigma':'Standard deviation of a normal distribution'}
	def __init__(A,mu=.0,sigma=_B):
		'NormalDist where mu is the mean and sigma is the standard deviation.';B=sigma
		if B<.0:raise StatisticsError('sigma must be non-negative')
		A._mu=float(mu);A._sigma=float(B)
	@classmethod
	def from_samples(C,data):
		'Make a normal distribution instance from sample data.';A=data
		if not isinstance(A,(list,tuple)):A=list(A)
		B=fmean(A);return C(B,stdev(A,B))
	def samples(A,n,*,seed=_A):'Generate *n* samples for a given mean and standard deviation.';B=random.gauss if seed is _A else random.Random(seed).gauss;C,D=A._mu,A._sigma;return[B(C,D)for A in range(n)]
	def pdf(B,x):
		'Probability density function.  P(x <= X < x+dx) / dx';A=B._sigma**2.
		if not A:raise StatisticsError('pdf() not defined when sigma is zero')
		return exp((x-B._mu)**2./(-2.*A))/sqrt(tau*A)
	def cdf(A,x):
		'Cumulative distribution function.  P(X <= x)'
		if not A._sigma:raise StatisticsError('cdf() not defined when sigma is zero')
		return .5*(_B+erf((x-A._mu)/(A._sigma*sqrt(2.))))
	def inv_cdf(A,p):
		'Inverse cumulative distribution function.  x : P(X <= x) = p\n\n        Finds the value of the random variable such that the probability of\n        the variable being less than or equal to that value equals the given\n        probability.\n\n        This function is also called the percent point function or quantile\n        function.\n        '
		if p<=.0 or p>=_B:raise StatisticsError('p must be in the range 0.0 < p < 1.0')
		if A._sigma<=.0:raise StatisticsError('cdf() not defined when sigma at or below zero')
		return _normal_dist_inv_cdf(p,A._mu,A._sigma)
	def quantiles(A,n=4):'Divide into *n* continuous intervals with equal probability.\n\n        Returns a list of (n - 1) cut points separating the intervals.\n\n        Set *n* to 4 for quartiles (the default).  Set *n* to 10 for deciles.\n        Set *n* to 100 for percentiles which gives the 99 cuts points that\n        separate the normal distribution in to 100 equal sized groups.\n        ';return[A.inv_cdf(B/n)for B in range(1,n)]
	def overlap(L,other):
		'Compute the overlapping coefficient (OVL) between two normal distributions.\n\n        Measures the agreement between two normal probability distributions.\n        Returns a value between 0.0 and 1.0 giving the overlapping area in\n        the two underlying probability density functions.\n\n            >>> N1 = NormalDist(2.4, 1.6)\n            >>> N2 = NormalDist(3.2, 2.0)\n            >>> N1.overlap(N2)\n            0.8035050657330205\n        ';F=other
		if not isinstance(F,NormalDist):raise TypeError('Expected another NormalDist instance')
		A,B=L,F
		if(B._sigma,B._mu)<(A._sigma,A._mu):A,B=B,A
		C,D=A.variance,B.variance
		if not C or not D:raise StatisticsError('overlap() not defined when sigma is zero')
		E=D-C;G=fabs(B._mu-A._mu)
		if not E:return _B-erf(G/(2.*A._sigma*sqrt(2.)))
		H=A._mu*D-B._mu*C;I=A._sigma*B._sigma*sqrt(G**2.+E*log(D/C));J=(H+I)/E;K=(H-I)/E;return _B-(fabs(B.cdf(J)-A.cdf(J))+fabs(B.cdf(K)-A.cdf(K)))
	def zscore(A,x):
		'Compute the Standard Score.  (x - mean) / stdev\n\n        Describes *x* in terms of the number of standard deviations\n        above or below the mean of the normal distribution.\n        '
		if not A._sigma:raise StatisticsError('zscore() not defined when sigma is zero')
		return(x-A._mu)/A._sigma
	@property
	def mean(self):'Arithmetic mean of the normal distribution.';return self._mu
	@property
	def median(self):'Return the median of the normal distribution';return self._mu
	@property
	def mode(self):'Return the mode of the normal distribution\n\n        The mode is the value x where which the probability density\n        function (pdf) takes its maximum value.\n        ';return self._mu
	@property
	def stdev(self):'Standard deviation of the normal distribution.';return self._sigma
	@property
	def variance(self):'Square of the standard deviation.';return self._sigma**2.
	def __add__(A,x2):
		'Add a constant or another NormalDist instance.\n\n        If *other* is a constant, translate mu by the constant,\n        leaving sigma unchanged.\n\n        If *other* is a NormalDist, add both the means and the variances.\n        Mathematically, this works only if the two distributions are\n        independent or if they are jointly normally distributed.\n        '
		if isinstance(x2,NormalDist):return NormalDist(A._mu+x2._mu,hypot(A._sigma,x2._sigma))
		return NormalDist(A._mu+x2,A._sigma)
	def __sub__(A,x2):
		'Subtract a constant or another NormalDist instance.\n\n        If *other* is a constant, translate by the constant mu,\n        leaving sigma unchanged.\n\n        If *other* is a NormalDist, subtract the means and add the variances.\n        Mathematically, this works only if the two distributions are\n        independent or if they are jointly normally distributed.\n        '
		if isinstance(x2,NormalDist):return NormalDist(A._mu-x2._mu,hypot(A._sigma,x2._sigma))
		return NormalDist(A._mu-x2,A._sigma)
	def __mul__(A,x2):'Multiply both mu and sigma by a constant.\n\n        Used for rescaling, perhaps to change measurement units.\n        Sigma is scaled with the absolute value of the constant.\n        ';return NormalDist(A._mu*x2,A._sigma*fabs(x2))
	def __truediv__(A,x2):'Divide both mu and sigma by a constant.\n\n        Used for rescaling, perhaps to change measurement units.\n        Sigma is scaled with the absolute value of the constant.\n        ';return NormalDist(A._mu/x2,A._sigma/fabs(x2))
	def __pos__(A):'Return a copy of the instance.';return NormalDist(A._mu,A._sigma)
	def __neg__(A):'Negates mu while keeping sigma the same.';return NormalDist(-A._mu,A._sigma)
	__radd__=__add__
	def __rsub__(A,x2):'Subtract a NormalDist from a constant or another NormalDist.';return-(A-x2)
	__rmul__=__mul__
	def __eq__(A,x2):
		'Two NormalDist objects are equal if their mu and sigma are both equal.'
		if not isinstance(x2,NormalDist):return NotImplemented
		return A._mu==x2._mu and A._sigma==x2._sigma
	def __hash__(A):'NormalDist objects hash equal if their mu and sigma are both equal.';return hash((A._mu,A._sigma))
	def __repr__(A):return f"{type(A).__name__}(mu={A._mu!r}, sigma={A._sigma!r})"