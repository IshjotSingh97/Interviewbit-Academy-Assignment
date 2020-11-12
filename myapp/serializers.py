from rest_framework import serializers
from .models import *

class ParticipantSerializer(serializers.ModelSerialize):
	class meta:
		model = Participant
		field = ['useremail']
	