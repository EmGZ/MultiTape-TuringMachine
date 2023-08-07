class MultiTapeTuringMachine:
    def __init__(self):
        self.tapes = []
        self.head_positions = []
        self.current_state = None
        self.transitions = {}
        self.accept_states = set()

    def add_tape(self, tape):
        self.tapes.append(tape)
        self.head_positions.append(0)

    def add_transition(self, state, read_symbol, new_state, write_symbol, move):
        self.transitions[(state, read_symbol)] = (new_state, write_symbol, move)
    
    def add_transition_for_multi_tapes(self, tape_idx, transitions):
        for transition in transitions:
            current_state, read_symbol, new_state, write_symbol, move = transition
            if (tape_idx, current_state, read_symbol) in self.transitions:
                self.transitions[(tape_idx, current_state, read_symbol)].append((new_state, write_symbol, move))
            else:
                self.transitions[(tape_idx, current_state, read_symbol)] = [(new_state, write_symbol, move)]

    def set_initial_state(self, initial_state):
        self.current_state = initial_state

    def add_accept_state(self, state):
        self.accept_states.add(state)

    def step(self):
        i = 0   # head_position index
        chk = 0 # checker if all inputs are within the transition
        for tape in (self.tapes):
            # print(tape)
            current_symbol = tape[self.head_positions[i]]
            # print(current_symbol)
            key = (i, self.current_state, current_symbol)
            if key in self.transitions:
                chk+=1

            i += 1

        # print("check: ", chk)
        j = 0
        #if all tapes is in the transition, proceed to next state
        if chk == len(self.tapes):
            for tape in (self.tapes):
                current_symbol = tape[self.head_positions[j]]
                key = (j, self.current_state, current_symbol)
                for x in self.transitions[key]:
                    new_state, new_symbol, move = x 
                tape[self.head_positions[j]] = new_symbol
                if move == 'L':
                    self.head_positions[j] -= 1 # Move Left
                    if self.head_positions[j] < 0:
                        return "You can't go to left any further"
                elif move == 'R':
                    self.head_positions[j] += 1 # Move Right
                    if self.head_positions[j] >= len(tape):
                        tape.append('_')
                elif move == 'S':
                    self.head_positions[j] += 0 # Stationary
                j += 1
            self.current_state = new_state    
            return "Ongoing"
        else:
            return "No More Possible Transitions"

        # print(self.tapes)
        # print(self.head_positions)

    def run(self):
        while self.current_state not in self.accept_states:
            self.step()

    def is_accepted(self):
        return self.current_state in self.accept_states

    def display_current_configuration(self):
        i = 0
        for tape in (self.tapes):
            if self.head_positions[i] >= 0:
                head = self.head_positions[i]
                left_tape = "".join(tape[:head])
                right_tape = "".join(tape[head+1:])
                print(f"Tape {i + 1}: {left_tape}[{tape[head]}]{right_tape}")
            else: 
                 print(f"Tape {i + 1}: Dead")

            i += 1

        print(f"Current State: {self.current_state}\n")


def read_turing_machine_input(filename):
    with open(filename, 'r') as file:
        num_states = int(file.readline().strip())
        states = file.readline().strip().split()
        num_tapes = int(file.readline().strip())
        input_symbols = file.readline().strip().split()
        num_transitions = int(file.readline().strip())

        tm = MultiTapeTuringMachine()

        transitions_for_tapes = [[] for _ in range(num_tapes)]  # Initialize empty transition list for each tape

        for _ in range(num_transitions):
            transition_data = file.readline().strip().split('|')
            for tape_idx in range(num_tapes):
                if tape_idx < len(transition_data):
                    transitions = []
                    parts = transition_data[tape_idx].strip().split()
                    for i in range(0, len(parts), 5):
                        current_state, read_symbol, new_state, write_symbol, move = parts[i:i+5]
                        read_symbol = ' ' if read_symbol == '_' else read_symbol  # Convert _ to blank symbol
                        write_symbol = ' ' if write_symbol == '_' else write_symbol  # Convert _ to blank symbol
                        transitions.append((current_state, read_symbol, new_state, write_symbol, move))
                    transitions_for_tapes[tape_idx].extend(transitions)

        for tape_idx, transitions in enumerate(transitions_for_tapes):
            print(tape_idx, transitions)
            tm.add_transition_for_multi_tapes(tape_idx, transitions)

        initial_state = file.readline().strip()
        final_state = file.readline().strip()

        tm.set_initial_state(initial_state)
        tm.add_accept_state(final_state)


        for i in range(num_tapes):
            tape_input = input(f"Enter tape {i + 1} content: ")
            tm.add_tape(list(tape_input))

        return tm


if __name__ == "__main__":
    machine = "machine_def.txt"  # Replace with the actual filename

    tm = read_turing_machine_input(machine)
    
    print("Initial Configuration:")
    tm.display_current_configuration()

    state = "Ongoing"
    while tm.current_state not in tm.accept_states and state == "Ongoing":
        user_input = input("Press 'n' to execute the next transition: ")
        if user_input.lower() == 'n':
            state = tm.step()
            print(state)
            print("After Step:")
            tm.display_current_configuration()

    if tm.is_accepted():
        print("Accepted")
    else:
        print("Rejected")
