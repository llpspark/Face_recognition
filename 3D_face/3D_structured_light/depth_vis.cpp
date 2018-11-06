//#include <iostream>
//#include <boost/thread/thread.hpp>
//#include <pcl/common/common_headers.h>
//#include <pcl/range_image/range_image.h>
//#include <pcl/io/pcd_io.h>
//#include <pcl/visualization/range_image_visualizer.h>
//#include <pcl/visualization/pcl_visualizer.h>
//#include <pcl/console/parse.h>
//#include<time.h>
//#include <windows.h>
//typedef pcl::PointXYZ PointType;
//
//// --------------------
//// -----Parameters-----
//// --------------------
//float angular_resolution_x = 0.5f,
//angular_resolution_y = angular_resolution_x;
//pcl::RangeImage::CoordinateFrame coordinate_frame = pcl::RangeImage::CAMERA_FRAME;
//bool live_update = false;
//
//// --------------
//// -----Help-----
//// --------------
//void printUsage(const char* progName)
//{
//	std::cout << "\n\nUsage: " << progName << " [options] <scene.pcd>\n\n"
//		<< "Options:\n"
//		<< "-------------------------------------------\n"
//		<< "-rx <float>  angular resolution in degrees (default " << angular_resolution_x << ")\n"
//		<< "-ry <float>  angular resolution in degrees (default " << angular_resolution_y << ")\n"
//		<< "-c <int>     coordinate frame (default " << (int)coordinate_frame << ")\n"
//		<< "-l           live update - update the range image according to the selected view in the 3D viewer.\n"
//		<< "-h           this help\n"
//		<< "\n\n";
//}
//
//void setViewerPose(pcl::visualization::PCLVisualizer& viewer, const Eigen::Affine3f& viewer_pose)   //�����ӽ�λ��
//{
//	Eigen::Vector3f pos_vector = viewer_pose * Eigen::Vector3f(0, 0, 0);   //eigen
//	Eigen::Vector3f look_at_vector = viewer_pose.rotation() * Eigen::Vector3f(0, 0, 1) + pos_vector;
//	Eigen::Vector3f up_vector = viewer_pose.rotation() * Eigen::Vector3f(0, -1, 0);
//	viewer.setCameraPosition(pos_vector[0], pos_vector[1], pos_vector[2],
//		look_at_vector[0], look_at_vector[1], look_at_vector[2],
//		up_vector[0], up_vector[1], up_vector[2]);
//}
//
//// --------------
//// -----Main-----
//// --------------
//int main(int argc, char** argv)
//{
//	// --------------------------------------
//	// -----Parse Command Line Arguments-----
//	// --------------------------------------
//	if (pcl::console::find_argument(argc, argv, "-h") >= 0)
//	{
//		printUsage(argv[0]);
//		return 0;
//	}
//	if (pcl::console::find_argument(argc, argv, "-l") >= 0)
//	{
//		live_update = true;
//		std::cout << "Live update is on.\n";
//	}
//	if (pcl::console::parse(argc, argv, "-rx", angular_resolution_x) >= 0)
//		std::cout << "Setting angular resolution in x-direction to " << angular_resolution_x << "deg.\n";
//	if (pcl::console::parse(argc, argv, "-ry", angular_resolution_y) >= 0)
//		std::cout << "Setting angular resolution in y-direction to " << angular_resolution_y << "deg.\n";
//	int tmp_coordinate_frame;
//	if (pcl::console::parse(argc, argv, "-c", tmp_coordinate_frame) >= 0)
//	{
//		coordinate_frame = pcl::RangeImage::CoordinateFrame(tmp_coordinate_frame);
//		std::cout << "Using coordinate frame " << (int)coordinate_frame << ".\n";
//	}
//	angular_resolution_x = pcl::deg2rad(angular_resolution_x);
//	angular_resolution_y = pcl::deg2rad(angular_resolution_y);
//
//	// ------------------------------------------------------------------
//	// -----Read pcd file or create example point cloud if not given-----
//	// ------------------------------------------------------------------
//	pcl::PointCloud<PointType>::Ptr point_cloud_ptr(new pcl::PointCloud<PointType>);
//	pcl::PointCloud<PointType>& point_cloud = *point_cloud_ptr;
//	Eigen::Affine3f scene_sensor_pose(Eigen::Affine3f::Identity());
//	std::vector<int> pcd_filename_indices = pcl::console::parse_file_extension_argument(argc, argv, "pcd");
//	if (!pcd_filename_indices.empty())
//	{
//		std::string filename = argv[pcd_filename_indices[0]];
//		if (pcl::io::loadPCDFile(filename, point_cloud) == -1)
//		{
//			std::cout << "Was not able to open file \"" << filename << "\".\n";
//			printUsage(argv[0]);
//			return 0;
//		}
//		scene_sensor_pose = Eigen::Affine3f(Eigen::Translation3f(point_cloud.sensor_origin_[0],
//			point_cloud.sensor_origin_[1],
//			point_cloud.sensor_origin_[2])) *
//			Eigen::Affine3f(point_cloud.sensor_orientation_);
//	}
//	else
//	{
//		std::cout << "\nNo *.pcd file given => Genarating example point cloud.\n\n";
//		for (float x = -0.5f; x <= 0.5f; x += 0.01f)
//		{
//			for (float y = -0.5f; y <= 0.5f; y += 0.01f)
//			{
//				PointType point;  point.x = x;  point.y = y;  point.z = 2.0f - y;
//				point_cloud.points.push_back(point);
//			}
//		}
//		point_cloud.width = (int)point_cloud.points.size();  point_cloud.height = 1;
//	}
//
//	std::cout << "Load successed!" << std::endl;
//	// -----------------------------------------------
//	// -----Create RangeImage from the PointCloud-----
//	// -----------------------------------------------
//	float noise_level = 0.0;
//	float min_range = 0.0f;
//	int border_size = 1;
//	boost::shared_ptr<pcl::RangeImage> range_image_ptr(new pcl::RangeImage);
//	pcl::RangeImage& range_image = *range_image_ptr;
//	std::cout << __FILE__ << ":::" << __LINE__ << std::endl;
//	range_image.createFromPointCloud(point_cloud, angular_resolution_x, angular_resolution_y,
//		pcl::deg2rad(360.0f), pcl::deg2rad(180.0f),
//		scene_sensor_pose, coordinate_frame, noise_level, min_range, border_size);
//	std::cout << __FILE__ << ":::" << __LINE__ << std::endl;
//
//	// --------------------------------------------
//	// -----Open 3D viewer and add point cloud-----
//	// --------------------------------------------
//	/*****************************************************************************************
//	����3D�Ӵ����󣬽�������ɫ����Ϊ��ɫ����Ӻ�ɫ�ģ����ƴ�СΪ1�����ͼ�񣨵��ƣ�����ʹ��Main����
//	���涨���setViewerPose�����������ͼ����ӵ��������ע�͵Ĳ���������Ӱ�����ϵ������ԭʼ���ƽ��п��ӻ�
//	*****************************************************************************************/
//	pcl::visualization::PCLVisualizer viewer("3D Viewer");     //�����ʼ�����ӻ�����
//	viewer.setBackgroundColor(1, 1, 1);                         //��������Ϊ��ɫ
//	pcl::visualization::PointCloudColorHandlerCustom<pcl::PointWithRange> range_image_color_handler(range_image_ptr, 0, 0, 0); //�����Զ�����ɫ
//	viewer.addPointCloud(range_image_ptr, range_image_color_handler, "range image");
//	viewer.setPointCloudRenderingProperties(pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 1, "range image");
//	//viewer.addCoordinateSystem (1.0f, "global");
//	//PointCloudColorHandlerCustom<PointType> point_cloud_color_handler (point_cloud_ptr, 150, 150, 150);
//	//viewer.addPointCloud (point_cloud_ptr, point_cloud_color_handler, "original point cloud");
//	viewer.initCameraParameters();
//	setViewerPose(viewer, range_image.getTransformationToWorldSystem());
//
//	// --------------------------
//	// -----Show range image-----
//	// --------------------------
//	//����ͼ��ķ�ʽ���ӻ����ͼ��ͼ�����ɫȡ�������ֵ
//	pcl::visualization::RangeImageVisualizer range_image_widget("Range image");
//	range_image_widget.showRangeImage(range_image);      //ͼ����ӻ���ʽ��ʾ���ͼ��
//
//														 //--------------------
//														 // -----Main loop-----
//														 //--------------------
//	std::cout << viewer.wasStopped() << std::endl;
//	while (!viewer.wasStopped())   //������ѭ���Ա�֤���ӻ��������Ч�ԣ�ֱ�����ӻ����ڹر�
//	{
//		range_image_widget.spinOnce();   //���ڴ������ͼ����ӻ���ĵ�ǰ�¼�
//		viewer.spinOnce();              //���ڴ���3D���ڵ�ǰ���¼����⻹������ʱ����2D���ͼ������Ӧ���ӻ������еĵ�ǰ�ӽǣ���ͨ��������-1������
//		Sleep(0.01);
//
//		//���ȴӴ����еõ���ǰ�Ĺ۲�λ�ã�Ȼ�󴴽���Ӧ�ӽǵ����ͼ�񣬲���ͼ����ʾ�������ʾ
//		if (live_update)
//		{
//			scene_sensor_pose = viewer.getViewerPose();
//			range_image.createFromPointCloud(point_cloud, angular_resolution_x, angular_resolution_y,
//				pcl::deg2rad(360.0f), pcl::deg2rad(180.0f),
//				scene_sensor_pose, pcl::RangeImage::LASER_FRAME, noise_level, min_range, border_size);
//			range_image_widget.showRangeImage(range_image);
//		}
//	}
//}



