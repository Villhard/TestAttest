MESSAGES = {
    "greeting admin": "Hello, admin!",
    "main menu": "Main menu",
    "tests": "List of tests",
    "users": "List of users",
    "test statistics": """\n\n<b>Statistics:</b>
                Success/Total: {statistics['completed']}/{statistics['total']}""",
    "users statistics": """<b>{user.name} {user.surname}</b>\n
                Tests passed: {results['completed']}/{results['total']}""",
    "add test": "Enter test name",
    "confirm delete test": "Are you sure you want to delete this test?",
    "delete test": "Test successfully deleted",
    "confirm publish test": "Are you sure you want to publish this test?",
    "publish test": "Test published",
}

BUTTONS = {
    "tests": "Tests",
    "users": "Users",
    "add test": "Add test",
    "back": "Back",
    "edit question": "Edit question",
    "delete question": "Delete question",
    "yes": "Yes",
    "no": "No",
}

LOGS = {
    # INFO
    "starting bot": "Starting bot",
    "stopping bot": "Stopping bot",
    # DEBUG
    "greeting admin": "Admin: {admin_id} started bot",
    "main menu": "Admin: {admin_id} got to main menu",
    "tests": "Admin: {admin_id} got to tests menu",
    "users": "Admin: {admin_id} got to users menu",
    "test": "Admin: {admin_id} got to test {test_id}",
    "question": "Admin: {admin_id} got to question {question_id}",
    "user": "Admin: {admin_id} got to user {user_id}",
    "add test": "Admin: {admin_id} started creating new test",
    "confirm delete test": "Admin: {admin_id} asked to delete test {test_id}",
    "delete test": "Admin: {admin_id} deleted test {test_id}",
    "confirm publish test": "Admin: {admin_id} asked to publish test {test_id}",
    "publish test": "Admin: {admin_id} published test {test_id}",
}
