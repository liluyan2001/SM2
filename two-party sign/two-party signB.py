import socket
from gmpy2 import invert
from random import randint
from os.path import commonprefix

#椭圆曲线参数

p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3    
a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
X = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
Y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2


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
HOST = ''
PORT = 8888
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((HOST, PORT))

print("B ready")

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