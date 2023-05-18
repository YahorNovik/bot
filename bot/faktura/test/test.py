import jinja2
import pdfkit

# Load the template file
with open('invoice-template.html.jinja', 'r', encoding='utf-8') as f:
    template_str = f.read()

# Compile the template
template = jinja2.Template(template_str)

# Define the data to be used in the template
data = {
    'invoice_number': '123',
    'issue_date': '2023-05-10',
    'sale_date': '2023-05-01',
    'due_date': '2023-05-31',
    'notes': 'Thank you for your business!',
    'payment_method': 'Credit card',
    'account_number': '1234567890',
    'user': {
        'name': 'John Smith',
        'business_name': 'Smith Inc.',
        'address': '123 Main St.',
        'nip': '123-456-78-90',
        'phone': '555-555-5555'
    },
    'cabinet': {
        'business_name': 'ABC Co.',
        'address': '456 Oak St.',
        'nip': '098-765-43-21'
    },
    'services': [
        {
            'name': 'Service A',
            'amount': 2,
            'unit': 'hour',
            'unit_price_netto': 100.00,
            'price_netto': 200.00,
            'vat_perc': 23,
            'vat_value': 46.00,
            'price_brutto': 246.00,
        }
    ],
    'in_total': {
        'price_netto': 250.00,
        'vat_value': 50.00,
        'price_brutto': 300.00,
        'price_brutto_verbally': 'trzysta złotych'
    },
    'in_total_details': [
        {
            'price_netto': 200.00,
            'vat_perc': 23,
            'vat_value': 46.00,
            'price_brutto': 300.00,
        }
    ]
}

# Render the template with the data
rendered_template = template.render(**data)

# Convert the HTML to a PDF file
pdfkit.from_string(rendered_template, 'invoice_123.pdf', configuration=pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"), options={"enable-local-file-access": ""}, css=['style.css'])
