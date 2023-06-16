'\nThe typing module: Support for gradual typing as defined by PEP 484.\n\nAt large scale, the structure of the module is following:\n* Imports and exports, all public names should be explicitly added to __all__.\n* Internal helper functions: these should never be used in code outside this module.\n* _SpecialForm and its instances (special forms):\n  Any, NoReturn, ClassVar, Union, Optional, Concatenate\n* Classes whose instances can be type arguments in addition to types:\n  ForwardRef, TypeVar and ParamSpec\n* The core of internal generics API: _GenericAlias and _VariadicGenericAlias, the latter is\n  currently only used by Tuple and Callable. All subscripted types like X[int], Union[int, str],\n  etc., are instances of either of these classes.\n* The public counterpart of the generics API consists of two classes: Generic and Protocol.\n* Public helper functions: get_type_hints, overload, cast, no_type_check,\n  no_type_check_decorator.\n* Generic aliases for collections.abc ABCs and few additional protocols.\n* Special types: NewType, NamedTuple, TypedDict.\n* Wrapper submodules for re and io related types.\n'
_y='Instance and class checks can only be used with @runtime_checkable protocols'
_x='__subclasshook__'
_w='__slots__'
_v='__new__'
_u='__contravariant__'
_t='__covariant__'
_s='__bound__'
_r='The last parameter to Concatenate should be a ParamSpec variable.'
_q='__doc__'
_p='__weakref__'
_o='builtins'
_n='AnyStr'
_m='TextIO'
_l='Pattern'
_k='BinaryIO'
_j='TypedDict'
_i='NamedTuple'
_h='FrozenSet'
_g='DefaultDict'
_f='Reversible'
_e='AsyncContextManager'
_d='Collection'
_c='AsyncIterable'
_b='Awaitable'
_a='Iterator'
_Z='Iterable'
_Y='Hashable'
_X='ContextManager'
_W='Container'
_V='AbstractSet'
_U='Optional'
_T='Generic'
_S='Annotated'
_R='__init__'
_Q='_is_runtime_protocol'
_P='__orig_bases__'
_O='typing'
_N='typing.'
_M='__qualname__'
_L='Protocol'
_K='Callable'
_J='__module__'
_I='_is_protocol'
_H='__main__'
_G='__dict__'
_F=', '
_E='__annotations__'
_D='__name__'
_C=False
_B=True
_A=None
from abc import abstractmethod,ABCMeta
import collections,collections.abc,contextlib,functools,operator,re as stdlib_re,sys,types
from types import WrapperDescriptorType,MethodWrapperType,MethodDescriptorType,GenericAlias
__all__=[_S,'Any',_K,'ClassVar','Concatenate','Final','ForwardRef',_T,'Literal',_U,'ParamSpec',_L,'Tuple','Type','TypeVar','Union',_V,'ByteString',_W,_X,_Y,'ItemsView',_Z,_a,'KeysView','Mapping','MappingView','MutableMapping','MutableSequence','MutableSet','Sequence','Sized','ValuesView',_b,'AsyncIterator',_c,'Coroutine',_d,'AsyncGenerator',_e,_f,'SupportsAbs','SupportsBytes','SupportsComplex','SupportsFloat','SupportsIndex','SupportsInt','SupportsRound','ChainMap','Counter','Deque','Dict',_g,'List','OrderedDict','Set',_h,_i,_j,'Generator',_k,'IO','Match',_l,_m,_n,'cast','final','get_args','get_origin','get_type_hints','is_typeddict','NewType','no_type_check','no_type_check_decorator','NoReturn','overload','ParamSpecArgs','ParamSpecKwargs','runtime_checkable','Text','TYPE_CHECKING','TypeAlias','TypeGuard']
def _type_convert(arg,module=_A,*,allow_special_forms=_C):
	'For converting None to type(None), and strings to ForwardRef.'
	if arg is _A:return type(_A)
	if isinstance(arg,str):return ForwardRef(arg,module=module,is_class=allow_special_forms)
	return arg
def _type_check(arg,msg,is_argument=_B,module=_A,*,allow_special_forms=_C):
	'Check that the argument is a type, and return it (internal helper).\n\n    As a special case, accept None and return type(None) instead. Also wrap strings\n    into ForwardRef instances. Consider several corner cases, for example plain\n    special forms like Union are not valid, while Union[int, str] is OK, etc.\n    The msg argument is a human-readable error message, e.g::\n\n        "Union[arg, ...]: arg should be a type."\n\n    We append the repr() of the actual value (truncated to 100 chars).\n    ';invalid_generic_forms=Generic,Protocol
	if not allow_special_forms:
		invalid_generic_forms+=ClassVar,
		if is_argument:invalid_generic_forms+=Final,
	arg=_type_convert(arg,module=module,allow_special_forms=allow_special_forms)
	if isinstance(arg,_GenericAlias)and arg.__origin__ in invalid_generic_forms:raise TypeError(f"{arg} is not valid as type argument")
	if arg in(Any,NoReturn,Final,TypeAlias):return arg
	if isinstance(arg,_SpecialForm)or arg in(Generic,Protocol):raise TypeError(f"Plain {arg} is not valid as type argument")
	if isinstance(arg,(type,TypeVar,ForwardRef,types.UnionType,ParamSpec,ParamSpecArgs,ParamSpecKwargs)):return arg
	if not callable(arg):raise TypeError(f"{msg} Got {arg!r:.100}.")
	return arg
def _is_param_expr(arg):return arg is...or isinstance(arg,(tuple,list,ParamSpec,_ConcatenateGenericAlias))
def _type_repr(obj):
	'Return the repr() of an object, special-casing types (internal helper).\n\n    If obj is a type, we return a shorter version than the default\n    type.__repr__, based on the module and qualified name, which is\n    typically enough to uniquely identify a type.  For everything\n    else, we fall back on repr(obj).\n    '
	if isinstance(obj,types.GenericAlias):return repr(obj)
	if isinstance(obj,type):
		if obj.__module__==_o:return obj.__qualname__
		return f"{obj.__module__}.{obj.__qualname__}"
	if obj is...:return'...'
	if isinstance(obj,types.FunctionType):return obj.__name__
	return repr(obj)
def _collect_type_vars(types_,typevar_types=_A):
	'Collect all type variable contained\n    in types in order of first appearance (lexicographic order). For example::\n\n        _collect_type_vars((T, List[S, T])) == (T, S)\n    '
	if typevar_types is _A:typevar_types=TypeVar
	tvars=[]
	for t in types_:
		if isinstance(t,typevar_types)and t not in tvars:tvars.append(t)
		if isinstance(t,(_GenericAlias,GenericAlias,types.UnionType)):tvars.extend([t for t in t.__parameters__ if t not in tvars])
	return tuple(tvars)
def _check_generic(cls,parameters,elen):
	'Check correct count for parameters of a generic cls (internal helper).\n    This gives a nice error message in case of count mismatch.\n    '
	if not elen:raise TypeError(f"{cls} is not a generic class")
	alen=len(parameters)
	if alen!=elen:raise TypeError(f"Too {'many'if alen>elen else'few'} arguments for {cls}; actual {alen}, expected {elen}")
def _prepare_paramspec_params(cls,params):
	'Prepares the parameters for a Generic containing ParamSpec\n    variables (internal helper).\n    '
	if len(cls.__parameters__)==1 and params and not _is_param_expr(params[0]):assert isinstance(cls.__parameters__[0],ParamSpec);return params,
	else:
		_check_generic(cls,params,len(cls.__parameters__));_params=[]
		for(p,tvar)in zip(params,cls.__parameters__):
			if isinstance(tvar,ParamSpec)and isinstance(p,list):p=tuple(p)
			_params.append(p)
		return tuple(_params)
def _deduplicate(params):
	all_params=set(params)
	if len(all_params)<len(params):
		new_params=[]
		for t in params:
			if t in all_params:new_params.append(t);all_params.remove(t)
		params=new_params;assert not all_params,all_params
	return params
def _remove_dups_flatten(parameters):
	'An internal helper for Union creation and substitution: flatten Unions\n    among parameters, then remove duplicates.\n    ';params=[]
	for p in parameters:
		if isinstance(p,(_UnionGenericAlias,types.UnionType)):params.extend(p.__args__)
		elif isinstance(p,tuple)and len(p)>0 and p[0]is Union:params.extend(p[1:])
		else:params.append(p)
	return tuple(_deduplicate(params))
def _flatten_literal_params(parameters):
	'An internal helper for Literal creation: flatten Literals among parameters';params=[]
	for p in parameters:
		if isinstance(p,_LiteralGenericAlias):params.extend(p.__args__)
		else:params.append(p)
	return tuple(params)
_cleanups=[]
def _tp_cache(func=_A,*,typed=_C):
	'Internal wrapper caching __getitem__ of generic types with a fallback to\n    original function for non-hashable arguments.\n    '
	def decorator(func):
		cached=functools.lru_cache(typed=typed)(func);_cleanups.append(cached.cache_clear)
		@functools.wraps(func)
		def inner(*args,**kwds):
			try:return cached(*args,**kwds)
			except TypeError:pass
			return func(*args,**kwds)
		return inner
	if func is not _A:return decorator(func)
	return decorator
