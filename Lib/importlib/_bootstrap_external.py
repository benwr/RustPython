'Core implementation of path-based import.\n\nThis module is NOT meant to be directly imported! It has been designed such\nthat it can be bootstrapped into Python as the implementation of import. As\nsuch it requires the injection of specific modules and attributes in order to\nwork. One should use importlib as the public-facing version of this module.\n\n'
_I='sys.implementation.cache_tag is None'
_H='path'
_G='mtime'
_F='__init__'
_E='little'
_D=False
_C=True
_B='.'
_A=None
_bootstrap=_A
import _imp,_io,sys,_warnings,marshal
_MS_WINDOWS=sys.platform=='win32'
if _MS_WINDOWS:import nt as _os,winreg
else:import posix as _os
if _MS_WINDOWS:path_separators=['\\','/']
else:path_separators=['/']
assert all(len(sep)==1 for sep in path_separators)
path_sep=path_separators[0]
path_sep_tuple=tuple(path_separators)
path_separators=''.join(path_separators)
_pathseps_with_colon={f":{s}"for s in path_separators}
_CASE_INSENSITIVE_PLATFORMS_STR_KEY='win',
_CASE_INSENSITIVE_PLATFORMS_BYTES_KEY='cygwin','darwin'
_CASE_INSENSITIVE_PLATFORMS=_CASE_INSENSITIVE_PLATFORMS_BYTES_KEY+_CASE_INSENSITIVE_PLATFORMS_STR_KEY
def _make_relax_case():
	if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS):
		if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS_STR_KEY):key='PYTHONCASEOK'
		else:key=b'PYTHONCASEOK'
		def _relax_case():'True if filenames must be checked case-insensitively and ignore environment flags are not set.';return not sys.flags.ignore_environment and key in _os.environ
	else:
		def _relax_case():'True if filenames must be checked case-insensitively.';return _D
	return _relax_case
_relax_case=_make_relax_case()
def _pack_uint32(x):'Convert a 32-bit integer to little-endian.';return(int(x)&4294967295).to_bytes(4,_E)
def _unpack_uint32(data):'Convert 4 bytes in little-endian to an integer.';assert len(data)==4;return int.from_bytes(data,_E)
def _unpack_uint16(data):'Convert 2 bytes in little-endian to an integer.';assert len(data)==2;return int.from_bytes(data,_E)
if _MS_WINDOWS:
	def _path_join(*path_parts):
		'Replacement for os.path.join().'
		if not path_parts:return''
		if len(path_parts)==1:return path_parts[0]
		root='';path=[]
		for(new_root,tail)in map(_os._path_splitroot,path_parts):
			if new_root.startswith(path_sep_tuple)or new_root.endswith(path_sep_tuple):root=new_root.rstrip(path_separators)or root;path=[path_sep+tail]
			elif new_root.endswith(':'):
				if root.casefold()!=new_root.casefold():root=new_root;path=[tail]
				else:path.append(tail)
			else:root=new_root or root;path.append(tail)
		path=[p.rstrip(path_separators)for p in path if p]
		if len(path)==1 and not path[0]:return root+path_sep
		return root+path_sep.join(path)
else:
	def _path_join(*path_parts):'Replacement for os.path.join().';return path_sep.join([part.rstrip(path_separators)for part in path_parts if part])
def _path_split(path):
	'Replacement for os.path.split().';i=max(path.rfind(p)for p in path_separators)
	if i<0:return'',path
	return path[:i],path[i+1:]
def _path_stat(path):'Stat the path.\n\n    Made a separate function to make it easier to override in experiments\n    (e.g. cache stat results).\n\n    ';return _os.stat(path)
def _path_is_mode_type(path,mode):
	'Test whether the path is the specified mode type.'
	try:stat_info=_path_stat(path)
	except OSError:return _D
	return stat_info.st_mode&61440==mode
def _path_isfile(path):'Replacement for os.path.isfile.';return _path_is_mode_type(path,32768)
def _path_isdir(path):
	'Replacement for os.path.isdir.'
	if not path:path=_os.getcwd()
	return _path_is_mode_type(path,16384)
if _MS_WINDOWS:
	def _path_isabs(path):
		'Replacement for os.path.isabs.'
		if not path:return _D
		root=_os._path_splitroot(path)[0].replace('/','\\');return len(root)>1 and(root.startswith('\\\\')or root.endswith('\\'))
else:
	def _path_isabs(path):'Replacement for os.path.isabs.';return path.startswith(path_separators)
def _write_atomic(path,data,mode=438):
	'Best-effort function to write data to a path atomically.\n    Be prepared to handle a FileExistsError if concurrent writing of the\n    temporary file is attempted.';path_tmp='{}.{}'.format(path,id(path));fd=_os.open(path_tmp,_os.O_EXCL|_os.O_CREAT|_os.O_WRONLY,mode&438)
	try:
		with _io.FileIO(fd,'wb')as file:file.write(data)
		_os.replace(path_tmp,path)
	except OSError:
		try:_os.unlink(path_tmp)
		except OSError:pass
		raise
