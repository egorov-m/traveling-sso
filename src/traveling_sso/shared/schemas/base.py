from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SsoBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        exclude_unset=True
    )
