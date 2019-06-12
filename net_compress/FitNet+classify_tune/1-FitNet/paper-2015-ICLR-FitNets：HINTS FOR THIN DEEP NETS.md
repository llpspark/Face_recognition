# 2015-ICLR-FitNets：HINTS FOR THIN DEEP NETS   
* paper:https://arxiv.org/pdf/1412.6550.pdf  
* code:https://github.com/net-titech/distillation/tree/master/FitNets            

### 预备知识  

* **课程学习(Curriculum Learning)或称自步学习(Self-paced Learning)**：我们可以模拟人的认知机理，先学习简单的、普适的知识（课程），然后逐渐增加难度，过渡到学习更复杂、更专门的知识，以此完成对复杂对象的认知。模拟这一过程，我们可以将学习对象(数据、特征、概念等)按其对学习目标的难易程度，从易到难开展学习，以这种方式让机器完成复杂的学习与推理任务。     

## Abstract     

* 摘要说明神经网络两个要点的权衡：网络性能、执行速度。再次强调网络的深度和性能相关性很大，但网络变深对于神经网络训练变得困难。因此，本文从蒸馏的角度，在不明显改变teacher Net整体结果的基础上增加网络的深度，并通过逐阶段网络训练的方式提升网络性能。     

## 1、introduction    

* 从模型压缩的角度回顾相应技术进展（当然包括Hinton的蒸馏论文），已证明神经网络层越深性能越好（Bengio2013的论文等）。     
* 提出本文从解决当神经网络层变深后所面临的网络模型压缩的问题。提出的FitNet可以很好的蒸馏一个比teacher Net更深、更薄（输出通道数少）的网络。该方法是基于Hinton蒸馏（KD）基础上网络训练上的改进提升，并在几个公开的数据集（MNIST, CIFAR-10, CIFAR-100, SVHN and AFLW）上得到了很好的结果。    

## 2、Method     

* 回顾了2015年Hinton提出的知识蒸馏的具体过程（此处略，具体可查阅之前总结的模型压缩论文survey中该论文的具体实现），指出知识整理设计的student和teacher网络深度基本差不多，而本文为了提升精读要蒸馏一个更深的网络，并提出FitNet来解决蒸馏深层网络中难于优化的问题。           
* 基于Hint的训练。这里的hint指的是在teacher网络中间层的网络输出，并以此指导训练student网络的前半部分（student被监督的层称之为guided layer）。两阶段法训练：先用 hint training 去 pretrain 小模型前半部分的参数，再用 KD Training 去训练全体参数。
	* （1）Teacher网络的某一中间层的权值为Wt=Whint，Student网络的某一中间层的权值为Ws=Wguided。使用一个映射函数Wr来使得Wguided的维度匹配Whint，得到Ws'。其中对于Wr的训练使用MSEloss  
