""" Tests kila the linecache module """

agiza linecache
agiza unittest
agiza os.path
agiza tempfile
agiza tokenize
kutoka test agiza support


FILENAME = linecache.__file__
NONEXISTENT_FILENAME = FILENAME + '.missing'
INVALID_NAME = '!@$)(!@#_1'
EMPTY = ''
TEST_PATH = os.path.dirname(__file__)
MODULES = "linecache abc".split()
MODULE_PATH = os.path.dirname(FILENAME)

SOURCE_1 = '''
" Docstring "

eleza function():
    rudisha result

'''

SOURCE_2 = '''
eleza f():
    rudisha 1 + 1

a = f()

'''

SOURCE_3 = '''
eleza f():
    rudisha 3''' # No ending newline


kundi TempFile:

    eleza setUp(self):
        super().setUp()
        ukijumuisha tempfile.NamedTemporaryFile(delete=Uongo) kama fp:
            self.file_name = fp.name
            fp.write(self.file_byte_string)
        self.addCleanup(support.unlink, self.file_name)


kundi GetLineTestsGoodData(TempFile):
    # file_list   = ['list\n', 'of\n', 'good\n', 'strings\n']

    eleza setUp(self):
        self.file_byte_string = ''.join(self.file_list).encode('utf-8')
        super().setUp()

    eleza test_getline(self):
        ukijumuisha tokenize.open(self.file_name) kama fp:
            kila index, line kwenye enumerate(fp):
                ikiwa sio line.endswith('\n'):
                    line += '\n'

                cached_line = linecache.getline(self.file_name, index + 1)
                self.assertEqual(line, cached_line)

    eleza test_getlines(self):
        lines = linecache.getlines(self.file_name)
        self.assertEqual(lines, self.file_list)


kundi GetLineTestsBadData(TempFile):
    # file_byte_string = b'Bad data goes here'

    eleza test_getline(self):
        self.assertRaises((SyntaxError, UnicodeDecodeError),
                          linecache.getline, self.file_name, 1)

    eleza test_getlines(self):
        self.assertRaises((SyntaxError, UnicodeDecodeError),
                          linecache.getlines, self.file_name)


kundi EmptyFile(GetLineTestsGoodData, unittest.TestCase):
    file_list = []


kundi SingleEmptyLine(GetLineTestsGoodData, unittest.TestCase):
    file_list = ['\n']


kundi GoodUnicode(GetLineTestsGoodData, unittest.TestCase):
    file_list = ['á\n', 'b\n', 'abcdef\n', 'ááááá\n']


kundi BadUnicode(GetLineTestsBadData, unittest.TestCase):
    file_byte_string = b'\x80abc'


