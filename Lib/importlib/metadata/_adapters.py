import re,textwrap,email.message
from._text import FoldedCase
class Message(email.message.Message):
	multiple_use_keys=set(map(FoldedCase,['Classifier','Obsoletes-Dist','Platform','Project-URL','Provides-Dist','Provides-Extra','Requires-Dist','Requires-External','Supported-Platform','Dynamic']));'\n    Keys that may be indicated multiple times per PEP 566.\n    '
	def __new__(cls,orig):res=super().__new__(cls);vars(res).update(vars(orig));return res
	def __init__(self,*args,**kwargs):self._headers=self._repair_headers()
	def __iter__(self):return super().__iter__()
	def _repair_headers(self):
		def redent(value):
			'Correct for RFC822 indentation'
			if not value or'\n'not in value:return value
			return textwrap.dedent(' '*8+value)
		headers=[(key,redent(value))for(key,value)in vars(self)['_headers']]
		if self._payload:headers.append(('Description',self.get_payload()))
		return headers
	@property
	def json(self):
		'\n        Convert PackageMetadata to a JSON-compatible format\n        per PEP 0566.\n        '
		def transform(key):
			value=self.get_all(key)if key in self.multiple_use_keys else self[key]
			if key=='Keywords':value=re.split('\\s+',value)
			tk=key.lower().replace('-','_');return tk,value
		return dict(map(transform,map(FoldedCase,self)))