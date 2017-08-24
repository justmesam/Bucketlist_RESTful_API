from flask import make_response, request, jsonify, url_for
from flask.views import MethodView
from app.common import auth_required
from app.models import User, Bucketlist
from app.bucketlist import bucketlist_blueprint


class BucketlistApi(MethodView):
    """
    The class bucketlist with all the methods
    """
    @auth_required
    def get(self, auth_data, _id=None):
        """
        method gets all bucketlist for a user
        """
        limit = request.args.get('limit')
        page = request.args.get('page')
        if not limit:
            if not _id:
                bucketlists = Bucketlist.query_all(auth_data)
                if not bucketlists:
                    response = {
                        'message' : 'No bucketlists for this user yet'
                    }
                    return make_response(jsonify(response)), 404
                else:
                    all_bucketlists = [bucketlist.serialize() for bucketlist in bucketlists]
                    return make_response(jsonify(all_bucketlists)), 200
            else:
                bucketlist = Bucketlist.query.filter_by(id=_id).first()
                if not bucketlist:
                    response = {
                        'message' : 'Bucketlist not available'
                    }
                    return make_response(jsonify(response)), 404
                else:
                    response = bucketlist.serialize()
                    return make_response(jsonify(response)), 200
        else:
            try:
                limit = int(limit)
                page = int(page)
            except ValueError:
                limit = 5
                page = 1
            limited_bucketlists = Bucketlist.query.filter_by\
             (owner=auth_data).paginate(page, limit, False)
            all_bucketlists = [bucketlist.serialize() for bucketlist in limited_bucketlists.items]
            if all_bucketlists:
                next_page = ''
                previous_page = ''
                def url_for_other_page(page):
                    """
                    generates url for the next and prev page of pagination
                    """
                    args = request.view_args.copy()
                    args['page'] = page
                    return url_for(request.endpoint, **args)
                if limited_bucketlists.has_next:
                    next_page = 'http://127.0.0.1:5000/' +\
                     url_for_other_page(page + 1)  + '&limit' + str(limit)
                if limited_bucketlists.has_prev:
                    previous_page = 'http://127.0.0.1:5000/' +\
                     url_for_other_page(page - 1)  + '&limit' + str(limit)
            else:
                response = {
                    'message' : 'No bucketlits available'
                }
                return make_response(jsonify(response)), 404
            return make_response(jsonify(bucketlists=all_bucketlists,
                                         next_page=next_page,
                                         previous_page=previous_page)), 200

    @auth_required
    def post(self, auth_data):
        """
        method used to create a bucketlist
        """
        title = request.get_json().get('title')
        intro = request.get_json().get('intro')
        bucketlist_ = Bucketlist.query.filter_by(title=title).first()
        if intro and title:
            bucketlist = Bucketlist(title=title,
                                    intro=intro,
                                    owner=auth_data)
            bucketlist.save_bucketlist()
            response = bucketlist.serialize()
            return make_response(jsonify(response)), 201

    @auth_required
    def put(self, _id, auth_data):
        """
        method used to update and delete a specific bucketlist using its id
        """
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
            response = bucketlist.serialize()
            return make_response(jsonify(response)), 200

    @auth_required
    def delete(self, _id, auth_data):
        """
        method used to delete a database using its id
        """
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


bucket_view = BucketlistApi.as_view('bucketlist_api')
bucketlist_blueprint.add_url_rule('/',
                                  view_func=bucket_view,
                                  defaults={'_id' : None},
                                  methods=['GET'])
bucketlist_blueprint.add_url_rule('/',
                                  view_func=bucket_view,
                                  methods=['POST'])
bucketlist_blueprint.add_url_rule('/<int:_id>/',
                                  view_func=bucket_view,
                                  methods=['GET', 'PUT', 'DELETE'])
