from structlog import get_logger

logger = get_logger()

class EntityNotFound(Exception):
    def __init__(self, entity_type, entity_id, *args, message="", **kwargs):
        super().__init__(*args, **kwargs)
        self.entity_type = entity_type
        self.entity_id   = entity_id

        logger.error(f"Not found", entity_type=entity_type, entity_id=entity_id, message=message)

    def __str__(self):
        return f"Not found :: {self.entity_type} {self.entity_id}"

class GenericAPIException(Exception):
    def __init__(self, *args, message="", **kwargs):
        super().__init__(*args, **kwargs)
        import ipdb; ipdb.set_trace()
        logger.error(f"500 - Internal Server", entity_type=entity_type, entity_id=entity_id, message=message)
