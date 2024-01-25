from openai import OpenAI
import time

client = OpenAI(api_key="")

# Step 1: Upload the file and get the response
file_response = client.files.create(
  file=open("EmployerList.xlsx", "rb"),
  purpose="assistants"
)
file_id = file_response.id

# Step 2: Function to check file upload status
def check_file_upload_status(client, file_id):
    while True:
        file_status = client.files.retrieve(file_id=file_id)
        if file_status.status == 'processed':
            print("File upload completed")
            break
        else:
            print("File is still uploading")
            print(file_status.status)
            time.sleep(5)  # Wait for 5 seconds before checking again

# Step 3: Call the function to check the file status
check_file_upload_status(client, file_id)
print(file_response)

# Step 4: Continue with the rest of the program once the file upload is complete
# ... rest of your code ...

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="The user will refer to an uploaded file. This is the file named EmployerList.xlsx",
    tools=[{"type": "code_interpreter"},{"type": "retrieval"}],
    model="gpt-4-1106-preview",
    file_ids = [file_id]
)

thread = client.beta.threads.create()
# print(thread)

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Can you tell me what the column names are of the uploaded file?"
)
# print(message)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  instructions="Please address the user as Jane Doe. The user has a premium account."
)

run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)
# print(run)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

# Function to check the status of the run
def check_run_status(client, thread_id, run_id):
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run_status.status == 'completed':
            print("Run completed")
            break
        elif run_status.status == 'failed':
            print("Run failed")
            break
        else:
            print("Run is still in progress")
            time.sleep(10)  # Wait for 10 seconds before checking again

# Call the function to check the run status
check_run_status(client, thread.id, run.id)

# Once the run is completed, retrieve the messages
messages = client.beta.threads.messages.list(thread_id=thread.id)

# Print the messages
for message in messages.data:
    if hasattr(message.content, 'text') and hasattr(message.content.text, 'value'):
        message_text = message.content.text.value
    else:
        # Convert to string using repr and then replace escaped characters
        message_text = repr(message.content)
        message_text = message_text.replace('\\n', '\n').replace('\\t', '\t')  # Add more replacements if needed

    print(f"{message.role.title()}: {message_text}")
