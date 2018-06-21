from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append('/home/software/mxnet/python')
import argparse
import numpy as np
from scipy import misc
#from sklearn.model_selection import KFold
from scipy import interpolate
#import sklearn
import datetime
import pickle
#from sklearn.decomposition import PCA

#import mxnet as mx
#from mxnet import ndarray as nd

import face_image
from PIL import Image
import time
import shutil


def init_model():
  image_size = [112, 112] 
  #print('image_size', image_size)
  ctx = mx.gpu(args.gpu)
  #ctx = mx.cpu()
  nets = []
  vec = args.model.split(',')
  prefix = args.model.split(',')[0]
  epochs = []
  if len(vec)==1:
    pdir = os.path.dirname(prefix)
    for fname in os.listdir(pdir):
      if not fname.endswith('.params'):
        continue
      _file = os.path.join(pdir, fname)
      if _file.startswith(prefix):
        epoch = int(fname.split('.')[0].split('-')[1])
        epochs.append(epoch)
    epochs = sorted(epochs, reverse=True)
    if len(args.max)>0:
      _max = [int(x) for x in args.max.split(',')]
      assert len(_max)==2
      if len(epochs)>_max[1]:
        epochs = epochs[_max[0]:_max[1]]
  
  else:
    epochs = [int(x) for x in vec[1].split('|')]
  print('model number', len(epochs))
  time0 = datetime.datetime.now()
  
  for epoch in epochs:
    print('loading',prefix, epoch)
    sym, arg_params, aux_params = mx.model.load_checkpoint(prefix, epoch)
    #arg_params, aux_params = ch_dev(arg_params, aux_params, ctx)
    all_layers = sym.get_internals()
    sym = all_layers['fc1_output']
    model = mx.mod.Module(symbol=sym, context=ctx, label_names = None)
    #model = mx.mod.Module(symbol=sym, label_names = None)
    model.bind(data_shapes=[('data', (args.batch_size, 3, image_size[0], image_size[1]))])
    model.set_params(arg_params, aux_params)
  
  #  nets.append(model)
  time_now = datetime.datetime.now()
  diff = time_now - time0
  print('model loading time', diff.total_seconds())



def read_img(path):
#  img = np.array(Image.open(path)) #.convert('L'))
  img = open(path, 'rb').read()
  img_ = mx.img.imdecode(img)
  img_1= mx.nd.array(img_, dtype=np.float32)
  return mx.nd.expand_dims(nd.transpose(img_1, axes=(2, 0, 1)), axis=0)



def get_feat(imgpath, mx_model, batch_size=1, data_extra = None, label_shape = None):
#  print('testing verification..')
#  data_list = data_set[0]
  data_set = read_img(imgpath)
  data_list = [data_set]
  #print(data_set)
#  issame_list = data_set[1]
  model = mx_model
  embeddings_list = []
  if data_extra is not None:
    _data_extra = nd.array(data_extra)
  time_consumed = 0.0
  if label_shape is None:
    _label = nd.ones( (batch_size,) )
  else:
    _label = nd.ones( label_shape )
  for i in range( len(data_list) ):
    data = data_list[i]
    embeddings = None
    ba = 0
    while ba<data.shape[0]:
      bb = min(ba+batch_size, data.shape[0])
      count = bb-ba
      _data = nd.slice_axis(data, axis=0, begin=bb-batch_size, end=bb)
      #print(_data.shape, _label.shape)
      time0 = datetime.datetime.now()
      if data_extra is None:
        db = mx.io.DataBatch(data=(_data,), label=(_label,))
      else:
        db = mx.io.DataBatch(data=(_data,_data_extra), label=(_label,))
      model.forward(db, is_train=False)
      net_out = model.get_outputs()
      _embeddings = net_out[0].asnumpy()
      time_now = datetime.datetime.now()
      diff = time_now - time0
      time_consumed+=diff.total_seconds()
      #print(_embeddings.shape)
      if embeddings is None:
        embeddings = np.zeros( (data.shape[0], _embeddings.shape[1]) )
      embeddings[ba:bb,:] = _embeddings[(batch_size-count):,:]
      ba = bb
    embeddings_list.append(embeddings) #total feature
  return embeddings_list[0][0]



#def get_feats(mx_model, img_root):
#  feat_list = []
#  label_list= []
#  count = 0
#  for root, dirs, files in os.walk(img_root):
#    for ff in files:
#      count += 1
#      print(count)
#      f_path = os.path.join(root, ff)
#      feat = get_feat(f_path, mx_model)
#      feat_list.append(feat)
#      label = ff
#      label_list.append(label)
#  fn = np.vstack(feat_list)
#  ln = np.array(label_list)
#  return fn, ln 

