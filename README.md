# server_test
## 整体介绍

模块|目录|功能|备注
:---:|:---:|:---:|:---:
用例|Cases/|yaml 文件，用于组织用例|～
测试入口|Entry/run.py|测试用例运行入口|
方法封装|Utils/|解析数据，组成用例执行并验证|

## 用例编辑规范

文件|备注
:---:|:---:
Default|默认配置参数，分server/get方法param/post方法header和body
其他|用例

### 用例格式

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
