#!-*-coding:ISO8859-1-*-
# This python file is to filter the satified threshod between inner-class
# Run this script like :
# >python2 inner_class_clean.py "/home/lthpc/data/NAS/NJJP/DATA/score_list_300" "/home/lthpc/data/NAS/NJJP/DATA/inner_filtered_score_list/stage1"
import sys
import os, shutil

# This func is get current dir
def get_dir():
    return os.getcwd()


# This function is change raw_name_string to new name
#   @parameter name: this is the input of raw_name
def cut_name(name_raw):
    fore_name, _ = name_raw.strip('\n').split('.')
    a = fore_name.split('\\')
    new_name = a[5] + "/" + a[6] + "/" + a[7]
    return new_name

# This function wark arround all dir under "root_dir" ,save the record which higher than "threshod"
#   @paramenter root_dir: this is the dir which the script placed
#   @paramenter threshod: this is the threshod we set
#num = 0
def clean_by_score(root_dir, threshod):
    #global num
    num = 0
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            #print(f)
            if f.endswith("txt"):
                print(f)
                with open(root + "/" + f + "_filter", 'w') as f_o:
                    with open(os.path.join(root, f), 'r') as f_i:
                        for line in f_i.readlines():
                            num += 1
                            line_sp = line.rstrip('\n').split(' ')
                            name_raw, score = line_sp[0], line_sp[1]
                            if float(score) >= threshod:
                                name = cut_name(name_raw)
                                f_o.write(name + " " + score + "\n")
                            else:
                                pass
    #print(num)
def move_to(scoce_dir, new_dir):
  if not os.path.exists(new_dir):
    os.makedirs(new_dir)
  for root, dirs, files in os.walk(score_dir):
    file_path_list  = [os.path.join(root, file_name) for file_name in files if file_name.endswith("_filter")]
    print(root)
    print(score_dir)
    mid_dir = root[root.find(score_dir) + len(score_dir) + 1 :]
    for i in range(len(file_path_list)):
      if not os.path.exists(os.path.join(new_dir, mid_dir)):
        os.makedirs(os.path.join(new_dir, mid_dir))
      shutil.move(file_path_list[i], os.path.join(new_dir, mid_dir))
  

if __name__ == "__main__":
    score_dir = sys.argv[1]
    new_dir = sys.argv[2]
    clean_by_score(score_dir, 80)
    print("clean over")
    move_to(score_dir, new_dir)
    print('ok')
