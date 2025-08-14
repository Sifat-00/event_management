from django.contrib.auth.models import User, Group
from django.db.models.signals  import post_save
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.dispatch import receiver
from django.conf import settings
from events.models import Profile

@receiver(post_save,sender=User) 
def assign_role(sender,instance,created, **kwargs) :
    if created :
        user_group, created = Group.objects.get_or_create(name = 'User')
        instance.groups.add(user_group)
        instance.save()

@receiver(post_save, sender =User)
def send_activation_email(sender, instance, created, **kwargs) :
    if created :
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/events/activate/{instance.id}/{token}/"

        subject = "Activate Your Account"


        message = f'Hi {instance.username},\n\nPlease activate your account by clicking the link below: \n {activation_url}'


        recipent_list = [instance.email]


        try :
            send_mail(subject,message, settings.EMAIL_HOST_USER, recipent_list)

            
        except Exception as e :
            print(f"Failed to send email to {instance.email} : {str(e)} ")




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)