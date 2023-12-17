# from sqlalchemy.orm import Mapper
# from sqlalchemy import event

# from calendarapi.extensions import cache


# def invalidate_cache(model: Mapper, cache_key: str, **kwargs):
#     @event.listens_for(model, "after_insert", **kwargs)
#     @event.listens_for(model, "after_update", **kwargs)
#     @event.listens_for(model, "after_delete", **kwargs)
#     def receive_after_change(mapper, connection, target):
#         cache.delete(cache_key)
