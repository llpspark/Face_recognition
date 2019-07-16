#include <stdio.h>
#include <string>
#include <vector>
#include <unistd.h>
#include <sys/stat.h>

#include "boost/algorithm/string.hpp"
#include "google/protobuf/text_format.h"

#include "caffe/blob.hpp"
#include "caffe/common.hpp"
#include "caffe/net.hpp"
#include "caffe/proto/caffe.pb.h"
#include "caffe/util/db.hpp"
#include "caffe/util/io.hpp"
#include "caffe/layers/memory_data_layer.hpp"
#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/highgui/highgui_c.h"
#include "opencv2/imgproc/imgproc.hpp"

using caffe::Blob;
using caffe::Caffe;
using caffe::Blob;
using caffe::Datum;
using caffe::Net;
using boost::shared_ptr;
using std::string;
namespace db =  caffe::db;



template <typename Dtype>
shared_ptr<Net<Dtype> > feature_extraction_init( string feature_extract_proto,
		string pre_trained_proto)
{
  std::cout << feature_extract_proto<< "\t" << pre_trained_proto << std::endl;
	shared_ptr<Net<Dtype> > feature_extraction_net(
			new Net<Dtype>(feature_extract_proto, caffe::TEST));
	 printf("before copy pretrained====\n");
	feature_extraction_net->CopyTrainedLayersFrom(pre_trained_proto);
	return feature_extraction_net;
}

////////////////////////////////////////////////////////////////////////////////
template<typename Dtype> 
int get_size(shared_ptr<Net<Dtype> >& net, string &layer_name)
{
  std::cout <<"get_size: " << layer_name << std::endl;
  shared_ptr<Blob<Dtype> > fea_blob = net->blob_by_name(layer_name);
  return fea_blob->width() *fea_blob->height() * fea_blob->channels();
}

template <typename Dtype>
int extraction_feature(cv::Mat img, shared_ptr<Net<Dtype> > feature_extraction_net,Dtype *fea, string layer_name)
{
	std::vector<Blob<Dtype>* > input_vec;
	std::vector<cv::Mat> dv;
	dv.push_back(img);
	//printf("before forward===\n");
	std::vector<int> dvl;
	dvl.push_back(0);
	boost::dynamic_pointer_cast<caffe::MemoryDataLayer<Dtype> >(feature_extraction_net-> \
			layers()[0])->AddMatVector(dv, dvl);
	std::vector<Blob<Dtype>*> results = feature_extraction_net->Forward(input_vec);
	//printf("forward succeed!!!!!\n");
	shared_ptr<Blob<Dtype> > feature_blob = feature_extraction_net->blob_by_name(layer_name);
	//printf("width:%d,height:%d,channels:%d\n",feature_blob->width(),feature_blob->height(),
	//	feature_blob->channels());

	memcpy(fea, feature_blob->cpu_data(),sizeof(Dtype) *feature_blob->width() * feature_blob->height()*
			feature_blob->channels());

	return feature_blob->width() * feature_blob->height()*feature_blob->channels();
}

////////////////////////////////////////////////////////////////////////////////

float sim(float *fea1, float *fea2, int len)
{
	float score = 0;
	float sum_tmp1 = 0;
	float sum_tmp2 = 0;
	for(int i=0; i<len; i++)
	{
		score += fea2[i] * fea1[i];
		sum_tmp1 += fea1[i] * fea1[i];
		sum_tmp2 += fea2[i] * fea2[i];
	}
	return score/ sqrt(sum_tmp1 * sum_tmp2);
}


int generate_roc(std::vector<float*> fea_vector, string filelist, int fea_dim)
{
	std::ifstream in_filelist(filelist.c_str());
	std::vector<std::string> lines;
	string file;
	while (in_filelist >> file)
	{
		lines.push_back(file);
	} 

	FILE * same_score = fopen("same_score.txt","w");
	FILE * diff_score = fopen("diff_score.txt","w");
#if 1
	for (int i=0; i< lines.size()-1; ++i)
	{
		int index = lines[i].rfind('/');
		string pic_name_i(lines[i].c_str()+index+1);
		if (pic_name_i[22] == 'C')
		{
			continue;
		}

		for(int j=i+1; j< lines.size(); j++)
		{
			string pic_name_j(lines[j].c_str() + index +1);
			if(pic_name_j[22] == 'C')
			{
				continue;
			}

			  float *fea_vector_i = fea_vector[i];
        float *fea_vector_j = fea_vector[j];
        float score = sim(fea_vector_i, fea_vector_j,fea_dim);

			if (pic_name_j.compare(0,21,pic_name_i,0,21) == 0)
			{
				fprintf(same_score,"%f,",score);
			}
			else
			{
				fprintf(diff_score,"%f,",score);
			}
		}
	}
#else

	for(int i=0; i<lines.size()-1; i++)
	{
		int index = lines[i].rfind('/');
		string pic_name_i(lines[i].c_str() + index + 1);
		for (int j=i+1; j<lines.size(); j++)
		{
      float *fea_vector_i = fea_vector[i];
      float *fea_vector_j = fea_vector[j];
			float score = sim(fea_vector_i,fea_vector_j, fea_dim*2);
			string pic_name_j(lines[j].c_str() + index + 1);
			if (pic_name_j.compare(0,21,pic_name_i,0,21)==0 && pic_name_j[22] != pic_name_i[22])
			{
				fprintf(same_score,"%f,",score);
			}
			else if(pic_name_j[22] != pic_name_i[22] && pic_name_j.compare(0,21,pic_name_i,0,21)!=0)
			{
				fprintf(diff_score,"%f,", score);
			}
		}
	}
#endif
  std::cout << "finished\n";
  for(int i=0; i<fea_vector.size(); i++)
  {
    free(fea_vector[i]);
  }
	fclose(same_score);
	fclose(diff_score);
	return 0;
}



