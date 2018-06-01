
#This script is redirect the input2's label and then merge input2 to input1, finnaly generate the new output
# run like:
#> python merge_data.py "train.txt" "SD.txt"  "output.txt" 85164
#> python merge_data.py "MS_SD_BK.txt" "JP.txt"  "output.txt" -1
#> python merge_data.py "SD.txt" "JP.txt"  "output.txt" -85165
import sys
def merge(input1, input2, cls_num, output):
  with open(output, 'w') as f_o:
    with open(input2, 'r') as f_i2:
      for line in f_i2.readlines():
        pre, pos = line.strip("\n").split(" ")
        f_o.write(pre + " " + str(int(pos) + int(cls_num)) + "\n")
        print(pre + " " + str(int(pos) + int(cls_num)))
    with open(input1, 'r') as f_i1:
      for line in f_i1.readlines():
        f_o.write(line)


if __name__ == "__main__":
  input1 = sys.argv[1]
  input2 = sys.argv[2]
  output = sys.argv[3]
  cls_num = sys.argv[4]
  merge(input1, input2, cls_num, output)
