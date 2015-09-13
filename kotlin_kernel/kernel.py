#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pexpect import replwrap
from ipykernel.kernelbase import Kernel

import re

crlf = re.compile(r"[\r\n]+")

class KotlinKernel(Kernel):
    implementation = "kotlin"
    implementation_version = "0.1"
    language_version = "0.1"
    language_info = {"name":"kotlin",
                     'codemirror_mode': 'kotlin',
                     "mimetype":"text/plain",
                     "file_extension":".kts"}
    banner = "Kotlin kernel"


    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_kernel()

    def _start_kernel(self):
        self.kotlinwrapper = replwrap.REPLWrapper("kotlinc-jvm", unicode(">>> "), None)

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        #code = crlf.sub(" ", code.strip())

        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        interrupted = False
        try:
            output = self.kotlinwrapper.run_command(code, timeout=None)
        except KeyboardInterrupt:
            self.kotlinwrapper.child.sendintr()
            interrupted = True
            self.kotlinwrapper._expect_prompt()
            output = self.kotlinwrapper.child.before

        if not silent:
            stream_content = {"name":"stdout", "text":output}
            self.send_response(self.iopub_socket, "stream", stream_content)


        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        return {
            "status":"ok",
            "execution_count":self.execution_count,
            "payload":[],
            "user_expressions":{}
        }
