#!/bin/bash

#Variables that I will move to Params~
DOCKER_IMAGE_NAME="vzdevopstraining/ovs"
DOCKER_IMAGE_VERSION="0.1"
INSTANCE_NAME_PREFIX="ovs"
DOCKER_HOST="tcp://ip-172-31-23-232.us-west-1.compute.internal:2375"
CURRENT_DOCKER_HOST=`echo $DOCKER_HOST`