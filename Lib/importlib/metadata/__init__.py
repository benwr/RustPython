_D='.egg-info'
_C='.dist-info'
_B='module'
_A=None
import os,re,abc,csv,sys,email,pathlib,zipfile,operator,textwrap,warnings,functools,itertools,posixpath,collections
from.import _adapters,_meta
from._collections import FreezableDefaultDict,Pair
from._functools import method_cache,pass_none
from._itertools import always_iterable,unique_everseen
from._meta import PackageMetadata,SimplePath
from contextlib import suppress
from importlib import import_module
from importlib.abc import MetaPathFinder
from itertools import starmap
from typing import List,Mapping,Optional,Union
__all__=['Distribution','DistributionFinder','PackageMetadata','PackageNotFoundError','distribution','distributions','entry_points','files','metadata','packages_distributions','requires','version']
class PackageNotFoundError(ModuleNotFoundError):
	'The package was not found.'
	def __str__(self):return f"No package metadata was found for {self.name}"
	@property
	def name(self):name,=self.args;return name
	@name.setter
	def name(self,value):import sys;sys.stderr.write('set value to PackageNotFoundError ignored\n')
class Sectioned:
	"\n    A simple entry point config parser for performance\n\n    >>> for item in Sectioned.read(Sectioned._sample):\n    ...     print(item)\n    Pair(name='sec1', value='# comments ignored')\n    Pair(name='sec1', value='a = 1')\n    Pair(name='sec1', value='b = 2')\n    Pair(name='sec2', value='a = 2')\n\n    >>> res = Sectioned.section_pairs(Sectioned._sample)\n    >>> item = next(res)\n    >>> item.name\n    'sec1'\n    >>> item.value\n    Pair(name='a', value='1')\n    >>> item = next(res)\n    >>> item.value\n    Pair(name='b', value='2')\n    >>> item = next(res)\n    >>> item.name\n    'sec2'\n    >>> item.value\n    Pair(name='a', value='2')\n    >>> list(res)\n    []\n    ";_sample=textwrap.dedent('\n        [sec1]\n        # comments ignored\n        a = 1\n        b = 2\n\n        [sec2]\n        a = 2\n        ').lstrip()
	@classmethod
	def section_pairs(cls,text):return(section._replace(value=Pair.parse(section.value))for section in cls.read(text,filter_=cls.valid)if section.name is not _A)
	@staticmethod
	def read(text,filter_=_A):
		lines=filter(filter_,map(str.strip,text.splitlines()));name=_A
		for value in lines:
			section_match=value.startswith('[')and value.endswith(']')
			if section_match:name=value.strip('[]');continue
			yield Pair(name,value)
	@staticmethod
	def valid(line):return line and not line.startswith('#')
class DeprecatedTuple:
	"\n    Provide subscript item access for backward compatibility.\n\n    >>> recwarn = getfixture('recwarn')\n    >>> ep = EntryPoint(name='name', value='value', group='group')\n    >>> ep[:]\n    ('name', 'value', 'group')\n    >>> ep[0]\n    'name'\n    >>> len(recwarn)\n    1\n    ";_warn=functools.partial(warnings.warn,'EntryPoint tuple interface is deprecated. Access members by name.',DeprecationWarning,stacklevel=2)
	def __getitem__(self,item):self._warn();return self._key()[item]
