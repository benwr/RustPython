'Bisection algorithms.'
_B='lo must be non-negative'
_A=None
def insort_right(a,x,lo=0,hi=_A,*,key=_A):
	'Insert item x in list a, and keep it sorted assuming a is sorted.\n\n    If x is already in a, insert it to the right of the rightmost x.\n\n    Optional args lo (default 0) and hi (default len(a)) bound the\n    slice of a to be searched.\n    '
	if key is _A:lo=bisect_right(a,x,lo,hi)
	else:lo=bisect_right(a,key(x),lo,hi,key=key)
	a.insert(lo,x)
def bisect_right(a,x,lo=0,hi=_A,*,key=_A):
	'Return the index where to insert item x in list a, assuming a is sorted.\n\n    The return value i is such that all e in a[:i] have e <= x, and all e in\n    a[i:] have e > x.  So if x already appears in the list, a.insert(i, x) will\n    insert just after the rightmost x already there.\n\n    Optional args lo (default 0) and hi (default len(a)) bound the\n    slice of a to be searched.\n    '
	if lo<0:raise ValueError(_B)
	if hi is _A:hi=len(a)
	if key is _A:
		while lo<hi:
			mid=(lo+hi)//2
			if x<a[mid]:hi=mid
			else:lo=mid+1
	else:
		while lo<hi:
			mid=(lo+hi)//2
			if x<key(a[mid]):hi=mid
			else:lo=mid+1
	return lo
def insort_left(a,x,lo=0,hi=_A,*,key=_A):
	'Insert item x in list a, and keep it sorted assuming a is sorted.\n\n    If x is already in a, insert it to the left of the leftmost x.\n\n    Optional args lo (default 0) and hi (default len(a)) bound the\n    slice of a to be searched.\n    '
	if key is _A:lo=bisect_left(a,x,lo,hi)
	else:lo=bisect_left(a,key(x),lo,hi,key=key)
	a.insert(lo,x)
def bisect_left(a,x,lo=0,hi=_A,*,key=_A):
	'Return the index where to insert item x in list a, assuming a is sorted.\n\n    The return value i is such that all e in a[:i] have e < x, and all e in\n    a[i:] have e >= x.  So if x already appears in the list, a.insert(i, x) will\n    insert just before the leftmost x already there.\n\n    Optional args lo (default 0) and hi (default len(a)) bound the\n    slice of a to be searched.\n    '
	if lo<0:raise ValueError(_B)
	if hi is _A:hi=len(a)
	if key is _A:
		while lo<hi:
			mid=(lo+hi)//2
			if a[mid]<x:lo=mid+1
			else:hi=mid
	else:
		while lo<hi:
			mid=(lo+hi)//2
			if key(a[mid])<x:lo=mid+1
			else:hi=mid
	return lo
try:from _bisect import*
except ImportError:pass
bisect=bisect_right
insort=insort_right