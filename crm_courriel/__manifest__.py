# -*- coding: utf-8 -*-
{
    'name': "customer_courriel",

    'summary': """
        Gestion du courriel""",

    'description': """
        Système de gestion du courriel effectué par le service
        d'acceuil du courriel de la structure
    """,

    'author': "HommeNoir",
    'website': "#",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Courriel management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale', 'mail'],

    # always loaded
    'data': [
        'data/mail_template_data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
