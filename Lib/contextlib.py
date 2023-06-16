'Utilities for with-statement contexts.  See PEP 343.'
_E="generator didn't stop"
_D="generator didn't yield"
_C=True
_B=False
_A=None
import abc,os,sys,_collections_abc
from collections import deque
from functools import wraps
from types import MethodType,GenericAlias
__all__=['asynccontextmanager','contextmanager','closing','nullcontext','AbstractContextManager','AbstractAsyncContextManager','AsyncExitStack','ContextDecorator','ExitStack','redirect_stdout','redirect_stderr','suppress','aclosing','chdir']
class AbstractContextManager(abc.ABC):
	'An abstract base class for context managers.';__class_getitem__=classmethod(GenericAlias)
	def __enter__(A):'Return `self` upon entering the runtime context.';return A
	@abc.abstractmethod
	def __exit__(self,exc_type,exc_value,traceback):'Raise any exception triggered within the runtime context.'
	@classmethod
	def __subclasshook__(A,C):
		if A is AbstractContextManager:return _collections_abc._check_methods(C,'__enter__','__exit__')
		return NotImplemented
class AbstractAsyncContextManager(abc.ABC):
	'An abstract base class for asynchronous context managers.';__class_getitem__=classmethod(GenericAlias)
	async def __aenter__(A):'Return `self` upon entering the runtime context.';return A
	@abc.abstractmethod
	async def __aexit__(self,exc_type,exc_value,traceback):'Raise any exception triggered within the runtime context.'
	@classmethod
	def __subclasshook__(A,C):
		if A is AbstractAsyncContextManager:return _collections_abc._check_methods(C,'__aenter__','__aexit__')
		return NotImplemented
class ContextDecorator:
	'A base class or mixin that enables context managers to work as decorators.'
	def _recreate_cm(A):'Return a recreated instance of self.\n\n        Allows an otherwise one-shot context manager like\n        _GeneratorContextManager to support use as\n        a decorator via implicit recreation.\n\n        This is a private interface just for _GeneratorContextManager.\n        See issue #11647 for details.\n        ';return A
	def __call__(A,func):
		@wraps(func)
		def B(*B,**C):
			with A._recreate_cm():return func(*B,**C)
		return B
class AsyncContextDecorator:
	'A base class or mixin that enables async context managers to work as decorators.'
	def _recreate_cm(A):'Return a recreated instance of self.\n        ';return A
	def __call__(A,func):
		@wraps(func)
		async def B(*B,**C):
			async with A._recreate_cm():return await func(*B,**C)
		return B
class _GeneratorContextManagerBase:
	'Shared functionality for @contextmanager and @asynccontextmanager.'
	def __init__(A,func,args,kwds):
		B=func;A.gen=B(*args,**kwds);A.func,A.args,A.kwds=B,args,kwds;C=getattr(B,'__doc__',_A)
		if C is _A:C=type(A).__doc__
		A.__doc__=C
	def _recreate_cm(A):return A.__class__(A.func,A.args,A.kwds)
class _GeneratorContextManager(_GeneratorContextManagerBase,AbstractContextManager,ContextDecorator):
	'Helper for @contextmanager decorator.'
	def __enter__(A):
		del A.args,A.kwds,A.func
		try:return next(A.gen)
		except StopIteration:raise RuntimeError(_D)from _A
	def __exit__(E,typ,value,traceback):
		D=typ;C=traceback;A=value
		if D is _A:
			try:next(E.gen)
			except StopIteration:return _B
			else:raise RuntimeError(_E)
		else:
			if A is _A:A=D()
			try:E.gen.throw(D,A,C)
			except StopIteration as B:return B is not A
			except RuntimeError as B:
				if B is A:B.__traceback__=C;return _B
				if isinstance(A,StopIteration)and B.__cause__ is A:A.__traceback__=C;return _B
				raise
			except BaseException as B:
				if B is not A:raise
				B.__traceback__=C;return _B
			raise RuntimeError("generator didn't stop after throw()")
