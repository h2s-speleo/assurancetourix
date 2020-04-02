#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pyo import *
inputs, outputs = pa_get_devices_infos()
for index in sorted(outputs.keys()):
    print(outputs[index]['name'])
