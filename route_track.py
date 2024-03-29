from flask import Blueprint
from flask import render_template, redirect, abort, request
from flask_login import login_required, current_user

from models import db_session
from models.__all_models import *
from forms.__all_forms import *


trc = Blueprint('track', __name__, template_folder='./templates/track')


@trc.route("/tracks")
@login_required
def show_user_tracks():
    session = db_session.create_session()

    tracks = session.query(Track).filter(
        (Track.user == current_user))
    return render_template("user_tracks.html", title="Список траекторий", tlist=tracks)


@trc.route("/track/<track_id>")
@login_required
def show_track(track_id):
    track_id = int(track_id[1:-1])
    session = db_session.create_session()
    track = session.query(Track).filter(Track.id == track_id,
                                        Track.user == current_user).first()
    if track:
        return render_template("track.html", title="Траектория", track=track,
                               sections=sorted(track.sections, key=lambda x: x.row))
    else:
        abort(404)


@trc.route("/edit_track/<track_id>", methods=['GET', 'POST'])
@login_required
def edit_track(track_id):
    form = NewTrackForm()
    track_id = int(track_id[1:-1])
    session = db_session.create_session()
    track = session.query(Track).filter(Track.id == track_id, Track.user == current_user).first()
    if request.method == "GET":
        if track:
            form.title.data = track.title
        else:
            abort(404)
    if form.validate_on_submit():
        if track:
            track.title = form.title.data
            session.commit()
            return redirect('/edit_track/<{}>'.format(track.id))
        else:
            abort(404)
    return render_template("track_edit.html", title="Редактирование траектории", track=track,
                           sections=sorted(track.sections, key=lambda x: x.row), form=form)


@trc.route('/create_track', methods=['GET', 'POST'])
@login_required
def create_track():
    form = NewTrackForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        track = Track()
        track.title = form.title.data
        current_user.tracks.append(track)
        session.merge(current_user)
        session.commit()
        return redirect('/tracks')
    return render_template('track_create.html', title='Создание новой траектории', form=form)


@trc.route('/del_track/<track_id>', methods=['GET', 'POST'])
@login_required
def del_track(track_id):
    track_id = int(track_id[1:-1])
    session = db_session.create_session()
    track = session.query(Track).filter(Track.id == track_id, Track.user == current_user).first()
    if track is None:
        abort(404)
    track.on_delete(session)
    session.delete(track)
    session.commit()
    return redirect('/tracks')


@trc.route('/activate_track/<track_id>', methods=['GET', 'POST'])
@login_required
def activate_track(track_id):
    track_id = int(track_id[1:-1])
    session = db_session.create_session()
    track = session.query(Track).filter(Track.id == track_id, Track.user == current_user).first()
    if track is None:
        abort(404)
    track.is_active = True
    session.commit()
    return redirect('/track/<{}>'.format(track.id))


@trc.route('/freeze_track/<track_id>', methods=['GET', 'POST'])
@login_required
def freeze_track(track_id):
    track_id = int(track_id[1:-1])
    session = db_session.create_session()
    track = session.query(Track).filter(Track.id == track_id, Track.user == current_user).first()
    if track is None:
        abort(404)
    track.is_active = False
    session.commit()
    return redirect('/track/<{}>'.format(track.id))
