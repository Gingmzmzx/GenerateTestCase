# GenerateTestCase
生成测试数据

## 先决条件
Python3，目前只支持Windows系统  

测试环境：
- Python 3.10.10
- Windows11 22H2

## 使用方法
- 下载源码`git clone git@github.com:Gingmzmzx/GenerateTestCase.git`
- 将你的正解命名为`solve.cpp`并放到项目根目录中
- 编写`data.json`，具体格式见下文
- 运行`python generate.py`，程序会自动生成`testcase.zip`，该文件可以直接导入至`Vijos`OJ中
  您也可以在任何项目中引入`generate.py`，并参考`if __name__ == "__main__":`语句块中的代码来生成测试数据

## 其他工具
在[converter目录](/converter/)中，提供了一些转换工具。
- [luogu2vijos.py](/converter/luogu2vijos.py)可以将Luogu兼容的测试数据格式转换为Vijos兼容的测试数据
- [vijos2luogu.py](/converter/vijos2luogu.py)可以将Vijos兼容的测试数据格式转换为Luogu兼容的测试数据

### `data.json`格式
该文件内容有一个列表构成，其中每个元素代表一组测试数据，有以下格式：
- `data`：一个列表，其中每个元素代表一组输入数据，具体格式见下文
- `count`：一个整数，代表该组测试数据中测试数据的数量（默认为`10`）
- `memory_limit`：一个整数，代表该组测试数据的内存限制，单位为KB（默认为`16384`）
- `time_limit`：一个整数，代表该组测试数据的时间限制，单位为秒（默认为`1`）

其中`data`字段的格式如下：
- `name`：一个字符串或一个字符串列表，代表该组输入数据的名称
- `range`：一个列表或字典。
  当`name`为字符串时，`range`为一个列表，代表该组输入数据的范围；当`name`为字符串列表时，`range`为一个字典，其中的每个元素代表对应`name`输入数据的范围。  
  范围使用一个列表表示，列表中的第一个元素代表该组输入数据的最小值，第二个元素代表该组输入数据的最大值。生成数据时将从该区间中随机选择一个整数作为该组输入数据的值。比如`"N": [1, 100000]`表示 $`N \in [1, 100000]`$  
  您也可以使用前面已有的输入数据的名称来表示该组输入数据的范围。比如`"N": [1, "M"]`，表示 $`N \in [1, M]`$
- `count`：一个整数或一个字符串，代表该组输入数据的数量。
  当为整数时，表示该组输入数据的数量为该整数；
  当为字符串时，表示该组输入数据的数量为前面已有的输入数据的名称。比如`"count": "N"`，表示该组输入数据的总共数量为 $`N`$

下面是一个实例，其中包含两组测试数据。每组数据都有 $`10`$ 个测试点，每组数据的每个测试点都包含三组输入数据，但是第一组测试数据和第二组测试数据的 $`N, M, C`$ 的数据范围并不一样：
```json
[
    {
        "data": [
            {
                "name": ["N", "M", "C"],
                "range": {
                    "N": [1, 100],
                    "M": [2, 1000],
                    "C": [1, 100]
                },
                "count": 1
            },
            {
                "name": "S",
                "range": [1, "M"],
                "count": "N"
            },
            {
                "name": ["a", "b", "x"],
                "range": {
                    "a": [1, "N"],
                    "b": [1, "N"],
                    "x": [1, "M"]
                },
                "count": "C"
            }
        ],
        "count": 10,
        "memory_limit": 16384,
        "time_limit": 1
    },
    {
        "data": [
            {
                "name": ["N", "M", "C"],
                "range": {
                    "N": [1, 1000],
                    "M": [2, 100000],
                    "C": [1, 1000]
                },
                "count": 1
            },
            {
                "name": "S",
                "range": [1, "M"],
                "count": "N"
            },
            {
                "name": ["a", "b", "x"],
                "range": {
                    "a": [1, "N"],
                    "b": [1, "N"],
                    "x": [1, "M"]
                },
                "count": "C"
            }
        ],
        "count": 10,
        "memory_limit": 16384,
        "time_limit": 1
    }
]
```

### 实例
本仓库中已包含一个`solve.cpp`（[AKIOI OJ P1009](https://oj.xzynb.top/p/1009)）和`data.json`。您可以直接运行`python generate.py`生成数据看一下效果。

## 开源协议
本项目使用`Apache License 2.0`开源协议，并不得商用，请自觉遵守，谢谢。
