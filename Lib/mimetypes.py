'Guess the MIME type of a file.\n\nThis module defines two useful functions:\n\nguess_type(url, strict=True) -- guess the MIME type and encoding of a URL.\n\nguess_extension(type, strict=True) -- guess the extension for a given MIME type.\n\nIt also contains the following, for tuning the behavior:\n\nData:\n\nknownfiles -- list of files to parse\ninited -- flag set when init() has been called\nsuffix_map -- dictionary mapping suffixes to suffixes\nencodings_map -- dictionary mapping suffixes to encodings\ntypes_map -- dictionary mapping suffixes to types\n\nFunctions:\n\ninit([files]) -- parse a list of files, default knownfiles (on Windows, the\n  default values are taken from the registry)\nread_mime_types(file) -- parse one file, return a dictionary or None\n'
_E='/usr/local/etc/httpd/conf/mime.types'
_D=False
_C='text/plain'
_B=None
_A=True
import os,sys,posixpath,urllib.parse
try:import winreg as _winreg
except ImportError:_winreg=_B
__all__=['knownfiles','inited','MimeTypes','guess_type','guess_all_extensions','guess_extension','add_type','init','read_mime_types','suffix_map','encodings_map','types_map','common_types']
knownfiles=['/etc/mime.types','/etc/httpd/mime.types','/etc/httpd/conf/mime.types','/etc/apache/mime.types','/etc/apache2/mime.types',_E,'/usr/local/lib/netscape/mime.types',_E,'/usr/local/etc/mime.types']
inited=_D
_db=_B
class MimeTypes:
	'MIME-types datastore.\n\n    This datastore can handle information from mime.types-style files\n    and supports basic determination of MIME type from a filename or\n    URL, and can guess a reasonable extension given a MIME type.\n    '
	def __init__(A,filenames=(),strict=_A):
		if not inited:init()
		A.encodings_map=_encodings_map_default.copy();A.suffix_map=_suffix_map_default.copy();A.types_map={},{};A.types_map_inv={},{}
		for(B,type)in _types_map_default.items():A.add_type(type,B,_A)
		for(B,type)in _common_types_default.items():A.add_type(type,B,_D)
		for C in filenames:A.read(C,strict)
	def add_type(B,type,ext,strict=_A):
		'Add a mapping between a type and an extension.\n\n        When the extension is already known, the new\n        type will replace the old one. When the type\n        is already known the extension will be added\n        to the list of known extensions.\n\n        If strict is true, information will be added to\n        list of standard types, else to the list of non-standard\n        types.\n        ';C=strict;A=ext;B.types_map[C][A]=type;D=B.types_map_inv[C].setdefault(type,[])
		if A not in D:D.append(A)
	def guess_type(E,url,strict=_A):
		"Guess the type of a file which is either a URL or a path-like object.\n\n        Return value is a tuple (type, encoding) where type is None if\n        the type can't be guessed (no or unknown suffix) or a string\n        of the form type/subtype, usable for a MIME Content-type\n        header; and encoding is None for no encoding or the name of\n        the program used to encode (e.g. compress or gzip).  The\n        mappings are table driven.  Encoding suffixes are case\n        sensitive; type suffixes are first tried case sensitive, then\n        case insensitive.\n\n        The suffixes .tgz, .taz and .tz (case sensitive!) are all\n        mapped to '.tar.gz'.  (This is table-driven too, using the\n        dictionary suffix_map.)\n\n        Optional `strict' argument when False adds a bunch of commonly found,\n        but non-standard types.\n        ";B=url;B=os.fspath(B);I,B=urllib.parse._splittype(B)
		if I=='data':
			G=B.find(',')
			if G<0:return _B,_B
			H=B.find(';',0,G)
			if H>=0:type=B[:H]
			else:type=B[:G]
			if'='in type or'/'not in type:type=_C
			return type,_B
		F,A=posixpath.splitext(B)
		while A in E.suffix_map:F,A=posixpath.splitext(F+E.suffix_map[A])
		if A in E.encodings_map:D=E.encodings_map[A];F,A=posixpath.splitext(F)
		else:D=_B
		C=E.types_map[_A]
		if A in C:return C[A],D
		elif A.lower()in C:return C[A.lower()],D
		elif strict:return _B,D
		C=E.types_map[_D]
		if A in C:return C[A],D
		elif A.lower()in C:return C[A.lower()],D
		else:return _B,D
	def guess_all_extensions(B,type,strict=_A):
		"Guess the extensions for a file based on its MIME type.\n\n        Return value is a list of strings giving the possible filename\n        extensions, including the leading dot ('.').  The extension is not\n        guaranteed to have been associated with any particular data stream,\n        but would be mapped to the MIME type `type' by guess_type().\n\n        Optional `strict' argument when false adds a bunch of commonly found,\n        but non-standard types.\n        ";type=type.lower();A=B.types_map_inv[_A].get(type,[])
		if not strict:
			for C in B.types_map_inv[_D].get(type,[]):
				if C not in A:A.append(C)
		return A
	def guess_extension(B,type,strict=_A):
		"Guess the extension for a file based on its MIME type.\n\n        Return value is a string giving a filename extension,\n        including the leading dot ('.').  The extension is not\n        guaranteed to have been associated with any particular data\n        stream, but would be mapped to the MIME type `type' by\n        guess_type().  If no extension can be guessed for `type', None\n        is returned.\n\n        Optional `strict' argument when false adds a bunch of commonly found,\n        but non-standard types.\n        ";A=B.guess_all_extensions(type,strict)
		if not A:return
		return A[0]
	def read(A,filename,strict=_A):
		'\n        Read a single mime.types-format file, specified by pathname.\n\n        If strict is true, information will be added to\n        list of standard types, else to the list of non-standard\n        types.\n        '
		with open(filename,encoding='utf-8')as B:A.readfp(B,strict)
	def readfp(D,fp,strict=_A):
		'\n        Read a single mime.types-format file.\n\n        If strict is true, information will be added to\n        list of standard types, else to the list of non-standard\n        types.\n        '
		while 1:
			B=fp.readline()
			if not B:break
			A=B.split()
			for C in range(len(A)):
				if A[C][0]=='#':del A[C:];break
			if not A:continue
			type,E=A[0],A[1:]
			for F in E:D.add_type(type,'.'+F,strict)
	def read_windows_registry(C,strict=_A):
		'\n        Load the MIME types database from Windows registry.\n\n        If strict is true, information will be added to\n        list of standard types, else to the list of non-standard\n        types.\n        '
		if not _winreg:return
		def D(mimedb):
			A=0
			while _A:
				try:B=_winreg.EnumKey(mimedb,A)
				except OSError:break
				else:
					if'\x00'not in B:yield B
				A+=1
		with _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT,'')as B:
			for A in D(B):
				try:
					with _winreg.OpenKey(B,A)as E:
						if not A.startswith('.'):continue
						F,G=_winreg.QueryValueEx(E,'Content Type')
						if G!=_winreg.REG_SZ:continue
						C.add_type(F,A,strict)
				except OSError:continue
