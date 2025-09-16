#This file contains examples of finite state machines.
from state_machine_template import *
import random

def basic_example_state_machine():
    '''A first example provided about how to use init_from_partial_def
    '''
    return state_machine.init_from_partial_def({'1':{'zero':'one','one':'zero'}, '0':{'zero':'zero'}},'zero',['zero','one'])
def exercise_221():
    r'''This example is provided for you. See Hopcroft and Ullman Exercise 2.2.1
    We label the states by three letters of d's (for diagonal) and a's, then L or R, depending on whether the marble exits at C or D
    For example, the state 'dad' corresponds to x_1= diagonal, ie. / , x_2=antidiagonal ie. \)'''
    transitions= {'A':{'dddL':'addL',
                       'ddaL':'adaL',
                       'dadL':'aadL',
                       'daaL':'aaaL',
                       'addL':'dadL',
                       'adaL':'daaL',
                       'aadL':'dddR',
                       'aaaL':'ddaR',
                       'dddR':'addL',
                       'ddaR':'adaL',
                       'dadR':'aadL',
                       'daaR':'aaaL',
                       'addR':'dadL',
                       'adaR':'daaL',
                       'aadR':'dddR',
                       'aaaR':'ddaR'},
                    'B':{'dddL':'daaL',
                         'ddaL':'dddR',
                         'dadL':'ddaR',
                         'daaL':'dadR',
                         'addL':'aaaL',
                         'adaL':'addR',
                         'aadL':'addR',
                         'aaaL':'aadR',
                         'dddR':'daaL',
                         'ddaR':'dddR',
                         'dadR':'ddaR',
                         'daaR':'dadR',
                         'addR':'aaaL',
                         'adaR':'addR',
                         'aadR':'addR',
                         'aaaR':'aadR'}}
    return state_machine.init_from_partial_def(transitions, 'dddL', [state for state in transitions['A'] if state[-1]=='R' ])

def implication_machine():
    '''
    Accepts if ((s1->s2)->s3)->... evaluates to True
    '''
    transitions = {
        'T':{'no_prev': 'prev_T',
             'prev_T':'prev_T',
             'prev_F':'prev_T'},
        'F':{'no_prev':'prev_F',
             'prev_T':'prev_F',
             'prev_F':'prev_T'}
    }
    return state_machine.init_from_partial_def(transitions, 'no_prev',['prev_T'])

def letter_counting_machine(multiple_dict={'0':2, '1':3}):
    '''Assumes that mulitple_dict is a dictionary whose keys are the letters
    The values are positive integers.
    The machine accepts iff letter appears a multiple of multiple_dict[letter] many times.'''

    '''creating list of states using mixed radix number system counter from left to right
    mixed radix number system because each letter has its own multiple
    for example multiple_dict={'0':2, '1':3} 0 is binary and 3 is ternary 
    for letter, mult in multiple_dict.items():
        if not states:
            for mult_num in range(mult):
                new_string = "(" + str(mult_num)
                for mult_dict_letter in range(len(multiple_dict)):
                    new_string += ", 0"
                new_string += ")"
                states.append(new_string)
        else:
            for state in states:
                for mult_num in range(mult):
                    keys = list(multiple_dict.keys())

                    halfs = state.split(",", keys.index(letter) + 1)
                    first_half = ",".join(halfs[:keys.index(letter) + 1]) + ","


                    second_half = ""
                    if keys.index(letter) == len(keys) - 1:
                        second_half = ")"
                    else:
                        halfs = state.split(",", keys.index(letter) + 2)
                        second_half = " ," + halfs[keys.index(letter) + 2]

                    new_string = first_half + str(mult_num) + second_half

                    states.append(new_string)'''
            
    # 1. creating the states
    # generate all possible state combinations
    state_ranges = [range(mult) for mult in multiple_dict.values()]
    all_state_tuples = list(itertools.product(*state_ranges))
    # convert to string
    states = [str(state_tuple) for state_tuple in all_state_tuples]

    # 2. creating the transitions
    transitions = {}
    letters = list(multiple_dict.keys())
    for letter in letters:
        transitions[letter] = {}
        letter_index = letters.index(letter)
        
        for state_tuple in all_state_tuples:
            current_state = str(state_tuple)
            # create new state by incrementing the count for this letter
            new_counts = list(state_tuple)
            new_counts[letter_index] = (new_counts[letter_index] + 1) % multiple_dict[letter]
            next_state = str(tuple(new_counts))
            transitions[letter][current_state] = next_state

    # 3. creating the initial state
    initial_state = str(tuple([0] * len(letters)))

    # 4. creating the accept state
    accept_states = [initial_state]

    # 5. put together to make final state machine
    return state_machine(transitions, initial_state, accept_states)
    
def divisibility_machine(b,k):
    '''Returns a machine that accepts the strings of base-b that are divisible by k.
    Assumes b is between 2 and 10, k is between 2 and 20.
    The strings are read as usual with the most significant digit first from left-to-right, big endian style.
    '''

    # alphabet: digits 0 to b-1
    alphabet = [str(d) for d in range(b)]

    # states: remainders s
    states = [str(r) for r in range(k)]

    # transitions
    transitions = {}
    for digit in alphabet:
        d = int(digit)
        transitions[digit] = {}
        for r in range(k):
            new_r = (r * b + d) % k
            transitions[digit][str(r)] = str(new_r)

    initial_state = '0'
    accept_states = ['0']

    return state_machine(transitions, initial_state, accept_states)
    
def implication_machine():
    transitions = {
        'T':{'no_prev': 'prev_T',
             'prev_T':'prev_T',
             'prev_F':'prev_T'},
        'F':{'no_prev':'prev_F',
             'prev_T':'prev_F',
             'prev_F':'prev_T'}
    }
    return state_machine.init_from_partial_def(transitions, 'no_prev',['prev_T'])
