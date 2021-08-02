from flask import Blueprint
from flask import render_template, redirect, abort, request
from flask_login import login_required, current_user

from models import db_session
from models.__all_models import *
from forms.__all_forms import *


sect = Blueprint('sect', __name__, template_folder='./templates/section')

@sect.route('/section/<section_id>', methods=['GET', 'POST'])
@login_required
def show_section(section_id):
    section_id = int(section_id[1:-1])
    session = db_session.create_session()
    section = session.query(Section).filter(Section.id == section_id).first()
    if section is None or section.track.user != current_user:
        abort(404)
    return render_template("section.html", title="Раздел", section=section,
                           resources=sorted(section.resources, key=lambda x: x.row))


@sect.route('/create_section/<track_id>/<section_id>', methods=['GET', 'POST'])
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
                section.row = prev_section.row + 1
            for item in track.sections:
                if item.row >= section.row:
                    item.row += 1
            section.duration = form.duration.data
            track.sections.append(section)
            track.sections.sort(key=lambda x: x.row)
            session.merge(track)
            session.commit()
            return redirect('/edit_section/<{}>'.format(section.id))
        else:
            abort(404)
    return render_template('section_create.html', title='Добавление элемента', form=form)


@sect.route('/edit_section/<section_id>', methods=['GET', 'POST'])
@login_required
def edit_section(section_id):
    form = NewSectionForm()
    section_id = int(section_id[1:-1])
    session = db_session.create_session()
    section = session.query(Section).filter(Section.id == section_id).first()
    if request.method == "GET":
        if section is None or section.track.user != current_user:
            abort(404)
        form.title.data = section.title
        form.duration.data = section.duration
        form.type.data = str(section.type)
    if form.validate_on_submit():
        if section is None or section.track.user != current_user:
            abort(404)
        section.title = form.title.data
        section.duration = form.duration.data
        session.commit()
        return redirect('/edit_section/<{}>'.format(section_id))
    return render_template('section_edit.html', title="Редактирование раздела", section=section,
                           resources=sorted(section.resources, key=lambda x: x.row), form=form)


@sect.route('/del_section/<section_id>', methods=['GET'])
@login_required
def del_section(section_id):
    section_id = int(section_id[1:-1])
    session = db_session.create_session()
    section = session.query(Section).filter(Section.id == section_id).first()
    if section is None or section.track.user != current_user:
        abort(404)
    track = section.track
    section.on_delete(session)
    session.delete(section)
    session.commit()
    if track.sections:
        track.progress = sum([sect.progress for sect in track.sections]) // len(track.sections)
    else:
        track.progress = 0
    session.merge(track)
    session.commit()
    return redirect('/edit_track/<{}>'.format(track.id))


@sect.route('/move_up_section/<section_id>', methods=['GET'])
@login_required
def move_up_section(section_id):
    section_id = int(section_id[1:-1])
    session = db_session.create_session()
    section = session.query(Section).filter(Section.id == section_id).first()
    if section is None or section.track.user != current_user:
        abort(404)
    if section.row > 0:
        prev_section = session.query(Section).filter(Section.row == section.row - 1,
                                                     Section.track_id == section.track_id).first()
        prev_section.row += 1
        section.row -= 1
        track = session.query(Track).filter(Track.id == section.track_id).first()
        track.sections.sort(key=lambda x: x.row)
        session.commit()
    return redirect('/edit_track/<{}>'.format(section.track_id))


@sect.route('/move_down_section/<section_id>', methods=['GET'])
@login_required
def move_down_section(section_id):
    section_id = int(section_id[1:-1])
    session = db_session.create_session()
    section = session.query(Section).filter(Section.id == section_id).first()
    if section is None or section.track.user != current_user:
        abort(404)
    track = session.query(Track).filter(Track.id == section.track_id,
                                        Track.user == current_user).first()
    if section.row < len(track.sections) - 1:
        next_section = session.query(Section).filter(Section.row == section.row + 1,
                                                     Section.track_id == section.track_id).first()
        next_section.row -= 1
        section.row += 1
        track.sections.sort(key=lambda x: x.row)
        session.commit()
    return redirect('/edit_track/<{}>'.format(section.track_id))
