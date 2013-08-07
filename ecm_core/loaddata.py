import csv
from mailer.models import Categories,Mail_address		


def csv_to_db(f,c_id):
	
	
	cat=Categories.objects.get(id=c_id)
	with open('/tmp/'+f.name,'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=",", quotechar='|')
		for line in spamreader:
			try:
				mail_address=Mail_address()
				mail_address.mid = line[1]
				mail_address.cid = cat
				mail_address.save()
			except:
				mail_address.cid = cat # some useless code



#from django.contrib.auth.models import User
#user = User.objects.get(id=user_id)
#staffprofile.user = user

