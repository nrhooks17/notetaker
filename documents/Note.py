from flask import current_app, make_response
from datetime import datetime
from pprint import pprint
import traceback, pprint


class Note:
    # TODO
    # class fields:
    # created_by
    # updated_by

    text: str = ""

    def __init__(self, data: dict):
        # set all the data when receving a new note
        self.text = data['text']
        self.notebook = data['notebook']
        self.page = data['page']

    # inserts a note into the mongodb database.
    @staticmethod
    def insert_note(note: dict):
        try:
            notes = Note.get_note_collection()
            current_datetime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

            # create
            note['updated_at'] = current_datetime
            note['created_at'] = current_datetime

            current_app.logger.info(f'inserting note into database: {note}')
            notes.insert_one(note)

            return [True, {}]

        except Exception as e:
            error_message = f'error inserting note into database: {traceback.print_exception(e)}'
            current_app.logger.error(error_message)
            return make_response({"message": error_message}, 500)

    @staticmethod
    def get_notes(page: int = 1, notebook: str = "default"):
        try:
            # grab database
            notes = Note.get_note_collection()

            # grab collection
            current_app.logger.info(f'grabbing notes from database')
            notes = notes.find({"notebook": notebook, "page": page})

            current_app.logger.info(f'page is {isinstance(page, str)}')
            current_app.logger.info('after pprint inisde of get_notes() function inside of Note.py')


            return list(notes)
        except Exception as e:
            error_message = f'error getting notes from database: {traceback.print_exception(e)}'
            current_app.logger.error(error_message)
            return make_response({"message": error_message}, 500)

    @staticmethod
    def retrieve_total_pages():
        try:
            notes = Note.get_note_collection()
            highest_paged_note = notes.find().sort('page', -1).limit(1)

            return highest_paged_note[0]['page']
        except Exception as e:
            error_message = f'error getting notes from database: {traceback.print_exception(e)}'
            current_app.logger.error(error_message)
            return make_response({"message": error_message}, 500)

    @staticmethod
    def get_note_collection():
        # grabs the collection of notes from the database
        current_app.logger.info("grabbing notes collection from database")
        db = current_app.mongo_client.notetaker
        return db.notes