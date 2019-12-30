"""zipagiza provides support for agizaing Python modules kutoka Zip archives.

This module exports three objects:
- zipimporter: a class; its constructor takes a path to a Zip archive.
- ZipImportError: exception raised by zipimporter objects. It's a
  subkundi of ImportError, so it can be caught as ImportError, too.
- _zip_directory_cache: a dict, mapping archive paths to zip directory
  info dicts, as used in zipimporter._files.

It is usually sio needed to use the zipagiza module explicitly; it is
used by the builtin agiza mechanism for sys.path items that are paths
to Zip archives.
"""

#kutoka importlib agiza _bootstrap_external
#kutoka importlib agiza _bootstrap  # for _verbose_message
agiza _frozen_importlib_external as _bootstrap_external
kutoka _frozen_importlib_external agiza _unpack_uint16, _unpack_uint32
agiza _frozen_importlib as _bootstrap  # for _verbose_message
agiza _imp  # for check_hash_based_pycs
agiza _io  # for open
agiza marshal  # for loads
agiza sys  # for modules
agiza time  # for mktime

__all__ = ['ZipImportError', 'zipimporter']


path_sep = _bootstrap_external.path_sep
alt_path_sep = _bootstrap_external.path_separators[1:]


kundi ZipImportError(ImportError):
    pass

# _read_directory() cache
_zip_directory_cache = {}

_module_type = type(sys)

END_CENTRAL_DIR_SIZE = 22
STRING_END_ARCHIVE = b'PK\x05\x06'
MAX_COMMENT_LEN = (1 << 16) - 1

