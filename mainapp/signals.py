from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    if created:
        # Присваиваем роль "Покупатель" новому пользователю
        buyer_group, created = Group.objects.get_or_create(name='Покупатель')
        instance.groups.add(buyer_group)
