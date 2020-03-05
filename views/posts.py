from flask import jsonify, request
from mongoengine import ValidationError

from app import app
from model import User, Post, Cover, Category
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
    except ValidationError:
        return jsonify({"error": "Post not found"}), 404

    return jsonify(post.to_public_json())