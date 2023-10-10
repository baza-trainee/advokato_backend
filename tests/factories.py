import factory
from calendarapi.models import User


class UserFactory(factory.Factory):
    username: str = factory.Sequence(lambda n: "user%d" % n)
    email: str = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password: str = "mypwd"

    class Meta:
        model = User
