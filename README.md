# TeleThrive

TeleThrive is a telemedicine platform that offers virtual therapy and psychiatry services, connecting users with licensed therapists and psychiatrists for remote mental health support.

## Features

- User registration and authentication
- Appointment scheduling for therapy and psychiatry sessions
- Integration with Google Meets API for video conferencing
- File storage for session notes and user uploads
- Planned integration with MPesa for payment system (future feature)

## Installation

1. Clone the repository:

git clone https://github.com/ynot93/tele-thrive.git


2. Navigate to the project directory:

cd tele-thrive


3. Install dependencies:

pip install -r requirements.txt


4. Set up environment variables:

   - Create a `.env` file in the root directory
   - Add the following variables:

FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url


5. Run the application:

flask run


6. Access the application in your web browser at `http://localhost:5000`

## Usage

- Register a new account or log in with existing credentials
- Schedule therapy or psychiatry appointments
- Join scheduled appointments using the provided Google Meet link
- Upload session notes or other relevant files

## Contributing

Contributions are welcome! If you'd like to contribute to TeleThrive, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

