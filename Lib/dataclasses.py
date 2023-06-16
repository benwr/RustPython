_M='_fields'
_L='__annotations__'
_K='__hash__'
_J='__repr__'
_I='__init__'
_H='MISSING'
_G='FrozenInstanceError'
_F='other'
_E='name'
_D='self'
_C=None
_B=False
_A=True
import re,sys,copy,types,inspect,keyword,builtins,functools,abc,_thread
from types import FunctionType,GenericAlias
__all__=['dataclass','field','Field',_G,'InitVar','KW_ONLY',_H,'fields','asdict','astuple','make_dataclass','replace','is_dataclass']
class FrozenInstanceError(AttributeError):0
class _HAS_DEFAULT_FACTORY_CLASS:
	def __repr__(self):return'<factory>'
_HAS_DEFAULT_FACTORY=_HAS_DEFAULT_FACTORY_CLASS()
class _MISSING_TYPE:0
MISSING=_MISSING_TYPE()
class _KW_ONLY_TYPE:0
KW_ONLY=_KW_ONLY_TYPE()
_EMPTY_METADATA=types.MappingProxyType({})
class _FIELD_BASE:
	def __init__(self,name):self.name=name
	def __repr__(self):return self.name
_FIELD=_FIELD_BASE('_FIELD')
_FIELD_CLASSVAR=_FIELD_BASE('_FIELD_CLASSVAR')
_FIELD_INITVAR=_FIELD_BASE('_FIELD_INITVAR')
_FIELDS='__dataclass_fields__'
_PARAMS='__dataclass_params__'
_POST_INIT_NAME='__post_init__'
_MODULE_IDENTIFIER_RE=re.compile('^(?:\\s*(\\w+)\\s*\\.)?\\s*(\\w+)')
class InitVar:
	__slots__='type',
	def __init__(self,type):self.type=type
	def __repr__(self):
		if isinstance(self.type,type)and not isinstance(self.type,GenericAlias):type_name=self.type.__name__
		else:type_name=repr(self.type)
		return f"dataclasses.InitVar[{type_name}]"
	def __class_getitem__(cls,type):return InitVar(type)
class Field:
	__slots__=_E,'type','default','default_factory','repr','hash','init','compare','metadata','kw_only','_field_type'
	def __init__(self,default,default_factory,init,repr,hash,compare,metadata,kw_only):self.name=_C;self.type=_C;self.default=default;self.default_factory=default_factory;self.init=init;self.repr=repr;self.hash=hash;self.compare=compare;self.metadata=_EMPTY_METADATA if metadata is _C else types.MappingProxyType(metadata);self.kw_only=kw_only;self._field_type=_C
	def __repr__(self):return f"Field(name={self.name!r},type={self.type!r},default={self.default!r},default_factory={self.default_factory!r},init={self.init!r},repr={self.repr!r},hash={self.hash!r},compare={self.compare!r},metadata={self.metadata!r},kw_only={self.kw_only!r},_field_type={self._field_type})"
	def __set_name__(self,owner,name):
		func=getattr(type(self.default),'__set_name__',_C)
		if func:func(self.default,owner,name)
	__class_getitem__=classmethod(GenericAlias)
class _DataclassParams:
	__slots__='init','repr','eq','order','unsafe_hash','frozen'
	def __init__(self,init,repr,eq,order,unsafe_hash,frozen):self.init=init;self.repr=repr;self.eq=eq;self.order=order;self.unsafe_hash=unsafe_hash;self.frozen=frozen
	def __repr__(self):return f"_DataclassParams(init={self.init!r},repr={self.repr!r},eq={self.eq!r},order={self.order!r},unsafe_hash={self.unsafe_hash!r},frozen={self.frozen!r})"
def field(*,default=MISSING,default_factory=MISSING,init=_A,repr=_A,hash=_C,compare=_A,metadata=_C,kw_only=MISSING):
	"Return an object to identify dataclass fields.\n\n    default is the default value of the field.  default_factory is a\n    0-argument function called to initialize a field's value.  If init\n    is true, the field will be a parameter to the class's __init__()\n    function.  If repr is true, the field will be included in the\n    object's repr().  If hash is true, the field will be included in the\n    object's hash().  If compare is true, the field will be used in\n    comparison functions.  metadata, if specified, must be a mapping\n    which is stored but not otherwise examined by dataclass.  If kw_only\n    is true, the field will become a keyword-only parameter to\n    __init__().\n\n    It is an error to specify both default and default_factory.\n    "
	if default is not MISSING and default_factory is not MISSING:raise ValueError('cannot specify both default and default_factory')
	return Field(default,default_factory,init,repr,hash,compare,metadata,kw_only)
