#!/usr/bin/python3
""" Unit tests for testing something """

import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

from models import storage
from models.state import State
from console import HBNBCommand

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Not testing with MySQL")
class TestSomething(unittest.TestCase):
    """ Test cases for testing something """

    def setUp(self):
        """ Set up test environment """
        storage.reset()
        self.console_out = StringIO()
        sys.stdout = self.console_out

    def tearDown(self):
        """ Clean up test environment """
        sys.stdout = sys.__stdout__

    @patch('sys.stdin', StringIO("create State name=\"California\"\n"))
    def test_create_state(self):
        """ Test creating a new state """
        # Get number of states before creating
        num_states_before = len(storage.all(State))

        # Execute console command
        HBNBCommand().onecmd("create State name=\"California\"")

        # Get number of states after creating
        num_states_after = len(storage.all(State))

        # Check if difference is +1
        self.assertEqual(num_states_after - num_states_before, 1)

