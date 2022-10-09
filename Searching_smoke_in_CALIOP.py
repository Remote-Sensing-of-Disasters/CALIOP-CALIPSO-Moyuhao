# 搜索影像中包含的CALIOP V4飞过的像元中是否有烟，输入的都是表格数据和葵花影像TIFF数据
import xlrd
import gdal
import os
import numpy as np

def searching_in_one_pixel(xlsxLon, xlsxLat, xlsxSmoke, lon,lat, interval):
    '''
    输入CALIOP的经纬度数组（4224）和Smoke（4224）数组，
    以及需要搜索的经纬度格网信息lon, lat（每个像元之间的经纬度间隔interval，左上角，所以纬度是减法，经度是加法）
    '''
    if not len(xlsxLon)==len(xlsxLat) and len(xlsxSmoke)==len(xlsxLon) and len(xlsxSmoke) == 4224:
        raise EOFError('好好看看你这个输入的表格对不对吧，是不是4224个数值')
    pixel_value = 0
    for i in range(4224):
        if lon<xlsxLon[i]<lon+interval and lat-interval<xlsxLat[i]<lat:
            pixel_value = 1
            if xlsxSmoke[i] > 0:
                pixel_value = 2
                break
    return pixel_value

def searching_in_one_image(pth_H8tif, pth_xlsxLon, pth_xlsxLat, pth_xlsSmoke, pth_dir, output_name):
    '''
    输入一张葵花图片路径，以及三个表格路径，
    输出一幅和葵花图片同样大小的标签图，包含路径名和文件名(pth_dir,output_name不带.tif)。
    '''
    img = gdal.Open(pth_H8tif)
    ary = img.ReadAsArray() # ary.shape 通道数，垂直方向像元数，水平方向像元数
    ul_Lon,ul_Lat = img.GetGeoTransform()[0], img.GetGeoTransform()[3] #图片左上角的经纬，记住是左上角像元的左上角的经纬
    interval = 0.02 # 懒得搞什么正负了，就直接打个上去，毕竟葵花是正方形像元，如果要搞还得GetGeoTransform
    sht_xlsxLon = xlrd.open_workbook(pth_xlsxLon).sheets()[0]
    sht_xlsxLat = xlrd.open_workbook(pth_xlsxLat).sheets()[0]
    sht_xlsSmoke = xlrd.open_workbook(pth_xlsSmoke).sheets()[0]
    xlsxLon = sht_xlsxLon.col_values(0)
    xlsxLat = sht_xlsxLat.col_values(0)
    xlsSmoke = sht_xlsSmoke.col_values(0)

    output = np.zeros([ary.shape[1],ary.shape[2]])
    for lon in range(ary.shape[2]):
        for lat in range(ary.shape[1]):
            Lon,Lat = ul_Lon+lon*0.02, ul_Lat-lat*0.02
            output[lat,lon] = searching_in_one_pixel(xlsxLon,xlsxLat,xlsSmoke,Lon,Lat,interval)
    if output.sum()==0: raise EOFError('好好看看咋回事吧，一个烟和扫到的地方都没！')
    # 下面是出图
    if not os.path.exists(pth_dir): raise OSError('文件路径都没有建立，搞咩啊')
    os.chdir(pth_dir)
    driver = gdal.GetDriverByName('GTiff')
    out = driver.Create('{}.tif'.format(output_name), ary.shape[2], ary.shape[1], 1, gdal.GDT_Int16)
    out.GetRasterBand(1).WriteArray(output)
    out.SetGeoTransform(img.GetGeoTransform())
    out.SetProjection(img.GetProjection())
    del out

pth_H8tif = r'E:\SmokeDetection\source\new_new_data\0901\0000.tif'
pth_xlsxLon = r'E:\SmokeDetection\source\CALIOP\longitude.xlsx'
pth_xlsxLat = r'E:\SmokeDetection\source\CALIOP\latitude.xlsx'
pth_xlsSmoke = r'E:\SmokeDetection\source\CALIOP\marine.xls'
pth_dir = r'E:\SmokeDetection\source\CALIOP'
output_name = 'test0901_0600_marine'
searching_in_one_image(pth_H8tif, pth_xlsxLon, pth_xlsxLat, pth_xlsSmoke, pth_dir, output_name)