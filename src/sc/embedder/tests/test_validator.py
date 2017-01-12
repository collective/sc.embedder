# -*- coding: utf-8 -*-
from sc.embedder.utils import validate_int_or_percentage

import unittest


class ValidatorTestCase(unittest.TestCase):

    def test_validate_int(self):
        self.assertTrue(validate_int_or_percentage('42 '))
        self.assertTrue(validate_int_or_percentage('123'))
        # invalid values
        self.assertFalse(validate_int_or_percentage('-420'))
        self.assertFalse(validate_int_or_percentage('0'))
        self.assertFalse(validate_int_or_percentage('1.23'))
        self.assertFalse(validate_int_or_percentage('123!'))
        self.assertFalse(validate_int_or_percentage('12%3'))
        self.assertFalse(validate_int_or_percentage('12 3'))
        self.assertFalse(validate_int_or_percentage('99999'))

    def test_validate_percentage(self):
        self.assertTrue(validate_int_or_percentage('99 %'))
        self.assertTrue(validate_int_or_percentage('100%'))
        # invalid values
        self.assertFalse(validate_int_or_percentage('1a%'))
        self.assertFalse(validate_int_or_percentage('-100%'))
        self.assertFalse(validate_int_or_percentage('0%'))
        self.assertFalse(validate_int_or_percentage('123%'))
        self.assertFalse(validate_int_or_percentage('999%'))
