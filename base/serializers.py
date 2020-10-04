from rest_framework import serializers

from .models import Project2
from .models import VideoInfo2

class Project2Serializer(serializers.ModelSerializer):
	class Meta:
		model = Project2
		fields = '__all__'
		

class VideoInfo2Serializer(serializers.ModelSerializer):
	class Meta:
		model = VideoInfo2
		fields = '__all__'


	