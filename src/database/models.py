from beanie import Document

from config import db_config
from core.schemas import SalaryRecord


class Record(Document, SalaryRecord):
    class Settings:
        name = db_config.COLLECTION_NAME
