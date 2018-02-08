import boto3

class UploadS3Driver(object):
    
    def __init__(self, Upload, StorageConfig):
        self.upload = Upload
        self.config = StorageConfig

    def store(self, fileitem, location=None):
        file_location = self.upload.driver('disk').store(fileitem)

        session = boto3.Session(
            aws_access_key_id=self.config.DRIVERS['s3']['client'],
            aws_secret_access_key=self.config.DRIVERS['s3']['secret'],
        )

        s3 = session.resource('s3')

        s3.meta.client.upload_file(
            file_location, self.config.DRIVERS['s3']['bucket'], fileitem.filename)
    def storeAs(self):
        pass
