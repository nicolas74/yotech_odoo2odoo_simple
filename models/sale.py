from datetime import datetime, timedelta
import time
from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
from openerp import workflow

import logging
_logger = logging.getLogger(__name__)

import oerplib


class sale_order(osv.osv):
    _inherit = "sale.order"

    def _main_odoo_instance_connect(self, cr, uid, ids, context=None):

        _logger.info("--> _main_odoo_instance_connect <--")
        o2o_simple_config_settings = self.pool.get('o2o_simple.config.settings').search(cr, uid, [])
        _logger.info("o2o_simple_config_settings =) "+ str(o2o_simple_config_settings))

        username = self.pool.get('ir.config_parameter').get_param(cr, uid, 'yo_o2o_username')
        password = self.pool.get('ir.config_parameter').get_param(cr, uid, 'yo_o2o_password')
        url = self.pool.get('ir.config_parameter').get_param(cr, uid, 'yo_o2o_url')
        port = self.pool.get('ir.config_parameter').get_param(cr, uid, 'yo_o2o_port')
        dbname = self.pool.get('ir.config_parameter').get_param(cr, uid, 'yo_o2o_dbname')
        default_dist_warehouse_id = self.pool.get('ir.config_parameter').get_param(cr, uid, 'yo_o2o_default_dist_warehouse_id')
        default_product_internal_categ_id = self.pool.get('ir.config_parameter').get_param(cr, uid, 'yo_o2o_default_product_internal_categ_id')
        default_dist_price_list_id = self.pool.get('ir.config_parameter').get_param(cr, uid, 'yo_o2o_default_dist_price_list_id')

        settings = {
            'default_dist_warehouse_id' : default_dist_warehouse_id,
            'default_product_internal_categ_id' : default_product_internal_categ_id,
            'default_dist_price_list_id' : default_dist_price_list_id
        }

        error = False

        #oerp = oerplib.OERP(url, protocol='xmlrpc', port=port)

        try :
            oerp = oerplib.OERP(url, protocol='xmlrpc', port=port)
        except:
            error = True
            _logger.error("Enable to connect Odoo main instance")
        # Check available databases
        #print(oerp.db.list())

        # Login (the object returned is a browsable record)
        if not error:
            user = oerp.login(username, password, dbname)
            #print(user.name)            # name of the user connected
            #print(user.company_id.name) # the name of its company

            # Simple 'raw' query
            user_data = oerp.execute('res.users', 'read', [user.id])
            #print(user_data)
        else:
            return False

        return {'OdooMainInstance': oerp , 'user': user , 'settings' : settings }

    def _export_partner(self, cr, uid, ids, odoo_connect, context=None):
        """ Export partner if needed """

        _logger.info("--> _export_partner <--")
        order_obj = self.pool.get('sale.order')
        res_partner_obj = self.pool.get('res.partner')
        dist_partner_obj = odoo_connect['OdooMainInstance'].get('res.partner')

        for order in order_obj.browse(cr, uid, ids):
            _logger.info("order.partner_id =) " + str(order.partner_id))
            dist_partner_info = {
                'name': order.partner_id.name,
                'email': order.partner_id.email,
                'phone': order.partner_id.phone,
                'mobile': order.partner_id.mobile,
                'fax': order.partner_id.fax,
                'street': order.partner_invoice_id.street,
                'street2': order.partner_invoice_id.street2,
                'zip': order.partner_invoice_id.zip,
                'city': order.partner_invoice_id.city
#                    'country_id': order.partner_invoice_id.country_id
            }
            if order.partner_id.dist_partner_id:
                dist_partner_id = dist_partner_obj.search([('id','=',order.partner_id.dist_partner_id)])
                _logger.info("dist_partner_id =) " + str(dist_partner_id))
                for dist_partner in dist_partner_obj.browse(dist_partner_id):
                    _logger.info("Odoo main instance partner =) " + str(dist_partner))
                #Update Dist Partner
                odoo_connect['OdooMainInstance'].write('res.partner',order.partner_id.dist_partner_id,dist_partner_info)
            else:
                _logger.info("Create distante Partner ")
                #Create Dist Partner
                new_dist_partner_id = odoo_connect['OdooMainInstance'].create('res.partner',dist_partner_info)
                _logger.info("dist_partner_info =) " + str(dist_partner_info))
                local_partner_info = {
                    'dist_partner_id' : new_dist_partner_id,                    
                }
                res_partner_obj.write(cr, uid, [order.partner_id.id], local_partner_info, context=context)

        return True

    def _export_products(self, cr, uid, ids, odoo_connect, context=None):
        """ Export products if needed """

        _logger.info("--> _export_products <--")
        order_obj = self.pool.get('sale.order')
        product_product_obj = self.pool.get('product.product')
        dist_product_obj = odoo_connect['OdooMainInstance'].get('product.product')

        default_product_internal_categ_id = odoo_connect['settings'].get('default_product_internal_categ_id')

        for order in order_obj.browse(cr, uid, ids):

            for line in order.order_line:
                dist_product_info = {
                    'name': line.product_id.name,
                    'type': line.product_id.type,
                    'categ_id': default_product_internal_categ_id
                }

                if line.product_id.dist_product_id:
                    dist_product_id = dist_product_obj.search([('id','=',line.product_id.dist_product_id)])
                    _logger.info("dist_product_id =) " + str(dist_product_id))
                    for dist_product in dist_product_obj.browse(dist_product_id):
                        _logger.info("Odoo main instance product =) " + str(dist_product))
                    # Update Dist Product
                    odoo_connect['OdooMainInstance'].write('product.product',line.product_id.dist_product_id)
                else:
                    _logger.info("Create distante Product ")
                    # Create Dist Product
                    new_dist_product_id = odoo_connect['OdooMainInstance'].create('product.product',dist_product_info)
                    _logger.info("dist_product_info =) " + str(dist_product_info))
                    local_product_info = {
                        'dist_product_id' : new_dist_product_id,
                    }
                    product_product_obj.write(cr, uid, [line.product_id.id], local_product_info, context=context)

        return True

    def _export_order(self, cr, uid, ids, odoo_connect, context=None):
        """ Export order and order_line if needed """

        _logger.info("--> _export_order <--")
        order_obj = self.pool.get('sale.order')
        order_line_obj = self.pool.get('sale.order')
        dist_order_obj = odoo_connect['OdooMainInstance'].get('sale.order')

        for order in order_obj.browse(cr, uid, ids):

            if odoo_connect['settings'].get('default_dist_warehouse_id'):
                warehouse_id = odoo_connect['settings'].get('default_dist_warehouse_id')
            else:
                warehouse_id = 2

            dist_order_info = {
                'partner_id': order.partner_id.dist_partner_id,
                'partner_invoice_id': order.partner_invoice_id.dist_partner_id,
                'partner_shipping_id': order.partner_shipping_id.dist_partner_id,
                'pricelist_id':odoo_connect['settings'].get('default_dist_price_list_id'),
                'date_order' : order.date_order,
                'warehouse_id' : warehouse_id,
                'picking_policy': 'direct',
#                'order_line' : dist_order_lines_info,
            }
            _logger.info("dist_order_info " + str(dist_order_info))

            if order.dist_order_id:
                _logger.info("Update distant order")
            else :
                _logger.info("Create distant order")

                new_dist_order_id = odoo_connect['OdooMainInstance'].create('sale.order',dist_order_info)

                for line in order.order_line:
                    _logger.info("line.discount " + str(line.discount))
                    dist_order_lines_info = {
                        'order_id': new_dist_order_id,
                        'product_id' : line.product_id.dist_product_id,
                        'product_uom_qty' : line.product_uom_qty,
                        'price_unit' : line.price_unit,
                        'discount' : line.discount,
                        'delay' : line.delay,
                        'name' : line.name,
                        'type': 'make_to_stock',
                        'product_uom' : 1,
                        'state' : 'draft'
                    }
                    _logger.info("dist_order_lines_info " + str(dist_order_lines_info))
                    _logger.info("order.id " + str(order.id))
                    odoo_connect['OdooMainInstance'].create('sale.order.line',dist_order_lines_info)                         
                
                # update local info
                local_order_info = {
                    'dist_order_id' : new_dist_order_id,
                }
                _logger.info("local_order_info " + str(local_order_info))
                _logger.info("order.id " + str(order.id))
                order_obj.write(cr, uid, [order.id], local_order_info, context=context)

        return True

    def push_main_instance(self, cr, uid, ids, context=None):
        """
            Push Order to main instance and check if objects must create if needed.
            Objects : Partner, Products...

        """


        if not context:
            context = {}
        #assert len(ids) == 1, 'This option should only be used for a single id at a time.'

        _logger.info("--> push_main_instance <--")

        # Prepare the connection to the server

        odoo_connect = self._main_odoo_instance_connect(cr,uid,ids, context)
        
        if odoo_connect:
            # Check if Partner in Order is in Master Odoo instance
            self._export_partner(cr,uid,ids, odoo_connect, context)
            # Check if Products in Order is in Master Odoo instance
            self._export_products(cr,uid,ids, odoo_connect, context)

            # Push Order to Master Odoo instance
            self._export_order(cr,uid,ids, odoo_connect, context)

        return True


