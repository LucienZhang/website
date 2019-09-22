# -*- coding: utf-8 -*-
# @Author: Lucien Zhang
# @Date:   2019-09-19 17:53:51
# @Last Modified by:   Lucien Zhang
# @Last Modified time: 2019-09-22 19:02:24
from flask import Blueprint, render_template, request

from app.ml import predict


ml_api = Blueprint('ml_api', __name__)


@ml_api.route('/')
def home():
    return render_template("ml.html")


@ml_api.route('/mnist', methods=['GET', 'POST'])
def mnist():
    if request.method == 'POST':
        predictImg = request.files['predictImg']
        # filename = str(int(time.mktime(time.localtime()))) + '.png'
        # imgurl = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # predictImg.save(imgurl)
        result, prob = predict.mnist_predict(predictImg)
        return str(result)
    else:
        return render_template("mnist.html")
