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
