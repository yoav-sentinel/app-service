# Project Title

app-service

## Introduction

Flask app designed to help developers create and manage their applications. The app allows developers to upload files
for their applications, with built-in validation to ensure that the uploaded files are valid zip archives containing
only `.zip` files with files with the `.doesntmakesense` extension. This streamlines the application creation process and ensures
consistency and compliance with the specified file format requirements.

## Features

This app-service project provides the following main features:

### App Feature

Manage data related to the app, including:

- **Endpoint to create an app**: Create a new app with data such as `developerId`, `AppName`
- **Endpoint to get a list of available apps**: Retrieve a list of all available apps.
- **Endpoint to get app info by app ID**: Fetch the app information by providing its ID.
- **Endpoint to delete an app by app ID**: Delete an existing app and its uploaded files.
- **Endpoint to upload files to an app by app ID**: Streams a file and upload it to a designated upload folder.

### Review Feature

Manage automatic review of the app files and decide whether to reject the files or approve them. Triggers asynchronously
when calling `app/app_id/upload` API endpoint.

### Storage Feature

The Storage feature save and delete app files to/from storage:

- **Save app files**: Called by Review Feature when app files approved.
- **Delete app files**: Called by `DELETE app/app_id` API endpoint.

## Installation

Follow these steps to install and set up the app-service project:

### Prerequisites

Ensure that you have the following software installed on your system:

- Python 3.6 or later
- Redis server
- PostgreSQL server

### Steps

1. Clone the repository to your local machine:

```
git clone https://github.com/yourusername/app-service.git`
```

2. Change to the project directory:

```
cd app-service
```

3. Create a virtual environment and activate it:

```
python3 -m venv venv
source venv/bin/activate
```

4. Install the required dependencies:

```
pip install -r requirements.txt
```

5. Set up your PostgreSQL server.
6. Modify The following parameters in `db_setup.py`:

```
SUPER_USER_PASSWORD # required
DB_HOST # required if not running on localhost
DB_PORT # required if not running on default port
USER_NAME # optional
USER_PASSWORD # required
```

7. Run `db_setup.py` to create designated database and user:

```
python db_setup.py
```

8. Set up your Redis server.
9. Modify the following parameters in `config.py`:

```
CELERY_BROKER_URL # required if not using default redis conifguration
CELERY_RESULT_BACKEND # required if not using default redis conifguration
DATABASE_URL # required if you didn't run db_setup.py
```

10. Run `run.py` to start the application:

```
python run.py
```

## Testing
All tests are located in `tests` directory. 

To run all tests:
```
python run_test.py
```

## API Examples
Assuming flask is running with default port 5000 on localhost
### Create Application
```POST http://localhost:5000/app```
#### Payload
```{"developer_id": 123456, "app_name": "my app"}```
#### Response
```
{
    "app_id": 4217,
    "app_name": "my app",
    "app_status": "not_uploaded",
    "created_at": "2023-05-08T12:29:14.977879",
    "developer_id": 123456,
    "updated_at": "2023-05-08T12:29:14.977879"
}
```

### Get Application by ID
```GET http://localhost:5000/app/4217```
#### Response
```
{
    "app_id": 4217,
    "app_name": "my app",
    "app_status": "not_uploaded",
    "created_at": "2023-05-08T12:29:14.977879",
    "developer_id": 123456,
    "updated_at": "2023-05-08T12:29:14.977879"
}
```

### Get Applications
```GET http://localhost:5000/app?app_status=not_uploaded&developer_id=123456```
#### Response
```
{
    "apps": [
        {
            "app_id": 4217,
            "app_name": "my app",
            "app_status": "not_uploaded",
            "created_at": "2023-05-08T12:29:14.977879",
            "developer_id": 123456,
            "updated_at": "2023-05-08T12:29:14.977879"
        }
    ]
}
```

### Upload File
```POST http://localhost:5000/app/4217/upload```
#### Request Body
```
Content-Disposition: form-data; name="file"; filename="example.zip"
Content-Type: application/zip
```
#### Response
```
{
    "result": "File upload successful. Validation in progress.",
    "task_id": "7f344aa5-49ee-430f-9d41-7cd3d86d7dd5"
}
```

### Delete Application
```DELETE http://localhost:5000/app/4217```

#### Response
```
{
    "result": "Application 4217 deletion successful."
}
```
