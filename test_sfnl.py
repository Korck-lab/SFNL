from unittest import TestCase
from sfnl import SFNL


class TestSFNL(TestCase):
    def test_authentication_ok(self):
        username = 'rafael.aguilher@gmail.com'
        password = 'sandbox@1'
        security_token = 'ktb7N4UF6M31ADx4qbxOvMkB'
        sf = SFNL(username, password, security_token)
        assert(sf is not None)

    def test_authentication_not_ok(self):
        username = 'rafael.aguilher@gmail.com'
        password = 'sdf@1'
        security_token = 'asd'
        try:
            sf = SFNL(username, password, security_token)
            raise AssertionError()
        except:
            pass

    def test_check_name_ok(self):
        name = 'Rafael'
        last_name = 'Costa'
        SFNL.check_name(name, last_name)

        name = '   Rafael    '
        last_name = '      Aguilher da Costa'
        name, last_name = SFNL.check_name(name, last_name)
        assert(last_name == 'Aguilher da Costa')
        assert(name == 'Rafael')

    def test_check_name_not_ok(self):
        name = 'Rafael1243'
        last_name = 'Costa'
        try:
            name, last_name = SFNL.check_name(name, last_name)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        name = 'Rafael'
        last_name = 'C*st@ '
        try:
            name, last_name = SFNL.check_name(name, last_name)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        name = 'Rafael'
        last_name = ''
        try:
            name, last_name = SFNL.check_name(name, last_name)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        name = ''
        last_name = 'Costa'
        try:
            name, last_name = SFNL.check_name(name, last_name)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

    def test_check_email_ok(self):
        email = ' Rafael.Aguilher@gmail.com    '
        email = SFNL.check_email(email)
        assert(email == 'rafael.aguilher@gmail.com')

        email = ' Rafael Aguilher da Costa <rafael.aguilher@gmail.com>'
        email = SFNL.check_email(email)
        assert(email == 'rafael.aguilher@gmail.com')

        email = ' 1234Rafael Aguilher da Costa <rafael.aguilher@gmail.com>'
        email = SFNL.check_email(email)
        assert (email == 'rafael.aguilher@gmail.com')

    def test_check_email_not_ok(self):
        email = ' Rafael@Aguilher@gmail.com    '
        try:
            email = SFNL.check_email(email)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        email = ' Rafael Aguilher da Costa <rafael@aguilher@gmail.com>'
        try:
            email = SFNL.check_email(email)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        email = ' Rafael Aguilher da Costa <rafael.aguilher.gmail.com>'
        try:
            email = SFNL.check_email(email)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        email = ' @Rafael Aguilher da Costa <rafael.aguilher@gmail.com>'
        try:
            email = SFNL.check_email(email)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

    def test_check_phone_ok(self):
        phone = ' (48) 99132-7087'
        phone = SFNL.check_phone(phone)
        assert(phone == '48991327087')

        phone = '048991327087'
        phone = SFNL.check_phone(phone)
        assert(phone == '048991327087')

        phone = '+5548991327087'
        phone = SFNL.check_phone(phone)
        assert(phone == '005548991327087')

        phone = ' +55 (48) 99132-7087 '
        phone = SFNL.check_phone(phone)
        assert(phone == '005548991327087')

    def test_check_phone_not_ok(self):
        phone = ' (48)asd 99132-7087'
        try:
            phone = SFNL.check_phone(phone)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        phone = '+(48)132-7087'
        try:
            phone = SFNL.check_phone(phone)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        phone = ' (48)132-7087'
        try:
            phone = SFNL.check_phone(phone)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        phone = ' (48)99132+7087'
        try:
            phone = SFNL.check_phone(phone)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

    def test_check_website_ok(self):
        website = 'www.google.com'
        website = SFNL.check_website(website)
        assert(website == 'http://www.google.com')

        website = '   https://www.google.com'
        website = SFNL.check_website(website)
        assert(website == 'https://www.google.com')

        website = '   google.com'
        website = SFNL.check_website(website)
        assert(website == 'http://google.com')

    def test_check_website_not_ok(self):
        website = 'askdpoaskd#$!@#$.com'
        try:
            website = SFNL.check_website(website)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        website = 'google.123.lsd'
        try:
            website = SFNL.check_website(website)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        website = 'https://resultadosdigitais.com.uk/'
        try:
            website = SFNL.check_website(website)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

    def test_check_company_ok(self):
        company = ' Resultados Digitais S./A. '
        company = SFNL.check_company(company)
        assert(company == 'Resultados Digitais S./A.')

        company = 'Oi! '
        company = SFNL.check_company(company)
        assert(company == 'Oi!')

        company = 'Viva :)'
        company = SFNL.check_company(company)
        assert(company == 'Viva :)')

    def test_check_company_not_ok(self):
        company = 12345
        try:
            company = SFNL.check_company(company)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        company = ' 12345 '
        try:
            company = SFNL.check_company(company)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        company = ''
        try:
            company = SFNL.check_company(company)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

    def test_check_job_title_ok(self):
        job_title = ' CEO '
        job_title = SFNL.check_job_title(job_title)
        assert(job_title == 'CEO')

        job_title = 'Jr. 2 '
        job_title = SFNL.check_job_title(job_title)
        assert(job_title == 'Jr. 2')

    def test_check_job_title_not_ok(self):
        job_title = 12345
        try:
            job_title = SFNL.check_job_title(job_title)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        job_title = '12345 '
        try:
            job_title = SFNL.check_job_title(job_title)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

        job_title = ' '
        try:
            job_title = SFNL.check_job_title(job_title)
            raise AssertionError()
        except Exception as invalid:
            print(invalid)

    def test_insert_new_lead(self):
        username = 'rafael.aguilher@gmail.com'
        password = 'sandbox@1'
        security_token = 'ktb7N4UF6M31ADx4qbxOvMkB'
        sf = SFNL(username, password, security_token)

        lead = dict(name='Rafael', last_name='da Costa', phone='(48) 9911-2222', website='www.google.com',
                    email='rafael.aguilher@gmail.com', company='MMC', job_title='Dir. Tech.')

        sf.delete_lead(lead['last_name'], lead['email'])
        id = sf.new_lead(lead)
        print(id, lead)

