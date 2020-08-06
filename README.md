# mysocks

This repository contains my work on socket programming. The goal of this project is to provide a python package based on socket programming that can enable developers to create server-client backend for seamless and secure multiple file transfers, group chats, etc.

### Prerequisites
Windows (Python3.x)

### Installing dependencies
*Note*: You can skip this step, if you are installing the packages. 
Dependencies are listed below and in the `requirements.txt` file.

* tqdm

Install one of python package managers in your distro. If you install pip, then you can install the dependencies by running 
`pip3 install -r requirements.txt` 


### Directory Structure
- `mysocks/` - Package folder which contains all the code files corresponding to package
### TODO: Write example files for easy understanding
- `examples/` - Contains examples on how to use the package

### Details of the package
- `utilities.py` - Contains helper functions for the package
- `file_transfer` - Code to transfer files. Contains two classes for sending/receiving files.
	- `1 - send_files`
	- `2 - receive_files`

### How to run
server side
`from mysocks import chat
chat.server()`

client side
`from mysocks import chat
chat.client`

### TODO: Examples
Have a look at `examples/` directory.

### Documentation
Code documentation can be found [here](https://mysocks.readthedocs.io/)

### Installation

A `setup.py` file is provided in the repository. You can run `python3 setup.py install` to install it at system level.
If you don't have privileges to do so, you can install it at user level by running `python3 setup.py install --user`.  

### Contributing to the repository.
* If you find any problem with the code, please feel free to open an issue.
* Found something you can improve, please send me a pull request with your changes.
I will be more than happy to review and approve them.

### Contacting me
You can send an email to [thecodeboxed@gmail.com](mailto:thecodeboxed@gmail.com)

**Note**: If you find this code useful, please leave a star :)
