# Generated by Django 5.2 on 2025-05-03 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0003_alter_invoiceitem_vat_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='buyer_address',
            field=models.TextField(blank=True, verbose_name="Adresse de l'acheteur"),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='buyer_name',
            field=models.CharField(blank=True, max_length=255, verbose_name="Nom de l'acheteur"),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='buyer_tax_code',
            field=models.CharField(blank=True, max_length=20, verbose_name="Numéro fiscal de l'acheteur"),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='exchange_rate',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, max_digits=10, null=True, verbose_name='Taux de change'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='issued_date',
            field=models.DateField(blank=True, null=True, verbose_name="Date d'émission"),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_method',
            field=models.CharField(blank=True, max_length=100, verbose_name='Méthode de paiement'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='seller_address',
            field=models.TextField(blank=True, verbose_name='Adresse du vendeur'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='seller_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Nom du vendeur'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='seller_tax_code',
            field=models.CharField(blank=True, max_length=20, verbose_name='Numéro fiscal du vendeur'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_after_tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Total TTC'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_before_tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Total HT'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_in_words',
            field=models.TextField(blank=True, null=True, verbose_name='Montant en lettres'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Montant de la TVA'),
        ),
    ]
