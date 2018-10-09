import scrapy


class NaiblogSpider(scrapy.Spider):
    name = 'naiblog'

    start_urls = [
        'http://blog.pynbo.or.ke/'
    ]

    def parse(self, response):
        # lets start by extracting the root node /html
        # from the response.
        html = response.xpath("/html")

        # select the body element which is inside
        # the root node html
        body = html.xpath("//body")

        # lets now get the content element
        content = body.xpath("//div[@class='content']")

        # extract the posts element
        posts = content.xpath("//div[@class='posts']")

        # iterate over the posts element in order to get
        # each individual post by extracting section node

        for post in posts.xpath("section[@class='post']"):

            # get the node header
            header = post.xpath("header[@class='post-header']")
            # finally get the title text
            title = header.xpath("h3 /a/text()").extract_first()

            # to get the description is the hardest part, if you inspect the element
            # of the page you will notice that there are two <p class='post-meta'> and there
            # is a <p> element without any attribute between them which holds a simple description
            # of the post. Basically it makes it hard to extract the description of the post.
            # I suggest the developers of the web app should look into it.
            # with that issue in mind I did some tweak below in order to get the empty <p>
            # tag.
            description = header.xpath("p[@class='post-meta']|p/text()").extract()[1]

            # extract post category
            category = header.xpath("p[@class='post-meta'] /a/text()").extract_first()

            # extract post date
            date = header.xpath("p[@class='post-meta'] /text()")[-1].extract()

            # finally lets return some data
            yield {
                  'description': description, 'category': category, 'title': title, 'date': date
            }

