import pandas as pd

#读取excel文件
df = pd.read_excel(r'C:\Users\Zz\Desktop\pythonProject1\前百高校排名.xlsx', sheet_name='Sheet1')

# 第二列为高校名称，存为列表
schools = df.iloc[:, 1].tolist()
print(schools)


