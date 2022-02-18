import api
from flask_restx import fields, Namespace


class ManagementDto:
    api = Namespace("management", description="api")

    test = ns.model(
        "test",
        {
            "ddd" : fields.String(description="dddd")
        }
    )