def guess_type(url,strict=_A):
	'Guess the type of a file based on its URL.\n\n    Return value is a tuple (type, encoding) where type is None if the\n    type can\'t be guessed (no or unknown suffix) or a string of the\n    form type/subtype, usable for a MIME Content-type header; and\n    encoding is None for no encoding or the name of the program used\n    to encode (e.g. compress or gzip).  The mappings are table\n    driven.  Encoding suffixes are case sensitive; type suffixes are\n    first tried case sensitive, then case insensitive.\n\n    The suffixes .tgz, .taz and .tz (case sensitive!) are all mapped\n    to ".tar.gz".  (This is table-driven too, using the dictionary\n    suffix_map).\n\n    Optional `strict\' argument when false adds a bunch of commonly found, but\n    non-standard types.\n    '
	if _db is _B:init()
	return _db.guess_type(url,strict)
def guess_all_extensions(type,strict=_A):
	"Guess the extensions for a file based on its MIME type.\n\n    Return value is a list of strings giving the possible filename\n    extensions, including the leading dot ('.').  The extension is not\n    guaranteed to have been associated with any particular data\n    stream, but would be mapped to the MIME type `type' by\n    guess_type().  If no extension can be guessed for `type', None\n    is returned.\n\n    Optional `strict' argument when false adds a bunch of commonly found,\n    but non-standard types.\n    "
	if _db is _B:init()
	return _db.guess_all_extensions(type,strict)
