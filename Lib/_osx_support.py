'Shared OS X support functions.'
_M='-arch\\s+\\w+\\s'
_L='\'"\'"\''
_K='LDSHARED'
_J='BLDSHARED'
_I='CXX'
_H='-arch'
_G='ARCHFLAGS'
_F=True
_E='CFLAGS'
_D=False
_C='CC'
_B=' '
_A=None
import os,re,sys
__all__=['compiler_fixup','customize_config_vars','customize_compiler','get_platform_osx']
_UNIVERSAL_CONFIG_VARS=_E,'LDFLAGS','CPPFLAGS','BASECFLAGS',_J,_K,_C,_I,'PY_CFLAGS','PY_LDFLAGS','PY_CPPFLAGS','PY_CORE_CFLAGS','PY_CORE_LDFLAGS'
_COMPILER_CONFIG_VARS=_J,_K,_C,_I
_INITPRE='_OSX_SUPPORT_INITIAL_'
def _find_executable(executable,path=_A):
	"Tries to find 'executable' in the directories listed in 'path'.\n\n    A string listing directories separated by 'os.pathsep'; defaults to\n    os.environ['PATH'].  Returns the complete filename or None if not found.\n    ";C='.exe';B=path;A=executable
	if B is _A:B=os.environ['PATH']
	E=B.split(os.pathsep);H,F=os.path.splitext(A)
	if sys.platform=='win32'and F!=C:A=A+C
	if not os.path.isfile(A):
		for G in E:
			D=os.path.join(G,A)
			if os.path.isfile(D):return D
		return
	else:return A
def _read_output(commandstring,capture_stderr=_D):
	'Output from successful command execution or None';B=commandstring;import contextlib as D
	try:import tempfile as E;A=E.NamedTemporaryFile()
	except ImportError:A=open('/tmp/_osx_support.%s'%(os.getpid(),),'w+b')
	with D.closing(A)as A:
		if capture_stderr:C="%s >'%s' 2>&1"%(B,A.name)
		else:C="%s 2>/dev/null >'%s'"%(B,A.name)
		return A.read().decode('utf-8').strip()if not os.system(C)else _A
def _find_build_tool(toolname):'Find a build tool on current path or using xcrun';A=toolname;return _find_executable(A)or _read_output('/usr/bin/xcrun -find %s'%(A,))or''
_SYSTEM_VERSION=_A
def _get_system_version():
	'Return the OS X system version as a string';global _SYSTEM_VERSION
	if _SYSTEM_VERSION is _A:
		_SYSTEM_VERSION=''
		try:A=open('/System/Library/CoreServices/SystemVersion.plist',encoding='utf-8')
		except OSError:pass
		else:
			try:B=re.search('<key>ProductUserVisibleVersion</key>\\s*<string>(.*?)</string>',A.read())
			finally:A.close()
			if B is not _A:_SYSTEM_VERSION='.'.join(B.group(1).split('.')[:2])
	return _SYSTEM_VERSION
_SYSTEM_VERSION_TUPLE=_A
def _get_system_version_tuple():
	'\n    Return the macOS system version as a tuple\n\n    The return value is safe to use to compare\n    two version numbers.\n    ';global _SYSTEM_VERSION_TUPLE
	if _SYSTEM_VERSION_TUPLE is _A:
		A=_get_system_version()
		if A:
			try:_SYSTEM_VERSION_TUPLE=tuple(int(A)for A in A.split('.'))
			except ValueError:_SYSTEM_VERSION_TUPLE=()
	return _SYSTEM_VERSION_TUPLE
def _remove_original_values(_config_vars):
	'Remove original unmodified values for testing';A=_config_vars
	for B in list(A):
		if B.startswith(_INITPRE):del A[B]
def _save_modified_value(_config_vars,cv,newvalue):
	'Save modified and original unmodified value of configuration var';B=newvalue;A=_config_vars;C=A.get(cv,'')
	if C!=B and _INITPRE+cv not in A:A[_INITPRE+cv]=C
	A[cv]=B
