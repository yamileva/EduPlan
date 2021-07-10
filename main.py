from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_required, current_user

from models import db_session
from models.__all_models import *
from forms.__all_forms import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'protected_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/tracks")
@login_required
def show_user_tracks():
    session = db_session.create_session()

    tracks = session.query(Track).filter(
        (Track.user == current_user))
    return render_template("user_tracks.html", tlist=tracks)


@app.route("/track_templates")
def show_templates():
    session = db_session.create_session()
    templates = session.query(TrackTemplate)
    return render_template("track_templates.html",
                           tlist=templates)


@app.route("/track/<track_id>")
@login_required
def show_track(track_id):
    track_id = int(track_id[1:-1])
    session = db_session.create_session()
    track = session.query(Track).filter(Track.id == track_id,
                                        Track.user == current_user).first()
    if track:
        return render_template("track.html", track=track, sections=track.sections_to_table())
    else:
        abort(404)


@app.route("/edit_track/<track_id>", methods=['GET', 'POST'])
@login_required
def edit_track(track_id):
    form = NewTrackForm()
    track_id = int(track_id[1:-1])
    session = db_session.create_session()
    track = session.query(Track).filter(Track.id == track_id,
                                        Track.user == current_user).first()
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
    return render_template("track_edit.html", track=track, sections=track.sections_to_table(),
                           form=form)


@app.route('/create_track', methods=['GET', 'POST'])
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


@app.route('/create_section/<track_id>/<section_id>', methods=['GET', 'POST'])
@login_required
def create_section(track_id, section_id):
    form = NewSectionForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        track_id = int(track_id[1:-1])
        track = session.query(Track).filter(Track.id == track_id,
                                            Track.user == current_user).first()
        if track:
            section = Section()
            section.title = form.title.data
            section.type = int(form.type.data)

            section_id = int(section_id[1:-1])
            if section_id == -1:
                section.row = 1
            else:
                prev_section = session.query(Section).filter(Section.id == section_id,
                                                             Section.track_id == track_id).first()
                section.row = prev_section.row + prev_section.rows
            for item in track.sections:
                if item.row >= section.row:
                    item.row += 1
            section.duration = form.duration.data
            track.sections.append(section)
            session.merge(current_user)
            session.commit()
            return redirect('/edit_track/<{}>'.format(track_id))
        else:
            abort(404)
    return render_template('section_create.html', title='Добавление элемента', form=form)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


def main():
    db_session.global_init("db/tracks.sqlite")
    app.run()


if __name__ == '__main__':
    #app.run(port=8080, host='127.0.0.1')
    main()
