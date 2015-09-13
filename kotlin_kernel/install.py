#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
sample https://github.com/takluyver/bash_kernel/blob/master/bash_kernel/install.py
"""

import json
import os
import sys

from jupyter_client.kernelspec import install_kernel_spec
from IPython.utils.tempdir import TemporaryDirectory

kernel_json = {
    "argv":[sys.executable,"-m","kotlin_kernel", "-f", "{connection_file}"],
    "display_name":"Kotlin",
    "language":"kotlin",
}

def install_my_kernel_spec(user=True):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755) # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
        # TODO: Copy resources once they're specified

        print('Installing IPython kernel spec')
        install_kernel_spec(td, 'kotlin', user=user, replace=True)

def main(argv=None):
    install_my_kernel_spec()

if __name__ == '__main__':
    main()