_cache_default_sysroot=_A
def _default_sysroot(cc):
	" Returns the root of the default SDK for this system, or '/' ";global _cache_default_sysroot
	if _cache_default_sysroot is not _A:return _cache_default_sysroot
	C=_read_output('%s -c -E -v - </dev/null'%(cc,),_F);B=_D
	for A in C.splitlines():
		if A.startswith('#include <...>'):B=_F
		elif A.startswith('End of search list'):B=_D
		elif B:
			A=A.strip()
			if A=='/usr/include':_cache_default_sysroot='/'
			elif A.endswith('.sdk/usr/include'):_cache_default_sysroot=A[:-12]
	if _cache_default_sysroot is _A:_cache_default_sysroot='/'
	return _cache_default_sysroot
def _supports_universal_builds():'Returns True if universal builds are supported on this system';A=_get_system_version_tuple();return bool(A>=(10,4))if A else _D
def _supports_arm64_builds():'Returns True if arm64 builds are supported on this system';A=_get_system_version_tuple();return A>=(11,0)if A else _D
def _find_appropriate_compiler(_config_vars):
	'Find appropriate C compiler for extension module builds';D='clang';B=_config_vars
	if _C in os.environ:return B
	A=G=B[_C].split()[0]
	if not _find_executable(A):A=_find_build_tool(D)
	elif os.path.basename(A).startswith('gcc'):
		E=_read_output("'%s' --version"%(A.replace("'",_L),))
		if E and'llvm-gcc'in E:A=_find_build_tool(D)
	if not A:raise SystemError('Cannot locate working compiler')
	if A!=G:
		for C in _COMPILER_CONFIG_VARS:
			if C in B and C not in os.environ:F=B[C].split();F[0]=A if C!=_I else A+'++';_save_modified_value(B,C,_B.join(F))
	return B
def _remove_universal_flags(_config_vars):
	'Remove all universal build arguments from config vars';B=_config_vars
	for C in _UNIVERSAL_CONFIG_VARS:
		if C in B and C not in os.environ:A=B[C];A=re.sub(_M,_B,A,flags=re.ASCII);A=re.sub('-isysroot\\s*\\S+',_B,A);_save_modified_value(B,C,A)
	return B
def _remove_unsupported_archs(_config_vars):
	'Remove any unsupported archs from config vars';A=_config_vars
	if _C in os.environ:return A
	if re.search('-arch\\s+ppc',A[_E])is not _A:
		D=os.system("echo 'int main{};' | '%s' -c -arch ppc -x c -o /dev/null /dev/null 2>/dev/null"%(A[_C].replace("'",_L),))
		if D:
			for B in _UNIVERSAL_CONFIG_VARS:
				if B in A and B not in os.environ:C=A[B];C=re.sub('-arch\\s+ppc\\w*\\s',_B,C);_save_modified_value(A,B,C)
	return A
def _override_all_archs(_config_vars):
	'Allow override of all archs with ARCHFLAGS env var';A=_config_vars
	if _G in os.environ:
		D=os.environ[_G]
		for C in _UNIVERSAL_CONFIG_VARS:
			if C in A and _H in A[C]:B=A[C];B=re.sub(_M,_B,B);B=B+_B+D;_save_modified_value(A,C,B)
	return A
def _check_for_unavailable_sdk(_config_vars):
	'Remove references to any SDKs not available';A=_config_vars;E=A.get(_E,'');D=re.search('-isysroot\\s*(\\S+)',E)
	if D is not _A:
		F=D.group(1)
		if not os.path.exists(F):
			for B in _UNIVERSAL_CONFIG_VARS:
				if B in A and B not in os.environ:C=A[B];C=re.sub('-isysroot\\s*\\S+(?:\\s|$)',_B,C);_save_modified_value(A,B,C)
	return A
