# This script is cluster different class by scores which generate by different img comparison.
#run like:
#> python multi_process_cluster.py 40 /home/lthpc/data/NAS/NJJP/DATA/filtered_noise/stage1_aligned_pair_score /home/lthpc/data/NAS/NJJP/DATA/filtered_noise/stage1_aligned /home/lthpc/data/NAS/NJJP/DATA/clustered_data/stage1 40



import os, sys
import pandas as pd
import heapq
from itertools import chain
import shutil
from multiprocessing import Process


def cal_set2set_simi(file_dict, set_data1, set_data2):
  # mean value similarity

  #sum_score = 0
  #for data1 in set_data1:
  #  for data2 in set_data2:
  #    sum_score += file_dict[(data1, data2)]
  #return sum_score / (len(set_data1)*len(set_data2))

  # max value similarity
  
  #temp_max = 0
  #for data1 in set_data1:
  #  for data2 in set_data2:
  #    if file_dict[(data1, data2)] > temp_max:
  #      temp_max = file_dict[(data1, data2)]
  #return temp_max

  # median similarity
  score_list = []
  for data1 in set_data1:
    for data2 in set_data2:
      score_list.append(file_dict[(data1, data2)])
  sorted_score = list(sorted(set(score_list)))
  return sorted_score[len(sorted_score) // 2]


def find_most_simi(file_dict,shell_list):
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
    second_max_score, index_i, index_j = find_most_simi(file_dict, shell_list)
    shell_list = merge_simi(shell_list, index_i, index_j)
    print('shell_list lenth:', len(shell_list))
    if second_max_score < threshod or len(shell_list)==1:
      return shell_list
       

def read_file(data_path):
  #for i, data_path_i in enumerate(os.listdir(src_dir)):
  #  if not i % proc_num == proc_id:
  #    continue
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
      #if float(words[2]) < 0: continue
      ret[(words[0],words[1])] = float(words[2])
      
      if not words[0] in shell_list:
        shell_list.append(words[0])
  shell_list = list(map(lambda x:[x],shell_list))
  print("load ok", len(ret.keys()))
  return ret, shell_list



def save_result(result, src_img_dir, dst_img_dir):
  len1 = 0
  for i in range(len(result)):
    save_path = os.path.join(dst_img_dir, str(i))
    x = result[i]
    if len(x) == 1:
      #len1 += 1
      continue
    if not os.path.exists(save_path):
      os.mkdir(save_path)
    for img in x:
      #img += '.jpg'
      shutil.copyfile(os.path.join(src_img_dir, img), os.path.join(save_path, img))
      #print(img)
  #print('merge number:', len(result) - len1)


def append_path(dst_path, append_path):
  if not os.path.exists(os.path.join(dst_path, append_path)):
    os.mkdir(os.path.join(dst_path, append_path))
  return os.path.join(dst_path, append_path)


def signle_cluster(proc_num, proc_id, src_score_dir, src_img_dir, dst_dir, threshod):
  for i, data_path in enumerate(os.listdir(src_score_dir)):
    if not i % proc_num == proc_id:
      continue
    file_dict, shell_list = read_file(os.path.join(src_score_dir, data_path))
    result = cluster_by_score(file_dict, shell_list, threshod)
    print(result)
    new_src_img_dir = os.path.join(src_img_dir, data_path.split(".")[0])
    new_dst_path = append_path(dst_dir, data_path.split(".")[0])
    save_result(result, new_src_img_dir, new_dst_path)


class Multi_Cluster(Process):
  def __init__(self, proc_num, proc_id, src_score_dir, src_img_dir, dst_dir, threshod):
    super().__init__()
    self.proc_num = proc_num
    self.proc_id = proc_id
    self.src_score_dir = src_score_dir
    self.src_img_dir = src_img_dir
    self.dst_dir = dst_dir
    self.threshod = threshod

  def run(self):
    signle_cluster(self.proc_num, self.proc_id, self.src_score_dir, src_img_dir, self.dst_dir, self.threshod)
    

def multi_run(proc_num, src_score_dir, src_img_dir, dst_dir, threshod):
  proc_list = []
  for i in range(proc_num):
    proc_list.append(Multi_Cluster(proc_num, i, src_score_dir, src_img_dir, dst_dir, threshod))

  for proc in proc_list:
    proc.start()

  for proc in proc_list:
    proc.join()


if __name__ == "__main__":
  proc_num = int(sys.argv[1])
  src_score_dir = sys.argv[2]
  src_img_dir = sys.argv[3]
  dst_dir = sys.argv[4]
  threshod = float(sys.argv[5])
  multi_run(proc_num, src_score_dir, src_img_dir, dst_dir, threshod)
  print("ok")

