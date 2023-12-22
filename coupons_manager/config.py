class Config:
    SECRET_KEY = "575a581e34d929fc5215c09a934d9a32"  # For dev it can be hardcoded # for prod get it from env variable
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    # MAIL_USE_TLS = True
    # MAIL_USEERNAME = os.environ.get("USER_EMAIL")
    # MAIL_PASSWORD = os.environ.get("EMAIL_PASS")