_code_type=type(_write_atomic.__code__)
MAGIC_NUMBER=(3495).to_bytes(2,_E)+b'\r\n'
_RAW_MAGIC_NUMBER=int.from_bytes(MAGIC_NUMBER,_E)
_PYCACHE='__pycache__'
_OPT='opt-'
SOURCE_SUFFIXES=['.py']
if _MS_WINDOWS:SOURCE_SUFFIXES.append('.pyw')
EXTENSION_SUFFIXES=_imp.extension_suffixes()
BYTECODE_SUFFIXES=['.pyc']
DEBUG_BYTECODE_SUFFIXES=OPTIMIZED_BYTECODE_SUFFIXES=BYTECODE_SUFFIXES
def cache_from_source(path,debug_override=_A,*,optimization=_A):
	"Given the path to a .py file, return the path to its .pyc file.\n\n    The .py file does not need to exist; this simply returns the path to the\n    .pyc file calculated as if the .py file were imported.\n\n    The 'optimization' parameter controls the presumed optimization level of\n    the bytecode file. If 'optimization' is not None, the string representation\n    of the argument is taken and verified to be alphanumeric (else ValueError\n    is raised).\n\n    The debug_override parameter is deprecated. If debug_override is not None,\n    a True value is the same as setting 'optimization' to the empty string\n    while a False value is equivalent to setting 'optimization' to '1'.\n\n    If sys.implementation.cache_tag is None then NotImplementedError is raised.\n\n    "
	if debug_override is not _A:
		_warnings.warn("the debug_override parameter is deprecated; use 'optimization' instead",DeprecationWarning)
		if optimization is not _A:message='debug_override or optimization must be set to None';raise TypeError(message)
		optimization=''if debug_override else 1
	path=_os.fspath(path);head,tail=_path_split(path);base,sep,rest=tail.rpartition(_B);tag=sys.implementation.cache_tag
	if tag is _A:raise NotImplementedError(_I)
	almost_filename=''.join([base if base else rest,sep,tag])
	if optimization is _A:
		if sys.flags.optimize==0:optimization=''
		else:optimization=sys.flags.optimize
	optimization=str(optimization)
	if optimization!='':
		if not optimization.isalnum():raise ValueError('{!r} is not alphanumeric'.format(optimization))
		almost_filename='{}.{}{}'.format(almost_filename,_OPT,optimization)
	filename=almost_filename+BYTECODE_SUFFIXES[0]
	if sys.pycache_prefix is not _A:
		if not _path_isabs(head):head=_path_join(_os.getcwd(),head)
		if head[1]==':'and head[0]not in path_separators:head=head[2:]
		return _path_join(sys.pycache_prefix,head.lstrip(path_separators),filename)
	return _path_join(head,_PYCACHE,filename)
def source_from_cache(path):
	'Given the path to a .pyc. file, return the path to its .py file.\n\n    The .pyc file does not need to exist; this simply returns the path to\n    the .py file calculated to correspond to the .pyc file.  If path does\n    not conform to PEP 3147/488 format, ValueError will be raised. If\n    sys.implementation.cache_tag is None then NotImplementedError is raised.\n\n    '
	if sys.implementation.cache_tag is _A:raise NotImplementedError(_I)
	path=_os.fspath(path);head,pycache_filename=_path_split(path);found_in_pycache_prefix=_D
	if sys.pycache_prefix is not _A:
		stripped_path=sys.pycache_prefix.rstrip(path_separators)
		if head.startswith(stripped_path+path_sep):head=head[len(stripped_path):];found_in_pycache_prefix=_C
	if not found_in_pycache_prefix:
		head,pycache=_path_split(head)
		if pycache!=_PYCACHE:raise ValueError(f"{_PYCACHE} not bottom-level directory in {path!r}")
	dot_count=pycache_filename.count(_B)
	if dot_count not in{2,3}:raise ValueError(f"expected only 2 or 3 dots in {pycache_filename!r}")
	elif dot_count==3:
		optimization=pycache_filename.rsplit(_B,2)[-2]
		if not optimization.startswith(_OPT):raise ValueError(f"optimization portion of filename does not start with {_OPT!r}")
		opt_level=optimization[len(_OPT):]
		if not opt_level.isalnum():raise ValueError(f"optimization level {optimization!r} is not an alphanumeric value")
	base_filename=pycache_filename.partition(_B)[0];return _path_join(head,base_filename+SOURCE_SUFFIXES[0])
def _get_sourcefile(bytecode_path):
	'Convert a bytecode file path to a source path (if possible).\n\n    This function exists purely for backwards-compatibility for\n    PyImport_ExecCodeModuleWithFilenames() in the C API.\n\n    '
	if len(bytecode_path)==0:return
	rest,_,extension=bytecode_path.rpartition(_B)
	if not rest or extension.lower()[-3:-1]!='py':return bytecode_path
	try:source_path=source_from_cache(bytecode_path)
	except(NotImplementedError,ValueError):source_path=bytecode_path[:-1]
	return source_path if _path_isfile(source_path)else bytecode_path
def _get_cached(filename):
	if filename.endswith(tuple(SOURCE_SUFFIXES)):
		try:return cache_from_source(filename)
		except NotImplementedError:pass
	elif filename.endswith(tuple(BYTECODE_SUFFIXES)):return filename
	else:return
