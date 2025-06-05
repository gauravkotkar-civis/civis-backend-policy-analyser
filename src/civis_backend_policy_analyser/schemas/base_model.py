from pydantic import BaseModel


class BaseModelSchema(BaseModel):
    class Config:
        from_attributes = True
        validate_default = True  # This will ensure all fields are validated
        arbitrary_types_allowed = (
            True  # Allow additional properties not defined in the schema
        )
