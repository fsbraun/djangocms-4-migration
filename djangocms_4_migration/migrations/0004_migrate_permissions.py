from django.db import migrations


def forwards(apps, schema_editor):
    PageContent = apps.get_model('cms', 'PageContent')
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Get all permissions related to the Title model
    title_permissions = Permission.objects.filter(content_type__app_label='cms', content_type__model='title')

    for perm in title_permissions:
        # Create the same permission for the PageContent model
        new_perm, _ = Permission.objects.get_or_create(
            codename=perm.codename,
            name=perm.name,
            content_type=PageContent._meta.get_field('content_type').related_model.objects.get(model='pagecontent')
        )

        # Assign the new permission to users and groups
        for user in User.objects.filter(user_permissions=perm):
            user.user_permissions.add(new_perm)

        for group in Group.objects.filter(permissions=perm):
            group.permissions.add(new_perm)


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_4_migration', '0003_page_version_integration_data_migration'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
