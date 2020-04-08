# ScrapyDoo2020

*ScrappyDoo2020* is a project that retrieves data from 3 different sources (Excelsior, Milenio and 20minutos) through a *web-scrapper* based on *BeautifulSoup4* according to an input that the user provides in a particular way and then is stored in a *PostgreSQL* database. When the input is repetead the data is retrieved from database. It also makes use of *TFIDF* in order to get the excpeted results through *cosine_similarity*.

Flow Chart of the project:

![alt text](https://github.com/jhgutsol1290/flask-scrapper-postgres/flow_chart.jpg)

Example of the input:

```python
{
    "keywords": ["presidente", "coronavirus", ...]
}
```

Example of response:
```python
{
    [
        {
            "content": "El presidente de la Asociación de Bancos de México destaca que plan de reactivación económica ‘se queda corto' de car...",
            "rating": 0.9491237233647926,
            "reference": "https://www.excelsior.com.mx/nacional/plan-de-reactivacion-economica-se-queda-corto-nino-de-rivera/1374663",
            "title": "Plan de reactivación económica se queda corto: Niño de Rivera"
        },
        {
            "content": "Analistas atribuyeron el alza a un mejor ánimo de los inversores a señales de que el coronavirus estaría desacelerando su ritmo de propagación en algunas regiones.",
            "rating": 0.9430295204760669,
            "reference": "https://www.milenio.com/negocios/bmv-cierra-marginal-avance-martes-cemex-sube-6-94",
            "title": "Bolsa mexicana cierra con marginal avance; Cemex lidera alza y gana 6.94%"
        },
        {
            "content": "Trabajadores de la Secretaría de Cultura bloquearon Insurgentes y Reforma para exigir que el presidente Andrés Manuel López Obrador gire las instrucciones necesarias para que se les otorgue un...",
            "rating": 0.9447559744337686,
            "reference": "https://www.20minutos.com.mx/noticia/523120/0/empleados-de-secretaria-de-cultura-protestan-y-piden-incremento-salarial/",
            "title": "Empleados de Secretaría de Cultura protestan y piden incremento salarial"
        }
    ]
}
```

The response is composed by three objects and each contains relevant data from the sources.


- **Content** -> Description of the news found.
- **Reference** -> Link to the reference.
- **Rating** -> How much text from content is similar to input.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
Jhair Gutiérrez Solís - 2020