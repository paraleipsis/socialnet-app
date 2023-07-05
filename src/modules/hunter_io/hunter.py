from modules.client.request_handler import ClientRequestHandler
from modules.hunter_io.exceptions import HunterApiError
from modules.logger.logs import logger


class HunterHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_params = {'api_key': api_key}
        self.base_endpoint = 'https://api.hunter.io/v2/{}'

    async def email_verifier(self, email):
        """
        Verify the existence of a given email address.

        :param email: The email address to check.
        """

        params = {
            'email': email,
            'api_key': self.api_key
        }

        async with ClientRequestHandler() as client:
            response = await client.get_request(
                url=self.base_endpoint.format('email-verifier'),
                params=params
            )

            if response.status != 200:
                logger['error'].error(
                    f'Error verifying email existence with Hunter.io API: {response.status} {response}'
                )
                raise HunterApiError

            data = await response.json()

        return data
