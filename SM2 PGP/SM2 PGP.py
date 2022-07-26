import random
from Crypto.Cipher import AES
from gmssl import sm2
import math

def kp(k, P, a, p):  # 倍点
    k_b = bin(k).replace('0b', '') 
    i = len(k_b) - 1
    R = P
    if i > 0:
        k = k - 2 ** i
        while i > 0:
            R = pANDq(R, R, a, p)
            i -= 1
        if k > 0:
            R = pANDq(R, kp(k, P, a, p), a, p)
    return R


def pANDq(P, Q, a, p):  # 点加函数
    if (math.isinf(P[0]) or math.isinf(P[1])) and (~math.isinf(Q[0]) and ~math.isinf(Q[1])):  # OP = P
        R = Q
    elif (~math.isinf(P[0]) and ~math.isinf(P[1])) and (math.isinf(Q[0]) or math.isinf(Q[1])):  # PO = P
        R = P
    elif (math.isinf(P[0]) or math.isinf(P[1])) and (math.isinf(Q[0]) or math.isinf(Q[1])):  # OO = O
        R = [float('inf'), float('inf')]
    else:
        if P != Q:
            l = Mod_Decimal(Q[1] - P[1], Q[0] - P[0], p)
        else:
            l = Mod_Decimal(3 * P[0] ** 2 + a, 2 * P[1], p)
        x = Mod(l ** 2 - P[0] - Q[0], p)
        y = Mod(l * (P[0] - x) - P[1], p)
        R = [x, y]
    return R


def Mod(a, b):  
    if math.isinf(a):
        return float('inf')
    else:
        return a % b


def Mod_Decimal(n, d, b):  # 小数模幂
    if d == 0:
        x = float('inf')
    elif n == 0:
        x = 0
    else:
        a = bin(b - 2).replace('0b', '')
        y = 1
        i = 0
        while i < len(a):  
            y = (y ** 2) % b  # 快速指数运算
            if a[i] == '1':
                y = (y * d) % b
            i += 1
        x = (y * n) % b
    return x


def generate_key(a, p, n, G): 

    sk = random.randint(1, n - 2)
    pk = kp(sk, G, a, p)
    return sk, pk


def Legendre(n, p):  # 判断是否为二次剩余
    return pow(n, (p - 1) // 2, p)


def Tonelli_Shanks(n, p):  # Tonelli-Shanks算法求二次剩余
    assert Legendre(n, p) == 1
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    for z in range(2, p):
        if Legendre(z, p) == p - 1:
            c = pow(z, q, p)
            break
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    if t % p == 1:
        return r
    else:
        i = 0
        while t % p != 1:
            temp = pow(t, 2 ** (i + 1), p)
            i += 1
            if temp % p == 1:
                b = pow(c, 2 ** (m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0
        return r


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