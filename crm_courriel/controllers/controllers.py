# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class CrmCourriel(http.Controller):
    @http.route('/service_courrier/courrier_entrant', website=True, auth='public')
    def index(self, **kw):
         #return "Hello, world"
         list_courrier = request.env['service.courriel'].sudo().search([])
         return request.render('crm_courriel.list_courrier', {
            'root': '/service_courrier/courrier_entrant',
            'Liste_du_courrier':list_courrier
         })
    
    """ def list(self, **kwargs):
        response = super().list(**kwargs)
        if kwargs.get("Sortant"):
            all_courrier = response.qcontext["list_courrier"]
            status_courrier = all_courrier.filtered(
              "is_io")
            response.qcontext["list_courrier"] = status_courrier
        return response """

    def list_courrier_entrant(self, **kwargs):
        """
        Méthode pour afficher la liste des courriers entrants
        """
        all_courrier = request.env['service.courriel'].sudo().search([])
        status_courrier = all_courrier.filtered("is_io")

        if request.params.get("Sortant"):
            status_courrier = all_courrier.filtered("is_io")

        return request.render('crm_courriel.list_courrier', {
            'Liste_du_courrier': status_courrier
        })
  
    @http.route('/service_courrier/courrier_list', website=True, auth='public')
    def list_courrier(self, **kwargs):
        """
        Méthode pour afficher la liste des courriers
        """
        all_courrier = request.env['service.courriel'].sudo().search([])

        if kwargs.get("Sortant"):
            status_courrier = all_courrier.filtered("is_io")
        else:
            status_courrier = all_courrier.filtered(lambda c: not c.is_io)

        return request.render('crm_courriel.list_courrier', {
            'Liste_du_courrier': status_courrier
        })
   


#     @http.route('/crm_courriel/crm_courriel/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('crm_courriel.listing', {
#             'root': '/crm_courriel/crm_courriel',
#             'objects': http.request.env['crm_courriel.crm_courriel'].search([]),
#         })

#     @http.route('/crm_courriel/crm_courriel/objects/<model("crm_courriel.crm_courriel"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('crm_courriel.object', {
#             'object': obj
#         })
