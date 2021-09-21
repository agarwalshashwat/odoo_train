{
    "name":"School Database",
    "version":"1.0",
    "depends":["base","mail"],
    "data":[
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/school_view.xml",
        "views/student_report.xml",
        "wizard/wizard_view.xml"
    ],
    "sequence":10,
    "installable":True,
    "application":True,
}