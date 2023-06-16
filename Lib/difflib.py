'\nModule difflib -- helpers for computing deltas between objects.\n\nFunction get_close_matches(word, possibilities, n=3, cutoff=0.6):\n    Use SequenceMatcher to return list of the best "good enough" matches.\n\nFunction context_diff(a, b):\n    For two lists of strings, return a delta in context diff format.\n\nFunction ndiff(a, b):\n    Return a delta: the difference between `a` and `b` (lists of strings).\n\nFunction restore(delta, which):\n    Return one of the two sequences that generated an ndiff delta.\n\nFunction unified_diff(a, b):\n    For two lists of strings, return a delta in unified diff format.\n\nClass SequenceMatcher:\n    A flexible class for comparing pairs of sequences of any type.\n\nClass Differ:\n    For producing human-readable deltas from sequences of lines of text.\n\nClass HtmlDiff:\n    For producing HTML side by side comparison with change highlights.\n'
_S='&nbsp;'
_R='--- {}{}{}'
_Q='unknown tag %r'
_P='\t{}'
_O='+ '
_N='- '
_M='\x01'
_L='\n'
_K='insert'
_J='delete'
_I='\x00'
_H='replace'
_G='equal'
_F=False
_E='+'
_D='-'
_C=' '
_B=True
_A=None
__all__=['get_close_matches','ndiff','restore','SequenceMatcher','Differ','IS_CHARACTER_JUNK','IS_LINE_JUNK','context_diff','unified_diff','diff_bytes','HtmlDiff','Match']
from heapq import nlargest as _nlargest
from collections import namedtuple as _namedtuple
from types import GenericAlias
Match=_namedtuple('Match','a b size')
def _calculate_ratio(matches,length):
	A=length
	if A:return 2.*matches/A
	return 1.
