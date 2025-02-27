def get_api_key():
    with open('key.txt', 'r') as file:
        return file.readline()


url = "https://api.artifactsmmo.com/"
headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer %s" % get_api_key()}


def dict_to_attributes(data, dict_name="data"):
    for key in data:
        print("self.%s = %s.get('%s', None)" % (key, dict_name, key))
