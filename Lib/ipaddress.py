'A fast, lightweight IPv4/IPv6 manipulation library in Python.\n\nThis library is used to create/poke/manipulate IPv4 and IPv6 addresses\nand networks.\n\n'
_R='fe80::/10'
_Q='_scope_id'
_P='240.0.0.0/4'
_O='127.0.0.0/8'
_N='169.254.0.0/16'
_M='%s has host bits set'
_L='__weakref__'
_K='Address cannot be empty'
_J='cannot set prefixlen_diff and new_prefix'
_I='%s(%r)'
_H='100.64.0.0/10'
_G='%s in %r'
_F='%s/%d'
_E='%s and %s are not of the same version'
_D='big'
_C='%s/%s'
_B=False
_A=None
__version__='1.0'
import functools
IPV4LENGTH=32
IPV6LENGTH=128
class AddressValueError(ValueError):'A Value Error related to the address.'
class NetmaskValueError(ValueError):'A Value Error related to the netmask.'
def ip_address(address):
	"Take an IP string/int and return an object of the correct type.\n\n    Args:\n        address: A string or integer, the IP address.  Either IPv4 or\n          IPv6 addresses may be supplied; integers less than 2**32 will\n          be considered to be IPv4 by default.\n\n    Returns:\n        An IPv4Address or IPv6Address object.\n\n    Raises:\n        ValueError: if the *address* passed isn't either a v4 or a v6\n          address\n\n    ";A=address
	try:return IPv4Address(A)
	except(AddressValueError,NetmaskValueError):pass
	try:return IPv6Address(A)
	except(AddressValueError,NetmaskValueError):pass
	raise ValueError(f"{A!r} does not appear to be an IPv4 or IPv6 address")
def ip_network(address,strict=True):
	"Take an IP string/int and return an object of the correct type.\n\n    Args:\n        address: A string or integer, the IP network.  Either IPv4 or\n          IPv6 networks may be supplied; integers less than 2**32 will\n          be considered to be IPv4 by default.\n\n    Returns:\n        An IPv4Network or IPv6Network object.\n\n    Raises:\n        ValueError: if the string passed isn't either a v4 or a v6\n          address. Or if the network has host bits set.\n\n    ";B=strict;A=address
	try:return IPv4Network(A,B)
	except(AddressValueError,NetmaskValueError):pass
	try:return IPv6Network(A,B)
	except(AddressValueError,NetmaskValueError):pass
	raise ValueError(f"{A!r} does not appear to be an IPv4 or IPv6 network")
def ip_interface(address):
	"Take an IP string/int and return an object of the correct type.\n\n    Args:\n        address: A string or integer, the IP address.  Either IPv4 or\n          IPv6 addresses may be supplied; integers less than 2**32 will\n          be considered to be IPv4 by default.\n\n    Returns:\n        An IPv4Interface or IPv6Interface object.\n\n    Raises:\n        ValueError: if the string passed isn't either a v4 or a v6\n          address.\n\n    Notes:\n        The IPv?Interface classes describe an Address on a particular\n        Network, so they're basically a combination of both the Address\n        and Network classes.\n\n    ";A=address
	try:return IPv4Interface(A)
	except(AddressValueError,NetmaskValueError):pass
	try:return IPv6Interface(A)
	except(AddressValueError,NetmaskValueError):pass
	raise ValueError(f"{A!r} does not appear to be an IPv4 or IPv6 interface")
def v4_int_to_packed(address):
	'Represent an address as 4 packed bytes in network (big-endian) order.\n\n    Args:\n        address: An integer representation of an IPv4 IP address.\n\n    Returns:\n        The integer address packed as 4 bytes in network (big-endian) order.\n\n    Raises:\n        ValueError: If the integer is negative or too large to be an\n          IPv4 IP address.\n\n    '
	try:return address.to_bytes(4,_D)
	except OverflowError:raise ValueError('Address negative or too large for IPv4')
def v6_int_to_packed(address):
	'Represent an address as 16 packed bytes in network (big-endian) order.\n\n    Args:\n        address: An integer representation of an IPv6 IP address.\n\n    Returns:\n        The integer address packed as 16 bytes in network (big-endian) order.\n\n    '
	try:return address.to_bytes(16,_D)
	except OverflowError:raise ValueError('Address negative or too large for IPv6')
def _split_optional_netmask(address):
	'Helper to split the netmask and raise AddressValueError if needed';A=address;B=str(A).split('/')
	if len(B)>2:raise AddressValueError(f"Only one '/' permitted in {A!r}")
	return B
def _find_address_range(addresses):
	'Find a sequence of sorted deduplicated IPv#Address.\n\n    Args:\n        addresses: a list of IPv#Address objects.\n\n    Yields:\n        A tuple containing the first and last IP addresses in the sequence.\n\n    ';D=iter(addresses);B=A=next(D)
	for C in D:
		if C._ip!=A._ip+1:yield(B,A);B=C
		A=C
	yield(B,A)
def _count_righthand_zero_bits(number,bits):
	'Count the number of zero bits on the right hand side.\n\n    Args:\n        number: an integer.\n        bits: maximum number of bits to count.\n\n    Returns:\n        The number of zero bits on the right hand side of the number.\n\n    ';A=number
	if A==0:return bits
	return min(bits,(~A&A-1).bit_length())
def summarize_address_range(first,last):
	"Summarize a network range given the first and last IP addresses.\n\n    Example:\n        >>> list(summarize_address_range(IPv4Address('192.0.2.0'),\n        ...                              IPv4Address('192.0.2.130')))\n        ...                                #doctest: +NORMALIZE_WHITESPACE\n        [IPv4Network('192.0.2.0/25'), IPv4Network('192.0.2.128/31'),\n         IPv4Network('192.0.2.130/32')]\n\n    Args:\n        first: the first IPv4Address or IPv6Address in the range.\n        last: the last IPv4Address or IPv6Address in the range.\n\n    Returns:\n        An iterator of the summarized IPv(4|6) network objects.\n\n    Raise:\n        TypeError:\n            If the first and last objects are not IP addresses.\n            If the first and last objects are not the same version.\n        ValueError:\n            If the last object is not greater than the first.\n            If the version of the first address is not 4 or 6.\n\n    ";C=last;A=first
	if not(isinstance(A,_BaseAddress)and isinstance(C,_BaseAddress)):raise TypeError('first and last must be IP addresses, not networks')
	if A.version!=C.version:raise TypeError(_E%(A,C))
	if A>C:raise ValueError('last IP address must be greater than first')
	if A.version==4:D=IPv4Network
	elif A.version==6:D=IPv6Network
	else:raise ValueError('unknown IP version')
	E=A._max_prefixlen;B=A._ip;F=C._ip
	while B<=F:
		G=min(_count_righthand_zero_bits(B,E),(F-B+1).bit_length()-1);H=D((B,E-G));yield H;B+=1<<G
		if B-1==D._ALL_ONES:break
