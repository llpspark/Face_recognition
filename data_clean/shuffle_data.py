
# This script shuffle the input file 
#run like:
#> python shuffle_data.py "MerS.txt" "MerDt.txt"



import sys
import random

def shuffle_data(input1, output):
  with open(output, 'w') as f_o:
    with open(input1, 'r') as f_i:
      lines = f_i.readlines()
      random.shuffle(lines)
      for line in lines:
        f_o.write(line)


if __name__ == "__main__":
  input1 = sys.argv[1]
  output = sys.argv[2]
  shuffle_data(input1, output)

