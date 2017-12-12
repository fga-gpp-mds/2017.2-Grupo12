from django.test import TestCase, Client
from django.shortcuts import reverse
from .views import getItems
from .views import getFilteredItems
from .views import getSchoolNames
from .forms import SchoolForm


class SearchSchoolTest(TestCase):
    def setUp(self):
        pass

    def testGetItems(self):
        name = 'ESCOLA ESTADUAL PEDRO LUDOVICO TEIXEIRA'
        state = 'TO'
        city = 'Maurilândia do Tocantins'
        item = getItems(name, state, city)
        self.assertEquals(item[0].get('nome'), name)

    def testGetFilteredItems(self):
        name = 'Maria'
        state = 'DF'
        city = 'Brasília'
        schoolList = getFilteredItems(name, state, city)
        schools = getSchoolNames(schoolList)
        testList = [
            'CEF 201 DE SANTA MARIA',
            'CEF 209 DE SANTA MARIA',
            'EC 218 DE SANTA MARIA',
            'CEF PROF MARIA DO ROSARIO GONDIM DA SILVA',
            'CEF 213 DE SANTA MARIA',
            'CEF 403 DE SANTA MARIA',
            'CEI 203 DE SANTA MARIA',
            ]
        self.assertEquals(schools, testList)

    def testRenderSchoolForm(self):
        client = Client()
        client.login(username="amanda", password="123")
        response = client.get(reverse('search_school:schoolForm'))
        self.assertEquals(response.status_code, 302)

    def test_redirectSchool_page(self):
        client = Client()
        response = client.get('/redirectSchool/')
        self.assertEquals(200, response.status_code)

    def test_notLoggedIn_page(self):
        client = Client()
        response = client.get('/notLoggedIn/')
        self.assertEquals(200, response.status_code)

    def test_SchoolForm_invalid(self):
        data = [
            'CEF 201 DE SANTA MARIA',
            'CEF 209 DE SANTA MARIA',
            'EC 218 DE SANTA MARIA',
            'CEF PROF MARIA DO ROSARIO GONDIM DA SILVA',
            'CEF 213 DE SANTA MARIA',
            'CEF 403 DE SANTA MARIA',
            'CEI 203 DE SANTA MARIA',
            ]
        form = SchoolForm(schools=data)
        self.assertFalse(form.is_valid())
