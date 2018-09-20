# ArcFace: Additive Angular Margin Loss for Deep Face Recognition     
* paper:https://arxiv.org/pdf/1801.07698.pdf  
* code:https://github.com/deepinsight/insightface       
  
该文是目前FR的state-of-art（2018-6-23）   

<font size = 3>
###预备知识  
* 经过神经网络提取的特征不仅可以用于人脸识别（验证和识别）还可以用于人脸聚类的原因：无论是识别任务还是聚类任务其本质都是不同特征直接进行距离度量，度量的结果是分数值，所以通过调整得分的阈值便可应用到识别和聚类两个不同的任务。   
* MegaFace数据集说明：MegaFace 包括两个不同的 Challenge，Challenge 1（MF1）与 Challenge 2（MF2）。MF1 可采用任何外部不限量的人脸数据来训练参赛算法；MF2 要求使用官方固定训练集 FaceScrub 和 FGNET 测试集进行训练。

##Abstract
* 摘要部分首先表明可以提取人脸判别性特征的CNN在FR中功不可没，在最近FR任务中为了提取更具有判别性特征，一些论文主要从loss函数上进行了改进（具体这些论文提出的方法会在后面逐一介绍）。本文从三个方面考虑并改进了FR：数据、网络结构和loss，并在公开的FR数据集上达到了state-of-art。    

##1、Introduction
论文首先介绍了影响人脸识别的三个重要的要素：   

* 第一个要素：训练模型的数据。
	* 列举现有的公开的数据集：VGG-Face, VGG2-Face, CAISAWebFace, UMDFaces, MS-Celeb-1M。有的数据集数量较小、MS和MegeFace虽数量较大但有一定的标记噪声和长尾现象。且因为数据是深度学习驱动的动力，工业界有比学术界更大量的数据，因此工业界FR的准确率始终比学术界要高。因此数据的质和量在FR中非常重要。   

* 第二个要素：网络结构和设置。  
	*  在FR任务中，使用诸如Res-Net、Inception-ResNet等网络结构能够得到比VGG-net、Google Inception V1等更加好的性能。同时，不同的应用场景也会使实际网络的部署在速度和准确率之间权衡。如移动端人脸验证的速度要求、十亿量级的安全系统的准确率要求等等。        
* 第三个要素：损失函数的设计。          
 	* 基于欧式距离裕量的损失  
 		* Deep Face（两篇论文）的方法使用Softmax分类层训练损失，然而基于分类的方法非常消耗GPU空间（因为全连接层对显存的消耗最大），而且对数据的样本的均衡和数据充足等有更高的要求。Centre loss、Range loss和Marginal loss 加入了压缩类内方差增大类间距离来提升准确率，但这些方法依然是组合softmax来训练识别模型。  
		* contrastive loss和Triplet loss使用“对训练”策略，对比损失函数由正样本对和负样本对组成，在梯度下降方法计算损失时，最小化anchor与正样本间的距离、最大化anchor与负样本间的距离。然而，对于以上这两种loss在选择有效的训练样本上很微妙（tricky）（主要体现在选择正负样本组对上）。  
	* 基于角度和cosine的距离裕量     
		* large margin Softmax（L-Softmax）提出通过加入角度乘法约束（对夹角乘以一个系数，同sphere face一样）来提升特征的判别性；sphere face（cos(m*theta)）应用L-Softmax并且将权重进行归一化，由于cosine 函数是非单调的函数，所以sphere face中使用分段函数来满足单调性，sphere face中通过组合softmax loss来促进和确保训练收敛。  
		* 为了克服sphere face收敛困难，AMSoftmax论文将角度裕量m移至cosine空间，这样实现和优化  additive cosine margin要比sphere face更加容易。对比基于欧式距离裕量的loss，基于角度和cosine裕量的loss明显在超球面流形空间上加入了判别约束，这也更符合人脸是一个流形曲面的先验。     
			 
* 本文在以上三个要素所作的工作：   
 	* 数据方面对MS1m数据进行了清洗；在网络结构上进行了很对对比尝试，实现速度与准确率之间的权衡；提出了新的loss 函数ArcFace 更具解释性，且在Megaface (最大的公开FR测试数据集)获得state-of-art的结果。具体后面介绍。     
 ##2、From Softmax to ArcFace   
