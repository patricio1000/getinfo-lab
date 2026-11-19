from django.contrib import admin
from django.test import TestCase
from django.urls import reverse

from .forms import InfoForm
from .models import Info

GOOD_DATA = {
    "name": "Ada Lovelace",
    "email": "ada@example.com",
    "cell_phone": "402-555-1234",
    "comments": "Please send me information about the CS program.",
}


class InfoModelTests(TestCase):
    def test_str_shows_name_and_email(self):
        info = Info.objects.create(**GOOD_DATA)
        self.assertEqual(str(info), "Ada Lovelace (ada@example.com)")

    def test_created_at_is_filled_in(self):
        info = Info.objects.create(**GOOD_DATA)
        self.assertIsNotNone(info.created_at)

    def test_info_is_in_admin(self):
        self.assertTrue(admin.site.is_registered(Info))


class InfoFormTests(TestCase):
    def test_form_has_four_fields(self):
        self.assertEqual(list(InfoForm().fields), ["name", "email", "cell_phone", "comments"])

    def test_good_data_is_valid(self):
        self.assertTrue(InfoForm(data=GOOD_DATA).is_valid())

    def test_every_field_is_required(self):
        form = InfoForm(data={})
        self.assertFalse(form.is_valid())
        for field in ["name", "email", "cell_phone", "comments"]:
            with self.subTest(field=field):
                self.assertFormError(form, field, "This field is required.")

    def test_bad_email_is_rejected(self):
        form = InfoForm(data={**GOOD_DATA, "email": "not-an-email"})
        self.assertFalse(form.is_valid())
        self.assertFormError(form, "email", "Enter a valid email address.")

    def test_phone_formats_are_accepted_and_cleaned(self):
        for phone in ["402-555-1234", "(402) 555-1234", "402.555.1234", "4025551234"]:
            with self.subTest(phone=phone):
                form = InfoForm(data={**GOOD_DATA, "cell_phone": phone})
                self.assertTrue(form.is_valid())
                self.assertEqual(form.cleaned_data["cell_phone"], "402-555-1234")

    def test_bad_phone_numbers_are_rejected(self):
        for phone in ["555-1234", "402-555-12345", "call me"]:
            with self.subTest(phone=phone):
                form = InfoForm(data={**GOOD_DATA, "cell_phone": phone})
                self.assertFalse(form.is_valid())
                self.assertFormError(
                    form, "cell_phone", "Enter a 10-digit phone number, like 402-555-1234."
                )


class GetInfoPageTests(TestCase):
    def test_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_name_works(self):
        response = self.client.get(reverse("get_info"))
        self.assertEqual(response.status_code, 200)

    def test_uses_template(self):
        response = self.client.get(reverse("get_info"))
        self.assertTemplateUsed(response, "info/get_info.html")
        self.assertTemplateUsed(response, "info/base.html")

    def test_shows_an_empty_form(self):
        response = self.client.get(reverse("get_info"))
        self.assertIsInstance(response.context["form"], InfoForm)
        self.assertFalse(response.context["form"].is_bound)
        for field in ["name", "email", "cell_phone", "comments"]:
            with self.subTest(field=field):
                self.assertContains(response, f'name="{field}"')

    def test_has_csrf_token(self):
        response = self.client.get(reverse("get_info"))
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_good_post_saves_and_redirects(self):
        response = self.client.post(reverse("get_info"), GOOD_DATA)
        self.assertRedirects(response, reverse("thanks"))
        self.assertEqual(Info.objects.count(), 1)
        self.assertEqual(Info.objects.get().name, "Ada Lovelace")

    def test_phone_is_saved_in_one_format(self):
        self.client.post(reverse("get_info"), {**GOOD_DATA, "cell_phone": "(402) 555 1234"})
        self.assertEqual(Info.objects.get().cell_phone, "402-555-1234")

    def test_bad_post_shows_errors_and_saves_nothing(self):
        response = self.client.post(reverse("get_info"), {**GOOD_DATA, "cell_phone": "555-1234"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a 10-digit phone number")
        self.assertEqual(Info.objects.count(), 0)


class ThanksPageTests(TestCase):
    def test_thanks_page_loads(self):
        response = self.client.get(reverse("thanks"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "info/thanks.html")
        self.assertContains(response, "Thank You")
