import uuid
from datetime import datetime, timedelta, timezone

from lib.db import db #query_commit, print_sql_err
# db not defined -- from lib.db import db was commented out
# removing the comment allowed SQL STATEMENT-[array]---- to print in the terminal
# conditionally hide because we only want it for dev and not prod

class CreateActivity:
  def run(message, user_handle, ttl):
    model = {
      'errors': None,
      'data': None
    }

    now = datetime.now(timezone.utc).astimezone()

    if (ttl == '30-days'):
      ttl_offset = timedelta(days=30) 
    elif (ttl == '7-days'):
      ttl_offset = timedelta(days=7) 
    elif (ttl == '3-days'):
      ttl_offset = timedelta(days=3) 
    elif (ttl == '1-day'):
      ttl_offset = timedelta(days=1) 
    elif (ttl == '12-hours'):
      ttl_offset = timedelta(hours=12) 
    elif (ttl == '3-hours'):
      ttl_offset = timedelta(hours=3) 
    elif (ttl == '1-hour'):
      ttl_offset = timedelta(hours=1) 
    else:
      model['errors'] = ['ttl_blank']

    if user_handle == None or len(user_handle) < 1:
      model['errors'] = ['user_handle_blank']

    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 280:
      model['errors'] = ['message_exceed_max_chars'] 

    if model['errors']:
      model['data'] = {
        'handle':  user_handle,
        'message': message
      }   
    else:
      # return an object
      # self.create_activity()
      expires_at = (now + ttl_offset) # new
      CreateActivity.create_activity(user_handle, message, expires_at) # new - originally self.create_activity but hit 'self' is not defined the changed to the stateless class 
      model['data'] = {
        'uuid': uuid.uuid4(),
        'display_name': 'Andrew Brown',
        'handle':  user_handle,
        'message': message,
        'created_at': now.isoformat(),
        'expires_at': (now + ttl_offset).isoformat()
      }
    return model
  
# def create_activity(user_uuid, message, expires_at):
#   sql = f"""
#   INSERT INTO (
#     user_uuid,
#     message,
#     expires_at
#   )
#   VALUES (
#     (SELECT uuid 
#       FROM public.users 
#       WHERE users.handle = 'andrewbrown' -- change to %(handle)s
#       LIMIT 1
#     ),
#     %s, --- changing to %(message)s
#     %s, --- changing to %(expires_at)s
#   ) RETURNING uuid;
# """
# uuid = db.query_commit_with_returning_id(sql, --- changed to db.query_commit_id 
#   user_uuid, --- change to handle=handle, ---- unexpected keyword argument 'handle'
#   message,   --- change to message=message,
#   expires_at --- change to expires_at=expires_at
#   }) -- needs to be splatted

#### NEW - refactored from above
# uuid = db.query_commit(sql, {
#   'handle': handle
#   'message': message,
#   'expires_at': expires_at
#   }) -- needs to be splatted

  def create_activity(handle, message, expires_at):
    # sql = db.load_sql ('create_activity.sql') # assume all files are sql by leaving out .sql --- changed name to template
    sql = db.template('create_activity')
    uuid = db.query_commit(sql,{
      'handle': handle, 
      'message': message,
      'expires_at': expires_at
    })


    #query_commit(sql)
  #def query_object_activity():