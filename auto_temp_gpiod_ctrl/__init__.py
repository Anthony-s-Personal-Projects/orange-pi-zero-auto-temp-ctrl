# __init__.py for auto_temp_gpiod_ctrl package
from .utils import gpio_control, temps_monitor
from .main import main

# For convenient import as 'import auto_temp_ctrl as ...'
__all__ = ["gpio_control", "temps_monitor", "main"]
# Optionally, alias for easier import
import sys
sys.modules["auto_temp_ctrl"] = sys.modules[__name__]
