# Setup your own cloud for Software as a Service (SaaS) over the existing LAN in your laboratory.
# In this assignment you have to write your own code for cloud controller using open-source
# technologies to implement with HDFS. Implement the basic operations may be like to divide the
# file in segments/blocks and upload/ download file on/from cloud in encrypted form.


# !pip install hdfs
# !pip install cryptography

from hdfs import InsecureClient
from cryptography.fernet import Fernet
import os


class CloudController:
    def __init__(self, hdfs_url):
        self.client = InsecureClient(hdfs_url)

    def upload_file(self, local_file_path, cloud_file_path):
        with open(local_file_path, 'rb') as local_file:
            self.client.upload(cloud_file_path, local_file)

    def download_file(self, cloud_file_path, local_file_path):
        with self.client.read(cloud_file_path) as cloud_file, open(local_file_path, 'wb') as local_file:
            for chunk in cloud_file:
                local_file.write(chunk)

    def encrypt_file(self, file_path):
        # Implement your decryption logic here
        pass

    def decrypt_file(self, file_path):
        # Implement your decryption logic here
        pass

    # Example usage
if __name__ == "__main__":
    cloud_controller = CloudController('http:localhost:50070')

    # Upload a sfile to the cloud
    cloud_controller.upload_file('local-file.txt', '/cloud-files/file.txt')

    # Download a file from the cloud
    cloud_controller.download_file(
        '/cloud-files/file.txt', 'downloaded-file.txt')

    # Encrypt a file
    cloud_controller.encrypt_file('local-file.txt')

    # Decrypt a file
    cloud_controller.decrypt_file('encrypted-file.txt')


# class CloudController:
#     def __init__(self, hdfs_url, encryption_key):
#         self.client = InsecureClient(hdfs_url)
#         self.encryption_key = encryption_key.encode()
#         self.cipher_suite = Fernet(self.encryption_key)

#     def encrypt_file(self, file_path):
#         with open(file_path, 'rb') as file:
#             file_data = file.read()
#             encrypted_data = self.cipher_suite.encrypt(file_data)
#             encrypted_file_path = file_path + ".encrypted"
#             with open(encrypted_file_path, 'wb') as encrypted_file:
#                 encrypted_file.write(encrypted_data)
#             self.client.upload('/cloud-files/' + os.path.basename(encrypted_file_path), encrypted_file_path)
#             os.remove(encrypted_file_path)

#     def decrypt_file(self, encrypted_file_path, decrypted_file_path):
#         with self.client.read(encrypted_file_path) as encrypted_file, open(decrypted_file_path, 'wb') as decrypted_file:
#             encrypted_data = encrypted_file.read()
#             decrypted_data = self.cipher_suite.decrypt(encrypted_data)
#             decrypted_file.write(decrypted_data)
