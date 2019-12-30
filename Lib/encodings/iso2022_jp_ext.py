#
# iso2022_jp_ext.py: Python Unicode Codec kila ISO2022_JP_EXT
#
# Written by Hye-Shik Chang <perky@FreeBSD.org>
#

agiza _codecs_iso2022, codecs
agiza _multibytecodec kama mbc

codec = _codecs_iso2022.getcodec('iso2022_jp_ext')

kundi Codec(codecs.Codec):
    encode = codec.encode
    decode = codec.decode

kundi IncrementalEncoder(mbc.MultibyteIncrementalEncoder,
                         codecs.IncrementalEncoder):
    codec = codec

kundi IncrementalDecoder(mbc.MultibyteIncrementalDecoder,
                         codecs.IncrementalDecoder):
    codec = codec

kundi StreamReader(Codec, mbc.MultibyteStreamReader, codecs.StreamReader):
    codec = codec

kundi StreamWriter(Codec, mbc.MultibyteStreamWriter, codecs.StreamWriter):
    codec = codec

eleza getregentry():
    rudisha codecs.CodecInfo(
        name='iso2022_jp_ext',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )
