'Core implementation of import.\n\nThis module is NOT meant to be directly imported! It has been designed such\nthat it can be bootstrapped into Python as the implementation of import. As\nsuch it requires the injection of specific modules and attributes in order to\nwork. One should use importlib as the public-facing version of this module.\n\n'
_S='missing loader'
_R='<module {!r} ({})>'
_Q='_ORIGIN'
_P='<module {!r} from {!r}>'
_O='<module {!r} ({!r})>'
_N='<module {!r}>'
_M='{!r} is not a built-in module'
_L='cannot release un-acquired lock'
_K='exec_module'
_J='__package__'
_I='__loader__'
_H='__name__'
_G='__spec__'
_F='__file__'
_E='__path__'
_D='.'
_C=True
_B=False
_A=None
def _object_name(obj):
	try:return obj.__qualname__
	except AttributeError:return type(obj).__qualname__
_thread=_A
_warnings=_A
_weakref=_A
_bootstrap_external=_A
def _wrap(new,old):
	'Simple substitute for functools.update_wrapper.'
	for replace in['__module__',_H,'__qualname__','__doc__']:
		if hasattr(old,replace):setattr(new,replace,getattr(old,replace))
	new.__dict__.update(old.__dict__)
def _new_module(name):return type(sys)(name)
_module_locks={}
_blocking_on={}
class _DeadlockError(RuntimeError):0
class _ModuleLock:
	'A recursive lock implementation which is able to detect deadlocks\n    (e.g. thread 1 trying to take locks A then B, and thread 2 trying to\n    take locks B then A).\n    '
	def __init__(self,name):self.lock=_thread.allocate_lock();self.wakeup=_thread.allocate_lock();self.name=name;self.owner=_A;self.count=0;self.waiters=0
	def has_deadlock(self):
		me=_thread.get_ident();tid=self.owner;seen=set()
		while _C:
			lock=_blocking_on.get(tid)
			if lock is _A:return _B
			tid=lock.owner
			if tid==me:return _C
			if tid in seen:return _B
			seen.add(tid)
	def acquire(self):
		'\n        Acquire the module lock.  If a potential deadlock is detected,\n        a _DeadlockError is raised.\n        Otherwise, the lock is always acquired and True is returned.\n        ';tid=_thread.get_ident();_blocking_on[tid]=self
		try:
			while _C:
				with self.lock:
					if self.count==0 or self.owner==tid:self.owner=tid;self.count+=1;return _C
					if self.has_deadlock():raise _DeadlockError('deadlock detected by %r'%self)
					if self.wakeup.acquire(_B):self.waiters+=1
				self.wakeup.acquire();self.wakeup.release()
		finally:del _blocking_on[tid]
	def release(self):
		tid=_thread.get_ident()
		with self.lock:
			if self.owner!=tid:raise RuntimeError(_L)
			assert self.count>0;self.count-=1
			if self.count==0:
				self.owner=_A
				if self.waiters:self.waiters-=1;self.wakeup.release()
	def __repr__(self):return'_ModuleLock({!r}) at {}'.format(self.name,id(self))
class _DummyModuleLock:
	'A simple _ModuleLock equivalent for Python builds without\n    multi-threading support.'
	def __init__(self,name):self.name=name;self.count=0
	def acquire(self):self.count+=1;return _C
	def release(self):
		if self.count==0:raise RuntimeError(_L)
		self.count-=1
	def __repr__(self):return'_DummyModuleLock({!r}) at {}'.format(self.name,id(self))
class _ModuleLockManager:
	def __init__(self,name):self._name=name;self._lock=_A
	def __enter__(self):self._lock=_get_module_lock(self._name);self._lock.acquire()
	def __exit__(self,*args,**kwargs):self._lock.release()
def _get_module_lock(name):
	'Get or create the module lock for a given module name.\n\n    Acquire/release internally the global import lock to protect\n    _module_locks.';_imp.acquire_lock()
	try:
		try:lock=_module_locks[name]()
		except KeyError:lock=_A
		if lock is _A:
			if _thread is _A:lock=_DummyModuleLock(name)
			else:lock=_ModuleLock(name)
			def cb(ref,name=name):
				_imp.acquire_lock()
				try:
					if _module_locks.get(name)is ref:del _module_locks[name]
				finally:_imp.release_lock()
			_module_locks[name]=_weakref.ref(lock,cb)
	finally:_imp.release_lock()
	return lock
