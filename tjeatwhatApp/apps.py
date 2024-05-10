from django.apps import AppConfig
from gensim.models import KeyedVectors

class TjeatwhatappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tjeatwhatApp'
    file='/root/tencent-ailab-embedding-zh-d100-v0.2.0-s/tencent-ailab-embedding-zh-d100-v0.2.0-s.txt'

    #file='/Users/ruoxizang/desktop/SE/tencent-ailab-embedding-zh-d100-v0.2.0-s.txt'
    model = KeyedVectors.load_word2vec_format(file, binary=False)

    def ready(self):
        import tjeatwhatApp.signals  # 导入信号接收器
        


        





    
