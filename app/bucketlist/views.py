from flask import make_response, request, jsonify
from flask.views import MethodView
from app.models import User, Bucketlist
from app.bucketlist import bucketlist_blueprint


class BucketlistApi(MethodView):
    """
    The class bucketlist with all the methods
    """
    def get(self, _id=None):
        """
        method gets all bucketlist for a user
        """
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split("Bearer ")[1]
        if auth_token:
            auth_data = User.token_decoding(auth_token)
            if not isinstance(auth_data, str):
                if not _id:
                    bucketlists = Bucketlist.query_all(auth_data)
                    if not bucketlists:
                        response = {
                            'message' : 'No bucketlists for this user yet'
                        }
                        return make_response(jsonify(response)), 404
                    else:
                        all_bucketlists = []
                        for bucketlist in bucketlists:
                            obj = {
                                'id' : bucketlist.id,
                                'owner' : bucketlist.owner,
                                'date_created' : bucketlist.date_created,
                                'date_updated' : bucketlist.date_updated,
                                'title' : bucketlist.title,
                                'intro' : bucketlist.intro
                            }
                            all_bucketlists.append(obj)
                            return make_response(jsonify(all_bucketlists)), 200
                else:
                    bucketlist = Bucketlist.query.filter_by(id=_id).first()
                    if not bucketlist:
                        response = {
                            'message' : 'Bucketlist not available'
                        }
                        return make_response(jsonify(response)), 404
                    else:
                        response = {
                            'id' : bucketlist.id,
                            'owner' : bucketlist.owner,
                            'date_created' : bucketlist.date_created,
                            'date_updated' : bucketlist.date_updated,
                            'title' : bucketlist.title,
                            'intro' : bucketlist.intro
                        }
                        return make_response(jsonify(response)), 200
            else:
                response = {
                    'message' : auth_data
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message' : 'No valid token'
            }
            return make_response(jsonify(response)), 401


    def post(self):
        """
        method used to create a database
        """
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split("Bearer ")[1]
        if auth_token:
            auth_data = User.token_decoding(auth_token)
            if not isinstance(auth_data, str):
                title = request.get_json().get('title')
                intro = request.get_json().get('intro')
                if intro and title:
                    bucketlist = Bucketlist(title=title,
                                            intro=intro,
                                            owner=auth_data)
                    bucketlist.save_bucketlist()
                    response = {
                        'id' : bucketlist.id,
                        'owner' : bucketlist.owner,
                        'date_created' : bucketlist.date_created,
                        'date_updated' : bucketlist.date_updated,
                        'title' : bucketlist.title,
                        'intro' : bucketlist.intro
                    }
                    return make_response(jsonify(response)), 201
            else:
                response = {
                    'message' : auth_data
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message' : 'No valid token'
            }
            return make_response(jsonify(response)), 401

    def put(self, _id):
        """
        method used to update and delete a specific DATABASE using its id
        """
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split("Bearer ")[1]
        if auth_token:
            auth_data = User.token_decoding(auth_token)
            if not isinstance(auth_data, str):
                bucketlist = Bucketlist.query.filter_by(id=_id).first()
                if not bucketlist:
                    response = {
                        'message' : 'Bucketlist not available'
                    }
                    return make_response(jsonify(response)), 404
                else:
                    title = request.get_json().get('title')
                    intro = request.get_json().get('intro')
                    bucketlist.title = title
                    bucketlist.intro = intro
                    bucketlist.save_bucketlist()
                    response = {
                        'id' : bucketlist.id,
                        'owner' : bucketlist.owner,
                        'date_created' : bucketlist.date_created,
                        'date_updated' : bucketlist.date_updated,
                        'title' : bucketlist.title,
                        'intro' : bucketlist.intro
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message' : auth_data
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message' : 'No valid token'
            }
            return make_response(jsonify(response)), 401

    def delete(self, _id):
        """
        method used to delete a database using its id
        """
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split("Bearer ")[1]
        if auth_token:
            auth_data = User.token_decoding(auth_token)
            if not isinstance(auth_data, str):
                bucketlist = Bucketlist.query.filter_by(id=_id).first()
                if not bucketlist:
                    response = {
                        'message' : 'Bucketlist not available'
                    }
                    return make_response(jsonify(response)), 404
                else:
                    bucketlist.delete()
                    response = {
                        'message' : 'Bucketlist deleted'
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message' : auth_data
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message' : 'No valid token'
            }
            return make_response(jsonify(response)), 401


bucket_view = BucketlistApi.as_view('bucketlist_api')
bucketlist_blueprint.add_url_rule('/',
                                  view_func=bucket_view,
                                  defaults={'_id' : None},
                                  methods=['GET'])
bucketlist_blueprint.add_url_rule('/',
                                  view_func=bucket_view,
                                  methods=['POST'])
bucketlist_blueprint.add_url_rule('/<int:_id>',
                                  view_func=bucket_view,
                                  methods=['GET', 'PUT', 'DELETE'])