def _lock_unlock_module(name):
	'Acquires then releases the module lock for a given module name.\n\n    This is used to ensure a module is completely initialized, in the\n    event it is being imported by another thread.\n    ';lock=_get_module_lock(name)
	try:lock.acquire()
	except _DeadlockError:pass
	else:lock.release()
def _call_with_frames_removed(f,*args,**kwds):'remove_importlib_frames in import.c will always remove sequences\n    of importlib frames that end with a call to this function\n\n    Use it instead of a normal call in places where including the importlib\n    frames introduces unwanted noise into the traceback (e.g. when executing\n    module code)\n    ';return f(*args,**kwds)
def _verbose_message(message,*args,verbosity=1):
	'Print the message to stderr if -v/PYTHONVERBOSE is turned on.'
	if sys.flags.verbose>=verbosity and hasattr(sys,'stderr'):
		if not message.startswith(('#','import ')):message='# '+message
		print(message.format(*args),file=sys.stderr)
def _requires_builtin(fxn):
	'Decorator to verify the named module is built-in.'
	def _requires_builtin_wrapper(self,fullname):
		if fullname not in sys.builtin_module_names:raise ImportError(_M.format(fullname),name=fullname)
		return fxn(self,fullname)
	_wrap(_requires_builtin_wrapper,fxn);return _requires_builtin_wrapper
def _requires_frozen(fxn):
	'Decorator to verify the named module is frozen.'
	def _requires_frozen_wrapper(self,fullname):
		if not _imp.is_frozen(fullname):raise ImportError('{!r} is not a frozen module'.format(fullname),name=fullname)
		return fxn(self,fullname)
	_wrap(_requires_frozen_wrapper,fxn);return _requires_frozen_wrapper
def _load_module_shim(self,fullname):
	'Load the specified module into sys.modules and return it.\n\n    This method is deprecated.  Use loader.exec_module() instead.\n\n    ';msg='the load_module() method is deprecated and slated for removal in Python 3.12; use exec_module() instead';_warnings.warn(msg,DeprecationWarning);spec=spec_from_loader(fullname,self)
	if fullname in sys.modules:module=sys.modules[fullname];_exec(spec,module);return sys.modules[fullname]
	else:return _load(spec)
def _module_repr(module):
	'The implementation of ModuleType.__repr__().';loader=getattr(module,_I,_A)
	if(spec:=getattr(module,_G,_A)):return _module_repr_from_spec(spec)
	elif hasattr(loader,'module_repr'):
		try:return loader.module_repr(module)
		except Exception:pass
	try:name=module.__name__
	except AttributeError:name='?'
	try:filename=module.__file__
	except AttributeError:
		if loader is _A:return _N.format(name)
		else:return _O.format(name,loader)
	else:return _P.format(name,filename)
