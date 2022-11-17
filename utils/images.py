import base64

from django.core.files.base import ContentFile


def parse_base64(data:str,name="")->ContentFile :
    if(data is None or data==""):
        return None
    format, imgstr = data.split(';base64,') 
    ext = format.split('/')[-1] 

    data = ContentFile(base64.b64decode(imgstr), name='temp.' if not name else name+'.' + ext)

    return data
