import datetime
import hashlib

from  mongoengine import *

connect("yesterday_toutiao")

class CustomQuerySet(QuerySet):
    def to_public_jsons(self):
        result = []
        try:
            for obj in self:
                tmp = obj.to_public_json()
                result.append(tmp)
        except:
            print('error')

        return result

class User(Document):
    email = EmailField(required=True, unique=True)
    username = StringField(max_length=50, required=True, unique=True)
    password = StringField(required=True)
    created = DateTimeField(required=True, default=datetime.datetime.now())
    head_img = StringField(required=True)
    gender = IntField(required=True)
    user_followed = ListField(ReferenceField("User"))#关注别人

    # meta = {'queryset_class': CustomQuerySet}

    def to_public_json(self):
        data = {
            "id": str(self.id),
            "username": self.username,
            "head_img": self.head_img,
            "gender": self.gender,
            "created": self.created.strftime("%Y-%m-%d"),
        }

        return data

class Comment(EmbeddedDocument):
    content = StringField(max_length=5000)
    user = ReferenceField(User)
    created = DateTimeField(required=True, default=datetime.datetime.now())

class Category(Document):
    name = StringField(max_length=120, required=True)

    meta = {'queryset_class': CustomQuerySet}

    def to_public_json(self):
        data = {
            "id": str(self.id),
            "name": self.name,
        }

        return data

class Cover(Document):
    url = StringField(max_length=300, required=True)

    # meta = {'queryset_class': CustomQuerySet}

    def to_public_json(self):
        data = {
            "message": "文件上传成功",
            "data": {
                "id": str(self.id),
                "url": '/file/' + self.url,
            },
        }

        return data

class Post(Document):
    title = StringField(max_length=120, required=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    user_collect = ListField(ReferenceField(User, reverse_delete_rule=CASCADE))
    user_agree = ListField(ReferenceField(User, reverse_delete_rule=CASCADE))
    content = StringField(max_length=5000)
    comments = ListField(EmbeddedDocumentField(Comment))
    created = DateTimeField(required=True, default=datetime.datetime.now())
    covers = ListField(ReferenceField(Cover, reverse_delete_rule=CASCADE))
    categories = ListField(ReferenceField(Category, reverse_delete_rule=CASCADE))
    type = IntField(required=True)
    has_star = BooleanField(required=False)
    has_like = BooleanField(required=False)
    has_follow = BooleanField(required=False)

    meta = {'queryset_class': CustomQuerySet}

    def to_public_json(self):
        data = {
            "id": str(self.id),
            "title": self.title,
            "has_star": self.has_star,
            "has_like": self.has_like,
            "has_follow": self.has_follow,
            "like_length": len(self.user_agree),

            "content": self.content,
            "user": {
                "id": str(self.user.id),
                "nickname": self.user.username
            },
            "comment_length": len(self.comments),

            "created": self.created.strftime("%Y-%m-%d %H:%M:%S"),
            "type": self.type,
            "categories": [{
                "id": str(category.id),
                "name": category.name
            } for category in self.categories],
            "cover": [{
                "id": str(cover.id),
                "url": '/file/' + cover.url
            } for cover in self.covers],
        }

        return data





