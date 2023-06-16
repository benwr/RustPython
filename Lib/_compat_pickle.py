_A8='CGIHTTPRequestHandler'
_A7='SimpleHTTPRequestHandler'
_A6='DocCGIXMLRPCRequestHandler'
_A5='DocXMLRPCRequestHandler'
_A4='XMLRPCDocGenerator'
_A3='ServerHTMLDoc'
_A2='SaveFileDialog'
_A1='LoadFileDialog'
_A0='_socketobject'
_z='_functools'
_y='pickle'
_x='CGIHTTPServer'
_w='SimpleHTTPServer'
_v='TimeoutError'
_u='OSError'
_t='ImportError'
_s='Exception'
_r='multiprocessing.context'
_q='functools'
_p='URLError'
_o='HTTPError'
_n='urlretrieve'
_m='urlopen'
_l='urlencode'
_k='urlcleanup'
_j='url2pathname'
_i='unquote'
_h='unquote_plus'
_g='quote_plus'
_f='pathname2url'
_e='getproxies'
_d='ContentTooShortError'
_c='Process'
_b='Connection'
_a='fromfd'
_Z='_socket'
_Y='intern'
_X='urllib.error'
_W='tkinter.simpledialog'
_V='urllib2'
_U='SimpleDialog'
_T='exceptions'
_S='whichdb'
_R='UserString'
_Q='UserList'
_P='reduce'
_O='socket'
_N='http.server'
_M='tkinter.filedialog'
_L='dbm'
_K='FileDialog'
_J='UserDict'
_I='urllib.parse'
_H='collections'
_G='itertools'
_F='urllib.request'
_E='xmlrpc.server'
_D='DocXMLRPCServer'
_C='__builtin__'
_B='urllib'
_A='builtins'
IMPORT_MAPPING={_C:_A,'copy_reg':'copyreg','Queue':'queue','SocketServer':'socketserver','ConfigParser':'configparser','repr':'reprlib','tkFileDialog':_M,'tkSimpleDialog':_W,'tkColorChooser':'tkinter.colorchooser','tkCommonDialog':'tkinter.commondialog','Dialog':'tkinter.dialog','Tkdnd':'tkinter.dnd','tkFont':'tkinter.font','tkMessageBox':'tkinter.messagebox','ScrolledText':'tkinter.scrolledtext','Tkconstants':'tkinter.constants','Tix':'tkinter.tix','ttk':'tkinter.ttk','Tkinter':'tkinter','markupbase':'_markupbase','_winreg':'winreg','thread':'_thread','dummy_thread':'_dummy_thread','dbhash':'dbm.bsd','dumbdbm':'dbm.dumb',_L:'dbm.ndbm','gdbm':'dbm.gnu','xmlrpclib':'xmlrpc.client','SimpleXMLRPCServer':_E,'httplib':'http.client','htmlentitydefs':'html.entities','HTMLParser':'html.parser','Cookie':'http.cookies','cookielib':'http.cookiejar','BaseHTTPServer':_N,'test.test_support':'test.support','commands':'subprocess','urlparse':_I,'robotparser':'urllib.robotparser',_V:_F,'anydbm':_L,'_abcoll':'collections.abc'}
NAME_MAPPING={(_C,'xrange'):(_A,'range'),(_C,_P):(_q,_P),(_C,_Y):('sys',_Y),(_C,'unichr'):(_A,'chr'),(_C,'unicode'):(_A,'str'),(_C,'long'):(_A,'int'),(_G,'izip'):(_A,'zip'),(_G,'imap'):(_A,'map'),(_G,'ifilter'):(_A,'filter'),(_G,'ifilterfalse'):(_G,'filterfalse'),(_G,'izip_longest'):(_G,'zip_longest'),(_J,'IterableUserDict'):(_H,_J),(_Q,_Q):(_H,_Q),(_R,_R):(_H,_R),(_S,_S):(_L,_S),(_Z,_a):(_O,_a),('_multiprocessing',_b):('multiprocessing.connection',_b),('multiprocessing.process',_c):(_r,_c),('multiprocessing.forking','Popen'):('multiprocessing.popen_fork','Popen'),(_B,_d):(_X,_d),(_B,_e):(_F,_e),(_B,_f):(_F,_f),(_B,_g):(_I,_g),(_B,'quote'):(_I,'quote'),(_B,_h):(_I,_h),(_B,_i):(_I,_i),(_B,_j):(_F,_j),(_B,_k):(_F,_k),(_B,_l):(_I,_l),(_B,_m):(_F,_m),(_B,_n):(_F,_n),(_V,_o):(_X,_o),(_V,_p):(_X,_p)}
PYTHON2_EXCEPTIONS='ArithmeticError','AssertionError','AttributeError','BaseException','BufferError','BytesWarning','DeprecationWarning','EOFError','EnvironmentError',_s,'FloatingPointError','FutureWarning','GeneratorExit','IOError',_t,'ImportWarning','IndentationError','IndexError','KeyError','KeyboardInterrupt','LookupError','MemoryError','NameError','NotImplementedError',_u,'OverflowError','PendingDeprecationWarning','ReferenceError','RuntimeError','RuntimeWarning','StopIteration','SyntaxError','SyntaxWarning','SystemError','SystemExit','TabError','TypeError','UnboundLocalError','UnicodeDecodeError','UnicodeEncodeError','UnicodeError','UnicodeTranslateError','UnicodeWarning','UserWarning','ValueError','Warning','ZeroDivisionError'
try:WindowsError
except NameError:pass
else:PYTHON2_EXCEPTIONS+='WindowsError',
try:JitError
except NameError:pass
else:PYTHON2_EXCEPTIONS+='JitError',
for excname in PYTHON2_EXCEPTIONS:NAME_MAPPING[_T,excname]=_A,excname
MULTIPROCESSING_EXCEPTIONS='AuthenticationError','BufferTooShort','ProcessError',_v
for excname in MULTIPROCESSING_EXCEPTIONS:NAME_MAPPING['multiprocessing',excname]=_r,excname
REVERSE_IMPORT_MAPPING=dict((B,A)for(A,B)in IMPORT_MAPPING.items())
assert len(REVERSE_IMPORT_MAPPING)==len(IMPORT_MAPPING)
REVERSE_NAME_MAPPING=dict((B,A)for(A,B)in NAME_MAPPING.items())
assert len(REVERSE_NAME_MAPPING)==len(NAME_MAPPING)
IMPORT_MAPPING.update({'cPickle':_y,'_elementtree':'xml.etree.ElementTree',_K:_M,_U:_W,_D:_E,_w:_N,_x:_N,_J:_H,_Q:_H,_R:_H,_S:_L,'StringIO':'io','cStringIO':'io'})
REVERSE_IMPORT_MAPPING.update({'_bz2':'bz2','_dbm':_L,_z:_q,'_gdbm':'gdbm','_pickle':_y})
NAME_MAPPING.update({(_C,'basestring'):(_A,'str'),(_T,'StandardError'):(_A,_s),(_J,_J):(_H,_J),(_O,_A0):(_O,'SocketType')})
REVERSE_NAME_MAPPING.update({(_z,_P):(_C,_P),(_M,_K):(_K,_K),(_M,_A1):(_K,_A1),(_M,_A2):(_K,_A2),(_W,_U):(_U,_U),(_E,_A3):(_D,_A3),(_E,_A4):(_D,_A4),(_E,_A5):(_D,_A5),(_E,_D):(_D,_D),(_E,_A6):(_D,_A6),(_N,_A7):(_w,_A7),(_N,_A8):(_x,_A8),(_Z,_O):(_O,_A0)})
PYTHON3_OSERROR_EXCEPTIONS='BrokenPipeError','ChildProcessError','ConnectionAbortedError','ConnectionError','ConnectionRefusedError','ConnectionResetError','FileExistsError','FileNotFoundError','InterruptedError','IsADirectoryError','NotADirectoryError','PermissionError','ProcessLookupError',_v
for excname in PYTHON3_OSERROR_EXCEPTIONS:REVERSE_NAME_MAPPING[_A,excname]=_T,_u
PYTHON3_IMPORTERROR_EXCEPTIONS='ModuleNotFoundError',
for excname in PYTHON3_IMPORTERROR_EXCEPTIONS:REVERSE_NAME_MAPPING[_A,excname]=_T,_t