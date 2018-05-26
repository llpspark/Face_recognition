#This script is redirect the label form number 0
# run this script like :
#> python change_label.py "/home/lthpc/data/ShanDa-2/result.txt" "/home/lthpc/data/ShanDa-2/sorted_result.txt" "/home/lthpc/data/ShanDa-2/new_result.txt"

import sys

def resort_file(input_dir, resorted_file):
  """
  This function is resort input file

  @parameter input_dir：input file which will deal with
  @parameter resorted_file: resorted result file
  """
  with open(resorted_file, 'w') as f_w:
    with open(input_dir, 'r') as f_r:
      order = f_r.readlines()
      new_order = sorted(order, key = lambda line: line.strip("\n").split(" ")[1])
      for i in new_order:
        f_w.write(i)


def redirect_label(file_dir, output_dir):
  """
  This function is redirect label from number "0"
  @parameter file_dir: this is sorted file
  @parameter output_dir: this is final result fie dir

  """
  new_label = 0
  with open(output_dir, 'w') as f_w:
    with open(file_dir, 'r') as f_r:
      lines = f_r.readlines()
      img_path = lines[0].strip("\n").split(" ")[0]
      pre_label = lines[0].strip("\n").split(" ")[1]
      f_w.write(img_path + " " + str(new_label) + "\n")
      length = len(lines)
      for i in range(1, length):
        line_sp = lines[i].strip("\n").split(" ")
        img_path, label = line_sp[0], line_sp[1]
        if label != pre_label:
          new_label = new_label + 1
          pre_label = label
        f_w.write(img_path + " " + str(new_label) + "\n")


if __name__ == "__main__":
  input_dir = sys.argv[1]
  resorted_file = sys.argv[2]
  output_dir = sys.argv[3]
  resort_file(input_dir, resorted_file)
  redirect_label(resorted_file, output_dir)
