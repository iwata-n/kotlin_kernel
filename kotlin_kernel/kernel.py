#!/usr/bin/env python
#-*- coding:utf-8 -*-

from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF

import signal
import tempfile
import os


class KotlinKernel(Kernel):
    """
    Kotlin Kernel for jupyter
    """
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
        """
        start kotlinc-jvm
        :return:
        """

        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            self.kotlinwrapper = replwrap.REPLWrapper("kotlinc-jvm", unicode(">>> "), None)
        finally:
            signal.signal(signal.SIGINT, sig)

    def parse_code(self, code):
        return code


    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        code = self.parse_code(code)
        print code
        if not code.strip():
            return {'status': 'ok', 'execution_count': self.execution_count,
                    'payload': [], 'user_expressions': {}}

        interrupted = False
        try:
            output = []
            for line in code.splitlines():
                output.append(self.kotlinwrapper.run_command(line))
        except KeyboardInterrupt:
            self.kotlinwrapper.child.sendintr()
            interrupted = True
            self.kotlinwrapper._expect_prompt()
            output = self.kotlinwrapper.child.before
        except EOF:
            output = self.kotlinwrapper.child.before + 'Restarting kotlin'
            self._start_kernel()

        if not silent:
            stream_content = {"name":"stdout", "text":"\r\n".join(output)}
            # stream_content = {"name":"stdout", "text":code}
            self.send_response(self.iopub_socket, "stream", stream_content)

        if interrupted:
            return {'status': 'abort', 'execution_count': self.execution_count}

        return {
            "status":"ok",
            "execution_count":self.execution_count,
            "payload":[],
            "user_expressions":{}
        }
