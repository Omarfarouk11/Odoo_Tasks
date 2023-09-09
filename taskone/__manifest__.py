{
    'name': 'purchase_request',
    'version': '1.6',
    'depends': ['base','product','mail','contacts','purchase'],
    'data': [
       'wizard/reject_view.xml',
       'views/custom_menu_view.xml',
       'views/create_order_view.xml',
       'views/mail_template_data.xml',
       'reports/purchase_request_report.xml',
       'reports/report.xml'


    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
