#This script is compute the score distribution of all data and plot it to visiblization

# rum like:
#> python plot_score_distribute.py "/home/lthpc/data/NAS/NJJP/DATA/jower_repaired"


import os, sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def statistics(src_file):
  pd.set_option('display.max_colwidth', 500)
  try:
    df = pd.read_table(src_file, header = None, encoding = 'gb2312', delim_whitespace = True)
  except:
    print(src_file, "error")
    return
  score_list = list(df[1].astype(int))  
  return score_list

def flatten_list(nested_list):
  res_list = []
  for item in nested_list:
    for i in item:
      res_list.append(i)
  return res_list


def show_percent(dit_data):
  dit_new = {}
  total_sum = sum(dit_data.values())
  print("total_sum",total_sum)
  for key in dit_data.keys():
    dit_new[key] = dit_data[key] / total_sum
  return dit_new

def show_edge_percent(dit_data):
  dit_edge = {}
  total_sum = sum(dit_data.values())
  print("total_sum", total_sum)
  temp_sum = 0
  for key in dit_data.keys():
    dit_edge[key] = dit_data[key] / total_sum + temp_sum
    temp_sum += dit_data[key] / total_sum
  return dit_edge


def list_len(root_dir, file_name):
  return os.path.getsize(os.path.join(root_dir, file_name))
  

def get_statistics(root_path):
  score_lists = []

  for root_path, dirs, files in os.walk(root_path):
    for file_name in files:
      if file_name.endswith("txt") and list_len(root_path, file_name) > 0:
        print(file_name)
        score_lists.append(statistics(os.path.join(root_path, file_name)))
  total_list = flatten_list(score_lists)
  total_dit = {k : total_list.count(k)for k in set(total_list) if int(k) > 0}
  percent_dit = show_edge_percent(total_dit)
  return total_dit, percent_dit

def figure_show(percent_dit):
  x = list(percent_dit.keys())
  y = list(percent_dit.values())
  fig = plt.figure()
  ax1 = fig.add_subplot(111)
  #ax1.plot(x, y)
  plt.savefig("percent.jpg")


if __name__ == "__main__":
  file_path = sys.argv[1]
  res, res_percent = get_statistics(file_path)
  #figure_show(res_percent)
  print(res, "\n")
  print(res_percent)
  print("ok")
