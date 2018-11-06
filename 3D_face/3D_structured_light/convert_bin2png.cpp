#include <stdio.h>
#include <stdlib.h>
#include <cv.h>
#include <opencv2/highgui.hpp>

/* 加载二进制数据，返回实际加载量，re-alloc内存，是否追加'\0'结尾 */
  int LoadFileMemory
(
 const char *chFile,       /* 全部载起的文件 */
 unsigned char **hBin,     /* 可re-alloc内存 */
 int nZro/* = 0*/        /* 是否追加'\0'尾 */
 )
{
  FILE *fp; int nFln = 0, nRet = 0; /* 参数安检 */
  if(!chFile || !chFile[0] || !hBin) return (0);
  if(nZro < 0) nZro = 0; /* 是否尾部追加'\0'符号 */

  fp = fopen(chFile, "rb"); /* 打开文件 */
  if(!fp) return (0);

  if(fseek(fp, 0, SEEK_END) != 0) goto TheEnd;
  if((nFln = (int)ftell(fp)) < 1) goto TheEnd; /* 文件长度 */
  if(fseek(fp, 0, SEEK_SET) != 0) goto TheEnd;

  *hBin = (unsigned char *)realloc(*hBin, nFln + nZro); /* 分配内存 */
  if(*hBin == NULL) goto TheEnd;
  if(fread(*hBin, nFln, 1, fp) != 1) goto TheEnd; /* 加载数据 */

  nRet = nFln; /* 返回不含'\0'的长度 */
  if(nZro) *(*hBin + nFln) = '\0'; /* 追加'\0'结尾 */

TheEnd: /* 统一出口 */
  if(nRet < 1 && *hBin) {free(*hBin); *hBin = NULL;}
  if(fp) {fclose(fp); fp = NULL;} return (nRet);
}


int main(int argc, char **argv)
{
  if (argc != 3)
  {
    printf("usage: %s bin_name, img_name\n",argv[0]);
    return -1;
  }
  unsigned char *buffer;
  int nret = LoadFileMemory(argv[1],&buffer,0);
  printf("LoadFileMemory ret:%d\n",nret);
  
  if(nret != 640*480*2) return -2;

  unsigned short *value = (unsigned short *)buffer;
  unsigned short max_val = 0;
  
  //FILE *fid = fopen("pp.txt","w");

  //for(int i=0; i<480; i++)
  //{
  //  for(int j=0; j<640; j++)
  //  {
  //    fprintf(fid,"%d,%d,%d\n",i,j,value[i*640+j]);
  //  }
  //}
  //fclose(fid);
  //
  //for(int i=0; i<640*480; i++)
  //{
  //  if(value[i] > max_val)
  //  {
  //    max_val = value[i];
  //  }
  //}

  //printf("max_value:%d\n",max_val);
  //unsigned char img_buffer[640*480]={0};
  unsigned short img_buffer[640*480] = {0};
  for(int i=0; i<640*480; i++)
  {
    //img_buffer[i] = (int)(value[i])*255 / max_val;
    //img_buffer[i] = (int)(value[i]);
    img_buffer[i] = (unsigned short)(value[i]);

  }
  //cv::Mat img(480,640,CV_8UC1,img_buffer);
  cv::Mat img(480,640,CV_16UC1,img_buffer);
  cv::imwrite(argv[2],img);
  free(buffer);

  return 0;
}