def _calc_mode(path):
	'Calculate the mode permissions for a bytecode file.'
	try:mode=_path_stat(path).st_mode
	except OSError:mode=438
	mode|=128;return mode
def _check_name(method):
	'Decorator to verify that the module being requested matches the one the\n    loader can handle.\n\n    The first argument (self) must define _name which the second argument is\n    compared against. If the comparison fails then ImportError is raised.\n\n    '
	def _check_name_wrapper(self,name=_A,*args,**kwargs):
		if name is _A:name=self.name
		elif self.name!=name:raise ImportError('loader for %s cannot handle %s'%(self.name,name),name=name)
		return method(self,name,*args,**kwargs)
	if _bootstrap is not _A:_wrap=_bootstrap._wrap
	else:
		def _wrap(new,old):
			for replace in['__module__','__name__','__qualname__','__doc__']:
				if hasattr(old,replace):setattr(new,replace,getattr(old,replace))
			new.__dict__.update(old.__dict__)
	_wrap(_check_name_wrapper,method);return _check_name_wrapper
def _find_module_shim(self,fullname):
	'Try to find a loader for the specified module by delegating to\n    self.find_loader().\n\n    This method is deprecated in favor of finder.find_spec().\n\n    ';_warnings.warn('find_module() is deprecated and slated for removal in Python 3.12; use find_spec() instead',DeprecationWarning);loader,portions=self.find_loader(fullname)
	if loader is _A and len(portions):msg='Not importing directory {}: missing __init__';_warnings.warn(msg.format(portions[0]),ImportWarning)
	return loader
def _classify_pyc(data,name,exc_details):
	'Perform basic validity checking of a pyc header and return the flags field,\n    which determines how the pyc should be further validated against the source.\n\n    *data* is the contents of the pyc file. (Only the first 16 bytes are\n    required, though.)\n\n    *name* is the name of the module being imported. It is used for logging.\n\n    *exc_details* is a dictionary passed to ImportError if it raised for\n    improved debugging.\n\n    ImportError is raised when the magic number is incorrect or when the flags\n    field is invalid. EOFError is raised when the data is found to be truncated.\n\n    ';magic=data[:4]
	if magic!=MAGIC_NUMBER:message=f"bad magic number in {name!r}: {magic!r}";_bootstrap._verbose_message('{}',message);raise ImportError(message,**exc_details)
	if len(data)<16:message=f"reached EOF while reading pyc header of {name!r}";_bootstrap._verbose_message('{}',message);raise EOFError(message)
	flags=_unpack_uint32(data[4:8])
	if flags&~3:message=f"invalid flags {flags!r} in {name!r}";raise ImportError(message,**exc_details)
	return flags
def _validate_timestamp_pyc(data,source_mtime,source_size,name,exc_details):
	'Validate a pyc against the source last-modified time.\n\n    *data* is the contents of the pyc file. (Only the first 16 bytes are\n    required.)\n\n    *source_mtime* is the last modified timestamp of the source file.\n\n    *source_size* is None or the size of the source file in bytes.\n\n    *name* is the name of the module being imported. It is used for logging.\n\n    *exc_details* is a dictionary passed to ImportError if it raised for\n    improved debugging.\n\n    An ImportError is raised if the bytecode is stale.\n\n    '
	if _unpack_uint32(data[8:12])!=source_mtime&4294967295:message=f"bytecode is stale for {name!r}";_bootstrap._verbose_message('{}',message);raise ImportError(message,**exc_details)
	if source_size is not _A and _unpack_uint32(data[12:16])!=source_size&4294967295:raise ImportError(f"bytecode is stale for {name!r}",**exc_details)
def _validate_hash_pyc(data,source_hash,name,exc_details):
	'Validate a hash-based pyc by checking the real source hash against the one in\n    the pyc header.\n\n    *data* is the contents of the pyc file. (Only the first 16 bytes are\n    required.)\n\n    *source_hash* is the importlib.util.source_hash() of the source file.\n\n    *name* is the name of the module being imported. It is used for logging.\n\n    *exc_details* is a dictionary passed to ImportError if it raised for\n    improved debugging.\n\n    An ImportError is raised if the bytecode is stale.\n\n    '
	if data[8:16]!=source_hash:raise ImportError(f"hash in bytecode doesn't match hash of source {name!r}",**exc_details)
def _compile_bytecode(data,name=_A,bytecode_path=_A,source_path=_A):
	'Compile bytecode as found in a pyc.';code=marshal.loads(data)
	if isinstance(code,_code_type):
		_bootstrap._verbose_message('code object from {!r}',bytecode_path)
		if source_path is not _A:_imp._fix_co_filename(code,source_path)
		return code
	else:raise ImportError('Non-code object in {!r}'.format(bytecode_path),name=name,path=bytecode_path)
