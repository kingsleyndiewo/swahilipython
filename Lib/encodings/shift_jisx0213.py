#
# shift_jisx0213.py: Python Unicode Codec kila SHIFT_JISX0213
#
# Written by Hye-Shik Chang <perky@FreeBSD.org>
#

agiza _codecs_jp, codecs
agiza _multibytecodec kama mbc

codec = _codecs_jp.getcodec('shift_jisx0213')

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
        name='shift_jisx0213',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )
