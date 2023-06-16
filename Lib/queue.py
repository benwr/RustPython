'A multi-producer, multi-consumer queue.'
_D="'timeout' must be a non-negative number"
_C=False
_B=True
_A=None
import threading,types
from collections import deque
from heapq import heappush,heappop
from time import monotonic as time
try:from _queue import SimpleQueue
except ImportError:SimpleQueue=_A
__all__=['Empty','Full','Queue','PriorityQueue','LifoQueue','SimpleQueue']
try:from _queue import Empty
except ImportError:
	class Empty(Exception):'Exception raised by Queue.get(block=0)/get_nowait().'
class Full(Exception):'Exception raised by Queue.put(block=0)/put_nowait().'
class Queue:
	'Create a queue object with a given maximum size.\n\n    If maxsize is <= 0, the queue size is infinite.\n    '
	def __init__(A,maxsize=0):B=maxsize;A.maxsize=B;A._init(B);A.mutex=threading.Lock();A.not_empty=threading.Condition(A.mutex);A.not_full=threading.Condition(A.mutex);A.all_tasks_done=threading.Condition(A.mutex);A.unfinished_tasks=0
	def task_done(A):
		'Indicate that a formerly enqueued task is complete.\n\n        Used by Queue consumer threads.  For each get() used to fetch a task,\n        a subsequent call to task_done() tells the queue that the processing\n        on the task is complete.\n\n        If a join() is currently blocking, it will resume when all items\n        have been processed (meaning that a task_done() call was received\n        for every item that had been put() into the queue).\n\n        Raises a ValueError if called more times than there were items\n        placed in the queue.\n        '
		with A.all_tasks_done:
			B=A.unfinished_tasks-1
			if B<=0:
				if B<0:raise ValueError('task_done() called too many times')
				A.all_tasks_done.notify_all()
			A.unfinished_tasks=B
	def join(A):
		'Blocks until all items in the Queue have been gotten and processed.\n\n        The count of unfinished tasks goes up whenever an item is added to the\n        queue. The count goes down whenever a consumer thread calls task_done()\n        to indicate the item was retrieved and all work on it is complete.\n\n        When the count of unfinished tasks drops to zero, join() unblocks.\n        '
		with A.all_tasks_done:
			while A.unfinished_tasks:A.all_tasks_done.wait()
	def qsize(A):
		'Return the approximate size of the queue (not reliable!).'
		with A.mutex:return A._qsize()
	def empty(A):
		'Return True if the queue is empty, False otherwise (not reliable!).\n\n        This method is likely to be removed at some point.  Use qsize() == 0\n        as a direct substitute, but be aware that either approach risks a race\n        condition where a queue can grow before the result of empty() or\n        qsize() can be used.\n\n        To create code that needs to wait for all queued tasks to be\n        completed, the preferred technique is to use the join() method.\n        '
		with A.mutex:return not A._qsize()
	def full(A):
		'Return True if the queue is full, False otherwise (not reliable!).\n\n        This method is likely to be removed at some point.  Use qsize() >= n\n        as a direct substitute, but be aware that either approach risks a race\n        condition where a queue can shrink before the result of full() or\n        qsize() can be used.\n        '
		with A.mutex:return 0<A.maxsize<=A._qsize()
	def put(A,item,block=_B,timeout=_A):
		"Put an item into the queue.\n\n        If optional args 'block' is true and 'timeout' is None (the default),\n        block if necessary until a free slot is available. If 'timeout' is\n        a non-negative number, it blocks at most 'timeout' seconds and raises\n        the Full exception if no free slot was available within that time.\n        Otherwise ('block' is false), put an item on the queue if a free slot\n        is immediately available, else raise the Full exception ('timeout'\n        is ignored in that case).\n        ";B=timeout
		with A.not_full:
			if A.maxsize>0:
				if not block:
					if A._qsize()>=A.maxsize:raise Full
				elif B is _A:
					while A._qsize()>=A.maxsize:A.not_full.wait()
				elif B<0:raise ValueError(_D)
				else:
					D=time()+B
					while A._qsize()>=A.maxsize:
						C=D-time()
						if C<=.0:raise Full
						A.not_full.wait(C)
			A._put(item);A.unfinished_tasks+=1;A.not_empty.notify()
	def get(A,block=_B,timeout=_A):
		"Remove and return an item from the queue.\n\n        If optional args 'block' is true and 'timeout' is None (the default),\n        block if necessary until an item is available. If 'timeout' is\n        a non-negative number, it blocks at most 'timeout' seconds and raises\n        the Empty exception if no item was available within that time.\n        Otherwise ('block' is false), return an item if one is immediately\n        available, else raise the Empty exception ('timeout' is ignored\n        in that case).\n        ";B=timeout
		with A.not_empty:
			if not block:
				if not A._qsize():raise Empty
			elif B is _A:
				while not A._qsize():A.not_empty.wait()
			elif B<0:raise ValueError(_D)
			else:
				D=time()+B
				while not A._qsize():
					C=D-time()
					if C<=.0:raise Empty
					A.not_empty.wait(C)
			E=A._get();A.not_full.notify();return E
	def put_nowait(A,item):'Put an item into the queue without blocking.\n\n        Only enqueue the item if a free slot is immediately available.\n        Otherwise raise the Full exception.\n        ';return A.put(item,block=_C)
	def get_nowait(A):'Remove and return an item from the queue without blocking.\n\n        Only get an item if one is immediately available. Otherwise\n        raise the Empty exception.\n        ';return A.get(block=_C)
	def _init(A,maxsize):A.queue=deque()
	def _qsize(A):return len(A.queue)
	def _put(A,item):A.queue.append(item)
	def _get(A):return A.queue.popleft()
	__class_getitem__=classmethod(types.GenericAlias)
