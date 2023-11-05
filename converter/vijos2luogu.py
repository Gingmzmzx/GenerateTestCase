import os
import shutil

# 将Vijos格式的测试数据转换为Luogu兼容的格式
# 将从Vijos下载的测试数据放到与本脚本同级目录下，并重命名为`testcase.zip`，然后执行本脚本即可。

def convert():
    # 解压`testcase.zip`
    shutil.unpack_archive('testcase.zip', 'testcase', 'zip')
    # 删除`testcase.zip`
    os.remove('testcase.zip')
    # 将testcase/Input文件夹中的所有文件移动到testcase文件夹中
    for root, dirs, files in os.walk('testcase/Input'):
        for file in files:
            shutil.move(os.path.join(root, file), os.path.join('testcase', file))
    # 将testcase/Output文件夹中的所有文件移动到testcase文件夹中
    for root, dirs, files in os.walk('testcase/Output'):
        for file in files:
            shutil.move(os.path.join(root, file), os.path.join('testcase', file))
    # 删除testcase/Input文件夹
    shutil.rmtree('testcase/Input')
    # 删除testcase/Output文件夹
    shutil.rmtree('testcase/Output')
    # 删除testcase/Config.ini
    os.remove('testcase/Config.ini')

    for root, dirs, files in os.walk('testcase'):
        for file in files:
            print(file)
            if file.endswith('.txt'):
                if "in" in file:
                    shutil.move(os.path.join(root, file), os.path.join(root, str(int(file.split(".")[0].replace("input", "")) + 1) + '.in'))
                elif "out" in file:
                    shutil.move(os.path.join(root, file), os.path.join(root, str(int(file.split(".")[0].replace("output", "")) + 1) + '.out'))
    
    # 将testcase文件夹中的所有文件添加到testcase-luogu.zip中
    shutil.make_archive('testcase-luogu', 'zip', 'testcase')
    # 删除testcase文件夹
    shutil.rmtree('testcase')

if __name__ == '__main__':
    convert()