# Generated by Django 5.1.2 on 2024-11-10 02:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercio', '0013_alter_plato_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='comercio.factura')),
                ('plato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comercio.plato')),
            ],
        ),
    ]
