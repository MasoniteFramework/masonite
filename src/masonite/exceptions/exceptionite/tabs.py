from exceptionite import Tab


class DumpsTab(Tab):
    id = "dumps"
    name = "Dumps"
    component = "DumpsTab"
    icon = "CodeIcon"
    advertise_content = True
    empty_msg = "Nothing dumped !"

    def build(self):
        dumps = self.handler.app.make("dumper").get_serialized_dumps()
        return {
            "dumps": dumps,
        }

    def has_content(self):
        return len(self.handler.app.make("dumper").get_dumps()) > 0
