from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .forms import InfoForm


def get_info_view(request):
    if request.method == "POST":
        form = InfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("thanks")
    else:
        form = InfoForm()
    return render(request, "info/get_info.html", {"form": form})


class ThanksPageView(TemplateView):
    template_name = "info/thanks.html"
