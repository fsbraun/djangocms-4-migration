from django.db import migrations


def forwards(apps, schema_editor):
    Title = apps.get_model('djangocms_4_migration', 'Title')
    PageContent = apps.get_model('djangocms_4_migration', 'PageContent')
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Get all permissions related to the Title model
    title_permissions = Permission.objects.filter(content_type__app='cms', content_type__model='title')

    for perm in title_permissions:
        # Create the same permission for the PageContent model
        perm.pk = None
        perm.content_type = PageContent._meta.get_field('content_type').related_model.objects.get(model='pagecontent')
        perm.save()

        # Assign the new permission to users and groups
        for user in User.objects.filter(user_permissions=perm):
            user.user_permissions.add(perm)

        for group in Group.objects.filter(permissions=perm):
            group.permissions.add(perm)


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_4_migration', '0003_page_version_integration_data_migration'),
    ]

    run_before = [
        ('cms', '0023_placeholder_source_field'),  # Be sure to run before CMS 4.0 migrations. After all 3.5 have run.
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
