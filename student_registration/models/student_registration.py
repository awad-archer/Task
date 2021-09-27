# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class StudentRegistration(models.Model):
    _name = 'student.registration'
    _description = "Student Registration"
    _order = 'date desc, name desc, id desc'
    """ 
        Student Registration Model 
    """
    READONLY_STATES = {'confirm': [('readonly', True)], 'cancel': [('readonly', True)], 'invoiced': [('readonly', True)]}


    name = fields.Char(string='Number', readonly=True, index=True, copy=False)
    date = fields.Date(required="true",default=fields.Date.context_today)
    student_id = fields.Many2one('res.partner', ondelete='restrict',  string='Student',
        required=True, index=True,help='Student Name', states=READONLY_STATES,domain=[('is_student', '=', True)])
    phone = fields.Char(related="student_id.phone", string='Phone', states=READONLY_STATES)
    age = fields.Char(compute="get_student_age", string='Age', store=True,
        help="Computed Student age From Birth Date")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id, readonly=True)
    amount = fields.Monetary(currency_field='currency_id', required=True)
    state = fields.Selection([
            ('draft', 'Draft'),
            ('confirm', 'Confirmed'),
            ('invoiced', 'Invoiced'),
            ('cancel', 'Canceled'),
        ], string='State', default='draft')

    @api.model
    def create(self, values):
        if values.get('name', 'New Registration') == 'New Registration':
            values['name'] = self.env['ir.sequence'].next_by_code('student.registration') or 'New Registration'
        return super(StudentRegistration, self).create(values)

    def reg_confirm(self):
        self.state = 'confirm'

    def reg_cancel(self):
        self.state = 'cancel'

    def reg_draft(self):
        self.state = 'draft'

    @api.depends('student_id', 'student_id.birth_date')
    def get_student_age(self):
        for rec in self:
            age = ''
            if rec.student_id.birth_date:
                end_data =  fields.Datetime.now()
                delta = relativedelta(end_data, rec.student_id.birth_date)
                if delta.years <= 2:
                    age = str(delta.years) + _(" Year") + str(delta.months) + _(" Month ") + str(delta.days) + _(" Days")
                else:
                    age = str(delta.years) + _(" Year")
            rec.age = age

    def create_invoice(self):
        partner = self.student_id
        data = {
            'partner_id': partner.id,
            'move_type': 'out_invoice',
            'ref': self.name,
            'invoice_origin': self.name,
            'currency_id': self.currency_id.id,
            'invoice_line_ids': [],
            'registration_id': self.id,
        }
        self.env['account.move'].create(data)
        self.state = 'invoiced'

    def action_refer_invoice(self):
        invoices = self.env['account.move'].search([('registration_id','=',self.id)])
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
        action['res_id'] = invoices.id
        context = {
            'default_move_type': 'out_invoice',
            'default_partner_id': self.student_id.id,
        }
        action['context'] = context
        return action
