# Generated by Django 5.1.1 on 2024-10-25 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercio', '0009_alter_encuesta_plato'),
    ]

    operations = [
        migrations.AddField(
            model_name='plato',
            name='categoria',
            field=models.CharField(blank=True, choices=[('dulce', 'Dulce'), ('postre', 'Postre'), ('te', 'Te')], max_length=10, null=True),
        ),
    ]