class SequenceMatcher:
	'\n    SequenceMatcher is a flexible class for comparing pairs of sequences of\n    any type, so long as the sequence elements are hashable.  The basic\n    algorithm predates, and is a little fancier than, an algorithm\n    published in the late 1980\'s by Ratcliff and Obershelp under the\n    hyperbolic name "gestalt pattern matching".  The basic idea is to find\n    the longest contiguous matching subsequence that contains no "junk"\n    elements (R-O doesn\'t address junk).  The same idea is then applied\n    recursively to the pieces of the sequences to the left and to the right\n    of the matching subsequence.  This does not yield minimal edit\n    sequences, but does tend to yield matches that "look right" to people.\n\n    SequenceMatcher tries to compute a "human-friendly diff" between two\n    sequences.  Unlike e.g. UNIX(tm) diff, the fundamental notion is the\n    longest *contiguous* & junk-free matching subsequence.  That\'s what\n    catches peoples\' eyes.  The Windows(tm) windiff has another interesting\n    notion, pairing up elements that appear uniquely in each sequence.\n    That, and the method here, appear to yield more intuitive difference\n    reports than does diff.  This method appears to be the least vulnerable\n    to synching up on blocks of "junk lines", though (like blank lines in\n    ordinary text files, or maybe "<P>" lines in HTML files).  That may be\n    because this is the only method of the 3 that has a *concept* of\n    "junk" <wink>.\n\n    Example, comparing two strings, and considering blanks to be "junk":\n\n    >>> s = SequenceMatcher(lambda x: x == " ",\n    ...                     "private Thread currentThread;",\n    ...                     "private volatile Thread currentThread;")\n    >>>\n\n    .ratio() returns a float in [0, 1], measuring the "similarity" of the\n    sequences.  As a rule of thumb, a .ratio() value over 0.6 means the\n    sequences are close matches:\n\n    >>> print(round(s.ratio(), 3))\n    0.866\n    >>>\n\n    If you\'re only interested in where the sequences match,\n    .get_matching_blocks() is handy:\n\n    >>> for block in s.get_matching_blocks():\n    ...     print("a[%d] and b[%d] match for %d elements" % block)\n    a[0] and b[0] match for 8 elements\n    a[8] and b[17] match for 21 elements\n    a[29] and b[38] match for 0 elements\n\n    Note that the last tuple returned by .get_matching_blocks() is always a\n    dummy, (len(a), len(b), 0), and this is the only case in which the last\n    tuple element (number of elements matched) is 0.\n\n    If you want to know how to change the first sequence into the second,\n    use .get_opcodes():\n\n    >>> for opcode in s.get_opcodes():\n    ...     print("%6s a[%d:%d] b[%d:%d]" % opcode)\n     equal a[0:8] b[0:8]\n    insert a[8:8] b[8:17]\n     equal a[8:29] b[17:38]\n\n    See the Differ class for a fancy human-friendly file differencer, which\n    uses SequenceMatcher both to compare sequences of lines, and to compare\n    sequences of characters within similar (near-matching) lines.\n\n    See also function get_close_matches() in this module, which shows how\n    simple code building on SequenceMatcher can be used to do useful work.\n\n    Timing:  Basic R-O is cubic time worst case and quadratic time expected\n    case.  SequenceMatcher is quadratic time for the worst case and has\n    expected-case behavior dependent in a complicated way on how many\n    elements the sequences have in common; best case time is linear.\n\n    Methods:\n\n    __init__(isjunk=None, a=\'\', b=\'\')\n        Construct a SequenceMatcher.\n\n    set_seqs(a, b)\n        Set the two sequences to be compared.\n\n    set_seq1(a)\n        Set the first sequence to be compared.\n\n    set_seq2(b)\n        Set the second sequence to be compared.\n\n    find_longest_match(alo, ahi, blo, bhi)\n        Find longest matching block in a[alo:ahi] and b[blo:bhi].\n\n    get_matching_blocks()\n        Return list of triples describing matching subsequences.\n\n    get_opcodes()\n        Return list of 5-tuples describing how to turn a into b.\n\n    ratio()\n        Return a measure of the sequences\' similarity (float in [0,1]).\n\n    quick_ratio()\n        Return an upper bound on .ratio() relatively quickly.\n\n    real_quick_ratio()\n        Return an upper bound on ratio() very quickly.\n    '
	def __init__(A,isjunk=_A,a='',b='',autojunk=_B):'Construct a SequenceMatcher.\n\n        Optional arg isjunk is None (the default), or a one-argument\n        function that takes a sequence element and returns true iff the\n        element is junk.  None is equivalent to passing "lambda x: 0", i.e.\n        no elements are considered to be junk.  For example, pass\n            lambda x: x in " \\t"\n        if you\'re comparing lines as sequences of characters, and don\'t\n        want to synch up on blanks or hard tabs.\n\n        Optional arg a is the first of two sequences to be compared.  By\n        default, an empty string.  The elements of a must be hashable.  See\n        also .set_seqs() and .set_seq1().\n\n        Optional arg b is the second of two sequences to be compared.  By\n        default, an empty string.  The elements of b must be hashable. See\n        also .set_seqs() and .set_seq2().\n\n        Optional arg autojunk should be set to False to disable the\n        "automatic junk heuristic" that treats popular elements as junk\n        (see module documentation for more information).\n        ';A.isjunk=isjunk;A.a=A.b=_A;A.autojunk=autojunk;A.set_seqs(a,b)
	def set_seqs(A,a,b):'Set the two sequences to be compared.\n\n        >>> s = SequenceMatcher()\n        >>> s.set_seqs("abcd", "bcde")\n        >>> s.ratio()\n        0.75\n        ';A.set_seq1(a);A.set_seq2(b)
	def set_seq1(A,a):
		'Set the first sequence to be compared.\n\n        The second sequence to be compared is not changed.\n\n        >>> s = SequenceMatcher(None, "abcd", "bcde")\n        >>> s.ratio()\n        0.75\n        >>> s.set_seq1("bcde")\n        >>> s.ratio()\n        1.0\n        >>>\n\n        SequenceMatcher computes and caches detailed information about the\n        second sequence, so if you want to compare one sequence S against\n        many sequences, use .set_seq2(S) once and call .set_seq1(x)\n        repeatedly for each of the other sequences.\n\n        See also set_seqs() and set_seq2().\n        '
		if a is A.a:return
		A.a=a;A.matching_blocks=A.opcodes=_A
	def set_seq2(A,b):
		'Set the second sequence to be compared.\n\n        The first sequence to be compared is not changed.\n\n        >>> s = SequenceMatcher(None, "abcd", "bcde")\n        >>> s.ratio()\n        0.75\n        >>> s.set_seq2("abcd")\n        >>> s.ratio()\n        1.0\n        >>>\n\n        SequenceMatcher computes and caches detailed information about the\n        second sequence, so if you want to compare one sequence S against\n        many sequences, use .set_seq2(S) once and call .set_seq1(x)\n        repeatedly for each of the other sequences.\n\n        See also set_seqs() and set_seq1().\n        '
		if b is A.b:return
		A.b=b;A.matching_blocks=A.opcodes=_A;A.fullbcount=_A;A.__chain_b()
	def __chain_b(B):
		D=B.b;B.b2j=C={}
		for(I,A)in enumerate(D):J=C.setdefault(A,[]);J.append(I)
		B.bjunk=E=set();F=B.isjunk
		if F:
			for A in C.keys():
				if F(A):E.add(A)
			for A in E:del C[A]
		B.bpopular=G=set();H=len(D)
		if B.autojunk and H>=200:
			K=H//100+1
			for(A,L)in C.items():
				if len(L)>K:G.add(A)
			for A in G:del C[A]
	def find_longest_match(G,alo,ahi,blo,bhi):
		'Find longest matching block in a[alo:ahi] and b[blo:bhi].\n\n        If isjunk is not defined:\n\n        Return (i,j,k) such that a[i:i+k] is equal to b[j:j+k], where\n            alo <= i <= i+k <= ahi\n            blo <= j <= j+k <= bhi\n        and for all (i\',j\',k\') meeting those conditions,\n            k >= k\'\n            i <= i\'\n            and if i == i\', j <= j\'\n\n        In other words, of all maximal matching blocks, return one that\n        starts earliest in a, and of all those maximal matching blocks that\n        start earliest in a, return the one that starts earliest in b.\n\n        >>> s = SequenceMatcher(None, " abcd", "abcd abcd")\n        >>> s.find_longest_match(0, 5, 0, 9)\n        Match(a=0, b=4, size=5)\n\n        If isjunk is defined, first the longest matching block is\n        determined as above, but with the additional restriction that no\n        junk element appears in the block.  Then that block is extended as\n        far as possible by matching (only) junk elements on both sides.  So\n        the resulting block never matches on junk except as identical junk\n        happens to be adjacent to an "interesting" match.\n\n        Here\'s the same example as before, but considering blanks to be\n        junk.  That prevents " abcd" from matching the " abcd" at the tail\n        end of the second sequence directly.  Instead only the "abcd" can\n        match, and matches the leftmost "abcd" in the second sequence:\n\n        >>> s = SequenceMatcher(lambda x: x==" ", " abcd", "abcd abcd")\n        >>> s.find_longest_match(0, 5, 0, 9)\n        Match(a=1, b=0, size=4)\n\n        If no blocks match, return (alo, blo, 0).\n\n        >>> s = SequenceMatcher(None, "ab", "c")\n        >>> s.find_longest_match(0, 2, 0, 1)\n        Match(a=0, b=0, size=0)\n        ';L=bhi;M=ahi;H=blo;I=alo;E,D,Q,J=G.a,G.b,G.b2j,G.bjunk.__contains__;C,B,A=I,H,0;N={};R=[]
		for O in range(I,M):
			S=N.get;P={}
			for F in Q.get(E[O],R):
				if F<H:continue
				if F>=L:break
				K=P[F]=S(F-1,0)+1
				if K>A:C,B,A=O-K+1,F-K+1,K
			N=P
		while C>I and B>H and not J(D[B-1])and E[C-1]==D[B-1]:C,B,A=C-1,B-1,A+1
		while C+A<M and B+A<L and not J(D[B+A])and E[C+A]==D[B+A]:A+=1
		while C>I and B>H and J(D[B-1])and E[C-1]==D[B-1]:C,B,A=C-1,B-1,A+1
		while C+A<M and B+A<L and J(D[B+A])and E[C+A]==D[B+A]:A=A+1
		return Match(C,B,A)
	def get_matching_blocks(B):
		'Return list of triples describing matching subsequences.\n\n        Each triple is of the form (i, j, n), and means that\n        a[i:i+n] == b[j:j+n].  The triples are monotonically increasing in\n        i and in j.  New in Python 2.5, it\'s also guaranteed that if\n        (i, j, n) and (i\', j\', n\') are adjacent triples in the list, and\n        the second is not the last triple in the list, then i+n != i\' or\n        j+n != j\'.  IOW, adjacent triples never describe adjacent equal\n        blocks.\n\n        The last triple is a dummy, (len(a), len(b), 0), and is the only\n        triple with n==0.\n\n        >>> s = SequenceMatcher(None, "abxcd", "abcd")\n        >>> list(s.get_matching_blocks())\n        [Match(a=0, b=0, size=2), Match(a=3, b=2, size=2), Match(a=5, b=4, size=0)]\n        '
		if B.matching_blocks is not _A:return B.matching_blocks
		O,P=len(B.a),len(B.b);D=[(0,O,0,P)];J=[]
		while D:
			K,L,M,N=D.pop();E,F,C=T=B.find_longest_match(K,L,M,N)
			if C:
				J.append(T)
				if K<E and M<F:D.append((K,E,M,F))
				if E+C<L and F+C<N:D.append((E+C,L,F+C,N))
		J.sort();G=H=A=0;I=[]
		for(Q,R,S)in J:
			if G+A==Q and H+A==R:A+=S
			else:
				if A:I.append((G,H,A))
				G,H,A=Q,R,S
		if A:I.append((G,H,A))
		I.append((O,P,0));B.matching_blocks=list(map(Match._make,I));return B.matching_blocks
	def get_opcodes(F):
		'Return list of 5-tuples describing how to turn a into b.\n\n        Each tuple is of the form (tag, i1, i2, j1, j2).  The first tuple\n        has i1 == j1 == 0, and remaining tuples have i1 == the i2 from the\n        tuple preceding it, and likewise for j1 == the previous j2.\n\n        The tags are strings, with these meanings:\n\n        \'replace\':  a[i1:i2] should be replaced by b[j1:j2]\n        \'delete\':   a[i1:i2] should be deleted.\n                    Note that j1==j2 in this case.\n        \'insert\':   b[j1:j2] should be inserted at a[i1:i1].\n                    Note that i1==i2 in this case.\n        \'equal\':    a[i1:i2] == b[j1:j2]\n\n        >>> a = "qabxcd"\n        >>> b = "abycdf"\n        >>> s = SequenceMatcher(None, a, b)\n        >>> for tag, i1, i2, j1, j2 in s.get_opcodes():\n        ...    print(("%7s a[%d:%d] (%s) b[%d:%d] (%s)" %\n        ...           (tag, i1, i2, a[i1:i2], j1, j2, b[j1:j2])))\n         delete a[0:1] (q) b[0:0] ()\n          equal a[1:3] (ab) b[0:2] (ab)\n        replace a[3:4] (x) b[2:3] (y)\n          equal a[4:6] (cd) b[3:5] (cd)\n         insert a[6:6] () b[5:6] (f)\n        '
		if F.opcodes is not _A:return F.opcodes
		A=B=0;F.opcodes=G=[]
		for(C,D,H)in F.get_matching_blocks():
			E=''
			if A<C and B<D:E=_H
			elif A<C:E=_J
			elif B<D:E=_K
			if E:G.append((E,A,C,B,D))
			A,B=C+H,D+H
			if H:G.append((_G,C,A,D,B))
		return G
	def get_grouped_opcodes(H,n=3):
		" Isolate change clusters by eliminating ranges with no changes.\n\n        Return a generator of groups with up to n lines of context.\n        Each group is in the same format as returned by get_opcodes().\n\n        >>> from pprint import pprint\n        >>> a = list(map(str, range(1,40)))\n        >>> b = a[:]\n        >>> b[8:8] = ['i']     # Make an insertion\n        >>> b[20] += 'x'       # Make a replacement\n        >>> b[23:28] = []      # Make a deletion\n        >>> b[30] += 'y'       # Make another replacement\n        >>> pprint(list(SequenceMatcher(None,a,b).get_grouped_opcodes()))\n        [[('equal', 5, 8, 5, 8), ('insert', 8, 8, 8, 9), ('equal', 8, 11, 9, 12)],\n         [('equal', 16, 19, 17, 20),\n          ('replace', 19, 20, 20, 21),\n          ('equal', 20, 22, 21, 23),\n          ('delete', 22, 27, 23, 23),\n          ('equal', 27, 30, 23, 26)],\n         [('equal', 31, 34, 27, 30),\n          ('replace', 34, 35, 30, 31),\n          ('equal', 35, 38, 31, 34)]]\n        ";C=H.get_opcodes()
		if not C:C=[(_G,0,1,0,1)]
		if C[0][0]==_G:G,A,D,B,E=C[0];C[0]=G,max(A,D-n),D,max(B,E-n),E
		if C[-1][0]==_G:G,A,D,B,E=C[-1];C[-1]=G,A,min(D,A+n),B,min(E,B+n)
		I=n+n;F=[]
		for(G,A,D,B,E)in C:
			if G==_G and D-A>I:F.append((G,A,min(D,A+n),B,min(E,B+n)));yield F;F=[];A,B=max(A,D-n),max(B,E-n)
			F.append((G,A,D,B,E))
		if F and not(len(F)==1 and F[0][0]==_G):yield F
	def ratio(A):'Return a measure of the sequences\' similarity (float in [0,1]).\n\n        Where T is the total number of elements in both sequences, and\n        M is the number of matches, this is 2.0*M / T.\n        Note that this is 1 if the sequences are identical, and 0 if\n        they have nothing in common.\n\n        .ratio() is expensive to compute if you haven\'t already computed\n        .get_matching_blocks() or .get_opcodes(), in which case you may\n        want to try .quick_ratio() or .real_quick_ratio() first to get an\n        upper bound.\n\n        >>> s = SequenceMatcher(None, "abcd", "bcde")\n        >>> s.ratio()\n        0.75\n        >>> s.quick_ratio()\n        0.75\n        >>> s.real_quick_ratio()\n        1.0\n        ';B=sum(A[-1]for A in A.get_matching_blocks());return _calculate_ratio(B,len(A.a)+len(A.b))
	def quick_ratio(A):
		"Return an upper bound on ratio() relatively quickly.\n\n        This isn't defined beyond that it is an upper bound on .ratio(), and\n        is faster to compute.\n        "
		if A.fullbcount is _A:
			A.fullbcount=C={}
			for B in A.b:C[B]=C.get(B,0)+1
		C=A.fullbcount;D={};G,E=D.__contains__,0
		for B in A.a:
			if G(B):F=D[B]
			else:F=C.get(B,0)
			D[B]=F-1
			if F>0:E=E+1
		return _calculate_ratio(E,len(A.a)+len(A.b))
	def real_quick_ratio(A):"Return an upper bound on ratio() very quickly.\n\n        This isn't defined beyond that it is an upper bound on .ratio(), and\n        is faster to compute than either .ratio() or .quick_ratio().\n        ";B,C=len(A.a),len(A.b);return _calculate_ratio(min(B,C),B+C)
	__class_getitem__=classmethod(GenericAlias)
