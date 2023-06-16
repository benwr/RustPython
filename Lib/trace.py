#!/usr/bin/env python3
'program/module to trace Python program or function execution\n\nSample use, command line:\n  trace.py -c -f counts --ignore-dir \'$prefix\' spam.py eggs\n  trace.py -t --ignore-dir \'$prefix\' spam.py eggs\n  trace.py --trackcalls spam.py eggs\n\nSample use, programmatically\n  import sys\n\n  # create a Trace object, telling it what to ignore, and whether to\n  # do tracing or line-counting or both.\n  tracer = trace.Trace(ignoredirs=[sys.base_prefix, sys.base_exec_prefix,],\n                       trace=0, count=1)\n  # run the new command using the given tracer\n  tracer.run(\'main()\')\n  # make a report, placing output in /tmp\n  r = tracer.results()\n  r.write_results(show_missing=True, coverdir="/tmp")\n'
_G='%s(%d): %s'
_F='__main__'
_E='line'
_D='__file__'
_C='call'
_B=False
_A=None
__all__=['Trace','CoverageResults']
import linecache,os,sys,sysconfig,token,tokenize,inspect,gc,dis,pickle
from time import monotonic as _time
import threading
PRAGMA_NOCOVER='#pragma NO COVER'
class _Ignore:
	def __init__(self,modules=_A,dirs=_A):self._mods=set()if not modules else set(modules);self._dirs=[]if not dirs else[os.path.normpath(d)for d in dirs];self._ignore={'<string>':1}
	def names(self,filename,modulename):
		if modulename in self._ignore:return self._ignore[modulename]
		if modulename in self._mods:self._ignore[modulename]=1;return 1
		for mod in self._mods:
			if modulename.startswith(mod+'.'):self._ignore[modulename]=1;return 1
		if filename is _A:self._ignore[modulename]=1;return 1
		for d in self._dirs:
			if filename.startswith(d+os.sep):self._ignore[modulename]=1;return 1
		self._ignore[modulename]=0;return 0
def _modname(path):'Return a plausible module name for the path.';base=os.path.basename(path);filename,ext=os.path.splitext(base);return filename
def _fullmodname(path):
	'Return a plausible module name for the path.';comparepath=os.path.normcase(path);longest=''
	for dir in sys.path:
		dir=os.path.normcase(dir)
		if comparepath.startswith(dir)and comparepath[len(dir)]==os.sep:
			if len(dir)>len(longest):longest=dir
	if longest:base=path[len(longest)+1:]
	else:base=path
	drive,base=os.path.splitdrive(base);base=base.replace(os.sep,'.')
	if os.altsep:base=base.replace(os.altsep,'.')
	filename,ext=os.path.splitext(base);return filename.lstrip('.')
