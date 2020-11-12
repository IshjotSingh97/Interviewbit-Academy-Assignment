from rest_framework import serializers
from .models import *

class ParticipantSerializer(serializers.ModelSerialize):
    def validate_email(self, value):
    lower_email = value.lower()
    if Participant.objects.filter(email__iexact=lower_email).exists():
        raise serializers.ValidationError("Duplicate")
    return lower_email
	class Meta:
		model = Participant
		field = ['useremail']
	