class EntryPoint(DeprecatedTuple):
	"An entry point as defined by Python packaging conventions.\n\n    See `the packaging docs on entry points\n    <https://packaging.python.org/specifications/entry-points/>`_\n    for more information.\n\n    >>> ep = EntryPoint(\n    ...     name=None, group=None, value='package.module:attr [extra1, extra2]')\n    >>> ep.module\n    'package.module'\n    >>> ep.attr\n    'attr'\n    >>> ep.extras\n    ['extra1', 'extra2']\n    ";pattern=re.compile('(?P<module>[\\w.]+)\\s*(:\\s*(?P<attr>[\\w.]+)\\s*)?((?P<extras>\\[.*\\])\\s*)?$');"\n    A regular expression describing the syntax for an entry point,\n    which might look like:\n\n        - module\n        - package.module\n        - package.module:attribute\n        - package.module:object.attribute\n        - package.module:attr [extra1, extra2]\n\n    Other combinations are possible as well.\n\n    The expression is lenient about whitespace around the ':',\n    following the attr, and following any extras.\n    ";name:0;value:0;group:0;dist=_A
	def __init__(self,name,value,group):vars(self).update(name=name,value=value,group=group)
	def load(self):'Load the entry point from its definition. If only a module\n        is indicated by the value, return that module. Otherwise,\n        return the named object.\n        ';match=self.pattern.match(self.value);module=import_module(match.group(_B));attrs=filter(_A,(match.group('attr')or'').split('.'));return functools.reduce(getattr,attrs,module)
	@property
	def module(self):match=self.pattern.match(self.value);return match.group(_B)
	@property
	def attr(self):match=self.pattern.match(self.value);return match.group('attr')
	@property
	def extras(self):match=self.pattern.match(self.value);return re.findall('\\w+',match.group('extras')or'')
	def _for(self,dist):vars(self).update(dist=dist);return self
	def __iter__(self):'\n        Supply iter so one may construct dicts of EntryPoints by name.\n        ';msg='Construction of dict of EntryPoints is deprecated in favor of EntryPoints.';warnings.warn(msg,DeprecationWarning);return iter((self.name,self))
	def matches(self,**params):"\n        EntryPoint matches the given parameters.\n\n        >>> ep = EntryPoint(group='foo', name='bar', value='bing:bong [extra1, extra2]')\n        >>> ep.matches(group='foo')\n        True\n        >>> ep.matches(name='bar', value='bing:bong [extra1, extra2]')\n        True\n        >>> ep.matches(group='foo', name='other')\n        False\n        >>> ep.matches()\n        True\n        >>> ep.matches(extras=['extra1', 'extra2'])\n        True\n        >>> ep.matches(module='bing')\n        True\n        >>> ep.matches(attr='bong')\n        True\n        ";attrs=(getattr(self,param)for param in params);return all(map(operator.eq,params.values(),attrs))
	def _key(self):return self.name,self.value,self.group
	def __lt__(self,other):return self._key()<other._key()
	def __eq__(self,other):return self._key()==other._key()
	def __setattr__(self,name,value):raise AttributeError('EntryPoint objects are immutable.')
	def __repr__(self):return f"EntryPoint(name={self.name!r}, value={self.value!r}, group={self.group!r})"
	def __hash__(self):return hash(self._key())
class DeprecatedList(list):
	"\n    Allow an otherwise immutable object to implement mutability\n    for compatibility.\n\n    >>> recwarn = getfixture('recwarn')\n    >>> dl = DeprecatedList(range(3))\n    >>> dl[0] = 1\n    >>> dl.append(3)\n    >>> del dl[3]\n    >>> dl.reverse()\n    >>> dl.sort()\n    >>> dl.extend([4])\n    >>> dl.pop(-1)\n    4\n    >>> dl.remove(1)\n    >>> dl += [5]\n    >>> dl + [6]\n    [1, 2, 5, 6]\n    >>> dl + (6,)\n    [1, 2, 5, 6]\n    >>> dl.insert(0, 0)\n    >>> dl\n    [0, 1, 2, 5]\n    >>> dl == [0, 1, 2, 5]\n    True\n    >>> dl == (0, 1, 2, 5)\n    True\n    >>> len(recwarn)\n    1\n    ";__slots__=();_warn=functools.partial(warnings.warn,'EntryPoints list interface is deprecated. Cast to list if needed.',DeprecationWarning,stacklevel=2)
	def _wrap_deprecated_method(method_name):
		def wrapped(self,*args,**kwargs):self._warn();return getattr(super(),method_name)(*args,**kwargs)
		return method_name,wrapped
	locals().update(map(_wrap_deprecated_method,'__setitem__ __delitem__ append reverse extend pop remove __iadd__ insert sort'.split()))
	def __add__(self,other):
		if not isinstance(other,tuple):self._warn();other=tuple(other)
		return self.__class__(tuple(self)+other)
	def __eq__(self,other):
		if not isinstance(other,tuple):self._warn();other=tuple(other)
		return tuple(self).__eq__(other)