int generate_roc_id_spot(std::vector<float*> fea_vector_id, std::vector<float*> fea_vector_sp, string filelist_id, string filelist_sp, int fea_dim)
{
  std::ifstream in_filelist_id(filelist_id.c_str());
  std::vector<std::string> lines_id;
  string file_id;

  while (in_filelist_id >> file_id)
  {
    lines_id.push_back(file_id);
  } 


  std::ifstream in_filelist_sp(filelist_sp.c_str());
  std::vector<std::string> lines_sp;
  string file_sp;

  while (in_filelist_sp >> file_sp)
  {
    lines_sp.push_back(file_sp);
  }
 
  FILE * same_score = fopen("same_score.txt","w");
  FILE * diff_score = fopen("diff_score.txt","w");
  

  for (int i=0; i< lines_id.size(); ++i)
  {
    int index = lines_id[i].rfind('/');
    string pic_name_id(lines_id[i].c_str()+index+1);
    
    for (int j=0; j< lines_sp.size(); ++j)
    {
      int index = lines_sp[i].rfind('/');
      string pic_name_sp(lines_sp[j].c_str()+index+1);

      float *fea_vector_i = fea_vector_id[i];
      float *fea_vector_j = fea_vector_sp[j];
      float score = sim(fea_vector_i, fea_vector_j,fea_dim);
    //  std::cout << pic_name_sp << std::endl ;

      if (pic_name_sp.compare(0,21,pic_name_id,0,21) == 0)
      {
        fprintf(same_score,"%f,",score);
      }
      else
      {
        fprintf(diff_score,"%f,",score);
      }
    }
  }




  std::cout << "finished\n"<<std::endl ;
  for(int i=0; i<fea_vector_id.size(); i++)
  {
    free(fea_vector_id[i]);
    free(fea_vector_sp[i]);
  }
  fclose(same_score);
  fclose(diff_score);
  return 0;
}



template <typename Dtype>
class fea_extracter
{
  public:
    fea_extracter(shared_ptr< Net<Dtype> > fea_net, string layer_name)
    {
      net_ = fea_net;
      layer_name_ = layer_name;
    }

    fea_extracter(string net_name,string trained_model, string layer_name)
    {
      shared_ptr<Net<Dtype> > net = feature_extraction_init<Dtype>(net_name, trained_model);
      net_ = net;
      layer_name_ = layer_name;
    }

    int get_fea_size()
    {
      return get_size<Dtype>(net_,layer_name_);
    }

    int get_fea(string img_filename, Dtype*fea)
    {
      cv::Mat img = cv::imread(img_filename,-1);
      return extraction_feature<Dtype>(img, net_, fea, layer_name_);
    }

  private:
    shared_ptr<Net<Dtype> > net_;
    string layer_name_;
};

void write_fea_to_disk(std::vector<float*>&fea_vector,int fea_size, string fea_path, string filelist)
{
  std::ifstream filelist_(filelist.c_str());
  std::vector<std::string> lines;
  string files;
  while(filelist_ >> files)
  {
    string sub = files.substr(0,files.find('.'));
    lines.push_back(fea_path+sub+ ".bin");
  }

  for(int i=0; i<lines.size(); i++)
  {
    string sub_path = lines[i].substr(0,lines[i].rfind('/'));
    if (access(sub_path.c_str(),F_OK) < 0)
    {
      mkdir(sub_path.c_str(),0755);
    }
    FILE *fid = fopen(lines[i].c_str(),"wb");
    fwrite(fea_vector[i],sizeof(float),fea_size,fid);
    fclose(fid);
    printf("processing to ...%d/%lu\n",i,lines.size());
  }
}
void write_feature_to_disk(float *fea, string fea_path,int fea_size, string filename)
{
  string sub = filename.substr(0,filename.find('.'));
  string full_path = fea_path + sub + ".bin";
  string sub_path = full_path.substr(0,full_path.rfind('/'));

  if (access(sub_path.c_str(),F_OK) < 0)
  {
    mkdir(sub_path.c_str(),0755);
  }
  FILE *fid = fopen(full_path.c_str(),"wb");
  fwrite(fea,sizeof(float),fea_size,fid);
  fclose(fid);
}


