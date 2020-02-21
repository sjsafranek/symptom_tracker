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
from symptoms import utils


agency = models.Agency(name='test')
agency.save()

me = User(username='stefan')
me.save()

therapist = models.Therapist(user=me)
therapist.save()
therapist.addAgency(agency)

client = models.Client(user=me)
client.save()
client.therapist = therapist
client.save()





therapist.addSymptom(client, 'barfing')
therapist.addSymptom(client, 'diaphoretic')
therapist.addSymptom(client, 'chest_pain')
therapist.addSymptom(client, 'nausea')


therapist.createSession(client)



client.recordSymptom('barfing', 8)
client.recordSymptom('diaphoretic', 4)
client.recordSymptom('chest_pain', 2)
client.recordSymptom('nausea', 7)



client.getSymptoms()
client.getHistory()




client.recordSymptom('barfing', 4)
client.recordSymptom('diaphoretic', 1)
client.recordSymptom('chest_pain', 3)
client.recordSymptom('nausea', 4)





from symptoms import utils
me = utils.getUserByUsername('stefan')
me.therapist.createSession(me.client)



"