def _eval_type(t,globalns,localns,recursive_guard=frozenset()):
	'Evaluate all forward references in the given type t.\n    For use of globalns and localns see the docstring for get_type_hints().\n    recursive_guard is used to prevent infinite recursion with a recursive\n    ForwardRef.\n    '
	if isinstance(t,ForwardRef):return t._evaluate(globalns,localns,recursive_guard)
	if isinstance(t,(_GenericAlias,GenericAlias,types.UnionType)):
		ev_args=tuple(_eval_type(a,globalns,localns,recursive_guard)for a in t.__args__)
		if ev_args==t.__args__:return t
		if isinstance(t,GenericAlias):return GenericAlias(t.__origin__,ev_args)
		if isinstance(t,types.UnionType):return functools.reduce(operator.or_,ev_args)
		else:return t.copy_with(ev_args)
	return t
class _Final:
	'Mixin to prohibit subclassing';__slots__=_p,
	def __init_subclass__(self,*args,**kwds):
		if'_root'not in kwds:raise TypeError('Cannot subclass special typing classes')
class _Immutable:
	'Mixin to indicate that object should not be copied.';__slots__=()
	def __copy__(self):return self
	def __deepcopy__(self,memo):return self
class _SpecialForm(_Final,_root=_B):
	__slots__='_name',_q,'_getitem'
	def __init__(self,getitem):self._getitem=getitem;self._name=getitem.__name__;self.__doc__=getitem.__doc__
	def __getattr__(self,item):
		if item in{_D,_M}:return self._name
		raise AttributeError(item)
	def __mro_entries__(self,bases):raise TypeError(f"Cannot subclass {self!r}")
	def __repr__(self):return _N+self._name
	def __reduce__(self):return self._name
	def __call__(self,*args,**kwds):raise TypeError(f"Cannot instantiate {self!r}")
	def __or__(self,other):return Union[self,other]
	def __ror__(self,other):return Union[other,self]
	def __instancecheck__(self,obj):raise TypeError(f"{self} cannot be used with isinstance()")
	def __subclasscheck__(self,cls):raise TypeError(f"{self} cannot be used with issubclass()")
	@_tp_cache
	def __getitem__(self,parameters):return self._getitem(self,parameters)
class _LiteralSpecialForm(_SpecialForm,_root=_B):
	def __getitem__(self,parameters):
		if not isinstance(parameters,tuple):parameters=parameters,
		return self._getitem(self,*parameters)
@_SpecialForm
def Any(self,parameters):'Special type indicating an unconstrained type.\n\n    - Any is compatible with every type.\n    - Any assumed to have all methods.\n    - All values assumed to be instances of Any.\n\n    Note that all the above statements are true from the point of view of\n    static type checkers. At runtime, Any should not be used with instance\n    or class checks.\n    ';raise TypeError(f"{self} is not subscriptable")
@_SpecialForm
def NoReturn(self,parameters):"Special type indicating functions that never return.\n    Example::\n\n      from typing import NoReturn\n\n      def stop() -> NoReturn:\n          raise Exception('no way')\n\n    This type is invalid in other positions, e.g., ``List[NoReturn]``\n    will fail in static type checkers.\n    ";raise TypeError(f"{self} is not subscriptable")
@_SpecialForm
def ClassVar(self,parameters):'Special type construct to mark class variables.\n\n    An annotation wrapped in ClassVar indicates that a given\n    attribute is intended to be used as a class variable and\n    should not be set on instances of that class. Usage::\n\n      class Starship:\n          stats: ClassVar[Dict[str, int]] = {} # class variable\n          damage: int = 10                     # instance variable\n\n    ClassVar accepts only types and cannot be further subscribed.\n\n    Note that ClassVar is not a class itself, and should not\n    be used with isinstance() or issubclass().\n    ';item=_type_check(parameters,f"{self} accepts only single type.");return _GenericAlias(self,(item,))
@_SpecialForm
def Final(self,parameters):'Special typing construct to indicate final names to type checkers.\n\n    A final name cannot be re-assigned or overridden in a subclass.\n    For example:\n\n      MAX_SIZE: Final = 9000\n      MAX_SIZE += 1  # Error reported by type checker\n\n      class Connection:\n          TIMEOUT: Final[int] = 10\n\n      class FastConnector(Connection):\n          TIMEOUT = 1  # Error reported by type checker\n\n    There is no runtime checking of these properties.\n    ';item=_type_check(parameters,f"{self} accepts only single type.");return _GenericAlias(self,(item,))
@_SpecialForm
def Union(self,parameters):
	'Union type; Union[X, Y] means either X or Y.\n\n    To define a union, use e.g. Union[int, str].  Details:\n    - The arguments must be types and there must be at least one.\n    - None as an argument is a special case and is replaced by\n      type(None).\n    - Unions of unions are flattened, e.g.::\n\n        Union[Union[int, str], float] == Union[int, str, float]\n\n    - Unions of a single argument vanish, e.g.::\n\n        Union[int] == int  # The constructor actually returns int\n\n    - Redundant arguments are skipped, e.g.::\n\n        Union[int, str, int] == Union[int, str]\n\n    - When comparing unions, the argument order is ignored, e.g.::\n\n        Union[int, str] == Union[str, int]\n\n    - You cannot subclass or instantiate a union.\n    - You can use Optional[X] as a shorthand for Union[X, None].\n    '
	if parameters==():raise TypeError('Cannot take a Union of no types.')
	if not isinstance(parameters,tuple):parameters=parameters,
	msg='Union[arg, ...]: each arg must be a type.';parameters=tuple(_type_check(p,msg)for p in parameters);parameters=_remove_dups_flatten(parameters)
	if len(parameters)==1:return parameters[0]
	if len(parameters)==2 and type(_A)in parameters:return _UnionGenericAlias(self,parameters,name=_U)
	return _UnionGenericAlias(self,parameters)
@_SpecialForm
def Optional(self,parameters):'Optional type.\n\n    Optional[X] is equivalent to Union[X, None].\n    ';arg=_type_check(parameters,f"{self} requires a single type.");return Union[arg,type(_A)]
@_LiteralSpecialForm
@_tp_cache(typed=_B)
def Literal(self,*parameters):
	"Special typing form to define literal types (a.k.a. value types).\n\n    This form can be used to indicate to type checkers that the corresponding\n    variable or function parameter has a value equivalent to the provided\n    literal (or one of several literals):\n\n      def validate_simple(data: Any) -> Literal[True]:  # always returns True\n          ...\n\n      MODE = Literal['r', 'rb', 'w', 'wb']\n      def open_helper(file: str, mode: MODE) -> str:\n          ...\n\n      open_helper('/some/path', 'r')  # Passes type check\n      open_helper('/other/path', 'typo')  # Error in type checker\n\n    Literal[...] cannot be subclassed. At runtime, an arbitrary value\n    is allowed as type argument to Literal[...], but type checkers may\n    impose restrictions.\n    ";parameters=_flatten_literal_params(parameters)
	try:parameters=tuple(p for(p,_)in _deduplicate(list(_value_and_type_iter(parameters))))
	except TypeError:pass
	return _LiteralGenericAlias(self,parameters)
@_SpecialForm
def TypeAlias(self,parameters):"Special marker indicating that an assignment should\n    be recognized as a proper type alias definition by type\n    checkers.\n\n    For example::\n\n        Predicate: TypeAlias = Callable[..., bool]\n\n    It's invalid when used anywhere except as in the example above.\n    ";raise TypeError(f"{self} is not subscriptable")
@_SpecialForm
def Concatenate(self,parameters):
	'Used in conjunction with ``ParamSpec`` and ``Callable`` to represent a\n    higher order function which adds, removes or transforms parameters of a\n    callable.\n\n    For example::\n\n       Callable[Concatenate[int, P], int]\n\n    See PEP 612 for detailed information.\n    '
	if parameters==():raise TypeError('Cannot take a Concatenate of no types.')
	if not isinstance(parameters,tuple):parameters=parameters,
	if not isinstance(parameters[-1],ParamSpec):raise TypeError(_r)
	msg='Concatenate[arg, ...]: each arg must be a type.';parameters=*(_type_check(p,msg)for p in parameters[:-1]),parameters[-1];return _ConcatenateGenericAlias(self,parameters,_typevar_types=(TypeVar,ParamSpec),_paramspec_tvars=_B)
