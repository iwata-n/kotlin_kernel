#!/usr/bin/env python
#-*- coding:utf-8 -*-


from ipykernel.kernelapp import IPKernelApp
from kernel import KotlinKernel

IPKernelApp.launch_instance(kernel_class=KotlinKernel)