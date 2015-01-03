#!/usr/bin/env python

import subprocess
import sys
import runpy

from bottle import run
import routes

import tests.tests
from tests.tests import *

def ParseArgs():
	# So that we can be 2.[67] compatible.
	try:
		import argparse
		argparser = argparse.ArgumentParser(description=description_string)
		add_argument = argparser.add_argument
		add_argument("args", nargs='+', default=[])
		use_optparse = False
	except:
		import optparse as argparse
		argparser = argparse.OptionParser()
		add_argument = argparser.add_option
		use_optparse = True

	add_argument("-c", "--config", dest="config", default="blog.ini", help="Blog configuration file.")

	kwargs = argparser.parse_args()
	args = []

	#To deal with the argparse vs optparse discrepency.
	if not use_optparse:
		args = kwargs.args
	else:
		args = kwargs[1]
		kwargs = kwargs[0]

	return (args, kwargs)


if __name__ == "__main__":
	(args, kwargs) = ParseArgs()

	if "tests" in args:
		#Man this is a hack.  Makes it so that the test runner doesn't think "tests" is a request.
		sys.argv.remove("tests")
		runpy.run_module("tests/tests", None,  "__main__", True)
		print "\n"
	else:
		routes.Run(kwargs.config)


#Movie 1:10
