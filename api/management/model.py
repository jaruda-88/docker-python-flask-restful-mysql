from api import management_ns
from flask_restx import fields


test = management_ns.model(
    "test",
    {
        "ddd" : fields.String(description="dddd")
    }
)