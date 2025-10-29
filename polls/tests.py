from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User

class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    # fixtures = ['testdb.json',]

    @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     opts = Options()
    #     cls.selenium = WebDriver(options=opts)
    #     cls.selenium.implicitly_wait(5)
    def setUp(self):
        super().setUpClass()
        opts = Options()
        self.selenium = WebDriver(options=opts)
        self.selenium.implicitly_wait(5)
        # creem superusuari
        user = User.objects.create_user(username="isard", email="isard@isardvdi.com", password="pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()

    @classmethod
    # def tearDownClass(cls):
    #     # tanquem browser
    #     # comentar la propera línia si volem veure el resultat de l'execució al navegador
    #     cls.selenium.quit()
    def tearDown(self):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        self.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )

    def test_login_error(self):
        # comprovem que amb un usuari i contrasenya inexistent, el test falla
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        # introduim dades de login
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('usuari_no_existent')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('contrasenya_incorrecta')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # utilitzem assertNotEqual per testejar que NO hem entrat
        self.assertNotEqual( self.selenium.title , "Site administration | Django site admin" )

    # def test_login_crear_usuari(self):
    #     # anem directament a la pàgina d'accés a l'admin panel
    #     self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

    #     # comprovem que el títol de la pàgina és el que esperem
    #     self.assertEqual( self.selenium.title , "Log in | Django site admin" )

    #     # introduïm dades de login i cliquem el botó "Log in" per entrar
    #     username_input = self.selenium.find_element(By.NAME,"username")
    #     username_input.send_keys('isard')
    #     password_input = self.selenium.find_element(By.NAME,"password")
    #     password_input.send_keys('pirineus')
    #     self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()
    #     # accedim a users
    #     self.selenium.find_element(By.LINK_TEXT, "Users").click()

    #     # afegim usuari
    #     self.selenium.find_element(By.LINK_TEXT, "ADD USER").click()

    #     # omplim formulari
    #     self.selenium.find_element(By.NAME, "username").send_keys("usuari_staf")
    #     self.selenium.find_element(By.NAME, "password1").send_keys("usrDjango25$")
    #     self.selenium.find_element(By.NAME, "password2").send_keys("usrDjango25$")

    #     # fer clik al botó save and continue editing
    #     self.selenium.find_element(By.NAME, "_continue").click()

    #     # a la següent plana
    #     # seleccionem el permís "Can view user" al selector múltiple de permisos
    #     from selenium.webdriver.support.ui import Select
    #     permisos_select = Select(self.selenium.find_element(By.ID, "id_user_permissions"))
    #     permisos_select.select_by_visible_text("Authentication and Authorization | user | Can view user")

    #     # guardem l'usuari definitiu
    #     self.selenium.find_element(By.NAME, "_save").click()