def _code_to_timestamp_pyc(code,mtime=0,source_size=0):'Produce the data for a timestamp-based pyc.';data=bytearray(MAGIC_NUMBER);data.extend(_pack_uint32(0));data.extend(_pack_uint32(mtime));data.extend(_pack_uint32(source_size));data.extend(marshal.dumps(code));return data
def _code_to_hash_pyc(code,source_hash,checked=_C):'Produce the data for a hash-based pyc.';data=bytearray(MAGIC_NUMBER);flags=1|checked<<1;data.extend(_pack_uint32(flags));assert len(source_hash)==8;data.extend(source_hash);data.extend(marshal.dumps(code));return data
def decode_source(source_bytes):'Decode bytes representing source code and return the string.\n\n    Universal newline support is used in the decoding.\n    ';import tokenize;source_bytes_readline=_io.BytesIO(source_bytes).readline;encoding=tokenize.detect_encoding(source_bytes_readline);newline_decoder=_io.IncrementalNewlineDecoder(_A,_C);return newline_decoder.decode(source_bytes.decode(encoding[0]))
_POPULATE=object()
def spec_from_file_location(name,location=_A,*,loader=_A,submodule_search_locations=_POPULATE):
	'Return a module spec based on a file location.\n\n    To indicate that the module is a package, set\n    submodule_search_locations to a list of directory paths.  An\n    empty list is sufficient, though its not otherwise useful to the\n    import system.\n\n    The loader must take a spec as its only __init__() arg.\n\n    '
	if location is _A:
		location='<unknown>'
		if hasattr(loader,'get_filename'):
			try:location=loader.get_filename(name)
			except ImportError:pass
	else:
		location=_os.fspath(location)
		if not _path_isabs(location):
			try:location=_path_join(_os.getcwd(),location)
			except OSError:pass
	spec=_bootstrap.ModuleSpec(name,loader,origin=location);spec._set_fileattr=_C
	if loader is _A:
		for(loader_class,suffixes)in _get_supported_file_loaders():
			if location.endswith(tuple(suffixes)):loader=loader_class(name,location);spec.loader=loader;break
		else:return
	if submodule_search_locations is _POPULATE:
		if hasattr(loader,'is_package'):
			try:is_package=loader.is_package(name)
			except ImportError:pass
			else:
				if is_package:spec.submodule_search_locations=[]
	else:spec.submodule_search_locations=submodule_search_locations
	if spec.submodule_search_locations==[]:
		if location:dirname=_path_split(location)[0];spec.submodule_search_locations.append(dirname)
	return spec
class WindowsRegistryFinder:
	'Meta path finder for modules declared in the Windows registry.';REGISTRY_KEY='Software\\Python\\PythonCore\\{sys_version}\\Modules\\{fullname}';REGISTRY_KEY_DEBUG='Software\\Python\\PythonCore\\{sys_version}\\Modules\\{fullname}\\Debug';DEBUG_BUILD=_MS_WINDOWS and'_d.pyd'in EXTENSION_SUFFIXES
	@staticmethod
	def _open_registry(key):
		try:return winreg.OpenKey(winreg.HKEY_CURRENT_USER,key)
		except OSError:return winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,key)
	@classmethod
	def _search_registry(cls,fullname):
		if cls.DEBUG_BUILD:registry_key=cls.REGISTRY_KEY_DEBUG
		else:registry_key=cls.REGISTRY_KEY
		key=registry_key.format(fullname=fullname,sys_version='%d.%d'%sys.version_info[:2])
		try:
			with cls._open_registry(key)as hkey:filepath=winreg.QueryValue(hkey,'')
		except OSError:return
		return filepath
	@classmethod
	def find_spec(cls,fullname,path=_A,target=_A):
		filepath=cls._search_registry(fullname)
		if filepath is _A:return
		try:_path_stat(filepath)
		except OSError:return
		for(loader,suffixes)in _get_supported_file_loaders():
			if filepath.endswith(tuple(suffixes)):spec=_bootstrap.spec_from_loader(fullname,loader(fullname,filepath),origin=filepath);return spec
	@classmethod
	def find_module(cls,fullname,path=_A):
		'Find module named in the registry.\n\n        This method is deprecated.  Use find_spec() instead.\n\n        ';_warnings.warn('WindowsRegistryFinder.find_module() is deprecated and slated for removal in Python 3.12; use find_spec() instead',DeprecationWarning);spec=cls.find_spec(fullname,path)
		if spec is not _A:return spec.loader
		else:return
class _LoaderBasics:
	'Base class of common code needed by both SourceLoader and\n    SourcelessFileLoader.'
	def is_package(self,fullname):"Concrete implementation of InspectLoader.is_package by checking if\n        the path returned by get_filename has a filename of '__init__.py'.";filename=_path_split(self.get_filename(fullname))[1];filename_base=filename.rsplit(_B,1)[0];tail_name=fullname.rpartition(_B)[2];return filename_base==_F and tail_name!=_F
	def create_module(self,spec):'Use default semantics for module creation.'
	def exec_module(self,module):
		'Execute the module.';code=self.get_code(module.__name__)
		if code is _A:raise ImportError('cannot load module {!r} when get_code() returns None'.format(module.__name__))
		_bootstrap._call_with_frames_removed(exec,code,module.__dict__)
	def load_module(self,fullname):'This method is deprecated.';return _bootstrap._load_module_shim(self,fullname)