kundi zipimporter:
    """zipimporter(archivepath) -> zipimporter object

    Create a new zipimporter instance. 'archivepath' must be a path to
    a zipfile, or to a specific path inside a zipfile. For example, it can be
    '/tmp/myagiza.zip', or '/tmp/myagiza.zip/mydirectory', if mydirectory is a
    valid directory inside the archive.

    'ZipImportError is raised if 'archivepath' doesn't point to a valid Zip
    archive.

    The 'archive' attribute of zipimporter objects contains the name of the
    zipfile targeted.
    """

    # Split the "subdirectory" kutoka the Zip archive path, lookup a matching
    # entry in sys.path_importer_cache, fetch the file directory kutoka there
    # if found, or isipokua read it kutoka the archive.
    def __init__(self, path):
        if sio isinstance(path, str):
            agiza os
            path = os.fsdecode(path)
        if sio path:
            ashiria ZipImportError('archive path is empty', path=path)
        if alt_path_sep:
            path = path.replace(alt_path_sep, path_sep)

        prefix = []
        wakati True:
            jaribu:
                st = _bootstrap_external._path_stat(path)
            tatizo (OSError, ValueError):
                # On Windows a ValueError is raised for too long paths.
                # Back up one path element.
                dirname, basename = _bootstrap_external._path_split(path)
                if dirname == path:
                    ashiria ZipImportError('not a Zip file', path=path)
                path = dirname
                prefix.append(basename)
            isipokua:
                # it exists
                if (st.st_mode & 0o170000) != 0o100000:  # stat.S_ISREG
                    # it's a sio file
                    ashiria ZipImportError('not a Zip file', path=path)
                koma

        jaribu:
            files = _zip_directory_cache[path]
        tatizo KeyError:
            files = _read_directory(path)
            _zip_directory_cache[path] = files
        self._files = files
        self.archive = path
        # a prefix directory following the ZIP file path.
        self.prefix = _bootstrap_external._path_join(*prefix[::-1])
        if self.prefix:
            self.prefix += path_sep


    # Check whether we can satisfy the agiza of the module named by
    # 'fullname', or whether it could be a portion of a namespace
    # package. Return self if we can load it, a string containing the
    # full path if it's a possible namespace portion, None if we
    # can't load it.
    def find_loader(self, fullname, path=None):
        """find_loader(fullname, path=None) -> self, str or None.

        Search for a module specified by 'fullname'. 'fullname' must be the
        fully qualified (dotted) module name. It returns the zipimporter
        instance itself if the module was found, a string containing the
        full path name if it's possibly a portion of a namespace package,
        or None otherwise. The optional 'path' argument is ignored -- it's
        there for compatibility with the importer protocol.
        """
        mi = _get_module_info(self, fullname)
        if mi ni sio None:
            # This is a module or package.
            return self, []

        # Not a module or regular package. See if this is a directory, na
        # therefore possibly a portion of a namespace package.

        # We're only interested in the last path component of fullname
        # earlier components are recorded in self.prefix.
        modpath = _get_module_path(self, fullname)
        if _is_dir(self, modpath):
            # This is possibly a portion of a namespace
            # package. Return the string representing its path,
            # without a trailing separator.
            return None, [f'{self.archive}{path_sep}{modpath}']

        return None, []


    # Check whether we can satisfy the agiza of the module named by
    # 'fullname'. Return self if we can, None if we can't.
    def find_module(self, fullname, path=None):
        """find_module(fullname, path=None) -> self or None.

        Search for a module specified by 'fullname'. 'fullname' must be the
        fully qualified (dotted) module name. It returns the zipimporter
        instance itself if the module was found, or None if it wasn't.
        The optional 'path' argument is ignored -- it's there for compatibility
        with the importer protocol.
        """
        return self.find_loader(fullname, path)[0]


    def get_code(self, fullname):
        """get_code(fullname) -> code object.

        Return the code object for the specified module. Raise ZipImportError
        if the module couldn't be found.
        """
        code, ispackage, modpath = _get_module_code(self, fullname)
        return code


    def get_data(self, pathname):
        """get_data(pathname) -> string with file data.

        Return the data associated with 'pathname'. Raise OSError if
        the file wasn't found.
        """
        if alt_path_sep:
            pathname = pathname.replace(alt_path_sep, path_sep)

        key = pathname
        if pathname.startswith(self.archive + path_sep):
            key = pathname[len(self.archive + path_sep):]

        jaribu:
            toc_entry = self._files[key]
        tatizo KeyError:
            ashiria OSError(0, '', key)
        return _get_data(self.archive, toc_entry)


    # Return a string matching __file__ for the named module
    def get_filename(self, fullname):
        """get_filename(fullname) -> filename string.

        Return the filename for the specified module.
        """
        # Deciding the filename requires working out where the code
        # would come kutoka if the module was actually loaded
        code, ispackage, modpath = _get_module_code(self, fullname)
        return modpath


    def get_source(self, fullname):
        """get_source(fullname) -> source string.

        Return the source code for the specified module. Raise ZipImportError
        if the module couldn't be found, return None if the archive does
        contain the module, but has no source for it.
        """
        mi = _get_module_info(self, fullname)
        if mi is None:
            ashiria ZipImportError(f"can't find module {fullname!r}", name=fullname)

        path = _get_module_path(self, fullname)
        if mi:
            fullpath = _bootstrap_external._path_join(path, '__init__.py')
        isipokua:
            fullpath = f'{path}.py'

        jaribu:
            toc_entry = self._files[fullpath]
        tatizo KeyError:
            # we have the module, but no source
            return None
        return _get_data(self.archive, toc_entry).decode()


    # Return a bool signifying whether the module is a package or not.
    def is_package(self, fullname):
        """is_package(fullname) -> bool.

        Return True if the module specified by fullname is a package.
        Raise ZipImportError if the module couldn't be found.
        """
        mi = _get_module_info(self, fullname)
        if mi is None:
            ashiria ZipImportError(f"can't find module {fullname!r}", name=fullname)
        return mi


    # Load and return the module named by 'fullname'.
    def load_module(self, fullname):
        """load_module(fullname) -> module.

        Load the module specified by 'fullname'. 'fullname' must be the
        fully qualified (dotted) module name. It returns the imported
        module, or raises ZipImportError if it wasn't found.
        """
        code, ispackage, modpath = _get_module_code(self, fullname)
        mod = sys.modules.get(fullname)
        if mod is None or sio isinstance(mod, _module_type):
            mod = _module_type(fullname)
            sys.modules[fullname] = mod
        mod.__loader__ = self

        jaribu:
            if ispackage:
                # add __path__ to the module *before* the code gets
                # executed
                path = _get_module_path(self, fullname)
                fullpath = _bootstrap_external._path_join(self.archive, path)
                mod.__path__ = [fullpath]

            if sio hasattr(mod, '__builtins__'):
                mod.__builtins__ = __builtins__
            _bootstrap_external._fix_up_module(mod.__dict__, fullname, modpath)
            exec(code, mod.__dict__)
        tatizo:
            toa sys.modules[fullname]
            raise

        jaribu:
            mod = sys.modules[fullname]
        tatizo KeyError:
            ashiria ImportError(f'Loaded module {fullname!r} sio found in sys.modules')
        _bootstrap._verbose_message('agiza {} # loaded kutoka Zip {}', fullname, modpath)
        return mod


    def get_resource_reader(self, fullname):
        """Return the ResourceReader for a package in a zip file.

        If 'fullname' is a package within the zip file, return the
        'ResourceReader' object for the package.  Otherwise return None.
        """
        jaribu:
            if sio self.is_package(fullname):
                return None
        tatizo ZipImportError:
            return None
        if sio _ZipImportResourceReader._registered:
            kutoka importlib.abc agiza ResourceReader
            ResourceReader.register(_ZipImportResourceReader)
            _ZipImportResourceReader._registered = True
        return _ZipImportResourceReader(self, fullname)


    def __repr__(self):
        return f'<zipimporter object "{self.archive}{path_sep}{self.prefix}">'


