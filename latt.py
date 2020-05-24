import math
from sys import argv
import os

values = [0]
slots = [0] * 4
current_slot = 0
loop_stack = []
pointer = 0
flag = 0
pc = 0 # Program counter
program_output = ""
finished = False


def increment_pointer():
    global pointer, values
    pointer += 1
    if(len(values)-1 < pointer):
        values.append(0)


def decrement_pointer():
    global pointer
    if(pointer <= 0):
        print("WARNING: Tried to decrement pointer past 0")
    else:
        pointer -= 1


def clear():
    global pointer, values
    values[pointer] = 0


def increment():
    global pointer, values
    values[pointer] += 1


def decrement():
    global pointer, values
    values[pointer] -= 1


def start_loop():
    global loop_stack
    loop_stack.append(pc-1)


def end_loop():
    global loop_stack, pc
    if(len(loop_stack) <= 0):
        print("ERROR: LEnd doesn't have an LStart!")
        exit(4)

    if(flag == 0):
        pc = loop_stack.pop()


def compare_iszero():
    global flag, pointer, values
    flag = 1 if values[pointer] == 0 else 0


def compare_isequal():
    global flag, pointer, values, slots, current_slot
    flag = 1 if values[pointer] == slots[current_slot] else 0


def compare_isnotequal():
    global flag, pointer, values, slots, current_slot
    flag = 1 if values[pointer] != slots[current_slot] else 0


def compare_isgreater():
    global flag, pointer, values, slots, current_slot
    flag = 1 if values[pointer] > slots[current_slot] else 0


def compare_islesser():
    global flag, pointer, values, slots, current_slot
    flag = 1 if values[pointer] < slots[current_slot] else 0


def compare_iszero():
    global flag, pointer, values
    flag = 1 if values[pointer] == 0 else 0


def set_slot0():
    global current_slot
    current_slot = 0


def set_slot1():
    global current_slot
    current_slot = 1


def set_slot2():
    global current_slot
    current_slot = 2


def set_slot3():
    global current_slot
    current_slot = 3


def load_to_slot():
    global current_slot, slots, pointer, values
    slots[current_slot] = values[pointer]


def put_from_slot():
    global current_slot, slots, pointer, values
    values[pointer] = slots[current_slot]


def clear_slot():
    global current_slot, slots
    slots[current_slot] = 0


def quick_load():
    global current_slot, slots, values
    if(len(values) > 0):
        slots[current_slot] = values[0]


def print_character():
    global pointer, values, program_output
    program_output += chr(values[pointer])


def return_code():
    global pointer, values, finished
    print(f"Program end (exit code {values[pointer]})")
    finished = True


def print_debug():
    global pointer, values, current_slot, slots, pc
    print(f"[DEBUG] PC={pc}")
    print(f"[DEBUG] values={values}, pointer={pointer}")
    print(f"[DEBUG] slots={slots}, current slot={current_slot}")


def no_op():
    pass


mnemonic_indices = {
    'CLEAR':     0, # (not useful, remove?)
    'INC':       1,
    'RET':       2,
    'DEC':       3,
    '???':       4, # unused
    'PINC':      5,
    'PDEC':      6,
    'LOAD':      7,
    'PUT':       8,
    'CLSLOT':    9, # (not useful, remove?)
    'QLOAD':    10, # (not useful, remove?)
    'ISZERO':   11,
    'LSTART':   12,
    'ISEQU':    13,
    'ISNEQ':    14,
    'ISGRE':    15,
    'ISLES':    16,
    'SLOT0':    17,
    'SLOT1':    18,
    'SLOT2':    19,
    'SLOT3':    20,
    'OUT':      21,
    'NOOP':     22,
    'LEND':     23
}


mnemonic_map = {
    'CLEAR':        clear,
    'INC':          increment,
    'DEC':          decrement,
    'PINC':         increment_pointer,
    'PDEC':         decrement_pointer,

    'LSTART':       start_loop,
    'LEND':         end_loop,

    'SLOT0':        set_slot0,
    'SLOT1':        set_slot1,
    'SLOT2':        set_slot2,
    'SLOT3':        set_slot3,
    'LOAD':         load_to_slot,
    'PUT':          put_from_slot,
    'CLSLOT':       clear_slot,
    'QLOAD':        quick_load,

    'ISEQU':        compare_isequal,
    'ISNEQ':        compare_isnotequal,
    'ISGRE':        compare_isgreater,
    'ISLES':        compare_islesser,
    'ISZERO':       compare_iszero,

    'OUT':          print_character,
    'RET':          return_code,
    'NOOP':         no_op,
    'PRINTDEBUG':   print_debug 
}


if(len(argv) < 2):
    print("No file selected")
    exit(1)

bytecode = []

f = open(argv[1], 'r')
lines = f.read().splitlines()
while not finished:
    l = lines[pc]
    if(l.startswith('#') or l == ""): # Skip comments and whitespace
        pc += 1
        continue
    
    mnemonic = l.lstrip().split(' ')

    if(mnemonic[0] not in mnemonic_map):
        print(f"ERROR: Undefined mnemonic '{mnemonic[0]}'")
        exit(4)
    
    if(len(mnemonic) > 2 and mnemonic[1] == '*'):
        for i in range(int(mnemonic[2])):
            mnemonic_map[mnemonic[0]]()
    else:
        mnemonic_map[mnemonic[0]]()
    pc += 1

for l in lines:
    if(l.startswith('#') or l == ""): # Skip whitespace
        continue
    
    mnemonic = l.lstrip().split(' ')
    if(mnemonic[0] == "PRINTDEBUG"):
        continue

    if(len(mnemonic) > 2 and mnemonic[1] == '*'):
        for i in range(int(mnemonic[2])):
            bytecode.append(mnemonic_indices[mnemonic[0]])
    else:
        bytecode.append(mnemonic_indices[mnemonic[0]])

# print(f"Program code: {bytecode} ({len(bytecode)} instructions, {len(bytecode) * 5} bits (or {math.ceil((len(bytecode) * 5) / 8)} bytes)")
print(f"Program output: '{program_output}'")

output_filename = os.path.splitext(os.path.basename(argv[1]))[0] + '.rlatt'
open(output_filename, 'wb').write(bytes(bytecode))
print(f"Bytecode written to {output_filename}")