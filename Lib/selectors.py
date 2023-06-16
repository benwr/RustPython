'Selectors module.\n\nThis module allows high-level and efficient I/O multiplexing, built upon the\n`select` module primitives.\n'
_F='kqueue'
_E='devpoll'
_D='poll'
_C=False
_B='{!r} is not registered'
_A=None
from abc import ABCMeta,abstractmethod
from collections import namedtuple
from collections.abc import Mapping
import math,select,sys
EVENT_READ=1<<0
EVENT_WRITE=1<<1
def _fileobj_to_fd(fileobj):
	'Return a file descriptor from a file object.\n\n    Parameters:\n    fileobj -- file object or file descriptor\n\n    Returns:\n    corresponding file descriptor\n\n    Raises:\n    ValueError if the object is invalid\n    ';A=fileobj
	if isinstance(A,int):B=A
	else:
		try:B=int(A.fileno())
		except(AttributeError,TypeError,ValueError):raise ValueError('Invalid file object: {!r}'.format(A))from _A
	if B<0:raise ValueError('Invalid file descriptor: {}'.format(B))
	return B
SelectorKey=namedtuple('SelectorKey',['fileobj','fd','events','data'])
SelectorKey.__doc__='SelectorKey(fileobj, fd, events, data)\n\n    Object used to associate a file object to its backing\n    file descriptor, selected event mask, and attached data.\n'
if sys.version_info>=(3,5):SelectorKey.fileobj.__doc__='File object registered.';SelectorKey.fd.__doc__='Underlying file descriptor.';SelectorKey.events.__doc__='Events that must be waited for on this file object.';SelectorKey.data.__doc__='Optional opaque data associated to this file object.\n    For example, this could be used to store a per-client session ID.'
class _SelectorMapping(Mapping):
	'Mapping of file objects to selector keys.'
	def __init__(A,selector):A._selector=selector
	def __len__(A):return len(A._selector._fd_to_key)
	def __getitem__(A,fileobj):
		B=fileobj
		try:C=A._selector._fileobj_lookup(B);return A._selector._fd_to_key[C]
		except KeyError:raise KeyError(_B.format(B))from _A
	def __iter__(A):return iter(A._selector._fd_to_key)
class BaseSelector(metaclass=ABCMeta):
	'Selector abstract base class.\n\n    A selector supports registering file objects to be monitored for specific\n    I/O events.\n\n    A file object is a file descriptor or any object with a `fileno()` method.\n    An arbitrary object can be attached to the file object, which can be used\n    for example to store context information, a callback, etc.\n\n    A selector can use various implementations (select(), poll(), epoll()...)\n    depending on the platform. The default `Selector` class uses the most\n    efficient implementation on the current platform.\n    '
	@abstractmethod
	def register(self,fileobj,events,data=_A):'Register a file object.\n\n        Parameters:\n        fileobj -- file object or file descriptor\n        events  -- events to monitor (bitwise mask of EVENT_READ|EVENT_WRITE)\n        data    -- attached data\n\n        Returns:\n        SelectorKey instance\n\n        Raises:\n        ValueError if events is invalid\n        KeyError if fileobj is already registered\n        OSError if fileobj is closed or otherwise is unacceptable to\n                the underlying system call (if a system call is made)\n\n        Note:\n        OSError may or may not be raised\n        ';raise NotImplementedError
	@abstractmethod
	def unregister(self,fileobj):'Unregister a file object.\n\n        Parameters:\n        fileobj -- file object or file descriptor\n\n        Returns:\n        SelectorKey instance\n\n        Raises:\n        KeyError if fileobj is not registered\n\n        Note:\n        If fileobj is registered but has since been closed this does\n        *not* raise OSError (even if the wrapped syscall does)\n        ';raise NotImplementedError
	def modify(A,fileobj,events,data=_A):'Change a registered file object monitored events or attached data.\n\n        Parameters:\n        fileobj -- file object or file descriptor\n        events  -- events to monitor (bitwise mask of EVENT_READ|EVENT_WRITE)\n        data    -- attached data\n\n        Returns:\n        SelectorKey instance\n\n        Raises:\n        Anything that unregister() or register() raises\n        ';B=fileobj;A.unregister(B);return A.register(B,events,data)
	@abstractmethod
	def select(self,timeout=_A):"Perform the actual selection, until some monitored file objects are\n        ready or a timeout expires.\n\n        Parameters:\n        timeout -- if timeout > 0, this specifies the maximum wait time, in\n                   seconds\n                   if timeout <= 0, the select() call won't block, and will\n                   report the currently ready file objects\n                   if timeout is None, select() will block until a monitored\n                   file object becomes ready\n\n        Returns:\n        list of (key, events) for ready file objects\n        `events` is a bitwise mask of EVENT_READ|EVENT_WRITE\n        ";raise NotImplementedError
	def close(A):'Close the selector.\n\n        This must be called to make sure that any underlying resource is freed.\n        '
	def get_key(C,fileobj):
		'Return the key associated to a registered file object.\n\n        Returns:\n        SelectorKey for this file object\n        ';A=fileobj;B=C.get_map()
		if B is _A:raise RuntimeError('Selector is closed')
		try:return B[A]
		except KeyError:raise KeyError(_B.format(A))from _A
	@abstractmethod
	def get_map(self):'Return a mapping of file objects to selector keys.';raise NotImplementedError
	def __enter__(A):return A
	def __exit__(A,*B):A.close()
