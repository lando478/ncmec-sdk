# ncmec-sdk

An unofficial Python SDK for the [NCMEC Poster API](https://posterapi.ncmec.org) — the National Center for Missing & Exploited Children.

NCMEC does not provide an official Python client. This SDK makes it easy to integrate missing children poster data into your Python applications.

> **Note:** Access to the NCMEC Poster API requires credentials from NCMEC. This SDK is not affiliated with or endorsed by NCMEC.

---

## Installation
```bash
pip install ncmec-sdk
```

---

## Quick Start
```python
from ncmec_sdk import NCMECClient

client = NCMECClient("your_client_id", "your_client_secret")
client.authenticate()

# Get a list of posters
posters = client.get_posters(limit=10)
for poster in posters:
    print(poster.caseNumber, poster.children[0].firstName)

# Search by state
posters = client.get_posters(missing_state="TX")

# Get a specific poster
poster = client.get_poster("NCMC", "2077508")

# Get a photo
photo = client.get_poster_photo("NCMC", "2077508", "md5hashhere")

# Get organization logo
logo_bytes = client.get_organization_logo("NCMC")
with open("logo.png", "wb") as f:
    f.write(logo_bytes)
```

---

## Available Methods

| Method | Description |
|--------|-------------|
| `authenticate()` | Authenticate and store token |
| `get_posters(**filters)` | Search paginated list of posters |
| `get_poster(org_code, case_number)` | Get a specific poster |
| `update_poster(org_code, case_number, poster)` | Update a poster |
| `delete_poster(org_code, case_number)` | Delete a poster |
| `get_poster_photo(org_code, case_number, md5)` | Get a photo by MD5 hash |
| `get_organization_logo(org_code)` | Get organization logo as bytes |
| `rotate_secret_key()` | Rotate your API secret |

---

## Search Filters

`get_posters()` supports extensive filtering:
```python
posters = client.get_posters(
    # Pagination
    skip=0,
    limit=20,

    # Child filters
    child_first_name="John",
    child_last_name="Doe",

    # Location filters
    missing_state="CA",
    missing_city="Los Angeles",
    found_state="TX",

    # Date filters
    missing_date_from="2024-01-01T00:00:00Z",
    missing_date_to="2024-12-31T00:00:00Z",

    # Sorting
    sort_type="lastModified",
    sort_order="desc",
)
```

---

## Models

All responses are deserialized into typed dataclasses:

- `Poster`
- `Child`
- `Companion`
- `Photo`
- `Contact`
- `Location`
- `PosterDescription`

---

## License

MIT