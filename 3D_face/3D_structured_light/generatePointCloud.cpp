

// C++ ��׼��
#include <iostream>
#include <string>
using namespace std;

// OpenCV ��
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

// PCL ��
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>

// �����������
//typedef pcl::PointXYZRGBA PointT;
typedef pcl::PointXYZRGB PointT;

typedef pcl::PointCloud<PointT> PointCloud;

// ����ڲ�
const double camera_factor = 1000;
const double camera_cx = 325.5;
const double camera_cy = 253.5;
const double camera_fx = 518.0;
const double camera_fy = 519.0;

// ������ 
int main(int argc, char** argv)
{
	string rgb_img = argv[1];
	string depth_img = argv[2];
	string output_pcd = argv[3];
	// ��ȡ./data/rgb.png��./data/depth.png����ת��Ϊ����

	// ͼ�����
	cv::Mat rgb, depth;
	// ʹ��cv::imread()����ȡͼ��
	rgb = cv::imread(rgb_img);
	// rgb ͼ����8UC3�Ĳ�ɫͼ��
	// depth ��16UC1�ĵ�ͨ��ͼ��ע��flags����-1,��ʾ��ȡԭʼ���ݲ����κ��޸�
	depth = cv::imread(depth_img, -1);


	// ���Ʊ���
	// ʹ������ָ�룬����һ���յ��ơ�����ָ��������Զ��ͷš�
	PointCloud::Ptr cloud(new PointCloud);
	// �������ͼ
	for (int m = 0; m < depth.rows; m++)
		for (int n = 0; n < depth.cols; n++)
		{
			// ��ȡ���ͼ��(m,n)����ֵ
			ushort d = depth.ptr<ushort>(m)[n];
			// d ����û��ֵ������ˣ������˵�
			if (d == 0)
				continue;
				//d = 2000;
			// d ����ֵ�������������һ����
			PointT p;

			// ���������Ŀռ�����
			p.z = double(d) / camera_factor;
			p.x = (n - camera_cx) * p.z / camera_fx;
			p.y = (m - camera_cy) * p.z / camera_fy;

			// ��rgbͼ���л�ȡ������ɫ
			// rgb����ͨ����BGR��ʽͼ�����԰������˳���ȡ��ɫ
			p.b = rgb.ptr<uchar>(m)[n * 3];
			p.g = rgb.ptr<uchar>(m)[n * 3 + 1];
			p.r = rgb.ptr<uchar>(m)[n * 3 + 2];
			// ��p���뵽������
			cloud->points.push_back(p);
		}


	// ���ò��������
	cloud->height = 1;
	cloud->width = cloud->points.size();
	cout << "point cloud size = " << cloud->points.size() << endl;
	cloud->is_dense = true;
	pcl::io::savePCDFile(output_pcd, *cloud);
	// ������ݲ��˳�
	cloud->points.clear();
	cout << "Point cloud saved." << endl;
	return 0;
}



