from django.db import models
from djangogram.users import models as user_model
# Create your models here.

class TimeStamedModel(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    
  


#사진 저장 하는 모델
class Post(TimeStamedModel):#상속 시킴
    author = models.ForeignKey(user_model.User, null=True, on_delete=models.CASCADE, related_name='post_author')
    image =models.ImageField(blank=False) #빈공간을 허용하지 않아서 사진과 caption 모두 받게 만들어줌
    caption = models.TextField(blank=False)
    image_likes = models.ManyToManyField(user_model.User, blank=True,related_name='post_image_likes')

    def __str__(self):
        return f"{self.author}: {self.caption}"


#댓글 관리 커맨트 데이터 모델
class Comment(TimeStamedModel):
    author = models.ForeignKey(user_model.User, null=True, on_delete=models.CASCADE, related_name='comment_author')
    posts= models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='comment_post') 
    contents = models.TextField(blank=True) 

    def __str__(self):
        return f"{self.author}: {self.contents}"