def _fields_in_init_order(fields):return tuple(f for f in fields if f.init and not f.kw_only),tuple(f for f in fields if f.init and f.kw_only)
def _tuple_str(obj_name,fields):
	if not fields:return'()'
	return f"({','.join([f'{obj_name}.{f.name}'for f in fields])},)"
def _recursive_repr(user_function):
	repr_running=set()
	@functools.wraps(user_function)
	def wrapper(self):
		key=id(self),_thread.get_ident()
		if key in repr_running:return'...'
		repr_running.add(key)
		try:result=user_function(self)
		finally:repr_running.discard(key)
		return result
	return wrapper
def _create_fn(name,args,body,*,globals=_C,locals=_C,return_type=MISSING):
	if locals is _C:locals={}
	return_annotation=''
	if return_type is not MISSING:locals['_return_type']=return_type;return_annotation='->_return_type'
	args=','.join(args);body='\n'.join(f"  {b}"for b in body);txt=f" def {name}({args}){return_annotation}:\n{body}";local_vars=', '.join(locals.keys());txt=f"def __create_fn__({local_vars}):\n{txt}\n return {name}";ns={};exec(txt,globals,ns);return ns['__create_fn__'](**locals)
def _field_assign(frozen,name,value,self_name):
	if frozen:return f"__dataclass_builtins_object__.__setattr__({self_name},{name!r},{value})"
	return f"{self_name}.{name}={value}"
def _field_init(f,frozen,globals,self_name,slots):
	default_name=f"_dflt_{f.name}"
	if f.default_factory is not MISSING:
		if f.init:globals[default_name]=f.default_factory;value=f"{default_name}() if {f.name} is _HAS_DEFAULT_FACTORY else {f.name}"
		else:globals[default_name]=f.default_factory;value=f"{default_name}()"
	elif f.init:
		if f.default is MISSING:value=f.name
		elif f.default is not MISSING:globals[default_name]=f.default;value=f.name
	elif slots and f.default is not MISSING:globals[default_name]=f.default;value=default_name
	else:return
	if f._field_type is _FIELD_INITVAR:return
	return _field_assign(frozen,f.name,value,self_name)
def _init_param(f):
	if f.default is MISSING and f.default_factory is MISSING:default=''
	elif f.default is not MISSING:default=f"=_dflt_{f.name}"
	elif f.default_factory is not MISSING:default='=_HAS_DEFAULT_FACTORY'
	return f"{f.name}:_type_{f.name}{default}"
def _init_fn(fields,std_fields,kw_only_fields,frozen,has_post_init,self_name,globals,slots):
	seen_default=_B
	for f in std_fields:
		if f.init:
			if not(f.default is MISSING and f.default_factory is MISSING):seen_default=_A
			elif seen_default:raise TypeError(f"non-default argument {f.name!r} follows default argument")
	locals={f"_type_{f.name}":f.type for f in fields};locals.update({_H:MISSING,'_HAS_DEFAULT_FACTORY':_HAS_DEFAULT_FACTORY,'__dataclass_builtins_object__':object});body_lines=[]
	for f in fields:
		line=_field_init(f,frozen,locals,self_name,slots)
		if line:body_lines.append(line)
	if has_post_init:params_str=','.join(f.name for f in fields if f._field_type is _FIELD_INITVAR);body_lines.append(f"{self_name}.{_POST_INIT_NAME}({params_str})")
	if not body_lines:body_lines=['pass']
	_init_params=[_init_param(f)for f in std_fields]
	if kw_only_fields:_init_params+=['*'];_init_params+=[_init_param(f)for f in kw_only_fields]
	return _create_fn(_I,[self_name]+_init_params,body_lines,locals=locals,globals=globals,return_type=_C)
def _repr_fn(fields,globals):fn=_create_fn(_J,(_D,),['return self.__class__.__qualname__ + f"('+', '.join([f"{f.name}={{self.{f.name}!r}}"for f in fields])+')"'],globals=globals);return _recursive_repr(fn)
def _frozen_get_del_attr(cls,fields,globals):
	locals={'cls':cls,_G:FrozenInstanceError}
	if fields:fields_str='('+','.join(repr(f.name)for f in fields)+',)'
	else:fields_str='()'
	return _create_fn('__setattr__',(_D,_E,'value'),(f"if type(self) is cls or name in {fields_str}:",' raise FrozenInstanceError(f"cannot assign to field {name!r}")',f"super(cls, self).__setattr__(name, value)"),locals=locals,globals=globals),_create_fn('__delattr__',(_D,_E),(f"if type(self) is cls or name in {fields_str}:",' raise FrozenInstanceError(f"cannot delete field {name!r}")',f"super(cls, self).__delattr__(name)"),locals=locals,globals=globals)
