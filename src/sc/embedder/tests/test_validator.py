# -*- coding: utf-8 -*-
from sc.embedder.content.embedder import validate_int_or_percentage
from zope.interface import Invalid

import unittest


class ValidatorTestCase(unittest.TestCase):

    def test_validate_int_or_percentage(self):
        # Integer
        self.assertEqual(validate_int_or_percentage('420'), None)

        # Percentage
        self.assertEqual(validate_int_or_percentage('100%'), None)

        # Spaces allowed
        self.assertEqual(validate_int_or_percentage('100 %'), None)

        # Invalid values
        with self.assertRaises(Invalid):
            validate_int_or_percentage('a123')

        with self.assertRaises(Invalid):
            validate_int_or_percentage('123!')

        with self.assertRaises(Invalid):
            validate_int_or_percentage('12%3')
