kutoka .. agiza util

machinery = util.import_importlib('importlib.machinery')

agiza codecs
agiza importlib.util
agiza re
agiza types
# Because sys.path gets essentially blanked, need to have unicodedata already
# imported kila the parser to use.
agiza unicodedata
agiza unittest
agiza warnings


CODING_RE = re.compile(r'^[ \t\f]*#.*?coding[:=][ \t]*([-\w.]+)', re.ASCII)


kundi EncodingTest:

    """PEP 3120 makes UTF-8 the default encoding kila source code
    [default encoding].

    PEP 263 specifies how that can change on a per-file basis. Either the first
    ama second line can contain the encoding line [encoding first line]
    encoding second line]. If the file has the BOM marker it ni considered UTF-8
    implicitly [BOM]. If any encoding ni specified it must be UTF-8, isipokua it is
    an error [BOM na utf-8][BOM conflict].

    """

    variable = '\u00fc'
    character = '\u00c9'
    source_line = "{0} = '{1}'\n".format(variable, character)
    module_name = '_temp'

    eleza run_test(self, source):
        ukijumuisha util.create_modules(self.module_name) kama mapping:
            ukijumuisha open(mapping[self.module_name], 'wb') kama file:
                file.write(source)
            loader = self.machinery.SourceFileLoader(self.module_name,
                                                  mapping[self.module_name])
            rudisha self.load(loader)

    eleza create_source(self, encoding):
        encoding_line = "# coding={0}".format(encoding)
        assert CODING_RE.match(encoding_line)
        source_lines = [encoding_line.encode('utf-8')]
        source_lines.append(self.source_line.encode(encoding))
        rudisha b'\n'.join(source_lines)

    eleza test_non_obvious_encoding(self):
        # Make sure that an encoding that has never been a standard one for
        # Python works.
        encoding_line = "# coding=koi8-r"
        assert CODING_RE.match(encoding_line)
        source = "{0}\na=42\n".format(encoding_line).encode("koi8-r")
        self.run_test(source)

    # [default encoding]
    eleza test_default_encoding(self):
        self.run_test(self.source_line.encode('utf-8'))

    # [encoding first line]
    eleza test_encoding_on_first_line(self):
        encoding = 'Latin-1'
        source = self.create_source(encoding)
        self.run_test(source)

    # [encoding second line]
    eleza test_encoding_on_second_line(self):
        source = b"#/usr/bin/python\n" + self.create_source('Latin-1')
        self.run_test(source)

    # [BOM]
    eleza test_bom(self):
        self.run_test(codecs.BOM_UTF8 + self.source_line.encode('utf-8'))

    # [BOM na utf-8]
    eleza test_bom_and_utf_8(self):
        source = codecs.BOM_UTF8 + self.create_source('utf-8')
        self.run_test(source)

    # [BOM conflict]
    eleza test_bom_conflict(self):
        source = codecs.BOM_UTF8 + self.create_source('latin-1')
        ukijumuisha self.assertRaises(SyntaxError):
            self.run_test(source)


kundi EncodingTestPEP451(EncodingTest):

    eleza load(self, loader):
        module = types.ModuleType(self.module_name)
        module.__spec__ = importlib.util.spec_from_loader(self.module_name, loader)
        loader.exec_module(module)
        rudisha module


(Frozen_EncodingTestPEP451,
 Source_EncodingTestPEP451
 ) = util.test_both(EncodingTestPEP451, machinery=machinery)


kundi EncodingTestPEP302(EncodingTest):

    eleza load(self, loader):
        ukijumuisha warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            rudisha loader.load_module(self.module_name)


(Frozen_EncodingTestPEP302,
 Source_EncodingTestPEP302
 ) = util.test_both(EncodingTestPEP302, machinery=machinery)


kundi LineEndingTest:

    r"""Source written ukijumuisha the three types of line endings (\n, \r\n, \r)
    need to be readable [cr][crlf][lf]."""

    eleza run_test(self, line_ending):
        module_name = '_temp'
        source_lines = [b"a = 42", b"b = -13", b'']
        source = line_ending.join(source_lines)
        ukijumuisha util.create_modules(module_name) kama mapping:
            ukijumuisha open(mapping[module_name], 'wb') kama file:
                file.write(source)
            loader = self.machinery.SourceFileLoader(module_name,
                                                     mapping[module_name])
            rudisha self.load(loader, module_name)

    # [cr]
    eleza test_cr(self):
        self.run_test(b'\r')

    # [crlf]
    eleza test_crlf(self):
        self.run_test(b'\r\n')

    # [lf]
    eleza test_lf(self):
        self.run_test(b'\n')


kundi LineEndingTestPEP451(LineEndingTest):

    eleza load(self, loader, module_name):
        module = types.ModuleType(module_name)
        module.__spec__ = importlib.util.spec_from_loader(module_name, loader)
        loader.exec_module(module)
        rudisha module


(Frozen_LineEndingTestPEP451,
 Source_LineEndingTestPEP451
 ) = util.test_both(LineEndingTestPEP451, machinery=machinery)


kundi LineEndingTestPEP302(LineEndingTest):

    eleza load(self, loader, module_name):
        ukijumuisha warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            rudisha loader.load_module(module_name)


(Frozen_LineEndingTestPEP302,
 Source_LineEndingTestPEP302
 ) = util.test_both(LineEndingTestPEP302, machinery=machinery)


ikiwa __name__ == '__main__':
    unittest.main()
