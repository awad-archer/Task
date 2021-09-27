# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class  AccountMove(models.Model):
    _inherit = "account.move"

    """ inherit Invoicing model """
    registration_id = fields.Many2one('student.registration')
