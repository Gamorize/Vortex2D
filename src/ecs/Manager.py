from Components import *
from collections import defaultdict
from Entity import Entity

class ECSManager:
    def __init__(self):
        self.entities = set()
        self.components = defaultdict(dict)

    def create_enitity(self):
        entity = Entity()
        self.entities.add(entity.id)
        return entity

    def add_component(self, entity: Entity, component):
        self.components[type(component)][entity.id] = component

    def get_component(self, entity: Entity, component_type):
        return self.components[component_type].get(entity.id)

    def get_entities_with_components(self, *component_types):
        sets = [set(self.components[ct].keys()) for ct in component_types]
        entity_ids = set.intersection(*sets)
        return [entity for entity in self.entities if entity in entity_ids]

