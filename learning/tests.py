from django.test import SimpleTestCase, override_settings


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