def get_close_matches(word,possibilities,n=3,cutoff=.6):
	'Use SequenceMatcher to return list of the best "good enough" matches.\n\n    word is a sequence for which close matches are desired (typically a\n    string).\n\n    possibilities is a list of sequences against which to match word\n    (typically a list of strings).\n\n    Optional arg n (default 3) is the maximum number of close matches to\n    return.  n must be > 0.\n\n    Optional arg cutoff (default 0.6) is a float in [0, 1].  Possibilities\n    that don\'t score at least that similar to word are ignored.\n\n    The best (no more than n) matches among the possibilities are returned\n    in a list, sorted by similarity score, most similar first.\n\n    >>> get_close_matches("appel", ["ape", "apple", "peach", "puppy"])\n    [\'apple\', \'ape\']\n    >>> import keyword as _keyword\n    >>> get_close_matches("wheel", _keyword.kwlist)\n    [\'while\']\n    >>> get_close_matches("Apple", _keyword.kwlist)\n    []\n    >>> get_close_matches("accept", _keyword.kwlist)\n    [\'except\']\n    ';B=cutoff
	if not n>0:raise ValueError('n must be > 0: %r'%(n,))
	if not .0<=B<=1.:raise ValueError('cutoff must be in [0.0, 1.0]: %r'%(B,))
	C=[];A=SequenceMatcher();A.set_seq2(word)
	for D in possibilities:
		A.set_seq1(D)
		if A.real_quick_ratio()>=B and A.quick_ratio()>=B and A.ratio()>=B:C.append((A.ratio(),D))
	C=_nlargest(n,C);return[A for(B,A)in C]
