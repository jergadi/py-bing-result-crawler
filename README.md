# py-bing-result-crawler
This is a Python (3) Spyder crawler project, that searches Bing.com and save the results to a csv file.
Why Bing? Bing is a search engine that has lesser security compared to Google and other popular search engines. 
The script sends a url search to bing, and then go through the results one by one, and get the header and metadata. 
Note that this does not go inside the websites themselves, only the bing results information.

## Getting Started
What you need to get started:
1. Python 3.7 or above. To download and install, follow this https://www.python.org/downloads/ 
2. Scrapy library. To download and install, follow this https://scrapy.org/.

## Running the Scraper
### Configure your input. 
The code below builds the URL for the bing search: 
```python
    with open('input\\cand_list_title.csv', 'r') as csvfile:
        next(csvfile)
        filereader = csv.reader(csvfile)
        for row in filereader:
			#this is the Bing search URL builder
            data = ("http://www.bing.com/search?q=%s" % (urllib.parse.quote_plus(row[0] + ' ' + row[1])),
                              row[0],
                              row[1])
            start_urls.append(data)
```
You can find the input file from the `input` folder, add as many columns as you want but note that you might need to adjust the URL builder if you want to add more keywords in your search. 

### Results returned. 
The scraper only gets linkedIn results. 
```python
				#this is to get only the LinkedIn results
                if 'linkedin.com/in' in response.xpath("//li[@class='b_algo'][%s]/div[@class='b_caption']/div[@class='b_attribution']/cite/text()" % i).get():
                    yield l.load_item()
                else:
                   pass
```
To get all result items, change it to: 
`yield l.load_item()`

### Going to result page #. 
Currently, this is configured to go only to the second page. You can build iter to make it visit x number of pages.
```python
        #this is configured to only go to the second page.            
        next_page = response.xpath("//li[@class='b_pag']/nav/ul/li/a[@aria-label='Page 2']/@href").get()
        if next_page is not None:
            next_page = "http://www.bing.com" + next_page
            yield response.follow(next_page, callback = self.parse)
```

### Run the Scraper
In your command prompt: 
`scrapy crawl bingcrawler`

### Results file
The code below saves the file to the home directory of this crawler. You can change it's configurations via the below code: 
```python 
    custom_settings = {
            'FEED_URI': 'bing_cralwer.csv',
            'FEED_FORMAT': 'csv',
            'FEED_EXPORT_ENCODING': 'utf-8-sig',
            'FEED_EXPORT_FIELDS': [
                'headline',
                'summary',
                'metadata',
                'li_url',
                'search',
                'link',
                'cand_name',
                'cand_detail'
             ],
         }
```

## Author
  * Jerome Gaditano

## Acknowledgements
  * Thanks to *jyjoryi* for his [repo](https://github.com/jyjoryi/WQD7005_DataMining) on using scrapy. 
