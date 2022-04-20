from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    # Removes mypy error when create model instance
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    # Generate __tablename__ automatically by class name
    @declared_attr
    def __tablename__(cls) -> str:      # noqa
        return cls.__name__.lower()

    def as_dict(self, exclude=None):
        exclude = [] if exclude is None else exclude
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in exclude}


# Mixins used in Generic CRUD classes

class MixinUID:
    uid: int


class MixinUser(MixinUID):
    user: int
