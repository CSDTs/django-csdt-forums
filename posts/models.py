from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from ttp import ttp

import misaka
import re
import time

from communities.models import Community
from accounts.models import User




class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts")
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    community = models.ForeignKey(Community, related_name="posts",
                                  null=True, blank=True)
    atted = models.ManyToManyField(settings.AUTH_USER_MODEL, through="AttedPost")

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        ending = '</p>'
        p = re.compile(r'@([^\s:]+)')
        base = ''
        from .curse import swear
        for row in self.message_html.split():
            for word in swear:
                found = row.find(word)
                while found is not -1:
                    print("curse word!")
                    row = row.replace(word,'****')

                    found = row.find(word)

            print("row: ",row)
            list_names = p.findall(row)
            if len(list_names) > 0:

                print("list_names: ",list_names[0])
                string_name = list_names[0].split('@')
                print(string_name)
                if len(string_name) > 1:
                    base += row + ' '
                    continue

                for person in string_name:
                    print("person: ", person)
                    # edge case: "hello@user1@user2"
                    # Strips "</p>"
                    if row.endswith(ending):
                        person=person[:-4]

                    #deploy: fix link address
                    replacement = re.sub(r'([A-Za-z]+)',r'<a href="http://127.0.0.1:8000/posts/by/\1/">@\1</a>', person)
                    if row.endswith(ending):
                        row = row[:-(len(person)+5)] + replacement + '</p>'
                        base += row
                    else:
                        if row.endswith(person):
                            row = row[:-(len(person)+1)] + replacement + ' '
                            base += row
                continue
            base += row + ' '



        print("base: ",base)
        self.message_html = base
        super().save(*args, **kwargs)
        p = ttp.Parser()
        result = p.parse(self.message_html)

        referenced = list(set(result.users))
        self_name = str(self.user)
        self_name = self_name[1:]
        for atted in referenced:
            print("atted:",atted)
            try:
                person = User.objects.get(username=atted)
                if atted == self_name:
                    continue
                try:
                    referenced.remove(atted)
                except ValueError:
                    continue
                AttedPost.objects.create(post=self, user_atted=person)
                from django.core.mail import send_mail
                send_mail(
                    "You have been messaged on CSDT's forums",
                    'You have been messaged on CSDT\'s forums (http://csdt.rpi.edu/msg). Here is the message from @{} on {}: "{}"'.format(self_name, self.created_at.strftime('%Y-%m-%d %H:%M:%S'), self.message),
                    'csdt@gmail.com',
                    [person.email],
                    fail_silently=False,
                )


            except User.DoesNotExist:
                pass




    def get_absolute_url(self):
        return reverse(
            "posts:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]


class AttedPost(models.Model):
    post = models.ForeignKey(Post, related_name="post_with_ats")
    user_atted = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="atted_user")