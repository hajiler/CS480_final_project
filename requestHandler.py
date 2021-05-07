from vaccineDB import DBManager
from flask import request, jsonify
import datetime


# Return index.html for bad log info, returns appropriate filename for good log info
def handle_login_attempt(req):
    username = req.form['username']
    password = req.form['password']
    role = req.form['role']
    db = DBManager()
    logged_in = db.isUser(username, password, role)
    print(logged_in, role)
    if not logged_in:
        return 'False', 'index.html', role, username
    elif role == 'Administrator':
        return 'True', 'admin.html', role, username
    elif role == 'Nurse':
        return 'True', 'nurse.html', role, username
    elif role == 'Patient':
        return 'True', 'patient.html', role, username


# Find, read, and return appropriate html form as requested
def handle_form_request(req):
    role = req.args['type']
    kind = req.args['kind']
    file_name = None
    if role == 'nurse':
        if kind == 'Register':
            file_name = './forms/nurse_registration.html'
    print(role, kind, file_name)
    with open(file_name) as file:
        form = file.read()
    print(form)
    return form


def register_nurse(req):
    registration_info = {
        'username': req.form['inputUsername'],
        'password': req.form['inputPassword'],
        'fname': req.form['inputFName'],
        'lname': req.form['inputLName'],
        'minitial': req.form['inputMI'],
        'id': req.form['inputID'],
        'ssn': req.form['inputSSN'],
        'address': req.form['inputAddress'],
        'phone': req.form['inputPhone'],
        'age': req.form['inputAge'],
        'gender': req.form['inputGender']
    }
    print(list(registration_info.items()))
    db = DBManager()
    db.insertIntoNurses(registration_info)


def update_nurse(req):
    updates = []
    print(list(req.form))
    if 'inputUpdateFName' in list(req.form):
        updates.append('='.join(['fname', '\'{0}\''.format(req.form['inputFName'])]))
    if 'inputUpdateLName' in list(req.form):
        updates.append('='.join(['lname', '\'{0}\''.format(req.form['inputLName'])]))
    if 'inputUpdateMI' in list(req.form):
        updates.append('='.join(['minitial', '\'{0}\''.format(req.form['inputMI'])]))
    if 'inputUpdateSSN' in list(req.form):
        updates.append('='.join(['ssn', '\'{0}\''.format(req.form['inputSSN'])]))
    if 'inputUpdateAge' in list(req.form):
        updates.append('='.join(['age', '\'{0}\''.format(req.form['inputAge'])]))
    if 'inputUpdateGender' in list(req.form):
        updates.append('='.join(['gender', '\'{0}\''.format(req.form['inputGender'])]))
    print(updates)

    db = DBManager()
    db.updateNurse(updates, req.form['inputID'])


def remove_nurse(req):
    nurse_id = req.form['inputID']
    db = DBManager()
    db.remove_nurse(nurse_id)
    print(nurse_id)


def register_vaccine(req):
    vaccine_info = {
        'name': req.form['inputName'],
        'company': req.form['inputCompany'],
        'doses': req.form['inputDoses'],
        'available': int(req.form['inputAvailable']),
        'onhold': int(req.form['inputOnhold'])
    }
    print(list(vaccine_info.items()))
    db = DBManager()
    db.insert_into_vaccines(vaccine_info)


def update_vaccine(req):
    updates = []
    print(list(req.form))
    updates.append('='.join(['available', '\'{0}\''.format(req.form['inputAvailable'])]))

    print(updates)

    db = DBManager()
    db.update_vaccine(updates, '\'{0}\''.format(req.form['inputName']))


def get_vaccine(req):
    vaccine_name = '\'{0}\''.format(req.args['inputName'])
    db = DBManager()
    print(vaccine_name)

    results = db.retrieve_vaccine(vaccine_name)
    return jsonify(name=results[0],
                   Company=results[1],
                   doses=results[2],
                   available=results[3],
                   onhold=results[4]
                   )

