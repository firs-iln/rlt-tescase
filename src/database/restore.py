import os

import bson

import logging

logger = logging.getLogger(__name__)


async def restore(path, conn, db_name):
    try:
        db = conn[db_name]
        for coll in os.listdir(path):
            if coll.endswith('.bson'):
                with open(os.path.join(path, coll), 'rb+') as f:
                    await db[coll.split('.')[0]].insert_many(bson.decode_all(f.read()))
        logger.info("Restored successfully")
    except Exception as e:
        logger.error(f"Error while restoring: {e}")
