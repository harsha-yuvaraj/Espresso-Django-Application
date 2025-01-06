from django.core.mail.backends.smtp import EmailBackend
import ssl
import certifi

class CustomEmailBackend(EmailBackend):
    def _get_connection(self):
        self.connection = super()._get_connection()
        self.connection.starttls(context=self._get_ssl_context())
        return self.connection

    def _get_ssl_context(self):
        context = ssl.create_default_context()
        context.load_verify_locations(certifi.where())
        return context
