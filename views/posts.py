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
