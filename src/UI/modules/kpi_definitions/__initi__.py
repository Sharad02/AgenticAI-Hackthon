# modules/kpi_definitions/__init__.py
# This file makes the kpi_definitions directory a Python package.

# By importing the functions/modules here, we can make them
# easily accessible from the package level.
# This allows for cleaner imports in the dashboard, like:
# from modules.kpi_definitions import banking

from . import banking
from . import credit
from . import investments
from . import net_worth

print("KPI Definitions package loaded with individual modules.")
