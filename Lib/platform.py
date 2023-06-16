#!/usr/bin/env python3
' This module tries to retrieve as much platform-identifying data as\n    possible. It makes this information available via function APIs.\n\n    If called from the command line, it prints the platform\n    information concatenated as single string to stdout. The output\n    format is useable as part of a filename.\n\n'
_L='WindowsPE'
_K='unknown'
_J='SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion'
_I='2003Server'
_H='Linux'
_G='Vista'
_F='dos'
_E='win16'
_D='win32'
_C='Windows'
_B='.'
_A=None
__copyright__='\n    Copyright (c) 1999-2000, Marc-Andre Lemburg; mailto:mal@lemburg.com\n    Copyright (c) 2000-2010, eGenix.com Software GmbH; mailto:info@egenix.com\n\n    Permission to use, copy, modify, and distribute this software and its\n    documentation for any purpose and without fee or royalty is hereby granted,\n    provided that the above copyright notice appear in all copies and that\n    both that copyright notice and this permission notice appear in\n    supporting documentation or portions thereof, including modifications,\n    that you make.\n\n    EGENIX.COM SOFTWARE GMBH DISCLAIMS ALL WARRANTIES WITH REGARD TO\n    THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND\n    FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,\n    INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING\n    FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,\n    NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION\n    WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !\n\n'
__version__='1.0.8'
import collections,os,re,sys,subprocess,functools,itertools
_ver_stages={'dev':10,'alpha':20,'a':20,'beta':30,'b':30,'c':40,'RC':50,'rc':50,'pl':200,'p':200}
_component_re=re.compile('([0-9]+|[._+-])')
def _comparable_version(version):
	B=[]
	for A in _component_re.split(version):
		if A not in'._+-':
			try:A=int(A,10);C=100
			except ValueError:C=_ver_stages.get(A,0)
			B.extend((C,A))
	return B
_libc_search=re.compile(b'(__libc_init)|(GLIBC_([0-9.]+))|(libc(_\\w+)?\\.so(?:\\.(\\d[0-9.]*))?)',re.ASCII)
def libc_ver(executable=_A,lib='',version='',chunksize=16384):
	' Tries to determine the libc version that the file executable\n        (which defaults to the Python interpreter) is linked against.\n\n        Returns a tuple of strings (lib,version) which default to the\n        given parameters in case the lookup fails.\n\n        Note that the function has intimate knowledge of how different\n        libc versions add symbols to the executable and thus is probably\n        only useable for executables compiled using gcc.\n\n        The file is read and scanned in chunks of chunksize bytes.\n\n    ';L='libc';M=chunksize;I='glibc';E=executable;C=lib;A=version
	if not E:
		try:
			Q=os.confstr('CS_GNU_LIBC_VERSION');N=Q.split(maxsplit=1)
			if len(N)==2:return tuple(N)
		except(AttributeError,ValueError,OSError):pass
		E=sys.executable
	G=_comparable_version
	if hasattr(os.path,'realpath'):E=os.path.realpath(E)
	with open(E,'rb')as O:
		B=O.read(M);F=0
		while F<len(B):
			if b'libc'in B or b'GLIBC'in B:D=_libc_search.search(B,F)
			else:D=_A
			if not D or D.end()==len(B):
				P=O.read(M)
				if P:B=B[max(F,len(B)-1000):]+P;F=0;continue
				if not D:break
			R,S,J,T,H,K=[A.decode('latin1')if A is not _A else A for A in D.groups()]
			if R and not C:C=L
			elif S:
				if C!=I:C=I;A=J
				elif G(J)>G(A):A=J
			elif T:
				if C!=I:
					C=L
					if K and(not A or G(K)>G(A)):A=K
					if H and A[-len(H):]!=H:A=A+H
			F=D.end()
	return C,A
def _norm_version(version,build=''):
	' Normalize the version and build strings and return a single\n        version string using the format major.minor.build (or patchlevel).\n    ';C=build;A=version;B=A.split(_B)
	if C:B.append(C)
	try:D=list(map(str,map(int,B)))
	except ValueError:D=B
	A=_B.join(D[:3]);return A
