"""
Test custom Django management command
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2OpError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands"""

    def test_wait_for_db_ready(self, patched_check):  
        """
        Test waiting for database if database ready
        patched_check is mock object which is replaced by "check"
        called above in @patch, used to customize behaviour
        """
        patched_check.return_value=True

        # call_command will execute the code inside "wait_for_db"
        # and does two things:
        # 1) Check for the command "wait_for_db" if it exists 
        #    or not. Or if it functions properly.
        # 2) Checks if database is ready or not, if the command 
        #    is set properly.
        call_command('wait_for_db')

        # this basically checks the mocked object which is check
        # gets called from inside wait_for_db for the default
        # database.
        patched_check.assert_called_once_with(databases=['default'])


    # time.sleep is passed as patched_sleep whereas the check object
    # above the class declaration is patched_check.
    # this works like inside out. for example: if we declare
    # @patch('time.sleep2')
    # @patch('time.sleep')
    # then the function will have arguments:
    # wait_for_db_delay(self, patched_sleep, patched_sleep2, patched_check)
    # the time.sleep just replaces the built in sleep function in python 
    # and does not actually pauses our tests by sleeping, but is just used for
    # mocking purpose
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """ Test waiting for database when getting Operational Error"""

        # First 2 times raise Psycopg2Error and next 3 times raise
        # OperationalError and the 6th time assign True value
        # Reason:
        # Since we are mocking the db here, therfore, when actual db
        # starts it is not ready to accept any connections and will 
        # probably give error similar to Psycopg2Error. After that
        # db is ready to accept connections but it has not created the 
        # testing db which we want to check and therefore we raise the 
        # OperationalError.
        #
        # NOTE: These are arbitrary values, and can be changed with
        #       respect to our scenario
        patched_check.side_effects = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])


