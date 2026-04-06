from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from utils.case_converter import camel_case_to_snake_case


class Base(DeclarativeBase):
    abstract = True

    @declared_attr.directive
    def __tablename__(self):
        return f"{camel_case_to_snake_case(self.__name__)}"

    id: Mapped[int] = mapped_column(primary_key=True)
