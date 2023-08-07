from core.session import Sessions, UserSession
from database.db import Database


def test_init_sessions() -> tuple:
    """
    Tests that the Sessions class is initialized correctly.
    user profile 

    args:
        - None

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    sessions = Sessions()

    if len(sessions.sessions) != 0:
        error = f"Error in test_init_sessions: Sessions dictionary is not empty.\n  - Actual: {len(sessions.sessions)}"
        return False, error
    else:
        return True, "Sessions dictionary is empty."


def test_add_new_session() -> tuple:
    """
    Tests that a new session is added correctly.
    testing whether a new user is added correctly

    args:
        - None

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    db = Database("database/store_records.db")
    sessions = Sessions()
    sessions.add_new_session("test", db)

    if len(sessions.sessions) == 0:
        error = f"Error in test_add_new_session: Sessions dictionary is empty.\n  - Actual: {len(sessions.sessions)}"
        return False, error
    else:
        return True, "Sessions dictionary is not empty."


def test_get_session() -> tuple:
    """
    Tests that a session is retrieved correctly.
    Testing to retrieve the right users (including the admin session)
    args:
        - None

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    db = Database("database/store_records.db")
    sessions = Sessions()
    sessions.add_new_session("test", db)
    session = sessions.get_session("test")

    if not isinstance(session, UserSession):
        error = f"Error in test_get_session: Session is not a UserSession object.\n  - Actual: {type(session)}"
        return False, error
    else:
        return True, "Session is a UserSession object."


def test_get_session_username() -> tuple:
    """
    Tests that a session's username is retrieved correctly.
    TEsting if the username is right (including admin)

    args:
        - None

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    db = Database("database/store_records.db")
    sessions = Sessions()
    sessions.add_new_session("test", db)
    session = sessions.get_session("test")

    if session.username != "test":
        error = f"Error in test_get_session_username: Session's username is incorrect.\n  - Expected: test\n  - Actual: {session.username}"
        return False, error
    else:
        return True, "Session's username is correct."


def test_get_session_db() -> tuple:
    """
    Tests that a session's database is retrieved correctly.

    args:
        - None

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    db = Database("database/store_records.db")
    sessions = Sessions()
    sessions.add_new_session("test", db)
    session = sessions.get_session("test")

    if session.db != db:
        error = f"Error in test_get_session_db: Session's database is incorrect.\n  - Expected: {db}\n  - Actual: {session.db}"
        return False, error
    else:
        return True, "Session's database is correct."
    
    '''
    -------------------------------------
    -----------REVIEW-TESTINGS-----------Zarin Khan---------------
    -------------------------------------
    '''
def test_review_submission() -> tuple:
        '''
        This is to review whether the database is obtaining the 
        review submission.

        Returns: 
        A tuple that contains a boolean and a string
        Boolean determines if the test passed or failed
        String will print out the test result
        '''
        db = Database("database/store_records.db") #Create database instance class

        #Get review length before addition
        all_reviews = db.get_all_reviews()
        length_before = len(all_reviews)

        #Review details that will be passed through the review submission by inserting it into table
        first_name = "Bumble"
        last_name = "Berry"
        email = "bberry@example.com"
        rev = "This is a test"

        db.insert_new_review(first_name, last_name, email, rev)

        #Get review length after addition 
        all_reviews = db.get_all_reviews()
        length_after = len(all_reviews)

        # Check if the review submission is successful
        if length_after > length_before :
            return True, "Review has been submitted successfully."
        else :
            return False, "Review submission failed."
            

