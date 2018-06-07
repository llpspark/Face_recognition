# This script is split noise data which inner-class score under 80, then copy them to new dir

#> run like:
#> python split_noise_data.py /home/lthpc/data/NAS/NJJP/DATA/repaired_score_list /home/lthpc/data/NAS/NJJP/DATA/inner_filtered_score_list/stage1/JPV1.txt /home/lthpc/data/NAS/NJJP/DATA/repaired_score_list /home/lthpc/data/NAS/NJJP/DATA/unrar /home/lthpc/data/NAS/NJJP/DATA/filtered_noise/stage1

import os,sys
import shutil
import pandas as pd

def split_data(full_list_dir, clean_data_path):
  full_list = [txt_file.split(".")[0] for txt_file in os.listdir(full_list_dir) if txt_file.endswith("txt")]
  pd.set_option('display.max_columns', 500)
  try:
    df = pd.read_table(clean_data_path, encoding='gb2312', header=None, delim_whitespace=True)
    print("load ok")
  except:
    print(clean_data_path, "read faile")
    return

  clean_file = list(set(df[1]))
  for i in range(len(clean_file)):
    clean_file[i] = str(clean_file[i])
  noise_files = [file_name + ".txt" for file_name in full_list if file_name not in clean_file] 
  print("noise_files", len(noise_files))
  return noise_files

def copy_noise_to(noise_files_dir, noise_files, img_root_dir, dst_dir):
  for noise_file in noise_files:
    with open(os.path.join(noise_files_dir, noise_file), 'r', encoding="ISO-8859-1") as f_r:
      date_folder = []
      for line in f_r.readlines():
        line_date = line.split(' ')[0].split('\\')[5]
        if line_date not in date_folder:
          date_folder.append(line_date)
          print(date_folder)
      if not os.path.exists(os.path.join(dst_dir, noise_file.split('.')[0])):
        os.mkdir(os.path.join(dst_dir, noise_file.split('.')[0]))
      for date_name in date_folder:
        for file_name in os.listdir(os.path.join(os.path.join(img_root_dir, date_name), noise_file.split('.')[0])):
            shutil.copyfile(os.path.join(os.path.join(img_root_dir, date_name), noise_file.split('.')[0] + "/" + file_name), os.path.join(dst_dir, noise_file.split('.')[0] + "/" + file_name))


if __name__ == "__main__":
  full_list_dir = sys.argv[1]
  clean_data_path = sys.argv[2]
  noise_files_dir = sys.argv[3]
  img_root_dir = sys.argv[4]
  dst_dir = sys.argv[5]
  noise_files = split_data(full_list_dir, clean_data_path)
  copy_noise_to(noise_files_dir, noise_files, img_root_dir, dst_dir)
  print("ok")
