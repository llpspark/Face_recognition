// run by: generatePointCloud_v1.exe color.png depth.raw name.pcd

// C++ 标准库
#include <iostream>
#include <string>
#include <fstream>
using namespace std;

// OpenCV 库
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

// PCL 库
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>

//typedef pcl::PointXYZRGBA PointT;
typedef pcl::PointXYZRGB PointT;

typedef pcl::PointCloud<PointT> PointCloud;

// 相机内参
const double camera_factor = 1000;
const double camera_cx = 325.5;
const double camera_cy = 253.5;
const double camera_fx = 518.0;
const double camera_fy = 519.0;


//The image size
const int im_w = 640;
const int im_h = 480;


int LoadBinFile(const char* BinFileName, char *&buffer)
{
	ifstream input(BinFileName, ios::in | ios::binary);
	if (!input.is_open())
	{
		std::cout << "cannot open the binfile" << endl;
	}

	input.seekg(0, ios::end);
	int length = input.tellg();
	input.seekg(0, ios::beg);

	buffer = new char [length];

	//read the hole binary block file to variable
	input.read(buffer, length);
	input.close();
	return length;
}

/*
ushort find_max(int length, unsigned short *val)
{
	ushort max_val = 0;
	for (int i = 0; i < length; i++)
	{
		if (val[i] > max_val)
			max_val = val[i];
	}
	return max_val;
}
*/

int main(int argc, char** argv)
{
	string rgb_img = argv[1];
	string depth_path = argv[2];
	string output_pcd = argv[3];
	cv::Mat rgb;
	rgb = cv::imread(rgb_img);
	
	char *buffer = NULL;
	const char* dep_path = depth_path.c_str();
	unsigned short length = LoadBinFile(dep_path, buffer);

	unsigned short *value = (unsigned short *)buffer;
	//ushort max_val = find_max(length, value);
	PointCloud::Ptr cloud(new PointCloud);

	// 遍历color and depth 
	for (int i = 0; i < im_h; i++)
		for (int j = 0; j < im_w; j++)
		{
			//ushort d = value[i * im_w + j] * 255 / max_val;
			//不需要将二进制的深度值归一化到0~255,直接使用即可。	
			ushort d = value[i * im_w + j];

			// d 可能没有值，若如此，跳过此点
			if (d == 0)
				continue;

			// d 存在值，则向点云增加一个点
			PointT p;
			p.z = double(d) / camera_factor;
			p.x = (j - camera_cx) * p.z / camera_fx;
			p.y = (i - camera_cy) * p.z / camera_fy;

			p.b = rgb.ptr<uchar>(i)[j * 3];
			p.g = rgb.ptr<uchar>(i)[j * 3 + 1];
			p.r = rgb.ptr<uchar>(i)[j * 3 + 2];
			cloud->points.push_back(p);
		}
	
	delete[]buffer;

	// 设置并保存点云
	cloud->height = 1;
	cloud->width = cloud->points.size();
	cout << "point cloud size = " << cloud->points.size() << endl;
	cloud->is_dense = false;
	pcl::io::savePCDFile(output_pcd, *cloud);

	// 清除数据并退出
	cloud->points.clear();
	cout << "Point cloud saved." << endl;
	return 0;
}