class CoverageResults:
	def __init__(self,counts=_A,calledfuncs=_A,infile=_A,callers=_A,outfile=_A):
		self.counts=counts
		if self.counts is _A:self.counts={}
		self.counter=self.counts.copy();self.calledfuncs=calledfuncs
		if self.calledfuncs is _A:self.calledfuncs={}
		self.calledfuncs=self.calledfuncs.copy();self.callers=callers
		if self.callers is _A:self.callers={}
		self.callers=self.callers.copy();self.infile=infile;self.outfile=outfile
		if self.infile:
			try:
				with open(self.infile,'rb')as f:counts,calledfuncs,callers=pickle.load(f)
				self.update(self.__class__(counts,calledfuncs,callers=callers))
			except(OSError,EOFError,ValueError)as err:print('Skipping counts file %r: %s'%(self.infile,err),file=sys.stderr)
	def is_ignored_filename(self,filename):'Return True if the filename does not refer to a file\n        we want to have reported.\n        ';return filename.startswith('<')and filename.endswith('>')
	def update(self,other):
		'Merge in the data from another CoverageResults';counts=self.counts;calledfuncs=self.calledfuncs;callers=self.callers;other_counts=other.counts;other_calledfuncs=other.calledfuncs;other_callers=other.callers
		for key in other_counts:counts[key]=counts.get(key,0)+other_counts[key]
		for key in other_calledfuncs:calledfuncs[key]=1
		for key in other_callers:callers[key]=1
	def write_results(self,show_missing=True,summary=_B,coverdir=_A):
		'\n        Write the coverage results.\n\n        :param show_missing: Show lines that had no hits.\n        :param summary: Include coverage summary per module.\n        :param coverdir: If None, the results of each module are placed in its\n                         directory, otherwise it is included in the directory\n                         specified.\n        ';A='***'
		if self.calledfuncs:
			print();print('functions called:');calls=self.calledfuncs
			for(filename,modulename,funcname)in sorted(calls):print('filename: %s, modulename: %s, funcname: %s'%(filename,modulename,funcname))
		if self.callers:
			print();print('calling relationships:');lastfile=lastcfile=''
			for((pfile,pmod,pfunc),(cfile,cmod,cfunc))in sorted(self.callers):
				if pfile!=lastfile:print();print(A,pfile,A);lastfile=pfile;lastcfile=''
				if cfile!=pfile and lastcfile!=cfile:print('  -->',cfile);lastcfile=cfile
				print('    %s.%s -> %s.%s'%(pmod,pfunc,cmod,cfunc))
		per_file={}
		for(filename,lineno)in self.counts:lines_hit=per_file[filename]=per_file.get(filename,{});lines_hit[lineno]=self.counts[filename,lineno]
		sums={}
		for(filename,count)in per_file.items():
			if self.is_ignored_filename(filename):continue
			if filename.endswith('.pyc'):filename=filename[:-1]
			if coverdir is _A:dir=os.path.dirname(os.path.abspath(filename));modulename=_modname(filename)
			else:
				dir=coverdir
				if not os.path.exists(dir):os.makedirs(dir)
				modulename=_fullmodname(filename)
			if show_missing:lnotab=_find_executable_linenos(filename)
			else:lnotab={}
			source=linecache.getlines(filename);coverpath=os.path.join(dir,modulename+'.cover')
			with open(filename,'rb')as fp:encoding,_=tokenize.detect_encoding(fp.readline)
			n_hits,n_lines=self.write_results_file(coverpath,source,lnotab,count,encoding)
			if summary and n_lines:percent=int(100*n_hits/n_lines);sums[modulename]=n_lines,percent,modulename,filename
		if summary and sums:
			print('lines   cov%   module   (path)')
			for m in sorted(sums):n_lines,percent,modulename,filename=sums[m];print('%5d   %3d%%   %s   (%s)'%sums[m])
		if self.outfile:
			try:
				with open(self.outfile,'wb')as f:pickle.dump((self.counts,self.calledfuncs,self.callers),f,1)
			except OSError as err:print("Can't save counts files because %s"%err,file=sys.stderr)
	def write_results_file(self,path,lines,lnotab,lines_hit,encoding=_A):
		'Return a coverage results file in path.'
		try:outfile=open(path,'w',encoding=encoding)
		except OSError as err:print('trace: Could not open %r for writing: %s - skipping'%(path,err),file=sys.stderr);return 0,0
		n_lines=0;n_hits=0
		with outfile:
			for(lineno,line)in enumerate(lines,1):
				if lineno in lines_hit:outfile.write('%5d: '%lines_hit[lineno]);n_hits+=1;n_lines+=1
				elif lineno in lnotab and not PRAGMA_NOCOVER in line:outfile.write('>>>>>> ');n_lines+=1
				else:outfile.write('       ')
				outfile.write(line.expandtabs(8))
		return n_hits,n_lines
def _find_lines_from_code(code,strs):
	'Return dict where keys are lines in the line number table.';linenos={}
	for(_,lineno)in dis.findlinestarts(code):
		if lineno not in strs:linenos[lineno]=1
	return linenos
