from structlog import get_logger

logger = get_logger()

class EntityNotFound(Exception):
    def __init__(self, entity_id, entity_type, *args, message="", **kwargs):
        super().__init__(*args, **kwargs)
        logger.error(f"Not found", entity_type=entity_type, entity_id=entity_id, message=message)
