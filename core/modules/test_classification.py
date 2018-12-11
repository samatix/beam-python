"""
Test sets for the classification methods
"""

import logging
import os
import unittest
import tempfile
from core.modules import classification
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
from datetime import datetime, timedelta

from core.modules.classification import *


class ClassificationTest(unittest.TestCase):

    def setUp(self):
        test_data = "Product,Counterparty Category,Value date,Maturity,Start date,Cash Flow Type,Amount,Currency\n" \
                    "Term Deposit,RETAIL,2017-01-01,2017-01-05,2017-01-01,Initial,10000.,USD\n" \
                    "Term Deposit,RETAIL,2017-01-05,2017-03-30,2017-07-05,Initial,10000.,EUR\n" \
                    "Term Deposit,RETAIL,2017-01-10,2017-03-30,2017-07-05,Initial,10000.,EUR"
        self.test_files = {}
        logging.info('Input Data : %s', str(test_data))
        # Test data file is a CSV file
        input_file = tempfile.NamedTemporaryFile(suffix='.csv', prefix='liquidity-', delete=False)
        input_file.write(test_data)
        input_file.seek(0)
        self.test_files['input_file_name'] = input_file.name
        logging.info('Temporary file created: %s', self.test_files['input_file_name'])

        # Test configuration definition :
        self.test_configuration = {
            'System Date': datetime.strptime("2017-01-02", "%Y-%m-%d"),
            'Currencies': ["EUR", "USD", "GBP", "AUD", "JPY", "CHF", "CAD"],
            'Base Currency': "USD"
        }

        # Test market data definition:
        self.test_market_data = {
            "FX Spots" : {
                "timestamp": 1319730758,
                "base": "USD",
                "rates": {
                    "EUR": 2,
                    "GBP": 3,
                    "AUD": 4,
                    "JPY": 5,
                    "CHF": 6,
                    "CAD": 7
                }
            }
        }

        self.contractual_run_keys = ['Currency', 'Product']

        logging.info('Test configuration : %s', self.test_configuration)

    def tearDown(self):
        for test_file in self.test_files.values():
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_CashFlowDic(self):
        with TestPipeline() as p:
            results = (p | 'Create' >> beam.io.Read(sources.CsvFileSource(self.test_files['input_file_name']))
                       | 'Process' >> beam.ParDo(classification.CashFlowDic(self.test_configuration)))
            assert_that(
                results,
                equal_to(
                    [{'Product': 'Term Deposit', 'Cash Flow Type': 'Initial', 'Forward Start': False,
                     'Maturity': datetime(2017, 1, 5, 0, 0), 'Amount': 10000.0,
                     'Cash Flow Date': timedelta(-1), 'Counterparty Category': 'RETAIL',
                     'Value date': datetime(2017, 1, 1, 0, 0), 'Start date': datetime(2017, 1, 1, 0, 0),
                     'Currency': 'USD'},
                    {'Product': 'Term Deposit', 'Cash Flow Type': 'Initial', 'Forward Start': True,
                     'Maturity': datetime(2017, 3, 30, 0, 0), 'Amount': 10000.0, 'Cash Flow Date': timedelta(3),
                     'Counterparty Category': 'RETAIL', 'Value date': datetime(2017, 1, 5, 0, 0),
                     'Start date': datetime(2017, 7, 5, 0, 0), 'Currency': 'EUR'},
                    {'Product': 'Term Deposit', 'Cash Flow Type': 'Initial', 'Forward Start': True,
                     'Maturity': datetime(2017, 3, 30, 0, 0), 'Amount': 10000.0, 'Cash Flow Date': timedelta(8),
                     'Counterparty Category': 'RETAIL', 'Value date': datetime(2017, 1, 10, 0, 0),
                     'Start date': datetime(2017, 7, 5, 0, 0), 'Currency': 'EUR'}]
                ))

    def test_PostTreatment(self):
        with TestPipeline() as p:
            results = (p | 'Create' >> beam.io.Read(sources.CsvFileSource(self.test_files['input_file_name']))
                       | 'Process' >> beam.ParDo(classification.CashFlowDic(self.test_configuration))
                       | 'Post treatment' >> beam.ParDo(classification.PostTreatment(self.test_configuration,
                                                                                      self.test_market_data)))
            assert_that(
                results,
                equal_to(
                    [{'Product': 'Term Deposit', 'Cash Flow Type': 'Initial', 'Forward Start': False,
                      'Maturity': datetime(2017, 1, 5, 0, 0), 'Amount': 10000.0,
                      'Cash Flow Date': timedelta(-1), 'Counterparty Category': 'RETAIL',
                      'Value date': datetime(2017, 1, 1, 0, 0), 'Start date': datetime(2017, 1, 1, 0, 0),
                      'Currency': 'USD', 'Amount in USD': 10000.0},
                     {'Product': 'Term Deposit', 'Cash Flow Type': 'Initial', 'Forward Start': True,
                      'Maturity': datetime(2017, 3, 30, 0, 0), 'Amount': 10000.0, 'Cash Flow Date': timedelta(3),
                      'Counterparty Category': 'RETAIL', 'Value date': datetime(2017, 1, 5, 0, 0),
                      'Start date': datetime(2017, 7, 5, 0, 0), 'Currency': 'EUR', 'Amount in USD': 20000.0},
                     {'Product': 'Term Deposit', 'Cash Flow Type': 'Initial', 'Forward Start': True,
                      'Maturity': datetime(2017, 3, 30, 0, 0), 'Amount': 10000.0, 'Cash Flow Date': timedelta(8),
                      'Counterparty Category': 'RETAIL', 'Value date': datetime(2017, 1, 10, 0, 0),
                      'Start date': datetime(2017, 7, 5, 0, 0), 'Currency': 'EUR', 'Amount in USD': 20000.0}]
                ))

    def test_ContractualRun(self):
        with TestPipeline() as p:
            results = (p | 'Create' >> beam.io.Read(sources.CsvFileSource(self.test_files['input_file_name']))
                       | 'Process' >> beam.ParDo(classification.CashFlowDic(self.test_configuration))
                       | 'Post treatment' >> beam.ParDo(classification.PostTreatment(self.test_configuration,
                                                                                      self.test_market_data))
                       | 'Contractual Run' >> beam.ParDo(classification.ContractualRun(
                        self.contractual_run_keys)))
            assert_that(
                results,
                equal_to(
                    [(('EUR', 'Term Deposit', 3), 20000.0), (('EUR', 'Term Deposit', 8), 20000.0),
                     (('USD', 'Term Deposit', -1), 10000.0)]
                ))

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    unittest.main()