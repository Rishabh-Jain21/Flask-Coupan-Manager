
# Flask-Coupon-Manager

A flask based Application to store coupons




## Features

- User Registration
- User Login
- Password Reset
- Cross platform
- Email Send


## Tech Stack

**Server:** Flask (Python)

**Database:** SqliteDb


## Environment Variables

To run this project, you will can set environment variables for variables in config.py or hardcode them accordingly.




## Run Locally

1.Clone the project

```bash
  git clone https://github.com/Rishabh-Jain21/Flask-Coupon-Manager
```

2.Go to the project directory

```bash
  cd Flask-Coupon-Manager
```

3.Create a virtual environment
This will create a virtual environment named **venv**
```bash
  python -m venv venv
```
4.Activate the virtual environment depending on operating System

a) For Windows
```bash
  .\venv\Scripts\activate
```
b) For Unix
```bash
source ./venv/bin/activate
```
5.Install required dependencies
```bash
  pip install -r requirments.txt
```
6.Initialise the database
```bash
  python -m flask --app run db upgrade
```
7.Start development server
```bash
  python -m flask --app run
```

## Password Reset

A reset url will be send to the user email.
For localhost testing a local SMPT server is created(smtp_server.py)
which simulates email send and receive.
Actual email is not being sent to the recepient
For production add the required smpt details.

For checking reset password locally

    1. Run smtp_server.py script in another terminal.
    2. Go to reset password page.
    3. Enter the email to reset password for.
    4. Check the console of locally run smtp server.
    5. Use the link printed in console to change password.