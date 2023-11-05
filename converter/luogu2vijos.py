"""
# 将测试数据转换为Vijos兼容的格式
比如我有以下格式的测试数据：
```
Workspace
├── convert.py
├── testcase
    ├── asd1.in
    ├── asd1.out
    ├── asd2.in
    ├── asd2.out
    ├── .....
    ├── asd20.in
    ├── asd20.out
```
或者是这样：
```
Workspace
├── convert.py
├── testcase
    ├── in1.txt
    ├── out1.txt
    ├── in2.txt
    ├── out2.txt
    ├── .....
    ├── in20.txt
    ├── out20.txt
```
_ **文件名无所谓** _  
那么你只需要把`convert.py`放到与`testcase`目录的同级目录下，然后执行`python convert.py testcase`即可。  
转换后会自动删除`testcase`目录，生成`testcase-testcase-vijos.zip`文件，直接上传即可。  

程序会自动提取文件名中的数字，然后计算偏移量，并重新从$`0`$下标开始命名，最后生成`Config.ini`并写入压缩包
"""

import os
import zipfile
import re
import sys
import shutil

NAME_PREFIX = sys.argv[1]

for root, dirs, files in os.walk(f"./{NAME_PREFIX}"):
    print(files)

    zipf = zipfile.ZipFile(
        os.path.join(root, "..", f"{NAME_PREFIX}-testcase-vijos.zip"),
        "w",
        zipfile.ZIP_DEFLATED
    )

    # 创建`Input`和`Output`目录
    try:
        os.mkdir(os.path.join(root, "Input"))
        os.mkdir(os.path.join(root, "Output"))

        zipf.write(os.path.join(root, "Input"), "Input")
        zipf.write(os.path.join(root, "Output"), "Output")
    except Exception:
        pass

    # 遍历其中的文件
    InOffset = False
    OutOffset = False
    testcase = 0
    for file in files:
        if file.endswith(".in"):
            print("rename", root, file)
            iter = int(re.findall(r"\d+", file)[0]) # 提取字符串中的数字
            if InOffset == False:
                InOffset = iter
            iter -= InOffset
            testcase += 1
            os.rename(
                os.path.join(root, file),
                os.path.join(root, "Input", "input" + str(iter) + ".txt")
            )
            zipf.write(
                os.path.join(root, "Input", "input" + str(iter) + ".txt"),
                "Input/input" + str(iter) + ".txt"
            )

        # 将`数字.out`文件重命名为`output数字.txt`文件
        elif file.endswith(".out") or file.endswith(".ans"):
            print("rename", root, file)
            iter = int(re.findall(r"\d+", file)[0]) # 提取字符串中的数字
            if OutOffset == False:
                OutOffset = iter
            iter -= OutOffset
            testcase += 1
            os.rename(
                os.path.join(root, file),
                os.path.join(root, "Output", "output" + str(iter) + ".txt")
            )
            zipf.write(
                os.path.join(root, "Output", "output" + str(iter) + ".txt"),
                "Output/output" + str(iter) + ".txt"
            )
            
    # 创建`Config.ini`文件，并写入内容
    with open(os.path.join(root, "Config.ini"), "w+") as f:
        testcase = int(testcase / 2)
        score = int(100 / testcase)
        print("Config.ini", testcase, score)
        f.write(f"{testcase}\n")
        for i in range(testcase):
            f.write(f"input{i}.txt|output{i}.txt|5|{score}|536870912\n")
    zipf.write(os.path.join(root, "Config.ini"), "Config.ini")
            
    zipf.close()

    break

shutil.rmtree(f"./{NAME_PREFIX}")
