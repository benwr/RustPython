_B='prepare() must be called first'
_A=None
from types import GenericAlias
__all__=['TopologicalSorter','CycleError']
_NODE_OUT=-1
_NODE_DONE=-2
class _NodeInfo:
	__slots__='node','npredecessors','successors'
	def __init__(A,node):A.node=node;A.npredecessors=0;A.successors=[]
class CycleError(ValueError):'Subclass of ValueError raised by TopologicalSorter.prepare if cycles\n    exist in the working graph.\n\n    If multiple cycles exist, only one undefined choice among them will be reported\n    and included in the exception. The detected cycle can be accessed via the second\n    element in the *args* attribute of the exception instance and consists in a list\n    of nodes, such that each node is, in the graph, an immediate predecessor of the\n    next node in the list. In the reported list, the first and the last node will be\n    the same, to make it clear that it is cyclic.\n    '
class TopologicalSorter:
	'Provides functionality to topologically sort a graph of hashable nodes'
	def __init__(A,graph=_A):
		B=graph;A._node2info={};A._ready_nodes=_A;A._npassedout=0;A._nfinished=0
		if B is not _A:
			for(C,D)in B.items():A.add(C,*D)
	def _get_nodeinfo(B,node):
		A=node
		if(C:=B._node2info.get(A))is _A:B._node2info[A]=C=_NodeInfo(A)
		return C
	def add(A,node,*B):
		'Add a new node and its predecessors to the graph.\n\n        Both the *node* and all elements in *predecessors* must be hashable.\n\n        If called multiple times with the same node argument, the set of dependencies\n        will be the union of all dependencies passed in.\n\n        It is possible to add a node with no dependencies (*predecessors* is not provided)\n        as well as provide a dependency twice. If a node that has not been provided before\n        is included among *predecessors* it will be automatically added to the graph with\n        no predecessors of its own.\n\n        Raises ValueError if called after "prepare".\n        '
		if A._ready_nodes is not _A:raise ValueError('Nodes cannot be added after a call to prepare()')
		C=A._get_nodeinfo(node);C.npredecessors+=len(B)
		for D in B:E=A._get_nodeinfo(D);E.successors.append(node)
	def prepare(A):
		'Mark the graph as finished and check for cycles in the graph.\n\n        If any cycle is detected, "CycleError" will be raised, but "get_ready" can\n        still be used to obtain as many nodes as possible until cycles block more\n        progress. After a call to this function, the graph cannot be modified and\n        therefore no more nodes can be added using "add".\n        '
		if A._ready_nodes is not _A:raise ValueError('cannot prepare() more than once')
		A._ready_nodes=[A.node for A in A._node2info.values()if A.npredecessors==0];B=A._find_cycle()
		if B:raise CycleError(f"nodes are in a cycle",B)
	def get_ready(A):
		'Return a tuple of all the nodes that are ready.\n\n        Initially it returns all nodes with no predecessors; once those are marked\n        as processed by calling "done", further calls will return all new nodes that\n        have all their predecessors already processed. Once no more progress can be made,\n        empty tuples are returned.\n\n        Raises ValueError if called without calling "prepare" previously.\n        '
		if A._ready_nodes is _A:raise ValueError(_B)
		B=tuple(A._ready_nodes);C=A._node2info
		for D in B:C[D].npredecessors=_NODE_OUT
		A._ready_nodes.clear();A._npassedout+=len(B);return B
	def is_active(A):
		'Return ``True`` if more progress can be made and ``False`` otherwise.\n\n        Progress can be made if cycles do not block the resolution and either there\n        are still nodes ready that haven\'t yet been returned by "get_ready" or the\n        number of nodes marked "done" is less than the number that have been returned\n        by "get_ready".\n\n        Raises ValueError if called without calling "prepare" previously.\n        '
		if A._ready_nodes is _A:raise ValueError(_B)
		return A._nfinished<A._npassedout or bool(A._ready_nodes)
	def __bool__(A):return A.is_active()
	def done(B,*H):
		'Marks a set of nodes returned by "get_ready" as processed.\n\n        This method unblocks any successor of each node in *nodes* for being returned\n        in the future by a call to "get_ready".\n\n        Raises :exec:`ValueError` if any node in *nodes* has already been marked as\n        processed by a previous call to this method, if a node was not added to the\n        graph by using "add" or if called without calling "prepare" previously or if\n        node has not yet been returned by "get_ready".\n        '
		if B._ready_nodes is _A:raise ValueError(_B)
		E=B._node2info
		for A in H:
			if(D:=E.get(A))is _A:raise ValueError(f"node {A!r} was not added using add()")
			C=D.npredecessors
			if C!=_NODE_OUT:
				if C>=0:raise ValueError(f"node {A!r} was not passed out (still not ready)")
				elif C==_NODE_DONE:raise ValueError(f"node {A!r} was already marked done")
				else:assert False,f"node {A!r}: unknown status {C}"
			D.npredecessors=_NODE_DONE
			for F in D.successors:
				G=E[F];G.npredecessors-=1
				if G.npredecessors==0:B._ready_nodes.append(F)
			B._nfinished+=1
	def _find_cycle(G):
		F=G._node2info;B=[];D=[];E=set();C={}
		for A in F:
			if A in E:continue
			while True:
				if A in E:
					if A in C:return B[C[A]:]+[A]
				else:E.add(A);D.append(iter(F[A].successors).__next__);C[A]=len(B);B.append(A)
				while B:
					try:A=D[-1]();break
					except StopIteration:del C[B.pop()];D.pop()
				else:break
	def static_order(A):
		'Returns an iterable of nodes in a topological order.\n\n        The particular order that is returned may depend on the specific\n        order in which the items were inserted in the graph.\n\n        Using this method does not require to call "prepare" or "done". If any\n        cycle is detected, :exc:`CycleError` will be raised.\n        ';A.prepare()
		while A.is_active():B=A.get_ready();yield from B;A.done(*B)
	__class_getitem__=classmethod(GenericAlias)