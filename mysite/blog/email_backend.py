"""
Custom email backend to handle SMTP compatibility issues
"""
import smtplib
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings


class FixedSMTPBackend(EmailBackend):
    """
    A custom SMTP backend that fixes the starttls() compatibility issue
    """
    
    def open(self):
        """
        Ensure an open connection to the email server. Return whether or not a
        new connection was required (True or False) or None if an exception
        occurred.
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False

        try:
            self.connection = self.connection_class(self.host, self.port)
            
            # TLS/SSL are mutually exclusive, so only attempt TLS over
            # non-secure connections.
            if not self.use_ssl and self.use_tls:
                # Fixed version - call starttls without extra arguments
                self.connection.starttls()
                
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except Exception as e:
            if not self.fail_silently:
                raise
            return False
