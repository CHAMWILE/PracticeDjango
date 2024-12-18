import datetime
import logging
import os
import uuid
from base64 import b64decode

from django.conf import settings

logger = logging.getLogger(__name__)


class UploadFile:
    @staticmethod
    def base64_handler(input,file_extension,parent_folder):
        bytes = b64decode(input.base64_string, validate=True)

        new_folder = str(parent_folder)+"/"+datetime.datetime.now().strftime("%Y-%m-%d")
        location = ""

        try:
            os.makedirs(os.path.join(str(settings.MEDIA_ROOT) +"/"+new_folder))
        except:
            pass
        finally:
            location = str(settings.MEDIA_ROOT)+"/"+new_folder

        sting_name = uuid.uuid4()
        absolute_file_path = "{}/{}{}".format(location, sting_name, file_extension)
        relative_file_path = "/{}/{}{}".format(new_folder,sting_name,file_extension)

        new_file = open(str(absolute_file_path), 'wb')
        new_file.write(bytes)
        new_file.close()


        return relative_file_path
    