class ModuleSpec:
	'The specification for a module, used for loading.\n\n    A module\'s spec is the source for information about the module.  For\n    data associated with the module, including source, use the spec\'s\n    loader.\n\n    `name` is the absolute name of the module.  `loader` is the loader\n    to use when loading the module.  `parent` is the name of the\n    package the module is in.  The parent is derived from the name.\n\n    `is_package` determines if the module is considered a package or\n    not.  On modules this is reflected by the `__path__` attribute.\n\n    `origin` is the specific location used by the loader from which to\n    load the module, if that information is available.  When filename is\n    set, origin will match.\n\n    `has_location` indicates that a spec\'s "origin" reflects a location.\n    When this is True, `__file__` attribute of the module is set.\n\n    `cached` is the location of the cached bytecode file, if any.  It\n    corresponds to the `__cached__` attribute.\n\n    `submodule_search_locations` is the sequence of path entries to\n    search when importing submodules.  If set, is_package should be\n    True--and False otherwise.\n\n    Packages are simply modules that (may) have submodules.  If a spec\n    has a non-None value in `submodule_search_locations`, the import\n    system will consider modules loaded from the spec as packages.\n\n    Only finders (see importlib.abc.MetaPathFinder and\n    importlib.abc.PathEntryFinder) should modify ModuleSpec instances.\n\n    '
	def __init__(self,name,loader,*,origin=_A,loader_state=_A,is_package=_A):self.name=name;self.loader=loader;self.origin=origin;self.loader_state=loader_state;self.submodule_search_locations=[]if is_package else _A;self._uninitialized_submodules=[];self._set_fileattr=_B;self._cached=_A
	def __repr__(self):
		args=['name={!r}'.format(self.name),'loader={!r}'.format(self.loader)]
		if self.origin is not _A:args.append('origin={!r}'.format(self.origin))
		if self.submodule_search_locations is not _A:args.append('submodule_search_locations={}'.format(self.submodule_search_locations))
		return'{}({})'.format(self.__class__.__name__,', '.join(args))
	def __eq__(self,other):
		smsl=self.submodule_search_locations
		try:return self.name==other.name and self.loader==other.loader and self.origin==other.origin and smsl==other.submodule_search_locations and self.cached==other.cached and self.has_location==other.has_location
		except AttributeError:return NotImplemented
	@property
	def cached(self):
		if self._cached is _A:
			if self.origin is not _A and self._set_fileattr:
				if _bootstrap_external is _A:raise NotImplementedError
				self._cached=_bootstrap_external._get_cached(self.origin)
		return self._cached
	@cached.setter
	def cached(self,cached):self._cached=cached
	@property
	def parent(self):
		"The name of the module's parent."
		if self.submodule_search_locations is _A:return self.name.rpartition(_D)[0]
		else:return self.name
	@property
	def has_location(self):return self._set_fileattr
	@has_location.setter
	def has_location(self,value):self._set_fileattr=bool(value)
def spec_from_loader(name,loader,*,origin=_A,is_package=_A):
	'Return a module spec based on various loader methods.'
	if origin is _A:origin=getattr(loader,_Q,_A)
	if not origin and hasattr(loader,'get_filename'):
		if _bootstrap_external is _A:raise NotImplementedError
		spec_from_file_location=_bootstrap_external.spec_from_file_location
		if is_package is _A:return spec_from_file_location(name,loader=loader)
		search=[]if is_package else _A;return spec_from_file_location(name,loader=loader,submodule_search_locations=search)
	if is_package is _A:
		if hasattr(loader,'is_package'):
			try:is_package=loader.is_package(name)
			except ImportError:is_package=_A
		else:is_package=_B
	return ModuleSpec(name,loader,origin=origin,is_package=is_package)
def _spec_from_module(module,loader=_A,origin=_A):
	try:spec=module.__spec__
	except AttributeError:pass
	else:
		if spec is not _A:return spec
	name=module.__name__
	if loader is _A:
		try:loader=module.__loader__
		except AttributeError:pass
	try:location=module.__file__
	except AttributeError:location=_A
	if origin is _A:
		if loader is not _A:origin=getattr(loader,_Q,_A)
		if not origin and location is not _A:origin=location
	try:cached=module.__cached__
	except AttributeError:cached=_A
	try:submodule_search_locations=list(module.__path__)
	except AttributeError:submodule_search_locations=_A
	spec=ModuleSpec(name,loader,origin=origin);spec._set_fileattr=_B if location is _A else origin==location;spec.cached=cached;spec.submodule_search_locations=submodule_search_locations;return spec
