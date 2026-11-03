from django.db import models

class Topic(models.Model):
    userid = models. IntegerField ()
    title = models. CharField(max_length=100)
    # 摘要之后的长期记忆信息
    longmemory = models.TextField(null=True,blank=True)
    # 已经摘要了多少条记录
    summary_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    # 需要做逻辑删除
    is_deleted = models.SmallIntegerField(default=0)
    # 删除时间
    deleted = models.DateTimeField(null=True)

class ChatMessage(models.Model):
    ROLE_CHOICES = (
        ("user","用户"),
        ("assistant","助手"),
        ("system","系统"),
    )

    topicid=models.IntegerField()# 关联的主题
    userid= models.IntegerField(default=0)#关联的用户
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField( )
    image_url = models.URLField(max_length=255,blank=True,null=True)
    # 需要做逻辑删除
    is_deleted = models.SmallIntegerField(default=0)
    # 删除时间
    deleted = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)