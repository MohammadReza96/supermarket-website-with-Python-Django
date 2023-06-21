import os 
import uuid

# fileupload module whhich is used for FileField & ImageField in models
#--------------------------------------------------------------
class FileUploader:
    def __init__(self,main_directory:str,perfix:str):
        self.__main_directory=main_directory
        self.__prefix=perfix
    def upload_to(self,instance,filename):
        filename,ext=os.path.splitext(filename)
        return f'{self.__main_directory}/{self.__prefix}/{filename}{uuid.uuid4()}{ext}'
    
# for testing module
#------------------------
if __name__=="__main__":
    file_uploder=FileUploader('media','images')
    print(file_uploder.upload_to('iphone_13','iphone_13_pro_max.jpeg'))