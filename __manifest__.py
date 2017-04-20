{
    'name' : "Yotech Odoo 2 Odoo Simple",
    'category': 'Connector',
    'description': """
        Allow you to push your order to another instance and manage invoice and stock separatly.
        Ideal when you want to manage multisite of the same company.
     """,
     'author':'Nicolas Trubert',
     'category': 'Hidden',
     'depends': ['web','sale','website_sale','stock','delivery'],
     'css': ['static/src/css/yotech.css'],
     'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/templates.xml'
     ],
     'active':True,
     'auto_install':False,
}