class SourceLoader(_LoaderBasics):
	def path_mtime(self,path):'Optional method that returns the modification time (an int) for the\n        specified path (a str).\n\n        Raises OSError when the path cannot be handled.\n        ';raise OSError
	def path_stats(self,path):"Optional method returning a metadata dict for the specified\n        path (a str).\n\n        Possible keys:\n        - 'mtime' (mandatory) is the numeric timestamp of last source\n          code modification;\n        - 'size' (optional) is the size in bytes of the source code.\n\n        Implementing this method allows the loader to read bytecode files.\n        Raises OSError when the path cannot be handled.\n        ";return{_G:self.path_mtime(path)}
	def _cache_bytecode(self,source_path,cache_path,data):'Optional method which writes data (bytes) to a file path (a str).\n\n        Implementing this method allows for the writing of bytecode files.\n\n        The source path is needed in order to correctly transfer permissions\n        ';return self.set_data(cache_path,data)
	def set_data(self,path,data):'Optional method which writes data (bytes) to a file path (a str).\n\n        Implementing this method allows for the writing of bytecode files.\n        '
	def get_source(self,fullname):
		'Concrete implementation of InspectLoader.get_source.';path=self.get_filename(fullname)
		try:source_bytes=self.get_data(path)
		except OSError as exc:raise ImportError('source not available through get_data()',name=fullname)from exc
		return decode_source(source_bytes)
	def source_to_code(self,data,path,*,_optimize=-1):"Return the code object compiled from source.\n\n        The 'data' argument can be any object type that compile() supports.\n        ";return _bootstrap._call_with_frames_removed(compile,data,path,'exec',dont_inherit=_C,optimize=_optimize)
	def get_code(self,fullname):
		'Concrete implementation of InspectLoader.get_code.\n\n        Reading of bytecode requires path_stats to be implemented. To write\n        bytecode, set_data must also be implemented.\n\n        ';source_path=self.get_filename(fullname);source_mtime=_A;source_bytes=_A;source_hash=_A;hash_based=_D;check_source=_C
		try:bytecode_path=cache_from_source(source_path)
		except NotImplementedError:bytecode_path=_A
		else:
			try:st=self.path_stats(source_path)
			except OSError:pass
			else:
				source_mtime=int(st[_G])
				try:data=self.get_data(bytecode_path)
				except OSError:pass
				else:
					exc_details={'name':fullname,_H:bytecode_path}
					try:
						flags=_classify_pyc(data,fullname,exc_details);bytes_data=memoryview(data)[16:];hash_based=flags&1!=0
						if hash_based:
							check_source=flags&2!=0
							if _imp.check_hash_based_pycs!='never'and(check_source or _imp.check_hash_based_pycs=='always'):source_bytes=self.get_data(source_path);source_hash=_imp.source_hash(_RAW_MAGIC_NUMBER,source_bytes);_validate_hash_pyc(data,source_hash,fullname,exc_details)
						else:_validate_timestamp_pyc(data,source_mtime,st['size'],fullname,exc_details)
					except(ImportError,EOFError):pass
					else:_bootstrap._verbose_message('{} matches {}',bytecode_path,source_path);return _compile_bytecode(bytes_data,name=fullname,bytecode_path=bytecode_path,source_path=source_path)
		if source_bytes is _A:source_bytes=self.get_data(source_path)
		code_object=self.source_to_code(source_bytes,source_path);_bootstrap._verbose_message('code object from {}',source_path)
		if not sys.dont_write_bytecode and bytecode_path is not _A and source_mtime is not _A:
			if hash_based:
				if source_hash is _A:source_hash=_imp.source_hash(source_bytes)
				data=_code_to_hash_pyc(code_object,source_hash,check_source)
			else:data=_code_to_timestamp_pyc(code_object,source_mtime,len(source_bytes))
			try:self._cache_bytecode(source_path,bytecode_path,data)
			except NotImplementedError:pass
		return code_object
class FileLoader:
	'Base file loader class which implements the loader protocol methods that\n    require file system usage.'
	def __init__(self,fullname,path):'Cache the module name and the path to the file found by the\n        finder.';self.name=fullname;self.path=path
	def __eq__(self,other):return self.__class__==other.__class__ and self.__dict__==other.__dict__
	def __hash__(self):return hash(self.name)^hash(self.path)
	@_check_name
	def load_module(self,fullname):'Load a module from a file.\n\n        This method is deprecated.  Use exec_module() instead.\n\n        ';return super(FileLoader,self).load_module(fullname)
	@_check_name
	def get_filename(self,fullname):'Return the path to the source file as found by the finder.';return self.path
	def get_data(self,path):
		'Return the data from path as raw bytes.'
		if isinstance(self,(SourceLoader,ExtensionFileLoader)):
			with _io.open_code(str(path))as file:return file.read()
		else:
			with _io.FileIO(path,'r')as file:return file.read()
	@_check_name
	def get_resource_reader(self,module):from importlib.readers import FileReader;return FileReader(self)