#include <iostream> 
#include <string> 
#include <pcl/io/pcd_io.h> 
#include <pcl/point_types.h> 
#include <pcl/visualization/pcl_visualizer.h> 
using namespace std;

int main(int argc, char** argv) {

	typedef pcl::PointXYZRGB PointT;
	pcl::PointCloud<PointT>::Ptr cloud(new pcl::PointCloud<PointT>);

	std::string file_path = argv[1];

	if (pcl::io::loadPCDFile<PointT>(file_path, *cloud) == -1) {
		 //load the file 
		PCL_ERROR("Couldn't read PCD file \n");
		return (-1);
	}
	printf("Loaded %d data points from PCD\n",
		cloud->width * cloud->height);

	/*for (size_t i = 0; i < cloud->points.size(); i += 10000)
		printf("%8.3f %8.3f %8.3f %5d %5d %5d\n",
			cloud->points[i].x,
			cloud->points[i].y,
			cloud->points[i].z,
			cloud->points[i].r,
			cloud->points[i].g,
			cloud->points[i].b
			);*/

	pcl::visualization::PCLVisualizer viewer("Cloud viewer");
	viewer.setCameraPosition(0, 0, -3.0, 0, -1, 0);
	//viewer.addCoordinateSystem(0.3);

	viewer.addPointCloud(cloud);
	while (!viewer.wasStopped())
		viewer.spinOnce(100);
	return (0);
}


