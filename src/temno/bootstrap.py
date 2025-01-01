from wireup import create_container

from temno import factories

container = create_container(service_modules=[factories])