class PriorityQueue(Queue):
	'Variant of Queue that retrieves open entries in priority order (lowest first).\n\n    Entries are typically tuples of the form:  (priority number, data).\n    '
	def _init(A,maxsize):A.queue=[]
	def _qsize(A):return len(A.queue)
	def _put(A,item):heappush(A.queue,item)
	def _get(A):return heappop(A.queue)
class LifoQueue(Queue):
	'Variant of Queue that retrieves most recently added entries first.'
	def _init(A,maxsize):A.queue=[]
	def _qsize(A):return len(A.queue)
	def _put(A,item):A.queue.append(item)
	def _get(A):return A.queue.pop()
class _PySimpleQueue:
	'Simple, unbounded FIFO queue.\n\n    This pure Python implementation is not reentrant.\n    '
	def __init__(A):A._queue=deque();A._count=threading.Semaphore(0)
	def put(A,item,block=_B,timeout=_A):"Put the item on the queue.\n\n        The optional 'block' and 'timeout' arguments are ignored, as this method\n        never blocks.  They are provided for compatibility with the Queue class.\n        ";A._queue.append(item);A._count.release()
	def get(B,block=_B,timeout=_A):
		"Remove and return an item from the queue.\n\n        If optional args 'block' is true and 'timeout' is None (the default),\n        block if necessary until an item is available. If 'timeout' is\n        a non-negative number, it blocks at most 'timeout' seconds and raises\n        the Empty exception if no item was available within that time.\n        Otherwise ('block' is false), return an item if one is immediately\n        available, else raise the Empty exception ('timeout' is ignored\n        in that case).\n        ";A=timeout
		if A is not _A and A<0:raise ValueError(_D)
		if not B._count.acquire(block,A):raise Empty
		return B._queue.popleft()
	def put_nowait(A,item):'Put an item into the queue without blocking.\n\n        This is exactly equivalent to `put(item, block=False)` and is only provided\n        for compatibility with the Queue class.\n        ';return A.put(item,block=_C)
	def get_nowait(A):'Remove and return an item from the queue without blocking.\n\n        Only get an item if one is immediately available. Otherwise\n        raise the Empty exception.\n        ';return A.get(block=_C)
	def empty(A):'Return True if the queue is empty, False otherwise (not reliable!).';return len(A._queue)==0
	def qsize(A):'Return the approximate size of the queue (not reliable!).';return len(A._queue)
	__class_getitem__=classmethod(types.GenericAlias)
if SimpleQueue is _A:SimpleQueue=_PySimpleQueue