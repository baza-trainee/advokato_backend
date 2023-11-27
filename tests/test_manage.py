from flask_sqlalchemy import SQLAlchemy
from calendarapi.manage import init
from calendarapi.models import City, Specialization, Lawyer, Schedule


def test_init_command(
    app,
    runner,
    db: SQLAlchemy,
):
    with app.app_context():
        result = runner.invoke(init, input="y\n")

        assert result.exit_code == 0
        assert "created user admin" in result.output

        cities = City.query.all()
        assert len(cities) == 3

        specializations = Specialization.query.all()
        assert len(specializations) == 7

        lawyers = Lawyer.query.all()
        assert len(lawyers) == 25

        schedules = Schedule.query.all()
        assert len(schedules) == 25
