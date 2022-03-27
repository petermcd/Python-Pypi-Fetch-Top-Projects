"""Main runner script."""
from pypi_top_projects.controller import Controller


def run():
    """Initiate process."""
    controller = Controller()
    controller.run()


if __name__ == "__main__":
    run()
