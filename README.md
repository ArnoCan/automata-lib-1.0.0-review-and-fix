#--------------------------
# Automata-acue

This is a review and bugfix release as part of a study for a common
extendable framework of Chomsky types.

Therefore some UseCases and tests are added as UnitTests for
Eclipse/PyDev/PyUnit.

Fixes/changes:

- added: \_\_str\_\_ for automata.tm.tape.TMTape - supported by Hover of PyDev.
- changed: \_\_eq\_\_ for automata.tm.tape.TMTape.
- added: initialization of *blank_symbol* for
  automata.tm.tape.TMTape._init_from_tape_params.
- added: automata.UseCases
- added: automata.tests
- added: automata.tm.tape.TMTapeWithState
  This manages the \_\_eq\_\_ operator:
  - TMTape.\_\_eq\_\_: content only -> content, blank_symbol
  - TMTapeWithState.\_\_eq\_\_: additional position

* Arno-Can Uestuensoez - https://arnocan.wordpress.com

The fixes are checked in into this repo, but there is no intention
to continue the work on this package after analysing the code. For
the current version refer to the original as referenced following.

#--------------------------

**Original**:

For Copyright, Licenses etc. refer to original:

- https://github.com/caleb531/automata
- https://pypi.python.org/pypi/automata-lib

#--------------------------

# Automata - with minor fixes/patches

Original: *Copyright 2016 Caleb Evans* - *Released under the MIT license*

Patches: *Copyright 2017 Arno-Can Uestuensoez* - *Released under the MIT license*


