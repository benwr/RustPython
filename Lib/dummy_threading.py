'Faux ``threading`` version using ``dummy_thread`` instead of ``thread``.\n\nThe module ``_dummy_threading`` is added to ``sys.modules`` in order\nto not have ``threading`` considered imported.  Had ``threading`` been\ndirectly imported it would have made all subsequent imports succeed\nregardless of whether ``_thread`` was available which is not desired.\n\n'
_D=False
_C='_thread'
_B='_threading_local'
_A='threading'
from sys import modules as sys_modules
import _dummy_thread
holding_thread=_D
holding_threading=_D
holding__threading_local=_D
try:
	if _C in sys_modules:held_thread=sys_modules[_C];holding_thread=True
	sys_modules[_C]=sys_modules['_dummy_thread']
	if _A in sys_modules:held_threading=sys_modules[_A];holding_threading=True;del sys_modules[_A]
	if _B in sys_modules:held__threading_local=sys_modules[_B];holding__threading_local=True;del sys_modules[_B]
	import threading;sys_modules['_dummy_threading']=sys_modules[_A];del sys_modules[_A];sys_modules['_dummy__threading_local']=sys_modules[_B];del sys_modules[_B];from _dummy_threading import*;from _dummy_threading import __all__
finally:
	if holding_threading:sys_modules[_A]=held_threading;del held_threading
	del holding_threading
	if holding__threading_local:sys_modules[_B]=held__threading_local;del held__threading_local
	del holding__threading_local
	if holding_thread:sys_modules[_C]=held_thread;del held_thread
	else:del sys_modules[_C]
	del holding_thread;del _dummy_thread;del sys_modules