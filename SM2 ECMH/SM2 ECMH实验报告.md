# <center>SM2 ECMH实验报告</center>

>**课程名称     <u>创新创业实践课程</u>  **       
>
>**学生姓名   <u>李路岩</u>      学号  <u>202022180198</u>**     
>
>**学院   <u>网络空间安全</u>学院    专业  <u>信息安全</u>**   

[TOC]

## <center>实验思路</center>

>ECMH是一个32字节的值，它是为一组数据元素唯一确定地定义的，无论其顺序如何。
>
>该模块允许为具有以下属性的集合计算加密安全哈希：
>
>集合元素的顺序不影响哈希
>
>可以将元素添加到集合中，而无需重新计算整个集合

## <center>关键代码</center>

```python
#主函数部分
from ECMH_function import MultiHash

set1 = (b'liluyan',)
set3 = (b'liluyan', b'202022180198')
set4 = (b'202022180198', b'liluyan')
set2 = (b'liluyan',b'liluyan')
result1 = MultiHash(set1)
result2 = MultiHash(set2)
result3 = MultiHash(set3)
result4 = MultiHash(set4)
print("hash(set1) = ", result1)
print("hash(set2) = ", result2)
print("hash(set3) = ", result3)
print("hash(set4) = ", result4)
```



## <center>实验结果</center>

><img src="https://img.gejiba.com/images/c1d07ee013a62e37e23d70cb29505d42.png" alt="SM2 ECMH" border="0">

可见能够实现ECMH验证