def _find_lines(code,strs):
	'Return lineno dict for all code objects reachable from code.';linenos=_find_lines_from_code(code,strs)
	for c in code.co_consts:
		if inspect.iscode(c):linenos.update(_find_lines(c,strs))
	return linenos
def _find_strings(filename,encoding=_A):
	'Return a dict of possible docstring positions.\n\n    The dict maps line numbers to strings.  There is an entry for\n    line that contains only a string or a part of a triple-quoted\n    string.\n    ';d={};prev_ttype=token.INDENT
	with open(filename,encoding=encoding)as f:
		tok=tokenize.generate_tokens(f.readline)
		for(ttype,tstr,start,end,line)in tok:
			if ttype==token.STRING:
				if prev_ttype==token.INDENT:
					sline,scol=start;eline,ecol=end
					for i in range(sline,eline+1):d[i]=1
			prev_ttype=ttype
	return d
def _find_executable_linenos(filename):
	'Return dict where keys are line numbers in the line number table.'
	try:
		with tokenize.open(filename)as f:prog=f.read();encoding=f.encoding
	except OSError as err:print('Not printing coverage data for %r: %s'%(filename,err),file=sys.stderr);return{}
	code=compile(prog,filename,'exec');strs=_find_strings(filename,encoding);return _find_lines(code,strs)
