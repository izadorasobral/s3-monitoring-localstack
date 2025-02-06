import os
import boto3
import time
import logging

# Configuração de logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuração do cliente S3 para LocalStack
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

BUCKET_NAME = "meu-bucket"
DIRECTORY_TO_WATCH = "./backup"

# Criar o bucket se ele não existir
try:
    s3.head_bucket(Bucket=BUCKET_NAME)
    logging.info(f"Bucket '{BUCKET_NAME}' já existe.")
except:
    s3.create_bucket(Bucket=BUCKET_NAME)
    logging.info(f"Bucket '{BUCKET_NAME}' criado.")

# Criar o diretório de backup se não existir
if not os.path.exists(DIRECTORY_TO_WATCH):
    os.makedirs(DIRECTORY_TO_WATCH)
    logging.info(f"Diretório '{DIRECTORY_TO_WATCH}' criado.")

# Função para fazer upload de arquivos
def upload_file(file_path):
    file_name = os.path.basename(file_path)
    try:
        s3.upload_file(file_path, BUCKET_NAME, file_name)
        logging.info(f"Arquivo '{file_name}' enviado para S3.")
    except Exception as e:
        logging.error(f"Erro ao enviar '{file_name}': {e}")

# Função para monitorar mudanças nos arquivos
def monitor_directory():
    seen_files = set(os.listdir(DIRECTORY_TO_WATCH))
    logging.info("Monitoramento iniciado...")

    while True:
        time.sleep(5)  # Verifica a cada 5 segundos
        current_files = set(os.listdir(DIRECTORY_TO_WATCH))

        new_files = current_files - seen_files
        for file in new_files:
            file_path = os.path.join(DIRECTORY_TO_WATCH, file)
            if os.path.isfile(file_path):
                upload_file(file_path)

        seen_files = current_files

if __name__ == "__main__":
    monitor_directory()
