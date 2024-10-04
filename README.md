# Text Moderation Microservice

## Description

This microservice performs text moderation, checking for prohibited content. It uses a pre-trained AI model for effective moderation. The service is written in Python and uses modern technologies for ease of use and deployment.

## Installation and Setup

To work with the microservice, it is recommended to create a virtual environment to avoid dependency conflicts. Follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/naumovmag/Moderator.git
   cd text-moderation-service
   ```

2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   ```
   For Linux/MacOS
   ```sh
   source venv/bin/activate
   ```
   For Windows
   ```sh
   venv\Scriptsctivate
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running Locally

After installing the dependencies, you can run the microservice locally:

```sh
python app.py
```

## Using Docker Compose

For convenient deployment, you can use Docker Compose.

1. First, make sure you have Docker and Docker Compose installed.

2. Build the Docker image and start the container:
   ```sh
   docker-compose up --build
   ```

3. After successful startup, the microservice will be available at: `http://localhost:5050`

## API Request Examples

The microservice provides an API for text moderation. Example request to check text using cURL:

```sh
curl -X POST http://localhost:5050/moderate   -H "Content-Type: application/json"   -d '{"text": "Text for moderation"}'
```

The response will contain the result of text moderation.

## License

This project is distributed under the MIT license. Details can be found in the LICENSE file.
