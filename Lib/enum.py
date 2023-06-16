_O='__module__'
_N='__class__'
_M="unsupported operand type(s) for 'in': '%s' and '%s'"
_L='%s.%s'
_K='<%s.%s: %r>'
_J='%r is not a valid %s'
_I='__new__'
_H='_order_'
_G=False
_F='__doc__'
_E=True
_D='_generate_next_value_'
_C='_ignore_'
_B='_'
_A=None
import sys
from types import MappingProxyType,DynamicClassAttribute
__all__=['EnumMeta','Enum','IntEnum','Flag','IntFlag','auto','unique']
def _is_descriptor(obj):'\n    Returns True if obj is a descriptor, False otherwise.\n    ';return hasattr(obj,'__get__')or hasattr(obj,'__set__')or hasattr(obj,'__delete__')
def _is_dunder(name):'\n    Returns True if a __dunder__ name, False otherwise.\n    ';return len(name)>4 and name[:2]==name[-2:]=='__'and name[2]!=_B and name[-3]!=_B
def _is_sunder(name):'\n    Returns True if a _sunder_ name, False otherwise.\n    ';return len(name)>2 and name[0]==name[-1]==_B and name[1:2]!=_B and name[-2:-1]!=_B
def _make_class_unpicklable(cls):
	'\n    Make the given class un-picklable.\n    '
	def _break_on_call_reduce(self,proto):raise TypeError('%r cannot be pickled'%self)
	cls.__reduce_ex__=_break_on_call_reduce;cls.__module__='<unknown>'
_auto_null=object()
class auto:'\n    Instances are replaced with an appropriate value in Enum class suites.\n    ';value=_auto_null
class _EnumDict(dict):
	'\n    Track enum member order and ensure member names are not reused.\n\n    EnumMeta will use the names found in self._member_names as the\n    enumeration member names.\n    '
	def __init__(self):super().__init__();self._member_names=[];self._last_values=[];self._ignore=[];self._auto_called=_G
	def __setitem__(self,key,value):
		'\n        Changes anything not dundered or not a descriptor.\n\n        If an enum member name is used twice, an error is raised; duplicate\n        values are not checked for.\n\n        Single underscore (sunder) names are reserved.\n        '
		if _is_sunder(key):
			if key not in(_H,'_create_pseudo_member_',_D,'_missing_',_C):raise ValueError('_names_ are reserved for future Enum use')
			if key==_D:
				if self._auto_called:raise TypeError('_generate_next_value_ must be defined before members')
				setattr(self,'_generate_next_value',value)
			elif key==_C:
				if isinstance(value,str):value=value.replace(',',' ').split()
				else:value=list(value)
				self._ignore=value;already=set(value)&set(self._member_names)
				if already:raise ValueError('_ignore_ cannot specify already set names: %r'%(already,))
		elif _is_dunder(key):
			if key=='__order__':key=_H
		elif key in self._member_names:raise TypeError('Attempted to reuse key: %r'%key)
		elif key in self._ignore:0
		elif not _is_descriptor(value):
			if key in self:raise TypeError('%r already defined as: %r'%(key,self[key]))
			if isinstance(value,auto):
				if value.value==_auto_null:value.value=self._generate_next_value(key,1,len(self._member_names),self._last_values[:]);self._auto_called=_E
				value=value.value
			self._member_names.append(key);self._last_values.append(value)
		super().__setitem__(key,value)
