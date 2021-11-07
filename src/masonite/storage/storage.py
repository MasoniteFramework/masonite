class StorageCapsule:
    def __init__(self):
        self.storage_templates = {}

    def add_storage_assets(self, templates):
        self.storage_templates.update(templates)
        return self

    def get_storage_assets(self):
        return self.storage_templates
