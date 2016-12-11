# Task

In order to use this project you need to install <b>Python3</b>. For the first task(emoticons.py) no additional libs are needed.
For the second task, you will need to install requirements from the <b> requirements.txt </b> file. 
You will also need PostgresSQL server running and create tables like in the file<b>create_db.sql</b>

<h1>Additional notes:</h1> 
I have solved the second problem first splitting the original file into smaller chunks with size 400K lines. <b>In order to split data use command from file splitter.</b> After that I have used 
Python multiprocessing in order to paralell the calculations. The most challenging part was possibly "uniting" broken groups that were
in two different files. I have done this using the second table unsorted_info.
You can check the realisation in the function: <b>process_splitted_elements()</b>

