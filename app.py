from flask import Flask, render_template, request, redirect, render_template_string, session
import requestHandler as rq

app = Flask(__name__)
app.config['SECRET_KEY'] = "CHANGE BEFORE DEPLOYMENT!!!!!"

def user_default():
    session['main'] = 'index.html'
    session['login_status'] = 'False'


# INDEX PAGE : Login form for nurse/patient/admin
@app.route('/')
def index():
    if 'main' not in session.keys():
        user_default()
    elif session['login_status'] == 'True':
        return render_template(session['main'])

    return render_template('index.html')


# LOGIN REQUEST : Checks if login info is correct => sends user appropriate html page
@app.route('/login', methods=['POST'])
def login_attempt():
    status, template, role, username = rq.handle_login_attempt(request)
    session['main'] = template
    session['login_status'] = status
    session['role'] = role
    session['username'] = username
    return render_template(template)


@app.route('/logout', methods=['POST'])
def logout_attempt():
    user_default()
    return redirect('/')


# FORM REQUEST : Return appropriate form for a specific user requested action
@app.route('/register', methods=['POST'])
def add_from_form():
    if request.args['type'] == 'nurse':
        rq.register_nurse(request)
    if request.args['type'] == 'vaccine':
        rq.register_vaccine(request)
    if request.args['type'] == 'record':
        rq.register_record(request)
    if request.args['type'] == 'patient':
        rq.register_patient(request)
    return render_template(session['main'])


@app.route('/update', methods=['POST'])
def update_from_form():
    print('updating ')
    if request.args['type'] == 'nurse':
        if session['role'] == 'Administrator':
            rq.update_nurse(request)
        elif session['role'] == 'Nurse':
            rq.update_nurse_self(request, session['username'])
    if request.args['type'] == 'vaccine':
        rq.update_vaccine(request)
    if request.args['type'] == 'patient':
        rq.update_patient(request, session['username'])
    return render_template(session['main'])


@app.route('/remove', methods=['POST'])
def remove_from_primary_key():
    print('removing')
    if request.args['type'] == 'nurse':
        rq.remove_nurse(request)
    if request.args['type'] == 'vaccine':
        rq.remove_vaccine(request)
    return render_template(session['main'])


@app.route('/view', methods=['GET'])
def view_from_primary_key():
    print('viewing ')
    if request.args['type'] == 'Nurse':
        if 'inputID' in request.args.keys():
            return rq.retrieve_nurse(request)
        else:
            return rq.retrieve_nurse_self(request, session['username'])
    if request.args['type'] == 'patient':
        if 'inputSSN' in request.args.keys():
            return rq.retrieve_patient(request)
        else:
            return rq.retrieve_patient_me(request, session['username'])
    if request.args['type'] == 'vaccine':
        return rq.get_vaccine(request)



@app.route('/schedule', methods=['GET', 'POST'])
def resolve_schedule_request():
    if request.method == 'GET':
        if 'Personal' in request.args.keys():
            return rq.retrieve_personal_slots(request, session['username'])
        return rq.retrieve_slots(request)

    print(list(request.args.items()))
    # if request.args['type'] == 'nurse':
    print('inserting slot')
    if 'action' in request.args:
        rq.remove_personal_slots(request, session['username'])
    else:
        rq.insert_slot(request, session['username'])
    return render_template(session['main'])


if __name__ == '__main__':
    app.run()
