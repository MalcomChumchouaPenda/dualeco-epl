import os
import sys
import pytest

test_dir = os.path.dirname(__file__)
code_dir = os.path.dirname(test_dir)
if code_dir not in sys.path:
    sys.path.append(code_dir)
