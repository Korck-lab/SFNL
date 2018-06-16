from simple_salesforce import Salesforce, SalesforceLogin
from email.utils import parseaddr
import httplib2


class SFNL:
    def __init__(self, username, password, security_token):
        self.username = username
        self.password = password
        self.security_token = security_token
        self.sf = self.connect()

    def connect(self):
        session_id, instance = SalesforceLogin(username=self.username,
                                               password=self.password,
                                               security_token=self.security_token)

        sf = Salesforce(session_id=session_id, instance=instance)
        return sf

    def delete_lead(self, last_name, email):
        ret = self.sf.query('SELECT Id from Lead WHERE LastName = \'{}\' and Email = \'{}\''.format(last_name, email))
        if len(ret['records']) > 0:
            id = ret['records'][0]['Id']
            self.sf.Lead.delete(id)

    def new_lead(self, contact):
        try:
            name, last_name = SFNL.check_name(contact['name'], contact['last_name'])
            email = SFNL.check_email(contact['email'])
            phone = SFNL.check_phone(contact['phone'])
            company = SFNL.check_company(contact['company'])
        except KeyError as key_not_found:
            raise Exception('Mandatory contact field:'+key_not_found)
        except Exception as invalid:
            raise invalid

        try:
            website = SFNL.check_website(contact['website'])
        except KeyError:
            website = ''
        except Exception as invalid:
            raise invalid

        try:
            job_title = SFNL.check_company(contact['job_title'])
        except KeyError:
            job_title = ''
        except Exception as invalid:
            raise invalid

        lead = dict(FirstName=name, LastName=last_name, Phone=phone, Email=email,
                    Title=job_title, Website=website, Company=company)

        try:
            to_del = dict(LastName=last_name, Email=email)
            self.sf.Lead.delete(to_del)
        except:
            pass

        ret = self.sf.Lead.create(lead)

        if not ret['success']:
            raise Exception(ret['errors'])

        return ret['id']

    @staticmethod
    def check_name(name, last_name):
        name = str(name).strip(' ')
        last_name = str(last_name).strip(' ')

        if len(name) == 0:
            raise Exception('Name cannot be blank')
        if not name.replace(' ', '').isalpha():
            raise Exception('Name accepts only alphabetic characters')
        if len(last_name) == 0:
            raise Exception('Last name cannot be blank')
        if not last_name.replace(' ', '').isalpha():
            raise Exception('Last name accepts only alphabetic characters')

        return name, last_name

    @staticmethod
    def check_email(email):
        email = parseaddr(str(email).lower().strip(' '))[1]

        user_domain = email.split('@')
        if len(user_domain) == 2 and len(user_domain[0]) > 0 and len(user_domain[1]) > 0:
            return email

        raise Exception('Invalid e-mail')

    @staticmethod
    def check_website(website):
        website = str(website).lower().strip(' ')
        if not website.startswith('http://') and not website.startswith('https://'):
            website = 'http://'+website

        h = httplib2.Http()
        resp = h.request(website, 'HEAD')
        if int(resp[0]['status']) < 400:
            return website

        raise Exception('Invalid website')

    @staticmethod
    def check_phone(phone):
        phone = str(phone).replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        size = 10  # 2 for DDD and 8 for fixed phones
        if phone[0] == '+':
            phone = '00'+phone[1:]
            size += 2
        if not phone.isnumeric() or len(phone) < size:
            raise Exception('Invalid phone number')
        return phone

    @staticmethod
    def check_company(company):
        company = str(company).strip(' ')
        if company.isnumeric() or len(company) == 0:
            raise Exception('Invalid company name')

        return company

    @staticmethod
    def check_job_title(job_title):
        job_title = str(job_title).strip(' ')

        if job_title.isnumeric() or len(job_title) == 0:
            raise Exception('Invalid job title')

        return job_title
