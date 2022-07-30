# <center>two-party sign实验报告</center>

>**课程名称     <u>创新创业实践课程</u>  **       
>
>**学生姓名   <u>李路岩</u>      学号  <u>202022180198</u>**     
>
>**学院   <u>网络空间安全</u>学院    专业  <u>信息安全</u>**   

[TOC]

## <center>实验思路</center>

<a href="https://img.gejiba.com/image/EyecJ8"><img src="https://img.gejiba.com/images/28ce38426fd2941fc4bbdb668cba0f45.png" alt="28ce38426fd2941fc4bbdb668cba0f45.png" border="0"></a>

>**1.A生成私钥的一个d1，计算P1，发送给B**
>
>**2.B生成私钥的另一个d2,计算公钥P**
>
>**3.A计算一个Z并计算e，和Q1发送给B**
>
>**4.B收到后计算r，s2，s3**
>
>5.A利用r,s2,s3来输出签名
>
>****

## <center>关键代码</center>

用户A：

```python
    # 生成d1
    d1 = randint(1,n-1)
    
    # 计算P1 = d1^(-1) * G
    P1 = kp(X,Y,invert(d1,p))
    x,y = hex(P1[0]),hex(P1[1])
    
    # 向B发送P1
    addr = (HOST, PORT)
    client.sendto(x.encode('utf-8'), addr)
    client.sendto(y.encode('utf-8'), addr)

    #计算ZA
    m = "liluyan202022180198"
    m = hex(int(binascii.b2a_hex(m.encode()).decode(), 16)).upper()[2:]
    ID_A = "sduliluyan"
    ID_A = hex(int(binascii.b2a_hex(ID_A.encode()).decode(), 16)).upper()[2:]
    ENTL_A = '{:04X}'.format(len(ID_A) * 4)

    #级联
    ma = ENTL_A + ID_A + '{:064X}'.format(a) + '{:064X}'.format(b) + '{:064X}'.format(X) + '{:064X}'.format(Y)

    #计算级联后的哈希
    ma_byte=str_to_byte(ma)
    ZA = sm3.sm3_hash(func.bytes_to_list(ma_byte))
    ZA_m_byte=str_to_byte(ZA+m)
    e = sm3.sm3_hash(func.bytes_to_list(ZA_m_byte))
    
    # 生成随机数k1
    k1 = randint(1,n-1)

    # 计算Q1 = k1 * G
    Q1 = kp(X,Y,k1)
    x,y = hex(Q1[0]),hex(Q1[1])

    # 向B发送Q1,e
    client.sendto(x.encode('utf-8'),addr)
    client.sendto(y.encode('utf-8'),addr)
    client.sendto(e.encode('utf-8'),addr)

    # 从B接收r,s2,s3
    r,addr = client.recvfrom(1024)
    r = int(r.decode(),16)
    s2,addr = client.recvfrom(1024)
    s2 = int(s2.decode(),16)
    s3,addr = client.recvfrom(1024)
    s3 = int(s3.decode(),16)

    # 计算s
    s=((d1 * k1) * s2 + d1 * s3 - r)%n
    if s!=0 or s!= n - r:
        print("Sign:")
        print((hex(r),hex(s)))
    client.close()
```

用户B：

```python
# 生成d2
d2 = randint(1,n-1)

# 从A接收P1
x,addr = client.recvfrom(1024)
x = int(x.decode(),16)
y,addr = client.recvfrom(1024)
y = int(y.decode(),16)

# 计算公钥P=d2^-1 * p1 - G
P1 = (x,y)
P = kp(P1[0],P1[1],invert(d2,p))
P = add(P[0],P[1],X,-Y)

# 从A接收Q1与e
x,addr = client.recvfrom(1024)
x = int(x.decode(),16)
y,addr = client.recvfrom(1024)
y = int(y.decode(),16)
Q1 = (x,y)
e,addr = client.recvfrom(1024)
e = int(e.decode(),16)

# 生成随机数k2,k3
k2 = randint(1,n-1)
k3 = randint(1,n-1)

# 计算Q2 = k2 * G
Q2 = kp(X,Y,k2)

# 计算(x1,y1) = k3 * Q1 + Q2
x1,y1 = kp(Q1[0],Q1[1],k3)
x1,y1 = add(x1,y1,Q2[0],Q2[1])
r =(x1 + e)%n
s2 = (d2 * k3)%n
s3 = (d2 * (r+k2))%n

# 向A发送r,s2,s3
client.sendto(hex(r).encode(),addr)
client.sendto(hex(s2).encode(),addr)
client.sendto(hex(s3).encode(),addr)

print("Closed!")
```



## <center>实验结果</center>

用户B：

<a href="https://img.gejiba.com/image/EyewBs"><img src="https://img.gejiba.com/images/7c2db9200a318153420ba667219d6ba0.png" alt="7c2db9200a318153420ba667219d6ba0.png" border="0"></a>

用户A：

<a href="https://img.gejiba.com/image/Eye4ri"><img src="https://img.gejiba.com/images/a84caf703fee28639f032bcbd519f51b.png" alt="a84caf703fee28639f032bcbd519f51b.png" border="0"></a>
