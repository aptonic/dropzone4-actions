# by bunny
import base64
import json
import re
import time
import requests
import hashlib
import os
import concurrent.futures

class We:
    def __init__(self):
        """
        wetransfer.com tool for anonymously uploading and downloading files.
        Made by @bunnykek

        example usage:\n
        wetransfer = we()\n
        metadata = wetransfer.upload('path/to/file')\n
        print(metadata['shortened_url'])\n
        wetransfer.download(metadata['shortened_url'])\n
        """
        self.__session = requests.Session()
        self.__session.headers.update({'X-Requested-With': 'XMLHttpRequest'})

    def upload(self, path: str, display_name: str = '', message: str = '', max_workers: int = 10):
        """Returns a json containing the metadata and the link to the uploaded file/folder"""

        print("Uploading", os.path.basename(path))
        if display_name == '':
            display_name = os.path.basename(path)
        files, type = self.__get_files(path)
        files_response = self.__link_files(files, display_name, message)
        transfer_id = files_response['id']
        files = files_response['files']
        auth_bearer = files_response['storm_upload_token']
        self.endpoints = self.__decodejwt(auth_bearer)
        return self.__process_files(files, transfer_id, path, type, auth_bearer, max_workers)

    def download(self, download_url: str, download_path: str = ''):
        """Downloads from a url
        -> https://wetransfer.com/downloads/XXXXXXXXXX/YYYYY\n
        -> https://we.tl/X-XXXXXX
        """
        id, hash = self.__get_id_hash(download_url)
        metadata = self.url_metadata(id, hash)
        ddl = self.__get_ddl(id, hash)
        ext = metadata['recommended_filename'].split('.')[-1]
        if download_path == '':
            download_path = os.path.join(
                os.getcwd(), metadata['display_name'].split('.')[0]+'.'+ext)

        print(
            f'Downloading {metadata["display_name"]} [{metadata["size"]/(1024*1014)} MB]')

        with open(download_path, 'wb') as f:
            f.write(self.__session.get(ddl).content)
        return download_path

    def __get_ddl(self, id: str, hash: str):

        json_data = {
            'security_hash': hash,
            'intent': 'entire_transfer',
        }

        response = self.__session.post(
            f'https://wetransfer.com/api/v4/transfers/{id}/download', json=json_data)

        if response.status_code == 200:
            return response.json()['direct_link']
        else:
            raise Exception('get_ddl error\n', response.text)

    def __get_id_hash(self, url: str):

        if 'downloads' in url:
            result = re.search(
                r'https://wetransfer\.com/downloads/(.+)/(.+)', url)
            if result:
                return result.group(1), result.group(2)
            else:
                raise Exception('get_id_hash error\n')

        response = self.__session.get(url)
        if response.status_code == 200:
            result = re.search(
                r'\"https://wetransfer\.com/downloads/(.+)/(.+)\"', response.text)
            if result:
                return result.group(1), result.group(2)
            else:
                raise Exception('get_id_hash error\n', response.text)

    def url_metadata(self, id: str, hash: str):
        json_data = {
            'security_hash': hash,
        }

        response = self.__session.post(
            f'https://wetransfer.com/api/v4/transfers/{id}/prepare-download', json=json_data)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('url_metadata error\n', response.text)

    def __get_files(self, path: str) -> list:
        if os.path.isfile(path):
            file = [{'name': os.path.basename(path), 'size': os.path.getsize(
                path), 'item_type': 'file'}]
            return file, 'file'
        elif os.path.isdir(path):
            files = []
            for file in os.listdir(path):
                if os.path.isfile(os.path.join(path, file)):
                    files.append({'name': file, 'size': os.path.getsize(os.path.join(
                        path, file)), 'item_type': 'file'})
            print("Total number of files:", len(files))
            return files, 'folder'
        else:
            raise Exception('Path is not a file or directory')

    def __link_files(self, files: list, display_name: str, message: str):
        json_data = {
            'message': message,
            'display_name': display_name,
            'ui_language': 'en',
            'files': files
        }

        response = self.__session.post(
            'https://wetransfer.com/api/v4/transfers/link', json=json_data)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("liink files error\n", response.text)

    def __process_files(self, files: dict, transfer_id: str, path: str, type: str, auth_bearer: str, max_workers: int):
        items = []
        contentlenforblocks = []
        content_md5 = []
        files_path = []
        file_name_bcount = []
        for file in files:

            file_name = file['name']
            file_size = file['size']

            if type == 'folder':
                file_path = os.path.join(path, file_name)
            elif type == 'file':
                file_path = path

            files_path.append(file_path)

            n = int(file_size/15728640)
            chunks_list = [15728640]*n

            rem_chunk = file_size % 15728640
            if rem_chunk:
                chunks_list.append(rem_chunk)
                n += 1

            file_name_bcount.append((file_name, n))

            blocks = []
            for contlen in chunks_list:
                blocks.append({'content_length': contlen})
                contentlenforblocks.append(contlen)

            with open(file_path, "rb") as f:
                data = f.read(15728640)
                while data:
                    content_md5.append(hashlib.md5(data).hexdigest())
                    data = f.read(15728640)

            item = {
                'path': file_name,
                'item_type': 'file',
                'blocks': blocks
            }

            items.append(item)

        self.__preflight(items, auth_bearer)

        blocks_payload = []
        for x, y in zip(contentlenforblocks, content_md5):
            blocks_payload.append({
                'content_length': x,
                'content_md5_hex': y
            })

        s3_urls = self.__blocks(blocks_payload, auth_bearer)  # url md5 blockid

        # print(s3_urls)

        self.__upload_chunks(files_path, s3_urls, max_workers=max_workers)

        time.sleep(4)

        self.__batch(file_name_bcount, s3_urls, auth_bearer)

        return self.__finalize_chunks_upload(transfer_id)

    def __batch(self, file_name_bcount, s3_urls, auth_bearer):

        items = []
        i = 0
        # print(file_name_bcount)
        for file_name, count in file_name_bcount:
            item = {
                'path': file_name,
                'item_type': 'file',
                'block_ids': [url[2] for url in s3_urls[i:i+count]]
            }
            i += count
            items.append(item)

        headers = {
            'Authorization': f'Bearer {auth_bearer}',
        }

        json_data = {
            'items': items
        }
        # print(json.dumps(json_data, indent=2))
        
        response = self.__session.post(self.endpoints['storm.create_batch_url'], headers=headers, json=json_data)
        # print(response.status_code)

    def __preflight(self, items, auth_bearer: str):
        headers = {
            'Authorization': f'Bearer {auth_bearer}',
        }

        json_data = {
            'items': items
        }

        # print(json.dumps(json_data, indent=2))
        response = self.__session.post(self.endpoints['storm.preflight_batch_url'], json=json_data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('enable_response_s3 error\n', response.text)

    def __blocks(self, blocks: list, auth_bearer: str):
        s3_urls = []

        headers = {
            'Authorization': f'Bearer {auth_bearer}',
        }

        json_data = {
            'blocks': blocks
        }

        response = self.__session.post(self.endpoints['storm.announce_blocks_url'], headers=headers, json=json_data)
        rblocks = response.json()['data']['blocks']
        for rblock in rblocks:
            s3_urls.append([rblock['presigned_put_url'],
                           rblock['put_request_headers']['Content-MD5'], rblock['block_id']])
        return s3_urls

    def __upload_chunk(self, s3_url, chunk, chunk_number, total_chunks):
        headers = {
            'Content-MD5': s3_url[1],
        }

        response = self.__session.put(s3_url[0], data=chunk, headers=headers)

        if response.status_code != 200:
            print('Error on upload_chunk', response.text)
            return False

        return True

    def __upload_chunks(self, files_path: list, s3_urls: list, max_workers: int):
        total_chunks = len(s3_urls)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            chunk_number = 1

            for file_path in files_path:
                with open(file_path, 'rb') as file:
                    while (chunk := file.read(15728640)):
                        futures.append(executor.submit(
                            self.__upload_chunk, s3_urls[chunk_number - 1], chunk, chunk_number, total_chunks))
                        chunk_number += 1

            for future in concurrent.futures.as_completed(futures):
                if not future.result():
                    raise Exception('Error in multi-threaded chunk upload')

            print(f'Uploaded {", ".join([os.path.basename(path) for path in files_path])}')

    def __finalize_chunks_upload(self, transfer_id: str):

        json_data = {
            'wants_storm': True,
        }

        response = self.__session.put(
            f'https://wetransfer.com/api/v4/transfers/{transfer_id}/finalize',
            json=json_data
        )

        if response.status_code != 200:
            raise Exception("Finalize error\n", response.text)
        else:
            return response.json()
    
    def __decodejwt(self, jwt_token):
        payload_b64= jwt_token.split('.')[1]
        payload = json.loads(base64.b64decode(payload_b64 + '==').decode('utf-8'))
        return payload
