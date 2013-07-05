# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Post.source'
        db.alter_column('scrapers_post', 'source_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['scrapers.Source']))

    def backwards(self, orm):

        # Changing field 'Post.source'
        db.alter_column('scrapers_post', 'source_id', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['scrapers.Source']))

    models = {
        'scrapers.artist': {
            'Meta': {'object_name': 'Artist'},
            'artist_duplicates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'artist_duplicates_rel_+'", 'null': 'True', 'to': "orm['scrapers.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labels': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'artists'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Label']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'artists'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Post']"}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'artists'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Sound']"}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'artists'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['scrapers.Source']"})
        },
        'scrapers.label': {
            'Meta': {'object_name': 'Label'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_duplicates': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'label_duplicates_rel_+'", 'null': 'True', 'to': "orm['scrapers.Label']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'posts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'labels'", 'null': 'True', 'to': "orm['scrapers.Post']"}),
            'sounds': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'labels'", 'null': 'True', 'to': "orm['scrapers.Sound']"}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'labels'", 'null': 'True', 'to': "orm['scrapers.Source']"})
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
        'scrapers.sound': {
            'Meta': {'object_name': 'Sound'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original_slug': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'sc_full_name': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'sc_track_id': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'sc_username': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['scrapers']