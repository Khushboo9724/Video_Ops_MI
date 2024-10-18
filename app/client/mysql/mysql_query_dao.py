from sqlalchemy import or_, desc

from app.db.database import Database

database = Database()
engine = database.get_db_connection()


def insert(create_object):
    session = database.get_db_session(engine)
    session.add(create_object)
    session.commit()
    session.refresh(create_object)
    session.close()
    return create_object


def get_by_id(table_name, field_name, id_value):
    session = database.get_db_session(engine)
    db_data = (session.query(table_name).filter
               (field_name == id_value, table_name.is_deleted == 0).first())
    session.close()
    return db_data


def get_by_name(table_name, field_name, name):
    session = database.get_db_session(engine)
    db_data = (session.query(table_name).filter
               (field_name == name, table_name.is_deleted == 0).first())
    session.close()
    return db_data


def get_all(table_name, skip=None, items_per_page=None):
    session = database.get_db_session(engine)
    if skip is not None and items_per_page is not None:
        filtered_query = session.query(table_name).filter_by(
            is_deleted=0).order_by(desc(table_name.created_on))
        limited_and_offset_query = filtered_query.limit(items_per_page).offset(
            skip)
        db_data = limited_and_offset_query.all()
    else:
        db_data = session.query(table_name).filter_by(is_deleted=0).all()
        db_data.reverse()
    session.close()
    return db_data


def get_by_token_id(table_name, field_name, name):
    session = database.get_db_session(engine)
    db_data = (session.query(table_name).filter
               (field_name == name, table_name.is_deleted == 0).first())
    session.close()
    return db_data


def update(update_object):
    session = database.get_db_session(engine)
    session.merge(update_object)
    session.flush()
    session.commit()
    # Get The I'd Of Updated Item
    session.close()
    return update_object


def delete(table_name, pk_column, user_pass_id):
    session = database.get_db_session(engine)
    session.query(table_name).filter(pk_column == user_pass_id).delete()
    session.flush()
    session.commit()
    session.close()
    return True


def get_by_username(table_name, u_name):
    session = database.get_db_session(engine)
    db_data = session.query(table_name).filter_by(username=u_name).first()
    session.close()
    return db_data


def get_by_email(table_name, u_email):
    session = database.get_db_session(engine)
    db_data = session.query(table_name).filter_by(email=u_email).first()
    session.close()
    return db_data


def get_by_phone(table_name, phone_number):
    session = database.get_db_session(engine)
    db_data = session.query(table_name).filter_by(phone=phone_number).first()
    session.close()
    return db_data


def search_all_videos_details(video, search_keyword):
    session = database.get_db_session(engine)
    search_keyword_int = None
    if search_keyword.isdigit():
        search_keyword_int = int(search_keyword)
    if not search_keyword_int:
        search_keyword_int = search_keyword
    query = session.query(
        video.id,
        video.file_name,
        video.path,
        video.size,
        video.created_on,
        video.modified_on,
        video.is_deleted
    ).order_by(desc(video.created_on))
    search_filter = (
        (video.file_name.ilike(f"%{search_keyword}%") )|
        (video.size.ilike(f"%{search_keyword_int}%"))
    )
    query = query.filter(search_filter)

    query = query.filter(video.is_deleted == False)

    result = query.all()

    data = [
        {
            "id": row[0],
            "file_name": row[1],
            "path": row[2],
            "size": row[3],
            "created_on": row[4],
            "modified_on": row[5],
            "is_deleted": row[6]
        }
        for row in result
    ]

    session.close()
    return data


def get_role(table_name, pk_column, user_pass_id):
    session = database.get_db_session(engine)
    db_data = session.query(table_name).filter(
        pk_column == user_pass_id).first()
    session.close()
    return db_data


def get_required_field_data_by_id(table_name, pk_column, user_pass_id,
                                  column_name):
    session = database.get_db_session(engine)
    column_to_select = getattr(table_name, column_name,
                               None)  # Use getattr to access the column
    db_data = session.query(column_to_select).filter(
        pk_column == user_pass_id).all()
    session.close()
    return db_data