_ver_output=re.compile('(?:([\\w ]+) ([\\w.]+) .*\\[.* ([\\d.]+)\\])')
def _syscmd_ver(system='',release='',version='',supported_platforms=(_D,_E,_F)):
	' Tries to figure out the OS version used and returns\n        a tuple (system, release, version).\n\n        It uses the "ver" shell command for this which is known\n        to exists on Windows, DOS. XXX Others too ?\n\n        In case this fails, the given parameters are used as\n        defaults.\n\n    ';C=system;B=release;A=version
	if sys.platform not in supported_platforms:return C,B,A
	import subprocess as D
	for G in('ver','command /c ver','cmd /c ver'):
		try:E=D.check_output(G,stdin=D.DEVNULL,stderr=D.DEVNULL,text=True,shell=True)
		except(OSError,D.CalledProcessError)as H:continue
		else:break
	else:return C,B,A
	E=E.strip();F=_ver_output.match(E)
	if F is not _A:
		C,B,A=F.groups()
		if B[-1]==_B:B=B[:-1]
		if A[-1]==_B:A=A[:-1]
		A=_norm_version(A)
	return C,B,A
_WIN32_CLIENT_RELEASES={(5,0):'2000',(5,1):'XP',(5,2):_I,(5,_A):'post2003',(6,0):_G,(6,1):'7',(6,2):'8',(6,3):'8.1',(6,_A):'post8.1',(10,0):'10',(10,_A):'post10'}
_WIN32_SERVER_RELEASES={(5,2):_I,(6,0):'2008Server',(6,1):'2008ServerR2',(6,2):'2012Server',(6,3):'2012ServerR2',(6,_A):'post2012ServerR2'}
def win32_is_iot():return win32_edition()in('IoTUAP','NanoServer','WindowsCoreHeadless','IoTEdgeOS')
def win32_edition():
	try:
		try:import winreg as A
		except ImportError:import _winreg as A
	except ImportError:pass
	else:
		try:
			B=_J
			with A.OpenKeyEx(A.HKEY_LOCAL_MACHINE,B)as C:return A.QueryValueEx(C,'EditionId')[0]
		except OSError:pass
def win32_ver(release='',version='',csd='',ptype=''):
	G=ptype;H=version;B=csd;C=release
	try:from sys import getwindowsversion as J
	except ImportError:return C,H,B,G
	D=J()
	try:A,E,I=map(int,_syscmd_ver()[2].split(_B))
	except ValueError:A,E,I=D.platform_version or D[:3]
	H='{0}.{1}.{2}'.format(A,E,I);C=_WIN32_CLIENT_RELEASES.get((A,E))or _WIN32_CLIENT_RELEASES.get((A,_A))or C
	if D[:2]==(A,E):
		try:B='SP{}'.format(D.service_pack_major)
		except AttributeError:
			if B[:13]=='Service Pack ':B='SP'+B[13:]
	if getattr(D,'product_type',_A)==3:C=_WIN32_SERVER_RELEASES.get((A,E))or _WIN32_SERVER_RELEASES.get((A,_A))or C
	try:
		try:import winreg as F
		except ImportError:import _winreg as F
	except ImportError:pass
	else:
		try:
			K=_J
			with F.OpenKeyEx(F.HKEY_LOCAL_MACHINE,K)as L:G=F.QueryValueEx(L,'CurrentType')[0]
		except OSError:pass
	return C,H,B,G
def _mac_ver_xml():
	B='/System/Library/CoreServices/SystemVersion.plist'
	if not os.path.exists(B):return
	try:import plistlib as C
	except ImportError:return
	with open(B,'rb')as D:E=C.load(D)
	F=E['ProductVersion'];G='','','';A=os.uname().machine
	if A in('ppc','Power Macintosh'):A='PowerPC'
	return F,G,A
def mac_ver(release='',versioninfo=('','',''),machine=''):
	" Get macOS version information and return it as tuple (release,\n        versioninfo, machine) with versioninfo being a tuple (version,\n        dev_stage, non_release_version).\n\n        Entries which cannot be determined are set to the parameter values\n        which default to ''. All tuple entries are strings.\n    ";A=_mac_ver_xml()
	if A is not _A:return A
	return release,versioninfo,machine
def _java_getprop(name,default):
	A=default;from java.lang import System as C
	try:
		B=C.getProperty(name)
		if B is _A:return A
		return B
	except AttributeError:return A
