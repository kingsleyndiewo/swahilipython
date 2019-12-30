"""Tests kila distutils.filelist."""
agiza os
agiza re
agiza unittest
kutoka distutils agiza debug
kutoka distutils.log agiza WARN
kutoka distutils.errors agiza DistutilsTemplateError
kutoka distutils.filelist agiza glob_to_re, translate_pattern, FileList
kutoka distutils agiza filelist

agiza test.support
kutoka test.support agiza captured_stdout, run_unittest
kutoka distutils.tests agiza support

MANIFEST_IN = """\
include ok
include xo
exclude xo
include foo.tmp
include buildout.cfg
global-include *.x
global-include *.txt
global-exclude *.tmp
recursive-include f *.oo
recursive-exclude global *.x
graft dir
prune dir3
"""


eleza make_local_path(s):
    """Converts '/' kwenye a string to os.sep"""
    rudisha s.replace('/', os.sep)


kundi FileListTestCase(support.LoggingSilencer,
                       unittest.TestCase):

    eleza assertNoWarnings(self):
        self.assertEqual(self.get_logs(WARN), [])
        self.clear_logs()

    eleza assertWarnings(self):
        self.assertGreater(len(self.get_logs(WARN)), 0)
        self.clear_logs()

    eleza test_glob_to_re(self):
        sep = os.sep
        ikiwa os.sep == '\\':
            sep = re.escape(os.sep)

        kila glob, regex kwenye (
            # simple cases
            ('foo*', r'(?s:foo[^%(sep)s]*)\Z'),
            ('foo?', r'(?s:foo[^%(sep)s])\Z'),
            ('foo??', r'(?s:foo[^%(sep)s][^%(sep)s])\Z'),
            # special cases
            (r'foo\\*', r'(?s:foo\\\\[^%(sep)s]*)\Z'),
            (r'foo\\\*', r'(?s:foo\\\\\\[^%(sep)s]*)\Z'),
            ('foo????', r'(?s:foo[^%(sep)s][^%(sep)s][^%(sep)s][^%(sep)s])\Z'),
            (r'foo\\??', r'(?s:foo\\\\[^%(sep)s][^%(sep)s])\Z')):
            regex = regex % {'sep': sep}
            self.assertEqual(glob_to_re(glob), regex)

    eleza test_process_template_line(self):
        # testing  all MANIFEST.in template patterns
        file_list = FileList()
        l = make_local_path

        # simulated file list
        file_list.allfiles = ['foo.tmp', 'ok', 'xo', 'four.txt',
                              'buildout.cfg',
                              # filelist does sio filter out VCS directories,
                              # it's sdist that does
                              l('.hg/last-message.txt'),
                              l('global/one.txt'),
                              l('global/two.txt'),
                              l('global/files.x'),
                              l('global/here.tmp'),
                              l('f/o/f.oo'),
                              l('dir/graft-one'),
                              l('dir/dir2/graft2'),
                              l('dir3/ok'),
                              l('dir3/sub/ok.txt'),
                             ]

        kila line kwenye MANIFEST_IN.split('\n'):
            ikiwa line.strip() == '':
                endelea
            file_list.process_template_line(line)

        wanted = ['ok',
                  'buildout.cfg',
                  'four.txt',
                  l('.hg/last-message.txt'),
                  l('global/one.txt'),
                  l('global/two.txt'),
                  l('f/o/f.oo'),
                  l('dir/graft-one'),
                  l('dir/dir2/graft2'),
                 ]

        self.assertEqual(file_list.files, wanted)

    eleza test_debug_andika(self):
        file_list = FileList()
        ukijumuisha captured_stdout() kama stdout:
            file_list.debug_andika('xxx')
        self.assertEqual(stdout.getvalue(), '')

        debug.DEBUG = Kweli
        jaribu:
            ukijumuisha captured_stdout() kama stdout:
                file_list.debug_andika('xxx')
            self.assertEqual(stdout.getvalue(), 'xxx\n')
        mwishowe:
            debug.DEBUG = Uongo

    eleza test_set_allfiles(self):
        file_list = FileList()
        files = ['a', 'b', 'c']
        file_list.set_allfiles(files)
        self.assertEqual(file_list.allfiles, files)

    eleza test_remove_duplicates(self):
        file_list = FileList()
        file_list.files = ['a', 'b', 'a', 'g', 'c', 'g']
        # files must be sorted beforehand (sdist does it)
        file_list.sort()
        file_list.remove_duplicates()
        self.assertEqual(file_list.files, ['a', 'b', 'c', 'g'])

    eleza test_translate_pattern(self):
        # sio regex
        self.assertKweli(hasattr(
            translate_pattern('a', anchor=Kweli, is_regex=Uongo),
            'search'))

        # ni a regex
        regex = re.compile('a')
        self.assertEqual(
            translate_pattern(regex, anchor=Kweli, is_regex=Kweli),
            regex)

        # plain string flagged kama regex
        self.assertKweli(hasattr(
            translate_pattern('a', anchor=Kweli, is_regex=Kweli),
            'search'))

        # glob support
        self.assertKweli(translate_pattern(
            '*.py', anchor=Kweli, is_regex=Uongo).search('filelist.py'))

    eleza test_exclude_pattern(self):
        # rudisha Uongo ikiwa no match
        file_list = FileList()
        self.assertUongo(file_list.exclude_pattern('*.py'))

        # rudisha Kweli ikiwa files match
        file_list = FileList()
        file_list.files = ['a.py', 'b.py']
        self.assertKweli(file_list.exclude_pattern('*.py'))

        # test excludes
        file_list = FileList()
        file_list.files = ['a.py', 'a.txt']
        file_list.exclude_pattern('*.py')
        self.assertEqual(file_list.files, ['a.txt'])

    eleza test_include_pattern(self):
        # rudisha Uongo ikiwa no match
        file_list = FileList()
        file_list.set_allfiles([])
        self.assertUongo(file_list.include_pattern('*.py'))

        # rudisha Kweli ikiwa files match
        file_list = FileList()
        file_list.set_allfiles(['a.py', 'b.txt'])
        self.assertKweli(file_list.include_pattern('*.py'))

        # test * matches all files
        file_list = FileList()
        self.assertIsTupu(file_list.allfiles)
        file_list.set_allfiles(['a.py', 'b.txt'])
        file_list.include_pattern('*')
        self.assertEqual(file_list.allfiles, ['a.py', 'b.txt'])

    eleza test_process_template(self):
        l = make_local_path
        # invalid lines
        file_list = FileList()
        kila action kwenye ('include', 'exclude', 'global-include',
                       'global-exclude', 'recursive-include',
                       'recursive-exclude', 'graft', 'prune', 'blarg'):
            self.assertRaises(DistutilsTemplateError,
                              file_list.process_template_line, action)

        # include
        file_list = FileList()
        file_list.set_allfiles(['a.py', 'b.txt', l('d/c.py')])

        file_list.process_template_line('include *.py')
        self.assertEqual(file_list.files, ['a.py'])
        self.assertNoWarnings()

        file_list.process_template_line('include *.rb')
        self.assertEqual(file_list.files, ['a.py'])
        self.assertWarnings()

        # exclude
        file_list = FileList()
        file_list.files = ['a.py', 'b.txt', l('d/c.py')]

        file_list.process_template_line('exclude *.py')
        self.assertEqual(file_list.files, ['b.txt', l('d/c.py')])
        self.assertNoWarnings()

        file_list.process_template_line('exclude *.rb')
        self.assertEqual(file_list.files, ['b.txt', l('d/c.py')])
        self.assertWarnings()

        # global-include
        file_list = FileList()
        file_list.set_allfiles(['a.py', 'b.txt', l('d/c.py')])

        file_list.process_template_line('global-include *.py')
        self.assertEqual(file_list.files, ['a.py', l('d/c.py')])
        self.assertNoWarnings()

        file_list.process_template_line('global-include *.rb')
        self.assertEqual(file_list.files, ['a.py', l('d/c.py')])
        self.assertWarnings()

        # global-exclude
        file_list = FileList()
        file_list.files = ['a.py', 'b.txt', l('d/c.py')]

        file_list.process_template_line('global-exclude *.py')
        self.assertEqual(file_list.files, ['b.txt'])
        self.assertNoWarnings()

        file_list.process_template_line('global-exclude *.rb')
        self.assertEqual(file_list.files, ['b.txt'])
        self.assertWarnings()

        # recursive-include
        file_list = FileList()
        file_list.set_allfiles(['a.py', l('d/b.py'), l('d/c.txt'),
                                l('d/d/e.py')])

        file_list.process_template_line('recursive-include d *.py')
        self.assertEqual(file_list.files, [l('d/b.py'), l('d/d/e.py')])
        self.assertNoWarnings()

        file_list.process_template_line('recursive-include e *.py')
        self.assertEqual(file_list.files, [l('d/b.py'), l('d/d/e.py')])
        self.assertWarnings()

        # recursive-exclude
        file_list = FileList()
        file_list.files = ['a.py', l('d/b.py'), l('d/c.txt'), l('d/d/e.py')]

        file_list.process_template_line('recursive-exclude d *.py')
        self.assertEqual(file_list.files, ['a.py', l('d/c.txt')])
        self.assertNoWarnings()

        file_list.process_template_line('recursive-exclude e *.py')
        self.assertEqual(file_list.files, ['a.py', l('d/c.txt')])
        self.assertWarnings()

        # graft
        file_list = FileList()
        file_list.set_allfiles(['a.py', l('d/b.py'), l('d/d/e.py'),
                                l('f/f.py')])

        file_list.process_template_line('graft d')
        self.assertEqual(file_list.files, [l('d/b.py'), l('d/d/e.py')])
        self.assertNoWarnings()

        file_list.process_template_line('graft e')
        self.assertEqual(file_list.files, [l('d/b.py'), l('d/d/e.py')])
        self.assertWarnings()

        # prune
        file_list = FileList()
        file_list.files = ['a.py', l('d/b.py'), l('d/d/e.py'), l('f/f.py')]

        file_list.process_template_line('prune d')
        self.assertEqual(file_list.files, ['a.py', l('f/f.py')])
        self.assertNoWarnings()

        file_list.process_template_line('prune e')
        self.assertEqual(file_list.files, ['a.py', l('f/f.py')])
        self.assertWarnings()


