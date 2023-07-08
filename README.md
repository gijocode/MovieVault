# Movie Showcase Application

The Movie Showcase Application is a Python script that interacts with IMDb to retrieve movie information and store it in a MongoDB database. It also processes torrent files to extract movie titles and adds new movies to the database.

## Prerequisites

Before running the code, ensure that you have the following dependencies installed:

- Python 3.x
- IMDbPY library: Install it using `pip install imdbpy`
- pymongo library: Install it using `pip install pymongo`
- MongoDB server: Set up a MongoDB server and ensure it is running locally or accessible through a connection URL.

## Setup

1. Clone or download the repository to your local machine.
2. Open the terminal or command prompt and navigate to the directory where the code files are located.
3. Install the required libraries by running the following command:
   `pip install imdbpy pymongo`
4. Update the connection details for MongoDB:

- Open the `movie_showcase.py` file in a text editor.
- Look for the `mongo_client` variable declaration and update it with the appropriate connection details. By default, it assumes a local MongoDB server connection without authentication.

5. Set the directory path containing torrent files:

- Look for the `directory` variable declaration and update it with the path to the directory where your torrent files are located.

## Usage

To run the Movie Showcase Application, execute the following command in the terminal or command prompt:
`python movie_showcase.py`

The script will perform the following steps:

1. Retrieve a list of movie titles from the torrent files in the specified directory.
2. Filter out unnecessary words and characters from the movie titles.
3. Query IMDb to obtain detailed information for each movie.
4. Extract the cast information and check if the actors are already present in the MongoDB database.
5. Add new actors to the actor collection in MongoDB if necessary.
6. Construct movie documents with relevant information and insert them into the movie collection in MongoDB.

## Additional Information

- The code utilizes the IMDbPY library to interact with IMDb's movie and person data. It allows you to search for movies, retrieve detailed information, and access the cast information.
- The movie data retrieved from IMDb includes details such as the title, synopsis, rating, poster image URL, and cast information.
- The script uses the `concurrent.futures` module to execute tasks in parallel, improving performance when retrieving movie and actor information.
- The code assumes that the MongoDB server is running locally. If you're using a remote MongoDB server, update the connection details accordingly.
- If any exceptions occur during the execution of the script, they will be printed to the console for debugging purposes.

Please note that IMDb's terms of service apply when using their data. Ensure that you comply with their usage guidelines.

Feel free to modify and extend the code to suit your specific requirements. Enjoy showcasing your movie collection!

# Update Movie Database Launchd Configuration

The Update Movie Database Launchd Configuration is an XML property list (plist) file that specifies the configuration for a launchd job on macOS. It defines the settings for automatically running a script, `update_movie_db.sh`, whenever changes occur in the specified directory. The script is responsible for updating the movie database.

## Usage

To use this plist file:

1. Create a shell script named `update_movie_db.sh` that contains the necessary logic to update the movie database.
2. Open a text editor and create a new file.
3. Copy the contents of the provided plist file into the new file.
4. Save the file with a `.plist` extension, such as `com.update_movie_db.plist`.

## Configuration

The plist file contains the following key-value pairs:

- `Label`: Specifies a unique identifier for the launchd job. In this case, it is set to `com.update_movie_db`.
- `ProgramArguments`: Defines the command or script to be executed when the launchd job is triggered. The path to the `update_movie_db.sh` script is specified here.
- `WatchPaths`: Specifies an array of paths to monitor for changes. Whenever changes occur in these paths, the launchd job will be triggered. In this case, the path to the directory containing the torrent files is specified.
- `StandardOutPath`: Sets the file path where the standard output of the executed script will be written. In this example, it is set to `/Users/gijomathew/scripts/logs/update_movie_db/output.log`.
- `StandardErrorPath`: Sets the file path where the standard error output of the executed script will be written. In this example, it is set to `/Users/gijomathew/scripts/logs/update_movie_db/error.log`.

## Installation

To install and activate the launchd job:

1. Move the `com.update_movie_db.plist` file to the `~/Library/LaunchAgents/` directory. If the directory doesn't exist, create it.
2. Open a terminal and execute the following command to load the launchd job:
   `launchctl load ~/Library/LaunchAgents/com.update_movie_db.plist`
3. The launchd job is now active and will monitor the specified directory for changes. Whenever changes occur, the `update_movie_db.sh` script will be executed.

## Logs

The script's standard output and error output are redirected to separate log files as specified in the plist file. You can check these log files to view the output and any potential errors or exceptions that occur during script execution.

Please note that the paths used in the plist file and the script should be updated to match your system configuration.

Feel free to modify the plist file and the script to suit your specific requirements.
