from src.masonite.foundation import Application
from src.masonite.foundation import Kernel
from src.masonite.foundation.TestsKernel import TestsKernel
from src.masonite.utils.location import base_path
from tests.integrations.config.providers import PROVIDERS
from tests.integrations.app.Kernel import Kernel as ApplicationKernel


# here the project base path is tests/integrations
application = Application(base_path("tests/integrations"))

"""First Bind important providers needed to start the server
"""

application.register_providers(
    Kernel,
    TestsKernel,
    ApplicationKernel,
)

application.add_providers(*PROVIDERS)