def _init_module_attrs(spec,module,*,override=_B):
	if override or getattr(module,_H,_A)is _A:
		try:module.__name__=spec.name
		except AttributeError:pass
	if override or getattr(module,_I,_A)is _A:
		loader=spec.loader
		if loader is _A:
			if spec.submodule_search_locations is not _A:
				if _bootstrap_external is _A:raise NotImplementedError
				NamespaceLoader=_bootstrap_external.NamespaceLoader;loader=NamespaceLoader.__new__(NamespaceLoader);loader._path=spec.submodule_search_locations;spec.loader=loader;module.__file__=_A
		try:module.__loader__=loader
		except AttributeError:pass
	if override or getattr(module,_J,_A)is _A:
		try:module.__package__=spec.parent
		except AttributeError:pass
	try:module.__spec__=spec
	except AttributeError:pass
	if override or getattr(module,_E,_A)is _A:
		if spec.submodule_search_locations is not _A:
			try:module.__path__=spec.submodule_search_locations
			except AttributeError:pass
	if spec.has_location:
		if override or getattr(module,_F,_A)is _A:
			try:module.__file__=spec.origin
			except AttributeError:pass
		if override or getattr(module,'__cached__',_A)is _A:
			if spec.cached is not _A:
				try:module.__cached__=spec.cached
				except AttributeError:pass
	return module
def module_from_spec(spec):
	'Create a module based on the provided spec.';module=_A
	if hasattr(spec.loader,'create_module'):module=spec.loader.create_module(spec)
	elif hasattr(spec.loader,_K):raise ImportError('loaders that define exec_module() must also define create_module()')
	if module is _A:module=_new_module(spec.name)
	_init_module_attrs(spec,module);return module
def _module_repr_from_spec(spec):
	'Return the repr to use for the module.';name='?'if spec.name is _A else spec.name
	if spec.origin is _A:
		if spec.loader is _A:return _N.format(name)
		else:return _O.format(name,spec.loader)
	elif spec.has_location:return _P.format(name,spec.origin)
	else:return _R.format(spec.name,spec.origin)
def _exec(spec,module):
	"Execute the spec's specified module in an existing module's namespace.";name=spec.name
	with _ModuleLockManager(name):
		if sys.modules.get(name)is not module:msg='module {!r} not in sys.modules'.format(name);raise ImportError(msg,name=name)
		try:
			if spec.loader is _A:
				if spec.submodule_search_locations is _A:raise ImportError(_S,name=spec.name)
				_init_module_attrs(spec,module,override=_C)
			else:
				_init_module_attrs(spec,module,override=_C)
				if not hasattr(spec.loader,_K):msg=f"{_object_name(spec.loader)}.exec_module() not found; falling back to load_module()";_warnings.warn(msg,ImportWarning);spec.loader.load_module(name)
				else:spec.loader.exec_module(module)
		finally:module=sys.modules.pop(spec.name);sys.modules[spec.name]=module
	return module
def _load_backward_compatible(spec):
	try:spec.loader.load_module(spec.name)
	except:
		if spec.name in sys.modules:module=sys.modules.pop(spec.name);sys.modules[spec.name]=module
		raise
	module=sys.modules.pop(spec.name);sys.modules[spec.name]=module
	if getattr(module,_I,_A)is _A:
		try:module.__loader__=spec.loader
		except AttributeError:pass
	if getattr(module,_J,_A)is _A:
		try:
			module.__package__=module.__name__
			if not hasattr(module,_E):module.__package__=spec.name.rpartition(_D)[0]
		except AttributeError:pass
	if getattr(module,_G,_A)is _A:
		try:module.__spec__=spec
		except AttributeError:pass
	return module
def _load_unlocked(spec):
	if spec.loader is not _A:
		if not hasattr(spec.loader,_K):msg=f"{_object_name(spec.loader)}.exec_module() not found; falling back to load_module()";_warnings.warn(msg,ImportWarning);return _load_backward_compatible(spec)
	module=module_from_spec(spec);spec._initializing=_C
	try:
		sys.modules[spec.name]=module
		try:
			if spec.loader is _A:
				if spec.submodule_search_locations is _A:raise ImportError(_S,name=spec.name)
			else:spec.loader.exec_module(module)
		except:
			try:del sys.modules[spec.name]
			except KeyError:pass
			raise
		module=sys.modules.pop(spec.name);sys.modules[spec.name]=module;_verbose_message('import {!r} # {!r}',spec.name,spec.loader)
	finally:spec._initializing=_B
	return module
def _load(spec):
	"Return a new module object, loaded by the spec's loader.\n\n    The module is not added to its parent.\n\n    If a module is already in sys.modules, that existing module gets\n    clobbered.\n\n    "
	with _ModuleLockManager(spec.name):return _load_unlocked(spec)