def _collapse_addresses_internal(addresses):
	"Loops through the addresses, collapsing concurrent netblocks.\n\n    Example:\n\n        ip1 = IPv4Network('192.0.2.0/26')\n        ip2 = IPv4Network('192.0.2.64/26')\n        ip3 = IPv4Network('192.0.2.128/26')\n        ip4 = IPv4Network('192.0.2.192/26')\n\n        _collapse_addresses_internal([ip1, ip2, ip3, ip4]) ->\n          [IPv4Network('192.0.2.0/24')]\n\n        This shouldn't be called directly; it is called via\n          collapse_addresses([]).\n\n    Args:\n        addresses: A list of IPv4Network's or IPv6Network's\n\n    Returns:\n        A list of IPv4Network's or IPv6Network's depending on what we were\n        passed.\n\n    ";D=list(addresses);B={}
	while D:
		A=D.pop();C=A.supernet();F=B.get(C)
		if F is _A:B[C]=A
		elif F!=A:del B[C];D.append(C)
	E=_A
	for A in sorted(B.values()):
		if E is not _A:
			if E.broadcast_address>=A.broadcast_address:continue
		yield A;E=A
def collapse_addresses(addresses):
	"Collapse a list of IP objects.\n\n    Example:\n        collapse_addresses([IPv4Network('192.0.2.0/25'),\n                            IPv4Network('192.0.2.128/25')]) ->\n                           [IPv4Network('192.0.2.0/24')]\n\n    Args:\n        addresses: An iterator of IPv4Network or IPv6Network objects.\n\n    Returns:\n        An iterator of the collapsed IPv(4|6)Network objects.\n\n    Raises:\n        TypeError: If passed a list of mixed version objects.\n\n    ";D=[];A=[];C=[]
	for B in addresses:
		if isinstance(B,_BaseAddress):
			if A and A[-1]._version!=B._version:raise TypeError(_E%(B,A[-1]))
			A.append(B)
		elif B._prefixlen==B._max_prefixlen:
			if A and A[-1]._version!=B._version:raise TypeError(_E%(B,A[-1]))
			try:A.append(B.ip)
			except AttributeError:A.append(B.network_address)
		else:
			if C and C[-1]._version!=B._version:raise TypeError(_E%(B,C[-1]))
			C.append(B)
	A=sorted(set(A))
	if A:
		for(E,F)in _find_address_range(A):D.extend(summarize_address_range(E,F))
	return _collapse_addresses_internal(D+C)
def get_mixed_type_key(obj):
	"Return a key suitable for sorting between networks and addresses.\n\n    Address and Network objects are not sortable by default; they're\n    fundamentally different so the expression\n\n        IPv4Address('192.0.2.0') <= IPv4Network('192.0.2.0/24')\n\n    doesn't make any sense.  There are some times however, where you may wish\n    to have ipaddress sort these for you anyway. If you need to do this, you\n    can use this function as the key= argument to sorted().\n\n    Args:\n      obj: either a Network or Address object.\n    Returns:\n      appropriate key.\n\n    ";A=obj
	if isinstance(A,_BaseNetwork):return A._get_networks_key()
	elif isinstance(A,_BaseAddress):return A._get_address_key()
	return NotImplemented
class _IPAddressBase:
	'The mother class.';__slots__=()
	@property
	def exploded(self):'Return the longhand version of the IP address as a string.';return self._explode_shorthand_ip_string()
	@property
	def compressed(self):'Return the shorthand version of the IP address as a string.';return str(self)
	@property
	def reverse_pointer(self):'The name of the reverse DNS pointer for the IP address, e.g.:\n            >>> ipaddress.ip_address("127.0.0.1").reverse_pointer\n            \'1.0.0.127.in-addr.arpa\'\n            >>> ipaddress.ip_address("2001:db8::1").reverse_pointer\n            \'1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa\'\n\n        ';return self._reverse_pointer()
	@property
	def version(self):A='%200s has no version specified'%(type(self),);raise NotImplementedError(A)
	def _check_int_address(A,address):
		B=address
		if B<0:C='%d (< 0) is not permitted as an IPv%d address';raise AddressValueError(C%(B,A._version))
		if B>A._ALL_ONES:C='%d (>= 2**%d) is not permitted as an IPv%d address';raise AddressValueError(C%(B,A._max_prefixlen,A._version))
	def _check_packed_address(D,address,expected_len):
		A=expected_len;B=address;C=len(B)
		if C!=A:E='%r (len %d != %d) is not permitted as an IPv%d address';raise AddressValueError(E%(B,C,A,D._version))
	@classmethod
	def _ip_int_from_prefix(A,prefixlen):'Turn the prefix length into a bitwise netmask\n\n        Args:\n            prefixlen: An integer, the prefix length.\n\n        Returns:\n            An integer.\n\n        ';return A._ALL_ONES^A._ALL_ONES>>prefixlen
	@classmethod
	def _prefix_from_ip_int(A,ip_int):
		'Return prefix length from the bitwise netmask.\n\n        Args:\n            ip_int: An integer, the netmask in expanded bitwise format\n\n        Returns:\n            An integer, the prefix length.\n\n        Raises:\n            ValueError: If the input intermingles zeroes & ones\n        ';B=ip_int;C=_count_righthand_zero_bits(B,A._max_prefixlen);D=A._max_prefixlen-C;E=B>>C;F=(1<<D)-1
		if E!=F:G=A._max_prefixlen//8;H=B.to_bytes(G,_D);I='Netmask pattern %r mixes zeroes & ones';raise ValueError(I%H)
		return D
	@classmethod
	def _report_invalid_netmask(B,netmask_str):A='%r is not a valid netmask'%netmask_str;raise NetmaskValueError(A)from _A
	@classmethod
	def _prefix_from_prefix_string(B,prefixlen_str):
		'Return prefix length from a numeric string\n\n        Args:\n            prefixlen_str: The string to be converted\n\n        Returns:\n            An integer, the prefix length.\n\n        Raises:\n            NetmaskValueError: If the input is not a valid netmask\n        ';A=prefixlen_str
		if not(A.isascii()and A.isdigit()):B._report_invalid_netmask(A)
		try:C=int(A)
		except ValueError:B._report_invalid_netmask(A)
		if not 0<=C<=B._max_prefixlen:B._report_invalid_netmask(A)
		return C
	@classmethod
	def _prefix_from_ip_string(A,ip_str):
		'Turn a netmask/hostmask string into a prefix length\n\n        Args:\n            ip_str: The netmask/hostmask to be converted\n\n        Returns:\n            An integer, the prefix length.\n\n        Raises:\n            NetmaskValueError: If the input is not a valid netmask/hostmask\n        ';B=ip_str
		try:C=A._ip_int_from_string(B)
		except AddressValueError:A._report_invalid_netmask(B)
		try:return A._prefix_from_ip_int(C)
		except ValueError:pass
		C^=A._ALL_ONES
		try:return A._prefix_from_ip_int(C)
		except ValueError:A._report_invalid_netmask(B)
	@classmethod
	def _split_addr_prefix(B,address):
		'Helper function to parse address of Network/Interface.\n\n        Arg:\n            address: Argument of Network/Interface.\n\n        Returns:\n            (addr, prefix) tuple.\n        ';A=address
		if isinstance(A,(bytes,int)):return A,B._max_prefixlen
		if not isinstance(A,tuple):A=_split_optional_netmask(A)
		if len(A)>1:return A
		return A[0],B._max_prefixlen
	def __reduce__(A):return A.__class__,(str(A),)
