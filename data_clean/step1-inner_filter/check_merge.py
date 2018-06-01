# run like :
#> python check_merge.py /home/lthpc/data/NAS/NJJP/DATA/jower_repaired

import os, sys

def check_file(root_path):
  len1 = len(os.listdir(root_path))
  len2 = len(set(os.listdir(root_path)))
  print(len1, len2)

if __name__ == "__main__":
  root_path = sys.argv[1]
  check_file(root_path)
  print("ok")