class SourceFileLoader(FileLoader,SourceLoader):
	'Concrete implementation of SourceLoader using the file system.'
	def path_stats(self,path):'Return the metadata for the path.';st=_path_stat(path);return{_G:st.st_mtime,'size':st.st_size}
	def _cache_bytecode(self,source_path,bytecode_path,data):mode=_calc_mode(source_path);return self.set_data(bytecode_path,data,_mode=mode)
	def set_data(self,path,data,*,_mode=438):
		'Write bytes data to a file.';A='could not create {!r}: {!r}';parent,filename=_path_split(path);path_parts=[]
		while parent and not _path_isdir(parent):parent,part=_path_split(parent);path_parts.append(part)
		for part in reversed(path_parts):
			parent=_path_join(parent,part)
			try:_os.mkdir(parent)
			except FileExistsError:continue
			except OSError as exc:_bootstrap._verbose_message(A,parent,exc);return
		try:_write_atomic(path,data,_mode);_bootstrap._verbose_message('created {!r}',path)
		except OSError as exc:_bootstrap._verbose_message(A,path,exc)
class SourcelessFileLoader(FileLoader,_LoaderBasics):
	'Loader which handles sourceless file imports.'
	def get_code(self,fullname):path=self.get_filename(fullname);data=self.get_data(path);exc_details={'name':fullname,_H:path};_classify_pyc(data,fullname,exc_details);return _compile_bytecode(memoryview(data)[16:],name=fullname,bytecode_path=path)
	def get_source(self,fullname):'Return None as there is no source code.'
class ExtensionFileLoader(FileLoader,_LoaderBasics):
	'Loader for extension modules.\n\n    The constructor is designed to work with FileFinder.\n\n    '
	def __init__(self,name,path):self.name=name;self.path=path
	def __eq__(self,other):return self.__class__==other.__class__ and self.__dict__==other.__dict__
	def __hash__(self):return hash(self.name)^hash(self.path)
	def create_module(self,spec):'Create an uninitialized extension module';module=_bootstrap._call_with_frames_removed(_imp.create_dynamic,spec);_bootstrap._verbose_message('extension module {!r} loaded from {!r}',spec.name,self.path);return module
	def exec_module(self,module):'Initialize an extension module';_bootstrap._call_with_frames_removed(_imp.exec_dynamic,module);_bootstrap._verbose_message('extension module {!r} executed from {!r}',self.name,self.path)
	def is_package(self,fullname):'Return True if the extension module is a package.';file_name=_path_split(self.path)[1];return any(file_name==_F+suffix for suffix in EXTENSION_SUFFIXES)
	def get_code(self,fullname):'Return None as an extension module cannot create a code object.'
	def get_source(self,fullname):'Return None as extension modules have no source code.'
	@_check_name
	def get_filename(self,fullname):'Return the path to the source file as found by the finder.';return self.path
class _NamespacePath:
	"Represents a namespace package's path.  It uses the module name\n    to find its parent module, and from there it looks up the parent's\n    __path__.  When this changes, the module's own path is recomputed,\n    using path_finder.  For top-level modules, the parent module's path\n    is sys.path.";_epoch=0
	def __init__(self,name,path,path_finder):self._name=name;self._path=path;self._last_parent_path=tuple(self._get_parent_path());self._last_epoch=self._epoch;self._path_finder=path_finder
	def _find_parent_path_names(self):
		'Returns a tuple of (parent-module-name, parent-path-attr-name)';parent,dot,me=self._name.rpartition(_B)
		if dot=='':return'sys',_H
		return parent,'__path__'
	def _get_parent_path(self):parent_module_name,path_attr_name=self._find_parent_path_names();return getattr(sys.modules[parent_module_name],path_attr_name)
	def _recalculate(self):
		parent_path=tuple(self._get_parent_path())
		if parent_path!=self._last_parent_path or self._epoch!=self._last_epoch:
			spec=self._path_finder(self._name,parent_path)
			if spec is not _A and spec.loader is _A:
				if spec.submodule_search_locations:self._path=spec.submodule_search_locations
			self._last_parent_path=parent_path;self._last_epoch=self._epoch
		return self._path
	def __iter__(self):return iter(self._recalculate())
	def __getitem__(self,index):return self._recalculate()[index]
	def __setitem__(self,index,path):self._path[index]=path
	def __len__(self):return len(self._recalculate())
	def __repr__(self):return'_NamespacePath({!r})'.format(self._path)
	def __contains__(self,item):return item in self._recalculate()
	def append(self,item):self._path.append(item)
class NamespaceLoader:
	def __init__(self,name,path,path_finder):self._path=_NamespacePath(name,path,path_finder)
	@staticmethod
	def module_repr(module):'Return repr for the module.\n\n        The method is deprecated.  The import machinery does the job itself.\n\n        ';_warnings.warn('NamespaceLoader.module_repr() is deprecated and slated for removal in Python 3.12',DeprecationWarning);return'<module {!r} (namespace)>'.format(module.__name__)
	def is_package(self,fullname):return _C
	def get_source(self,fullname):return''
	def get_code(self,fullname):return compile('','<string>','exec',dont_inherit=_C)
	def create_module(self,spec):'Use default semantics for module creation.'
	def exec_module(self,module):0
	def load_module(self,fullname):'Load a namespace module.\n\n        This method is deprecated.  Use exec_module() instead.\n\n        ';_bootstrap._verbose_message('namespace module loaded with path {!r}',self._path);return _bootstrap._load_module_shim(self,fullname)
	def get_resource_reader(self,module):from importlib.readers import NamespaceReader;return NamespaceReader(self._path)
