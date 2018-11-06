<center> 
#2018-ECCV-Joint 3D Face Reconstruction and Dense Alignment with Position Map Regression Network（PRNet）
2018/9/13 16:09:26  ; by llpspark
</center>
论文链接：[点我](https://arxiv.org/abs/1803.07835)  
代码链接：[点我1](https://github.com/YadiraF/PRNet)    
相关博客：[点我1](https://blog.csdn.net/linmingan/article/details/79657327#comments)， [点我2（该链接系列都很好）](https://www.52cv.net/?p=644)  ，[点我3](https://www.jianshu.com/p/c5e6820a599a?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation) ，[点我4](https://www.jianshu.com/p/b460e99e03b0)      
  
##预备知识：   
* UV图与UV展开：[链接点我](http://geometryhub.net/notes/uvunfold) （该链接博主的系列文章都很好）   
* 点云数据（point cloud）：[链接点我](https://www.cnblogs.com/mazhenyu/p/8287785.html)：通过雷达，激光扫描，立体摄像机等三维测量设备获取的点云数据，具有数据量大，**分布不均匀**等特点，作为三维领域中一个重要的数据来源，点云主要是表征目标表面的海量点的集合，并不具备传统网格数据的几何拓扑信息，所以点云数据处理中最为核心的问题就是建立离散点间的拓扑关系，实现基于邻域关系的快速查找。   
* 迭代最近点(ICP)算法 ：[连接点我](https://blog.csdn.net/Dstar2/article/details/68066739)     
* ICP算法涉及到最小二乘法相关：[链接1](https://blog.csdn.net/zkw12312/article/details/78783939)；[链接2](https://blog.csdn.net/monsterhoho/article/details/46753673?utm_source=blogxgwz0)
* 关键点检测 **!=** 人脸对齐:[链接](https://www.cnblogs.com/cv-pr/p/5438351.html)



<font size=3>    

##Abstract    
* 作者提出了一个直接地同时重建3D人脸并进行稠密3D人脸关键点检测（对齐）的方法，作者主要通过将3D模型通过2D形式的UV Positoin map(由UV参数曲面转换得到）进行表达，然后通过简单的卷积神经网络由单一2D图像作为输入，得到的输出UV Position map(位置图)做回归训练（网络输出为UV position map）。在网络训练时将weight mask 融入到loss函数中从而提升网络性能。该方法不依赖任何人脸模型先验知识，并且可根据语义完全地重建面部几何形状。提出的方法轻量且快速（9.8ms/img）,在人脸重建和关键点检测（对齐）上达到了state-of-art。  


##Introduction    
* 3D人脸重建和人脸对其是计算机视觉中两个基础且强相关的任务。起初人脸对齐旨在检测出人脸中的2D基准点以便作为人脸识别和辅助3D人脸重建等任务的前提。但在2D人脸对其中会出现一些困难，如处理大姿态或遮挡问题。随着CNN在CV的应用，一些研究者使用CNNs来估计3D MM（Morphable Model）的参数或3D模型的扭曲函数 从2D图像复原相应的3D信息。然而，由于人脸模型理论或模板所定义的3D空间的局限性，以上方法的性能受限。
* 最近，两个端到端的工作（一个是VRNet,另一个是How far are we from solving the 2D & 3D Face Alignment problem? ）规避开了模型空间导致的局限性（避开3DMM），并在相应的任务上达到了state-of-art性能。论文（How far are we from solving the 2D & 3D Face Alignment problem?）从一张图像中通过复杂的网络回归68个人脸关键点的2D坐标，但需要一个额外的网络估计深度值，此外，该方法不提供稠密的对齐（关键点检测）。论文VRNet提出了通过体素（Volumetric）表示3D人脸，并使用一个网络从2D图像中回归体素。然而，这种表示丢弃了点的语义信息，因此网络为了复原人脸形状需要回归整个体积，而人脸形状只是整个体积的一部分。因此这种表示限制了恢复形状的分辨率，并且需要一个很复杂的网络来回归它。作者发现这种限制在之前的model-based（3DMM）方法中是不存在的，基于此痛点，作者提出了本文不基于model(3DMM)并可以同时进行3D重建和稠密对齐的算法。    
* 概括本文的contributions：
	* 第一次解决了不受低维的解空间限制 以端到端的形式同时3D人脸重建和人脸对齐。  
	* 为了能够直接地回归3D面部结构和稠密关键点，作者提出了新的表示--称之为UV位置图（注意与UV纹理图区分，是UV纹理图的转换（R,G,B替换为x,y,z）），该UV位置图记录了3D人脸的位置信息并且在UV空间中为每个点提供了稠密的语义对应。    
	* 在训练时，作者提出了将加权的mask指定到UV位置图的每一个点上，从而计算加权的loss。通过加权loss的设计提升了网络的性能。   
	* 框架轻量，速度可达100FPS。    
	* 在AFLW2000-3D 和 Florence数据集上比当前state-of-art方法（VRnet和How far are...）在人脸重建和稠密对齐性能提升至少25%。   

##Related Works   

###2.1、3D Face Reconstruction   
* 自从1999年Blanz and Vetter提出3DMM，在单目3D人脸形状重建上一直非常流行。最早的方法是通过建立输入图像和3D关键点、局部特征的对应关系，然后求解非线性优化函数来回归3DMM的系数。但这种方法严重依赖关键点和其他特征点的检测器，因此一些方法开始使用CNNs来学习输入图像和3D模板的对应关系，然后通过预测稠密的约束来计算3DMM参数。最近的一些工作也开始利用CNN来直接预测3DMM参数进行3D人脸重建。然而以上这些3DMM的方法的主要障碍是均为model-based的，生成的3D几何是在约束的几何空间下通过估计出的参数进行3D mesh处理得到的，这导致生成的3D几何空间受限。  后来的一些方法虽然避开了通过3D shape basis的方式，但是需要通过3D面部模板，这也同时需要学习一个3D Thin Plate Spline(TPS)扭曲函数来重建几何形状。最近VRNnet提出了直接预测3D重建的方法，本文不同于该方法从新的角度同时进行3D人脸重建和人脸对齐。   

###2.2、Face Alignment    
* 人脸对齐最初是定位2D人脸的一些关键点，比较典型的方法有经典的Active Appearance Model(AMM)方法、Constrained Local Models(CLM)方法，后来出现了级联回归方法和基于CNNs的方法。但是2D人脸对齐在大姿态人脸条件下（并非正脸）条件下描述人脸形状遇到困难。由此3D人脸对齐解决了这一困难。3D人脸对齐最初通过2D人脸图片上拟合3DMM或者注册3D面部模板完成，后来[How far are we from solving the 2d and 3d face alignment problem?]通过CNN预测heat map来得到3D对齐人脸并达到了state-of-art效果。   

##Proposed Method   
###3.1 3D Face Representation    
* 论文的目标是与输入单一的2D图像建立稠密的对应关系来回归3D面部几何，因此需要一种可以通过神经网络直接预测的合适的3D面部表示。简单且普遍的用法是用一个1D向量来表示，即将3D点信息用一个向量来表示，然后用网络预测；然而，这种方法丢失了空间信息。此外也会很自然地想到通过神经网络的全连接层预测对应点的坐标输出，但FC层大大增加了网络的大小，并且很难训练。当然，有人通过将FC层最大输出点的数量设置为1024来通过神经网络实现直接对点的预测，但1024个点对应精准的3D建模远远不够。相关研究中也有预测3DMM等模型的系数，然后同坐模型建模来得到3D点云，但这些方法太过依赖3DMM模型，并且流程复杂；最近的VRN用Volumetric来表示，成功摆脱了上述问题，但是其网络需要输出192x192x200的一个Volume，要重建的3D shape只是预测的体素的一部分，计算量相当大，重建分辨率将会受到限制。    

为了解决上述工作种的问题，作者提出了UV位置图作为整个3D面部结构的表示。UV位置图（或称位置图）是将3D位置信息在2D UV空间进行存储的图，其主要目的是参数化3D空间到2D。UV空间或UV坐标系在近几年就已经提出了，并应用在表达3D人脸纹理（就是常用的UV纹理图）、高度图（2.5D 几何）和3D面部 网格对应等。与以往不同的是作者通过UV空间来存储3D人脸模型的3维点坐标，亦可以简单地理解：UV位置图是使用x,y,z坐标替换了UV纹理图中的r,g,b值。     
<center/>
![](https://i.imgur.com/c7s4ixw.png)
</center>
如上图，左图是输入图像的3D图和3D点云ground-truth；右边第1行，分别是2D图像，UV文理映射图，相应的UV位置映射图；右边第2行，分别是UV位置映射图的x，y，z通道。（实际上UV 位置图最初来源于3dmmasSTN，与3DDFA中的PNNC有类似的功能，二者详细内容及区别请参见这两篇论文介绍。）     

* 为了保存位置图中的语义信息，作者基于3DMM构建UV坐标（3DMM的介绍请参考另一篇3DMM的解读）。那么如何构建的坐标系呢，由于3DMM的点有5w多个，于是本文选择256*256（共65536）的位置图与之进行对应，这样可以忽略掉微不足道的重采样（为什么叫重采样，因为图像的高、宽都发生了改变）错误而获得高精度的点云。在训练时采用的是300W-LP数据集，300W-LP数据集是一个包含60k无约束图像的且每张图像均拟合了3DMM参数的数据集，该数据集也非常适合生成训练对。此外，该数据集的3DMM参数是基于[Basel Face Model(BFM)](https://gravis.dmi.unibas.ch/publications/2009/BFModel09.pdf)的（即有形状和纹理参数），为了充分使用该数据集，本文将参数化的UV坐标对应到BFM。具体过程没懂（下边这句话）：
![](https://i.imgur.com/r82MDdz.png)

###3.2 Network Architecture and Loss Function    
PRN的结构如下图：   
<center/>
![](https://i.imgur.com/K1JFSDt.png)
</center>
网络输入为 256 × 256 × 3的RGB图像输出为 256 × 256 × 3的位置图。论文采用encoder-decoder的结构进行对等学习。encoder结构由1个卷积层+10个残差块构成，encoder结构的输出为8 × 8 × 512的特征图。 decoder网络结构由17个转置卷积构成，最终生成256 × 256 × 3的位置图。所有卷积和转置卷积的卷积核均为4*4，使用ReLU激活。   
为了学习网络参数，本文提出了新的损失函数（基于区域加权的MSE）。Mean square error (MSE) 对所有像素点的学习是均等的，而人脸的中间区域要比其他区域具有更有判别性的特征，因此，本文提出使用权重mask来改进MSE。    
<center/>
![](https://i.imgur.com/H4a4WUC.png)
</center>
如上图，最右图为权重mask，根据判别性大小将图片分为以下4个子区域：子区域1（68个关键点），子区域2（眼睛、鼻子、嘴），子区域3（其他人脸区域），子区域4（脖子），且其权重比例为16：4：3：0。     
那么对应的加权后的MSE为：
<center/>
![](https://i.imgur.com/EdyN3hg.png)
</center>
###3.3 Training Details   
论文使用选择例如[300W-LP数据集](https://drive.google.com/file/d/0B7OEHD3T4eCkVGs0TkhUWFN6N1k/view)来生成训练数据，因为该数据集包含标有3DMM参数的不同角度的人脸图像，因此从该数据集中很容易得到3D点云数据。具体地，首先按照ground truth bounding box从图片中抠取人脸并将其rescale到256 × 256，然后利用标记好的3DMM参数生成对应的3D位置，并将其渲染到UV空间从而得到ground truth UV位置图。训练时的位置图大小也为256 × 256，这就可以将多于45k个点进行准确地回归训练。值得一提的时，尽管训练数据是通过3DMM生成的，但网络输出的位置图并不会收到任何人脸模板或3DMM线性空间的限制。  当然作者也提出，可以采用其他的数据集来训练，那样的话可能就不需要3dmm模型等相关的处理技巧，反正无论如何，流程都是：得到3D点云-> 插值形成uv位置图->训练网络这个步骤。只是得到3d点云的方式不同而已。     
论文通过在2D图像平面上随机旋转、翻转目标人脸进行数据扩增。具体地，对目标人脸在（-45，45）范围旋转，随机以输入尺寸的10%平移目标人脸，以（0.9，1.2）范围内的比例放缩人脸。为了处理遮挡情况的图像，作者通过向原图项中加入纹理噪声来合成遮挡。通过以上数据扩增工作，生成的数据集覆盖了所有不同的情形。    
训练使用Adam优化器，lr以0.0001开始，并每5个epoch衰减一半。batchsize为16，使用Tensorflow实现。（作者代码功底算是算法领域很好的水平，代码无论是网络实现，还是api接口，都非常简洁易懂，并且完全用python实现了3ddfa，3dmmasSTN中相关处理的matlab代码，大大的佩服。）    
##Experimental Results  
该部分通过3D人脸对齐和3D人脸重建来评估提出算法的性能。   
###4.1 Test Dataset    
* **AFLW2000-3D**：AFLW2000-3D数据集是评估非限制条件下3D人脸对齐的挑战数据集。该数据集包括最初AFLW数据集中的2000张图像加上后来拓展出的拟合好的3DMM参数标签和68个3D关键点。本文使用该数据集评估对齐和重建结果。   
* **AFLW-LFPA**：AFLW-LFPA数据集是AFLW数据集的另一个拓展集。该数据集是从AFKW数据集中按照姿态挑选了1299张图像，使这些图像中的人脸的偏离角度具有平衡的分布。此外，在该1299图像上，将每张图像仅有的21个可见关键点基础上增加13个关键点，最终获得该数据集。本文通过该数据集中的ground truth 34个关键点来评估3D人脸对齐任务。   
* **Florence**：Florence数据集包含53个主题，并且其ground truth 3D网格是由结构光扫描系统获得。使用该数据集评估然连重建性能。   
###4.2 3D Face Alignment  
为了评估人脸对齐性能，本文使用Normalized Mean Error(NME)来评估度量，bounding box的尺寸作为归一化因子（loss除以bounding box的像素数）。    
首先在68个面部关键点上评估提出的方法，并且在AFLW2000-3D数据集上与3DDFA、DeFA 和 3D-FAN方法做了比较。结果如下图所示（Cumulative Errors Distribution,**CED曲线**，即累积误差分布曲线），当计算2D坐标下与每个关键点距离时提出的方法略高于当前最好的3DFAN，当将深度值纳入比较范畴，提出的方法和3D-FAN的性能差异变大。其值得注意的是，3D-FAN需要额外的网络来预测关键点的Z坐标，而本文的方法直接就可获得。   
<center/>
![](https://i.imgur.com/RRBpjVT.png)
</center>
为了进一步论证提出的方法在不同姿态和数据集下的性能。作者在AFLW2000-3D数据集下分别在小、中、大偏离角度进行NME评估，并同时在AFW2000-3D和AFLW-LPFA数据集下计算了平均NME。数据见下表：
<center/>
![](https://i.imgur.com/zmDhXqm.png)
</center>
作者提到，AFLW2000-3D 数据集的ground truth是备受争议的。所以作者可视化了提出方法检出的关键点和ground truth关键点，可以发现本文的方法比ground truth更准确，见下图。    
<center/>
![](https://i.imgur.com/cOkcMKH.png)
</center>   
###4.3 3D Face Reconstruction    
本文在AFLW2000和Florence数据集上对人脸重建进行了评估。
在评估3D重建性能，首先使用ICP（迭代最近点）算法发现网络输出和ground truth点云对应最近点的匹配，然后计算对应的NME(normalized by outer
interocular distance of 3D coordinate)。结果如下图：
<center/>
![](https://i.imgur.com/ID31Dhi.png)
</center> 
如上图所示，提出的方法远超当前最好的算法。由于AFLW2000-3D数据集重建标签是通过3DMM参数拟合得到的，所以作者进一步在Florence数据集上进行了性能评估，该数据集的ground truth 3D点云是由结构光3D扫描系统获得的。   
为了更好地评估不同姿态下提出的算法3D重建的性能，作者在不同偏斜角度下分别计算了NME。如下图的CED(累积误差曲线)所示，显然提出的方法更稳定，更好：      
<center/>
![](https://i.imgur.com/70vSi2V.png)
</center> 
### 4.4 Runtime   
本文的模型轻量（160M），而VRN1.5G，且运行速度超快，如下表所示：    
<center/>
![](https://i.imgur.com/pcVZW2B.png)
</center> 
### 4.5 Ablation Study（消融研究，即控制变量证明参数性能）    
该部分的消融实验，主要通过控制不同mask权重的比例最终证明最终使用的比例的有效性。具体比例设置如下图：     
<center/>
![](https://i.imgur.com/9nLFrCW.png)
</center> 
具体不同比例的实验结果如下图：    
<center/>
![](https://i.imgur.com/NK708WN.png)
</center> 

##5 Conclusion   
本文提出了端到到的同时3D人脸对齐和3D重建的方法。性能好，速度块。





</size>    