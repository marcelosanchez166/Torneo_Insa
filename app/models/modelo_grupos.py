from app.models.entities.grupos import Grupos
from flask import flash, render_template
from app.database.db import get_connection

# class ModeloGrupos:
#     @classmethod
#     def get_grupos(cls):
#         try:
#             connection = get_connection()
#             cursor = connection.cursor()
#             cursor.execute('''