# This file is part of product_oneclick_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Not, Bool
from trytond.modules.product_esale.tools import slugify

__all__ = ['ProductOneClickView', 'ProductOneClick']


class ProductOneClickView:
    __metaclass__ = PoolMeta
    __name__ = 'product.oneclick.view'
    esale_available = fields.Boolean('Available eSale',
        help='Product are available in e-commerce.')
    esale_active = fields.Boolean('Active')
    esale_visibility = fields.Selection([
        ('all','All'),
        ('search','Search'),
        ('catalog','Catalog'),
        ('none','None'),
        ], 'Visibility')
    esale_slug = fields.Char('Slug', 
        states={
            'required': Eval('esale_available', True),
        }, depends=['esale_available'])
    esale_shortdescription = fields.Text('Short Description',
        states={
            'required': Eval('esale_available', True),
        }, depends=['esale_available'],
        help='You could write wiki markup to create html content. Formats text following '
        'the MediaWiki (http://meta.wikimedia.org/wiki/Help:Editing) syntax.')
    esale_description = fields.Text('Sale Description',
        help='You could write wiki markup to create html content. Formats text following '
        'the MediaWiki (http://meta.wikimedia.org/wiki/Help:Editing) syntax.')
    esale_metadescription = fields.Char('Meta Description',
        states={
            'required': Eval('esale_available', True),
        }, depends=['esale_available'],
        help='Almost all search engines recommend it to be shorter ' \
        'than 155 characters of plain text')
    esale_metakeyword = fields.Char('Meta Keyword',
        states={
            'required': Eval('esale_available', True),
        }, depends=['esale_available'])
    esale_metatitle = fields.Char('Meta Title')
    esale_menus = fields.Many2Many('product.template-esale.catalog.menu',
        'template', 'menu', 'Menus')
    esale_relateds = fields.Many2Many('product.template-product.related', 
        'template', 'related', 'Relateds',
        domain=[
            ('id', '!=', Eval('id')),
            ('esale_available', '=', True),
            ('salable', '=', True),
        ], depends=['id'])
    esale_upsells = fields.Many2Many('product.template-product.upsell',
        'template', 'upsell', 'Up Sells',
        domain=[
            ('id', '!=', Eval('id')),
            ('esale_available', '=', True),
            ('salable', '=', True),
        ], depends=['id'])
    esale_crosssells = fields.Many2Many('product.template-product.crosssell',
        'template', 'crosssell', 'Cross Sells',
        domain=[
            ('id', '!=', Eval('id')),
            ('esale_available', '=', True),
            ('salable', '=', True),
        ], depends=['id'])
    esale_sequence = fields.Integer('Sequence', 
        help='Gives the sequence order when displaying category list.')

    @staticmethod
    def default_esale_active():
        return True

    @staticmethod
    def default_esale_visibility():
        return 'all'

    @fields.depends('name')
    def on_change_with_esale_slug(self):
        """Create slug from name: az09"""
        name = self.name or ''
        name = slugify(name)
        return name

    @classmethod
    def view_attributes(cls):
        return super(ProductOneClickView, cls).view_attributes() + [
            ('//page[@id="esale"]', 'states', {
                    'invisible': Not(Bool(Eval('esale_available'))),
                    })]


class ProductOneClick:
    __metaclass__ = PoolMeta
    __name__ = 'product.oneclick'

    @classmethod
    def get_template_values(self, vals):
        values = super(ProductOneClick, self).get_template_values(vals)
        if vals.esale_available:
            values['esale_available'] = vals.esale_available
            values['esale_active'] = vals.esale_active
            values['esale_visibility'] = vals.esale_visibility
            values['esale_slug'] = vals.esale_slug
            values['esale_shortdescription'] = vals.esale_shortdescription
            values['esale_description'] = vals.esale_description or None
            values['esale_metadescription'] = vals.esale_metadescription
            values['esale_metakeyword'] = vals.esale_metakeyword
            values['esale_metatitle'] = vals.esale_metatitle or None
            if vals.esale_menus:
                values['esale_menus'] = [
                    tuple(['add', [x.id for x in vals.esale_menus]])]
            if vals.esale_relateds:
                values['esale_relateds'] = [
                    tuple(['add', [x.id for x in vals.esale_relateds]])]
            if vals.esale_upsells:
                values['esale_upsells'] = [
                    tuple(['add', [x.id for x in vals.esale_upsells]])]
            if vals.esale_crosssells:
                values['esale_crosssells'] = [
                    tuple(['add', [x.id for x in vals.esale_crosssells]])]
            values['esale_sequence'] = vals.esale_sequence or 1
        return values
