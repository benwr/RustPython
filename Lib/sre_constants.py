'Internal support module for sre'
_B='u32'
_A=None
MAGIC=20171005
from _sre import MAXREPEAT,MAXGROUPS
class error(Exception):
	'Exception raised for invalid regular expressions.\n\n    Attributes:\n\n        msg: The unformatted error message\n        pattern: The regular expression pattern\n        pos: The index in the pattern where compilation failed (may be None)\n        lineno: The line corresponding to pos (may be None)\n        colno: The column corresponding to pos (may be None)\n    ';__module__='re'
	def __init__(self,msg,pattern=_A,pos=_A):
		self.msg=msg;self.pattern=pattern;self.pos=pos
		if pattern is not _A and pos is not _A:
			msg='%s at position %d'%(msg,pos)
			if isinstance(pattern,str):newline='\n'
			else:newline=b'\n'
			self.lineno=pattern.count(newline,0,pos)+1;self.colno=pos-pattern.rfind(newline,0,pos)
			if newline in pattern:msg='%s (line %d, column %d)'%(msg,self.lineno,self.colno)
		else:self.lineno=self.colno=_A
		super().__init__(msg)
class _NamedIntConstant(int):
	def __new__(cls,value,name):self=super(_NamedIntConstant,cls).__new__(cls,value);self.name=name;return self
	def __repr__(self):return self.name
