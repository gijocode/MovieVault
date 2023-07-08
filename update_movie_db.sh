say -v Samantha "File added to the torrents folder. Running movie DB update"
echo "File added to the folder. Running script...date is $(date)"
source /Users/gijomathew/Code/MoviesWatchedShowcase/env/bin/activate
python /Users/gijomathew/Code/MoviesWatchedShowcase/main.py
deactivate
say -v Samantha "DB updated!"