def java_ver(release='',vendor='',vminfo=('','',''),osinfo=('','','')):
	" Version interface for Jython.\n\n        Returns a tuple (release, vendor, vminfo, osinfo) with vminfo being\n        a tuple (vm_name, vm_release, vm_vendor) and osinfo being a\n        tuple (os_name, os_version, os_arch).\n\n        Values which cannot be determined are set to the defaults\n        given as parameters (which all default to '').\n\n    ";A=osinfo;B=vminfo;C=vendor;D=release
	try:import java.lang
	except ImportError:return D,C,B,A
	C=_java_getprop('java.vendor',C);D=_java_getprop('java.version',D);E,F,G=B;E=_java_getprop('java.vm.name',E);G=_java_getprop('java.vm.vendor',G);F=_java_getprop('java.vm.version',F);B=E,F,G;H,I,J=A;J=_java_getprop('java.os.arch',J);H=_java_getprop('java.os.name',H);I=_java_getprop('java.os.version',I);A=H,I,J;return D,C,B,A
def system_alias(system,release,version):
	' Returns (system, release, version) aliased to common\n        marketing names used for some systems.\n\n        It also does some reordering of the information in some cases\n        where it would otherwise cause confusion.\n\n    ';E='Solaris';F=version;B=release;A=system
	if A=='SunOS':
		if B<'5':return A,B,F
		C=B.split(_B)
		if C:
			try:D=int(C[0])
			except ValueError:pass
			else:D=D-3;C[0]=str(D);B=_B.join(C)
		if B<'6':A=E
		else:A=E
	elif A in(_D,_E):A=_C
	return A,B,F
def _platform(*D):
	' Helper to format the platform string in a filename\n        compatible format e.g. "system-version-machine".\n    ';B='-';A=B.join(A.strip()for A in filter(len,D));A=A.replace(' ','_');A=A.replace('/',B);A=A.replace('\\',B);A=A.replace(':',B);A=A.replace(';',B);A=A.replace('"',B);A=A.replace('(',B);A=A.replace(')',B);A=A.replace(_K,'')
	while 1:
		C=A.replace('--',B)
		if C==A:break
		A=C
	while A[-1]==B:A=A[:-1]
	return A
def _node(default=''):
	' Helper to determine the node name of this machine.\n    ';A=default
	try:import socket as B
	except ImportError:return A
	try:return B.gethostname()
	except OSError:return A
def _follow_symlinks(filepath):
	' In case filepath is a symlink, follow it until a\n        real file is reached.\n    ';A=filepath;A=os.path.abspath(A)
	while os.path.islink(A):A=os.path.normpath(os.path.join(os.path.dirname(A),os.readlink(A)))
	return A
def _syscmd_file(target,default=''):
	" Interface to the system's file command.\n\n        The function uses the -b option of the file command to have it\n        omit the filename in its output. Follow the symlinks. It returns\n        default in case the command should fail.\n\n    ";A=default;B=target
	if sys.platform in(_F,_D,_E):return A
	import subprocess as C;B=_follow_symlinks(B);E=dict(os.environ,LC_ALL='C')
	try:D=C.check_output(['file','-b',B],stderr=C.DEVNULL,env=E)
	except(OSError,C.CalledProcessError):return A
	if not D:return A
	return D.decode('latin-1')
_default_architecture={_D:('',_L),_E:('',_C),_F:('','MSDOS')}
def architecture(executable=sys.executable,bits='',linkage=''):
	' Queries the given executable (defaults to the Python interpreter\n        binary) for various architecture information.\n\n        Returns a tuple (bits, linkage) which contains information about\n        the bit architecture and the linkage format used for the\n        executable. Both values are returned as strings.\n\n        Values that cannot be determined are returned as given by the\n        parameter presets. If bits is given as \'\', the sizeof(pointer)\n        (or sizeof(long) on Python version < 1.5.2) is used as\n        indicator for the supported pointer size.\n\n        The function relies on the system\'s "file" command to do the\n        actual work. This is available on most if not all Unix\n        platforms. On some non-Unix platforms where the "file" command\n        does not exist and the executable is set to the Python interpreter\n        binary defaults from _default_architecture are used.\n\n    ';E='COFF';F='ELF';D=executable;C=bits;B=linkage
	if not C:import struct as I;J=I.calcsize('P');C=str(J*8)+'bit'
	if D:A=_syscmd_file(D,'')
	else:A=''
	if not A and D==sys.executable:
		if sys.platform in _default_architecture:
			G,H=_default_architecture[sys.platform]
			if G:C=G
			if H:B=H
		return C,B
	if'executable'not in A and'shared object'not in A:return C,B
	if'32-bit'in A:C='32bit'
	elif'64-bit'in A:C='64bit'
	if F in A:B=F
	elif'PE'in A:
		if _C in A:B=_L
		else:B='PE'
	elif E in A:B=E
	elif'MS-DOS'in A:B='MSDOS'
	else:0
	return C,B