Enum=_A
class EnumMeta(type):
	'\n    Metaclass for Enum\n    '
	@classmethod
	def __prepare__(metacls,cls,bases):
		metacls._check_for_existing_members(cls,bases);enum_dict=_EnumDict();member_type,first_enum=metacls._get_mixins_(cls,bases)
		if first_enum is not _A:enum_dict[_D]=getattr(first_enum,_D,_A)
		return enum_dict
	def __new__(metacls,cls,bases,classdict):
		B='_value_';A='__reduce_ex__';classdict.setdefault(_C,[]).append(_C);ignore=classdict[_C]
		for key in ignore:classdict.pop(key,_A)
		member_type,first_enum=metacls._get_mixins_(cls,bases);__new__,save_new,use_args=metacls._find_new_(classdict,member_type,first_enum);enum_members={k:classdict[k]for k in classdict._member_names}
		for name in classdict._member_names:del classdict[name]
		_order_=classdict.pop(_H,_A);invalid_names=set(enum_members)&{'mro',''}
		if invalid_names:raise ValueError('Invalid enum member name: {0}'.format(','.join(invalid_names)))
		if _F not in classdict:classdict[_F]='An enumeration.'
		enum_class=super().__new__(metacls,cls,bases,classdict);enum_class._member_names_=[];enum_class._member_map_={};enum_class._member_type_=member_type;dynamic_attributes={k for c in enum_class.mro()for(k,v)in c.__dict__.items()if isinstance(v,DynamicClassAttribute)};enum_class._value2member_map_={}
		if A not in classdict:
			if member_type is not object:
				methods='__getnewargs_ex__','__getnewargs__',A,'__reduce__'
				if not any(m in member_type.__dict__ for m in methods):_make_class_unpicklable(enum_class)
		for member_name in classdict._member_names:
			value=enum_members[member_name]
			if not isinstance(value,tuple):args=value,
			else:args=value
			if member_type is tuple:args=args,
			if not use_args:
				enum_member=__new__(enum_class)
				if not hasattr(enum_member,B):enum_member._value_=value
			else:
				enum_member=__new__(enum_class,*args)
				if not hasattr(enum_member,B):
					if member_type is object:enum_member._value_=value
					else:enum_member._value_=member_type(*args)
			value=enum_member._value_;enum_member._name_=member_name;enum_member.__objclass__=enum_class;enum_member.__init__(*args)
			for(name,canonical_member)in enum_class._member_map_.items():
				if canonical_member._value_==enum_member._value_:enum_member=canonical_member;break
			else:enum_class._member_names_.append(member_name)
			if member_name not in dynamic_attributes:setattr(enum_class,member_name,enum_member)
			enum_class._member_map_[member_name]=enum_member
			try:enum_class._value2member_map_[value]=enum_member
			except TypeError:pass
		for name in('__repr__','__str__','__format__',A):
			if name in classdict:continue
			class_method=getattr(enum_class,name);obj_method=getattr(member_type,name,_A);enum_method=getattr(first_enum,name,_A)
			if obj_method is not _A and obj_method is class_method:setattr(enum_class,name,enum_method)
		if Enum is not _A:
			if save_new:enum_class.__new_member__=__new__
			enum_class.__new__=Enum.__new__
		if _order_ is not _A:
			if isinstance(_order_,str):_order_=_order_.replace(',',' ').split()
			if _order_!=enum_class._member_names_:raise TypeError('member order does not match _order_')
		return enum_class
	def __bool__(self):'\n        classes/types should always be True.\n        ';return _E
	def __call__(cls,value,names=_A,*,module=_A,qualname=_A,type=_A,start=1):
		"\n        Either returns an existing member, or creates a new enum class.\n\n        This method is used both when an enum class is given a value to match\n        to an enumeration member (i.e. Color(3)) and for the functional API\n        (i.e. Color = Enum('Color', names='RED GREEN BLUE')).\n\n        When used for the functional API:\n\n        `value` will be the name of the new class.\n\n        `names` should be either a string of white-space/comma delimited names\n        (values will start at `start`), or an iterator/mapping of name, value pairs.\n\n        `module` should be set to the module this class is being created in;\n        if it is not set, an attempt to find that module will be made, but if\n        it fails the class will not be picklable.\n\n        `qualname` should be set to the actual location this class can be found\n        at in its module; by default it is set to the global scope.  If this is\n        not correct, unpickling will fail in some circumstances.\n\n        `type`, if set, will be mixed in as the first base class.\n        "
		if names is _A:return cls.__new__(cls,value)
		return cls._create_(value,names,module=module,qualname=qualname,type=type,start=start)
	def __contains__(cls,member):
		if not isinstance(member,Enum):raise TypeError(_M%(type(member).__qualname__,cls.__class__.__qualname__))
		return isinstance(member,cls)and member._name_ in cls._member_map_
	def __delattr__(cls,attr):
		if attr in cls._member_map_:raise AttributeError('%s: cannot delete Enum member.'%cls.__name__)
		super().__delattr__(attr)
	def __dir__(self):return[_N,_F,'__members__',_O]+self._member_names_
	def __getattr__(cls,name):
		"\n        Return the enum member matching `name`\n\n        We use __getattr__ instead of descriptors or inserting into the enum\n        class' __dict__ in order to support `name` and `value` being both\n        properties for enum members (which live in the class' __dict__) and\n        enum members themselves.\n        "
		if _is_dunder(name):raise AttributeError(name)
		try:return cls._member_map_[name]
		except KeyError:raise AttributeError(name)from _A
	def __getitem__(cls,name):return cls._member_map_[name]
	def __iter__(cls):'\n        Returns members in definition order.\n        ';return(cls._member_map_[name]for name in cls._member_names_)
	def __len__(cls):return len(cls._member_names_)
	@property
	def __members__(cls):'\n        Returns a mapping of member name->value.\n\n        This mapping lists all enum members, including aliases. Note that this\n        is a read-only view of the internal mapping.\n        ';return MappingProxyType(cls._member_map_)
	def __repr__(cls):return'<enum %r>'%cls.__name__
	def __reversed__(cls):'\n        Returns members in reverse definition order.\n        ';return(cls._member_map_[name]for name in reversed(cls._member_names_))
	def __setattr__(cls,name,value):
		'\n        Block attempts to reassign Enum members.\n\n        A simple assignment to the class namespace only changes one of the\n        several possible ways to get an Enum member from the Enum class,\n        resulting in an inconsistent Enumeration.\n        ';member_map=cls.__dict__.get('_member_map_',{})
		if name in member_map:raise AttributeError('Cannot reassign members.')
		super().__setattr__(name,value)
	def _create_(cls,class_name,names,*,module=_A,qualname=_A,type=_A,start=1):
		'\n        Convenience method to create a new Enum class.\n\n        `names` can be:\n\n        * A string containing member names, separated either with spaces or\n          commas.  Values are incremented by 1 from `start`.\n        * An iterable of member names.  Values are incremented by 1 from `start`.\n        * An iterable of (member name, value) pairs.\n        * A mapping of member name -> value pairs.\n        ';metacls=cls.__class__;bases=(cls,)if type is _A else(type,cls);_,first_enum=cls._get_mixins_(cls,bases);classdict=metacls.__prepare__(class_name,bases)
		if isinstance(names,str):names=names.replace(',',' ').split()
		if isinstance(names,(tuple,list))and names and isinstance(names[0],str):
			original_names,names=names,[];last_values=[]
			for(count,name)in enumerate(original_names):value=first_enum._generate_next_value_(name,start,count,last_values[:]);last_values.append(value);names.append((name,value))
		for item in names:
			if isinstance(item,str):member_name,member_value=item,names[item]
			else:member_name,member_value=item
			classdict[member_name]=member_value
		enum_class=metacls.__new__(metacls,class_name,bases,classdict)
		if module is _A:
			try:module=sys._getframe(2).f_globals['__name__']
			except(AttributeError,ValueError,KeyError)as exc:pass
		if module is _A:_make_class_unpicklable(enum_class)
		else:enum_class.__module__=module
		if qualname is not _A:enum_class.__qualname__=qualname
		return enum_class
	def _convert_(cls,name,module,filter,source=_A):
		'\n        Create a new Enum subclass that replaces a collection of global constants\n        ';module_globals=vars(sys.modules[module])
		if source:source=vars(source)
		else:source=module_globals
		members=[(name,value)for(name,value)in source.items()if filter(name)]
		try:members.sort(key=lambda t:(t[1],t[0]))
		except TypeError:members.sort(key=lambda t:t[0])
		cls=cls(name,members,module=module);cls.__reduce_ex__=_reduce_ex_by_name;module_globals.update(cls.__members__);module_globals[name]=cls;return cls
	def _convert(cls,*args,**kwargs):import warnings;warnings.warn('_convert is deprecated and will be removed in 3.9, use _convert_ instead.',DeprecationWarning,stacklevel=2);return cls._convert_(*args,**kwargs)
	@staticmethod
	def _check_for_existing_members(class_name,bases):
		for chain in bases:
			for base in chain.__mro__:
				if issubclass(base,Enum)and base._member_names_:raise TypeError('%s: cannot extend enumeration %r'%(class_name,base.__name__))
	@staticmethod
	def _get_mixins_(class_name,bases):
		'\n        Returns the type for creating enum members, and the first inherited\n        enum class.\n\n        bases: the tuple of bases that was given to __new__\n        '
		if not bases:return object,Enum
		def _find_data_type(bases):
			data_types=[]
			for chain in bases:
				candidate=_A
				for base in chain.__mro__:
					if base is object:continue
					elif issubclass(base,Enum):
						if base._member_type_ is not object:data_types.append(base._member_type_);break
					elif _I in base.__dict__:
						if issubclass(base,Enum):continue
						data_types.append(candidate or base);break
					else:candidate=base
			if len(data_types)>1:raise TypeError('%r: too many data types: %r'%(class_name,data_types))
			elif data_types:return data_types[0]
			else:return
		first_enum=bases[-1]
		if not issubclass(first_enum,Enum):raise TypeError('new enumerations should be created as `EnumName([mixin_type, ...] [data_type,] enum_type)`')
		member_type=_find_data_type(bases)or object
		if first_enum._member_names_:raise TypeError('Cannot extend enumerations')
		return member_type,first_enum
	@staticmethod
	def _find_new_(classdict,member_type,first_enum):
		'\n        Returns the __new__ to be used for creating the enum members.\n\n        classdict: the class dictionary given to __new__\n        member_type: the data type whose __new__ will be used by default\n        first_enum: enumeration to check for an overriding __new__\n        ';__new__=classdict.get(_I,_A);save_new=__new__ is not _A
		if __new__ is _A:
			for method in('__new_member__',_I):
				for possible in(member_type,first_enum):
					target=getattr(possible,method,_A)
					if target not in{_A,_A.__new__,object.__new__,Enum.__new__}:__new__=target;break
				if __new__ is not _A:break
			else:__new__=object.__new__
		if __new__ is object.__new__:use_args=_G
		else:use_args=_E
		return __new__,save_new,use_args
