import os, sys


def move_to(scoce_dir, new_dir):
  if not os.path.exists(new_dir):
    os.makedirs(new_dir)
  for root, dirs, files in os.walk(score_dir):
    file_path_list  = [os.path.join(root, file_name) for file_name in files if file_name.endswith("_ori")]
    for i in range(len(file_path_list)):
      shutil.move(file_path_list[i], new_dir)

if __name__ == "__main__":
  move_to(score_dir, new_dir)
