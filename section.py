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
    return render_template("section.html", section=section)


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

    return render_template('section_edit.html', section=section, form=form)