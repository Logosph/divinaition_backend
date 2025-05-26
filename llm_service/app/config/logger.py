import logging
import sys

# Настройка логгера
logger = logging.getLogger("llm_service")
logger.setLevel(logging.INFO)

# Создаем обработчик для вывода в консоль
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)

# Создаем форматтер
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(handler) 