_address_fmt_re=_A
@functools.total_ordering
class _BaseAddress(_IPAddressBase):
	'A generic IP object.\n\n    This IP class contains the version independent methods which are\n    used by single IP addresses.\n    ';__slots__=()
	def __int__(A):return A._ip
	def __eq__(A,other):
		B=other
		try:return A._ip==B._ip and A._version==B._version
		except AttributeError:return NotImplemented
	def __lt__(B,other):
		A=other
		if not isinstance(A,_BaseAddress):return NotImplemented
		if B._version!=A._version:raise TypeError(_E%(B,A))
		if B._ip!=A._ip:return B._ip<A._ip
		return _B
	def __add__(A,other):
		B=other
		if not isinstance(B,int):return NotImplemented
		return A.__class__(int(A)+B)
	def __sub__(A,other):
		B=other
		if not isinstance(B,int):return NotImplemented
		return A.__class__(int(A)-B)
	def __repr__(A):return _I%(A.__class__.__name__,str(A))
	def __str__(A):return str(A._string_from_ip_int(A._ip))
	def __hash__(A):return hash(hex(int(A._ip)))
	def _get_address_key(A):return A._version,A
	def __reduce__(A):return A.__class__,(A._ip,)
	def __format__(A,fmt):
		"Returns an IP address as a formatted string.\n\n        Supported presentation types are:\n        's': returns the IP address as a string (default)\n        'b': converts to binary and returns a zero-padded string\n        'X' or 'x': converts to upper- or lower-case hex and returns a zero-padded string\n        'n': the same as 'b' for IPv4 and 'x' for IPv6\n\n        For binary and hex presentation types, the alternate form specifier\n        '#' and the grouping option '_' are supported.\n        ";B=fmt
		if not B or B[-1]=='s':return format(str(A),B)
		global _address_fmt_re
		if _address_fmt_re is _A:import re;_address_fmt_re=re.compile('(#?)(_?)([xbnX])')
		E=_address_fmt_re.fullmatch(B)
		if not E:return super().__format__(B)
		F,G,C=E.groups()
		if C=='n':
			if A._version==4:C='b'
			else:C='x'
		if C=='b':D=A._max_prefixlen
		else:D=A._max_prefixlen//4
		if G:D+=D//4-1
		if F:D+=2
		return format(int(A),f"{F}0{D}{G}{C}")
