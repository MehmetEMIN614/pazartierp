# contact/models/contact.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import PaymentTerm
from apps.core.models import BaseModel


class Contact(BaseModel):
    """
    A flexible contact model, suitable for customers, vendors, and internal contacts.
    """
    CONTACT_TYPE_CHOICES = [
        ('CUSTOMER', _('Customer')),
        ('VENDOR', _('Vendor')),
        ('INTERNAL', _('Internal')),
        ('OTHER', _('Other'))
    ]

    name = models.CharField(max_length=255)  # Legal name or company name
    display_name = models.CharField(max_length=255)  # Name to be displayed
    contact_type = models.CharField(max_length=20, choices=CONTACT_TYPE_CHOICES, default='CUSTOMER')

    # Contact Details
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)  # Added mobile field
    website = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)  # Allows longer addresses
    city = models.CharField(max_length=100, blank=True, null=True)  # Added city field
    state = models.CharField(max_length=100, blank=True, null=True)  # Added state field
    zip_code = models.CharField(max_length=20, blank=True, null=True)  # Added zip_code field
    country = models.CharField(max_length=100, blank=True, null=True)  # Added country field

    # Financial Details (Optional - adjust based on your needs)
    vat_number = models.CharField(max_length=50, blank=True, null=True)
    tax_exempt = models.BooleanField(default=False)  # Added tax exempt field
    payment_terms = models.ForeignKey(PaymentTerm, on_delete=models.SET_NULL, null=True,
                                      blank=True)  # Link to accounting payment terms

    # Other Details
    note = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name

    class Meta:
        unique_together = (('org', 'email'), ('org', 'vat_number'))  # enforce unique emails and VAT numbers per org
