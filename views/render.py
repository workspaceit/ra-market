from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        if not pdf.err:
            httpResponse = HttpResponse(response.getvalue(), content_type='application/pdf')
            httpResponse['Content-Disposition'] = 'attachment; filename="deals-report.pdf"'
            return httpResponse
        else:
            return HttpResponse("Error Rendering PDF", status=400)
