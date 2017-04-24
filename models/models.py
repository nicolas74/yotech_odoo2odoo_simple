# -*- coding: utf-8 -*-
##############################################################################
#
#    Yotech module
#    Copyright (C) 2014-2017 Yotech (<http://yotech.pro>).
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

from odoo import api, fields, models, tools, _
import odoo.addons.decimal_precision as dp
from odoo.tools.translate import html_translate

import logging
_logger = logging.getLogger(__name__)


class O2osimpleConfigSettings(models.TransientModel):
    _name = 'o2osimple.config.settings'
    _inherit = 'res.config.settings'

    yo_o2o_username = fields.Char(string='Username')
    yo_o2o_password = fields.Char(string='Password')
    yo_o2o_dbname = fields.Char(string='DataBase Name')
    yo_o2o_url = fields.Char(string='Url')
    yo_o2o_port = fields.Char(string='Port')
    yo_o2o_instance_type = fields.Selection([
        ('master', 'Master'),
        ('slave', 'Slave'),
    ], "Instance Type", default='slave', help="Adds an availability status on the web product page.")
    yo_o2o_default_dist_warehouse_id = fields.Char(string='Default Dist WareHouse ID')
    yo_o2o_default_product_internal_categ_id = fields.Char(string='Default Product internal Categ ID')
    yo_o2o_default_dist_price_list_id' = fields.Char(string='Default Dist Price List id ')
    yo_o2o_sale_order_prefix = fields.Char(string='Sale Order Prefix')

    @api.model
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

    @api.model
    def get_default_o2o_simple_config(self,fields):
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
        }


class ResPartner(models.Model):
    _inherit = 'res.partner'

    dist_partner_id = fields.Integer('Distant Partner ID', default=0)

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def create(self, values):
        values['dist_product_id'] = 0
        new_id = super(ProductProduct, self).create(values)
        return new_id

    dist_product_id = fields.Integer('Distant Product ID', default=0)    

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, values):
        values['dist_order_id'] = 0
        new_id = super(SaleOrder, self).create(values)
        return new_id

    dist_order_id = fields.Integer('Distant Order ID', default=0)
    dist_order_name = fields.Char(string='Distant Order Name')

