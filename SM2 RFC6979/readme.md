# <center>SM2 RFC6979实验报告</center>

>**课程名称     <u>创新创业实践课程</u>  **       
>
>**学生姓名   <u>李路岩</u>      学号  <u>202022180198</u>**     
>
>**学院   <u>网络空间安全</u>学院    专业  <u>信息安全</u>**   

[TOC]

## <center>实验思路</center>

>利用HMAC与HASH来生成一个又随机，又冷门的随机数k

## <center>关键代码</center>

```python
#---RFC4979中生成随机数k------
if sys.version[0] == '2':
    safe_ord = ord
else:
    safe_ord = lambda x: x
def bytes_to_int(x):
    o = 0
    for b in x:
        o = (o << 8) + safe_ord(b)
    return o
def deterministic_generate_k(msghash, priv):
    v = b'\x01' * 32
    k = b'\x00' * 32
    k = hmac.new(k, v+b'\x00'+priv+msghash, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v+b'\x01'+priv+msghash, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    return bytes_to_int(hmac.new(k, v, hashlib.sha256).digest())
i="123"
i_sha = hashlib.sha256(i.encode('utf-8')).digest()
i_priv=i.encode(encoding="utf8",errors="strict")
k=deterministic_generate_k(i_sha,i_priv)
print(k)
#---RFC4979中生成随机数k------
```



## <center>实验结果</center>

><img src="https://img.gejiba.com/images/2e8cae4627b37367a3b1560c3276809f.jpg" alt="SM2 6979" border="0">
可见加解密一致

验证签名成功
