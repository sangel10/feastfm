# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
"""
from django.db import models

class Annotation(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.IntegerField()
    text = models.TextField(blank=True)
    changelog = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'annotation'

class Application(models.Model):
    id = models.IntegerField(primary_key=True)
    owner = models.IntegerField()
    name = models.TextField()
    oauth_id = models.TextField(unique=True)
    oauth_secret = models.TextField()
    oauth_redirect_uri = models.TextField(blank=True)
    class Meta:
        db_table = u'application'

class AreaType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = u'area_type'

class Area(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True) # This field type is a guess.
    name = models.CharField(max_length=-1)
    sort_name = models.CharField(max_length=-1)
    type = models.IntegerField(null=True, blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    begin_date_year = models.SmallIntegerField(null=True, blank=True)
    begin_date_month = models.SmallIntegerField(null=True, blank=True)
    begin_date_day = models.SmallIntegerField(null=True, blank=True)
    end_date_year = models.SmallIntegerField(null=True, blank=True)
    end_date_month = models.SmallIntegerField(null=True, blank=True)
    end_date_day = models.SmallIntegerField(null=True, blank=True)
    ended = models.BooleanField()
    class Meta:
        db_table = u'area'

class AreaGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) # This field type is a guess.
    new_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'area_gid_redirect'

class AreaAliasType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    class Meta:
        db_table = u'area_alias_type'

class AreaAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    area = models.IntegerField()
    name = models.CharField(max_length=-1)
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    sort_name = models.CharField(max_length=-1)
    begin_date_year = models.SmallIntegerField(null=True, blank=True)
    begin_date_month = models.SmallIntegerField(null=True, blank=True)
    begin_date_day = models.SmallIntegerField(null=True, blank=True)
    end_date_year = models.SmallIntegerField(null=True, blank=True)
    end_date_month = models.SmallIntegerField(null=True, blank=True)
    end_date_day = models.SmallIntegerField(null=True, blank=True)
    primary_for_locale = models.BooleanField()
    class Meta:
        db_table = u'area_alias'

class AreaAnnotation(models.Model):
    area = models.IntegerField()
    annotation = models.IntegerField()
    class Meta:
        db_table = u'area_annotation'

class Artist(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True) # This field type is a guess.
    name = models.IntegerField(unique=True)
    sort_name = models.IntegerField()
    begin_date_year = models.SmallIntegerField(null=True, blank=True)
    begin_date_month = models.SmallIntegerField(null=True, blank=True)
    begin_date_day = models.SmallIntegerField(null=True, blank=True)
    end_date_year = models.SmallIntegerField(null=True, blank=True)
    end_date_month = models.SmallIntegerField(null=True, blank=True)
    end_date_day = models.SmallIntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    ended = models.BooleanField()
    begin_area = models.IntegerField(null=True, blank=True)
    end_area = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'artist'

class ArtistAliasType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    class Meta:
        db_table = u'artist_alias_type'

class ArtistAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    artist = models.IntegerField()
    name = models.IntegerField()
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    sort_name = models.IntegerField()
    begin_date_year = models.SmallIntegerField(null=True, blank=True)
    begin_date_month = models.SmallIntegerField(null=True, blank=True)
    begin_date_day = models.SmallIntegerField(null=True, blank=True)
    end_date_year = models.SmallIntegerField(null=True, blank=True)
    end_date_month = models.SmallIntegerField(null=True, blank=True)
    end_date_day = models.SmallIntegerField(null=True, blank=True)
    primary_for_locale = models.BooleanField()
    class Meta:
        db_table = u'artist_alias'

class ArtistAnnotation(models.Model):
    artist = models.IntegerField()
    annotation = models.IntegerField()
    class Meta:
        db_table = u'artist_annotation'

class ArtistIpi(models.Model):
    artist = models.IntegerField()
    ipi = models.CharField(max_length=11)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'artist_ipi'

class ArtistIsni(models.Model):
    artist = models.IntegerField()
    isni = models.CharField(max_length=16)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'artist_isni'

class ArtistMeta(models.Model):
    id = models.IntegerField(primary_key=True)
    rating = models.SmallIntegerField(null=True, blank=True)
    rating_count = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'artist_meta'

class ArtistTag(models.Model):
    artist = models.IntegerField()
    tag = models.IntegerField()
    count = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'artist_tag'

class ArtistRatingRaw(models.Model):
    artist = models.IntegerField()
    editor = models.IntegerField()
    rating = models.SmallIntegerField()
    class Meta:
        db_table = u'artist_rating_raw'

class ArtistTagRaw(models.Model):
    artist = models.IntegerField()
    editor = models.IntegerField()
    tag = models.IntegerField()
    class Meta:
        db_table = u'artist_tag_raw'

class ArtistCredit(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.IntegerField()
    artist_count = models.SmallIntegerField()
    ref_count = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'artist_credit'

class ArtistCreditName(models.Model):
    artist_credit = models.IntegerField()
    position = models.SmallIntegerField()
    artist = models.IntegerField()
    name = models.IntegerField()
    join_phrase = models.TextField()
    class Meta:
        db_table = u'artist_credit_name'

class ArtistGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) # This field type is a guess.
    new_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'artist_gid_redirect'

class ArtistName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=-1, unique=True)
    class Meta:
        db_table = u'artist_name'

class ArtistType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = u'artist_type'

class AutoeditorElection(models.Model):
    id = models.IntegerField(primary_key=True)
    candidate = models.IntegerField()
    proposer = models.IntegerField()
    seconder_1 = models.IntegerField(null=True, blank=True)
    seconder_2 = models.IntegerField(null=True, blank=True)
    status = models.IntegerField()
    yes_votes = models.IntegerField()
    no_votes = models.IntegerField()
    propose_time = models.DateTimeField()
    open_time = models.DateTimeField(null=True, blank=True)
    close_time = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'autoeditor_election'

class AutoeditorElectionVote(models.Model):
    id = models.IntegerField(primary_key=True)
    autoeditor_election = models.IntegerField()
    voter = models.IntegerField()
    vote = models.IntegerField()
    vote_time = models.DateTimeField()
    class Meta:
        db_table = u'autoeditor_election_vote'

class Cdtoc(models.Model):
    id = models.IntegerField(primary_key=True)
    discid = models.CharField(max_length=28, unique=True)
    freedb_id = models.CharField(max_length=8)
    track_count = models.IntegerField()
    leadout_offset = models.IntegerField()
    track_offset = models.TextField() # This field type is a guess.
    degraded = models.BooleanField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'cdtoc'

class CdtocRaw(models.Model):
    id = models.IntegerField(primary_key=True)
    release = models.IntegerField()
    discid = models.CharField(max_length=28)
    track_count = models.IntegerField()
    leadout_offset = models.IntegerField()
    track_offset = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'cdtoc_raw'

class Clientversion(models.Model):
    id = models.IntegerField(primary_key=True)
    version = models.CharField(max_length=64)
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'clientversion'

class CountryArea(models.Model):
    area = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'country_area'

class Edit(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.IntegerField()
    type = models.SmallIntegerField()
    status = models.SmallIntegerField()
    data = models.TextField()
    yes_votes = models.IntegerField()
    no_votes = models.IntegerField()
    autoedit = models.SmallIntegerField()
    open_time = models.DateTimeField(null=True, blank=True)
    close_time = models.DateTimeField(null=True, blank=True)
    expire_time = models.DateTimeField()
    language = models.IntegerField(null=True, blank=True)
    quality = models.SmallIntegerField()
    class Meta:
        db_table = u'edit'

class EditNote(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.IntegerField()
    edit = models.IntegerField()
    text = models.TextField()
    post_time = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'edit_note'

class EditArea(models.Model):
    edit = models.IntegerField()
    area = models.IntegerField()
    class Meta:
        db_table = u'edit_area'

class EditArtist(models.Model):
    edit = models.IntegerField()
    artist = models.IntegerField()
    status = models.SmallIntegerField()
    class Meta:
        db_table = u'edit_artist'

class EditLabel(models.Model):
    edit = models.IntegerField()
    label = models.IntegerField()
    status = models.SmallIntegerField()
    class Meta:
        db_table = u'edit_label'

class EditRelease(models.Model):
    edit = models.IntegerField()
    release = models.IntegerField()
    class Meta:
        db_table = u'edit_release'

class EditReleaseGroup(models.Model):
    edit = models.IntegerField()
    release_group = models.IntegerField()
    class Meta:
        db_table = u'edit_release_group'

class EditRecording(models.Model):
    edit = models.IntegerField()
    recording = models.IntegerField()
    class Meta:
        db_table = u'edit_recording'

class EditWork(models.Model):
    edit = models.IntegerField()
    work = models.IntegerField()
    class Meta:
        db_table = u'edit_work'

class EditUrl(models.Model):
    edit = models.IntegerField()
    url = models.IntegerField()
    class Meta:
        db_table = u'edit_url'

class Editor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    privs = models.IntegerField(null=True, blank=True)
    email = models.CharField(max_length=64, blank=True)
    website = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    member_since = models.DateTimeField(null=True, blank=True)
    email_confirm_date = models.DateTimeField(null=True, blank=True)
    last_login_date = models.DateTimeField(null=True, blank=True)
    edits_accepted = models.IntegerField(null=True, blank=True)
    edits_rejected = models.IntegerField(null=True, blank=True)
    auto_edits_accepted = models.IntegerField(null=True, blank=True)
    edits_failed = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'editor'

class EditorLanguage(models.Model):
    editor = models.IntegerField()
    language = models.IntegerField()
    fluency = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'editor_language'

class EditorPreference(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.IntegerField()
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    class Meta:
        db_table = u'editor_preference'

class EditorSubscribeArtist(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.IntegerField()
    artist = models.IntegerField()
    last_edit_sent = models.IntegerField()
    deleted_by_edit = models.IntegerField()
    merged_by_edit = models.IntegerField()
    class Meta:
        db_table = u'editor_subscribe_artist'

class EditorSubscribeCollection(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.IntegerField()
    collection = models.IntegerField()
    last_edit_sent = models.IntegerField()
    available = models.BooleanField()
    last_seen_name = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'editor_subscribe_collection'

class EditorSubscribeLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.IntegerField()
    label = models.IntegerField()
    last_edit_sent = models.IntegerField()
    deleted_by_edit = models.IntegerField()
    merged_by_edit = models.IntegerField()
    class Meta:
        db_table = u'editor_subscribe_label'

class EditorSubscribeEditor(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.IntegerField()
    subscribed_editor = models.IntegerField()
    last_edit_sent = models.IntegerField()
    class Meta:
        db_table = u'editor_subscribe_editor'

class Gender(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = u'gender'

class Iso31661(models.Model):
    area = models.IntegerField()
    code = models.CharField(max_length=2, primary_key=True)
    class Meta:
        db_table = u'iso_3166_1'

class Iso31662(models.Model):
    area = models.IntegerField()
    code = models.CharField(max_length=10, primary_key=True)
    class Meta:
        db_table = u'iso_3166_2'

class Iso31663(models.Model):
    area = models.IntegerField()
    code = models.CharField(max_length=4, primary_key=True)
    class Meta:
        db_table = u'iso_3166_3'

class Isrc(models.Model):
    id = models.IntegerField(primary_key=True)
    recording = models.IntegerField()
    isrc = models.CharField(max_length=12)
    source = models.SmallIntegerField(null=True, blank=True)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'isrc'

class Iswc(models.Model):
    id = models.IntegerField(primary_key=True)
    work = models.IntegerField()
    iswc = models.CharField(max_length=15, blank=True)
    source = models.SmallIntegerField(null=True, blank=True)
    edits_pending = models.IntegerField()
    created = models.DateTimeField()
    class Meta:
        db_table = u'iswc'

class LAreaArea(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_area_area'

class LAreaArtist(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_area_artist'

class LAreaLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_area_label'

class LAreaWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_area_work'

class LAreaUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_area_url'

class LAreaRecording(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_area_recording'

class LAreaReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_area_release_group'

class LAreaRelease(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_area_release'

class LArtistArtist(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_artist_artist'

class LArtistLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_artist_label'

class LArtistRecording(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_artist_recording'

class LArtistRelease(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_artist_release'

class LArtistReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_artist_release_group'

class LArtistUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_artist_url'

class LArtistWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_artist_work'

class LLabelLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_label_label'

class LLabelRecording(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_label_recording'

class LLabelRelease(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_label_release'

class LLabelReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_label_release_group'

class LLabelUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_label_url'

class LLabelWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_label_work'

class LRecordingRecording(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_recording_recording'

class LRecordingRelease(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_recording_release'

class LRecordingReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_recording_release_group'

class LRecordingUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_recording_url'

class LRecordingWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_recording_work'

class LReleaseRelease(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_release_release'

class LReleaseReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_release_release_group'

class LReleaseUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_release_url'

class LReleaseWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_release_work'

class LReleaseGroupReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_release_group_release_group'

class LReleaseGroupUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_release_group_url'

class LReleaseGroupWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_release_group_work'

class LUrlUrl(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_url_url'

class LUrlWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_url_work'

class LWorkWork(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.IntegerField()
    entity0 = models.IntegerField()
    entity1 = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'l_work_work'

class Label(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True) # This field type is a guess.
    name = models.IntegerField(unique=True)
    sort_name = models.IntegerField()
    begin_date_year = models.SmallIntegerField(null=True, blank=True)
    begin_date_month = models.SmallIntegerField(null=True, blank=True)
    begin_date_day = models.SmallIntegerField(null=True, blank=True)
    end_date_year = models.SmallIntegerField(null=True, blank=True)
    end_date_month = models.SmallIntegerField(null=True, blank=True)
    end_date_day = models.SmallIntegerField(null=True, blank=True)
    label_code = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    ended = models.BooleanField()
    class Meta:
        db_table = u'label'

class LabelRatingRaw(models.Model):
    label = models.IntegerField()
    editor = models.IntegerField()
    rating = models.SmallIntegerField()
    class Meta:
        db_table = u'label_rating_raw'

class LabelTagRaw(models.Model):
    label = models.IntegerField()
    editor = models.IntegerField()
    tag = models.IntegerField()
    class Meta:
        db_table = u'label_tag_raw'

class LabelAliasType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    class Meta:
        db_table = u'label_alias_type'

class LabelAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.IntegerField()
    name = models.IntegerField()
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    sort_name = models.IntegerField()
    begin_date_year = models.SmallIntegerField(null=True, blank=True)
    begin_date_month = models.SmallIntegerField(null=True, blank=True)
    begin_date_day = models.SmallIntegerField(null=True, blank=True)
    end_date_year = models.SmallIntegerField(null=True, blank=True)
    end_date_month = models.SmallIntegerField(null=True, blank=True)
    end_date_day = models.SmallIntegerField(null=True, blank=True)
    primary_for_locale = models.BooleanField()
    class Meta:
        db_table = u'label_alias'

class LabelAnnotation(models.Model):
    label = models.IntegerField()
    annotation = models.IntegerField()
    class Meta:
        db_table = u'label_annotation'

class LabelIpi(models.Model):
    label = models.IntegerField()
    ipi = models.CharField(max_length=11)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'label_ipi'

class LabelIsni(models.Model):
    label = models.IntegerField()
    isni = models.CharField(max_length=16)
    edits_pending = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'label_isni'

class LabelMeta(models.Model):
    id = models.IntegerField(primary_key=True)
    rating = models.SmallIntegerField(null=True, blank=True)
    rating_count = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'label_meta'

class LabelGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) # This field type is a guess.
    new_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'label_gid_redirect'

class LabelName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=-1, unique=True)
    class Meta:
        db_table = u'label_name'

class LabelTag(models.Model):
    label = models.IntegerField()
    tag = models.IntegerField()
    count = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'label_tag'

class LabelType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = u'label_type'

class Language(models.Model):
    id = models.IntegerField(primary_key=True)
    iso_code_2t = models.CharField(max_length=3, unique=True, blank=True)
    iso_code_2b = models.CharField(max_length=3, unique=True, blank=True)
    iso_code_1 = models.CharField(max_length=2, unique=True, blank=True)
    name = models.CharField(max_length=100)
    frequency = models.IntegerField()
    iso_code_3 = models.CharField(max_length=3, unique=True, blank=True)
    class Meta:
        db_table = u'language'

class Link(models.Model):
    id = models.IntegerField(primary_key=True)
    link_type = models.IntegerField()
    begin_date_year = models.SmallIntegerField(null=True, blank=True)
    begin_date_month = models.SmallIntegerField(null=True, blank=True)
    begin_date_day = models.SmallIntegerField(null=True, blank=True)
    end_date_year = models.SmallIntegerField(null=True, blank=True)
    end_date_month = models.SmallIntegerField(null=True, blank=True)
    end_date_day = models.SmallIntegerField(null=True, blank=True)
    attribute_count = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    ended = models.BooleanField()
    class Meta:
        db_table = u'link'

class LinkAttribute(models.Model):
    link = models.IntegerField()
    attribute_type = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'link_attribute'

class LinkAttributeType(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.IntegerField(null=True, blank=True)
    root = models.IntegerField()
    child_order = models.IntegerField()
    gid = models.TextField(unique=True) # This field type is a guess.
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'link_attribute_type'

class LinkCreditableAttributeType(models.Model):
    attribute_type = models.IntegerField(primary_key=True)
    class Meta:
        db_table = u'link_creditable_attribute_type'

class LinkAttributeCredit(models.Model):
    link = models.IntegerField()
    attribute_type = models.IntegerField()
    credited_as = models.TextField()
    class Meta:
        db_table = u'link_attribute_credit'

class LinkType(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.IntegerField(null=True, blank=True)
    child_order = models.IntegerField()
    gid = models.TextField(unique=True) # This field type is a guess.
    entity_type0 = models.CharField(max_length=50)
    entity_type1 = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link_phrase = models.CharField(max_length=255)
    reverse_link_phrase = models.CharField(max_length=255)
    long_link_phrase = models.CharField(max_length=255)
    priority = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'link_type'

class LinkTypeAttributeType(models.Model):
    link_type = models.IntegerField()
    attribute_type = models.IntegerField()
    min = models.SmallIntegerField(null=True, blank=True)
    max = models.SmallIntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'link_type_attribute_type'

class EditorCollection(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True) # This field type is a guess.
    editor = models.IntegerField()
    name = models.CharField(max_length=-1)
    public = models.BooleanField()
    description = models.TextField()
    class Meta:
        db_table = u'editor_collection'

class EditorCollectionRelease(models.Model):
    collection = models.IntegerField()
    release = models.IntegerField()
    class Meta:
        db_table = u'editor_collection_release'

class EditorOauthToken(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.IntegerField()
    application = models.IntegerField()
    authorization_code = models.TextField(blank=True)
    refresh_token = models.TextField(unique=True, blank=True)
    access_token = models.TextField(unique=True, blank=True)
    mac_key = models.TextField(blank=True)
    mac_time_diff = models.IntegerField(null=True, blank=True)
    expire_time = models.DateTimeField()
    scope = models.IntegerField()
    granted = models.DateTimeField()
    class Meta:
        db_table = u'editor_oauth_token'

class EditorWatchPreferences(models.Model):
    editor = models.IntegerField(primary_key=True)
    notify_via_email = models.BooleanField()
    notification_timeframe = models.TextField() # This field type is a guess.
    last_checked = models.DateTimeField()
    class Meta:
        db_table = u'editor_watch_preferences'

class EditorWatchArtist(models.Model):
    artist = models.IntegerField()
    editor = models.IntegerField()
    class Meta:
        db_table = u'editor_watch_artist'

class EditorWatchReleaseGroupType(models.Model):
    editor = models.IntegerField()
    release_group_type = models.IntegerField()
    class Meta:
        db_table = u'editor_watch_release_group_type'

class EditorWatchReleaseStatus(models.Model):
    editor = models.IntegerField()
    release_status = models.IntegerField()
    class Meta:
        db_table = u'editor_watch_release_status'

class Medium(models.Model):
    id = models.IntegerField(primary_key=True)
    release = models.IntegerField()
    position = models.IntegerField()
    format = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    track_count = models.IntegerField()
    class Meta:
        db_table = u'medium'

class MediumCdtoc(models.Model):
    id = models.IntegerField(primary_key=True)
    medium = models.IntegerField()
    cdtoc = models.IntegerField()
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'medium_cdtoc'

class MediumFormat(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    parent = models.IntegerField(null=True, blank=True)
    child_order = models.IntegerField()
    year = models.SmallIntegerField(null=True, blank=True)
    has_discids = models.BooleanField()
    class Meta:
        db_table = u'medium_format'

class Puid(models.Model):
    id = models.IntegerField(primary_key=True)
    puid = models.CharField(max_length=36, unique=True)
    version = models.IntegerField()
    class Meta:
        db_table = u'puid'

class ReplicationControl(models.Model):
    id = models.IntegerField(primary_key=True)
    current_schema_sequence = models.IntegerField()
    current_replication_sequence = models.IntegerField(null=True, blank=True)
    last_replication_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'replication_control'

class Recording(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True) # This field type is a guess.
    name = models.IntegerField()
    artist_credit = models.IntegerField()
    length = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'recording'

class RecordingRatingRaw(models.Model):
    recording = models.IntegerField()
    editor = models.IntegerField()
    rating = models.SmallIntegerField()
    class Meta:
        db_table = u'recording_rating_raw'

class RecordingTagRaw(models.Model):
    recording = models.IntegerField()
    editor = models.IntegerField()
    tag = models.IntegerField()
    class Meta:
        db_table = u'recording_tag_raw'

class RecordingAnnotation(models.Model):
    recording = models.IntegerField()
    annotation = models.IntegerField()
    class Meta:
        db_table = u'recording_annotation'

class RecordingMeta(models.Model):
    id = models.IntegerField(primary_key=True)
    rating = models.SmallIntegerField(null=True, blank=True)
    rating_count = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'recording_meta'

class RecordingGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) # This field type is a guess.
    new_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'recording_gid_redirect'

class RecordingPuid(models.Model):
    id = models.IntegerField(primary_key=True)
    puid = models.IntegerField()
    recording = models.IntegerField()
    edits_pending = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'recording_puid'

class RecordingTag(models.Model):
    recording = models.IntegerField()
    tag = models.IntegerField()
    count = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'recording_tag'

class Release(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True) # This field type is a guess.
    name = models.IntegerField()
    artist_credit = models.IntegerField()
    release_group = models.IntegerField()
    status = models.IntegerField(null=True, blank=True)
    packaging = models.IntegerField(null=True, blank=True)
    language = models.IntegerField(null=True, blank=True)
    script = models.IntegerField(null=True, blank=True)
    barcode = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    quality = models.SmallIntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'release'

class ReleaseCountry(models.Model):
    release = models.IntegerField()
    country = models.IntegerField()
    date_year = models.SmallIntegerField(null=True, blank=True)
    date_month = models.SmallIntegerField(null=True, blank=True)
    date_day = models.SmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'release_country'

class ReleaseUnknownCountry(models.Model):
    release = models.IntegerField(primary_key=True)
    date_year = models.SmallIntegerField(null=True, blank=True)
    date_month = models.SmallIntegerField(null=True, blank=True)
    date_day = models.SmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'release_unknown_country'

class ReleaseRaw(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    added = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(null=True, blank=True)
    lookup_count = models.IntegerField(null=True, blank=True)
    modify_count = models.IntegerField(null=True, blank=True)
    source = models.IntegerField(null=True, blank=True)
    barcode = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255)
    class Meta:
        db_table = u'release_raw'

class ReleaseTagRaw(models.Model):
    release = models.IntegerField()
    editor = models.IntegerField()
    tag = models.IntegerField()
    class Meta:
        db_table = u'release_tag_raw'

class ReleaseAnnotation(models.Model):
    release = models.IntegerField()
    annotation = models.IntegerField()
    class Meta:
        db_table = u'release_annotation'

class ReleaseGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) # This field type is a guess.
    new_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'release_gid_redirect'

class ReleaseMeta(models.Model):
    id = models.IntegerField(primary_key=True)
    date_added = models.DateTimeField(null=True, blank=True)
    info_url = models.CharField(max_length=255, blank=True)
    amazon_asin = models.CharField(max_length=10, blank=True)
    amazon_store = models.CharField(max_length=20, blank=True)
    cover_art_presence = models.TextField() # This field type is a guess.
    class Meta:
        db_table = u'release_meta'

class ReleaseCoverart(models.Model):
    id = models.IntegerField(primary_key=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    cover_art_url = models.CharField(max_length=255, blank=True)
    class Meta:
        db_table = u'release_coverart'

class ReleaseLabel(models.Model):
    id = models.IntegerField(primary_key=True)
    release = models.IntegerField()
    label = models.IntegerField(null=True, blank=True)
    catalog_number = models.CharField(max_length=255, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'release_label'

class ReleasePackaging(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = u'release_packaging'

class ReleaseStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = u'release_status'

class ReleaseTag(models.Model):
    release = models.IntegerField()
    tag = models.IntegerField()
    count = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'release_tag'

class ReleaseGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True) # This field type is a guess.
    name = models.IntegerField()
    artist_credit = models.IntegerField()
    type = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'release_group'

class ReleaseGroupRatingRaw(models.Model):
    release_group = models.IntegerField()
    editor = models.IntegerField()
    rating = models.SmallIntegerField()
    class Meta:
        db_table = u'release_group_rating_raw'

class ReleaseGroupTagRaw(models.Model):
    release_group = models.IntegerField()
    editor = models.IntegerField()
    tag = models.IntegerField()
    class Meta:
        db_table = u'release_group_tag_raw'

class ReleaseGroupAnnotation(models.Model):
    release_group = models.IntegerField()
    annotation = models.IntegerField()
    class Meta:
        db_table = u'release_group_annotation'

class ReleaseGroupGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) # This field type is a guess.
    new_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'release_group_gid_redirect'

class ReleaseGroupMeta(models.Model):
    id = models.IntegerField(primary_key=True)
    release_count = models.IntegerField()
    first_release_date_year = models.SmallIntegerField(null=True, blank=True)
    first_release_date_month = models.SmallIntegerField(null=True, blank=True)
    first_release_date_day = models.SmallIntegerField(null=True, blank=True)
    rating = models.SmallIntegerField(null=True, blank=True)
    rating_count = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'release_group_meta'

class ReleaseGroupTag(models.Model):
    release_group = models.IntegerField()
    tag = models.IntegerField()
    count = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'release_group_tag'

class ReleaseGroupPrimaryType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = u'release_group_primary_type'

class ReleaseGroupSecondaryType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    class Meta:
        db_table = u'release_group_secondary_type'

class ReleaseGroupSecondaryTypeJoin(models.Model):
    release_group = models.IntegerField()
    secondary_type = models.IntegerField()
    created = models.DateTimeField()
    class Meta:
        db_table = u'release_group_secondary_type_join'

class ReleaseName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=-1, unique=True)
    class Meta:
        db_table = u'release_name'

class Script(models.Model):
    id = models.IntegerField(primary_key=True)
    iso_code = models.CharField(max_length=4, unique=True)
    iso_number = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    frequency = models.IntegerField()
    class Meta:
        db_table = u'script'

class ScriptLanguage(models.Model):
    id = models.IntegerField(primary_key=True)
    script = models.IntegerField()
    language = models.IntegerField()
    frequency = models.IntegerField()
    class Meta:
        db_table = u'script_language'

class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    ref_count = models.IntegerField()
    class Meta:
        db_table = u'tag'

class TagRelation(models.Model):
    tag1 = models.IntegerField()
    tag2 = models.IntegerField()
    weight = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'tag_relation'

class Track(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField() # This field type is a guess.
    recording = models.IntegerField()
    medium = models.IntegerField()
    position = models.IntegerField()
    number = models.TextField()
    name = models.IntegerField()
    artist_credit = models.IntegerField()
    length = models.IntegerField(null=True, blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'track'

class TrackGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) # This field type is a guess.
    new_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'track_gid_redirect'

class TrackRaw(models.Model):
    id = models.IntegerField(primary_key=True)
    release = models.IntegerField()
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255, blank=True)
    sequence = models.IntegerField()
    class Meta:
        db_table = u'track_raw'

class TrackName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=-1, unique=True)
    class Meta:
        db_table = u'track_name'

class MediumIndex(models.Model):
    medium = models.IntegerField(primary_key=True)
    toc = models.TextField(blank=True)
    class Meta:
        db_table = u'medium_index'

class Url(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True) # This field type is a guess.
    url = models.TextField(unique=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'url'

class UrlGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) # This field type is a guess.
    new_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'url_gid_redirect'

class Vote(models.Model):
    id = models.IntegerField(primary_key=True)
    editor = models.IntegerField()
    edit = models.IntegerField()
    vote = models.SmallIntegerField()
    vote_time = models.DateTimeField(null=True, blank=True)
    superseded = models.BooleanField()
    class Meta:
        db_table = u'vote'

class Work(models.Model):
    id = models.IntegerField(primary_key=True)
    gid = models.TextField(unique=True) # This field type is a guess.
    name = models.IntegerField()
    type = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=255)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    language = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'work'

class WorkRatingRaw(models.Model):
    work = models.IntegerField()
    editor = models.IntegerField()
    rating = models.SmallIntegerField()
    class Meta:
        db_table = u'work_rating_raw'

class WorkTagRaw(models.Model):
    work = models.IntegerField()
    editor = models.IntegerField()
    tag = models.IntegerField()
    class Meta:
        db_table = u'work_tag_raw'

class WorkAliasType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    class Meta:
        db_table = u'work_alias_type'

class WorkAlias(models.Model):
    id = models.IntegerField(primary_key=True)
    work = models.IntegerField()
    name = models.IntegerField()
    locale = models.TextField(blank=True)
    edits_pending = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    sort_name = models.IntegerField()
    begin_date_year = models.SmallIntegerField(null=True, blank=True)
    begin_date_month = models.SmallIntegerField(null=True, blank=True)
    begin_date_day = models.SmallIntegerField(null=True, blank=True)
    end_date_year = models.SmallIntegerField(null=True, blank=True)
    end_date_month = models.SmallIntegerField(null=True, blank=True)
    end_date_day = models.SmallIntegerField(null=True, blank=True)
    primary_for_locale = models.BooleanField()
    class Meta:
        db_table = u'work_alias'

class WorkAnnotation(models.Model):
    work = models.IntegerField()
    annotation = models.IntegerField()
    class Meta:
        db_table = u'work_annotation'

class WorkGidRedirect(models.Model):
    gid = models.TextField(primary_key=True) # This field type is a guess.
    new_id = models.IntegerField()
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'work_gid_redirect'

class WorkMeta(models.Model):
    id = models.IntegerField(primary_key=True)
    rating = models.SmallIntegerField(null=True, blank=True)
    rating_count = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'work_meta'

class WorkName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=-1, unique=True)
    class Meta:
        db_table = u'work_name'

class WorkTag(models.Model):
    work = models.IntegerField()
    tag = models.IntegerField()
    count = models.IntegerField()
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u'work_tag'

class WorkType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = u'work_type'

class WorkAttributeType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=255)
    free_text = models.BooleanField()
    class Meta:
        db_table = u'work_attribute_type'

class WorkAttributeTypeAllowedValue(models.Model):
    id = models.IntegerField(primary_key=True)
    work_attribute_type = models.IntegerField()
    value = models.TextField(blank=True)
    class Meta:
        db_table = u'work_attribute_type_allowed_value'

class WorkAttribute(models.Model):
    id = models.IntegerField(primary_key=True)
    work = models.IntegerField()
    work_attribute_type = models.IntegerField()
    work_attribute_type_allowed_value = models.IntegerField(null=True, blank=True)
    work_attribute_text = models.TextField(blank=True)
    class Meta:
        db_table = u'work_attribute'

class SArtist(models.Model):
    id = models.IntegerField(null=True, blank=True)
    gid = models.TextField(blank=True) # This field type is a guess.
    name = models.CharField(max_length=-1, blank=True)
    sort_name = models.CharField(max_length=-1, blank=True)
    begin_date_year = models.SmallIntegerField(null=True, blank=True)
    begin_date_month = models.SmallIntegerField(null=True, blank=True)
    begin_date_day = models.SmallIntegerField(null=True, blank=True)
    end_date_year = models.SmallIntegerField(null=True, blank=True)
    end_date_month = models.SmallIntegerField(null=True, blank=True)
    end_date_day = models.SmallIntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    edits_pending = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    ended = models.BooleanField(null=True, blank=True)
    begin_area = models.IntegerField(null=True, blank=True)
    end_area = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u's_artist'

class SArtistCredit(models.Model):
    id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=-1, blank=True)
    artist_count = models.SmallIntegerField(null=True, blank=True)
    ref_count = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u's_artist_credit'

class SArtistCreditName(models.Model):
    artist_credit = models.IntegerField(null=True, blank=True)
    position = models.SmallIntegerField(null=True, blank=True)
    artist = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=-1, blank=True)
    join_phrase = models.TextField(blank=True)
    class Meta:
        db_table = u's_artist_credit_name'

class SLabel(models.Model):
    id = models.IntegerField(null=True, blank=True)
    gid = models.TextField(blank=True) # This field type is a guess.
    name = models.CharField(max_length=-1, blank=True)
    sort_name = models.CharField(max_length=-1, blank=True)
    begin_date_year = models.SmallIntegerField(null=True, blank=True)
    begin_date_month = models.SmallIntegerField(null=True, blank=True)
    begin_date_day = models.SmallIntegerField(null=True, blank=True)
    end_date_year = models.SmallIntegerField(null=True, blank=True)
    end_date_month = models.SmallIntegerField(null=True, blank=True)
    end_date_day = models.SmallIntegerField(null=True, blank=True)
    label_code = models.IntegerField(null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    edits_pending = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    ended = models.BooleanField(null=True, blank=True)
    class Meta:
        db_table = u's_label'

class SRecording(models.Model):
    id = models.IntegerField(null=True, blank=True)
    gid = models.TextField(blank=True) # This field type is a guess.
    name = models.CharField(max_length=-1, blank=True)
    artist_credit = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    edits_pending = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u's_recording'

class SRelease(models.Model):
    id = models.IntegerField(null=True, blank=True)
    gid = models.TextField(blank=True) # This field type is a guess.
    name = models.CharField(max_length=-1, blank=True)
    artist_credit = models.IntegerField(null=True, blank=True)
    release_group = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True)
    packaging = models.IntegerField(null=True, blank=True)
    language = models.IntegerField(null=True, blank=True)
    script = models.IntegerField(null=True, blank=True)
    barcode = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    edits_pending = models.IntegerField(null=True, blank=True)
    quality = models.SmallIntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u's_release'

class SReleaseCountry(models.Model):
    release = models.IntegerField(null=True, blank=True)
    country = models.IntegerField(null=True, blank=True)
    date_year = models.SmallIntegerField(null=True, blank=True)
    date_month = models.SmallIntegerField(null=True, blank=True)
    date_day = models.SmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = u's_release_country'

class SFirstReleaseCountry(models.Model):
    release = models.IntegerField(null=True, blank=True)
    country = models.IntegerField(null=True, blank=True)
    date_year = models.SmallIntegerField(null=True, blank=True)
    date_month = models.SmallIntegerField(null=True, blank=True)
    date_day = models.SmallIntegerField(null=True, blank=True)
    class Meta:
        db_table = u's_first_release_country'

class SReleaseGroup(models.Model):
    id = models.IntegerField(null=True, blank=True)
    gid = models.TextField(blank=True) # This field type is a guess.
    name = models.CharField(max_length=-1, blank=True)
    artist_credit = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    edits_pending = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u's_release_group'

class STrack(models.Model):
    id = models.IntegerField(null=True, blank=True)
    gid = models.TextField(blank=True) # This field type is a guess.
    recording = models.IntegerField(null=True, blank=True)
    medium = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=-1, blank=True)
    artist_credit = models.IntegerField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    edits_pending = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    number = models.TextField(blank=True)
    class Meta:
        db_table = u's_track'

class SWork(models.Model):
    id = models.IntegerField(null=True, blank=True)
    gid = models.TextField(blank=True) # This field type is a guess.
    name = models.CharField(max_length=-1, blank=True)
    type = models.IntegerField(null=True, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    edits_pending = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = u's_work'

"""