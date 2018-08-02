# This script is modify net structure. just like layer name;num_output;find the appoint net location and change num_output ;add lr_mult, weight decay; modify BatchNorm Parameter ...
#> run like:
#> python modify_net_struct.py test_code/res_100_1_b_0.5.prototxt 0.5


import sys, os

def modify_layername(input_net):
  '''
  modify all the name of net work layer which
  add with "_stu"

  '''
  loc_name = ["name", "bottom", "top"]
  with open(input_net + "_tmp", "w") as o_f:
    with open(input_net, "r") as i_f:
      for line in i_f.readlines():
        flag = 1
        for loc in loc_name:
          if loc in line:
            flag = 0
            line_sp = line.split("\"")
            o_f.write(line_sp[0] +  "\"" + line_sp[1] + "_stu" + "\"" + line_sp[2])
        if flag:
          o_f.write(line)
  os.rename(input_net + "_tmp", input_net)

def modify_num_output(net_work, rate):
  with open(net_work, "r") as f:
    with open(net_work + "tmp", "w") as f_o:
      content = f.readlines()
      for line in content:
        if "num_output" in line:
          line_sp = line.strip("\n").split(":")
          f_o.write(line_sp[0] + ":" + str(round(int(line_sp[1]) * rate)) + "\n")
        else:
          f_o.write(line)
  os.rename(net_work + "tmp", net_work)


def find_appoint_loc(net_work, divide_rate):
  '''
  This function is find the location of appoint

  @param divide_rate: this parameter indicate the rate of locate depth to whole depth(locate depth/whole depth)
  '''
  loc_list = []
  with open(net_work, "r") as f:
    lines = enumerate(f.readlines(), 1)
    for line in lines:
      if "Convolution" in line[1]:
        loc_list.append(line[0])
  print("conv layer number:", len(loc_list))
  print("the line number you want find:", loc_list[int(len(loc_list) * divide_rate)])


def find_all_layer_type(net_work):
  '''
  This function is all the net type
  '''
  type_list = []
  with open(net_work, 'r') as f_r:
    for line in f_r.readlines():
      if "type" in line:
        type_str = line.strip('\n').split(":")[1]
        if not type_str in type_list:
          type_list.append(type_str)
  return type_list

def add_lr_wd(net_work, style = "teacher"):
  '''
  This function is add param about lr_mult and weight decay

  @param style: this paramter is appoint which type net will be modify(teacher weight decay must to be 0 )

  '''
  t_w_b = '''
    param{
          lr_mult: 0
          decay_mult: 0
          }
        '''
  
  s_w = '''
    param{
          lr_mult: 1
          decay_mult: 1
          }
        '''
  
  s_b = '''
    param{
          lr_mult: 2
          decay_mult: 0
          }
        '''
  type_list = ["Convolution", "InnerProduct",  "Scale", "BatchNorm", "PReLU"]

  if style == "teacher":
    with open(net_work, "r") as f_r:
      with open(net_work + "_tmp", "w") as f_w:
        for line in f_r.readlines():
          f_w.write(line)
          if "#" in line:
            pass
          elif type_list[0] in line or type_list[1] in line or type_list[2] in line:
            f_w.write(t_w_b *2)
          elif type_list[3] in line:
            f_w.write(t_w_b * 3)
          elif type_list[4] in line:
            f_w.write(t_w_b)
          else:
            pass
  elif style == "student":
    with open(net_work, "r") as f_r:
      with open(net_work + "_tmp", "w") as f_w:
        for line in f_r.readlines():
          f_w.write(line)
          if "#" in line:
            pass
          elif type_list[0] in line or type_list[1] in line or type_list[2] in line:
            f_w.write(s_w)
            f_w.write(s_b)
          elif type_list[3] in line:
            f_w.write(t_w_b * 3)   # batchnorm 无论是训练还是测试学习率参数都是0
          elif type_list[4] in line:
            f_w.write(s_w)
  os.rename(net_work + "_tmp", net_work)

def modify_batchnorm_parameter(net_work):
  '''
  This function is delete "use_global_stats" term in the net' BN layer, because :
  By default, it is set to false when the network is in the training
  phase and true when the network is in the testing phase. And 
  It must be done otherwise can't be converge when training.

  '''
  with open(net_work, "r") as f_r:
    with open(net_work + "_tmp", "w") as f_w:
      for line in f_r.readlines():
        if "use_global_stats" in line:
          pass
        else:
          f_w.write(line)
  os.rename(net_work + "_tmp", net_work)      

def modify_conv_bias(net_work):
  '''
  This function is delete "bias_term" in the net's Convolution layer,
  so that make bias term to default(bias is true)

  '''
  with open(net_work, "r") as f_r:
    with open(net_work + "_tmp", "w") as f_w:
      for line in f_r.readlines():
        if "bias_term" in line:
          pass
        else:
          f_w.write(line)
  os.rename(net_work + "_tmp", net_work)      


if __name__ == "__main__":
  input_net = sys.argv[1]
  rate = float(sys.argv[2])
  modify_layername(input_net)
  modify_num_output(input_net, rate)
  print("all layer type are as list:",find_all_layer_type(input_net))
  modify_conv_bias(input_net)
  add_lr_wd(input_net, "student")
  modify_batchnorm_parameter(input_net)
  find_appoint_loc(input_net, divide_rate = 0.5)
  print("ok")

