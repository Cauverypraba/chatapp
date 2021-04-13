# Generated by Django 3.1.5 on 2021-04-13 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('real_chat', '0006_auto_20210407_0801'),
    ]

    operations = [
        migrations.CreateModel(
            name='HiddenFriends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curr_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='real_chat.user')),
                ('users', models.ManyToManyField(to='real_chat.user')),
            ],
        ),
    ]
