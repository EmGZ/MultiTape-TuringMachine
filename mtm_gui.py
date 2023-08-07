import tkinter as tk
from tkinter import scrolledtext

class MultiTapeTuringMachine:
    def __init__(self):
        self.num_tapes = 0
        self.num_transitions = 0
        self.tapes = []
        self.head_positions = []
        self.initial_state = None
        self.current_state = None
        self.transitions = []
        self.accept_states = set()

    def initialize_transitions(self, transitions, tapes):
        self.transitions = [[0] * transitions for _ in range(tapes)]

    def set_num_tapes(self, num_tapes):
        self.num_tapes = num_tapes

    def set_num_transitions(self, num_transitions):
        self.num_transitions = num_transitions

    def add_tape(self, tape):
        self.tapes.append(tape)
        self.head_positions.append(0)
    
    def add_transition_for_multi_tapes(self, tape_idx, transitions):
        transition_num = 0
        for transition in transitions:
            current_state, read_symbol, new_state, write_symbol, move = transition
            self.transitions[tape_idx][transition_num] = (current_state, read_symbol, new_state, write_symbol, move)
            # print(f"[{tape_idx}][{transition_num}]: ", self.transitions[tape_idx][transition_num])
            transition_num += 1

    def set_initial_state(self, initial_state):
        self.current_state = initial_state
        self.initial_state = initial_state

    def add_accept_state(self, state):
        self.accept_states.add(state)

    def step(self):
        i = 0   # head_position index
        highest_count = 0 # checker for transitions
        acc_trans = [] # Container for the transitions indices that are accepted
        for tape in (self.tapes):
            # print(tape)
            current_symbol = tape[self.head_positions[i]]
            # print(current_symbol)
            key = (self.current_state, current_symbol)
            for idx, transition in enumerate(self.transitions[i]):
                # print("trans: ", transition[:2])
                # print(idx)
                if transition[:2] == key:
                    acc_trans.append(idx)
                    # print(idx)

            i += 1
        
        if acc_trans:
            transition_count = {}  # Create a dictionary to store counts for each transition index
            for idx in acc_trans:
                transition_count[idx] = transition_count.get(idx, 0) + 1

            most_common_idx = max(transition_count, key=transition_count.get)
            highest_count = transition_count[most_common_idx]

        # print("Highest Count: ", highest_count)
        # print("Most Common: ", most_common_idx)

        # print("check: ", chk)
        j = 0
        #if all tapes is in the transition, proceed to next state
        if highest_count == len(self.tapes):
            for tape in (self.tapes):
                a, b, new_state, new_symbol, move = self.transitions[j][most_common_idx] 
                tape[self.head_positions[j]] = new_symbol
                if move == 'L':
                    self.head_positions[j] -= 1 # Move Left
                    if self.head_positions[j] < 0:
                        tape.insert(0, '_')
                        self.head_positions[j] = 0       
                elif move == 'R':
                    self.head_positions[j] += 1 # Move Right
                    if self.head_positions[j] >= len(tape):
                        tape.append('_')
                elif move == 'S':
                    self.head_positions[j] += 0 # Stationary
                j += 1
                # print(tape)
            # print(self.head_positions)
            self.current_state = new_state    
            return "Ongoing"
        else:
            return "No More Possible Transitions"

        # print(self.tapes)

    def is_accepted(self):
        return self.current_state in self.accept_states


def read_turing_machine_input(filename):
    with open(filename, 'r') as file:
        num_states = int(file.readline().strip())
        states = file.readline().strip().split()
        num_tapes = int(file.readline().strip())
        input_symbols = file.readline().strip().split()
        num_transitions = int(file.readline().strip())

        tm = MultiTapeTuringMachine()

        transitions_for_tapes = [[] for _ in range(num_tapes)]  # Initialize empty transition list for each tape
        tm.initialize_transitions(num_transitions, num_tapes)

        for _ in range(num_transitions):
            transition_data = file.readline().strip().split('|')
            for tape_idx in range(num_tapes):
                if tape_idx < len(transition_data):
                    transitions = []
                    parts = transition_data[tape_idx].strip().split()
                    for i in range(0, len(parts), 5):
                        current_state, read_symbol, new_state, write_symbol, move = parts[i:i+5]
                        transitions.append((current_state, read_symbol, new_state, write_symbol, move))
                    transitions_for_tapes[tape_idx].extend(transitions)

        for tape_idx, transitions in enumerate(transitions_for_tapes):
            # print(tape_idx, transitions)
            tm.add_transition_for_multi_tapes(tape_idx, transitions)
        
        # print(tm.transitions)
        initial_state = file.readline().strip()
        final_state = file.readline().strip()

        tm.set_num_tapes(num_tapes)
        tm.set_num_transitions(num_transitions)
        tm.set_initial_state(initial_state)
        tm.add_accept_state(final_state)

        return tm
    

