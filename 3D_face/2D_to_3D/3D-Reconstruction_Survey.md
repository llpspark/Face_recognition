<center> 
#3D-Reconstruction-Survey  
2018/9/11 10:40:42 ; by llpspark
</center>
<font size=3>    
##写在前面：
按照3D人脸重建的发展的里程碑（不同类型）：     

*  1、基于Statistical shape representations的3DMM重建（统计数据集中3D人脸形状分布并将其表示在一个子空间，重建时在这个子空间搜索与输入图像相似的表示进行重建，该方法基本不实用，不列举论文）。
*  2、Scene assumption methods。输入图片的场景和角度进行估计。一些方法采用光源、脸部反射，脸部对称性等信息来进行估计，如Shape fromshading method。但是，这类估计在现实中不适用，不列举论文。    
*  3、Example based methods（或者说3DMM类）。按照输入图片来调整模板3d人脸。    
*  4、Landmark fitting method。由2D图像直接进行关键点检测并重建3D人脸（VRN和PRN）。
##预备知识：   
* UV图与UV展开：[链接点我](http://geometryhub.net/notes/uvunfold) （该链接博主的系列文章都很好）  
##说明：survey的主线按照开源和未开源，并以大致时间先后排序    

##1、人脸三维重建(开源)     

* **1999-SIGGRAPH-A Morphable Model For The Synthesis Of 3D Faces（3DMM重建开山之作）**   
	* 论文链接：[点我](https://www.cs.cmu.edu/~efros/courses/AP06/Papers/Blanz-siggraph-99.pdf)   
	* code:[点我](https://github.com/YadiraF/face3d)  
	* 相关博客：[点我](https://blog.csdn.net/likewind1993/article/details/79177566)   
	* 方法类型：典型的基于统计的三维建模方法(3DMM类)
	* 方法：  
		* 通过一个人脸数据库构造一个平均人脸形变模型，在给出新的人脸图像后，将人脸图像与模型进行匹配结合，修改模型相应的参数，将模型进行形变，直到模型与人脸图像的差异减到最小，最后完成人脸建模。  
		* 通过统计分析方法明确地学习了3D人脸的先验知识。它表示的三维人脸是基本三维人脸的线性组合，由主成分分析(PCA)在一组密集排列的3D人脸上得到。将三维人脸重建问题看做是模型拟合问题，
	* 实现方式：
		* 主要分为两阶段计算过程：
			* 构建平均的脸部模型
			* 形变模型与照片的匹配   
	* 特点：
		* 3维人脸重建的里程碑，很多论文是基于该工作进行小调整实现改进的。
		* 重建结果往往都接近平均模型，缺少个性化特征，进而效果收到制约。


* **2015-中科院+刘晓明-Face Alignment Across Large Poses: A 3D Solution(3DDFA）**       
	* 项目页：[链接](http://www.cbsr.ia.ac.cn/users/xiangyuzhu/projects/3DDFA/main.htm)       
	* 代码链接：官方Matlab 代码，[pytorch复现](https://github.com/cleardusk/3DDFA)       
	* 论文链接：[点我](https://arxiv.org/pdf/1511.07212.pdf)       
	* 方法类型：将深度神经网络用在3DMM的参数预测上（取代传统的迭代优化形状和纹理参数--过慢），是3DMM方法在神经网络上的变种，通过该论文方法生成的       

* **2017年-英国帝国理工学院 James Booth团队在3D人脸重建上的姊妹篇**     
	* 说明：效果在2017年发表时达到了state-of-art，并得到了science报道   
	* 相关资料：[点我](http://chuansong.me/n/1804520051536)
	* 方法类型：第一篇是基于3DMM方法；第二篇是基于第一篇中得到的数据驱动的2D转3D。
	* **IJCV-Large Scale 3D Morphable Models**     
		* 论文链接：[点我](https://link.springer.com/article/10.1007/s11263-017-1009-7)  
		* code:[点我](https://github.com/menpo/lsfm)   
		* 方法：本文主要创建大规模人脸模型（LSFM），包含不同种族、年龄的人脸，实现了由扫描数据到3D人脸建模的算法。   
		* 方法说明：   
			* 该论文主要是将扫描出的人脸图像通过提出的算法进行3DMM建模（输入并非2D图像）   
			* 全自动构建大型 3DMM 流程：（1）基于综合呈现视图进行自动标记。（2）在自动标记的引导下，3D 模型不断迭代变形，以精确匹配数据集的每个 3D 面部网格。（3）构建初步的全局 PCA，（4）自动删去错误的对应。（5）由剩余的干净数据构建 LSFM 模型。图像描述如下：
			
			<center/>
			![](https://i.imgur.com/haEfdLI.png)
			</center>
   
			* 个人认为本质讲该工作是通过提出的算法构建了一个大规模的3D人脸模型库，使3D可变模型在调整时有更加丰富的组合，再加上算法中提出的3DMM模型调整算法使重建人脸比以前的质量更高。      
	* **CVPR-Face Normals “in-the-wild” using Fully Convolutional Networks**    
		* 论文链接：[点我](http://openaccess.thecvf.com/content_cvpr_2017/papers/Trigeorgis_Face_Normals_In-The-Wild_CVPR_2017_paper.pdf)    
		* code:[点我](https://github.com/trigeorgis/face_normals_cvpr17)  
		* 方法：利用 上文（LSMM）合成的 10,000 张人脸作为训练数据，通过深度学习将任意（casual）2D 快照转换为精确的 3D 人脸模型。

* **2017-CVPR-Regressing Robust and Discriminative 3D Morphable Models with a very Deep Neural Network（3DMM_CNN）**    
	* 论文链接：[点我](https://arxiv.org/abs/1612.04904)   
	* code:[点我](https://github.com/anhttran/3dmm_cnn)   
	* 相关资料：[点我](https://zhuanlan.zhihu.com/p/24316690)   
	* 方法类型：3DMM类（cnn 回归参数）
	* 实现方式：
		* 通过传统方法构建3D人脸训练集（同一个人多张图像）
		* 对同一个人的每一张图像构建shape和纹理特征参数
		* 训练模型模型时使用同一个体的多张图片和单个pool的3DMM进行监督训练，使模型可以根据同一个体不同的图片来生成类似的3DMM特征向量。   
		* 使用非对称的MSE	进行监督训练  
		* 文章直接使用预测出的3DMM参数最为人脸特征进行人脸识别应用，作者说可以达到与2D图像相媲美的效果，网上很多人评论说与	2D效果有差距。    
	* 特点：使用cnn预测3DMM参数，并将预测出的3DMM参数作为人脸特征用于人脸识别。   
	* 备注：可尝试  

* **2017-ICCV-Large Pose 3D Face Reconstruction from a Single Image via Direct Volumetric CNN Regression（VRNet）**    
	* 论文链接：[点我](https://arxiv.org/abs/1703.07834)
	* code:[点我](https://github.com/AaronJackson/vrn)  （基于Torch-Lua）   
	* 方法类型：神经网络端到端（预测Volumetric） 
	* 方法：
		* 论文提出二种方法实现人脸三维重建，第一种是直接通过沙漏网络（HG）图片端到端重建重建，第二种方法通过迭代沙漏网络生成68个标记点，再将生成的标记点融合到输入图像中，再次通过堆叠的沙漏网络进行人脸重建。此外论文还提出重建3D人脸的同时进行人脸关键点预测。
	* 实现方式： 该方法对单个2D图像的3D面部几何进行体积表征的直接回归（regression）。 首先提出基于沙漏网络端到端地得到相应输入人脸的特征点，然后融合得到的特征点，通过堆叠的沙漏网络进行3D体素估计，最终得到重建后的3D人脸。作者具体采用的三种架构如下图：

	<center/>
	![](https://i.imgur.com/r5wbQiY.png)
	</center> 
	* 备注：最火，3.1k-star；可尝试。 

* **2018-ECCV-Joint 3D Face Reconstruction and Dense Alignment with Position Map Regression Network（PRNet）**    
	* 论文链接：[点我](https://arxiv.org/abs/1803.07835)
	* code:[点我1](https://github.com/YadiraF/PRNet)     
	* 方法类型：神经网络端到端（预测Position Map） 
	* 相关博客：[点我](https://blog.csdn.net/linmingan/article/details/79657327#comments)， [点我2（该链接系列都很好）](https://www.52cv.net/?p=644)  ，[点我3](https://www.jianshu.com/p/c5e6820a599a?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation)
	* 方法：论文同时预测人脸特征点和3D mesh的顶点坐标，论文实现了通过神经网络直接预测3D mesh的定点坐标（应该是首次，其本质为通过UV图建立2D人脸和3D人脸的映射关系）。   
	* 实现方式：
		* 开创性地通过UV图对3D mesh进行映射，使顶点坐标可通过cnn进行预测。   
		* 通过神经网络以预测特征图的形式对mesh进行预测   
		* 为了使预测出来的mesh更有意义。他们在计算损失函数的时候，对不同区域的顶点的误差进行加权
	* 备注：可尝试 
	
		

##2、人脸三维重建(未开源)    
* **2015-arxiv-On 3D Face Reconstruction via Cascaded Regression in Shape Space(川大-刘峰)**    
	* 论文链接：[点我](https://arxiv.org/abs/1509.06161v3)     
	* 方法类型：3DMM+CNN回归   
	* 方法：传统的3D重建问题解决方法是模型匹配(model fitting)，本文将3D重建问题建模转换成回归问题。    
	* 论文提出的重建过程：
		* 先选定一个初始的3D形状S0（这里用训练集的平均形状），然后根据2D图片上的特征点使用回归不断调整3D形状，最后使得3D到2D的投影上的特征点和原始图片相符。本质上先选定初始3D形状，通过回归不断调整形状。   
		* 这篇文章不涉及2D人脸关键点检测，用到的2D人脸关键点都是预先检测好的。

* **2016-ECCV-Joint Face Alignment and 3D Face Reconstruction with Application to Face Recognition（川大-刘峰）** 
	* 论文链接：[点我](https://arxiv.org/abs/1708.02734)   
	* 相关博客：[点我](https://mp.weixin.qq.com/s/udr3573GXQOOF46jLriekg)     
	* 3DMM+CNN回归 
	* 方法：本文是作者在之前Cascaded Regressor论文的基础上，将二维人脸图像特征点检测（即人脸对齐）与三维人脸重建过程耦合起来，在回归的框架下同时实现这两个任务，此外，作者还将人脸表情、姿态归一化融入到3D建模中。   
	* 算法整体框架如下图：
<center/>
![](https://i.imgur.com/MkbaFc1.png)
</center>


  

</size>    