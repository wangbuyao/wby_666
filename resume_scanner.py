import os
import pdfplumber
import re
import PySimpleGUI as sg
import csv
import time

# 岗位技能关键词列表，不区分大小写
keywords = ["仿真", "滤波", "Matlab", 'ZYNQ', 'FPGA', 'C++', 'C', 'Python', 'Linux', 'ROS', 'CAN', '串口', 'SPI', 'I2C', 'UART', 'USB', 'TCP', 'UDP', 'IP', 'RTOS', 'ARM', 'STM32']

#生成欢迎语
layout = [
    [sg.Text('欢迎使用简历扫描器！')],
    [sg.Text('')],
    [sg.Text('')],
    [sg.Text('开发者：WBY')]
]

# 生成复选框，选择关键词；生成输入框，以、分隔新增关键词
layout = [
    [sg.Text('请选择关键词：')],
    [sg.Checkbox(key, default=False, key=key) for key in keywords],
    # 生成全选键，用于全选列表中的所有关键词
    [sg.Button('全选',key='all')],
    [sg.B('取消全选',key='cancel')],
    [sg.Text('新增关键词：')],
    [sg.InputText(key='-IN-')],
    [sg.Text('选择简历文件夹：')],
    [sg.InputText(key='-FOLDER-'), sg.FolderBrowse()],
    [sg.Button('开始筛选'), sg.Button('退出')]
]

# 创建窗口
window = sg.Window('简历扫描', layout, font=('雅黑', 16))


# 读取窗口中的值
while True:
    event, values = window.read()
    if event in (None, '退出'):
        break
    # 若选中了全选键，则将所有关键词选中，反之则反
    if event == 'all':
        for key in keywords:
            window[key].update(True)
    if event == 'cancel':
        for key in keywords:
            window[key].update(False)
    if event == '开始筛选':
        # 读取关键词列表
        keywords = [key for key in keywords if values[key]]
        # 读取新增关键词
        new_keywords = values['-IN-'].split('、')
        # 将新增关键词添加到关键词列表中
        for new_keyword in new_keywords:
            if new_keyword != '':
                keywords.append(new_keyword)
        # 读取简历文件夹路径
        folder_path = values['-FOLDER-']
        # 关闭窗口
        window.close()
        # 新建csv文件，用于存储筛选结果,列名分别为“文件名”、“总击中次数”、“每个关键词的名称（key）”、“文件路径”
        with open('简历筛选' + time.strftime("%m_%d_%H_%M", time.localtime()) + '.csv', 'w', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(['文件名'] + ['总击中次数'] + list(keywords) + ['文件路径'] + ['筛选时间'])

            # 读取简历文件夹中的文件
            for file in os.listdir(folder_path):
                # 读取简历文件
                file_path = os.path.join(folder_path, file)
                with pdfplumber.open(file_path) as pdf:
                    # 读取简历文本
                    text = ''
                    for page in pdf.pages:
                        text += page.extract_text()
                        # 将nice_school中的key作为关键词，检查其是否在文本中出现,如出现则将其添加csv文件中，作为新的一列
                        nice_school = ['清华大学', '北京大学', '中国科学技术大学', '复旦大学', '上海交通大学', '南京大学', '浙江大学', '中国人民大学', '西安交通大学', '哈尔滨工业大学', '国防科技大学', '中国科学院大学', '北京航空航天大学', '同济大学', '北京师范大学', '武汉大学', '南开大学', '东南大学', '华中科技大学', '中山大学', '厦门大学', '北京理工大学', '电子科技大学', '上海财经大学', '天津大学', '四川大学', '山东大学', '西北工业大学', '华东师范大学', '对外经济贸易大学', '中央财经大学', '中南大学', '兰州大学', '华南理工大学', '吉林大学', '中国农业大学', '中国政法大学', '北京邮电大学', '北京外国语大学', '北京协和医学院', '中国社会科学院大学', '大连理工大学', '湖南大学', '南京航空航天大学', '东北大学', '重庆大学', '上海外国语大学', '南方科技大学', '中国传媒大学', '首都医科大学', '南京理工大学', '哈尔滨工程大学', '西安电子科技大学', '中国海洋大学', '北京交通大学', '上海科技大学', '南京医科大学', '华东理工大学', '南京农业大学', '北京科技大学', '郑州大学', '西南交通大学', '合肥工业大学', '武汉理工大学', '暨南大学', '华北电力大学', '西北农林科技大学', '天津医科大学', '中南财经政法大学', '中央民族大学', '华中师范大学', '南京师范大学', '河海大学', '西南大学', '上海大学', '长安大学', '东华大学', '北京工业大学', '中国矿业大学', '苏州大学', '西南政法大学', '西南财经大学', '上海对外经贸大学', '南京邮电大学', '北京语言大学', '中国矿业大学(北京)', '太原理工大学', '北京化工大学', '云南大学', '江南大学', '华中农业大学', '中国医科大学', '中国地质大学', '哈尔滨医科大学', '南方医科大学', '中国地质大学（北京）', '福州大学', '东北财经大学', '华东政法大学', '西北大学', '东北师范大学', '中国石油大学(华东)', '中国石油大学(北京)', '陕西师范大学', '华南师范大学', '南京财经大学', '安徽大学', '南昌大学', '深圳大学', '宁波大学', '华侨大学', '中国药科大学', '江西财经大学', '湖南师范大学', '南京信息工程大学', '广西大学', '杭州电子科技大学', '南京工业大学', '首都师范大学', '浙江工业大学', '燕山大学', '扬州大学', '大连海事大学', '河南大学', '南京林业大学', '青岛大学', '湘潭大学', '广东工业大学', '贵州大学', '武汉科技大学', '昆明理工大学', '安徽师范大学', '东北林业大学']
                        for key1 in nice_school:
                            if key1 in text:
                                nice_school = key1
                                break
                            # 若文本中没有出现nice_school中的关键词，则将nice_school设为“其他”
                            else:
                                nice_school = '其他'


                    # 统计每个pdf中每个关键词出现的次数，并以字典形式存储，不区分大小写
                    keywords_count = {keyword: len(re.findall(keyword, text, re.IGNORECASE)) for keyword in keywords}
                    # 将筛选结果写入csv文件中
                    csv_writer.writerow([file] + [sum(keywords_count.values())] + list(keywords_count.values()) + [file_path] + [nice_school] + [time.strftime("%Y-%m-%d-%H:%M", time.localtime())])

# 打印筛选结果
        print('筛选完成！')
        print('文件名：', file)
        print('文件路径：', file_path)
        print('关键词：', keywords)
        print('关键词出现次数：', keywords_count)
        print('高校名称：', nice_school)
        print('-' * 25)


        # 关闭窗口
        window.close()
        # 生成提示窗口
        layout = [
            [sg.Text('筛选完成！')],
            [sg.Button('退出')]
        ]
        window = sg.Window('简历扫描', layout)
        # 读取窗口中的值
        while True:
            event, values = window.read()
            if event in (None, '退出'):
                break
        # 关闭窗口
        window.close()
        break

