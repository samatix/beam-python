"""
 Global Configuration that goes also through other pipelines
"""

from datetime import datetime

global_configuration = {
    'System Date': datetime.strptime("2017-01-02", "%Y-%m-%d"),
    'Currencies': ["EUR", "USD", "GBP", "AUD", "JPY", "CHF", "CAD"],
    'Base Currency': "USD"
}


# Hardcoded keys
contractual_run_keys = ['Currency', 'Product']