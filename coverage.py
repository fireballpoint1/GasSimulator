from Setup import *
import Setup
import unittest
from unittest.mock import patch

class TestSetup(unittest.TestCase):
	def test_whole_func(self):
		user_input=[
				"2 100 5 1 0 1.0 1.5 2.0",
				"2   12   0   0   0   0",
				"80.000 20.000 0.0 0.0 0.0 0.0 20.000 760.000",
				"2.000 3.000 30.000 0 0",
				"50.0 0.55 2 1 1 1 1 1 1"
				]
		# print(Setup.NGAS)
		with patch('builtins.input',side_effect=user_input):
			out=SETUP(0)
			# ngas=SETUP(0).NGAS
		output=0
		print("output",output,Setup.NGAS)
		self.assertEqual(out,output)

class TestGas12(unittest.TestCase):
	def test_whole_func(self):
		# input arguments
		Q=numpy.zeros((6+1,20000+1))
		QIN=numpy.zeros((250+1,20000+1))
		NIN=0
		E=numpy.zeros((6+1))



if __name__ == '__main__':
	unittest.main()	