class _AsyncGeneratorContextManager(_GeneratorContextManagerBase,AbstractAsyncContextManager,AsyncContextDecorator):
	'Helper for @asynccontextmanager decorator.'
	async def __aenter__(A):
		del A.args,A.kwds,A.func
		try:return await anext(A.gen)
		except StopAsyncIteration:raise RuntimeError(_D)from _A
	async def __aexit__(E,typ,value,traceback):
		D=typ;C=traceback;A=value
		if D is _A:
			try:await anext(E.gen)
			except StopAsyncIteration:return _B
			else:raise RuntimeError(_E)
		else:
			if A is _A:A=D()
			try:await E.gen.athrow(D,A,C)
			except StopAsyncIteration as B:return B is not A
			except RuntimeError as B:
				if B is A:B.__traceback__=C;return _B
				if isinstance(A,(StopIteration,StopAsyncIteration))and B.__cause__ is A:A.__traceback__=C;return _B
				raise
			except BaseException as B:
				if B is not A:raise
				B.__traceback__=C;return _B
			raise RuntimeError("generator didn't stop after athrow()")
def contextmanager(func):
	'@contextmanager decorator.\n\n    Typical usage:\n\n        @contextmanager\n        def some_generator(<arguments>):\n            <setup>\n            try:\n                yield <value>\n            finally:\n                <cleanup>\n\n    This makes this:\n\n        with some_generator(<arguments>) as <variable>:\n            <body>\n\n    equivalent to this:\n\n        <setup>\n        try:\n            <variable> = <value>\n            <body>\n        finally:\n            <cleanup>\n    '
	@wraps(func)
	def A(*A,**B):return _GeneratorContextManager(func,A,B)
	return A
def asynccontextmanager(func):
	'@asynccontextmanager decorator.\n\n    Typical usage:\n\n        @asynccontextmanager\n        async def some_async_generator(<arguments>):\n            <setup>\n            try:\n                yield <value>\n            finally:\n                <cleanup>\n\n    This makes this:\n\n        async with some_async_generator(<arguments>) as <variable>:\n            <body>\n\n    equivalent to this:\n\n        <setup>\n        try:\n            <variable> = <value>\n            <body>\n        finally:\n            <cleanup>\n    '
	@wraps(func)
	def A(*A,**B):return _AsyncGeneratorContextManager(func,A,B)
	return A
class closing(AbstractContextManager):
	'Context to automatically close something at the end of a block.\n\n    Code like this:\n\n        with closing(<module>.open(<arguments>)) as f:\n            <block>\n\n    is equivalent to this:\n\n        f = <module>.open(<arguments>)\n        try:\n            <block>\n        finally:\n            f.close()\n\n    '
	def __init__(A,thing):A.thing=thing
	def __enter__(A):return A.thing
	def __exit__(A,*B):A.thing.close()
class aclosing(AbstractAsyncContextManager):
	'Async context manager for safely finalizing an asynchronously cleaned-up\n    resource such as an async generator, calling its ``aclose()`` method.\n\n    Code like this:\n\n        async with aclosing(<module>.fetch(<arguments>)) as agen:\n            <block>\n\n    is equivalent to this:\n\n        agen = <module>.fetch(<arguments>)\n        try:\n            <block>\n        finally:\n            await agen.aclose()\n\n    '
	def __init__(A,thing):A.thing=thing
	async def __aenter__(A):return A.thing
	async def __aexit__(A,*B):await A.thing.aclose()
class _RedirectStream(AbstractContextManager):
	_stream=_A
	def __init__(A,new_target):A._new_target=new_target;A._old_targets=[]
	def __enter__(A):A._old_targets.append(getattr(sys,A._stream));setattr(sys,A._stream,A._new_target);return A._new_target
	def __exit__(A,exctype,excinst,exctb):setattr(sys,A._stream,A._old_targets.pop())
