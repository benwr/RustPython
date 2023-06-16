_A=None
from itertools import filterfalse
def unique_everseen(iterable,key=_A):
	'List unique elements, preserving order. Remember all elements ever seen.';C=iterable;B=set();D=B.add
	if key is _A:
		for A in filterfalse(B.__contains__,C):D(A);yield A
	else:
		for A in C:
			E=key(A)
			if E not in B:D(E);yield A
def always_iterable(obj,base_type=(str,bytes)):
	"If *obj* is iterable, return an iterator over its items::\n\n        >>> obj = (1, 2, 3)\n        >>> list(always_iterable(obj))\n        [1, 2, 3]\n\n    If *obj* is not iterable, return a one-item iterable containing *obj*::\n\n        >>> obj = 1\n        >>> list(always_iterable(obj))\n        [1]\n\n    If *obj* is ``None``, return an empty iterable:\n\n        >>> obj = None\n        >>> list(always_iterable(None))\n        []\n\n    By default, binary and text strings are not considered iterable::\n\n        >>> obj = 'foo'\n        >>> list(always_iterable(obj))\n        ['foo']\n\n    If *base_type* is set, objects for which ``isinstance(obj, base_type)``\n    returns ``True`` won't be considered iterable.\n\n        >>> obj = {'a': 1}\n        >>> list(always_iterable(obj))  # Iterate over the dict's keys\n        ['a']\n        >>> list(always_iterable(obj, base_type=dict))  # Treat dicts as a unit\n        [{'a': 1}]\n\n    Set *base_type* to ``None`` to avoid any special handling and treat objects\n    Python considers iterable as iterable:\n\n        >>> obj = 'foo'\n        >>> list(always_iterable(obj, base_type=None))\n        ['f', 'o', 'o']\n    ";B=base_type;A=obj
	if A is _A:return iter(())
	if B is not _A and isinstance(A,B):return iter((A,))
	try:return iter(A)
	except TypeError:return iter((A,))