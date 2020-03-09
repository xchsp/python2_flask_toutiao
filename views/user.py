from flask import jsonify

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