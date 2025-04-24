from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import DateFieldListFilter
from django.http import HttpResponse
from django.utils.translation import gettext as _

from .models import Invoice, InvoiceItem, InvoiceUpload, UserProfile
from .services import import_zip_file

import openpyxl
from datetime import datetime


# ============ ACTION EXCEL =============

@admin.action(description=_("Exporter (feuilles séparées)"))
def export_invoices_to_excel(modeladmin, request, queryset):
    wb = openpyxl.Workbook()

    # === Feuille 1 : Factures ===
    ws1 = wb.active
    ws1.title = "Factures"

    headers_invoice = [
        _("N°"),
        _("Série"),
        _("Date"),
        _("Vendeur"),
        _("Acheteur"),
        _("Total HT"),
        _("TVA"),
        _("Total TTC"),
    ]
    ws1.append(headers_invoice)

    for invoice in queryset:
        ws1.append([
            invoice.invoice_number,
            invoice.invoice_symbol,
            invoice.issued_date.strftime('%Y-%m-%d') if invoice.issued_date else "",
            invoice.seller_name,
            invoice.buyer_name,
            float(invoice.total_before_tax),
            float(invoice.total_tax),
            float(invoice.total_after_tax),
        ])

    # === Feuille 2 : Détails de lignes ===
    ws2 = wb.create_sheet(title="Lignes de facture")

    headers_items = [
        _("Facture"),
        _("N° ligne"),
        _("Désignation"),
        _("Unité"),
        _("Quantité"),
        _("Prix unitaire"),
        _("Montant HT"),
        _("TVA"),
    ]
    ws2.append(headers_items)

    for invoice in queryset:
        for item in invoice.items.all():
            ws2.append([
                f"{invoice.invoice_symbol}-{invoice.invoice_number}",
                item.line_number,
                item.name,
                item.unit,
                item.quantity,
                float(item.unit_price),
                float(item.total_price),
                item.vat_rate,
            ])

    # Réponse HTTP
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"factures_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    wb.save(response)
    return response


@admin.action(description=_("Exporter fusionné (tout sur une feuille)"))
def export_invoices_fusionned(modeladmin, request, queryset):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Factures détaillées"

    headers = [
        _("Série"),
        _("N° facture"),
        _("Date"),
        _("Nom vendeur"),
        _("Nom acheteur"),
        _("Désignation"),
        _("Unité"),
        _("Quantité"),
        _("Prix unitaire"),
        _("Montant HT"),
        _("TVA"),
    ]
    ws.append(headers)

    for invoice in queryset:
        for item in invoice.items.all():
            ws.append([
                invoice.invoice_symbol,
                invoice.invoice_number,
                invoice.issued_date.strftime('%Y-%m-%d') if invoice.issued_date else "",
                invoice.seller_name,
                invoice.buyer_name,
                item.name,
                item.unit,
                item.quantity,
                float(item.unit_price),
                float(item.total_price),
                item.vat_rate,
            ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"factures_fusion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    wb.save(response)
    return response


# ============ INVOICE & ITEMS =============

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0
    readonly_fields = ['line_number', 'name', 'unit', 'quantity', 'unit_price', 'total_price', 'vat_rate']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'invoice_symbol', 'invoice_number', 'issued_date',
        'seller_name', 'buyer_name', 'total_after_tax', 'import_date'
    )
    list_filter = (
        'currency',
        ('issued_date', DateFieldListFilter),
        ('import_date', DateFieldListFilter),
    )
    search_fields = ('invoice_number', 'seller_name', 'buyer_name')
    inlines = [InvoiceItemInline]
    actions = [export_invoices_to_excel, export_invoices_fusionned]


# ============ ZIP IMPORT =============

@admin.register(InvoiceUpload)
class InvoiceUploadAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.file.name.endswith('.zip'):
            import_zip_file(obj.file)


# ============ PROFIL UTILISATEUR =============

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_language')
    list_filter = ('preferred_language',)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Profil utilisateur"
    fk_name = "user"


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


# Remplace l'admin User par défaut
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
