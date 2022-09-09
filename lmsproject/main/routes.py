from flask import render_template, Blueprint
from flask_login import login_required
from flask import Blueprint


main = Blueprint('main', __name__)



@main.route('/', methods=["GET","POST"])
@main.route('/home', methods=["GET","POST"])
def home():
    return render_template('main/index.html',title='Home')



@main.route('/elearningunit1',methods=['GET','POST'])
@login_required
def elearningunit1():
    return render_template('main/elearningunit1.html',title='E-learning Unit1')



@main.route('/elearningunit2',methods=['GET','POST'])
@login_required
def elearningunit2():
    return render_template('main/elearningunit2.html',title='E-learning Unit2')



@main.route('/elearningunit4',methods=['GET','POST'])
@login_required
def elearningunit4():
    return render_template('main/elearningunit4.html',title='E-learning Unit4')



@main.route('/elearning',methods=['GET','POST'])
@login_required
def elearning():
    return render_template('main/elearning.html',title='E-learning')



@main.route('/faculty',methods=['GET','POST'])
@login_required
def faculty():
    return render_template('main/faculty.html',title='Faculty')



@main.route('/semester',methods=['GET','POST'])
@login_required
def semester():
    return render_template('main/semester.html',title='Semester')



@main.route('/subject',methods=['GET','POST'])
@login_required
def subject():
    return render_template('main/subject.html',title='Subject')
