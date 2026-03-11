import os
import json
import zipfile
import pika
import traceback
import cv2
import tempfile
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.files import File
from io import BytesIO
from videos.models import Video
import shutil


def process_video(channel, method, properties, body):

    temp_dir = None
    try:
        data = json.loads(body)
        video = Video.objects.create(name=data["name"], video_file=data["video_file"])

        # Criar um diretório temporário para processamento
        temp_dir = tempfile.mkdtemp()
        print(f"Diretório temporário criado: {temp_dir}")

        # CORREÇÃO 1: Baixar o vídeo do MinIO para o diretório temporário
        video_temp_path = os.path.join(temp_dir, f"original_{video.id}.mp4")

        # Abrir o arquivo do storage e salvar localmente
        with default_storage.open(video.video_file.name, 'rb') as remote_file:
            with open(video_temp_path, 'wb') as local_file:
                shutil.copyfileobj(remote_file, local_file)

        print(f"Vídeo baixado para: {video_temp_path}")

        # Verificar se o arquivo foi baixado corretamente
        if not os.path.exists(video_temp_path):
            raise Exception(f"Arquivo não foi baixado corretamente: {video_temp_path}")

        file_size = os.path.getsize(video_temp_path)
        print(f"Tamanho do arquivo: {file_size} bytes")

        if file_size == 0:
            raise Exception("Arquivo de vídeo está vazio")

        # Processar o vídeo localmente
        output_folder = os.path.join(temp_dir, 'extracted_frames')
        os.makedirs(output_folder, exist_ok=True)

        cap = cv2.VideoCapture(video_temp_path)

        if not cap.isOpened():
            raise Exception(f"Não foi possível abrir o vídeo com OpenCV: {video_temp_path}")

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_filename = os.path.join(output_folder, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            frame_count += 1

        cap.release()

        print(f"Total de frames extraídos: {frame_count}")

        if frame_count == 0:
            raise Exception("Nenhum frame foi extraído do vídeo")

        # CORREÇÃO 2: Criar o ZIP com os frames
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            files_added = 0
            for root, _, files in os.walk(output_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Nome do arquivo dentro do ZIP (sem o caminho completo)
                    arcname = os.path.relpath(file_path, output_folder)
                    zip_file.write(file_path, arcname)
                    files_added += 1

            print(f"Total de arquivos adicionados ao ZIP: {files_added}")

        # CORREÇÃO 3: Salvar o ZIP no MinIO via Django storage
        zip_buffer.seek(0)

        # Nome do arquivo ZIP no storage
        zip_filename = f"processed_videos/processed_{video.id}.zip"

        # Salvar diretamente no storage (MinIO)
        default_storage.save(zip_filename, ContentFile(zip_buffer.read()))

        # Atualizar o modelo com o caminho do arquivo ZIP
        video.zip_video_file.name = zip_filename
        video.save()

        print(f"ZIP salvo no MinIO: {zip_filename}")

        # Publicar mensagem de sucesso
        channel.basic_publish(
            exchange="",
            routing_key="video_processed",
            body=json.dumps(
                {
                    "video_id": str(video.id),
                    "video_name": video.name,
                    "status": "success",
                    "email": data.get("email", "admin@admin.com"),
                }
            ),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    except Exception as e:
        print(f"Error processing video: {e}")
        traceback.print_exc()

        # Tentar publicar mensagem de erro (data pode não existir se o erro for na criação do vídeo)
        video_name = data.get("name", "") if 'data' in locals() else ""
        email = data.get("email", "admin@admin.com") if 'data' in locals() else "admin@admin.com"

        channel.basic_publish(
            exchange="",
            routing_key="video_processed",
            body=json.dumps(
                {
                    "video_id": None,
                    "video_name": video_name,
                    "status": "error",
                    "email": email,
                }
            ),
            properties=pika.BasicProperties(delivery_mode=2),
        )

    finally:
        # CORREÇÃO 4: Limpar arquivos temporários
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"Diretório temporário removido: {temp_dir}")
