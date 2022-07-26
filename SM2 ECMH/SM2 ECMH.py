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