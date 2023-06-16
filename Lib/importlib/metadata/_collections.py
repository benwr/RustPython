import collections
class FreezableDefaultDict(collections.defaultdict):
	"\n    Often it is desirable to prevent the mutation of\n    a default dict after its initial construction, such\n    as to prevent mutation during iteration.\n\n    >>> dd = FreezableDefaultDict(list)\n    >>> dd[0].append('1')\n    >>> dd.freeze()\n    >>> dd[1]\n    []\n    >>> len(dd)\n    1\n    "
	def __missing__(A,key):return getattr(A,'_frozen',super().__missing__)(key)
	def freeze(A):A._frozen=lambda key:A.default_factory()
class Pair(collections.namedtuple('Pair','name value')):
	@classmethod
	def parse(A,text):return A(*map(str.strip,text.split('=',1)))