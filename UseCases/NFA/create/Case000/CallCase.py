from __future__ import absolute_import

import unittest
import doctest

import os
#import sys

from automata.fa.nfa import NFA

#
#######################
#
class CallUnits(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        NFA which matches strings beginning with 'a', ending with 'a', and containing
        no consecutive 'b's
        """
        cls.nfa = NFA(
            states={'q0', 'q1', 'q2'},
            input_symbols={'a', 'b'},
            transitions={
                'q0': {'a': {'q1'}},
                # Use '' as the key name for empty string (lambda/epsilon) transitions
                'q1': {'a': {'q1'}, '': {'q2'}},
                'q2': {'b': {'q0'}}
            },
            initial_state='q0',
            final_states={'q1'}
        )

        pass

    def testCase000(self):
        """The validate_self() method checks whether the NFA is
        actually a valid NFA. The method has the same basic behavior
        and prescribed use case as the DFA.validate_self() method,
        despite being less restrictive (since NFAs are naturally
        less restrictive than DFAs).
        """
        ret = self.nfa.validate_self()
        assert ret
        pass


    def testCase010(self):
        """
        The validate_input() method checks whether or not the given string
        is accepted by the NFA.

        If the string is accepted, the method returns a set of states the FA
        stopped on (which presumably contains at least one valid final state).
        """
        ret = self.nfa.validate_input('aba')  # returns {'q1', 'q2'}
        assert ret
        pass

    def testCase020(self):
        """If the string is rejected by the NFA, the method will raise a RejectionError.
        """
        ret = False
        try:
            self.nfa.validate_input('abba')  # raises RejectionError
        except:
            ret = True

        return ret
        pass

    def testCase030(self):
        """If you supply the step keyword argument with a value of True, the method will
        return a generator which yields each set of states reached as the NFA reads
        characters from the input string.
        """
        ret = list(self.nfa.validate_input('aba', step=True))
        # returns [{'q0'}, {'q1', 'q2'}, {'q0'}, {'q1', 'q2'}]

        assert ret == [{'q0'}, {'q1', 'q2'}, {'q0'}, {'q1', 'q2'}]
        pass

    def testCase100(self):
        """To create a deep copy of an NFA, simply pass an
        NFA instance into the NFA constructor.
        """
        nfa_copy = NFA(self.nfa)  # returns a deep copy of nfa

        self.assertEqual(self.nfa,nfa_copy)
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
