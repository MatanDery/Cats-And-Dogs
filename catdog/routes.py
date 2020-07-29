from flask import Flask, render_template, flash, request, make_response, redirect ,url_for
from catdog import app, que, r, worker
from catdog.forms import VoteForm, UpdateImage
from catdog.poll_votes import update_votes
import subprocess
from catdog.user_image_page import save_picture, detect_wraper
from hashlib import md5


def init_db():
    value = r.get("Dogs")
    if value is None:
        r.set("Dogs", 0)
    value = r.get("Cats")
    if value is None:
        r.set("Cats", 0)


init_db()


@app.route('/', methods=['GET', 'POST'])
def home():
    form = VoteForm()
    if form.validate_on_submit():
        #req_ip = request.remote_addr
        req_ip = request.headers.getlist("X-Forwarded-For")[0]
        if request.cookies.get('Voted') == 'True':
            flash('You Already Voted!', category='danger')
            return redirect('/')

        que.enqueue(update_votes, voted=form.vote.data, req_ip=req_ip)

        if len(que) > 10:
            subprocess.Popen(['rqworker', "--url", "redis://redis:6379", "-b"])
        flash(f'Voted! {form.vote.data}', category='success')

        resp = make_response(render_template('home.html', form=form, r=r))
        resp.set_cookie('Voted', 'True')
        return resp

    elif request.method == 'POST':
        flash('Pick Your Vote', category='primary')

    return render_template('home.html', form=form, r=r)


@app.route('/images', methods=['GET', 'POST'])
def user_images():
    form = UpdateImage()

    #req_ip = request.remote_addr  # todo
    req_ip = request.headers.getlist("X-Forwarded-For")[0]

    if form.validate_on_submit():
        if form.picture.data:
            pic = save_picture(form.picture.data, req_ip)
            que.enqueue(detect_wraper, picture_name=pic)  # todo more workers?

            flash('The detection will be in shortly :)', category='success')

    load_pic = False
    detection = None
    pic_name = md5(req_ip.encode()).hexdigest()+'.jpg'
    if r.hget('picture_detaction', pic_name) is not None:
        load_pic = True
        detection = r.hget('picture_detaction', pic_name)
        pic_name = url_for('static', filename='user_pictures/' + pic_name)
    return render_template('images.html', form=form, pic_name=pic_name,
                           load_pic=load_pic, detection=detection)