@functools.total_ordering
class _BaseNetwork(_IPAddressBase):
	'A generic IP network object.\n\n    This IP class contains the version independent methods which are\n    used by networks.\n    '
	def __repr__(A):return _I%(A.__class__.__name__,str(A))
	def __str__(A):return _F%(A.network_address,A.prefixlen)
	def hosts(A):
		"Generate Iterator over usable hosts in a network.\n\n        This is like __iter__ except it doesn't return the network\n        or broadcast addresses.\n\n        ";B=int(A.network_address);C=int(A.broadcast_address)
		for D in range(B+1,C):yield A._address_class(D)
	def __iter__(A):
		B=int(A.network_address);C=int(A.broadcast_address)
		for D in range(B,C+1):yield A._address_class(D)
	def __getitem__(A,n):
		D='address out of range';B=int(A.network_address);C=int(A.broadcast_address)
		if n>=0:
			if B+n>C:raise IndexError(D)
			return A._address_class(B+n)
		else:
			n+=1
			if C+n<B:raise IndexError(D)
			return A._address_class(C+n)
	def __lt__(B,other):
		A=other
		if not isinstance(A,_BaseNetwork):return NotImplemented
		if B._version!=A._version:raise TypeError(_E%(B,A))
		if B.network_address!=A.network_address:return B.network_address<A.network_address
		if B.netmask!=A.netmask:return B.netmask<A.netmask
		return _B
	def __eq__(A,other):
		B=other
		try:return A._version==B._version and A.network_address==B.network_address and int(A.netmask)==int(B.netmask)
		except AttributeError:return NotImplemented
	def __hash__(A):return hash(int(A.network_address)^int(A.netmask))
	def __contains__(A,other):
		B=other
		if A._version!=B._version:return _B
		if isinstance(B,_BaseNetwork):return _B
		else:return B._ip&A.netmask._ip==A.network_address._ip
	def overlaps(A,other):'Tell if self is partly contained in other.';B=other;return A.network_address in B or(A.broadcast_address in B or(B.network_address in A or B.broadcast_address in A))
	@functools.cached_property
	def broadcast_address(self):A=self;return A._address_class(int(A.network_address)|int(A.hostmask))
	@functools.cached_property
	def hostmask(self):A=self;return A._address_class(int(A.netmask)^A._ALL_ONES)
	@property
	def with_prefixlen(self):return _F%(self.network_address,self._prefixlen)
	@property
	def with_netmask(self):return _C%(self.network_address,self.netmask)
	@property
	def with_hostmask(self):return _C%(self.network_address,self.hostmask)
	@property
	def num_addresses(self):'Number of hosts in the current subnet.';return int(self.broadcast_address)-int(self.network_address)+1
	@property
	def _address_class(self):A='%200s has no associated address class'%(type(self),);raise NotImplementedError(A)
	@property
	def prefixlen(self):return self._prefixlen
	def address_exclude(D,other):
		"Remove an address from a larger block.\n\n        For example:\n\n            addr1 = ip_network('192.0.2.0/28')\n            addr2 = ip_network('192.0.2.1/32')\n            list(addr1.address_exclude(addr2)) =\n                [IPv4Network('192.0.2.0/32'), IPv4Network('192.0.2.2/31'),\n                 IPv4Network('192.0.2.4/30'), IPv4Network('192.0.2.8/29')]\n\n        or IPv6:\n\n            addr1 = ip_network('2001:db8::1/32')\n            addr2 = ip_network('2001:db8::1/128')\n            list(addr1.address_exclude(addr2)) =\n                [ip_network('2001:db8::1/128'),\n                 ip_network('2001:db8::2/127'),\n                 ip_network('2001:db8::4/126'),\n                 ip_network('2001:db8::8/125'),\n                 ...\n                 ip_network('2001:db8:8000::/33')]\n\n        Args:\n            other: An IPv4Network or IPv6Network object of the same type.\n\n        Returns:\n            An iterator of the IPv(4|6)Network objects which is self\n            minus other.\n\n        Raises:\n            TypeError: If self and other are of differing address\n              versions, or if other is not a network object.\n            ValueError: If other is not completely contained by self.\n\n        ";E='Error performing exclusion: s1: %s s2: %s other: %s';A=other
		if not D._version==A._version:raise TypeError(_E%(D,A))
		if not isinstance(A,_BaseNetwork):raise TypeError('%s is not a network object'%A)
		if not A.subnet_of(D):raise ValueError('%s not contained in %s'%(A,D))
		if A==D:return
		A=A.__class__(_C%(A.network_address,A.prefixlen));B,C=D.subnets()
		while B!=A and C!=A:
			if A.subnet_of(B):yield C;B,C=B.subnets()
			elif A.subnet_of(C):yield B;B,C=C.subnets()
			else:raise AssertionError(E%(B,C,A))
		if B==A:yield C
		elif C==A:yield B
		else:raise AssertionError(E%(B,C,A))
	def compare_networks(A,other):
		"Compare two IP objects.\n\n        This is only concerned about the comparison of the integer\n        representation of the network addresses.  This means that the\n        host bits aren't considered at all in this method.  If you want\n        to compare host bits, you can easily enough do a\n        'HostA._ip < HostB._ip'\n\n        Args:\n            other: An IP object.\n\n        Returns:\n            If the IP versions of self and other are the same, returns:\n\n            -1 if self < other:\n              eg: IPv4Network('192.0.2.0/25') < IPv4Network('192.0.2.128/25')\n              IPv6Network('2001:db8::1000/124') <\n                  IPv6Network('2001:db8::2000/124')\n            0 if self == other\n              eg: IPv4Network('192.0.2.0/24') == IPv4Network('192.0.2.0/24')\n              IPv6Network('2001:db8::1000/124') ==\n                  IPv6Network('2001:db8::1000/124')\n            1 if self > other\n              eg: IPv4Network('192.0.2.128/25') > IPv4Network('192.0.2.0/25')\n                  IPv6Network('2001:db8::2000/124') >\n                      IPv6Network('2001:db8::1000/124')\n\n          Raises:\n              TypeError if the IP versions are different.\n\n        ";B=other
		if A._version!=B._version:raise TypeError('%s and %s are not of the same type'%(A,B))
		if A.network_address<B.network_address:return-1
		if A.network_address>B.network_address:return 1
		if A.netmask<B.netmask:return-1
		if A.netmask>B.netmask:return 1
		return 0
	def _get_networks_key(A):'Network-only key function.\n\n        Returns an object that identifies this address\' network and\n        netmask. This function is a suitable "key" argument for sorted()\n        and list.sort().\n\n        ';return A._version,A.network_address,A.netmask
	def subnets(A,prefixlen_diff=1,new_prefix=_A):
		'The subnets which join to make the current subnet.\n\n        In the case that self contains only one IP\n        (self._prefixlen == 32 for IPv4 or self._prefixlen == 128\n        for IPv6), yield an iterator with just ourself.\n\n        Args:\n            prefixlen_diff: An integer, the amount the prefix length\n              should be increased by. This should not be set if\n              new_prefix is also set.\n            new_prefix: The desired new prefix length. This must be a\n              larger number (smaller prefix) than the existing prefix.\n              This should not be set if prefixlen_diff is also set.\n\n        Returns:\n            An iterator of IPv(4|6) objects.\n\n        Raises:\n            ValueError: The prefixlen_diff is too small or too large.\n                OR\n            prefixlen_diff and new_prefix are both set or new_prefix\n              is a smaller number than the current prefix (smaller\n              number means a larger network)\n\n        ';C=new_prefix;B=prefixlen_diff
		if A._prefixlen==A._max_prefixlen:yield A;return
		if C is not _A:
			if C<A._prefixlen:raise ValueError('new prefix must be longer')
			if B!=1:raise ValueError(_J)
			B=C-A._prefixlen
		if B<0:raise ValueError('prefix length diff must be > 0')
		D=A._prefixlen+B
		if D>A._max_prefixlen:raise ValueError('prefix length diff %d is invalid for netblock %s'%(D,A))
		E=int(A.network_address);F=int(A.broadcast_address)+1;G=int(A.hostmask)+1>>B
		for H in range(E,F,G):I=A.__class__((H,D));yield I
	def supernet(A,prefixlen_diff=1,new_prefix=_A):
		'The supernet containing the current network.\n\n        Args:\n            prefixlen_diff: An integer, the amount the prefix length of\n              the network should be decreased by.  For example, given a\n              /24 network and a prefixlen_diff of 3, a supernet with a\n              /21 netmask is returned.\n\n        Returns:\n            An IPv4 network object.\n\n        Raises:\n            ValueError: If self.prefixlen - prefixlen_diff < 0. I.e., you have\n              a negative prefix length.\n                OR\n            If prefixlen_diff and new_prefix are both set or new_prefix is a\n              larger number than the current prefix (larger number means a\n              smaller network)\n\n        ';C=new_prefix;B=prefixlen_diff
		if A._prefixlen==0:return A
		if C is not _A:
			if C>A._prefixlen:raise ValueError('new prefix must be shorter')
			if B!=1:raise ValueError(_J)
			B=A._prefixlen-C
		D=A.prefixlen-B
		if D<0:raise ValueError('current prefixlen is %d, cannot have a prefixlen_diff of %d'%(A.prefixlen,B))
		return A.__class__((int(A.network_address)&int(A.netmask)<<B,D))
	@property
	def is_multicast(self):'Test if the address is reserved for multicast use.\n\n        Returns:\n            A boolean, True if the address is a multicast address.\n            See RFC 2373 2.7 for details.\n\n        ';return self.network_address.is_multicast and self.broadcast_address.is_multicast
	@staticmethod
	def _is_subnet_of(a,b):
		try:
			if a._version!=b._version:raise TypeError(f"{a} and {b} are not of the same version")
			return b.network_address<=a.network_address and b.broadcast_address>=a.broadcast_address
		except AttributeError:raise TypeError(f"Unable to test subnet containment between {a} and {b}")
	def subnet_of(A,other):'Return True if this network is a subnet of other.';return A._is_subnet_of(A,other)
	def supernet_of(A,other):'Return True if this network is a supernet of other.';return A._is_subnet_of(other,A)
	@property
	def is_reserved(self):'Test if the address is otherwise IETF reserved.\n\n        Returns:\n            A boolean, True if the address is within one of the\n            reserved IPv6 Network ranges.\n\n        ';return self.network_address.is_reserved and self.broadcast_address.is_reserved
	@property
	def is_link_local(self):'Test if the address is reserved for link-local.\n\n        Returns:\n            A boolean, True if the address is reserved per RFC 4291.\n\n        ';return self.network_address.is_link_local and self.broadcast_address.is_link_local
	@property
	def is_private(self):'Test if this address is allocated for private networks.\n\n        Returns:\n            A boolean, True if the address is reserved per\n            iana-ipv4-special-registry or iana-ipv6-special-registry.\n\n        ';return self.network_address.is_private and self.broadcast_address.is_private
	@property
	def is_global(self):'Test if this address is allocated for public networks.\n\n        Returns:\n            A boolean, True if the address is not reserved per\n            iana-ipv4-special-registry or iana-ipv6-special-registry.\n\n        ';return not self.is_private
	@property
	def is_unspecified(self):'Test if the address is unspecified.\n\n        Returns:\n            A boolean, True if this is the unspecified address as defined in\n            RFC 2373 2.5.2.\n\n        ';return self.network_address.is_unspecified and self.broadcast_address.is_unspecified
	@property
	def is_loopback(self):'Test if the address is a loopback address.\n\n        Returns:\n            A boolean, True if the address is a loopback address as defined in\n            RFC 2373 2.5.3.\n\n        ';return self.network_address.is_loopback and self.broadcast_address.is_loopback
