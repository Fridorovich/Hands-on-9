# Hands-on-9 (event-driven system)

## Description

The system consists of four services:
1. REST API server for receiving messages from users.
2. Filter is a service for filtering messages by stop words.
3. SCREAMING service for converting text to uppercase.
4. Publish service for sending emails.

## Project structure

project/
│
├── app/
│ ├── init.py
│ └── app.py
│
├── filter_service/
│ ├── init.py
│ └── filter_service.py
│
├── screaming_service/
│ ├── init.py
│ └── screaming_service.py
│
├── publish_service/
│ ├── init.py
│ └── publish_service.py
│
├── .env
├── requirements.txt
└── README.md

## Installation and launch

1. **Install dependencies**:
- Install dependencies using pip:
```bash
pip install -r requirements.txt
```

2. **Configure the `.env` file**:
- Create a `.env` file in the root directory of the project and add environment variables to it:
     ```env
     SMTP_SERVER=mail.innopolis.ru
     SMTP_PORT=587
     SMTP_USER=your_email
     SMTP_PASSWORD=your_password
     RECIPIENT_EMAIL=recipient_email1,recipient_email2,...
     ```

3. **Launch RabbitMQ**:
   - Make sure that the RabbitMQ server is running and available on `localhost:15672'.

4. **Launch services**:
- Launch each service in a separate terminal:
     ```bash
     python app/app.py
     python filter_service/filter_service.py
     python screaming_service/screaming_service.py
     python publish_service/publish_service.py
     ```

5. **Sending a message via the REST API**:
- Use `Invoke-WebRequest` in PowerShell to send a POST request to `/send`:
     ```powershell
     Invoke-WebRequest -Uri http://localhost:5000/send -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"user": "test_user", "message": "Hello, world!"}'
     ```

## Checking the result

1. **Check RabbitMQ**:
- Make sure that the message is in the `message_queue` queue.
   - You can check it through the RabbitMQ web interface at `http://localhost:15672 `.

2. **Check the recipient's email**:
- Open the email `recipient_email`.
   - Find a new email with the subject "New Message".
   - Check the text of the letter:
     ```
     From the user: test_user
     Message: HELLO, WORLD!
     ```

## Event-driven system

In this variant, each service operates independently and interacts via RabbitMQ.

#### Advantages:
- Scalability and fault tolerance.

- Simplified processing of asynchronous events.


#### Disadvantages:
- A more complex architecture.

- Possible delays in message processing.
