path = 'tcp.txt'
key = 42 #from encrypt.py
output = 'decrypted'  
with open(path, 'rb') as f:
    tcp_bytes = f.read()

decrypted_data = bytes([(b - key + 256) % 256 for b in tcp_bytes])

with open(output, 'wb') as f_out:
    f_out.write(decrypted_data)
