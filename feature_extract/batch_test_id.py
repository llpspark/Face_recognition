#!/usr/bin/python
import os
import shutil
import numpy
import string
#import matplotlib.pyplot as plt
import sys


def quick_roc():
    same_score= open('same_score.txt','r').read().rstrip().split(',')
    diff_score= open('diff_score.txt','r').read().rstrip().split(',')
    
    frr = numpy.zeros(128)
    far = numpy.zeros(128)
    
    for i in range(len(same_score)-1):
    	ind = abs(int((string.atof(same_score[i]))*127+0.5))
    	frr[ind] = frr[ind]+1
    for j in range(len(diff_score)-1):
    	ind = abs(int((string.atof(diff_score[j]))*127+0.5))
    	far[ind] = far[ind]+1
    
    tmp_sum_same = 0
    tmp_sum_diff = 0
    num_same = len(same_score)-1
    num_diff = len(diff_score)-1
    for i in range(128):
    	tmp_sum_same = tmp_sum_same + frr[i]
    	frr[i] = tmp_sum_same / num_same
    	tmp_sum_diff = tmp_sum_diff + far[i]
    	far[i] = 1 - tmp_sum_diff / num_diff
    	
    
    fhand_frr = open('frr.txt','w')
    fhand_far = open('far.txt','w')
    for i in range(frr.shape[0]):
            fhand_frr.write("%.5f," %frr[i])
            fhand_far.write("%.5f," %far[i])
    
    fhand_frr.write(str(1))
    fhand_far.write(str(0))
    fhand_frr.close()
    fhand_far.close()
    
    tmp = abs(frr - far)
    index = numpy.argmin(tmp)
    err = []
    point = []
    for i in range(128):
    	if far[i]>=0.001 and far[i+1]<0.001:
    		err.append(frr[i]*100)
    		point.append(i)
    	if far[i]>=0.0001 and far[i+1]<0.0001:
    		err.append(frr[i]*100)
    		point.append(i)
    	if far[i]>=0.00001 and far[i+1]<0.00001:
    		err.append(frr[i]*100)
    		point.append(i)
    	 
    err.append((far[index]+frr[index])*50)
    return err, point

class batch_extractor(object):
   def __init__(self,net_proto,trained_model,layer_name,pic_path_id,pic_path_sp,pic_list_id,pic_list_sp,model_path,model_prefix,name):
    self.net_proto = net_proto
    self.trained_model = trained_model
    self.layer_name = layer_name
    self.pic_path_id = pic_path_id
    self.pic_path_sp = pic_path_sp
    self.pic_list_id = pic_list_id
    self.pic_list_sp = pic_list_sp
    self.model_path = model_path
    self.model_prefix = model_prefix
    self.name = name

   def copy_trained_model(self,model_index):
        full_model_name = self.model_prefix+str(model_index)+'.caffemodel'
        print full_model_name
        shutil.copyfile(os.path.join(self.model_path,full_model_name),self.trained_model)

   def get_max_iter(self):
        filelist = os.listdir(self.model_path)
        max_iter = 0
        for ff in filelist:
          try:
            if ff.endswith('caffemodel'):
                words = ff.split('_')[-1].split('.')
                if string.atoi(words[0])>max_iter:
                    max_iter = string.atoi(words[0])
          except:
            continue
        return max_iter


def batch_test(extractor, fid):
    max_iter = extractor.get_max_iter()
    print 'max_iter:',max_iter

    begin_index = string.atoi(raw_input('please enter witch iter you want to begin:'))
    stepsize = string.atoi(raw_input('enter the stepsize of iter:'))
    for i in range(begin_index,max_iter+stepsize,stepsize):
        extractor.copy_trained_model(i)
        os.system('./batch_extrator_id_spot.bin > /dev/null %s %s %s %s %s %s %s' %(extractor.net_proto, extractor.trained_model,
            extractor.layer_name, extractor.pic_path_id, extractor.pic_path_sp, extractor.pic_list_id, extractor.pic_list_sp))
        eer, pot = quick_roc()
        print '-'*50
        print 'iter:%d'%i
        print eer
        print pot
        fid.write(str(i)+'\t'+str(eer)+'\n')
    fid.close()

if __name__ == '__main__':
 
    id_spot = batch_extractor('./proto/finetune_distilled_spse_deploy.prototxt',
             './model/test_finetune_distilled_spse.caffemodel','pool_8x8_s1_1','./std_IC_v1/I/', './std_IC_v1/C/', './std_IC_v1/ilist.txt',  './std_IC_v1/clist.txt',
             '/home/spark/caffe-master/examples/MS_112_classify/model/finetune_distilled_spse_3','finetune_distilled_spse_11.2_iter_','v3')

    result_fid = open('result/result.txt', 'w')
    batch_test(id_spot, result_fid)
