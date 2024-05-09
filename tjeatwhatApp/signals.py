from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import RestImage,Dish

@receiver(post_delete, sender=RestImage)
def delete_restaurant_image(sender, instance, **kwargs):
    # 检查 Restaurant 对象是否有关联的图片字段
    if instance.image:
        # 删除图片文件
        instance.image.delete(False)  # False 表示不删除数据库记录


@receiver(post_delete, sender=Dish)
def delete_dish_image(sender, instance, **kwargs):
    # 检查 Dish对象是否有关联的图片字段
    if instance.image:
        # 删除图片文件
        instance.image.delete(False)  # False 表示不删除数据库记录
