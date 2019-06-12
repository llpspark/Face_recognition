# ArcFace工程代码解析   
* code:https://github.com/deepinsight/insightface       

  ## train_softmax.py代码流程解析  

### insigthface/src/train_softmax.py     
* 功能：训练程序入口。集成了初始化、（训练、验证）数据加载、计算图生成、拟合训练、模型性保存等等。

* 所调用的其他python模块（py文件）
	* /src/image_iter.py 下的FaceImageIter、FaceImageIterList类用于加载训练数据   
	* /src/common/face_image.py下的load_property函数，用于加载训练数据的property文件   
	* /src/eval/verification.py下的1）load_bin函数用于将bin类型的验证数据解析为mx支持的NDARRAY； 2）test函数，测试加载后的验证数据（lfw等）   
	* /src/symbols/fresnet.py 用于生成resnet类型的计算图     
	
* 具体流程   
	1） 设置设备上下文（GPU or CPU）  
	2）设置初始化参数（模型路径、batch_size、训练数据路径、类别数、lr、wd、momentun等等）   
	3）加载预训模型并通过调用其他模块生成对应的计算图    
	4）warp好计算图准备前向传播   
	5）根据loss的类型选择不同的度量方式（AccMetric 和 LossValueMetric两个类）   
	6）构建权重初始化器initilizer（优先级低于pretrain model）    
	7）设置优化器opt（SGD）    
	8）定义训练日志中的速度计Speedometer，用来记录训练速度和acc   
	9）加载测试数据集（调用verification模块）   
	10）设置lr_step(与batch_size相关联)   
	11）通过PrefetchingIter加载训练数据迭代器，一边迭代训练使用     
	12）定义_batch_callback函数，在训练过程中每完成一次batch迭代则调用该方法，方法描述如下：   

	```
	* 全局变量mbatch + 1（mbatch为当前迭代的batch总次数）   
	* 如果mbatch达到lr_step + beta_freeze设置的值，则lr缩小10倍    
	* 执行定义好的速度计（确认每个指定batch数进行速度计log打印）    
	* 如果mbatch是1000的整数倍，则打印当前lr、epoch_nbatch、epoch数   
	* 如果mbath达到verbose指定数，则在验证集上进行测试，并进行一下操作：
		* 测试lfw数据集时，根据测试准确率数值决定是否保存模型（在ckpt=1情况下）  
		* 打印所有验证集（lfw、agedb等）中最高的准确率    
	* 如果mbatch超过预设的最大迭代次数，则程序退出    
```
	13）加载以上配置，通过mxnet的fit函数进行参数拟合训练        
	
* 说明：
	* 在流程3）生成计算图主要分两步：1、根据不同的网络结构类型 调用对应的计算图生成模块来生成基础计算图（除loss部分的计算图）；2、在基础网络的基础上加上loss层的symbol（包括fc7、arcloss softmax）。注意此处的基础网络指：数据输入层 + input卷积层conv0 + resnet(堆叠units) + 输出embedding层fc1。
	* 在该脚本中通过参数解析argparse来获取程序所需参数，arg_parse函数返回的为参数解析后的Namespace类型的变量arg(其本质类似于字典),然后作者通过将arg变量变成global变量的方式，即便arg变量中没有某个分量，依旧可以对指定的该分量赋值。     
	
* 相关调用模块代码说明
	* /src/image_iter.py     
		* FaceImageIter类说明（构造函数）
			* 通过recordio模块加载rec和与其同路径下的idx文件
			* 通过idx的索引对训练数据文件进行索引   
			* 加载数据
		* FaceImageIterList类说明（构造函数）
	* /src/common/face_image.py
		* load_property函数
			* 加载data_dir下（同rec、idx）的property文件数据(类别数，图像高，宽)
	* /src/eval/verification.py    
		* load_bin函数(加载验证数据集)
			* load bin类型的二进制验证数据集（lfw...）   
			* 对加载上的数据集进行解码为MXnet的NDarray类型   
			* 对每一张图像进行变换：CHW->HWC  
			* 对图像沿通道方向进行翻转（flip为1表示翻转），扩增数据   
			* 返回最后生成的ndarray数据（每加载1000张图像，输出“loading bin i”信息）     
		* test函数（对加载的所有验证集测试其准确率）      
			* 将每个验证集均按照batch_size的大小进行batch划分        
			* 通过DataBatch的形式加载验证集数据   
			* forward网络传播，得到网络输出output（即embedding）   
			* 计算并返回所有同一个验证集下所有batch 的平均准确率和标准差(表示偏离程度)    
	* /src/symbols/fresnet.py （生成res100基础结构的symbol图）   
		*  说明：
			* res100的100层指： input_conv(conv0) + res_units(98层，不包含不同stage间用于特征匹配的卷积层) + embedding层即output_fc(fc1) = 100;注意这里不包含用于loss的fc层（fc7）   
		* 根据网络结构类型、网络层数指定不同的卷积核参数(filter_list)和不同的残差单元的设置units   
		* 具体生成过程      
			* 1）生成data层symbol（对数据规范化到（-1，1））  2）根据input_conv生成对应的输入卷积层 3）version_se、version_act类型、version_unit等类型生成res_units的全部symbol计算图  4）根据output_fc的类型生成embedding层的symbol      