class _BaseSelectorImpl(BaseSelector):
	'Base selector implementation.'
	def __init__(A):A._fd_to_key={};A._map=_SelectorMapping(A)
	def _fileobj_lookup(C,fileobj):
		'Return a file descriptor from a file object.\n\n        This wraps _fileobj_to_fd() to do an exhaustive search in case\n        the object is invalid but we still have it in our map.  This\n        is used by unregister() so we can unregister an object that\n        was previously registered even if it is closed.  It is also\n        used by _SelectorMapping.\n        ';A=fileobj
		try:return _fileobj_to_fd(A)
		except ValueError:
			for B in C._fd_to_key.values():
				if B.fileobj is A:return B.fd
			raise
	def register(C,fileobj,events,data=_A):
		D=fileobj;B=events
		if not B or B&~(EVENT_READ|EVENT_WRITE):raise ValueError('Invalid events: {!r}'.format(B))
		A=SelectorKey(D,C._fileobj_lookup(D),B,data)
		if A.fd in C._fd_to_key:raise KeyError('{!r} (FD {}) is already registered'.format(D,A.fd))
		C._fd_to_key[A.fd]=A;return A
	def unregister(A,fileobj):
		B=fileobj
		try:C=A._fd_to_key.pop(A._fileobj_lookup(B))
		except KeyError:raise KeyError(_B.format(B))from _A
		return C
	def modify(B,fileobj,events,data=_A):
		E=events;D=data;C=fileobj
		try:A=B._fd_to_key[B._fileobj_lookup(C)]
		except KeyError:raise KeyError(_B.format(C))from _A
		if E!=A.events:B.unregister(C);A=B.register(C,E,D)
		elif D!=A.data:A=A._replace(data=D);B._fd_to_key[A.fd]=A
		return A
	def close(A):A._fd_to_key.clear();A._map=_A
	def get_map(A):return A._map
	def _key_from_fd(A,fd):
		'Return the key associated to a given file descriptor.\n\n        Parameters:\n        fd -- file descriptor\n\n        Returns:\n        corresponding key, or None if not found\n        '
		try:return A._fd_to_key[fd]
		except KeyError:return
class SelectSelector(_BaseSelectorImpl):
	'Select-based selector.'
	def __init__(A):super().__init__();A._readers=set();A._writers=set()
	def register(C,fileobj,events,data=_A):
		A=events;B=super().register(fileobj,A,data)
		if A&EVENT_READ:C._readers.add(B.fd)
		if A&EVENT_WRITE:C._writers.add(B.fd)
		return B
	def unregister(B,fileobj):A=super().unregister(fileobj);B._readers.discard(A.fd);B._writers.discard(A.fd);return A
	if sys.platform=='win32':
		def _select(B,r,w,_,timeout=_A):r,w,A=select.select(r,w,w,timeout);return r,w+A,[]
	else:_select=select.select
	def select(A,timeout=_A):
		B=timeout;B=_A if B is _A else max(B,0);E=[]
		try:C,D,I=A._select(A._readers,A._writers,[],B)
		except InterruptedError:return E
		C=set(C);D=set(D)
		for F in C|D:
			G=0
			if F in C:G|=EVENT_READ
			if F in D:G|=EVENT_WRITE
			H=A._key_from_fd(F)
			if H:E.append((H,G&H.events))
		return E
class _PollLikeSelector(_BaseSelectorImpl):
	'Base class shared between poll, epoll and devpoll selectors.';_selector_cls=_A;_EVENT_READ=_A;_EVENT_WRITE=_A
	def __init__(A):super().__init__();A._selector=A._selector_cls()
	def register(A,fileobj,events,data=_A):
		D=fileobj;B=events;E=super().register(D,B,data);C=0
		if B&EVENT_READ:C|=A._EVENT_READ
		if B&EVENT_WRITE:C|=A._EVENT_WRITE
		try:A._selector.register(E.fd,C)
		except:super().unregister(D);raise
		return E
	def unregister(B,fileobj):
		A=super().unregister(fileobj)
		try:B._selector.unregister(A.fd)
		except OSError:pass
		return A
	def modify(B,fileobj,events,data=_A):
		D=fileobj;C=events
		try:A=B._fd_to_key[B._fileobj_lookup(D)]
		except KeyError:raise KeyError(f"{D!r} is not registered")from _A
		E=_C
		if C!=A.events:
			F=0
			if C&EVENT_READ:F|=B._EVENT_READ
			if C&EVENT_WRITE:F|=B._EVENT_WRITE
			try:B._selector.modify(A.fd,F)
			except:super().unregister(D);raise
			E=True
		if data!=A.data:E=True
		if E:A=A._replace(events=C,data=data);B._fd_to_key[A.fd]=A
		return A
	def select(B,timeout=_A):
		A=timeout
		if A is _A:A=_A
		elif A<=0:A=0
		else:A=math.ceil(A*1e3)
		C=[]
		try:G=B._selector.poll(A)
		except InterruptedError:return C
		for(H,F)in G:
			D=0
			if F&~B._EVENT_READ:D|=EVENT_WRITE
			if F&~B._EVENT_WRITE:D|=EVENT_READ
			E=B._key_from_fd(H)
			if E:C.append((E,D&E.events))
		return C