def _cmp_fn(name,op,self_tuple,other_tuple,globals):return _create_fn(name,(_D,_F),['if other.__class__ is self.__class__:',f" return {self_tuple}{op}{other_tuple}",'return NotImplemented'],globals=globals)
def _hash_fn(fields,globals):self_tuple=_tuple_str(_D,fields);return _create_fn(_K,(_D,),[f"return hash({self_tuple})"],globals=globals)
def _is_classvar(a_type,typing):return a_type is typing.ClassVar or type(a_type)is typing._GenericAlias and a_type.__origin__ is typing.ClassVar
def _is_initvar(a_type,dataclasses):return a_type is dataclasses.InitVar or type(a_type)is dataclasses.InitVar
def _is_kw_only(a_type,dataclasses):return a_type is dataclasses.KW_ONLY
def _is_type(annotation,cls,a_module,a_type,is_type_predicate):
	match=_MODULE_IDENTIFIER_RE.match(annotation)
	if match:
		ns=_C;module_name=match.group(1)
		if not module_name:ns=sys.modules.get(cls.__module__).__dict__
		else:
			module=sys.modules.get(cls.__module__)
			if module and module.__dict__.get(module_name)is a_module:ns=sys.modules.get(a_type.__module__).__dict__
		if ns and is_type_predicate(ns.get(match.group(2)),a_module):return _A
	return _B
def _get_field(cls,a_name,a_type,default_kw_only):
	default=getattr(cls,a_name,MISSING)
	if isinstance(default,Field):f=default
	else:
		if isinstance(default,types.MemberDescriptorType):default=MISSING
		f=field(default=default)
	f.name=a_name;f.type=a_type;f._field_type=_FIELD;typing=sys.modules.get('typing')
	if typing:
		if _is_classvar(a_type,typing)or isinstance(f.type,str)and _is_type(f.type,cls,typing,typing.ClassVar,_is_classvar):f._field_type=_FIELD_CLASSVAR
	if f._field_type is _FIELD:
		dataclasses=sys.modules[__name__]
		if _is_initvar(a_type,dataclasses)or isinstance(f.type,str)and _is_type(f.type,cls,dataclasses,dataclasses.InitVar,_is_initvar):f._field_type=_FIELD_INITVAR
	if f._field_type in(_FIELD_CLASSVAR,_FIELD_INITVAR):
		if f.default_factory is not MISSING:raise TypeError(f"field {f.name} cannot have a default factory")
	if f._field_type in(_FIELD,_FIELD_INITVAR):
		if f.kw_only is MISSING:f.kw_only=default_kw_only
	else:
		assert f._field_type is _FIELD_CLASSVAR
		if f.kw_only is not MISSING:raise TypeError(f"field {f.name} is a ClassVar but specifies kw_only")
	if f._field_type is _FIELD and isinstance(f.default,(list,dict,set)):raise ValueError(f"mutable default {type(f.default)} for field {f.name} is not allowed: use default_factory")
	return f
def _set_qualname(cls,value):
	if isinstance(value,FunctionType):value.__qualname__=f"{cls.__qualname__}.{value.__name__}"
	return value
def _set_new_attribute(cls,name,value):
	if name in cls.__dict__:return _A
	_set_qualname(cls,value);setattr(cls,name,value);return _B