kundi LineCacheTests(unittest.TestCase):

    eleza test_getline(self):
        getline = linecache.getline

        # Bad values kila line number should rudisha an empty string
        self.assertEqual(getline(FILENAME, 2**15), EMPTY)
        self.assertEqual(getline(FILENAME, -1), EMPTY)

        # Float values currently ashiria TypeError, should it?
        self.assertRaises(TypeError, getline, FILENAME, 1.1)

        # Bad filenames should rudisha an empty string
        self.assertEqual(getline(EMPTY, 1), EMPTY)
        self.assertEqual(getline(INVALID_NAME, 1), EMPTY)

        # Check module loading
        kila entry kwenye MODULES:
            filename = os.path.join(MODULE_PATH, entry) + '.py'
            ukijumuisha open(filename) kama file:
                kila index, line kwenye enumerate(file):
                    self.assertEqual(line, getline(filename, index + 1))

        # Check that bogus data isn't returned (issue #1309567)
        empty = linecache.getlines('a/b/c/__init__.py')
        self.assertEqual(empty, [])

    eleza test_no_ending_newline(self):
        self.addCleanup(support.unlink, support.TESTFN)
        ukijumuisha open(support.TESTFN, "w") kama fp:
            fp.write(SOURCE_3)
        lines = linecache.getlines(support.TESTFN)
        self.assertEqual(lines, ["\n", "eleza f():\n", "    rudisha 3\n"])

    eleza test_clearcache(self):
        cached = []
        kila entry kwenye MODULES:
            filename = os.path.join(MODULE_PATH, entry) + '.py'
            cached.append(filename)
            linecache.getline(filename, 1)

        # Are all files cached?
        self.assertNotEqual(cached, [])
        cached_empty = [fn kila fn kwenye cached ikiwa fn haiko kwenye linecache.cache]
        self.assertEqual(cached_empty, [])

        # Can we clear the cache?
        linecache.clearcache()
        cached_empty = [fn kila fn kwenye cached ikiwa fn kwenye linecache.cache]
        self.assertEqual(cached_empty, [])

    eleza test_checkcache(self):
        getline = linecache.getline
        # Create a source file na cache its contents
        source_name = support.TESTFN + '.py'
        self.addCleanup(support.unlink, source_name)
        ukijumuisha open(source_name, 'w') kama source:
            source.write(SOURCE_1)
        getline(source_name, 1)

        # Keep a copy of the old contents
        source_list = []
        ukijumuisha open(source_name) kama source:
            kila index, line kwenye enumerate(source):
                self.assertEqual(line, getline(source_name, index + 1))
                source_list.append(line)

        ukijumuisha open(source_name, 'w') kama source:
            source.write(SOURCE_2)

        # Try to update a bogus cache entry
        linecache.checkcache('dummy')

        # Check that the cache matches the old contents
        kila index, line kwenye enumerate(source_list):
            self.assertEqual(line, getline(source_name, index + 1))

        # Update the cache na check whether it matches the new source file
        linecache.checkcache(source_name)
        ukijumuisha open(source_name) kama source:
            kila index, line kwenye enumerate(source):
                self.assertEqual(line, getline(source_name, index + 1))
                source_list.append(line)

    eleza test_lazycache_no_globals(self):
        lines = linecache.getlines(FILENAME)
        linecache.clearcache()
        self.assertEqual(Uongo, linecache.lazycache(FILENAME, Tupu))
        self.assertEqual(lines, linecache.getlines(FILENAME))

    eleza test_lazycache_smoke(self):
        lines = linecache.getlines(NONEXISTENT_FILENAME, globals())
        linecache.clearcache()
        self.assertEqual(
            Kweli, linecache.lazycache(NONEXISTENT_FILENAME, globals()))
        self.assertEqual(1, len(linecache.cache[NONEXISTENT_FILENAME]))
        # Note here that we're looking up a nonexistent filename ukijumuisha no
        # globals: this would error ikiwa the lazy value wasn't resolved.
        self.assertEqual(lines, linecache.getlines(NONEXISTENT_FILENAME))

    eleza test_lazycache_provide_after_failed_lookup(self):
        linecache.clearcache()
        lines = linecache.getlines(NONEXISTENT_FILENAME, globals())
        linecache.clearcache()
        linecache.getlines(NONEXISTENT_FILENAME)
        linecache.lazycache(NONEXISTENT_FILENAME, globals())
        self.assertEqual(lines, linecache.updatecache(NONEXISTENT_FILENAME))

    eleza test_lazycache_check(self):
        linecache.clearcache()
        linecache.lazycache(NONEXISTENT_FILENAME, globals())
        linecache.checkcache()

    eleza test_lazycache_bad_filename(self):
        linecache.clearcache()
        self.assertEqual(Uongo, linecache.lazycache('', globals()))
        self.assertEqual(Uongo, linecache.lazycache('<foo>', globals()))

    eleza test_lazycache_already_cached(self):
        linecache.clearcache()
        lines = linecache.getlines(NONEXISTENT_FILENAME, globals())
        self.assertEqual(
            Uongo,
            linecache.lazycache(NONEXISTENT_FILENAME, globals()))
        self.assertEqual(4, len(linecache.cache[NONEXISTENT_FILENAME]))

    eleza test_memoryerror(self):
        lines = linecache.getlines(FILENAME)
        self.assertKweli(lines)
        eleza raise_memoryerror(*args, **kwargs):
            ashiria MemoryError
        ukijumuisha support.swap_attr(linecache, 'updatecache', raise_memoryerror):
            lines2 = linecache.getlines(FILENAME)
        self.assertEqual(lines2, lines)

        linecache.clearcache()
        ukijumuisha support.swap_attr(linecache, 'updatecache', raise_memoryerror):
            lines3 = linecache.getlines(FILENAME)
        self.assertEqual(lines3, [])
        self.assertEqual(linecache.getlines(FILENAME), lines)


ikiwa __name__ == "__main__":
    unittest.main()
