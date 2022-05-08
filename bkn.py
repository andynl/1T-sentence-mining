# import requests
# import json

# URL = 'http://localhost:8765'

# def main():
#     res = requests.get(URL)
#     print(res.content)
#     res = requests.post(URL, json={
#         'action': 'findNotes',
#         'version': 6,
#         'params': {
#             'query': 'deck:Netflix',
#         },
#     }).json()
#     if res.get('error', None):
#         print('error:', res['error'])
#         return
#     detail_res = requests.post(URL, json={
#         'action': 'notesInfo',
#         'version': 6,
#         'params': {
#             'notes': res['result']
#         },
#     }).json()
#     with open('notes.json', 'w') as fp:
#        json.dump(detail_res, fp)

# if __name__ == "__main__":
#     main()