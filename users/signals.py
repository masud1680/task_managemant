#signals import
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f'{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/'
        # print(activation_url)
        
        subject = 'Activate Your Account'
        message = f'Hi {instance.username}, \n\n Please activate your account by clicking the link below: \n {activation_url} \n\n Thank You!'
        recipient_list = [instance.email]
        # print(recipient_list)
        
        try:
            # print('test emailhotr user : ', settings.EMAIL_HOST_USER , settings.EMAIL_HOST_PASSWORD)
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f'Faield to send email to {instance.email} : {str(e)}')
        
        
@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name='user')
        instance.group.add(user_group)
        instance.save()       
        
        
        
        