def retrieve_nurse_self(req, username):
    db = DBManager()
    results, slots = db.retrieve_nurse_self('\'{0}\''.format(username))
    return jsonify(id=results[0],
                   ssn=results[1],
                   fname=results[2],
                   lname=results[3],
                   minital=results[4],
                   address=results[5],
                   age=results[6],
                   phonenumber=results[7],
                   gender=list(results[8])[0],
                   times=slots
                   )


def retrieve_nurse(req):
    nurse_id = req.args['inputID']
    db = DBManager()
    results = db.retrieve_nurse(nurse_id)
    return jsonify(id=results[0],
                   ssn=results[1],
                   fname=results[2],
                   lname=results[3],
                   minital=results[4],
                   address=results[5],
                   age=results[6],
                   phonenumber=results[7],
                   gender=list(results[8])[0]
                   )



def retrieve_patient(req):
    patient_ssn = '\'{0}\''.format(req.args['inputSSN'])
    db = DBManager()
    results, slots = db.retrieve_patient(patient_ssn)
    return jsonify(ssn="SSN :" + str(results[0]),
                   fname="First Name: " + str(results[1]),
                   lname="Last name: " + str(results[2]),
                   minital="Middle Name: " + str(results[3]),
                   address="Address: " + str(results[4]),
                   race="Race: " + str(list(results[5])[0]),
                   gender="Gender: " + str(list(results[6])[0]),
                   age="Age: " + str(results[7]),
                   phonenumber="Phonenumber: " + str(results[8]),
                   occupation="Occupation: " + str(results[9]),
                   mhistory="Medical History: " + str(results[10]),
                   doses="Doses recieved: " + str(results[12]),
                   times=slots
                   )


def retrieve_patient_me(req, username):
    db = DBManager()
    results, slots = db.retrieve_patient_self(username)
    return jsonify(ssn="SSN :" + str(results[0]),
                   fname="First Name: " + str(results[1]),
                   lname="Last name: " + str(results[2]),
                   minital="Middle Name: " + str(results[3]),
                   address="Address: " + str(results[4]),
                   race="Race: " + str(list(results[5])[0]),
                   gender="Gender: " + str(list(results[6])[0]),
                   age="Age: " + str(results[7]),
                   phonenumber="Phonenumber: " + str(results[8]),
                   occupation="Occupation: " + str(results[9]),
                   mhistory="Medical History: " + str(results[10]),
                   doses="Doses recieved: " + str(results[12]),
                   times=slots
                   )


def update_nurse_self(req, username):
    updates = []
    print(list(req.form))
    if 'inputUpdateAddress' in list(req.form):
        updates.append('='.join(['address', '\'{0}\''.format(req.form['inputAddress'])]))
    if 'inputUpdatePhone' in list(req.form):
        updates.append('='.join(['phone', '\'{0}\''.format(req.form['inputPhone'])]))
    print(updates)

    db = DBManager()
    db.updateNurse_by_username(updates, '\'{0}\''.format(username))


def retrieve_slots(req):
    results = None
    db = DBManager()
    if req.args['type'] == 'nurse':
        results = db.retrieve_nurse_slots()
    elif req.args['type'] == 'patient':
        results = db.retrieve_open_slots()
    time_slots = [value[0] for value in results]
    return jsonify(times=time_slots)


def convert_time(t):
    t = t.split(', ')
    day = t[0]
    rest = t[1]
    if day == 'Mon':
        return 'Monday, ' + rest
    if day == 'Tue':
        return 'Tuesday, ' + rest


def insert_slot(req, username):
    print('parsing request')
    d = convert_time(req.args['inputSlot'][:-4])
    f = "%A, %d %B %Y %H:%M:%S"
    time = datetime.datetime.strptime(d, f)
    slot = time.strftime('%Y-%m-%d %H:%M:%S')
    print(slot)
    db = DBManager()
    if request.args['type'] == 'nurse':
        db.insert_nurse_slot(slot, '\'{0}\''.format(username))
    elif request.args['type'] == 'patient':
        db.insert_patient_slot(slot, '\'{0}\''.format(username))


