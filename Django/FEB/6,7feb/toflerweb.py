
from . import Logging
from cgi import FieldStorage 
try:
    from cgi import parse_qs
except:
    from urllib.parse import parse_qs
import datetime
import time
import json
import re
import os
import hashlib
from jinja2 import Environment, PackageLoader
from pytofler.utils import formatter
from toflercommon import Common

from . import pytoflershim

from . import statichandler
from . import shoppingcarthandler
from . import mcahandler
from . import signinhandler
from . import userdashboardhandler
from . import sitemaphandler
from . import mischandlers
from . import adminmanagement
from . import businesshandler
from . import advancedsearchhandler
from . import comparatorhandler

import traceback
from six import StringIO


class ToflerWeb(object):

    '''
    The core class for the Tofler website.

    An object of this class is created and the webrequest is passed to the
    webcall method. All further processing is coordinated from there.

    On creation, the _init_ method registers all the handlers etc for webcall
    to work seamlessly.
    '''

    _config_ = {}
    reqKeys = []
    defaultStatus = '500 Internal Server Error'
    defaultOutput = '<html><head><title>TOFLER</title></head><body>There seems to be a problem. Please try again in some time.</body></html>'
    templatefiles = {
        'ErrorPage':'static/errorpage.html',
        '404Error': 'static/404error.html',
        '500Error':'static/500error.html',
        }
    precompiledtemplates = {}
    actions = {}
    __jinjaenv = None
    _alphanumpattern = None
    _known_bots = [
        '^66.249', '^72.14.', '^157.55.', '^40.77.',
        '^207.46.', '^148.64.56.', '^13.66.139.',
        '^216.244.66.', '^91.242.168.',
        '^52.162.161.', '^37.9.87.',
        '^141.8.144.', '^46.229.168.',
        '^54.36.148.', '^54.36.149.',
        '^54.36.150.', '^52.167.144.',
        '^52.231.', '^52.233.106.']

    def _registerAction(self, action, function):
        ''' Method to register a handler for a particular action. '''
        if (action not in self.actions):
            self.actions[action] = function
            return True
        else:
            Logging.log('Handling for Action %s already specified...' % action)
            return False

    def _get_app_version(self):
        filename = os.path.join(
            os.path.dirname(os.path.abspath(_file_)),
            'VERSION.json')
        with open(filename, 'r') as version_file:
            app_version = json.load(version_file)
            return '{major}.{minor}.{build}'.format(**app_version)


    def _init_(self, config):
        ''' Validate the configuration and register handlers for events. '''
        validConfig = True
        for key in self.reqKeys:
            if (key not in config):
                validConfig = False
                Logging.log('Malformed Configuration Supplied to ToflerWeb Application. Initialization Failed...')
                return None
        self._config_ = config
        self.alphanumpattern = re.compile('[\W]+')

        bot_pattern = '|'.join(self._known_bots)
        self._bot_pattern = re.compile(bot_pattern)

        self._cdn_config = self._get_site_config('cdn_config')
        self._environment = self._get_site_config('environment')
        self._app_version = self._get_app_version()
        #self._cdn_config = {'cdn_prefix':''}
        if 'cdn_prefix' not in self._cdn_config:
            self._cdn_config = {'cdn_prefix':''}
        if self._environment == 'dev':
            self._version_suffix = '.%s' % self._app_version
        else:
            self._version_suffix = '.prod.%s' % self._app_version

        self.mca_handler = mcahandler.MCAHandler(self)
        self.business_handler = businesshandler.BusinessHandler(self)
        static_handler = statichandler.StaticHandler(self)
        shoppingcart_handler = shoppingcarthandler.ShoppingCartHandler(self)
        signin_handler = signinhandler.SigninHandler(self)
        dashboard_handler = userdashboardhandler.UserDashboardHandler(self)
        sitemap_handler = sitemaphandler.SitemapHandler(self)
        misc_handler = mischandlers.MiscHandler(self)
        search_handler = advancedsearchhandler.AdvancedSearchHandler(self)
        comparator_handler = comparatorhandler.ComparatorHandler(self)

        self.templatefiles.update(static_handler.get_templates_list())
        self.templatefiles.update(shoppingcart_handler.get_templates_list())
        self.templatefiles.update(signin_handler.get_templates_list())
        self.templatefiles.update(self.mca_handler.get_templates_list())
        self.templatefiles.update(self.business_handler.get_templates_list())
        self.templatefiles.update(dashboard_handler.get_templates_list())
        self.templatefiles.update(sitemap_handler.get_templates_list())
        self.templatefiles.update(misc_handler.get_templates_list())
        self.templatefiles.update(search_handler.get_templates_list())
        self.templatefiles.update(comparator_handler.get_templates_list())

        #register actions
        #static pages
        self._registerAction('homepage',static_handler.get_homepage)
        self._registerAction('about',static_handler.get_aboutpage)
        self._registerAction('tos',static_handler.get_terms_of_service)
        # self._registerAction('faq',static_handler.get_faq_page)
        self._registerAction('privacy',static_handler.get_privacy_page)
        self._registerAction('price-and-plans', static_handler.get_price_and_plans_page)
        self._registerAction('benefits', static_handler.get_benefits_page)
        self._registerAction('demos-and-guides', static_handler.get_demos_and_guides_page)
        self._registerAction('disclaimer', static_handler.get_disclaimer_page)

        ## old URLs redirecting to new ones
        self._registerAction('companyfinancialspackages', static_handler.redirect_to_benefits_page)
        self._registerAction('companyresearchreport', static_handler.redirect_to_benefits_page)
        self._registerAction('company360plans', static_handler.redirect_to_price_and_plans)
        self._registerAction('company360lite', static_handler.redirect_to_price_and_plans)
        self._registerAction('company360', static_handler.redirect_to_price_and_plans)

        # different aliases for static blog pages on website
        for category in misc_handler.get_blog_categories():
            self._registerAction(category, misc_handler.get_blog_page)

        # company 360 lite pages
        # self._registerAction('start360litetrial', shoppingcart_handler.start_360_lite_trial)

        #mca stuff
        self._registerAction('company', self.business_handler.get_business_page)
        self._registerAction('downloadexcel',self.business_handler.download_excel_file)
        self._registerAction('downloadpptreport',self.business_handler.download_pptx_file)
        self._registerAction('director', self.business_handler.get_director_page)
        self._registerAction('getcompanydocument', self.business_handler.get_company_document)

        self._registerAction('cnamesearch', self.getCompanyNames)
        self._registerAction('visualizationdata',self.mca_handler.getVisualizationData)

        self._registerAction('companylist', self.mca_handler.handle_company_list_path)
        self._registerAction('pluscompany',self.mca_handler.getPlusCompanyInfoPage)

        # TODO: triage for retirement
        self._registerAction('basiccompanyinfo',self.mca_handler.handle_old_company_info_path)
        self._registerAction('companyinfo',self.mca_handler.handle_old_company_info_path)

        self._registerAction('basicsignatoryinfo',self.mca_handler.getBasicSignatoryInformation)
        self._registerAction('findcompany',self.mca_handler.findCompany)
        self._registerAction('browsecompanies',self.mca_handler.getBrowseCompaniesPage)
        self._registerAction('getfinancialreports', self.mca_handler.getFinancialReports)

        #information pages
        #self._registerAction('search',self.getRunSearchResults) #TODO: bring this back
        self._registerAction('getdocument',self.getDocument)   ##this is for stored reports etc (not MCA documents per se)

        #search related
        self._registerAction('finder', search_handler.get_advanced_search_page)

        #shopping cart related
        #self._registerAction('ConfirmTransaction',self.getConfirmTransactionPage)
        self._registerAction('viewcart',shoppingcart_handler.getShoppingCartPage)
        self._registerAction('removeitemfromcart',shoppingcart_handler.removeProductFromShoppingCart)
        self._registerAction('confirmemail',shoppingcart_handler.getCheckoutPage)
        self._registerAction('checkout',shoppingcart_handler.getCheckoutPage)
        self._registerAction('redeemcoupon',shoppingcart_handler.get_apply_coupon_to_order_response)
        self._registerAction('canceltransaction',shoppingcart_handler.getCancelTransaction)
        self._registerAction('PaymentConfirmation',shoppingcart_handler.get_payment_status_redirection)
        self._registerAction('payment',shoppingcart_handler.proceedForPayment)
        self._registerAction('razorpay', shoppingcart_handler.get_razorpay_response)
        self._registerAction('paymentsuccess', shoppingcart_handler.getPaymentConfirmationPage)
        self._registerAction('paymentfailure', shoppingcart_handler.getPaymentConfirmationPage)
        self._registerAction('paymentfailurefeedback', shoppingcart_handler.get_payment_failure_feedback)
        self._registerAction('requestdashboardunlock', shoppingcart_handler.request_dashboard_unlock)

        self._registerAction('orderinfo', shoppingcart_handler.get_order_history)
        self._registerAction('taxinvoice', shoppingcart_handler.get_tax_invoice)
        self._registerAction('getorderresources', shoppingcart_handler.get_order_resources)
        self._registerAction('orderdocuments', shoppingcart_handler.get_documents_download_page)
        self._registerAction('downloaddocument', shoppingcart_handler.get_order_document_download_link)
        #buy documents related
        self._registerAction('buyfinancials', shoppingcart_handler.get_buy_company_financials)
        self._registerAction('buyproduct', shoppingcart_handler.get_buy_product_response)
        self._registerAction('buyitemizedproduct', shoppingcart_handler.get_buy_itemized_product)

        #signin/signup related - ALL DONE
        self._registerAction('login',signin_handler.getLoginPage)
        self._registerAction('logoff',signin_handler.getLogoffPage)
        self._registerAction('signup',signin_handler.getSignupPage)
        self._registerAction('createaccount', signin_handler.getCreateAccountResponse)
        self._registerAction('activateaccount',signin_handler.getAccountActivationPage)
        self._registerAction('forgotpassword',signin_handler.getForgotPasswordPage)
        self._registerAction('loginstatus',signin_handler.checkLoggedinStatus)
        self._registerAction('resetpassword',signin_handler.getResetPasswordResponse)

        self._registerAction('autologin', self.autologin)

        self._registerAction('dashboard', dashboard_handler.get_user_dashboard)
        # self._registerAction('account-settings', dashboard_handler.get_account_settings_page)
        self._registerAction('lists', dashboard_handler.get_lists_page)

        self._registerAction('updateaccountinfo',dashboard_handler.get_update_account_info_response)

        # Favorite list management routes
        self._registerAction('addcompanytolist', dashboard_handler.add_company_to_list)
        self._registerAction('deletecompanyfromlist', dashboard_handler.delete_company_from_list)
        self._registerAction('createnewlist', dashboard_handler.create_new_list)
        self._registerAction('getallcompaniesfromlist', dashboard_handler.get_all_companies_from_list)
        self._registerAction('getalllists', dashboard_handler.get_all_lists)
        self._registerAction('deletelist', dashboard_handler.delete_list)
        self._registerAction('filtercompany', dashboard_handler.filter_company)

        # Comparator endpoints
        self._registerAction('comparator', comparator_handler.get_comparator_page)
        self._registerAction('comparatordata', self.business_handler.get_comparator_data)
        self._registerAction('savecomparator', dashboard_handler.save_comparator)
        self._registerAction('getcomparatornames', dashboard_handler.get_comparator_names)            
        self._registerAction('deletecomparator', dashboard_handler.delete_comprator_for_user)
        self._registerAction('updatecomparatorname', dashboard_handler.update_comparator_name)
        self._registerAction('getsavedcomparator', dashboard_handler.get_saved_comparator)

        self._registerAction('beacon',self.get_beacon_image)

        self._registerAction('adminaccess', self.enable_admin_access)
        self._registerAction('devaccess', self.enable_dev_access)
        self._registerAction('adminmachine', self.admin_machine_management)

        self.__jinjaenv = Environment(loader=PackageLoader('toflerweb','templates'))
        self.__jinjaenv.globals.update(
            unicode_decode=formatter.unicode_decode
        )
        self.__jinjaenv.globals.update(
            make_human_amount=formatter.make_human_amount
        )

        #sitemap
        self._registerAction('sitemap', sitemap_handler.handle_request)

        #load the blank invisible pixel
        f = open('/var/www/images/spacer.gif','rb')
        self.invisible_pixel = f.read()
        f.close()

    def checkValidUTF8(self,chkstring):
        if type(chkstring) is str:
            return True
        try:
            chkstring.decode('utf-8')
        except UnicodeDecodeError:
            return False
        return True

    #limit rate specifies the time required to elapse between each request
    def rateLimit(self, segment, limitrate, environ):
        try:
            sourceip = environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
        except KeyError:
            sourceip = environ['REMOTE_ADDR']

        #check against whitelist
        #right now do the dirty thing - this is Google
        if environ['is_google']:
            return True

        if (sourceip == "106.51.244.112" or sourceip == "202.83.18.222"):
            return False

        now = datetime.datetime.now()
        lastaccessed = Common.get_from_memcache('%s:%s'%(segment,sourceip))
        Common.put_in_memcache('%s:%s'%(segment,sourceip),now)
        if (lastaccessed is None):
            return True
        elif ((now - lastaccessed).seconds >= limitrate):
            return True

        return False

    def IsSpecialBot(self, user_agent):
        return False
        ## Special bots for ScreamingFrog/InfiDigit
        special_bots = [
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.120 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        ]
        for bot in special_bots:
            if bot == user_agent:
                return True
        return False

    def dailyAccessLimit(self, segment, limitrate, environ):
        try:
            sourceip = environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
        except KeyError:
            sourceip = environ['REMOTE_ADDR']

        #check against whitelist
        #right now do the dirty thing - this is Google
        if environ['is_google']:
            return True

        try:
            has_referer = environ['HTTP_REFERER']
        except:
            useragent = environ['HTTP_USER_AGENT']
            if useragent.startswith('python'):
                limitrate = min(limitrate, 5)

        now = datetime.datetime.today()
        key = "%s:DAILY:%s" % (segment, sourceip)
        accessstats = Common.get_from_memcache(key)
        if (accessstats is None):
            Common.put_in_memcache(key,(now,1))
            return True
        else:
            if ((now - accessstats[0]).days >= 1):
                Common.put_in_memcache(key,(now,1))
                return True
            else:
                #print "Pages Accessed: %s" % accessstats[1]
                Common.put_in_memcache(key,(accessstats[0],accessstats[1]+1))
                if (accessstats[1] > limitrate):
                    useragent = environ['HTTP_USER_AGENT']
                    return self.IsSpecialBot(useragent)
                else:
                    return True

    #could parse_qs do a better job
    #could be a security hole. Don't know
    #SECURITY
    def getPostData(self, environ):
        post = {}
        data = ''
        if 'wsgi.input' in environ:
            postdata = environ['wsgi.input']
            data = postdata.read()
        else:
            return post
        if 'CONTENT_TYPE' in environ:
            content_type = environ['CONTENT_TYPE']
            if content_type.startswith('application/json'):
                try:
                    post = json.loads(data)
                except:
                    pass
                return post
            elif content_type.startswith('text/plain; charset=UTF-8'):
                post = data.decode()
                return post
            elif content_type.startswith('application/x-www-form-urlencoded'):
                post = parse_qs(data.decode())
                return post
        try:
            post = parse_qs(data.decode())
        except:
            data = StringIO(data)
            post = FieldStorage(fp=data, environ=environ, keep_blank_values=False)
            data = {}
            keys = list(post.keys())
            for key in keys:
                if isinstance(post[key], list):
                    inputs = []
                    for item in post[key]:
                        if item.filename is not None:
                            inputs.append((item.filename, item.value))
                        else:
                            inputs.append(item.value)
                    data[key] = inputs
                else:
                    if post[key].filename is not None:
                        data[key] = [(post[key].filename, post[key].value)]
                    else:
                        data[key] = [post[key].value]
            post = data
        return post

    def getEncodedPostData(self, environ):
        post = {}
        postdata = environ['wsgi.input']
        data = postdata.read()
        data = StringIO(data)
        post = FieldStorage(fp=data, environ=environ, keep_blank_values=False)
        return post

    def getStandardHeaders(self,outputlength):
        ''' Return a standard text/html header to be sent back to the webserver. '''
        return [('Content-type','text/html; charset=UTF-8'),('Content-Length',str(outputlength))]

    def getStaticPage(self, template=None, session=None):
        dictionary = {}
        status, headers, output = self.getTemplatizedOutput(template, dictionary, session)
        return status, headers, output

    def getTemplatizedOutput(self,template,dictionary, session=None):
        user_info = self._get_user_profile_info(session)
        user_auth = self._get_user_authorization_list(session)
        dictionary['user_info'] = user_info
        dictionary['user_auth'] = user_auth
        dictionary['_cdn_config'] = self._cdn_config
        dictionary['_app_version'] = self._app_version
        dictionary['_version_suffix'] = self._version_suffix
        dictionary['_logged_in'] = False
        if user_info is not None:
            dictionary['_logged_in'] = True if user_info.get('userid') else False
        ## Temporary
        dictionary['_disable_ads'] = True
        if (template not in self.templatefiles):
            status = '500 Internal Server Error'
            output = 'Unknown Template. If you see this page, please let us know at tofler@tofler.in'
            headers = self.getStandardHeaders(len(output))
            return status, headers, output

        jinjatemplate = self.__jinjaenv.get_template(self.templatefiles[template])

        missing_type_templates = {
            'CINNotFound', 'DINNotFound', 'ErrorPage'
        }

        output = jinjatemplate.render(dictionary).encode('utf8','ignore')
        if template in missing_type_templates:
            status = '404 Not Found'
        else:
            status = '200 OK'
        headers = self.getStandardHeaders(len(output))
        return status, headers, output

    def getAjaxifiedOutput(self,responseobject):
        def ajaxhandler(obj):
            if type(obj) is bytes:
                obj = obj.decode('utf8')
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                return obj
        output = json.dumps(responseobject,default=ajaxhandler)
        output = output.encode('utf8')
        headers = [('Content-type','application/json'),('Content-Length',str(len(output)))]
        status = '200 OK'
        return status, headers, output

    def urlize(self, text):
        splchrs = ["'", '.', ',', '"', ';', '(', ')', '`', '%', '[', ']', '+', '=', '*', ':', '/', '?', '!']
        text = text.lower()
        for char in splchrs:
            text = text.replace(char, ' ')
        text = text.replace('&', ' and ')
        text = text.replace('@', ' at ')
        text = text.encode('ascii', 'ignore').decode('ascii')
        text = '-'.join(text.split())
        return text

    def _get_user_profile_info(self, session):
        if session is None:
            return None
        sessioncode = 'USERCODE:%s' % session
        user_info = Common.get_from_memcache(sessioncode)
        if user_info is None:
            sessionuser = pytoflershim.checkSessionLoggedin(session)
            if sessionuser:
                user_info = pytoflershim.get_user_profile_info(sessionuser)
                user_info['item_count'] = pytoflershim.get_cart_item_count(session, sessionuser)['itemcount']
                user_info['userid'] = sessionuser
            else:
                user_info = {}
                user_info['item_count'] = pytoflershim.get_cart_item_count(session, False)['itemcount']
            Common.put_in_memcache(sessioncode, user_info)
        return user_info

    def _get_user_authorization_list(self, session):
        return pytoflershim.get_user_authorization_list(session, cache_lookup=True)

    def _reset_user_profile_info_cache(self, session):
        sessioncode = 'USERCODE:%s' % session
        Common.put_in_memcache(sessioncode, None)
        sessioncode = "AUTHINFO:%s" % session
        Common.put_in_memcache(sessioncode, None)

    def get_user_special_code(self, sessionuser):
        sessionusercode = 'USERCODE:%s' % sessionuser
        special_code = Common.get_from_memcache(sessionusercode)
        if special_code is None:
            special_code = pytoflershim.get_special_user_code(sessionuser)
            Common.put_in_memcache(sessionusercode, special_code)
        return special_code

    def reset_all_user_sessions(self, session):
        if session is None:
            return
        sessionuser = pytoflershim.checkSessionLoggedin(session)
        also_reset_sessions = pytoflershim.get_all_sessions_of_user(sessionuser)
        if also_reset_sessions is not None:
            for reset_session in also_reset_sessions:
                if session != reset_session['sessionid']:
                    self._reset_user_profile_info_cache(str(reset_session['sessionid']))

    def _get_site_config(self, cfg_property):
        query = """SELECT value FROM tofler_site_config WHERE property = %s"""
        response = Common.execute_query(query, cfg_property)
        if len(response) > 0:
            return json.loads(response[0]['value'])
        return {}

    def get_beacon_image(self,environ,getdata,postdata,session):
        Logging.logBeacon(environ,getdata)
        status = '200 OK'
        response_headers = [('Content-type','image/gif'),('Content-Length',str(len(self.invisible_pixel)))]
        return status, response_headers, self.invisible_pixel

    def getTooManyRequestsPage(self):
        status, headers, output = self.getTemplatizedOutput('ErrorPage',{'error':"Slow down. You're going too fast. Please keep in mind that automatic/bulk crawling/downloading of data is against the terms of service of this website. If you are not using an automated system, please try again in a few seconds. Thanks!"})
        status = '429 Too Many Requests'
        return status, headers, output

    def getIPBlockedPage(self,environ):
        try:
            sourceip = environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
        except KeyError:
            sourceip = environ['REMOTE_ADDR']
        errorstring = "Service Unavailable. It seems that there have been too many accesses from your IP %s. This could be because of a virus or malware on your computer or network. If you think your IP has been blocked incorrectly, please feel free to get in touch with us at webmaster@tofler.in citing the IP address mentioned here. Thanks!" % sourceip
        status, headers, output = self.getTemplatizedOutput('ErrorPage',{'error':errorstring})
        status = '503 Service Unavailable'
        return status, headers, output

    def getCompanyNames(self,environ,getdata,postdata,session):
        namestr = postdata.get('cname',[''])[0]
        validator = postdata.get('nonce',[''])[0]
        checkstring = hashlib.md5('a{}'.format(namestr).encode('utf8')).hexdigest()
        if validator != checkstring:
            output = json.dumps('Unauthorized access')
            headers = [('Content-type','text/html'),('Content-Length',str(len(output)))]
            status = '401 Unauthorized'
            return status, headers, output
        return self.mca_handler.getCompanyNames(environ, getdata, postdata, session)

    def redirect_permanently_to_homepage(self,environ,getdata,postdata,session):
        return self.redirect_to_specific_page('/', permanent=True)

    def redirectToLoginPage(self,url=None,cookieheader=None):
        status = '302 Moved Temporarily'
        doc = ''
        headers = self.getStandardHeaders(len(doc))
        headers.append((
            'Location', '/login?redirecturl={}'.format(url)))
        if cookieheader is not None:
            for header in cookieheader:
                headers.append(header)
        return status, headers, doc

    def redirectToCheckoutPage(self):
        status = '302 Moved Temporarily'
        doc = ''
        headers = self.getStandardHeaders(len(doc))
        headers.append(('Location','/checkout'))
        return status, headers, doc

    def redirectToShoppingCartPage(self):
        status = '302 Moved Temporarily'
        doc = ''
        headers = self.getStandardHeaders(len(doc))
        headers.append(('Location','/viewcart'))
        return status, headers, doc

    def redirect_to_specific_page(self, url, permanent=False):
        status = '302 Moved Temporarily'
        if permanent:
            status = '301 Moved Permanently'
        doc = ''
        headers = self.getStandardHeaders(len(doc))
        headers.append(('Location', url))
        return status, headers, doc

    def get_footer_companies_list(self, list_name):
        query = '''
            SELECT footer_content FROM toflerweb_footer_companies_list
            WHERE listname = %s
        '''
        response = Common.execute_query(query, list_name)
        if len(response) == 0:
            return None
        else:
            try:
                return json.loads(response[0]['footer_content'])
            except:
                return None

    def get_footer_directors_list(self, start, count):
        query = '''
            SELECT name, din FROM mca_famous_directors
            LIMIT %s, %s
        '''
        return Common.execute_query(query, (start, count))

    def getRunSearchResults(self,environ,getdata,postdata,session):
        if (not self.dailyAccessLimit('BASICSEARCH',limitrate=200,environ=environ)):
            return self.getIPBlockedPage(environ)
        return self.mca_handler.getBasicSearchResults(environ,getdata,postdata,session)

    def getDocument(self,environ,getdata,postdata,session):
        '''this function supports the /pages/ idiom. Do not Disable!!'''

        #ideally check for authorization etc
        docid = getdata.get('docid',['None'])[0]
        print("Fetching document %s" % docid)
        details = pytoflershim.getDocument(docid)
        if (details is None):
            status = '404 Not Found'
            doc = 'Document not found'
            headers = [('Content-type','text/html'),('Content-Length',str(len(doc)))]
            return status, headers, doc
        filetype = details['Filetype']
        filename = details['Filename']
        compressed = details['Compressed']
        doc = details['Document']
        headers = []
        if (not (filetype == 'html')):
            headers.append(('Content-type','application/%s' % str(filetype)))
            headers.append(('Content-Disposition','attachment; filename="%s"' % str(filename)))
        else:
            headers.append(('Content-type','text/html'))
        if (compressed):
            headers.append(('Content-Encoding','gzip'))
        headers.append(('Content-Length',str(len(doc))))
        status = '200 OK'
        return status, headers, doc

    def autologin(self, environ, getdata, postdata, session):
        path = getdata.get('path', [None])[0]
        action = getdata.get('action', [None])[0]
        fullpath = '/{}/{}'.format(action, path)
        if session is None:
            # the user has just come to the page.
            # we need to reload the page to get the session cookie
            return self.redirect_to_specific_page(fullpath)

        items = path.split('/')
        if len(items) < 2:
            return self.getTemplatizedOutput('ErrorPage', {
                'error': 'No login credentials provided'},
                session)
        userid = items[0]
        try:
            userid = int(userid)
        except:
            return self.getTemplatizedOutput(
                'ErrorPage', {'error': 'Invalid login credentials'})
        token = items[1]
        success = pytoflershim.login_user_with_token(
            userid, token, session)
        if success:
            return self.redirect_to_specific_page(
                'http://plus.tofler.in/dashboard')
        else:
            return self.getTemplatizedOutput('ErrorPage', {
                'error': 'Login failed'
                })


    def extractCookie(self,environ):
        cookies = environ.get('HTTP_COOKIE','').split(';')
        for cookie in cookies:
            splitted = cookie.split('=')
            if (not len(splitted) == 2):
                continue
            if (splitted[0].strip() == 'ToflerSession'):
                return splitted[1].strip()
        return None

    def get_ist_time(self):
        now = datetime.datetime.now() + datetime.timedelta(hours=5.5)
        return now

    def enable_admin_access(self, environ, getdata, putdata, session):
        '''This whole method is ugly ugly. It can break at any time'''
        '''But we don't care because this is only for internal use'''

        user_email = pytoflershim.getUserEmail(
                pytoflershim.checkSessionLoggedin(session))
        if user_email.split('@')[1] != 'tofler.in' and user_email != 'parijatgarg@gmail.com':
            return self.getTemplatizedOutput('404Error', {}, session)

        adminmanagement.remove_temporary_iprange_rules_from_security_group(
            'sg-0b62725644fc170dc')
        adminmanagement.whitelist_ips_in_firewall(
            'sg-0b62725644fc170dc', environ['sourceip'], [80]
        )

        return self.getTemplatizedOutput(
            'ErrorPage', {
            'error':"It has been done."
            }, session
        )

    def enable_dev_access(self, environ, getdata, putdata, session):
        '''This whole method is ugly ugly. It can break at any time'''
        '''But we don't care because this is only for internal use'''

        user_email = pytoflershim.getUserEmail(
                pytoflershim.checkSessionLoggedin(session))
        if user_email not in ['parijatgarg@gmail.com', 'tofler@squareboat.com']:
            return self.getTemplatizedOutput('404Error', {}, session)

        adminmanagement.remove_temporary_iprange_rules_from_security_group(
            'sg-0afbd42148383c102')
        adminmanagement.whitelist_ips_in_firewall(
            'sg-0afbd42148383c102', environ['sourceip'], [80, 81, 82, 83, 85, 86, 22, 443]
        )

        return self.getTemplatizedOutput(
            'ErrorPage', {
            'error':"It has been done."
            }, session
        )

    def admin_machine_management(self, environ, getdata, putdata, session):
        user_email = pytoflershim.getUserEmail(
                pytoflershim.checkSessionLoggedin(session))
        if user_email not in ['parijatgarg@gmail.com', 'mahesh@tofler.in']:
            return self.getTemplatizedOutput('404Error', {}, session)
        action = getdata.get('command', [None])[0]
        state = adminmanagement.get_admin_machine_status()
        if action == 'stop':
            if state == 'running':
                adminmanagement.stop_admin_machine()
                state = adminmanagement.get_admin_machine_status()
                return self.getTemplatizedOutput(
                    'ErrorPage', {
                        'error': 'Machine is being stopped. Status: {}'.format(state)
                    }, session
                )
            else:
                return self.getTemplatizedOutput(
                    'ErrorPage', {
                        'error': 'Cannot stop machine. Try again later. Status: {}'.format(state)
                    }, session
                )
        elif action == 'start':
            if state == 'stopped':
                adminmanagement.start_admin_machine()
                state = adminmanagement.get_admin_machine_status()
                return self.getTemplatizedOutput(
                    'ErrorPage', {
                        'error': 'Machine is being started. Status: {}'.format(state)
                    }, session
                )
            else:
                return self.getTemplatizedOutput(
                    'ErrorPage', {
                        'error': 'Cannot start machine. Try again later. Status: {}'.format(state)
                    }, session
                )
        else:
            return self.getTemplatizedOutput(
                'ErrorPage', {
                    'error': 'Status: {}'.format(state)
                }, session
            )

    def webcall(self, environ, start_response):
        sourceip = None
        try:
            sourceip = environ['HTTP_X_FORWARDED_FOR'].split(',')[-1].strip()
        except KeyError:
            sourceip = environ['REMOTE_ADDR']
        if self._bot_pattern.match(sourceip):
            environ['is_google'] = True
        else:
            environ['is_google'] = False

        if not environ['is_google']:
            try:
                Logging.logHit(environ)             #Log the hit to database
            except:
                '''This only really happens when there is an IPv6 address'''
                pass

        #allow = self.rateLimit('OVERALL',limitrate=1,environ=environ)      #check if this request is abusive
        #if (allow is False):
        #   return self.getTooManyRequestsPage()
        environ['sourceip'] = sourceip
        environ['useragent'] = environ.get('HTTP_USER_AGENT','')
        cookieheader = None
        toflersession = self.extractCookie(environ)

        if ((not toflersession or not pytoflershim.checkSessionExists(toflersession)) and not environ['is_google']):
            session = pytoflershim.createNewSession(sourceip)
            expires = time.time() + 365 * 24 * 3600
            expiry = time.strftime("%a, %d-%b-%Y %T GMT", time.gmtime(expires))
            cookieheader = [
                ('Set-Cookie','ToflerSession=%s;expires=%s;path=/'%(session,expiry)),
                ('Set-Cookie','ToflerSession=%s;expires=%s;path=/;domain=.tofler.in'%(session,expiry))
                ]

        getdata = parse_qs(environ['QUERY_STRING'])
        try:
            postdata = self.getPostData(environ)
        except:
            postdata = self.getEncodedPostData(environ)
        action = getdata.get('action',['None'])[0]
        try:
            runfunction = self.actions[action]
        except KeyError:
            Logging.log('ToflerWeb does not know what to do on Action request %s' % action)
            return self.getTemplatizedOutput('404Error', {}, toflersession)
            #headers = self.getStandardHeaders(len(self.defaultOutput))
            #return self.defaultStatus, headers, self.defaultOutput

        #run the chosen function
        status = None
        headers = None
        output = None

        try:
            status, headers, output = runfunction(environ,getdata,postdata,toflersession)
        except:
            traceback.print_exc()
            return self.getTemplatizedOutput('500Error',{})

        if cookieheader is not None:
            for header in cookieheader:
                headers.append(header)
        if type(output) is not bytes:
            output = output.encode('utf8')
        return status, headers, output