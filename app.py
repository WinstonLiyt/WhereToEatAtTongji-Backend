from gensim.models import KeyedVectors
from flask import Flask, request, jsonify


file='/root/tencent-ailab-embedding-zh-d100-v0.2.0-s/tencent-ailab-embedding-zh-d100-v0.2.0-s.txt'

    #file='/Users/ruoxizang/desktop/SE/tencent-ailab-embedding-zh-d100-v0.2.0-s.t
model = KeyedVectors.load_word2vec_format(file, binary=False)



app = Flask(__name__)

@app.route('/model/', methods=['GET'])
def get_sim():
    # 获取 GET 请求参数
    name = request.args.get('name')
    try:
        sim=model.most_similar(name, topn=10)
    except KeyError:
        sim=[]
    #sim=['hello']
    # 构造返回的 JSON 数据
    data = {
        'sim': sim,
    }

    # 返回 JSON 格式的数据
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=False)
