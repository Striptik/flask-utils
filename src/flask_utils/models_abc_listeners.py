from .models_abc import BaseModel
from sqlalchemy.event import listen
from datetime import datetime


def update_created_modified_on_create_listener(mapper, connection, target):
    target.created_at = datetime.utcnow()
    target.updated_at = datetime.utcnow()


def update_modified_on_update_listener(mapper, connection, target):
    target.updated_at = datetime.utcnow()


for cls in BaseModel._all_subclasses():
    listen(cls, 'before_insert',  update_created_modified_on_create_listener)
    listen(cls, 'before_update',  update_modified_on_update_listener)
