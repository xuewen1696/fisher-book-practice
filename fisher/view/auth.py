from fisher.models.base import db
from fisher.forms.author import RegisterForm, LoginForm, EmailForm,ResetPasswordForm
from fisher.models.user import User
from . import web

from flask import render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        print('i am in')
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            try:
                next_url = request.args.get('next')
            except AttributeError:
                next_url = None
            print(next_url)
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('web.index')
            return redirect(next_url)
        else:
            flash("账号不存在或密码错误")

    return render_template('auth/login.html', form={'data': {}})


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    if request.method == 'POST':
        form = EmailForm(request.form)
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            from fisher.libs.email import send_mail
            send_mail(form.email.data, '重置您的密码', 'email/reset_password.html', user=user, token=user.generate_token())
            flash('一封邮件已经发送到您的注册邮箱' + account_email + '请及时查收')
    return render_template('auth/forget_password_request.html')


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('您的密码已经更新，请重新登陆')
            return redirect('web.login')
        else:
            flash('密码重置失败')

    render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
