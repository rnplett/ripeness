
## Very Simple Flask implementation

Since this is an introductory contained implementation of Flask, I've put together
simple step by step instructions for setting up a Flask web page.

Assumptions:
- Python 3.6 is installed. This example uses a typical python3.6 install on MacOS.
- You are starting in a terminal window in the directory that you want to add Flask
- You have administrative rights to create directories and install python packages

The first command will create a directory with the base Flask framework files:
```
git clone https://github.com/rnplett/FlaskBareDash.git
```

Once the framework files have been created locally you will start working in that directory.
```
cd FlaskBareDash
```

Next we will create a virtual environment that will contain all the requirements for running Flask and then activate that environment.
```
virtualenv -p /usr/local/bin/python3.6 vFlaskBareDash
source /vFlaskBareDash/bin/activate
```

In this virtual environment there are no python packages installed by default. The requirements.txt file contains all the needed packages. They can all be installed with one line.
```
pip install -r requirements.txt
```

If you're interested in publishing your own version of this dashboard once you've customized it for your needs the following commands will set up the git version control required for backing it up and making it accessible to others.

The following commands set up the project as a git repository locally and commit the code for versioning.
```
git init
git add .
git commit -m "First commit"
```

In order to publish the code you will need to log into https://github.com with your own username and create a new repository there. Take note of the url for this new repository. The following commands will set you up to publish your updated files every time you commit changes in version control locally.
```
git remote add origin << url of your repo on github >>
git push -u origin master
```

After every coding session you can update your online repository with the following command sequence.
```
git add .
git commit -m "The message you publish with the new committed changes"
git push -u origin master
```

Now you are ready to run the flask "web server". The following command prompt will initiate the web service:
```
FLASK_APP=hello.py flask run
```

After you issue the command above, the system will respond with a url that you can put in your favorite web browser to test your flask pages.  Here's an example of what that url may look like:
```
http://127.0.0.1:5000/hello
```

When you're done testing the ctrl-C key combination will escape you out of the process so you have your terminal prompt back.
