# A Simple Build Server


This application allows users to build a C program and download the generated artifact.

## Prerequisites
 * Before you begin, ensure you have the following installed on your system:
   * Python 3.x
   * pip3 (Python package installer)
   * git (to clone repositories)




## Setting Up a Virtual Environment
Create a virtual environment: Open a terminal and navigate to your project directory. Run the following command to create a virtual environment named venv:
```bash
python -m venv venv
```
## Activate the virtual environment:

```bash
source venv/bin/activate
```

## Clone Build server
```
git clone git@github.com:aodeniyide/build-server.git
```
## Install required packages
```
pip3 install -r requirements.txt
```


## Running the Application
```
python3 server.py

Access the application: Open your web browser and navigate to http://127.0.0.1:8000 to access the application.
```

### Using the Application
  * On the home page, enter the [GitHub repository URL of the program](git@github.com:aodeniyide/sample-program.git) and click the **Start** button.
  * After submission, the application will clone the repository and run the Makefile. You can monitor the logs displayed on the page.

## Download the Artifact:
If the build is successful, a download link for the generated artifact will be provided. Click on the link to download the file.