def _keep_original_ws(s,tag_s):'Replace whitespace with the original whitespace characters in `s`';return''.join(A if B==_C and A.isspace()else B for(A,B)in zip(s,tag_s))
class Differ:
	'\n    Differ is a class for comparing sequences of lines of text, and\n    producing human-readable differences or deltas.  Differ uses\n    SequenceMatcher both to compare sequences of lines, and to compare\n    sequences of characters within similar (near-matching) lines.\n\n    Each line of a Differ delta begins with a two-letter code:\n\n        \'- \'    line unique to sequence 1\n        \'+ \'    line unique to sequence 2\n        \'  \'    line common to both sequences\n        \'? \'    line not present in either input sequence\n\n    Lines beginning with \'? \' attempt to guide the eye to intraline\n    differences, and were not present in either input sequence.  These lines\n    can be confusing if the sequences contain tab characters.\n\n    Note that Differ makes no claim to produce a *minimal* diff.  To the\n    contrary, minimal diffs are often counter-intuitive, because they synch\n    up anywhere possible, sometimes accidental matches 100 pages apart.\n    Restricting synch points to contiguous matches preserves some notion of\n    locality, at the occasional cost of producing a longer diff.\n\n    Example: Comparing two texts.\n\n    First we set up the texts, sequences of individual single-line strings\n    ending with newlines (such sequences can also be obtained from the\n    `readlines()` method of file-like objects):\n\n    >>> text1 = \'\'\'  1. Beautiful is better than ugly.\n    ...   2. Explicit is better than implicit.\n    ...   3. Simple is better than complex.\n    ...   4. Complex is better than complicated.\n    ... \'\'\'.splitlines(keepends=True)\n    >>> len(text1)\n    4\n    >>> text1[0][-1]\n    \'\\n\'\n    >>> text2 = \'\'\'  1. Beautiful is better than ugly.\n    ...   3.   Simple is better than complex.\n    ...   4. Complicated is better than complex.\n    ...   5. Flat is better than nested.\n    ... \'\'\'.splitlines(keepends=True)\n\n    Next we instantiate a Differ object:\n\n    >>> d = Differ()\n\n    Note that when instantiating a Differ object we may pass functions to\n    filter out line and character \'junk\'.  See Differ.__init__ for details.\n\n    Finally, we compare the two:\n\n    >>> result = list(d.compare(text1, text2))\n\n    \'result\' is a list of strings, so let\'s pretty-print it:\n\n    >>> from pprint import pprint as _pprint\n    >>> _pprint(result)\n    [\'    1. Beautiful is better than ugly.\\n\',\n     \'-   2. Explicit is better than implicit.\\n\',\n     \'-   3. Simple is better than complex.\\n\',\n     \'+   3.   Simple is better than complex.\\n\',\n     \'?     ++\\n\',\n     \'-   4. Complex is better than complicated.\\n\',\n     \'?            ^                     ---- ^\\n\',\n     \'+   4. Complicated is better than complex.\\n\',\n     \'?           ++++ ^                      ^\\n\',\n     \'+   5. Flat is better than nested.\\n\']\n\n    As a single multi-line string it looks like this:\n\n    >>> print(\'\'.join(result), end="")\n        1. Beautiful is better than ugly.\n    -   2. Explicit is better than implicit.\n    -   3. Simple is better than complex.\n    +   3.   Simple is better than complex.\n    ?     ++\n    -   4. Complex is better than complicated.\n    ?            ^                     ---- ^\n    +   4. Complicated is better than complex.\n    ?           ++++ ^                      ^\n    +   5. Flat is better than nested.\n\n    Methods:\n\n    __init__(linejunk=None, charjunk=None)\n        Construct a text differencer, with optional filters.\n\n    compare(a, b)\n        Compare two sequences of lines; generate the resulting delta.\n    '
	def __init__(A,linejunk=_A,charjunk=_A):'\n        Construct a text differencer, with optional filters.\n\n        The two optional keyword parameters are for filter functions:\n\n        - `linejunk`: A function that should accept a single string argument,\n          and return true iff the string is junk. The module-level function\n          `IS_LINE_JUNK` may be used to filter out lines without visible\n          characters, except for at most one splat (\'#\').  It is recommended\n          to leave linejunk None; the underlying SequenceMatcher class has\n          an adaptive notion of "noise" lines that\'s better than any static\n          definition the author has ever been able to craft.\n\n        - `charjunk`: A function that should accept a string of length 1. The\n          module-level function `IS_CHARACTER_JUNK` may be used to filter out\n          whitespace characters (a blank or tab; **note**: bad idea to include\n          newline in this!).  Use of IS_CHARACTER_JUNK is recommended.\n        ';A.linejunk=linejunk;A.charjunk=charjunk
	def compare(A,a,b):
		'\n        Compare two sequences of lines; generate the resulting delta.\n\n        Each sequence must contain individual single-line strings ending with\n        newlines. Such sequences can be obtained from the `readlines()` method\n        of file-like objects.  The delta generated also consists of newline-\n        terminated strings, ready to be printed as-is via the writeline()\n        method of a file-like object.\n\n        Example:\n\n        >>> print(\'\'.join(Differ().compare(\'one\\ntwo\\nthree\\n\'.splitlines(True),\n        ...                                \'ore\\ntree\\nemu\\n\'.splitlines(True))),\n        ...       end="")\n        - one\n        ?  ^\n        + ore\n        ?  ^\n        - two\n        - three\n        ?  -\n        + tree\n        + emu\n        ';H=SequenceMatcher(A.linejunk,a,b)
		for(B,D,E,F,G)in H.get_opcodes():
			if B==_H:C=A._fancy_replace(a,D,E,b,F,G)
			elif B==_J:C=A._dump(_D,a,D,E)
			elif B==_K:C=A._dump(_E,b,F,G)
			elif B==_G:C=A._dump(_C,a,D,E)
			else:raise ValueError(_Q%(B,))
			yield from C
	def _dump(B,tag,x,lo,hi):
		'Generate comparison results for a same-tagged range.'
		for A in range(lo,hi):yield'%s %s'%(tag,x[A])
	def _plain_replace(A,a,alo,ahi,b,blo,bhi):
		B=bhi;C=blo;D=ahi;E=alo;assert E<D and C<B
		if B-C<D-E:F=A._dump(_E,b,C,B);G=A._dump(_D,a,E,D)
		else:F=A._dump(_D,a,E,D);G=A._dump(_E,b,C,B)
		for H in(F,G):yield from H
	def _fancy_replace(D,a,alo,ahi,b,blo,bhi):
		'\n        When replacing one block of lines with another, search the blocks\n        for *similar* lines; the best-matching pair (if any) is used as a\n        synch point, and intraline difference marking is done on the\n        similar pair. Lots of work, but often worth it.\n\n        Example:\n\n        >>> d = Differ()\n        >>> results = d._fancy_replace([\'abcDefghiJkl\\n\'], 0, 1,\n        ...                            [\'abcdefGhijkl\\n\'], 0, 1)\n        >>> print(\'\'.join(results), end="")\n        - abcDefghiJkl\n        ?    ^  ^  ^\n        + abcdefGhijkl\n        ?    ^  ^  ^\n        ';J=bhi;K=blo;L=ahi;M=alo;B,W=.74,.75;A=SequenceMatcher(D.charjunk);C,S=_A,_A
		for N in range(K,J):
			T=b[N];A.set_seq2(T)
			for O in range(M,L):
				U=a[O]
				if U==T:
					if C is _A:C,S=O,N
					continue
				A.set_seq1(U)
				if A.real_quick_ratio()>B and A.quick_ratio()>B and A.ratio()>B:B,F,G=A.ratio(),O,N
		if B<W:
			if C is _A:yield from D._plain_replace(a,M,L,b,K,J);return
			F,G,B=C,S,1.
		else:C=_A
		yield from D._fancy_helper(a,M,F,b,K,G);P,V=a[F],b[G]
		if C is _A:
			H=I='';A.set_seqs(P,V)
			for(E,X,Y,Z,c)in A.get_opcodes():
				Q,R=Y-X,c-Z
				if E==_H:H+='^'*Q;I+='^'*R
				elif E==_J:H+=_D*Q
				elif E==_K:I+=_E*R
				elif E==_G:H+=_C*Q;I+=_C*R
				else:raise ValueError(_Q%(E,))
			yield from D._qformat(P,V,H,I)
		else:yield'  '+P
		yield from D._fancy_helper(a,F+1,L,b,G+1,J)
	def _fancy_helper(D,a,alo,ahi,b,blo,bhi):
		E=ahi;F=alo;A=bhi;B=blo;C=[]
		if F<E:
			if B<A:C=D._fancy_replace(a,F,E,b,B,A)
			else:C=D._dump(_D,a,F,E)
		elif B<A:C=D._dump(_E,b,B,A)
		yield from C
	def _qformat(E,aline,bline,atags,btags):
		'\n        Format "?" output and deal with tabs.\n\n        Example:\n\n        >>> d = Differ()\n        >>> results = d._qformat(\'\\tabcDefghiJkl\\n\', \'\\tabcdefGhijkl\\n\',\n        ...                      \'  ^ ^  ^      \', \'  ^ ^  ^      \')\n        >>> for line in results: print(repr(line))\n        ...\n        \'- \\tabcDefghiJkl\\n\'\n        \'? \\t ^ ^  ^\\n\'\n        \'+ \\tabcdefGhijkl\\n\'\n        \'? \\t ^ ^  ^\\n\'\n        ';C=bline;D=aline;A=btags;B=atags;B=_keep_original_ws(D,B).rstrip();A=_keep_original_ws(C,A).rstrip();yield _N+D
		if B:yield f"? {B}\n"
		yield _O+C
		if A:yield f"? {A}\n"
