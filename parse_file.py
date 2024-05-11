import json
from PIL import Image


class parse:
    def __init__(self):
        self.vtx_releases_path = "resource/vtx_releases"
        self.vtx_common_path = "resource/vtx_common"
        self.event_vrx_releases_path = "resource/event_vrx_releases"
        self.monitor_releases_path = "resource/monitor_releases"
        self.vtx_tragets_image_path = "resource/vtx_targets.png"

        self.vtx_info = {}
        self.event_vrx_info = {}
        self.monitor_info = {}
        self.vtx_target_image = []

    def parse_vtx_common(self):
        try:
            with open(self.vtx_common_path) as file:
                lines = file.readlines()
                start = 0
                for i in range(len(lines)):
                    if start == 1:
                        words = lines[i].split()
                        for j in range(len(words)):
                            if words[j] == "defined":
                                name = words[j+1].lower()
                            if words[j] == "VTX_ID":
                                if words[j+1] != "0x00":
                                    word = words[j+1].strip("0x")
                                    self.vtx_info[name] = {"id": int(word, 16)}
                    if lines[i] == "/* define VTX ID start */\n":
                        start = 1
                    elif lines[i] == "/* define VTX ID end */\n":
                        start = 0
            return 1
        except:
            print("something error")
            return 0

    def parse_vtx_releases(self):
        try:
            with open(self.vtx_releases_path) as f:
                data = json.load(f)

            for i in range(len(data)):
                link_list = []
                name_list = []
                for j in range(len(data[i]['assets'])):
                    link_list.append(data[i]['assets'][j]
                                     ['browser_download_url'])

                    name_start = link_list[j].rfind('/') + len('/')
                    name_end = link_list[j].index(".zip", name_start)
                    name_list.append(link_list[j][name_start:name_end])
                    name = link_list[j][name_start:name_end]
                    if name == "hdzero_freestyle":
                        name = "hdzero_freestyle_v1"

                    version = data[i]['tag_name']
                    url = data[i]['assets'][j]['browser_download_url']
                    self.vtx_info[name][version] = url
            return 1
        except:
            return 0

    def parse_event_vrx_releases(self):
        try:
            with open(self.event_vrx_releases_path) as f:
                data = json.load(f)

            for i in range(len(data)):
                link_list = []
                for j in range(len(data[i]['assets'])):
                    link_list.append(data[i]['assets'][j]
                                     ['browser_download_url'])

                    version = data[i]['tag_name']
                    url = data[i]['assets'][j]['browser_download_url']
                    self.event_vrx_info[version] = url
            return 1
        except:
            return 0

    def parse_monitor_releases(self):
        try:
            with open(self.monitor_releases_path) as f:
                data = json.load(f)

            for i in range(len(data)):
                link_list = []
                for j in range(len(data[i]['assets'])):
                    link_list.append(data[i]['assets'][j]
                                     ['browser_download_url'])

                    version = data[i]['tag_name']
                    url = data[i]['assets'][j]['browser_download_url']
                    self.monitor_info[version] = url
            return 1
        except:
            return 0

    def parse_vtx_tragets_image(self, num):
        try:
            ori_img = Image.open(self.vtx_tragets_image_path)
        except:
            return 0

        for i in range(0, num):
            try:
                self.vtx_target_image.append(
                    ori_img.crop((0, i*100, 299, i*100+99)))
            except:
                return 0

        return 1


my_parse = parse()
