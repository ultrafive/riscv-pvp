import numpy as np
import pytest

def linspace_mm(type, w, h):
    return pytest.param(
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h), 
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h), 
        id=f'{w}x{h}'
    )

@pytest.fixture(scope='function', autouse=True)
def workdir(request, tmpdir_factory):
    test_name = request.function.__self__.__class__.__name__ + '.' + request.function.__name__

    request.cls.workdir = tmpdir_factory.mktemp(test_name)