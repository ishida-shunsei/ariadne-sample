from datetime import datetime
import pytz
from sqlalchemy import (
    Column,
    DateTime,
)


def gen_utc_now():
    return datetime.now(pytz.utc)


def gen_created_at_column():
    return Column(DateTime(timezone=True), nullable=False, default=gen_utc_now)


def gen_updated_at_column():
    return Column(DateTime(timezone=True), nullable=False, default=gen_utc_now, onupdate=gen_utc_now)
