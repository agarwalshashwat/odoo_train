#manifest
{
    'name':'Real Estate',
    'version':'1.0',
    'depends':['base'],
    'summary':'List your property on sale',
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/estate_view.xml",
        "data/description_data.xml",
        "wizard/wizard_view.xml",
        ],
    "demo":["demo/property_demo.xml","demo/offer_demo.xml"],
    'sequence': 10,
    'installable': True,
    'application': True,
}