class _BaseV4:
	'Base IPv4 object.\n\n    The following methods are used by IPv4 objects in both single IP\n    addresses and networks.\n\n    ';__slots__=();_version=4;_ALL_ONES=2**IPV4LENGTH-1;_max_prefixlen=IPV4LENGTH;_netmask_cache={}
	def _explode_shorthand_ip_string(A):return str(A)
	@classmethod
	def _make_netmask(A,arg):
		'Make a (netmask, prefix_len) tuple from the given argument.\n\n        Argument can be:\n        - an integer (the prefix length)\n        - a string representing the prefix length (e.g. "24")\n        - a string representing the prefix netmask (e.g. "255.255.255.0")\n        ';B=arg
		if B not in A._netmask_cache:
			if isinstance(B,int):
				C=B
				if not 0<=C<=A._max_prefixlen:A._report_invalid_netmask(C)
			else:
				try:C=A._prefix_from_prefix_string(B)
				except NetmaskValueError:C=A._prefix_from_ip_string(B)
			D=IPv4Address(A._ip_int_from_prefix(C));A._netmask_cache[B]=D,C
		return A._netmask_cache[B]
	@classmethod
	def _ip_int_from_string(C,ip_str):
		"Turn the given IP string into an integer for comparison.\n\n        Args:\n            ip_str: A string, the IP ip_str.\n\n        Returns:\n            The IP ip_str as an integer.\n\n        Raises:\n            AddressValueError: if ip_str isn't a valid IPv4 Address.\n\n        ";A=ip_str
		if not A:raise AddressValueError(_K)
		B=A.split('.')
		if len(B)!=4:raise AddressValueError('Expected 4 octets in %r'%A)
		try:return int.from_bytes(map(C._parse_octet,B),_D)
		except ValueError as D:raise AddressValueError(_G%(D,A))from _A
	@classmethod
	def _parse_octet(D,octet_str):
		"Convert a decimal octet into an integer.\n\n        Args:\n            octet_str: A string, the number to parse.\n\n        Returns:\n            The octet as an integer.\n\n        Raises:\n            ValueError: if the octet isn't strictly a decimal from [0..255].\n\n        ";A=octet_str
		if not A:raise ValueError('Empty octet not permitted')
		if not(A.isascii()and A.isdigit()):B='Only decimal digits permitted in %r';raise ValueError(B%A)
		if len(A)>3:B='At most 3 characters permitted in %r';raise ValueError(B%A)
		if A!='0'and A[0]=='0':B='Leading zeros are not permitted in %r';raise ValueError(B%A)
		C=int(A,10)
		if C>255:raise ValueError('Octet %d (> 255) not permitted'%C)
		return C
	@classmethod
	def _string_from_ip_int(A,ip_int):'Turns a 32-bit integer into dotted decimal notation.\n\n        Args:\n            ip_int: An integer, the IP address.\n\n        Returns:\n            The IP address as a string in dotted decimal notation.\n\n        ';return'.'.join(map(str,ip_int.to_bytes(4,_D)))
	def _reverse_pointer(A):'Return the reverse DNS pointer name for the IPv4 address.\n\n        This implements the method described in RFC1035 3.5.\n\n        ';B=str(A).split('.')[::-1];return'.'.join(B)+'.in-addr.arpa'
	@property
	def max_prefixlen(self):return self._max_prefixlen
	@property
	def version(self):return self._version
class IPv4Address(_BaseV4,_BaseAddress):
	'Represent and manipulate single IPv4 Addresses.';__slots__='_ip',_L
	def __init__(B,address):
		"\n        Args:\n            address: A string or integer representing the IP\n\n              Additionally, an integer can be passed, so\n              IPv4Address('192.0.2.1') == IPv4Address(3221225985).\n              or, more generally\n              IPv4Address(int(IPv4Address('192.0.2.1'))) ==\n                IPv4Address('192.0.2.1')\n\n        Raises:\n            AddressValueError: If ipaddress isn't a valid IPv4 address.\n\n        ";A=address
		if isinstance(A,int):B._check_int_address(A);B._ip=A;return
		if isinstance(A,bytes):B._check_packed_address(A,4);B._ip=int.from_bytes(A,_D);return
		C=str(A)
		if'/'in C:raise AddressValueError(f"Unexpected '/' in {A!r}")
		B._ip=B._ip_int_from_string(C)
	@property
	def packed(self):'The binary representation of this address.';return v4_int_to_packed(self._ip)
	@property
	def is_reserved(self):'Test if the address is otherwise IETF reserved.\n\n         Returns:\n             A boolean, True if the address is within the\n             reserved IPv4 Network range.\n\n        ';return self in self._constants._reserved_network
	@property
	@functools.lru_cache()
	def is_private(self):'Test if this address is allocated for private networks.\n\n        Returns:\n            A boolean, True if the address is reserved per\n            iana-ipv4-special-registry.\n\n        ';return any(self in A for A in self._constants._private_networks)
	@property
	@functools.lru_cache()
	def is_global(self):A=self;return A not in A._constants._public_network and not A.is_private
	@property
	def is_multicast(self):'Test if the address is reserved for multicast use.\n\n        Returns:\n            A boolean, True if the address is multicast.\n            See RFC 3171 for details.\n\n        ';return self in self._constants._multicast_network
	@property
	def is_unspecified(self):'Test if the address is unspecified.\n\n        Returns:\n            A boolean, True if this is the unspecified address as defined in\n            RFC 5735 3.\n\n        ';return self==self._constants._unspecified_address
	@property
	def is_loopback(self):'Test if the address is a loopback address.\n\n        Returns:\n            A boolean, True if the address is a loopback per RFC 3330.\n\n        ';return self in self._constants._loopback_network
	@property
	def is_link_local(self):'Test if the address is reserved for link-local.\n\n        Returns:\n            A boolean, True if the address is link-local per RFC 3927.\n\n        ';return self in self._constants._linklocal_network
class IPv4Interface(IPv4Address):
	def __init__(A,address):B,C=A._split_addr_prefix(address);IPv4Address.__init__(A,B);A.network=IPv4Network((B,C),strict=_B);A.netmask=A.network.netmask;A._prefixlen=A.network._prefixlen
	@functools.cached_property
	def hostmask(self):return self.network.hostmask
	def __str__(A):return _F%(A._string_from_ip_int(A._ip),A._prefixlen)
	def __eq__(B,other):
		C=other;A=IPv4Address.__eq__(B,C)
		if A is NotImplemented or not A:return A
		try:return B.network==C.network
		except AttributeError:return _B
	def __lt__(A,other):
		B=other;C=IPv4Address.__lt__(A,B)
		if C is NotImplemented:return NotImplemented
		try:return A.network<B.network or A.network==B.network and C
		except AttributeError:return _B
	def __hash__(A):return hash((A._ip,A._prefixlen,int(A.network.network_address)))
	__reduce__=_IPAddressBase.__reduce__
	@property
	def ip(self):return IPv4Address(self._ip)
	@property
	def with_prefixlen(self):A=self;return _C%(A._string_from_ip_int(A._ip),A._prefixlen)
	@property
	def with_netmask(self):A=self;return _C%(A._string_from_ip_int(A._ip),A.netmask)
	@property
	def with_hostmask(self):A=self;return _C%(A._string_from_ip_int(A._ip),A.hostmask)
