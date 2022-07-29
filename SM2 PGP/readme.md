# <center>SM2 PGP实验报告</center>

>**课程名称     <u>创新创业实践课程</u>  **       
>
>**学生姓名   <u>李路岩</u>      学号  <u>202022180198</u>**     
>
>**学院   <u>网络空间安全</u>学院    专业  <u>信息安全</u>**   

[TOC]

## <center>实验思路</center>

>PGP-Pretty Good Privacy，是一个基于RSA公钥和对称加密相结合的邮件加密软件。该系统能为电子邮件和文件存储应用过程提供认证业务和保密业务。
>
>PGP是个混合加密算法，它由一个对称加密算法、一个非对称加密算法、与单向散列算法以及一个随机数产生器组成的，每种算法都是PGP不可分割的组成部分。
>
>PGP让使用者可以安全地从未见过的人们通信，而事先并不需要任何保密的渠道用来传递密钥。
>
>**在这里，我使用了SM2和AES来进行实现**

## <center>关键代码</center>

```python
def PGP_EN(message, k):
    mode = AES.MODE_OFB
    iv = b'0000000000000000'
    cryptor = AES.new(k.encode('utf-8'), mode, iv)
    length = 16
    count = len(message)
    if count % length != 0:
        add = length - (count % length)
    else:
        add = 0
    message = message + ('\0' * add)#填充message长度

    ciphertext1 = cryptor.encrypt(message.encode('utf-8'))#AES与k加密message
    plaintext_bytes = k.encode('utf-8')
    ciphertext2 = sm2_crypt.encrypt(plaintext_bytes)#SM2加密会话密钥

    return ciphertext1, ciphertext2


def PGP_DE(mes1, mes2):
    mode = AES.MODE_OFB
    iv = b'0000000000000000'
    get_key = sm2_crypt.decrypt(mes2)
    print("用SM2私钥得到会话密钥k：", get_key.decode('utf-8'))
    cryptor = AES.new(get_key, mode, iv)
    plain_text = cryptor.decrypt(mes1)
    print("原加密消息值", plain_text.decode('utf-8'))

n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
G = [Gx, Gy]

#16进制的公钥和私钥
[sk, pk] = generate_key(a, p, n, G)
sk_bytes = hex(sk)[2:]
pk_bytes = hex(pk[0])[2:] + hex(pk[1])[2:]

sm2_crypt = sm2.CryptSM2(public_key=pk_bytes, private_key=sk_bytes)
message = "liluyan202022180198"
k = hex(random.randint(2 ** 127, 2 ** 128))[2:]
ciphertext1, ciphertext2 = PGP_EN(message, k)

print("想要加密的信息：", message)
print("随机生成的密钥)：", k)
print("用密钥加密消息：", ciphertext1)
print("加密会话密钥", ciphertext2)

PGP_DE(ciphertext1, ciphertext2)
```



## <center>实验结果</center>

<img src="https://img.gejiba.com/images/e0e2c79eb12f24b58ca8736c3fa42caf.png" alt="SM2 PGP" border="0">
