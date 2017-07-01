import yt
import os
import glob
import re


# Global Vars
append = "-trailer"  # Plex requires this
movie_dir = "X:/Videos/Movies/"  # My movie directory
# All movies must be in separate directories
movie_name_list = os.listdir(movie_dir)

# Empty lists for later
movie_dir_list = []
missing_trailer_list = []
downloaded_trailer_list = []

# Filter dotfiles
for movie in movie_name_list:
    if movie.startswith('.'):
        movie_name_list.remove(movie)

# Get movie paths
for movie in movie_name_list:
    movie_dir_list.append(movie_dir + movie + "/")

# Download trailers
for x in range(len(movie_name_list)):
    # Check if trailer exists
    # If so, skip
    if glob.glob("{}*-trailer*".format(movie_dir_list[x])):
        print(
            "Pre-existing trailer for {}. Skipping...".format(movie_name_list[x]))
        continue

    # Store trailer information in vid_nfo
    vid_nfo = yt.get_snippet_info(
        "{} trailer".format(movie_name_list[x]), title_append=append)

    # Get watch_url from video's youtube ID
    watch_url = yt.get_watch_url(vid_nfo[0]["id"])

    # Tries to download a matching video
    try:
        # re.sub removes characters not allowed in filenames on Windows
        yt.download_video(watch_url, re.sub(
            '[<>:|?"]', "", vid_nfo["title"]), directory=movie_dir_list[x])

        # Save which trailers were downloaded for later
        downloaded_trailer_list.append(movie_name_list[x])

        print("Downloaded trailer for {}. Success!".format(movie_name_list[x]))

    # No videos found / malfunction
    except:
        # Remember which trailers could not be downloaded
        missing_trailer_list.append(movie_name_list[x])
        print("Fatal error downloading trailer for {}. Skipping...".format(
            vid_nfo["title"]))
        continue

# If no trailers were downloaded / updated
if len(missing_trailer_list) == 0 and len(downloaded_trailer_list) == 0:
    print("-----------------------------------------------------------")
    print("Done. All trailers up to date.")
    print("-----------------------------------------------------------")

# If some trailers failed / were updated
else:
    print("-----------------------------------------------------------")
    print("Downloaded trailers for:")
    for x in range(len(downloaded_trailer_list)):
        print(downloaded_trailer_list[x])
    print("-----------------------------------------------------------")
    print("Unable to find trailers for:")
    print("-----------------------------------------------------------")
    for x in range(len(missing_trailer_list)):
        print(missing_trailer_list[x])
