'Append module search paths for third-party packages to sys.path.\n\n****************************************************************\n* This module is automatically imported during initialization. *\n****************************************************************\n\nThis will append site-specific paths to the module search path.  On\nUnix (including Mac OSX), it starts with sys.prefix and\nsys.exec_prefix (if different) and appends\nlib/python<version>/site-packages.\nOn other platforms (such as Windows), it tries each of the\nprefixes directly, as well as with lib/site-packages appended.  The\nresulting directories, if they exist, are appended to sys.path, and\nalso inspected for path configuration files.\n\nIf a file named "pyvenv.cfg" exists one directory above sys.executable,\nsys.prefix and sys.exec_prefix are set to that directory and\nit is also checked for site-packages (sys.base_prefix and\nsys.base_exec_prefix will always be the "real" prefixes of the Python\ninstallation). If "pyvenv.cfg" (a bootstrap configuration file) contains\nthe key "include-system-site-packages" set to anything other than "false"\n(case-insensitive), the system-level prefixes will still also be\nsearched for site-packages; otherwise they won\'t.\n\nAll of the resulting site-specific directories, if they exist, are\nappended to sys.path, and also inspected for path configuration\nfiles.\n\nA path configuration file is a file whose name has the form\n<package>.pth; its contents are additional directories (one per line)\nto be added to sys.path.  Non-existing directories (or\nnon-directories) are never added to sys.path; no directory is added to\nsys.path more than once.  Blank lines and lines beginning with\n\'#\' are skipped. Lines starting with \'import\' are executed.\n\nFor example, suppose sys.prefix and sys.exec_prefix are set to\n/usr/local and there is a directory /usr/local/lib/python2.5/site-packages\nwith three subdirectories, foo, bar and spam, and two path\nconfiguration files, foo.pth and bar.pth.  Assume foo.pth contains the\nfollowing:\n\n  # foo package configuration\n  foo\n  bar\n  bletch\n\nand bar.pth contains:\n\n  # bar package configuration\n  bar\n\nThen the following directories are added to sys.path, in this order:\n\n  /usr/local/lib/python2.5/site-packages/bar\n  /usr/local/lib/python2.5/site-packages/foo\n\nNote that bletch is omitted because it doesn\'t exist; bar precedes foo\nbecause bar.pth comes alphabetically before foo.pth; and spam is\nomitted because it is not mentioned in either path configuration file.\n\nThe readline module is also automatically configured to enable\ncompletion for systems that support it.  This can be overridden in\nsitecustomize, usercustomize or PYTHONSTARTUP.  Starting Python in\nisolated mode (-I) disables automatic readline configuration.\n\nAfter these operations, an attempt is made to import a module\nnamed sitecustomize, which can perform arbitrary additional\nsite-specific customizations.  If this import fails with an\nImportError exception, it is silently ignored.\n'
_C='darwin'
_B=False
_A=None
import sys,os,builtins,_sitebuiltins,io
PREFIXES=[sys.prefix,sys.exec_prefix]
ENABLE_USER_SITE=_A
USER_SITE=_A
USER_BASE=_A
def _trace(message):
	if sys.flags.verbose:print(message,file=sys.stderr)
def makepath(*paths):
	dir=os.path.join(*paths)
	try:dir=os.path.abspath(dir)
	except OSError:pass
	return dir,os.path.normcase(dir)
def abs_paths():
	'Set all module __file__ and __cached__ attributes to an absolute path'
	for m in set(sys.modules.values()):
		loader_module=_A
		try:loader_module=m.__loader__.__module__
		except AttributeError:
			try:loader_module=m.__spec__.loader.__module__
			except AttributeError:pass
		if loader_module not in{'_frozen_importlib','_frozen_importlib_external'}:continue
		try:m.__file__=os.path.abspath(m.__file__)
		except(AttributeError,OSError,TypeError):pass
		try:m.__cached__=os.path.abspath(m.__cached__)
		except(AttributeError,OSError,TypeError):pass
def removeduppaths():
	' Remove duplicate entries from sys.path along with making them\n    absolute';L=[];known_paths=set()
	for dir in sys.path:
		dir,dircase=makepath(dir)
		if dircase not in known_paths:L.append(dir);known_paths.add(dircase)
	sys.path[:]=L;return known_paths
