" Python 'utf-8' Codec\n\n\nWritten by Marc-Andre Lemburg (mal@lemburg.com).\n\n(c) Copyright CNRI, All Rights Reserved. NO WARRANTY.\n\n"
import codecs
encode=codecs.utf_8_encode
def decode(input,errors='strict'):return codecs.utf_8_decode(input,errors,True)
class IncrementalEncoder(codecs.IncrementalEncoder):
	def encode(A,input,final=False):return codecs.utf_8_encode(input,A.errors)[0]
class IncrementalDecoder(codecs.BufferedIncrementalDecoder):_buffer_decode=codecs.utf_8_decode
class StreamWriter(codecs.StreamWriter):encode=codecs.utf_8_encode
class StreamReader(codecs.StreamReader):decode=codecs.utf_8_decode
def getregentry():return codecs.CodecInfo(name='utf-8',encode=encode,decode=decode,incrementalencoder=IncrementalEncoder,incrementaldecoder=IncrementalDecoder,streamreader=StreamReader,streamwriter=StreamWriter)