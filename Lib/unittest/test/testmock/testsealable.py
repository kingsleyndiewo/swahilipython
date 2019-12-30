agiza unittest
kutoka unittest agiza mock


kundi SampleObject:

    eleza method_sample1(self): pita

    eleza method_sample2(self): pita


kundi TestSealable(unittest.TestCase):

    eleza test_attributes_return_more_mocks_by_default(self):
        m = mock.Mock()

        self.assertIsInstance(m.test, mock.Mock)
        self.assertIsInstance(m.test(), mock.Mock)
        self.assertIsInstance(m.test().test2(), mock.Mock)

    eleza test_new_attributes_cannot_be_accessed_on_seal(self):
        m = mock.Mock()

        mock.seal(m)
        ukijumuisha self.assertRaises(AttributeError):
            m.test
        ukijumuisha self.assertRaises(AttributeError):
            m()

    eleza test_new_attributes_cannot_be_set_on_seal(self):
        m = mock.Mock()

        mock.seal(m)
        ukijumuisha self.assertRaises(AttributeError):
            m.test = 1

    eleza test_existing_attributes_can_be_set_on_seal(self):
        m = mock.Mock()
        m.test.test2 = 1

        mock.seal(m)
        m.test.test2 = 2
        self.assertEqual(m.test.test2, 2)

    eleza test_new_attributes_cannot_be_set_on_child_of_seal(self):
        m = mock.Mock()
        m.test.test2 = 1

        mock.seal(m)
        ukijumuisha self.assertRaises(AttributeError):
            m.test.test3 = 1

    eleza test_existing_attributes_allowed_after_seal(self):
        m = mock.Mock()

        m.test.return_value = 3

        mock.seal(m)
        self.assertEqual(m.test(), 3)

    eleza test_initialized_attributes_allowed_after_seal(self):
        m = mock.Mock(test_value=1)

        mock.seal(m)
        self.assertEqual(m.test_value, 1)

    eleza test_call_on_sealed_mock_fails(self):
        m = mock.Mock()

        mock.seal(m)
        ukijumuisha self.assertRaises(AttributeError):
            m()

    eleza test_call_on_defined_sealed_mock_succeeds(self):
        m = mock.Mock(return_value=5)

        mock.seal(m)
        self.assertEqual(m(), 5)

    eleza test_seals_recurse_on_added_attributes(self):
        m = mock.Mock()

        m.test1.test2().test3 = 4

        mock.seal(m)
        self.assertEqual(m.test1.test2().test3, 4)
        ukijumuisha self.assertRaises(AttributeError):
            m.test1.test2().test4
        ukijumuisha self.assertRaises(AttributeError):
            m.test1.test3

    eleza test_seals_recurse_on_magic_methods(self):
        m = mock.MagicMock()

        m.test1.test2["a"].test3 = 4
        m.test1.test3[2:5].test3 = 4

        mock.seal(m)
        self.assertEqual(m.test1.test2["a"].test3, 4)
        self.assertEqual(m.test1.test2[2:5].test3, 4)
        ukijumuisha self.assertRaises(AttributeError):
            m.test1.test2["a"].test4
        ukijumuisha self.assertRaises(AttributeError):
            m.test1.test3[2:5].test4

    eleza test_seals_dont_recurse_on_manual_attributes(self):
        m = mock.Mock(name="root_mock")

        m.test1.test2 = mock.Mock(name="not_sealed")
        m.test1.test2.test3 = 4

        mock.seal(m)
        self.assertEqual(m.test1.test2.test3, 4)
        m.test1.test2.test4  # Does sio raise
        m.test1.test2.test4 = 1  # Does sio raise

    eleza test_integration_with_spec_att_definition(self):
        """You are sio restricted when using mock ukijumuisha spec"""
        m = mock.Mock(SampleObject)

        m.attr_sample1 = 1
        m.attr_sample3 = 3

        mock.seal(m)
        self.assertEqual(m.attr_sample1, 1)
        self.assertEqual(m.attr_sample3, 3)
        ukijumuisha self.assertRaises(AttributeError):
            m.attr_sample2

    eleza test_integration_with_spec_method_definition(self):
        """You need to defin the methods, even ikiwa they are kwenye the spec"""
        m = mock.Mock(SampleObject)

        m.method_sample1.return_value = 1

        mock.seal(m)
        self.assertEqual(m.method_sample1(), 1)
        ukijumuisha self.assertRaises(AttributeError):
            m.method_sample2()

    eleza test_integration_with_spec_method_definition_respects_spec(self):
        """You cannot define methods out of the spec"""
        m = mock.Mock(SampleObject)

        ukijumuisha self.assertRaises(AttributeError):
            m.method_sample3.return_value = 3

    eleza test_sealed_exception_has_attribute_name(self):
        m = mock.Mock()

        mock.seal(m)
        ukijumuisha self.assertRaises(AttributeError) kama cm:
            m.SECRETE_name
        self.assertIn("SECRETE_name", str(cm.exception))

    eleza test_attribute_chain_is_maintained(self):
        m = mock.Mock(name="mock_name")
        m.test1.test2.test3.test4

        mock.seal(m)
        ukijumuisha self.assertRaises(AttributeError) kama cm:
            m.test1.test2.test3.test4.boom
        self.assertIn("mock_name.test1.test2.test3.test4.boom", str(cm.exception))

    eleza test_call_chain_is_maintained(self):
        m = mock.Mock()
        m.test1().test2.test3().test4

        mock.seal(m)
        ukijumuisha self.assertRaises(AttributeError) kama cm:
            m.test1().test2.test3().test4()
        self.assertIn("mock.test1().test2.test3().test4", str(cm.exception))


ikiwa __name__ == "__main__":
    unittest.main()