class BuiltinImporter:
	'Meta path import for built-in modules.\n\n    All methods are either class or static methods to avoid the need to\n    instantiate the class.\n\n    ';_ORIGIN='built-in'
	@staticmethod
	def module_repr(module):'Return repr for the module.\n\n        The method is deprecated.  The import machinery does the job itself.\n\n        ';_warnings.warn('BuiltinImporter.module_repr() is deprecated and slated for removal in Python 3.12',DeprecationWarning);return f"<module {module.__name__!r} ({BuiltinImporter._ORIGIN})>"
	@classmethod
	def find_spec(cls,fullname,path=_A,target=_A):
		if path is not _A:return
		if _imp.is_builtin(fullname):return spec_from_loader(fullname,cls,origin=cls._ORIGIN)
		else:return
	@classmethod
	def find_module(cls,fullname,path=_A):"Find the built-in module.\n\n        If 'path' is ever specified then the search is considered a failure.\n\n        This method is deprecated.  Use find_spec() instead.\n\n        ";_warnings.warn('BuiltinImporter.find_module() is deprecated and slated for removal in Python 3.12; use find_spec() instead',DeprecationWarning);spec=cls.find_spec(fullname,path);return spec.loader if spec is not _A else _A
	@staticmethod
	def create_module(spec):
		'Create a built-in module'
		if spec.name not in sys.builtin_module_names:raise ImportError(_M.format(spec.name),name=spec.name)
		return _call_with_frames_removed(_imp.create_builtin,spec)
	@staticmethod
	def exec_module(module):'Exec a built-in module';_call_with_frames_removed(_imp.exec_builtin,module)
	@classmethod
	@_requires_builtin
	def get_code(cls,fullname):'Return None as built-in modules do not have code objects.'
	@classmethod
	@_requires_builtin
	def get_source(cls,fullname):'Return None as built-in modules do not have source code.'
	@classmethod
	@_requires_builtin
	def is_package(cls,fullname):'Return False as built-in modules are never packages.';return _B
	load_module=classmethod(_load_module_shim)
