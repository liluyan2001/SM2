# <center>two-party Decrypt实验报告</center>

>**课程名称     <u>创新创业实践课程</u>  **       
>
>**学生姓名   <u>李路岩</u>      学号  <u>202022180198</u>**     
>
>**学院   <u>网络空间安全</u>学院    专业  <u>信息安全</u>**   

[TOC]

## <center>实验思路</center>

<a href="https://img.gejiba.com/image/EyHBOO"><img src="https://img.gejiba.com/images/860b22e9ec5d87cafc6f6b91662d1350.png" alt="860b22e9ec5d87cafc6f6b91662d1350.png" border="0"></a>

>**1.A生成私钥d1，B生成私钥d2**
>
>**2.A生成密文传给B**
>
>**3.B计算T2发给A**
>
>**4.A解密**
>
>****

## <center>关键代码</center>

用户A：

```python
 # 生成子私钥 d1
    d1 = func.random_hex(64)
    
    # 获取密文 C = C1||C2||C3
    C1 = (func.random_hex(64),func.random_hex(64))
    C2 = func.random_hex(38)
    C3 = func.random_hex(64)
    
    # 计算T1 = d1^(-1) * C1
    T1 = kp(C1[0], C1[1], invert(d1, p))
    x, y = hex(T1[0]), hex(T1[1])
    klen = len(hex(C2)[2:])*4
    
    # 将T1发送给B
    addr = (HOST, PORT)
    s.sendto(x.encode('utf-8'), addr)
    s.sendto(y.encode('utf-8'), addr)

    # 从B接收到T2
    x1, addr = s.recvfrom(1024)
    x1 = int(x1.decode(), 16)
    y1, addr = s.recvfrom(1024)
    y1 = int(y1.decode(), 16)
    T2 = (x1, y1)
    
    # 计算T2 - C1
    x2, y2 = add(T2[0], T2[1], C1[0], -C1[1])
    x2, y2 = '{:0256b}'.format(x2), '{:0256b}'.format(y2)
    # t= generate_key(x2||y2,klen)
    t = generate_key(x2 + y2, klen)
    # M2 = C2 ^ t
    M2 = C2 ^ int(t,2)
    m = hex(int(x2,2)).upper()[2:] + hex(M2).upper()[2:] + hex(int(y2,2)).upper()[2:]

    # SM3
    m_byte=str_to_byte(m)
    u = sm3.sm3_hash(func.bytes_to_list(m_byte))
    if (u == C3):
        print(hex(M2).upper()[2:])
    print("result:",hex(M2)[2:])
    s.close() 
```

用户B：

```python
# 生成子私钥 d2
d2 = func.random_hex(64)

# 从A接收到T1
x, addr = s.recvfrom(1024)
x = int(x.decode(), 16)
y, addr = s.recvfrom(1024)
y = int(y.decode(), 16)
T1 = (x, y)

# 计算T2 = d2^(-1) * T1
T2 = kp(x, y, invert(d2, p))
x, y = hex(T2[0]), hex(T2[1])

s.sendto(x.encode('utf-8'), addr)
s.sendto(y.encode('utf-8'), addr)

print("Closed!")
```



## <center>实验结果</center>

用户B：

<a href="https://img.gejiba.com/image/EyHhfU"><img src="https://img.gejiba.com/images/1fcc745e6688a4bd3d2796102e221ab4.png" alt="1fcc745e6688a4bd3d2796102e221ab4.png" border="0"></a>

用户A：

<a href="https://img.gejiba.com/image/EyHziA"><img src="https://img.gejiba.com/images/e5c15df162f06269e9bc451ae29999a2.png" alt="e5c15df162f06269e9bc451ae29999a2.png" border="0"></a>
