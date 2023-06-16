'Common operations on Posix pathnames.\n\nInstead of importing this module directly, import os and refer to\nthis module as os.path.  The "os.path" name is an alias for this\nmodule on Posix systems; on other systems (e.g. Windows),\nos.path provides the same operations in a manner specific to that\nplatform, and is an alias to another module (e.g. ntpath).\n\nSome of this can actually be useful on non-Posix systems too, e.g.\nfor manipulation of the pathname component of URLs.\n'
_K='commonpath'
_J='relpath'
_I=b'..'
_H=True
_G=b'.'
_F='..'
_E=b'/'
_D='.'
_C='/'
_B=False
_A=None
curdir=_D
pardir=_F
extsep=_D
sep=_C
pathsep=':'
defpath='/bin:/usr/bin'
altsep=_A
devnull='/dev/null'
try:import os
except ImportError:import _dummy_os as os
import sys,stat,genericpath
from genericpath import*
__all__=['normcase','isabs','join','splitdrive','split','splitext','basename','dirname','commonprefix','getsize','getmtime','getatime','getctime','islink','exists','lexists','isdir','isfile','ismount','expanduser','expandvars','normpath','abspath','samefile','sameopenfile','samestat','curdir','pardir','sep','pathsep','defpath','altsep','extsep','devnull','realpath','supports_unicode_filenames',_J,_K]
def _get_sep(path):
	if isinstance(path,bytes):return _E
	else:return _C
def normcase(s):'Normalize case of pathname.  Has no effect under Posix';return os.fspath(s)
def isabs(s):'Test whether a path is absolute';s=os.fspath(s);sep=_get_sep(s);return s.startswith(sep)
def join(a,*p):
	"Join two or more pathname components, inserting '/' as needed.\n    If any component is an absolute path, all previous path components\n    will be discarded.  An empty last part will result in a path that\n    ends with a separator.";a=os.fspath(a);sep=_get_sep(a);path=a
	try:
		if not p:path[:0]+sep
		for b in map(os.fspath,p):
			if b.startswith(sep):path=b
			elif not path or path.endswith(sep):path+=b
			else:path+=sep+b
	except(TypeError,AttributeError,BytesWarning):genericpath._check_arg_types('join',a,*p);raise
	return path
def split(p):
	'Split a pathname.  Returns tuple "(head, tail)" where "tail" is\n    everything after the final slash.  Either part may be empty.';p=os.fspath(p);sep=_get_sep(p);i=p.rfind(sep)+1;head,tail=p[:i],p[i:]
	if head and head!=sep*len(head):head=head.rstrip(sep)
	return head,tail
def splitext(p):
	p=os.fspath(p)
	if isinstance(p,bytes):sep=_E;extsep=_G
	else:sep=_C;extsep=_D
	return genericpath._splitext(p,sep,_A,extsep)
splitext.__doc__=genericpath._splitext.__doc__
def splitdrive(p):'Split a pathname into drive and path. On Posix, drive is always\n    empty.';p=os.fspath(p);return p[:0],p
def basename(p):'Returns the final component of a pathname';p=os.fspath(p);sep=_get_sep(p);i=p.rfind(sep)+1;return p[i:]
def dirname(p):
	'Returns the directory component of a pathname';p=os.fspath(p);sep=_get_sep(p);i=p.rfind(sep)+1;head=p[:i]
	if head and head!=sep*len(head):head=head.rstrip(sep)
	return head
def islink(path):
	'Test whether a path is a symbolic link'
	try:st=os.lstat(path)
	except(OSError,ValueError,AttributeError):return _B
	return stat.S_ISLNK(st.st_mode)
def lexists(path):
	'Test whether a path exists.  Returns True for broken symbolic links'
	try:os.lstat(path)
	except(OSError,ValueError):return _B
	return _H
def ismount(path):
	'Test whether a path is a mount point'
	try:s1=os.lstat(path)
	except(OSError,ValueError):return _B
	else:
		if stat.S_ISLNK(s1.st_mode):return _B
	if isinstance(path,bytes):parent=join(path,_I)
	else:parent=join(path,_F)
	parent=realpath(parent)
	try:s2=os.lstat(parent)
	except(OSError,ValueError):return _B
	dev1=s1.st_dev;dev2=s2.st_dev
	if dev1!=dev2:return _H
	ino1=s1.st_ino;ino2=s2.st_ino
	if ino1==ino2:return _H
	return _B
def expanduser(path):
	'Expand ~ and ~user constructions.  If user or $HOME is unknown,\n    do nothing.';A='HOME';path=os.fspath(path)
	if isinstance(path,bytes):tilde=b'~'
	else:tilde='~'
	if not path.startswith(tilde):return path
	sep=_get_sep(path);i=path.find(sep,1)
	if i<0:i=len(path)
	if i==1:
		if A not in os.environ:
			import pwd
			try:userhome=pwd.getpwuid(os.getuid()).pw_dir
			except KeyError:return path
		else:userhome=os.environ[A]
	else:
		import pwd;name=path[1:i]
		if isinstance(name,bytes):name=str(name,'ASCII')
		try:pwent=pwd.getpwnam(name)
		except KeyError:return path
		userhome=pwent.pw_dir
	if userhome is _A and sys.platform=='vxworks':return path
	if isinstance(path,bytes):userhome=os.fsencode(userhome);root=_E
	else:root=_C
	userhome=userhome.rstrip(root);return userhome+path[i:]or root
