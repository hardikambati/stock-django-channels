from django.db import models


class Room(models.Model):

    room_name = models.CharField(max_length=1000)

    def __str__(self):

        return self.room_name


class ChannelName(models.Model):

    room_name = models.ForeignKey(to=Room, on_delete=models.CASCADE)

    channel_name = models.CharField(max_length=1000)

    def __str__(self):
        
        return self.channel_name