def _init_pathinfo():
	'Return a set containing all existing file system items from sys.path.';d=set()
	for item in sys.path:
		try:
			if os.path.exists(item):_,itemcase=makepath(item);d.add(itemcase)
		except TypeError:continue
	return d
def addpackage(sitedir,name,known_paths):
	"Process a .pth file within the site-packages directory:\n       For each line in the file, either combine it with sitedir to a path\n       and add that to known_paths, or execute it if it starts with 'import '.\n    "
	if known_paths is _A:known_paths=_init_pathinfo();reset=True
	else:reset=_B
	fullname=os.path.join(sitedir,name);_trace(f"Processing .pth file: {fullname!r}")
	try:f=io.TextIOWrapper(io.open_code(fullname),encoding='locale')
	except OSError:return
	with f:
		for(n,line)in enumerate(f):
			if line.startswith('#'):continue
			if line.strip()=='':continue
			try:
				if line.startswith(('import ','import\t')):exec(line);continue
				line=line.rstrip();dir,dircase=makepath(sitedir,line)
				if not dircase in known_paths and os.path.exists(dir):sys.path.append(dir);known_paths.add(dircase)
			except Exception:
				print('Error processing line {:d} of {}:\n'.format(n+1,fullname),file=sys.stderr);import traceback
				for record in traceback.format_exception(*sys.exc_info()):
					for line in record.splitlines():print('  '+line,file=sys.stderr)
				print('\nRemainder of file ignored',file=sys.stderr);break
	if reset:known_paths=_A
	return known_paths
def addsitedir(sitedir,known_paths=_A):
	"Add 'sitedir' argument to sys.path if missing and handle .pth files in\n    'sitedir'";_trace(f"Adding directory: {sitedir!r}")
	if known_paths is _A:known_paths=_init_pathinfo();reset=True
	else:reset=_B
	sitedir,sitedircase=makepath(sitedir)
	if not sitedircase in known_paths:sys.path.append(sitedir);known_paths.add(sitedircase)
	try:names=os.listdir(sitedir)
	except OSError:return
	names=[name for name in names if name.endswith('.pth')]
	for name in sorted(names):addpackage(sitedir,name,known_paths)
	if reset:known_paths=_A
	return known_paths
def check_enableusersite():
	'Check if user site directory is safe for inclusion\n\n    The function tests for the command line flag (including environment var),\n    process uid/gid equal to effective uid/gid.\n\n    None: Disabled for security reasons\n    False: Disabled by user (command line option)\n    True: Safe and enabled\n    '
	if sys.flags.no_user_site:return _B
	if hasattr(os,'getuid')and hasattr(os,'geteuid'):
		if os.geteuid()!=os.getuid():return
	if hasattr(os,'getgid')and hasattr(os,'getegid'):
		if os.getegid()!=os.getgid():return
	return True
def _getuserbase():
	env_base=os.environ.get('PYTHONUSERBASE',_A)
	if env_base:return env_base
	if sys.platform in{'emscripten','vxworks','wasi'}:return
	def joinuser(*args):return os.path.expanduser(os.path.join(*args))
	if os.name=='nt':base=os.environ.get('APPDATA')or'~';return joinuser(base,'RustPython')
	if sys.platform==_C and sys._framework:return joinuser('~','Library',sys._framework,'%d.%d'%sys.version_info[:2])
	return joinuser('~','.local')
def _get_path(userbase):
	version=sys.version_info
	if os.name=='nt':ver_nodot=sys.winver.replace('.','');return f"{userbase}\\RustPython{ver_nodot}\\site-packages"
	if sys.platform==_C and sys._framework:return f"{userbase}/lib/rustpython/site-packages"
	return f"{userbase}/lib/rustpython{version[0]}.{version[1]}/site-packages"
def getuserbase():
	'Returns the `user base` directory path.\n\n    The `user base` directory can be used to store data. If the global\n    variable ``USER_BASE`` is not initialized yet, this function will also set\n    it.\n    ';global USER_BASE
	if USER_BASE is _A:USER_BASE=_getuserbase()
	return USER_BASE
def getusersitepackages():
	'Returns the user-specific site-packages directory path.\n\n    If the global variable ``USER_SITE`` is not initialized yet, this\n    function will also set it.\n    ';global USER_SITE,ENABLE_USER_SITE;userbase=getuserbase()
	if USER_SITE is _A:
		if userbase is _A:ENABLE_USER_SITE=_B
		else:USER_SITE=_get_path(userbase)
	return USER_SITE