import re
def IS_LINE_JUNK(line,pat=re.compile('\\s*(?:#\\s*)?$').match):"\n    Return True for ignorable line: iff `line` is blank or contains a single '#'.\n\n    Examples:\n\n    >>> IS_LINE_JUNK('\\n')\n    True\n    >>> IS_LINE_JUNK('  #   \\n')\n    True\n    >>> IS_LINE_JUNK('hello\\n')\n    False\n    ";return pat(line)is not _A
def IS_CHARACTER_JUNK(ch,ws=' \t'):"\n    Return True for ignorable character: iff `ch` is a space or tab.\n\n    Examples:\n\n    >>> IS_CHARACTER_JUNK(' ')\n    True\n    >>> IS_CHARACTER_JUNK('\\t')\n    True\n    >>> IS_CHARACTER_JUNK('\\n')\n    False\n    >>> IS_CHARACTER_JUNK('x')\n    False\n    ";return ch in ws
def _format_range_unified(start,stop):
	'Convert range to the "ed" format';C=start;A=C+1;B=stop-C
	if B==1:return'{}'.format(A)
	if not B:A-=1
	return'{},{}'.format(A,B)
def unified_diff(a,b,fromfile='',tofile='',fromfiledate='',tofiledate='',n=3,lineterm=_L):
	'\n    Compare two sequences of lines; generate the delta as a unified diff.\n\n    Unified diffs are a compact way of showing line changes and a few\n    lines of context.  The number of context lines is set by \'n\' which\n    defaults to three.\n\n    By default, the diff control lines (those with ---, +++, or @@) are\n    created with a trailing newline.  This is helpful so that inputs\n    created from file.readlines() result in diffs that are suitable for\n    file.writelines() since both the inputs and outputs have trailing\n    newlines.\n\n    For inputs that do not have trailing newlines, set the lineterm\n    argument to "" so that the output will be uniformly newline free.\n\n    The unidiff format normally has a header for filenames and modification\n    times.  Any or all of these may be specified using strings for\n    \'fromfile\', \'tofile\', \'fromfiledate\', and \'tofiledate\'.\n    The modification times are normally expressed in the ISO 8601 format.\n\n    Example:\n\n    >>> for line in unified_diff(\'one two three four\'.split(),\n    ...             \'zero one tree four\'.split(), \'Original\', \'Current\',\n    ...             \'2005-01-26 23:30:50\', \'2010-04-02 10:20:52\',\n    ...             lineterm=\'\'):\n    ...     print(line)                 # doctest: +NORMALIZE_WHITESPACE\n    --- Original        2005-01-26 23:30:50\n    +++ Current         2010-04-02 10:20:52\n    @@ -1,4 +1,4 @@\n    +zero\n     one\n    -two\n    -three\n    +tree\n     four\n    ';G=tofile;H=fromfile;C=tofiledate;D=fromfiledate;B=lineterm;_check_types(a,b,H,G,D,C,B);I=_F
	for E in SequenceMatcher(_A,a,b).get_grouped_opcodes(n):
		if not I:I=_B;N=_P.format(D)if D else'';O=_P.format(C)if C else'';yield _R.format(H,N,B);yield'+++ {}{}{}'.format(G,O,B)
		J,K=E[0],E[-1];P=_format_range_unified(J[1],K[2]);Q=_format_range_unified(J[3],K[4]);yield'@@ -{} +{} @@{}'.format(P,Q,B)
		for(F,L,M,R,S)in E:
			if F==_G:
				for A in a[L:M]:yield _C+A
				continue
			if F in{_H,_J}:
				for A in a[L:M]:yield _D+A
			if F in{_H,_K}:
				for A in b[R:S]:yield _E+A
def _format_range_context(start,stop):
	'Convert range to the "ed" format';C=start;A=C+1;B=stop-C
	if not B:A-=1
	if B<=1:return'{}'.format(A)
	return'{},{}'.format(A,A+B-1)
def context_diff(a,b,fromfile='',tofile='',fromfiledate='',tofiledate='',n=3,lineterm=_L):
	'\n    Compare two sequences of lines; generate the delta as a context diff.\n\n    Context diffs are a compact way of showing line changes and a few\n    lines of context.  The number of context lines is set by \'n\' which\n    defaults to three.\n\n    By default, the diff control lines (those with *** or ---) are\n    created with a trailing newline.  This is helpful so that inputs\n    created from file.readlines() result in diffs that are suitable for\n    file.writelines() since both the inputs and outputs have trailing\n    newlines.\n\n    For inputs that do not have trailing newlines, set the lineterm\n    argument to "" so that the output will be uniformly newline free.\n\n    The context diff format normally has a header for filenames and\n    modification times.  Any or all of these may be specified using\n    strings for \'fromfile\', \'tofile\', \'fromfiledate\', and \'tofiledate\'.\n    The modification times are normally expressed in the ISO 8601 format.\n    If not specified, the strings default to blanks.\n\n    Example:\n\n    >>> print(\'\'.join(context_diff(\'one\\ntwo\\nthree\\nfour\\n\'.splitlines(True),\n    ...       \'zero\\none\\ntree\\nfour\\n\'.splitlines(True), \'Original\', \'Current\')),\n    ...       end="")\n    *** Original\n    --- Current\n    ***************\n    *** 1,4 ****\n      one\n    ! two\n    ! three\n      four\n    --- 1,4 ----\n    + zero\n      one\n    ! tree\n      four\n    ';H=tofile;I=fromfile;D=tofiledate;E=fromfiledate;A=lineterm;_check_types(a,b,I,H,E,D,A);J=dict(insert=_O,delete=_N,replace='! ',equal='  ');K=_F
	for B in SequenceMatcher(_A,a,b).get_grouped_opcodes(n):
		if not K:K=_B;N=_P.format(E)if E else'';O=_P.format(D)if D else'';yield'*** {}{}{}'.format(I,N,A);yield _R.format(H,O,A)
		L,M=B[0],B[-1];yield'***************'+A;P=_format_range_context(L[1],M[2]);yield'*** {} ****{}'.format(P,A)
		if any(B in{_H,_J}for(B,A,A,A,A)in B):
			for(C,Q,R,F,F)in B:
				if C!=_K:
					for G in a[Q:R]:yield J[C]+G
		S=_format_range_context(L[3],M[4]);yield'--- {} ----{}'.format(S,A)
		if any(B in{_H,_K}for(B,A,A,A,A)in B):
			for(C,F,F,T,U)in B:
				if C!=_J:
					for G in b[T:U]:yield J[C]+G
