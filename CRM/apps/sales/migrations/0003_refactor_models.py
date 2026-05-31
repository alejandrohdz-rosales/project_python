import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


def convert_null_phones_to_empty(apps, schema_editor):
    Customer = apps.get_model('sales', 'Customer')
    Customer.objects.filter(phone__isnull=True).update(phone='')


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomerModel',
            new_name='Customer',
        ),
        migrations.RenameModel(
            old_name='CallLogModel',
            new_name='CallLog',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='agent_id',
            new_name='agent',
        ),
        migrations.AddField(
            model_name='customer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.RunPython(convert_null_phones_to_empty, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='agent',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='customers',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='calllog',
            name='agent',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='calls_made',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='calllog',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'customer',
                'verbose_name_plural': 'customers',
            },
        ),
        migrations.AlterModelOptions(
            name='calllog',
            options={
                'ordering': ['-call_date'],
                'verbose_name': 'call log',
                'verbose_name_plural': 'call logs',
            },
        ),
    ]
