from modules.clearbit.exceptions import ClearbitApiError
from modules.client.request_handler import ClientRequestHandler
from modules.logger.logs import logger


class ClearbitHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        self.person_endpoint = 'https://person.clearbit.com/v2/people/{}'

    async def email_lookup(self, email):
        """
        Lookup info of a given email address.

        :param email: The email address to check.
        """

        params = {
            'email': email,
            'stream': True
        }

        async with ClientRequestHandler() as client:
            response = await client.get_request(
                url=self.person_endpoint.format('find'),
                params=params,
                headers=self.headers
            )

            if response.status != 200:
                logger['debug'].debug(
                    f'Error lookup email with Clearbit API: {response.status} {response}'
                )
                raise ClearbitApiError

            data = await response.json()

        return data
