#run like:
#> python score_intersect_img.py /home/lthpc/data/NAS/NJJP/DATA/inner_filtered_score_list/stage1/score.txt /home/lthpc/data/NAS/NJJP/DATA/NJ_ALIGNED_112X112/stage1  /home/lthpc/data/NAS/NJJP/DATA/inner_filtered_score_list/stage1/JPV1.txt

import os, sys
import numpy as np
import pandas as pd


def score_intersect_img(score_path, img_dir, output_path):
  pd.set_option("display.max_colwidth", 500)
  try:
    df = pd.read_table(score_path, header = None, encoding = 'utf-8', delim_whitespace = True)
    print("read ok")
  except:
    print(score_path, "error")
    return

  mask = [os.path.exists(os.path.join(img_dir, i)) for i in df[0]]
  print(mask)

  df_0  = [os.path.join(img_dir, i) for i in df.loc[mask, 0]]
  
  df_1 = [i for i in df.loc[mask, 1]]
  new_len = len(df_0)
  df_w = pd.DataFrame(np.arange(2* new_len).reshape(new_len, -1))
  df_w.loc[:, 0] = df_0
  df_w.loc[:, 1] = df_1
  
  


  df_w.to_csv(output_path, sep = ' ', header = False, index = False)


if __name__ == "__main__":
  score_path = sys.argv[1]
  img_dir = sys.argv[2]
  output_path = sys.argv[3]
  score_intersect_img(score_path, img_dir, output_path)
  print("ok")
