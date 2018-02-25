from django.db import models
import os.path
from PIL import Image
from io import BytesIO
import uuid
from django.core.files.base import ContentFile

THUMB_SIZE = (200, 200)
ALLOWED_EXTENSIONS = ("jpg", "jpeg", "gif", "png")

class PostManager(models.Manager):
    def new_thread(self, post_data, file_data):

        errors = []

        if "image" not in file_data:
            errors.append("You must upload an image to start a thread")
        elif file_data["image"].name.find(".") == -1:
            errors.append("Image must be '.jpg', 'jpeg', '.gif', or '.png'")
        elif file_data["image"].name.split(".")[-1].lower() not in ALLOWED_EXTENSIONS:
            errors.append("Image must be '.jpg', 'jpeg', '.gif', or '.png'")

        if len(post_data["subject"]) < 1:
            errors.append("You must include a subject to start a thread")
        elif len(post_data["subject"]) < 3:
            errors.append("Subject must be 3 characters or more")

        if len(errors) < 1:
            file_name = file_data["image"].name
            file_data["image"].name = "{}.{}".format(uuid.uuid4().hex, file_name.split(".")[-1])

            return Post.objects.create(
                subject=post_data["subject"],
                name="Anonymous" if len(post_data["name"]) == 0 else post_data["name"],
                email=post_data["email"],
                comment=post_data["comment"], 
                file_name=file_name,
                image=file_data["image"],
                is_thread=True,
                is_sage=False
            )
        else:
            return errors

    def new_reply(self, post_data, file_data, post_id):

        errors = []

        if "image" not in file_data and len(post_data["comment"]) < 1:
            errors.append("You must reply with an image or a comment")
        elif "image" not in file_data and len(post_data["comment"]) < 2:
            errors.append("Comment must be 2 characters or more")
        
        if "image" in file_data:
            if file_data["image"].name.find(".") == -1:
                errors.append("Image must be '.jpg', 'jpeg', '.gif', or '.png'")
            elif file_data["image"].name.split(".")[-1].lower() not in ALLOWED_EXTENSIONS:
                errors.append("Image must be '.jpg', 'jpeg', '.gif', or '.png'")
            else:
                file_name = file_data["image"].name
                file_data["image"].name = "{}.{}".format(uuid.uuid4().hex, file_name.split(".")[-1])

        if len(errors) < 1:
            post = Post.objects.create(
                name="Anonymous" if len(post_data["name"]) == 0 else post_data["name"],
                email=post_data["email"],
                comment=post_data["comment"],
                file_name=None if "image" not in file_data else file_name,
                image=None if "image" not in file_data else file_data["image"],
                is_thread=False,
                is_sage=post_data["email"].lower() == "sage"
            )
            thread = Post.objects.get(id=post_id)
            thread.replies.add(post)
            return post
        else:
            return errors


class Post(models.Model):
    subject = models.CharField(max_length=255, default=None, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    comment = models.TextField(max_length=1000)
    file_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    image = models.ImageField(upload_to="forums", default=None, blank=True, null=True)
    thumbnail = models.ImageField(upload_to="forums", default=None, blank=True, null=True)
    is_thread = models.BooleanField()
    is_sage = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    replies = models.ManyToManyField("self", blank=True, related_name="thread")

    objects = PostManager()

    def save(self, *args, **kwargs):

        if self.image != None:
            if not self.make_thumbnail():
                raise Exception('Could not create thumbnail - is the file type valid?')

        super(Post, self).save(*args, **kwargs)

    def make_thumbnail(self):

        image = Image.open(self.image)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_s' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True