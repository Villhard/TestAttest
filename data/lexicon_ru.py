MESSAGES = {
    "greeting admin": "Привет, админ!",
    "main menu": "Главное меню",
    "tests": "Список тестов",
    "users": "Список пользователей",
    "test statistics": """\n\n<b>Статистика:</b>
                Успех/Всего: {statistics['completed']}/{statistics['total']}""",
    "users statistics": """<b>{user.name} {user.surname}</b>\n
                Тестов пройдено: {results['completed']}/{results['total']}""",
    "add test": "Введите название теста",
}

BUTTONS = {
    "tests": "Тесты",
    "users": "Пользователи",
    "add test": "Добавить тест",
    "back": "Назад",
    "edit question": "Редактировать вопрос",
    "delete question": "Удалить вопрос",
}

LOGS = {
    # INFO
    "starting bot": "Запуск бота",
    "stopping bot": "Остановка бота",
    # DEBUG
    "greeting admin": "Админ: {admin_id} запустил бота",
    "main menu": "Админ: {admin_id} перешел в главное меню",
    "tests": "Админ: {admin_id} перешел в меню тестов",
    "users": "Админ: {admin_id} перешел в меню пользователей",
    "test": "Админ: {admin_id} перешел в тест {test_id}",
    "question": "Админ: {admin_id} перешел в вопрос {question_id}",
    "user": "Админ: {admin_id} перешел в пользователь {user_id}",
    "add test": "Админ: {admin_id} начал создание нового теста",
}
