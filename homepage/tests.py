import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.staticfiles import finders
from django.test import SimpleTestCase, override_settings
from django.urls import resolve, reverse

from models.mailing_list import MailingList
from models.message import Message
from models.user import User
from services.mailing_service import MailService
from storage.json_storage import JsonStorage


class WebPagesTests(SimpleTestCase):
    """Проверки шаблонов используют отдельный тестовый JSON."""

    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.data_file = Path(directory.name) / "mailservice.json"
        self.service = MailService()
        self.service.add_user("Алиса")
        self.service.add_user("Борис")
        self.service.add_mailing_list("Новости проекта", 1)
        self.service.add_mailing_list("Без читателей", 1)
        self.service.subscribe(2, 1)
        self.service.send_message(1, "Привет, читатели!\nНовости MailService.")
        self.service.messages[0].date = "2026-10-10"
        self.save_data()
        patcher = patch("web_data.DATA_FILE", self.data_file)
        patcher.start()
        self.addCleanup(patcher.stop)

    def save_data(self):
        JsonStorage(self.data_file).save(self.service)

    def test_all_pages_use_the_base_and_navigation(self):
        pages = {
            "/": "homepage/index.html",
            "/users/": "users_web/list.html",
            "/users/1/": "users_web/detail.html",
            "/lists/": "mailing_lists_web/list.html",
            "/lists/1/": "mailing_lists_web/detail.html",
            "/messages/": "messages_web/list.html",
            "/messages/1/": "messages_web/detail.html",
            "/subscriptions/": "subscriptions_web/list.html",
        }
        for url, template in pages.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)
                self.assertTemplateUsed(response, "base.html")
                self.assertTemplateUsed(response, "includes/navigation.html")
                self.assertContains(response, "homepage/js/main.js")

    def test_named_urls_and_integer_parameters(self):
        self.assertEqual(reverse("homepage:index"), "/")
        for namespace, url in [
            ("users", "/users/"), ("mailing_lists", "/lists/"),
            ("messages", "/messages/"),
        ]:
            with self.subTest(namespace=namespace):
                self.assertEqual(reverse(f"{namespace}:list"), url)
                self.assertEqual(
                    reverse(f"{namespace}:detail", args=[12]), f"{url}12/",
                )
                match = resolve(f"{url}12/")
                self.assertEqual(match.namespace, namespace)
                self.assertEqual(list(match.kwargs.values()), [12])

    def test_context_preserves_domain_objects(self):
        response = self.client.get("/lists/1/")
        mailing_list = response.context["mailing_list"]
        self.assertIsInstance(mailing_list, MailingList)
        self.assertIsInstance(mailing_list.owner, User)
        message = response.context["messages"][0]["message"]
        self.assertIsInstance(message, Message)
        self.assertIs(message.mailing_list, mailing_list)

    def test_home_shows_real_counts(self):
        response = self.client.get("/")
        self.assertEqual(len(response.context["users"]), 2)
        self.assertEqual(len(response.context["mailing_lists"]), 2)
        self.assertEqual(len(response.context["subscriptions"]), 1)
        self.assertEqual(len(response.context["messages"]), 1)
        self.assertContains(response, '<strong>2</strong>', count=2)
        self.assertContains(response, '<strong>1</strong>', count=2)

    def test_cards_include_both_subscriber_statuses(self):
        response = self.client.get("/lists/")
        self.assertTemplateUsed(
            response, "mailing_lists_web/includes/card.html",
        )
        self.assertTemplateUsed(
            response, "mailing_lists_web/includes/status.html",
        )
        self.assertContains(response, "Есть подписчики")
        self.assertContains(response, "Нет подписчиков")
        self.assertContains(response, 'href="/lists/1/"')
        self.assertContains(response, 'href="/users/1/"')

    def test_mailing_detail_only_shows_related_records(self):
        response = self.client.get("/lists/1/")
        self.assertEqual(
            [user.name for user in response.context["subscribers"]], ["Борис"],
        )
        self.assertEqual(len(response.context["messages"]), 1)
        self.assertContains(response, 'href="/messages/1/"')
        self.assertNotContains(response, "Без читателей")

    def test_mailing_without_subscribers_or_messages(self):
        response = self.client.get("/lists/2/")
        self.assertContains(response, "Нет подписчиков")
        self.assertContains(response, "пока нет подписчиков")
        self.assertContains(response, "пока нет сообщений")
        self.assertNotContains(response, "Борис")

    def test_profile_distinguishes_owned_lists_and_subscriptions(self):
        author = self.client.get("/users/1/")
        reader = self.client.get("/users/2/")
        self.assertEqual(len(author.context["mailing_lists"]), 2)
        self.assertEqual(len(author.context["subscriptions"]), 0)
        self.assertEqual(len(reader.context["mailing_lists"]), 0)
        self.assertEqual(len(reader.context["subscriptions"]), 1)
        self.assertContains(reader, "нет собственных рассылок")

    def test_message_date_and_full_multiline_text(self):
        for url in ["/messages/", "/messages/1/", "/lists/1/"]:
            with self.subTest(url=url):
                self.assertContains(self.client.get(url), "10.10.2026")
        self.assertContains(
            self.client.get("/messages/1/"), self.service.messages[0].text,
        )

    def test_message_preview_is_shortened_but_detail_is_complete(self):
        self.service.messages[0].text = (
            "Начало " + "длинный текст " * 30
        ).rstrip()
        self.save_data()
        full_text = self.service.messages[0].text
        self.assertNotContains(self.client.get("/messages/"), full_text)
        self.assertContains(self.client.get("/messages/1/"), full_text)

    def test_invalid_date_uses_template_fallback(self):
        self.service.messages[0].date = "не дата"
        self.save_data()
        for url in ["/messages/", "/messages/1/", "/lists/1/"]:
            with self.subTest(url=url):
                self.assertContains(self.client.get(url), "Дата не указана")

    def test_missing_objects_render_template_with_404(self):
        for url, key, text in [
            ("/lists/999/", "mailing_list", "Рассылка не найдена"),
            ("/users/999/", "profile", "Пользователь не найден"),
            ("/messages/999/", "message", "Сообщение не найдено"),
        ]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertIsNone(response.context[key])
                self.assertContains(response, text, status_code=404)
                self.assertTemplateUsed(response, "base.html")

    @override_settings(DEBUG=False)
    def test_unknown_routes_and_non_integer_ids_use_custom_404(self):
        for url in ["/unknown/", "/lists/text/", "/messages/text/",
                    "/users/text/"]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(
                    response, "Страница не найдена", status_code=404,
                )
                self.assertTemplateUsed(response, "404.html")

    def test_empty_collections(self):
        self.data_file.write_text("{}", encoding="utf-8")
        for url, text in [
            ("/users/", "Пользователи отсутствуют."),
            ("/lists/", "Списки рассылок отсутствуют."),
            ("/messages/", "Сообщения отсутствуют."),
            ("/subscriptions/", "Подписки отсутствуют."),
        ]:
            with self.subTest(url=url):
                self.assertContains(self.client.get(url), text)
        self.assertContains(
            self.client.get("/"), "<strong>0</strong>", count=4,
        )

    def test_missing_file_is_not_created_by_page_views(self):
        self.data_file.unlink()
        self.assertContains(self.client.get("/lists/"), "отсутствуют")
        self.assertFalse(self.data_file.exists())

    def test_corrupt_json_returns_empty_page_and_logs_problem(self):
        self.data_file.write_text("{broken json", encoding="utf-8")
        with self.assertLogs("web_data", level="WARNING"):
            self.assertContains(self.client.get("/lists/"), "отсутствуют")

    def test_invalid_json_structure_does_not_break_pages(self):
        for data in [[], None, {"users": [{"id": 1}]},
                     {"mailing_lists": [{"id": 1, "owner_id": 999}]}]:
            with self.subTest(data=data):
                self.data_file.write_text(json.dumps(data), encoding="utf-8")
                with self.assertLogs("web_data", level="WARNING"):
                    self.assertContains(
                        self.client.get("/lists/"), "отсутствуют",
                    )

    def test_get_requests_do_not_change_json(self):
        original = self.data_file.read_bytes()
        for url in ["/", "/users/", "/users/1/", "/lists/", "/lists/1/",
                    "/messages/", "/messages/1/", "/subscriptions/"]:
            self.client.get(url)
        self.assertEqual(original, self.data_file.read_bytes())

    def test_message_html_is_escaped(self):
        payload = '<script>alert("test")</script>'
        self.service.messages[0].text = payload
        self.save_data()
        for url in ["/messages/", "/messages/1/", "/lists/1/"]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertNotContains(response, payload)
                self.assertContains(response, "&lt;script&gt;")

    def test_default_filter_handles_empty_display_name(self):
        self.service.mailing_lists[0].name = ""
        with patch("mailing_lists_web.views.load_service",
                   return_value=self.service):
            self.assertContains(self.client.get("/lists/"), "Без названия")
            self.assertContains(self.client.get("/lists/1/"), "Без названия")

    def test_static_assets_are_available(self):
        for asset in ["css/style.css", "js/main.js", "img/logo.svg",
                      "vendor/bootstrap.min.css"]:
            with self.subTest(asset=asset):
                self.assertIsNotNone(finders.find(f"homepage/{asset}"))
