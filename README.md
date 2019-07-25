Pre - requisites:

Python 3.7 should be installed alongside following packages:
bs4
lxml
requests
openpyxl
xlsxwriter (can be replaced by openpyxl)
sklearn
pandas
numpy
gensim
wget

To use the javap command jdk and jre (latest versions for both of them).

These programs run in Linux environment. Thus there may arise a need for modification if one has to run them in Windows or any other environment.

For ubuntu 16.04, python3.7 (alongwith pip3.7) can be installed using the given script install.sh and invoked using python3.7 in terminal

Description and how to use these programs:

1.) Obtaining all possible categories of the data :

- The program Get_Category.py is used to obtain the total categories , usage of the categories and url to the main page under a particular category. 

- The program uses xlsxwriter to write the fetched data to a file named "Category_info.xlsx" (change the name according to requirement).

- BS4,lxml and requests are used for scraping the data from mavenrepository. 

- To prevent choking the website server, time delay has been added b/w each requests made to the website ( alongwith employing user agent rotation to avoid IP address being blocked.)

- Simply run Get_Category.py and it will start fetching the data.

- Persistent Internet connection is needed because resume capability (for fetching data) is not supported as of now.

2.) Obtaining meta_data for libraries under the categories :

- The xlsx obtained from Get_Category.py is used to obtain the urls for each category page

- After using BS4,lxml and requests to parse the page, url for each library on the page is obtained. 

- From there the meta_Data fields are captured. Some libraries have certain fields missing which can lead to erroneous entries in the xlsx file.

- This procedure is repeated for each library on the page and then for the first 10 pages in the category and finally for each category itself.

- Adjust for the path of Category_info.xlsx in Meta_data.py, then run it and it will start fetching the data.

- Persistent Internet connection is needed because resume capability (for fetching data) is not supported as of now.

3.) Downloading the jars :

- The xlsx obtained from Meta_Data.py is used to download jar files for each library

- The jar files downloaded are for the latest version for the first os type found on the page of the library. They are stored separately for each category and library. 

- wget is used to download and store the files.

- This procedure is repeated for each library on the page and then for the first 10 pages in the category and finally for each category itself.

- Adjust for the path of Meta_data.xlsx in Meta_data.py and the path where you want the libraries to be downloaded and stored at. After this run the program and it will start fetching the data.

- Persistent Internet connection is needed because resume capability (for fetching data) is not supported as of now.

4.) decompressing ,decompiling and storing byte code :

- Extract_class_info.py is used to decompress , decompile and store jvm byte code in txt format

- The path specified in the program should point to where the downloaded libraries are stored.

- unzip and javap commands are used to decompress and decompile the jar file respectively for each library found in the downloaded files.

- A integer flag is available to allow for removing comments in the decompiled code. If enabled code with comment as well as without comment will be stored in separate files.

- Adjust for the path for downloaded files and run program as "python Extract_class_info.py (0/non 0)" to get output.

- This task is mainly bound by disk I/O activity and thus can take time.
