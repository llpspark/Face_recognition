# 3D Structured Light      

* 动机：由于准确率和防假体的需要，各大厂商现在都在进军3D人脸识别和检活等新方向。由于2D转成的3D不具备防假体及真实3D数据的特性，从3D相机获取的3D数据做3D方向的相关研究显得十分重要。
* 硬件配置：    
	* orbbec Astra mini相机（项目中要使用的相机），输出深度图、色彩图和近红外图像，无3D处理等相关的api。      
	* inter RealSense 相机，有相关的api可调用（生成人脸点云和人脸关键点、点云的三角剖分）      

## 目录     

* 深度图-->点云生成
	* 坐标变换（相机坐标系-->空间坐标系）     
	* 点云生成和渲染
	* pcl可视化点云

## 附录       

* 常见的3D数据格式：     
	* obj + mtl: wavefront公司建立，可兼容绝大多数3D软件   
	* pcd: 点云，主要依托PCL点云库    
	* ply（polygon file format）:多边形文件格式，通过定义立体多边形表示3D          
	* stl:通过定义所有三角面片及对应顶点表现3D，autoCAD、3d打印常使用的格式    
	* VTK：依托于VTK工具包的一种3D数据格式    
	* **注意**：深度图（range image）并不是3D数据，可称2.5D。   
	* 各格式间的转换可使用PCL中的工具：[convert](https://github.com/PointCloudLibrary/pcl/blob/master/io/tools/converter.cpp)    