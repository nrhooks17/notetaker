from flask import current_app, make_response
from datetime import datetime
import traceback, pprint


class Note:
    # TODO
    # class fields:
    # created_by
    # updated_by

    text: str = ""

    def __init__(self, data: dict):
        # set all the data when receving a new note
        self.text = data['note']
        self.notebook = data['notebook']
        self.page = data['page']

    # inserts a note into the mongodb database.
    @staticmethod
    def insert_note(note: 'Note'):
        try:
            # grabs the database from the app state
            db = current_app.mongo_client.notetaker

            # grabs the collection of notes from the database
            current_app.logger.info("grabbing notes collection from database")
            notes = db.notes
            current_datetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

            # create
            document = {
                'text': note.text,
                'page': note.page,
                'notebook': note.notebook,
                'updated_at': current_datetime,
                'created_at': current_datetime
            }

            current_app.logger.info(f'inserting note into database: {document}')
            notes.insert_one(document)

            return [True, {}]

        except Exception as e:
            error_message = f'error inserting note into database: {traceback.print_exception(e)}'
            current_app.logger.error(error_message)
            return make_response({"message": error_message}, 500)

    @staticmethod
    def get_notes():
        try:
            # grab database
            db = current_app.mongo_client.notetaker

            # grab collection
            current_app.logger.info(f'grabbing notes from database')
            notes = db.notes.find()

            # list_of_notes = []

            current_app.logger.info(pprint.pprint(notes))

            # return list_of_notes
            return []
        except Exception as e:
            error_message = f'error getting notes from database: {traceback.print_exception(e)}'
            current_app.logger.error(error_message)

            return make_response({"message": error_message}, 500)
