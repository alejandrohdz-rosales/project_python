import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
        ('sales', '0006_customer_org_email_unique'),
        ('users', '0007_user_add_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='organization',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='customers',
                to='organizations.organization',
            ),
        ),
    ]
