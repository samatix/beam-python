# Sample Apache Beam Development Environment for Python
Based initially on : https://github.com/danieldeleo/beam-workshop 


## Install Cloud SDK
* Follow the appropriate [quickstart](https://cloud.google.com/sdk/docs/quickstarts) for your OS
* Verify if already installed by typing `gcloud` in bash terminal 
* Initialize tool
  * `gcloud init`
    * Create your own project when prompted
* Set default application credentials
  * `gcloud auth application-default login`

## Download IDE (Integrated Development Environment) & Setup a Project Basic Configuration
* [Download/Install PyCharm Community Edition](https://www.jetbrains.com/pycharm/download)
* Add a new project by selecting VCS/Checkout From Version Control/GIT then select this repository : 
`https://github.com/samatix/beam-python`
* In Pycharm/Preferences/Project: Project_Name/Project Interpreter/Select parameters next to the project interepreter and click on add to create a new virtual environment. Check inherit global variables
* In Pycharm/Preferences/Tools/Python Integrated Tools, select the requirements.txt file as Package Requirements File. 
* Go to requirements file and hit install. This will help you automanage the dependencies 
* Under the main file, create a run configuration by putting the following parameters:

## Unitary testing setup 

## Debugging 
