import random

import factory
import faker
from calendarapi.models import User, City, Lawyer, Specialization, Schedule


fake = faker.Faker()


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


class LawyersFactory(factory.Factory):
    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    lawyer_mail = factory.Faker("email")

    class Meta:
        model = Lawyer


class ScheduleFactory(factory.Factory):
    class Meta:
        model = Schedule

    lawyer_id = factory.Faker("random_int", min=1, max=100)
    date = factory.Faker("date_between", start_date="today", end_date="+30d")