@_SpecialForm
def TypeGuard(self,parameters):'Special typing form used to annotate the return type of a user-defined\n    type guard function.  ``TypeGuard`` only accepts a single type argument.\n    At runtime, functions marked this way should return a boolean.\n\n    ``TypeGuard`` aims to benefit *type narrowing* -- a technique used by static\n    type checkers to determine a more precise type of an expression within a\n    program\'s code flow.  Usually type narrowing is done by analyzing\n    conditional code flow and applying the narrowing to a block of code.  The\n    conditional expression here is sometimes referred to as a "type guard".\n\n    Sometimes it would be convenient to use a user-defined boolean function\n    as a type guard.  Such a function should use ``TypeGuard[...]`` as its\n    return type to alert static type checkers to this intention.\n\n    Using  ``-> TypeGuard`` tells the static type checker that for a given\n    function:\n\n    1. The return value is a boolean.\n    2. If the return value is ``True``, the type of its argument\n       is the type inside ``TypeGuard``.\n\n       For example::\n\n          def is_str(val: Union[str, float]):\n              # "isinstance" type guard\n              if isinstance(val, str):\n                  # Type of ``val`` is narrowed to ``str``\n                  ...\n              else:\n                  # Else, type of ``val`` is narrowed to ``float``.\n                  ...\n\n    Strict type narrowing is not enforced -- ``TypeB`` need not be a narrower\n    form of ``TypeA`` (it can even be a wider form) and this may lead to\n    type-unsafe results.  The main reason is to allow for things like\n    narrowing ``List[object]`` to ``List[str]`` even though the latter is not\n    a subtype of the former, since ``List`` is invariant.  The responsibility of\n    writing type-safe type guards is left to the user.\n\n    ``TypeGuard`` also works with type variables.  For more information, see\n    PEP 647 (User-Defined Type Guards).\n    ';item=_type_check(parameters,f"{self} accepts only single type.");return _GenericAlias(self,(item,))
class ForwardRef(_Final,_root=_B):
	'Internal wrapper to hold a forward reference.';__slots__='__forward_arg__','__forward_code__','__forward_evaluated__','__forward_value__','__forward_is_argument__','__forward_is_class__','__forward_module__'
	def __init__(self,arg,is_argument=_B,module=_A,*,is_class=_C):
		if not isinstance(arg,str):raise TypeError(f"Forward reference must be a string -- got {arg!r}")
		try:code=compile(arg,'<string>','eval')
		except SyntaxError:raise SyntaxError(f"Forward reference must be an expression -- got {arg!r}")
		self.__forward_arg__=arg;self.__forward_code__=code;self.__forward_evaluated__=_C;self.__forward_value__=_A;self.__forward_is_argument__=is_argument;self.__forward_is_class__=is_class;self.__forward_module__=module
	def _evaluate(self,globalns,localns,recursive_guard):
		if self.__forward_arg__ in recursive_guard:return self
		if not self.__forward_evaluated__ or localns is not globalns:
			if globalns is _A and localns is _A:globalns=localns={}
			elif globalns is _A:globalns=localns
			elif localns is _A:localns=globalns
			if self.__forward_module__ is not _A:globalns=getattr(sys.modules.get(self.__forward_module__,_A),_G,globalns)
			type_=_type_check(eval(self.__forward_code__,globalns,localns),'Forward references must evaluate to types.',is_argument=self.__forward_is_argument__,allow_special_forms=self.__forward_is_class__);self.__forward_value__=_eval_type(type_,globalns,localns,recursive_guard|{self.__forward_arg__});self.__forward_evaluated__=_B
		return self.__forward_value__
	def __eq__(self,other):
		if not isinstance(other,ForwardRef):return NotImplemented
		if self.__forward_evaluated__ and other.__forward_evaluated__:return self.__forward_arg__==other.__forward_arg__ and self.__forward_value__==other.__forward_value__
		return self.__forward_arg__==other.__forward_arg__ and self.__forward_module__==other.__forward_module__
	def __hash__(self):return hash((self.__forward_arg__,self.__forward_module__))
	def __repr__(self):return f"ForwardRef({self.__forward_arg__!r})"
class _TypeVarLike:
	'Mixin for TypeVar-like types (TypeVar and ParamSpec).'
	def __init__(self,bound,covariant,contravariant):
		"Used to setup TypeVars and ParamSpec's bound, covariant and\n        contravariant attributes.\n        "
		if covariant and contravariant:raise ValueError('Bivariant types are not supported.')
		self.__covariant__=bool(covariant);self.__contravariant__=bool(contravariant)
		if bound:self.__bound__=_type_check(bound,'Bound must be a type.')
		else:self.__bound__=_A
	def __or__(self,right):return Union[self,right]
	def __ror__(self,left):return Union[left,self]
	def __repr__(self):
		if self.__covariant__:prefix='+'
		elif self.__contravariant__:prefix='-'
		else:prefix='~'
		return prefix+self.__name__
	def __reduce__(self):return self.__name__
class TypeVar(_Final,_Immutable,_TypeVarLike,_root=_B):
	"Type variable.\n\n    Usage::\n\n      T = TypeVar('T')  # Can be anything\n      A = TypeVar('A', str, bytes)  # Must be str or bytes\n\n    Type variables exist primarily for the benefit of static type\n    checkers.  They serve as the parameters for generic types as well\n    as for generic function definitions.  See class Generic for more\n    information on generic types.  Generic functions work as follows:\n\n      def repeat(x: T, n: int) -> List[T]:\n          '''Return a list containing n references to x.'''\n          return [x]*n\n\n      def longest(x: A, y: A) -> A:\n          '''Return the longest of two strings.'''\n          return x if len(x) >= len(y) else y\n\n    The latter example's signature is essentially the overloading\n    of (str, str) -> str and (bytes, bytes) -> bytes.  Also note\n    that if the arguments are instances of some subclass of str,\n    the return type is still plain str.\n\n    At runtime, isinstance(x, T) and issubclass(C, T) will raise TypeError.\n\n    Type variables defined with covariant=True or contravariant=True\n    can be used to declare covariant or contravariant generic types.\n    See PEP 484 for more details. By default generic types are invariant\n    in all type variables.\n\n    Type variables can be introspected. e.g.:\n\n      T.__name__ == 'T'\n      T.__constraints__ == ()\n      T.__covariant__ == False\n      T.__contravariant__ = False\n      A.__constraints__ == (str, bytes)\n\n    Note that only type variables defined in global scope can be pickled.\n    ";__slots__=_D,_s,'__constraints__',_t,_u,_G
	def __init__(self,name,*constraints,bound=_A,covariant=_C,contravariant=_C):
		self.__name__=name;super().__init__(bound,covariant,contravariant)
		if constraints and bound is not _A:raise TypeError('Constraints cannot be combined with bound=...')
		if constraints and len(constraints)==1:raise TypeError('A single constraint is not allowed')
		msg='TypeVar(name, constraint, ...): constraints must be types.';self.__constraints__=tuple(_type_check(t,msg)for t in constraints)
		try:def_mod=sys._getframe(1).f_globals.get(_D,_H)
		except(AttributeError,ValueError):def_mod=_A
		if def_mod!=_O:self.__module__=def_mod
class ParamSpecArgs(_Final,_Immutable,_root=_B):
	'The args for a ParamSpec object.\n\n    Given a ParamSpec object P, P.args is an instance of ParamSpecArgs.\n\n    ParamSpecArgs objects have a reference back to their ParamSpec:\n\n       P.args.__origin__ is P\n\n    This type is meant for runtime introspection and has no special meaning to\n    static type checkers.\n    '
	def __init__(self,origin):self.__origin__=origin
	def __repr__(self):return f"{self.__origin__.__name__}.args"
	def __eq__(self,other):
		if not isinstance(other,ParamSpecArgs):return NotImplemented
		return self.__origin__==other.__origin__
class ParamSpecKwargs(_Final,_Immutable,_root=_B):
	'The kwargs for a ParamSpec object.\n\n    Given a ParamSpec object P, P.kwargs is an instance of ParamSpecKwargs.\n\n    ParamSpecKwargs objects have a reference back to their ParamSpec:\n\n       P.kwargs.__origin__ is P\n\n    This type is meant for runtime introspection and has no special meaning to\n    static type checkers.\n    '
	def __init__(self,origin):self.__origin__=origin
	def __repr__(self):return f"{self.__origin__.__name__}.kwargs"
	def __eq__(self,other):
		if not isinstance(other,ParamSpecKwargs):return NotImplemented
		return self.__origin__==other.__origin__
class ParamSpec(_Final,_Immutable,_TypeVarLike,_root=_B):
	"Parameter specification variable.\n\n    Usage::\n\n       P = ParamSpec('P')\n\n    Parameter specification variables exist primarily for the benefit of static\n    type checkers.  They are used to forward the parameter types of one\n    callable to another callable, a pattern commonly found in higher order\n    functions and decorators.  They are only valid when used in ``Concatenate``,\n    or as the first argument to ``Callable``, or as parameters for user-defined\n    Generics.  See class Generic for more information on generic types.  An\n    example for annotating a decorator::\n\n       T = TypeVar('T')\n       P = ParamSpec('P')\n\n       def add_logging(f: Callable[P, T]) -> Callable[P, T]:\n           '''A type-safe decorator to add logging to a function.'''\n           def inner(*args: P.args, **kwargs: P.kwargs) -> T:\n               logging.info(f'{f.__name__} was called')\n               return f(*args, **kwargs)\n           return inner\n\n       @add_logging\n       def add_two(x: float, y: float) -> float:\n           '''Add two numbers together.'''\n           return x + y\n\n    Parameter specification variables defined with covariant=True or\n    contravariant=True can be used to declare covariant or contravariant\n    generic types.  These keyword arguments are valid, but their actual semantics\n    are yet to be decided.  See PEP 612 for details.\n\n    Parameter specification variables can be introspected. e.g.:\n\n       P.__name__ == 'T'\n       P.__bound__ == None\n       P.__covariant__ == False\n       P.__contravariant__ == False\n\n    Note that only parameter specification variables defined in global scope can\n    be pickled.\n    ";__slots__=_D,_s,_t,_u,_G
	@property
	def args(self):return ParamSpecArgs(self)
	@property
	def kwargs(self):return ParamSpecKwargs(self)
	def __init__(self,name,*,bound=_A,covariant=_C,contravariant=_C):
		self.__name__=name;super().__init__(bound,covariant,contravariant)
		try:def_mod=sys._getframe(1).f_globals.get(_D,_H)
		except(AttributeError,ValueError):def_mod=_A
		if def_mod!=_O:self.__module__=def_mod
