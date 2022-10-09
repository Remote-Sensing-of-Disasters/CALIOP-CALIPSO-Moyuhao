# 把XLSX表格中的VFM算出来哪里有烟
import xlwt
import xlrd
from tqdm import tqdm
xlsxFCF = r'E:\SmokeDetection\source\CALIOP\VFM.xlsx'

workbook = xlrd.open_workbook(xlsxFCF)
FCF = workbook.sheets()[0] # 这两行代码是打开XLSX文件的代码，会有点慢因为数据有点大
output = []
for i in tqdm(range(4224)):
    row = FCF.row_values(rowx = i, start_colx=0)#开始一行行地调用
    for j in range(5515):
        # 查找这行中有没有烟
        num = bin(int(row[j])) # 二进制 字符串型
        #print(num)
        if len(num)>=14: #加上开头的'0b'有没有12位 二进制数是'0b1000001'这样排列的，最右边是第一位——2的0次方
            if num[-3:] == '011': # bit1-3对流层中
                if num[-12:-9] == '111': # bit10-12位是烟 elevated smoke的代码
                    output.append(1)
                    break
                if num[-12:-9] == '001':
                    output.append(1)
                    break
                '''elif num[-3:] == '100': # bit1-3平流层中
                    if num[-12:-9] == '100': #同上
                        output.append(1)
                        break'''
            '''if num[-7:-5]=='01':
                output.append(1)
                break'''
        if j == 5514: #到最后了还没有搞完就给个0
            output.append(0)
outWorkbook = xlwt.Workbook()
sheetOut = outWorkbook.add_sheet('Smoke')
#print(len(output))
#print(output[2])
for k in range(len(output)):
    sheetOut.write(k,0,output[k])
outWorkbook.save(r'E:\SmokeDetection\source\CALIOP\marine.xls') #输出路径可以改
def transform_FCF(xlsxFCF):
    '''
    就是把FCF表格文件给做成1*4224的表格，0表示无烟，1表示有烟
    '''
    pass
