<center> 
#模型压缩之Fitnet+classify_finetune
</center>     
## 实验流程					

### stage1：（FitNet distill training）     

* 说明：stage1下分为两个子阶段，第一个子阶段为hint监督训练，第二个子阶段为整个网络监督训练。   

* 实验环境：caffe
* 训练数据：insight face使用的训练数据        
* student网络结构上：
	* 变薄：减少卷积核数量  
		* 卷积核减少方式（整体减少、在网络后半部分减少）
		* 卷积核减少量级（使用1/2，4/5两个量级）    
* Hint层的设计：
	* hint监督数量：--使用论文已经论证数量为1才有助于训练
	* hint监督位置--论文所有实验均加在网络中间（偏后）   
* 问题与解决方案：
	* experience 1:
		* problem：（使用caffe）网络在训练过程中student没有分类性能且teacher网络性能下降。
		* solution：1、student 网络要将delopy形式的结果转为train形式的prototxt（具体参照[本人GitHub](https://github.com/llpspark/Face_recognition/tree/master/net_distill/code)）； 2、再将teacher net停止反向传播的同时要将其weight_decay 置为0；
* 结果和结论：
	* 该阶段的识别结果：      

![](https://i.imgur.com/jZSxzlL.png)

	* 结论：通过Fitnet方法与直接进行模型蒸馏训练student net对比，Fitnet方法得到的模型人脸识别准确率更高（直接蒸馏准确率很低）。
### stage2:(one hot finetune)  

* 说明：基于stage1的训练结果通过one hot的方式（通过全局度量学习损失函数）进行微调，微调中的损失基于insight face 的loss类型。

* 实验环境：MXnet	
* 寻优方法：该阶段调整不同的超参数优化微调结果。    
* 训练数据： face_emore(insight face 后期又发布的数据集)    
* 问题与解决方案：
	* experience 1:
		* caffe 模型转MXnet出现的问题（使用微软的MMdnn）--微调转换后的模型收敛慢，且准确率提升不高。   
		* 使用mmdnn 由caffe转 mxnet模型时，mmdnn将res100中网络尾部的pre_fc1层的名字自动改了（变为pre_fc1_1）,原因可能：1、caffe的cov层后直接接fc层导致（没有明确定义flat层）。因为在生成的mxnet模型型中自动增加flat层，且命名pre_fc1_0,pre_fc1变成了pre_fc1_1。 2、可能是dorpout层导致，可能经过dropout层后，转换时自动增加了flat层（这个只是推测）。
* 结果和结论：
	* stage2 结果：       

![](https://i.imgur.com/4rEw812.png)

	* stage2 结论：将stage1得到的Fitnet蒸馏压缩的结果使用分类loss进行微调是有效的（使用当前最优的全局度量学习loss A-softmax(arcface)）。   
### stage3：(triplet loss finetune) 

* 说明：该阶段基于stage2的训练结果通过局部度量损失函数（npair loss、triplet loss、triplet with margin）进行进一步微调。    
* 环境：MXnet
* 寻优方式：通过不同类型的局部度量损失对模型进行微调。   
* 结果和结论：
	* 该阶段的识别结果：
    

![](https://i.imgur.com/sYl3gQh.png)

	* 结论：对stage2得到的模型进行局部度量类型loss下的进一步finetune得到了较大的提升（尤其是百万分点以后提升较大），其中使用triplet with margin类型的loss得到了最优的结果，triplet loss次之，npair loss提升最小。

## 实验总结

* 通过以上三个阶段的模型压缩与微调是有效的。
* 由stage3中得到的最终结果看，在千分点到十万分点压缩后的模型基本与teacher 模型性能相当，百万和千万分点压缩后的模型性能低于teacher模型。
