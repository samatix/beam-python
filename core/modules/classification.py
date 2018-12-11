"""
Classification methods used to import, modify and classify the results
"""

import apache_beam as beam
from datetime import datetime
from core.configuration import global_config


class CashFlowDic(beam.DoFn):
    """
    Changes the typologies of the fields in the imported data:
    - Changing dates into datetime format
    - Converting the numerical data from string to float

    """

    def __init__(self, global_configuration):
        super(CashFlowDic, self).__init__()
        self.global_configuration = global_configuration

    def process(self, element):
        # Product,Counterparty Category,Value date,Maturity,Start date,Cash flow type,Amount,Currency
        start_date_temp = datetime.strptime(element['Start date'], "%Y-%m-%d")
        value_date_temp = datetime.strptime(element['Value date'], "%Y-%m-%d")
        element['Maturity'] = datetime.strptime(element['Maturity'], "%Y-%m-%d")
        element['Start date'] = start_date_temp
        element['Value date'] = value_date_temp
        element['Forward Start'] = (start_date_temp > self.global_configuration['System Date'])
        element['Cash Flow Date'] = value_date_temp - self.global_configuration['System Date']
        element['Amount'] = float(element['Amount'])
        yield element


class PostTreatment(beam.DoFn):
    """Apply operations:
    1. Convert to base currency
    """

    def __init__(self, global_configuration, market_data):
        super(PostTreatment, self).__init__()
        self.base_currency = global_configuration['Base Currency']
        self.market_data = market_data

    def process(self, element):
        # Product,Counterparty Category,Value date,Maturity,Start date,Cash flow type,Amount,Currency
        if element['Currency'] == self.base_currency:
            element['Amount in USD'] = element['Amount']
        else:
            element['Amount in USD'] = element['Amount'] * self.market_data['FX Spots']['rates'][element['Currency']]
        yield element


class ContractualRun(beam.DoFn):
    """
    Outputs key, value that will be grouped and generated
    """

    def __init__(self, contractual_run_keys):
        super(ContractualRun, self).__init__()
        self.contractual_run_keys = contractual_run_keys

    def process(self, element):
        if element['Cash Flow Date'].days < 0:
            days = -1
        elif element['Cash Flow Date'].days > 30:
            days = 30
        else:
            days = element['Cash Flow Date'].days

        yield (
        tuple(element[key] for key in global_config.contractual_run_keys) + tuple((days,)), element['Amount in USD'])