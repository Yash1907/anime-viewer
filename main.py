import os
import subprocess
import requests

def main():
    print("type quit at anytime to quit the program")
    anime_input = input("enter anime to search: ")
    while anime_input.lower() != 'quit':
        if bool(anime_input):
            if anime_input.lower() == 'quit': break
            search_resp = search(anime_input)
            show_str = ""
            for i in range(len(search_resp["results"])):
                show_str += f"{i+1}. {search_resp['results'][i]['title']}\n"
            print("search result\n")
            print(show_str)
            anime = input("enter anime number: ")
            if bool(anime):
                if str(anime).lower() == 'quit': break
                anime = int(anime)
                if anime >= 1 and anime <= len(search_resp["results"]):
                    anime_info = get_anime(search_resp['results'][anime-1]['id'])
                    episode_str = ""
                    for j in range(len(anime_info["episodes"])):
                        episode_str += f"{j+1}. {anime_info['title']} episode {anime_info['episodes'][j]['number']}\n"
                    print("episode list:\n")
                    print(episode_str)
                    episode = input("enter episode number: ")
                    if bool(episode):
                        if str(episode).lower() == 'quit': break
                        episode = int(episode)
                        if episode >= 1 and episode <= len(anime_info["episodes"]):                               
                            stream_link = get_stream_link(anime_info["episodes"][episode-1]["id"])
                            video_path = stream_link['sources'][3]['url']
                            title = anime_info['title']+" episode "+ str(anime_info['episodes'][episode-1]['number'])
                            create_html(title,video_path)
                            run_html(r"video.html")
                            break
                        else:
                            print("enter valid episode number")
                    else:
                        print("enter valid input (int)")
                else:
                    print("enter valid anime number")
            else:
                print("enter valid input (int)")
        else:
            print("enter valid input (string)")
            anime_input = input("enter anime to search: ")

def search(anime_input):
    url = f"https://api-consumet-virid.vercel.app/anime/gogoanime/{anime_input}"
    resp = requests.get(url)
    data = resp.json()
    return data

def get_anime(id):
    url = f"https://api-consumet-virid.vercel.app/anime/gogoanime/info/{id}"
    resp = requests.get(url)
    data = resp.json()
    return data

def get_stream_link(id):
    url = f"https://api-consumet-virid.vercel.app/anime/gogoanime/watch/{id}"
    resp = requests.get(url)
    data = resp.json()
    return data

def create_html(title,video_path):
    video_html = open("video.html", "w")
    HTML = """<!DOCTYPE html>
    <html>
    <head>
    <meta charset=utf-8 />
    <title>"""+title+"""</title>
        <link href='https://unpkg.com/video.js/dist/video-js.css' rel='stylesheet'>
    </head>
    <body>
    
        <video-js id='stream' class='vjs-default-skin vjs-fluid' controls preload='auto' width='max-width' height='max-height'>
        <source src='"""+video_path+"""' type='application/x-mpegURL'>
        </video-js>
        
        <script src='https://unpkg.com/video.js/dist/video.js'></script>
    
        <script>
        var player = videojs('stream');
        player.fluid(true);
        </script>
        
    </body>
    </html>"""
    video_html.write(HTML)
    video_html.close()

def run_html(file_path):
    url = file_path
    try: # should work on Windows
        os.startfile(url)
    except AttributeError:
        try: # should work on MacOS and most linux versions
            subprocess.call(['open', url])
        except:
            print('Could not open URL')
            
main()