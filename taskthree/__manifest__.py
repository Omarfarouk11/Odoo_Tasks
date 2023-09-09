{
    'name': 'sales_module',
    'version': '1.6',
    'depends': ['base','product', 'sale', 'stock','account'],
    'data': [
        'views/viewsinproducttemplate.xml',
        'views/viewinsaleorderline.xml',
        'views/viewinstockmove.xml',
        'views/viewaccountmove.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
