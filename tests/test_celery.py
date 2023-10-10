from calendarapi.tasks.example import dummy_task


def test_example(celery_session_app, celery_session_worker):
    """Simply test our dummy task using celery"""
    res = dummy_task.delay()
    assert res.get() == "OK"
