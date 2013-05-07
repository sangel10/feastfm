# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sound'
        db.create_table('scrapers_sound', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('original_slug', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('yt_track_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500, blank=True)),
            ('sc_track_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500, blank=True)),
            ('vimeo_track_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500, blank=True)),
            ('sc_username', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('sc_full_name', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('vimeo_username', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('sc_release', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('sc_label', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('first_appeared', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('DJ_set', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tracklist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('original_tracklist', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('mix_series', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('mix_series_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('discogs_id', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('release_number', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('length', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('scrapers', ['Sound'])

        # Adding M2M table for field tracklist_models on 'Sound'
        db.create_table('scrapers_sound_tracklist_models', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_sound', models.ForeignKey(orm['scrapers.sound'], null=False)),
            ('to_sound', models.ForeignKey(orm['scrapers.sound'], null=False))
        ))
        db.create_unique('scrapers_sound_tracklist_models', ['from_sound_id', 'to_sound_id'])

        # Adding M2M table for field sound_duplicates on 'Sound'
        db.create_table('scrapers_sound_sound_duplicates', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_sound', models.ForeignKey(orm['scrapers.sound'], null=False)),
            ('to_sound', models.ForeignKey(orm['scrapers.sound'], null=False))
        ))
        db.create_unique('scrapers_sound_sound_duplicates', ['from_sound_id', 'to_sound_id'])

        # Adding model 'Source'
        db.create_table('scrapers_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.TextField')(unique=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('scrapers', ['Source'])

        # Adding M2M table for field sounds on 'Source'
        db.create_table('scrapers_source_sounds', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('source', models.ForeignKey(orm['scrapers.source'], null=False)),
            ('sound', models.ForeignKey(orm['scrapers.sound'], null=False))
        ))
        db.create_unique('scrapers_source_sounds', ['source_id', 'sound_id'])

        # Adding model 'Playlist'
        db.create_table('scrapers_playlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sc_playlist_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500, blank=True)),
            ('yt_playlist_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500, blank=True)),
            ('vimeo_playlist_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=500, blank=True)),
            ('tracklist', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('scrapers', ['Playlist'])

        # Adding M2M table for field sounds on 'Playlist'
        db.create_table('scrapers_playlist_sounds', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('playlist', models.ForeignKey(orm['scrapers.playlist'], null=False)),
            ('sound', models.ForeignKey(orm['scrapers.sound'], null=False))
        ))
        db.create_unique('scrapers_playlist_sounds', ['playlist_id', 'sound_id'])

        # Adding model 'Post'
        db.create_table('scrapers_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post_url', self.gf('django.db.models.fields.TextField')(unique=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['scrapers.Source'])),
            ('date_posted', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('scrapers', ['Post'])

        # Adding M2M table for field playlist on 'Post'
        db.create_table('scrapers_post_playlist', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['scrapers.post'], null=False)),
            ('playlist', models.ForeignKey(orm['scrapers.playlist'], null=False))
        ))
        db.create_unique('scrapers_post_playlist', ['post_id', 'playlist_id'])

        # Adding M2M table for field sound on 'Post'
        db.create_table('scrapers_post_sound', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['scrapers.post'], null=False)),
            ('sound', models.ForeignKey(orm['scrapers.sound'], null=False))
        ))
        db.create_unique('scrapers_post_sound', ['post_id', 'sound_id'])

        # Adding model 'Label'
        db.create_table('scrapers_label', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('scrapers', ['Label'])

        # Adding M2M table for field label_duplicates on 'Label'
        db.create_table('scrapers_label_label_duplicates', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_label', models.ForeignKey(orm['scrapers.label'], null=False)),
            ('to_label', models.ForeignKey(orm['scrapers.label'], null=False))
        ))
        db.create_unique('scrapers_label_label_duplicates', ['from_label_id', 'to_label_id'])

        # Adding M2M table for field sounds on 'Label'
        db.create_table('scrapers_label_sounds', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('label', models.ForeignKey(orm['scrapers.label'], null=False)),
            ('sound', models.ForeignKey(orm['scrapers.sound'], null=False))
        ))
        db.create_unique('scrapers_label_sounds', ['label_id', 'sound_id'])

        # Adding M2M table for field sources on 'Label'
        db.create_table('scrapers_label_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('label', models.ForeignKey(orm['scrapers.label'], null=False)),
            ('source', models.ForeignKey(orm['scrapers.source'], null=False))
        ))
        db.create_unique('scrapers_label_sources', ['label_id', 'source_id'])

        # Adding M2M table for field posts on 'Label'
        db.create_table('scrapers_label_posts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('label', models.ForeignKey(orm['scrapers.label'], null=False)),
            ('post', models.ForeignKey(orm['scrapers.post'], null=False))
        ))
        db.create_unique('scrapers_label_posts', ['label_id', 'post_id'])

        # Adding model 'Artist'
        db.create_table('scrapers_artist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal('scrapers', ['Artist'])

        # Adding M2M table for field artist_duplicates on 'Artist'
        db.create_table('scrapers_artist_artist_duplicates', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_artist', models.ForeignKey(orm['scrapers.artist'], null=False)),
            ('to_artist', models.ForeignKey(orm['scrapers.artist'], null=False))
        ))
        db.create_unique('scrapers_artist_artist_duplicates', ['from_artist_id', 'to_artist_id'])

        # Adding M2M table for field labels on 'Artist'
        db.create_table('scrapers_artist_labels', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artist', models.ForeignKey(orm['scrapers.artist'], null=False)),
            ('label', models.ForeignKey(orm['scrapers.label'], null=False))
        ))
        db.create_unique('scrapers_artist_labels', ['artist_id', 'label_id'])

        # Adding M2M table for field sounds on 'Artist'
        db.create_table('scrapers_artist_sounds', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artist', models.ForeignKey(orm['scrapers.artist'], null=False)),
            ('sound', models.ForeignKey(orm['scrapers.sound'], null=False))
        ))
        db.create_unique('scrapers_artist_sounds', ['artist_id', 'sound_id'])

        # Adding M2M table for field sources on 'Artist'
        db.create_table('scrapers_artist_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artist', models.ForeignKey(orm['scrapers.artist'], null=False)),
            ('source', models.ForeignKey(orm['scrapers.source'], null=False))
        ))
        db.create_unique('scrapers_artist_sources', ['artist_id', 'source_id'])

        # Adding M2M table for field posts on 'Artist'
        db.create_table('scrapers_artist_posts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artist', models.ForeignKey(orm['scrapers.artist'], null=False)),
            ('post', models.ForeignKey(orm['scrapers.post'], null=False))
        ))
        db.create_unique('scrapers_artist_posts', ['artist_id', 'post_id'])


    def backwards(self, orm):
        # Deleting model 'Sound'
        db.delete_table('scrapers_sound')

        # Removing M2M table for field tracklist_models on 'Sound'
        db.delete_table('scrapers_sound_tracklist_models')

        # Removing M2M table for field sound_duplicates on 'Sound'
        db.delete_table('scrapers_sound_sound_duplicates')

        # Deleting model 'Source'
        db.delete_table('scrapers_source')

        # Removing M2M table for field sounds on 'Source'
        db.delete_table('scrapers_source_sounds')

        # Deleting model 'Playlist'
        db.delete_table('scrapers_playlist')

        # Removing M2M table for field sounds on 'Playlist'
        db.delete_table('scrapers_playlist_sounds')

        # Deleting model 'Post'
        db.delete_table('scrapers_post')

        # Removing M2M table for field playlist on 'Post'
        db.delete_table('scrapers_post_playlist')

        # Removing M2M table for field sound on 'Post'
        db.delete_table('scrapers_post_sound')

        # Deleting model 'Label'
        db.delete_table('scrapers_label')

        # Removing M2M table for field label_duplicates on 'Label'
        db.delete_table('scrapers_label_label_duplicates')

        # Removing M2M table for field sounds on 'Label'
        db.delete_table('scrapers_label_sounds')

        # Removing M2M table for field sources on 'Label'
        db.delete_table('scrapers_label_sources')

        # Removing M2M table for field posts on 'Label'
        db.delete_table('scrapers_label_posts')

        # Deleting model 'Artist'
        db.delete_table('scrapers_artist')

        # Removing M2M table for field artist_duplicates on 'Artist'
        db.delete_table('scrapers_artist_artist_duplicates')

        # Removing M2M table for field labels on 'Artist'
        db.delete_table('scrapers_artist_labels')

        # Removing M2M table for field sounds on 'Artist'
        db.delete_table('scrapers_artist_sounds')

        # Removing M2M table for field sources on 'Artist'
        db.delete_table('scrapers_artist_sources')

        # Removing M2M table for field posts on 'Artist'
        db.delete_table('scrapers_artist_posts')


    models = {
        'scrapers.artist': {
            'Meta': {'object_name': 'Artist'},
            'artist_duplicates': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'artist_duplicates_rel_+'", 'blank': 'True', 'to': "orm['scrapers.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'artists'", 'blank': 'True', 'to': "orm['scrapers.Label']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'artists'", 'blank': 'True', 'to': "orm['scrapers.Post']"}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'artists'", 'blank': 'True', 'to': "orm['scrapers.Sound']"}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'artists'", 'blank': 'True', 'to': "orm['scrapers.Source']"})
        },
        'scrapers.label': {
            'Meta': {'object_name': 'Label'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_duplicates': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'label_duplicates_rel_+'", 'blank': 'True', 'to': "orm['scrapers.Label']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'labels'", 'symmetrical': 'False', 'to': "orm['scrapers.Post']"}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'labels'", 'symmetrical': 'False', 'to': "orm['scrapers.Sound']"}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'labels'", 'symmetrical': 'False', 'to': "orm['scrapers.Source']"})
        },
        'scrapers.playlist': {
            'Meta': {'object_name': 'Playlist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sc_playlist_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500', 'blank': 'True'}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'playlists'", 'symmetrical': 'False', 'to': "orm['scrapers.Sound']"}),
            'tracklist': ('django.db.models.fields.TextField', [], {}),
            'vimeo_playlist_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500', 'blank': 'True'}),
            'yt_playlist_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500', 'blank': 'True'})
        },
        'scrapers.post': {
            'Meta': {'object_name': 'Post'},
            'date_posted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'playlist': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'posts'", 'blank': 'True', 'to': "orm['scrapers.Playlist']"}),
            'post_url': ('django.db.models.fields.TextField', [], {'unique': 'True'}),
            'sound': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'posts'", 'blank': 'True', 'to': "orm['scrapers.Sound']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['scrapers.Source']"})
        },
        'scrapers.sound': {
            'DJ_set': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'Meta': {'object_name': 'Sound'},
            'discogs_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'first_appeared': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mix_series': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'mix_series_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original_slug': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'original_tracklist': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'release_number': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'sc_full_name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'sc_label': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'sc_release': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'sc_track_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500', 'blank': 'True'}),
            'sc_username': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'sound_duplicates': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'sound_duplicates_rel_+'", 'blank': 'True', 'to': "orm['scrapers.Sound']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'tracklist': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tracklist_models': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tracklist_models_rel_+'", 'blank': 'True', 'to': "orm['scrapers.Sound']"}),
            'vimeo_track_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500', 'blank': 'True'}),
            'vimeo_username': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'yt_track_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '500', 'blank': 'True'})
        },
        'scrapers.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'source'", 'symmetrical': 'False', 'to': "orm['scrapers.Sound']"}),
            'url': ('django.db.models.fields.TextField', [], {'unique': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['scrapers']