class EntryPoints(DeprecatedList):
	'\n    An immutable collection of selectable EntryPoint objects.\n    ';__slots__=()
	def __getitem__(self,name):
		'\n        Get the EntryPoint in self matching name.\n        '
		if isinstance(name,int):warnings.warn('Accessing entry points by index is deprecated. Cast to tuple if needed.',DeprecationWarning,stacklevel=2);return super().__getitem__(name)
		try:return next(iter(self.select(name=name)))
		except StopIteration:raise KeyError(name)
	def select(self,**params):'\n        Select entry points from self that match the\n        given parameters (typically group and/or name).\n        ';return EntryPoints(ep for ep in self if ep.matches(**params))
	@property
	def names(self):'\n        Return the set of all names of all entry points.\n        ';return{ep.name for ep in self}
	@property
	def groups(self):'\n        Return the set of all groups of all entry points.\n\n        For coverage while SelectableGroups is present.\n        >>> EntryPoints().groups\n        set()\n        ';return{ep.group for ep in self}
	@classmethod
	def _from_text_for(cls,text,dist):return cls(ep._for(dist)for ep in cls._from_text(text))
	@staticmethod
	def _from_text(text):return(EntryPoint(name=item.value.name,value=item.value.value,group=item.name)for item in Sectioned.section_pairs(text or''))
class Deprecated:
	"\n    Compatibility add-in for mapping to indicate that\n    mapping behavior is deprecated.\n\n    >>> recwarn = getfixture('recwarn')\n    >>> class DeprecatedDict(Deprecated, dict): pass\n    >>> dd = DeprecatedDict(foo='bar')\n    >>> dd.get('baz', None)\n    >>> dd['foo']\n    'bar'\n    >>> list(dd)\n    ['foo']\n    >>> list(dd.keys())\n    ['foo']\n    >>> 'foo' in dd\n    True\n    >>> list(dd.values())\n    ['bar']\n    >>> len(recwarn)\n    1\n    ";_warn=functools.partial(warnings.warn,'SelectableGroups dict interface is deprecated. Use select.',DeprecationWarning,stacklevel=2)
	def __getitem__(self,name):self._warn();return super().__getitem__(name)
	def get(self,name,default=_A):self._warn();return super().get(name,default)
	def __iter__(self):self._warn();return super().__iter__()
	def __contains__(self,*args):self._warn();return super().__contains__(*args)
	def keys(self):self._warn();return super().keys()
	def values(self):self._warn();return super().values()
class SelectableGroups(Deprecated,dict):
	'\n    A backward- and forward-compatible result from\n    entry_points that fully implements the dict interface.\n    '
	@classmethod
	def load(cls,eps):by_group=operator.attrgetter('group');ordered=sorted(eps,key=by_group);grouped=itertools.groupby(ordered,by_group);return cls((group,EntryPoints(eps))for(group,eps)in grouped)
	@property
	def _all(self):'\n        Reconstruct a list of all entrypoints from the groups.\n        ';groups=super(Deprecated,self).values();return EntryPoints(itertools.chain.from_iterable(groups))
	@property
	def groups(self):return self._all.groups
	@property
	def names(self):'\n        for coverage:\n        >>> SelectableGroups().names\n        set()\n        ';return self._all.names
	def select(self,**params):
		if not params:return self
		return self._all.select(**params)
class PackagePath(pathlib.PurePosixPath):
	'A reference to a path in a package'
	def read_text(self,encoding='utf-8'):
		with self.locate().open(encoding=encoding)as stream:return stream.read()
	def read_binary(self):
		with self.locate().open('rb')as stream:return stream.read()
	def locate(self):'Return a path-like object for this path';return self.dist.locate_file(self)
class FileHash:
	def __init__(self,spec):self.mode,_,self.value=spec.partition('=')
	def __repr__(self):return f"<FileHash mode: {self.mode} value: {self.value}>"
