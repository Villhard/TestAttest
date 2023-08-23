"""Утилиты для администратора."""
import os
import shutil


def create_test_dir(test_id: int) -> None:
    """Создание директории теста для изображений."""
    if not os.path.exists("img"):
        os.mkdir("img")
    os.mkdir(f"img/test_{test_id}")


def delete_test_dir(test_id: int) -> None:
    """Удаление директории теста для изображений."""
    if os.path.exists(f"img/test_{test_id}"):
        shutil.rmtree(f"img/test_{test_id}")


def check_exists_image(test_id: int) -> bool:
    """Проверка наличия изображений в тесте."""
    return os.path.exists(f"img/test_{test_id}/default.jpg")


def get_count_images(test_id: int) -> int:
    """Получение количества изображений в директории теста."""
    return len(os.listdir(f"img/test_{test_id}"))
