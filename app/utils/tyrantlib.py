from secrets import token_hex
from time import time


token_epoch = 1620198608689
base69chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_~;$*,'

def encode_b69(b10:int) -> str:
	b69 = ''
	while b10:
		b69 = base69chars[b10%69]+b69
		b10 //= 69
	return b69

def decode_b69(b69:str) -> int:
	b10 = 0
	for i in range(len(b69)):
			b10 += base69chars.index(b69[i])*(69**(len(b69)-i-1))
	return b10

def generate_token(user_id:int) -> str:
	return f'{encode_b69(user_id)}.{encode_b69(int((time()*1000)-token_epoch))}.{encode_b69(int(token_hex(20),16))}'