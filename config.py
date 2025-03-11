import os

SECRET_KEY = 'CHAVE_SECRETA_SECRETISSIMA'
DEBUG = True

# Conexão do banco
DB_HOST = 'localhost'
DB_NAME = r'C:\Users\Aluno\Downloads\doe_ai\BANCO.FDB'
DB_USER = 'sysdba'
DB_PASSWORD = 'sysdba'

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ID_USUARIO = 0