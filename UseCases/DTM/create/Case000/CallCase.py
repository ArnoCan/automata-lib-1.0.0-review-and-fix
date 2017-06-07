from __future__ import absolute_import

import unittest
import doctest

import os
#import sys

from automata.tm.dtm import DTM
from automata.tm.tape import TMTape

#
#######################
#
class CallUnits(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        DTM which matches all strings beginning with '0's, and followed by
        the same number of '1's
        """
        cls.dtm = DTM(
            states={'q0', 'q1', 'q2', 'q3', 'q4'},
            input_symbols={'0', '1'},
            tape_symbols={'0', '1', 'x', 'y', '.'},
            transitions={
                'q0': {
                    '0': ('q1', 'x', 'R'),
                    'y': ('q3', 'y', 'R')
                },
                'q1': {
                    '0': ('q1', '0', 'R'),
                    '1': ('q2', 'y', 'L'),
                    'y': ('q1', 'y', 'R')
                },
                'q2': {
                    '0': ('q2', '0', 'L'),
                    'x': ('q0', 'x', 'R'),
                    'y': ('q2', 'y', 'L')
                },
                'q3': {
                    'y': ('q3', 'y', 'R'),
                    '.': ('q4', '.', 'R')
                }
            },
            initial_state='q0',
            blank_symbol='.',
            final_states={'q4'}
        )

        pass

    def testCase000(self):
        """The validate_self() method checks whether the DTM is actually a valid DTM.
        The method has the same basic behavior and prescribed use case as the
        DFA.validate_self() and NFA.validate_self() methods, while (naturally)
        containing validation checks specific to DTMs.
        """
        ret = self.dtm.validate_self()
        assert ret
        pass


    def testCase010(self):
        """
        If the string is accepted, the method returns a tuple containing the state
        the machine stopped on (which presumably is a valid final state), as well
        as a TMTape object representing the DTM’s internal tape.
        """
        ret = self.dtm.validate_input('01')  # returns ('q4', TMTape('xy.'))
        self.assertEqual(ret, ('q4', TMTape('xy.',blank_symbol=self.dtm.blank_symbol)))
        pass

    def testCase020(self):
        """
        If the string is rejected by the DTM, the method will raise a RejectionError.
        """
        ret = False
        try:
            self.dtm.validate_input('011')  # raises RejectionError
        except:
            ret = True

        return ret
        pass

    def testCase030(self):
        """If you supply the step keyword argument with a value of True,
        the method will return a generator which yields a tuple containing
        the current state and the current tape as a TMTape object.
        """
        ret = [(state, tape.copy()) for state, tape in self.dtm.validate_input('01', step=True)]
        # returns [
        #   ('q0', TMTape('01',blank_symbol='.'))
        #   ('q1', TMTape('x1',blank_symbol='.'))
        #   ('q2', TMTape('xy',blank_symbol='.'))
        #   ('q0', TMTape('xy',blank_symbol='.'))
        #   ('q3', TMTape('xy',blank_symbol='.'))
        #   ('q3', TMTape('xy.',blank_symbol='.'))

#FIXME:
        #   ('q0', TMTape('01'))
        #   ('q1', TMTape('x1'))
        #   ('q2', TMTape('xy'))
        #   ('q0', TMTape('xy'))
        #   ('q3', TMTape('xy'))
        #   ('q3', TMTape('xy.'))
        # ]

        self.assertEqual(ret, [
            ('q0', TMTape('01',blank_symbol='.')),
            ('q1', TMTape('x1',blank_symbol='.')),
            ('q2', TMTape('xy',blank_symbol='.')),
            ('q0', TMTape('xy',blank_symbol='.')),
            ('q3', TMTape('xy',blank_symbol='.')),
            ('q4', TMTape('xy.',blank_symbol='.')),
            ]
        )

        pass

    def testCase100(self):
        """To create a deep copy of a DTM, simply pass a
        DTM instance into the DTM constructor.
        """
        dtm_copy = DTM(self.dtm)  # returns a deep copy of dtm

        self.assertEqual(self.dtm,dtm_copy)
        pass



#     def runTest( self ):
#         """Trivia: import examp
#         """
#         try:
#             import examp
#         except ImportError, e:
#             self.Fail( str( e ) )

#
#######################
#
#
#######################
#
if __name__ == '__main__':
    unittest.main()


# mport unittest
#    2 import doctest
#    3
#    4 class DeviceTest( unittest.TestCase ):
#    5     # This is a simple test that just tries to load the module
#    6     def runTest( self ):
#    7         try:
#    8             import examp
#    9         except ImportError, e:
#   10             self.Fail( str( e ) )
