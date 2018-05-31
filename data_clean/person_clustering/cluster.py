# This script is cluster different class by scores which generate by different img comparison.
#run like:
#> python cluster.py /home/lthpc/data/NAS/NJJP/SRC/test/pair_dist.txt 80



import os, sys
import pandas as pd
import heapq
from itertools import chain

def cal_elem2elem_simi(df, elem1, elem2):
  return float(df.loc[df[(df[0] == elem1) & (df[1] == elem2)].index.tolist(), 2].item())


def cal_elem2set_simi(df, elem, set_data):
  sum_score = 0
  for data in set_data:
    sum_score += float(df.loc[df[(df[0] == elem) & (df[1] == data)].index.tolist(), 2].item())
  return sum_score / len(set_data)

def cal_set2set_simi(df, set_data1, set_data2):
  sum_score = 0
  for data1 in set_data1:
    for data2 in set_data2:
      sum_score += float(df.loc[df[(df[0] == data1) & (df[1] == data2)].index.tolist(), 2].item())
  return sum_score / (len(data1)*len(data2))


def switch_func(df, data1, data2):
  if isinstance(data1, str) and isinstance(data2, str):
    print("cal elem2elem ")
    return cal_elem2elem_simi(df, data1, data2)
  elif isinstance(data1, str) and isinstance(data2, list):
    print("cal elem2set ")
    return cal_elem2set_simi(df, data1, data2)
  elif isinstance(data1, list) and isinstance(data2, str):
    print("cal set2elem ")
    return cal_elem2set_simi(df, data2, data1)
  elif isinstance(data1, list) and isinstance(data2, list):
    print("cal set2set ")
    return cal_set2set_simi(df, data1, data2)
  else:
    print("data type error, switch func fail")
    return


def find_sec_most_simi(df, shell_list):
  score_list = []
  for data in shell_list:
    temp_score_list = []
    for data_ in shell_list:
      temp_score_list.append(switch_func(df, data, data_))
    score_list.append(temp_score_list)
  #find second largest simi and return
  second_max_score = heapq.nlargest(2, list(chain(*score_list)))[1]
  print("second_max_score:",second_max_score)
  for i in range(len(score_list)):
    for j in range(len(score_list)):
      if score_list[i][j] == second_max_score and i != j:
        return second_max_score, i, j
      else:
        print("error, havent find second largest score")
        return 



  
def merge_simi(shell_list, i, j):
  data1 = shell_list.pop(i)
  data2 = shell_list.pop(j)
  if isinstance(data1, str) and isinstance(data2, str):
    sub_list = [data1, data2]
    return shell_list.append(sub_list)
  elif isinstance(data1, str) and isinstance(data2, list):
    return shell_list.append(data2.append(data1))
  elif isinstance(data1, list) and isinstance(data2, str):
    return shell_list.append(data1.append(data2))
  elif isinstance(data1, list) and isinstance(data2, list):
    for data in data1:
      data2.append(data)
    return shell_list.append(data2)
  else:
    print("data type error")
    return



def cluster_by_score(df, threshod):
  shell_list = list(set(df[0]))
  while True:
    second_max_score, i, j = find_sec_most_simi(df, shell_list)
    shell_list = merge_simi(shell_list, i, j)
    if second_max_score < threshod:
      return shell_list
       

def read_file(data_path):
  pd.set_option('display.max_columns', 500)
  try:
    df = pd.read_table(data_path, encoding='gb2312', header=None, delim_whitespace=True)
    print("load ok")
    return df
  except:
    print(clean_data_path, "read faile")
    return

if __name__ == "__main__":
  data_path = sys.argv[1]
  threshod = float(sys.argv[2])
  df = read_file(data_path)
  result = cluster_by_score(df, threshod)
  print(result)



