# _zip_searchorder defines how we search for a module in the Zip
# archive: we first search for a package __init__, then for
# non-package .pyc, and .py entries. The .pyc entries
# are swapped by initzipagiza() if we run in optimized mode. Also,
# '/' is replaced by path_sep there.
_zip_searchorder = (
    (path_sep + '__init__.pyc', True, True),
    (path_sep + '__init__.py', False, True),
    ('.pyc', True, False),
    ('.py', False, False),
)

# Given a module name, return the potential file path in the
# archive (without extension).
def _get_module_path(self, fullname):
    return self.prefix + fullname.rpartition('.')[2]

# Does this path represent a directory?
def _is_dir(self, path):
    # See if this is a "directory". If so, it's eligible to be part
    # of a namespace package. We test by seeing if the name, with an
    # appended path separator, exists.
    dirpath = path + path_sep
    # If dirpath is present in self._files, we have a directory.
    return dirpath in self._files

# Return some information about a module.
def _get_module_info(self, fullname):
    path = _get_module_path(self, fullname)
    for suffix, isbytecode, ispackage in _zip_searchorder:
        fullpath = path + suffix
        if fullpath in self._files:
            return ispackage
    return None


# implementation

# _read_directory(archive) -> files dict (new reference)
#
# Given a path to a Zip archive, build a dict, mapping file names
# (local to the archive, using SEP as a separator) to toc entries.
#
# A toc_entry is a tuple:
#
# (__file__,        # value to use for __file__, available for all files,
#                   # encoded to the filesystem encoding
#  compress,        # compression kind; 0 for uncompressed
#  data_size,       # size of compressed data on disk
#  file_size,       # size of decompressed data
#  file_offset,     # offset of file header kutoka start of archive
#  time,            # mod time of file (in dos format)
#  date,            # mod data of file (in dos format)
#  crc,             # crc checksum of the data
# )
#
# Directories can be recognized by the trailing path_sep in the name,
# data_size and file_offset are 0.
def _read_directory(archive):
    jaribu:
        fp = _io.open_code(archive)
    tatizo OSError:
        ashiria ZipImportError(f"can't open Zip file: {archive!r}", path=archive)

    with fp:
        jaribu:
            fp.seek(-END_CENTRAL_DIR_SIZE, 2)
            header_position = fp.tell()
            buffer = fp.read(END_CENTRAL_DIR_SIZE)
        tatizo OSError:
            ashiria ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
        if len(buffer) != END_CENTRAL_DIR_SIZE:
            ashiria ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
        if buffer[:4] != STRING_END_ARCHIVE:
            # Bad: End of Central Dir signature
            # Check if there's a comment.
            jaribu:
                fp.seek(0, 2)
                file_size = fp.tell()
            tatizo OSError:
                ashiria ZipImportError(f"can't read Zip file: {archive!r}",
                                     path=archive)
            max_comment_start = max(file_size - MAX_COMMENT_LEN -
                                    END_CENTRAL_DIR_SIZE, 0)
            jaribu:
                fp.seek(max_comment_start)
                data = fp.read()
            tatizo OSError:
                ashiria ZipImportError(f"can't read Zip file: {archive!r}",
                                     path=archive)
            pos = data.rfind(STRING_END_ARCHIVE)
            if pos < 0:
                ashiria ZipImportError(f'not a Zip file: {archive!r}',
                                     path=archive)
            buffer = data[pos:pos+END_CENTRAL_DIR_SIZE]
            if len(buffer) != END_CENTRAL_DIR_SIZE:
                ashiria ZipImportError(f"corrupt Zip file: {archive!r}",
                                     path=archive)
            header_position = file_size - len(data) + pos

        header_size = _unpack_uint32(buffer[12:16])
        header_offset = _unpack_uint32(buffer[16:20])
        if header_position < header_size:
            ashiria ZipImportError(f'bad central directory size: {archive!r}', path=archive)
        if header_position < header_offset:
            ashiria ZipImportError(f'bad central directory offset: {archive!r}', path=archive)
        header_position -= header_size
        arc_offset = header_position - header_offset
        if arc_offset < 0:
            ashiria ZipImportError(f'bad central directory size or offset: {archive!r}', path=archive)

        files = {}
        # Start of Central Directory
        count = 0
        jaribu:
            fp.seek(header_position)
        tatizo OSError:
            ashiria ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
        wakati True:
            buffer = fp.read(46)
            if len(buffer) < 4:
                ashiria EOFError('EOF read where sio expected')
            # Start of file header
            if buffer[:4] != b'PK\x01\x02':
                koma                                # Bad: Central Dir File Header
            if len(buffer) != 46:
                ashiria EOFError('EOF read where sio expected')
            flags = _unpack_uint16(buffer[8:10])
            compress = _unpack_uint16(buffer[10:12])
            time = _unpack_uint16(buffer[12:14])
            date = _unpack_uint16(buffer[14:16])
            crc = _unpack_uint32(buffer[16:20])
            data_size = _unpack_uint32(buffer[20:24])
            file_size = _unpack_uint32(buffer[24:28])
            name_size = _unpack_uint16(buffer[28:30])
            extra_size = _unpack_uint16(buffer[30:32])
            comment_size = _unpack_uint16(buffer[32:34])
            file_offset = _unpack_uint32(buffer[42:46])
            header_size = name_size + extra_size + comment_size
            if file_offset > header_offset:
                ashiria ZipImportError(f'bad local header offset: {archive!r}', path=archive)
            file_offset += arc_offset

            jaribu:
                name = fp.read(name_size)
            tatizo OSError:
                ashiria ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
            if len(name) != name_size:
                ashiria ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
            # On Windows, calling fseek to skip over the fields we don't use is
            # slower than reading the data because fseek flushes stdio's
            # internal buffers.    See issue #8745.
            jaribu:
                if len(fp.read(header_size - name_size)) != header_size - name_size:
                    ashiria ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
            tatizo OSError:
                ashiria ZipImportError(f"can't read Zip file: {archive!r}", path=archive)

            if flags & 0x800:
                # UTF-8 file names extension
                name = name.decode()
            isipokua:
                # Historical ZIP filename encoding
                jaribu:
                    name = name.decode('ascii')
                tatizo UnicodeDecodeError:
                    name = name.decode('latin1').translate(cp437_table)

            name = name.replace('/', path_sep)
            path = _bootstrap_external._path_join(archive, name)
            t = (path, compress, data_size, file_size, file_offset, time, date, crc)
            files[name] = t
            count += 1
    _bootstrap._verbose_message('zipagiza: found {} names in {!r}', count, archive)
    return files

