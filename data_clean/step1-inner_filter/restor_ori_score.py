#This script is restore the score list to correct(some problems due to it) 

#run like:
#> python2 restor_ori_score.py "/home/lthpc/data/NAS/NJJP/DATA/score_list_300"
#> python2 restor_ori_score.py "/home/lthpc/data/NAS/NJJP/DATA/score_list_300" "/home/lthpc/data/NAS/NJJP/DATA/inner_filtered_img/stage1"
from __future__ import division
import os, sys
import shutil


posi_sum = 0
def get_num(root_path, file_name):
  with open(os.path.join(root_path, file_name), "r") as f_r1:
    count_sum = len(f_r1.readlines())
    f_r1.seek(0)
    for line in f_r1.readlines():
      if float(line.strip("\n").strip("\r").split(" ")[1]) > 0:
        global posi_sum
        posi_sum += 1
  return count_sum, posi_sum

  

def restore_origin(root_path):
  for root, dirs, files in os.walk(root_path):
    for file_name in files:
      global count_sum, posi_sum
      if file_name.endswith("txt"):
        # get count_sum and posi_sum
        count_sum, posi_sum = get_num(root, file_name)
        print(count_sum, posi_sum)
        # write the new value      
        with open(os.path.join(root, file_name + "_ori"), "w") as f_w:
          with open(os.path.join(root, file_name), "r") as f_r2:
            for line in f_r2.readlines():
              val = float(line.strip("\n").split(" ")[1]) 
              if val > 0:
                print(count_sum / posi_sum)
                f_w.write(line.strip("\n").split(" ")[0] + " " + str(count_sum / posi_sum * val) + "\n")
      posi_sum = 0


def merge_same_id(root_path, dst_dir):
  unique_list = []
  for root, dirs, files in os.walk(root_path):
    for file_name in files:
      print(root)
      if file_name.endswith("_ori") and file_name not in unique_list:
        unique_list.append(file_name)
        shutil.move(os.path.join(root,file_name), dst_dir)
      elif file_name.endswith("_ori") and file_name in unique_list:
        with open(os.path.join(dst_dir, file_name), "a") as f_w:
          with open(os.path.join(root, file_name), "r") as f_r:
            for line in f_r.readlines():
              f_w.write(line)
        os.remove(os.path.join(root, file_name))

        
def rename_file(files_dir):
  for file_name in os.listdir(files_dir):
    new_name = file_name.split("_")[0]
    shutil.move(os.path.join(files_dir, file_name), os.path.join(files_dir, new_name))



if __name__ == "__main__":
  root_path = sys.argv[1]
  dst_dir = sys.argv[2]
  #restore_origin(root_path)
  #merge_same_id(root_path, dst_dir)
  rename_file(dst_dir)

  print("ok")
  



