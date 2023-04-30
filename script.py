from __future__ import print_function
import shutil
import urllib.request
import requests
import os

subreddits  = [
    'r/Wallpaper',
    'r/Wallpapers',
    'r/MinimalWallpaper', 
      
    'r/PixelArt',
    'r/DigitalArt',
    'r/ImaginaryLandscapes',
    'r/Illustration'
]

def getImage(i):
      curr_dir = os.getcwd()
      curr_dir = os.path.join(curr_dir,"wallpapers")
      file_name = i[2:] + '.png'
      if os.path.isfile(os.path.join(curr_dir,file_name)) == True:
        return "-1"
      url =  f"http://www.reddit.com/{i}/top.json?t=day"
      query_params = {
        "limit":5
      }
      headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
      r = requests.get(f"{url}",params=query_params , headers=headers)
      print("req code : " + str(r.status_code))
      print(i)
      if r.status_code != 200:
        return "-1"
      else:
        res = r.json()
        print(len(res['data']['children']))
        for post in res['data']['children']:
            if 'preview' in post['data']:              
              resolution_width = post['data']['preview']['images'][0]['resolutions'][-1]['width']
              url  = post['data']['url']
              if post['data']['over_18'] == False and resolution_width == 1080 and (url.endswith('.png') or url.endswith('.jpg') or url.endswith('.gif')):
                  print('url sent...')
                  return url
              else:
                print("sry...")

def downloadImage(i):
    url = ""
    url  = getImage(i)
    
    if url != "-1" and url is not None:
        file_name = i[2:]+'.png'
        print(url)
        curr_dir = os.getcwd()
        curr_dir = os.path.join(curr_dir,"wallpapers",file_name)
        urllib.request.urlretrieve(url,curr_dir)
        print(f"{file_name} downloaded...")

def deletePrevImages():
  curr_dir = os.getcwd()
  folder_name = "wallpapers"
  curr_path = os.path.join(curr_dir,folder_name)
  # print(curr_dir)
  print(curr_path)
  if os.path.isdir(curr_path):
    # os.removedirs(curr_path)
    shutil.rmtree(curr_path,ignore_errors=True)

  os.mkdir(curr_path)

deletePrevImages()
for i in range(50):
    for subreddit in subreddits:
      downloadImage(subreddit)

print("Done...")