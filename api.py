import requests
from config import Config
import urllib
from models import Search

class SearchAPI(object):
    def __init__(self, api):
        self._api = api
    
    def search_items(self, term, **kwargs):
        data = dict()
        for field in ["item_types", "fields", "search_for_related_items", "exact_match", "include_fields", "start", "limit"]:
            if kwargs.get(field):
                data[field] = kwargs.get(field)
        url = "itemSearch?term=%s&%s" % (
            term,
            urllib.parse.urlencode(data)
        )
        search_result = Search(**self._api._get(url))
        import pdb; pdb.set_trace()
        return search_result.get_item(kwargs.get("item_types"))

class API(object):
    def __init__(self, *args, **kwargs):
        """Creates a wrapper to perform API actions.
        Arguments:
          domain:    the Freshdesk domain (not custom). e.g. company.freshdesk.com
          api_key:   the API key
        Instances:
          .tickets:  the Ticket API
        """

        self._api_prefix = "https://api.pipedrive.com/v1/{}&api_token=%s" % Config.PD_API_KEY
        self.headers = {'Content-Type': 'application/json'}

        self.search = SearchAPI(self)
        """
        self.tickets = TicketAPI(self)
        self.comments = CommentAPI(self)
        self.contacts = ContactAPI(self)
        self.companies = CompanyAPI(self)
        self.groups = GroupAPI(self)
        self.customers = CustomerAPI(self)
        self.agents = AgentAPI(self)
        self.roles = RoleAPI(self)
        self.ticket_fields = TicketFieldAPI(self)
        """
        # if domain.find('freshdesk.com') < 0:
        #     raise AttributeError('Freshdesk v2 API works only via Freshdesk'
        #                          'domains and not via custom CNAMEs')
        # self.domain = domain

    def _action(self, req):
        try:
            j = req.json()
        except ValueError as e:
            j = {"error": str(e)}

        """
        error_message = 'PD Request Failed'
        # To - Do : Map pd errors here
        if 'errors' in j:
            error_message = '{}: {}'.format(j.get('description'), j.get('errors'))
        elif 'message' in j:
            error_message = j['message']
            
        # To - Do : Create these error classes in errors.py
        if req.status_code == 400:
            raise FreshdeskBadRequest(error_message)
        elif req.status_code == 401:
            raise FreshdeskUnauthorized(error_message)
        elif req.status_code == 403:
            raise FreshdeskAccessDenied(error_message)
        elif req.status_code == 404:
            raise FreshdeskNotFound(error_message)
        elif req.status_code == 429:
            raise FreshdeskRateLimited(
                '429 Rate Limit Exceeded: API rate-limit has been reached until {} seconds. See '
                'http://freshdesk.com/api#ratelimit'.format(req.headers.get('Retry-After')))
        elif 500 < req.status_code < 600:
            raise FreshdeskServerError('{}: Server Error'.format(req.status_code))

        # Catch any other errors
        try:
            req.raise_for_status()
        except HTTPError as e:
            raise FreshdeskError("{}: {}".format(e, j))
        """
        return j

    def _get(self, url, params={}):
        """Wrapper around request.get() to use the API prefix. Returns a JSON response."""
        req = requests.get(self._api_prefix + url, params=params)
        return self._action(req)

    def _post(self, url, data={}, **kwargs):
        """Wrapper around request.post() to use the API prefix. Returns a JSON response."""
        req = requests.post(self._api_prefix + url, data=data, **kwargs)
        return self._action(req)

    def _put(self, url, data={}):
        """Wrapper around request.put() to use the API prefix. Returns a JSON response."""
        req = requests.put(self._api_prefix + url, data=data)
        return self._action(req)

    def _delete(self, url):
        """Wrapper around request.delete() to use the API prefix. Returns a JSON response."""
        req = requests.delete(self._api_prefix + url)
        return self._action(req)