* softmax loss  
![](https://i.imgur.com/56DO22s.png)     
* Weights Normalisation（权重规范化）   
为简单起见，将偏执项置为0，按照sphere face等的设置，将权重通过L2正则的方式进行规范化，使权重的模为1。    
![](https://i.imgur.com/UgJ8XzR.png)  
* Multiplicative Angular Margin （乘角度裕量，如Sphere face）   
 sphere face中通过将m乘以角度，引入角度裕量m。为了保持目标函数的单调性，限制L3公式中theta角度范围在[0 , π/m]。在具体实现中，为了避免加入的 margin(即 m) 过大，引入了新的超参 λ，和 Softmax 一起联合训练。    
![](https://i.imgur.com/WOJvu4D.png)     
  为了去除角度范围的限制，将cos(mθ)替换为分段单调函数 ，从而进一步公式化为：    
![](https://i.imgur.com/BKnIyqU.png)
* Feature Normalisation（特征规范化）    
 特征归一化之前已经广泛应用在人脸验证上，如L2范数归一化的欧式距离和cosine距离（以cosine距离计算为例：在计算特征间的距离时，先归一化所有特征，构建特征矩阵和对应的转置矩阵，再通过特征矩阵相乘的方式求得特征间的cosine距离），相关的论文从解析、几何和实验的角度分析特征归一化在度量学习中均有一定的作用。直观地将特征和模型权重进行归一化处理可以去除径向差异并且将每个特征的分布推到一个超球面上。  
论文中将特征向量以L2范数的方式规范化为s,论文中s的取值为64，将特征和权重都规范化后，可以得到特征规范化的sphere loss，定义为SphereFace-FNorm：   
![](https://i.imgur.com/uUsEQHE.png)      
* Additive Cosine Margin（加cosine裕量，如AMSoftmax）   
在论文Additive margin softmax for face verification和facecnn v1中，将角度裕量 m 从cos(theta) 中删除，因此他们提出的cosine 裕量损失函数为：
![](https://i.imgur.com/fb7SVh3.png)   
该论文的实验中设置cosine裕量m的值为0.35.与Sphere Face相比，加cosine裕量（Cosine-Face）有三个优势：（1）不需要技巧性的超参数即可极简单的实现；（2）没有softmax监督训练也可以收敛（3）明显的性能提升   
* Additive Angular Margin（加角度裕量）   
虽然cosine裕量与角度裕量从cosine空间到角度空间有一对一的映射关系，但这两种裕量仍然存在差异。事实上角度裕量比cosine裕量在几何上具有更加清晰的可解释性，并且角度空间的裕量可以直接对应到超球面流形上的弧度距离。    
本文在cosine（theta）中加入了角度裕量m,由于theta在[0，π − m]范围内时cos(theta + m)小于cos(theta),所以这样的限制对于分类任务更加直接。定义本文提出的ArcFace为：   
![](https://i.imgur.com/bfFfpOr.png)   
对应地：   
![](https://i.imgur.com/iA22nTA.png)    
不同裕量比较分析：  
将本文提出的加角度裕量的基本公式cos(theta + m)展开得cos(theta + m) =  cos(theta)cos(m) -sin(theta)sin(m),与加cosine裕量cos(theta) - m相比较,两公式大体类似，但提出的ArcFace的裕量是可以随着sin(theta)动态变化的。下图是本文给出的几何解释（我并没看懂比其他的裕量好在哪）   
![](https://i.imgur.com/5mobpgH.png)    
* 不同裕量损失在二值（两类）情况下的比较：   
![](https://i.imgur.com/QP9BPuT.png)     
* Target Logit Analysis     
作者通过画出目标分对数曲线，对softmax、cosine face、arcface loss性能提升进行分析(在一定范围内，目标分对数曲线比softmax越低，裕量惩罚越大，性能越好，但超出一定范围则相反)   
![](https://i.imgur.com/SMa9f9l.png)    
从上图中对sphere face 进行分析。（整体目标分对数值最大的曲线是softmax分布曲线），sphere face最好的设置是m=4,lambda= 5,其曲线与m=1.5,lambda=0相似，但sphere face的实现中m值为整型，那么当m由1.5变到m=2时，此时sphere loss不收敛，因此可以得出结论，当适当降低（分对数值变小）softmax的分对数曲线时增加了训练难度但网络性能得到了提升，但如果降低的太多则会导致网络不收敛。----m的值并不是越大越好    
对于cosine face和arcface 的分析。
由上图（a）cosineface 和arcface的分对数曲线可知，theta在[30，90]范围内时arcface的曲线低于sphere face，对应地裕量惩罚也就更大；而且从图（b）中也可以看出在训练开始时arcface的裕量惩罚也较大（红虚线低于蓝虚线）。theta在[0,30]cosine loss的裕量惩罚更大。     
分对数分析的结论：当theta处于[60,90]时加入过大的裕量回到时网络不收敛（如m=2,lambda=0），theta处于[30,60]时，加入裕量能够显著提升网络性能，原因是theta在这个范围内对应的是semi-hard negative samples（半难负样本）；当在theta在[0,30]时，添加margin裕量并不能获得明显的性能提升，原因是在这个区间对应的是最简单样本（容易分类的样本）。因此回看上图（a）中的对分曲线，在依据上述参数，theta在[30,60]间我们便可知为什么softmax、sphereFace、cosineFace到ArcFace性能提升原因。主要这里的theta角度---30度和60度为简单训练样本和难训练样本的粗略估计阈值。     
##3、Experiments    
本文在MegaFace（当前最大的人脸识别和验证的benchmark）上获得了state-of-art的准确率，将LFW、CFP、AgeDB作为验证集，并在网络结构的设计和loss函数的设计，在以上四个数据集上均取得了state-of-art。    

* Data    
	* Training Data    
		* VGG2:VGG2训练集包含8631个ID共324w图像，测试集包含500ID共169396图像。该数据集包含了各种姿势、年龄、光照、种族等数据，因为该数据集质量很高，所以本文直接拿来训练，没有进行清洗。
		* MS-Celeb-1M：原始的MS1M包含10wID共1000w图像，为了获得高质量的图像本文对该数据集进行了清洗，最终获得8.5W个ID共380w张图像。清洗后的数据已公开，但清洗的代码没有公开。具体的清洗过程为：计算同一个ID下的所有图像与ID中心（代表ID的图像）的距离并排序，将距离远里ID中心的图像通过设定阈值自动删除；然后对每一个ID下的阈值附近的人脸图片进行人工的check，进行进一步的确认和清洗。----该数据的清理方式，我在时间数据清理是也用到了类似的方法（类内清洗）：并不是指定ID下某一张图像为ID的中心，而是将每一张图像分别与余下所有图像的特征相互比较，然后将该图像与所有图像的比分求其平均值作为该图像与ID中心的距离。    
	* Validation data（人脸验证数据集）   
		* LFW：包含5749ID共13233张来自网络收集的图像。按照“无限制的户外标签数据”的标准测试协议，本文在6000对**人脸验证**上进行了准确率测试。    
		* CFP：该数据集包含500个主题，每个主题下包含10张正脸和4张侧脸的图像。该数据集的评估协议包含正脸-正脸（frontal-frontal，FF）和正脸-侧脸（frontal-profile，FP）**人脸验证**。本文使用最具由挑战性的FR协议来评估性能。 
		* AgeDB:该数据集是收集自室外的数据集，在数据在姿势、表情、光照和年龄等变化较大。包含440个子主题（男演员、女演员、作家、科学家、飞行员等）共12240张图像，最大年龄101最小年龄3，每个子主题平均年龄范围是49年。测试集分为四组分别为四种年份间隔（5年、10年、20年、30年），本文选用最具挑战性的组AgeDB-30做性能评估，该数据集的**人脸验证**协议与LFW相同。  
	* Test data（人脸鉴别数据集，1 比 N ）  
		* MegaFace: (人脸识别测试数据集非人脸验证测试)，该数据集包含注册集（gallery）和探测集(probe)(两者的区别和关系在sphere face中介绍过)，其中注册集为采自雅虎旗下Flickr网站的69w人的100w张图像；probe（探测）集是两个现成的数据集FaceScrub和FGNet。FaceScrub是一个公开的数据集，包含530人共10w张照片，其中由5.5w张男性照片，5.2w张女性照片；FGNnet是一个面部老化数据集，共82ID下共1002张图像，每个ID下的多张人脸年龄从1-69岁不等。  
		* 对MegaFace测试集的清洗：由于MegaFace数据集的数据量之大，噪声不可避免，本文对Mageface数据集的百万干扰集（gallery注册集）和probe下的Facescrub进行了类内清洗（清洗过程与训练集清洗相同）。从作者给出的清洗前后的CMC曲线和ROC曲线看，清洗后准确率明显提升。   
* Network Settings    
	* 超参数设置：本文通过MxNet实现，在4或8卡的Tesla P40（24G）上以batchsize为512进行训练，初始学习率0.1，分别在迭代10，14、16w次时学习率处以10，共迭代20W次。momentum设置0.9，权重衰减设置为5e-4。  
	* Input setting    
	如同sphere Face那样，本文通过MTCNN检测出的5个人脸关键点（眼中心、鼻尖和嘴角）进行相似变换（平移、旋转和放缩）来规范化（有时翻译成归一化）人脸。最后人脸抠取并resize到112 * 112大小。对于像素值规范化的方式为：将[1,255]的图像减127.5再处以128。   
	对于大多数再ImageNet上的分类神经网络输入图片的大小一般是224 * 224甚至更大，因为本文抠取的人脸图像为112 * 112，为了保持更高特征图的分辨率，本文将第一个卷积层从conv7 * 7\stride=2变为conv3 * 3\ stride=1,这样最终卷积网路的输出由3 * 3变为7 * 7（调整卷积后的网络名前加L）。     
	* Output setting    
	在神经网络的最后几层，作者提供了一下几个选项来研究如何进行特征嵌入才能使模型的性能最好。除了Option A外，所有特征嵌入尺寸为512维，而Option A的嵌入特征的维度由最后一层卷积的通道数决定。   
	Option A:使用 全局池化（GP）    
	Option B:使用 GP-->FC（全连接）   
	Option C:使用 GP-->FC-->BN（Batch Normalisation）    
	Option D:使用 GP-->FC-->BN-->PReLu     
	Option E:在最后的卷积层后直接使用 BN-->Dropout-->FC-->BN
	* Block Setting  
	除了原始的ResNet残差块单元，本文提出了改进后的残差块（Improved Residual,在模型名后指定 IR 标识），该残差块由BN-Conv-BN-PReLu-Conv-BN 结构组成。如下图所示，与原始的ResNet相比 ，本文将PRelu替换了原始的Relu，并且将残差块中的第二个卷积层的卷积步长由原始的1变为2。   
	![](https://i.imgur.com/XywWSva.png)   

	* Backbones  
	基于最近提出的性能先进的模型结构设计，本文在人脸识别的骨干网络分别在MobileNet、InceptionResnet-V2、DenseNet、Squeeze and excitation networks
    (SE)、Dual path Network (DPN)网络上进行了探索。本文中从准确率、速度、模型大小三方面比较了以上主干网络的性能。    
	* Network Setting Conclusions   
		* Input selects L.作者通过对比实验，选择网络输入第一层卷积为conv3 * 3\ stride=1，网络输出特征图大小为7 * 7时，在各个数据集上的人脸验证准确率最高。    
		* Output selects E.神经网络的最后几层选择Option E能使特征嵌入达到最优，得到最高的准确率。   
		* Block selects IR. 通过实验表明改进的残差块（IR）比原始的残差块性能更好。    
		* Backbones Comparisons.下表为不同骨架网络在人脸验证集上速度、准确率和模型大小的比较，作者基于以上三个因素的权衡，最终选择LResNet100E-IR网络在MegaFace数据集上进行测试。（注：LResNet100E-IR表示网络input选用L，output选用option E,使用改进(IR)的resNet100网络）    
		![](https://i.imgur.com/apTCpjw.png)      
* Loss Setting   
本文的提出的arcface loss是加入角度裕量，作者将角度裕量从0.2到0.8进行尝试，最终选用最优的m = 0.5作为最终值，本文还对比了arcface与sphere face 、cosine face的性能，同等条件下，Arcface虽然比cosine提升了一点点（如下图），但arcface从几何解释和直观上更加有说服性。
![](https://i.imgur.com/SARCRw8.png)     

*  MegaFace Challenge1 on FaceScrub   
  在MegaFace数据集上，本文基于是否做训练集MS1M清洗做了对比，结果显示清洗后得到了明显的效果。如下图分别显示了在该数据集下人脸鉴别和人脸验证的准确率：   
![](https://i.imgur.com/nX9eTmi.png)    
* Further Improvement by Triplet Loss  
   （**Triple Loss 说明**：相比 Softmax，其特点是可以方便训练大规模 ID(百万，千万) 的数据集，不受显存的限制。但是相应的，因为它的关注点过于局部，使得性能无法达到最佳且训练需要的周期非常长。）	     
   由于GPU存储的限制基于softmax的方法（如sphereFace、Cosine Face、ArcFace）很难训练百万级别ID的人脸数据。一个实际的解决方案是使用度量学习方法，且最广泛应用的方法为Triple Loss。但Triple Loss收敛速度较慢，因此，本文采用Triple Loss来finetune 基于softmax方法训练好的模型。   
   本文在使用Triple Loss微调的实验中，本文使用LResNet100EIR 网络，设置学习率为0.005，momentum为0，权重衰减为5e-4.作者给出了对比实验，其中softmax loss微调后提升最大，同时也说明了（1）两阶段模型训练的有效性（基于softmax + triple loss 微调），（2）局部的度量学习可以与全局的超球面度量学习互为补充，共同提升模型性能。       
##4、 Conclusions   
重申了本文的贡献：数据清洗、模型提出（Improved ResNet）、提出新Loss（ArcFace）并达到了state-of-art的准确率。























 		   

   


</size>