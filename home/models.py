from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
 
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key = True,default=uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

class Blog(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    blog_text = models.TextField()
    main_image = models.ImageField(upload_to='blog_images')

    def __str__(self):
        return self.title