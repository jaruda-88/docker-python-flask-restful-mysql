import imp
from .controller import api as ns
from flask_restx import fields


test = ns.model(
    "test",
    {
        "ddd" : fields.String(description="dddd")
    }
)