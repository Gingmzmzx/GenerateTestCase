import json
import random
import os
import shutil
import time
import zipfile

def AppendInputData(content, file: int, split: str = " "):
    with open(f"Input/input{file}.txt", "a+", encoding="utf-8") as f:
        f.write(f"{content}{split}")

def GetJsonData(file:str = "data.json"):
    with open(file, "r", encoding="utf-8") as f:
        json_data = json.loads(f.read())
    return json_data

def SetRandomSeed(seed: int = int(time.time())):
    random.seed(seed)
    return seed

def ClearData():
    # Clear data
    # 删除Input和Output目录
    if os.path.exists("Input"):
        shutil.rmtree("Input")
    if os.path.exists("Output"):
        shutil.rmtree("Output")
    # 创建Input和Output目录
    os.mkdir("Input")
    os.mkdir("Output")
    # 删除testcase.zip
    if os.path.exists("testcase.zip"):
        os.remove("testcase.zip")
    # 删除Config.ini
    if os.path.exists("Config.ini"):
        os.remove("Config.ini")
    # 删除solve.exe
    if os.path.exists("solve.exe"):
        os.remove("solve.exe")

def GenerateInputFile(file: str="data.json"):
    # Generate input data
    json_data = GetJsonData(file)
    vars = dict()
    baseCnt = 0
    for item in json_data:
        data = item.get("data", list())
        groupCount = int(item.get("count", 10))
        print("Group 1", "count", groupCount, "data", data)
        for dataCnt in range(baseCnt, baseCnt+groupCount):
            print("generate the", dataCnt, "th input data")
            for i in data:
                name, rang, count = i.get("name"), i.get("range"), i.get("count")
                if isinstance(count, str):
                    count = int(vars.get(count))
                for Cnt in range(count):
                    if isinstance(name, str):
                        print("No.", Cnt, "name", name, "count", count, "range", rang)
                        if not isinstance(rang, list):
                            raise Exception("single name but range not list")
                        lrange, rrange = rang[0], rang[1]
                        if isinstance(lrange, str):
                            lrange = int(vars.get(lrange))
                        if isinstance(rrange, str):
                            rrange = int(vars.get(rrange))
                        vars[name] = random.randint(lrange, rrange)
                        AppendInputData(vars[name], dataCnt)
                    elif isinstance(name, list):
                        if not isinstance(rang, dict):
                            raise Exception("multiple name but range not dict")
                        for j in name:
                            print("No.", Cnt, "name", j, "count", count, "range", rang.get(j))
                            lrange, rrange = rang.get(j)[0], rang.get(j)[1]
                            if isinstance(lrange, str):
                                lrange = int(vars.get(lrange))
                            if isinstance(rrange, str):
                                rrange = int(vars.get(rrange))
                            vars[j] = random.randint(lrange, rrange)
                            AppendInputData(vars[j], dataCnt)
                    AppendInputData("", dataCnt, "\n")
                AppendInputData("", dataCnt, "\n")
        baseCnt += groupCount

def GenerateOutputFile(file: str="data.json"):
    # Generate output data by `solve.cpp`
    # Make sure that you have called `GenerateInputFile` before calling this function
    json_data = GetJsonData(file)
    os.system("g++ solve.cpp -o solve.exe -std=c++14 -O2 -static") # 编译参数参照CSP-S2023编译参数
    baseCnt = 0
    for item in json_data:
        count = int(item.get("count", 10))
        for i in range(baseCnt, baseCnt + count):
            os.system(f".\solve.exe < Input/input{i}.txt > Output/output{i}.txt")
        baseCnt += count
    os.remove("solve.exe")

def GenerateConfigIni(file: str="data.json"):
    json_data = GetJsonData(file)
    testcase = 0
    for item in json_data:
        count = int(item.get("count", 10))
        testcase += count
    
    # 创建`Config.ini`文件，并写入内容
    with open("Config.ini", "w+") as f:
        score = int(100 / testcase)
        print("Config.ini", "number of testcase", testcase, "score", score)
        f.write(f"{testcase}\n")
        
        baseCnt = 0
        for item in json_data:
            count = int(item.get("count", 10))
            memory_limit = int(item.get("memory_limit", 16384))
            time_limit = int(item.get("time_limit", 1))
            for i in range(baseCnt, baseCnt + count):
                f.write(f"input{i}.txt|output{i}.txt|{time_limit}|{score}|{memory_limit}\n")
            baseCnt += count

def GenerateZipFile(file: str = "testcase.zip"):
    # Generate zip file
    zipf = zipfile.ZipFile(file, "w", zipfile.ZIP_DEFLATED)
    for file in os.listdir("Input"):
        zipf.write(os.path.join("Input", file), os.path.join("Input", file))
    for file in os.listdir("Output"):
        zipf.write(os.path.join("Output", file), os.path.join("Output", file))
    zipf.write("Config.ini", "Config.ini")
    zipf.close()

if __name__ == "__main__":
    # Set random seed
    SetRandomSeed()
    # Clear data
    ClearData()
    # Generate input data
    GenerateInputFile()
    # Generate output data by `solve.cpp`
    GenerateOutputFile()
    # Generate `Config.ini`
    GenerateConfigIni()
    # Generate zip file
    GenerateZipFile()