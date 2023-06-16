'Conversion functions between RGB and other color systems.\nThis modules provides two functions for each color system ABC:\n  rgb_to_abc(r, g, b) --> a, b, c\n  abc_to_rgb(a, b, c) --> r, g, b\nAll inputs and outputs are triples of floats in the range [0.0...1.0]\n(with the exception of I and Q, which covers a slightly larger range).\nInputs outside the valid range may cause exceptions or invalid outputs.\nSupported color systems:\nRGB: Red, Green, Blue components\nYIQ: Luminance, Chrominance (used by composite video signals)\nHLS: Hue, Luminance, Saturation\nHSV: Hue, Saturation, Value\n'
_B=.0
_A=1.
__all__=['rgb_to_yiq','yiq_to_rgb','rgb_to_hls','hls_to_rgb','rgb_to_hsv','hsv_to_rgb']
ONE_THIRD=_A/3.
ONE_SIXTH=_A/6.
TWO_THIRD=2./3.
def rgb_to_yiq(r,g,b):A=.3*r+.59*g+.11*b;B=.74*(r-A)-.27*(b-A);C=.48*(r-A)+.41*(b-A);return A,B,C
def yiq_to_rgb(y,i,q):
	A=y+.9468822170900693*i+.6235565819861433*q;B=y-.27478764629897834*i-.6356910791873801*q;C=y-1.1085450346420322*i+1.7090069284064666*q
	if A<_B:A=_B
	if B<_B:B=_B
	if C<_B:C=_B
	if A>_A:A=_A
	if B>_A:B=_A
	if C>_A:C=_A
	return A,B,C
def rgb_to_hls(r,g,b):
	A=max(r,g,b);B=min(r,g,b);D=(B+A)/2.
	if B==A:return _B,D,_B
	if D<=.5:E=(A-B)/(A+B)
	else:E=(A-B)/(2.-A-B)
	F=(A-r)/(A-B);G=(A-g)/(A-B);H=(A-b)/(A-B)
	if r==A:C=H-G
	elif g==A:C=2.+F-H
	else:C=4.+G-F
	C=C/6.%_A;return C,D,E
def hls_to_rgb(h,l,s):
	if s==_B:return l,l,l
	if l<=.5:A=l*(_A+s)
	else:A=l+s-l*s
	B=2.*l-A;return _v(B,A,h+ONE_THIRD),_v(B,A,h),_v(B,A,h-ONE_THIRD)
def _v(m1,m2,hue):
	B=m1;A=hue;A=A%_A
	if A<ONE_SIXTH:return B+(m2-B)*A*6.
	if A<.5:return m2
	if A<TWO_THIRD:return B+(m2-B)*(TWO_THIRD-A)*6.
	return B
def rgb_to_hsv(r,g,b):
	A=max(r,g,b);B=min(r,g,b);D=A
	if B==A:return _B,_B,D
	H=(A-B)/A;E=(A-r)/(A-B);F=(A-g)/(A-B);G=(A-b)/(A-B)
	if r==A:C=G-F
	elif g==A:C=2.+E-G
	else:C=4.+F-E
	C=C/6.%_A;return C,H,D
def hsv_to_rgb(h,s,v):
	if s==_B:return v,v,v
	A=int(h*6.);E=h*6.-A;B=v*(_A-s);C=v*(_A-s*E);D=v*(_A-s*(_A-E));A=A%6
	if A==0:return v,D,B
	if A==1:return C,v,B
	if A==2:return B,v,D
	if A==3:return B,C,v
	if A==4:return D,B,v
	if A==5:return v,B,C