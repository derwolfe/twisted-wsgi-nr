Using New Relic with Twisted as a WSGI app Server
=================================================

XXX NEEDS TESTS

This repository is meant to show an example of how to setup Twisted, New Relic, and a WSGI app.

### Building
If you have docker installed, make sure that you forward port 8713 on your VM. Otherwise, you won't be able to hit the application.

### Running
The included `runner.sh` script will stop, start, and rebuild the docker container.
As long as your docker daemon is running, just typing `./runner.sh` should get the application running.

### New Relic
The application is setup in developer mode. This means that New Relic is installed, but that none of the data it collects will be sent to their servers.

Instead of using a configuration file, the docker file uses environment variables.

### TODO
Fix logging to just use structlog.