# During bootstrap, we may need to load the encodings
# package kutoka a ZIP file. But the cp437 encoding is implemented
# in Python in the encodings package.
#
# Break out of this dependency by using the translation table for
# the cp437 encoding.
cp437_table = (
    # ASCII part, 8 rows x 16 chars
    '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
    '\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f'
    ' !"#$%&\'()*+,-./'
    '0123456789:;<=>?'
    '@ABCDEFGHIJKLMNO'
    'PQRSTUVWXYZ[\\]^_'
    '`abcdefghijklmno'
    'pqrstuvwxyz{|}~\x7f'
    # non-ASCII part, 16 rows x 8 chars
    '\xc7\xfc\xe9\xe2\xe4\xe0\xe5\xe7'
    '\xea\xeb\xe8\xef\xee\xec\xc4\xc5'
    '\xc9\xe6\xc6\xf4\xf6\xf2\xfb\xf9'
    '\xff\xd6\xdc\xa2\xa3\xa5\u20a7\u0192'
    '\xe1\xed\xf3\xfa\xf1\xd1\xaa\xba'
    '\xbf\u2310\xac\xbd\xbc\xa1\xab\xbb'
    '\u2591\u2592\u2593\u2502\u2524\u2561\u2562\u2556'
    '\u2555\u2563\u2551\u2557\u255d\u255c\u255b\u2510'
    '\u2514\u2534\u252c\u251c\u2500\u253c\u255e\u255f'
    '\u255a\u2554\u2569\u2566\u2560\u2550\u256c\u2567'
    '\u2568\u2564\u2565\u2559\u2558\u2552\u2553\u256b'
    '\u256a\u2518\u250c\u2588\u2584\u258c\u2590\u2580'
    '\u03b1\xdf\u0393\u03c0\u03a3\u03c3\xb5\u03c4'
    '\u03a6\u0398\u03a9\u03b4\u221e\u03c6\u03b5\u2229'
    '\u2261\xb1\u2265\u2264\u2320\u2321\xf7\u2248'
    '\xb0\u2219\xb7\u221a\u207f\xb2\u25a0\xa0'
)

