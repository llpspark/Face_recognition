# PRNnet工程代码指南   
* code:[点我](https://github.com/YadiraF/PRNet)       



## 代码解析    

*  run_basics.py   
	* 功能：测试论文给出的示例图像，进行3D重建测试（图像的68个关键点已经求出，直接加载即可）     
	* 基本流程：    
		* 初始化PRN网络（通过调用api.py的PRN类）   
		* 加载测试数据和对应图片的关键点（此处的关键点用于抠取图像中的人脸）    
		* 通过PRN网络进行POS图预测     
		* 通过得到的POS图得到对应图像的3D关键点、3D定点坐标、对应3D坐标的色彩    
		* 保存3D模型    

* demo.py    
	* 功能：加载测试图片，进行3D重建、3D关键点检测、纹理编辑、深度图预测等功能测试。    
	* 基本流程：    
		* 初始化PRN网络（通过调用api.py的PRN类）   
		* 加载测试数据并对测试图片进行预处理，预处理工作包括：
			* 如果图像最长边大于1000，则等比例放缩到长边为1000    
			* 检测并对齐：检测出的人脸图像如果是等边长则直接resize到网络输入尺寸（256*256），如果是矩形则通过**相似变换**，将检测出的人脸变换到网络输入尺寸     
			* 对齐后的图像通过PRN网络，预测Pos图，并将Pos图通过逆相似变换，对应到对齐前的人脸图像        
			* 通过得到的Pos图，求出对应的3D定点坐标、获得3D纹理图（色彩值）、深度图、关键点、估计姿态等，其中纹理图的获取：以得到Pos图的x,y对应坐标作为cv2.remap函数分别在x,y方向的映射坐标位置，由输入图像的像素重映射出纹理图。     

* api.py  
	* 功能：通过定义PRN 类实现PRN网络的相关操作（模型加载、网络传播、图片预处理（检测和对齐））    
	* 类成员：
		* 初始化工作：加载PRN预测模型，加载UV文件（关键点位置index文件、人脸位置索引文件、三角形网格文件）     
		* 获取UV图中人脸位置对应的3D人脸位置坐标    
		* 使用dlib检测人脸   
		* 网络前向传播   
		* 对图像进行预处理：检测和对齐，具体过程：
			* 通过关键点定位出最大bbox（可能是矩形）   
			* 通过bbox获得相应的正方形bbox，并对得到的bbox通过相似变换到256*256大小的图像    
		* 网络传播进行预测得到pos    
		* 对pos逆相似变换得到原图中的对应人脸的pos图     
		* 通过得到的pos获取3D关键点   
		* 通过得到的pos获取3D定点坐标   
		* 通过得到的pos获取color值     

* predictor.py  
	* 功能：定义resfcn256网络结构、对建立的网络结构进行前向传播    
	* 相关类和模块：    
		* class resfcn256： 定义resfcn256网络 (注意类中@property装饰器的使用；__call__的使用：将一个类实例当做函数调用，x.__call__(1,2)等同于调用x(1,2))      
		* class PosPrediction：定义网络的前向传播（与tensorflow相关）：    
			* 加载预训模型    
			* 前向传播预测   
			* 分batch前向传播预测      
			

## 相关points:   

1、图像变换（相似变换）：https://cloud.tencent.com/developer/section/1415102    
2、api.py中的process函数：

* 将检测到的矩形框由中心点抠取出正方形（正方形边会越出矩形短边），
* 然后将正方形抠取的图像转换到输入图像所在的坐标系下且得到指定边长的正方形，并对无值的边界区域进行填充，
* 最终crop到指定大小的（对齐的）人脸图像
* croped图像通过网络forward得到对应croped_pos图,
* 通过逆变换将croped_pos图对应回原图，从而得到最终的原图的pos图。    

3、api.py中的process函数下的warp函数调用：

- warp:根据给定的坐标变换来变形图像(默认输入shape保留，也可指定output_shape（插值）)。它将输出图像中的坐标转换为输入图像中相应的坐标。 

4、opencv中的remap函数：
http://www.opencv.org.cn/opencvdoc/2.3.2/html/doc/tutorials/imgproc/imgtrans/remap/remap.html#remap    
5、程序中涉及到的相似变换及其逆。   
6、在opencv中的图片时Mat类型的，且数据范围[0，255]，而通过opencv-python加载后的图像图像为numpy的narry类型（因为python本身没有像opencv那样的Mat、Vec3d、size等类型），其数据范围[0,1]。opencv-python是opencv的python绑定，对相关数值类型的转换opencv-python包已经自动完成（如可通过opencv-python imshow [0,1]范围的图像数据：imshow函数自动将数据范围和类型进行变换，然后调用oencv的imshow函数进行显示）。    
7、通过最小二乘法拟合姿态变换的坐标变换矩阵 [链接1](https://blog.csdn.net/bitcarmanlee/article/details/51589143) ；[补充](https://www.cnblogs.com/wangkundentisy/p/7505487.html)