def _hash_set_none(cls,fields,globals):0
def _hash_add(cls,fields,globals):flds=[f for f in fields if(f.compare if f.hash is _C else f.hash)];return _set_qualname(cls,_hash_fn(flds,globals))
def _hash_exception(cls,fields,globals):raise TypeError(f"Cannot overwrite attribute __hash__ in class {cls.__name__}")
_hash_action={(_B,_B,_B,_B):_C,(_B,_B,_B,_A):_C,(_B,_B,_A,_B):_C,(_B,_B,_A,_A):_C,(_B,_A,_B,_B):_hash_set_none,(_B,_A,_B,_A):_C,(_B,_A,_A,_B):_hash_add,(_B,_A,_A,_A):_C,(_A,_B,_B,_B):_hash_add,(_A,_B,_B,_A):_hash_exception,(_A,_B,_A,_B):_hash_add,(_A,_B,_A,_A):_hash_exception,(_A,_A,_B,_B):_hash_add,(_A,_A,_B,_A):_hash_exception,(_A,_A,_A,_B):_hash_add,(_A,_A,_A,_A):_hash_exception}
def _process_class(cls,init,repr,eq,order,unsafe_hash,frozen,match_args,kw_only,slots):
	A='__eq__';fields={}
	if cls.__module__ in sys.modules:globals=sys.modules[cls.__module__].__dict__
	else:globals={}
	setattr(cls,_PARAMS,_DataclassParams(init,repr,eq,order,unsafe_hash,frozen));any_frozen_base=_B;has_dataclass_bases=_B
	for b in cls.__mro__[-1:0:-1]:
		base_fields=getattr(b,_FIELDS,_C)
		if base_fields is not _C:
			has_dataclass_bases=_A
			for f in base_fields.values():fields[f.name]=f
			if getattr(b,_PARAMS).frozen:any_frozen_base=_A
	cls_annotations=cls.__dict__.get(_L,{});cls_fields=[];KW_ONLY_seen=_B;dataclasses=sys.modules[__name__]
	for(name,type)in cls_annotations.items():
		if _is_kw_only(type,dataclasses)or isinstance(type,str)and _is_type(type,cls,dataclasses,dataclasses.KW_ONLY,_is_kw_only):
			if KW_ONLY_seen:raise TypeError(f"{name!r} is KW_ONLY, but KW_ONLY has already been specified")
			KW_ONLY_seen=_A;kw_only=_A
		else:cls_fields.append(_get_field(cls,name,type,kw_only))
	for f in cls_fields:
		fields[f.name]=f
		if isinstance(getattr(cls,f.name,_C),Field):
			if f.default is MISSING:delattr(cls,f.name)
			else:setattr(cls,f.name,f.default)
	for(name,value)in cls.__dict__.items():
		if isinstance(value,Field)and not name in cls_annotations:raise TypeError(f"{name!r} is a field but has no type annotation")
	if has_dataclass_bases:
		if any_frozen_base and not frozen:raise TypeError('cannot inherit non-frozen dataclass from a frozen one')
		if not any_frozen_base and frozen:raise TypeError('cannot inherit frozen dataclass from a non-frozen one')
	setattr(cls,_FIELDS,fields);class_hash=cls.__dict__.get(_K,MISSING);has_explicit_hash=not(class_hash is MISSING or class_hash is _C and A in cls.__dict__)
	if order and not eq:raise ValueError('eq must be true if order is true')
	all_init_fields=[f for f in fields.values()if f._field_type in(_FIELD,_FIELD_INITVAR)];std_init_fields,kw_only_init_fields=_fields_in_init_order(all_init_fields)
	if init:has_post_init=hasattr(cls,_POST_INIT_NAME);_set_new_attribute(cls,_I,_init_fn(all_init_fields,std_init_fields,kw_only_init_fields,frozen,has_post_init,'__dataclass_self__'if _D in fields else _D,globals,slots))
	field_list=[f for f in fields.values()if f._field_type is _FIELD]
	if repr:flds=[f for f in field_list if f.repr];_set_new_attribute(cls,_J,_repr_fn(flds,globals))
	if eq:flds=[f for f in field_list if f.compare];self_tuple=_tuple_str(_D,flds);other_tuple=_tuple_str(_F,flds);_set_new_attribute(cls,A,_cmp_fn(A,'==',self_tuple,other_tuple,globals=globals))
	if order:
		flds=[f for f in field_list if f.compare];self_tuple=_tuple_str(_D,flds);other_tuple=_tuple_str(_F,flds)
		for(name,op)in[('__lt__','<'),('__le__','<='),('__gt__','>'),('__ge__','>=')]:
			if _set_new_attribute(cls,name,_cmp_fn(name,op,self_tuple,other_tuple,globals=globals)):raise TypeError(f"Cannot overwrite attribute {name} in class {cls.__name__}. Consider using functools.total_ordering")
	if frozen:
		for fn in _frozen_get_del_attr(cls,field_list,globals):
			if _set_new_attribute(cls,fn.__name__,fn):raise TypeError(f"Cannot overwrite attribute {fn.__name__} in class {cls.__name__}")
	hash_action=_hash_action[bool(unsafe_hash),bool(eq),bool(frozen),has_explicit_hash]
	if hash_action:cls.__hash__=hash_action(cls,field_list,globals)
	if not getattr(cls,'__doc__'):cls.__doc__=cls.__name__+str(inspect.signature(cls)).replace(' -> None','')
	if match_args:_set_new_attribute(cls,'__match_args__',tuple(f.name for f in std_init_fields))
	if slots:cls=_add_slots(cls,frozen)
	abc.update_abstractmethods(cls);return cls
