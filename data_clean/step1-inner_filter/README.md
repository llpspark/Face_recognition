# data_clean:step1(选择合适阈值进行类内筛选)
## 人脸数据类内清洗处理流程如下图：
![](https://i.imgur.com/7l8b3FA.png)


* 分数表复原（生成原始分数表）
	* 代码：restor_ori_score.py
	* 复原结果：有效数据（得分高于0）
* 数据得分分布统计分析
	* 代码：plot_score_distribute.py
	* 统计结果示例（横坐标为得分，纵坐标为得分占比）（上图为各分数的分布、下图为对应的边缘分布）
	* ![](https://i.imgur.com/2XxwgQW.jpg)
	* ![](https://i.imgur.com/4k7wJXh.jpg)
* 挑选特定得分段数据进行check
	* 代码：select_data_by_score.py  
	* 将筛选后的数据用于检测  
	* 代码：merge_list.py
* 得分与img取交集生成训练集
 * 代码： score_intersect_img.py
* label 重定向（重排序、从0开始索引）
	* 代码： change_label.py
* 合并不同训练集生成的列表
	* 代码：merge_data.py
* 对生成的可训练list进行shuffle
	* 代码： shuffle_data.py