class Distribution:
	'A Python distribution package.'
	@abc.abstractmethod
	def read_text(self,filename):'Attempt to load metadata file given by the name.\n\n        :param filename: The name of the file in the distribution info.\n        :return: The text if found, otherwise None.\n        '
	@abc.abstractmethod
	def locate_file(self,path):'\n        Given a path to a file in this distribution, return a path\n        to it.\n        '
	@classmethod
	def from_name(cls,name):
		"Return the Distribution for the given package name.\n\n        :param name: The name of the distribution package to search for.\n        :return: The Distribution instance (or subclass thereof) for the named\n            package, if found.\n        :raises PackageNotFoundError: When the named package's distribution\n            metadata cannot be found.\n        :raises ValueError: When an invalid value is supplied for name.\n        "
		if not name:raise ValueError('A distribution name is required.')
		try:return next(cls.discover(name=name))
		except StopIteration:raise PackageNotFoundError(name)
	@classmethod
	def discover(cls,**kwargs):
		'Return an iterable of Distribution objects for all packages.\n\n        Pass a ``context`` or pass keyword arguments for constructing\n        a context.\n\n        :context: A ``DistributionFinder.Context`` object.\n        :return: Iterable of Distribution objects for all packages.\n        ';context=kwargs.pop('context',_A)
		if context and kwargs:raise ValueError('cannot accept context and kwargs')
		context=context or DistributionFinder.Context(**kwargs);return itertools.chain.from_iterable(resolver(context)for resolver in cls._discover_resolvers())
	@staticmethod
	def at(path):'Return a Distribution for the indicated metadata path\n\n        :param path: a string or path-like object\n        :return: a concrete Distribution instance for the path\n        ';return PathDistribution(pathlib.Path(path))
	@staticmethod
	def _discover_resolvers():'Search the meta_path for resolvers.';declared=(getattr(finder,'find_distributions',_A)for finder in sys.meta_path);return filter(_A,declared)
	@property
	def metadata(self):'Return the parsed metadata for this Distribution.\n\n        The returned object will have keys that name the various bits of\n        metadata.  See PEP 566 for details.\n        ';text=self.read_text('METADATA')or self.read_text('PKG-INFO')or self.read_text('');return _adapters.Message(email.message_from_string(text))
	@property
	def name(self):"Return the 'Name' metadata for the distribution package.";return self.metadata['Name']
	@property
	def _normalized_name(self):'Return a normalized version of the name.';return Prepared.normalize(self.name)
	@property
	def version(self):"Return the 'Version' metadata for the distribution package.";return self.metadata['Version']
	@property
	def entry_points(self):return EntryPoints._from_text_for(self.read_text('entry_points.txt'),self)
	@property
	def files(self):
		'Files in this distribution.\n\n        :return: List of PackagePath for this distribution or None\n\n        Result is `None` if the metadata file that enumerates files\n        (i.e. RECORD for dist-info or SOURCES.txt for egg-info) is\n        missing.\n        Result may be empty if the metadata exists but is empty.\n        '
		def make_file(name,hash=_A,size_str=_A):result=PackagePath(name);result.hash=FileHash(hash)if hash else _A;result.size=int(size_str)if size_str else _A;result.dist=self;return result
		@pass_none
		def make_files(lines):return list(starmap(make_file,csv.reader(lines)))
		return make_files(self._read_files_distinfo()or self._read_files_egginfo())
	def _read_files_distinfo(self):'\n        Read the lines of RECORD\n        ';text=self.read_text('RECORD');return text and text.splitlines()
	def _read_files_egginfo(self):'\n        SOURCES.txt might contain literal commas, so wrap each line\n        in quotes.\n        ';text=self.read_text('SOURCES.txt');return text and map('"{}"'.format,text.splitlines())
	@property
	def requires(self):'Generated requirements specified for this Distribution';reqs=self._read_dist_info_reqs()or self._read_egg_info_reqs();return reqs and list(reqs)
	def _read_dist_info_reqs(self):return self.metadata.get_all('Requires-Dist')
	def _read_egg_info_reqs(self):source=self.read_text('requires.txt');return pass_none(self._deps_from_requires_text)(source)
	@classmethod
	def _deps_from_requires_text(cls,source):return cls._convert_egg_info_reqs_to_simple_reqs(Sectioned.read(source))
	@staticmethod
	def _convert_egg_info_reqs_to_simple_reqs(sections):
		"\n        Historically, setuptools would solicit and store 'extra'\n        requirements, including those with environment markers,\n        in separate sections. More modern tools expect each\n        dependency to be defined separately, with any relevant\n        extras and environment markers attached directly to that\n        requirement. This method converts the former to the\n        latter. See _test_deps_from_requires_text for an example.\n        "
		def make_condition(name):return name and f'extra == "{name}"'
		def quoted_marker(section):
			section=section or'';extra,sep,markers=section.partition(':')
			if extra and markers:markers=f"({markers})"
			conditions=list(filter(_A,[markers,make_condition(extra)]));return'; '+' and '.join(conditions)if conditions else''
		def url_req_space(req):'\n            PEP 508 requires a space between the url_spec and the quoted_marker.\n            Ref python/importlib_metadata#357.\n            ';return' '*('@'in req)
		for section in sections:space=url_req_space(section.value);yield section.value+space+quoted_marker(section.name)
