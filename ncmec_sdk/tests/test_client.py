from ncmec_sdk.client import NCMECClient
from ncmec_sdk.models import Poster, Photo
import pytest
from unittest.mock import patch, MagicMock
from dataclasses import asdict


@pytest.fixture
def client():
    c = NCMECClient("test_client_id", "test_client_secret")
    c.access_token = "fake_token"
    c.token_expiry = float("inf")  # never expires during tests
    return c


@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.json.return_value = {"posters": [], "count": 0}  # match real API shape
    mock.raise_for_status.return_value = None
    return mock


# -------------------------
# DEFAULTS
# -------------------------

def test_get_posters_default_params(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_posters()
        _, kwargs = mock_get.call_args
        params = kwargs["params"]

        assert params["skip"] == 0
        assert params["limit"] == 20
        assert params["enableIpGeolocationSearch"] == False
        assert params["geolocationDistanceInMiles"] == 50


# NEW
def test_get_posters_returns_list_of_posters(client, mock_response):
    with patch("requests.get", return_value=mock_response):
        result = client.get_posters()
        assert isinstance(result, list)
        assert all(isinstance(p, Poster) for p in result)


# -------------------------
# PAGINATION
# -------------------------

def test_get_posters_pagination(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_posters(skip=40, limit=10)
        params = mock_get.call_args[1]["params"]

        assert params["skip"] == 40
        assert params["limit"] == 10


# -------------------------
# OPTIONAL PARAMS EXCLUDED WHEN NONE
# -------------------------
@pytest.mark.parametrize("param_name", [
    "languageId", "posterType", "childFirstName", "childLastName",
    "companionFirstName", "companionLastName",
    "missingCity", "missingCounty", "missingState", "missingZip", "missingCountry",
    "foundCity", "foundCounty", "foundState", "foundZip", "foundCountry",
    "missingDate", "missingDateFrom", "missingDateTo",
    "foundDate", "foundDateFrom", "foundDateTo",
    "lastModified", "lastModifiedFrom", "lastModifiedTo",
    "dateCreated", "dateCreatedFrom", "dateCreatedTo",
    "sortType", "sortOrder",
])
def test_none_params_excluded(client, mock_response, param_name):
    """None values should never be sent to the API"""
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_posters()
        params = mock_get.call_args[1]["params"]
        assert param_name not in params


# -------------------------
# OPTIONAL PARAMS INCLUDED WHEN PROVIDED
# -------------------------
@pytest.mark.parametrize("kwarg,api_key,value", [
    ("child_first_name",     "childFirstName",     "John"),
    ("child_last_name",      "childLastName",      "Doe"),
    ("companion_first_name", "companionFirstName", "Jane"),
    ("companion_last_name",  "companionLastName",  "Doe"),
    ("language_id",          "languageId",         "en"),
    ("poster_type",          "posterType",         "MISSING"),
    ("missing_city",         "missingCity",        "Dallas"),
    ("missing_county",       "missingCounty",      "Dallas County"),
    ("missing_state",        "missingState",       "TX"),
    ("missing_zip",          "missingZip",         "75001"),
    ("missing_country",      "missingCountry",     "US"),
    ("found_city",           "foundCity",          "Austin"),
    ("found_county",         "foundCounty",        "Travis County"),
    ("found_state",          "foundState",         "TX"),
    ("found_zip",            "foundZip",           "78701"),
    ("found_country",        "foundCountry",       "US"),
    ("missing_date",         "missingDate",        "2024-01-01T00:00:00Z"),
    ("missing_date_from",    "missingDateFrom",    "2024-01-01T00:00:00Z"),
    ("missing_date_to",      "missingDateTo",      "2024-12-31T00:00:00Z"),
    ("found_date",           "foundDate",          "2024-06-01T00:00:00Z"),
    ("found_date_from",      "foundDateFrom",      "2024-06-01T00:00:00Z"),
    ("found_date_to",        "foundDateTo",        "2024-06-30T00:00:00Z"),
    ("last_modified",        "lastModified",       "2024-01-01T00:00:00Z"),
    ("last_modified_from",   "lastModifiedFrom",   "2024-01-01T00:00:00Z"),
    ("last_modified_to",     "lastModifiedTo",     "2024-12-31T00:00:00Z"),
    ("date_created",         "dateCreated",        "2023-01-01T00:00:00Z"),
    ("date_created_from",    "dateCreatedFrom",    "2023-01-01T00:00:00Z"),
    ("date_created_to",      "dateCreatedTo",      "2023-12-31T00:00:00Z"),
    ("sort_type",            "sortType",           "lastModified"),
    ("sort_order",           "sortOrder",          "desc"),
])
def test_optional_param_included_when_provided(client, mock_response, kwarg, api_key, value):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_posters(**{kwarg: value})
        params = mock_get.call_args[1]["params"]
        assert params[api_key] == value


# -------------------------
# ARRAY PARAMS
# -------------------------

def test_organization_codes_included(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_posters(organization_codes=["ORG1", "ORG2"])
        params = mock_get.call_args[1]["params"]
        assert params["organizationCodes"] == ["ORG1", "ORG2"]


def test_races_included(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_posters(races=["WHITE", "BLACK"])
        params = mock_get.call_args[1]["params"]
        assert params["races"] == ["WHITE", "BLACK"]


def test_organization_codes_excluded_when_none(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_posters()
        params = mock_get.call_args[1]["params"]
        assert "organizationCodes" not in params


def test_races_excluded_when_none(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_posters()
        params = mock_get.call_args[1]["params"]
        assert "races" not in params


# -------------------------
# GEOLOCATION
# -------------------------

def test_geolocation_enabled(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_posters(enable_ip_geolocation_search=True, geolocation_distance_in_miles=100)
        params = mock_get.call_args[1]["params"]
        assert params["enableIpGeolocationSearch"] == True
        assert params["geolocationDistanceInMiles"] == 100


# -------------------------
# AUTH
# -------------------------

def test_get_posters_triggers_auth_if_no_token(mock_response):
    c = NCMECClient("id", "secret")
    # no token set
    with patch.object(c, "authenticate") as mock_auth, \
         patch("requests.get", return_value=mock_response):

        def set_token():
            c.access_token = "fake"
            c.token_expiry = float("inf")

        mock_auth.side_effect = set_token
        c.get_posters()
        mock_auth.assert_called_once()


def test_get_posters_triggers_reauth_if_token_expired(mock_response):
    c = NCMECClient("id", "secret")
    c.access_token = "expired_token"
    c.token_expiry = 0  # already expired

    with patch.object(c, "authenticate") as mock_auth, \
         patch("requests.get", return_value=mock_response):

        def refresh_token():
            c.access_token = "new_token"
            c.token_expiry = float("inf")

        mock_auth.side_effect = refresh_token
        c.get_posters()
        mock_auth.assert_called_once()


# -------------------------
# ERROR HANDLING
# -------------------------

def test_get_posters_raises_on_http_error(client):
    mock = MagicMock()
    mock.raise_for_status.side_effect = Exception("401 Unauthorized")

    with patch("requests.get", return_value=mock):
        with pytest.raises(Exception, match="401 Unauthorized"):
            client.get_posters()


def test_correct_url_called(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_posters()
        url = mock_get.call_args[0][0]
        assert url == "https://posterapi.ncmec.org/Posters"


def test_auth_header_sent(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_posters()
        headers = mock_get.call_args[1]["headers"]
        assert headers["Authorization"] == "Bearer fake_token"
        
        
        
# -------------------------
# GET POSTER
# -------------------------

def test_get_poster_correct_url(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_poster("ORG1", "CASE123")
        url = mock_get.call_args[0][0]
        assert url == "https://posterapi.ncmec.org/Poster/ORG1/CASE123"


# GET POSTER - now returns a Poster object
def test_get_poster_returns_json(client, mock_response):
    with patch("requests.get", return_value=mock_response):
        result = client.get_poster("ORG1", "CASE123")
        assert isinstance(result, Poster)


# UPDATE POSTER - mock returns {"posters": [], "count": 0} not {"total": 0}
def test_update_poster_returns_json(client, mock_response):
    with patch("requests.put", return_value=mock_response):
        poster = Poster(organizationCode="ORG1", caseNumber="CASE123")
        result = client.update_poster("ORG1", "CASE123", poster)
        assert result == {"posters": [], "count": 0}


# DELETE POSTER - same fix
def test_delete_poster_returns_json(client, mock_response):
    with patch("requests.delete", return_value=mock_response):
        result = client.delete_poster("ORG1", "CASE123")
        assert result == {"posters": [], "count": 0}


# GET POSTER PHOTO - now returns a Photo object
def test_get_poster_photo_returns_json(client, mock_response):
    with patch("requests.get", return_value=mock_response):
        result = client.get_poster_photo("ORG1", "CASE123", "abc123md5")
        assert isinstance(result, Photo)


# GET ORGANIZATION LOGO - now returns bytes
def test_get_organization_logo_returns_json(client, mock_response):
    mock_response.content = b"fake_image_bytes"
    with patch("requests.get", return_value=mock_response):
        result = client.get_organization_logo("ORG1")
        assert isinstance(result, bytes)


def test_get_poster_auth_header(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_poster("ORG1", "CASE123")
        assert mock_get.call_args[1]["headers"]["Authorization"] == "Bearer fake_token"


def test_get_poster_raises_on_error(client):
    mock = MagicMock()
    mock.raise_for_status.side_effect = Exception("404 Not Found")
    with patch("requests.get", return_value=mock):
        with pytest.raises(Exception, match="404 Not Found"):
            client.get_poster("ORG1", "CASE123")


# -------------------------
# UPDATE POSTER
# -------------------------

def test_update_poster_correct_url(client, mock_response):
    with patch("requests.put", return_value=mock_response) as mock_put:
        poster = Poster(organizationCode="ORG1", caseNumber="CASE123")
        client.update_poster("ORG1", "CASE123", poster)
        url = mock_put.call_args[0][0]
        assert url == "https://posterapi.ncmec.org/Poster/ORG1/CASE123"


def test_update_poster_sends_json_body(client, mock_response):
    with patch("requests.put", return_value=mock_response) as mock_put:
        poster = Poster(organizationCode="ORG1", caseNumber="CASE123")
        client.update_poster("ORG1", "CASE123", poster)
        body = mock_put.call_args[1]["json"]
        assert body["organizationCode"] == "ORG1"
        assert body["caseNumber"] == "CASE123"




def test_update_poster_raises_on_error(client):
    mock = MagicMock()
    mock.raise_for_status.side_effect = Exception("400 Bad Request")
    with patch("requests.put", return_value=mock):
        with pytest.raises(Exception, match="400 Bad Request"):
            client.update_poster("ORG1", "CASE123", Poster())


# -------------------------
# DELETE POSTER
# -------------------------

def test_delete_poster_correct_url(client, mock_response):
    with patch("requests.delete", return_value=mock_response) as mock_delete:
        client.delete_poster("ORG1", "CASE123")
        url = mock_delete.call_args[0][0]
        assert url == "https://posterapi.ncmec.org/Poster/ORG1/CASE123"


def test_delete_poster_raises_on_error(client):
    mock = MagicMock()
    mock.raise_for_status.side_effect = Exception("404 Not Found")
    with patch("requests.delete", return_value=mock):
        with pytest.raises(Exception, match="404 Not Found"):
            client.delete_poster("ORG1", "CASE123")


# -------------------------
# GET POSTER PHOTO
# -------------------------

def test_get_poster_photo_correct_url(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_poster_photo("ORG1", "CASE123", "abc123md5")
        url = mock_get.call_args[0][0]
        assert url == "https://posterapi.ncmec.org/Poster/ORG1/CASE123/Photo/abc123md5"



def test_get_poster_photo_raises_on_error(client):
    mock = MagicMock()
    mock.raise_for_status.side_effect = Exception("404 Not Found")
    with patch("requests.get", return_value=mock):
        with pytest.raises(Exception, match="404 Not Found"):
            client.get_poster_photo("ORG1", "CASE123", "abc123md5")


# -------------------------
# GET ORGANIZATION LOGO
# -------------------------

def test_get_organization_logo_correct_url(client, mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client.get_organization_logo("ORG1")
        url = mock_get.call_args[0][0]
        assert url == "https://posterapi.ncmec.org/Poster/ORG1/Logo"



def test_get_organization_logo_raises_on_error(client):
    mock = MagicMock()
    mock.raise_for_status.side_effect = Exception("404 Not Found")
    with patch("requests.get", return_value=mock):
        with pytest.raises(Exception, match="404 Not Found"):
            client.get_organization_logo("ORG1")