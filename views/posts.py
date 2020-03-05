from flask import jsonify, request

from app import app
from model import User, Post
from views.auth import login_required


@app.route('/api/posts',methods=['POST'])
@login_required
def posts_create(userid):
    print(userid)
    user = User.objects(id=userid).first()

    coverLst = []
    for cover in request.json.get('cover'):
        coverLst.append(cover['id'])


    Post(
        title=request.json.get('title'),
        categories=request.json.get('categories'),
        content=request.json.get("content"),
        user=user,
        covers=coverLst,
        type=request.json.get('type'),
        comments=[],
        user_collect=[],
        user_agree=[],
    ).save()

    return jsonify({'message':'success'})

@app.route('/api/get_posts')
@login_required
def get_posts(userid):
    pageIndex = int(request.args.get('pageIndex'))
    pageSize = int(request.args.get('pageSize'))

    try:
        userobj = User.objects(id=userid).first()
    except:
        return jsonify({'message':'user not found'})

    posts = Post.objects(user=userobj).order_by("-created").skip(pageSize*(pageIndex-1)).limit(pageSize)

    post_lst = []
    for obj in posts:
        tmp = obj.to_public_json()
        post_lst.append(tmp)

    return jsonify({'data':post_lst})