def _is_dunder(attr):return attr.startswith('__')and attr.endswith('__')
class _BaseGenericAlias(_Final,_root=_B):
	"The central part of internal API.\n\n    This represents a generic version of type 'origin' with type arguments 'params'.\n    There are two kind of these aliases: user defined and special. The special ones\n    are wrappers around builtin collections and ABCs in collections.abc. These must\n    have 'name' always set. If 'inst' is False, then the alias can't be instantiated,\n    this is used by e.g. typing.List and typing.Dict.\n    "
	def __init__(self,origin,*,inst=_B,name=_A):self._inst=inst;self._name=name;self.__origin__=origin;self.__slots__=_A
	def __call__(self,*args,**kwargs):
		if not self._inst:raise TypeError(f"Type {self._name} cannot be instantiated; use {self.__origin__.__name__}() instead")
		result=self.__origin__(*args,**kwargs)
		try:result.__orig_class__=self
		except AttributeError:pass
		return result
	def __mro_entries__(self,bases):
		res=[]
		if self.__origin__ not in bases:res.append(self.__origin__)
		i=bases.index(self)
		for b in bases[i+1:]:
			if isinstance(b,_BaseGenericAlias)or issubclass(b,Generic):break
		else:res.append(Generic)
		return tuple(res)
	def __getattr__(self,attr):
		if attr in{_D,_M}:return self._name or self.__origin__.__name__
		if'__origin__'in self.__dict__ and not _is_dunder(attr):return getattr(self.__origin__,attr)
		raise AttributeError(attr)
	def __setattr__(self,attr,val):
		if _is_dunder(attr)or attr in{'_name','_inst','_nparams','_typevar_types','_paramspec_tvars'}:super().__setattr__(attr,val)
		else:setattr(self.__origin__,attr,val)
	def __instancecheck__(self,obj):return self.__subclasscheck__(type(obj))
	def __subclasscheck__(self,cls):raise TypeError('Subscripted generics cannot be used with class and instance checks')
	def __dir__(self):return list(set(super().__dir__()+[attr for attr in dir(self.__origin__)if not _is_dunder(attr)]))
class _GenericAlias(_BaseGenericAlias,_root=_B):
	def __init__(self,origin,params,*,inst=_B,name=_A,_typevar_types=TypeVar,_paramspec_tvars=_C):
		super().__init__(origin,inst=inst,name=name)
		if not isinstance(params,tuple):params=params,
		self.__args__=tuple(...if a is _TypingEllipsis else()if a is _TypingEmpty else a for a in params);self.__parameters__=_collect_type_vars(params,typevar_types=_typevar_types);self._typevar_types=_typevar_types;self._paramspec_tvars=_paramspec_tvars
		if not name:self.__module__=origin.__module__
	def __eq__(self,other):
		if not isinstance(other,_GenericAlias):return NotImplemented
		return self.__origin__==other.__origin__ and self.__args__==other.__args__
	def __hash__(self):return hash((self.__origin__,self.__args__))
	def __or__(self,right):return Union[self,right]
	def __ror__(self,left):return Union[left,self]
	@_tp_cache
	def __getitem__(self,params):
		if self.__origin__ in(Generic,Protocol):raise TypeError(f"Cannot subscript already-subscripted {self}")
		if not isinstance(params,tuple):params=params,
		params=tuple(_type_convert(p)for p in params)
		if self._paramspec_tvars and any(isinstance(t,ParamSpec)for t in self.__parameters__):params=_prepare_paramspec_params(self,params)
		else:_check_generic(self,params,len(self.__parameters__))
		subst=dict(zip(self.__parameters__,params));new_args=[]
		for arg in self.__args__:
			if isinstance(arg,self._typevar_types):
				if isinstance(arg,ParamSpec):
					arg=subst[arg]
					if not _is_param_expr(arg):raise TypeError(f"Expected a list of types, an ellipsis, ParamSpec, or Concatenate. Got {arg}")
				else:arg=subst[arg]
			elif isinstance(arg,(_GenericAlias,GenericAlias,types.UnionType)):
				subparams=arg.__parameters__
				if subparams:subargs=tuple(subst[x]for x in subparams);arg=arg[subargs]
			if self.__origin__==collections.abc.Callable and isinstance(arg,tuple):new_args.extend(arg)
			else:new_args.append(arg)
		return self.copy_with(tuple(new_args))
	def copy_with(self,params):return self.__class__(self.__origin__,params,name=self._name,inst=self._inst,_typevar_types=self._typevar_types,_paramspec_tvars=self._paramspec_tvars)
	def __repr__(self):
		if self._name:name=_N+self._name
		else:name=_type_repr(self.__origin__)
		args=_F.join([_type_repr(a)for a in self.__args__]);return f"{name}[{args}]"
	def __reduce__(self):
		if self._name:origin=globals()[self._name]
		else:origin=self.__origin__
		args=tuple(self.__args__)
		if len(args)==1 and not isinstance(args[0],tuple):args,=args
		return operator.getitem,(origin,args)
	def __mro_entries__(self,bases):
		if isinstance(self.__origin__,_SpecialForm):raise TypeError(f"Cannot subclass {self!r}")
		if self._name:return super().__mro_entries__(bases)
		if self.__origin__ is Generic:
			if Protocol in bases:return()
			i=bases.index(self)
			for b in bases[i+1:]:
				if isinstance(b,_BaseGenericAlias)and b is not self:return()
		return self.__origin__,
class _SpecialGenericAlias(_BaseGenericAlias,_root=_B):
	def __init__(self,origin,nparams,*,inst=_B,name=_A):
		if name is _A:name=origin.__name__
		super().__init__(origin,inst=inst,name=name);self._nparams=nparams
		if origin.__module__==_o:self.__doc__=f"A generic version of {origin.__qualname__}."
		else:self.__doc__=f"A generic version of {origin.__module__}.{origin.__qualname__}."
	@_tp_cache
	def __getitem__(self,params):
		if not isinstance(params,tuple):params=params,
		msg='Parameters to generic types must be types.';params=tuple(_type_check(p,msg)for p in params);_check_generic(self,params,self._nparams);return self.copy_with(params)
	def copy_with(self,params):return _GenericAlias(self.__origin__,params,name=self._name,inst=self._inst)
	def __repr__(self):return _N+self._name
	def __subclasscheck__(self,cls):
		if isinstance(cls,_SpecialGenericAlias):return issubclass(cls.__origin__,self.__origin__)
		if not isinstance(cls,_GenericAlias):return issubclass(cls,self.__origin__)
		return super().__subclasscheck__(cls)
	def __reduce__(self):return self._name
	def __or__(self,right):return Union[self,right]
	def __ror__(self,left):return Union[left,self]
class _CallableGenericAlias(_GenericAlias,_root=_B):
	def __repr__(self):
		assert self._name==_K;args=self.__args__
		if len(args)==2 and _is_param_expr(args[0]):return super().__repr__()
		return f"typing.Callable[[{_F.join([_type_repr(a)for a in args[:-1]])}], {_type_repr(args[-1])}]"
	def __reduce__(self):
		args=self.__args__
		if not(len(args)==2 and _is_param_expr(args[0])):args=list(args[:-1]),args[-1]
		return operator.getitem,(Callable,args)
class _CallableType(_SpecialGenericAlias,_root=_B):
	def copy_with(self,params):return _CallableGenericAlias(self.__origin__,params,name=self._name,inst=self._inst,_typevar_types=(TypeVar,ParamSpec),_paramspec_tvars=_B)
	def __getitem__(self,params):
		if not isinstance(params,tuple)or len(params)!=2:raise TypeError('Callable must be used as Callable[[arg, ...], result].')
		args,result=params
		if isinstance(args,list):params=tuple(args),result
		else:params=args,result
		return self.__getitem_inner__(params)
	@_tp_cache
	def __getitem_inner__(self,params):
		args,result=params;msg='Callable[args, result]: result must be a type.';result=_type_check(result,msg)
		if args is Ellipsis:return self.copy_with((_TypingEllipsis,result))
		if not isinstance(args,tuple):args=args,
		args=tuple(_type_convert(arg)for arg in args);params=args+(result,);return self.copy_with(params)
class _TupleType(_SpecialGenericAlias,_root=_B):
	@_tp_cache
	def __getitem__(self,params):
		if params==():return self.copy_with((_TypingEmpty,))
		if not isinstance(params,tuple):params=params,
		if len(params)==2 and params[1]is...:msg='Tuple[t, ...]: t must be a type.';p=_type_check(params[0],msg);return self.copy_with((p,_TypingEllipsis))
		msg='Tuple[t0, t1, ...]: each t must be a type.';params=tuple(_type_check(p,msg)for p in params);return self.copy_with(params)
class _UnionGenericAlias(_GenericAlias,_root=_B):
	def copy_with(self,params):return Union[params]
	def __eq__(self,other):
		if not isinstance(other,(_UnionGenericAlias,types.UnionType)):return NotImplemented
		return set(self.__args__)==set(other.__args__)
	def __hash__(self):return hash(frozenset(self.__args__))
	def __repr__(self):
		args=self.__args__
		if len(args)==2:
			if args[0]is type(_A):return f"typing.Optional[{_type_repr(args[1])}]"
			elif args[1]is type(_A):return f"typing.Optional[{_type_repr(args[0])}]"
		return super().__repr__()
	def __instancecheck__(self,obj):return self.__subclasscheck__(type(obj))
	def __subclasscheck__(self,cls):
		for arg in self.__args__:
			if issubclass(cls,arg):return _B
	def __reduce__(self):func,(origin,args)=super().__reduce__();return func,(Union,args)
def _value_and_type_iter(parameters):return((p,type(p))for p in parameters)
class _LiteralGenericAlias(_GenericAlias,_root=_B):
	def __eq__(self,other):
		if not isinstance(other,_LiteralGenericAlias):return NotImplemented
		return set(_value_and_type_iter(self.__args__))==set(_value_and_type_iter(other.__args__))
	def __hash__(self):return hash(frozenset(_value_and_type_iter(self.__args__)))
