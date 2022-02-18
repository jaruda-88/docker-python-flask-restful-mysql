# api 모델


from flask_restx import fields, Namespace


class ManagementDto:
    api = Namespace("management", description="sample api")


    SampleResponse = api.model(
        "SampleResponse",
        {
            "sample" : fields.String(description="sample")
        }
    )