# This file is part of of product_oneclick_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .product_oneclick import *

def register():
    Pool.register(
        ProductOneClickView,
        module='product_oneclick_esale', type_='model')
    Pool.register(
        ProductOneClick,
        module='product_oneclick_esale', type_='wizard')
