from marshmallow import Schema, fields, validate, post_load
import models
import utils


class ArtistsSchema(Schema):
    artist_name = fields.String(required=True, validate=validate.Length(min=1))
    artist_info = fields.String(required=True, validate=validate.Length(min=2))


class SongsSchema(Schema):
    song_name = fields.String(required=True, validate=validate.Length(min=1))
    song_text = fields.String(required=True, validate=validate.Length(min=10))
    song_year = fields.Integer(
        required=True, validate=validate.Range(min=1800, max=2025))
    original_lang = fields.String(
        required=True, validate=validate.OneOf(utils.LANG_CODES))


class AlbumsSchema(Schema):
    album_name = fields.String(required=True, validate=validate.Length(min=1))
    album_info = fields.String(required=True, validate=validate.Length(min=10))
    album_year = fields.Integer(
        required=True, validate=validate.Range(min=1800, max=2025))
    