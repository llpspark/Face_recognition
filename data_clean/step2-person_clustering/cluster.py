# This script is cluster different class by scores which generate by different img comparison.
#run like:
#> python cluster_v3.py /home/lthpc/data/NAS/NJJP/SRC/test/pair_dist.txt 80 /home/lthpc/data/NAS/NJJP/DATA/unrar/201604/140001223068 ./test/res



import os, sys
import pandas as pd
import heapq
from itertools import chain
import shutil


def cal_set2set_simi(file_dict, set_data1, set_data2):
  sum_score = 0
  for data1 in set_data1:
    for data2 in set_data2:
      sum_score += file_dict[(data1, data2)]
  return sum_score / (len(set_data1)*len(set_data2))


#def find_sec_most_simi(file_dict, shell_list):
#  score_list = []
#  for data in shell_list:
#    temp_score_list = []
#    for data_ in shell_list:
#      temp_score_list.append(cal_set2set_simi(file_dict, data, data_))
#    score_list.append(temp_score_list)
#  #find second largest simi and return
#  second_max_score = heapq.nlargest(2, list(chain(*score_list)))[1]
#  print("second_max_score:",second_max_score)
#  for i in range(len(score_list)):
#    for j in range(len(score_list)):
#      if score_list[i][j] == second_max_score and i != j:
#        return second_max_score, i, j
#      else:
#        print("error, havent find second largest score")
#        return 
#

def find_sec_most_simi(file_dict,shell_list):
  tmp_max = 0
  index_i = None
  index_j = None
  for i in range(len(shell_list)-1):
    for j in range(i+1,len(shell_list)):
      tmp = cal_set2set_simi(file_dict,shell_list[i],shell_list[j])
      if tmp > tmp_max:
        tmp_max = tmp
        index_i = shell_list[i]
        index_j = shell_list[j]

  print('-' * 30)
  #print(shell_list[i], shell_list[j])
  #print(index_i, index_j)
  return tmp_max, index_i, index_j

def merge_simi(shell_list, index_i, index_j):
  shell_list.remove(index_i)
  shell_list.remove(index_j)
  if isinstance(index_i, list) and isinstance(index_j, list):
    for data in index_i:
      index_j.append(data)
    shell_list.append(index_j)
    return shell_list
  else:
    print("data type error")
    return



def cluster_by_score(file_dict, shell_list, threshod):
  while True:
    second_max_score, index_i, index_j = find_sec_most_simi(file_dict, shell_list)
    shell_list = merge_simi(shell_list, index_i, index_j)
    print('shell_list lenth:', len(shell_list))
    if second_max_score < threshod or len(shell_list)==1:
      return shell_list
       

def read_file(data_path):
  ret = dict()
  shell_list = []
  #count = 0
  with open(data_path,'r') as fid:
    for lines  in fid:
      #if(count % 1000)==0:
        #print('processing to  {0}....'.format(count))
      #count += 1
      words = lines.strip().split()
      if len(words) != 3: continue
      ret[(words[0],words[1])] = float(words[2])
      
      if not words[0] in shell_list:
        shell_list.append(words[0])
  shell_list = list(map(lambda x:[x],shell_list))
  print("load ok", len(ret.keys()))
  return ret, shell_list

if __name__ == "__main__":
  data_path = sys.argv[1]
  threshod = float(sys.argv[2])
  src_path = sys.argv[3]
  dst = sys.argv[4]
  file_dict, shell_list = read_file(data_path)
  result = cluster_by_score(file_dict, shell_list, threshod)
  len1 = 0
  for i in range(len(result)):
    save_path = os.path.join(dst,str(i))
    x = result[i]
    if len(x) == 1:
      len1 += 1
      continue
    if not os.path.exists(save_path):
      os.mkdir(save_path)
    for img in x:
      img += '.jpg'
      shutil.copyfile(os.path.join(src_path,img),os.path.join(save_path,img))
      #print(img)
  print('merge number:', len(result) - len1)


