from flask import Blueprint, request, current_app, jsonify, make_response
from documents.Note import Note
from bson.json_util import dumps
import traceback

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/note', methods=['POST'])
def submit_note():
    current_app.logger.info("inside of routes.submit_note() function")
    try:
        if request.method == 'POST':
            # get the note text from the request
            current_app.logger.info("inside of submit_note() function")
            note = request.get_json()
            current_app.logger.info("note: " + note["text"] + " notebook: " + note["notebook"] + " page: " + str(note["page"]))

            # submit the new note
            Note.insert_note(note)

            return {"message": "successfully submitted " + note['text'] + " note into database"}

    except Exception as e:
        current_app.logger.error("error submitting note")
        return make_response({"message": f'error submitting note: {traceback.print_exception(e)}'}, 500)


@api_blueprint.route('/notes', methods=['GET'])
def get_notes():
    current_app.logger.info("inside of routes.get_notes() function")
    try:
        if request.method == 'GET':
            current_app.logger.info("inside of get_notes() function inside of routes.py")

            page = int(request.args.get("page"))
            notebook = request.args.get("notebook")
            upper_date_bound = request.args.get("upperDateBound")
            lower_date_bound = request.args.get("lowerDateBound")

            current_app.logger.info(f' notes page: {page}')
            current_app.logger.info(f' notebook: {notebook}')
            current_app.logger.info(f' upper date bound: {upper_date_bound}')
            current_app.logger.info(f' lower date bound: {lower_date_bound}')

            return dumps(Note.get_notes(page, notebook, upper_date_bound, lower_date_bound))

    except Exception as e:
        current_app.logger.error(f'error getting notes: {traceback.print_exception(e)}')
        return make_response({"message": f'error getting notes: {e}'}, 500)

@api_blueprint.route('/note', methods=['GET'])
def get_note():
    current_app.logger.info("inside of routes.get_note() function")
    try:
        if request.method == 'GET':
            return {"message": "successfully retrieved note from database"}

    except Exception as e:
        current_app.logger.error(f'error getting note: {e}')
        return make_response({"message": f'error getting note: {traceback.print_exception(e)}'}, 500)

@api_blueprint.route('/total_pages', methods=['GET'])
def retrieve_total_pages():
    current_app.logger.info("inside of routes.retrieve_total_pages() function")
    try:
        if request.method == 'GET':
            current_app.logger.info('inside of retrieve_total_pages() function')
            return dumps({"total_pages": Note.retrieve_total_pages()})

    except Exception as e:
        current_app.logger.error(f'error retrieving total pages from notes collection in database: {traceback.print_exception(e)}')
        return make_response({"message": f'error retrieving total pages from notes collection in database: {e}'}, 500)

@api_blueprint.route('/notebooks', methods=['GET'])
def get_notebooks():
    try:
        if request.method == 'GET':
            current_app.logger.info("inside of get_notebooks() function")
            return dumps(Note.get_notebooks())

    except Exception as e:
        current_app.logger.error(f'error getting notebooks: {e}')
        return make_response({"message": f'error getting notebook: {traceback.print_exception(e)}'}, 500)

@api_blueprint.route("/notebook", methods=['POST'])
def insert_notebook():
    try:
        if request.method == 'POST':
            current_app.logger.info("inside of insert_notebook() function")
            data = request.get_json()

            # create new note.
            note = {
                "notebook": data['notebook'],
                "text": f'created notebook: {data["notebook"]}',
                "page": 1
            }

            current_app.logger.info(f'inserting notebook by inserting note: {note}')
            Note.insert_note(note)
            current_app.logger.info(f'inserted notebook: {data["notebook"]}')
            return {"message": f'inserted notebook: {data["notebook"]}'}

    except Exception as e:
        current_app.logger.error(f'error inserting notebook: {e}')
        return make_response({"message": f'error inserting notebook: {traceback.print_exception(e)}'}, 500)