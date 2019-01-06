# Generated by Django 2.1.4 on 2019-01-05 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('serviceID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('serviceTypeID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='serviceType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shifts.ServiceType'),
        ),
    ]