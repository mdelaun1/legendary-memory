import logging
import random
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@dataclass
class DataConnection:
    username: str
    password: str
    connection: str = None

    def __post_init__(self):
        log.info(f"Connected with {self.username} {self.password}")

    def upload(self, clean_data):
        log.info("Mocking upload")
        num = random.randrange(1, 11)
        if num % 2 == 0:
            log.info(f"Upload succeeded: {clean_data}")
            return True
        else:
            raise ConnectionError