# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    """ inherit Partner model """
    is_student = fields.Boolean(default=False)
    birth_date = fields.Date(string="Date of Birth")

    @api.constrains('birth_date')
    def check_birth_date(self):
        """ check Date of Birth to be in past
            if is student selected
        """
        if self.is_student:
            present = datetime.now()
            if self.birth_date >= present.date():
                raise ValidationError(_("Date of Birth must be in the past."))
