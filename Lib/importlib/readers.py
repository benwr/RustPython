'\nCompatibility shim for .resources.readers as found on Python 3.10.\n\nConsumers that can rely on Python 3.11 should use the other\nmodule directly.\n'
from.resources.readers import FileReader,ZipReader,MultiplexedPath,NamespaceReader
__all__=['FileReader','ZipReader','MultiplexedPath','NamespaceReader']