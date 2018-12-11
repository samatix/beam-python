# Sample Apache Beam Development Environment

## Install Cloud SDK
* (Optional) [Request a Test Google Account](https://goo.gl/forms/di6SDpBFtvqnroSC3)
* Verify if already installed by typing `gcloud` in bash terminal 
* Follow the appropriate [quickstart](https://cloud.google.com/sdk/docs/quickstarts) for your OS
* Initialize tool
  * `gcloud init`
    * Create your own project when prompted
* Set default application credentials
  * `gcloud auth application-default login`

## Download IDE (Integrated Development Environment)

For Python Developers:
* [Download/Install PyCharm Community Edition](https://www.jetbrains.com/pycharm/download)

For Developers with only a browser:
* Clone GitHub repos in cloud shell and use code editor
  * [Shortcut to automatically clone beam-workshop](https://console.cloud.google.com/cloudshell/open?git_repo=https%3A%2F%2Fgithub.com%2Fdanieldeleo%2Fbeam-workshop)
    * Alternatively in cloud shell run:
    
    `git clone https://github.com/danieldeleo/beam-workshop.git`

## Launch your IDE

On the welcome screen:
* Select **Checkout from Version Control**
* Choose **Git** from the dropdown

Enter git repo URL:
* For Java Developers enter:
  * https://github.com/GoogleCloudPlatform/DataflowTemplates.git
* For Python Developers enter:
  * https://github.com/danieldeleo/beam-workshop.git
  
  
## Running Beam in Cloud Dataflow

Set the following required pipeline arguments:
* --runner=DataflowRunner
* --project=YOUR_PROJECT_ID

[More Dataflow Pipeline Options](https://cloud.google.com/dataflow/pipelines/specifying-exec-params#setting-other-cloud-pipeline-options)

## Build and Run Beam SDK Examples

Launch IntelliJ and on the welcome screen:
* Select **Checkout from Version Control**
* Choose **Git** from the dropdown
* Enter git repo URL:
https://github.com/apache/beam.git

### Python

The following commands should be run in the `sdks/python` directory
* `virtualenv env`
* `source env/bin/activate`
* `pip install -e .[gcp]`


## Source