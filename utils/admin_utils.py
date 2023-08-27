"""
Утилиты для администратора.

Функции:
    create_test_dir:
        Создание директории теста для изображений.
    delete_test_dir:
        Удаление директории теста для изображений.
    get_next_number_image:
        Получение следующего номера изображения.
"""
import os
import shutil


def create_test_dir(test_id: int) -> None:
    """Создание директории теста для изображений."""
    if not os.path.exists("img"):
        os.mkdir("img")
    if not os.path.exists(f"img/test_{test_id}"):
        os.mkdir(f"img/test_{test_id}")


def delete_test_dir(test_id: int) -> None:
    """Удаление директории теста для изображений."""
    if os.path.exists(f"img/test_{test_id}"):
        shutil.rmtree(f"img/test_{test_id}")


def get_next_number_image(test_id: int) -> int:
    """Получение следующего номера изображения."""
    return len(os.listdir(f"img/test_{test_id}")) + 1