class Trace:
	def __init__(self,count=1,trace=1,countfuncs=0,countcallers=0,ignoremods=(),ignoredirs=(),infile=_A,outfile=_A,timing=_B):
		"\n        @param count true iff it should count number of times each\n                     line is executed\n        @param trace true iff it should print out each line that is\n                     being counted\n        @param countfuncs true iff it should just output a list of\n                     (filename, modulename, funcname,) for functions\n                     that were called at least once;  This overrides\n                     `count' and `trace'\n        @param ignoremods a list of the names of modules to ignore\n        @param ignoredirs a list of the names of directories to ignore\n                     all of the (recursive) contents of\n        @param infile file from which to read stored counts to be\n                     added into the results\n        @param outfile file in which to write the results\n        @param timing true iff timing information be displayed\n        ";self.infile=infile;self.outfile=outfile;self.ignore=_Ignore(ignoremods,ignoredirs);self.counts={};self.pathtobasename={};self.donothing=0;self.trace=trace;self._calledfuncs={};self._callers={};self._caller_cache={};self.start_time=_A
		if timing:self.start_time=_time()
		if countcallers:self.globaltrace=self.globaltrace_trackcallers
		elif countfuncs:self.globaltrace=self.globaltrace_countfuncs
		elif trace and count:self.globaltrace=self.globaltrace_lt;self.localtrace=self.localtrace_trace_and_count
		elif trace:self.globaltrace=self.globaltrace_lt;self.localtrace=self.localtrace_trace
		elif count:self.globaltrace=self.globaltrace_lt;self.localtrace=self.localtrace_count
		else:self.donothing=1
	def run(self,cmd):import __main__;dict=__main__.__dict__;self.runctx(cmd,dict,dict)
	def runctx(self,cmd,globals=_A,locals=_A):
		if globals is _A:globals={}
		if locals is _A:locals={}
		if not self.donothing:threading.settrace(self.globaltrace);sys.settrace(self.globaltrace)
		try:exec(cmd,globals,locals)
		finally:
			if not self.donothing:sys.settrace(_A);threading.settrace(_A)
	def runfunc(self,func,*args,**kw):
		result=_A
		if not self.donothing:sys.settrace(self.globaltrace)
		try:result=func(*args,**kw)
		finally:
			if not self.donothing:sys.settrace(_A)
		return result
	def file_module_function_of(self,frame):
		code=frame.f_code;filename=code.co_filename
		if filename:modulename=_modname(filename)
		else:modulename=_A
		funcname=code.co_name;clsname=_A
		if code in self._caller_cache:
			if self._caller_cache[code]is not _A:clsname=self._caller_cache[code]
		else:
			self._caller_cache[code]=_A;funcs=[f for f in gc.get_referrers(code)if inspect.isfunction(f)]
			if len(funcs)==1:
				dicts=[d for d in gc.get_referrers(funcs[0])if isinstance(d,dict)]
				if len(dicts)==1:
					classes=[c for c in gc.get_referrers(dicts[0])if hasattr(c,'__bases__')]
					if len(classes)==1:clsname=classes[0].__name__;self._caller_cache[code]=clsname
		if clsname is not _A:funcname='%s.%s'%(clsname,funcname)
		return filename,modulename,funcname
	def globaltrace_trackcallers(self,frame,why,arg):
		'Handler for call events.\n\n        Adds information about who called who to the self._callers dict.\n        '
		if why==_C:this_func=self.file_module_function_of(frame);parent_func=self.file_module_function_of(frame.f_back);self._callers[parent_func,this_func]=1
	def globaltrace_countfuncs(self,frame,why,arg):
		'Handler for call events.\n\n        Adds (filename, modulename, funcname) to the self._calledfuncs dict.\n        '
		if why==_C:this_func=self.file_module_function_of(frame);self._calledfuncs[this_func]=1
	def globaltrace_lt(self,frame,why,arg):
		"Handler for call events.\n\n        If the code block being entered is to be ignored, returns `None',\n        else returns self.localtrace.\n        "
		if why==_C:
			code=frame.f_code;filename=frame.f_globals.get(_D,_A)
			if filename:
				modulename=_modname(filename)
				if modulename is not _A:
					ignore_it=self.ignore.names(filename,modulename)
					if not ignore_it:
						if self.trace:print(' --- modulename: %s, funcname: %s'%(modulename,code.co_name))
						return self.localtrace
			else:return
	def localtrace_trace_and_count(self,frame,why,arg):
		if why==_E:
			filename=frame.f_code.co_filename;lineno=frame.f_lineno;key=filename,lineno;self.counts[key]=self.counts.get(key,0)+1
			if self.start_time:print('%.2f'%(_time()-self.start_time),end=' ')
			bname=os.path.basename(filename);print(_G%(bname,lineno,linecache.getline(filename,lineno)),end='')
		return self.localtrace
	def localtrace_trace(self,frame,why,arg):
		if why==_E:
			filename=frame.f_code.co_filename;lineno=frame.f_lineno
			if self.start_time:print('%.2f'%(_time()-self.start_time),end=' ')
			bname=os.path.basename(filename);print(_G%(bname,lineno,linecache.getline(filename,lineno)),end='')
		return self.localtrace
	def localtrace_count(self,frame,why,arg):
		if why==_E:filename=frame.f_code.co_filename;lineno=frame.f_lineno;key=filename,lineno;self.counts[key]=self.counts.get(key,0)+1
		return self.localtrace
	def results(self):return CoverageResults(self.counts,infile=self.infile,outfile=self.outfile,calledfuncs=self._calledfuncs,callers=self._callers)
