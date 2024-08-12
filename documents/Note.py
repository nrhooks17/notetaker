from flask import current_app, make_response
from pymongo import DESCENDING
from datetime import datetime
import traceback
import re


class Note:
    # class fields:
    # created_by
    # updated_by

    def __init__(self, data: dict):
        # set all the data when receving a new note
        self.text = data['text']
        self.notebook = data['notebook']    
        self.page = data['page']

    # inserts a note into the mongodb database.
    @staticmethod
    def insert_note(note: dict):
        current_app.logger.info(f'inside of Note.insert_note() function')
        try:
            notes = Note.get_note_collection()
            current_datetime = datetime.now()

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
    def get_notes(page: int = 1, notebook: str = "default", upper_date_bound: str = None, lower_date_bound: str = None, note_search_string: str = ""):
        try:
            current_app.logger.info(f'inside of Note.get_notes() function')

            # grab notes collection
            notes = Note.get_note_collection()

            # grab collection
            current_app.logger.info(f'grabbing notes from database')
            current_app.logger.info(f'notebook: {notebook}, page: {page}')
            current_app.logger.info(f'upper date bound: {upper_date_bound}, lower date bound: {lower_date_bound}')
            current_app.logger.info(f'note search string: {note_search_string}')

            # grab parameters for find query
            query = Note.retrieve_notes_query(lower_date_bound, notebook, upper_date_bound, note_search_string)

            # grab total pages
            total_pages = Note.retrieve_total_pages(query)

            # do some pagination
            current_app.logger.info(f'query: {query}')
            notes = notes.find(query).sort("updated_at", DESCENDING).skip((page - 1) * current_app.amount_per_page).limit(current_app.amount_per_page)

            current_app.logger.info(f'successfully retrieved notes from database')
            return { "notes" : notes, "total_pages": total_pages, "current_page": page}

        except Exception as e:
            error_message = f'error getting notes from database: {traceback.print_exception(e)}'
            current_app.logger.error(error_message)
            return make_response({"message": error_message}, 500)

    @staticmethod
    def retrieve_notes_query(lower_date_bound: str, notebook: str, upper_date_bound: str, note_search_string: str):


        date_format: str = '%Y-%m-%d %H:%M:%S'
        # convert dates to utc.
        if (upper_date_bound and lower_date_bound) or (upper_date_bound != "" and lower_date_bound != ""):
            utc_lower_date_bound: datetime = datetime.strptime(lower_date_bound, date_format)
            utc_upper_date_bound: datetime = datetime.strptime(upper_date_bound, date_format)

            current_app.logger.info(f'lower date bound: {utc_lower_date_bound}')
            current_app.logger.info(f'upper date bound: {utc_upper_date_bound}')

            query = {
                "notebook": notebook,
                "updated_at": {
                    "$gt": utc_lower_date_bound,
                    "$lt": utc_upper_date_bound
                }
            }
        else:
            query = {
                "notebook": notebook,
            }

        # escape any regex characters
        note_search_string = re.escape(note_search_string)

        # filter based on search string if the query parameter exists.
        if note_search_string or note_search_string != "":
            query["text"] = {"$regex": note_search_string, "$options": "i"}


        current_app.logger.info(f'query: {query}')

        return query

    @staticmethod
    def retrieve_total_pages(query: dict):
        try:
            current_app.logger.info('inside of Note.retrieve_total_pages() function')
            notes  = Note.get_note_collection()
            current_app.logger.info(f'query: {query}')
            total_notes: str = notes.count_documents(query)

            # Need this due to the fact that the page count is not always divisible by the total notes.
            # If it isn't then I need to add 1 to the total pages as the last page will have any remaining notes
            # If the total notes is divisible by the page count then I can just return the total notes divided by
            # the page count.
            if total_notes % current_app.amount_per_page > 0:
                # Need to cast to int. Kinda hard to have a fraction of a page
                total_pages = int(total_notes / current_app.amount_per_page + 1)
                current_app.logger.info(f'total_pages: {total_pages}')
                return total_pages
            else:
                total_pages = int(total_notes / current_app.amount_per_page)
                current_app.logger.info(f'total_pages: {total_pages}')
                return total_pages

        except Exception as e:
            error_message = f'error getting notes from database: {traceback.print_exception(e)}'
            current_app.logger.error(error_message)
            return make_response({"message": error_message}, 500)

    @staticmethod
    def get_notebooks():
        try:
            current_app.logger.info(f'entering Note.getNotebooks() function')
            current_app.logger.info(f'grabbing notebooks from database')
            notes = Note.get_note_collection()

            projection = {"notebook": 1, "_id": 0, "updated_at": 1}

            notebooks = notes.find({}, projection).sort("updated_at", DESCENDING)

            unique_notebooks = set()
            ordered_notebooks =[]

            # only need notebooks. uses a set to make sure that there are no duplicates
            # list is there to preserve order
            for notebook in notebooks:
                if notebook["notebook"] not in unique_notebooks:
                    unique_notebooks.add(notebook["notebook"])
                    ordered_notebooks.append(notebook["notebook"])

            return { "notebooks": ordered_notebooks }

        except Exception as e:
            error_message = f'error getting notebooks from database: {traceback.print_exception(e)}'
            current_app.logger.error(error_message)
            return make_response({"message": error_message}, 500)

    @staticmethod
    def get_note_collection():
        current_app.logger.info(f'inside of Note.get_note_collection() function')
        # grabs the collection of notes from the database
        current_app.logger.info("grabbing notes collection from database")
        db = current_app.mongo_client.notetaker
        return db.notes