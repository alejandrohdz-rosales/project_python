from django.db import migrations


def assign_customer_organization(apps, schema_editor):
    Organization = apps.get_model('users', 'Organization')
    Customer = apps.get_model('sales', 'Customer')
    User = apps.get_model('users', 'User')

    default_org = Organization.objects.filter(slug='default').first()
    if default_org is None:
        default_org = Organization.objects.create(
            slug='default',
            name='Default Organization',
        )

    for customer in Customer.objects.filter(organization__isnull=True).iterator():
        if customer.agent_id:
            agent = User.objects.filter(pk=customer.agent_id).first()
            if agent and agent.organization_id:
                customer.organization_id = agent.organization_id
                customer.save(update_fields=['organization_id'])
                continue
        customer.organization_id = default_org.id
        customer.save(update_fields=['organization_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_customer_organization'),
    ]

    operations = [
        migrations.RunPython(assign_customer_organization, migrations.RunPython.noop),
    ]
