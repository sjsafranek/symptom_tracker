#!/bin/bash
set +x

rm credentials.ini
rm db.sqlite3
rm symptoms/migrations/00*.py
python3 manage.py makemigrations
python3 manage.py migrate

# create admin user
if [ ! -f "`pwd`/credentials.ini" ]; then
	echo "Creating admin user..."
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@monsters.com', 'dev')" | python3 manage.py shell
	echo "[credentials]
username: admin
password: dev" >> credentials.ini
	cat credentials.ini
fi



: "
python3 manage.py shell

from django.contrib.auth.models import User
from symptoms import models

testAgency = models.Agency(name='test')
testAgency.save()

me = User(username='stefan')
me.save()

testTherapist = models.Therapist(user=me)
testTherapist.save()
testTherapist.agencies.add(testAgency)
testTherapist.save()

testClient = models.Client(user=me)
testClient.save()
testClient.therapists.add(testTherapist)
testClient.save()

session = testTherapist.createSession(testClient)

symptom = session.createSymptom(name='gas',rank=8)

"