class redirect_stdout(_RedirectStream):"Context manager for temporarily redirecting stdout to another file.\n\n        # How to send help() to stderr\n        with redirect_stdout(sys.stderr):\n            help(dir)\n\n        # How to write help() to a file\n        with open('help.txt', 'w') as f:\n            with redirect_stdout(f):\n                help(pow)\n    ";_stream='stdout'
class redirect_stderr(_RedirectStream):'Context manager for temporarily redirecting stderr to another file.';_stream='stderr'
class suppress(AbstractContextManager):
	'Context manager to suppress specified exceptions\n\n    After the exception is suppressed, execution proceeds with the next\n    statement following the with statement.\n\n         with suppress(FileNotFoundError):\n             os.remove(somefile)\n         # Execution still resumes here if the file was already removed\n    '
	def __init__(A,*B):A._exceptions=B
	def __enter__(A):0
	def __exit__(B,exctype,excinst,exctb):A=exctype;return A is not _A and issubclass(A,B._exceptions)
class _BaseExitStack:
	'A base class for ExitStack and AsyncExitStack.'
	@staticmethod
	def _create_exit_wrapper(cm,cm_exit):return MethodType(cm_exit,cm)
	@staticmethod
	def _create_cb_wrapper(A,*B,**C):
		def D(exc_type,exc,tb):A(*B,**C)
		return D
	def __init__(A):A._exit_callbacks=deque()
	def pop_all(A):'Preserve the context stack by transferring it to a new instance.';B=type(A)();B._exit_callbacks=A._exit_callbacks;A._exit_callbacks=deque();return B
	def push(A,exit):
		'Registers a callback with the standard __exit__ method signature.\n\n        Can suppress exceptions the same way __exit__ method can.\n        Also accepts any object with an __exit__ method (registering a call\n        to the method instead of the object itself).\n        ';B=type(exit)
		try:C=B.__exit__
		except AttributeError:A._push_exit_callback(exit)
		else:A._push_cm_exit(exit,C)
		return exit
	def enter_context(B,cm):
		'Enters the supplied context manager.\n\n        If successful, also pushes its __exit__ method as a callback and\n        returns the result of the __enter__ method.\n        ';A=type(cm)
		try:C=A.__enter__;D=A.__exit__
		except AttributeError:raise TypeError(f"'{A.__module__}.{A.__qualname__}' object does not support the context manager protocol")from _A
		E=C(cm);B._push_cm_exit(cm,D);return E
	def callback(B,A,*D,**E):'Registers an arbitrary callback and arguments.\n\n        Cannot suppress exceptions.\n        ';C=B._create_cb_wrapper(A,*D,**E);C.__wrapped__=A;B._push_exit_callback(C);return A
	def _push_cm_exit(A,cm,cm_exit):'Helper to correctly register callbacks to __exit__ methods.';B=A._create_exit_wrapper(cm,cm_exit);A._push_exit_callback(B,_C)
	def _push_exit_callback(A,callback,is_sync=_C):A._exit_callbacks.append((is_sync,callback))
class ExitStack(_BaseExitStack,AbstractContextManager):
	'Context manager for dynamic management of a stack of exit callbacks.\n\n    For example:\n        with ExitStack() as stack:\n            files = [stack.enter_context(open(fname)) for fname in filenames]\n            # All opened files will automatically be closed at the end of\n            # the with statement, even if attempts to open files later\n            # in the list raise an exception.\n    '
	def __enter__(A):return A
	def __exit__(C,*A):
		F=A[0]is not _A;G=sys.exc_info()[1]
		def H(new_exc,old_exc):
			C=old_exc;B=new_exc
			while 1:
				A=B.__context__
				if A is _A or A is C:return
				if A is G:break
				B=A
			B.__context__=C
		D=_B;B=_B
		while C._exit_callbacks:
			I,J=C._exit_callbacks.pop();assert I
			try:
				if J(*A):D=_C;B=_B;A=_A,_A,_A
			except:E=sys.exc_info();H(E[1],A[1]);B=_C;A=E
		if B:
			try:K=A[1].__context__;raise A[1]
			except BaseException:A[1].__context__=K;raise
		return F and D
	def close(A):'Immediately unwind the context stack.';A.__exit__(_A,_A,_A)
