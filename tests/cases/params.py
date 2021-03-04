import numpy as np
import pytest

def linspace_mm(type, w, h):
    return pytest.param(
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h), 
        np.linspace(-127, 200, w*h, dtype=type).reshape(w, h), 
        id=f'{w}x{h}'
    )

