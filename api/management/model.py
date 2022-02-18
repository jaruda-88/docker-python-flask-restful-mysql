from flask_restx import Namespace, fields


management_ns = Namespace("management", description="api")


test = management_ns.model(
    "test",
    {
        "ddd" : fields.String(description="dddd")
    }
)