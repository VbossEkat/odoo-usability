# -*- encoding: utf-8 -*-
##############################################################################
#
#    Purchase Usability Extension module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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

from openerp import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    _order = 'order_id, sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(track_visibility='onchange')
    location_id = fields.Many2one(track_visibility='onchange')
    picking_type_id = fields.Many2one(track_visibility='onchange')
    dest_address_id = fields.Many2one(track_visibility='onchange')
    pricelist_id = fields.Many2one(track_visibility='onchange')
    date_approve = fields.Date(track_visibility='onchange')
    validator = fields.Many2one(track_visibility='onchange')
    invoice_method = fields.Selection(track_visibility='onchange')
    payment_term_id = fields.Many2one(track_visibility='onchange')
    fiscal_position = fields.Many2one(track_visibility='onchange')
    incoterm_id = fields.Many2one(track_visibility='onchange')
    partner_ref = fields.Char(track_visibility='onchange')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.one
    def _purchase_stats(self):
        poo = self.env['purchase.order']
        aio = self.env['account.invoice']
        try:
            self.purchase_order_count = poo.search_count(
                [('partner_id', 'child_of', self.id)])
        except:
            pass
        try:
            self.supplier_invoice_count = aio.search_count([
                ('partner_id', 'child_of', self.id),
                ('type', '=', 'in_invoice')])
        except:
            pass

    # Fix an access right issue when accessing partner form without being
    # a member of the purchase/User group
    purchase_order_count = fields.Integer(
        compute='_purchase_stats', string='# of Purchase Order')
    supplier_invoice_count = fields.Integer(
        compute='_purchase_stats', string='# Supplier Invoices')
