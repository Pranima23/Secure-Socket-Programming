import unittest
import client, server
from secure import *


class TestEncryptDecrypt(unittest.TestCase):
    
    def test_generateRSAKey(self):
        """
        test to check generated keys are RSA keys
        """
        private_key, public_key = generateRSAKey()
        self.assertTrue(isinstance(private_key, RSA.RsaKey))
        self.assertTrue(isinstance(public_key, RSA.RsaKey))
        
        
    def test_generateSessionKey(self):
        """
        test to check generated AES key is of 16 bytes
        """
        session_key = generateSessionKey()
        self.assertEqual(len(session_key), 16)
        
    def test_encryptSessionKey(self):
        """
        test to check session key is encrypted
        """
        private_key, public_key = generateRSAKey()
        session_key = generateSessionKey()
        enc_session_key = encryptSessionKey(session_key, public_key)
        self.assertNotEqual(enc_session_key, session_key)
        
    def test_decryptSessionKey(self):
        """
        test to check decrypted session key matches original session key
        """
        private_key, public_key = generateRSAKey()
        session_key = generateSessionKey()
        enc_session_key = encryptSessionKey(session_key, public_key)
        decrypted_session_key = decryptSessionKey(enc_session_key, private_key)
        self.assertEqual(decrypted_session_key, session_key)
        
    def test_encryptData(self):
        """
        test to check data is encrypted using AES key
        """
        session_key = generateSessionKey()
        data = b"This is a test message"
        encrypted_data = encryptData(data, session_key)
        self.assertNotEqual(encrypted_data, data)
        
    def test_decryptData(self):
        """
        test to check decrypted data matches original data
        """
        session_key = generateSessionKey()
        data = b"This is a test message"
        encrypted_data = encryptData(data, session_key)
        decrypted_data = decryptData(encrypted_data, session_key)
        self.assertEqual(decrypted_data, data)

class TestServerMessageSanitization(unittest.TestCase):
        
    def test_sanitizeRequest(self):
        """
        test to check sanitization of request from client
        """
        actual_message = server.sanitizeRequest(b"hello<script>alert('hacked');</script>")
        expected_message = "helloscriptalerthackedscript"
        self.assertEqual(actual_message, expected_message)
        
if __name__ == "__main__":
    unittest.main()