def main():
	E='__cached__';D='__package__';C='__name__';B='append';A='store_true';import argparse;parser=argparse.ArgumentParser();parser.add_argument('--version',action='version',version='trace 2.0');grp=parser.add_argument_group('Main options','One of these (or --report) must be given');grp.add_argument('-c','--count',action=A,help="Count the number of times each line is executed and write the counts to <module>.cover for each module executed, in the module's directory. See also --coverdir, --file, --no-report below.");grp.add_argument('-t','--trace',action=A,help='Print each line to sys.stdout before it is executed');grp.add_argument('-l','--listfuncs',action=A,help='Keep track of which functions are executed at least once and write the results to sys.stdout after the program exits. Cannot be specified alongside --trace or --count.');grp.add_argument('-T','--trackcalls',action=A,help='Keep track of caller/called pairs and write the results to sys.stdout after the program exits.');grp=parser.add_argument_group('Modifiers');_grp=grp.add_mutually_exclusive_group();_grp.add_argument('-r','--report',action=A,help='Generate a report from a counts file; does not execute any code. --file must specify the results file to read, which must have been created in a previous run with --count --file=FILE');_grp.add_argument('-R','--no-report',action=A,help='Do not generate the coverage report files. Useful if you want to accumulate over several runs.');grp.add_argument('-f','--file',help='File to accumulate counts over several runs');grp.add_argument('-C','--coverdir',help='Directory where the report files go. The coverage report for <package>.<module> will be written to file <dir>/<package>/<module>.cover');grp.add_argument('-m','--missing',action=A,help='Annotate executable lines that were not executed with ">>>>>> "');grp.add_argument('-s','--summary',action=A,help='Write a brief summary for each file to sys.stdout. Can only be used with --count or --report');grp.add_argument('-g','--timing',action=A,help='Prefix each line with the time since the program started. Only used while tracing');grp=parser.add_argument_group('Filters','Can be specified multiple times');grp.add_argument('--ignore-module',action=B,default=[],help='Ignore the given module(s) and its submodules (if it is a package). Accepts comma separated list of module names.');grp.add_argument('--ignore-dir',action=B,default=[],help='Ignore files in the given directory (multiple directories can be joined by os.pathsep).');parser.add_argument('--module',action=A,default=_B,help='Trace a module. ');parser.add_argument('progname',nargs='?',help='file to run as main program');parser.add_argument('arguments',nargs=argparse.REMAINDER,help='arguments to the program');opts=parser.parse_args()
	if opts.ignore_dir:_prefix=sysconfig.get_path('stdlib');_exec_prefix=sysconfig.get_path('platstdlib')
	def parse_ignore_dir(s):s=os.path.expanduser(os.path.expandvars(s));s=s.replace('$prefix',_prefix).replace('$exec_prefix',_exec_prefix);return os.path.normpath(s)
	opts.ignore_module=[mod.strip()for i in opts.ignore_module for mod in i.split(',')];opts.ignore_dir=[parse_ignore_dir(s)for i in opts.ignore_dir for s in i.split(os.pathsep)]
	if opts.report:
		if not opts.file:parser.error('-r/--report requires -f/--file')
		results=CoverageResults(infile=opts.file,outfile=opts.file);return results.write_results(opts.missing,opts.summary,opts.coverdir)
	if not any([opts.trace,opts.count,opts.listfuncs,opts.trackcalls]):parser.error('must specify one of --trace, --count, --report, --listfuncs, or --trackcalls')
	if opts.listfuncs and(opts.count or opts.trace):parser.error('cannot specify both --listfuncs and (--trace or --count)')
	if opts.summary and not opts.count:parser.error('--summary can only be used with --count or --report')
	if opts.progname is _A:parser.error('progname is missing: required with the main options')
	t=Trace(opts.count,opts.trace,countfuncs=opts.listfuncs,countcallers=opts.trackcalls,ignoremods=opts.ignore_module,ignoredirs=opts.ignore_dir,infile=opts.file,outfile=opts.file,timing=opts.timing)
	try:
		if opts.module:import runpy;module_name=opts.progname;mod_name,mod_spec,code=runpy._get_module_details(module_name);sys.argv=[code.co_filename,*opts.arguments];globs={C:_F,_D:code.co_filename,D:mod_spec.parent,'__loader__':mod_spec.loader,'__spec__':mod_spec,E:_A}
		else:
			sys.argv=[opts.progname,*opts.arguments];sys.path[0]=os.path.dirname(opts.progname)
			with open(opts.progname,'rb')as fp:code=compile(fp.read(),opts.progname,'exec')
			globs={_D:opts.progname,C:_F,D:_A,E:_A}
		t.runctx(code,globs,globs)
	except OSError as err:sys.exit('Cannot run file %r because: %s'%(sys.argv[0],err))
	except SystemExit:pass
	results=t.results()
	if not opts.no_report:results.write_results(opts.missing,opts.summary,opts.coverdir)
if __name__==_F:main()