def addusersitepackages(known_paths):
	'Add a per user site-package to sys.path\n\n    Each user has its own python directory with site-packages in the\n    home directory.\n    ';_trace('Processing user site-packages');user_site=getusersitepackages()
	if ENABLE_USER_SITE and os.path.isdir(user_site):addsitedir(user_site,known_paths)
	return known_paths
def getsitepackages(prefixes=_A):
	'Returns a list containing all global site-packages directories.\n\n    For each directory present in ``prefixes`` (or the global ``PREFIXES``),\n    this function will find its `site-packages` subdirectory depending on the\n    system environment, and will return a list of full paths.\n    ';B='site-packages';A='lib';sitepackages=[];seen=set()
	if prefixes is _A:prefixes=PREFIXES
	for prefix in prefixes:
		if not prefix or prefix in seen:continue
		seen.add(prefix)
		if os.sep=='/':
			libdirs=[sys.platlibdir]
			if sys.platlibdir!=A:libdirs.append(A)
			for libdir in libdirs:path=os.path.join(prefix,libdir,'rustpython%d.%d'%sys.version_info[:2],B);sitepackages.append(path)
		else:sitepackages.append(prefix);sitepackages.append(os.path.join(prefix,'Lib',B))
	return sitepackages
def addsitepackages(known_paths,prefixes=_A):
	'Add site-packages to sys.path';_trace('Processing global site-packages')
	for sitedir in getsitepackages(prefixes):
		if os.path.isdir(sitedir):addsitedir(sitedir,known_paths)
	return known_paths
def setquit():
	"Define new builtins 'quit' and 'exit'.\n\n    These are objects which make the interpreter exit when called.\n    The repr of each object contains a hint at how it works.\n\n    "
	if os.sep=='\\':eof='Ctrl-Z plus Return'
	else:eof='Ctrl-D (i.e. EOF)'
	builtins.quit=_sitebuiltins.Quitter('quit',eof);builtins.exit=_sitebuiltins.Quitter('exit',eof)
def setcopyright():
	"Set 'copyright' and 'credits' in builtins";A='credits';builtins.copyright=_sitebuiltins._Printer('copyright',sys.copyright)
	if sys.platform[:4]=='java':builtins.credits=_sitebuiltins._Printer(A,'Jython is maintained by the Jython developers (www.jython.org).')
	else:builtins.credits=_sitebuiltins._Printer(A,'    Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands\n    for supporting Python development.  See www.python.org for more information.')
	files,dirs=[],[];here=getattr(sys,'_stdlib_dir',_A)
	if not here and hasattr(os,'__file__'):here=os.path.dirname(os.__file__)
	if here:files.extend(['LICENSE.txt','LICENSE']);dirs.extend([os.path.join(here,os.pardir),here,os.curdir])
	builtins.license=_sitebuiltins._Printer('license','See https://www.python.org/psf/license/',files,dirs)
def sethelper():builtins.help=_sitebuiltins._Helper()
def enablerlcompleter():
	'Enable default readline configuration on interactive prompts, by\n    registering a sys.__interactivehook__.\n\n    If the readline module can be imported, the hook will set the Tab key\n    as completion key and register ~/.python_history as history file.\n    This can be overridden in the sitecustomize or usercustomize module,\n    or in a PYTHONSTARTUP file.\n    '
	def register_readline():
		import atexit
		try:import readline,rlcompleter
		except ImportError:return
		readline_doc=getattr(readline,'__doc__','')
		if readline_doc is not _A and'libedit'in readline_doc:readline.parse_and_bind('bind ^I rl_complete')
		else:readline.parse_and_bind('tab: complete')
		try:readline.read_init_file()
		except OSError:pass
		if readline.get_current_history_length()==0:
			history=os.path.join(os.path.expanduser('~'),'.python_history')
			try:readline.read_history_file(history)
			except OSError:pass
			def write_history():
				try:readline.write_history_file(history)
				except OSError:pass
			atexit.register(write_history)
	sys.__interactivehook__=register_readline
