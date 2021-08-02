from flask import Blueprint
from flask import render_template, redirect, abort, request
from flask_login import login_required, current_user

from models import db_session
from models.__all_models import *
from forms.__all_forms import *


resrc = Blueprint('resrc', __name__, template_folder='./templates/resource')


@resrc.route('/check_progress/<resource_id>', methods=['GET', 'POST'])
@login_required
def check_progress(resource_id):
    form = CheckProgressForm()
    resource_id = int(resource_id[1:-1])
    session = db_session.create_session()
    resource = session.query(Resource).filter(Resource.id == resource_id).first()
    if request.method == "GET":
        if resource is None or resource.section.track.user != current_user:
            abort(404)
        form.completed.data = resource.completed

    if form.validate_on_submit():
        if resource is None or resource.section.track.user != current_user:
            abort(404)
        resource.completed = form.completed.data
        resource.progress = resource.completed * 100 // resource.intensity
        check_date = datetime.datetime.now()
        check_week = int(check_date.strftime('%W')) + int(check_date.strftime('%y')) * 52

        check = Check(
            resource_id=resource.id,
            completed=resource.completed,
            progress=resource.progress,
            check_date=check_date,
            check_week=check_week,
            resource=resource
        )
        resource.checks.append(check)
        session.merge(resource)

        section = resource.section
        section.progress = sum([res.progress for res in section.resources]) // len(section.resources)
        track = section.track
        track.progress = sum([sect.progress for sect in track.sections]) // len(track.sections)
        session.merge(section)
        session.merge(track)
        session.commit()
        return redirect('/section/<{}>'.format(resource.section.id))

    return render_template('check_progress.html', title="Отметить прогресс", resource=resource, form=form)


@resrc.route('/create_resource/<section_id>', methods=['GET', 'POST'])
@login_required
def create_resource(section_id):
    form = NewResourceForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        section_id = int(section_id[1:-1])
        section = session.query(Section).filter(Section.id == section_id).first()
        if section is None or section.track.user != current_user:
            abort(404)

        resource = Resource()
        resource.title = form.title.data
        resource.content = form.content.data
        resource.intensity = form.intensity.data
        resource.dim = form.dim.data
        resource.duration = form.duration.data
        resource.completed = form.completed.data
        resource.progress = resource.completed * 100 // resource.intensity
        resource.row = len(section.resources)

        section.resources.append(resource)
        session.merge(section)
        session.commit()
        section.duration = sum([res.duration for res in section.resources])
        section.progress = sum([res.progress for res in section.resources]) // len(section.resources)
        session.commit()
        track = section.track
        track.progress = sum([sect.progress for sect in track.sections]) // len(track.sections)
        session.merge(section)
        session.merge(track)
        session.commit()
        return redirect('/edit_section/<{}>'.format(section.id))

    return render_template('resource_create.html', title='Добавить ресурс', button_value="Создать", form=form)


@resrc.route('/edit_resource/<resource_id>', methods=['GET', 'POST'])
@login_required
def edit_resource(resource_id):
    form = NewResourceForm()
    resource_id = int(resource_id[1:-1])
    session = db_session.create_session()
    resource = session.query(Resource).filter(Resource.id == resource_id).first()
    if request.method == "GET":
        if resource is None or resource.section.track.user != current_user:
            abort(404)
        form.title.data = resource.title
        form.content.data = resource.content
        form.dim.data = resource.dim
        form.intensity.data = resource.intensity
        form.duration.data = resource.duration
        form.completed.data = resource.completed

    if form.validate_on_submit():
        if resource is None or resource.section.track.user != current_user:
            abort(404)
        resource.title = form.title.data
        resource.content = form.content.data
        resource.intensity = form.intensity.data
        resource.dim = form.dim.data
        resource.duration = form.duration.data
        resource.completed = form.completed.data
        resource.progress = resource.completed * 100 // resource.intensity

        section = resource.section
        section.duration = sum([res.duration for res in section.resources])
        section.progress = sum([res.progress for res in section.resources]) // len(section.resources)
        session.commit()
        track = section.track
        track.progress = sum([sect.progress for sect in track.sections]) // len(track.sections)
        session.merge(section)
        session.merge(track)
        session.commit()
        return redirect('/edit_section/<{}>'.format(resource.section.id))

    return render_template('resource_edit.html', title="Редактировать ресурс", button_value="Изменить",
                           resource=resource, form=form)


@resrc.route('/del_resource/<resource_id>', methods=['GET', 'POST'])
@login_required
def del_resource(resource_id):
    resource_id = int(resource_id[1:-1])
    session = db_session.create_session()
    resource = session.query(Resource).filter(Resource.id == resource_id).first()
    if resource is None or resource.section.track.user != current_user:
        abort(404)
    section = resource.section
    resource.on_delete(session)
    session.delete(resource)
    session.commit()
    if section.resources:
        section.duration = sum([res.duration for res in section.resources])
        section.progress = sum([res.progress for res in section.resources]) // len(section.resources)
    else:
        section.duration = 0
        section.progress = 0
    track = section.track
    track.progress = sum([sect.progress for sect in track.sections]) // len(track.sections)
    session.merge(section)
    session.merge(track)
    session.commit()
    return redirect('/edit_section/<{}>'.format(section.id))


@resrc.route('/move_up_resource/<resource_id>', methods=['GET'])
@login_required
def move_up_resource(resource_id):
    resource_id = int(resource_id[1:-1])
    session = db_session.create_session()
    resource = session.query(Resource).filter(Resource.id == resource_id).first()
    if resource is None or resource.section.track.user != current_user:
        abort(404)
    if resource.row > 0:
        prev_resource = session.query(Resource).filter(Resource.row == resource.row - 1,
                                                       Resource.section_id == resource.section_id).first()
        prev_resource.row += 1
        resource.row -= 1
        session.commit()
    return redirect('/edit_section/<{}>'.format(resource.section_id))


@resrc.route('/move_down_resource/<resource_id>', methods=['GET'])
@login_required
def move_down_resource(resource_id):
    resource_id = int(resource_id[1:-1])
    session = db_session.create_session()
    resource = session.query(Resource).filter(Resource.id == resource_id).first()
    if resource is None or resource.section.track.user != current_user:
        abort(404)
    section = session.query(Section).filter(Section.id == resource.section_id).first()
    if resource.row < len(section.resources) - 1:
        next_resource = session.query(Resource).filter(Resource.row == resource.row + 1,
                                                       Resource.section_id == resource.section_id).first()
        next_resource.row -= 1
        resource.row += 1
        session.commit()
    return redirect('/edit_section/<{}>'.format(resource.section_id))
