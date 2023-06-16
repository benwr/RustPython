'Abstract Base Classes (ABCs) according to PEP 3119.'
_A=True
def abstractmethod(funcobj):"A decorator indicating abstract methods.\n\n    Requires that the metaclass is ABCMeta or derived from it.  A\n    class that has a metaclass derived from ABCMeta cannot be\n    instantiated unless all of its abstract methods are overridden.\n    The abstract methods can be called using any of the normal\n    'super' call mechanisms.  abstractmethod() may be used to declare\n    abstract methods for properties and descriptors.\n\n    Usage:\n\n        class C(metaclass=ABCMeta):\n            @abstractmethod\n            def my_abstract_method(self, ...):\n                ...\n    ";A=funcobj;A.__isabstractmethod__=_A;return A
class abstractclassmethod(classmethod):
	"A decorator indicating abstract classmethods.\n\n    Deprecated, use 'classmethod' with 'abstractmethod' instead:\n\n        class C(ABC):\n            @classmethod\n            @abstractmethod\n            def my_abstract_classmethod(cls, ...):\n                ...\n\n    ";__isabstractmethod__=_A
	def __init__(A,callable):callable.__isabstractmethod__=_A;super().__init__(callable)
class abstractstaticmethod(staticmethod):
	"A decorator indicating abstract staticmethods.\n\n    Deprecated, use 'staticmethod' with 'abstractmethod' instead:\n\n        class C(ABC):\n            @staticmethod\n            @abstractmethod\n            def my_abstract_staticmethod(...):\n                ...\n\n    ";__isabstractmethod__=_A
	def __init__(A,callable):callable.__isabstractmethod__=_A;super().__init__(callable)
class abstractproperty(property):"A decorator indicating abstract properties.\n\n    Deprecated, use 'property' with 'abstractmethod' instead:\n\n        class C(ABC):\n            @property\n            @abstractmethod\n            def my_abstract_property(self):\n                ...\n\n    ";__isabstractmethod__=_A
try:from _abc import get_cache_token,_abc_init,_abc_register,_abc_instancecheck,_abc_subclasscheck,_get_dump,_reset_registry,_reset_caches
except ModuleNotFoundError:from _py_abc import ABCMeta,get_cache_token;ABCMeta.__module__='abc'
except ImportError:from _py_abc import ABCMeta,get_cache_token;ABCMeta.__module__='abc'
else:
	class ABCMeta(type):
		"Metaclass for defining Abstract Base Classes (ABCs).\n\n        Use this metaclass to create an ABC.  An ABC can be subclassed\n        directly, and then acts as a mix-in class.  You can also register\n        unrelated concrete classes (even built-in classes) and unrelated\n        ABCs as 'virtual subclasses' -- these and their descendants will\n        be considered subclasses of the registering ABC by the built-in\n        issubclass() function, but the registering ABC won't show up in\n        their MRO (Method Resolution Order) nor will method\n        implementations defined by the registering ABC be callable (not\n        even via super()).\n        "
		def __new__(B,C,D,E,**F):A=super().__new__(B,C,D,E,**F);_abc_init(A);return A
		def register(A,subclass):'Register a virtual subclass of an ABC.\n\n            Returns the subclass, to allow usage as a class decorator.\n            ';return _abc_register(A,subclass)
		def __instancecheck__(A,instance):'Override for isinstance(instance, cls).';return _abc_instancecheck(A,instance)
		def __subclasscheck__(A,subclass):'Override for issubclass(subclass, cls).';return _abc_subclasscheck(A,subclass)
		def _dump_registry(B,file=None):'Debug helper to print the ABC registry.';A=file;print(f"Class: {B.__module__}.{B.__qualname__}",file=A);print(f"Inv. counter: {get_cache_token()}",file=A);C,D,E,F=_get_dump(B);print(f"_abc_registry: {C!r}",file=A);print(f"_abc_cache: {D!r}",file=A);print(f"_abc_negative_cache: {E!r}",file=A);print(f"_abc_negative_cache_version: {F!r}",file=A)
		def _abc_registry_clear(A):'Clear the registry (for debugging or testing).';_reset_registry(A)
		def _abc_caches_clear(A):'Clear the caches (for debugging or testing).';_reset_caches(A)
def update_abstractmethods(cls):
	'Recalculate the set of abstract methods of an abstract class.\n\n    If a class has had one of its abstract methods implemented after the\n    class was created, the method will not be considered implemented until\n    this function is called. Alternatively, if a new abstract method has been\n    added to the class, it will only be considered an abstract method of the\n    class after this function is called.\n\n    This function should be called before any use is made of the class,\n    usually in class decorators that add methods to the subject class.\n\n    Returns cls, to allow usage as a class decorator.\n\n    If cls is not an instance of ABCMeta, does nothing.\n    ';E=False;F='__isabstractmethod__';G='__abstractmethods__';A=cls
	if not hasattr(A,G):return A
	C=set()
	for H in A.__bases__:
		for B in getattr(H,G,()):
			D=getattr(A,B,None)
			if getattr(D,F,E):C.add(B)
	for(B,D)in A.__dict__.items():
		if getattr(D,F,E):C.add(B)
	A.__abstractmethods__=frozenset(C);return A
class ABC(metaclass=ABCMeta):'Helper class that provides a standard way to create an ABC using\n    inheritance.\n    ';__slots__=()