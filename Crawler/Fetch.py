import urlparse as urlp
import Document

Doc = Document.DocumentSoup

class Datafetcher:

	def get_img_src(self,soup_doc):
		img_href = []
		for x in soup_doc.findAll("img"):
			#size = image(size).size
			link = x["src"]
			if link[0:6] != "//bits" and x.has_key("width") and x.has_key("height"):
				link=urlp.urljoin(Doc.CurrentLink,link)
				#link = fix_url(Document.CurrentLink,link)
				img_href.append((link,x["width"],x["height"]))
		return img_href

	def get_a_href(self,soup_doc):
		a_href=[]
		for x in soup_doc.findAll('a'):
			if x.has_key("href") and x.has_key("title"):
				link=x["href"]
				title=x["title"]
				if link[0:3] != "/w":
					link=urlp.urljoin(Doc.CurrentLink,link)
					a_href.append((link,title))
		return a_href

	def get_content(self,soup_doc):
		content_list=[]
		for x in soup_doc.findAll("p"):
			content_list.append(x.getText())
		return content_list