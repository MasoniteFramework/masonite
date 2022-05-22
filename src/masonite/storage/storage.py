class StorageCapsule:
    """Storage capsule class used to manage storage assets and their alias."""

    def __init__(self):
        self.storage_templates: dict = {}

    def add_storage_assets(self, templates: dict):
        self.storage_templates.update(templates)
        return self

    def get_storage_assets(self) -> dict:
        return self.storage_templates