def _get_machine_win32():return os.environ.get('PROCESSOR_ARCHITEW6432','')or os.environ.get('PROCESSOR_ARCHITECTURE','')
class _Processor:
	@classmethod
	def get(A):B=getattr(A,f"get_{sys.platform}",A.from_subprocess);return B()or''
	def get_win32():return os.environ.get('PROCESSOR_IDENTIFIER',_get_machine_win32())
	def get_OpenVMS():
		try:import vms_lib as A
		except ImportError:pass
		else:C,B=A.getsyi('SYI$_CPU',0);return'Alpha'if B>=128 else'VAX'
	def from_subprocess():
		'\n        Fall back to `uname -p`\n        '
		try:return subprocess.check_output(['uname','-p'],stderr=subprocess.DEVNULL,text=True).strip()
		except(OSError,subprocess.CalledProcessError):pass
def _unknown_as_blank(val):return''if val==_K else val
class uname_result(collections.namedtuple('uname_result_base','system node release version machine')):
	'\n    A uname_result that\'s largely compatible with a\n    simple namedtuple except that \'processor\' is\n    resolved late and cached to avoid calling "uname"\n    except when needed.\n    '
	@functools.cached_property
	def processor(self):return _unknown_as_blank(_Processor.get())
	def __iter__(A):return itertools.chain(super().__iter__(),(A.processor,))
	@classmethod
	def _make(A,iterable):
		C=len(A._fields);B=A.__new__(A,*iterable)
		if len(B)!=C+1:D=f"Expected {C} arguments, got {len(B)}";raise TypeError(D)
		return B
	def __getitem__(A,key):return tuple(A)[key]
	def __len__(A):return len(tuple(iter(A)))
	def __reduce__(A):return uname_result,tuple(A)[:len(A._fields)]
_uname_cache=_A
def uname():
	" Fairly portable uname interface. Returns a tuple\n        of strings (system, node, release, version, machine, processor)\n        identifying the underlying platform.\n\n        Note that unlike the os.uname function this also returns\n        possible processor information as an additional tuple entry.\n\n        Entries which cannot be determined are set to ''.\n\n    ";E='Microsoft';global _uname_cache
	if _uname_cache is not _A:return _uname_cache
	try:A,F,B,C,D=G=os.uname()
	except AttributeError:A=sys.platform;F=_node();B=C=D='';G=()
	if not any(G):
		if A==_D:B,C,K,L=win32_ver();D=D or _get_machine_win32()
		if not(B and C):
			A,B,C=_syscmd_ver(A)
			if A=='Microsoft Windows':A=_C
			elif A==E and B==_C:
				A=_C
				if'6.0'==C[:3]:B=_G
				else:B=''
		if A in(_D,_E):
			if not C:
				if A==_D:C='32bit'
				else:C='16bit'
			A=_C
		elif A[:4]=='java':
			B,H,I,M=java_ver();A='Java';C=', '.join(I)
			if not C:C=H
	if A=='OpenVMS':
		if not B or B=='0':B=C;C=''
	if A==E and B==_C:A=_C;B=_G
	J=A,F,B,C,D;_uname_cache=uname_result(*map(_unknown_as_blank,J));return _uname_cache
