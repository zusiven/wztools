import logging

import pytest


@pytest.fixture(autouse=True)
def log_to_file():
    logger = logging.getLogger()
    handler = logging.FileHandler("test_run_cmd.log", encoding="utf-8")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    yield
    logger.removeHandler(handler)
    handler.close()
