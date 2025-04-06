from requests.exceptions import RequestException

class ApythingException(Exception):
    pass

class HttpUtil:
    @staticmethod
    def safe_request(session, url, headers, method='GET', data=None, files=None):
        try:
            response = session.request(method, url, json=data, headers=headers, files=files)
        except RequestException as e:
            # Handle network or HTTP request errors
            raise ApythingException("Error: request failed") from e
        
        if response.ok:
            try:
                return response.json()
            except ValueError:
                # Some endpoints do not return any json data, only HTTP codes
                return response.ok
        else:
            raise ApythingException(f"Error: request returned {response.status_code} code\nResponse: {response.text}")
