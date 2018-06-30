from __future__ import unicode_literals
from django import test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

from pyquery import PyQuery as pq

User = get_user_model()


# class TabularPermissionsLiveTest(AdminSeleniumTestCase):
#
#     available_apps = AdminSeleniumTestCase.available_apps + ['tabular_permissions']
#     browsers = ['firefox']
#
#     def setUp(self):
#         self.user = User.objects.create_superuser('super', 'myemail@test.com', 'secret')
#
#     def goto_user_change(self):
#         self.admin_login(username='super', password='secret')
#         self.selenium.get('%s%s' % (self.live_server_url,
#                                     reverse('admin:auth_user_change', args=(self.user.pk,))))
#
#     def test_select_all_boxes(self):
#         """
#         Ensure that the select-all check boxed behave as expected.
#         """
#         self.admin_login(username='super', password='secret')
#         self.selenium.get('%s%s' % (self.live_server_url,
#                                     reverse('admin:auth_user_change', args=(self.user.pk,))))
#         test_classes = (
#             ('perm_add_select_all', '.checkbox.add'),
#             ('perm_delete_select_all', '.checkbox.delete'),
#             ('perm_change_select_all', '.checkbox.change')
#         )
#         for elem_id, css_class in test_classes:
#             add_select_all = self.selenium.find_element_by_id(
#                 elem_id)
#             add_select_all.click()
#
#             add_checkboxes = self.selenium.find_elements_by_css_selector(css_class)
#             for e in add_checkboxes:
#                 self.assertEqual(e.get_attribute('checked'), 'true')
#
#     @skip('To be reviewed')
#     def test_initial_widget_is_hidden(self):
#         """
#         Case No extra permissions, FilteredSelectMultiple Should be hidden
#         as it contains no Values
#         """
#         self.admin_login(username='super', password='secret')
#         self.selenium.get('%s%s' % (self.live_server_url,
#                                     reverse('admin:auth_user_change', args=(self.user.pk,))))
#         original_widget = self.selenium.find_element_by_css_selector('[name=user_permissions]')
#         self.assertFalse(original_widget.is_displayed())
#
#     def test_initial_widget_is_visible_on_extra_permissions(self):
#         """
#         Case of extra permissions, FilteredSelectMultiple Should be visible
#         to handle assignment.
#         """
#         Permission.objects.create(codename='custom_perm', content_type_id=1)
#         self.goto_user_change()
#         original_widget = self.selenium.find_element_by_css_selector('[name=user_permissions]')
#         self.assertTrue(original_widget.is_displayed())
#
#     def test_save_table_permissions(self):
#         """
#         Test that checked permissions from the widget are saved, and they are the only permissions
#         for that user.
#         """
#
#         self.goto_user_change()
#         add_select_all = self.selenium.find_element_by_id('perm_add_select_all')
#         add_checkboxes = self.selenium.find_elements_by_css_selector('.checkbox.add:not(.select-all)')
#         user_perms = []
#         for e in add_checkboxes:
#             user_perms.append(e.get_attribute('data-perm-id'))
#         reminder_user_perms = list(user_perms)
#         add_select_all.click()
#         save = self.selenium.find_element_by_css_selector('[name=_save]')
#         save.click()
#         self.wait_for('#changelist-form')
#         user = self.user
#         user_saved_permissions = user.user_permissions.values_list('id', flat=True)
#         user_saved_permissions = [force_text(x) for x in user_saved_permissions]
#         for perm in user_perms:
#             try:
#                 user_saved_permissions.remove(perm)
#                 reminder_user_perms.remove(perm)
#             except ValueError:
#                 pass
#         self.assertEqual(len(user_saved_permissions), 0)
#         self.assertEqual(len(reminder_user_perms), 0)
#
#     def test_visible_on_group_admin(self):
#         """
#         Test tabular_permissions visible on GroupAdmin with right data-input-name
#         """
#         self.admin_login(username='super', password='secret')
#         self.selenium.get('%s%s' % (self.live_server_url,
#                                     reverse('admin:auth_group_add')))
#         table = self.selenium.find_element_by_css_selector('#tabular_permissions')
#         self.assertEqual(table.get_attribute('data-input-name'), 'permissions')
#
#     def test_select_all_row(self):
#         """
#         Test Select All Row behaves as expected
#         """
#         self.goto_user_change()
#         first_row_checkbox = self.selenium.find_elements_by_css_selector('.select-all.select-row')[0]
#         first_row_checkbox.click()
#         model_name = first_row_checkbox.get_attribute('data-model-name')
#         related_checkboxes = self.selenium.find_elements_by_css_selector('.checkbox.%s' % model_name)
#         for c in related_checkboxes:
#             self.assertTrue(c.get_attribute('checked'))


class TabularPermissionsTestCase(test.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TabularPermissionsTestCase, cls).setUpClass()
        cls.user = User.objects.create_superuser(username='super', password='secret', email='email@domain.com')

    def test_visible_on_group_admin(self):
            """
            Test tabular_permissions visible on GroupAdmin with right data-input-name
            """
            self.client.login(username='super', password='secret')
            response = self.client.get((reverse('admin:auth_group_add')))
            self.assertEqual(response.status_code, 200)
            doc = pq(response.content)
            table = doc.find('#tabular_permissions')
            self.assertEqual(table.attr('data-input-name'), 'permissions')

    def test_initial_widget_is_visible_on_extra_permissions(self):
        """
        Case of extra permissions, FilteredSelectMultiple Should be visible
        to handle assignment.
        """
        Permission.objects.create(codename='custom_perm', content_type_id=1)
        self.client.login(username='super', password='secret')
        response = self.client.get(reverse('admin:auth_user_change', args=(self.user.pk,)))
        doc = pq(response.content)
        table = doc.find('[name=user_permissions]')
        self.assertEqual(len(table), 1)
