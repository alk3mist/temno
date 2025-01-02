from wireup import create_container

from . import factories

container = create_container(service_modules=[factories])
