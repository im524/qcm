
from django.db import models
from django.contrib.auth.models import User


class departement(models.Model):
    iddepartement = models.AutoField(primary_key=True)
    description = models.TextField()


class enseignant(models.Model):
    idEnseignant = models.AutoField(primary_key=True)
    login = models.CharField(max_length=20, unique=True)
    nom = models.TextField()
    prenom = models.TextField()
    estAdmin = models.BooleanField()
    motDePasse = models.CharField(max_length=20)
    iddepartement = models.ForeignKey(departement, on_delete=models.CASCADE)


class matiere(models.Model):
    idmatiere = models.AutoField(primary_key=True)
    nomMatiere = models.TextField()


class filiere(models.Model):
    idfiliere = models.AutoField(primary_key=True)
    iddepartement = models.ForeignKey(departement, on_delete=models.CASCADE)
    description = models.CharField(max_length=20)


class appartenir(models.Model):
    idEnseignant = models.ForeignKey(enseignant, on_delete=models.CASCADE)
    idfil = models.ForeignKey(filiere, on_delete=models.CASCADE)


class apparMATFil(models.Model):
    idMat = models.ForeignKey(matiere, on_delete=models.CASCADE)
    idfilli = models.ForeignKey(filiere, on_delete=models.CASCADE)


class niveau(models.Model):
    id_niveau = models.AutoField(primary_key=True)
    description = models.TextField()


class question(models.Model):
    id_question = models.AutoField(primary_key=True)
    questionA = models.TextField()
    explication = models.TextField()
    difficulte = models.IntegerField()
    idMatiere = models.ForeignKey(matiere, on_delete=models.CASCADE)
    idEnsei = models.ForeignKey(enseignant, on_delete=models.CASCADE)


class reponse(models.Model):
    id_reponse = models.AutoField(primary_key=True)
    response = models.TextField()
    estVrai = models.BooleanField()
    commentaire = models.TextField()
    idQuest = models.ForeignKey(question, on_delete=models.CASCADE)


class herit(models.Model):
    id_quiz = models.AutoField(primary_key=True)
    idmatiere = models.ForeignKey(matiere, on_delete=models.CASCADE)
    id_niveau = models.ForeignKey(niveau, on_delete=models.CASCADE)
    id_Enseignant = models.ForeignKey(enseignant, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class quiz(herit):
    description = models.CharField(max_length=20)


class evaluation(herit):
    dateDebut = models.DateTimeField()
    dateFin = models.DateTimeField()

    description = models.CharField(max_length=20)


class Etudiant(models.Model):
    idEtudiant = models.AutoField(primary_key=True)
    login = models.CharField(max_length=20, unique=True)
    nom = models.TextField()
    prenom = models.TextField()
    motDePasse = models.CharField(max_length=20)
    idfiliere = models.ForeignKey(filiere, on_delete=models.CASCADE)


class contenir(models.Model):
    idQuiz = models.ForeignKey(quiz, on_delete=models.CASCADE)
    idQuestion = models.ForeignKey(question, on_delete=models.CASCADE)


class contenirEval(models.Model):
    idQuiz = models.ForeignKey(evaluation, on_delete=models.CASCADE)
    idQuestion = models.ForeignKey(question, on_delete=models.CASCADE)


class submitEval(models.Model):
    class Meta:
        unique_together = (('idev', 'idetud'),)

    idev = models.ForeignKey(evaluation, on_delete=models.CASCADE)
    idetud = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    submitDate = models.DateTimeField(auto_now_add=True)
    note = models.IntegerField()
    totalQ = models.IntegerField()

# Create your models here.
class reponse2(models.Model):
    idr = models.AutoField(primary_key=True)
    idEtudiants = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    id_quizs = models.ForeignKey(evaluation, on_delete=models.CASCADE)
    id_reponses = models.ForeignKey(reponse, on_delete=models.CASCADE)

class comment(models.Model):
    commentaire = models.TextField()
    idEtt = models.ForeignKey(Etudiant, on_delete=models.CASCADE)

