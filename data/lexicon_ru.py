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
    "confirm delete test": "Вы уверены, что хотите удалить этот тест?",
    "delete test": "Тест успешно удален",
    "confirm publish test": "Вы уверены, что хотите опубликовать этот тест?",
    "publish test": "Тест опубликован",
}

BUTTONS = {
    "tests": "Тесты",
    "users": "Пользователи",
    "add test": "Добавить тест",
    "back": "Назад",
    "edit question": "Редактировать вопрос",
    "delete question": "Удалить вопрос",
    "yes": "Да",
    "no": "Нет",
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
    "confirm delete test": "Админ: {admin_id} запросил удалить этот тест {test_id}",
    "delete test": "Админ: {admin_id} удалил тест {test_id}",
    "confirm publish test": "Админ: {admin_id} запросил опубликовать этот тест {test_id}",
    "publish test": "Админ: {admin_id} опубликовал тест {test_id}",
}