class DistributionFinder(MetaPathFinder):
	'\n    A MetaPathFinder capable of discovering installed distributions.\n    '
	class Context:
		'\n        Keyword arguments presented by the caller to\n        ``distributions()`` or ``Distribution.discover()``\n        to narrow the scope of a search for distributions\n        in all DistributionFinders.\n\n        Each DistributionFinder may expect any parameters\n        and should attempt to honor the canonical\n        parameters defined below when appropriate.\n        ';name=_A;'\n        Specific name for which a distribution finder should match.\n        A name of ``None`` matches all distributions.\n        '
		def __init__(self,**kwargs):vars(self).update(kwargs)
		@property
		def path(self):'\n            The sequence of directory path that a distribution finder\n            should search.\n\n            Typically refers to Python installed package paths such as\n            "site-packages" directories and defaults to ``sys.path``.\n            ';return vars(self).get('path',sys.path)
	@abc.abstractmethod
	def find_distributions(self,context=Context()):'\n        Find distributions.\n\n        Return an iterable of all Distribution instances capable of\n        loading the metadata for packages matching the ``context``,\n        a DistributionFinder.Context instance.\n        '
class FastPath:
	"\n    Micro-optimized class for searching a path for\n    children.\n\n    >>> FastPath('').children()\n    ['...']\n    "
	@functools.lru_cache()
	def __new__(cls,root):return super().__new__(cls)
	def __init__(self,root):self.root=root
	def joinpath(self,child):return pathlib.Path(self.root,child)
	def children(self):
		with suppress(Exception):return os.listdir(self.root or'.')
		with suppress(Exception):return self.zip_children()
		return[]
	def zip_children(self):zip_path=zipfile.Path(self.root);names=zip_path.root.namelist();self.joinpath=zip_path.joinpath;return dict.fromkeys(child.split(posixpath.sep,1)[0]for child in names)
	def search(self,name):return self.lookup(self.mtime).search(name)
	@property
	def mtime(self):
		with suppress(OSError):return os.stat(self.root).st_mtime
		self.lookup.cache_clear()
	@method_cache
	def lookup(self,mtime):return Lookup(self)
class Lookup:
	def __init__(self,path):
		base=os.path.basename(path.root).lower();base_is_egg=base.endswith('.egg');self.infos=FreezableDefaultDict(list);self.eggs=FreezableDefaultDict(list)
		for child in path.children():
			low=child.lower()
			if low.endswith((_C,_D)):name=low.rpartition('.')[0].partition('-')[0];normalized=Prepared.normalize(name);self.infos[normalized].append(path.joinpath(child))
			elif base_is_egg and low=='egg-info':name=base.rpartition('.')[0].partition('-')[0];legacy_normalized=Prepared.legacy_normalize(name);self.eggs[legacy_normalized].append(path.joinpath(child))
		self.infos.freeze();self.eggs.freeze()
	def search(self,prepared):infos=self.infos[prepared.normalized]if prepared else itertools.chain.from_iterable(self.infos.values());eggs=self.eggs[prepared.legacy_normalized]if prepared else itertools.chain.from_iterable(self.eggs.values());return itertools.chain(infos,eggs)
class Prepared:
	'\n    A prepared search for metadata on a possibly-named package.\n    ';normalized=_A;legacy_normalized=_A
	def __init__(self,name):
		self.name=name
		if name is _A:return
		self.normalized=self.normalize(name);self.legacy_normalized=self.legacy_normalize(name)
	@staticmethod
	def normalize(name):'\n        PEP 503 normalization plus dashes as underscores.\n        ';return re.sub('[-_.]+','-',name).lower().replace('-','_')
	@staticmethod
	def legacy_normalize(name):'\n        Normalize the package name as found in the convention in\n        older packaging tools versions and specs.\n        ';return name.lower().replace('-','_')
	def __bool__(self):return bool(self.name)
class MetadataPathFinder(DistributionFinder):
	@classmethod
	def find_distributions(cls,context=DistributionFinder.Context()):'\n        Find distributions.\n\n        Return an iterable of all Distribution instances capable of\n        loading the metadata for packages matching ``context.name``\n        (or all names if ``None`` indicated) along the paths in the list\n        of directories ``context.path``.\n        ';found=cls._search_paths(context.name,context.path);return map(PathDistribution,found)
	@classmethod
	def _search_paths(cls,name,paths):'Find metadata directories in paths heuristically.';prepared=Prepared(name);return itertools.chain.from_iterable(path.search(prepared)for path in map(FastPath,paths))
	def invalidate_caches(cls):FastPath.__new__.cache_clear()
