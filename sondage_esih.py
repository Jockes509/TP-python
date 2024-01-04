import pandas as pd
import openpyxl
import boto3

class SondageEsih:
    def __init__(self):
        self.reponse={}
        self.question=[]
        
        
    def generer_question(self, questions):
        self.question.append(questions)
        
    
    def afficher_question(self):
        print("Voici la liste des questions que vous aurez a repondre \n ")
        for idx, questions in enumerate(self.question, start=1):
            print(f"{idx}. {questions}")
        print("\n")
            
    
    def collecter_donnees(self):
        print("\n Bienvenue dans le sondage de l'ESIH !")
        self.afficher_question()
        for quest in self.question:
            rep= input(f"Repondez a cette question:  {quest}")
            if quest in self.reponse:
                self.reponse[quest].append(rep)
            else: 
                self.reponse[quest]= [rep]
        print("\n Merci d'avoir participer au sondage !")
    
    
    def afficher_resultat_sondage(self):
        print("\n Affichage des resultats du sondage: ")
        for quest, rep in self.reponse.items():
            print(f"Question: {quest}")
            print("Reponses: ")
            for idx, rep in enumerate(self.reponse, start=1):
                print(f"{idx}. {rep}")
            print("\n")
                    
            
            
    def sauvegarder_resultats_excel(self, resultat_sondage):
        
        
        entete= ['Intention de quitter le pays','Tranche age','Niveau','Pays vise','Raison depart','Objectif depart','Duree dehors','Intention retour']
        
        try:
            df = pd.read_excel(resultat_sondage)
            df_concatene = pd.concat([df, pd.DataFrame(self.reponse)], axis=0, ignore_index=True)
            df_concatene.to_excel(resultat_sondage, index=False)
            print(f"Résultats ajoutés à '{resultat_sondage}'.")
        except FileNotFoundError:
            df = pd.DataFrame(self.reponse)
            df.to_excel(resultat_sondage, header=entete, index=False)
            print(f"Les résultats du sondage sont sauvegardés dans '{resultat_sondage}'.")

    

    
    def sauvegarder_resultats_sondage_s3(self, resultat_sondage, bucket_name='jockesbucket'):
        entete= ['Intention de quitter le pays','Tranche age','Niveau','Pays vise','Raison depart','Objectif depart','Duree dehors','Intention retour']
        bucket_name='jockesbucket'
        try:
            df = pd.read_excel(resultat_sondage)
            df_concatene = pd.concat([df, pd.DataFrame(self.reponse)], axis=0, ignore_index=True)
            df_concatene.to_excel(resultat_sondage, index=False)
            print(f"Résultats ajoutés à '{resultat_sondage}'.")

            
            s3 = boto3.client('s3',aws_access_key_id='AKIAQNDVXKJVAVJERVFL',aws_secret_access_key='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')
            bucket_name='jockesbucket'

            
            s3.upload_file(resultat_sondage, bucket_name, resultat_sondage)
            print(f"Résultats téléversés vers S3 dans le bucket '{bucket_name}'.")
        except FileNotFoundError:
            df = pd.DataFrame(self.reponse)
            df.to_excel(resultat_sondage, header=entete, index=False)
            print(f"Les résultats du sondage sont sauvegardés dans '{resultat_sondage}'.")

            pass



    
sondage= SondageEsih()

sondage.generer_question("Avez-vous l'intention de quitter le pays après avoir terminé vos études universitaires? (Repondez par: oui, non ou incertain)\n")
sondage.generer_question("Quel est votre âge actuel?\n")
sondage.generer_question("À quel niveau d'études êtes-vous actuellement?\n")
sondage.generer_question("Vers quel(s) pays envisagez-vous de vous rendre?\n")
sondage.generer_question("Pourquoi envisagez-vous de quitter le pays?\n")
sondage.generer_question("Envisagez-vous de quitter le pays pour des études supplémentaires ou d'autres raisons?\n")
sondage.generer_question("Si vous envisagez un départ temporaire, quelle est la durée prévue de votre séjour?\n")
sondage.generer_question("Avez-vous l'intention de retourner dans votre pays d'origine après votre séjour à l'étranger?\n")


sondage.collecter_donnees()

resultat_sondage="resultat.xlsx"

sondage.sauvegarder_resultats_sondage_s3(resultat_sondage,'bucket_name')