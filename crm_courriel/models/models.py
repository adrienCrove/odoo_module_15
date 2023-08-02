# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date
from odoo.osv import expression
from odoo.tools import float_is_zero, html_keep_url, is_html_empty

AVAILABLE_PRIORITIES = [
    ('0', 'Faible'),
    ('1', 'Normal'),
    ('2', 'Urgent'),
    ('3', 'Très urgent')
]

class ServiceCourriel(models.Model):
    _name = 'service.courriel'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']
    _description = 'Modèle enregistrant les differents courriels reçus'
    _rec_name = 'ref'

    """def _default_validity_date(self):
        if self.env['ir.config_parameter'].sudo().get_param('sale.use_quotation_validity_days'):
            days = self.env.company.quotation_validity_days
            if days > 0:
                return fields.Date.to_string(datetime.now() + timedelta(days))
        return False """

    ref = fields.Char(string="N° reference du courriel")
    ref_auto=fields.Char(string="Reference générée du courriel", compute="sequence_crl")
    object_courriel = fields.Selection([
        ('OF', 'Offre de service'),
        ('RC', 'Reponse de courrier '),
        ('INV', 'Facture'),
        ('DA', 'Dossier Administratif'),
        ('SM', 'Sommation')],
         string="objet du courrier",default='OF')
    courriel_type = fields.Selection([
        ('receipt', 'Entrant'),
        ('delivry', 'Sortant')], default='receipt') 
    date_receipt_courriel = fields.Date(string='Date de réception', default=fields.Date.context_today)
    sender_courriel = fields.Many2one('res.partner', string='Expéditeur')
    description_courriel = fields.Char(string='Description')
    cr_attachment = fields.Binary(
        string=_("PJ Courrier"), 
        track_visibility="onchange",
        help='Ajouter la fichier du courriel reçu que ce soit en image ou en fichier word,pdf')
    cr_name = fields.Char(string=_("File Name"), 
        track_visibility="onchange")
    state = fields.Selection([
        ('draft', 'Nouveau'),
        ('received', 'Assignation département'),
        ('emp_ass', 'Assignation employé'),
        ('send', 'Confirmation assignation'),], default='draft', string="status")
    state_out = fields.Selection([
        ('draft', 'Nouveau'),
        ('send', 'Courrier délivré'),
     ], default='draft', string="status")
    user_id = fields.Many2one('res.users', string='Receptionné par', index=True, track_visibility='onchange', default=lambda self: self.env.user)
    is_io= fields.Boolean(compute="_courriel_is_IO")
    priority=fields.Selection(AVAILABLE_PRIORITIES, "Priorité", default='0')
    issued_to = fields.Many2one('res.users', string='délivré à')
    date_of_issue = fields.Date(string='date de délivrance', default=fields.Date.context_today)
    signature_recipient = fields.Html(related='issued_to.signature', string="signature")
    dept_employee = fields.Many2one('hr.department')
    employee_name = fields.Many2one('hr.employee', tracking=True)
    notes= fields.Text(string='Notes')

    """ @api.onchange('dept_employee')
    def _update_employee_manager(self):
        for rec in self:
            rec.employee_name = rec.env['hr.employee'].search([
                ('department_id', '=', rec.dept_employee.id)])[0]
            #rec.employee_name = rec.filtered(lambda inv: inv.dept_employee != 'paid') """
    
    """ @api.onchange('dept_employee')
    def _update_employee_manager(self):
        if self.dept_employee:
            self.employee_name = self.env['hr.employee'].search([]).filtered(
                lambda item : item.department_id == self.dept_employee.id
            ) """

    """ for rec in self:
            rec.employee_name = rec.env['hr.employee'].search([
             ('department_id', '=', rec.dept_employee.id)])[0]
     """
    
    @api.constrains('state')
    def send_notification_state(self):
        user = self.env.user
        if self.state == 'emp_ass':           
            if user:
                #odoo_bot_id = self.env.ref('base.partner_root')
                summary = 'Départment attribué'
                notification_ids = [(0, 0, {
                    'res_partner_id': user.partner_id.id,
                    'notification_type': 'inbox'
                })]
                self.sudo().message_post(
                    subject=summary,
                    body='Le courrier a un département assigné, veuillez assigné un employé en charge',
                    message_type='notification',
                    subtype_xmlid='mail.mt_comment',
                    author_id=user.partner_id.id,
                    notification_ids=notification_ids)
                
    @api.constrains('employee_name')
    def send_notification_to_employee(self):
        if self.employee_name:
            notification_ids = [(0, 0, {
                    'res_partner_id': self.employee_name.user_id.partner_id.id,
                    'notification_type': 'inbox'
                })]
            self.sudo().message_post(
                    subject='Nouveau courrier attribué',
                    body='Le courrier vous a été assigné, veuillez confirmer la prise en charge',
                    message_type='notification',
                    subtype_xmlid='mail.mt_comment',
                    author_id=self.env.user.partner_id.id,
                    notification_ids=notification_ids)

    
    def check_courriel(self):
        if self.cr_attachment:
            self.state = 'received'
        else:
            raise ValidationError('Veuillez insérer une pièce jointe')
    
    def action_assign_department(self):
       if not self.dept_employee:
           raise ValidationError('Veuillez renseignez le department à assigner le courrier')
       else:
           self.write({'state':'emp_ass'})
           
    
    def action_retour(self):
       self.write({'state':'received'})

    
    @api.depends('courriel_type')
    def _courriel_is_IO(self):
        if self.courriel_type=='delivry':
            self.is_io=True
        else:
            self.is_io=False
    
    @api.depends('courriel_type')
    def sequence_crl(self):
        if self.courriel_type=='delivry':
            self.ref_auto =  self.env['ir.sequence'].next_by_code('sequence.courriel.code')
        else:
            self.ref_auto = ""
    
    def action_confirm_issue(self):
        user_account = self.env.user
        if self.courriel_type=='receipt':
            if self.employee_name.user_id != user_account:
                raise UserError('C\'est l\'employé sollicité qui doit confirmer l\'assignation du courrier')
            else:
                self.state='send'
        #self.write({'state':'send'})

    @api.constrains('courriel_type')
    def _courriel_is_delivry(self):
        if self.courriel_type=='delivry':
            self.ref=self.ref_auto
    
    #Controle de l'anti-date des courriers
    """ @api.onchange('date_receipt_courriel')
    def _check_date(self):
        current_date = fields.Date.today()
        for rec in self:
            if rec.date_receipt_courriel:
                datetime_obj = datetime.strptime(rec.date_receipt_courriel,'%Y-%m-%d').strftime('%Y-%m-%d')
                if datetime_obj < current_date:
                    raise ValidationError('La date de fin de validite ne doit pas etre inferieure a la date du jour') """
        
    
    
    """ @api.model
    def create(self, vals):
        try:
            if not vals['is_io']:
                vals['ref_auto'] = self.env['ir.sequence'].next_by_code('sequence.courriel.code')
            else:
                vals['ref'] = self.ref_auto
        except KeyError:
                vals['ref_auto'] = self.env['ir.sequence'].next_by_code('sequence.courriel.code')

        return super(ServiceCourriel, self).create(vals) """
    
    
    def action_courriel_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()
        template_id = self.env.ref('crm_courriel.mail_notification_courriel').id

        """ lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id) """
        ctx = {
            'default_model': 'service.courriel',
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        if self.env.context.get('mark_so_as_sent'):
            self.filtered(lambda o: o.state == 'draft').with_context(tracking_disable=True).write({'state': 'sendmail'})
        return super(ServiceCourriel, self.with_context(mail_post_autofollow=self.env.context.get('mail_post_autofollow', True))).message_post(**kwargs)

         
