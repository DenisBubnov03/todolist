# Generated by Django 4.1.5 on 2023-01-27 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_board_boardparticipant'),
    ]

    operations = [
        migrations.AddField(
            model_name='goalcategory',
            name='board',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='goals.board', verbose_name='Доска'),
        ),
    ]