class FrozenImporter:
	'Meta path import for frozen modules.\n\n    All methods are either class or static methods to avoid the need to\n    instantiate the class.\n\n    ';_ORIGIN='frozen'
	@staticmethod
	def module_repr(m):'Return repr for the module.\n\n        The method is deprecated.  The import machinery does the job itself.\n\n        ';_warnings.warn('FrozenImporter.module_repr() is deprecated and slated for removal in Python 3.12',DeprecationWarning);return _R.format(m.__name__,FrozenImporter._ORIGIN)
	@classmethod
	def _fix_up_module(cls,module):
		spec=module.__spec__;state=spec.loader_state
		if state is _A:
			origname=vars(module).pop('__origname__',_A);assert origname,'see PyImport_ImportFrozenModuleObject()';ispkg=hasattr(module,_E);assert _imp.is_frozen_package(module.__name__)==ispkg,ispkg;filename,pkgdir=cls._resolve_filename(origname,spec.name,ispkg);spec.loader_state=type(sys.implementation)(filename=filename,origname=origname);__path__=spec.submodule_search_locations
			if ispkg:
				assert __path__==[],__path__
				if pkgdir:spec.submodule_search_locations.insert(0,pkgdir)
			else:assert __path__ is _A,__path__
			assert not hasattr(module,_F),module.__file__
			if filename:
				try:module.__file__=filename
				except AttributeError:pass
			if ispkg:
				if module.__path__!=__path__:assert module.__path__==[],module.__path__;module.__path__.extend(__path__)
		else:
			__path__=spec.submodule_search_locations;ispkg=__path__ is not _A;assert sorted(vars(state))==['filename','origname'],state
			if state.origname:
				__file__,pkgdir=cls._resolve_filename(state.origname,spec.name,ispkg);assert state.filename==__file__,(state.filename,__file__)
				if pkgdir:assert __path__==[pkgdir],(__path__,pkgdir)
				else:assert __path__==([]if ispkg else _A),__path__
			else:__file__=_A;assert state.filename is _A,state.filename;assert __path__==([]if ispkg else _A),__path__
			if __file__:assert hasattr(module,_F);assert module.__file__==__file__,(module.__file__,__file__)
			else:assert not hasattr(module,_F),module.__file__
			if ispkg:assert hasattr(module,_E);assert module.__path__==__path__,(module.__path__,__path__)
			else:assert not hasattr(module,_E),module.__path__
		assert not spec.has_location
	@classmethod
	def _resolve_filename(cls,fullname,alias=_A,ispkg=_B):
		if not fullname or not getattr(sys,'_stdlib_dir',_A):return _A,_A
		try:sep=cls._SEP
		except AttributeError:sep=cls._SEP='\\'if sys.platform=='win32'else'/'
		if fullname!=alias:
			if fullname.startswith('<'):
				fullname=fullname[1:]
				if not ispkg:fullname=f"{fullname}.__init__"
			else:ispkg=_B
		relfile=fullname.replace(_D,sep)
		if ispkg:pkgdir=f"{sys._stdlib_dir}{sep}{relfile}";filename=f"{pkgdir}{sep}__init__.py"
		else:pkgdir=_A;filename=f"{sys._stdlib_dir}{sep}{relfile}.py"
		return filename,pkgdir
	@classmethod
	def find_spec(cls,fullname,path=_A,target=_A):
		info=_call_with_frames_removed(_imp.find_frozen,fullname)
		if info is _A:return
		_,ispkg,origname=info;spec=spec_from_loader(fullname,cls,origin=cls._ORIGIN,is_package=ispkg);filename,pkgdir=cls._resolve_filename(origname,fullname,ispkg);spec.loader_state=type(sys.implementation)(filename=filename,origname=origname)
		if pkgdir:spec.submodule_search_locations.insert(0,pkgdir)
		return spec
	@classmethod
	def find_module(cls,fullname,path=_A):'Find a frozen module.\n\n        This method is deprecated.  Use find_spec() instead.\n\n        ';_warnings.warn('FrozenImporter.find_module() is deprecated and slated for removal in Python 3.12; use find_spec() instead',DeprecationWarning);return cls if _imp.is_frozen(fullname)else _A
	@staticmethod
	def create_module(spec):
		'Set __file__, if able.';module=_new_module(spec.name)
		try:filename=spec.loader_state.filename
		except AttributeError:pass
		else:
			if filename:module.__file__=filename
		return module
	@staticmethod
	def exec_module(module):spec=module.__spec__;name=spec.name;code=_call_with_frames_removed(_imp.get_frozen_object,name);exec(code,module.__dict__)
	@classmethod
	def load_module(cls,fullname):
		'Load a frozen module.\n\n        This method is deprecated.  Use exec_module() instead.\n\n        ';module=_load_module_shim(cls,fullname);info=_imp.find_frozen(fullname);assert info is not _A;_,ispkg,origname=info;module.__origname__=origname;vars(module).pop(_F,_A)
		if ispkg:module.__path__=[]
		cls._fix_up_module(module);return module
	@classmethod
	@_requires_frozen
	def get_code(cls,fullname):'Return the code object for the frozen module.';return _imp.get_frozen_object(fullname)
	@classmethod
	@_requires_frozen
	def get_source(cls,fullname):'Return None as frozen modules do not have source code.'
	@classmethod
	@_requires_frozen
	def is_package(cls,fullname):'Return True if the frozen module is a package.';return _imp.is_frozen_package(fullname)
class _ImportLockContext:
	'Context manager for the import lock.'
	def __enter__(self):'Acquire the import lock.';_imp.acquire_lock()
	def __exit__(self,exc_type,exc_value,exc_traceback):'Release the import lock regardless of any raised exceptions.';_imp.release_lock()
def _resolve_name(name,package,level):
	'Resolve a relative module name to an absolute one.';bits=package.rsplit(_D,level-1)
	if len(bits)<level:raise ImportError('attempted relative import beyond top-level package')
	base=bits[0];return'{}.{}'.format(base,name)if name else base
def _find_spec_legacy(finder,name,path):
	msg=f"{_object_name(finder)}.find_spec() not found; falling back to find_module()";_warnings.warn(msg,ImportWarning);loader=finder.find_module(name,path)
	if loader is _A:return
	return spec_from_loader(name,loader)
def _find_spec(name,path,target=_A):
	"Find a module's spec.";meta_path=sys.meta_path
	if meta_path is _A:raise ImportError('sys.meta_path is None, Python is likely shutting down')
	if not meta_path:_warnings.warn('sys.meta_path is empty',ImportWarning)
	is_reload=name in sys.modules
	for finder in meta_path:
		with _ImportLockContext():
			try:find_spec=finder.find_spec
			except AttributeError:
				spec=_find_spec_legacy(finder,name,path)
				if spec is _A:continue
			else:spec=find_spec(name,path,target)
		if spec is not _A:
			if not is_reload and name in sys.modules:
				module=sys.modules[name]
				try:__spec__=module.__spec__
				except AttributeError:return spec
				else:
					if __spec__ is _A:return spec
					else:return __spec__
			else:return spec
	else:return
def _sanity_check(name,package,level):
	'Verify arguments are "sane".'
	if not isinstance(name,str):raise TypeError('module name must be str, not {}'.format(type(name)))
	if level<0:raise ValueError('level must be >= 0')
	if level>0:
		if not isinstance(package,str):raise TypeError('__package__ not set to a string')
		elif not package:raise ImportError('attempted relative import with no known parent package')
	if not name and level==0:raise ValueError('Empty module name')
_ERR_MSG_PREFIX='No module named '
_ERR_MSG=_ERR_MSG_PREFIX+'{!r}'
def _find_and_load_unlocked(name,import_):
	path=_A;parent=name.rpartition(_D)[0];parent_spec=_A
	if parent:
		if parent not in sys.modules:_call_with_frames_removed(import_,parent)
		if name in sys.modules:return sys.modules[name]
		parent_module=sys.modules[parent]
		try:path=parent_module.__path__
		except AttributeError:msg=(_ERR_MSG+'; {!r} is not a package').format(name,parent);raise ModuleNotFoundError(msg,name=name)from _A
		parent_spec=parent_module.__spec__;child=name.rpartition(_D)[2]
	spec=_find_spec(name,path)
	if spec is _A:raise ModuleNotFoundError(_ERR_MSG.format(name),name=name)
	else:
		if parent_spec:parent_spec._uninitialized_submodules.append(child)
		try:module=_load_unlocked(spec)
		finally:
			if parent_spec:parent_spec._uninitialized_submodules.pop()
	if parent:
		parent_module=sys.modules[parent]
		try:setattr(parent_module,child,module)
		except AttributeError:msg=f"Cannot set an attribute on {parent!r} for child module {child!r}";_warnings.warn(msg,ImportWarning)
	return module
_NEEDS_LOADING=object()
def _find_and_load(name,import_):
	'Find and load the module.';module=sys.modules.get(name,_NEEDS_LOADING)
	if module is _NEEDS_LOADING or getattr(getattr(module,_G,_A),'_initializing',_B):
		with _ModuleLockManager(name):
			module=sys.modules.get(name,_NEEDS_LOADING)
			if module is _NEEDS_LOADING:return _find_and_load_unlocked(name,import_)
		_lock_unlock_module(name)
	if module is _A:message='import of {} halted; None in sys.modules'.format(name);raise ModuleNotFoundError(message,name=name)
	return module
def _gcd_import(name,package=_A,level=0):
	'Import and return the module based on its name, the package the call is\n    being made from, and the level adjustment.\n\n    This function represents the greatest common denominator of functionality\n    between import_module and __import__. This includes setting __package__ if\n    the loader did not.\n\n    ';_sanity_check(name,package,level)
	if level>0:name=_resolve_name(name,package,level)
	return _find_and_load(name,_gcd_import)
def _handle_fromlist(module,fromlist,import_,*,recursive=_B):
	"Figure out what __import__ should return.\n\n    The import_ parameter is a callable which takes the name of module to\n    import. It is required to decouple the function from assuming importlib's\n    import implementation is desired.\n\n    "
	for x in fromlist:
		if not isinstance(x,str):
			if recursive:where=module.__name__+'.__all__'
			else:where="``from list''"
			raise TypeError(f"Item in {where} must be str, not {type(x).__name__}")
		elif x=='*':
			if not recursive and hasattr(module,'__all__'):_handle_fromlist(module,module.__all__,import_,recursive=_C)
		elif not hasattr(module,x):
			from_name='{}.{}'.format(module.__name__,x)
			try:_call_with_frames_removed(import_,from_name)
			except ModuleNotFoundError as exc:
				if exc.name==from_name and sys.modules.get(from_name,_NEEDS_LOADING)is not _A:continue
				raise
	return module
def _calc___package__(globals):
	'Calculate what __package__ should be.\n\n    __package__ is not guaranteed to be defined or could be set to None\n    to represent that its proper value is unknown.\n\n    ';package=globals.get(_J);spec=globals.get(_G)
	if package is not _A:
		if spec is not _A and package!=spec.parent:_warnings.warn(f"__package__ != __spec__.parent ({package!r} != {spec.parent!r})",ImportWarning,stacklevel=3)
		return package
	elif spec is not _A:return spec.parent
	else:
		_warnings.warn("can't resolve package from __spec__ or __package__, falling back on __name__ and __path__",ImportWarning,stacklevel=3);package=globals[_H]
		if _E not in globals:package=package.rpartition(_D)[0]
	return package
def __import__(name,globals=_A,locals=_A,fromlist=(),level=0):
	"Import a module.\n\n    The 'globals' argument is used to infer where the import is occurring from\n    to handle relative imports. The 'locals' argument is ignored. The\n    'fromlist' argument specifies what should exist as attributes on the module\n    being imported (e.g. ``from module import <fromlist>``).  The 'level'\n    argument represents the package location to import from in a relative\n    import (e.g. ``from ..pkg import mod`` would have a 'level' of 2).\n\n    "
	if level==0:module=_gcd_import(name)
	else:globals_=globals if globals is not _A else{};package=_calc___package__(globals_);module=_gcd_import(name,package,level)
	if not fromlist:
		if level==0:return _gcd_import(name.partition(_D)[0])
		elif not name:return module
		else:cut_off=len(name)-len(name.partition(_D)[0]);return sys.modules[module.__name__[:len(module.__name__)-cut_off]]
	elif hasattr(module,_E):return _handle_fromlist(module,fromlist,_gcd_import)
	else:return module
def _builtin_from_name(name):
	spec=BuiltinImporter.find_spec(name)
	if spec is _A:raise ImportError('no built-in module named '+name)
	return _load_unlocked(spec)
def _setup(sys_module,_imp_module):
	'Setup importlib by importing needed built-in modules and injecting them\n    into the global namespace.\n\n    As sys is needed for sys.modules access and _imp is needed to load built-in\n    modules, those two modules must be explicitly passed in.\n\n    ';global _imp,sys;_imp=_imp_module;sys=sys_module;module_type=type(sys)
	for(name,module)in sys.modules.items():
		if isinstance(module,module_type):
			if name in sys.builtin_module_names:loader=BuiltinImporter
			elif _imp.is_frozen(name):loader=FrozenImporter
			else:continue
			spec=_spec_from_module(module,loader);_init_module_attrs(spec,module)
			if loader is FrozenImporter:loader._fix_up_module(module)
	self_module=sys.modules[__name__]
	for builtin_name in('_thread','_warnings','_weakref'):
		if builtin_name not in sys.modules:builtin_module=_builtin_from_name(builtin_name)
		else:builtin_module=sys.modules[builtin_name]
		setattr(self_module,builtin_name,builtin_module)
def _install(sys_module,_imp_module):'Install importers for builtin and frozen modules';_setup(sys_module,_imp_module);sys.meta_path.append(BuiltinImporter);sys.meta_path.append(FrozenImporter)
def _install_external_importers():'Install importers that require external filesystem access';global _bootstrap_external;import _frozen_importlib_external;_bootstrap_external=_frozen_importlib_external;_frozen_importlib_external._install(sys.modules[__name__])