def venv(known_paths):
	B='true';A='__PYVENV_LAUNCHER__';global PREFIXES,ENABLE_USER_SITE;env=os.environ
	if sys.platform==_C and A in env:executable=sys._base_executable=os.environ[A]
	else:executable=sys.executable
	exe_dir,_=os.path.split(os.path.abspath(executable));site_prefix=os.path.dirname(exe_dir);sys._home=_A;conf_basename='pyvenv.cfg';candidate_confs=[conffile for conffile in(os.path.join(exe_dir,conf_basename),os.path.join(site_prefix,conf_basename))if os.path.isfile(conffile)]
	if candidate_confs:
		virtual_conf=candidate_confs[0];system_site=B
		with open(virtual_conf,encoding='utf-8')as f:
			for line in f:
				if'='in line:
					key,_,value=line.partition('=');key=key.strip().lower();value=value.strip()
					if key=='include-system-site-packages':system_site=value.lower()
					elif key=='home':sys._home=value
		sys.prefix=sys.exec_prefix=site_prefix;addsitepackages(known_paths,[sys.prefix])
		if system_site==B:PREFIXES.insert(0,sys.prefix)
		else:PREFIXES=[sys.prefix];ENABLE_USER_SITE=_B
	return known_paths
def execsitecustomize():
	'Run custom site specific code, if available.'
	try:
		try:import sitecustomize
		except ImportError as exc:
			if exc.name=='sitecustomize':0
			else:raise
	except Exception as err:
		if sys.flags.verbose:sys.excepthook(*sys.exc_info())
		else:sys.stderr.write('Error in sitecustomize; set PYTHONVERBOSE for traceback:\n%s: %s\n'%(err.__class__.__name__,err))
def execusercustomize():
	'Run custom user specific code, if available.'
	try:
		try:import usercustomize
		except ImportError as exc:
			if exc.name=='usercustomize':0
			else:raise
	except Exception as err:
		if sys.flags.verbose:sys.excepthook(*sys.exc_info())
		else:sys.stderr.write('Error in usercustomize; set PYTHONVERBOSE for traceback:\n%s: %s\n'%(err.__class__.__name__,err))
def main():
	'Add standard site-specific directories to the module search path.\n\n    This function is called automatically when this module is imported,\n    unless the python interpreter was started with the -S flag.\n    ';global ENABLE_USER_SITE;orig_path=sys.path[:];known_paths=removeduppaths()
	if orig_path!=sys.path:abs_paths()
	known_paths=venv(known_paths)
	if ENABLE_USER_SITE is _A:ENABLE_USER_SITE=check_enableusersite()
	known_paths=addusersitepackages(known_paths);known_paths=addsitepackages(known_paths);setquit();setcopyright();sethelper()
	if not sys.flags.isolated:enablerlcompleter()
	execsitecustomize()
	if ENABLE_USER_SITE:execusercustomize()
if not sys.flags.no_site:main()
def _script():
	help="    %s [--user-base] [--user-site]\n\n    Without arguments print some useful information\n    With arguments print the value of USER_BASE and/or USER_SITE separated\n    by '%s'.\n\n    Exit codes with --user-base or --user-site:\n      0 - user site directory is enabled\n      1 - user site directory is disabled by user\n      2 - user site directory is disabled by super user\n          or for security reasons\n     >2 - unknown error\n    ";args=sys.argv[1:]
	if not args:
		user_base=getuserbase();user_site=getusersitepackages();print('sys.path = [')
		for dir in sys.path:print('    %r,'%(dir,))
		print(']')
		def exists(path):
			if path is not _A and os.path.isdir(path):return'exists'
			else:return"doesn't exist"
		print(f"USER_BASE: {user_base!r} ({exists(user_base)})");print(f"USER_SITE: {user_site!r} ({exists(user_site)})");print(f"ENABLE_USER_SITE: {ENABLE_USER_SITE!r}");sys.exit(0)
	buffer=[]
	if'--user-base'in args:buffer.append(USER_BASE)
	if'--user-site'in args:buffer.append(USER_SITE)
	if buffer:
		print(os.pathsep.join(buffer))
		if ENABLE_USER_SITE:sys.exit(0)
		elif ENABLE_USER_SITE is _B:sys.exit(1)
		elif ENABLE_USER_SITE is _A:sys.exit(2)
		else:sys.exit(3)
	else:import textwrap;print(textwrap.dedent(help%(sys.argv[0],os.pathsep)));sys.exit(10)
if __name__=='__main__':_script()