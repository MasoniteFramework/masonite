from .Command import Command


class PublishPackageCommand(Command):
    """
    Publish package files to your project

    package:publish
        {name : Name of the package}
        {--r|--resources=? : Resources to publish in you project (config, views, migrations...)}
        {--d|--dry=? : Just show a preview of what will be published into your project}
    """

    def __init__(self, application):
        super().__init__()
        self.app = application

    def handle(self):
        from ..packages import PackageProvider

        name = self.argument("name")
        selected_provider = None
        for provider in self.app.get_providers():
            if isinstance(provider, PackageProvider) and provider.package.name == name:
                selected_provider = provider
        if not selected_provider:
            self.error(f"No package has been registered under the name {name}.")
            return

        if self.option("resources"):
            resources = self.option("resources").split(",")
        else:
            resources = None
        dry = self.option("dry")
        published_resources = selected_provider.publish(resources, dry)
        if dry:
            self.info("The following files would be published:")
        else:
            self.info("The following files have been published:")
        for resource, files in published_resources.items():
            self.info("\n")
            self.info(f"{resource.capitalize()}:")
            for f in files:
                self.info(f" - {f}")
