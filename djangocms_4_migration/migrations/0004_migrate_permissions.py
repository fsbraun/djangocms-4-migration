from django.db import migrations


def forwards(apps, schema_editor):
    PageContent = apps.get_model('cms', 'PageContent')
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Get all permissions related to the Title model
    title_permissions = Permission.objects.filter(content_type__app_label='cms', content_type__model='pagecontent')

    for perm in title_permissions:
        perm.codename.replace('_title', '_pagecontent')
        perm.name.replace(' title', ' pagecontent')
        perm.save()
        # Create the same permission for the PageContent model
        version_perm, _ = Permission.objects.get_or_create(
            codename=perm.codename.replace('_title', '_pagecontentversion'),
            name=perm.name.replace(' title', ' pagecontentversion'),
            content_type=PageContent._meta.get_field('content_type').related_model.objects.get(model='pagecontentversion')
        )

        # Assign the new permission to users and groups
        for user in User.objects.filter(user_permissions=perm):
            user.user_permissions.add(version_perm)

        for group in Group.objects.filter(permissions=perm):
            group.permissions.add(version_perm)


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_4_migration', '0003_page_version_integration_data_migration'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
