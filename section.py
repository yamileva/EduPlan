from flask import Blueprint
from flask import render_template, redirect, abort, request
from flask_login import login_required, current_user

from models import db_session
from models.__all_models import *
from forms.__all_forms import *


sect = Blueprint('sect', __name__, template_folder='./templates/section')


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

