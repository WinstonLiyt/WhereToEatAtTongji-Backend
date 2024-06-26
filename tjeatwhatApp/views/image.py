from django.http import JsonResponse
from django.conf import settings
import os
from uuid import uuid4

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes

from tjeatwhatApp.extensions.auth import JwtQueryParamsAuthentication,EmptyParamsAuthentication
#这里只负责图片上传到后端并存储到特定文件夹，
#注意！！！没有存到数据库，数据库的路径要求其他模块存储文件的路径，从而在前端可以使用url调用图片

#!!!为了防止图片路径重合，这里需要前端修改文件的name,比如加上时间和用户id，或者随机数，防止数据覆盖
@api_view(['POST'])
@authentication_classes([JwtQueryParamsAuthentication])
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
      
        file= request.FILES['file']
        # 处理上传的文件，保存到服务器上
        _, ext = os.path.splitext(file.name)
        new_name = f"images/{uuid4().hex}{ext}"

        nn_name=f"/media/{new_name}"

        where = '%s/%s' % (settings.MEDIA_ROOT, new_name)
        # 分块保存image
        content = file.chunks()
        with open(where, 'wb') as f:
            for i in content:
                f.write(i)
    
        return JsonResponse({'new_name':nn_name,'message': 'File uploaded successfully'},status=200)
    else:
        return JsonResponse({'message': 'Only POST requests with file uploads are allowed'}, status=405)


