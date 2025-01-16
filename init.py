#!/bin/python
import config
import os

if not os.path.exists(config.train_central_pipe_name):
    os.mkfifo(config.train_central_pipe_name)

if not os.path.exists(config.lineman_central_pipe_name):
    os.mkfifo(config.lineman_central_pipe_name)

if not os.path.exists(config.central_lineman_pipe_name):
    os.mkfifo(config.central_lineman_pipe_name)
