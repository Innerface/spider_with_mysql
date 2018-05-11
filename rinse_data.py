# -*- coding: utf-8 -*-
# Author: YuYuE (1019303381@qq.com) 2018.02.05 
import os  
def file_name(file_dir):   
	L=[]   
	root_out = "D:/NLP/fact_triple_extraction/washedtext/"
	for root, dirs, files in os.walk(file_dir):  
		for file in files:  
			if os.path.splitext(file)[1] == '.txt':  
				L.append(os.path.join(root, file))  
				file_path = os.path.join(root, file)
				file_out = os.path.join(root_out, file)
				print(file_path)
				with open(file_path,"r",encoding="utf-8") as f:
					lines = f.readlines()
					#print(lines)
				with open(file_out,"w",encoding="utf-8") as f_w:
					for line in lines:
						# if line.find('，') == -1 and line.find('、') == -1 and line.find('。') == -1 and len(line)<18:
							# continue
						f_w.write(line)
				# exit()
	return L  

file = "D:/NLP/fact_triple_extraction/originaltext/"
file_list = file_name(file)
print(file_list)
#其中os.path.splitext()函数将路径拆分为文件名+扩展名