class AsyncExitStack(_BaseExitStack,AbstractAsyncContextManager):
	'Async context manager for dynamic management of a stack of exit\n    callbacks.\n\n    For example:\n        async with AsyncExitStack() as stack:\n            connections = [await stack.enter_async_context(get_connection())\n                for i in range(5)]\n            # All opened connections will automatically be released at the\n            # end of the async with statement, even if attempts to open a\n            # connection later in the list raise an exception.\n    '
	@staticmethod
	def _create_async_exit_wrapper(cm,cm_exit):return MethodType(cm_exit,cm)
	@staticmethod
	def _create_async_cb_wrapper(A,*B,**C):
		async def D(exc_type,exc,tb):await A(*B,**C)
		return D
	async def enter_async_context(B,cm):
		'Enters the supplied async context manager.\n\n        If successful, also pushes its __aexit__ method as a callback and\n        returns the result of the __aenter__ method.\n        ';A=type(cm)
		try:C=A.__aenter__;D=A.__aexit__
		except AttributeError:raise TypeError(f"'{A.__module__}.{A.__qualname__}' object does not support the asynchronous context manager protocol")from _A
		E=await C(cm);B._push_async_cm_exit(cm,D);return E
	def push_async_exit(A,exit):
		'Registers a coroutine function with the standard __aexit__ method\n        signature.\n\n        Can suppress exceptions the same way __aexit__ method can.\n        Also accepts any object with an __aexit__ method (registering a call\n        to the method instead of the object itself).\n        ';B=type(exit)
		try:C=B.__aexit__
		except AttributeError:A._push_exit_callback(exit,_B)
		else:A._push_async_cm_exit(exit,C)
		return exit
	def push_async_callback(B,A,*D,**E):'Registers an arbitrary coroutine function and arguments.\n\n        Cannot suppress exceptions.\n        ';C=B._create_async_cb_wrapper(A,*D,**E);C.__wrapped__=A;B._push_exit_callback(C,_B);return A
	async def aclose(A):'Immediately unwind the context stack.';await A.__aexit__(_A,_A,_A)
	def _push_async_cm_exit(A,cm,cm_exit):'Helper to correctly register coroutine function to __aexit__\n        method.';B=A._create_async_exit_wrapper(cm,cm_exit);A._push_exit_callback(B,_B)
	async def __aenter__(A):return A
	async def __aexit__(C,*A):
		H=A[0]is not _A;I=sys.exc_info()[1]
		def J(new_exc,old_exc):
			C=old_exc;B=new_exc
			while 1:
				A=B.__context__
				if A is _A or A is C:return
				if A is I:break
				B=A
			B.__context__=C
		D=_B;B=_B
		while C._exit_callbacks:
			K,E=C._exit_callbacks.pop()
			try:
				if K:F=E(*A)
				else:F=await E(*A)
				if F:D=_C;B=_B;A=_A,_A,_A
			except:G=sys.exc_info();J(G[1],A[1]);B=_C;A=G
		if B:
			try:L=A[1].__context__;raise A[1]
			except BaseException:A[1].__context__=L;raise
		return H and D
class nullcontext(AbstractContextManager,AbstractAsyncContextManager):
	'Context manager that does no additional processing.\n\n    Used as a stand-in for a normal context manager, when a particular\n    block of code is only sometimes used with a normal context manager:\n\n    cm = optional_cm if condition else nullcontext()\n    with cm:\n        # Perform operation, using optional_cm if condition is True\n    '
	def __init__(A,enter_result=_A):A.enter_result=enter_result
	def __enter__(A):return A.enter_result
	def __exit__(A,*B):0
	async def __aenter__(A):return A.enter_result
	async def __aexit__(A,*B):0
class chdir(AbstractContextManager):
	'Non thread-safe context manager to change the current working directory.'
	def __init__(A,path):A.path=path;A._old_cwd=[]
	def __enter__(A):A._old_cwd.append(os.getcwd());os.chdir(A.path)
	def __exit__(A,*B):os.chdir(A._old_cwd.pop())