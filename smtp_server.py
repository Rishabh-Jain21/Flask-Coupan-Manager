import asyncio
from aiosmtpd.controller import Controller
from email.message import EmailMessage


class CustomSMTPServer:
    async def handle_DATA(self, server, session, envelope):
        message = EmailMessage()
        message["From"] = envelope.mail_from
        message["To"] = ", ".join(envelope.rcpt_tos)
        message.set_content(envelope.content.decode("utf-8"))

        # Simulate sending the email (replace this with your sending logic)
        print(f"Received message: {message.as_string()}")

        return "250 Message accepted for delivery"


async def start_server():
    controller = Controller(CustomSMTPServer(), hostname="localhost", port=1025)
    controller.start()

    print("SMTP server running...")

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(start_server())
