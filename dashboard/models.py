from django.db import models


class IncomingMessage(models.Model):
    """
    Store messages submitted through the public contact form.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.subject} - {self.name}"
