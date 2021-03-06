from flask import redirect, render_template, request, url_for, Blueprint
from project.users.models import User
from project.users.forms import UserForm
from project import db

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)


@users_blueprint.route('/', methods =["GET", "POST"])
def index():
	if request.method == "POST":
		form = UserForm(request.form)
		if form.validate():
			new_user = User(request.form['username'], request.form['email'], request.form['first_name'], request.form['last_name'])
			db.session.add(new_user)
			db.session.commit()
			return redirect(url_for('users.index'))
		return render_template('users/new.html', form=form)
	return render_template('users/index.html', users=User.query.all())

@users_blueprint.route('/new')
def new():
    form = UserForm()
    return render_template('users/new.html', form=form)

@users_blueprint.route('/<int:id>/edit')
def edit(id):
	users=User.query.get(id)
	form = UserForm(obj=users)
	return render_template('users/edit.html', form=form, user=users)

@users_blueprint.route('/<int:id>', methods =["GET", "PATCH", "DELETE"])
def show(id):
    found_user = User.query.get(id)
    if request.method == b"PATCH":
        form = UserForm(request.form)
        if form.validate():
            found_user.first_name = request.form['first_name']
            found_user.last_name = request.form['last_name']
            db.session.add(found_user)
            db.session.commit()
            return redirect(url_for('users.index'))
        return render_template('users/edit.html', form=form, user=found_user)
    if request.method == b"DELETE":
        db.session.delete(found_user)
        db.session.commit()
        return redirect(url_for('users.index'))
    return render_template('users/show.html', user=found_user)
