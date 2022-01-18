from django.shortcuts import render
from django.views.generic import TemplateView

class ReportSaleView(TemplateView):
    template_name = 'report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Reporte de ventas'
        context["list_url"] = reverse_lazy('')
        context["title"] = 'Reporte de ventas'
        return context
    