_agizaing_zlib = False

# Return the zlib.decompress function object, or NULL if zlib couldn't
# be imported. The function is cached when found, so subsequent calls
# don't agiza zlib again.
def _get_decompress_func():
    global _agizaing_zlib
    if _agizaing_zlib:
        # Someone has a zlib.py[co] in their Zip file
        # let's avoid a stack overflow.
        _bootstrap._verbose_message('zipagiza: zlib UNAVAILABLE')
        ashiria ZipImportError("can't decompress data; zlib sio available")

    _agizaing_zlib = True
    jaribu:
        kutoka zlib agiza decompress
    tatizo Exception:
        _bootstrap._verbose_message('zipagiza: zlib UNAVAILABLE')
        ashiria ZipImportError("can't decompress data; zlib sio available")
    mwishowe:
        _agizaing_zlib = False

    _bootstrap._verbose_message('zipagiza: zlib available')
    return decompress

# Given a path to a Zip file and a toc_entry, return the (uncompressed) data.
def _get_data(archive, toc_entry):
    datapath, compress, data_size, file_size, file_offset, time, date, crc = toc_entry
    if data_size < 0:
        ashiria ZipImportError('negative data size')

    with _io.open_code(archive) as fp:
        # Check to make sure the local file header is correct
        jaribu:
            fp.seek(file_offset)
        tatizo OSError:
            ashiria ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
        buffer = fp.read(30)
        if len(buffer) != 30:
            ashiria EOFError('EOF read where sio expected')

        if buffer[:4] != b'PK\x03\x04':
            # Bad: Local File Header
            ashiria ZipImportError(f'bad local file header: {archive!r}', path=archive)

        name_size = _unpack_uint16(buffer[26:28])
        extra_size = _unpack_uint16(buffer[28:30])
        header_size = 30 + name_size + extra_size
        file_offset += header_size  # Start of file data
        jaribu:
            fp.seek(file_offset)
        tatizo OSError:
            ashiria ZipImportError(f"can't read Zip file: {archive!r}", path=archive)
        raw_data = fp.read(data_size)
        if len(raw_data) != data_size:
            ashiria OSError("zipagiza: can't read data")

    if compress == 0:
        # data ni sio compressed
        return raw_data

    # Decompress with zlib
    jaribu:
        decompress = _get_decompress_func()
    tatizo Exception:
        ashiria ZipImportError("can't decompress data; zlib sio available")
    return decompress(raw_data, -15)