def _check_types(a,b,*C):
	A='lines to compare must be str, not %s (%r)'
	if a and not isinstance(a[0],str):raise TypeError(A%(type(a[0]).__name__,a[0]))
	if b and not isinstance(b[0],str):raise TypeError(A%(type(b[0]).__name__,b[0]))
	for B in C:
		if not isinstance(B,str):raise TypeError('all arguments must be str, not: %r'%(B,))
def diff_bytes(dfunc,a,b,fromfile=b'',tofile=b'',fromfiledate=b'',tofiledate=b'',n=3,lineterm=b'\n'):
	'\n    Compare `a` and `b`, two sequences of lines represented as bytes rather\n    than str. This is a wrapper for `dfunc`, which is typically either\n    unified_diff() or context_diff(). Inputs are losslessly converted to\n    strings so that `dfunc` only has to worry about strings, and encoded\n    back to bytes on return. This is necessary to compare files with\n    unknown or inconsistent encoding. All other inputs (except `n`) must be\n    bytes rather than str.\n    ';G='surrogateescape';H='ascii';B=lineterm;C=tofiledate;D=fromfiledate;E=tofile;F=fromfile
	def A(s):
		try:return s.decode(H,G)
		except AttributeError as A:B='all arguments must be bytes, not %s (%r)'%(type(s).__name__,s);raise TypeError(B)from A
	a=list(map(A,a));b=list(map(A,b));F=A(F);E=A(E);D=A(D);C=A(C);B=A(B);I=dfunc(a,b,F,E,D,C,n,B)
	for J in I:yield J.encode(H,G)
def ndiff(a,b,linejunk=_A,charjunk=IS_CHARACTER_JUNK):'\n    Compare `a` and `b` (lists of strings); return a `Differ`-style delta.\n\n    Optional keyword parameters `linejunk` and `charjunk` are for filter\n    functions, or can be None:\n\n    - linejunk: A function that should accept a single string argument and\n      return true iff the string is junk.  The default is None, and is\n      recommended; the underlying SequenceMatcher class has an adaptive\n      notion of "noise" lines.\n\n    - charjunk: A function that accepts a character (string of length\n      1), and returns true iff the character is junk. The default is\n      the module-level function IS_CHARACTER_JUNK, which filters out\n      whitespace characters (a blank or tab; note: it\'s a bad idea to\n      include newline in this!).\n\n    Tools/scripts/ndiff.py is a command-line front-end to this function.\n\n    Example:\n\n    >>> diff = ndiff(\'one\\ntwo\\nthree\\n\'.splitlines(keepends=True),\n    ...              \'ore\\ntree\\nemu\\n\'.splitlines(keepends=True))\n    >>> print(\'\'.join(diff), end="")\n    - one\n    ?  ^\n    + ore\n    ?  ^\n    - two\n    - three\n    ?  -\n    + tree\n    + emu\n    ';return Differ(linejunk,charjunk).compare(a,b)
def _mdiff(fromlines,tolines,context=_A,linejunk=_A,charjunk=IS_CHARACTER_JUNK):
	'Returns generator yielding marked up from/to side by side differences.\n\n    Arguments:\n    fromlines -- list of text lines to compared to tolines\n    tolines -- list of text lines to be compared to fromlines\n    context -- number of context lines to display on each side of difference,\n               if None, all from/to text lines will be generated.\n    linejunk -- passed on to ndiff (see ndiff documentation)\n    charjunk -- passed on to ndiff (see ndiff documentation)\n\n    This function returns an iterator which returns a tuple:\n    (from line tuple, to line tuple, boolean flag)\n\n    from/to line tuple -- (line num, line text)\n        line num -- integer or None (to indicate a context separation)\n        line text -- original line text with following markers inserted:\n            \'\\0+\' -- marks start of added text\n            \'\\0-\' -- marks start of deleted text\n            \'\\0^\' -- marks start of changed text\n            \'\\1\' -- marks end of added/deleted/changed text\n\n    boolean flag -- None indicates context separation, True indicates\n        either "from" or "to" line contains a change, otherwise False.\n\n    This function/iterator was originally developed to generate side by side\n    file difference for making HTML pages (see HtmlDiff class for example\n    usage).\n\n    Note, this function utilizes the ndiff function to generate the side by\n    side difference markup.  Optional ndiff arguments may be passed to this\n    function and they in turn will be passed to ndiff.\n    ';F='?';A=context;import re;L=re.compile('(\\++|\\-+|\\^+)');M=ndiff(fromlines,tolines,linejunk,charjunk)
	def B(lines,format_key,side,num_lines=[0,0]):
		'Returns line of text with user\'s change markup and line formatting.\n\n        lines -- list of lines from the ndiff generator to produce a line of\n                 text from.  When producing the line of text to return, the\n                 lines used are removed from this list.\n        format_key -- \'+\' return first line in list with "add" markup around\n                          the entire line.\n                      \'-\' return first line in list with "delete" markup around\n                          the entire line.\n                      \'?\' return first line in list with add/delete/change\n                          intraline markup (indices obtained from second line)\n                      None return first line in list with no markup\n        side -- indice into the num_lines list (0=from,1=to)\n        num_lines -- from/to current line number.  This is NOT intended to be a\n                     passed parameter.  It is present as a keyword argument to\n                     maintain memory of the current line numbers between calls\n                     of this function.\n\n        Note, this function is purposefully not defined at the module scope so\n        that data it needs from its parent function (within whose context it\n        is defined) does not need to be of module scope.\n        ';C=num_lines;D=side;E=format_key;B=lines;C[D]+=1
		if E is _A:return C[D],B.pop(0)[2:]
		if E==F:
			A,J=B.pop(0),B.pop(0);G=[]
			def K(match_object,sub_info=G):A=match_object;sub_info.append([A.group(1)[0],A.span()]);return A.group(1)
			L.sub(K,J)
			for(M,(H,I))in reversed(G):A=A[0:H]+_I+M+A[H:I]+_M+A[I:]
			A=A[2:]
		else:
			A=B.pop(0)[2:]
			if not A:A=_C
			A=_I+E+A+_M
		return C[D],A
	def N():
		'Yields from/to lines of text with a change indication.\n\n        This function is an iterator.  It itself pulls lines from a\n        differencing iterator, processes them and yields them.  When it can\n        it yields both a "from" and a "to" line, otherwise it will yield one\n        or the other.  In addition to yielding the lines of from/to text, a\n        boolean flag is yielded to indicate if the text line(s) have\n        differences in them.\n\n        Note, this function is purposefully not defined at the module scope so\n        that data it needs from its parent function (within whose context it\n        is defined) does not need to be of module scope.\n        ';G='X';A=[];D,E=0,0
		while _B:
			while len(A)<4:A.append(next(M,G))
			C=''.join([A[0]for A in A])
			if C.startswith(G):E=D
			elif C.startswith('-?+?'):yield(B(A,F,0),B(A,F,1),_B);continue
			elif C.startswith('--++'):D-=1;yield(B(A,_D,0),_A,_B);continue
			elif C.startswith(('--?+','--+',_N)):H,I=B(A,_D,0),_A;E,D=D-1,0
			elif C.startswith('-+?'):yield(B(A,_A,0),B(A,F,1),_B);continue
			elif C.startswith('-?+'):yield(B(A,F,0),B(A,_A,1),_B);continue
			elif C.startswith(_D):D-=1;yield(B(A,_D,0),_A,_B);continue
			elif C.startswith('+--'):D+=1;yield(_A,B(A,_E,1),_B);continue
			elif C.startswith((_O,'+-')):H,I=_A,B(A,_E,1);E,D=D+1,0
			elif C.startswith(_E):D+=1;yield(_A,B(A,_E,1),_B);continue
			elif C.startswith(_C):yield(B(A[:],_A,0),B(A,_A,1),_F);continue
			while E<0:E+=1;yield(_A,('',_L),_B)
			while E>0:E-=1;yield(('',_L),_A,_B)
			if C.startswith(G):return
			else:yield(H,I,_B)
	def O():
		'Yields from/to lines of text with a change indication.\n\n        This function is an iterator.  It itself pulls lines from the line\n        iterator.  Its difference from that iterator is that this function\n        always yields a pair of from/to text lines (with the change\n        indication).  If necessary it will collect single from/to lines\n        until it has a matching pair from/to pair to yield.\n\n        Note, this function is purposefully not defined at the module scope so\n        that data it needs from its parent function (within whose context it\n        is defined) does not need to be of module scope.\n        ';F=N();C,D=[],[]
		while _B:
			while len(C)==0 or len(D)==0:
				try:A,B,E=next(F)
				except StopIteration:return
				if A is not _A:C.append((A,E))
				if B is not _A:D.append((B,E))
			A,G=C.pop(0);B,H=D.pop(0);yield(A,B,G or H)
	G=O()
	if A is _A:yield from G
	else:
		A+=1;C=0
		while _B:
			D,K=0,[_A]*A;E=_F
			while E is _F:
				try:H,I,E=next(G)
				except StopIteration:return
				J=D%A;K[J]=H,I,E;D+=1
			if D>A:yield(_A,_A,_A);C=A
			else:C=D;D=0
			while C:J=D%A;D+=1;yield K[J];C-=1
			C=A-1
			try:
				while C:
					H,I,E=next(G)
					if E:C=A-1
					else:C-=1
					yield(H,I,E)
			except StopIteration:return