class _ConcatenateGenericAlias(_GenericAlias,_root=_B):
	def copy_with(self,params):
		if isinstance(params[-1],(list,tuple)):return*params[:-1],*params[-1]
		if isinstance(params[-1],_ConcatenateGenericAlias):params=*params[:-1],*params[-1].__args__
		elif not isinstance(params[-1],ParamSpec):raise TypeError(_r)
		return super().copy_with(params)
class Generic:
	'Abstract base class for generic types.\n\n    A generic type is typically declared by inheriting from\n    this class parameterized with one or more type variables.\n    For example, a generic mapping type might be defined as::\n\n      class Mapping(Generic[KT, VT]):\n          def __getitem__(self, key: KT) -> VT:\n              ...\n          # Etc.\n\n    This class can then be used as follows::\n\n      def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:\n          try:\n              return mapping[key]\n          except KeyError:\n              return default\n    ';__slots__=();_is_protocol=_C
	@_tp_cache
	def __class_getitem__(cls,params):
		if not isinstance(params,tuple):params=params,
		if not params and cls is not Tuple:raise TypeError(f"Parameter list to {cls.__qualname__}[...] cannot be empty")
		params=tuple(_type_convert(p)for p in params)
		if cls in(Generic,Protocol):
			if not all(isinstance(p,(TypeVar,ParamSpec))for p in params):raise TypeError(f"Parameters to {cls.__name__}[...] must all be type variables or parameter specification variables.")
			if len(set(params))!=len(params):raise TypeError(f"Parameters to {cls.__name__}[...] must all be unique")
		elif any(isinstance(t,ParamSpec)for t in cls.__parameters__):params=_prepare_paramspec_params(cls,params)
		else:_check_generic(cls,params,len(cls.__parameters__))
		return _GenericAlias(cls,params,_typevar_types=(TypeVar,ParamSpec),_paramspec_tvars=_B)
	def __init_subclass__(cls,*args,**kwargs):
		super().__init_subclass__(*args,**kwargs);tvars=[]
		if _P in cls.__dict__:error=Generic in cls.__orig_bases__
		else:error=Generic in cls.__bases__ and cls.__name__!=_L
		if error:raise TypeError('Cannot inherit from plain Generic')
		if _P in cls.__dict__:
			tvars=_collect_type_vars(cls.__orig_bases__,(TypeVar,ParamSpec));gvars=_A
			for base in cls.__orig_bases__:
				if isinstance(base,_GenericAlias)and base.__origin__ is Generic:
					if gvars is not _A:raise TypeError('Cannot inherit from Generic[...] multiple types.')
					gvars=base.__parameters__
			if gvars is not _A:
				tvarset=set(tvars);gvarset=set(gvars)
				if not tvarset<=gvarset:s_vars=_F.join(str(t)for t in tvars if t not in gvarset);s_args=_F.join(str(g)for g in gvars);raise TypeError(f"Some type variables ({s_vars}) are not listed in Generic[{s_args}]")
				tvars=gvars
		cls.__parameters__=tuple(tvars)
class _TypingEmpty:'Internal placeholder for () or []. Used by TupleMeta and CallableMeta\n    to allow empty list/tuple in specific places, without allowing them\n    to sneak in where prohibited.\n    '
class _TypingEllipsis:'Internal placeholder for ... (ellipsis).'
_TYPING_INTERNALS=['__parameters__',_P,'__orig_class__',_I,_Q]
_SPECIAL_NAMES=['__abstractmethods__',_E,_G,_q,_R,_J,_v,_w,_x,_p,'__class_getitem__']
EXCLUDED_ATTRIBUTES=_TYPING_INTERNALS+_SPECIAL_NAMES+['_MutableMapping__marker']
def _get_protocol_attrs(cls):
	'Collect protocol members from a protocol class objects.\n\n    This includes names actually defined in the class dictionary, as well\n    as names that appear in annotations. Special names (above) are skipped.\n    ';attrs=set()
	for base in cls.__mro__[:-1]:
		if base.__name__ in(_L,_T):continue
		annotations=getattr(base,_E,{})
		for attr in list(base.__dict__.keys())+list(annotations.keys()):
			if not attr.startswith('_abc_')and attr not in EXCLUDED_ATTRIBUTES:attrs.add(attr)
	return attrs
def _is_callable_members_only(cls):return all(callable(getattr(cls,attr,_A))for attr in _get_protocol_attrs(cls))
def _no_init_or_replace_init(self,*args,**kwargs):
	cls=type(self)
	if cls._is_protocol:raise TypeError('Protocols cannot be instantiated')
	if cls.__init__ is not _no_init_or_replace_init:return
	for base in cls.__mro__:
		init=base.__dict__.get(_R,_no_init_or_replace_init)
		if init is not _no_init_or_replace_init:cls.__init__=init;break
	else:cls.__init__=object.__init__
	cls.__init__(self,*args,**kwargs)
def _caller(depth=1,default=_H):
	try:return sys._getframe(depth+1).f_globals.get(_D,default)
	except(AttributeError,ValueError):return
def _allow_reckless_class_checks(depth=3):
	'Allow instance and class checks for special stdlib modules.\n\n    The abc and functools modules indiscriminately call isinstance() and\n    issubclass() on the whole MRO of a user class, which may contain protocols.\n    '
	try:return sys._getframe(depth).f_globals[_D]in['abc','functools']
	except(AttributeError,ValueError):return _B
_PROTO_ALLOWLIST={'collections.abc':[_K,_b,_Z,_a,_c,_Y,'Sized',_W,_d,_f],'contextlib':['AbstractContextManager','AbstractAsyncContextManager']}
class _ProtocolMeta(ABCMeta):
	def __instancecheck__(cls,instance):
		if getattr(cls,_I,_C)and not getattr(cls,_Q,_C)and not _allow_reckless_class_checks(depth=2):raise TypeError(_y)
		if(not getattr(cls,_I,_C)or _is_callable_members_only(cls))and issubclass(instance.__class__,cls):return _B
		if cls._is_protocol:
			if all(hasattr(instance,attr)and(not callable(getattr(cls,attr,_A))or getattr(instance,attr)is not _A)for attr in _get_protocol_attrs(cls)):return _B
		return super().__instancecheck__(instance)
class Protocol(Generic,metaclass=_ProtocolMeta):
	'Base class for protocol classes.\n\n    Protocol classes are defined as::\n\n        class Proto(Protocol):\n            def meth(self) -> int:\n                ...\n\n    Such classes are primarily used with static type checkers that recognize\n    structural subtyping (static duck-typing), for example::\n\n        class C:\n            def meth(self) -> int:\n                return 0\n\n        def func(x: Proto) -> int:\n            return x.meth()\n\n        func(C())  # Passes static type check\n\n    See PEP 544 for details. Protocol classes decorated with\n    @typing.runtime_checkable act as simple-minded runtime protocols that check\n    only the presence of given attributes, ignoring their type signatures.\n    Protocol classes can be generic, they are defined as::\n\n        class GenProto(Protocol[T]):\n            def meth(self) -> T:\n                ...\n    ';__slots__=();_is_protocol=_B;_is_runtime_protocol=_C
	def __init_subclass__(cls,*args,**kwargs):
		super().__init_subclass__(*args,**kwargs)
		if not cls.__dict__.get(_I,_C):cls._is_protocol=any(b is Protocol for b in cls.__bases__)
		def _proto_hook(other):
			if not cls.__dict__.get(_I,_C):return NotImplemented
			if not getattr(cls,_Q,_C):
				if _allow_reckless_class_checks():return NotImplemented
				raise TypeError(_y)
			if not _is_callable_members_only(cls):
				if _allow_reckless_class_checks():return NotImplemented
				raise TypeError("Protocols with non-method members don't support issubclass()")
			if not isinstance(other,type):raise TypeError('issubclass() arg 1 must be a class')
			for attr in _get_protocol_attrs(cls):
				for base in other.__mro__:
					if attr in base.__dict__:
						if base.__dict__[attr]is _A:return NotImplemented
						break
					annotations=getattr(base,_E,{})
					if isinstance(annotations,collections.abc.Mapping)and attr in annotations and issubclass(other,Generic)and other._is_protocol:break
				else:return NotImplemented
			return _B
		if _x not in cls.__dict__:cls.__subclasshook__=_proto_hook
		if not cls._is_protocol:return
		for base in cls.__bases__:
			if not(base in(object,Generic)or base.__module__ in _PROTO_ALLOWLIST and base.__name__ in _PROTO_ALLOWLIST[base.__module__]or issubclass(base,Generic)and base._is_protocol):raise TypeError('Protocols can only inherit from other protocols, got %r'%base)
		cls.__init__=_no_init_or_replace_init
class _AnnotatedAlias(_GenericAlias,_root=_B):
	"Runtime representation of an annotated type.\n\n    At its core 'Annotated[t, dec1, dec2, ...]' is an alias for the type 't'\n    with extra annotations. The alias behaves like a normal typing alias,\n    instantiating is the same as instantiating the underlying type, binding\n    it to types is also the same.\n    "
	def __init__(self,origin,metadata):
		if isinstance(origin,_AnnotatedAlias):metadata=origin.__metadata__+metadata;origin=origin.__origin__
		super().__init__(origin,origin);self.__metadata__=metadata
	def copy_with(self,params):assert len(params)==1;new_type=params[0];return _AnnotatedAlias(new_type,self.__metadata__)
	def __repr__(self):return'typing.Annotated[{}, {}]'.format(_type_repr(self.__origin__),_F.join(repr(a)for a in self.__metadata__))
	def __reduce__(self):return operator.getitem,(Annotated,(self.__origin__,)+self.__metadata__)
	def __eq__(self,other):
		if not isinstance(other,_AnnotatedAlias):return NotImplemented
		return self.__origin__==other.__origin__ and self.__metadata__==other.__metadata__
	def __hash__(self):return hash((self.__origin__,self.__metadata__))
	def __getattr__(self,attr):
		if attr in{_D,_M}:return _S
		return super().__getattr__(attr)