def guess_extension(type,strict=_A):
	"Guess the extension for a file based on its MIME type.\n\n    Return value is a string giving a filename extension, including the\n    leading dot ('.').  The extension is not guaranteed to have been\n    associated with any particular data stream, but would be mapped to the\n    MIME type `type' by guess_type().  If no extension can be guessed for\n    `type', None is returned.\n\n    Optional `strict' argument when false adds a bunch of commonly found,\n    but non-standard types.\n    "
	if _db is _B:init()
	return _db.guess_extension(type,strict)
def add_type(type,ext,strict=_A):
	'Add a mapping between a type and an extension.\n\n    When the extension is already known, the new\n    type will replace the old one. When the type\n    is already known the extension will be added\n    to the list of known extensions.\n\n    If strict is true, information will be added to\n    list of standard types, else to the list of non-standard\n    types.\n    '
	if _db is _B:init()
	return _db.add_type(type,ext,strict)
def init(files=_B):
	B=files;global suffix_map,types_map,encodings_map,common_types;global inited,_db;inited=_A
	if B is _B or _db is _B:
		A=MimeTypes()
		if _winreg:A.read_windows_registry()
		if B is _B:B=knownfiles
		else:B=knownfiles+list(B)
	else:A=_db
	for C in B:
		if os.path.isfile(C):A.read(C)
	encodings_map=A.encodings_map;suffix_map=A.suffix_map;types_map=A.types_map[_A];common_types=A.types_map[_D];_db=A
def read_mime_types(file):
	try:A=open(file,encoding='utf-8')
	except OSError:return
	with A:B=MimeTypes();B.readfp(A,_A);return B.types_map[_A]
