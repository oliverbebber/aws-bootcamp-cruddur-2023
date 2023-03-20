from psycopg_pool import ConnectionPool
import os
import re # importing to use regex so we don't have 2 functions for RETURNING 
import sys # importing due to sys os not defined error
from flask import current_app as app # reference app template

class Db:
    def __init__(self):
        self.init_pool()

    # def load_sql(): --- changed name to template
    def template(self, name): # added self as an arg due to takes 1 positional arg but 2 were given
        # template_path = os.path.join(app.instance_path, 'db', 'sql', name+'.sql') --- changed to app.root_path due to "no such file or dir 'backend-flask/INSTANCE/db/sql/create_activity.sql"
        # with open(template_path, 'r') as f: 
            # template_content = f.read()
        # return template_content
        template_path = os.path.join(app.root_path, 'db', 'sql', f"{name}.sql")
        with open(template_path, 'r') as f:
            template_content = f.read()
        return template_content

    def init_pool(self):
        connection_url = os.getenv("CONNECTION_URL")
        self.pool = ConnectionPool(connection_url)

    def print_sql(self, title, sql):
        cyan = '\033[96m'
        no_color = '\033[0m'
        print("\n")
        print(f'{cyan}SQL STATEMENT-[{title}]------{no_color}')
        print(sql + "\n")

    #def query_commit_with_returning_id(self, sql, *kwargs):----changed to query_commit_id --- changed to query_commit & params
    # def query_commit_id(self, sql, *kwargs):
        #print("SQL STATEMENT-[commit with returning]------")
        #try: 
            #conn = self.pool.connection()
            #cur = conn.cursor()
            #cur.execute(sql, kwargs) ----- allows us to change VALUES to be %s
            #returning_id = cur.fetchone()[0]
            #conn.commit()
            #return returning_id

        ## ----- fix lambda
        #         VALUES(%s,%s,%s,%s)
        #
        #         params = [
        #    user_display_name, 
        #    user_email, 
        #    user_handle, 
        #    user_cognito_id
        #]
        #cur.execute(sql, *params)
        #conn.commit()

    ## we want to commit data such as an insert
    ## be sure RETURNING is in all caps
    def query_commit(self, sql, params): # new, refactored from query_commit_returning_id
        print("SQL STATEMENT-[commit with returning]------") # edited - "with returning"
        #print(sql = "\n")
        self.print_sql('commit with returning', sql) # new

        pattern = r"\bRETURNING\b"
        is_returning_id = re.search(pattern, sql) # (pattern, my_string) originally -- changed to sql

        try:
            # conn = self.pool.connection() ---this conn has no object called cursor on the next line
            # cur = conn.cursor() ---- object has no attribute 'cursor' line 24 error -- skips fixing this to create new sql folder - create_activity.sql ---- error appeared again 
            # cur.execute(sql, kwargs)
            # if is_returning_id:
                # returning_id = cur.fetchone()[0]
            # conn.commit()
            # if is_returning_id:
                # return returning_id
        # except Exception as err:
            # self.print_sql_err(err)
            
            with self.pool.connection() as conn: # added after object has no attribute 'cursor' error
                # with conn.cursor() as cur: # does not resolve issue - potentially causing other issues
                cur = conn.cursor()
                cur.execute(sql, params) # sql statement [commit with returning] should be printing out before this line & it does. Add color next
                if is_returning_id:
                    returning_id = cur.fetchone()[0]
                conn.commit()
                if is_returning_id:
                    return returning_id
        except Exception as err:
            self.print_sql_err(err)

    # when we want to return an array of json objects
    def query_array_json(self, sql):
        print("SQL STATEMENT-[array]------")
        print(sql + "\n")
        wrapped_sql = self.query_wrap_array(sql)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql)
                # this will return a tuple
                # the first field being the data
                json = cur.fetchone()
                return json[0]

    # when we want to return a json object
    def query_object_json(self, sql):
        print("SQL STATEMENT-[object]------")
        print(sql + "\n")
        wrapped_sql = self.query_wrap_object(sql)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql)
                # this will return a tuple
                # the first field being the data
                json = cur.fetchone()
                return json[0]

    def query_wrap_object(self, template):
        sql = f"""
        (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
        {template}
        ) object_row);
        """
        return sql

    def query_wrap_array(self, template):
        sql = f"""
        (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
        {template}
        ) array_row);
        """
        return sql

    # define a function that handles and parses psycopg exceptions
    def print_sql_err(self, err):
        # get details about the exception
        err_type, err_obj, traceback = sys.exc_info()

        # get the line number when exception occured
        line_num = traceback.tb_lineno

        # print the connect() error
        print ("\npsycopg ERROR:", err, "on line number:", line_num)
        print ("psycopg traceback:", traceback, "-- type:", err_type)

        # psycopg extensions.Diagnostics object attribute
        # print ("\nextensions.Diagnostics:", err.diag) ---commented out due to attribute error object has no attribute 'diag'

        # print the pgcode and pgerror exceptions
        # print ("pgerror:", err.pgerror)
        # print ("pgcode:", err.pgcode, "\n")

db = Db()