def retrieve_personal_slots(req, username):
    results = None
    db = DBManager()
    if request.args['type'] == 'nurse':
        results = db.view_nurse_slots('\'{0}\''.format(username))
    elif request.args['type'] == 'Patient':
        results = db.view_patient_slots('\'{0}\''.format(username))

    time_slots = [value[0] for value in results]
    return jsonify(times=time_slots)


def remove_personal_slots(req, username):
    print('parsing request')
    d = convert_time(req.args['inputSlot'][:-4])
    f = "%A, %d %B %Y %H:%M:%S"
    time = datetime.datetime.strptime(d, f)
    slot = time.strftime('%Y-%m-%d %H:%M:%S')
    print(slot)
    db = DBManager()
    if request.args['type'] == 'nurse':
        db.remove_nurse_slot('\'{0}\''.format(slot), '\'{0}\''.format(username))
    elif request.args['type'] == 'patient':
        db.remove_patient_slot('\'{0}\''.format(slot), '\'{0}\''.format(username))


def register_record(req):
    registration_info = {
        'patient_ssn': req.form['inputPatientSSN'],
        'nurse_id': req.form['inputNurseID'],
        'vaccine': req.form['inputVaccine'],
        'dose': req.form['inputDose'],
        'slot': req.form['inputSlot']
    }
    print(list(registration_info.items()))
    db = DBManager()
    db.insert_into_records(registration_info)


def register_patient(req):
    registration_info = {
        'username': req.form['inputUsername'],
        'password': req.form['inputPassword'],
        'ssn': req.form['inputSSN'],
        'fname': req.form['inputFName'],
        'lname': req.form['inputLName'],
        'minitial': req.form['inputMI'],
        'address': req.form['inputAddress'],
        'race': req.form['inputRace'],
        'gender': req.form['inputGender'],
        'phone': req.form['inputPhone'],
        'age': req.form['inputAge'],
        'occupation': req.form['inputJob'],
        'medical_hist': req.form['inputHistory'],
    }
    print(list(registration_info.items()))
    db = DBManager()
    db.insert_into_patients(registration_info)


def update_patient(req, username):
    updates = []
    print(list(req.form))
    if 'inputUpdateFName' in list(req.form):
        updates.append('='.join(['fname', '\'{0}\''.format(req.form['inputFName'])]))
    if 'inputUpdateLName' in list(req.form):
        updates.append('='.join(['lname', '\'{0}\''.format(req.form['inputLName'])]))
    if 'inputUpdateMI' in list(req.form):
        updates.append('='.join(['minitial', '\'{0}\''.format(req.form['inputMI'])]))
    if 'inputUpdateSSN' in list(req.form):
        updates.append('='.join(['ssn', '\'{0}\''.format(req.form['inputSSN'])]))
    if 'inputUpdateAge' in list(req.form):
        updates.append('='.join(['age', '\'{0}\''.format(req.form['inputAge'])]))
    if 'inputUpdateGender' in list(req.form):
        updates.append('='.join(['gender', '\'{0}\''.format(req.form['inputGender'])]))
    if 'inputUpdateRace' in list(req.form):
        updates.append('='.join(['race', '\'{0}\''.format(req.form['inputRace'])]))
    if 'inputUpdateJob' in list(req.form):
        updates.append('='.join(['occupation', '\'{0}\''.format(req.form['inputJob'])]))
    if 'inputUpdateHistory' in list(req.form):
        updates.append('='.join(['medical_hist', '\'{0}\''.format(req.form['inputHistory'])]))
    print(updates)

    db = DBManager()
    db.update_patient_by_username(updates, '\'{0}\''.format(username))

    # TODO: MAKE FIELDS REQUIRED
    # TODO: Front end for view FOR ADMIN
    # TODO: Patient functionality
    # TODO: Nurse Functionality
    # TODO: Fill up db with filler values
    # TODO: TEST
