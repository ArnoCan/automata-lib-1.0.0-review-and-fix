from __future__ import absolute_import

import unittest
import doctest

import os
#import sys

from automata.fa.dfa import DFA

#
#######################
#
class CallUnits(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        DFA which matches all binary strings ending in an odd number of '1's
        """
        cls.dfa = DFA(
            states={'q0', 'q1', 'q2'},
            input_symbols={'0', '1'},
            transitions={
                'q0': {'0': 'q0', '1': 'q1'},
                'q1': {'0': 'q0', '1': 'q2'},
                'q2': {'0': 'q2', '1': 'q1'}
            },
            initial_state='q0',
            final_states={'q1'}
        )
        pass

    def testCase000(self):
        """The validate_self() method checks whether the DFA is actually
        a valid DFA. The method returns True if the DFA is valid; otherwise,
        it will raise the appropriate exception (e.g. the state transition
        is missing for a particular symbol). This method is automatically
        called when the DFA is initialized, so it’s only really useful if
        a DFA object is modified after instantiation.
        """
        ret = self.dfa.validate_self()
        assert ret
        pass

    def testCase010(self):
        """If the string is accepted, the method returns the state the DFA
        stopped on (which presumably is a valid final state).
        """
        ret = self.dfa.validate_input('01')  # returns 'q1'
        assert ret == 'q1'
        pass

    def testCase020(self):
        """If the string is rejected by the DFA, the method will raise a RejectionError.
        """
        ret = False
        try:
            self.dfa.validate_input('011')  # raises RejectionError
        except:
            ret = True

        return ret
        pass

    def testCase030(self):
        """If you supply the step keyword argument with a value of True,
        the method will return a generator which yields each state
        reached as the DFA reads characters from the input string.
        """
        ret = list(self.dfa.validate_input('0111', step=True))
        # returns ['q0', 'q0', 'q1', 'q2', 'q1']

        assert ret == ['q0', 'q0', 'q1', 'q2', 'q1']
        pass

    def testCase100(self):
        """To create a deep copy of an NFA, simply pass an
        NFA instance into the NFA constructor.
        """
        dfa_copy = DFA(self.dfa)  # returns a deep copy of nfa

        self.assertEqual(self.dfa,dfa_copy)
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
