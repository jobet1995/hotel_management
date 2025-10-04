from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserAPITests(APITestCase):

    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='password', role='Admin')
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        # Create a regular user (patient)
        self.patient_user = User.objects.create_user(username='patient', email='patient@example.com', password='password', role='Patient')

        # Create another regular user
        self.doctor_user = User.objects.create_user(username='doctor', email='doctor@example.com', password='password', role='Doctor')

    def test_register_patient(self):
        """
        Ensure we can register a new patient.
        """
        url = reverse('register')
        data = {'username': 'newpatient', 'email': 'newpatient@example.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(User.objects.get(email='newpatient@example.com').role, 'Patient')

    def test_login_user(self):
        """
        Ensure a user can log in and get a JWT token.
        """
        url = reverse('login')
        data = {'email': 'patient@example.com', 'password': 'password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_logout_user(self):
        """
        Ensure a user can log out by blacklisting the refresh token.
        """
        login_url = reverse('login')
        login_data = {'email': 'patient@example.com', 'password': 'password'}
        login_response = self.client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']

        logout_url = reverse('logout')
        logout_data = {'refresh': refresh_token}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}")
        response = self.client.post(logout_url, logout_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_admin_can_list_users(self):
        """
        Ensure admin users can list all users.
        """
        url = reverse('user-list')
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_non_admin_cannot_list_users(self):
        """
        Ensure non-admin users cannot list all users.
        """
        url = reverse('user-list')
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_retrieve_user(self):
        """
        Ensure admin can retrieve any user's details.
        """
        url = reverse('user-detail', kwargs={'pk': self.patient_user.pk})
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.patient_user.email)

    def test_user_can_retrieve_own_profile(self):
        """
        Ensure user can retrieve their own profile details.
        """
        url = reverse('user-detail', kwargs={'pk': self.patient_user.pk})
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.patient_user.email)

    def test_user_cannot_retrieve_other_profile(self):
        """
        Ensure user cannot retrieve another user's profile details.
        """
        url = reverse('user-detail', kwargs={'pk': self.doctor_user.pk})
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_own_profile(self):
        """
        Ensure authenticated user can retrieve their profile via /api/profile/.
        """
        url = reverse('profile')
        self.client.force_authenticate(user=self.patient_user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.patient_user.email)

    def test_update_own_profile(self):
        """
        Ensure user can update their own profile.
        """
        url = reverse('profile')
        self.client.force_authenticate(user=self.patient_user)
        data = {'first_name': 'New', 'last_name': 'Name'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.patient_user.refresh_from_db()
        self.assertEqual(self.patient_user.first_name, 'New')
