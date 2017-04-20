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

import cStringIO
import contextlib
import datetime
import hashlib
import inspect
import logging
import math
import mimetypes
import unicodedata
import os
import re
import time
import urlparse

from PIL import Image
from sys import maxint


import logging
_logger = logging.getLogger(__name__)


# class product_template(osv.osv):
#     _inherit = "product.template"
#
#     _columns = {
#         'message_type_ids': fields.many2many('message.type', 'message_type_rel', 'child_id', 'parent_id', 'Message list'),
#     }
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
