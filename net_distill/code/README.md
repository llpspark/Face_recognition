##code 说明
* modify_net_struct.py
	* 修改student网络名不能与teacher网络名重复
	* student网络的num_output在teacher网络基础上减少
	* 根据具体层（类型和参数）需求添加lr_mult和decay_mult参数
		* 卷积bais为true时应有两个param{}参数
		* BatchNorm层有三个param{}参数（分别对应均值、方差、滑动系数），并且需要注意的时无论时训练还是测试，三个param参数中的lr_mult和decay_mult的值均设为0
	* 在BatchNorm 层中将参数"use_global_stats"删除，该参数为是否使用保存的均值和方差，将其状态使用caffe默认的形式（训练时该参数为false（使用滑动系数）,测试时为true（使用保存值））,否则训练网络不收敛。
	