class TuringMachineGUI(tk.Tk):
    def __init__(self, tm):
        super().__init__()
        self.title("Multi-Tape Turing Machine Simulator")
        self.tm = tm
        self.create_widgets()

    def create_widgets(self):
        self.tape_entries = []
        for i in range(self.tm.num_tapes):
            tape_label = tk.Label(self, text=f"Tape {i+1} Content:")
            tape_label.grid(row=i, column=0)
            tape_entry = tk.Entry(self)
            tape_entry.grid(row=i, column=1)
            self.tape_entries.append(tape_entry)
            self.tm.add_tape(tape_entry)

        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.grid(row=self.tm.num_tapes, column=0, columnspan=2)

        self.step_button = tk.Button(self, text="Step", command=self.on_step)
        self.step_button.grid(row=self.tm.num_tapes + 1, column=0, columnspan=2)
        self.step_button.config(state=tk.DISABLED)

        self.reset_button = tk.Button(self, text="New Input", command=self.reset)
        self.reset_button.grid(row=self.tm.num_tapes + 2, column=0, columnspan=2)
        self.reset_button.config(state=tk.DISABLED)

        self.output_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=90, height=30)
        self.output_text.grid(row=self.tm.num_tapes + 3, column=0, columnspan=2)

        self.step_count = 0

    def start(self):
        for i in range(len(self.tm.tapes)):
                tape_content = self.tape_entries[i].get()
                if not tape_content.strip():  # Check if the input is empty or contains only whitespaces
                    self.tm.tapes[i] = ['_']  # Fill the tape with '_' if the input is null
                else:
                    self.tm.tapes[i] = list(tape_content)
                self.tape_entries[i].config(state=tk.DISABLED) # Disable the tape once it starts
        self.output_text.insert(tk.END, "Starting: \n")
        self.display_current_configuration()
        self.step_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

    def on_step(self):
        self.step_count += 1
        state = self.tm.step()
        self.output_text.insert(tk.END, f"Step {self.step_count}: \n")
        self.display_current_configuration()

        if self.tm.is_accepted():
            self.output_text.insert(tk.END, "Accepted\n")
            self.step_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)
        elif state == "No More Possible Transitions" or state == "You can't go to left any further":
            self.output_text.insert(tk.END, f"{state}\n")
            self.output_text.insert(tk.END, "Rejected\n")
            self.step_button.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)


    def display_current_configuration(self):
        self.output_text.insert(tk.END, "Current Configuration:\n")
        for i, tape in enumerate(self.tm.tapes):
            if self.tm.head_positions[i] >= 0:
                head = self.tm.head_positions[i]
                left_tape = "".join(tape[:head])
                right_tape = "".join(tape[head + 1:])
                self.output_text.insert(tk.END, f"Tape {i + 1}: {left_tape}[{tape[head]}]{right_tape}\n")
            else:
                self.output_text.insert(tk.END, f"Tape {i + 1}: Dead\n")
        self.output_text.insert(tk.END, f"Current State: {self.tm.current_state}\n\n")
    
    def reset(self):
        self.tm.head_positions = [0] * len(self.tm.tapes)
        self.tm.current_state = self.tm.initial_state
        self.step_count = 0
        self.step_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        self.output_text.delete(1.0, tk.END)
        # Clear all input entries
        for tape_entry in self.tape_entries:
            tape_entry.config(state=tk.NORMAL)
            tape_entry.delete(0, tk.END)


def main():
    machine = "machine_def.txt"  # Replace with the actual filename

    tm = read_turing_machine_input(machine)

    app = TuringMachineGUI(tm)
    app.mainloop()


if __name__ == "__main__":
    main()
