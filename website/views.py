from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm, NewsLetterForm

# Create your views here.

class IndexView(TemplateView):
    template_name = "website/index.html"


class AboutView(TemplateView):
    template_name = "website/about.html"


class ContactView(FormView):
    template_name = "website/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("website:contact")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "تیکت شما با موفقیت ارسال شد و در اسرع وقت با شما تماس حاصل خواهد شد")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "مشکلی در ارسال تیکت بوجود آمد لطفا فیلد ها را بررسی و دوباره تلاش نمایید")
        return redirect(self.request.META.get('HTTP_REFERER'))
    

class NewsLetterView(CreateView):
    
    success_url = "/"
    form_class = NewsLetterForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "ایمیل شما با موفقیت ثبت شد. منتظر اخبار ما باشید.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "مشکلی در ثبت ایمیل شما وجود دارد لطفا دوباره تلاش کنید.")
        return redirect("website:index")