![](https://i.imgur.com/0230dis.png)   
	* （2）改造softmax的loss（即为Hinton论文的方法）：
![](https://i.imgur.com/7KFJkhF.png)    
![](https://i.imgur.com/Msls4Qc.png)   
	* 具体训练过程如下图所示。在第一阶段通过公式（3）训练时，对student网络直接基于feature map的求L2 loss，而不是将feature map 拉成一维的vector再求L2 loss（主要原因作者分析了训练参数数量，全连接训练参数数量巨大（   
![](https://i.imgur.com/d3jrmo2.png)，N，o分别为特征图的边长像素数和通道数）不容易收敛，而二维的feature map监督训练可训练参数为（    
![](https://i.imgur.com/zszED2O.png)，k和o分别为卷积核尺寸和输出通道数）更容易收敛）    
![](https://i.imgur.com/JXMKNZZ.jpg)
 * 与课程学习(Curriculum Learning)的关系
 	* 作者认为提出的FitNet训练过程类似于课程学习的过程（课程学习已在前面介绍），具体无干货，略。     

## 3、Results on Benchmark Datasets  
本文在几个公开的benchmark 数据集上做了测试，首先对不同数据集进行了介绍，然后在不同数据集上进行了实验和结果分析。 
     

* 数据集介绍及相应实验：    
	* CIFAR-10，CIFAR-100数据集介绍：        
		* CIFAR-10数据集包含60000个32*32的彩色图像，共有10类。有50000个训练图像和10000个测试图像。数据集分为5个训练块和1个测试块，每个块有10000个图像。测试块包含从每类随机选择的1000个图像。训练块以随机的顺序包含这些图像，但一些训练块可能比其它类包含更多的图像。训练块每类包含5000个图像。    
		* CIFAR-100数据集包含100小类，每小类包含600个图像，其中有500个训练图像和100个测试图像。100类被分组为20个大类。每个图像带有1个小类的“fine”标签和1个大类“coarse”标签。    
	* 作者的实验中teacher Net使用三层的maxout-卷积（maxout是一种激活函数）网络，student net使用17层maxout-卷积网络。    
	* 对于从teacher net的中间层选择hint层的输出监督student的中间层训练，直观的想法是从hint层中得到期望的输出来监督student net的中间层（这里期望的输出并不是期望提取的最好特征）。下面着重讨论从teacher Net上进行Hint的方式和说明。    
		* 逐阶段训练。第一阶段基于分类目标训练前半部分网络，第二阶段基于分类任务训练整个网络。注意这里的第一阶段相当于在teacher 的hint层和student的guided 层均进行分类输出求loss，而不是直接进行feature map 的L2 loss。文中提到，在此情况下，第一阶段得到了很好的局部最优化貌似并不能充分地帮助网络第二阶段的训练。    
		* 为了进一步辅助训练薄而深的神经网络，尝试从teacher net中添加额外的hint层（多hint层训练），来共同监督student net的guided layer。作者指出这样的话，在数据通过神经网络过程中，会将输入数据中的部分信息弃用，在网络的分类输出之前需要更多的网络层。   
		* 逐阶段蒸馏。第一阶段通过蒸馏的方式训练前半部分网络，第二阶段通过蒸馏的方式训练整个网络。这类似于第一种情况，在第一阶段训练出的局部最优权重，并不能有效地辅助整个网络的训练，从而学习失败。    
		* 联合hint层对guided层、两个网络输出之间分类输出的共同训练（说白了就是把hint阶段归并到和网络分类loss一起训）。论文指出，通过这种同时联合训练的方式并没能够使student网络学到东西。    
		* 联合hint层对guided层、两个网络输出之间进行蒸馏的共同训练（说白了就是把hint阶段归并到和蒸馏一起训）。论文指出，通过这种同时联合训练的方式同样并没能够使student网络学到东西。  
	* SVHN（google 房屋数字数据集--数字的数据集） 、 MNIST、AFLW（人脸识别的小数据集）介绍和相关实验略。   

## Analysis of empirical results     

该部分对KD、fitnet 等训练和实验结果进行了简单的理论分析，具体略。    

## Conclusion     

本文通过在teacher net的中间层引入hint来监督训练student net的内部隐层，使得将宽、深的网络蒸馏到更深、更薄的网络，并且student拥有更少的参数和更快的inference速度。在几个公开的数据集上得到了很好的效果。    

##附录A：网络结构和训练过程
* 这里只将网络训练过程中的一些重要参数总结说明（以CIFAR-10、CIFAR-100为例）   
如table 6所示为基于teacher net设计的四个student net的具体网络结构   
![](https://i.imgur.com/Ggcp4Ye.png)     
	* Fitnet参数采用随机初始化 + SGD寻优   
	* 初始学习率0.005   
	* 第一阶段用的训练数据使CIFAIR的train set，第二阶段使用的训练数据使train set和validation set   
	* 注意第二阶段并不是对网络前半部分的微调，而是用和第一阶段相同的学习率参数进行训练。


