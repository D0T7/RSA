import time
from src.rsa import RSA



st = time.perf_counter()
public_key, private_key = RSA.generate_keys(2048)
message = "This is a test message"
et = time.perf_counter()
print(f"Key generation time = {et-st:.5f}")



st = time.perf_counter()
ec_l = []
for m in message:
    ec_l.append(RSA.encrypt(ord(m), public_key))

et = time.perf_counter()
print(f"Encrypting time = {et-st:.5f}")




st = time.perf_counter()
res = ""
for ec in ec_l:
    res += chr(RSA.decrypt(ec, private_key))

print("Decrypted message:", res)
et = time.perf_counter()
print(f"Decryption time = {et-st:.5f}")
