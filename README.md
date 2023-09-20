# TestAttest is telegram-bot test attestation service

## Admin Handlers

The `admin_handlers.py` module contains command and callback handlers for the bot administrator.

### State Machines

#### FSMCreateTest

The state class for creating a test.

- `title`: Input for test title
- `description`: Input for test description

#### FSMCreateQuestions

The state class for creating questions.

- `text`: Input for question text
- `answers`: Input for answer text
- `image`: Input for question image

### Navigation

- `cmd_start`: Admin greeting
- `cmd_help`: Admin help
- `call_main_menu`: Main menu
- `call_tests`: View all tests
- `call_test_by_id`: View test
- `call_question_by_id`: View question
- `call_users`: View users
- `call_user_by_id`: View user
- `call_result_by_id`: View result

### Test and Question Creation, Editing, and Deletion

- `call_add_test`: Create test
- `call_confirm_delete_test`: Confirm test deletion
- `call_delete_test`: Delete test
- `call_confirm_publish_test`: Confirm test publication
- `call_publish_test`: Publish test
- `call_edit_correct_answer`: Edit correct answer
- `call_delete_question`: Delete question

### Test Creation Process

- `process_input_title`: Create test. Get test title
- `process_input_description`: Create test. Get test description

### Question Creation Process

- `call_add_question`: Create question
- `process_input_question_text`: Create question. Get question text
- `process_input_answers_text`: Create question. Get answer text
- `process_input_correct_answer`: Create question. Get correct answer
- `process_input_image_question`: Create question. Get question image
- `process_skip_image_question`: Create question. Skip question image

___

## User Handlers

The `user_handlers.py` module contains command and callback handlers for the bot users.

### State Machines

#### FSMUserInputName

The state class for user's name and surname input.

- `fullname`: Input for user's full name

#### FSMTesting

The state class for test taking.

- `testing`: Test taking state

### Navigation

- `cmd_start`: User greeting or request for name input
- `cmd_help`: User help
- `call_main_menu`: Go to the main menu
- `call_tests`: Go to the test list
- `call_test`: Go to a specific test

### User Creation Process

- `process_input_name`: Get user's name and surname
- `process_incorrect_input_name`: Handle incorrect name input

### Test Taking Process

- `call_start_test`: Start the test
- `call_answering`: Process test questions and answers