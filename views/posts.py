from flask import jsonify, request
from mongoengine import ValidationError

from app import app
from model import User, Post, Cover, Category, Comment
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


@app.route('/api/update_post/<pid>',methods=['POST'])
@login_required
def posts_update(userid,pid):
    print(userid)

    try:
        post = Post.objects(pk=pid).first()
        if not post:
            raise ValidationError

        coverLst = post.covers
        coverLst.clear()

        for cover_obj in request.json.get('cover'):
            cover = Cover.objects(pk=cover_obj['uid']).first()
            coverLst.append(cover)

        post.categories.clear()
        for category_id in request.json.get('categories'):
            cate = Category.objects(pk=category_id).first()
            post.categories.append(cate)

        post.title = request.json.get('title')
        post.content = request.json.get('content')
        post.type = request.json.get('type')

        post.save()

    except:
        return jsonify({'message':'post not found'})

    return jsonify(post.to_public_json())


@app.route('/api/get_cate_posts')
@login_required
def get_cate_posts(userid):
    pageIndex = int(request.args.get('pageIndex'))
    pageSize = int(request.args.get('pageSize'))
    cateID = request.args.get('category')



    posts = Post.objects(categories=cateID).order_by("-created")
    paged_posts = posts.skip(pageSize*(pageIndex-1)).limit(pageSize)

    post_lst = paged_posts.to_public_jsons()

    return jsonify({'data':post_lst,'total': posts.count()})

@app.route('/api/get_posts')
@login_required
def get_posts(userid):
    pageIndex = int(request.args.get('pageIndex'))
    pageSize = int(request.args.get('pageSize'))

    try:
        userobj = User.objects(id=userid).first()
    except:
        return jsonify({'message':'user not found'})

    posts = Post.objects(user=userobj).order_by("-created")
    paged_posts = posts.skip(pageSize*(pageIndex-1)).limit(pageSize)

    # post_lst = []
    # for obj in paged_posts:
    #     tmp = obj.to_public_json()
    #     post_lst.append(tmp)

    post_lst = paged_posts.to_public_jsons()

    return jsonify({'data':post_lst,'total': posts.count()})

@app.route("/api/posts/id/<string:id>", methods=["DELETE"])
@login_required
def posts_delete(userid, id):
    try:
        post = Post.objects(pk=id).first()

        # If post has alreay been deleted
        if not post:
            raise ValidationError
    except ValidationError:
        return jsonify({"error": "Post not found"}), 404

    user = User.objects(id=userid).first()

    # Check whether action was called by creator of the post
    if user.username != post.user.username:
        return jsonify({"error": "You are not the creator of the post"}), 401

    post_info = post.to_public_json()

    post.delete()

    return jsonify(post_info)

@app.route("/api/post/<string:id>")
@login_required
def posts_detail(userid,id):
    try:
        post = Post.objects(pk=id).first()

        # If post has alreay been deleted
        if not post:
            raise ValidationError

        user = User.objects(pk=userid).first()

        user_collect = post.user_collect
        usernameLst = [u.username for u in user_collect]
        if user.username in usernameLst:
            post.has_star = True
        else:
            post.has_star = False

        user_agree = post.user_agree
        usernameLst = [u.username for u in user_agree]
        if user.username in usernameLst:
            post.has_like = True
        else:
            post.has_like = False

        if post.user in user.user_followed:
            post.has_follow = True
        else:
            post.has_follow = False

    except ValidationError:
        return jsonify({"error": "Post not found"}), 404

    return jsonify(post.to_public_json())

@app.route("/api/get_comments/<string:id>", methods=["GET"])
@login_required
def get_comments(userid,id):
    try:
        post = Post.objects(pk=id).first()

    except ValidationError:
        return jsonify({"error": "Post not found"}), 404

    if not request.args.get('pageSize'):
        pageSize = len(post.comments)
    else:
        pageSize = int(request.args.get('pageSize'))

    commentLst = []
    for comment in post.comments[::-1]:
        commentLst.append({
            "content": comment.content,
            "created": comment.created.strftime("%Y-%m-%d %H:%M:%S"),
            "user": {
                "id": str(comment.user.id),
                "nickname": comment.user.username
            }
        })

        pageSize -= 1
        if pageSize == 0:
            break

    return jsonify(commentLst)

@app.route("/api/create_comment/<string:id>", methods=["POST"])
@login_required
def posts_create_comment(userid, id):
    if not request.json.get('content'):
        return jsonify({"error": "No content specified"}), 409
    content = request.json.get('content')

    try:
        post = Post.objects(pk=id).first()
    except ValidationError:
        return jsonify({"error": "Post not found"}), 404

    user = User.objects(id=userid).first()
    comments = post.comments
    comments.append(Comment(user=user, content=content))
    post.save()

    return jsonify({'message':'添加评论成功'})


@app.route("/api/post_star/<string:pid>", methods=["POST"])
@login_required
def post_star(userid, pid):
    resp = {}
    try:
        post = Post.objects(pk=pid).first()
        user = User.objects(pk=userid).first()
        user_collect = post.user_collect
        usernameLst = [u.username for u in user_collect]
        if user.username in usernameLst:
            userIndex = usernameLst.index(user.username)
            user_collect.pop(userIndex)
            post.save()
            resp['message'] = '取消收藏成功'
        else:
            user_collect.append(user)
            post.save()
            resp['message'] = '收藏成功'
    except:
        pass

    return jsonify(resp)

@app.route("/api/post_like/<string:pid>", methods=["POST"])
@login_required
def post_like(userid, pid):
    resp = {}
    try:
        post = Post.objects(pk=pid).first()
        user = User.objects(pk=userid).first()
        user_agree = post.user_agree
        usernameLst = [u.username for u in user_agree]
        if user.username in usernameLst:
            userIndex = usernameLst.index(user.username)
            user_agree.pop(userIndex)
            post.save()
            resp['message'] = '取消点赞成功'
        else:
            user_agree.append(user)
            post.save()
            resp['message'] = '点赞成功'
    except:
        pass

    return jsonify(resp)


# 后台请求
@app.route("/api/post_search", methods=["GET"])
@login_required
def post_search(userid):
    keyword = request.args.get("keyword")
    print(keyword.strip())
    from mongoengine.queryset.visitor import Q
    posts = Post.objects(Q(content__icontains=keyword.strip())|Q(title__icontains=keyword.strip()))

    return jsonify(posts.to_public_jsons())