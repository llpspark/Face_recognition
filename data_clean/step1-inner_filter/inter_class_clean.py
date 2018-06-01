#!-*-coding:utf-8-*-
# This script filter the higer similarity (metric by threshod) between inter-class and merge them to same label ,finaly genate the train datasets

#excute like this:
#> python inter_class_clean.py --inter_cls_dir "/home/lthpc/data/ShanDa-2/shanda2_idpair_score" --inner_cls_dir "/home/lthpc/data/ShanDa-2/ShanDa2_score" --output_dir "/home/lthpc/data/ShanDa-2/result.txt"  --want_prefix "/home/lthpc/data/ShanDa-2/std_112_mct_color/" --threshod 114

import argparse
import os
import sys


# This function is delete the given postfix of the fllename
#   @parameter filename: the filename of inpout
#   @parameter symbol: the symbol we will delete behind of it
def split_symbol(filename, symbol):
  names = filename.strip('\n').split(symbol)
  return names[0]


# This function is judged whether the element in nesting list
#   @parameter element: this is the input element
#   @parameter merge_list: this is the nesting list
#   #return : return a list which have bool and sub_list_name
def judge_in_list(element, merge_list):
  for sub_list in merge_list:
    if element in sub_list:
      sub_list_ = sub_list
      return [True, sub_list_]
  return [False, []]

# this function is search all "*txt" file and filter the name which the score satisfy given threshod
#   @parameter root_dir: this is the path which the script placed
#   @parameter threshod: this is the given threshod
merge_list = []
def clean_by_score(root_dir, threshod):
  file_list = os.listdir(root_dir)
  for filename in file_list:
    file_path = os.path.join(root_dir, filename)
    if os.path.isdir(file_path):
      clean_by_score(file_path, threshod)
    else:
      if not filename.endswith('txt'):
        pass
      elif not judge_in_list(split_symbol(filename, '.'), merge_list)[0]:
        sub_list = []
        with open(file_path, 'r') as f_i:
          for line in f_i.readlines():
            line = line.strip('\n').split(' ')
            if float(line[1]) > threshod:
              if split_symbol(filename, '.') not in sub_list:
                sub_list.append(split_symbol(filename, '.'))
              else:
                pass
              if not judge_in_list(line[0], merge_list)[0]:
                sub_list.append(line[0])
              else:
                pass
          if len(sub_list) > 1:
            merge_list.append(sub_list)
  return merge_list


# This function merge inter-class label and generate final train result  according to the filtered inner-class file 
#   @param output_dir: this is the result file dir which we place
#   @param inner_cls_dir: this is filtered inner-class txt file dir
#   param merge_list: this is the result which "clean_by_score" function generated
#   param want_prefix: this is the pre_fix we want plus to
def get_label_from_clsinner(output_dir, inner_cls_dir, merge_list,  want_prefix):
  #print(merge_list)
  temp = 0
  with open(output_dir, 'w') as f_w:
    for file_dir in os.listdir(inner_cls_dir):
      if os.path.isfile(os.path.join(inner_cls_dir, file_dir)) and file_dir.endswith("filter"):
        temp += 1
        new_file_name = split_symbol(file_dir, '_')
        new_file_pure_name = split_symbol(new_file_name, '.')
        if not judge_in_list(new_file_pure_name, merge_list)[0] or \
        judge_in_list(new_file_pure_name, merge_list)[0] and \
        new_file_pure_name == judge_in_list(new_file_pure_name, merge_list)[1][0]:
          label = new_file_pure_name
          #print(label)
        else:
          label = judge_in_list(new_file_pure_name, merge_list)[1][0]
          print(new_file_name)
        with open(os.path.join(inner_cls_dir, file_dir), 'r') as f_r:              
          for line in f_r.readlines():
            name_and_label =  want_prefix + split_symbol(line, ' ') + ".jpg" + " " + label + "\n"
            f_w.write(name_and_label)

if __name__ == "__main__":
  
  parser = argparse.ArgumentParser(description="parse  the input args")
  parser.add_argument("--inter_cls_dir", type=str, help="inter-class files directory", default="/home/lthpc/data/ShanDa-2/shanda2_idpair_score")
  parser.add_argument("--inner_cls_dir", type=str, help="inner-class files directory",default="/home/lthpc/data/ShanDa-2/ShanDa2_score")
  parser.add_argument("--output_dir", type=str, help="output_file directory", default="/home/lthpc/data/ShanDa-2/result.txt")
  parser.add_argument("--want_prefix", type=str, help="add prefix to result", default="/home/lthpc/data/ShanDa-2/std_112_mct_color/")
  parser.add_argument("--threshod", type=int, help="set threshod to inter class", default=114)
  
  args = parser.parse_args()
  inter_cls_dir = args.inter_cls_dir
  inner_cls_dir = args.inner_cls_dir
  output_dir = args.output_dir
  want_prefix = args.want_prefix
  threshod = args.threshod
  
  get_label_from_clsinner(output_dir, inner_cls_dir, clean_by_score(inter_cls_dir, threshod),  want_prefix)

  print('ok')
