from flask import make_response, request, jsonify
from flask.views import MethodView
from app.models import User, Item
from app.item import item_blueprint


class itemApi(MethodView):
    """
    The class item with all the methods
    """
    def get(self, bucketlist_id, _id=None):
        """
        method gets all item for a user
        """
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split("Bearer ")[1]
        if auth_token:
            auth_data = User.token_decoding(auth_token)
            if not isinstance(auth_data, str):
                if not _id:
                    items = Item.query_items(bucketlist_id)
                    if not items:
                        response = {
                            'message' : 'No items for this user yet'
                        }
                        return make_response(jsonify(response)), 404
                    else:
                        all_items = []
                        for item in items:
                            obj = {
                                'id' : item.id,
                                'owner' : item.owner,
                                'date_created' : item.date_created,
                                'date_updated' : item.date_updated,
                                'title' : item.title,
                                'intro' : item.intro
                            }
                            all_items.append(obj)
                            return make_response(jsonify(all_items)), 200
                else:
                    item = Item.query.filter_by(id=_id).first()
                    if not item:
                        response = {
                            'message' : 'item not available'
                        }
                        return make_response(jsonify(response)), 404
                    else:
                        response = {
                            'id' : item.id,
                            'owner' : item.owner,
                            'date_created' : item.date_created,
                            'date_updated' : item.date_updated,
                            'title' : item.title,
                            'intro' : item.intro
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


    def post(self, bucketlist_id):
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
                    item = Item(title=title,
                                intro=intro,
                                owner=bucketlist_id)
                    item.save_item()
                    response = {
                        'id' : item.id,
                        'owner' : item.owner,
                        'date_created' : item.date_created,
                        'date_updated' : item.date_updated,
                        'title' : item.title,
                        'intro' : item.intro
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

    def put(self,bucketlist_id, _id):
        """
        method used to update and delete a specific DATABASE using its id
        """
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split("Bearer ")[1]
        if auth_token:
            auth_data = User.token_decoding(auth_token)
            if not isinstance(auth_data, str):
                item = Item.query.filter_by(owner=bucketlist_id, id=_id).first()
                if not item:
                    response = {
                        'message' : 'item not available'
                    }
                    return make_response(jsonify(response)), 404
                else:
                    title = request.get_json().get('title')
                    intro = request.get_json().get('intro')

                    item.title = title
                    item.intro = intro
                    item.save_item()
                    response = {
                        'id' : item.id,
                        'owner' : item.owner,
                        'date_created' : item.date_created,
                        'date_updated' : item.date_updated,
                        'title' : item.title,
                        'intro' : item.intro
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

    def delete(self, bucketlist_id, _id):
        """
        method used to delete a database using its id
        """
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split("Bearer ")[1]
        if auth_token:
            auth_data = User.token_decoding(auth_token)
            if not isinstance(auth_data, str):
                item = Item.query.filter_by(owner=bucketlist_id, id=_id).first()
                if not item:
                    response = {
                        'message' : 'item not available'
                    }
                    return make_response(jsonify(response)), 404
                else:
                    item.delete()
                    response = {
                        'message' : 'item deleted'
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


item_view = itemApi.as_view('item_api')
item_blueprint.add_url_rule('/<int:bucketlist_id>/items/',
                            view_func=item_view,
                            defaults={'_id' : None},
                            methods=['GET'])
item_blueprint.add_url_rule('/<int:bucketlist_id>/items/',
                            view_func=item_view,
                            methods=['POST'])
item_blueprint.add_url_rule('/<int:bucketlist_id>/items/<int:_id>',
                            view_func=item_view,
                            methods=['GET', 'PUT', 'DELETE'])
