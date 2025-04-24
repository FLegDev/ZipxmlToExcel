import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO

from django.db import transaction, IntegrityError
from .models import Invoice, InvoiceItem

def import_zip_file(zip_file):
    """
    Prend un fichier ZIP contenant des factures XML,
    extrait et enregistre les données en base.
    """
    invoices_created = []

    with zipfile.ZipFile(zip_file) as archive:
        for filename in archive.namelist():
            if not filename.lower().endswith('.xml'):
                continue

            with archive.open(filename) as file:
                xml_content = file.read()
                invoice = parse_xml_content(xml_content)

                if invoice:
                    invoices_created.append(invoice)

    return invoices_created

def parse_xml_content(xml_bytes):
    """
    Parse un fichier XML de facture au format SmartSign
    et retourne un objet Invoice créé en base.
    """
    try:
        root = ET.fromstring(xml_bytes)

        dlhdon = root.find("DLHDon")
        ttchung = dlhdon.find("TTChung")
        ndhhdon = dlhdon.find("NDHDon")

        invoice_number = ttchung.findtext("SHDon")
        invoice_symbol = f"{ttchung.findtext('KHMSHDon')}{ttchung.findtext('KHHDon')}"
        issued_date = ttchung.findtext("NLap")
        payment_method = ttchung.findtext("HTTToan")
        currency = ttchung.findtext("DVTTe")
        exchange_rate = ttchung.findtext("TGia")

        nban = ndhhdon.find("NBan")
        seller_name = nban.findtext("Ten")
        seller_tax = nban.findtext("MST")
        seller_address = nban.findtext("DChi")

        nmua = ndhhdon.find("NMua")
        buyer_name = nmua.findtext("Ten")
        buyer_tax = nmua.findtext("MST")
        buyer_address = nmua.findtext("DChi")

        ttoan = ndhhdon.find("TToan")
        total_before_tax = ttoan.findtext("TgTCThue")
        total_tax = ttoan.findtext("TgTThue")
        total_after_tax = ttoan.findtext("TgTTTBSo")
        total_in_words = ttoan.findtext("TgTTTBChu")

        # Vérifier doublon
        if Invoice.objects.filter(invoice_number=invoice_number, invoice_symbol=invoice_symbol).exists():
            return None

        with transaction.atomic():
            invoice = Invoice.objects.create(
                invoice_number=invoice_number,
                invoice_symbol=invoice_symbol,
                issued_date=issued_date,
                payment_method=payment_method,
                currency=currency,
                exchange_rate=exchange_rate or 1,
                seller_name=seller_name,
                seller_tax_code=seller_tax,
                seller_address=seller_address,
                buyer_name=buyer_name,
                buyer_tax_code=buyer_tax,
                buyer_address=buyer_address,
                total_before_tax=total_before_tax,
                total_tax=total_tax,
                total_after_tax=total_after_tax,
                total_in_words=total_in_words,
            )

            # Parse des lignes de facture
            items = ndhhdon.find("DSHHDVu")
            for item in items.findall("HHDVu"):
                try:
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        line_number=item.findtext("STT") or 0,
                        name=item.findtext("THHDVu") or "Sans nom",
                        unit=item.findtext("DVTinh") or "",
                        quantity=item.findtext("SLuong") or 0,
                        unit_price=item.findtext("DGia") or 0,
                        total_price=item.findtext("ThTien") or 0,
                        vat_rate=item.findtext("TSuat") or "0%",
                    )
                except IntegrityError as e:
                    print(f"Erreur ligne facture ignorée : {e}")

        return invoice

    except Exception as e:
        print(f"Erreur lors du parsing XML : {e}")
        return None