if hasattr(select,_D):
	class PollSelector(_PollLikeSelector):'Poll-based selector.';_selector_cls=select.poll;_EVENT_READ=select.POLLIN;_EVENT_WRITE=select.POLLOUT
if hasattr(select,'epoll'):
	class EpollSelector(_PollLikeSelector):
		'Epoll-based selector.';_selector_cls=select.epoll;_EVENT_READ=select.EPOLLIN;_EVENT_WRITE=select.EPOLLOUT
		def fileno(A):return A._selector.fileno()
		def select(B,timeout=_A):
			A=timeout
			if A is _A:A=-1
			elif A<=0:A=0
			else:A=math.ceil(A*1e3)*.001
			G=max(len(B._fd_to_key),1);C=[]
			try:H=B._selector.poll(A,G)
			except InterruptedError:return C
			for(I,F)in H:
				D=0
				if F&~select.EPOLLIN:D|=EVENT_WRITE
				if F&~select.EPOLLOUT:D|=EVENT_READ
				E=B._key_from_fd(I)
				if E:C.append((E,D&E.events))
			return C
		def close(A):A._selector.close();super().close()
if hasattr(select,_E):
	class DevpollSelector(_PollLikeSelector):
		'Solaris /dev/poll selector.';_selector_cls=select.devpoll;_EVENT_READ=select.POLLIN;_EVENT_WRITE=select.POLLOUT
		def fileno(A):return A._selector.fileno()
		def close(A):A._selector.close();super().close()
if hasattr(select,_F):
	class KqueueSelector(_BaseSelectorImpl):
		'Kqueue-based selector.'
		def __init__(A):super().__init__();A._selector=select.kqueue()
		def fileno(A):return A._selector.fileno()
		def register(D,fileobj,events,data=_A):
			E=fileobj;A=events;B=super().register(E,A,data)
			try:
				if A&EVENT_READ:C=select.kevent(B.fd,select.KQ_FILTER_READ,select.KQ_EV_ADD);D._selector.control([C],0,0)
				if A&EVENT_WRITE:C=select.kevent(B.fd,select.KQ_FILTER_WRITE,select.KQ_EV_ADD);D._selector.control([C],0,0)
			except:super().unregister(E);raise
			return B
		def unregister(C,fileobj):
			A=super().unregister(fileobj)
			if A.events&EVENT_READ:
				B=select.kevent(A.fd,select.KQ_FILTER_READ,select.KQ_EV_DELETE)
				try:C._selector.control([B],0,0)
				except OSError:pass
			if A.events&EVENT_WRITE:
				B=select.kevent(A.fd,select.KQ_FILTER_WRITE,select.KQ_EV_DELETE)
				try:C._selector.control([B],0,0)
				except OSError:pass
			return A
		def select(B,timeout=_A):
			A=timeout;A=_A if A is _A else max(A,0);H=max(len(B._fd_to_key),1);C=[]
			try:I=B._selector.control(_A,H,A)
			except InterruptedError:return C
			for F in I:
				J=F.ident;G=F.filter;D=0
				if G==select.KQ_FILTER_READ:D|=EVENT_READ
				if G==select.KQ_FILTER_WRITE:D|=EVENT_WRITE
				E=B._key_from_fd(J)
				if E:C.append((E,D&E.events))
			return C
		def close(A):A._selector.close();super().close()
def _can_use(method):
	'Check if we can use the selector depending upon the\n    operating system. ';A=method;B=getattr(select,A,_A)
	if B is _A:return _C
	try:
		C=B()
		if A==_D:C.poll(0)
		else:C.close()
		return True
	except OSError:return _C
if _can_use(_F):DefaultSelector=KqueueSelector
elif _can_use('epoll'):DefaultSelector=EpollSelector
elif _can_use(_E):DefaultSelector=DevpollSelector
elif _can_use(_D):DefaultSelector=PollSelector
else:DefaultSelector=SelectSelector