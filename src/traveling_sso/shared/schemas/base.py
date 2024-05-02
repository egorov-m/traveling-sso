from datetime import datetime

from pydantic import BaseModel, SecretStr


class SsoBaseModel(BaseModel):
    class Config:
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        str_strip_whitespace = True
        exclude_unset = True

        json_encoders = {
            # custom output conversion for datetime
            # %H:%M %b %d, %Y %Z%z
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S %Z%z") if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }
