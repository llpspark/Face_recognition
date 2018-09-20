<center> 
#Week Report

##Work for This Week
</center>

						
<font size=3>  

* 引：从模型压缩的角度调查了有关蒸馏相关的进展。与视觉应用型论文不同模型压缩的论文开源的比例并不多，相比较之下蒸馏相关工作算是开源比例大的。下面主要从是否开源或实现两方面按照发表时间列出相关论文和实现。并在有源码实现了论文中做了进一步相关方法的调查。    
##一、知识蒸馏相关论文和进展survey：（开源或有第三方实现）   
* **2014-NIPS-Do Deep Nets Really Need to be Deep?**   
	* 论文连接：[点我](http://xueshu.baidu.com/s?wd=paperuri%3A%28078415e6ab570770529798299e0d8b90%29&filter=sc_long_sign&tn=SE_xueshusource_2kduw22v&sc_vurl=http%3A%2F%2Farxiv.org%2Fabs%2F1312.6184&ie=utf-8&sc_us=7007594391503052629)  
	* 方法：文章采用一种模型压缩（model compression）的方法模拟深度网络训练浅层网络，新的浅层模型的准确率能够达到和深度模型几乎一样的效果。（但直接训练浅层网络得到的准确率和深度网络还是没法比的）   
	* 蒸馏类型：在softmax之前作特征匹配，Hinton称之为logit匹配
	* 实现方式：     
		*  1、训练一个优秀的复杂的深度网络   
		*  2、用深度网络监督寻训练浅层网络（通过softmax前的特征作L2 loss监督训练）    
	* 复现性：当前我们使用的方法即为该方法    
	* 注意事项：
		*  1、采用训练好的深度网络和 unlabeled data 共同训练浅层网络。unlabeled的样本最好不能只是将deep model的训练集中的label去掉而得到的样本，因为deep model往往在这些样本点上有overfitting；      
		*  2、unlabel的样本数需要比deep model的训练集中的样本数要多得多，这样才能更可能的近似原来的这个deep model，unlabeled set 比 train set更大时会work best。     
* **2015-NIPS-Distilling the Knowledge in a Neural Network**（Hinton系统诠释蒸馏）    
	* 论文链接：[点我](https://arxiv.org/pdf/1503.02531.pdf)   
	* 方法： 该方法与之前论文方法不同的是采用在softmax层内特征匹配的策略。其本质上是使用softmax的输出得分作为监督，但为了使得到的得分vector更soft，在softmax层加上了蒸馏温度T,使蒸馏的性能显著提升。    
	* 蒸馏类型：在softmax层进行特征匹配     
	* 实现方式（分两阶段）：
		* 原始模型训练阶段：
			* 1. 根据提出的目标问题，设计一个或多个复杂网络（N1，N2,…,Nt）。   
			* 2. 收集足够的训练数据，按照常规CNN模型训练流程，并行的训练1中的多个网络得到。得到（M1,M2,…,Mt）
		* 浅层模型训练阶段：
			* 1. 根据（N1，N2,…,Nt）设计一个简单网络N0。   
			* 2. 收集简单模型训练数据，此处的训练数据可以是训练原始网络的有标签数据，也可以是额外的无标签数据。   
			* 3. 将2中收集到的样本输入原始模型（M1,M2,…,Mt），修改原始模型softmax层中温度参数T为一个较大值如T=20。每一个样本在每个原始模型可以得到其最终的分类概率向量，选取其中概率至最大即为该模型对于当前样本的判定结果。对于t个原始模型就可以t概率向量。然后对t概率向量求取均值作为当前样本最后的概率输出向量，记为soft_target，保存。
			![](https://i.imgur.com/uFaTz8I.jpg)     
			* 4. 标签融合2中收集到的数据定义为hard_target，有标签数据的hard_target取值为其标签值1，无标签数据hard_taret取值为0。Target = a*hard_target + b*soft_target（a+b=1）。Target最终作为训练数据的标签去训练精简模型。参数a，b是用于控制标签融合权重的，推荐经验值为（a=0.1 b=0.9）    
			* 5. 设置精简模型softmax层温度参数与原始复杂模型产生Soft-target时所采用的温度，按照常规模型训练精简网络模型。   
			* 6. 部署时将精简模型中的softmax温度参数重置为1，即采用最原始的softmax  
			![](https://i.imgur.com/5FgJaJD.jpg)   
	* 复现性：无官方开源，下面使第三方实现：    
		* caffe实现（作者只实现的cpu版本，据说并不是特别拖速度）:[knowledge_distillation_caffe](https://github.com/wentianli/knowledge_distillation_caffe)    
		* keras实现：[knowledge-distillation-keras](https://github.com/TropComplique/knowledge-distillation-keras)    
		* Tensorflow实现：[model_compression](https://github.com/chengshengchan/model_compression) 不保证能跑通，有人提出跑不起来
	* 注意事项：训练时将浅层网络温度与深层网络一致，部署时将浅层网络温度置1.   
* **2015-ICLR-FitNets：HINTS FOR THIN DEEP NETS**    
	* 论文链接：[点我 ](https://arxiv.org/pdf/1412.6550.pdf)
	* 方法：这篇论文的蒸馏方式与前两篇有所不同。其一，从网络结构上，该文目的是蒸馏一个更深但是复杂度比较小的网络，其二，对于蒸馏更深的网络，本文提出使用在中间层加入loss的方法，如此分成两个loss来训练，最后得到比复杂模型更好的结果。    
	![](https://i.imgur.com/JXMKNZZ.jpg)     
	如上图，之所以有Wr是因为teacher network的层输出与小网络的往往是不一样的，因此需要这样一个mapping来匹配，并且这个mapping也是需要学习的。paper中提到说用多加一个conv层的方法比较节省参数（其实也比较符合逻辑），然后这个conv层不加padding，不stride。  
	* 蒸馏类型：多loss，向更窄更深压缩网络   
	* 实现方式：
		* 两阶段法：先用 hint training 去 pretrain 小模型前半部分的参数，再用 KD Training 去训练全体参数。
		* （1）Teacher网络的某一中间层的权值为Wt=Whint，Student网络的某一中间层的权值为Ws=Wguided。使用一个映射函数Wr来使得Wguided的维度匹配Whint，得到Ws'。其中对于Wr的训练使用MSEloss  
		![](https://i.imgur.com/0230dis.png)   
		* （2）改造softmax的loss（即为Hinton论文的方法）：
		![](https://i.imgur.com/7KFJkhF.png)    
		![](https://i.imgur.com/Msls4Qc.png)   
	* 复现性：   
		* Theano实现：[distillation](https://github.com/net-titech/distillation/tree/master/FitNets)      
	* 注意事项:teacher和student网络结构不类似的话，上述方法就失效了
* **2016-AAAI-Face Model Compression by Distilling Knowledge from Neurons**(汤晓欧组)		
	* 论文链接：[点我](http://personal.ie.cuhk.edu.hk/~pluo/pdf/aaai16-face-model-compression.pdf)
	* 方法：本文将知识蒸馏研究到人脸识别任务中。监督训练方式回归到logit匹配形式（softmax类别数原因难收敛），并提出神经元选择策略，去除神经元噪声，使特征更精准。   
	* 蒸馏类型：采用logit方式进行特征监督匹配，神经元选择是该论文的重头戏。     
	* 实现方式：
		* 1、logit匹配训练  
		* 2、神经元选择（具体过程还需读论文）
	* 复现性：  
		* caffe + t-SNE + matlab实现: [mobile-id](https://github.com/liuziwei7/mobile-id)	   
* **2017-ICLR-Paying More Attention to Attention: Improving the Performance of Convolutional Neural Networks via Attention Transfer**    
	* 论文链接：[点我](https://arxiv.org/pdf/1612.03928.pdf)    
	* 方法：将注意力模型用于Teacher-Student蒸馏过程
	* 蒸馏类型：深度学习注意力机制 + 知识蒸馏（文中提到把teacher模型中loss对input的导数作为知识传递给student模型，因为loss对input的导数反映了网络output的变化对于input的敏感程度，如果某个像素一个小的变化对于对于网络输出有一个大的影响，我们就可以认为网络"pay attention"那个像素）
	* 实现方式：需要具体读论文
	* 复现性：
		* PyTorch实现：[attention-transfer](https://github.com/szagoruyko/attention-transfer)      

* **2017-NIPS and AISTATS-Data-Free Knowledge Distillation For Deep Neural Networks**   
	* 论文链接：[点我](https://arxiv.org/pdf/1710.07535.pdf)    
	* 方法：通过重构元数据的方式进行知识蒸馏。应用场景是当训练数据由于隐私等问题对于student模型不可用的时候，如何通过extra metadata的方式解决。   
	* 蒸馏类型：元数据重构解决蒸馏数据问题   
	* 实现方式：需要具体读论文
	* 复现性：
		* PyTorch实现：[replayed_distillation](https://github.com/iRapha/replayed_distillation)        
* **2018-AAAI-Rocket Launching: A Universal and Efficient Framework for Training Well-performing Light Net** （阿里+清华合作）   
	* 论文链接：[点我](https://arxiv.org/pdf/1708.04106.pdf)    
	* 论文解读：[点我](http://www.infoq.com/cn/articles/alibaba-AAAI-2018-rocket-launching)      
	* 方法：teacher和student共享部分网络，同时一起训练。让teacher从头至尾一直指导student，loss是加权网络的cross entropy和两个网络的feature的regression。   
	* 蒸馏类型：
	* 复现性：
		* PyTorch实现：[Rocket-Launching](https://github.com/zhougr1993/Rocket-Launching)     
	* 注意事项：teacher和student同时训练会导致teacher的精度降低，虽然作者加入了gradient block来缓解student对teacher的影响，但是这样一定程度还是会影响student提升的效果。      
* **2018-AAAI-DarkRank: Accelerating Deep Metric Learning via Cross Sample Similarities Transfer**（图森）       
	* 论文链接：[点我](https://arxiv.org/pdf/1707.01220.pdf)     
	* 论文解读：[点我](https://blog.csdn.net/sinat_35188997/article/details/78180419) 
	* 方法：该论文从一个新的视角对Teacher和Student网络间的loss进行了设计，将不同样本之间的相似性排序融入到监督训练中，并融合了softmax、Verify loss、triplet loss共同训练student。(该方法在小数据集下的行人再识别上做的实验)
	* 实现方式：（如下图）
	![](https://i.imgur.com/mnRvby2.png)   
	* 复现性:
		* MxNet实现：[DarkRank](https://github.com/TuSimple/DarkRank)
 
					




##二、知识蒸馏相关论文和进展survey：（未开源或无第三方实现）    
 
* **2017-ICLR and CVPR-Learning Loss for Knowledge Distillation with Conditional Adversarial Networks**   
	* 论文链接：[点我](https://arxiv.org/pdf/1709.00513.pdf)   
	* 方法：主要通过条件GAN和KD（知识蒸馏）的形式对监督loss进行协同学习，作者认为直接使用L2loss太过武断，一定程度上限制了student模型的自主学习空间。   
	* 蒸馏类型：对损失函数进行改进（CAN + KD）   
	* 实现方式：学生网络是生成器，判别器是一个多层感知机网络，生成器和判别器迭代优化，生成器的目标是生成让判别器无法辨别的logits。某种程度上，这个工作也可以理解成对损失函数做了改进。    

* **2017-CVPR-Knowledge Projection for Effective Design of Thinner and Faster Deep Neural Networks**    
	* 论文链接：[点我](https://arxiv.org/pdf/1710.09505.pdf)    
	* 方法：类似于Fitnets形式采用多loss形式蒸馏student网络   
	* 蒸馏类型:同Fitnets属于多loss    
	
* **2017-CVPR-Moonshine: Distilling with Cheap Convolutions**  
	* 论文链接：[点我](https://arxiv.org/abs/1711.02613)   
	* 方法：将深度学习注意力机制融合到知识蒸馏中
* **2017-CVPR-A Gift from Knowledge Distillation:Fast Optimization, Network Minimization and Transfer Learning**（韩国科学院）
	* 论文链接：[点我](http://openaccess.thecvf.com/content_cvpr_2017/papers/Yim_A_Gift_From_CVPR_2017_paper.pdf)   
	* 方法：该论文想法独特，画风清奇。之前的文章都是把大模型的输出当成小模型要去拟合的目标，该论文一改此做法，他不拟合大模型的输出，而是去拟合大模型与小模型层与层之间的关系，并认为这才是真正要转移和蒸馏的知识。    
	* 蒸馏类型：通过拟合Teacher网络和Student网络的层与层之间的关系进行蒸馏    
	* 实现方式（二阶段法）：
		* 1、先根据大模型的 FSP 矩阵调整小模型参数，使得小模型层间关系也和大模型的层间关系类似；
		* 2、然后直接用原损失函数（如交叉熵）继续精调小模型参数。
		![](https://i.imgur.com/1LNwG4j.jpg)  



##附：
* 模型压缩和蒸馏相关文档链接：
	* [模型压缩那些事](https://zhuanlan.zhihu.com/p/28872061)   
	* [优秀的模型压缩论文](http://memoiry.me/2018/03/19/Awesome-model-compression-and-acceleration/)      
	* [awesome-knowledge-distillation](https://github.com/dkozlov/awesome-knowledge-distillation#papers)
	* 

* 针对服务器端高性能网络：
	* VGGNet:
	* ResNet:
	* InceptionNet:
	* DenseNet:
	* Inside-OutsideNet:
	* SE-Net:
* 针对移动端部署的网络：
	* MobileNet:
	* ShuffleNet:
	* ShuffleNet V2:
	* MobileFaceNets:

