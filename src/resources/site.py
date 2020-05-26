from flask_restful import Resource, reqparse
from models.site import SiteModel
import traceback

args = reqparse.RequestParser()
args.add_argument("url", type=str, required=True, help="The field 'url' cannot be left blank.")

class Sites(Resource):
	@staticmethod
	def get():
		return {"sites": [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
	@staticmethod
	def get(url):
		site = SiteModel.find_site(url)
		if site:
			return site.json()
		return {"message": f"site '{url}' not found!"}, 404 #not found

	@staticmethod
	def post(url):
		if SiteModel.find_site(url):
			return {"message": f"the site '{url}' already exists!"}, 400 #bad request
		site = SiteModel(url)
		try:
			site.save_site()
		except:
			traceback.print_exc()
			return {"message": "An error ocurred trying to create site."}, 500 #Internal Server Error
		return site.json(), 201
	
	@staticmethod
	def delete(url):
		site = SiteModel.find_site(url)
		if site:
			site.delete_site()
			return {"message": "the site has been deleted!"}
		return {"message": "site not found!"}, 404
		