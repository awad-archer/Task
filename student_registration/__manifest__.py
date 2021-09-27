# -*- coding: utf-8 -*-

{
    'name': 'Student Registration',
    'version': '14.0.1.0.0',
    'category': 'Education',
    'summary': 'Allow users to manage student registration workflow',
    'description': "",
    'author': "Composer-Codes",
    'website': 'https://archer.solutions/',
    'depends': ['account'],
    "license": "LGPL-3",
    'data': [
        'data/student_registration_data.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/student_registration.xml',
        'views/menu.xml',
    ],
    "images": ['static/description/icon.png'],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