def system():" Returns the system/OS name, e.g. 'Linux', 'Windows' or 'Java'.\n\n        An empty string is returned if the value cannot be determined.\n\n    ";return uname().system
def node():" Returns the computer's network name (which may not be fully\n        qualified)\n\n        An empty string is returned if the value cannot be determined.\n\n    ";return uname().node
def release():" Returns the system's release, e.g. '2.2.0' or 'NT'\n\n        An empty string is returned if the value cannot be determined.\n\n    ";return uname().release
def version():" Returns the system's release version, e.g. '#3 on degas'\n\n        An empty string is returned if the value cannot be determined.\n\n    ";return uname().version
def machine():" Returns the machine type, e.g. 'i386'\n\n        An empty string is returned if the value cannot be determined.\n\n    ";return uname().machine
def processor():" Returns the (true) processor name, e.g. 'amdk6'\n\n        An empty string is returned if the value cannot be\n        determined. Note that many platforms do not provide this\n        information or simply return the same value as for machine(),\n        e.g.  NetBSD does this.\n\n    ";return uname().processor
_sys_version_parser=re.compile('([\\w.+]+)\\s*\\(#?([^,]+)(?:,\\s*([\\w ]*)(?:,\\s*([\\w :]*))?)?\\)\\s*\\[([^\\]]+)\\]?',re.ASCII)
_ironpython_sys_version_parser=re.compile('IronPython\\s*([\\d\\.]+)(?: \\(([\\d\\.]+)\\))? on (.NET [\\d\\.]+)',re.ASCII)
_ironpython26_sys_version_parser=re.compile('([\\d.]+)\\s*\\(IronPython\\s*[\\d.]+\\s*\\(([\\d.]+)\\) on ([\\w.]+ [\\d.]+(?: \\(\\d+-bit\\))?)\\)')
_pypy_sys_version_parser=re.compile('([\\w.+]+)\\s*\\(#?([^,]+),\\s*([\\w ]+),\\s*([\\w :]+)\\)\\s*\\[PyPy [^\\]]+\\]?')
_sys_version_cache={}
def _sys_version(sys_version=_A):
	" Returns a parsed version of Python's sys.version as tuple\n        (name, version, branch, revision, buildno, builddate, compiler)\n        referring to the Python implementation name, version, branch,\n        revision, build number, build date/time as string and the compiler\n        identification string.\n\n        Note that unlike the Python sys.version, the returned value\n        for the Python version will always include the patchlevel (it\n        defaults to '.0').\n\n        The function returns empty strings for tuple entries that\n        cannot be determined.\n\n        sys_version may be given to parse an alternative version\n        string, e.g. if the version was read from a different Python\n        interpreter.\n\n    ";N='PyPy';J='IronPython';A=sys_version
	if A is _A:A=sys.version
	E=_sys_version_cache.get(A,_A)
	if E is not _A:return E
	if J in A:
		F=J
		if A.startswith(J):B=_ironpython_sys_version_parser.match(A)
		else:B=_ironpython26_sys_version_parser.match(A)
		if B is _A:raise ValueError('failed to parse IronPython sys.version: %s'%repr(A))
		D,P,G=B.groups();H='';C=''
	elif sys.platform.startswith('java'):
		F='Jython';B=_sys_version_parser.match(A)
		if B is _A:raise ValueError('failed to parse Jython sys.version: %s'%repr(A))
		D,H,C,I,O=B.groups()
		if C is _A:C=''
		G=sys.platform
	elif N in A:
		F=N;B=_pypy_sys_version_parser.match(A)
		if B is _A:raise ValueError('failed to parse PyPy sys.version: %s'%repr(A))
		D,H,C,I=B.groups();G=''
	else:
		B=_sys_version_parser.match(A)
		if B is _A:raise ValueError('failed to parse CPython sys.version: %s'%repr(A))
		D,H,C,I,G=B.groups()
		if'rustc'in A:F='RustPython'
		else:F='CPython'
		if C is _A:C=''
		elif I:C=C+' '+I
	if hasattr(sys,'_git'):O,K,L=sys._git
	elif hasattr(sys,'_mercurial'):O,K,L=sys._mercurial
	else:K='';L=''
	M=D.split(_B)
	if len(M)==2:M.append('0');D=_B.join(M)
	E=F,D,K,L,H,C,G;_sys_version_cache[A]=E;return E
