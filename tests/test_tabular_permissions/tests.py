from __future__ import unicode_literals
import pdb
import datetime
from django import test
from django.contrib.admin.tests import AdminSeleniumWebDriverTestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test.utils import override_settings

User = get_user_model()
class TabularPermissionsLiveTest(AdminSeleniumWebDriverTestCase):
    available_apps = ['tabular_permissions'] + AdminSeleniumWebDriverTestCase.available_apps

    def setUp(self):
        User.objects.create(pk=1000,
            username='super', first_name='Super', last_name='User', email='super@example.com',
            password='sha1$995a3$6011485ea3834267d719b4c801409b8b1ddd0158', is_active=True, is_superuser=True,
            is_staff=True, last_login=datetime.datetime(2007, 5, 30, 13, 20, 10),
            date_joined=datetime.datetime(2007, 5, 30, 13, 20, 10)
        )
    #     User = get_user_model()
    #     User.objects.create_superuser('super', None, 'secret')
    #     self.client.login(username='super', password='secret')
    #     self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
    #     username_input = self.selenium.find_element_by_name("username")
    #     username_input.send_keys('super')
    #     password_input = self.selenium.find_element_by_name("password")
    #     password_input.send_keys('secret')
    #     self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()

    def goto_user_change(self):
        self.admin_login(username='super', password='secret')
        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('admin:auth_user_change', args=(1000,))))

    def test_select_all_boxes(self):
        """
        Ensure that the "Add another XXX" link correctly adds items to the
        stacked formset.
        """
        self.admin_login(username='super', password='secret')
        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('admin:auth_user_change', args=(1000,))))
        test_classes = (
            ('perm_add_select_all','.checkbox.add'),
            ('perm_delete_select_all','.checkbox.delete'),
            ('perm_change_select_all','.checkbox.change')
        )
        for elem_id, css_class in test_classes:
            add_select_all = self.selenium.find_element_by_id(
                elem_id)
            add_select_all.click()

            add_checkboxes = self.selenium.find_elements_by_css_selector(css_class)
            for e in add_checkboxes:
                self.assertEqual(e.get_attribute('checked'), 'true')



    def test_initial_widget_is_hidden(self):
        self.admin_login(username='super', password='secret')
        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('admin:auth_user_change', args=(1000,))))
        original_widget = self.selenium.find_element_by_css_selector('[name=user_permissions]')
        self.assertFalse(original_widget.is_displayed())

    def test_initial_widget_is_visible_on_extra_permissions(self):
        Permission.objects.create(codename='custom_perm', content_type_id=1)
        self.goto_user_change()
        original_widget = self.selenium.find_element_by_css_selector('[name=user_permissions]')
        self.assertTrue(original_widget.is_displayed())

    def test_save_table_permissions(self):
        self.goto_user_change()
        add_select_all = self.selenium.find_element_by_id('perm_add_select_all')
        add_checkboxes = self.selenium.find_elements_by_css_selector('.checkbox.add:not(.select-all)')
        user_perms = []
        for e in add_checkboxes:
            user_perms.append(e.get_attribute('data-perm-id'))
            # self.assertEqual(e.get_attribute('checked'), 'true')
        reminder_user_perms = list(user_perms)
        add_select_all.click()
        save = self.selenium.find_element_by_css_selector('[name=_continue]')
        save.click()
        self.wait_page_loaded()
        user = User.objects.get(pk=1000)
        user_saved_permissions = user.user_permissions.values_list('id', flat=True)
        user_saved_permissions = [force_text(x) for x in user_saved_permissions]
        for perm in user_perms:
            try:
                user_saved_permissions.remove(perm)
                reminder_user_perms.remove(perm)
            except:
                raise AssertionError
        self.assertEqual(len(user_saved_permissions), 0)
        self.assertEqual(len(reminder_user_perms), 0)




class TabularPermissionsHelpers(test.TestCase):
    pass
