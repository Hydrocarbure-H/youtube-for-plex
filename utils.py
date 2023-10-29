import yt_dlp as youtube_dl
import datetime


def check_for_new_videos(channels):
    """
    Check for new videos in the channels list
    :param channels:
    :return:
    """
    for vid in channels:
        ydl_opts = {
            'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            'merge_output_format': 'mp4',
            'playlistend': 1,
            'outtmpl': f'/YOUR FOLDER/{vid["folder_name"]}/%(title)s - %(uploader)s - %(upload_date)s.%(ext)s'.encode(
                'ascii', 'ignore').decode('ascii'),
            'quiet': True
        }

        print("Checking for new videos in " + vid['folder_name'] + "...", end=" ")

        # Get the last video uploaded on the channel
        try:
            ydl = youtube_dl.YoutubeDL(ydl_opts)
            video_info = ydl.extract_info(vid['url'], download=False)
        except Exception as e:
            print("Error: " + str(e))
            continue

        # First walk - get the entries from the root of the json
        entries = video_info["entries"]

        # For some unkwnonw reason, the first walk doesn't always return the entries
        if not get_video(entries, ydl, vid):
            entries = entries[0]["entries"]
            # Second walk - get the entries from the first entry of the root
            get_video(entries, ydl, vid)

    print("All channel checks complete.")


def get_video(entries, ydl, vid):
    """
    Get the last video uploaded on the channel from the entries list
    :param vid:
    :param ydl:
    :param entries:
    :return:
    """
    TODAY = datetime.datetime.now().date()

    for entry in entries:
        if entry and 'upload_date' in entry:
            upload_date = datetime.datetime.strptime(entry['upload_date'], '%Y%m%d').date()

            # Compare the upload date with TODAY's date
            if upload_date >= TODAY:
                print("New video found! Downloading " + vid['folder_name'] + "...")
                # Download the video
                try:
                    ydl.download([vid['url']])
                except Exception as e:
                    print("Error: " + str(e))
                    continue
                print("Download complete for " + vid['folder_name'])
            else:
                print("No new videos found for " + vid['folder_name'])
            return True
    return False
