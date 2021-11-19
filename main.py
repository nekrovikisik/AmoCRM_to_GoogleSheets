from wtforms.fields.datetime import  DateField
from wtforms import validators, SubmitField, SelectField
from flask import Flask, redirect,  render_template, session
from flask_wtf import FlaskForm
import gsheets
from gsheets import *
from export_leads import *

app = Flask(__name__)

app.config['SECRET_KEY'] = '#$%^&*'


class InfoForm(FlaskForm):
    startdate = DateField('Start Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    enddate = DateField('End Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField('Submit')
    project = SelectField(u'select project', choices=[('RE', 'Ремонт-Экспресс'),
                            ('MR', 'Московский ремонтник'), ('FR', 'Флагман ремонта'),
                            ('RR', 'Русский ремонт'), ('BH', 'BeHome'),
                            ('spb.RE', 'Спб.Ремонт-Экспресс'),('sbp.FR', 'СПб.Флагман ремонта'),
                                                      ('NR', 'Невский ремонтник'), ],
                          validators=(validators.DataRequired(),))


@app.route('/', methods=['GET', 'POST'])
def index():
    infoForm = InfoForm()
    print(infoForm.startdate.data)
    if infoForm.validate_on_submit():
        print('click')
        session['startdate'] = infoForm.startdate.data.strftime('%d/%m/%Y')
        session['enddate'] = infoForm.enddate.data.strftime('%d/%m/%Y')
        session['project'] = infoForm.project.data
        return redirect('date')
    return render_template('index.html', infoForm=infoForm)

@app.route('/date', methods=['GET','POST'])
def date():
    #global sheet_id
    session['sheet_id']=f"{session['project']}_{session['startdate']}-{session['enddate']}"
    print(session, type(session['startdate']))
    df = getLeadsDF(session['startdate'], session['enddate'])
    print('start paste')
    session['sheet_id'] = gsheets.pastDataFrame_into_Sheets(df, f'{session["project"]}: {session["startdate"]}-{session["enddate"]}')
    print('pasted')
    return render_template('date.html')


if __name__ == '__main__':
    app.run(debug=True)
