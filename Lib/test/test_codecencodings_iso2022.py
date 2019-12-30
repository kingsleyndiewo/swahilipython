# Codec encoding tests kila ISO 2022 encodings.

kutoka test agiza multibytecodec_support
agiza unittest

COMMON_CODEC_TESTS = (
        # invalid bytes
        (b'ab\xFFcd', 'replace', 'ab\uFFFDcd'),
        (b'ab\x1Bdef', 'replace', 'ab\x1Bdef'),
        (b'ab\x1B$def', 'replace', 'ab\uFFFD'),
    )

kundi Test_ISO2022_JP(multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'iso2022_jp'
    tstring = multibytecodec_support.load_teststring('iso2022_jp')
    codectests = COMMON_CODEC_TESTS + (
        (b'ab\x1BNdef', 'replace', 'ab\x1BNdef'),
    )

kundi Test_ISO2022_JP2(multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'iso2022_jp_2'
    tstring = multibytecodec_support.load_teststring('iso2022_jp')
    codectests = COMMON_CODEC_TESTS + (
        (b'ab\x1BNdef', 'replace', 'abdef'),
    )

kundi Test_ISO2022_KR(multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'iso2022_kr'
    tstring = multibytecodec_support.load_teststring('iso2022_kr')
    codectests = COMMON_CODEC_TESTS + (
        (b'ab\x1BNdef', 'replace', 'ab\x1BNdef'),
    )

    # iso2022_kr.txt cannot be used to test "chunk coding": the escape
    # sequence ni only written on the first line
    @unittest.skip('iso2022_kr.txt cannot be used to test "chunk coding"')
    eleza test_chunkcoding(self):
        pita

ikiwa __name__ == "__main__":
    unittest.main()
