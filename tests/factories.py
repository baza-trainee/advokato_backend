import random

import factory

from calendarapi.models import User, City, Lawyer, Specialization


class UserFactory(factory.Factory):
    username: str = factory.Sequence(lambda n: "user%d" % n)
    email: str = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password: str = "mypwd"

    class Meta:
        model = User


class CityFactory(factory.Factory):
    city_name: str = factory.Sequence(lambda n: f"Test City {n}")

    class Meta:
        model = City


class LawyerFactory(factory.Factory):
    name: str = "John"
    surname: str = "Doe"
    lawyer_mail: str = factory.Sequence(lambda n: f"john{n}@example.com")
    city_id: int = 1

    class Meta:
        model = Lawyer


class SpecializationFactory(factory.Factory):
    specialization_name: str = factory.LazyAttribute(
        lambda _: random.choice(
            [
                "Цивільна",
                "Адміністративна",
                "Кримінальна",
                "Сімейна",
                "Військовий",
                "Зруйноване майно",
                "Порушення прав людини",
            ]
        )
    )

    class Meta:
        model = Specialization
