# -*- coding: utf-8 -*-
#############################################################################
#
#    Tamaco Technologies Pvt. Ltd.#
#    Copyright (C) TODAY Tamaco Technologies
#    Author: Tamaco
#
#############################################################################

import time
from odoo import api, models, fields, _
from odoo.exceptions import UserError

class EducationalOrientation(models.Model):
    _name = "orientation.subject"
    _description = 'Domaine d\'orientation'

    name = fields.Char(string='Nom')

class ResConfigSetting(models.Model):
    _inherit = "res.company"

    advertising_banner = fields.Binary('Bannière publicitaire', track_visibility="onchange")
    fname = fields.Char('Nom du fichier', track_visibility="onchange")
    bank_space_infos = fields.Html('Infos \"coordonnées bancaires\"')