class IPv4Network(_BaseV4,_BaseNetwork):
	"This class represents and manipulates 32-bit IPv4 network + addresses..\n\n    Attributes: [examples for IPv4Network('192.0.2.0/27')]\n        .network_address: IPv4Address('192.0.2.0')\n        .hostmask: IPv4Address('0.0.0.31')\n        .broadcast_address: IPv4Address('192.0.2.32')\n        .netmask: IPv4Address('255.255.255.224')\n        .prefixlen: 27\n\n    ";_address_class=IPv4Address
	def __init__(A,address,strict=True):
		"Instantiate a new IPv4 network object.\n\n        Args:\n            address: A string or integer representing the IP [& network].\n              '192.0.2.0/24'\n              '192.0.2.0/255.255.255.0'\n              '192.0.2.0/0.0.0.255'\n              are all functionally the same in IPv4. Similarly,\n              '192.0.2.1'\n              '192.0.2.1/255.255.255.255'\n              '192.0.2.1/32'\n              are also functionally equivalent. That is to say, failing to\n              provide a subnetmask will create an object with a mask of /32.\n\n              If the mask (portion after the / in the argument) is given in\n              dotted quad form, it is treated as a netmask if it starts with a\n              non-zero field (e.g. /255.0.0.0 == /8) and as a hostmask if it\n              starts with a zero field (e.g. 0.255.255.255 == /8), with the\n              single exception of an all-zero mask which is treated as a\n              netmask == /0. If no mask is given, a default of /32 is used.\n\n              Additionally, an integer can be passed, so\n              IPv4Network('192.0.2.1') == IPv4Network(3221225985)\n              or, more generally\n              IPv4Interface(int(IPv4Interface('192.0.2.1'))) ==\n                IPv4Interface('192.0.2.1')\n\n        Raises:\n            AddressValueError: If ipaddress isn't a valid IPv4 address.\n            NetmaskValueError: If the netmask isn't valid for\n              an IPv4 address.\n            ValueError: If strict is True and a network address is not\n              supplied.\n        ";C,D=A._split_addr_prefix(address);A.network_address=IPv4Address(C);A.netmask,A._prefixlen=A._make_netmask(D);B=int(A.network_address)
		if B&int(A.netmask)!=B:
			if strict:raise ValueError(_M%A)
			else:A.network_address=IPv4Address(B&int(A.netmask))
		if A._prefixlen==A._max_prefixlen-1:A.hosts=A.__iter__
		elif A._prefixlen==A._max_prefixlen:A.hosts=lambda:[IPv4Address(C)]
	@property
	@functools.lru_cache()
	def is_global(self):'Test if this address is allocated for public networks.\n\n        Returns:\n            A boolean, True if the address is not reserved per\n            iana-ipv4-special-registry.\n\n        ';A=self;return not(A.network_address in IPv4Network(_H)and A.broadcast_address in IPv4Network(_H))and not A.is_private
class _IPv4Constants:_linklocal_network=IPv4Network(_N);_loopback_network=IPv4Network(_O);_multicast_network=IPv4Network('224.0.0.0/4');_public_network=IPv4Network(_H);_private_networks=[IPv4Network('0.0.0.0/8'),IPv4Network('10.0.0.0/8'),IPv4Network(_O),IPv4Network(_N),IPv4Network('172.16.0.0/12'),IPv4Network('192.0.0.0/29'),IPv4Network('192.0.0.170/31'),IPv4Network('192.0.2.0/24'),IPv4Network('192.168.0.0/16'),IPv4Network('198.18.0.0/15'),IPv4Network('198.51.100.0/24'),IPv4Network('203.0.113.0/24'),IPv4Network(_P),IPv4Network('255.255.255.255/32')];_reserved_network=IPv4Network(_P);_unspecified_address=IPv4Address('0.0.0.0')
IPv4Address._constants=_IPv4Constants
class _BaseV6:
	'Base IPv6 object.\n\n    The following methods are used by IPv6 objects in both single IP\n    addresses and networks.\n\n    ';__slots__=();_version=6;_ALL_ONES=2**IPV6LENGTH-1;_HEXTET_COUNT=8;_HEX_DIGITS=frozenset('0123456789ABCDEFabcdef');_max_prefixlen=IPV6LENGTH;_netmask_cache={}
	@classmethod
	def _make_netmask(A,arg):
		'Make a (netmask, prefix_len) tuple from the given argument.\n\n        Argument can be:\n        - an integer (the prefix length)\n        - a string representing the prefix length (e.g. "24")\n        - a string representing the prefix netmask (e.g. "255.255.255.0")\n        ';B=arg
		if B not in A._netmask_cache:
			if isinstance(B,int):
				C=B
				if not 0<=C<=A._max_prefixlen:A._report_invalid_netmask(C)
			else:C=A._prefix_from_prefix_string(B)
			D=IPv6Address(A._ip_int_from_prefix(C));A._netmask_cache[B]=D,C
		return A._netmask_cache[B]
	@classmethod
	def _ip_int_from_string(D,ip_str):
		"Turn an IPv6 ip_str into an integer.\n\n        Args:\n            ip_str: A string, the IPv6 ip_str.\n\n        Returns:\n            An int, the IPv6 address\n\n        Raises:\n            AddressValueError: if ip_str isn't a valid IPv6 Address.\n\n        ";L="Trailing ':' only permitted as part of '::' in %r";M="Leading ':' only permitted as part of '::' in %r";C=ip_str
		if not C:raise AddressValueError(_K)
		A=C.split(':');N=3
		if len(A)<N:B='At least %d parts expected in %r'%(N,C);raise AddressValueError(B)
		if'.'in A[-1]:
			try:O=IPv4Address(A.pop())._ip
			except AddressValueError as J:raise AddressValueError(_G%(J,C))from _A
			A.append('%x'%(O>>16&65535));A.append('%x'%(O&65535))
		P=D._HEXTET_COUNT+1
		if len(A)>P:B='At most %d colons permitted in %r'%(P-1,C);raise AddressValueError(B)
		G=_A
		for E in range(1,len(A)-1):
			if not A[E]:
				if G is not _A:B="At most one '::' permitted in %r"%C;raise AddressValueError(B)
				G=E
		if G is not _A:
			H=G;I=len(A)-G-1
			if not A[0]:
				H-=1
				if H:B=M;raise AddressValueError(B%C)
			if not A[-1]:
				I-=1
				if I:B=L;raise AddressValueError(B%C)
			K=D._HEXTET_COUNT-(H+I)
			if K<1:B="Expected at most %d other parts with '::' in %r";raise AddressValueError(B%(D._HEXTET_COUNT-1,C))
		else:
			if len(A)!=D._HEXTET_COUNT:B="Exactly %d parts expected without '::' in %r";raise AddressValueError(B%(D._HEXTET_COUNT,C))
			if not A[0]:B=M;raise AddressValueError(B%C)
			if not A[-1]:B=L;raise AddressValueError(B%C)
			H=len(A);I=0;K=0
		try:
			F=0
			for E in range(H):F<<=16;F|=D._parse_hextet(A[E])
			F<<=16*K
			for E in range(-I,0):F<<=16;F|=D._parse_hextet(A[E])
			return F
		except ValueError as J:raise AddressValueError(_G%(J,C))from _A
	@classmethod
	def _parse_hextet(B,hextet_str):
		"Convert an IPv6 hextet string into an integer.\n\n        Args:\n            hextet_str: A string, the number to parse.\n\n        Returns:\n            The hextet as an integer.\n\n        Raises:\n            ValueError: if the input isn't strictly a hex number from\n              [0..FFFF].\n\n        ";A=hextet_str
		if not B._HEX_DIGITS.issuperset(A):raise ValueError('Only hex digits permitted in %r'%A)
		if len(A)>4:C='At most 4 characters permitted in %r';raise ValueError(C%A)
		return int(A,16)
	@classmethod
	def _compress_hextets(I,hextets):
		'Compresses a list of hextets.\n\n        Compresses a list of strings, replacing the longest continuous\n        sequence of "0" in the list with "" and adding empty strings at\n        the beginning or at the end of the string such that subsequently\n        calling ":".join(hextets) will produce the compressed version of\n        the IPv6 address.\n\n        Args:\n            hextets: A list of strings, the hextets to compress.\n\n        Returns:\n            A list of strings.\n\n        ';A=hextets;B=-1;C=0;D=-1;E=0
		for(G,H)in enumerate(A):
			if H=='0':
				E+=1
				if D==-1:D=G
				if E>C:C=E;B=D
			else:E=0;D=-1
		if C>1:
			F=B+C
			if F==len(A):A+=['']
			A[B:F]=['']
			if B==0:A=['']+A
		return A
	@classmethod
	def _string_from_ip_int(B,ip_int=_A):
		'Turns a 128-bit integer into hexadecimal notation.\n\n        Args:\n            ip_int: An integer, the IP address.\n\n        Returns:\n            A string, the hexadecimal representation of the address.\n\n        Raises:\n            ValueError: The address is bigger than 128 bits of all ones.\n\n        ';A=ip_int
		if A is _A:A=int(B._ip)
		if A>B._ALL_ONES:raise ValueError('IPv6 address is too large')
		D='%032x'%A;C=['%x'%int(D[A:A+4],16)for A in range(0,32,4)];C=B._compress_hextets(C);return':'.join(C)
	def _explode_shorthand_ip_string(A):
		'Expand a shortened IPv6 address.\n\n        Args:\n            ip_str: A string, the IPv6 address.\n\n        Returns:\n            A string, the expanded IPv6 address.\n\n        '
		if isinstance(A,IPv6Network):B=str(A.network_address)
		elif isinstance(A,IPv6Interface):B=str(A.ip)
		else:B=str(A)
		D=A._ip_int_from_string(B);E='%032x'%D;C=[E[A:A+4]for A in range(0,32,4)]
		if isinstance(A,(_BaseNetwork,IPv6Interface)):return _F%(':'.join(C),A._prefixlen)
		return':'.join(C)
	def _reverse_pointer(A):'Return the reverse DNS pointer name for the IPv6 address.\n\n        This implements the method described in RFC3596 2.5.\n\n        ';B=A.exploded[::-1].replace(':','');return'.'.join(B)+'.ip6.arpa'
	@staticmethod
	def _split_scope_id(ip_str):
		'Helper function to parse IPv6 string address with scope id.\n\n        See RFC 4007 for details.\n\n        Args:\n            ip_str: A string, the IPv6 address.\n\n        Returns:\n            (addr, scope_id) tuple.\n\n        ';B=ip_str;C,D,A=B.partition('%')
		if not D:A=_A
		elif not A or'%'in A:raise AddressValueError('Invalid IPv6 address: "%r"'%B)
		return C,A
	@property
	def max_prefixlen(self):return self._max_prefixlen
	@property
	def version(self):return self._version