class Annotated:
	"Add context specific metadata to a type.\n\n    Example: Annotated[int, runtime_check.Unsigned] indicates to the\n    hypothetical runtime_check module that this type is an unsigned int.\n    Every other consumer of this type can ignore this metadata and treat\n    this type as int.\n\n    The first argument to Annotated must be a valid type.\n\n    Details:\n\n    - It's an error to call `Annotated` with less than two arguments.\n    - Nested Annotated are flattened::\n\n        Annotated[Annotated[T, Ann1, Ann2], Ann3] == Annotated[T, Ann1, Ann2, Ann3]\n\n    - Instantiating an annotated type is equivalent to instantiating the\n    underlying type::\n\n        Annotated[C, Ann1](5) == C(5)\n\n    - Annotated can be used as a generic type alias::\n\n        Optimized = Annotated[T, runtime.Optimize()]\n        Optimized[int] == Annotated[int, runtime.Optimize()]\n\n        OptimizedList = Annotated[List[T], runtime.Optimize()]\n        OptimizedList[int] == Annotated[List[int], runtime.Optimize()]\n    ";__slots__=()
	def __new__(cls,*args,**kwargs):raise TypeError('Type Annotated cannot be instantiated.')
	@_tp_cache
	def __class_getitem__(cls,params):
		if not isinstance(params,tuple)or len(params)<2:raise TypeError('Annotated[...] should be used with at least two arguments (a type and an annotation).')
		msg='Annotated[t, ...]: t must be a type.';origin=_type_check(params[0],msg,allow_special_forms=_B);metadata=tuple(params[1:]);return _AnnotatedAlias(origin,metadata)
	def __init_subclass__(cls,*args,**kwargs):raise TypeError('Cannot subclass {}.Annotated'.format(cls.__module__))
def runtime_checkable(cls):
	"Mark a protocol class as a runtime protocol.\n\n    Such protocol can be used with isinstance() and issubclass().\n    Raise TypeError if applied to a non-protocol class.\n    This allows a simple-minded structural check very similar to\n    one trick ponies in collections.abc such as Iterable.\n    For example::\n\n        @runtime_checkable\n        class Closable(Protocol):\n            def close(self): ...\n\n        assert isinstance(open('/some/file'), Closable)\n\n    Warning: this will check only the presence of the required methods,\n    not their type signatures!\n    "
	if not issubclass(cls,Generic)or not cls._is_protocol:raise TypeError('@runtime_checkable can be only applied to protocol classes, got %r'%cls)
	cls._is_runtime_protocol=_B;return cls
def cast(typ,val):"Cast a value to a type.\n\n    This returns the value unchanged.  To the type checker this\n    signals that the return value has the designated type, but at\n    runtime we intentionally don't check anything (we want this\n    to be as fast as possible).\n    ";return val
def _get_defaults(func):
	'Internal helper to extract the default arguments, by name.'
	try:code=func.__code__
	except AttributeError:return{}
	pos_count=code.co_argcount;arg_names=code.co_varnames;arg_names=arg_names[:pos_count];defaults=func.__defaults__ or();kwdefaults=func.__kwdefaults__;res=dict(kwdefaults)if kwdefaults else{};pos_offset=pos_count-len(defaults)
	for(name,value)in zip(arg_names[pos_offset:],defaults):assert name not in res;res[name]=value
	return res
_allowed_types=types.FunctionType,types.BuiltinFunctionType,types.MethodType,types.ModuleType,WrapperDescriptorType,MethodWrapperType,MethodDescriptorType
def get_type_hints(obj,globalns=_A,localns=_A,include_extras=_C):
	"Return type hints for an object.\n\n    This is often the same as obj.__annotations__, but it handles\n    forward references encoded as string literals, adds Optional[t] if a\n    default value equal to None is set and recursively replaces all\n    'Annotated[T, ...]' with 'T' (unless 'include_extras=True').\n\n    The argument may be a module, class, method, or function. The annotations\n    are returned as a dictionary. For classes, annotations include also\n    inherited members.\n\n    TypeError is raised if the argument is not of a type that can contain\n    annotations, and an empty dictionary is returned if no annotations are\n    present.\n\n    BEWARE -- the behavior of globalns and localns is counterintuitive\n    (unless you are familiar with how eval() and exec() work).  The\n    search order is locals first, then globals.\n\n    - If no dict arguments are passed, an attempt is made to use the\n      globals from obj (or the respective module's globals for classes),\n      and these are also used as the locals.  If the object does not appear\n      to have globals, an empty dictionary is used.  For classes, the search\n      order is globals first then locals.\n\n    - If one dict argument is passed, it is used for both globals and\n      locals.\n\n    - If two dict arguments are passed, they specify globals and\n      locals, respectively.\n    "
	if getattr(obj,'__no_type_check__',_A):return{}
	if isinstance(obj,type):
		hints={}
		for base in reversed(obj.__mro__):
			if globalns is _A:base_globals=getattr(sys.modules.get(base.__module__,_A),_G,{})
			else:base_globals=globalns
			ann=base.__dict__.get(_E,{})
			if isinstance(ann,types.GetSetDescriptorType):ann={}
			base_locals=dict(vars(base))if localns is _A else localns
			if localns is _A and globalns is _A:base_globals,base_locals=base_locals,base_globals
			for(name,value)in ann.items():
				if value is _A:value=type(_A)
				if isinstance(value,str):value=ForwardRef(value,is_argument=_C,is_class=_B)
				value=_eval_type(value,base_globals,base_locals);hints[name]=value
		return hints if include_extras else{k:_strip_annotations(t)for(k,t)in hints.items()}
	if globalns is _A:
		if isinstance(obj,types.ModuleType):globalns=obj.__dict__
		else:
			nsobj=obj
			while hasattr(nsobj,'__wrapped__'):nsobj=nsobj.__wrapped__
			globalns=getattr(nsobj,'__globals__',{})
		if localns is _A:localns=globalns
	elif localns is _A:localns=globalns
	hints=getattr(obj,_E,_A)
	if hints is _A:
		if isinstance(obj,_allowed_types):return{}
		else:raise TypeError('{!r} is not a module, class, method, or function.'.format(obj))
	defaults=_get_defaults(obj);hints=dict(hints)
	for(name,value)in hints.items():
		if value is _A:value=type(_A)
		if isinstance(value,str):value=ForwardRef(value,is_argument=not isinstance(obj,types.ModuleType),is_class=_C)
		value=_eval_type(value,globalns,localns)
		if name in defaults and defaults[name]is _A:value=Optional[value]
		hints[name]=value
	return hints if include_extras else{k:_strip_annotations(t)for(k,t)in hints.items()}
def _strip_annotations(t):
	'Strips the annotations from a given type.\n    '
	if isinstance(t,_AnnotatedAlias):return _strip_annotations(t.__origin__)
	if isinstance(t,_GenericAlias):
		stripped_args=tuple(_strip_annotations(a)for a in t.__args__)
		if stripped_args==t.__args__:return t
		return t.copy_with(stripped_args)
	if isinstance(t,GenericAlias):
		stripped_args=tuple(_strip_annotations(a)for a in t.__args__)
		if stripped_args==t.__args__:return t
		return GenericAlias(t.__origin__,stripped_args)
	if isinstance(t,types.UnionType):
		stripped_args=tuple(_strip_annotations(a)for a in t.__args__)
		if stripped_args==t.__args__:return t
		return functools.reduce(operator.or_,stripped_args)
	return t
def get_origin(tp):
	'Get the unsubscripted version of a type.\n\n    This supports generic types, Callable, Tuple, Union, Literal, Final, ClassVar\n    and Annotated. Return None for unsupported types. Examples::\n\n        get_origin(Literal[42]) is Literal\n        get_origin(int) is None\n        get_origin(ClassVar[int]) is ClassVar\n        get_origin(Generic) is Generic\n        get_origin(Generic[T]) is Generic\n        get_origin(Union[T, int]) is Union\n        get_origin(List[Tuple[T, T]][int]) == list\n        get_origin(P.args) is P\n    '
	if isinstance(tp,_AnnotatedAlias):return Annotated
	if isinstance(tp,(_BaseGenericAlias,GenericAlias,ParamSpecArgs,ParamSpecKwargs)):return tp.__origin__
	if tp is Generic:return Generic
	if isinstance(tp,types.UnionType):return types.UnionType
def get_args(tp):
	'Get type arguments with all substitutions performed.\n\n    For unions, basic simplifications used by Union constructor are performed.\n    Examples::\n        get_args(Dict[str, int]) == (str, int)\n        get_args(int) == ()\n        get_args(Union[int, Union[T, int], str][int]) == (int, str)\n        get_args(Union[int, Tuple[T, int]][str]) == (int, Tuple[str, int])\n        get_args(Callable[[], T][int]) == ([], int)\n    '
	if isinstance(tp,_AnnotatedAlias):return(tp.__origin__,)+tp.__metadata__
	if isinstance(tp,(_GenericAlias,GenericAlias)):
		res=tp.__args__
		if tp.__origin__ is collections.abc.Callable and not(len(res)==2 and _is_param_expr(res[0])):res=list(res[:-1]),res[-1]
		return res
	if isinstance(tp,types.UnionType):return tp.__args__
	return()
