from typing import List
import uuid

class Entity:
    def __init__(self):
        self.id = self._generate_id()

    def _generate_id(self):
        return uuid.uuid4()