class IPv6Address(_BaseV6,_BaseAddress):
	'Represent and manipulate single IPv6 Addresses.';__slots__='_ip',_Q,_L
	def __init__(A,address):
		"Instantiate a new IPv6 address object.\n\n        Args:\n            address: A string or integer representing the IP\n\n              Additionally, an integer can be passed, so\n              IPv6Address('2001:db8::') ==\n                IPv6Address(42540766411282592856903984951653826560)\n              or, more generally\n              IPv6Address(int(IPv6Address('2001:db8::'))) ==\n                IPv6Address('2001:db8::')\n\n        Raises:\n            AddressValueError: If address isn't a valid IPv6 address.\n\n        ";B=address
		if isinstance(B,int):A._check_int_address(B);A._ip=B;A._scope_id=_A;return
		if isinstance(B,bytes):A._check_packed_address(B,16);A._ip=int.from_bytes(B,_D);A._scope_id=_A;return
		C=str(B)
		if'/'in C:raise AddressValueError(f"Unexpected '/' in {B!r}")
		C,A._scope_id=A._split_scope_id(C);A._ip=A._ip_int_from_string(C)
	def __str__(A):B=super().__str__();return B+'%'+A._scope_id if A._scope_id else B
	def __hash__(A):return hash((A._ip,A._scope_id))
	def __eq__(C,other):
		A=other;B=super().__eq__(A)
		if B is NotImplemented:return NotImplemented
		if not B:return _B
		return C._scope_id==getattr(A,_Q,_A)
	@property
	def scope_id(self):"Identifier of a particular zone of the address's scope.\n\n        See RFC 4007 for details.\n\n        Returns:\n            A string identifying the zone of the address if specified, else None.\n\n        ";return self._scope_id
	@property
	def packed(self):'The binary representation of this address.';return v6_int_to_packed(self._ip)
	@property
	def is_multicast(self):'Test if the address is reserved for multicast use.\n\n        Returns:\n            A boolean, True if the address is a multicast address.\n            See RFC 2373 2.7 for details.\n\n        ';return self in self._constants._multicast_network
	@property
	def is_reserved(self):'Test if the address is otherwise IETF reserved.\n\n        Returns:\n            A boolean, True if the address is within one of the\n            reserved IPv6 Network ranges.\n\n        ';return any(self in A for A in self._constants._reserved_networks)
	@property
	def is_link_local(self):'Test if the address is reserved for link-local.\n\n        Returns:\n            A boolean, True if the address is reserved per RFC 4291.\n\n        ';return self in self._constants._linklocal_network
	@property
	def is_site_local(self):'Test if the address is reserved for site-local.\n\n        Note that the site-local address space has been deprecated by RFC 3879.\n        Use is_private to test if this address is in the space of unique local\n        addresses as defined by RFC 4193.\n\n        Returns:\n            A boolean, True if the address is reserved per RFC 3513 2.5.6.\n\n        ';return self in self._constants._sitelocal_network
	@property
	@functools.lru_cache()
	def is_private(self):
		'Test if this address is allocated for private networks.\n\n        Returns:\n            A boolean, True if the address is reserved per\n            iana-ipv6-special-registry, or is ipv4_mapped and is\n            reserved in the iana-ipv4-special-registry.\n\n        ';A=self;B=A.ipv4_mapped
		if B is not _A:return B.is_private
		return any(A in B for B in A._constants._private_networks)
	@property
	def is_global(self):'Test if this address is allocated for public networks.\n\n        Returns:\n            A boolean, true if the address is not reserved per\n            iana-ipv6-special-registry.\n\n        ';return not self.is_private
	@property
	def is_unspecified(self):'Test if the address is unspecified.\n\n        Returns:\n            A boolean, True if this is the unspecified address as defined in\n            RFC 2373 2.5.2.\n\n        ';return self._ip==0
	@property
	def is_loopback(self):'Test if the address is a loopback address.\n\n        Returns:\n            A boolean, True if the address is a loopback address as defined in\n            RFC 2373 2.5.3.\n\n        ';return self._ip==1
	@property
	def ipv4_mapped(self):
		'Return the IPv4 mapped address.\n\n        Returns:\n            If the IPv6 address is a v4 mapped address, return the\n            IPv4 mapped address. Return None otherwise.\n\n        '
		if self._ip>>32!=65535:return
		return IPv4Address(self._ip&4294967295)
	@property
	def teredo(self):
		"Tuple of embedded teredo IPs.\n\n        Returns:\n            Tuple of the (server, client) IPs or None if the address\n            doesn't appear to be a teredo address (doesn't start with\n            2001::/32)\n\n        ";A=self
		if A._ip>>96!=536936448:return
		return IPv4Address(A._ip>>64&4294967295),IPv4Address(~A._ip&4294967295)
	@property
	def sixtofour(self):
		"Return the IPv4 6to4 embedded address.\n\n        Returns:\n            The IPv4 6to4-embedded address if present or None if the\n            address doesn't appear to contain a 6to4 embedded address.\n\n        "
		if self._ip>>112!=8194:return
		return IPv4Address(self._ip>>80&4294967295)
