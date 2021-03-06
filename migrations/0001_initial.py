# Generated by Django 3.0.2 on 2020-05-06 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='departement',
            fields=[
                ('iddepartement', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='enseignant',
            fields=[
                ('idEnseignant', models.AutoField(primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=20, unique=True)),
                ('nom', models.TextField()),
                ('prenom', models.TextField()),
                ('estAdmin', models.BooleanField()),
                ('motDePasse', models.CharField(max_length=20)),
                ('iddepartement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.departement')),
            ],
        ),
        migrations.CreateModel(
            name='matiere',
            fields=[
                ('idmatiere', models.AutoField(primary_key=True, serialize=False)),
                ('nomMatiere', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='niveau',
            fields=[
                ('id_niveau', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='question',
            fields=[
                ('id_question', models.AutoField(primary_key=True, serialize=False)),
                ('questionA', models.TextField()),
                ('explication', models.TextField()),
                ('difficulte', models.IntegerField()),
                ('idEnsei', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.enseignant')),
                ('idMatiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.matiere')),
            ],
        ),
        migrations.CreateModel(
            name='reponse',
            fields=[
                ('id_reponse', models.AutoField(primary_key=True, serialize=False)),
                ('response', models.TextField()),
                ('estVrai', models.BooleanField()),
                ('commentaire', models.TextField()),
                ('idQuest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.question')),
            ],
        ),
        migrations.CreateModel(
            name='quiz',
            fields=[
                ('id_quiz', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=20)),
                ('id_Enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.enseignant')),
                ('id_niveau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.niveau')),
                ('idmatiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.matiere')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='filiere',
            fields=[
                ('idfiliere', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=20)),
                ('iddepartement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.departement')),
            ],
        ),
        migrations.CreateModel(
            name='evaluation',
            fields=[
                ('id_quiz', models.AutoField(primary_key=True, serialize=False)),
                ('dateDebut', models.DateTimeField()),
                ('dateFin', models.DateTimeField()),
                ('description', models.CharField(max_length=20)),
                ('id_Enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.enseignant')),
                ('id_niveau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.niveau')),
                ('idmatiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.matiere')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('idEtudiant', models.AutoField(primary_key=True, serialize=False)),
                ('login', models.CharField(max_length=20, unique=True)),
                ('nom', models.TextField()),
                ('prenom', models.TextField()),
                ('motDePasse', models.CharField(max_length=20)),
                ('idfiliere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.filiere')),
            ],
        ),
        migrations.CreateModel(
            name='contenirEval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idQuestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.question')),
                ('idQuiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.evaluation')),
            ],
        ),
        migrations.CreateModel(
            name='contenir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idQuestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.question')),
                ('idQuiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='appartenir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idEnseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.enseignant')),
                ('idfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.filiere')),
            ],
        ),
        migrations.CreateModel(
            name='apparMATFil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idMat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.matiere')),
                ('idfilli', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.filiere')),
            ],
        ),
        migrations.CreateModel(
            name='submitEval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitDate', models.DateTimeField(auto_now_add=True)),
                ('begintDate', models.DateTimeField(auto_now_add=True)),
                ('note', models.IntegerField()),
                ('totalQ', models.IntegerField()),
                ('idetud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.Etudiant')),
                ('idev', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.evaluation')),
            ],
            options={
                'unique_together': {('idev', 'idetud')},
            },
        ),
    ]
