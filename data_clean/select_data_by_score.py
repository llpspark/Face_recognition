#This script is select some identify imgs' folder where satisafy score threshod then copy it to new folder


#run like:
#> python select_data_by_score.py  /home/lthpc/data/NAS/NJJP/DATA/jower_repaired /home/lthpc/data/NAS/NJJP/DATA/unrar /home/lthpc/data/NAS/NJJP/DATA/check_data/ 50 56 15

import os, sys
import pandas as pd
import shutil


def count_num(list_data, score_thre_low, score_thre_hig):
  num = 0
  for i in list_data:
    if int(score_thre_low) < i < int(score_thre_hig):
      num += 1
  return num

def select_file(list_path, img_dir, dst_dir, score_thre_low, score_thre_hig, num_threshod):
  pd.set_option('display.max_colwidth', 500)
  try:
    df = pd.read_table(list_path, header = None, encoding = 'gb2312', delim_whitespace = True)
  except:
    print(list_path, "error")
    return
  if count_num(list(df[1]), score_thre_low, score_thre_hig) >= int(num_threshod):
    short_dir = list(df[0])[0].split("\\")[0] + "/" + list(df[0])[0].split("\\")[1]
    src_path = os.path.join(img_dir, short_dir)
    shutil.copytree(src_path, dst_dir)


def batch_select(list_dir, img_dir, dst_dir, score_thre_low, score_thre_hig, num_threshod):
  for file_name in os.listdir(list_dir):
    select_file(os.path.join(list_dir, file_name), img_dir, dst_dir + "/" + file_name.split(".")[0], score_thre_low, score_thre_hig, num_threshod)


    


if __name__ == "__main__":
  list_dir = sys.argv[1]
  img_dir = sys.argv[2]
  dst_dir = sys.argv[3]
  score_thre_low = sys.argv[4]
  score_thre_hig = sys.argv[5]
  num_threshod = sys.argv[6]
  batch_select(list_dir, img_dir, dst_dir, score_thre_low, score_thre_hig, num_threshod)
