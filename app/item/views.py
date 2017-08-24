from flask import make_response, request, jsonify, url_for
from flask.views import MethodView
from app.models import User, Item
from app.item import item_blueprint
from app.common import auth_required


class itemApi(MethodView):
    """
    The class item with all the methods
    """
    @auth_required
    def get(self, bucketlist_id, auth_data, _id=None):
        """
        method gets all item for a user
        """
        limit = request.args.get('limit')
        page = request.args.get('page')
        if not limit:
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
                        all_items.append(item.serialize())
                    return make_response(jsonify(all_items)), 200
            else:
                item = Item.query.filter_by(id=_id).first()
                if not item:
                    response = {
                        'message' : 'item not available'
                    }
                    return make_response(jsonify(response)), 404
                else:
                    response = item.serialize()
                    return make_response(jsonify(response)), 200
        else:
            try:
                limit = int(limit)
                page = int(page)
            except ValueError:
                limit = 5
                page = 1
            limited_items = Item.query.filter_by\
             (owner=bucketlist_id).paginate(page, limit, False)
            all_items = [item.serialize() for item in limited_items.items]
            if all_items:
                next_page = ''
                previous_page = ''
                def url_for_other_page(page):
                    """
                    generates url for the next and prev page of pagination
                    """
                    args = request.view_args.copy()
                    args['page'] = page
                    return url_for(request.endpoint, **args)
                if limited_items.has_next:
                    next_page = 'http://127.0.0.1:5000/' +\
                     url_for_other_page(page + 1)  + '&limit' + str(limit)
                if limited_items.has_prev:
                    previous_page = 'http://127.0.0.1:5000/' +\
                     url_for_other_page(page - 1)  + '&limit' + str(limit)
            else:
                response = {
                    'message' : 'No items available'
                }
                return make_response(jsonify(response)), 404
            return make_response(jsonify(bucketlists=all_items,
                                         next_page=next_page,
                                         previous_page=previous_page)), 200


    @auth_required
    def post(self, auth_data, bucketlist_id):
        """
        method used to create a database
        """
        title = request.get_json().get('title')
        intro = request.get_json().get('intro')
        if intro and title:
            item = Item(title=title,
                        intro=intro,
                        owner=bucketlist_id)
            item.save_item()
            response = item.serialize()
            return make_response(jsonify(response)), 201

    @auth_required
    def put(self,bucketlist_id, auth_data, _id):
        """
        method used to update and delete a specific DATABASE using its id
        """
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
            response = item.serialize()
            return make_response(jsonify(response)), 200

    @auth_required
    def delete(self, bucketlist_id, auth_data, _id):
        """
        method used to delete a database using its id
        """
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


item_view = itemApi.as_view('item_api')
item_blueprint.add_url_rule('/<int:bucketlist_id>/items/',
                            view_func=item_view,
                            defaults={'_id' : None},
                            methods=['GET'])
item_blueprint.add_url_rule('/<int:bucketlist_id>/items/',
                            view_func=item_view,
                            methods=['POST'])
item_blueprint.add_url_rule('/<int:bucketlist_id>/items/<int:_id>/',
                            view_func=item_view,
                            methods=['GET', 'PUT', 'DELETE'])
