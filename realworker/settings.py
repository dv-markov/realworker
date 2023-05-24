from pathlib import Path
import os

# load local settings if available

try:
    from .local_settings import *
except ImportError:
    from .server_settings import *
