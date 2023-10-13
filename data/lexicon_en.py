MESSAGES = {
    "greeting admin": "Hello, admin!",
    "main menu": "Main menu",
    "tests": "List of tests",
    "users": "List of users",
    "test statistics": (
        """\n\n<b>Statistics:</b>
        Success/Total: {statistics['completed']}/{statistics['total']}"""
    ),
    "users statistics": (
        """<b>{user.name} {user.surname}</b>\n
        Tests passed: {results['completed']}/{results['total']}"""
    ),
    "add test": "Enter test name",
    "add test description": "Enter test description",
    "confirm delete test": "Are you sure you want to delete this test?",
    "delete test": "Test successfully deleted",
    "confirm publish test": "Are you sure you want to publish this test?",
    "publish test": "Test published",
    "delete question": "Question successfully deleted",
    "success create test": "Test successfully created!",
    "add question": "Enter question text",
    "add question answer 1": "Enter answer text 1",
    "add-question answer n": "Enter answer text {n}",
    "confirm correct answer": "Select correct answer",
    "add question image": "Upload image or skip it",
    "question created": "Question successfully created",
    "greeting user": "Hello, {name}!",
    "greeting stranger": (
        """Welcome to the bot for testing!
        Enter your name and surname"""
    )
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
    "skip": "Skip",
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
    "edit correct answer": "Admin: {admin_id} edited correct answer on question {question_id}",
    "delete question": "Admin: {admin_id} deleted question {question_id}",
    "add test title": "Admin: {admin_id} is creating test {title}",
    "add test description": "Admin: {admin_id} is creating description {description} for test {title}",
    "add question": "Admin: {admin_id} started creating new question in test {test_id}",
}
