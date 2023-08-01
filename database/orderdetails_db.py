from core.utils import dict_factory, calculate_cost
import datetime as dt

class OrderDetailsDB: 

    def get_sale_detail_by_id(self, dbconnection, sale_id: int):
            """
            Gets the sales for a sale from the database.

            args:
                - sale_id: The id of the sale whose information to get.

            returns:
                - The sales records for the sale with the given id.
            """
            dbconnection.cursor.execute(
                "SELECT a.username, a.item_id, a.quantity, a.cost, b.item_name FROM sales a JOIN inventory b ON a.item_id = b.id WHERE sale_id = ?", (sale_id,))
            return dbconnection.cursor.fetchone()