class Enum(metaclass=EnumMeta):
	'\n    Generic enumeration.\n\n    Derive from this class to define new enumerations.\n    '
	def __new__(cls,value):
		if type(value)is cls:return value
		try:return cls._value2member_map_[value]
		except KeyError:pass
		except TypeError:
			for member in cls._member_map_.values():
				if member._value_==value:return member
		try:exc=_A;result=cls._missing_(value)
		except Exception as e:exc=e;result=_A
		if isinstance(result,cls):return result
		else:
			ve_exc=ValueError(_J%(value,cls.__name__))
			if result is _A and exc is _A:raise ve_exc
			elif exc is _A:exc=TypeError('error in %s._missing_: returned %r instead of None or a valid member'%(cls.__name__,result))
			exc.__context__=ve_exc;raise exc
	def _generate_next_value_(name,start,count,last_values):
		'\n        Generate the next value when not given.\n\n        name: the name of the member\n        start: the initial start value or None\n        count: the number of existing members\n        last_value: the last value assigned or None\n        '
		for last_value in reversed(last_values):
			try:return last_value+1
			except TypeError:pass
		else:return start
	@classmethod
	def _missing_(cls,value):0
	def __repr__(self):return _K%(self.__class__.__name__,self._name_,self._value_)
	def __str__(self):return _L%(self.__class__.__name__,self._name_)
	def __dir__(self):'\n        Returns all members and all public methods\n        ';added_behavior=[m for cls in self.__class__.mro()for m in cls.__dict__ if m[0]!=_B and m not in self._member_map_]+[m for m in self.__dict__ if m[0]!=_B];return[_N,_F,_O]+added_behavior
	def __format__(self,format_spec):
		'\n        Returns format using actual value type unless __str__ has been overridden.\n        ';str_overridden=type(self).__str__ not in(Enum.__str__,Flag.__str__)
		if self._member_type_ is object or str_overridden:cls=str;val=str(self)
		else:cls=self._member_type_;val=self._value_
		return cls.__format__(val,format_spec)
	def __hash__(self):return hash(self._name_)
	def __reduce_ex__(self,proto):return self.__class__,(self._value_,)
	@DynamicClassAttribute
	def name(self):'The name of the Enum member.';return self._name_
	@DynamicClassAttribute
	def value(self):'The value of the Enum member.';return self._value_