def is_typeddict(tp):'Check if an annotation is a TypedDict class\n\n    For example::\n        class Film(TypedDict):\n            title: str\n            year: int\n\n        is_typeddict(Film)  # => True\n        is_typeddict(Union[list, str])  # => False\n    ';return isinstance(tp,_TypedDictMeta)
def no_type_check(arg):
	'Decorator to indicate that annotations are not type hints.\n\n    The argument must be a class or function; if it is a class, it\n    applies recursively to all methods and classes defined in that class\n    (but not to methods defined in its superclasses or subclasses).\n\n    This mutates the function(s) or class(es) in place.\n    '
	if isinstance(arg,type):
		arg_attrs=arg.__dict__.copy()
		for(attr,val)in arg.__dict__.items():
			if val in arg.__bases__+(arg,):arg_attrs.pop(attr)
		for obj in arg_attrs.values():
			if isinstance(obj,types.FunctionType):obj.__no_type_check__=_B
			if isinstance(obj,type):no_type_check(obj)
	try:arg.__no_type_check__=_B
	except TypeError:pass
	return arg
def no_type_check_decorator(decorator):
	'Decorator to give another decorator the @no_type_check effect.\n\n    This wraps the decorator with something that wraps the decorated\n    function in @no_type_check.\n    '
	@functools.wraps(decorator)
	def wrapped_decorator(*args,**kwds):func=decorator(*args,**kwds);func=no_type_check(func);return func
	return wrapped_decorator
def _overload_dummy(*args,**kwds):'Helper for @overload to raise when called.';raise NotImplementedError('You should not call an overloaded function. A series of @overload-decorated functions outside a stub module should always be followed by an implementation that is not @overload-ed.')
def overload(func):'Decorator for overloaded functions/methods.\n\n    In a stub file, place two or more stub definitions for the same\n    function in a row, each decorated with @overload.  For example:\n\n      @overload\n      def utf8(value: None) -> None: ...\n      @overload\n      def utf8(value: bytes) -> bytes: ...\n      @overload\n      def utf8(value: str) -> bytes: ...\n\n    In a non-stub file (i.e. a regular .py file), do the same but\n    follow it with an implementation.  The implementation should *not*\n    be decorated with @overload.  For example:\n\n      @overload\n      def utf8(value: None) -> None: ...\n      @overload\n      def utf8(value: bytes) -> bytes: ...\n      @overload\n      def utf8(value: str) -> bytes: ...\n      def utf8(value):\n          # implementation goes here\n    ';return _overload_dummy
def final(f):'A decorator to indicate final methods and final classes.\n\n    Use this decorator to indicate to type checkers that the decorated\n    method cannot be overridden, and decorated class cannot be subclassed.\n    For example:\n\n      class Base:\n          @final\n          def done(self) -> None:\n              ...\n      class Sub(Base):\n          def done(self) -> None:  # Error reported by type checker\n                ...\n\n      @final\n      class Leaf:\n          ...\n      class Other(Leaf):  # Error reported by type checker\n          ...\n\n    There is no runtime checking of these properties.\n    ';return f
T=TypeVar('T')
KT=TypeVar('KT')
VT=TypeVar('VT')
T_co=TypeVar('T_co',covariant=_B)
V_co=TypeVar('V_co',covariant=_B)
VT_co=TypeVar('VT_co',covariant=_B)
T_contra=TypeVar('T_contra',contravariant=_B)
CT_co=TypeVar('CT_co',covariant=_B,bound=type)
AnyStr=TypeVar(_n,bytes,str)
_alias=_SpecialGenericAlias
Hashable=_alias(collections.abc.Hashable,0)
Awaitable=_alias(collections.abc.Awaitable,1)
Coroutine=_alias(collections.abc.Coroutine,3)
AsyncIterable=_alias(collections.abc.AsyncIterable,1)
AsyncIterator=_alias(collections.abc.AsyncIterator,1)
Iterable=_alias(collections.abc.Iterable,1)
Iterator=_alias(collections.abc.Iterator,1)
Reversible=_alias(collections.abc.Reversible,1)
Sized=_alias(collections.abc.Sized,0)
Container=_alias(collections.abc.Container,1)
Collection=_alias(collections.abc.Collection,1)
Callable=_CallableType(collections.abc.Callable,2)
Callable.__doc__='Callable type; Callable[[int], str] is a function of (int) -> str.\n\n    The subscription syntax must always be used with exactly two\n    values: the argument list and the return type.  The argument list\n    must be a list of types or ellipsis; the return type must be a single type.\n\n    There is no syntax to indicate optional or keyword arguments,\n    such function types are rarely used as callback types.\n    '
AbstractSet=_alias(collections.abc.Set,1,name=_V)
MutableSet=_alias(collections.abc.MutableSet,1)
Mapping=_alias(collections.abc.Mapping,2)
MutableMapping=_alias(collections.abc.MutableMapping,2)
Sequence=_alias(collections.abc.Sequence,1)
MutableSequence=_alias(collections.abc.MutableSequence,1)
ByteString=_alias(collections.abc.ByteString,0)
Tuple=_TupleType(tuple,-1,inst=_C,name='Tuple')
Tuple.__doc__='Tuple type; Tuple[X, Y] is the cross-product type of X and Y.\n\n    Example: Tuple[T1, T2] is a tuple of two elements corresponding\n    to type variables T1 and T2.  Tuple[int, float, str] is a tuple\n    of an int, a float and a string.\n\n    To specify a variable-length tuple of homogeneous type, use Tuple[T, ...].\n    '
List=_alias(list,1,inst=_C,name='List')
Deque=_alias(collections.deque,1,name='Deque')
Set=_alias(set,1,inst=_C,name='Set')
FrozenSet=_alias(frozenset,1,inst=_C,name=_h)
MappingView=_alias(collections.abc.MappingView,1)
KeysView=_alias(collections.abc.KeysView,1)
ItemsView=_alias(collections.abc.ItemsView,2)
ValuesView=_alias(collections.abc.ValuesView,1)
ContextManager=_alias(contextlib.AbstractContextManager,1,name=_X)
AsyncContextManager=_alias(contextlib.AbstractAsyncContextManager,1,name=_e)
Dict=_alias(dict,2,inst=_C,name='Dict')
DefaultDict=_alias(collections.defaultdict,2,name=_g)
OrderedDict=_alias(collections.OrderedDict,2)
Counter=_alias(collections.Counter,1)
ChainMap=_alias(collections.ChainMap,2)
Generator=_alias(collections.abc.Generator,3)
AsyncGenerator=_alias(collections.abc.AsyncGenerator,2)
Type=_alias(type,1,inst=_C,name='Type')
Type.__doc__="A special construct usable to annotate class objects.\n\n    For example, suppose we have the following classes::\n\n      class User: ...  # Abstract base for User classes\n      class BasicUser(User): ...\n      class ProUser(User): ...\n      class TeamUser(User): ...\n\n    And a function that takes a class argument that's a subclass of\n    User and returns an instance of the corresponding class::\n\n      U = TypeVar('U', bound=User)\n      def new_user(user_class: Type[U]) -> U:\n          user = user_class()\n          # (Here we could write the user object to a database)\n          return user\n\n      joe = new_user(BasicUser)\n\n    At this point the type checker knows that joe has type BasicUser.\n    "
@runtime_checkable
class SupportsInt(Protocol):
	'An ABC with one abstract method __int__.';__slots__=()
	@abstractmethod
	def __int__(self):0
@runtime_checkable
class SupportsFloat(Protocol):
	'An ABC with one abstract method __float__.';__slots__=()
	@abstractmethod
	def __float__(self):0
@runtime_checkable
class SupportsComplex(Protocol):
	'An ABC with one abstract method __complex__.';__slots__=()
	@abstractmethod
	def __complex__(self):0
@runtime_checkable
class SupportsBytes(Protocol):
	'An ABC with one abstract method __bytes__.';__slots__=()
	@abstractmethod
	def __bytes__(self):0
@runtime_checkable
class SupportsIndex(Protocol):
	'An ABC with one abstract method __index__.';__slots__=()
	@abstractmethod
	def __index__(self):0
@runtime_checkable
class SupportsAbs(Protocol[T_co]):
	'An ABC with one abstract method __abs__ that is covariant in its return type.';__slots__=()
	@abstractmethod
	def __abs__(self):0
@runtime_checkable
class SupportsRound(Protocol[T_co]):
	'An ABC with one abstract method __round__ that is covariant in its return type.';__slots__=()
	@abstractmethod
	def __round__(self,ndigits=0):0
def _make_nmtuple(name,types,module,defaults=()):fields=[n for(n,t)in types];types={n:_type_check(t,f"field {n} annotation must be a type")for(n,t)in types};nm_tpl=collections.namedtuple(name,fields,defaults=defaults,module=module);nm_tpl.__annotations__=nm_tpl.__new__.__annotations__=types;return nm_tpl
_prohibited=frozenset({_v,_R,_w,'__getnewargs__','_fields','_field_defaults','_make','_replace','_asdict','_source'})
_special=frozenset({_J,_D,_E})
class NamedTupleMeta(type):
	def __new__(cls,typename,bases,ns):
		assert bases[0]is _NamedTuple;types=ns.get(_E,{});default_names=[]
		for field_name in types:
			if field_name in ns:default_names.append(field_name)
			elif default_names:raise TypeError(f"Non-default namedtuple field {field_name} cannot follow default field{'s'if len(default_names)>1 else''} {_F.join(default_names)}")
		nm_tpl=_make_nmtuple(typename,types.items(),defaults=[ns[n]for n in default_names],module=ns[_J])
		for key in ns:
			if key in _prohibited:raise AttributeError('Cannot overwrite NamedTuple attribute '+key)
			elif key not in _special and key not in nm_tpl._fields:setattr(nm_tpl,key,ns[key])
		return nm_tpl
