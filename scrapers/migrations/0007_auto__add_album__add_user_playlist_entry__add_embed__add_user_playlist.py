# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Album'
        db.create_table('scrapers_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('full_title', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('album_type', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('mbid', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal('scrapers', ['Album'])

        # Adding M2M table for field artists on 'Album'
        m2m_table_name = db.shorten_name('scrapers_album_artists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm['scrapers.album'], null=False)),
            ('artist', models.ForeignKey(orm['scrapers.artist'], null=False))
        ))
        db.create_unique(m2m_table_name, ['album_id', 'artist_id'])

        # Adding M2M table for field labels on 'Album'
        m2m_table_name = db.shorten_name('scrapers_album_labels')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('album', models.ForeignKey(orm['scrapers.album'], null=False)),
            ('label', models.ForeignKey(orm['scrapers.label'], null=False))
        ))
        db.create_unique(m2m_table_name, ['album_id', 'label_id'])

        # Adding model 'User_playlist_entry'
        db.create_table('scrapers_user_playlist_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('scrapers', ['User_playlist_entry'])

        # Adding M2M table for field sounds on 'User_playlist_entry'
        m2m_table_name = db.shorten_name('scrapers_user_playlist_entry_sounds')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user_playlist_entry', models.ForeignKey(orm['scrapers.user_playlist_entry'], null=False)),
            ('sound', models.ForeignKey(orm['scrapers.sound'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_playlist_entry_id', 'sound_id'])

        # Adding M2M table for field embeds on 'User_playlist_entry'
        m2m_table_name = db.shorten_name('scrapers_user_playlist_entry_embeds')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user_playlist_entry', models.ForeignKey(orm['scrapers.user_playlist_entry'], null=False)),
            ('embed', models.ForeignKey(orm['scrapers.embed'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_playlist_entry_id', 'embed_id'])

        # Adding M2M table for field albums on 'User_playlist_entry'
        m2m_table_name = db.shorten_name('scrapers_user_playlist_entry_albums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user_playlist_entry', models.ForeignKey(orm['scrapers.user_playlist_entry'], null=False)),
            ('album', models.ForeignKey(orm['scrapers.album'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_playlist_entry_id', 'album_id'])

        # Adding model 'Embed'
        db.create_table('scrapers_embed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('playlist_boolean', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('host_id', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('full_title', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal('scrapers', ['Embed'])

        # Adding M2M table for field sounds on 'Embed'
        m2m_table_name = db.shorten_name('scrapers_embed_sounds')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('embed', models.ForeignKey(orm['scrapers.embed'], null=False)),
            ('sound', models.ForeignKey(orm['scrapers.sound'], null=False))
        ))
        db.create_unique(m2m_table_name, ['embed_id', 'sound_id'])

        # Adding model 'User_playlist'
        db.create_table('scrapers_user_playlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('scrapers', ['User_playlist'])

        # Adding M2M table for field users on 'User_playlist'
        m2m_table_name = db.shorten_name('scrapers_user_playlist_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user_playlist', models.ForeignKey(orm['scrapers.user_playlist'], null=False)),
            ('userprofile', models.ForeignKey(orm['scrapers.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_playlist_id', 'userprofile_id'])

        # Adding M2M table for field entries on 'User_playlist'
        m2m_table_name = db.shorten_name('scrapers_user_playlist_entries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user_playlist', models.ForeignKey(orm['scrapers.user_playlist'], null=False)),
            ('user_playlist_entry', models.ForeignKey(orm['scrapers.user_playlist_entry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_playlist_id', 'user_playlist_entry_id'])

        # Adding M2M table for field albums on 'UserProfile'
        m2m_table_name = db.shorten_name('scrapers_userprofile_albums')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['scrapers.userprofile'], null=False)),
            ('album', models.ForeignKey(orm['scrapers.album'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'album_id'])

        # Adding field 'Sound.date_created'
        db.add_column('scrapers_sound', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Album'
        db.delete_table('scrapers_album')

        # Removing M2M table for field artists on 'Album'
        db.delete_table(db.shorten_name('scrapers_album_artists'))

        # Removing M2M table for field labels on 'Album'
        db.delete_table(db.shorten_name('scrapers_album_labels'))

        # Deleting model 'User_playlist_entry'
        db.delete_table('scrapers_user_playlist_entry')

        # Removing M2M table for field sounds on 'User_playlist_entry'
        db.delete_table(db.shorten_name('scrapers_user_playlist_entry_sounds'))

        # Removing M2M table for field embeds on 'User_playlist_entry'
        db.delete_table(db.shorten_name('scrapers_user_playlist_entry_embeds'))

        # Removing M2M table for field albums on 'User_playlist_entry'
        db.delete_table(db.shorten_name('scrapers_user_playlist_entry_albums'))

        # Deleting model 'Embed'
        db.delete_table('scrapers_embed')

        # Removing M2M table for field sounds on 'Embed'
        db.delete_table(db.shorten_name('scrapers_embed_sounds'))

        # Deleting model 'User_playlist'
        db.delete_table('scrapers_user_playlist')

        # Removing M2M table for field users on 'User_playlist'
        db.delete_table(db.shorten_name('scrapers_user_playlist_users'))

        # Removing M2M table for field entries on 'User_playlist'
        db.delete_table(db.shorten_name('scrapers_user_playlist_entries'))

        # Removing M2M table for field albums on 'UserProfile'
        db.delete_table(db.shorten_name('scrapers_userprofile_albums'))

        # Deleting field 'Sound.date_created'
        db.delete_column('scrapers_sound', 'date_created')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scrapers.album': {
            'Meta': {'object_name': 'Album'},
            'album_type': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'albums'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Artist']"}),
            'full_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'albums'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Label']"}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        'scrapers.artist': {
            'Meta': {'object_name': 'Artist'},
            'artist_duplicates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'artist_duplicates_rel_+'", 'null': 'True', 'to': "orm['scrapers.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'artists'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Label']"}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'artists'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Post']"}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'artists'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Sound']"}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'artists'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Source']"})
        },
        'scrapers.embed': {
            'Meta': {'object_name': 'Embed'},
            'full_title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'host_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'playlist_boolean': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'embeds'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Sound']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        'scrapers.label': {
            'Meta': {'object_name': 'Label'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_duplicates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'label_duplicates_rel_+'", 'null': 'True', 'to': "orm['scrapers.Label']"}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'labels'", 'null': 'True', 'to': "orm['scrapers.Post']"}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'labels'", 'null': 'True', 'to': "orm['scrapers.Sound']"}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'labels'", 'null': 'True', 'to': "orm['scrapers.Source']"})
        },
        'scrapers.mbz_release': {
            'Meta': {'object_name': 'mbz_release'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mbz_catalog_number': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'mbz_reid': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'scrapers.mix_series': {
            'Meta': {'object_name': 'Mix_Series'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mixes': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'mix series'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.MixesDB_mix']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'scrapers.mixesdb_mix': {
            'Meta': {'object_name': 'MixesDB_mix'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'mixes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'mixes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Label']"}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mix_duplicates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'mix_duplicates_rel_+'", 'null': 'True', 'to': "orm['scrapers.MixesDB_mix']"}),
            'original_slug': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'mixes'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Sound']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        'scrapers.playlist': {
            'Meta': {'object_name': 'Playlist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sc_playlist_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'playlists'", 'null': 'True', 'to': "orm['scrapers.Sound']"}),
            'vimeo_playlist_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'yt_playlist_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        'scrapers.post': {
            'Meta': {'object_name': 'Post'},
            'date_posted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'playlist': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'posts'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Playlist']"}),
            'post_url': ('django.db.models.fields.TextField', [], {}),
            'sound': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'posts'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Sound']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'null': 'True', 'to': "orm['scrapers.Source']"})
        },
        'scrapers.release': {
            'Meta': {'object_name': 'Release'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'releases'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Artist']"}),
            'catalog_number': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'date_released_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'releases'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Label']"}),
            'primary_type': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'release_group_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'release_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'secondary_types': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        'scrapers.release_group': {
            'Meta': {'object_name': 'Release_group'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'release_groups'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Artist']"}),
            'date_released': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'release_groups'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Label']"}),
            'mbz_releases': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'release_groups'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.mbz_release']"}),
            'mbz_rgid': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'release_groups'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Sound']"}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'release_groups'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Source']"})
        },
        'scrapers.sound': {
            'Meta': {'object_name': 'Sound'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'original_slug': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'sc_full_name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'sc_track_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'sc_username': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'scraped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sound_duplicates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sound_duplicates_rel_+'", 'null': 'True', 'to': "orm['scrapers.Sound']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'vimeo_track_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'vimeo_username': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'yt_track_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        },
        'scrapers.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'source'", 'null': 'True', 'to': "orm['scrapers.Sound']"}),
            'url': ('django.db.models.fields.TextField', [], {'unique': 'True', 'blank': 'True'})
        },
        'scrapers.user_playlist': {
            'Meta': {'object_name': 'User_playlist'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'entries': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_playlists'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.User_playlist_entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_playlists'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.UserProfile']"})
        },
        'scrapers.user_playlist_entry': {
            'Meta': {'object_name': 'User_playlist_entry'},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_playlist_entries'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Album']"}),
            'embeds': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_playlist_entries'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Embed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_playlist_entries'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Sound']"})
        },
        'scrapers.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'albums': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'users'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Album']"}),
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'users'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'users'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Label']"}),
            'mix_series': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'users'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Mix_Series']"}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'users'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Sound']"}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'users'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Source']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['scrapers']