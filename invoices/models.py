from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils.timezone import now


class Invoice(models.Model):
    invoice_number = models.CharField(_("Numéro de facture"), max_length=50)
    invoice_symbol = models.CharField(_("Série de facture"), max_length=20)
    issued_date = models.DateField(_("Date d'émission"))
    payment_method = models.CharField(_("Méthode de paiement"), max_length=100)
    currency = models.CharField(_("Devise"), max_length=10, default="VND")
    exchange_rate = models.DecimalField(_("Taux de change"), max_digits=10, decimal_places=2, default=1)

    seller_name = models.CharField(_("Nom du vendeur"), max_length=255)
    seller_tax_code = models.CharField(_("Numéro fiscal du vendeur"), max_length=20)
    seller_address = models.TextField(_("Adresse du vendeur"))

    buyer_name = models.CharField(_("Nom de l'acheteur"), max_length=255)
    buyer_tax_code = models.CharField(_("Numéro fiscal de l'acheteur"), max_length=20)
    buyer_address = models.TextField(_("Adresse de l'acheteur"))

    total_before_tax = models.DecimalField(_("Total HT"), max_digits=15, decimal_places=2)
    total_tax = models.DecimalField(_("Montant de la TVA"), max_digits=15, decimal_places=2)
    total_after_tax = models.DecimalField(_("Total TTC"), max_digits=15, decimal_places=2)
    total_in_words = models.TextField(_("Montant en lettres"))

    created_at = models.DateTimeField(auto_now_add=True)
    import_date = models.DateField(_("Date d'importation"), default=now)

    def __str__(self):
        return f"{self.invoice_symbol} - {self.invoice_number}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)

    line_number = models.PositiveIntegerField(_("N° ligne"))
    name = models.CharField(_("Désignation"), max_length=255)
    unit = models.CharField(_("Unité"), max_length=50)
    quantity = models.FloatField(_("Quantité"))
    unit_price = models.DecimalField(_("Prix unitaire"), max_digits=15, decimal_places=2)
    total_price = models.DecimalField(_("Montant HT ligne"), max_digits=15, decimal_places=2)
    vat_rate = models.CharField(_("Taux de TVA"), max_length=10)

    def __str__(self):
        return f"{self.name} (x{self.quantity})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_language = models.CharField(
        max_length=10,
        choices=[('fr', 'Français'), ('vi', 'Tiếng Việt')],
        default='fr',
    )

    def __str__(self):
        return self.user.username


class InvoiceUpload(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name