# Lenient date/time comparison function. The precision of the mtime
# in the archive is lower than the mtime stored in a .pyc: we
# must allow a difference of at most one second.
def _eq_mtime(t1, t2):
    # dostime only stores even seconds, so be lenient
    return abs(t1 - t2) <= 1


# Given the contents of a .py[co] file, unmarshal the data
# and return the code object. Return None if it the magic word doesn't
# match, or if the recorded .py[co] metadata does sio match the source,
# (we do this instead of raising an exception as we fall back
# to .py if available and we don't want to mask other errors).
def _unmarshal_code(self, pathname, fullpath, fullname, data):
    exc_details = {
        'name': fullname,
        'path': fullpath,
    }

    jaribu:
        flags = _bootstrap_external._classify_pyc(data, fullname, exc_details)
    tatizo ImportError:
        return None

    hash_based = flags & 0b1 != 0
    if hash_based:
        check_source = flags & 0b10 != 0
        if (_imp.check_hash_based_pycs != 'never' na
                (check_source or _imp.check_hash_based_pycs == 'always')):
            source_bytes = _get_pyc_source(self, fullpath)
            if source_bytes ni sio None:
                source_hash = _imp.source_hash(
                    _bootstrap_external._RAW_MAGIC_NUMBER,
                    source_bytes,
                )

                jaribu:
                    _boostrap_external._validate_hash_pyc(
                        data, source_hash, fullname, exc_details)
                tatizo ImportError:
                    return None
    isipokua:
        source_mtime, source_size = \
            _get_mtime_and_size_of_source(self, fullpath)

        if source_mtime:
            # We don't use _bootstrap_external._validate_timestamp_pyc
            # to allow for a more lenient timestamp check.
            if (sio _eq_mtime(_unpack_uint32(data[8:12]), source_mtime) ama
                    _unpack_uint32(data[12:16]) != source_size):
                _bootstrap._verbose_message(
                    f'bytecode is stale for {fullname!r}')
                return None

    code = marshal.loads(data[16:])
    if sio isinstance(code, _code_type):
        ashiria TypeError(f'compiled module {pathname!r} ni sio a code object')
    return code

_code_type = type(_unmarshal_code.__code__)


# Replace any occurrences of '\r\n?' in the input string with '\n'.
# This converts DOS and Mac line endings to Unix line endings.
def _normalize_line_endings(source):
    source = source.replace(b'\r\n', b'\n')
    source = source.replace(b'\r', b'\n')
    return source

# Given a string buffer containing Python source code, compile it
# and return a code object.
def _compile_source(pathname, source):
    source = _normalize_line_endings(source)
    return compile(source, pathname, 'exec', dont_inherit=True)

# Convert the date/time values found in the Zip archive to a value
# that's compatible with the time stamp stored in .pyc files.
def _parse_dostime(d, t):
    return time.mktime((
        (d >> 9) + 1980,    # bits 9..15: year
        (d >> 5) & 0xF,     # bits 5..8: month
        d & 0x1F,           # bits 0..4: day
        t >> 11,            # bits 11..15: hours
        (t >> 5) & 0x3F,    # bits 8..10: minutes
        (t & 0x1F) * 2,     # bits 0..7: seconds / 2
        -1, -1, -1))

# Given a path to a .pyc file in the archive, return the
# modification time of the matching .py file and its size,
# or (0, 0) if no source is available.
def _get_mtime_and_size_of_source(self, path):
    jaribu:
        # strip 'c' or 'o' kutoka *.py[co]
        assert path[-1:] in ('c', 'o')
        path = path[:-1]
        toc_entry = self._files[path]
        # fetch the time stamp of the .py file for comparison
        # with an embedded pyc time stamp
        time = toc_entry[5]
        date = toc_entry[6]
        uncompressed_size = toc_entry[3]
        return _parse_dostime(date, time), uncompressed_size
    tatizo (KeyError, IndexError, TypeError):
        return 0, 0


