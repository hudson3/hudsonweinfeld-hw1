'''
This file contains a template for the first homework assignment for Theory of Computation Fall 2025, Tulane University
'''
from collections import defaultdict
import copy
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import time

def compose(f1,f2):
    '''Assumes that f1 and f2 are dictionaries that represent functions.
    Returns a dictionary whose keys are those of f1 and that represents the composition of f1 and f2.'''
    return {key:f2[f1[key]] for key in f1}


class state_machine(object):
    
    def __init__(self, transitions, initial_state, accept_states):
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        # alphabet is already stored in transitions
        self.alphabet = list(transitions.keys())
        
    def get_next_state(self, current_state, input_letter):
        trans_from_letter = self.transitions[input_letter]
        return trans_from_letter[current_state]

    #Operations on machines
    def iterative_match(self, input_string):
        '''Assumes that the string is a string in the alphabet.
        Returns True or False, depending on whether or not the input_string is accepted.
        '''
        current_state = self.initial_state

        for letter in input_string:
            current_state = self.get_next_state(current_state, letter)

        return current_state in self.accept_states
    def complement(self):
        '''Returns the complement machine, that accepts the strings that the original machine does not accept'''
        # collect all states from transitions
        all_states = set()
        for letter in self.alphabet:
            all_states.update(self.transitions[letter].keys())

        new_accepts = [s for s in all_states if s not in self.accept_states]

        return state_machine(self.transitions, self.initial_state, new_accepts)


    def intersection(self,other):
        '''other is assumed to be a machine with the same alphabet.
        returns a machine that accepts when both self and other accept.'''

        transitions = {}
        for letter in self.alphabet:
            transitions[letter] = {}
            for s1 in self.transitions[letter]:
                for s2 in other.transitions[letter]:
                    current_state = (s1, s2)
                    next_state = (self.transitions[letter][s1],
                                other.transitions[letter][s2])
                    transitions[letter][current_state] = next_state

        initial_state = (self.initial_state, other.initial_state)

        accept_states = [
            (s1, s2)
            for s1 in self.transitions[self.alphabet[0]].keys()
            for s2 in other.transitions[self.alphabet[0]].keys()
            if s1 in self.accept_states and s2 in other.accept_states
        ]

        return state_machine(transitions, initial_state, accept_states)
    
    @classmethod
    def init_from_partial_def(cls,transitions,initial,accept_states):
        '''
        Assumes transitions is a dictionary of dictionaries. The keys of the outer dictionaries all of the letters of the alphabet.
            Each value of transitions is a dictionary, whose keys and values are (not necessarily all) of the states (strings) of the machine.
            initial is the initial state (a string).
            accept_states is a list of states that are accepted. Each state in accept state is assumed to have been mentioned in the transitions dictionary somewhere.

        See state_machines_examples_template.py for examples.
        '''
        return cls(transitions, initial, accept_states)    
