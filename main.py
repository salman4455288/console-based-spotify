# import pandas as pd
# import os 
# # os.mkdir("artist")
# # os.mkdir("genere")
# # os.mkdir("songs")
# # os.mkdir("account")
# # os.mkdir("user")
# parent_directory=os.getcwd()
# artist_path=os.getcwd() + "/artist"
# genere_path=os.getcwd() + "/genere"
# print(parent_directory)
# print(artist_path)
# print(genere_path)
# print("____________________-------------print-------------------_____________________")
# cv1 = pd.read_csv("/home/salman/Downloads/artist name .csv")  # Correct path: / and raw string
# # os.chdir("user")
# # os.mkdir("artist")
# # os.mkdir("listner")
# os.chdir("user/listner")
# for artist, genre,name in zip(cv1["Artist Name"], cv1["Genre"],cv1["Title"]):
#     #print(name,"  ",artist, "  ", genre)
#     #for genere 
#     os.chdir(genere_path)
#     print("moved to genere path")
#     if(os.path.isdir(genre)):
#         os.chdir(genere_path+"/"+ genre)
#         f1=open(genre+".txt","a")
#         f1.write(name+'\n')
#     else:
#         os.mkdir(genre)
#         os.chdir(genere_path+"/"+ genre)
#         f1=open(genre+".txt","a")
#         f1.write(name+'\n')       

    
#     os.chdir(artist_path)
#     if(os.path.isdir(artist)):
#         os.chdir(artist_path+"/"+ artist)
#         f1=open(artist+".txt","a")
#         f1.write(name+'\n')
#     else:
#         os.mkdir(artist)
#         os.chdir(artist_path+"/"+ artist)
#         f1=open(artist+".txt","a")
#         f1.write(name+'\n') 
    