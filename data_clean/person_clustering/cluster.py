# This script is cluster different class by scores which generate by different img comparison.
#run like:
#> python cluster.py /home/lthpc/data/NAS/NJJP/SRC/test/pair_dist.txt 80



import os, sys
import pandas as pd
import heapq
from itertools import chain


def cal_set2set_simi(file_dict, set_data1, set_data2):
  print("cal_set2set_simi")
  sum_score = 0
  for data1 in set_data1:
    for data2 in set_data2:
      sum_score += file_dict[(data1, data2)]
  return sum_score / (len(data1)*len(data2))


def find_sec_most_simi(file_dict, shell_list):
  score_list = []
  for data in shell_list:
    temp_score_list = []
    for data_ in shell_list:
      temp_score_list.append(cal_set2set_simi(file_dict, data, data_))
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
  if isinstance(data1, list) and isinstance(data2, list):
    for data in data1:
      data2.append(data)
    return shell_list.append(data2)
  else:
    print("data type error")
    return



def cluster_by_score(file_dict, shell_list, threshod):
  while True:
    second_max_score, i, j = find_sec_most_simi(file_dict, shell_list)
    shell_list = merge_simi(shell_list, i, j)
    if second_max_score < threshod:
      return shell_list
       

def read_file(data_path):
  pd.set_option('display.max_columns', 500)
  try:
    df = pd.read_table(data_path, encoding='gb2312', header=None, delim_whitespace=True)
    shell_list = []
    for i in list(set(df[0])):
      temp_list = []
      temp_list.append(i)
      shell_list.append(temp_list)
    file_dict = {}
    for i, k in enumerate(zip(df[0], df[1])):
      file_dict[k] = list(df[2])[i]
    print("load ok")
    return file_dict, shell_list
  except:
    print(data_path, "read faile")
    return

if __name__ == "__main__":
  data_path = sys.argv[1]
  threshod = float(sys.argv[2])
  file_dict, shell_list = read_file(data_path)
  result = cluster_by_score(file_dict, shell_list, threshod)
  print(result)