_NamespaceLoader=NamespaceLoader
class PathFinder:
	'Meta path finder for sys.path and package __path__ attributes.'
	@staticmethod
	def invalidate_caches():
		'Call the invalidate_caches() method on all path entry finders\n        stored in sys.path_importer_caches (where implemented).'
		for(name,finder)in list(sys.path_importer_cache.items()):
			if finder is _A or not _path_isabs(name):del sys.path_importer_cache[name]
			elif hasattr(finder,'invalidate_caches'):finder.invalidate_caches()
		_NamespacePath._epoch+=1
	@staticmethod
	def _path_hooks(path):
		"Search sys.path_hooks for a finder for 'path'."
		if sys.path_hooks is not _A and not sys.path_hooks:_warnings.warn('sys.path_hooks is empty',ImportWarning)
		for hook in sys.path_hooks:
			try:return hook(path)
			except ImportError:continue
		else:return
	@classmethod
	def _path_importer_cache(cls,path):
		'Get the finder for the path entry from sys.path_importer_cache.\n\n        If the path entry is not in the cache, find the appropriate finder\n        and cache it. If no finder is available, store None.\n\n        '
		if path=='':
			try:path=_os.getcwd()
			except FileNotFoundError:return
		try:finder=sys.path_importer_cache[path]
		except KeyError:finder=cls._path_hooks(path);sys.path_importer_cache[path]=finder
		return finder
	@classmethod
	def _legacy_get_spec(cls,fullname,finder):
		if hasattr(finder,'find_loader'):msg=f"{_bootstrap._object_name(finder)}.find_spec() not found; falling back to find_loader()";_warnings.warn(msg,ImportWarning);loader,portions=finder.find_loader(fullname)
		else:msg=f"{_bootstrap._object_name(finder)}.find_spec() not found; falling back to find_module()";_warnings.warn(msg,ImportWarning);loader=finder.find_module(fullname);portions=[]
		if loader is not _A:return _bootstrap.spec_from_loader(fullname,loader)
		spec=_bootstrap.ModuleSpec(fullname,_A);spec.submodule_search_locations=portions;return spec
	@classmethod
	def _get_spec(cls,fullname,path,target=_A):
		'Find the loader or namespace_path for this module/package name.';namespace_path=[]
		for entry in path:
			if not isinstance(entry,str):continue
			finder=cls._path_importer_cache(entry)
			if finder is not _A:
				if hasattr(finder,'find_spec'):spec=finder.find_spec(fullname,target)
				else:spec=cls._legacy_get_spec(fullname,finder)
				if spec is _A:continue
				if spec.loader is not _A:return spec
				portions=spec.submodule_search_locations
				if portions is _A:raise ImportError('spec missing loader')
				namespace_path.extend(portions)
		else:spec=_bootstrap.ModuleSpec(fullname,_A);spec.submodule_search_locations=namespace_path;return spec
	@classmethod
	def find_spec(cls,fullname,path=_A,target=_A):
		"Try to find a spec for 'fullname' on sys.path or 'path'.\n\n        The search is based on sys.path_hooks and sys.path_importer_cache.\n        "
		if path is _A:path=sys.path
		spec=cls._get_spec(fullname,path,target)
		if spec is _A:return
		elif spec.loader is _A:
			namespace_path=spec.submodule_search_locations
			if namespace_path:spec.origin=_A;spec.submodule_search_locations=_NamespacePath(fullname,namespace_path,cls._get_spec);return spec
			else:return
		else:return spec
	@classmethod
	def find_module(cls,fullname,path=_A):
		"find the module on sys.path or 'path' based on sys.path_hooks and\n        sys.path_importer_cache.\n\n        This method is deprecated.  Use find_spec() instead.\n\n        ";_warnings.warn('PathFinder.find_module() is deprecated and slated for removal in Python 3.12; use find_spec() instead',DeprecationWarning);spec=cls.find_spec(fullname,path)
		if spec is _A:return
		return spec.loader
	@staticmethod
	def find_distributions(*args,**kwargs):'\n        Find distributions.\n\n        Return an iterable of all Distribution instances capable of\n        loading the metadata for packages matching ``context.name``\n        (or all names if ``None`` indicated) along the paths in the list\n        of directories ``context.path``.\n        ';from importlib.metadata import MetadataPathFinder;return MetadataPathFinder.find_distributions(*args,**kwargs)
