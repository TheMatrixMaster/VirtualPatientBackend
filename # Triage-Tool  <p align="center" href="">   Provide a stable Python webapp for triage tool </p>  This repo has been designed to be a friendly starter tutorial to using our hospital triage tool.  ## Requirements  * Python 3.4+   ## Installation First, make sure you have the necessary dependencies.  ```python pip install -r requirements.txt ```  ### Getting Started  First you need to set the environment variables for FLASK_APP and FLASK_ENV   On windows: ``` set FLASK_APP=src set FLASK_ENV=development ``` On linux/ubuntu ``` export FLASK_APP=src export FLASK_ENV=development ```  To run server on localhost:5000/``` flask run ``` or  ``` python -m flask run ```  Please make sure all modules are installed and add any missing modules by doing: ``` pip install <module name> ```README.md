# Virtual Patient Back-end Service

<p align="center" href="">
  Provide a stable Flask Back-end to handle text and speech processing
</p>

This repo has been designed to be a friendly starter tutorial to using our virtual patient.

## Requirements

* Python 3.4+


## Installation
First, make sure you have the necessary dependencies.

```python
pip install -r requirements.txt
```

### Getting Started

First you need to set the environment variables for FLASK_APP and FLASK_ENV 
You also need to provide a path towards your GOOGLE_APPLICATION_CREDENTIALS file that can be obtained from your google cloud service identity.

On windows:
```
set FLASK_APP=src
set FLASK_ENV=development
set GOOGLE_APPLICATION_CREDENTIALS=path/to/your/file
```
On linux/ubuntu
```
export FLASK_APP=src
export FLASK_ENV=development
export GOOGLE_APPLICATION_CREDENTIALS=path/to/your/file
```

To run server on localhost:5000/
```
flask run
```
or 
```
python -m flask run
```

Please make sure all modules are installed and add any missing modules by doing:
```
pip install <module name>
```
