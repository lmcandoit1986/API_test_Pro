# server_test
## 优点

* 填鸭式补充用例，简单方便
* 参数定义多样化，支持默认填充，也支持自行定义，冲突以自定义优先采用
* 支持参数函数化定制，让值多样化
* 校验多样化，支持value值，type类型，接口返回整体校验
* 校验定位采用直接定位、jsonpath定位，简单强大，满足需求
* 支持个人用例校验
* 支持分模块执行
* 支持全用例执行
* 结果收集并上报数据库，统一展示

## 整体介绍

模块|目录|功能|备注
:---:|:---:|:---:|:---:
用例|Cases/|yaml 文件，用于组织用例|～
测试入口|Entry/run.py|测试用例运行入口|
方法封装|Utils/|解析数据，组成用例执行并验证|

### 环境
* Python3
* 相关模块
    * numpy
    * yaml 
    * jsonpath

## 用例编辑规范

文件|备注
:---:|:---:
Default|默认配置参数，分server/get方法param/post方法header和body
其他|用例

### 用例格式-Get
    注意：当入参中的参数 和 Default中的参数有冲突时，保留个人的入参

    Server: default  #Server 可指定服务器，也可以默认 default，使用 Default文件的server 值
    Cases:  # Case体
      - CaseName: getBXList # 用例名称
        charger:  xx # 负责人
        detail: 获取投保保单列表 #用例详情
        api: /mapi/policyList.json # 接口信息
        method: get # 请求方式
        In: #入参
          default: true # 如果需要添加默认的参数，则为true，添加Default中的param 项
          pageNo: 1 # 接口特有的业务参数
          type: 1 # 接口特有的业务参数
        Out: #出参 验证
          type: key 
          code: 1
          # 支持验证方式 key，验证字段内容，
          # 支持验证方式 type，验证返回各字段数据类型，支持验证：int，str，dict，list，bool,none
          # 支持验证方式 file，直接验证整个返回结果完全校对，需要提供标准的结果保存文件名，放到Utils/Result文件夹下即可；
          # 举例
          type: type
          code: int
          msg: str
          
          # 举例 
          type: file
          file: standard_policyList          
### 用例格式-Post
    注意：当入参body中的参数 和 Default中的参数有冲突时，保留个人的入参
    Cases:  # Case体
      - CaseName: getBXList # 用例名称
        charger:  xx # 负责人
        detail: 获取投保保单列表 #用例详情
        api: /mapi/policyList.json # 接口信息
        method: post # 请求方式
        header: default #使用 Default文件中的 header，也可以自行定制
        body: # 接口特有的业务参数
          default: true # 添加Default文件中的 body，不添加为 false
          key1: 1
          key2: add
        Out: #出参 验证 同上
          type: key 
          code: 1

### 支持JSONPATH 定位

定位结果数据时，支持JsonPath定位更深层的数据，写法见JSONPath规范

Xpath|	JSONPath|	描述
:---:|:---:|:---:
/|	$	|跟节点
.	|@	|现行节点
/	|. or []	|取子节点
..	|n/a	|就是不管位置，选择所有符合条件的条件
 '*'	|*	|匹配所有元素节点
[]	|[]	|迭代器标示(可以在里面做简单的迭代操作，如数组下标，根据内容选值等)
&#124|	[,]	|支持迭代器中做多选
[]	|?()|	支持过滤操作
n/a	|()	|支持表达式计算
()	|n/a	|分组，JsonPath不支持     


举例：
        
        #定位{'code':1,'result':{'name':'ceshi','res':true}} 中的res
        $.result.res : true
        $['result']['res'] : true
        $..res : true
        以上三种写法都支持


## 用例执行入口

Entry/run.py

* 支持指定单个或多个用例执行
* 支持指定测试文件执行
* 支持指定文件夹执行
* 支持全部用例执行

* 支持接口多线程模拟访问，用于验证接口有判重的场景校验，该方法不做结果验证处理。

### 举例
        def test_example(self):
            case = self.readCasesFromDirectory('Medical') # 获取某个文件夹下的所有用例，用于获取各模块下的用例，目前不支持模块下再分文件夹
            #case = self.readCasesFromClass('Medical/List_bx') # 获取某个文件的所有用例
            #case = self.readAllCases() # 获取Cases/下的所有用例
            Request_Create.create(case) # 正常执行用例
            #Request_Create.create(case,'getBXList1') # 执行用例中的某个用例
            #Request_Create.create(case, 'getBXList1','getBXList2') # 执行用例中的多个用例
            #Request_Create.createThreading(case,2,'getBXList1') #该方法多线程调用2次
            
            
### 日志输出

        2019-07-22 09:56:54:INSTRUMENTATION_STATUS: CaseName=getBXList1
        2019-07-22 09:56:54:INSTRUMENTATION_STATUS: Detail=获取投保保单列表1
        2019-07-22 09:56:54:INSTRUMENTATION_STATUS: charger=xx
        2019-07-22 09:56:54:INSTRUMENTATION_STATUS: path=Cases/Medical/List_bx
        2019-07-22 10:23:06:INSTRUMENTATION_STATUS: result=Failed
        2019-07-22 10:23:06:INSTRUMENTATION_STATUS: log=数据不匹配，检查返回:{'code': 22, 'msg': '登陆令牌超时，请重新登陆', 'data': None}
        
        2019-07-22 10:23:06:INSTRUMENTATION_STATUS: result=Pass
        
        2019-07-22 09:56:54:INSTRUMENTATION_STATUS: thread=Thread-1
        2019-07-22 09:56:54:INSTRUMENTATION_STATUS: thread=Thread-2
        2019-07-22 09:56:55:INSTRUMENTATION_STATUS: thread=Thread-1,time=489
        2019-07-22 09:56:55:INSTRUMENTATION_STATUS:thread=Thread-1, res={'code': 22, 'msg': '登陆令牌超时，请重新登陆', 'data': None}
        2019-07-22 09:56:55:INSTRUMENTATION_STATUS: thread=Thread-2,time=492
        2019-07-22 09:56:55:INSTRUMENTATION_STATUS:thread=Thread-2, res={'code': 22, 'msg': '登陆令牌超时，请重新登陆', 'data': None}
        2019-07-22 10:23:06:INSTRUMENTATION_STATUS: result=Pass
## 基础方法

* Utils/Request_Create.create() 总入口，传入测试用例执行并验证结果

### 对接 http://152.136.202.79:9092/web/index
    统一执行入口：
    cd  ./API_test_Pro
    python3 Run_Collect_Upload.py 
    执行完成后输出结果查看地址：
    url:http://152.136.202.79:9092/web/watcher?only=201907240950
