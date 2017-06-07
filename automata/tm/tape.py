#!/usr/bin/env python3
"""Classes and methods for working with Turing machine tapes."""


class TMTape(object):
    """A Turing machine tape.

    Mainly single-tape view of Turing machines.
    """

    def __init__(self, tape, **kwargs):
        """Initialize the new Turing machine tape."""
        if isinstance(tape, TMTape):
            self._init_from_tape_obj(tape)
        else:
            self._init_from_tape_params(tape, **kwargs)

#FIXME:    def _init_from_tape_params(self, tape, *, blank_symbol, current_position=0,
    def _init_from_tape_params(self, tape, *, blank_symbol='', current_position=0,
                               position_offset=0):
        """Initialize a TM tape from the defined tape parameters."""
        self.tape = list(tape)
        self.blank_symbol = blank_symbol
        self.current_position = current_position
        self.position_offset = position_offset

    def _init_from_tape_obj(self, tape_obj):
        """Initialize this Tape as a deep copy of the given Tape."""
        self.__init__(
            tape=tape_obj.tape, blank_symbol=tape_obj.blank_symbol,
            current_position=tape_obj.current_position,
            position_offset=tape_obj.position_offset)

    def read_symbol(self):
        """Read the symbol at the current position in the tape."""
        actual_position = self.current_position + self.position_offset
        if actual_position == -1 or actual_position == len(self.tape):
            return self.blank_symbol
        else:
            return self.tape[actual_position]

    def write_symbol(self, new_tape_symbol):
        """Write the given symbol at the current position in the tape."""
        actual_position = self.current_position + self.position_offset
        if actual_position == -1:
            self.tape.insert(0, new_tape_symbol)
            self.position_offset += 1
        elif actual_position == len(self.tape):
            self.tape.append(new_tape_symbol)
        else:
            self.tape[actual_position] = new_tape_symbol

    def move(self, direction):
        """Move the tape to the next symbol in the given direction."""
        if direction == 'R':
            self.current_position += 1
        elif direction == 'L':  # pragma: no branch
            self.current_position -= 1

    def copy(self):
        """Return a deep copy of the tape."""
        return self.__class__(self)

    def __len__(self):
        """Return the number of symbols on the tape."""
        return len(self.tape)

    def __iter__(self):
        """Return an interator for the tape."""
        return iter(self.tape)

    def __str__(self):
        """Return a string representation of the tape."""
        res = ""
        res += "\ntape =" +str(self.tape)
        res += "\nblank_symbol = '"+str(self.blank_symbol)+"' "
        res += "\n"
        return res

    def __repr__(self):
        """Return a string representation of the tape."""
        res = "{"
        res += "'tape': '"+str(self.tape)+"',"
        res += "'blank_symbol': '"+str(self.blank_symbol)+"',"
        res += "}"
        return res

    def __eq__(self, other):
        """Check if two tapes are equal.

        Equal means: content AND blank_symbol

        """
#FIXME:
        return self.tape == other.tape and self.blank_symbol == other.blank_symbol

class TMTapeWithState(TMTape):
    """A Turing machine tape including processing positions.

    Multiple-tape Turing machines.
    """

    def __init__(self, tape, **kwargs):
        """Initialize the new Turing machine tape."""
        if isinstance(tape, TMTapeWithState):
            self.__init__(
                tape=tape.tape, blank_symbol=tape.blank_symbol,
                current_position=tape.current_position,
                position_offset=tape.position_offset)

            self._init_from_tape_obj(tape)
        else:
            super(TMTapeWithState,self).__init__(tape, **kwargs)

    def __eq__(self, other):
        """Check if two tapes are equal.

        Equal means: content, blank_symbol, processing positions

        The dictionaries contain:

            self.tape
            self.blank_symbol
            self.current_position
            self.position_offset

        """
        return self.__dict__ == other.__dict__

    def __str__(self):
        """Return a string representation of the tape."""
        res = ""
        res += "\ntape =" +str(self.tape)
        res += "\nblank_symbol = '"+str(self.blank_symbol)+"' "
        res += "\ncurrent_position = "+str(self.current_position)
        res += "\nposition_offset = "+str(self.position_offset)
        res += "\n"
        return res

    def __repr__(self):
        """Return a string representation of the tape."""
        res = "{"
        res += "'tape': '"+str(self.tape)+"',"
        res += "'blank_symbol': '"+str(self.blank_symbol)+"',"
        res += "'current_position': "+str(self.current_position)+","
        res += "'position_offset': "+str(self.position_offset)+","
        res += "}"
        return res