int batch_extract(string net_name, string trained_model,string layer_name, string file_path, string filelist, std::vector<float*> &fea_vector)
{
  fea_extracter<float> my_extor(net_name, trained_model, layer_name);
  int fea_dim = my_extor.get_fea_size();
  
  printf("fea_dim:%d\n",fea_dim);
  std::ifstream filelist_(filelist.c_str());
  std::vector<std::string> lines;
  string files;

  while(filelist_ >> files)
  {
    lines.push_back(file_path+files);
  }

  for(int i=0; i<lines.size(); i++)
  {
    float *tmp_fea = (float*)malloc(sizeof(float)*fea_dim);
    my_extor.get_fea(lines[i],tmp_fea);
    std::cout<<lines[i]<<std::endl;
#if 0
    write_feature_to_disk(tmp_fea,fea_path,fea_dim,lines[i]);
    free(tmp_fea);
#else
    fea_vector.push_back(tmp_fea);
#endif
    printf("processing to ...%d/%lu\n",i,lines.size());
  }
  return fea_dim;
}

int batch_extract(string fea_description, string filelist, std::vector<float*> &fea_vector)
{
  std::ifstream description(fea_description.c_str());
  std::vector<std::string> lines;
  string line;
  while(description >> line)
  {
    if (line.find("#") == 0)
    {
      continue;
    }
    lines.push_back(line);
  }
  return batch_extract(lines[0],lines[1],lines[2],lines[3],filelist, fea_vector);
}

int mutil_net(string net_description, string filelist, std::vector<float*> &fea_vector)
{
  std::ifstream net_description_(net_description.c_str());
  std::vector<std::string>nets;
  std::string line;
  while(net_description_ >> line)
  {
    if (line.find("#")==0)
    {
      continue;
    }
    nets.push_back(line);
  }
  int fea_len = 0;
  std::vector<int> fea_len_array;
  std::vector<std::vector<float*> > tmp_feas;

  if (nets.size() ==1 )
  {
    return batch_extract(nets[0],filelist,fea_vector);
  }
  for(int i=0; i<nets.size(); i++)
  {
    std::vector<float*> tmp;
    int fea_length = batch_extract(nets[i],filelist, tmp);
    fea_len_array.push_back(fea_length);
    tmp_feas.push_back(tmp);
    fea_len += fea_length;
  }

  for(int i=0; i < tmp_feas[0].size(); i++)
  {
    float *tmpf = (float*)malloc(sizeof(float)*fea_len);
    float *p_tmp = tmpf;
    for (int j=0; j<tmp_feas.size(); j++)
    {
      memcpy(p_tmp,tmp_feas[j][i],sizeof(float)*fea_len_array[j]);
      p_tmp += fea_len_array[j];
      std::cout << "here\n";
      free(tmp_feas[j][i]);
    }
    fea_vector.push_back(tmpf);
  }
  return fea_len;
}



int main(int argc, char** argv)
{
  ::google::InitGoogleLogging(argv[0]);
//	Caffe::set_mode(Caffe::CPU);
  Caffe::set_mode(Caffe::GPU);
  Caffe::SetDevice(4);
#if 0
  std::vector<float*> fea_vec;
  int fea_len = mutil_net(argv[1],argv[2],fea_vec);
  generate_roc(fea_vec,argv[2],fea_len);
#else
  std::vector<float*> fea_vec_id;
  std::vector<float*> fea_vec_sp;
  int fea_dim_id=  batch_extract(argv[1], argv[2],argv[3], argv[4], argv[6], fea_vec_id);
  std::cout << "get spot feature"<<fea_vec_id.size() << std::endl ;
  int fea_dim_sp=  batch_extract(argv[1], argv[2],argv[3], argv[5], argv[7], fea_vec_sp);

  generate_roc_id_spot(fea_vec_id, fea_vec_sp, argv[6], argv[7], fea_dim_id) ;
//  std::vector<float*> fea_vec ;
//  int fea_dim=  batch_extract(argv[1], argv[2],argv[3], argv[4], argv[5], fea_vec);
//  std::cout << "get feature success" << std::endl ;
//  generate_roc(fea_vec, argv[5], fea_dim) ;

#endif
 return 0;
}