MAXREPEAT=_NamedIntConstant(MAXREPEAT,'MAXREPEAT')
def _makecodes(names):names=names.strip().split();items=[_NamedIntConstant(i,name)for(i,name)in enumerate(names)];globals().update({item.name:item for item in items});return items
OPCODES=_makecodes('\n    FAILURE SUCCESS\n\n    ANY ANY_ALL\n    ASSERT ASSERT_NOT\n    AT\n    BRANCH\n    CALL\n    CATEGORY\n    CHARSET BIGCHARSET\n    GROUPREF GROUPREF_EXISTS\n    IN\n    INFO\n    JUMP\n    LITERAL\n    MARK\n    MAX_UNTIL\n    MIN_UNTIL\n    NOT_LITERAL\n    NEGATE\n    RANGE\n    REPEAT\n    REPEAT_ONE\n    SUBPATTERN\n    MIN_REPEAT_ONE\n\n    GROUPREF_IGNORE\n    IN_IGNORE\n    LITERAL_IGNORE\n    NOT_LITERAL_IGNORE\n\n    GROUPREF_LOC_IGNORE\n    IN_LOC_IGNORE\n    LITERAL_LOC_IGNORE\n    NOT_LITERAL_LOC_IGNORE\n\n    GROUPREF_UNI_IGNORE\n    IN_UNI_IGNORE\n    LITERAL_UNI_IGNORE\n    NOT_LITERAL_UNI_IGNORE\n    RANGE_UNI_IGNORE\n\n    MIN_REPEAT MAX_REPEAT\n')
del OPCODES[-2:]
ATCODES=_makecodes('\n    AT_BEGINNING AT_BEGINNING_LINE AT_BEGINNING_STRING\n    AT_BOUNDARY AT_NON_BOUNDARY\n    AT_END AT_END_LINE AT_END_STRING\n\n    AT_LOC_BOUNDARY AT_LOC_NON_BOUNDARY\n\n    AT_UNI_BOUNDARY AT_UNI_NON_BOUNDARY\n')
CHCODES=_makecodes('\n    CATEGORY_DIGIT CATEGORY_NOT_DIGIT\n    CATEGORY_SPACE CATEGORY_NOT_SPACE\n    CATEGORY_WORD CATEGORY_NOT_WORD\n    CATEGORY_LINEBREAK CATEGORY_NOT_LINEBREAK\n\n    CATEGORY_LOC_WORD CATEGORY_LOC_NOT_WORD\n\n    CATEGORY_UNI_DIGIT CATEGORY_UNI_NOT_DIGIT\n    CATEGORY_UNI_SPACE CATEGORY_UNI_NOT_SPACE\n    CATEGORY_UNI_WORD CATEGORY_UNI_NOT_WORD\n    CATEGORY_UNI_LINEBREAK CATEGORY_UNI_NOT_LINEBREAK\n')
OP_IGNORE={LITERAL:LITERAL_IGNORE,NOT_LITERAL:NOT_LITERAL_IGNORE}
OP_LOCALE_IGNORE={LITERAL:LITERAL_LOC_IGNORE,NOT_LITERAL:NOT_LITERAL_LOC_IGNORE}
OP_UNICODE_IGNORE={LITERAL:LITERAL_UNI_IGNORE,NOT_LITERAL:NOT_LITERAL_UNI_IGNORE}
AT_MULTILINE={AT_BEGINNING:AT_BEGINNING_LINE,AT_END:AT_END_LINE}
AT_LOCALE={AT_BOUNDARY:AT_LOC_BOUNDARY,AT_NON_BOUNDARY:AT_LOC_NON_BOUNDARY}
AT_UNICODE={AT_BOUNDARY:AT_UNI_BOUNDARY,AT_NON_BOUNDARY:AT_UNI_NON_BOUNDARY}
CH_LOCALE={CATEGORY_DIGIT:CATEGORY_DIGIT,CATEGORY_NOT_DIGIT:CATEGORY_NOT_DIGIT,CATEGORY_SPACE:CATEGORY_SPACE,CATEGORY_NOT_SPACE:CATEGORY_NOT_SPACE,CATEGORY_WORD:CATEGORY_LOC_WORD,CATEGORY_NOT_WORD:CATEGORY_LOC_NOT_WORD,CATEGORY_LINEBREAK:CATEGORY_LINEBREAK,CATEGORY_NOT_LINEBREAK:CATEGORY_NOT_LINEBREAK}
CH_UNICODE={CATEGORY_DIGIT:CATEGORY_UNI_DIGIT,CATEGORY_NOT_DIGIT:CATEGORY_UNI_NOT_DIGIT,CATEGORY_SPACE:CATEGORY_UNI_SPACE,CATEGORY_NOT_SPACE:CATEGORY_UNI_NOT_SPACE,CATEGORY_WORD:CATEGORY_UNI_WORD,CATEGORY_NOT_WORD:CATEGORY_UNI_NOT_WORD,CATEGORY_LINEBREAK:CATEGORY_UNI_LINEBREAK,CATEGORY_NOT_LINEBREAK:CATEGORY_UNI_NOT_LINEBREAK}
SRE_FLAG_TEMPLATE=1
SRE_FLAG_IGNORECASE=2
SRE_FLAG_LOCALE=4
SRE_FLAG_MULTILINE=8
SRE_FLAG_DOTALL=16
SRE_FLAG_UNICODE=32
SRE_FLAG_VERBOSE=64
SRE_FLAG_DEBUG=128
SRE_FLAG_ASCII=256
SRE_INFO_PREFIX=1
SRE_INFO_LITERAL=2
SRE_INFO_CHARSET=4
if __name__=='__main__':
	def dump(f,d,typ,int_t,prefix):
		items=sorted(d);f.write(f"#[derive(num_enum::TryFromPrimitive, Debug)]\n#[repr({int_t})]\n#[allow(non_camel_case_types, clippy::upper_case_acronyms)]\npub enum {typ} {{\n")
		for item in items:name=str(item).removeprefix(prefix);val=int(item);f.write(f"    {name} = {val},\n")
		f.write('}\n')
	import sys
	if len(sys.argv)>1:constants_file=sys.argv[1]
	else:import os;constants_file=os.path.join(os.path.dirname(__file__),'../../sre-engine/src/constants.rs')
	with open(constants_file,'w')as f:
		f.write("/*\n * Secret Labs' Regular Expression Engine\n *\n * regular expression matching engine\n *\n * NOTE: This file is generated by sre_constants.py.  If you need\n * to change anything in here, edit sre_constants.py and run it.\n *\n * Copyright (c) 1997-2001 by Secret Labs AB.  All rights reserved.\n *\n * See the _sre.c file for information on usage and redistribution.\n */\n\n");f.write('use bitflags::bitflags;\n\n');f.write('pub const SRE_MAGIC: usize = %d;\n'%MAGIC);dump(f,OPCODES,'SreOpcode',_B,'');dump(f,ATCODES,'SreAtCode',_B,'AT_');dump(f,CHCODES,'SreCatCode',_B,'CATEGORY_')
		def bitflags(typ,int_t,prefix,flags):
			f.write(f"bitflags! {{\n    pub struct {typ}: {int_t} {{\n")
			for name in flags:val=globals()[prefix+name];f.write(f"        const {name} = {val};\n")
			f.write('    }\n}\n')
		bitflags('SreFlag','u16','SRE_FLAG_',['TEMPLATE','IGNORECASE','LOCALE','MULTILINE','DOTALL','UNICODE','VERBOSE','DEBUG','ASCII']);bitflags('SreInfo',_B,'SRE_INFO_',['PREFIX','LITERAL','CHARSET'])
	print('done')