kundi FindAllTestCase(unittest.TestCase):
    @test.support.skip_unless_symlink
    eleza test_missing_symlink(self):
        ukijumuisha test.support.temp_cwd():
            os.symlink('foo', 'bar')
            self.assertEqual(filelist.findall(), [])

    eleza test_basic_discovery(self):
        """
        When findall ni called ukijumuisha no parameters ama with
        '.' kama the parameter, the dot should be omitted from
        the results.
        """
        ukijumuisha test.support.temp_cwd():
            os.mkdir('foo')
            file1 = os.path.join('foo', 'file1.txt')
            test.support.create_empty_file(file1)
            os.mkdir('bar')
            file2 = os.path.join('bar', 'file2.txt')
            test.support.create_empty_file(file2)
            expected = [file2, file1]
            self.assertEqual(sorted(filelist.findall()), expected)

    eleza test_non_local_discovery(self):
        """
        When findall ni called ukijumuisha another path, the full
        path name should be returned.
        """
        ukijumuisha test.support.temp_dir() kama temp_dir:
            file1 = os.path.join(temp_dir, 'file1.txt')
            test.support.create_empty_file(file1)
            expected = [file1]
            self.assertEqual(filelist.findall(temp_dir), expected)


eleza test_suite():
    rudisha unittest.TestSuite([
        unittest.makeSuite(FileListTestCase),
        unittest.makeSuite(FindAllTestCase),
    ])


ikiwa __name__ == "__main__":
    run_unittest(test_suite())