def python_implementation():" Returns a string identifying the Python implementation.\n\n        Currently, the following implementations are identified:\n          'CPython' (C implementation of Python),\n          'IronPython' (.NET implementation of Python),\n          'Jython' (Java implementation of Python),\n          'PyPy' (Python implementation of Python).\n\n    ";return _sys_version()[0]
def python_version():" Returns the Python version as string 'major.minor.patchlevel'\n\n        Note that unlike the Python sys.version, the returned value\n        will always include the patchlevel (it defaults to 0).\n\n    ";return _sys_version()[1]
def python_version_tuple():' Returns the Python version as tuple (major, minor, patchlevel)\n        of strings.\n\n        Note that unlike the Python sys.version, the returned value\n        will always include the patchlevel (it defaults to 0).\n\n    ';return tuple(_sys_version()[1].split(_B))
def python_branch():' Returns a string identifying the Python implementation\n        branch.\n\n        For CPython this is the SCM branch from which the\n        Python binary was built.\n\n        If not available, an empty string is returned.\n\n    ';return _sys_version()[2]
def python_revision():' Returns a string identifying the Python implementation\n        revision.\n\n        For CPython this is the SCM revision from which the\n        Python binary was built.\n\n        If not available, an empty string is returned.\n\n    ';return _sys_version()[3]
def python_build():' Returns a tuple (buildno, builddate) stating the Python\n        build number and date as strings.\n\n    ';return _sys_version()[4:6]
def python_compiler():' Returns a string identifying the compiler used for compiling\n        Python.\n\n    ';return _sys_version()[6]
_platform_cache={}
def platform(aliased=0,terse=0):
	' Returns a single string identifying the underlying platform\n        with as much useful information as possible (but no more :).\n\n        The output is intended to be human readable rather than\n        machine parseable. It may look different on different\n        platforms and this is intended.\n\n        If "aliased" is true, the function will use aliases for\n        various platforms that report system names which differ from\n        their common names, e.g. SunOS will be reported as\n        Solaris. The system_alias() function is used to implement\n        this.\n\n        Setting terse to true causes the function to return only the\n        absolute minimum information needed to identify the platform.\n\n    ';G=aliased;E=terse;I=_platform_cache.get((G,E),_A)
	if I is not _A:return I
	A,S,B,D,H,F=uname()
	if H==F:F=''
	if G:A,B,D=system_alias(A,B,D)
	if A=='Darwin':
		J=mac_ver()[0]
		if J:A='macOS';B=J
	if A==_C:
		T,U,L,V=win32_ver(D)
		if E:C=_platform(A,B)
		else:C=_platform(A,B,D,L)
	elif A in(_H,):M,N=libc_ver();C=_platform(A,B,H,F,'with',M+N)
	elif A=='Java':
		W,X,Y,(K,O,P)=java_ver()
		if E or not K:C=_platform(A,B,D)
		else:C=_platform(A,B,D,'on',K,O,P)
	elif E:C=_platform(A,B)
	else:Q,R=architecture(sys.executable);C=_platform(A,B,H,F,Q,R)
	_platform_cache[G,E]=C;return C
_os_release_line=re.compile('^(?P<name>[a-zA-Z0-9_]+)=(?P<quote>["\']?)(?P<value>.*)(?P=quote)$')
_os_release_unescape=re.compile('\\\\([\\\\\\$\\"\\\'`])')
_os_release_candidates='/etc/os-release','/usr/lib/os-release'
_os_release_cache=_A
def _parse_os_release(lines):
	B={'NAME':_H,'ID':'linux','PRETTY_NAME':_H}
	for C in lines:
		A=_os_release_line.match(C)
		if A is not _A:B[A.group('name')]=_os_release_unescape.sub('\\1',A.group('value'))
	return B
def freedesktop_os_release():
	'Return operation system identification from freedesktop.org os-release\n    ';global _os_release_cache
	if _os_release_cache is _A:
		A=_A
		for B in _os_release_candidates:
			try:
				with open(B,encoding='utf-8')as C:_os_release_cache=_parse_os_release(C)
				break
			except OSError as D:A=D.errno
		else:raise OSError(A,f"Unable to read files {', '.join(_os_release_candidates)}")
	return _os_release_cache.copy()
if __name__=='__main__':terse='terse'in sys.argv or'--terse'in sys.argv;aliased=not'nonaliased'in sys.argv and not'--nonaliased'in sys.argv;print(platform(aliased,terse));sys.exit(0)