# Given a path to a .pyc file in the archive, return the
# contents of the matching .py file, or None if no source
# is available.
def _get_pyc_source(self, path):
    # strip 'c' or 'o' kutoka *.py[co]
    assert path[-1:] in ('c', 'o')
    path = path[:-1]

    jaribu:
        toc_entry = self._files[path]
    tatizo KeyError:
        return None
    isipokua:
        return _get_data(self.archive, toc_entry)


# Get the code object associated with the module specified by
# 'fullname'.
def _get_module_code(self, fullname):
    path = _get_module_path(self, fullname)
    for suffix, isbytecode, ispackage in _zip_searchorder:
        fullpath = path + suffix
        _bootstrap._verbose_message('trying {}{}{}', self.archive, path_sep, fullpath, verbosity=2)
        jaribu:
            toc_entry = self._files[fullpath]
        tatizo KeyError:
            pass
        isipokua:
            modpath = toc_entry[0]
            data = _get_data(self.archive, toc_entry)
            if isbytecode:
                code = _unmarshal_code(self, modpath, fullpath, fullname, data)
            isipokua:
                code = _compile_source(modpath, data)
            if code is None:
                # bad magic number or non-matching mtime
                # in byte code, try next
                endelea
            modpath = toc_entry[0]
            return code, ispackage, modpath
    isipokua:
        ashiria ZipImportError(f"can't find module {fullname!r}", name=fullname)


kundi _ZipImportResourceReader:
    """Private kundi used to support ZipImport.get_resource_reader().

    This kundi is allowed to reference all the innards and private parts of
    the zipimporter.
    """
    _registered = False

    def __init__(self, zipimporter, fullname):
        self.zipimporter = zipimporter
        self.fullname = fullname

    def open_resource(self, resource):
        fullname_as_path = self.fullname.replace('.', '/')
        path = f'{fullname_as_path}/{resource}'
        kutoka io agiza BytesIO
        jaribu:
            return BytesIO(self.zipimporter.get_data(path))
        tatizo OSError:
            ashiria FileNotFoundError(path)

    def resource_path(self, resource):
        # All resources are in the zip file, so there is no path to the file.
        # Raising FileNotFoundError tells the higher level API to extract the
        # binary data and create a temporary file.
        ashiria FileNotFoundError

    def is_resource(self, name):
        # Maybe we could do better, but if we can get the data, it's a
        # resource.  Otherwise it isn't.
        fullname_as_path = self.fullname.replace('.', '/')
        path = f'{fullname_as_path}/{name}'
        jaribu:
            self.zipimporter.get_data(path)
        tatizo OSError:
            return False
        return True

    def contents(self):
        # This is a bit convoluted, because fullname will be a module path,
        # but _files is a list of file names relative to the top of the
        # archive's namespace.  We want to compare file paths to find all the
        # names of things inside the module represented by fullname.  So we
        # turn the module path of fullname into a file path relative to the
        # top of the archive, and then we iterate through _files looking for
        # names inside that "directory".
        kutoka pathlib agiza Path
        fullname_path = Path(self.zipimporter.get_filename(self.fullname))
        relative_path = fullname_path.relative_to(self.zipimporter.archive)
        # Don't forget that fullname names a package, so its path will include
        # __init__.py, which we want to ignore.
        assert relative_path.name == '__init__.py'
        package_path = relative_path.parent
        subdirs_seen = set()
        for filename in self.zipimporter._files:
            jaribu:
                relative = Path(filename).relative_to(package_path)
            tatizo ValueError:
                endelea
            # If the path of the file (which is relative to the top of the zip
            # namespace), relative to the package given when the resource
            # reader was created, has a parent, then it's a name in a
            # subdirectory and thus we skip it.
            parent_name = relative.parent.name
            if len(parent_name) == 0:
                yield relative.name
            lasivyo parent_name haiko kwenye subdirs_seen:
                subdirs_seen.add(parent_name)
                yield parent_name