def _dataclass_getstate(self):return[getattr(self,f.name)for f in fields(self)]
def _dataclass_setstate(self,state):
	for(field,value)in zip(fields(self),state):object.__setattr__(self,field.name,value)
def _add_slots(cls,is_frozen):
	A='__slots__'
	if A in cls.__dict__:raise TypeError(f"{cls.__name__} already specifies __slots__")
	cls_dict=dict(cls.__dict__);field_names=tuple(f.name for f in fields(cls));cls_dict[A]=field_names
	for field_name in field_names:cls_dict.pop(field_name,_C)
	cls_dict.pop('__dict__',_C);qualname=getattr(cls,'__qualname__',_C);cls=type(cls)(cls.__name__,cls.__bases__,cls_dict)
	if qualname is not _C:cls.__qualname__=qualname
	if is_frozen:cls.__getstate__=_dataclass_getstate;cls.__setstate__=_dataclass_setstate
	return cls
def dataclass(cls=_C,*,init=_A,repr=_A,eq=_A,order=_B,unsafe_hash=_B,frozen=_B,match_args=_A,kw_only=_B,slots=_B):
	'Returns the same class as was passed in, with dunder methods\n    added based on the fields defined in the class.\n\n    Examines PEP 526 __annotations__ to determine fields.\n\n    If init is true, an __init__() method is added to the class. If\n    repr is true, a __repr__() method is added. If order is true, rich\n    comparison dunder methods are added. If unsafe_hash is true, a\n    __hash__() method function is added. If frozen is true, fields may\n    not be assigned to after instance creation. If match_args is true,\n    the __match_args__ tuple is added. If kw_only is true, then by\n    default all fields are keyword-only. If slots is true, an\n    __slots__ attribute is added.\n    '
	def wrap(cls):return _process_class(cls,init,repr,eq,order,unsafe_hash,frozen,match_args,kw_only,slots)
	if cls is _C:return wrap
	return wrap(cls)
def fields(class_or_instance):
	'Return a tuple describing the fields of this dataclass.\n\n    Accepts a dataclass or an instance of one. Tuple elements are of\n    type Field.\n    '
	try:fields=getattr(class_or_instance,_FIELDS)
	except AttributeError:raise TypeError('must be called with a dataclass type or instance')
	return tuple(f for f in fields.values()if f._field_type is _FIELD)
def _is_dataclass_instance(obj):'Returns True if obj is an instance of a dataclass.';return hasattr(type(obj),_FIELDS)
def is_dataclass(obj):'Returns True if obj is a dataclass or an instance of a\n    dataclass.';cls=obj if isinstance(obj,type)and not isinstance(obj,GenericAlias)else type(obj);return hasattr(cls,_FIELDS)
def asdict(obj,*,dict_factory=dict):
	"Return the fields of a dataclass instance as a new dictionary mapping\n    field names to field values.\n\n    Example usage:\n\n      @dataclass\n      class C:\n          x: int\n          y: int\n\n      c = C(1, 2)\n      assert asdict(c) == {'x': 1, 'y': 2}\n\n    If given, 'dict_factory' will be used instead of built-in dict.\n    The function applies recursively to field values that are\n    dataclass instances. This will also look into built-in containers:\n    tuples, lists, and dicts.\n    "
	if not _is_dataclass_instance(obj):raise TypeError('asdict() should be called on dataclass instances')
	return _asdict_inner(obj,dict_factory)
def _asdict_inner(obj,dict_factory):
	if _is_dataclass_instance(obj):
		result=[]
		for f in fields(obj):value=_asdict_inner(getattr(obj,f.name),dict_factory);result.append((f.name,value))
		return dict_factory(result)
	elif isinstance(obj,tuple)and hasattr(obj,_M):return type(obj)(*[_asdict_inner(v,dict_factory)for v in obj])
	elif isinstance(obj,(list,tuple)):return type(obj)(_asdict_inner(v,dict_factory)for v in obj)
	elif isinstance(obj,dict):return type(obj)((_asdict_inner(k,dict_factory),_asdict_inner(v,dict_factory))for(k,v)in obj.items())
	else:return copy.deepcopy(obj)
