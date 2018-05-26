# This script is merge lists to one file and add lable.

#run like:
#> python merge_list.py /home/lthpc/data/NAS/NJJP/DATA/inner_filtered_score_list/stage1 /home/lthpc/data/NAS/NJJP/DATA/inner_filtered_score_list/stage1/train_list.txt /home/lthpc/data/NAS/NJJP/DATA/inner_filtered_score_list/new_train_list.txt

import os, sys

def merge_list(root_dir, output_path):
  with open(output_path, "w") as f_w:
    for root, dirs, files in os.walk(root_dir):
      for file_name in files:
        if file_name.endswith("filter") and os.path.getsize(os.path.join(root, file_name)) > 0:
          with open(os.path.join(root, file_name), "r") as f_r:
            for line in f_r.readlines():
              f_w.write(line)

def add_label(src_path, dst_path):
  with open(dst_path, "w") as f_w:
    with open(src_path, "r") as f_r:
      for line in f_r.readlines():
        label = line.split(" ")[0].split("/")[1]
        f_w.write(line.split(" ")[0] + ".jpg" + " " + label + "\n")


if __name__ == "__main__":
  root_dir = sys.argv[1]
  output_path = sys.argv[2]
  output_new_path = sys.argv[3]
  #merge_list(root_dir, output_path)
  add_label(output_path, output_new_path)
  print("ok")