class IntEnum(int,Enum):'Enum where members are also (and must be) ints'
def _reduce_ex_by_name(self,proto):return self.name
class Flag(Enum):
	'\n    Support for flags\n    '
	def _generate_next_value_(name,start,count,last_values):
		'\n        Generate the next value when not given.\n\n        name: the name of the member\n        start: the initial start value or None\n        count: the number of existing members\n        last_value: the last value assigned or None\n        '
		if not count:return start if start is not _A else 1
		for last_value in reversed(last_values):
			try:high_bit=_high_bit(last_value);break
			except Exception:raise TypeError('Invalid Flag value: %r'%last_value)from _A
		return 2**(high_bit+1)
	@classmethod
	def _missing_(cls,value):
		'\n        Returns member (possibly creating it) if one can be found for value.\n        ';original_value=value
		if value<0:value=~value
		possible_member=cls._create_pseudo_member_(value)
		if original_value<0:possible_member=~possible_member
		return possible_member
	@classmethod
	def _create_pseudo_member_(cls,value):
		'\n        Create a composite member iff value contains only members.\n        ';pseudo_member=cls._value2member_map_.get(value,_A)
		if pseudo_member is _A:
			_,extra_flags=_decompose(cls,value)
			if extra_flags:raise ValueError(_J%(value,cls.__name__))
			pseudo_member=object.__new__(cls);pseudo_member._name_=_A;pseudo_member._value_=value;pseudo_member=cls._value2member_map_.setdefault(value,pseudo_member)
		return pseudo_member
	def __contains__(self,other):
		'\n        Returns True if self has at least the same flags set as other.\n        '
		if not isinstance(other,self.__class__):raise TypeError(_M%(type(other).__qualname__,self.__class__.__qualname__))
		return other._value_&self._value_==other._value_
	def __repr__(self):
		cls=self.__class__
		if self._name_ is not _A:return _K%(cls.__name__,self._name_,self._value_)
		members,uncovered=_decompose(cls,self._value_);return _K%(cls.__name__,'|'.join([str(m._name_ or m._value_)for m in members]),self._value_)
	def __str__(self):
		cls=self.__class__
		if self._name_ is not _A:return _L%(cls.__name__,self._name_)
		members,uncovered=_decompose(cls,self._value_)
		if len(members)==1 and members[0]._name_ is _A:return'%s.%r'%(cls.__name__,members[0]._value_)
		else:return _L%(cls.__name__,'|'.join([str(m._name_ or m._value_)for m in members]))
	def __bool__(self):return bool(self._value_)
	def __or__(self,other):
		if not isinstance(other,self.__class__):return NotImplemented
		return self.__class__(self._value_|other._value_)
	def __and__(self,other):
		if not isinstance(other,self.__class__):return NotImplemented
		return self.__class__(self._value_&other._value_)
	def __xor__(self,other):
		if not isinstance(other,self.__class__):return NotImplemented
		return self.__class__(self._value_^other._value_)
	def __invert__(self):
		members,uncovered=_decompose(self.__class__,self._value_);inverted=self.__class__(0)
		for m in self.__class__:
			if m not in members and not m._value_&self._value_:inverted=inverted|m
		return self.__class__(inverted)