[![Build Status](https://travis-ci.org/caleb531/automata.svg?branch=master)](https://travis-ci.org/caleb531/automata)
[![Coverage Status](https://coveralls.io/repos/caleb531/automata/badge.svg?branch=master)](https://coveralls.io/r/caleb531/automata?branch=master)

Automata is a Python 3 library which implements the structures and algorithms I
am learning in my Automata Theory class, particularly finite automata and Turing
machines.

Automata requires Python 3.4 or newer.

## Installing

You can install the latest version of Automata via pip:

```
pip install automata-lib
```

## API

### class Automaton

The `Automaton` class is an abstract base class from which all automata
(including Turing machines) inherit. As such, it cannot be instantiated on its
own; you must use a defined subclasses instead (or you may create your own
subclass if you're feeling adventurous). The `Automaton` class can be found
under `automata/shared/automaton.py`.

If you wish to subclass `Automaton`, you can import it like so:

```python
from automata.shared.automaton import Automaton
```


### class FA

The `FA` class is an abstract base class from which all finite automata inherit.
As such, it cannot be instantiated on its own; you must use the `DFA` and `NFA`
classes instead (or you may create your own subclass if you're feeling
adventurous). The `FA` class can be found under `automata/fa/fa.py`.

If you wish to subclass `FA`, you can import it like so:

```python
from automata.fa.fa import FA
```

### class DFA

The `DFA` class is a subclass of class `FA` which represents a deterministic
finite automaton. The `DFA` class can be found under `automata/fa/dfa.py`.

#### DFA properties

Every DFA instance has the following properties:

1. `states`: a `set` of the DFA's valid states, each of which must be
represented as a string

2. `input_symbols`: a `set` of the DFA's valid input symbols, each of which must
also be represented as a string

3. `transitions`: a `dict` consisting of the transitions for each state. Each
key is a state name and each value is a `dict` which maps a symbol (the key) to
a state (the value).

4. `initial_state`: the name of the initial state for this DFA

5. `final_states`: a `set` of final states for this DFA

All of these properties must be supplied when the DFA is
instantiated (see the examples below).

```python
from automata.fa.dfa import DFA
# DFA which matches all binary strings ending in an odd number of '1's
dfa = DFA(
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
```

Please note that the below DFA code examples reference the above `dfa` object.

#### DFA.validate_input(self, input_str, step=False)

The `validate_input()` method checks whether or not the given string is accepted
by the DFA.

If the string is accepted, the method returns the state the DFA stopped on
(which presumably is a valid final state).

```python
dfa.validate_input('01')  # returns 'q1'
```

If the string is rejected by the DFA, the method will raise a `RejectionError`.

```python
dfa.validate_input('011')  # raises RejectionError
```

If you supply the `step` keyword argument with a value of `True`, the method
will return a generator which yields each state reached as the DFA reads
characters from the input string.

```python
list(dfa.validate_input('0111', step=True))
# returns ['q0', 'q0', 'q1', 'q2', 'q1']
```

Note that the first yielded state is always the DFA's initial state (before any
input has been read) and the last yielded state is always the DFA's final state
(after all input has been read). If the string is rejected by the DFA, the
method still raises a `RejectionError`.

#### DFA.validate_self(self)

The `validate_self()` method checks whether the DFA is actually a valid DFA. The
method returns `True` if the DFA is valid; otherwise, it will raise the
appropriate exception (*e.g.* the state transition is missing for a particular
symbol). This method is automatically called when the DFA is initialized, so
it's only really useful if a DFA object is modified after instantiation.

#### Copying a DFA

To create a deep copy of a DFA, simply pass an `DFA` instance into the `DFA`
constructor.

```python
dfa_copy = DFA(dfa)  # returns a deep copy of dfa
```

### class NFA

The `NFA` class is a subclass of class `FA` which represents a nondeterministic
finite automaton. The `NFA` class can be found under `automata/fa/nfa.py`.

#### NFA properties

Every NFA contains the same five DFA properties: `state`, `input_symbols`,
`transitions`, `initial_state`, and `final_states`. However, the structure of
the  `transitions` object has been modified slightly to accommodate the fact
that a single state can have more than one transition for the same symbol.
Therefore, instead of mapping a symbol to *one* end state in each sub-dict, each
symbol is mapped to a *set* of end states.

```python
from automata.fa.nfa import NFA
# NFA which matches strings beginning with 'a', ending with 'a', and containing
# no consecutive 'b's
nfa = NFA(
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
```

#### NFA.validate_input(self, input_str, step=False)

The `validate_input()` method checks whether or not the given string is accepted
by the NFA.

If the string is accepted, the method returns a `set` of states the FA stopped
on (which presumably contains at least one valid final state).

```python
nfa.validate_input('aba')  # returns {'q1', 'q2'}
```

If the string is rejected by the NFA, the method will raise a `RejectionError`.

```python
nfa.validate_input('abba')  # raises RejectionError
```

If you supply the `step` keyword argument with a value of `True`, the method
will return a generator which yields each set of states reached as the NFA reads
characters from the input string.

```python
list(nfa.validate_input('aba', step=True))
# returns [{'q0'}, {'q1', 'q2'}, {'q0'}, {'q1', 'q2'}]
```

Note that the first yielded set is always the lambda closure of the NFA's
initial state, and the last yielded set always contains the lambda closure of at
least one of the NFA's final states (after all input has been read). If the
string is rejected by the NFA, the method still raises a `RejectionError`.

#### NFA.validate_self(self)

The `validate_self()` method checks whether the NFA is actually a valid NFA. The
method has the same basic behavior and prescribed use case as the
`DFA.validate_self()` method, despite being less restrictive (since NFAs are
naturally less restrictive than DFAs).

#### Converting an NFA to a DFA

To create a DFA that is equivalent to an existing NFA, simply pass the `NFA`
instance to the `DFA` constructor.

```python
from automata.fa.dfa import DFA
dfa = DFA(nfa)  # returns an equivalent DFA
```

#### Copying an NFA

To create a deep copy of an NFA, simply pass an `NFA` instance into the `NFA`
constructor.

```python
nfa_copy = NFA(nfa)  # returns a deep copy of nfa
```

#### class PDA

The `PDA` class is an abstract base class from which all pushdown automata
inherit. The `PDA` class can be found under `automata/pda/pda.py`.

### class DPDA

The `DPDA` class is a subclass of class `PDA` which represents a deterministic
finite automaton. The `DPDA` class can be found under `automata/pda/dpda.py`.

#### DPDA properties

Every DPDA instance has the following properties:

1. `states`: a `set` of the DPDA's valid states, each of which must be
represented as a string

2. `input_symbols`: a `set` of the DPDA's valid input symbols, each of which
must also be represented as a string

3. `stack_symbols`: a `set` of the DPDA's valid stack symbols

4. `transitions`: a `dict` consisting of the transitions for each state; see the
example below for the exact syntax

5. `initial_state`: the name of the initial state for this DPDA

6. `initial_stack_symbol`: the name of the initial symbol on the stack for this
DPDA

7. `final_states`: a `set` of final states for this DPDA

All of these properties must be supplied when the DPDA is
instantiated (see the examples below).

```python
from automata.pda.dpda import DPDA
# DPDA which which matches zero or more 'a's, followed by the same
# number of 'b's (accepting by final state)
dpda = DPDA(
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
```

Please note that the below DPDA code examples reference the above `dpda` object.

#### DPDA.validate_input(self, input_str, step=False)

The `validate_input()` method checks whether or not the given string is accepted
by the DPDA.

If the string is accepted, the method returns a tuple containing the state the
DPDA stopped on (which presumably is a valid final state), as well as a
`PDAStack` object representing the DPDA's internal stack.

```python
dpda.validate_input('ab')  # returns PDAStack(['0'])
```

If the string is rejected by the DPDA, the method will raise a `RejectionError`.

```python
dpda.validate_input('aab')  # raises RejectionError
```

If you supply the `step` keyword argument with a value of `True`, the method
will return a generator which yields a tuple containing the current state and
the current tape as a `PDAStack` object.

```python
[(state, stack.copy()) for state, stack in dpda.validate_input('ab', step=True)]
# returns [
#   ('q0', PDAStack(['0'])),
#   ('q1', PDAStack(['0', '1'])),
#   ('q3', PDAStack(['0'])),
# ]
```

Note that the first yielded state is always the DPDA's initial state (before any
input has been read) and the last yielded state is always the DPDA's final state
(after all input has been read) (or possibly a non-final state if the stack is
empty). If the string is rejected by the DPDA, the method still raises a
`RejectionError`.

#### DPDA.validate_self(self)

The `validate_self()` method checks whether the DPDA is actually a valid DPDA.
The method has the same basic behavior and prescribed use case as the
`DFA.validate_self()` and `NFA.validate_self()` methods, while (naturally)
containing validation checks specific to DPDAs.

#### Copying a DPDA

To create a deep copy of a DPDA, simply pass an `DPDA` instance into the
`DPDA` constructor.

```python
dpda_copy = DPDA(dpda)  # returns a deep copy of dpda
```

### class TM

The `TM` class is an abstract base class from which all Turing machines inherit.
The `TM` class can be found under `automata/tm/tm.py`.

### class DTM

The `DTM` class is a subclass of class `TM` which represents a deterministic
Turing machine. The `DTM` class can be found under `automata/tm/dtm.py`.

#### DTM properties

Every DTM instance has the following properties:

1. `states`: a `set` of the DTM's valid states, each of which must be
represented as a string

2. `input_symbols`: a `set` of the DTM's valid input symbols represented as
strings

3. `tape_symbols`: a `set` of the DTM's valid tape symbols represented as
strings

4. `transitions`: a `dict` consisting of the transitions for each state; each
key is a state name and each value is a `dict` which maps a symbol (the key) to
a state (the value)

5. `initial_state`: the name of the initial state for this DTM

6. `blank_symbol`: a symbol from `tape_symbols` to be used as the blank symbol
for this DTM

7. `final_states`: a `set` of final states for this DTM

All of these properties must be supplied when the DTM is instantiated (see the
examples below).

The tape comprises the following attributes:

- tape: content
- blank_symbol: "empty" field
- current_position: head position
- position_offset: offset

In case of required comparison operation *__eq__* two classes are provided.
This is required e.g. for Unit tests, when a reference class with static content
has to be checked only.

- TMTape: content only
- TMTapeWithState: content and operational state, positions.

```python
from automata.tm.dtm import DTM
# DTM which matches all strings beginning with '0's, and followed by
# the same number of '1's
dtm = DTM(
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
```

Please note that the below DTM code examples reference the above `dtm` object.

#### DTM.validate_input(self, input_str, step=False)

The `validate_input()` method checks whether or not the given string is accepted
by the DTM.

If the string is accepted, the method returns a tuple containing the state the
machine stopped on (which presumably is a valid final state), as well as a
`TMTape` object representing the DTM's internal tape.

```python
dtm.validate_input('01')  # returns ('q4', TMTape('xy.'))
```

If the string is rejected by the DTM, the method will raise a `RejectionError`.

```python
dtm.validate_input('011')  # raises RejectionError
```

If you supply the `step` keyword argument with a value of `True`, the method
will return a generator which yields a tuple containing the current state and
the current tape as a `TMTape` object.

```python
[(state, tape.copy()) for state, tape in dtm.validate_input('01', step=True)]
# returns [
#   ('q0', TMTape('01',blank_symbol=BS))
#   ('q1', TMTape('x1',blank_symbol=BS))
#   ('q2', TMTape('xy',blank_symbol=BS))
#   ('q0', TMTape('xy',blank_symbol=BS))
#   ('q3', TMTape('xy',blank_symbol=BS))
#   ('q3', TMTape('xy.',blank_symbol=BS))
# ]
# Where BS is the blank symbol, default:=''.
#
```

Please note that each tuple contains a reference to (not a copy of) the current
`TMTape` object. Therefore, if you wish to store the tape at every step, you
must copy the tape as you iterate over the machine configurations (as shown
above).

Also note that the first yielded state is always the DTM's initial state (before
any input has been read) and the last yielded state is always the DTM's final
state (after all input has been read). If the string is rejected by the DTM, the
method still raises a `RejectionError`.

The following includes the state-recognition for *\_\_eq\_\_*, *\_\_str\_\_*, *\_\_repr\_\_*.

```python
[(state, TMTapeWithState(tape) for state, tape in dtm.validate_input('01', step=True)]
# returns [
#   ('q0', TMTapeWithState('01',blank_symbol=BS,current_position=CP,position_offset=PO))
#   ('q1', TMTapeWithState('x1',blank_symbol=BS,current_position=CP,position_offset=PO))
#   ('q2', TMTapeWithState('xy',blank_symbol=BS,current_position=CP,position_offset=PO))
#   ('q0', TMTapeWithState('xy',blank_symbol=BS,current_position=CP,position_offset=PO))
#   ('q3', TMTapeWithState('xy',blank_symbol=BS,current_position=CP,position_offset=PO))
#   ('q3', TMTapeWithState('xy.',blank_symbol=BS,current_position=CP,position_offset=PO))
# ]
#
# Where the values from *TMTape* are pushed:
# - 'tape', tape.tape
# - BS is the blank symbol, tape.blank_symbol
# - CP is the current position, tape.current_position
# - PO is the position offset, tape.position_offset
#
# When set explicit:
# - BS is the blank symbol, default:=''.
# - CP is the current position, default:=0.
# - PO is the position offset, default:=0.
#
```

#### DTM.validate_self(self)

The `validate_self()` method checks whether the DTM is actually a valid DTM. The
method has the same basic behavior and prescribed use case as the
`DFA.validate_self()` and `NFA.validate_self()` methods, while (naturally)
containing validation checks specific to DTMs.

#### Copying a DTM

To create a deep copy of a DTM, simply pass a `DTM` instance into the `DTM`
constructor.

```python
dtm_copy = DTM(dtm)  # returns a deep copy of dtm
```

### Shared exception classes

The library also includes a number of exception classes to ensure that errors
never pass silently (unless explicitly silenced). See `automata/fa.py` for these
class definitions.

To reference these exceptions (so as to catch them in a `try..except` block or
whatnot), simply import `automata.shared.exceptions` however you'd like:

```python
import automata.shared.exceptions as exceptions
```

#### class AutomatonError

A base class from which all other automata exceptions inherit (including finite
automata and Turing machines).

#### class InvalidStateError

Raised if a state is not a valid state for this FA.

#### class InvalidSymbolError

Raised if a symbol is not a valid symbol for this FA.

#### class MissingStateError

Raised if a state is missing from the machine definition.

#### class MissingSymbolError

Raised if a symbol is missing from the machine definition.

#### class InitialStateError

Raised if the initial state fails to meet some required condition for this type
of machine.

#### class FinalStateError

Raised if a final state fails to meet some required condition for this type of
machine.

#### class RejectionError

Raised if the FA stopped on a non-final state after validating input.

### Turing machine exception classes

The `automata.tm` package also includes a module for exceptions specific to
Turing machines. You can reference these exception classes like so:

```python
import automata.tm.exceptions as tmexceptions
```

#### class TMError

A base class from which all other Turing machine exceptions inherit.

#### class InvalidDirectionError

Raised if a direction specified in this machine's transition map is not a valid
direction.
