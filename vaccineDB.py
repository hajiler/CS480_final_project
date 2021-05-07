import mysql.connector


class DBManager:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Cps43637142",
            database="ui_health_schema"
        )

    def isUser(self, user, psswrd, role):
        query = "SELECT isUSER(\'{0}\',\'{1}\',\'{2}\');".format(user, psswrd, role)
        print(query)
        cursor = self.db.cursor()
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result == 1

    def insertIntoNurses(self, nurse_info):
        cursor = self.db.cursor()

        query = "INSERT INTO USERS(username, password, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (nurse_info['username'], nurse_info['password'], "Nurse"))

        columns = "(nurse_id, ssn, fname, lname, minitial, username, address, phone, age, gender)"
        value_place_holder = "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        query = "INSERT INTO NURSE" + columns + value_place_holder

        values = (nurse_info['id'], nurse_info['ssn'], nurse_info['fname'],
                  nurse_info['lname'], nurse_info['minitial'], nurse_info['username'],
                  nurse_info['address'], nurse_info['phone'], nurse_info['age'], nurse_info['gender']
                  )
        cursor.execute(query, values)
        #
        # query = "INSERT INTO NURSE_SCHEDULE(nurse_id, slot) VALUES (%s, %s)"
        # values = (nurse_info['id'], "2008-10-29 14:56:59")
        # cursor.execute(query, values)
        self.db.commit()

    def updateNurse(self, update_statements, id):
        statement = 'SET ' + ', '.join(update_statements)
        condition = '='.join(['WHERE nurse_id', id])
        query = ' '.join(['UPDATE NURSE', statement, condition])
        print(query)
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()

    def remove_nurse(self, id):
        condition = '='.join(['WHERE nurse_id', id])
        query = ' '.join(['DELETE FROM NURSE', condition])
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()

    def insert_into_vaccines(self, vaccine_info):
        cursor = self.db.cursor()

        columns = "(name, company, doses, available, onhold)"
        value_place_holder = "VALUES (%s, %s, %s, %s, %s)"
        query = "INSERT INTO VACCINES" + columns + value_place_holder

        values = (vaccine_info['name'], vaccine_info['company'], vaccine_info['doses'],
                  vaccine_info['available'], vaccine_info['onhold']
                  )
        cursor.execute(query, values)
        self.db.commit()

    def retrieve_vaccine(self, vaccine_name):
        condition = '='.join(['WHERE name', vaccine_name])
        query = ' '.join(['SELECT * FROM VACCINES', condition])
        cursor = self.db.cursor()
        cursor.execute(query)
        values = list(cursor.fetchone())
        print(values)
        return values


    def update_vaccine(self, update_statements, id):
        statement = 'SET ' + ', '.join(update_statements)
        condition = '='.join(['WHERE name', id])
        query = ' '.join(['UPDATE VACCINES', statement, condition])
        print(query)
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()

    def remove_vaccine(self, id):
        condition = '='.join(['WHERE name', id])
        query = ' '.join(['DELETE FROM VACCINES', condition])
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()

    def retrieve_nurse(self, id):
        condition = '='.join(['WHERE nurse_id', id])
        query = ' '.join(['SELECT * FROM NURSE', condition])
        cursor = self.db.cursor()
        cursor.execute(query)
        values = list(cursor.fetchone())
        print(values)
        return values

    def retrieve_nurse_self(self, username):
        id_query = "SELECT nurse_id FROM NURSE WHERE username={0}".format(username)
        print(id_query)
        cursor = self.db.cursor()
        cursor.execute(id_query)
        id = list(cursor.fetchone())[0]
        print(id)

        condition = '='.join(['WHERE nurse_id', id])
        query = ' '.join(['SELECT * FROM NURSE', condition])
        cursor = self.db.cursor()
        cursor.execute(query)
        info = list(cursor.fetchone())
        print(info)

        slot_query = 'SELECT slot FROM NURSE_SCHEDULE WHERE nurse_id={0}'.format(id);
        print(slot_query)
        cursor.execute(slot_query)
        slots = [list(row) for row in cursor.fetchall()]
        print(slots)
        return info, slots

    def retrieve_patient(self, ssn):
        condition = '='.join(['WHERE ssn', ssn])
        query = ' '.join(['SELECT * FROM PATIENTS', condition])
        print(query)
        cursor = self.db.cursor()
        cursor.execute(query)
        values = list(cursor.fetchone())
        print(values)

        slot_query = 'SELECT slot FROM APPOINTMENTS WHERE patient_ssn={0}'.format(ssn);
        print(slot_query)
        cursor.execute(slot_query)
        slots = [list(row) for row in cursor.fetchall()]
        print(slots)

        num_query = 'SELECT dose FROM RECORDS WHERE patient_ssn={0} ORDER BY dose DESC'.format(ssn);
        cursor.execute(num_query)
        try:
            values.append(list(cursor.fetchone())[0])
        except TypeError:
            values.append('0')
        return values, slots

    def retrieve_patient_self(self, username):
        snn_query = "SELECT ssn FROM PATIENTS WHERE username=\'{0}\'".format(username)
        print(snn_query)
        cursor = self.db.cursor()
        cursor.execute(snn_query)
        ssn = "\'{0}\'".format(list(cursor.fetchone())[0])
        print(ssn)

        condition = '='.join(['WHERE ssn', ssn])
        query = ' '.join(['SELECT * FROM PATIENTS', condition])
        print(query)
        cursor = self.db.cursor()
        cursor.execute(query)
        values = list(cursor.fetchone())
        print(values)

        slot_query = 'SELECT slot FROM APPOINTMENTS WHERE patient_ssn={0}'.format(ssn);
        print(slot_query)
        cursor.execute(slot_query)
        slots = [list(row) for row in cursor.fetchall()]
        print(slots)

        num_query = 'SELECT dose FROM RECORDS WHERE patient_ssn={0} ORDER BY dose DESC'.format(ssn);
        cursor.execute(num_query)
        try:
            values.append(list(cursor.fetchone())[0])
        except TypeError:
            values.append('0')
        return values, slots

    def updateNurse_by_username(self, update_statements, username):
        statement = 'SET ' + ', '.join(update_statements)
        condition = '='.join(['WHERE username', username])
        query = ' '.join(['UPDATE NURSE', statement, condition])
        print(query)
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()

    def retrieve_nurse_slots(self):
        query = 'SELECT * FROM nurse_slots'
        cursor = self.db.cursor()
        cursor.execute(query)
        values = [list(row) for row in cursor.fetchall()]
        print(values)
        return values

    def insert_nurse_slot(self, slot, username):
        id_query = "SELECT nurse_id FROM NURSE WHERE username={0}".format(username)
        print(id_query)
        cursor = self.db.cursor()
        cursor.execute(id_query)
        id = list(cursor.fetchone())[0]
        print(id)

        insert_query = 'INSERT INTO NURSE_SCHEDULE (nurse_id, slot) VALUES (%s, %s)'
        print(insert_query)
        cursor.execute(insert_query, (id, slot))
        self.db.commit()

    def view_nurse_slots(self, username):
        id_query = "SELECT nurse_id FROM NURSE WHERE username={0}".format(username)
        print(id_query)
        cursor = self.db.cursor()
        cursor.execute(id_query)
        id = list(cursor.fetchone())[0]
        print(id)

        slot_query = 'SELECT slot FROM NURSE_SCHEDULE WHERE nurse_id={0}'.format(id);
        print(slot_query)
        cursor.execute(slot_query)
        values = [list(row) for row in cursor.fetchall()]
        print(values)
        return values

    def remove_nurse_slot(self, slot, username):
        id_query = "SELECT nurse_id FROM NURSE WHERE username={0}".format(username)
        cursor = self.db.cursor()
        cursor.execute(id_query)
        id = list(cursor.fetchone())[0]

        remove_query = 'DELETE FROM NURSE_SCHEDULE WHERE slot={0} AND nurse_id={1}'.format(slot, id)
        print(remove_query)
        cursor.execute(remove_query)
        self.db.commit()

    def insert_into_records(self, record_info):
        cursor = self.db.cursor()

        columns = "(patient_ssn, nurse_id, vaccine, dose, slot)"
        value_place_holder = "VALUES (%s, %s, %s, %s, %s)"
        query = "INSERT INTO RECORDS" + columns + value_place_holder

        print(query)
        values = (record_info['patient_ssn'], record_info['nurse_id'], record_info['vaccine'],
                  record_info['dose'], record_info['slot']
                  )
        cursor.execute(query, values)
        self.db.commit()

    def insert_into_patients(self, patient_info):
        cursor = self.db.cursor()

        query = "INSERT INTO USERS(username, password, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (patient_info['username'], patient_info['password'], "Patient"))

        columns = "(username, ssn, fname, lname, minitial, address, race, age, gender, phone, occupation, medical_hist)"
        value_place_holder = "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        query = "INSERT INTO PATIENTS" + columns + value_place_holder

        values = (patient_info['username'], patient_info['ssn'], patient_info['fname'],
                  patient_info['lname'], patient_info['minitial'], patient_info['address'],
                  patient_info['race'], patient_info['age'], patient_info['gender'],
                  patient_info['phone'], patient_info['occupation'], patient_info['medical_hist']
                  )
        cursor.execute(query, values)
        self.db.commit()

    def update_patient_by_username(self, update_statements, username):
        statement = 'SET ' + ', '.join(update_statements)
        condition = '='.join(['WHERE username', username])
        query = ' '.join(['UPDATE PATIENTS', statement, condition])
        print(query)
        cursor = self.db.cursor()
        cursor.execute(query)
        self.db.commit()

    def retrieve_open_slots(self):
        query = 'SELECT * FROM patient_slots'
        print(query)
        cursor = self.db.cursor()
        cursor.execute(query)
        values = [list(row) for row in cursor.fetchall()]
        print(values)
        return values

    def insert_patient_slot(self, slot, username):
        snn_query = "SELECT ssn FROM PATIENTS WHERE username={0}".format(username)
        print(snn_query)
        cursor = self.db.cursor()
        cursor.execute(snn_query)
        ssn = list(cursor.fetchone())[0]
        print(ssn)

        vac_query = "SELECT name FROM VACCINES ORDER BY available DESC"
        cursor = self.db.cursor()
        cursor.execute(vac_query)
        vaccine = list(cursor.fetchone())[0]
        cursor.fetchall()

        insert_query = 'INSERT INTO APPOINTMENTS (patient_ssn, slot, vaccine) VALUES (%s, %s, %s)'
        print(insert_query)
        cursor.execute(insert_query, (ssn, slot, vaccine))

        update_query = 'UPDATE VACCINES SET onhold = onhold + 1, available = available - 1 WHERE name=\'{0}\';'.format(
            vaccine)
        cursor.execute(update_query)
        self.db.commit()

    def remove_patient_slot(self, slot, username):
        snn_query = "SELECT ssn FROM PATIENTS WHERE username={0}".format(username)
        print(snn_query)
        cursor = self.db.cursor()
        cursor.execute(snn_query)
        ssn = list(cursor.fetchone())[0]
        print(ssn)

        vac_query = 'SELECT vaccine FROM APPOINTMENTS WHERE patient_ssn={0}'.format(ssn)
        cursor = self.db.cursor()
        cursor.execute(vac_query)
        vaccine = list(cursor.fetchone())[0]
        cursor.fetchall()

        update_query = 'UPDATE VACCINES SET onhold = onhold + 1, available = available - 1 WHERE name=\'{0}\';'.format(
            vaccine)
        cursor.execute(update_query)

        remove_query = 'DELETE FROM APPOINTMENTS WHERE slot={0} AND patient_ssn={1}'.format(slot, ssn)
        print(remove_query)
        cursor.execute(remove_query)
        self.db.commit()

    def view_patient_slots(self, username):
        snn_query = "SELECT ssn FROM PATIENTS WHERE username={0}".format(username)
        print(snn_query)
        cursor = self.db.cursor()
        cursor.execute(snn_query)
        ssn = list(cursor.fetchone())[0]
        print(ssn)

        slot_query = 'SELECT slot FROM APPOINTMENTS WHERE patient_ssn={0}'.format(ssn);
        print(slot_query)
        cursor.execute(slot_query)
        values = [list(row) for row in cursor.fetchall()]
        print(values)
        return values