def _default_mime_types():M='audio/midi';N='video/quicktime';O='text/x-sgml';P='text/html';Q='image/tiff';R='audio/mpeg';S='audio/basic';T='application/x-texinfo';U='application/x-python-code';V='application/x-pkcs12';W='application/x-netcdf';X='application/vnd.ms-excel';Y='application/vnd.apple.mpegurl';Z='application/javascript';a='.jpg';b='.bmp';F='image/pict';G='image/jpeg';H='audio/x-aiff';I='application/x-troff';J='application/postscript';K='application/msword';L='.tar.gz';D='message/rfc822';E='application/xml';B='video/mpeg';C='application/vnd.ms-powerpoint';A='application/octet-stream';global suffix_map,_suffix_map_default;global encodings_map,_encodings_map_default;global types_map,_types_map_default;global common_types,_common_types_default;suffix_map=_suffix_map_default={'.svgz':'.svg.gz','.tgz':L,'.taz':L,'.tz':L,'.tbz2':'.tar.bz2','.txz':'.tar.xz'};encodings_map=_encodings_map_default={'.gz':'gzip','.Z':'compress','.bz2':'bzip2','.xz':'xz'};types_map=_types_map_default={'.js':Z,'.mjs':Z,'.json':'application/json','.webmanifest':'application/manifest+json','.doc':K,'.dot':K,'.wiz':K,'.bin':A,'.a':A,'.dll':A,'.exe':A,'.o':A,'.obj':A,'.so':A,'.oda':'application/oda','.pdf':'application/pdf','.p7c':'application/pkcs7-mime','.ps':J,'.ai':J,'.eps':J,'.m3u':Y,'.m3u8':Y,'.xls':X,'.xlb':X,'.ppt':C,'.pot':C,'.ppa':C,'.pps':C,'.pwz':C,'.wasm':'application/wasm','.bcpio':'application/x-bcpio','.cpio':'application/x-cpio','.csh':'application/x-csh','.dvi':'application/x-dvi','.gtar':'application/x-gtar','.hdf':'application/x-hdf','.h5':'application/x-hdf5','.latex':'application/x-latex','.mif':'application/x-mif','.cdf':W,'.nc':W,'.p12':V,'.pfx':V,'.ram':'application/x-pn-realaudio','.pyc':U,'.pyo':U,'.sh':'application/x-sh','.shar':'application/x-shar','.swf':'application/x-shockwave-flash','.sv4cpio':'application/x-sv4cpio','.sv4crc':'application/x-sv4crc','.tar':'application/x-tar','.tcl':'application/x-tcl','.tex':'application/x-tex','.texi':T,'.texinfo':T,'.roff':I,'.t':I,'.tr':I,'.man':'application/x-troff-man','.me':'application/x-troff-me','.ms':'application/x-troff-ms','.ustar':'application/x-ustar','.src':'application/x-wais-source','.xsl':E,'.rdf':E,'.wsdl':E,'.xpdl':E,'.zip':'application/zip','.au':S,'.snd':S,'.mp3':R,'.mp2':R,'.aif':H,'.aifc':H,'.aiff':H,'.ra':'audio/x-pn-realaudio','.wav':'audio/x-wav',b:'image/bmp','.gif':'image/gif','.ief':'image/ief',a:G,'.jpe':G,'.jpeg':G,'.png':'image/png','.svg':'image/svg+xml','.tiff':Q,'.tif':Q,'.ico':'image/vnd.microsoft.icon','.ras':'image/x-cmu-raster',b:'image/x-ms-bmp','.pnm':'image/x-portable-anymap','.pbm':'image/x-portable-bitmap','.pgm':'image/x-portable-graymap','.ppm':'image/x-portable-pixmap','.rgb':'image/x-rgb','.xbm':'image/x-xbitmap','.xpm':'image/x-xpixmap','.xwd':'image/x-xwindowdump','.eml':D,'.mht':D,'.mhtml':D,'.nws':D,'.css':'text/css','.csv':'text/csv','.html':P,'.htm':P,'.txt':_C,'.bat':_C,'.c':_C,'.h':_C,'.ksh':_C,'.pl':_C,'.rtx':'text/richtext','.tsv':'text/tab-separated-values','.py':'text/x-python','.etx':'text/x-setext','.sgm':O,'.sgml':O,'.vcf':'text/x-vcard','.xml':'text/xml','.mp4':'video/mp4','.mpeg':B,'.m1v':B,'.mpa':B,'.mpe':B,'.mpg':B,'.mov':N,'.qt':N,'.webm':'video/webm','.avi':'video/x-msvideo','.movie':'video/x-sgi-movie'};common_types=_common_types_default={'.rtf':'application/rtf','.midi':M,'.mid':M,a:'image/jpg','.pict':F,'.pct':F,'.pic':F,'.xul':'text/xul'}
_default_mime_types()
def _main():
	E="I don't know anything about type";import getopt as F;I='Usage: mimetypes.py [options] type\n\nOptions:\n    --help / -h       -- print this message and exit\n    --lenient / -l    -- additionally search of some common, but non-standard\n                         types.\n    --extension / -e  -- guess extension instead of type\n\nMore than one type argument may be given.\n'
	def G(code,msg=''):
		print(I)
		if msg:print(msg)
		sys.exit(code)
	try:J,K=F.getopt(sys.argv[1:],'hle',['help','lenient','extension'])
	except F.error as L:G(1,L)
	C=1;H=0
	for(D,N)in J:
		if D in('-h','--help'):G(0)
		elif D in('-l','--lenient'):C=0
		elif D in('-e','--extension'):H=1
	for B in K:
		if H:
			A=guess_extension(B,C)
			if not A:print(E,B)
			else:print(A)
		else:
			A,M=guess_type(B,C)
			if not A:print(E,B)
			else:print('type:',A,'encoding:',M)
if __name__=='__main__':_main()