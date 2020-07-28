from flask import Flask, render_template, flash, request, make_response, redirect ,url_for
from catdog import app, que, r, worker
from catdog.forms import VoteForm
from time import sleep
import subprocess

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


def update_votes(voted, req_ip):
    sleep(2)
    if vote_check(req_ip) != 0:
        r.set(voted, int(r.get(voted)) + 1)
    return


def vote_check(req_ip):
    x = r.sadd('voted_ip', req_ip)
    return x


