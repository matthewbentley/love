# -*- coding: utf-8 -*-
import mock

from testing.factories.employee import create_employee
from testing.factories.love import create_love
from testing.util import LoggedInAdminBaseTest


class EmailLoveTestCase(LoggedInAdminBaseTest):

    def setUp(self):
        self.sender = create_employee(username='john')
        self.recipient = create_employee(username='jenny')
        self.love = create_love(
            sender_key=self.sender.key,
            recipient_key=self.recipient.key,
            message='Love!'
        )

    def tearDown(self):
        self.love.key.delete()
        self.recipient.key.delete()
        self.sender.key.delete()

    @mock.patch('logic.love.send_email', autospec=True)
    def test_send_love_email(self, mock_send_email):  # noqa
        response = self.app.post(
            '/tasks/love/email',
            {'id': self.love.key.id()},
        )

        self.assertEqual(response.status_int, 200)
        mock_send_email.assert_called_once_with(self.love)


class LoadEmployeesTestCase(LoggedInAdminBaseTest):

    @mock.patch('logic.employee.load_employees', autospec=True)
    def test_load_employees_from_s3(self, mock_load_employees):  # noqa
        response = self.app.get('/tasks/employees/load/s3')

        self.assertEqual(response.status_int, 200)
        mock_load_employees.assert_called_with()

    @mock.patch('logic.employee.load_employees_from_csv', autospec=True)
    def test_load_employees_from_csv(self, mock_load_employees_from_csv):  # noqa
        response = self.app.post('/tasks/employees/load/csv')

        self.assertEqual(response.status_int, 200)
        mock_load_employees_from_csv.assert_called_with()
