from core.session import Sessions, UserSession
from database.db import Database
from flask import Flask, render_template_string
from flask.testing import FlaskClient
from unittest.mock import patch
from app import app


def test_place_order_total_price() -> tuple:
    """
    Hsomot Siu
    Tests the total price calculation and rendering in the order confirmation page.

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """
    with app.test_request_context():
        with app.test_client() as client:
            mock_bakery_items = {
                'cakes': [{'name': 'Fruit Sponge Cake', 'price': 30.0}],
            }

            expected_subtotal = mock_bakery_items['cakes'][0]['price'] * 1  # Assuming quantity is 1
            expected_tax = round(0.02 * expected_subtotal, 2)
            expected_total_price = expected_subtotal + expected_tax

            expected_subtotal_string = f"${expected_subtotal:.1f}"

            response = client.post('/place_order', data={
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'phone': '123-456-7890',
                'pickUpDate': '2023-08-01',
                'customizationNote': 'No customization',
                'selectBakery1': 'Fruit Sponge Cake',
                'quantity1': '1',
            })

            assert response.status_code == 200

            response_data = response.get_data(as_text=True).strip()

            print("Response Data:")
            print(response_data)

            error_report = []

            if expected_subtotal_string not in response_data:
                error_report.append(f"Expected subtotal string not found in response data.\n  - Expected: {expected_subtotal_string}")
            if f"${expected_tax:.1f}" not in response_data:
                error_report.append(f"Expected tax not found in response data.\n  - Expected: {f'${expected_tax:.1f}'}")
            if f"${expected_total_price:.1f}" not in response_data:
                error_report.append(f"Expected total price not found in response data.\n  - Expected: {f'${expected_total_price:.1}'}")

            if error_report:
                error_message = "\n".join(error_report)
                return False, error_message
            else:
                return True, "Total price calculation and rendering test passed."

def test_init_sessions() -> tuple:
    """
    Tests that the Sessions class is initialized correctly.

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
            

