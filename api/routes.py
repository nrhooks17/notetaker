from flask import Blueprint, request, current_app, jsonify, make_response
from documents.Note import Note
import traceback

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/note', methods=['POST'])
def submit_note():
    try:
        if request.method == 'POST':
            # get the note text from the request
            current_app.logger.info("inside of submit_note() function")

            data = request.get_json()
            note = Note(data)

            current_app.logger.info("note: " + note.text)

            # submit the new note
            Note.insert_note(note)

            return {"message": "successfully submitted " + note.text + " note into database"}
    except Exception as e:
        current_app.logger.error("error submitting note")

        return make_response({"message": f'error submitting note: {traceback.print_exception(e)}'}, 500)


@api_blueprint.route('/notes', methods=['GET'])
def get_notes():
    try:
        if request.method == 'GET':
            current_app.logger.info("inside of get_notes() function inside of routes.py")

            page = request.args.get("page")
            current_app.logger.info(f' notes page: {page}')
            notes = Note.get_notes()

            return jsonify(notes)
    except Exception as e:
        current_app.logger.error(f'error getting notes: {traceback.print_exception(e)}')
        return make_response({"message": f'error getting notes: {e}'}, 500)


@api_blueprint.route('/note', methods=['GET'])
def get_note():
    try:
        if request.method == 'GET':
            return {"message": "successfully retrieved note from database"}

    except Exception as e:
        current_app.logger.error(f'error getting note: {e}')
        return make_response({"message": f'error getting note: {traceback.print_exception(e)}'}, 500)
