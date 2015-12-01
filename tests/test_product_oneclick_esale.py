# This file is part of the product_oneclick_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProductOneclickEsaleTestCase(ModuleTestCase):
    'Test Product Oneclick Esale module'
    module = 'product_oneclick_esale'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductOneclickEsaleTestCase))
    return suite