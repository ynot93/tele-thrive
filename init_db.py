from app import db, User, Therapist, Appointment

db.drop_all()
db.create_all()

user1 = User(username='Tony', email='tony@test.com', password='password', role='client')
user2 = User(username='Nadia', email='nadia@test.com', password='password2', role='client')
user3 = User(username='Milly', email='milly@test.com', password='password3', role='admin')
user4 = User(username='Tim', email='tim@test.com', password='password4', role='client')

therapist1 = Therapist(therapist_name='Daktari', email='doc1@test.com', specialization='Depression', license_number=12345, password='password5')
therapist2 = Therapist(therapist_name='Doc', email='doc2@test.com', specialization='Anxiety', license_number=67890, password='password6')

appointment1 = Appointment(appointment_name='Tony\'s depression appointment', status='scheduled', user_id=1, therapist_id=1)

db.session.add_all([user1, user2, user3, user4])
db.session.add_all([therapist1, therapist2])
db.session.add_all([appointment1])

db.session.commit()