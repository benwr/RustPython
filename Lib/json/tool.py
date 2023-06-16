'Command-line tool to validate and pretty-print JSON\n\nUsage::\n\n    $ echo \'{"json":"obj"}\' | python -m json.tool\n    {\n        "json": "obj"\n    }\n    $ echo \'{ 1.2:3.4}\' | python -m json.tool\n    Expecting property name enclosed in double quotes: line 1 column 3 (char 2)\n\n'
import argparse,json,sys
from pathlib import Path
def main():
	H='store_const';I='ensure_ascii';J=False;K='utf-8';F='store_true';C='indent';D=None;P='python -m json.tool';Q='A simple command line interface for json module to validate and pretty-print JSON objects.';B=argparse.ArgumentParser(prog=P,description=Q);B.add_argument('infile',nargs='?',type=argparse.FileType(encoding=K),help='a JSON file to be validated or pretty-printed',default=sys.stdin);B.add_argument('outfile',nargs='?',type=Path,help='write the output of infile to outfile',default=D);B.add_argument('--sort-keys',action=F,default=J,help='sort the output of dictionaries alphabetically by key');B.add_argument('--no-ensure-ascii',dest=I,action='store_false',help='disable escaping of non-ASCII characters');B.add_argument('--json-lines',action=F,default=J,help='parse input using the JSON Lines format. Use with --no-indent or --compact to produce valid JSON Lines output.');E=B.add_mutually_exclusive_group();E.add_argument('--indent',default=4,type=int,help='separate items with newlines and use this number of spaces for indentation');E.add_argument('--tab',action=H,dest=C,const='\t',help='separate items with newlines and use tabs for indentation');E.add_argument('--no-indent',action=H,dest=C,const=D,help='separate items with spaces rather than newlines');E.add_argument('--compact',action=F,help='suppress all whitespace separation (most compact)');A=B.parse_args();G={'sort_keys':A.sort_keys,C:A.indent,I:A.ensure_ascii}
	if A.compact:G[C]=D;G['separators']=',',':'
	with A.infile as L:
		try:
			if A.json_lines:M=(json.loads(A)for A in L)
			else:M=json.load(L),
			if A.outfile is D:N=sys.stdout
			else:N=A.outfile.open('w',encoding=K)
			with N as O:
				for R in M:json.dump(R,O,**G);O.write('\n')
		except ValueError as S:raise SystemExit(S)
if __name__=='__main__':
	try:main()
	except BrokenPipeError as exc:sys.exit(exc.errno)