from calendarapi.models import Visitor


def test_visitor_repr():
    # Create a new Visitor object
    visitor = Visitor(
        name="John",
        surname="Doe",
        email="john.doe@example.com",
        phone_number="1234567890",
        is_beneficiary=True,
    )

    expected_repr = "John Doe"
    assert repr(visitor), expected_repr