_varprog=_A
_varprogb=_A
def expandvars(path):
	'Expand shell variables of form $var and ${var}.  Unknown variables\n    are left unchanged.';path=os.fspath(path);global _varprog,_varprogb
	if isinstance(path,bytes):
		if b'$'not in path:return path
		if not _varprogb:import re;_varprogb=re.compile(b'\\$(\\w+|\\{[^}]*\\})',re.ASCII)
		search=_varprogb.search;start=b'{';end=b'}';environ=getattr(os,'environb',_A)
	else:
		if'$'not in path:return path
		if not _varprog:import re;_varprog=re.compile('\\$(\\w+|\\{[^}]*\\})',re.ASCII)
		search=_varprog.search;start='{';end='}';environ=os.environ
	i=0
	while _H:
		m=search(path,i)
		if not m:break
		i,j=m.span(0);name=m.group(1)
		if name.startswith(start)and name.endswith(end):name=name[1:-1]
		try:
			if environ is _A:value=os.fsencode(os.environ[os.fsdecode(name)])
			else:value=environ[name]
		except KeyError:i=j
		else:tail=path[j:];path=path[:i]+value;i=len(path);path+=tail
	return path
def normpath(path):
	'Normalize path, eliminating double slashes, etc.';path=os.fspath(path)
	if isinstance(path,bytes):sep=_E;empty=b'';dot=_G;dotdot=_I
	else:sep=_C;empty='';dot=_D;dotdot=_F
	if path==empty:return dot
	initial_slashes=path.startswith(sep)
	if initial_slashes and path.startswith(sep*2)and not path.startswith(sep*3):initial_slashes=2
	comps=path.split(sep);new_comps=[]
	for comp in comps:
		if comp in(empty,dot):continue
		if comp!=dotdot or not initial_slashes and not new_comps or new_comps and new_comps[-1]==dotdot:new_comps.append(comp)
		elif new_comps:new_comps.pop()
	comps=new_comps;path=sep.join(comps)
	if initial_slashes:path=sep*initial_slashes+path
	return path or dot
def abspath(path):
	'Return an absolute path.';path=os.fspath(path)
	if not isabs(path):
		if isinstance(path,bytes):cwd=os.getcwdb()
		else:cwd=os.getcwd()
		path=join(cwd,path)
	return normpath(path)
def realpath(filename,*,strict=_B):'Return the canonical path of the specified filename, eliminating any\nsymbolic links encountered in the path.';filename=os.fspath(filename);path,ok=_joinrealpath(filename[:0],filename,strict,{});return abspath(path)
def _joinrealpath(path,rest,strict,seen):
	if isinstance(path,bytes):sep=_E;curdir=_G;pardir=_I
	else:sep=_C;curdir=_D;pardir=_F
	if isabs(rest):rest=rest[1:];path=sep
	while rest:
		name,_,rest=rest.partition(sep)
		if not name or name==curdir:continue
		if name==pardir:
			if path:
				path,name=split(path)
				if name==pardir:path=join(path,pardir,pardir)
			else:path=pardir
			continue
		newpath=join(path,name)
		try:st=os.lstat(newpath)
		except OSError:
			if strict:raise
			is_link=_B
		else:is_link=stat.S_ISLNK(st.st_mode)
		if not is_link:path=newpath;continue
		if newpath in seen:
			path=seen[newpath]
			if path is not _A:continue
			if strict:os.stat(newpath)
			else:return join(newpath,rest),_B
		seen[newpath]=_A;path,ok=_joinrealpath(path,os.readlink(newpath),strict,seen)
		if not ok:return join(path,rest),_B
		seen[newpath]=path
	return path,_H
supports_unicode_filenames=sys.platform=='darwin'
def relpath(path,start=_A):
	'Return a relative version of a path'
	if not path:raise ValueError('no path specified')
	path=os.fspath(path)
	if isinstance(path,bytes):curdir=_G;sep=_E;pardir=_I
	else:curdir=_D;sep=_C;pardir=_F
	if start is _A:start=curdir
	else:start=os.fspath(start)
	try:
		start_list=[x for x in abspath(start).split(sep)if x];path_list=[x for x in abspath(path).split(sep)if x];i=len(commonprefix([start_list,path_list]));rel_list=[pardir]*(len(start_list)-i)+path_list[i:]
		if not rel_list:return curdir
		return join(*rel_list)
	except(TypeError,AttributeError,BytesWarning,DeprecationWarning):genericpath._check_arg_types(_J,path,start);raise
def commonpath(paths):
	'Given a sequence of path names, returns the longest common sub-path.'
	if not paths:raise ValueError('commonpath() arg is an empty sequence')
	paths=tuple(map(os.fspath,paths))
	if isinstance(paths[0],bytes):sep=_E;curdir=_G
	else:sep=_C;curdir=_D
	try:
		split_paths=[path.split(sep)for path in paths]
		try:isabs,=set(p[:1]==sep for p in paths)
		except ValueError:raise ValueError("Can't mix absolute and relative paths")from _A
		split_paths=[[c for c in s if c and c!=curdir]for s in split_paths];s1=min(split_paths);s2=max(split_paths);common=s1
		for(i,c)in enumerate(s1):
			if c!=s2[i]:common=s1[:i];break
		prefix=sep if isabs else sep[:0];return prefix+sep.join(common)
	except(TypeError,AttributeError):genericpath._check_arg_types(_K,*paths);raise