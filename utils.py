""" Useful functions. """

import hashlib

from Crypto.PublicKey import RSA
from urlparse import urlparse


def encrypt_RSA(pem_loc, message):
    ''' Encrypt data with RSA key.

    param: pem_loc Path to public key
    param: message String to be encrypted
    return encrypted string
    '''
    with open(pem_loc, 'r') as key_file:
        key = RSA.importKey(key_file.read())
    public_key = key.publickey()
    return public_key.encrypt(message.encode('utf-8'), 32)[0]


def decrypt_RSA(pem_loc, encrypted_msg):
    ''' Decrypt data with RSA key.
    param: pem_loc Path to your private key
    param: package String to be decrypted
    return decrypted string
    '''
    with open(pem_loc, 'r') as key_file:
        key = RSA.importKey(key_file.read())
    return key.decrypt(encrypted_msg)


def get_word_hash(word):
    """ Returns word salted hash. """
    prepare_str = word + 'salt'
    return hashlib.sha512(prepare_str.encode('utf-8')).hexdigest()


def uri_validator(uri):
    """ Checks if uri is valid or not. """
    try:
        result = urlparse(uri)
        return True if [result.scheme, result.netloc, result.path] else False
    except:
        return False


if __name__ == '__main__':
    test = 'text'
    enc = encrypt_RSA('/home/psavyuk/myapp/ChallengeTestWords/key.pem', test)
    #print(enc)
    #print(decrypt_RSA('/home/psavyuk/myapp/ChallengeTestWords/key.pem', enc))