_file_template='\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n\n<html>\n\n<head>\n    <meta http-equiv="Content-Type"\n          content="text/html; charset=%(charset)s" />\n    <title></title>\n    <style type="text/css">%(styles)s\n    </style>\n</head>\n\n<body>\n    %(table)s%(legend)s\n</body>\n\n</html>'
_styles='\n        table.diff {font-family:Courier; border:medium;}\n        .diff_header {background-color:#e0e0e0}\n        td.diff_header {text-align:right}\n        .diff_next {background-color:#c0c0c0}\n        .diff_add {background-color:#aaffaa}\n        .diff_chg {background-color:#ffff77}\n        .diff_sub {background-color:#ffaaaa}'
_table_template='\n    <table class="diff" id="difflib_chg_%(prefix)s_top"\n           cellspacing="0" cellpadding="0" rules="groups" >\n        <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>\n        <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>\n        %(header_row)s\n        <tbody>\n%(data_rows)s        </tbody>\n    </table>'
_legend='\n    <table class="diff" summary="Legends">\n        <tr> <th colspan="2"> Legends </th> </tr>\n        <tr> <td> <table border="" summary="Colors">\n                      <tr><th> Colors </th> </tr>\n                      <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>\n                      <tr><td class="diff_chg">Changed</td> </tr>\n                      <tr><td class="diff_sub">Deleted</td> </tr>\n                  </table></td>\n             <td> <table border="" summary="Links">\n                      <tr><th colspan="2"> Links </th> </tr>\n                      <tr><td>(f)irst change</td> </tr>\n                      <tr><td>(n)ext change</td> </tr>\n                      <tr><td>(t)op</td> </tr>\n                  </table></td> </tr>\n    </table>'
class HtmlDiff:
	'For producing HTML side by side comparison with change highlights.\n\n    This class can be used to create an HTML table (or a complete HTML file\n    containing the table) showing a side by side, line by line comparison\n    of text with inter-line and intra-line change highlights.  The table can\n    be generated in either full or contextual difference mode.\n\n    The following methods are provided for HTML generation:\n\n    make_table -- generates HTML for a single side by side table\n    make_file -- generates complete HTML file with a single side by side table\n\n    See tools/scripts/diff.py for an example usage of this class.\n    ';_file_template=_file_template;_styles=_styles;_table_template=_table_template;_legend=_legend;_default_prefix=0
	def __init__(A,tabsize=8,wrapcolumn=_A,linejunk=_A,charjunk=IS_CHARACTER_JUNK):'HtmlDiff instance initializer\n\n        Arguments:\n        tabsize -- tab stop spacing, defaults to 8.\n        wrapcolumn -- column number where lines are broken and wrapped,\n            defaults to None where lines are not wrapped.\n        linejunk,charjunk -- keyword arguments passed into ndiff() (used by\n            HtmlDiff() to generate the side by side HTML differences).  See\n            ndiff() documentation for argument default values and descriptions.\n        ';A._tabsize=tabsize;A._wrapcolumn=wrapcolumn;A._linejunk=linejunk;A._charjunk=charjunk
	def make_file(A,fromlines,tolines,fromdesc='',todesc='',context=_F,numlines=5,*,charset='utf-8'):'Returns HTML file of side by side comparison with change highlights\n\n        Arguments:\n        fromlines -- list of "from" lines\n        tolines -- list of "to" lines\n        fromdesc -- "from" file column header string\n        todesc -- "to" file column header string\n        context -- set to True for contextual differences (defaults to False\n            which shows full differences).\n        numlines -- number of context lines.  When context is set True,\n            controls number of lines displayed before and after the change.\n            When context is False, controls the number of lines to place\n            the "next" link anchors before the next change (so click of\n            "next" link jumps to just before the change).\n        charset -- charset of the HTML document\n        ';B=charset;return(A._file_template%dict(styles=A._styles,legend=A._legend,table=A.make_table(fromlines,tolines,fromdesc,todesc,context=context,numlines=numlines),charset=B)).encode(B,'xmlcharrefreplace').decode(B)
	def _tab_newline_replace(D,fromlines,tolines):
		'Returns from/to line lists with tabs expanded and newlines removed.\n\n        Instead of tab characters being replaced by the number of spaces\n        needed to fill in to the next tab stop, this function will fill\n        the space with tab characters.  This is done so that the difference\n        algorithms can identify changes in a file when tabs are replaced by\n        spaces and vice versa.  At the end of the HTML generation, the tab\n        characters will be replaced with a nonbreakable space.\n        ';A=tolines;B=fromlines
		def C(line):A=line;A=A.replace(_C,_I);A=A.expandtabs(D._tabsize);A=A.replace(_C,'\t');return A.replace(_I,_C).rstrip(_L)
		B=[C(A)for A in B];A=[C(A)for A in A];return B,A
	def _split_line(I,data_list,line_num,text):
		'Builds list of text lines by splitting text lines at wrap point\n\n        This function will determine if the input text line needs to be\n        wrapped (split) into separate lines.  If so, the first wrap point\n        will be determined and the first line appended to the output\n        text line list.  This function is used recursively to handle\n        the second part of the split line to further split it.\n        ';C=line_num;D=data_list;B=text
		if not C:D.append((C,B));return
		F=len(B);max=I._wrapcolumn
		if F<=max or F-B.count(_I)*3<=max:D.append((C,B));return
		A=0;J=0;E=''
		while J<max and A<F:
			if B[A]==_I:A+=1;E=B[A];A+=1
			elif B[A]==_M:A+=1;E=''
			else:A+=1;J+=1
		G=B[:A];H=B[A:]
		if E:G=G+_M;H=_I+E+H
		D.append((C,G));I._split_line(D,'>',H)
	def _line_wrapper(F,diffs):
		'Returns iterator that splits (wraps) mdiff text lines'
		for(A,B,E)in diffs:
			if E is _A:yield(A,B,E);continue
			(G,H),(I,J)=A,B;C,D=[],[];F._split_line(C,G,H);F._split_line(D,I,J)
			while C or D:
				if C:A=C.pop(0)
				else:A='',_C
				if D:B=D.pop(0)
				else:B='',_C
				yield(A,B,E)
	def _collect_lines(D,diffs):
		'Collects mdiff output into separate lists\n\n        Before storing the mdiff from/to data into a list, it is converted\n        into a single line of text with HTML markup.\n        ';A,B,E=[],[],[]
		for(F,G,C)in diffs:
			try:A.append(D._format_line(0,C,*F));B.append(D._format_line(1,C,*G))
			except TypeError:A.append(_A);B.append(_A)
			E.append(C)
		return A,B,E
	def _format_line(C,side,flag,linenum,text):
		'Returns HTML markup of "from" / "to" text lines\n\n        side -- 0 or 1 indicating "from" or "to" text\n        flag -- indicates if difference on line\n        linenum -- line number (used for line number column)\n        text -- line text to be marked up\n        ';B=linenum;A=text
		try:B='%d'%B;id=' id="%s%s"'%(C._prefix[side],B)
		except TypeError:id=''
		A=A.replace('&','&amp;').replace('>','&gt;').replace('<','&lt;');A=A.replace(_C,_S).rstrip();return'<td class="diff_header"%s>%s</td><td nowrap="nowrap">%s</td>'%(id,B,A)
	def _make_prefix(A):'Create unique anchor prefixes';B='from%d_'%HtmlDiff._default_prefix;C='to%d_'%HtmlDiff._default_prefix;HtmlDiff._default_prefix+=1;A._prefix=[B,C]
	def _convert_flags(K,fromlist,tolist,flaglist,context,numlines):
		'Makes list of "next" links';G=tolist;C=fromlist;A=flaglist;D=K._prefix[1];H=['']*len(A);B=['']*len(A);I,J=0,_F;E=0
		for(F,L)in enumerate(A):
			if L:
				if not J:J=_B;E=F;F=max([0,F-numlines]);H[F]=' id="difflib_chg_%s_%d"'%(D,I);I+=1;B[E]='<a href="#difflib_chg_%s_%d">n</a>'%(D,I)
			else:J=_F
		if not A:
			A=[_F];H=[''];B=[''];E=0
			if context:C=['<td></td><td>&nbsp;No Differences Found&nbsp;</td>'];G=C
			else:C=G=['<td></td><td>&nbsp;Empty File&nbsp;</td>']
		if not A[0]:B[0]='<a href="#difflib_chg_%s_0">f</a>'%D
		B[E]='<a href="#difflib_chg_%s_top">t</a>'%D;return C,G,A,B,H
	def make_table(A,fromlines,tolines,fromdesc='',todesc='',context=_F,numlines=5):
		'Returns HTML table of side by side comparison with change highlights\n\n        Arguments:\n        fromlines -- list of "from" lines\n        tolines -- list of "to" lines\n        fromdesc -- "from" file column header string\n        todesc -- "to" file column header string\n        context -- set to True for contextual differences (defaults to False\n            which shows full differences).\n        numlines -- number of context lines.  When context is set True,\n            controls number of lines displayed before and after the change.\n            When context is False, controls the number of lines to place\n            the "next" link anchors before the next change (so click of\n            "next" link jumps to just before the change).\n        ';J='<th colspan="2" class="diff_header">%s</th>';K='<th class="diff_next"><br /></th>';L=numlines;M=context;N=todesc;O=fromdesc;D=tolines;E=fromlines;A._make_prefix();E,D=A._tab_newline_replace(E,D)
		if M:P=L
		else:P=_A
		F=_mdiff(E,D,P,linejunk=A._linejunk,charjunk=A._charjunk)
		if A._wrapcolumn:F=A._line_wrapper(F)
		G,H,C=A._collect_lines(F);G,H,C,Q,S=A._convert_flags(G,H,C,M,L);I=[];T='            <tr><td class="diff_next"%s>%s</td>%s'+'<td class="diff_next">%s</td>%s</tr>\n'
		for B in range(len(C)):
			if C[B]is _A:
				if B>0:I.append('        </tbody>        \n        <tbody>\n')
			else:I.append(T%(S[B],Q[B],G[B],Q[B],H[B]))
		if O or N:R='<thead><tr>%s%s%s%s</tr></thead>'%(K,J%O,K,J%N)
		else:R=''
		U=A._table_template%dict(data_rows=''.join(I),header_row=R,prefix=A._prefix[1]);return U.replace('\x00+','<span class="diff_add">').replace('\x00-','<span class="diff_sub">').replace('\x00^','<span class="diff_chg">').replace(_M,'</span>').replace('\t',_S)
del re
def restore(delta,which):
	'\n    Generate one of the two sequences that generated a delta.\n\n    Given a `delta` produced by `Differ.compare()` or `ndiff()`, extract\n    lines originating from file 1 or 2 (parameter `which`), stripping off line\n    prefixes.\n\n    Examples:\n\n    >>> diff = ndiff(\'one\\ntwo\\nthree\\n\'.splitlines(keepends=True),\n    ...              \'ore\\ntree\\nemu\\n\'.splitlines(keepends=True))\n    >>> diff = list(diff)\n    >>> print(\'\'.join(restore(diff, 1)), end="")\n    one\n    two\n    three\n    >>> print(\'\'.join(restore(diff, 2)), end="")\n    ore\n    tree\n    emu\n    ';A=which
	try:C={1:_N,2:_O}[int(A)]
	except KeyError:raise ValueError('unknown delta choice (must be 1 or 2): %r'%A)from _A
	D='  ',C
	for B in delta:
		if B[:2]in D:yield B[2:]
def _test():import doctest as A,difflib as B;return A.testmod(B)
if __name__=='__main__':_test()