'Drop-in replacement for the thread module.\n\nMeant to be used as a brain-dead substitute so that threaded code does\nnot need to be rewritten for when the thread module is not present.\n\nSuggested usage is::\n\n    try:\n        import _thread\n    except ImportError:\n        import _dummy_thread as _thread\n\n'
_E='unlocked'
_D='locked'
_C=None
_B=False
_A=True
__all__=['error','start_new_thread','exit','get_ident','allocate_lock','interrupt_main','LockType','RLock','_count']
TIMEOUT_MAX=2**31
error=RuntimeError
def start_new_thread(function,args,kwargs={}):
	'Dummy implementation of _thread.start_new_thread().\n\n    Compatibility is maintained by making sure that ``args`` is a\n    tuple and ``kwargs`` is a dictionary.  If an exception is raised\n    and it is SystemExit (which can be done by _thread.exit()) it is\n    caught and nothing is done; all other exceptions are printed out\n    by using traceback.print_exc().\n\n    If the executed function calls interrupt_main the KeyboardInterrupt will be\n    raised when the function returns.\n\n    ';A=kwargs
	if type(args)!=type(tuple()):raise TypeError('2nd arg must be a tuple')
	if type(A)!=type(dict()):raise TypeError('3rd arg must be a dict')
	global _main;_main=_B
	try:function(*args,**A)
	except SystemExit:pass
	except:import traceback as B;B.print_exc()
	_main=_A;global _interrupt
	if _interrupt:_interrupt=_B;raise KeyboardInterrupt
def exit():'Dummy implementation of _thread.exit().';raise SystemExit
def get_ident():'Dummy implementation of _thread.get_ident().\n\n    Since this module should only be used when _threadmodule is not\n    available, it is safe to assume that the current process is the\n    only thread.  Thus a constant can be safely returned.\n    ';return-1
def allocate_lock():'Dummy implementation of _thread.allocate_lock().';return LockType()
def stack_size(size=_C):
	'Dummy implementation of _thread.stack_size().'
	if size is not _C:raise error('setting thread stack size not supported')
	return 0
def _set_sentinel():'Dummy implementation of _thread._set_sentinel().';return LockType()
def _count():'Dummy implementation of _thread._count().';return 0
class LockType:
	'Class implementing dummy implementation of _thread.LockType.\n\n    Compatibility is maintained by maintaining self.locked_status\n    which is a boolean that stores the state of the lock.  Pickling of\n    the lock, though, should not be done since if the _thread module is\n    then used with an unpickled ``lock()`` from here problems could\n    occur from this class not having atomic methods.\n\n    '
	def __init__(A):A.locked_status=_B
	def acquire(A,waitflag=_C,timeout=-1):
		"Dummy implementation of acquire().\n\n        For blocking calls, self.locked_status is automatically set to\n        True and returned appropriately based on value of\n        ``waitflag``.  If it is non-blocking, then the value is\n        actually checked and not set if it is already acquired.  This\n        is all done so that threading.Condition's assert statements\n        aren't triggered and throw a little fit.\n\n        ";B=timeout;C=waitflag
		if C is _C or C:A.locked_status=_A;return _A
		elif not A.locked_status:A.locked_status=_A;return _A
		else:
			if B>0:import time;time.sleep(B)
			return _B
	__enter__=acquire
	def __exit__(A,typ,val,tb):A.release()
	def release(A):
		'Release the dummy lock.'
		if not A.locked_status:raise error
		A.locked_status=_B;return _A
	def locked(A):return A.locked_status
	def _at_fork_reinit(A):A.locked_status=_B
	def __repr__(A):return'<%s %s.%s object at %s>'%(_D if A.locked_status else _E,A.__class__.__module__,A.__class__.__qualname__,hex(id(A)))
_interrupt=_B
_main=_A
def interrupt_main():
	'Set _interrupt flag to True to have start_new_thread raise\n    KeyboardInterrupt upon exiting.'
	if _main:raise KeyboardInterrupt
	else:global _interrupt;_interrupt=_A
class RLock:
	def __init__(A):A.locked_count=0
	def acquire(A,waitflag=_C,timeout=-1):A.locked_count+=1;return _A
	__enter__=acquire
	def __exit__(A,typ,val,tb):A.release()
	def release(A):
		if not A.locked_count:raise error
		A.locked_count-=1;return _A
	def locked(A):return A.locked_status!=0
	def __repr__(A):return'<%s %s.%s object owner=%s count=%s at %s>'%(_D if A.locked_count else _E,A.__class__.__module__,A.__class__.__qualname__,get_ident()if A.locked_count else 0,A.locked_count,hex(id(A)))