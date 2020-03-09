from flask import jsonify, request
from werkzeug.security import generate_password_hash

from app import app
from model import Post, User
from views.auth import login_required


@app.route("/api/user_follow/<string:uid>", methods=["POST"])
@login_required
def user_follow(userid, uid):

    resp = {}

    if userid == uid:
        resp['message'] = '不能关注自己'
        return jsonify(resp)

    try:
        userFollowed = User.objects(pk=uid).first()
        userFollower = User.objects(pk=userid).first()

        user_followedLst = userFollower.user_followed

        usernameLst = [u.username for u in user_followedLst]
        if userFollowed.username in usernameLst:
            userIndex = usernameLst.index(userFollowed.username)
            user_followedLst.pop(userIndex)
            userFollower.save()
            resp['message'] = '取消关注成功'
        else:
            user_followedLst.append(userFollowed)
            userFollower.save()
            resp['message'] = '关注成功'
    except:
        pass

    return jsonify(resp)

@app.route("/api/user_comments")
@login_required
def user_comments(userid):
    try:
        user = User.objects(pk=userid).first()

        commentLst = []
        posts = Post.objects(comments__user=user)
        for post in posts:
            comments = post.comments
            for comment in comments:
                if comment.user.id == user.id:
                    obj = {
                            "content": comment.content,
                            "created": comment.created.strftime("%Y-%m-%d %H:%M:%S"),
                            "user": {
                                "id": str(comment.user.id),
                                "nickname": comment.user.username
                            }
                    }

                    commentLst.append(obj)
    except:
        pass

    return jsonify(commentLst)


@app.route("/api/user_star")
@login_required
def user_star(userid):
    try:
        user = User.objects(pk=userid).first()
        posts = Post.objects(user_collect=user)

        return jsonify(posts.to_public_jsons())
    except:
        pass

    return jsonify([])


@app.route("/api/user_follows")
@login_required
def user_follows(userid):
    try:
        user = User.objects(pk=userid).first()

        userLst = []
        for user in user.user_followed:
            userLst.append(user.to_public_json())

        return jsonify(userLst)
    except:
        pass

    return jsonify([])


@app.route("/api/me")
@login_required
def get_user_info(userid):
    try:
        user = User.objects(pk=userid).first()
        return jsonify(user.to_public_json())
    except:
        pass

    return jsonify({})


@app.route("/api/update_user",methods=['POST'])
@login_required
def update_user(userid):
    try:
        user = User.objects(pk=userid).first()

        if request.json.get('head_img'):
            user.head_img = request.json.get('head_img')
        if request.json.get('username'):
            user.username = request.json.get('username')
        if request.json.get('password'):
            user.password = generate_password_hash(request.json.get('password'))
        if request.json.get('gender') != None:
            user.gender = request.json.get('gender')

        user.save()
        return jsonify(user.to_public_json())
    except:
        pass

    return jsonify({})