def astuple(obj,*,tuple_factory=tuple):
	"Return the fields of a dataclass instance as a new tuple of field values.\n\n    Example usage::\n\n      @dataclass\n      class C:\n          x: int\n          y: int\n\n    c = C(1, 2)\n    assert astuple(c) == (1, 2)\n\n    If given, 'tuple_factory' will be used instead of built-in tuple.\n    The function applies recursively to field values that are\n    dataclass instances. This will also look into built-in containers:\n    tuples, lists, and dicts.\n    "
	if not _is_dataclass_instance(obj):raise TypeError('astuple() should be called on dataclass instances')
	return _astuple_inner(obj,tuple_factory)
def _astuple_inner(obj,tuple_factory):
	if _is_dataclass_instance(obj):
		result=[]
		for f in fields(obj):value=_astuple_inner(getattr(obj,f.name),tuple_factory);result.append(value)
		return tuple_factory(result)
	elif isinstance(obj,tuple)and hasattr(obj,_M):return type(obj)(*[_astuple_inner(v,tuple_factory)for v in obj])
	elif isinstance(obj,(list,tuple)):return type(obj)(_astuple_inner(v,tuple_factory)for v in obj)
	elif isinstance(obj,dict):return type(obj)((_astuple_inner(k,tuple_factory),_astuple_inner(v,tuple_factory))for(k,v)in obj.items())
	else:return copy.deepcopy(obj)
def make_dataclass(cls_name,fields,*,bases=(),namespace=_C,init=_A,repr=_A,eq=_A,order=_B,unsafe_hash=_B,frozen=_B,match_args=_A,kw_only=_B,slots=_B):
	"Return a new dynamically created dataclass.\n\n    The dataclass name will be 'cls_name'.  'fields' is an iterable\n    of either (name), (name, type) or (name, type, Field) objects. If type is\n    omitted, use the string 'typing.Any'.  Field objects are created by\n    the equivalent of calling 'field(name, type [, Field-info])'.\n\n      C = make_dataclass('C', ['x', ('y', int), ('z', int, field(init=False))], bases=(Base,))\n\n    is equivalent to:\n\n      @dataclass\n      class C(Base):\n          x: 'typing.Any'\n          y: int\n          z: int = field(init=False)\n\n    For the bases and namespace parameters, see the builtin type() function.\n\n    The parameters init, repr, eq, order, unsafe_hash, and frozen are passed to\n    dataclass().\n    "
	if namespace is _C:namespace={}
	seen=set();annotations={};defaults={}
	for item in fields:
		if isinstance(item,str):name=item;tp='typing.Any'
		elif len(item)==2:name,tp=item
		elif len(item)==3:name,tp,spec=item;defaults[name]=spec
		else:raise TypeError(f"Invalid field: {item!r}")
		if not isinstance(name,str)or not name.isidentifier():raise TypeError(f"Field names must be valid identifiers: {name!r}")
		if keyword.iskeyword(name):raise TypeError(f"Field names must not be keywords: {name!r}")
		if name in seen:raise TypeError(f"Field name duplicated: {name!r}")
		seen.add(name);annotations[name]=tp
	def exec_body_callback(ns):ns.update(namespace);ns.update(defaults);ns[_L]=annotations
	cls=types.new_class(cls_name,bases,{},exec_body_callback);return dataclass(cls,init=init,repr=repr,eq=eq,order=order,unsafe_hash=unsafe_hash,frozen=frozen,match_args=match_args,kw_only=kw_only,slots=slots)
def replace(obj,**changes):
	'Return a new object replacing specified fields with new values.\n\n    This is especially useful for frozen classes.  Example usage:\n\n      @dataclass(frozen=True)\n      class C:\n          x: int\n          y: int\n\n      c = C(1, 2)\n      c1 = replace(c, x=3)\n      assert c1.x == 3 and c1.y == 2\n      '
	if not _is_dataclass_instance(obj):raise TypeError('replace() should be called on dataclass instances')
	for f in getattr(obj,_FIELDS).values():
		if f._field_type is _FIELD_CLASSVAR:continue
		if not f.init:
			if f.name in changes:raise ValueError(f"field {f.name} is declared with init=False, it cannot be specified with replace()")
			continue
		if f.name not in changes:
			if f._field_type is _FIELD_INITVAR and f.default is MISSING:raise ValueError(f"InitVar {f.name!r} must be specified with replace()")
			changes[f.name]=getattr(obj,f.name)
	return obj.__class__(**changes)