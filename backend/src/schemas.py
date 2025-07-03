from typing import ClassVar, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

from exceptions import NoFieldsProvidedException


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
    object_name: ClassVar[str]
    model: ClassVar[type]

    @model_validator(mode="after")
    def check_fields(self):
        values = self.model_dump(exclude_none=True)
        cls = self.__class__

        if not hasattr(cls, "object_name") or not hasattr(cls, "model"):
            raise RuntimeError("Subclasses must define 'object_name' and 'model'")

        if not values:
            raise NoFieldsProvidedException(cls.object_name)

        column_values = self.get_column_values(cls=cls)
        if not column_values.values():
            raise NoFieldsProvidedException(cls.object_name)

        return self

    def are_new_column_values_provided(self, db_instance) -> bool:
        """Compare values from the update request with the current values in DB.

        Returns:
            bool: True if at least one field is changing.
        """
        cls = self.__class__
        provided_column_values = self.get_column_values(cls=cls, exclude_none=True)
        for column, provided_value in provided_column_values.items():
            current_value = getattr(db_instance, column, None)
            if current_value != provided_value:
                return True

        return False

    def get_column_values(self, cls, exclude_none: bool = False) -> dict:
        try:
            column_names = [col.name for col in cls.model.__table__.columns]
        except AttributeError:
            raise RuntimeError(
                f"Model {cls.model.__name__} is not a valid SQLAlchemy model"
            )

        column_values = self.model_dump(include=column_names, exclude_none=exclude_none)
        return column_values
