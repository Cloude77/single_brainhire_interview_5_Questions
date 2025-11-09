import requests
import threading
import time
import logging
import os
from datetime import datetime

# === КОНФИГУРАЦИЯ ===
CANDIDATE_IDS = [
    "64cd9d71-779a-4918-884a-805b89beb140",
    "62397b15-b887-4cc2-bf8f-16a9e3d8abbf",
    "184dab35-2a9d-4107-ad6e-bfbb24c0b296",
    "32d16e4f-742a-4a79-821b-40b8aada8786",
]

VIDEO_PATH = "C:/Users/Sergio/Desktop/Video/file.mp4"
URL = "https://bh75.brainhire.tech/api/candidates/current_interview/video/"
TIMEOUT = 30  # секунд

# === НАСТРОЙКА ЛОГИРОВАНИЯ ===
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_filename = os.path.join(
    log_dir,
    f"load_test_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()  # дублирует в консоль
    ]
)
logger = logging.getLogger("VideoLoadTest")

# === ФУНКЦИЯ ОТПРАВКИ ===
def upload_video(candidate_id: str, index: int):
    logger.info(f"[Кандидат {index}] Начало отправки для candidate_interview_id={candidate_id}")
    try:
        if not os.path.exists(VIDEO_PATH):
            raise FileNotFoundError(f"Видео не найдено: {VIDEO_PATH}")

        with open(VIDEO_PATH, "rb") as f:
            files = {"media_data": (f"video_{index}.mp4", f, "video/mp4")}
            data = {
                "candidate_interview_id": candidate_id,
                "media_name": f"question_load_test_{index}"
            }

            start_time = time.time()
            response = requests.post(URL, data=data, files=files, timeout=TIMEOUT)
            elapsed = time.time() - start_time

            try:
                response_data = response.json()
            except Exception as e:
                response_data = {"raw_response": response.text[:200]}

            if response.status_code == 202:
                logger.info(
                    f"[Кандидат {index}] УСПЕХ | Статус: {response.status_code} | "
                    f"Время: {elapsed:.2f}с | task_id: {response_data.get('task_id', 'N/A')}"
                )
            else:
                logger.error(
                    f"[Кандидат {index}] ОШИБКА | Статус: {response.status_code} | "
                    f"Время: {elapsed:.2f}с | Ответ: {response_data}"
                )

    except FileNotFoundError as e:
        logger.critical(f"[Кандидат {index}] ФАТАЛЬНАЯ ОШИБКА: {e}")
    except requests.exceptions.Timeout:
        logger.error(f"[Кандидат {index}] ТАЙМАУТ — запрос дольше {TIMEOUT} секунд")
    except requests.exceptions.RequestException as e:
        logger.error(f"[Кандидат {index}] СЕТЕВАЯ ОШИБКА: {e}")
    except Exception as e:
        logger.exception(f"[Кандидат {index}] НЕОЖИДАННОЕ ИСКЛЮЧЕНИЕ: {e}")

# === ЗАПУСК ===
if __name__ == "__main__":
    logger.info("🚀 Старт нагрузочного теста: 4 параллельные загрузки видео")
    logger.info(f"Используемый файл: {VIDEO_PATH}")
    logger.info(f"Эндпоинт: {URL}")

    threads = []
    start_time = time.time()

    for i, cid in enumerate(CANDIDATE_IDS, 1):
        t = threading.Thread(target=upload_video, args=(cid, i), name=f"Candidate-{i}")
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_time = time.time() - start_time
    logger.info(f"✅ Тест завершён. Общее время: {total_time:.2f} секунд")
    logger.info(f"Подробный лог сохранён в: {log_filename}")