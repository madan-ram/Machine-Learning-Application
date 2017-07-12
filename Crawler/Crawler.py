import Fetch
import Document
from collections import deque
import mysqlConnect as myCon

con=myCon.mysqlConnection()

Doc=Document.DocumentSoup()
DF = Fetch.Datafetcher()

class Crawl:
	links=[]
	def BFSCrawl(self,link_info):
		prev_title=""
		id1=0
		db=con.getConnection("Tnooz")
		self.links.append(link_info)
		while(len(self.links)!=0):
			(link,title) = self.links[0]
			self.links=self.links[1:len(self.links)]
			soup_html = Doc.getDocumentSoup(link)
			im_list = DF.get_img_src(soup_html)
			href_list = DF.get_a_href(soup_html)
			#content_list = DF.get_content(soup_html)
			self.links=self.links+href_list
			content=""
			if prev_title!=title:
				cursor = db.cursor()
				id1=id1+1
				sql1="INSERT INTO ImageTitle(ID,Title,Parent_URL) VALUES(%s,\'%s\',\'%s\');" % (id1,title,link);
				#templet=[title,link,content];
				print sql1
				cursor.execute(sql1)
				db.commit()
			for x in im_list:
				(l,w,h)=x
				sql2="INSERT INTO ImageDescription(ID,sizeX,sizeY,url) VALUES(\'%s\',%s,%s,\'%s\')" % (id1,w,h,l);
				cursor.execute(sql2)
				db.commit()
			#if prev_title!=title:
			#	file=open(title,"a")
			#	prev_title=title
			#file.write("title:"+title.encode('utf-8'))
			#file.write("		image list:\n")
			#for x in im_list:
			#	file.write("			:\n"+x.encode('utf-8'))
			#file.write("		content list:\n")
			#for x in content_list:
			#	file.write("			:\n"+x.encode('utf-8'))
			##print content_list
#
#db=con.getConnection("Tnooz")
#cursor = db.cursor()
#cursor.execute("insert into ")
#res=cursor.fetchall()
#for row in res:
#	print row[1]