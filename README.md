<h1 align="center">IF2211 Strategy Algorithm</h1>
<h1 align="center">Sem II 2023/2024</h1>
<h3 align="center">Implementing String Matching Algorithm to Trace Song Identities from fragment of lyrics </p>

![GitHub last commit](https://img.shields.io/github/last-commit/AlbertChoe/Song_String_Matching)

## Table of Contents
- [Overview](#overview)
- [Abstraction](#abstraction)
- [Built With](#built-with)
- [How to Run](#How-TO-Run)
- [Creator](#creator)
- [Links](#links)

## Overview
This project implements string matching algorithms to identify song titles based on lyric fragments. By leveraging popular algorithms such as Knuth-Morris-Pratt (KMP), Boyer-Moore, and Brute Force, the program efficiently matches input lyric fragments against a dataset of song lyrics. The project demonstrates practical applications of these algorithms in the field of music information retrieval.

## Abstraction
The ability to identify songs from partial lyrics is a valuable tool for music enthusiasts. This project combines data from Spotify and Genius to create a comprehensive dataset, which is then used to test and analyze the performance of different string matching algorithms. The algorithms process the lyrics and match input fragments to the corresponding songs, demonstrating their efficiency and accuracy.

## Built With
- Python: The primary programming language used for implementing the algorithms and processing data.
- Spotify API: Used to retrieve song metadata such as track name, artist name, album details, and popularity.]
- Genius API: Used to fetch accurate and detailed lyrics for the songs.
- BeautifulSoup: For web scraping the lyrics from Genius.

## How to Run 
1. Clone this repository :

```shell
git clone https://github.com/AlbertChoe/Song_String_Matching.git
```

2. Install the required packages:
```shell
pip install requests beautifulsoup4 nltk

```
3. Set up Api Keys:
- Spotify: Create an app on the Spotify Developer Dashboard to get client_id and client_secret.
- Genius: Sign up on Genius to get the genius_api_key.

4. Run the main script to fetch data:

```shell
python song.py

```
5. Run the processing script to search for song lyrics:
```shell
python process.py
```


## Creator

| NIM      | Nama   | Kelas |
| -------- | ------ | ----- |
| 13522081 | Albert | K-01  |
