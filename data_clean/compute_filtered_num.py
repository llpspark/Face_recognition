#This script is compute all the number of identify and imgs respectively.

# run like:
#> python compute_filtered_num.py "/home/lthpc/data/JiaPei/score_list_300/"

import os,sys

num_imgs = 0
num_identify = 0
def compute_list_num(root_path):
  global num_imgs
  global num_identify
  for root, dirs, files in  os.walk(root_path):
    for file_name in files:
      if file_name.endswith("filter"):
        with open(os.path.join(root, file_name), "r") as f_r:
          if len(f_r.readlines()) > 0:
            num_identify += 1
          f_r.seek(0)
          num_imgs += len(f_r.readlines())

if __name__ == "__main__":
  root_path = sys.argv[1]
  compute_list_num(root_path)
  print("num_imgs:", num_imgs)
  print("num_identity:", num_identify)
  print("ok")