class PathDistribution(Distribution):
	def __init__(self,path):'Construct a distribution.\n\n        :param path: SimplePath indicating the metadata directory.\n        ';self._path=path
	def read_text(self,filename):
		with suppress(FileNotFoundError,IsADirectoryError,KeyError,NotADirectoryError,PermissionError):return self._path.joinpath(filename).read_text(encoding='utf-8')
	read_text.__doc__=Distribution.read_text.__doc__
	def locate_file(self,path):return self._path.parent/path
	@property
	def _normalized_name(self):'\n        Performance optimization: where possible, resolve the\n        normalized name from the file system path.\n        ';stem=os.path.basename(str(self._path));return pass_none(Prepared.normalize)(self._name_from_stem(stem))or super()._normalized_name
	@staticmethod
	def _name_from_stem(stem):
		"\n        >>> PathDistribution._name_from_stem('foo-3.0.egg-info')\n        'foo'\n        >>> PathDistribution._name_from_stem('CherryPy-3.0.dist-info')\n        'CherryPy'\n        >>> PathDistribution._name_from_stem('face.egg-info')\n        'face'\n        >>> PathDistribution._name_from_stem('foo.bar')\n        ";filename,ext=os.path.splitext(stem)
		if ext not in(_C,_D):return
		name,sep,rest=filename.partition('-');return name
def distribution(distribution_name):'Get the ``Distribution`` instance for the named package.\n\n    :param distribution_name: The name of the distribution package as a string.\n    :return: A ``Distribution`` instance (or subclass thereof).\n    ';return Distribution.from_name(distribution_name)
def distributions(**kwargs):'Get all ``Distribution`` instances in the current environment.\n\n    :return: An iterable of ``Distribution`` instances.\n    ';return Distribution.discover(**kwargs)
def metadata(distribution_name):'Get the metadata for the named package.\n\n    :param distribution_name: The name of the distribution package to query.\n    :return: A PackageMetadata containing the parsed metadata.\n    ';return Distribution.from_name(distribution_name).metadata
def version(distribution_name):'Get the version string for the named package.\n\n    :param distribution_name: The name of the distribution package to query.\n    :return: The version string for the package as defined in the package\'s\n        "Version" metadata key.\n    ';return distribution(distribution_name).version
_unique=functools.partial(unique_everseen,key=operator.attrgetter('_normalized_name'))
'\nWrapper for ``distributions`` to return unique distributions by name.\n'
def entry_points(**params):'Return EntryPoint objects for all installed packages.\n\n    Pass selection parameters (group or name) to filter the\n    result to entry points matching those properties (see\n    EntryPoints.select()).\n\n    For compatibility, returns ``SelectableGroups`` object unless\n    selection parameters are supplied. In the future, this function\n    will return ``EntryPoints`` instead of ``SelectableGroups``\n    even when no selection parameters are supplied.\n\n    For maximum future compatibility, pass selection parameters\n    or invoke ``.select`` with parameters on the result.\n\n    :return: EntryPoints or SelectableGroups for all installed packages.\n    ';eps=itertools.chain.from_iterable(dist.entry_points for dist in _unique(distributions()));return SelectableGroups.load(eps).select(**params)
def files(distribution_name):'Return a list of files for the named package.\n\n    :param distribution_name: The name of the distribution package to query.\n    :return: List of files composing the distribution.\n    ';return distribution(distribution_name).files
def requires(distribution_name):'\n    Return a list of requirements for the named package.\n\n    :return: An iterator of requirements, suitable for\n        packaging.requirement.Requirement.\n    ';return distribution(distribution_name).requires
def packages_distributions():
	'\n    Return a mapping of top-level packages to their\n    distributions.\n\n    >>> import collections.abc\n    >>> pkgs = packages_distributions()\n    >>> all(isinstance(dist, collections.abc.Sequence) for dist in pkgs.values())\n    True\n    ';pkg_to_dist=collections.defaultdict(list)
	for dist in distributions():
		for pkg in _top_level_declared(dist)or _top_level_inferred(dist):pkg_to_dist[pkg].append(dist.metadata['Name'])
	return dict(pkg_to_dist)
def _top_level_declared(dist):return(dist.read_text('top_level.txt')or'').split()
def _top_level_inferred(dist):return{f.parts[0]if len(f.parts)>1 else f.with_suffix('').name for f in always_iterable(dist.files)if f.suffix=='.py'}