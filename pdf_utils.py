import os
from getpass import getpass

import click
import pikepdf


@click.command()
@click.option("-e", "--encrypt", is_flag=True, help="Encrypt pdf")
@click.option("-d", "--decrypt", is_flag=True, help="Decrypt pdf")
@click.argument("pdf-file", type=click.Path(exists=True))
def pdf_utils(encrypt, decrypt, pdf_file):
    if encrypt and decrypt:
        raise click.BadOptionUsage(
            "encrypt/decrypt", "use encrypt or decrypt one at time"
        )

    if encrypt or decrypt:
        password = getpass("Password: ")

    pdf_dir = os.path.dirname(pdf_file) or "."
    if encrypt:
        new_pdf_name = os.path.join(pdf_dir, f"encrypted_{pdf_file}")
        with pikepdf.Pdf.open(pdf_file) as pdf:
            pdf.save(
                new_pdf_name,
                encryption=pikepdf.Encryption(owner=password, user=password, R=6),
            )
    elif decrypt:
        new_pdf_name = os.path.join(pdf_dir, f"decrypted_{pdf_file}")
        with pikepdf.Pdf.open(pdf_file, password=password) as pdf:
            pdf.save(new_pdf_name)


if __name__ == "__main__":
    pdf_utils()
