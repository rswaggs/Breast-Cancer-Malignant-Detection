from flask import Blueprint, render_template, request, url_for, redirect, session, flash

from db_extension import mysql

from wrapper_funcs import login_req

search_blueprint = Blueprint("search", __name__)

@search_blueprint.route('/search', methods=['GET', 'POST'])
@login_req
def searchpage():
  conn = mysql.connect()
  cursor = conn.cursor()

  cursor.callproc('GetPatientData')
  patient_data = cursor.fetchall()

  if request.method == "POST":

    patient = request.form['patient']

    patient_fname = str(patient).split()[0]
    patient_lname = str(patient).split()[1]

    cursor.callproc('GetOnePatient', (patient_fname, patient_lname))
    searched_patient_data = cursor.fetchall()[0]

    cursor.close()
    conn.close()

    if not searched_patient_data:
      return render_template('views/search.html', patient=None, patients=patient_data)

    else:
      return render_template('views/search.html', patient=searched_patient_data, patients=patient_data)
    
    return render_template('views/search.html', patient=None, patients=patient_data)

  else:
    cursor.close()
    conn.close()
    return render_template('views/search.html', patient=None, patients=patient_data)