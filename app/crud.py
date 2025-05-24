# CRUD-Logik für Notizen
def create_note_in_db(note_data):
    note_id = len(notes_db) + 1
    notes_db.append({
        'id': note_id,
        'title': note_data['title'],
        'content': note_data['content'],
        'owner_id': note_data['owner_id']
    })
    return note_id

def update_note_in_db(note_id, note_data):
    note = find_note_by_id(note_id)
    if note:
        note.update({
            'title': note_data['title'],
            'content': note_data['content']
        })
        return True
    return False

def delete_note_in_db(note_id):
    note = find_note_by_id(note_id)
    if note:
        notes_db.remove(note)
        return True
    return False
