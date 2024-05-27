import pytest

from specmatic.core.specmatic import Specmatic
from specmatic.utils import get_project_root

from main import app
PROJECT_ROOT = get_project_root()

app_host = "127.0.0.1"
app_port = 8210
stub_host = "127.0.0.1"
stub_port = 8290

expectation_json_file = '../specmatic.json'


class TestContract:
    pass


Specmatic() \
    .with_project_root(PROJECT_ROOT) \
    .with_specmatic_json_file_path("..\specmatic.json") \
    .with_asgi_app('main:app', app_host, app_port) \
    .test(TestContract, 'main:app') \
    .run()

if __name__ == '__main__':
    pytest.main()