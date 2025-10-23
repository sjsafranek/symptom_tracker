#!/bin/bash
#set +x
rm credentials.ini
rm db.sqlite3
rm symptoms/migrations/00*.py
python manage.py makemigrations
python manage.py migrate

# create admin user
if [ ! -f "`pwd`/credentials.ini" ]; then
	echo "Creating admin user..."
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@tracker.com', 'dev')" | python manage.py shell
	echo "[credentials]
username: admin
password: dev" >> credentials.ini
	cat credentials.ini
fi



: "
python manage.py shell


import random
import datetime
from django.contrib.auth.models import User
from symptoms import models





from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create a new group
group, created = Group.objects.get_or_create(name='Therapists')

# Get the content type for a specific model (e.g., 'myapp.MyModel')
# Replace 'myapp' and 'MyModel' with your actual app and model names
content_types = ContentType.objects.filter(app_label='symptoms')

# Get specific permissions for that model
for content_type in content_types: 
	# Add permissions to the group
	for permission in Permission.objects.filter(content_type=content_type):
		group.permissions.add(permission)

group.save()








user = User(username='test-therapist', first_name='test', last_name='therapist')
user.save()
therapist = models.Therapist(user=user)
therapist.save()


user = User(username='test-client', first_name='test', last_name='client')
user.save()
client = models.Client(user=user)
client.therapist = therapist
client.save()


symptomCategories = [ 
	SymptomCategory(name = 'scream'),
	SymptomCategory(name = 'shout'),
	SymptomCategory(name = 'freakout')
]
for symptomCategory in symptomCategories:
	symptomCategory.save()


for symptomCategory in symptomCategories:
	clientSymptom = ClientSymptom(
		client=client,
		description=symptomCategory.name+'!!',
		baseline_goodweek=7,
		baseline_badweek=10,
		baseline_usualweek=8
	)
	clientSymptom.save()
	clientSymptom.symptom_categories.add(symptomCategory)
	clientSymptom.save()
	clientSymptoms.append(clientSymptom)
clientSymptoms = [item for item in client.clientsymptom_set.all()]


note = ClientNote(client=client, therapist=therapist, note='Very strange dude')
note.save()
note = ClientNote(client=client, therapist=therapist, note='Needs to chill out')
note.save()


session = ClientSession(client=client, therapist=therapist, date=datetime.datetime.now())
session.save()


for clientSymptom in clientSymptoms:
	score = ClientSessionSymptomScore(session=session, symptom=clientSymptom, score=random.randint(6,10))
	score.save()










symptom_categories [
	SymptomCategory(name = 'scream'),
	SymptomCategory(name = 'shout'),
	SymptomCategory(name = 'freakout')
]
for symptomCategory in symptomCategories:
	symptomCategory.save()




"
