{
    "name": "Hospital Managment System",
    "author": "Tommaso Sollo",
    "license": "LGPL-3",
    "version": "17.0.1.0",
    "depends": [
        "mail",
        "product"
    ],

    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/patient_views.xml",
        "views/patient_tag_views.xml",
        "views/patient_readonly_views.xml",
        "views/appointment_views.xml",
        "views/menu.xml",
        "data/sequence.xml",
    ],
    "installable": True,
    "application": True,
}