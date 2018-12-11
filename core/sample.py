# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
An Apache Beam Sample Workflow
"""

from __future__ import absolute_import
import argparse
import logging
import re
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from core.configuration import global_config
from core.marketdata import global_data
from core.modules import classification
from utils.io import sources


def run(argv=None):
    """Main entry point to the liquidity module"""

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input', default='', help='Input root file (e.g : gs//data/file.txt')
    parser.add_argument('--output', dest='output',
                        default='./output.txt', help='Output file')

    known_args, pipeline_args = parser.parse_known_args(argv)

    with beam.Pipeline(argv=pipeline_args) as liquidity_pipeline:
        (liquidity_pipeline | 'Create' >> beam.io.Read(sources.CsvFileSource(known_args.input))
         | 'Process' >> beam.ParDo(classification.CashFlowDic(global_config.global_configuration))
         | 'Post treatment' >> beam.ParDo(classification.PostTreatment(global_config.global_configuration,
                                                                       global_data.market_data))
         | 'Contractual Run' >> beam.ParDo(classification.ContractualRun(global_config.contractual_run_keys))
         | 'Combing the results' >> beam.CombinePerKey(sum)
         | 'Write to file' >> beam.io.WriteToText(known_args.output))
