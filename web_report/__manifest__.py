# -*- coding: utf-8 -*-
#############################################################################
#
#    Tamaco Technologies Pvt. Ltd.#
#    Copyright (C) TODAY Tamaco Technologies
#    Author: Tamaco
#
#############################################################################

{
    'name': 'update web report ',
    'version': '15.0.1.1.1',
    'category': 'report',
    'summary': """Personnalisaton des rapports envoyés et partagés avec les clients""",
    'author': 'Tamaco Techno Solutions, Odoo SA',
    'website': "https://www.tamaco.com",
    'company': 'Tamaco Techno Solutions',
    'maintainer': 'Tamaco Techno Solutions',
    'depends': ['base','web'],
    'data': [
        'views/res_company_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