class IntFlag(int,Flag):
	'\n    Support for integer-based Flags\n    '
	@classmethod
	def _missing_(cls,value):
		'\n        Returns member (possibly creating it) if one can be found for value.\n        '
		if not isinstance(value,int):raise ValueError(_J%(value,cls.__name__))
		new_member=cls._create_pseudo_member_(value);return new_member
	@classmethod
	def _create_pseudo_member_(cls,value):
		'\n        Create a composite member iff value contains only members.\n        ';pseudo_member=cls._value2member_map_.get(value,_A)
		if pseudo_member is _A:
			need_to_create=[value];_,extra_flags=_decompose(cls,value)
			while extra_flags:
				bit=_high_bit(extra_flags);flag_value=2**bit
				if flag_value not in cls._value2member_map_ and flag_value not in need_to_create:need_to_create.append(flag_value)
				if extra_flags==-flag_value:extra_flags=0
				else:extra_flags^=flag_value
			for value in reversed(need_to_create):pseudo_member=int.__new__(cls,value);pseudo_member._name_=_A;pseudo_member._value_=value;pseudo_member=cls._value2member_map_.setdefault(value,pseudo_member)
		return pseudo_member
	def __or__(self,other):
		if not isinstance(other,(self.__class__,int)):return NotImplemented
		result=self.__class__(self._value_|self.__class__(other)._value_);return result
	def __and__(self,other):
		if not isinstance(other,(self.__class__,int)):return NotImplemented
		return self.__class__(self._value_&self.__class__(other)._value_)
	def __xor__(self,other):
		if not isinstance(other,(self.__class__,int)):return NotImplemented
		return self.__class__(self._value_^self.__class__(other)._value_)
	__ror__=__or__;__rand__=__and__;__rxor__=__xor__
	def __invert__(self):result=self.__class__(~self._value_);return result