def get_feats(mx_model, img_root):
  feat_list = []
  label_list= []
  count = 0
  for root, dirs, files in os.walk(img_root):
    if len(files) > 0:
      count += 1
      print(count)
      f_path = os.path.join(root, files[0])
      feat = get_feat(f_path, mx_model)
      feat_list.append(feat)
      label = os.path.basename(os.path.dirname(root)) + "/" + os.path.basename(root)
      print(label)
      label_list.append(label)
  fn = np.vstack(feat_list)
  ln = np.array(label_list)
  return fn, ln 


def cal_dist_pair_v1(feas, names, fid):
  #fid  = open('pair_dist.txt','w')
  #Normalize the feature
  fea=feas/np.tile(np.expand_dims(np.linalg.norm(\
          feas,axis=1),axis=1),(1,feas.shape[1]))

  score_table = fea.dot(fea.T)*127
  for i in range(score_table.shape[0]):
    for j in range(i + 1, score_table.shape[1]):
      score = score_table[i][j]
      fid.write(names[i]+' '+names[j]+' '+str(score)+'\n')
  fid.close()


def cal_dist_pair_v2(feas, names, mid_dst_path):
  #fid  = open('pair_dist.txt','w')
  #Normalize the feature
  fea=feas/np.tile(np.expand_dims(np.linalg.norm(\
          feas,axis=1),axis=1),(1,feas.shape[1]))
  score_table = fea.dot(fea.T)*127
  np.savez(mid_dst_path, names = names, score_table = score_table)


def merge_and_save(threshod, src_dir, mid_dst_path, dst_dir):
  start = time.time()
  mid_res = np.load(mid_dst_path)
  mid = time.time()
  names = mid_res["names"]
  score_table = mid_res["score_table"]
  end = time.time()
  print("load time: %f, assign time: %f" % ((mid - start), (end - start)))
  count = 0
  for i in range(score_table.shape[0]):
    count += 1
    print(count)
    dst_dir_cat_i = os.path.join(dst_dir, names[i])
    if False in set((score_table[i, :] == 0.0).tolist()):
      os.makedirs(dst_dir_cat_i)
      try:
        src_dir_cat_i = os.path.join(src_dir, names[i])
        for pic in os.listdir(src_dir_cat_i):
          shutil.copyfile(os.path.join(src_dir_cat_i, pic), os.path.join(dst_dir_cat_i, pic))
      except:
        print("can not found i'th ID")
        return 
    else:
      continue
    for j in range(i + 1, score_table.shape[1]):
      if score_table[i][j] > threshod:
        score_table[j,:] = 0.0
        src_dir_cat_j = os.path.join(src_dir, names[j])
        for pic in os.listdir(src_dir_cat_j):
          shutil.copyfile(os.path.join(src_dir_cat_j, pic), os.path.join(dst_dir_cat_i, pic))
      else:
        pass




#----------------------
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='do verification')
  # general
  parser.add_argument('--model', default='/home/JowerMan/work/insightface/models/model-r100-self_train/model,219', help='path to load model.')
  #parser.add_argument('--model', default='/home/JowerMan/work/insightface/models/model-r100-self_train/model-0020.params,0', help='path to load model.')
  #parser.add_argument('--model', default='../../models/model-r50-am-lfw/model,0', help='path to load model.')
  parser.add_argument('--target', default='lfw', help='test targets.')
  parser.add_argument('--gpu', default=0, type=int, help='gpu id')
  parser.add_argument('--batch_size', default=1, type=int, help='')
  parser.add_argument('--max', default='', type=str, help='')
  parser.add_argument('--src_dir', default= '/home/lthpc/data/NAS/NJJP/DATA/clustered_data/stage1', type = str, help = 'src_dir')
  parser.add_argument('--mid_dst_dir', default = '/home/lthpc/data/NAS/NJJP/DATA/clustered_data')
  parser.add_argument('--dst_dir', default = '/home/lthpc/data/NAS/NJJP/DATA/clustered_data/stage2')
  parser.add_argument('--threshod', default=90, type=int, help='inter-class clustering threshod')
  args = parser.parse_args()
  
  #init_model()
  #feats, names = get_feats(model, args.src_dir)
  mid_dst_path = os.path.join(args.mid_dst_dir, "result.npz")
  #cal_dist_pair_v2(feats, names, mid_dst_path)
  merge_and_save(args.threshod, args.src_dir, mid_dst_path, args.dst_dir)
  print("ok")
