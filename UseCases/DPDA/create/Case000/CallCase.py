from __future__ import absolute_import

import unittest
import doctest

import os
#import sys

from automata.pda.dpda import DPDA
from automata.pda.stack import PDAStack
#
#######################
#
class CallUnits(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        DPDA which which matches zero or more 'a's, followed by the same
        number of 'b's (accepting by final state)
        """
        cls.dpda = DPDA(
            states={'q0', 'q1', 'q2', 'q3'},
            input_symbols={'a', 'b'},
            stack_symbols={'0', '1'},
            transitions={
                'q0': {
                    'a': {'0': ('q1', ('1', '0'))}  # transition pushes '1' to stack
                },
                'q1': {
                    'a': {'1': ('q1', ('1', '1'))},
                    'b': {'1': ('q2', '')}  # transition pops from stack
                },
                'q2': {
                    'b': {'1': ('q2', '')},
                    '': {'0': ('q3', ('0',))}  # transition does not change stack
                }
            },
            initial_state='q0',
            initial_stack_symbol='0',
            final_states={'q3'}
        )

        pass

    def testCase000(self):
        """The validate_self() method checks whether the DPDA is actually
        a valid DPDA. The method has the same basic behavior and prescribed
        use case as the DFA.validate_self() and NFA.validate_self() methods,
        while (naturally) containing validation checks specific to DPDAs.
        """
        ret = self.dpda.validate_self()
        assert ret
        pass


    def testCase010(self):
        """
        If the string is accepted, the method returns a tuple containing
        the state the DPDA stopped on (which presumably is a valid final state),
        as well as a PDAStack object representing the DPDA’s internal stack.
        """
        ret = self.dpda.validate_input('ab')  # returns PDAStack(['0'])
        assert ret == ('q3', PDAStack(['0']))
        pass

    def testCase020(self):
        """If the string is rejected by the DPDA, the method will raise a RejectionError.
        """
        ret = False
        try:
            self.dpda.validate_input('aab')  # raises RejectionError
        except:
            ret = True

        return ret
        pass

    def testCase030(self):
        """If you supply the step keyword argument with a value of True, the method
        will return a generator which yields a tuple containing the current state
        and the current tape as a PDAStack object.
        """
        ret = [(state, stack.copy()) for state, stack in self.dpda.validate_input('ab', step=True)]
        # returns [
        #   ('q0', PDAStack(['0'])),
        #   ('q1', PDAStack(['0', '1'])),
        #   ('q3', PDAStack(['0'])),
        # ]

        self.assertEqual(ret, [
            ('q0', PDAStack(['0'])),
            ('q1', PDAStack(['0', '1'])),
            ('q3', PDAStack(['0'])),
            ]
        )
        pass

    def testCase100(self):
        """To create a deep copy of an NFA, simply pass an
        NFA instance into the NFA constructor.
        """
        dpda_copy = DPDA(self.dpda)  # returns a deep copy of dpda

        self.assertEqual(self.dpda,dpda_copy)
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
