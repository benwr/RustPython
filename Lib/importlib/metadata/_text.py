import re
from._functools import method_cache
class FoldedCase(str):
	'\n    A case insensitive string class; behaves just like str\n    except compares equal when the only variation is case.\n\n    >>> s = FoldedCase(\'hello world\')\n\n    >>> s == \'Hello World\'\n    True\n\n    >>> \'Hello World\' == s\n    True\n\n    >>> s != \'Hello World\'\n    False\n\n    >>> s.index(\'O\')\n    4\n\n    >>> s.split(\'O\')\n    [\'hell\', \' w\', \'rld\']\n\n    >>> sorted(map(FoldedCase, [\'GAMMA\', \'alpha\', \'Beta\']))\n    [\'alpha\', \'Beta\', \'GAMMA\']\n\n    Sequence membership is straightforward.\n\n    >>> "Hello World" in [s]\n    True\n    >>> s in ["Hello World"]\n    True\n\n    You may test for set inclusion, but candidate and elements\n    must both be folded.\n\n    >>> FoldedCase("Hello World") in {s}\n    True\n    >>> s in {FoldedCase("Hello World")}\n    True\n\n    String inclusion works as long as the FoldedCase object\n    is on the right.\n\n    >>> "hello" in FoldedCase("Hello World")\n    True\n\n    But not if the FoldedCase object is on the left:\n\n    >>> FoldedCase(\'hello\') in \'Hello World\'\n    False\n\n    In that case, use in_:\n\n    >>> FoldedCase(\'hello\').in_(\'Hello World\')\n    True\n\n    >>> FoldedCase(\'hello\') > FoldedCase(\'Hello\')\n    False\n    '
	def __lt__(A,other):return A.lower()<other.lower()
	def __gt__(A,other):return A.lower()>other.lower()
	def __eq__(A,other):return A.lower()==other.lower()
	def __ne__(A,other):return A.lower()!=other.lower()
	def __hash__(A):return hash(A.lower())
	def __contains__(A,other):return super().lower().__contains__(other.lower())
	def in_(A,other):'Does self appear in other?';return A in FoldedCase(other)
	@method_cache
	def lower(self):return super().lower()
	def index(A,sub):return A.lower().index(sub.lower())
	def split(A,splitter=' ',maxsplit=0):B=re.compile(re.escape(splitter),re.I);return B.split(A,maxsplit)