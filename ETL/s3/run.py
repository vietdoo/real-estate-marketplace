from s3 import S3

S3_client = S3()

S3_client.upload_file_to_s3(bucket_name = 'tigerlake', input_name = 'rain.png', output_name = 'images/rain29.png')