def compiler_fixup(compiler_so,cc_args):
	"\n    This function will strip '-isysroot PATH' and '-arch ARCH' from the\n    compile flags if the user has specified one them in extra_compile_flags.\n\n    This is needed because '-arch ARCH' adds another architecture to the\n    build, without a way to remove an architecture. Furthermore GCC will\n    barf if multiple '-isysroot' arguments are present.\n    ";G=cc_args;D='-isysroot';A=compiler_so;H=J=_D;A=list(A)
	if not _supports_universal_builds():H=J=_F
	else:H=_H in G;J=any(A for A in G if A.startswith(D))
	if H or _G in os.environ:
		while _F:
			try:B=A.index(_H);del A[B:B+2]
			except ValueError:break
	elif not _supports_arm64_builds():
		for C in reversed(range(len(A))):
			if A[C]==_H and A[C+1]=='arm64':del A[C:C+2]
	if _G in os.environ and not H:A=A+os.environ[_G].split()
	if J:
		while _F:
			E=[A for(A,B)in enumerate(A)if B.startswith(D)]
			if not E:break
			B=E[0]
			if A[B]==D:del A[B:B+2]
			else:del A[B:B+1]
	F=_A;I=G;E=[A for(A,B)in enumerate(G)if B.startswith(D)]
	if not E:I=A;E=[A for(A,B)in enumerate(A)if B.startswith(D)]
	for C in E:
		if I[C]==D:F=I[C+1];break
		else:F=I[C][len(D):];break
	if F and not os.path.isdir(F):sys.stderr.write(f"Compiling with an SDK that doesn't seem to exist: {F}\n");sys.stderr.write('Please check your Xcode installation\n');sys.stderr.flush()
	return A
def customize_config_vars(_config_vars):
	'Customize Python build configuration variables.\n\n    Called internally from sysconfig with a mutable mapping\n    containing name/value pairs parsed from the configured\n    makefile used to build this interpreter.  Returns\n    the mapping updated as needed to reflect the environment\n    in which the interpreter is running; in the case of\n    a Python from a binary installer, the installed\n    environment may be very different from the build\n    environment, i.e. different OS levels, different\n    built tools, different available CPU architectures.\n\n    This customization is performed whenever\n    distutils.sysconfig.get_config_vars() is first\n    called.  It may be used in environments where no\n    compilers are present, i.e. when installing pure\n    Python dists.  Customization of compiler paths\n    and detection of unavailable archs is deferred\n    until the first extension module build is\n    requested (in distutils.sysconfig.customize_compiler).\n\n    Currently called from distutils.sysconfig\n    ';A=_config_vars
	if not _supports_universal_builds():_remove_universal_flags(A)
	_override_all_archs(A);_check_for_unavailable_sdk(A);return A
def customize_compiler(_config_vars):'Customize compiler path and configuration variables.\n\n    This customization is performed when the first\n    extension module build is requested\n    in distutils.sysconfig.customize_compiler.\n    ';A=_config_vars;_find_appropriate_compiler(A);_remove_unsupported_archs(A);_override_all_archs(A);return A
def get_platform_osx(_config_vars,osname,release,machine):
	'Filter values for get_platform()';J='fat';K=release;L=osname;H='ppc64';I=_config_vars;G='ppc';E='i386';D='x86_64';A=machine;F=I.get('MACOSX_DEPLOYMENT_TARGET','');C=_get_system_version()or F;F=F or C
	if F:
		K=F;L='macosx';M=I.get(_INITPRE+_E,I.get(_E,''))
		if C:
			try:C=tuple(int(A)for A in C.split('.')[0:2])
			except ValueError:C=10,3
		else:C=10,3
		if C>=(10,4)and _H in M.strip():
			A=J;B=re.findall('-arch\\s+(\\S+)',M);B=tuple(sorted(set(B)))
			if len(B)==1:A=B[0]
			elif B==('arm64',D):A='universal2'
			elif B==(E,G):A=J
			elif B==(E,D):A='intel'
			elif B==(E,G,D):A='fat3'
			elif B==(H,D):A='fat64'
			elif B==(E,G,H,D):A='universal'
			else:raise ValueError("Don't know machine value for archs=%r"%(B,))
		elif A==E:
			if sys.maxsize>=2**32:A=D
		elif A in('PowerPC','Power_Macintosh'):
			if sys.maxsize>=2**32:A=H
			else:A=G
	return L,K,A