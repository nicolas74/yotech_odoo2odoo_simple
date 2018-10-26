# -*- coding: utf-8 -*-
##############################################################################
#
#    Yotech module
#    Copyright (C) 2014-2015 Yotech (<http://yotech.pro>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import openerp.addons.decimal_precision as dp
from openerp.tools.float_utils import float_round, float_compare

from openerp import api
from openerp.osv import fields, osv

from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)


class o2o_simple_config_settings(osv.TransientModel):
    _name = 'o2o_simple.config.settings'
    _inherit = 'res.config.settings'


    _columns = {
        'yo_o2o_username': fields.char('Username'),
        'yo_o2o_password': fields.char('Password'),
        'yo_o2o_dbname': fields.char('DataBase Name'),
        'yo_o2o_url': fields.char('Url'),
        'yo_o2o_port': fields.char('Port'),
        'yo_o2o_instance_type': fields.selection([('master', 'Master'), ('slave','Slave')], 'Instance Type'),
        'yo_o2o_default_dist_warehouse_id' :fields.char('Default Dist WareHouse ID'),
        'yo_o2o_default_product_internal_categ_id' : fields.char('Default Product internal Categ ID'),
        'yo_o2o_default_dist_price_list_id' : fields.char('Default Dist Price List ID'),
        'yo_o2o_sale_order_prefix' : fields.char('Sale Order Prefix'),
        'yo_o2o_default_dist_company_id' : fields.char('Default Dist Company ID'),
    }

    _defaults = {
        'yo_o2o_instance_type' : 'slave',
        'yo_o2o_default_dist_company_id' : '1'
    }

    @api.multi
    def set_o2o_simple_config(self):
        set_param = self.env['ir.config_parameter'].set_param
        username = self[0].yo_o2o_username or ''
        set_param('yo_o2o_username', username)
        password = self[0].yo_o2o_password or ''
        set_param('yo_o2o_password', password)
        dbname = self[0].yo_o2o_dbname or ''
        set_param('yo_o2o_dbname', dbname)
        url = self[0].yo_o2o_url or ''
        set_param('yo_o2o_url', url)
        port = self[0].yo_o2o_port or ''
        set_param('yo_o2o_port', port)
        instance_type = self[0].yo_o2o_instance_type or ''
        set_param('yo_o2o_instance_type', instance_type)
        default_dist_warehouse_id = self[0].yo_o2o_default_dist_warehouse_id or ''
        set_param('yo_o2o_default_dist_warehouse_id', default_dist_warehouse_id)
        default_product_internal_categ_id = self[0].yo_o2o_default_product_internal_categ_id or ''
        set_param('yo_o2o_default_product_internal_categ_id', default_product_internal_categ_id)
        default_dist_price_list_id = self[0].yo_o2o_default_dist_price_list_id or ''
        set_param('yo_o2o_default_dist_price_list_id', default_dist_price_list_id)
        sale_order_prefix = self[0].yo_o2o_sale_order_prefix or ''
        set_param('yo_o2o_sale_order_prefix', sale_order_prefix)
        default_dist_company_id = self[0].yo_o2o_default_dist_company_id or ''
        set_param('yo_o2o_default_dist_company_id', default_dist_company_id)

    @api.multi
    def get_default_o2o_simple_config(self):
        get_param = self.env['ir.config_parameter'].get_param
        username = get_param('yo_o2o_username', default='')
        password = get_param('yo_o2o_password', default='')
        dbname = get_param('yo_o2o_dbname', default='')
        url = get_param('yo_o2o_url', default='')
        port = get_param('yo_o2o_port', default='')
        instance_type = get_param('yo_o2o_instance_type', default='')
        default_dist_warehouse_id = get_param('yo_o2o_default_dist_warehouse_id', default='')
        default_product_internal_categ_id = get_param('yo_o2o_default_product_internal_categ_id', default='')
        default_dist_price_list_id = get_param('yo_o2o_default_dist_price_list_id', default='')
        sale_order_prefix = get_param('yo_o2o_sale_order_prefix', default='')
        default_dist_company_id = get_param('yo_o2o_default_dist_company_id', default='')

        return {
            'yo_o2o_username': username,
            'yo_o2o_password': password,
            'yo_o2o_dbname': dbname,
            'yo_o2o_url': url,
            'yo_o2o_port': port,
            'yo_o2o_instance_type' : instance_type,
            'yo_o2o_default_dist_warehouse_id' : default_dist_warehouse_id,
            'yo_o2o_default_product_internal_categ_id' : default_product_internal_categ_id,
            'yo_o2o_sale_order_prefix' : sale_order_prefix,
            'yo_o2o_default_dist_price_list_id' : default_dist_price_list_id,
            'yo_o2o_default_dist_company_id' : default_dist_company_id,
        }

class res_partner(osv.osv):
    _inherit = 'res.partner'

    _columns = {
        'dist_partner_id' : fields.integer('Distant partner ID'),
    }

class account_tax(osv.osv):
    _inherit = 'account.tax'

    _columns = {
        'dist_tax_id' : fields.integer('Distant Taxe ID'),
    }

class product_product(osv.osv):
    _inherit = "product.product"

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        ctx = dict(context or {}, mail_create_nolog=True)
        vals['dist_product_id'] = 0
        new_id = super(product_product, self).create(cr, uid, vals, context=ctx)
        return new_id

    _columns = {
        'dist_product_id' : fields.integer('Distant product ID'),
    }

class sale_order(osv.osv):
    _inherit = "sale.order"

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        ctx = dict(context or {}, mail_create_nolog=True)
        vals['dist_order_id'] = 0
        vals['dist_order_name'] = ''
        new_id = super(sale_order, self).create(cr, uid, vals, context=ctx)
        return new_id

    _columns = {
        'dist_order_id' : fields.integer('Distant Order ID'),
        'dist_order_name' : fields.char('Distant Order Name',size=10),
    }

    _defaults = {
        'dist_order_id': 0
    }
