from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
import time

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
        time.sleep(3)

    def test_login_crear_usuari(self):
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
        # accedim a users
        self.selenium.find_element(By.LINK_TEXT, "Users").click()

        # afegim usuari
        self.selenium.find_element(By.LINK_TEXT, "ADD USER").click()

        # omplim formulari
        self.selenium.find_element(By.NAME, "username").send_keys("usuari_staff")
        self.selenium.find_element(By.NAME, "password1").send_keys("usrDjango25$")
        self.selenium.find_element(By.NAME, "password2").send_keys("usrDjango25$")

        # fer clik al botó save and continue editing
        self.selenium.find_element(By.NAME, "_continue").click()

        # a la següent plana
        self.selenium.find_element(By.NAME, "is_staff").click()
        select_element = self.selenium.find_element(By.ID, "id_user_permissions_from")
        time.sleep(10)
        select = Select(select_element)
        select.select_by_visible_text("Authentication and Authorization | user | Can view user")
        # select.select_by_value("24")
        # Al principi vaig optar per fer la selecció pel valor però més tard em vaig adonar que 
        # si es carrega el formulari varies vegades, asigna valors diferents així que vaig decidir
        # buscar pel text.

        self.selenium.find_element(By.ID, "id_user_permissions_add").click()
        # faig temps per veure que ha seleccionat el permís correcte
        time.sleep(3)

        # guardem l'usuari definitivament
        self.selenium.find_element(By.NAME, "_save").click()

        # afegim usuari1
        self.selenium.find_element(By.LINK_TEXT, "ADD USER").click()

        # omplim formulari
        self.selenium.find_element(By.NAME, "username").send_keys("usuari1")
        self.selenium.find_element(By.NAME, "password1").send_keys("usrDjango25$")
        self.selenium.find_element(By.NAME, "password2").send_keys("usrDjango25$")
        # guardem l'usuari una vegada per cadasquna de les dues planes
        self.selenium.find_element(By.NAME, "_save").click()
        self.selenium.find_element(By.NAME, "_save").click()


        # afegim usuari
        self.selenium.find_element(By.LINK_TEXT, "ADD USER").click()

        # omplim formulari
        self.selenium.find_element(By.NAME, "username").send_keys("usuari2")
        self.selenium.find_element(By.NAME, "password1").send_keys("usrDjango25$")
        self.selenium.find_element(By.NAME, "password2").send_keys("usrDjango25$")
        # guardem l'usuari una vegada per cadasquna de les dues planes
        self.selenium.find_element(By.NAME, "_save").click()
        self.selenium.find_element(By.NAME, "_save").click()


        # afegim usuari
        self.selenium.find_element(By.LINK_TEXT, "ADD USER").click()

        # omplim formulari
        self.selenium.find_element(By.NAME, "username").send_keys("usuari3")
        self.selenium.find_element(By.NAME, "password1").send_keys("usrDjango25$")
        self.selenium.find_element(By.NAME, "password2").send_keys("usrDjango25$")
        # guardem l'usuari una vegada per cadasquna de les dues planes
        self.selenium.find_element(By.NAME, "_save").click()
        self.selenium.find_element(By.NAME, "_save").click()

        # faig temps per veure que tots el usuris s'han creat
        time.sleep(1)

        # sortirm del formulari ja que si iniciem un altre test no hi són els usuaris
        self.selenium.find_element(By.ID, "logout-form").click()

        time.sleep(1)

        # busquem iniciar de nou la sesió
        self.selenium.find_element(By.LINK_TEXT,"Log in again").click()
        time.sleep(1)

        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        # faig el focus al username
        self.selenium.find_element(By.NAME, "username").click()

        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('usuari_staff')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('usrDjango25$')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        time.sleep(1)

        # accedim a users
        self.selenium.find_element(By.LINK_TEXT, "Users").click()

        time.sleep(1)

        # seleccionem usuari1
        self.selenium.find_element(By.LINK_TEXT, "usuari1").click()

        # Busquem el botó "Close" ja que de poder editar aquest botó no hi seria
        # Només surt com a únic botó si només tenim privilegis per veure
        self.selenium.find_element(By.LINK_TEXT, "Close").click()

        time.sleep(1)
