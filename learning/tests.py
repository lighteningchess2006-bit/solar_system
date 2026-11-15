from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse


@override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'])
class DeployedStaticFilesTests(SimpleTestCase):
    def test_bundled_assets_are_served_without_runserver(self):
        assets = {
            '/static/learning/study.css': 'text/css',
            '/static/explorer/style.css': 'text/css',
            '/static/explorer/app.js': 'text/javascript',
            '/static/explorer/solar-system.html': 'text/html',
        }
        for url, content_type in assets.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response['Content-Type'].startswith(content_type))
                self.assertTrue(b''.join(response.streaming_content))
                response.close()


from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    password = 'Curious-Student-482!'

    def signup(self, **changes):
        data = {'username': 'student', 'password1': self.password, 'password2': self.password}
        data.update(changes)
        return self.client.post(reverse('learning:signup'), data)

    def test_public_pages_and_account_links(self):
        for name in ['home', 'science', 'signup', 'login']:
            self.assertEqual(self.client.get(reverse('learning:' + name)).status_code, 200)
        self.assertContains(self.client.get(reverse('learning:home')), 'Sign up')

    def test_signup_hashes_password_signs_in_and_shows_username(self):
        self.assertRedirects(self.signup(), reverse('learning:home'))
        user = get_user_model().objects.get(username='student')
        self.assertNotEqual(user.password, self.password)
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(int(self.client.session[SESSION_KEY]), user.pk)
        self.assertContains(self.client.get(reverse('learning:home')), 'Welcome, student!')

    def test_invalid_signup_does_not_create_user(self):
        for changes, field in [({'password2': 'different'}, 'password2'),
                               ({'password1': '123', 'password2': '123'}, 'password2'),
                               ({'username': ''}, 'username')]:
            with self.subTest(changes=changes):
                response = self.signup(**changes)
                self.assertEqual(response.status_code, 200)
                self.assertIn(field, response.context['form'].errors)
                self.assertFalse(get_user_model().objects.exists())
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_duplicate_username_is_rejected(self):
        get_user_model().objects.create_user(username='student', password=self.password)
        response = self.signup()
        self.assertIn('username', response.context['form'].errors)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_login_and_logout(self):
        get_user_model().objects.create_user(username='student', password=self.password)
        url = reverse('learning:login')
        response = self.client.post(url, {'username': 'student', 'password': 'wrong'})
        self.assertTrue(response.context['form'].non_field_errors())
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertRedirects(self.client.post(url, {'username': 'student', 'password': self.password}), reverse('learning:home'))
        self.assertEqual(self.client.get(reverse('learning:logout')).status_code, 405)
        self.assertIn(SESSION_KEY, self.client.session)
        self.assertRedirects(self.client.post(reverse('learning:logout')), reverse('learning:home'))
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertNotContains(self.client.get(reverse('learning:home')), 'Welcome, student!')

    def test_login_rejects_external_redirect(self):
        get_user_model().objects.create_user(username='student', password=self.password)
        response = self.client.post(reverse('learning:login'), {
            'username': 'student', 'password': self.password, 'next': 'https://example.com/'})
        self.assertRedirects(response, reverse('learning:home'))

    def test_auth_posts_require_csrf(self):
        client = Client(enforce_csrf_checks=True)
        for name in ['signup', 'login', 'logout']:
            self.assertEqual(client.post(reverse('learning:' + name), {}).status_code, 403)
