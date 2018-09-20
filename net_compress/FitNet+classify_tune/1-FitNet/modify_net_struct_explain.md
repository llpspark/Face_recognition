##code 说明
* modify_net_struct.py
	* 修改student网络名不能与teacher网络名重复
	* student网络的num_output在teacher网络基础上减少
	* 根据具体层（类型和参数）需要添加lr_mult和decay_mult参数
		* 卷积bais为true时应有两个param{}参数
		* BatchNorm层有三个param{}参数（分别对应均值、方差、滑动系数），并且需要注意的时无论时训练还是测试，三个param参数中的lr_mult和decay_mult的值均设为0
	* 在BatchNorm 层中将参数"use_global_stats"删除，该参数为是否使用保存的均值和方差，将其状态使用caffe默认的形式（训练时该参数为false（使用滑动系数）,测试时为true（使用保存值））,否则训练网络不收敛。   
	* 将卷积层的参数指定填充方式并填充（在训练中不能使用默认值0）   

##附：
* caffe实现蒸馏网络相关主要事项：
	* 由deploy.ptototxt向train.prototxt转换注意：
		* 在各类可学习参数层中添加lr_mult和decay_mult参数
		* BN层、conv层的param{}参数要添加上
		* 注意BN层的“use_global_stats”参数（最好删除）  
		* 卷积层的权重、偏执填充（weight_filler {type: "xavier"std: 0.01}bias_filler {type: "constant"value: 0.2}）;全连接层权重填充（）不能使用默认（默认为0），否则导致loss始终不下降。   
	* 模型由mxnet格式转caffe格式后，通过caffe训练注意：
		* 需要注意在数据输入层处是否对数据进行了规范化处理（将数据规范到（-1，1）之间）（caffe中使用transform_param转换），尤其模型是从mxnet转到caffe时，模型的输入数据需要规范化到（-1，1）的。
		* 注意由Mxnet转caffe转成的模型，模型默认的输入为RGB（caffe将图像读为BGR），所以如果是直接用转过来的模型在caffe做测试，应将输入转为RGB（Slice+Concat）  
	* 如果蒸馏过程很难训（loss不下降）可以考虑：
		* 将蒸馏网络尾部的全连接改为卷积+全局pooling+Flatten，这样可以大量减少训练参数     
		* 在最后输出前添加relu层，使输出的分别在更小的范围内，使网络容易收敛。   