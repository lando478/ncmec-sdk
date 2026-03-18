import requests
import time
from typing import Optional, List
from dataclasses import asdict
from dacite import from_dict
from .models import Poster, Photo


class NCMECClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://posterapi.ncmec.org"
        self.access_token = None
        self.token_expiry = 0  # unix timestamp

    def authenticate(self):
        """Authenticate and store token + expiration"""
        payload = {
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }
        try:
            response = requests.post(
                f"{self.base_url}/Auth/Token",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            response.raise_for_status()
            data = response.json()
            self.access_token = data.get("accessToken")
            # expires in 24 hours (API docs say this)
            self.token_expiry = time.time() + (24 * 60 * 60)
            print("Authenticated successfully")
        except Exception as e:
            print(f"Authentication failed: {e}")
            raise

    def _ensure_authenticated(self):
        """Ensure token exists and is not expired"""
        if not self.access_token or time.time() >= self.token_expiry:
            print("Token missing or expired. Re-authenticating...")
            self.authenticate()

    def rotate_secret_key(self):
        self._ensure_authenticated()
        try:
            response = requests.post(
                f"{self.base_url}/Auth/RotateSecret",
                headers=self._headers()
            )
            response.raise_for_status()
            data = response.json()
            print(data)
            self.client_secret = data.get("clientSecret")

        except Exception as e:
            print(f"Error while rotating secret key: {e}")

    def get_posters(
        self,
        # pagination
        skip: int = 0,
        limit: int = 20,
        # organization
        organization_codes: Optional[List[str]] = None,
        language_id: Optional[str] = None,
        poster_type: Optional[str] = None,
        # child filters
        child_first_name: Optional[str] = None,
        child_last_name: Optional[str] = None,
        # companion filters
        companion_first_name: Optional[str] = None,
        companion_last_name: Optional[str] = None,
        # demographics
        races: Optional[List[str]] = None,
        # missing location
        missing_city: Optional[str] = None,
        missing_county: Optional[str] = None,
        missing_state: Optional[str] = None,
        missing_zip: Optional[str] = None,
        missing_country: Optional[str] = None,
        # found location
        found_city: Optional[str] = None,
        found_county: Optional[str] = None,
        found_state: Optional[str] = None,
        found_zip: Optional[str] = None,
        found_country: Optional[str] = None,
        # date filters
        missing_date: Optional[str] = None,
        missing_date_from: Optional[str] = None,
        missing_date_to: Optional[str] = None,
        found_date: Optional[str] = None,
        found_date_from: Optional[str] = None,
        found_date_to: Optional[str] = None,
        last_modified: Optional[str] = None,
        last_modified_from: Optional[str] = None,
        last_modified_to: Optional[str] = None,
        date_created: Optional[str] = None,
        date_created_from: Optional[str] = None,
        date_created_to: Optional[str] = None,
        # sorting
        sort_type: Optional[str] = None,
        sort_order: Optional[str] = None,
        # geolocation
        enable_ip_geolocation_search: bool = False,
        geolocation_distance_in_miles: int = 50,
    ) -> List[Poster]:
        self._ensure_authenticated()
        # Map Python snake_case to API's camelCase, only include non-None values
        params = {
            "skip": skip,
            "limit": limit,
            "enableIpGeolocationSearch": enable_ip_geolocation_search,
            "geolocationDistanceInMiles": geolocation_distance_in_miles,
        }

        optional_params = {
            "languageId": language_id,
            "posterType": poster_type,
            "childFirstName": child_first_name,
            "childLastName": child_last_name,
            "companionFirstName": companion_first_name,
            "companionLastName": companion_last_name,
            "missingCity": missing_city,
            "missingCounty": missing_county,
            "missingState": missing_state,
            "missingZip": missing_zip,
            "missingCountry": missing_country,
            "foundCity": found_city,
            "foundCounty": found_county,
            "foundState": found_state,
            "foundZip": found_zip,
            "foundCountry": found_country,
            "missingDate": missing_date,
            "missingDateFrom": missing_date_from,
            "missingDateTo": missing_date_to,
            "foundDate": found_date,
            "foundDateFrom": found_date_from,
            "foundDateTo": found_date_to,
            "lastModified": last_modified,
            "lastModifiedFrom": last_modified_from,
            "lastModifiedTo": last_modified_to,
            "dateCreated": date_created,
            "dateCreatedFrom": date_created_from,
            "dateCreatedTo": date_created_to,
            "sortType": sort_type,
            "sortOrder": sort_order,
        }
        # Only add params that were actually provided
        params.update({k: v for k, v in optional_params.items() if v is not None})
        # Arrays need special handling — requests sends them as repeated keys
        if organization_codes:
            params["organizationCodes"] = organization_codes
        if races:
            params["races"] = races
        response = requests.get(
            f"{self.base_url}/Posters",
            headers=self._headers(),
            params=params
        )
        response.raise_for_status()
        data = response.json()
        raw_posters = data["posters"]
        return [from_dict(data_class=Poster, data=p) for p in raw_posters]

    def get_poster(self, organization_code: str, case_number: str) -> Poster:
        """GET /Poster/{organizationCode}/{caseNumber}"""
        self._ensure_authenticated()
        response = requests.get(
            f"{self.base_url}/Poster/{organization_code}/{case_number}",
            headers=self._headers()
        )
        response.raise_for_status()
        return from_dict(data_class=Poster, data=response.json())


    def update_poster(self, organization_code: str, case_number: str, poster: Poster) -> dict:
        """PUT /Poster/{organizationCode}/{caseNumber}"""
        self._ensure_authenticated()
        response = requests.put(
            f"{self.base_url}/Poster/{organization_code}/{case_number}",
            headers=self._headers(),
            json=asdict(poster)
        )
        response.raise_for_status()
        return response.json()


    def delete_poster(self, organization_code: str, case_number: str) -> dict:
        """DELETE /Poster/{organizationCode}/{caseNumber}"""
        self._ensure_authenticated()
        response = requests.delete(
            f"{self.base_url}/Poster/{organization_code}/{case_number}",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()


    def get_poster_photo(self, organization_code: str, case_number: str, md5: str) -> Photo:
        """GET /Poster/{organizationCode}/{caseNumber}/Photo/{md5}"""
        self._ensure_authenticated()
        response = requests.get(
            f"{self.base_url}/Poster/{organization_code}/{case_number}/Photo/{md5}",
            headers=self._headers()
        )
        response.raise_for_status()
        return from_dict(data_class=Photo, data=response.json())


    def get_organization_logo(self, organization_code: str) -> bytes:
        """GET /Poster/{organizationCode}/Logo"""
        self._ensure_authenticated()
        response = requests.get(
            f"{self.base_url}/Poster/{organization_code}/Logo",
            headers=self._headers()
        )
        response.raise_for_status()
        return response.content  # raw bytes, not .json()
        
    def _headers(self):
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }