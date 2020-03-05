from flask import jsonify

from app import app
from model import Category
from views.auth import login_required


@app.route('/api/category')
@login_required
def get_all_category(userid):
    print(userid)
    categories = Category.objects()
    print(type(categories))

    # cate_lst = []
    # for obj in categories:
    #     tmp = obj.to_public_json()
    #     cate_lst.append(tmp)

    return jsonify(categories.to_public_jsons())
