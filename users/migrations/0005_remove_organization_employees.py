# Generated by Django 5.1.2 on 2024-10-24 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_organization_capital_alter_organization_debt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='employees',
        ),
    ]