class FileFinder:
	'File-based finder.\n\n    Interactions with the file system are cached for performance, being\n    refreshed when the directory the finder is handling has been modified.\n\n    '
	def __init__(self,path,*loader_details):
		'Initialize with the path to search on and a variable number of\n        2-tuples containing the loader and the file suffixes the loader\n        recognizes.';loaders=[]
		for(loader,suffixes)in loader_details:loaders.extend((suffix,loader)for suffix in suffixes)
		self._loaders=loaders
		if not path or path==_B:self.path=_os.getcwd()
		elif not _path_isabs(path):self.path=_path_join(_os.getcwd(),path)
		else:self.path=path
		self._path_mtime=-1;self._path_cache=set();self._relaxed_path_cache=set()
	def invalidate_caches(self):'Invalidate the directory mtime.';self._path_mtime=-1
	find_module=_find_module_shim
	def find_loader(self,fullname):
		'Try to find a loader for the specified module, or the namespace\n        package portions. Returns (loader, list-of-portions).\n\n        This method is deprecated.  Use find_spec() instead.\n\n        ';_warnings.warn('FileFinder.find_loader() is deprecated and slated for removal in Python 3.12; use find_spec() instead',DeprecationWarning);spec=self.find_spec(fullname)
		if spec is _A:return _A,[]
		return spec.loader,spec.submodule_search_locations or[]
	def _get_spec(self,loader_class,fullname,path,smsl,target):loader=loader_class(fullname,path);return spec_from_file_location(fullname,path,loader=loader,submodule_search_locations=smsl)
	def find_spec(self,fullname,target=_A):
		'Try to find a spec for the specified module.\n\n        Returns the matching spec, or None if not found.\n        ';is_namespace=_D;tail_module=fullname.rpartition(_B)[2]
		try:mtime=_path_stat(self.path or _os.getcwd()).st_mtime
		except OSError:mtime=-1
		if mtime!=self._path_mtime:self._fill_cache();self._path_mtime=mtime
		if _relax_case():cache=self._relaxed_path_cache;cache_module=tail_module.lower()
		else:cache=self._path_cache;cache_module=tail_module
		if cache_module in cache:
			base_path=_path_join(self.path,tail_module)
			for(suffix,loader_class)in self._loaders:
				init_filename=_F+suffix;full_path=_path_join(base_path,init_filename)
				if _path_isfile(full_path):return self._get_spec(loader_class,fullname,full_path,[base_path],target)
			else:is_namespace=_path_isdir(base_path)
		for(suffix,loader_class)in self._loaders:
			try:full_path=_path_join(self.path,tail_module+suffix)
			except ValueError:return
			_bootstrap._verbose_message('trying {}',full_path,verbosity=2)
			if cache_module+suffix in cache:
				if _path_isfile(full_path):return self._get_spec(loader_class,fullname,full_path,_A,target)
		if is_namespace:_bootstrap._verbose_message('possible namespace for {}',base_path);spec=_bootstrap.ModuleSpec(fullname,_A);spec.submodule_search_locations=[base_path];return spec
	def _fill_cache(self):
		'Fill the cache of potential modules and packages for this directory.';path=self.path
		try:contents=_os.listdir(path or _os.getcwd())
		except(FileNotFoundError,PermissionError,NotADirectoryError):contents=[]
		if not sys.platform.startswith('win'):self._path_cache=set(contents)
		else:
			lower_suffix_contents=set()
			for item in contents:
				name,dot,suffix=item.partition(_B)
				if dot:new_name='{}.{}'.format(name,suffix.lower())
				else:new_name=name
				lower_suffix_contents.add(new_name)
			self._path_cache=lower_suffix_contents
		if sys.platform.startswith(_CASE_INSENSITIVE_PLATFORMS):self._relaxed_path_cache={fn.lower()for fn in contents}
	@classmethod
	def path_hook(cls,*loader_details):
		'A class method which returns a closure to use on sys.path_hook\n        which will return an instance using the specified loaders and the path\n        called on the closure.\n\n        If the path called on the closure is not a directory, ImportError is\n        raised.\n\n        '
		def path_hook_for_FileFinder(path):
			'Path hook for importlib.machinery.FileFinder.'
			if not _path_isdir(path):raise ImportError('only directories are supported',path=path)
			return cls(path,*loader_details)
		return path_hook_for_FileFinder
	def __repr__(self):return'FileFinder({!r})'.format(self.path)
def _fix_up_module(ns,name,pathname,cpathname=_A):
	B='__spec__';A='__loader__';loader=ns.get(A);spec=ns.get(B)
	if not loader:
		if spec:loader=spec.loader
		elif pathname==cpathname:loader=SourcelessFileLoader(name,pathname)
		else:loader=SourceFileLoader(name,pathname)
	if not spec:spec=spec_from_file_location(name,pathname,loader=loader)
	try:ns[B]=spec;ns[A]=loader;ns['__file__']=pathname;ns['__cached__']=cpathname
	except Exception:pass
def _get_supported_file_loaders():'Returns a list of file-based module loaders.\n\n    Each item is a tuple (loader, suffixes).\n    ';extensions=ExtensionFileLoader,_imp.extension_suffixes();source=SourceFileLoader,SOURCE_SUFFIXES;bytecode=SourcelessFileLoader,BYTECODE_SUFFIXES;return[extensions,source,bytecode]
def _set_bootstrap_module(_bootstrap_module):global _bootstrap;_bootstrap=_bootstrap_module
def _install(_bootstrap_module):'Install the path-based import components.';_set_bootstrap_module(_bootstrap_module);supported_loaders=_get_supported_file_loaders();sys.path_hooks.extend([FileFinder.path_hook(*supported_loaders)]);sys.meta_path.append(PathFinder)