def NamedTuple(typename,fields=_A,**kwargs):
	"Typed version of namedtuple.\n\n    Usage in Python versions >= 3.6::\n\n        class Employee(NamedTuple):\n            name: str\n            id: int\n\n    This is equivalent to::\n\n        Employee = collections.namedtuple('Employee', ['name', 'id'])\n\n    The resulting class has an extra __annotations__ attribute, giving a\n    dict that maps field names to types.  (The field names are also in\n    the _fields attribute, which is part of the namedtuple API.)\n    Alternative equivalent keyword syntax is also accepted::\n\n        Employee = NamedTuple('Employee', name=str, id=int)\n\n    In Python versions <= 3.5 use::\n\n        Employee = NamedTuple('Employee', [('name', str), ('id', int)])\n    "
	if fields is _A:fields=kwargs.items()
	elif kwargs:raise TypeError('Either list of fields or keywords can be provided to NamedTuple, not both')
	try:module=sys._getframe(1).f_globals.get(_D,_H)
	except(AttributeError,ValueError):module=_A
	return _make_nmtuple(typename,fields,module=module)
_NamedTuple=type.__new__(NamedTupleMeta,_i,(),{})
def _namedtuple_mro_entries(bases):
	if len(bases)>1:raise TypeError('Multiple inheritance with NamedTuple is not supported')
	assert bases[0]is NamedTuple;return _NamedTuple,
NamedTuple.__mro_entries__=_namedtuple_mro_entries
class _TypedDictMeta(type):
	def __new__(cls,name,bases,ns,total=_B):
		'Create new typed dict class object.\n\n        This method is called when TypedDict is subclassed,\n        or when TypedDict is instantiated. This way\n        TypedDict supports all three syntax forms described in its docstring.\n        Subclasses and instances of TypedDict return actual dictionaries.\n        '
		for base in bases:
			if type(base)is not _TypedDictMeta:raise TypeError('cannot inherit from both a TypedDict type and a non-TypedDict base class')
		tp_dict=type.__new__(_TypedDictMeta,name,(dict,),ns);annotations={};own_annotations=ns.get(_E,{});own_annotation_keys=set(own_annotations.keys());msg="TypedDict('Name', {f0: t0, f1: t1, ...}); each t must be a type";own_annotations={n:_type_check(tp,msg,module=tp_dict.__module__)for(n,tp)in own_annotations.items()};required_keys=set();optional_keys=set()
		for base in bases:annotations.update(base.__dict__.get(_E,{}));required_keys.update(base.__dict__.get('__required_keys__',()));optional_keys.update(base.__dict__.get('__optional_keys__',()))
		annotations.update(own_annotations)
		if total:required_keys.update(own_annotation_keys)
		else:optional_keys.update(own_annotation_keys)
		tp_dict.__annotations__=annotations;tp_dict.__required_keys__=frozenset(required_keys);tp_dict.__optional_keys__=frozenset(optional_keys)
		if not hasattr(tp_dict,'__total__'):tp_dict.__total__=total
		return tp_dict
	__call__=dict
	def __subclasscheck__(cls,other):raise TypeError('TypedDict does not support instance and class checks')
	__instancecheck__=__subclasscheck__
def TypedDict(typename,fields=_A,*,total=_B,**kwargs):
	"A simple typed namespace. At runtime it is equivalent to a plain dict.\n\n    TypedDict creates a dictionary type that expects all of its\n    instances to have a certain set of keys, where each key is\n    associated with a value of a consistent type. This expectation\n    is not checked at runtime but is only enforced by type checkers.\n    Usage::\n\n        class Point2D(TypedDict):\n            x: int\n            y: int\n            label: str\n\n        a: Point2D = {'x': 1, 'y': 2, 'label': 'good'}  # OK\n        b: Point2D = {'z': 3, 'label': 'bad'}           # Fails type check\n\n        assert Point2D(x=1, y=2, label='first') == dict(x=1, y=2, label='first')\n\n    The type info can be accessed via the Point2D.__annotations__ dict, and\n    the Point2D.__required_keys__ and Point2D.__optional_keys__ frozensets.\n    TypedDict supports two additional equivalent forms::\n\n        Point2D = TypedDict('Point2D', x=int, y=int, label=str)\n        Point2D = TypedDict('Point2D', {'x': int, 'y': int, 'label': str})\n\n    By default, all keys must be present in a TypedDict. It is possible\n    to override this by specifying totality.\n    Usage::\n\n        class point2D(TypedDict, total=False):\n            x: int\n            y: int\n\n    This means that a point2D TypedDict can have any of the keys omitted.A type\n    checker is only expected to support a literal False or True as the value of\n    the total argument. True is the default, and makes all items defined in the\n    class body be required.\n\n    The class syntax is only supported in Python 3.6+, while two other\n    syntax forms work for Python 2.7 and 3.2+\n    "
	if fields is _A:fields=kwargs
	elif kwargs:raise TypeError('TypedDict takes either a dict or keyword arguments, but not both')
	ns={_E:dict(fields)}
	try:ns[_J]=sys._getframe(1).f_globals.get(_D,_H)
	except(AttributeError,ValueError):pass
	return _TypedDictMeta(typename,(),ns,total=total)
_TypedDict=type.__new__(_TypedDictMeta,_j,(),{})
TypedDict.__mro_entries__=lambda bases:(_TypedDict,)
class NewType:
	"NewType creates simple unique types with almost zero\n    runtime overhead. NewType(name, tp) is considered a subtype of tp\n    by static type checkers. At runtime, NewType(name, tp) returns\n    a dummy callable that simply returns its argument. Usage::\n\n        UserId = NewType('UserId', int)\n\n        def name_by_id(user_id: UserId) -> str:\n            ...\n\n        UserId('user')          # Fails type check\n\n        name_by_id(42)          # Fails type check\n        name_by_id(UserId(42))  # OK\n\n        num = UserId(5) + 1     # type: int\n    "
	def __init__(self,name,tp):
		self.__qualname__=name
		if'.'in name:name=name.rpartition('.')[-1]
		self.__name__=name;self.__supertype__=tp;def_mod=_caller()
		if def_mod!=_O:self.__module__=def_mod
	def __repr__(self):return f"{self.__module__}.{self.__qualname__}"
	def __call__(self,x):return x
	def __reduce__(self):return self.__qualname__
	def __or__(self,other):return Union[self,other]
	def __ror__(self,other):return Union[other,self]
Text=str
TYPE_CHECKING=_C
class IO(Generic[AnyStr]):
	'Generic base class for TextIO and BinaryIO.\n\n    This is an abstract, generic version of the return of open().\n\n    NOTE: This does not distinguish between the different possible\n    classes (text vs. binary, read vs. write vs. read/write,\n    append-only, unbuffered).  The TextIO and BinaryIO subclasses\n    below capture the distinctions between text vs. binary, which is\n    pervasive in the interface; however we currently do not offer a\n    way to track the other distinctions in the type system.\n    ';__slots__=()
	@property
	@abstractmethod
	def mode(self):0
	@property
	@abstractmethod
	def name(self):0
	@abstractmethod
	def close(self):0
	@property
	@abstractmethod
	def closed(self):0
	@abstractmethod
	def fileno(self):0
	@abstractmethod
	def flush(self):0
	@abstractmethod
	def isatty(self):0
	@abstractmethod
	def read(self,n=-1):0
	@abstractmethod
	def readable(self):0
	@abstractmethod
	def readline(self,limit=-1):0
	@abstractmethod
	def readlines(self,hint=-1):0
	@abstractmethod
	def seek(self,offset,whence=0):0
	@abstractmethod
	def seekable(self):0
	@abstractmethod
	def tell(self):0
	@abstractmethod
	def truncate(self,size=_A):0
	@abstractmethod
	def writable(self):0
	@abstractmethod
	def write(self,s):0
	@abstractmethod
	def writelines(self,lines):0
	@abstractmethod
	def __enter__(self):0
	@abstractmethod
	def __exit__(self,type,value,traceback):0
class BinaryIO(IO[bytes]):
	'Typed version of the return of open() in binary mode.';__slots__=()
	@abstractmethod
	def write(self,s):0
	@abstractmethod
	def __enter__(self):0
class TextIO(IO[str]):
	'Typed version of the return of open() in text mode.';__slots__=()
	@property
	@abstractmethod
	def buffer(self):0
	@property
	@abstractmethod
	def encoding(self):0
	@property
	@abstractmethod
	def errors(self):0
	@property
	@abstractmethod
	def line_buffering(self):0
	@property
	@abstractmethod
	def newlines(self):0
	@abstractmethod
	def __enter__(self):0
class io:'Wrapper namespace for IO generic classes.';__all__=['IO',_m,_k];IO=IO;TextIO=TextIO;BinaryIO=BinaryIO
io.__name__=__name__+'.io'
sys.modules[io.__name__]=io
Pattern=_alias(stdlib_re.Pattern,1)
Match=_alias(stdlib_re.Match,1)
class re:'Wrapper namespace for re type aliases.';__all__=[_l,'Match'];Pattern=Pattern;Match=Match
re.__name__=__name__+'.re'
sys.modules[re.__name__]=re