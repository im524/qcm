from django.shortcuts import render
from django.http import HttpResponse, request
from django.template import context
from django.template.loader import get_template
from django.views.generic import View
from .utils import render_to_pdf
# Create your views here.
from django.shortcuts import render
from .models import enseignant
from .forms import connexion
from .models import Etudiant
from .models import matiere
from .models import question, filiere, apparMATFil
from .models import reponse, contenir, niveau, herit, quiz, appartenir
from .models import quiz, evaluation, contenirEval, submitEval,reponse2,comment

from django.shortcuts import render, redirect
import datetime

from datetime import timedelta
from django.contrib import auth
from django.utils.timezone import utc




import pytz



# from django.http import HttpResponse
# page d'accueil
def home(request):
    return render(request, 'myblog/home.html')



# espace enseignant login
def espaceEnseignant(request):
    form = connexion()
    message = ""

    if request.method == 'POST':
        form = connexion(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            # recuperer id enseignant avec les sessions
            try:
             emp_list = enseignant.objects.get(login=login)
             emp_names = emp_list.idEnseignant
             request.session['k'] = emp_names
            ########################################
             motDePasse = form.cleaned_data['motDePasse']
             enseignante = enseignant.objects.get(login=login, motDePasse=motDePasse)
             all_mat = matiere.objects.all()
             k = comment.objects.all()
             lem = filiere.objects.all()
             return render(request, "myblog/home0.html", {'mat': all_mat, 'k': k, 'lem': lem})

            except enseignant.DoesNotExist:
               message = "nom d'utilisateur ou mot de passe incorrect"
               return render(request, 'myblog/formEnseignant.html', {'form': form, 'message': message})

    return render(request, 'myblog/formEnseignant.html', {'form': form})



# espace etudiant login

def espaceEtudiant(request):
    form = connexion()
    message = ""
    if request.method == 'POST':
        form = connexion(request.POST)
        if form.is_valid():
            message=" "
            login = login = form.cleaned_data['login']

            motDePasse = form.cleaned_data['motDePasse']
            all_mat = matiere.objects.all()
            all_niv = niveau.objects.all()
            try:
             emp = Etudiant.objects.get(login=login)
             emp_name = emp.idEtudiant
             request.session['et'] = emp_name
             etudiant = Etudiant.objects.get(login=login, motDePasse=motDePasse)
             return render(request, 'myblog/etudiant0.html', {'niv': all_niv, 'mat': all_mat})

            except Etudiant.DoesNotExist:
                  message = "nom d'utilisateur ou mot de passe incorrect"
                  return render(request, 'myblog/formEtudiant.html', { 'form': form,'message': message})
    return render(request, 'myblog/formEtudiant.html', {'form': form})

# page about
def about(request):
    return render(request, 'myblog/about.html', {''})
    # return HttpResponse('<h1>Blog About</h1>')


# page questionnaire
def questionnaire(request):
    idens = request.session['k']
    fili = appartenir.objects.filter(idEnseignant=idens).values('idfil')
    tab = []
    f = []

    for t in fili:
        all_mat = apparMATFil.objects.filter(idfilli=t['idfil']).values('idMat')
        tab.extend(all_mat)
    for k in tab:
        matt = matiere.objects.filter(idmatiere=k['idMat'])
        f.extend(matt)
        f = list(set(f))
    return render(request, 'myblog/questionnaire.html', {'mat': f})


# formulaire de creation des questions et reponses
def add_question_form_submission(request):
    print(request.POST)
    Commentaire = request.POST["Commentaire"]
    questions = request.POST["question"]
    matier = request.POST["matiere"]
    dif = request.POST["dif"]
    #comments = request.POST.getlist('comment')
    ##utilistion de l'id de l'enseignant avec session
    idens = request.session['k']
    ########################################################
    reponses = request.POST.getlist('reponse')
    comment = request.POST.getlist('comment')
    flags = request.POST.getlist('flag')
    ques = question(questionA=questions, explication=Commentaire, difficulte=dif,
                    idMatiere=matiere.objects.get(idmatiere=matier), idEnsei=enseignant.objects.get(idEnseignant=idens))
    ques.save()
    for i in range(len(reponses)):
        #if reponses[i] != '':

            rep = reponse(response=reponses[i], commentaire=comment[i], estVrai=flags[i],
                          idQuest=question.objects.get(id_question=ques.id_question))
            rep.save()

        ##################################bring matiere
    idens = request.session['k']
    fili = appartenir.objects.filter(idEnseignant=idens).values('idfil')
    tab = []
    f = []

    for t in fili:
            all_mat = apparMATFil.objects.filter(idfilli=t['idfil']).values('idMat')
            tab.extend(all_mat)
    for k in tab:
         matt = matiere.objects.filter(idmatiere=k['idMat'])
         f.extend(matt)
         f = list(set(f))
         return render(request, "myblog/questionnaire.html", {'mat': f})


# page de creation d'un quiz choix des matieres

def subject(request):
    all_niv = niveau.objects.all()
    idens = request.session['k']
    fili = appartenir.objects.filter(idEnseignant=idens).values('idfil')
    tab = []
    f = []
    all_niv = niveau.objects.all()
    for t in fili:
        all_mat = apparMATFil.objects.filter(idfilli=t['idfil']).values('idMat')
        tab.extend(all_mat)
    for k in tab:
        matt = matiere.objects.filter(idmatiere=k['idMat'])
        f.extend(matt)
        f = list(set(f))

    return render(request, 'myblog/subject.html', {'niv': all_niv, 'f': f})


# affichage des questions pour creer  quiz  table quiz
def subj(request):
    matier = request.POST["matiere"]
    descri = request.POST["desc"]
    idN = request.POST["niveauQ"]
    idens = request.session['k']
    quess = quiz(idmatiere=matiere.objects.get(idmatiere=matier), id_niveau=niveau.objects.get(id_niveau=idN),
                 description=descri, id_Enseignant=enseignant.objects.get(idEnseignant=idens))
    quess.save()
    allQu = question.objects.filter(idMatiere=matier, idEnsei=idens)

    return render(request, 'myblog/subj.html', {'quest': allQu, 'idQ': quess.id_quiz})


# creation du qcm table contenir

def createQcm(request):
    q = request.POST.getlist("choix")
    r = request.POST["s"]
    for i in q:
        rep = contenir(idQuestion=question.objects.get(id_question=i), idQuiz=quiz.objects.get(id_quiz=r))
        rep.save()
    return render(request, 'myblog/home0.html')


########## partie etudiant###########"
##### chercher les qcms disponible selon matiere et niveau
def home1(request):
    idet = request.session['et']
    fil = Etudiant.objects.get(idEtudiant=idet).idfiliere
    all_niv = niveau.objects.all()
    l = quiz.objects.all()
    # dept= filiere.objects.get(idfiliere=fil).iddepartement
    mat = apparMATFil.objects.filter(idfilli=fil).values('idMat')
    print(mat)
    m = []
    for k in mat:
        resul = matiere.objects.filter(idmatiere=k['idMat'])

        m.extend(resul)

    return render(request, 'myblog/home1.html', {'niv': all_niv, 'mat': m, 'l': l})


####formulaire pour extraire les qcms selon matiere et niveau choisit
def ChoixMt(request):
    sub = request.POST["subjects"]
    leve = request.POST["level"]
    resul = quiz.objects.filter(idmatiere=sub, id_niveau=leve)

    return render(request, 'myblog/home1.html', {'idQuizz': resul})


#####choix du qcm parmi la liste
def home2(request):
    return render(request, 'myblog/home2.html')


# recupere les questions liées à un quiz
def allQuiz(request):
    allQui = request.POST["allQuizs"]
    request.session['quizi'] = allQui
    a = contenir.objects.filter(idQuiz=quiz.objects.get(id_quiz=allQui)).values('idQuestion')
    print(a)
    z = []
    repa = []
    k=0
    for i in a:

        c = question.objects.filter(id_question=i['idQuestion'])
        r = reponse.objects.filter(idQuest=i['idQuestion'])
        k=k+1
        z.extend(c)
        repa.extend(r)
    return render(request, 'myblog/home3.html', {'questi': z, 'ref': repa,'k':k})


######affichage du quiz
def home3(request):
    return render(request, 'myblog/home3.html')


############## traiter les reponses
def traitQcm(request):
    resultat = request.POST.getlist('choix')
    h= request.POST['val']
    tot = request.POST['total']
    bb = []
    for f in resultat:
        lm = reponse.objects.filter(id_reponse=f)
        bb.extend(lm)
    iq = request.session['quizi']
    a = contenir.objects.filter(idQuiz=quiz.objects.get(id_quiz=iq)).values('idQuestion')
    print(a)
    z = []
    repa = []
    for i in a:
        c = question.objects.filter(id_question=i['idQuestion'])
        r = reponse.objects.filter(idQuest=i['idQuestion'])
        z.extend(c)
        repa.extend(r)

    return render(request, 'myblog/correction.html', {'questi': z, 'ref': repa, 'bb': bb,'note':h,'tot':tot})


####afficher la correction
def correction(request):

    return render(request, 'myblog/correction.html')


def details(request):
    iq = request.session['quizi']
    a = contenir.objects.filter(idQuiz=quiz.objects.get(id_quiz=iq)).values('idQuestion')
    print(a)
    z = []
    repa = []
    for i in a:
        c = question.objects.filter(id_question=i['idQuestion'])
        r = reponse.objects.filter(idQuest=i['idQuestion'])
        z.extend(c)
        repa.extend(r)

    return render(request, 'myblog/correctionDetails.html', {'questi': z, 'ref': repa})


def correctionDetails(request):
    return render(request, 'myblog/correctionDetails.html')


def home0(request):
    return render(request, 'myblog/home0.html')


def etudiant0(request):
    return render(request, 'myblog/etudiant0.html')


def evalu(request):
    idens = request.session['k']
    fili = appartenir.objects.filter(idEnseignant=idens).values('idfil')
    tab = []
    f = []
    h = []
    all_niv = niveau.objects.all()
    for t in fili:
        all_mat = apparMATFil.objects.filter(idfilli=t['idfil']).values('idMat')

        tab.extend(all_mat)
        # print(tab)
    for k in tab:
        matt = matiere.objects.filter(idmatiere=k['idMat'])

        f.extend(matt)

    f = list(set(f))
    return render(request, 'myblog/evalu.html', {'niv': all_niv, 'f': f})


def eval(request):

    matie = request.POST["matiere"]
    idN = request.POST["niveauQ"]
    des=request.POST["descri"]
    idens = request.session['k']
    db = request.POST["evd"]
    df = request.POST["evf"]

    brr = evaluation(dateDebut=db, idmatiere=matiere.objects.get(idmatiere=matie),
                     id_niveau=niveau.objects.get(id_niveau=idN),
                     id_Enseignant=enseignant.objects.get(idEnseignant=idens), dateFin=df,description=des)
    brr.save()
    allQu = question.objects.filter(idMatiere=matie, idEnsei=idens)
    return render(request, 'myblog/eval.html', {'quest': allQu, 'idQ': brr.id_quiz})


def createEval(request):
    q = request.POST.getlist("choix")
    r = request.POST["s"]

    for i in q:

        rep = contenirEval(idQuestion=question.objects.get(id_question=i), idQuiz=evaluation.objects.get(id_quiz=r))
        rep.save()

    return render(request, 'myblog/home0.html')


def home2Eval(request):
    idet = request.session['et']
    fil = Etudiant.objects.get(idEtudiant=idet).idfiliere
    # dept= filiere.objects.get(idfiliere=fil).iddepartement
    mat = apparMATFil.objects.filter(idfilli=fil)
    m = []
    for k in mat:
        resul = evaluation.objects.filter(idmatiere=k.idMat)

        m.extend(resul)
        print(m)
    z = []
    # sub = request.POST["subjects"]
    # leve = request.POST["level"]

    dt = datetime.datetime.now()
    # here, now.tzinfo is None, it's a naive datetime
    dt = pytz.utc.localize(dt)
    k=dt-timedelta(minutes=5)

    for i in m:
        if i.dateDebut >= k:
            #print(i.dateDebut)
            #print(dt)
            z.append(i)
            ############################
    idet = request.session['et']
    eva1 = submitEval.objects.filter(idetud=idet)
    eva = submitEval.objects.filter(idetud=idet).values('idev')
    f = []
    for i in eva:
        qr = i['idev']
        f.append(qr)

    return render(request, 'myblog/home2Eval.html', {'idQuizz': z,'eva':f,'ev':eva1})


#### le choix de matiere et niveau

##la page qui affiche  les questions de l'evaluation
def allQuizEval(request):

    idet = request.session['et']
    allQui = request.POST["allQuizs"]
    rd = evaluation.objects.get(id_quiz=allQui).dateDebut
    rf = evaluation.objects.get(id_quiz=allQui).dateFin
    # print(rd)

    dt = datetime.datetime.now()
    print(dt)
    # here, now.tzinfo is None, it's a naive datetime
    #dt1=datetime.datetime.strptime(dt,'%Y-%m-%d %H:%M:%S.%f')
    dt = pytz.utc.localize(dt)

    dure = rf - rd
    minutes = dure.seconds / 60

    request.session['quizi'] = allQui
    try:
        s=submitEval.objects.get(idev=allQui,idetud=idet)
        message = "vous avez deja passé cette evaluation"
        return render(request,'myblog/exception.html',{'message':message})
    except submitEval.DoesNotExist:
      a = contenirEval.objects.filter(idQuiz=evaluation.objects.get(id_quiz=allQui)).values('idQuestion')
      k=0
      #print(k)
      q = []
      repo = []
    for i in a:
        c = question.objects.filter(id_question=i['idQuestion'])
        r = reponse.objects.filter(idQuest=i['idQuestion'])
        k=k+1
        q.extend(c)
        repo.extend(r)

    return render(request, 'myblog/home3Eval.html', {'questi': q, 'ref': repo, 'duree': minutes, 'dt': dt, 'rd': rd,'k':k})

def home3Eval(request):
    return render(request, 'myblog/home3.html')
def traitEval(request):

    #timi = request.POST["tim"]
    #print(timi)
   # timi1=datetime.datetime.strptime(timi,'%Y-%m-%d %H:%M:%S.%f')


    #timi=datetime.datetime.strptime(timi,"%Y-%m-%d %H:%M:%S")

    #timi1 =timi + timedelta(minutes=1)
    idet = request.session['et']
    resultat = request.POST.getlist('choix')
    repoChoisi = []
    iq = request.session['quizi']
    h= request.POST["val"]
    tot=request.POST["total"]
    #dt1 = request.session['tim']
    print(h)
    f = submitEval(idev=evaluation.objects.get(id_quiz=iq), idetud=Etudiant.objects.get(idEtudiant=idet),note=h,totalQ=tot)
    f.save()
    for f in resultat:
        lm = reponse.objects.filter(id_reponse=f)
        repoChoisi.extend(lm)

        a = contenirEval.objects.filter(idQuiz=evaluation.objects.get(id_quiz=iq)).values('idQuestion')
        print(a)
        q = []
        repo = []
    for i in a:
        c = question.objects.filter(id_question=i['idQuestion'])
        r = reponse.objects.filter(idQuest=i['idQuestion'])
        q.extend(c)
        repo.extend(r)
    for b in resultat:
            info = reponse2(id_quizs=evaluation.objects.get(id_quiz=iq), idEtudiants=Etudiant.objects.get(idEtudiant=idet), id_reponses=reponse.objects.get(id_reponse=b))
            info.save()

    return render(request, 'myblog/correctionEval.html', {'questi': q, 'ref': repo, 'bb': repoChoisi,'note':h,'tot':tot})


def correctionEval(request):
    return render(request, 'myblog/correctionEval.html')

def logout(request):

    auth.logout(request)
    return redirect('/')

def extractNote(request):
    ideva = request.POST["allEvaluations"]
    score = submitEval.objects.filter(idev=ideva)
    l=score.values('idetud')
    students=[]
    for i in l :
        r= Etudiant.objects.filter(idEtudiant=i['idetud'])
        students.extend(r)

    return render(request, 'myblog/listNotes.html', {'scores':score,'etu':students})

def selectNote(request):
    idens = request.session['k']
    ext =evaluation.objects.filter(id_Enseignant=idens)
    return render(request,'myblog/selectNote.html',{'evalute':ext})

def listNotes(request):
    return render(request, 'myblog/listNotes.html')
def detailsEval(request):
    iq = request.session['quizi']
    a = contenirEval.objects.filter(idQuiz=evaluation.objects.get(id_quiz=iq)).values('idQuestion')
    print(a)
    z = []
    repa = []
    for i in a:
        c = question.objects.filter(id_question=i['idQuestion'])
        r = reponse.objects.filter(idQuest=i['idQuestion'])
        z.extend(c)
        repa.extend(r)

    return render(request, 'myblog/correctionDetailsEval.html', {'questi': z, 'ref': repa})
def correctionDetailsEval(request):
    return render(request, 'myblog/correctionEval.html')


def comments(request):
    Comments = request.POST["com"]
    idet = request.session['et']
    infos = comment(idEtt=Etudiant.objects.get(idEtudiant=idet),commentaire = Comments)
    infos.save()
    return render(request, 'myblog/correctionDetails.html')

def recup(request):
    idet = request.session['et']
    iq = request.session['quizi']
    c = reponse2(idEtudiants=Etudiant.objects.get(idEtudiant=idet),id_reponses=reponse.objects.get(id_reponse=request.id_reponse),id_quizs=evaluation.objects.get(id_quiz=iq))
    return render(request, 'myblog/rep.html', {'c': c })

def rep(request):
    return render(request, 'myblog/rep.html')

class GeneratePdf(View):

        def get(self, request, *args, **kwargs):
            data = {
                'nom': 'lasi',
                'prenom':'kawtar',
                'note': '2',
            }
            pdf = render_to_pdf('myblog/extrat.html', data)
            return HttpResponse(pdf, content_type='application/pdf')

def extrat(request):
    return render(request, 'myblog/extrat.html')

def correct(request):
    result = request.POST('kl')
    idet = request.session['et']
    lm = reponse2.objects.filter(idEtudiants= idet, id_quizs=result)
    return render(request, 'myblog/correct1.html',{'cc': lm})

def correct1(request):
    return render(request, 'myblog/correct1.html')
def notes(request):
    idet = request.session['et']
    d = submitEval.objects.filter(idetud=idet)
    return render(request, 'myblog/note.html',{'d': d})

def note(request):
    return render(request, 'myblog/note.html')
def cor(request):
    k=request.POST["ch"]
    idet = request.session['et']
    l = reponse.objects.all()
    j = submitEval.objects.all
    r=reponse2.objects.filter(id_quizs=evaluation.objects.get(id_quiz=k),idEtudiants=idet)
    print(r)
    #c = reponse.objects.filter()
    return render(request, 'myblog/home2Eval.html', {'evi': r, 'cc': l,'j': j})
