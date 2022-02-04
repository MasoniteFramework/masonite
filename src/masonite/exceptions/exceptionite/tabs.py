from exceptionite.tabs import Tab


class DumpsTab(Tab):
    id = "dumps"
    name = "Dumps"
    component = "DumpsTab"
    icon = "CodeIcon"
    advertise_content = True

    def build(self):
        dumps = self.handler.app.make("dumper").get_serialized_dumps()
        return {
            "dumps": dumps,
        }

    def has_content(self):
        return len(self.handler.app.make("dumper").get_dumps()) > 0


class RecommendationsTab(Tab):
    id = "recommendations"
    name = "Recommendations"
    icon = "CheckCircleIcon"
    advertise_content = True


class SolutionsTab(Tab):
    id = "solutions"
    name = "Solutions"
    icon = "SparklesIcon"
    component = "SolutionsTab"
    advertise_content = True
