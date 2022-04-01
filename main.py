from __future__ import print_function
from ButtonMapping import ButtonMapping
from Client import Client
import asyncio
import json

# Inputs.py is a module which aims to provide easy to use, cross-platform, user input device support for Python
# Inputs.py: Copyright (c) 2016, 2018: Zeth
# All rights reserved.
from inputs import get_gamepad, devices

import math
import csv
import datetime
client = Client()
asyncio.run(client.connect())
readControllerInput = ButtonMapping(client=client)
