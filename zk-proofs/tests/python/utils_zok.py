import math
from utils import byte32_to_u32_array8
import re
import subprocess

def calculate_tree_root_zok(values):
    # for each value in values, convert it to a 32 byte array
    zokratesvalues = [byte32_to_u32_array8(value) for value in values]
    size = len(zokratesvalues)
    logsize = math.log(size, 2)
    # convert zokratesvalues to a string made by only the values separated by a space
    zokratesvalues = " ".join([" ".join(value) for value in zokratesvalues])
    bash_command = f"zokrates compute-witness -i ./zok_files/merkleTree/out --verbose -a {zokratesvalues}"
    result = subprocess.run(bash_command, shell=True, capture_output=True, text=True)
    # Get the output of the command (stdout)
    output = result.stdout
    # Extract the array from the stdout using regular expression
    match = re.search(r'\[.*\]', output)

    if match:
        array_str = match.group(0)
    else:
        raise ValueError("No array found in the stdout.")

    # Remove the double quotes from the array string and split it into individual numbers
    numbers_str = array_str.replace('"', '').replace('[','').replace(']','').split(',')

    return numbers_str