def _high_bit(value):'\n    returns index of highest bit, or -1 if value is zero or negative\n    ';return value.bit_length()-1
def unique(enumeration):
	'\n    Class decorator for enumerations ensuring unique member values.\n    ';duplicates=[]
	for(name,member)in enumeration.__members__.items():
		if name!=member.name:duplicates.append((name,member.name))
	if duplicates:alias_details=', '.join(['%s -> %s'%(alias,name)for(alias,name)in duplicates]);raise ValueError('duplicate values found in %r: %s'%(enumeration,alias_details))
	return enumeration
def _decompose(flag,value):
	'\n    Extract all members from the value.\n    ';not_covered=value;negative=value<0
	if negative:flags_to_check=[(m,v)for(v,m)in list(flag._value2member_map_.items())if m.name is not _A]
	else:flags_to_check=[(m,v)for(v,m)in list(flag._value2member_map_.items())if m.name is not _A or _power_of_two(v)]
	members=[]
	for(member,member_value)in flags_to_check:
		if member_value and member_value&value==member_value:members.append(member);not_covered&=~member_value
	if not members and value in flag._value2member_map_:members.append(flag._value2member_map_[value])
	members.sort(key=lambda m:m._value_,reverse=_E)
	if len(members)>1 and members[0].value==value:members.pop(0)
	return members,not_covered
def _power_of_two(value):
	if value<1:return _G
	return value==2**_high_bit(value)