import os

from Crypto.PublicKey import RSA
from Crypto import Random

def generate_keys(path, name='key.pem'):
    path_to_key = os.path.join(path, name)
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    with open(path_to_key, 'w') as fl:
        fl.write(str(key.exportKey('PEM').decode('utf-8')))

if __name__ == '__main__':
   dir_path = os.path.dirname(os.path.realpath(__file__))
   print('PEM file will be here: {}'.format(dir_path))
   generate_keys(dir_path)
