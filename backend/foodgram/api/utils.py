from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def pdf_download(request, ingredients):
    pdfmetrics.registerFont(
        TTFont('Helvetica', 'Helvetica.ttf', 'UTF-8'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.pdf"')
    page = canvas.Canvas(response)
    page.setFont('Helvetica', size=20)
    page.drawString(180, 800, 'Список ингредиентов для ')
    page.drawString(160, 775, f'пользователя {request.user.get_full_name()}')
    page.setFont('Helvetica', size=16)
    height = 700
    final_list = {}
    for item in ingredients:
        final_list[item['ingredient__name']] = {
            'unit': item['ingredient__measurement_unit'],
            'amount': item['amount']
        }
    for number, (name, data) in enumerate(final_list.items(), 1):
        page.drawString(75, height, (
            f'{number}) {name} - {data["amount"]} '
            f'{data["unit"]}'
        ))
        height -= 25
    page.showPage()
    page.save()
    return response