class IPv6Interface(IPv6Address):
	def __init__(A,address):B,C=A._split_addr_prefix(address);IPv6Address.__init__(A,B);A.network=IPv6Network((B,C),strict=_B);A.netmask=A.network.netmask;A._prefixlen=A.network._prefixlen
	@functools.cached_property
	def hostmask(self):return self.network.hostmask
	def __str__(A):return _F%(super().__str__(),A._prefixlen)
	def __eq__(B,other):
		C=other;A=IPv6Address.__eq__(B,C)
		if A is NotImplemented or not A:return A
		try:return B.network==C.network
		except AttributeError:return _B
	def __lt__(A,other):
		B=other;C=IPv6Address.__lt__(A,B)
		if C is NotImplemented:return C
		try:return A.network<B.network or A.network==B.network and C
		except AttributeError:return _B
	def __hash__(A):return hash((A._ip,A._prefixlen,int(A.network.network_address)))
	__reduce__=_IPAddressBase.__reduce__
	@property
	def ip(self):return IPv6Address(self._ip)
	@property
	def with_prefixlen(self):A=self;return _C%(A._string_from_ip_int(A._ip),A._prefixlen)
	@property
	def with_netmask(self):A=self;return _C%(A._string_from_ip_int(A._ip),A.netmask)
	@property
	def with_hostmask(self):A=self;return _C%(A._string_from_ip_int(A._ip),A.hostmask)
	@property
	def is_unspecified(self):return self._ip==0 and self.network.is_unspecified
	@property
	def is_loopback(self):return self._ip==1 and self.network.is_loopback
class IPv6Network(_BaseV6,_BaseNetwork):
	"This class represents and manipulates 128-bit IPv6 networks.\n\n    Attributes: [examples for IPv6('2001:db8::1000/124')]\n        .network_address: IPv6Address('2001:db8::1000')\n        .hostmask: IPv6Address('::f')\n        .broadcast_address: IPv6Address('2001:db8::100f')\n        .netmask: IPv6Address('ffff:ffff:ffff:ffff:ffff:ffff:ffff:fff0')\n        .prefixlen: 124\n\n    ";_address_class=IPv6Address
	def __init__(A,address,strict=True):
		"Instantiate a new IPv6 Network object.\n\n        Args:\n            address: A string or integer representing the IPv6 network or the\n              IP and prefix/netmask.\n              '2001:db8::/128'\n              '2001:db8:0000:0000:0000:0000:0000:0000/128'\n              '2001:db8::'\n              are all functionally the same in IPv6.  That is to say,\n              failing to provide a subnetmask will create an object with\n              a mask of /128.\n\n              Additionally, an integer can be passed, so\n              IPv6Network('2001:db8::') ==\n                IPv6Network(42540766411282592856903984951653826560)\n              or, more generally\n              IPv6Network(int(IPv6Network('2001:db8::'))) ==\n                IPv6Network('2001:db8::')\n\n            strict: A boolean. If true, ensure that we have been passed\n              A true network address, eg, 2001:db8::1000/124 and not an\n              IP address on a network, eg, 2001:db8::1/124.\n\n        Raises:\n            AddressValueError: If address isn't a valid IPv6 address.\n            NetmaskValueError: If the netmask isn't valid for\n              an IPv6 address.\n            ValueError: If strict was True and a network address was not\n              supplied.\n        ";C,D=A._split_addr_prefix(address);A.network_address=IPv6Address(C);A.netmask,A._prefixlen=A._make_netmask(D);B=int(A.network_address)
		if B&int(A.netmask)!=B:
			if strict:raise ValueError(_M%A)
			else:A.network_address=IPv6Address(B&int(A.netmask))
		if A._prefixlen==A._max_prefixlen-1:A.hosts=A.__iter__
		elif A._prefixlen==A._max_prefixlen:A.hosts=lambda:[IPv6Address(C)]
	def hosts(A):
		"Generate Iterator over usable hosts in a network.\n\n          This is like __iter__ except it doesn't return the\n          Subnet-Router anycast address.\n\n        ";B=int(A.network_address);C=int(A.broadcast_address)
		for D in range(B+1,C+1):yield A._address_class(D)
	@property
	def is_site_local(self):'Test if the address is reserved for site-local.\n\n        Note that the site-local address space has been deprecated by RFC 3879.\n        Use is_private to test if this address is in the space of unique local\n        addresses as defined by RFC 4193.\n\n        Returns:\n            A boolean, True if the address is reserved per RFC 3513 2.5.6.\n\n        ';return self.network_address.is_site_local and self.broadcast_address.is_site_local
class _IPv6Constants:_linklocal_network=IPv6Network(_R);_multicast_network=IPv6Network('ff00::/8');_private_networks=[IPv6Network('::1/128'),IPv6Network('::/128'),IPv6Network('::ffff:0:0/96'),IPv6Network('100::/64'),IPv6Network('2001::/23'),IPv6Network('2001:2::/48'),IPv6Network('2001:db8::/32'),IPv6Network('2001:10::/28'),IPv6Network('fc00::/7'),IPv6Network(_R)];_reserved_networks=[IPv6Network('::/8'),IPv6Network('100::/8'),IPv6Network('200::/7'),IPv6Network('400::/6'),IPv6Network('800::/5'),IPv6Network('1000::/4'),IPv6Network('4000::/3'),IPv6Network('6000::/3'),IPv6Network('8000::/3'),IPv6Network('A000::/3'),IPv6Network('C000::/3'),IPv6Network('E000::/4'),IPv6Network('F000::/5'),IPv6Network('F800::/6'),IPv6Network('FE00::/9')];_sitelocal_network=IPv6Network('fec0::/10')
IPv6Address._constants=_IPv6Constants