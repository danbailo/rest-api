from sql_alchemy import db

class SiteModel(db.Model):
	__tablename__ = "sites"

	site_id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(64))
	hotels = db.relationship("HotelModel") #return a list of Hotels obj

	def __init__(self, url):
		self.url = url

	def json(self):
		return {
			"site_id": self.site_id,
			"url": self.url,
			"hotels": [hotel.json() for hotel in self.hotels] 
		} #self.hotels in this context means only the hotels that are a HotelModel object

	@classmethod
	def find_site(cls, url):
		site = cls.query.filter_by(url=url).first()
		if site:
			return site
		return None

	def save_site(self):
		db.session.add(self)
		db.session.commit()

	def delete_site(self):
		db.session.delete(self)
		db.session.commit()