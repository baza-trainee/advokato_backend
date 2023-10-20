import random
import factory
import faker
from calendarapi.models import User, City, Lawyer, Specialization, Schedule, Visitor


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
    class Meta:
        model = Lawyer

    _id_counter = 0

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    lawyer_mail = factory.Faker("email")


class ScheduleFactory(factory.Factory):
    class Meta:
        model = Schedule

    date = factory.Faker("date_between", start_date="today", end_date="+30d")
    time = ["09:00", "10:00", "11:00", "12:00"]


class VisitorFactory(factory.Factory):
    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    email = factory.Faker("email")
    is_beneficiary = False

    class Meta:
        model = Visitor

    @factory.lazy_attribute
    def phone_number(self):
        return fake.unique.lexify(text="?" * 20)
