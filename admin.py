from django.contrib import admin
from .models import enseignant, reponse2,comment
from .models import departement
from .models import filiere
from .models import appartenir
from .models import matiere
from .models import question
from .models import reponse
from .models import niveau
from .models import evaluation,quiz,apparMATFil
from .models import Etudiant,contenir,contenirEval,submitEval
admin.site.register(enseignant)
admin.site.register(departement)
admin.site.register(filiere)
admin.site.register(appartenir)
admin.site.register(matiere)
class questionAdmin(admin.ModelAdmin):
   list_display=('id_question','questionA')
admin.site.register(question,questionAdmin)

admin.site.register(reponse)
admin.site.register(niveau)
admin.site.register(evaluation)
admin.site.register(quiz)
admin.site.register(Etudiant)
admin.site.register(contenir)
admin.site.register(contenirEval)
admin.site.register(submitEval)
admin.site.register(apparMATFil)
admin.site.register(reponse2)
admin.site.register(comment)


# Register your models here.
