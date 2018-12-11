"""
An Apache Beam Sample Development Setup

This configuration is initially inspired from the juliaset examples available
in the Apache Beam Package.

This example has in the core/ folder all the code needed to execute the
workflow.

It is organized in this way so that it can be packaged as a Python
package and later installed in the VM workers executing the job. The root
directory for the example contains just a "driver" script to launch the job
and the setup.py file needed to create a package.

The advantages for organizing the code is that large projects will naturally
evolve beyond just one module and you will have to make sure the additional
modules are present in the worker.

In Python Dataflow, using the --setup_file option when submitting a job, will
trigger creating a source distribution (as if running python setup.py sdist) and
then staging the resulting tarball in the staging area. The workers, upon
startup, will install the tarball.

Below is a complete command line for running the juliaset workflow remotely as
an example:

python sample_main.py \
  --job_name core-$USER \
  --project YOUR-PROJECT \
  --runner DataflowRunner \
  --setup_file ./setup.py \
  --staging_location gs://YOUR-BUCKET/core-dev/staging \
  --temp_location gs://YOUR-BUCKET/core-dev/temp \
  --coordinate_output gs://YOUR-BUCKET/core-dev/out \
  --grid_size 20 \
"""

import logging
from core import sample

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    sample.run()
