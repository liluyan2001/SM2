import sys
import socket
import binascii
from gmpy2 import invert
from random import randint
from os.path import commonprefix
from gmssl import sm3,func

p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3    
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
X = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
def str_to_byte(str):  # 字符串转换成byte
    ml = len(str)
    msg_byte = []
    msg_bytearray = str.encode('utf-8')
    for i in range(ml):
        msg_byte.append(msg_bytearray[i])
    return msg_byte

#椭圆曲线上的加法
def add(x1,y1,x2,y2):
    if x1 == x2 and y1 == p-y2:
        return False
    if x1!=x2:
        r=((y2 - y1) * invert(x2 - x1, p))%p#invert函数用于求模逆
    else:
        r=(((3 * x1 * x1 + a)%p) * invert(2 * y1, p))%p
        
    x = (r * - x1 - x2)%p
    y = (r * (x1 - x) - y1)%p
    return x,y

#点乘k*(x,y)
def kp(x,y,k):
    k = k%p
    k = bin(k)[2:]
    rx,ry = x,y
    for i in range(1,len(k)):
        rx,ry = add(rx, ry, rx, ry)
        if k[i] == '1':
            rx,ry = add(rx, ry, x, y)
    return rx%p,ry%p

#网络部分
HOST = '127.0.0.1'
PORT = 8888
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#尝试连接
try:
    client.connect((HOST, PORT))
    print("A ready")
except Exception:
    print('failed!')
    sys.exit()
else:

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