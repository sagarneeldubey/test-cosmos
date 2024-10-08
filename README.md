### Summary

Simple Get API application that returns the meta-data as follows given the url from the data source: https://huggingface.co/datasets/AlekseyKorshuk/fiction-books

* url
* author
* title
* year
* genre
* summary


### Development

1. Install Docker Engine, if not already installed
https://docs.docker.com/engine/install/

2. Add the OpenAI API Key as below in `docker-compose.yml`

```sh
    environment:
      - OPENAI_API_KEY=your-api-key
```

2. Build the images and spin up the container:

```sh
$ docker-compose up -d --build
```

3. From bash or using Postman run the following command:

The parameter `url` should be changed to correct the url that needs to be looked for meta data extraction

```sh
$ curl --location 'http://localhost:2432/meta-data?url=https%3A%2F%2Fwww.bookrix.com%2F_ebook-m-b-julien-anthology-complex%2F'
```

4. A sample response for the above request is shown below. If the url is not found then `null` is returned.

```sh
{
    "url": "https://www.bookrix.com/_ebook-m-b-julien-anthology-complex/",
    "author": "M.B. Julien",
    "title": "Anthology Complex",
    "year": 2016,
    "genre": "nonfiction",
    "summary": "The text reflects on the nature of dreams and choices in life, illustrated through a dream about parked cars. The narrator muses on how dreams could represent alternate lives shaped by decisions not made. The dream features a man in a running car, symbolizing potential and reluctance to change. The author connects their own educational choices to the idea that a single decision can significantly alter one's life path, suggesting that dreams might reveal possible selves and highlight the impact of choices."
}
```

