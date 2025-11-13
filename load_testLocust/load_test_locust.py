# load_test_locust.py 50 видео одновременно
from locust import HttpUser, task, between, events
import time
import random
import os
import logging
from datetime import datetime

# === НАСТРОЙКИ ===
CANDIDATE_ID = "64cd9d71-779a-4918-884a-805b89beb140"
CANDIDATE_INTERVIEW_ID = "3236337e-f7b7-4da6-ad1a-9218eb77b24e"
VIDEO_FILENAME = "C:/Users/Sergio/Desktop/Video/file.mp4"      # "file.mp4"

# Создаём папку для логов
log_dir = "locust_logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Настраиваем логгер
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("VideoLoadTest")

class VideoUploadUser(HttpUser):
    wait_time = between(0.1, 0.3)

    @task
    def upload_video(self):
        # media_name = f"question_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
        media_name = f"test{random.randint(1, 10000)}_1"
        if not os.path.exists(VIDEO_FILENAME):
            logger.error(f"Файл не найден: {VIDEO_FILENAME}")
            return

        try:
            with open(VIDEO_FILENAME, "rb") as f:
                files = {"media_data": (VIDEO_FILENAME, f, "video/mp4")}
                data = {
                    "candidate_interview_id": CANDIDATE_INTERVIEW_ID,
                    "media_name": media_name
                }
                with self.client.post(
                        "/api/candidates/current_interview/video/",
                        data=data,
                        files=files,
                        name="POST /video/",
                        catch_response=True
                ) as response:
                    try:
                        body = response.json()
                    except Exception:
                        body = response.text

                    if response.status_code == 202:
                        logger.info(
                            f"✅ УСПЕХ | media_name={media_name} | "
                            f"status={response.status_code} | body={body}"
                        )
                    else:
                        logger.error(
                            f"❌ ОШИБКА | media_name={media_name} | "
                            f"status={response.status_code} | body={body}"
                        )
                        response.failure(f"Unexpected status {response.status_code}")

        except Exception as e:
            logger.exception(f"💥 ИСКЛЮЧЕНИЕ | media_name={media_name} | ошибка={e}")

# Описание теста (для документации)
"""
Нагрузочный тест эндпоинта загрузки видео:
- Цель: проверить устойчивость /api/candidates/current_interview/video/ под нагрузкой.
- Метод: 20–100 параллельных пользователей, каждый отправляет видео с уникальным media_name.
- Особенность: используется один candidate_interview_id, но разные media_name → изоляция данных.
- Ожидаемый результат: 100% ответов 202 Accepted, отсутствие ошибок, стабильность CPU/памяти.
"""

# #locust -f load_test_locust.py --host https://bh75.brainhire.tech



# # load_test_locust.py 50 видео одновременно    200 25 300 30
# from locust import HttpUser, task, between, events
# import time
# import random
# import os
# import logging
# from datetime import datetime
#
# # === НАСТРОЙКИ ===
# CANDIDATE_ID = "3236337e-f7b7-4da6-ad1a-9218eb77b24e"
# VIDEO_FILENAME = "file.mp4"
#
# # Создаём папку для логов
# log_dir = "locust_logs"
# os.makedirs(log_dir, exist_ok=True)
# log_path = os.path.join(log_dir, f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
#
# # Настраиваем логгер
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(message)s",
#     handlers=[
#         logging.FileHandler(log_path, encoding='utf-8'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger("VideoLoadTest")
#
# class VideoUploadUser(HttpUser):
#     wait_time = between(0.1, 0.3)
#
#     @task
#     def upload_video(self):
#         media_name = f"q_load_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
#
#         if not os.path.exists(VIDEO_FILENAME):
#             logger.error(f"Файл не найден: {VIDEO_FILENAME}")
#             return
#
#         try:
#             with open(VIDEO_FILENAME, "rb") as f:
#                 files = {"media_data": (VIDEO_FILENAME, f, "video/mp4")}
#                 data = {
#                     "candidate_interview_id": CANDIDATE_ID,
#                     "media_name": media_name
#                 }
#                 with self.client.post(
#                     "/api/candidates/current_interview/video/",
#                     data=data,
#                     files=files,
#                     name="POST /video/",
#                     catch_response=True
#                 ) as response:
#                     if response.status_code == 202:
#                         logger.info(f"✅ УСПЕХ | media_name={media_name} | task_id={response.json().get('task_id', 'N/A')}")
#                     else:
#                         logger.error(f"❌ ОШИБКА | media_name={media_name} | статус={response.status_code}")
#
#         except Exception as e:
#             logger.exception(f"💥 ИСКЛЮЧЕНИЕ | media_name={media_name} | ошибка={e}")
#
# # Описание теста (для документации)
# """
# Нагрузочный тест эндпоинта загрузки видео:
# - Цель: проверить устойчивость /api/candidates/current_interview/video/ под нагрузкой.
# - Метод: 20–100 параллельных пользователей, каждый отправляет видео с уникальным media_name.
# - Особенность: используется один candidate_interview_id, но разные media_name → изоляция данных.
# - Ожидаемый результат: 100% ответов 202 Accepted, отсутствие ошибок, стабильность CPU/памяти.
# """

# locust -f load_test_locust.py --host https://bh75.brainhire.tech



