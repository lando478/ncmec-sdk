from .client import NCMECClient
from .models import Poster

class NCMECRepl:
    def __init__(self, client: NCMECClient):
        self.client = client

    def run(self):
        commands = (
            "get_posters, get_poster, update_poster, delete_poster, "
            "get_poster_photo, get_org_logo, rotate_secret_key, exit"
        )
        while True:
            command = input(f"\nEnter command ({commands}): ").strip()

            if command == "get_posters":
                first_name = input("Child first name (or blank): ").strip()
                posters = self.client.get_posters(child_first_name=first_name or None)
                print(posters)

            elif command == "get_poster":
                org_code = input("Organization code: ").strip()
                case_number = input("Case number: ").strip()
                print(self.client.get_poster(org_code, case_number))

            elif command == "update_poster":
                org_code = input("Organization code: ").strip()
                case_number = input("Case number: ").strip()
                poster = Poster(organizationCode=org_code, caseNumber=case_number)
                print(self.client.update_poster(org_code, case_number, poster))

            elif command == "delete_poster":
                org_code = input("Organization code: ").strip()
                case_number = input("Case number: ").strip()
                confirm = input(f"Are you sure you want to delete {org_code}/{case_number}? (yes/no): ").strip()
                if confirm == "yes":
                    print(self.client.delete_poster(org_code, case_number))
                else:
                    print("Cancelled.")

            elif command == "get_poster_photo":
                org_code = input("Organization code: ").strip()
                case_number = input("Case number: ").strip()
                md5 = input("Photo MD5 hash: ").strip()
                print(self.client.get_poster_photo(org_code, case_number, md5))

            elif command == "get_org_logo":
                org_code = input("Organization code: ").strip()
                print(self.client.get_organization_logo(org_code))

            elif command == "rotate_secret_key":
                self.client.rotate_secret_key()

            elif command == "exit":
                break

            else:
                print("Unknown command. Try again.")