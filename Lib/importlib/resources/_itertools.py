from itertools import filterfalse
from typing import Callable,Iterable,Iterator,Optional,Set,TypeVar,Union
_T=TypeVar('_T')
_U=TypeVar('_U')
def unique_everseen(iterable,key=None):
	'List unique elements, preserving order. Remember all elements ever seen.';C=iterable;B=set();D=B.add
	if key is None:
		for A in filterfalse(B.__contains__,C):D(A);yield A
	else:
		for A in C:
			E=key(A)
			if E not in B:D(E);yield A