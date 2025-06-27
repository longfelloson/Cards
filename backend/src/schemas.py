from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator

from exceptions import MissingUpdateData


class BaseFilter(BaseModel):
    offset: int = Field(default=0, ge=0, description="Offset for pagination")
    limit: int = Field(default=25, ge=1, le=100, description="Limit for pagination")
    query: Optional[str] = Field(
        default=None, description="Query for searching objects by name"
    )

    def get_conditions(self, model) -> list:
        conditions = []

        for field_name, value in self.model_dump(exclude_none=True).items():
            if field_name in {"offset", "limit"}:
                continue

            if hasattr(model, field_name):
                column = getattr(model, field_name)
                conditions.append(column == value)

        return conditions

    @field_validator("query", mode="before")
    @classmethod
    def make_lowercase(cls, value: Optional[str]) -> Optional[str]:
        return value.lower() if value else value


class BaseUpdate(BaseModel):
    __object_name: str = "object"

    @model_validator(mode="after")
    def check_at_least_one_field_provided(self):
        if not any(value is not None for value in self.__dict__.values()):
            raise MissingUpdateData(object_name=self.__object_name)
        return self
