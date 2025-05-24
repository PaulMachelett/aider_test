from app.models import users_db, notes_db
def find_user_by_email(email):
    return next((user for user in users_db if user['email'] == email), None)

def find_user_by_id(user_id):
    return next((user for user in users_db if user['id'] == user_id), None)

def find_note_by_id(note_id):
    return next((note for note in notes_db if note['id'] == note_id), None)
