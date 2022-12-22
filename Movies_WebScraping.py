from bs4 import BeautifulSoup as bs
import requests, openpyxl
import shutil

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = 'IMDB_Movies'
sheet.append(['id', 'title', 'year', 'duration', 'genre', 'imdb_rating', 'img_loc'])

genres = ['action', 'adventure', 'animation', 'biography', 'comedy', 'crime', 'drama', 'family', 'fantasy', 'film_noir', 'history', 'horror', 'music', 'musical', 'mystery', 'romance', 'sci_fi', 'sport', 'thriller', 'war', 'western']
mid = 1
name_list = []
for i in range(len(genres)):
    try:
        source = requests.get('https://www.imdb.com/search/title/?genres='+genres[i]+'&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=SD7Q6R80HM885EAFQZC0&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_'+str(i+1))
        source.raise_for_status()
    
        soup = bs(source.text, 'html.parser')

        movies = soup.find('div', class_='lister-list').find_all('div', class_='lister-item mode-advanced')
        count=1
        for movie in movies:

            imgurl = (str(movie.find('div', class_='lister-item-image float-left').a.img).split())[-3]
            imgsrc = imgurl[10:-1]
            imgsrc = imgsrc.split('._V')[0]+'.jpg'

            div =  movie.find('div', class_='lister-item-content')
            name = div.h3.a.text
            year = div.find('span', class_='lister-item-year text-muted unbold').text.strip('()')
            if len(year)>4:
              continue
            subdiv = div.find('p', class_='text-muted')
            duration = subdiv.find('span', class_='runtime').text.strip()
            genre = subdiv.find('span', class_='genre').text.strip()
            genre = genre.split(',')[0]
            rating = div.find('div', class_='ratings-bar').find('strong').text.strip()

            if name not in name_list:
                name_list.append(name)
                imgrequest = requests.get(imgsrc, stream=True)
                if imgrequest.status_code == 200:
                    imgfile = "movie_image/"+str(mid)+".jpg"
                    with open('media/'+imgfile, 'wb') as f:
                        imgrequest.raw.decode_content = True
                        shutil.copyfileobj(imgrequest.raw, f)
                    sheet.append([mid, name, year, duration, genre, rating, imgfile])
            mid+=1      
            if count>=10:
              break 

    except Exception as e:
        print(e)
print(len(name_list))
excel.save('imdb_movies.xlsx') 