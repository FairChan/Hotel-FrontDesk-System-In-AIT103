The input folder, which contains our training images two folders:  
📂first folder: clear_face is used to store unknown face data (to prevent overfitting).

📁second folder: clear_named_faces, with the character name + number for model training.

💾train4.py is used to train the model.

💾recognize.py is used to detect faces and read the csv to get the occupant information (the one that pops up the dialog box). 

💾guest_info.csv is the csv file used to store the occupant information. 

💾face_classifier.pkl pca.pkl label_encoder. pkl These three files are all the same as the model. pkl these three files are the training package obtained after train training, predict is to read these to recognize the face. 

💾Cam2jpg.py is to convert the video read from the camera into a photo stored in input/clear_named_face, and ask the user to enter the name to label.

💾info2csv.py is to manage the user's data backend admin tool to modify csv.

💾chatbot.py is able to run a AIML drived program in background.

💾Hotel.py is the main streamlit program which drives the web page and bridges between different modules.

❗️For successfully using the system, there is something you need to pay attention to:

1.Change the absolute path in Hotel.py and recognize.py(I have made marks in the python file)

2.To launch the program, you need type the command in the terminal
  
  (Before you typed such code to run, make sure your anaconda environment are suitable for the running)
  
  python (the path of the chatbot.py)

  streamlit run (the path of the Hotel.py)
